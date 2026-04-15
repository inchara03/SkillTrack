from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import sqlite3
from datetime import datetime, timedelta
import os
from functools import wraps
import hashlib

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = "skilltrack_secret_key"

MANAGER_ACCESS_CODE = "MANAGER@123"

# ---------- LOGIN REQUIRED DECORATORS ----------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("manager_logged_in"):
            return redirect("/manager/login")
        return f(*args, **kwargs)
    return decorated_function

def user_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_logged_in"):
            return redirect("/user/login")
        return f(*args, **kwargs)
    return decorated_function


# ---------- DATABASE CONNECTION ----------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------- INITIALIZE DATABASE ----------
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS associates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        phone TEXT,
        role TEXT,
        skills TEXT,
        experience INTEGER,
        department TEXT,
        profile_picture TEXT,
        date_joined TEXT,
        status TEXT DEFAULT 'Active',
        project_status TEXT,
        project_name TEXT
    )
    """)

    # Add missing columns if they don't exist
    cursor.execute("PRAGMA table_info(associates)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'project_status' not in columns:
        cursor.execute("ALTER TABLE associates ADD COLUMN project_status TEXT")
    if 'project_name' not in columns:
        cursor.execute("ALTER TABLE associates ADD COLUMN project_name TEXT")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS certificates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        associate_id INTEGER,
        certificate_name TEXT NOT NULL,
        issue_date TEXT,
        expiry_date TEXT,
        issuing_organization TEXT,
        certificate_url TEXT,
        FOREIGN KEY (associate_id) REFERENCES associates(id) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skills_master (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        skill_name TEXT UNIQUE,
        category TEXT,
        proficiency_level TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        phone TEXT,
        skills TEXT,
        experience INTEGER,
        education TEXT,
        date_registered TEXT,
        status TEXT DEFAULT 'Active',
        project_status TEXT,
        project_name TEXT
    )
    """)

    # Add missing columns if they don't exist
    cursor.execute("PRAGMA table_info(users)")
    user_columns = [column[1] for column in cursor.fetchall()]
    
    if 'project_status' not in user_columns:
        cursor.execute("ALTER TABLE users ADD COLUMN project_status TEXT")
    if 'project_name' not in user_columns:
        cursor.execute("ALTER TABLE users ADD COLUMN project_name TEXT")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_openings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        department TEXT,
        description TEXT,
        required_skills TEXT,
        experience_required INTEGER,
        status TEXT DEFAULT 'Open',
        posted_date TEXT,
        closing_date TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------- CERTIFICATE STATUS ----------
def certificate_status(expiry_date):
    if not expiry_date:
        return "No Expiry"
    try:
        today = datetime.today().date()
        expiry = datetime.strptime(expiry_date, "%Y-%m-%d").date()

        if expiry < today:
            return "Expired"
        elif expiry <= today + timedelta(days=30):
            return "Expiring Soon"
        else:
            return "Active"
    except:
        return "Invalid Date"

# ---------- HOME PAGE (LOGIN CHOICE) ----------
@app.route("/")
def home():
    # Always show login choice page
    return render_template("login_choice.html")

# ---------- USER LOGIN ----------
@app.route("/user/login", methods=["GET", "POST"])
def user_login():
    if request.method == "POST":
        # Handle both form and JSON data
        if request.is_json:
            data = request.json
            email = data.get("email")
            password = data.get("password")
            is_json = True
        else:
            email = request.form.get("email")
            password = request.form.get("password")
            is_json = False
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            # Simple password hash comparison
            stored_hash = user["password"]
            input_hash = hashlib.sha256(password.encode()).hexdigest()
            
            if stored_hash == input_hash:
                session["user_logged_in"] = True
                session["user_id"] = user["id"]
                session["user_name"] = user["name"]
                session["user_email"] = user["email"]
                
                if is_json:
                    return jsonify({"message": "Login successful"}), 200
                else:
                    return redirect("/user/dashboard")
        
        if is_json:
            return jsonify({"error": "Invalid email or password"}), 401
        else:
            return render_template("user_login.html", error="Invalid email or password")
    
    return render_template("user_login.html")

