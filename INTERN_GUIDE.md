# SkillTrack - Intern Implementation Guide

## 📚 Welcome to Your Internship Project!

This guide will help you understand, run, modify, and enhance the SkillTrack application.

---

## 🎯 Project Goals for This Internship

By completing this project, you will learn:

1. ✅ **Full-Stack Web Development** - Frontend + Backend integration
2. ✅ **Database Design** - SQLite data modeling
3. ✅ **RESTful APIs** - Creating HTTP endpoints
4. ✅ **HTML/CSS/JavaScript** - Frontend technologies
5. ✅ **Python & Flask** - Backend framework
6. ✅ **User Experience** - Building attractive UIs
7. ✅ **Project Management** - Planning and execution
8. ✅ **Code Quality** - Writing clean, maintainable code

---

## 📋 Week-by-Week Timeline

### **Week 1: Setup & Understanding**
- [ ] Install Python and dependencies
- [ ] Run application successfully
- [ ] Explore all pages and features
- [ ] Read README.md and code comments
- [ ] Add 10 sample associates
- [ ] Test search and filtering
- [ ] Understand database schema

**Deliverable**: Working app with sample data

### **Week 2: Core Features Deep-Dive**
- [ ] Study app.py structure
- [ ] Understand API endpoints
- [ ] Review HTML templates
- [ ] Study JavaScript functions
- [ ] Review CSS styling
- [ ] Add form validation
- [ ] Test edge cases

**Deliverable**: Feature documentation

### **Week 3: Enhancements**
- [ ] Add profile pictures (Phase 1)
- [ ] Implement bulk import feature
- [ ] Add sorting functionality
- [ ] Improve error handling
- [ ] Add keyboard shortcuts
- [ ] Optimize database queries
- [ ] Add inline help/documentation

**Deliverable**: Enhanced application

### **Week 4: Polish & Deploy**
- [ ] Fix bugs and issues
- [ ] Optimize performance
- [ ] Add remaining features
- [ ] Write comprehensive documentation
- [ ] Test on multiple browsers
- [ ] Deploy to cloud (Heroku/AWS)
- [ ] Create demo video

**Deliverable**: Production-ready application

---

## 🚀 Getting Started (Day 1)

### Step 1: Installation
```bash
# Navigate to project
cd c:\Users\isubramanya\Desktop\SkillTrack

# Install dependencies
pip install -r Requirements.py

# Run application
python app.py

# Should see:
# * Running on http://127.0.0.1:5000/
```

### Step 2: First Access
- Open browser → http://localhost:5000
- Click through all pages
- Add your first associate
- Test search functionality

### Step 3: Explore Code
- Open app.py in VS Code
- Read code comments
- Identify key functions
- Understand flow

### Step 4: Document Findings
Create a file `LEARNING_LOG.md`:
```markdown
# Learning Log - Week 1

## What I Learned
1. Flask basics
2. SQLite queries
3. HTML templates
4. Bootstrap usage

## Questions for Manager
1. How to add authentication?
2. How to deploy to cloud?

## Code I Studied
- app.py (main application)
- base.html (template structure)
- style.css (styling)
```

---

## 🛠️ Development Workflow

### Making Changes

#### Step 1: Create a Feature Branch (Git)
```bash
git checkout -b feature/add-profile-pictures
```

#### Step 2: Make Code Changes
```python
# Example: Add new route to app.py
@app.route("/api/upload-profile", methods=["POST"])
def upload_profile():
    """Upload profile picture for associate"""
    # Your code here
    pass
```

#### Step 3: Test Changes
```bash
# Run app
python app.py

# Test in browser
# Test with different data
# Check console for errors
```

#### Step 4: Commit Changes
```bash
git add .
git commit -m "feat: add profile picture upload functionality"
git push origin feature/add-profile-pictures
```

#### Step 5: Create Pull Request
- Go to GitHub
- Create PR with description
- Explain what changed and why

---

## 💻 Common Development Tasks

### Task 1: Add a New Field to Associate

**Step 1**: Update Database Schema
```python
# In app.py, modify init_db() function
cursor.execute("""
ALTER TABLE associates ADD COLUMN linkedin_profile TEXT;
""")
```

**Step 2**: Update Add Associate Form
```html
<!-- In add_associate.html -->
<div class="mb-3">
    <label for="linkedin" class="form-label">LinkedIn Profile</label>
    <input type="url" class="form-control" id="linkedin" name="linkedin">
</div>
```

**Step 3**: Update JavaScript
```javascript
// In add_associate.html JavaScript
const formData = {
    // ... existing fields
    linkedin_profile: document.getElementById('linkedin').value
};
```

