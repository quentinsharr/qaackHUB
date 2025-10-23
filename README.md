# QAAckHub Healthcare

**AI-Powered Medical Assistant Built with Flask, MySQL & MongoDB**

Winner of **Best Beginner Project** at Steel Hacks XII (200+ participants)

## 🚀 Project Overview

QuackHub Healthcare is an intelligent web application that analyzes patient symptoms, demographics, and severity levels to provide personalized medical recommendations using Google's Gemini AI. The system determines urgency, suggests medications with dosages, recommends specialist referrals, and alerts users to emergency situations.

### Key Features

✅ **AI-Powered Diagnosis** - Uses Google Gemini API for intelligent symptom analysis  
✅ **Dual Database System** - MySQL for user data, MongoDB for API responses  
✅ **Emergency Detection** - Automatic 911/ER alerts for critical symptoms  
✅ **Medication Recommendations** - Specific drugs and dosages  
✅ **Specialist Referrals** - Directs users to appropriate medical professionals  
✅ **Location Services** - Finds nearest emergency rooms  
✅ **Query History** - Tracks past symptom checks  

---

## 🛠️ Tech Stack

- **Backend**: Python 3.x, Flask
- **Databases**: 
  - MySQL (user queries, demographics)
  - MongoDB (AI responses, analysis history)
- **AI/ML**: Google Gemini API
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Libraries**: SQLAlchemy, PyMongo, Flask-SQLAlchemy

---

## 📂 Project Structure

```
QuackHub-Healthcare/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main web interface
├── static/
│   └── css/
│       └── styles.css    # Styling
└── README.md             # This file
```

---

## 🔧 Installation & Setup

### Prerequisites

1. **Python 3.8+** installed
2. **MySQL** installed and running
3. **MongoDB** installed and running
4. **Google Gemini API Key** (get from [Google AI Studio](https://aistudio.google.com/))

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/QuackHub-Healthcare.git
cd QuackHub-Healthcare
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Set Up MySQL Database

```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE healthcare_db;
EXIT;
```

### Step 4: Configure the Application

Open `app.py` and update these settings:

```python
# MySQL Configuration (line 18)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://YOUR_USER:YOUR_PASSWORD@localhost/healthcare_db'

# Update your Gemini API Key (line 28)
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

# Change secret key (line 14)
app.secret_key = 'your-random-secret-key'
```

### Step 5: Initialize Database Tables

The app will automatically create tables when you first run it, but you can also do it manually:

```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

### Step 6: Start MongoDB

```bash
# Make sure MongoDB is running
mongod
# or on Linux/Mac:
sudo systemctl start mongod
```

### Step 7: Run the Application

```bash
python app.py
```

Visit: **http://localhost:5000**

---

## 🎯 How It Works

### 1. **User Input**
- Symptoms description
- Demographics (age, sex, weight, height)
- Symptom duration & severity (1-10)

### 2. **Data Storage**
- **MySQL** stores: User queries, demographics, emergency status
- **MongoDB** stores: AI responses, analysis history, timestamps

### 3. **AI Analysis**
- Flask sends prompt to Google Gemini API
- AI returns: diagnosis, medications, dosages, specialist referrals, urgency level

### 4. **Emergency Detection**
- Keywords: "chest pain", "difficulty breathing", "severe bleeding"
- Severity: Level 8+ triggers alert
- Response: 911 button + nearest ER locator

### 5. **Results Display**
- Diagnosis with confidence level
- Medication recommendations
- Emergency banner (if critical)
- Timestamp & query history

---

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main web interface |
| `/analyze` | POST | Submit symptoms for AI analysis |
| `/history` | GET | Retrieve query history (last 10) |
| `/response/<id>` | GET | Get detailed AI response by query ID |
| `/stats` | GET | Dashboard statistics (total queries, emergencies) |

---

## 📊 Database Schema

### MySQL: `user_query` Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| symptoms | Text | User's symptom description |
| age | Integer | Patient age |
| sex | String(20) | Patient sex |
| weight | Integer | Weight in lbs |
| height | Integer | Height in inches |
| duration | String(50) | Symptom duration |
| severity | Integer | Pain level (1-10) |
| timestamp | DateTime | Query timestamp |
| is_emergency | Boolean | Emergency flag |

### MongoDB: `gemini_responses` Collection

```json
{
  "query_id": 123,
  "symptoms": "headache, fever",
  "ai_response": "Full AI analysis...",
  "is_emergency": false,
  "timestamp": "2025-01-15T10:30:00Z",
  "user_info": {
    "age": 35,
    "sex": "male",
    "severity": 5
  }
}
```

---

## 🏆 Hackathon Achievement

**Steel Hacks XII - Best Beginner Project** (200+ participants)

### Challenge
- 24-hour time limit
- Mid-hackathon pivot from JavaScript to Python/Flask
- First time using Flask, MySQL, MongoDB integration
- Learned API integration under pressure

### Learning Outcomes
✅ Full-stack web development with Flask  
✅ Database integration (SQL & NoSQL)  
✅ RESTful API design  
✅ External API integration (Google Gemini)  
✅ Emergency detection algorithms  
✅ Real-time geolocation services  

---

## 🔐 Security Considerations

⚠️ **Important**: This is a hackathon project. For production use:

1. **Never commit API keys** - Use environment variables
2. **Secure database credentials** - Use `.env` files
3. **Input validation** - Sanitize all user inputs
4. **HTTPS only** - Encrypt data in transit
5. **Medical disclaimer** - Not a substitute for professional medical advice

---

## 🚀 Deployment

### Deploy to Heroku

```bash
# Install Heroku CLI
heroku login
heroku create quackhub-healthcare

# Add MySQL & MongoDB addons
heroku addons:create jawsdb:kitefin
heroku addons:create mongolab:sandbox

# Set environment variables
heroku config:set GEMINI_API_KEY=your_key_here
heroku config:set SECRET_KEY=your_secret_key

# Deploy
git push heroku main
```

### Deploy to Render/Railway

1. Connect your GitHub repo
2. Set environment variables in dashboard
3. Add MySQL & MongoDB services
4. Deploy with one click

---

## 📸 Screenshots

![QuackHub Interface](screenshot.png)
*AI-powered symptom analysis interface*

---

## 🤝 Contributing

This was a hackathon project, but contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

MIT License - feel free to use this project for learning!

---

## 👨‍💻 Author

**Quentin Sharr**
- GitHub: [@quentinsharr](https://github.com/quentinsharr)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

Built at **Steel Hacks XII** - University of Pittsburgh  
Team: Quentin, Allen, Vihaan

---

## 🙏 Acknowledgments

- Google Gemini AI for the intelligent analysis
- Steel Hacks organizing team
- University of Pittsburgh
- Our amazing team for the collaboration

---

## ⚠️ Medical Disclaimer

**This application is for educational and informational purposes only.**

- NOT a substitute for professional medical advice
- NOT intended to diagnose, treat, cure, or prevent any disease
- Always consult qualified healthcare professionals for medical concerns
- In case of emergency, call 911 immediately

---

## 🐛 Known Issues & Future Improvements

- [ ] Add user authentication
- [ ] Implement symptom autocomplete
- [ ] Add multilingual support
- [ ] Export results as PDF
- [ ] Integrate with pharmacy APIs for medication availability
- [ ] Add telemedicine video consultation
- [ ] Mobile app version

---

**Made with ❤️ and lots of ☕ during a 24-hour hackathon**