# ---------- USER REGISTER ----------
@app.route("/user/register", methods=["GET", "POST"])
def user_register():
    if request.method == "POST":
        # Handle both form and JSON data
        if request.is_json:
            data = request.json
            name = data.get("name")
            email = data.get("email")
            password = data.get("password")
            phone = data.get("phone", "")
            is_json = True
        else:
            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")
            phone = request.form.get("phone", "")
            is_json = False
        
        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO users (name, email, password, phone, date_registered, status)
            VALUES (?, ?, ?, ?, ?, 'Active')
            """, (name, email, password_hash, phone, datetime.now().strftime("%Y-%m-%d")))
            conn.commit()
            conn.close()
            
            if is_json:
                return jsonify({"message": "Registration successful!"}), 201
            else:
                return render_template("user_register.html", success="Registration successful! Please login.")
        except sqlite3.IntegrityError:
            if is_json:
                return jsonify({"error": "Email already registered"}), 400
            else:
                return render_template("user_register.html", error="Email already registered")
        except Exception as e:
            if is_json:
                return jsonify({"error": str(e)}), 400
            else:
                return render_template("user_register.html", error=str(e))
    
    return render_template("user_register.html")

# ---------- USER LOGOUT ----------
@app.route("/user/logout")
def user_logout():
    session.clear()
    return redirect("/")

# ---------- USER DASHBOARD ----------
@app.route("/user/dashboard")
@user_login_required
def user_dashboard():
    conn = get_db()
    cursor = conn.cursor()
    
    # Get user's associate record
    cursor.execute("SELECT * FROM associates WHERE email = ?", (session.get("user_email"),))
    user_associate = cursor.fetchone()
    
    conn.close()
    
    return render_template("user_dashboard.html", user_associate=user_associate, project_info=user_associate)

# ---------- GET OPEN POSITIONS (API) ----------
@app.route("/api/open_positions")
def api_open_positions():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM job_openings WHERE status = 'Open' ORDER BY posted_date DESC")
    positions = cursor.fetchall()
    conn.close()
    
    result = []
    for pos in positions:
        result.append({
            "id": pos["id"],
            "title": pos["title"],
            "department": pos["department"],
            "description": pos["description"],
            "required_skills": pos["required_skills"],
            "experience_required": pos["experience_required"],
            "posted_date": pos["posted_date"],
            "closing_date": pos["closing_date"]
        })
    
    return jsonify(result)

# ---------- DASHBOARD ----------
@app.route("/dashboard")
@login_required
def dashboard_page():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM associates")
    total_associates = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM associates WHERE status = 'Active'")
    active_associates = cursor.fetchone()[0]

    cursor.execute("SELECT expiry_date FROM certificates")
    certs = cursor.fetchall()

    active = expired = expiring = 0
    for c in certs:
        status = certificate_status(c["expiry_date"])
        if status == "Active":
            active += 1
        elif status == "Expired":
            expired += 1
        elif status == "Expiring Soon":
            expiring += 1

    stats = {
        "total_associates": total_associates,
        "active_associates": active_associates,
        "active_certificates": active,
        "expiring_soon": expiring,
        "expired_certificates": expired
    }

    conn.close()
    return render_template("manager_dashboard.html", stats=stats)

# ---------- GET DASHBOARD DATA (API) ----------
@app.route("/api/dashboard")
def api_dashboard():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM associates")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT expiry_date FROM certificates")
    certs = cursor.fetchall()

    active = expired = expiring = 0
    for c in certs:
        status = certificate_status(c["expiry_date"])
        if status == "Active":
            active += 1
        elif status == "Expired":
            expired += 1
        else:
            expiring += 1

    conn.close()
    return jsonify({
        "total_associates": total,
        "active_certificates": active,
        "expiring_soon": expiring,
        "expired_certificates": expired
    })

# ---------- ADD ASSOCIATE PAGE ----------
@app.route("/add_associate")
@user_login_required
def add_associate_page():
    return render_template("add_associate.html")

# ---------- ADD ASSOCIATE (API) ----------
@app.route("/api/add_associate", methods=["POST"])
def api_add_associate():
    try:
        data = request.json
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO associates (name, email, phone, role, skills, experience, department, date_joined, status, project_status, project_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Active', ?, ?)
        """, (
            data.get("name"),
            data.get("email"),
            data.get("phone"),
            data.get("role"),
            data.get("skills"),
            data.get("experience"),
            data.get("department"),
            datetime.now().strftime("%Y-%m-%d"),
            data.get("project_status", "Not Assigned"),
            data.get("project_name", "")
        ))

        associate_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return jsonify({"message": "Associate added successfully", "id": associate_id}), 201
    except Exception as e:
        error_msg = str(e)
        # Provide specific error message for duplicate email
        if "UNIQUE constraint failed: associates.email" in error_msg or "unique" in error_msg.lower():
            return jsonify({"error": "This email address is already registered. Please use a different email."}), 400
        return jsonify({"error": error_msg}), 400

