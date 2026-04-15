# SkillTrack - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. **Install & Run**
```bash
cd SkillTrack
pip install -r Requirements.py
python app.py
```

**Output**: `Running on http://127.0.0.1:5000/`

### 2. **Access Application**
Open browser → `http://localhost:5000`

---

## 📌 Main Features at a Glance

| Feature | How to Use | Location |
|---------|-----------|----------|
| **View Dashboard** | Click "Dashboard" in navbar | Real-time stats & analytics |
| **Add Associate** | Fill form → Submit | /add_associate |
| **View All Associates** | Click "Associates" | View profiles & certificates |
| **Search Associates** | Enter query in search bar | Smart filtering |
| **Add Certificate** | Click "Add Cert" on associate card | Manage certifications |
| **Edit Associate** | Click "Edit" on associate card | Update profile |
| **Delete Associate** | Click "Delete" on associate card | Remove record |

---

## 💡 Example Workflow

### Adding Your First Associate:

1. **Click** → "Add Associate"
2. **Fill**:
   - Name: John Doe
   - Email: john@company.com
   - Role: Software Developer
   - Department: Engineering
   - Experience: 3 years
   - Skills: Python, JavaScript, AWS, Docker
3. **Click** → "Add Associate"
4. **See** → Success message with Associate ID

### Adding a Certificate:

1. **Go** → "Associates"
2. **Click** → "Add Cert" button on associate card
3. **Fill**:
   - Certificate: AWS Solutions Architect
   - Issue Date: 2023-01-15
   - Expiry Date: 2025-01-15
   - Organization: Amazon Web Services
4. **Click** → "Add Certificate"
5. **See** → Certificate added to profile

### Searching:

1. **Go** → "Associates"
2. **Type** → "Python" in search bar
3. **Select** → "Skills" from filter
4. **Click** → "Search"
5. **See** → All associates with Python skill

---

## 📊 Dashboard Understanding

| Indicator | Color | Meaning |
|-----------|-------|---------|
| Active Certificates | 🟢 Green | Valid for >30 days |
| Expiring Soon | 🟡 Yellow | Expiring within 30 days |
| Expired | 🔴 Red | Already expired |
| Attention Required | Red Alert Box | Take action needed |

---

## 🔍 Smart Search Tips

```
Search Type: All Fields
Query: "python"
Result: Associates with Python in name, skill, or role

Search Type: Skills
Query: "aws"
Result: Only associates with AWS in their skills

Search Type: Role
Query: "developer"
Result: Only associates with Developer in their role

Search Type: Name
Query: "john"
Result: Only associates with John in their name
```

---

## 🎨 UI Elements Explained

### Navbar (Top)
- SkillTrack Logo - Click to go Home
- Home - Main landing page
- Dashboard - Analytics view
- Associates - Manage profiles
- Add Associate - New profile form

### Color Coding
- 🔵 **Primary (Blue/Purple)** - Main actions
- 🟢 **Success (Green)** - Active/Good status
- 🟡 **Warning (Yellow)** - Expiring Soon/Caution
- 🔴 **Danger (Red)** - Expired/Delete

### Action Buttons
- 📝 Edit - Modify associate info
- 🎓 Add Cert - Add new certificate
- 🗑️ Delete - Remove associate

---

## 📱 Responsive Design

- ✅ Works on Desktop
- ✅ Works on Tablet
- ✅ Works on Mobile
- ✅ Automatic layout adjustment

---

## 🆘 Common Issues & Solutions

### Issue: "Address already in use"
**Solution**: Change port in app.py (line 8)
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue: "Templates not found"
**Solution**: Create `templates` folder
```bash
mkdir templates
```

### Issue: "Module not found"
**Solution**: Install dependencies
```bash
pip install -r Requirements.py
```

### Issue: "Database locked"
**Solution**: Delete database and restart
```bash
rm database.db
python app.py
```

---

## 📈 Certificate Status Logic

```
Today: 2024-01-15

Certificate 1:
  Expiry: 2024-02-14 → "Expiring Soon" (within 30 days)
  
Certificate 2:
  Expiry: 2024-01-10 → "Expired" (past expiry)
  
Certificate 3:
  Expiry: 2024-03-15 → "Active" (>30 days remaining)
```

---

## 🎯 What Each Page Does

### Home (`/`)
- Welcome message
- Quick stats overview
- Feature highlights
- Navigation to main sections

### Dashboard (`/dashboard`)
- Total associates count
- Certificate statistics
- Visual charts
- Expiring certificates alert
- Last updated timestamp

### Associates (`/associates`)
- List of all associates
- Associate cards with details
- Search functionality
- Add/Edit/Delete operations
- Certificate management

### Add Associate (`/add_associate`)
- Form for new associate
- Input validation
- Success confirmation
- Quick navigation after add

---

## 🔐 Data You Can Store

**Per Associate**:
- Full Name ✅
- Email Address ✅
- Phone Number ✅
- Job Role ✅
- Department ✅
- Years of Experience ✅
- Skills (Multiple) ✅
- Status (Active/Inactive) ✅
- Date Joined ✅

**Per Certificate**:
- Certificate Name ✅
- Issue Date ✅
- Expiry Date ✅
- Issuing Organization ✅
- Status (Auto-calculated) ✅

---

## 💻 API Quick Reference

```bash
# Get all associates
curl http://localhost:5000/api/associates

# Search associates
curl "http://localhost:5000/api/search?q=python&type=skill"

# Get dashboard stats
curl http://localhost:5000/api/dashboard

# Get expiring certificates
curl http://localhost:5000/api/expiring_certificates
```

---

## 🎓 Learning Path for Interns

1. **Understand Project Structure** - Review README.md
2. **Run Application** - Follow installation steps
3. **Explore Dashboard** - Add sample data
4. **Test Search** - Try different queries
5. **Review Code** - Study app.py and templates
6. **Make Changes** - Modify features
7. **Deploy** - Host on cloud platform

---

## 📚 Resources

- Flask Docs: https://flask.palletsprojects.com/
- Bootstrap: https://getbootstrap.com/
- Chart.js: https://www.chartjs.org/
- SQLite: https://www.sqlite.org/

---

## ✅ Checklist: First Time Setup

- [ ] Python 3.7+ installed
- [ ] Requirements.py dependencies installed
- [ ] Application running on localhost:5000
- [ ] Dashboard loads without errors
- [ ] Added first associate successfully
- [ ] Added certificate to associate
- [ ] Search functionality working
- [ ] Navigation bar working smoothly

**All checked? You're ready to go!** 🎉

---

## 🚀 Next Steps

1. **Add Sample Data** - Create 5-10 test associates
2. **Explore Features** - Try all functionality
3. **Customize** - Modify colors, text, add new fields
4. **Study Code** - Understand Flask and SQLite integration
5. **Deploy** - Put app on cloud (Heroku, AWS, etc.)

---

**Need Help?** Check the main README.md or review app.py comments.

Happy Learning! 🎓