**Step 4**: Update Backend
```python
# In api_add_associate() function
cursor.execute("""
INSERT INTO associates (..., linkedin_profile)
VALUES (..., ?)
""", (..., data.get("linkedin_profile")))
```

**Step 5**: Update Display
```html
<!-- In associates.html associate card -->
<p class="mb-1">
    <strong>LinkedIn:</strong> 
    <a href="{{ assoc.linkedin_profile }}" target="_blank">Profile</a>
</p>
```

---

### Task 2: Add Email Notification Feature

**Step 1**: Install Email Library
```bash
pip install python-dotenv
pip install secure-smtplib  # Optional
```

**Step 2**: Create Notification Function
```python
# In app.py
import smtplib
from email.mime.text import MIMEText

def send_certificate_alert(email, cert_name, days_left):
    """Send email alert for expiring certificate"""
    sender = "alerts@skilltrack.com"
    subject = f"Certificate Alert: {cert_name}"
    body = f"Your certificate expires in {days_left} days"
    
    # Email sending logic
    pass
```

**Step 3**: Call When Checking Expiry
```python
# In certificate_status() function
if expiry <= today + timedelta(days=30):
    send_certificate_alert(associate.email, cert_name, days_left)
    return "Expiring Soon"
```

---

### Task 3: Add Sorting to Associates List

**Step 1**: Update API Endpoint
```python
# In app.py
@app.route("/api/associates")
def api_get_associates():
    sort_by = request.args.get("sort_by", "name")  # name, role, experience
    order = request.args.get("order", "asc")       # asc, desc
    
    if sort_by == "experience":
        cursor.execute(f"SELECT * FROM associates ORDER BY experience {order}")
    elif sort_by == "role":
        cursor.execute(f"SELECT * FROM associates ORDER BY role {order}")
    else:  # name
        cursor.execute(f"SELECT * FROM associates ORDER BY name {order}")
    
    # Return results
```

**Step 2**: Add UI for Sorting
```html
<!-- In associates.html -->
<div class="sort-controls mb-3">
    <select id="sortBy" class="form-select w-auto">
        <option value="name">Sort by Name</option>
        <option value="role">Sort by Role</option>
        <option value="experience">Sort by Experience</option>
    </select>
    <select id="sortOrder" class="form-select w-auto">
        <option value="asc">Ascending</option>
        <option value="desc">Descending</option>
    </select>
</div>
```

**Step 3**: Add JavaScript
```javascript
document.getElementById('sortBy').addEventListener('change', loadAssociates);
document.getElementById('sortOrder').addEventListener('change', loadAssociates);

async function loadAssociates() {
    const sort = document.getElementById('sortBy').value;
    const order = document.getElementById('sortOrder').value;
    const response = await fetch(`/api/associates?sort_by=${sort}&order=${order}`);
    // Display results
}
```

---

## 🧪 Testing Checklist

Before submitting any changes:

- [ ] Application runs without errors
- [ ] All pages load correctly
- [ ] Forms submit successfully
- [ ] Search works as expected
- [ ] Data persists after refresh
- [ ] No console errors (F12 → Console)
- [ ] Responsive on mobile view
- [ ] Keyboard navigation works
- [ ] All links are active
- [ ] Database queries are efficient

### Quick Test Commands
```bash
# Check for Python syntax errors
python -m py_compile app.py

# Run application
python app.py

# Test in browser
# Open each page manually
# Try adding/editing/deleting
# Test search with various inputs
```

---

## 📚 Learning Resources