# ---------- VIEW ALL ASSOCIATES ----------
@app.route("/associates")
@login_required
def associates_page():
    return render_template("associates.html")

# ---------- GET ALL ASSOCIATES (API) ----------
@app.route("/api/associates")
def api_get_associates():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM associates ORDER BY name")
    associates = cursor.fetchall()
    
    result = []
    for a in associates:
        cert_cursor = conn.cursor()
        cert_cursor.execute("SELECT * FROM certificates WHERE associate_id = ?", (a["id"],))
        certs = cert_cursor.fetchall()
        
        cert_list = []
        for c in certs:
            cert_list.append({
                "id": c["id"],
                "name": c["certificate_name"],
                "issuing_org": c["issuing_organization"],
                "expiry_date": c["expiry_date"],
                "status": certificate_status(c["expiry_date"])
            })
        
        result.append({
            "id": a["id"],
            "name": a["name"],
            "email": a["email"],
            "phone": a["phone"],
            "role": a["role"],
            "skills": a["skills"],
            "experience": a["experience"],
            "department": a["department"],
            "status": a["status"],
            "project_status": a["project_status"],
            "project_name": a["project_name"],
            "certificates": cert_list
        })
    
    conn.close()
    return jsonify(result)

# ---------- SEARCH BY SKILL, ROLE, or NAME ----------
@app.route("/api/search")
def api_search():
    query = request.args.get("q", "").lower()
    search_type = request.args.get("type", "all")  # all, skill, role, name

    conn = get_db()
    cursor = conn.cursor()

    if search_type == "skill" or search_type == "all":
        cursor.execute("SELECT * FROM associates WHERE skills LIKE ? ORDER BY name", (f"%{query}%",))
    elif search_type == "role":
        cursor.execute("SELECT * FROM associates WHERE role LIKE ? ORDER BY name", (f"%{query}%",))
    elif search_type == "name":
        cursor.execute("SELECT * FROM associates WHERE name LIKE ? ORDER BY name", (f"%{query}%",))
    else:
        cursor.execute("SELECT * FROM associates WHERE skills LIKE ? OR role LIKE ? OR name LIKE ? ORDER BY name", 
                      (f"%{query}%", f"%{query}%", f"%{query}%"))

    associates = cursor.fetchall()

    results = []
    for a in associates:
        cursor.execute("SELECT * FROM certificates WHERE associate_id = ?", (a["id"],))
        certs = cursor.fetchall()

        cert_list = []
        for c in certs:
            cert_list.append({
                "certificate": c["certificate_name"],
                "expiry_date": c["expiry_date"],
                "status": certificate_status(c["expiry_date"])
            })

        results.append({
            "id": a["id"],
            "name": a["name"],
            "email": a["email"],
            "role": a["role"],
            "skills": a["skills"],
            "experience": a["experience"],
            "department": a["department"],
            "certificates": cert_list
        })

    conn.close()
    return jsonify(results)

