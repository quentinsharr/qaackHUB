"""
QuackHub Healthcare - AI-Powered Medical Assistant
A Flask web application that analyzes symptoms and provides medical recommendations
"""

from flask import Flask, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
import google.generativeai as genai
from datetime import datetime
import os
import json

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change this in production

# MySQL Configuration (stores user data and queries)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/healthcare_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# MongoDB Configuration (stores API responses and analysis history)
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['healthcare_responses']
responses_collection = mongo_db['gemini_responses']

# Google Gemini API Configuration
GEMINI_API_KEY = "AIzaSyBqZ4uSsnutN0-3Vt75QgRy4cfJCVrxKGY"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro-002')


# ============= DATABASE MODELS =============

class UserQuery(db.Model):
    """MySQL table for storing user queries and basic info"""
    id = db.Column(db.Integer, primary_key=True)
    symptoms = db.Column(db.Text, nullable=False)
    age = db.Column(db.Integer)
    sex = db.Column(db.String(20))
    weight = db.Column(db.Integer)
    height = db.Column(db.Integer)
    duration = db.Column(db.String(50))
    severity = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_emergency = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<UserQuery {self.id}: {self.symptoms[:30]}...>'


# ============= ROUTES =============

@app.route('/')
def home():
    """Home page - displays the main symptom checker interface"""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze_symptoms():
    """
    Main analysis endpoint - processes symptoms and returns AI recommendations
    Stores data in MySQL and MongoDB
    """
    try:
        # Get data from the form
        data = request.get_json()
        symptoms = data.get('symptoms', '')
        age = data.get('age')
        sex = data.get('sex')
        weight = data.get('weight')
        height = data.get('height')
        duration = data.get('duration')
        severity = data.get('severity')
        
        # Validate input
        if not symptoms:
            return jsonify({'error': 'Please enter symptoms'}), 400
        
        # Save user query to MySQL
        user_query = UserQuery(
            symptoms=symptoms,
            age=age,
            sex=sex,
            weight=weight,
            height=height,
            duration=duration,
            severity=severity
        )
        db.session.add(user_query)
        db.session.commit()
        
        # Create detailed prompt for Gemini AI
        prompt = create_medical_prompt(symptoms, age, sex, weight, height, duration, severity)
        
        # Call Gemini API
        response = model.generate_content(prompt)
        ai_response = response.text
        
        # Parse the response to determine if it's an emergency
        is_emergency = check_emergency(ai_response, symptoms, severity)
        
        # Update emergency status in MySQL
        user_query.is_emergency = is_emergency
        db.session.commit()
        
        # Save AI response to MongoDB
        mongo_document = {
            'query_id': user_query.id,
            'symptoms': symptoms,
            'ai_response': ai_response,
            'is_emergency': is_emergency,
            'timestamp': datetime.utcnow(),
            'user_info': {
                'age': age,
                'sex': sex,
                'severity': severity
            }
        }
        responses_collection.insert_one(mongo_document)
        
        # Return the analysis results
        return jsonify({
            'success': True,
            'diagnosis': ai_response,
            'is_emergency': is_emergency,
            'query_id': user_query.id,
            'timestamp': datetime.now().strftime('%I:%M:%S %p')
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/history')
def get_history():
    """Get user's query history from MySQL"""
    queries = UserQuery.query.order_by(UserQuery.timestamp.desc()).limit(10).all()
    history = []
    
    for query in queries:
        history.append({
            'id': query.id,
            'symptoms': query.symptoms,
            'age': query.age,
            'severity': query.severity,
            'is_emergency': query.is_emergency,
            'timestamp': query.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify({'history': history})


@app.route('/response/<int:query_id>')
def get_response(query_id):
    """Get detailed AI response from MongoDB for a specific query"""
    mongo_response = responses_collection.find_one({'query_id': query_id})
    
    if mongo_response:
        # Convert MongoDB ObjectId to string for JSON serialization
        mongo_response['_id'] = str(mongo_response['_id'])
        return jsonify({'response': mongo_response})
    
    return jsonify({'error': 'Response not found'}), 404


@app.route('/stats')
def get_stats():
    """Dashboard statistics - combines MySQL and MongoDB data"""
    # Get total queries from MySQL
    total_queries = UserQuery.query.count()
    emergency_count = UserQuery.query.filter_by(is_emergency=True).count()
    
    # Get recent queries
    recent_queries = UserQuery.query.order_by(UserQuery.timestamp.desc()).limit(5).all()
    
    # Get MongoDB stats
    mongo_total = responses_collection.count_documents({})
    
    stats = {
        'total_queries': total_queries,
        'emergency_cases': emergency_count,
        'mongo_responses': mongo_total,
        'recent_queries': [
            {
                'symptoms': q.symptoms[:50],
                'severity': q.severity,
                'timestamp': q.timestamp.strftime('%Y-%m-%d %H:%M')
            }
            for q in recent_queries
        ]
    }
    
    return jsonify(stats)


# ============= HELPER FUNCTIONS =============

def create_medical_prompt(symptoms, age, sex, weight, height, duration, severity):
    """Create a detailed medical prompt for the AI"""
    prompt = f"""You are a medical AI assistant. Analyze the following patient information and provide:

1. **Potential Diagnosis**: What conditions might cause these symptoms?
2. **Recommended Medications**: Suggest over-the-counter or common medications (with dosages)
3. **Specialist Referral**: Which type of doctor should they see?
4. **Urgency Level**: Rate from 1-10 and indicate if ER visit needed
5. **Home Care Tips**: Self-care recommendations

**Patient Information:**
- Symptoms: {symptoms}
- Age: {age if age else 'Not provided'}
- Sex: {sex if sex else 'Not provided'}
- Weight: {weight} lbs (if weight else 'Not provided')
- Height: {height} inches (if height else 'Not provided')
- Duration: {duration if duration else 'Not provided'}
- Pain/Severity (1-10): {severity if severity else 'Not provided'}

Please provide clear, actionable medical guidance. If symptoms indicate emergency, clearly state "EMERGENCY" at the start of your response.

**IMPORTANT DISCLAIMER**: This is for informational purposes only. Always consult a healthcare professional for medical advice."""
    
    return prompt


def check_emergency(ai_response, symptoms, severity):
    """Determine if the case is an emergency based on AI response and symptoms"""
    emergency_keywords = [
        'emergency', 'urgent', '911', 'chest pain', 'difficulty breathing',
        'severe bleeding', 'unconscious', 'stroke', 'heart attack', 
        'severe pain', 'immediate', 'life-threatening'
    ]
    
    # Check AI response
    response_lower = ai_response.lower()
    for keyword in emergency_keywords:
        if keyword in response_lower:
            return True
    
    # Check symptoms
    symptoms_lower = symptoms.lower()
    for keyword in emergency_keywords:
        if keyword in symptoms_lower:
            return True
    
    # Check severity
    if severity and int(severity) >= 8:
        return True
    
    return False


# ============= DATABASE INITIALIZATION =============

def init_db():
    """Initialize the database tables"""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")


# ============= RUN APPLICATION =============

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Run the Flask app
    print("QuackHub Healthcare Server Starting...")
    print("MySQL: Storing user queries")
    print("MongoDB: Storing AI responses")
    print("Gemini AI: Ready for symptom analysis")
    app.run(debug=True, host='0.0.0.0', port=5000)