### Python & Flask
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python Official Docs](https://docs.python.org/3/)
- [Real Python Flask Tutorial](https://realpython.com/flask-by-example/)

### Frontend
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.3/)
- [MDN Web Docs](https://developer.mozilla.org/)
- [JavaScript.info](https://javascript.info/)

### Database
- [SQLite Tutorial](https://www.sqlite.org/docs.html)
- [SQL Basics](https://www.w3schools.com/sql/)

### Deployment
- [Heroku Deployment Guide](https://devcenter.heroku.com/)
- [AWS Deployment](https://aws.amazon.com/getting-started/)

---

## 🎓 Code Review Checklist

When reviewing code (yours or others):

- [ ] **Readability** - Is it easy to understand?
- [ ] **Naming** - Are variables/functions named clearly?
- [ ] **Comments** - Are complex sections explained?
- [ ] **DRY** - No code duplication?
- [ ] **Error Handling** - Edge cases covered?
- [ ] **Security** - Input validation done?
- [ ] **Performance** - Efficient queries?
- [ ] **Testing** - Does it work as expected?

---

## 🐛 Debugging Guide

### Browser Console (F12)
```javascript
// Check if variable exists
console.log(myVariable);

// Check API response
fetch('/api/associates').then(r => r.json()).then(console.log);

// Find errors
console.error("Error message");
```

### Python Debugging
```python
# Print for debugging
print(f"Associate: {associate}")

# Check variable type
print(type(variable))

# Check dictionary keys
print(data.keys())

# Flask debug mode (already enabled)
app.run(debug=True)
```

### Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| 404 Error | Route not found | Check URL spelling |
| 500 Error | Server error | Check app.py console |
| Form not submitting | JavaScript error | Check browser console |
| Database locked | Concurrent access | Close other connections |
| No data showing | Database empty | Add sample data |

---

## 📝 Documentation Standards

When writing code, follow this format:

```python
def calculate_age(birth_date):
    """
    Calculate age from birth date.
    
    Args:
        birth_date (str): Date in format YYYY-MM-DD
        
    Returns:
        int: Age in years
        
    Raises:
        ValueError: If date format is invalid
        
    Example:
        >>> calculate_age("2000-01-15")
        23
    """
    # Implementation
    pass
```

---

## 🚀 Deployment Preparation

### Pre-Deployment Checklist
- [ ] All features working locally
- [ ] Tests passing
- [ ] No console errors
- [ ] Database backups created
- [ ] Environment variables configured
- [ ] Security settings enabled
- [ ] Performance optimized
- [ ] Documentation complete
- [ ] README updated
- [ ] Deployment plan documented

### Deploy to Heroku
```bash
# Install Heroku CLI
# Create Procfile
echo "web: python app.py" > Procfile

# Create requirements.txt
pip freeze > requirements.txt

# Deploy
heroku create skilltrack-demo
git push heroku main
```

---

## 💡 Best Practices

### 1. Commit Messages
```bash
# ✅ GOOD
git commit -m "feat: add profile picture upload"
git commit -m "fix: correct certificate expiry calculation"
git commit -m "docs: update README with deployment steps"

# ❌ BAD
git commit -m "stuff"
git commit -m "fixed things"
git commit -m "updates"
```

### 2. Code Comments
```python
# ✅ GOOD
# Filter associates by department before querying database
query = f"SELECT * FROM associates WHERE department = '{dept_id}'"

# ❌ BAD
# Get associates
query = "SELECT * FROM associates WHERE department = " + str(dept_id)
```

### 3. Function Naming
```python
# ✅ GOOD NAMES
def get_active_associates()
def calculate_certificate_expiry_days()
def send_expiry_notification()

# ❌ BAD NAMES
def get_stuff()
def calc()
def send()
```

---

## 🎯 Success Criteria

Your internship will be successful when you can:

1. ✅ Explain all features of the application
2. ✅ Add new features independently
3. ✅ Debug and fix issues
4. ✅ Write clean, documented code
5. ✅ Deploy application to production
6. ✅ Teach another person how to use it
7. ✅ Suggest improvements and enhancements
8. ✅ Handle edge cases and errors gracefully

---

## 📞 Getting Help

### Resources in Order:
1. Check existing code comments
2. Read the documentation files
3. Search Stack Overflow
4. Check official documentation
5. Ask your manager/mentor
6. Use ChatGPT (but try first!)

### Questions to Ask Manager:
- "How does [feature] work?"
- "Why did you design it this way?"
- "What's the priority for next features?"
- "Can I refactor [code section]?"
- "Is there a specific pattern you prefer?"

---

## 🎉 Final Notes

This project is your foundation in web development. Take it seriously, ask questions, and don't be afraid to make mistakes - they're learning opportunities!

**Key Mindsets:**
- 🤔 Be curious - understand the *why*, not just the *what*
- 🎯 Be focused - complete features fully before moving on
- 📚 Be learning-oriented - read documentation and code
- 🤝 Be collaborative - discuss with your manager
- ⚡ Be proactive - suggest improvements

---

## 📅 Submission Checklist

When ready to submit:

- [ ] Application runs without errors
- [ ] All CRUD operations working
- [ ] Search and filtering functional
- [ ] UI is attractive and responsive
- [ ] Code is clean and documented
- [ ] README updated with features
- [ ] Test data added
- [ ] Deployment successful
- [ ] Demo prepared
- [ ] Improvements documented

---

**Good luck with your internship! You've got this! 🚀**

---

### Questions?
- Email: [Manager Email]
- Slack: #skilltrack-project
- Office Hours: [Time]

**Happy Coding!** 💻✨