# ---------- GET ASSOCIATE DETAILS ----------
@app.route("/api/associate/<int:associate_id>")
def api_get_associate(associate_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM associates WHERE id = ?", (associate_id,))
    associate = cursor.fetchone()

    if not associate:
        return jsonify({"error": "Associate not found"}), 404

    cursor.execute("SELECT * FROM certificates WHERE associate_id = ?", (associate_id,))
    certs = cursor.fetchall()

    cert_list = []
    for c in certs:
        cert_list.append({
            "id": c["id"],
            "name": c["certificate_name"],
            "issuing_org": c["issuing_organization"],
            "issue_date": c["issue_date"],
            "expiry_date": c["expiry_date"],
            "status": certificate_status(c["expiry_date"])
        })

    conn.close()
    return jsonify({
        "id": associate["id"],
        "name": associate["name"],
        "email": associate["email"],
        "phone": associate["phone"],
        "role": associate["role"],
        "skills": associate["skills"],
        "experience": associate["experience"],
        "department": associate["department"],
        "status": associate["status"],
        "date_joined": associate["date_joined"],
        "project_status": associate["project_status"],
        "project_name": associate["project_name"],
        "certificates": cert_list
    })

# ---------- UPDATE ASSOCIATE ----------
@app.route("/api/associate/<int:associate_id>", methods=["PUT"])
def api_update_associate(associate_id):
    try:
        data = request.json
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE associates 
        SET name = ?, email = ?, phone = ?, role = ?, skills = ?, experience = ?, department = ?, status = ?
        WHERE id = ?
        """, (
            data.get("name"),
            data.get("email"),
            data.get("phone"),
            data.get("role"),
            data.get("skills"),
            data.get("experience"),
            data.get("department"),
            data.get("status", "Active"),
            associate_id
        ))

        conn.commit()
        conn.close()
        return jsonify({"message": "Associate updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ---------- DELETE ASSOCIATE ----------
@app.route("/api/associate/<int:associate_id>", methods=["DELETE"])
def api_delete_associate(associate_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM associates WHERE id = ?", (associate_id,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Associate deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ---------- UPDATE PROJECT ASSIGNMENT (Manager Only) ----------
@app.route("/api/update-project-assignment/<int:associate_id>", methods=["PUT"])
@login_required
def api_update_project_assignment(associate_id):
    try:
        data = request.json
        conn = get_db()
        cursor = conn.cursor()

        # Update only project status and project name
        cursor.execute("""
        UPDATE associates 
        SET project_status = ?, project_name = ?
        WHERE id = ?
        """, (
            data.get("project_status", "Not Assigned"),
            data.get("project_name", ""),
            associate_id
        ))

        conn.commit()
        conn.close()
        return jsonify({"message": "Project assignment updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ---------- ADD CERTIFICATE ----------
@app.route("/api/add_certificate", methods=["POST"])
def api_add_certificate():
    try:
        data = request.json
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO certificates (associate_id, certificate_name, issue_date, expiry_date, issuing_organization, certificate_url)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data.get("associate_id"),
            data.get("certificate_name"),
            data.get("issue_date"),
            data.get("expiry_date"),
            data.get("issuing_organization"),
            data.get("certificate_url")
        ))

        cert_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return jsonify({"message": "Certificate added successfully", "id": cert_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ---------- DELETE CERTIFICATE ----------
@app.route("/api/certificate/<int:cert_id>", methods=["DELETE"])
def api_delete_certificate(cert_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM certificates WHERE id = ?", (cert_id,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Certificate deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ---------- GET EXPIRING CERTIFICATES ----------
@app.route("/api/expiring_certificates")
def api_expiring_certificates():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT a.id, a.name, c.id as cert_id, c.certificate_name, c.expiry_date 
    FROM associates a 
    JOIN certificates c ON a.id = c.associate_id 
    WHERE c.expiry_date IS NOT NULL
    ORDER BY c.expiry_date ASC
    """)

    certs = cursor.fetchall()
    result = []

    for c in certs:
        status = certificate_status(c["expiry_date"])
        if status in ["Expiring Soon", "Expired"]:
            result.append({
                "associate_id": c["id"],
                "associate_name": c["name"],
                "certificate_name": c["certificate_name"],
                "expiry_date": c["expiry_date"],
                "status": status
            })

    conn.close()
    return jsonify(result)

@app.route("/manager/login", methods=["GET", "POST"])
def manager_login():
    if request.method == "POST":
        # Handle both form and JSON data
        if request.is_json:
            data = request.json
            code = data.get("access_code")
            is_json = True
        else:
            code = request.form.get("access_code")
            is_json = False

        if code == MANAGER_ACCESS_CODE:
            session["manager_logged_in"] = True
            if is_json:
                return jsonify({"message": "Login successful"}), 200
            else:
                return redirect("/manager/dashboard")
        else:
            if is_json:
                return jsonify({"error": "Invalid Access Code"}), 401
            else:
                return render_template("manager_login.html", error="Invalid Access Code")

    return render_template("manager_login.html")

