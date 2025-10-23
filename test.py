"""
QuackHub Healthcare - Simple Test Script
Tests database connections and basic functionality
"""

def test_imports():
    """Test if all required packages are installed"""
    print("Testing imports...")
    try:
        import flask
        print("✅ Flask installed")
        import flask_sqlalchemy
        print("✅ Flask-SQLAlchemy installed")
        import pymongo
        print("✅ PyMongo installed")
        import google.generativeai
        print("✅ Google Generative AI installed")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def test_mysql_connection():
    """Test MySQL database connection"""
    print("\nTesting MySQL connection...")
    try:
        from sqlalchemy import create_engine
        # Update this with your actual credentials
        engine = create_engine('mysql+pymysql://root:password@localhost/healthcare_db')
        connection = engine.connect()
        connection.close()
        print("✅ MySQL connection successful")
        return True
    except Exception as e:
        print(f"❌ MySQL connection failed: {e}")
        print("   Please check your MySQL credentials in app.py")
        return False


def test_mongodb_connection():
    """Test MongoDB connection"""
    print("\nTesting MongoDB connection...")
    try:
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
        # Trigger connection
        client.server_info()
        print("✅ MongoDB connection successful")
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("   Make sure MongoDB is running: sudo systemctl start mongod")
        return False


def test_gemini_api():
    """Test Gemini API connection (requires API key)"""
    print("\nTesting Gemini API...")
    try:
        import google.generativeai as genai
        # You need to set your API key here
        API_KEY = "YOUR_API_KEY"  # Update this
        
        if API_KEY == "YOUR_API_KEY":
            print("⚠️  Skipping Gemini API test - no API key set")
            print("   Update the API_KEY in test.py or app.py")
            return None
        
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-pro-002')
        response = model.generate_content("Say hello")
        print("✅ Gemini API connection successful")
        print(f"   Response: {response.text[:50]}...")
        return True
    except Exception as e:
        print(f"❌ Gemini API test failed: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("QuackHub Healthcare - System Test")
    print("=" * 50)
    
    results = {
        'imports': test_imports(),
        'mysql': test_mysql_connection(),
        'mongodb': test_mongodb_connection(),
        'gemini': test_gemini_api()
    }
    
    print("\n" + "=" * 50)
    print("Test Results:")
    print("=" * 50)
    
    for test, result in results.items():
        if result is True:
            print(f"✅ {test.upper()}: PASSED")
        elif result is False:
            print(f"❌ {test.upper()}: FAILED")
        else:
            print(f"⚠️  {test.upper()}: SKIPPED")
    
    print("\n")
    
    # Check if critical tests passed
    if results['imports'] and results['mysql'] and results['mongodb']:
        print("🎉 All critical tests passed! You're ready to run the app.")
        print("   Run: python app.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues above before running the app.")


if __name__ == "__main__":
    run_all_tests()
