# SkillTrack - Associate Skills & Certification Management System

A modern, feature-rich web application for managing associate profiles, skills, and certifications. Built with Flask, SQLite, Bootstrap 5, and Chart.js.

## 🎯 Project Overview

SkillTrack is designed to help organizations efficiently manage their workforce by tracking:
- Associate profiles and contact information
- Skills and competencies
- Professional certifications with expiry tracking
- Certificate status (Active, Expiring Soon, Expired)
- Advanced search and filtering capabilities

---

## ⚙️ System Requirements

- **Python**: 3.7+
- **Flask**: 2.3.0
- **SQLite**: Built-in with Python
- **Browser**: Modern browser (Chrome, Firefox, Edge, Safari)
- **RAM**: 512MB minimum
- **Storage**: 100MB minimum

---

## 📦 Installation & Setup

### Step 1: Clone or Download Project
```bash
cd SkillTrack
```

### Step 2: Install Dependencies
```bash
pip install -r Requirements.py
```

Or manually install:
```bash
pip install Flask==2.3.0
pip install Werkzeug==2.3.0
```

### Step 3: Run the Application
```bash
python app.py
```

### Step 4: Access Application
Open your browser and navigate to:
```
http://localhost:5000
```

---

## 📋 Database Schema

### Associates Table
```sql
CREATE TABLE associates (
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
    status TEXT DEFAULT 'Active'
)
```

### Certificates Table
```sql
CREATE TABLE certificates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    associate_id INTEGER,
    certificate_name TEXT NOT NULL,
    issue_date TEXT,
    expiry_date TEXT,
    issuing_organization TEXT,
    certificate_url TEXT,
    FOREIGN KEY (associate_id) REFERENCES associates(id) ON DELETE CASCADE
)
```

### Skills Master Table (Future Enhancement)
```sql
CREATE TABLE skills_master (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_name TEXT UNIQUE,
    category TEXT,
    proficiency_level TEXT
)
```

---

## 🚀 Features

### 1. **Dashboard Analytics**
   - Total associates count
   - Active associates tracking
   - Active/Expiring/Expired certificate metrics
   - Visual charts using Chart.js
   - Certificate expiry alerts

### 2. **Associate Management**
   - ✅ Add new associates with detailed profiles
   - ✅ View all associates with complete information
   - ✅ Edit associate details
   - ✅ Delete associates (with cascade delete of certificates)
   - ✅ Track personal info (Email, Phone, Department)
   - ✅ Experience level tracking

### 3. **Advanced Search**
   - 🔍 Search by associate name
   - 🔍 Search by skills
   - 🔍 Search by role/position
   - 🔍 Search by department
   - 🔍 Filter by search type
   - Real-time search results

### 4. **Certificate Management**
   - ➕ Add certificates to associates
   - 📅 Track issue and expiry dates
   - 📊 Certificate status tracking:
     - **Active**: Valid for more than 30 days
     - **Expiring Soon**: Expiring within 30 days
     - **Expired**: Past expiry date
   - 🔔 Automatic expiry alerts
   - 🗑️ Delete certificates

### 5. **Smart Notifications**
   - Certificate expiry alerts (30-day warning)
   - Auto-updated dashboard
   - Real-time status indicators

### 6. **User Interface**
   - Modern, responsive design
   - Mobile-friendly layout
   - Intuitive navigation
   - Beautiful gradient backgrounds
   - Smooth animations and transitions
   - Professional color scheme

---

## 🎨 Attractive Features for Enhancement

### Phase 2 Features (Future):

1. **Profile Pictures**
   - Upload profile photos
   - Gallery view
   - Photo validation

2. **Reports & Export**
   - Export associates to CSV/PDF
   - Generate certification reports
   - Skill matrix reports
   - Expiry date reports

3. **Authentication & Roles**
   - User login system
   - Role-based access control
   - Admin dashboard
   - Permission levels

4. **Advanced Analytics**
   - Skill distribution charts
   - Department-wise breakdown
   - Certification by issuing organization
   - Experience level distribution
   - Trend analysis over time

5. **Notifications System**
   - Email alerts for expiring certs
   - SMS notifications
   - In-app notifications
   - Scheduled reminders

6. **Integrations**
   - Calendar integration
   - Email integration
   - Slack notifications
   - Google Drive backup

7. **Bulk Operations**
   - Bulk import associates from CSV
   - Bulk certificate upload
   - Batch update operations

8. **Advanced Filtering**
   - Multi-criteria filtering
   - Save filter preferences
   - Custom filter creation
   - Smart filters

9. **Performance Metrics**
   - Associate productivity scores
   - Skill maturity levels
   - Certification completion rates
   - Team skill coverage