@app.route("/manager/logout")
def manager_logout():
    session.clear()
    return redirect("/")

@app.route("/manager/dashboard")
def manager_dashboard():
    return dashboard_page()

@app.route("/manager/associates")
def manager_associates():
    return associates_page()

@app.before_request
def protect_routes():
    # Protect manager routes
    if request.path.startswith("/manager"):
        # Allow access to login page
        if request.path == "/manager/login":
            return
        if not session.get("manager_logged_in"):
            return redirect("/manager/login")
    
    # Protect user routes
    if request.path.startswith("/user"):
        # Allow access to login and register pages
        if request.path in ["/user/login", "/user/register"]:
            return
        if not session.get("user_logged_in"):
            return redirect("/user/login")
    
    # Protect API endpoints (require manager or user login)
    if request.path.startswith("/api"):
        if request.path == "/api/open_positions":
            return  # Allow public access to job positions
        
        # Allow certificate operations for both managers and users
        if request.path.startswith("/api/add_certificate") or request.path.startswith("/api/certificate"):
            if session.get("manager_logged_in") or session.get("user_logged_in"):
                return
            return jsonify({"error": "Unauthorized"}), 401
        
        # Other API endpoints require manager login
        if not session.get("manager_logged_in"):
            return jsonify({"error": "Unauthorized"}), 401

# ---------- USER EDIT PROFILE ----------
@app.route("/user/edit-profile", methods=["GET", "POST"])
@user_login_required
def user_edit_profile():
    if request.method == "POST":
        conn = get_db()
        cursor = conn.cursor()
        
        name = request.form.get("name")
        phone = request.form.get("phone")
        
        cursor.execute("""
        UPDATE users SET name = ?, phone = ? WHERE id = ?
        """, (name, phone, session.get("user_id")))
        
        conn.commit()
        conn.close()
        
        session["user_name"] = name
        return redirect("/user/edit-profile")
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (session.get("user_id"),))
    user = cursor.fetchone()
    conn.close()
    
    return render_template("user_edit_profile.html", user=user)

# ---------- USER ADD ASSOCIATE (Add Own Details) ----------
@app.route("/user/add-associate", methods=["GET", "POST"])
@user_login_required
def user_add_associate():
    if request.method == "POST":
        try:
            data = request.json
            conn = get_db()
            cursor = conn.cursor()

            user_email = session.get("user_email")

            # Check if user details already exist
            cursor.execute("SELECT id FROM associates WHERE email = ?", (user_email,))
            existing = cursor.fetchone()

            if existing:
                # Update existing record
                cursor.execute("""
                UPDATE associates 
                SET phone = ?, role = ?, skills = ?, experience = ?, department = ?, 
                    project_status = ?, project_name = ?
                WHERE email = ?
                """, (
                    data.get("phone"),
                    data.get("role"),
                    data.get("skills"),
                    data.get("experience"),
                    data.get("department"),
                    data.get("project_status", "Not Assigned"),
                    data.get("project_name", ""),
                    user_email
                ))
                conn.commit()
                conn.close()
                return jsonify({"message": "Your details have been updated successfully", "associate_id": existing["id"]}), 200
            else:
                # Insert new record
                cursor.execute("""
                INSERT INTO associates (name, email, phone, role, skills, experience, department, date_joined, status, project_status, project_name)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Active', ?, ?)
                """, (
                    session.get("user_name"),
                    user_email,
                    data.get("phone"),
                    data.get("role"),
                    data.get("skills"),
                    data.get("experience"),
                    data.get("department"),
                    datetime.now().strftime("%Y-%m-%d"),
                    data.get("project_status", "Not Assigned"),
                    data.get("project_name", "")
                ))

                associate_id = cursor.lastrowid
                conn.commit()
                conn.close()

                return jsonify({"message": "Your details added successfully", "associate_id": associate_id}), 201
        except Exception as e:
            error_msg = str(e)
            return jsonify({"error": error_msg}), 400

    return render_template("user_add_associate.html")


# ---------- RUN SERVER ----------
if __name__ == "__main__":
    # Create templates folder if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    if not os.path.exists('static'):
        os.makedirs('static')
    
    app.run(debug=True, host='0.0.0.0', port=5000)