10. **Mobile App**
    - Native mobile application
    - Offline functionality
    - Push notifications

---

## 📱 API Endpoints

### Associates
- `GET /` - Home page
- `GET /dashboard` - Dashboard page
- `GET /associates` - View all associates
- `GET /add_associate` - Add new associate form

### API Routes
```
GET  /api/dashboard                      - Get dashboard stats
GET  /api/associates                      - Get all associates
GET  /api/associate/<id>                  - Get specific associate
POST /api/add_associate                   - Add new associate
PUT  /api/associate/<id>                  - Update associate
DELETE /api/associate/<id>                - Delete associate

GET  /api/search?q=<query>&type=<type>   - Search associates
GET  /api/expiring_certificates           - Get expiring certificates

POST /api/add_certificate                 - Add certificate
DELETE /api/certificate/<id>              - Delete certificate
```

---

## 🔄 Workflow Example

### Adding an Associate:
1. Navigate to "Add Associate" → Fill form → Submit
2. Associate record created in database
3. Receive confirmation with Associate ID

### Adding a Certificate:
1. View Associates → Click "Add Cert" button
2. Enter certificate details
3. System auto-calculates expiry status

### Searching:
1. Use search bar on Associates page
2. Select search type (Name, Skill, Role, All)
3. View filtered results instantly

### Monitoring Expiry:
1. Dashboard shows expiring certificates
2. Red alert box lists all certificates needing attention
3. Click on associate to view and manage

---

## 📊 Dashboard Metrics Explained

| Metric | Description |
|--------|-------------|
| **Total Associates** | Complete count of all associates in system |
| **Active Associates** | Associates with "Active" status |
| **Active Certificates** | Valid certificates (>30 days to expiry) |
| **Expiring Soon** | Certificates expiring within 30 days |
| **Expired** | Certificates past expiry date |

---

## 🛠️ Technical Stack

### Backend
- **Framework**: Flask 2.3.0
- **Database**: SQLite3
- **Language**: Python 3.7+

### Frontend
- **UI Framework**: Bootstrap 5.3.0
- **CSS**: Custom CSS3
- **JavaScript**: Vanilla JS + Axios
- **Charts**: Chart.js
- **Icons**: Font Awesome 6.4.0

### Tools & Libraries
- Jinja2 (Template Engine)
- JSON (Data Format)

---

## 🔐 Security Considerations

### Current Implementation:
- SQL Injection prevention (Parameterized queries)
- CSRF protection ready (can be enabled)
- Input validation
- Error handling

### Future Enhancements:
- Add authentication system
- Implement role-based access control
- Add data encryption
- Regular security audits
- HTTPS enforcement

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Database Lock Error
```bash
# Delete database.db and restart
rm database.db
python app.py
```

### Templates Not Found
- Ensure `templates/` folder exists
- Check all HTML files are in correct location

### Module Not Found
```bash
pip install --upgrade -r Requirements.py
```

---

## 📝 File Structure

```
SkillTrack/
├── app.py                          # Main Flask application
├── database.db                     # SQLite database (auto-created)
├── Requirements.py                 # Python dependencies
├── templates/
│   ├── base.html                   # Base template with navbar
│   ├── index.html                  # Home page
│   ├── dashboard.html              # Analytics dashboard
│   ├── add_associate.html          # Add associate form
│   └── associates.html             # View/manage associates
├── static/
│   ├── style.css                   # Custom styles
│   └── script.js                   # Utility functions
└── README.md                       # This file
```

---

## 🎓 Learning Objectives

As an intern, this project teaches:
- ✅ Full-stack web development
- ✅ Database design and SQL
- ✅ RESTful API design
- ✅ Frontend frameworks (Bootstrap, Charts)
- ✅ JavaScript async operations
- ✅ MVC architecture
- ✅ Form handling and validation
- ✅ Version control (Git)

---

## 🚀 Deployment Options

### Local Deployment
```bash
python app.py
```

### Heroku Deployment
1. Create `Procfile`: `web: python app.py`
2. Add `heroku/python` buildpack
3. Push to Heroku

### Docker Deployment
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r Requirements.py
CMD ["python", "app.py"]
```

### AWS/Google Cloud
- Use App Engine or Compute Engine
- Configure environment variables
- Set up cloud database

---

## 📞 Support & Contact

For questions or issues:
- Check troubleshooting section
- Review Flask documentation: https://flask.palletsprojects.com/
- Check Bootstrap docs: https://getbootstrap.com/docs/5.3/

---

## 📄 License

This project is created for educational purposes. Feel free to use and modify as needed.

---

## 🎉 Conclusion

SkillTrack provides a solid foundation for workforce management. With the features outlined and future enhancements, it can become a comprehensive enterprise solution.

**Happy Coding!** 🚀
