import sqlite3
import pandas as pd
import os
import pickle
import numpy as np
from datetime import datetime, timedelta
import json

DATABASE_PATH = 'bantai_security.db'

def get_ts(hours_ago):
    """Get timestamp for X hours ago"""
    return (datetime.now() - timedelta(hours=hours_ago)).strftime('%Y-%m-%d %H:%M:%S')

def get_connection():
    """Get database connection"""
    return sqlite3.connect(DATABASE_PATH)

def load_ml_model():
    """Load the trained ML model"""
    try:
        with open('bantai_model.pkl', 'rb') as f:
            model_data = pickle.load(f)
        
        print("✅ ML model loaded successfully")
        print(f"   Model type: {type(model_data)}")
        
        # Check if it's a dictionary containing the model
        if isinstance(model_data, dict):
            # Try common dictionary keys where the model might be stored
            if 'model' in model_data:
                actual_model = model_data['model']
                print(f"   Extracted model type: {type(actual_model)}")
                return actual_model
            elif 'classifier' in model_data:
                actual_model = model_data['classifier']
                print(f"   Extracted model type: {type(actual_model)}")
                return actual_model
            else:
                print(f"   Available keys: {list(model_data.keys())}")
                print("   Please check which key contains your trained model")
                return None
        else:
            # It's already the model object
            return model_data
            
    except FileNotFoundError:
        print("⚠ Model file not found - using dummy predictions")
        return None

def get_full_model_prediction(user_id, current_login_data):
    """
    Get complete model prediction matching your notebook output
    Returns detailed analysis with Filipino-specific context
    """
    model = load_ml_model()
    
    if model is None:
        # Enhanced dummy prediction for testing
        return {
            'risk_score': 0.250,
            'risk_percentage': 25.0,
            'classification': 'MEDIUM',
            'action': 'ALLOW_WITH_OTP',
            'recommendation': 'ALLOW with SMS OTP: Model not available - manual review required.',
            'analysis_factors': [
                'Model not loaded - using fallback prediction',
                'Manual verification recommended'
            ],
            'warnings': ['⚠ Model unavailable'],
            'behavior_consistency': 75,
            'location_context': 'Unknown location context'
        }
    
    # Prepare features for your model (6 features as per your training)
    features = np.array([[
        current_login_data['time_diff'],
        current_login_data['distance'],
        current_login_data['device_type'],  # 0=mobile, 1=desktop, 2=tablet
        current_login_data['is_attack_ip'],
        current_login_data['login_successful'],
        current_login_data['latency']
    ]])
    
    try:
        # Get model prediction
        risk_probability = model.predict_proba(features)[0][1]
        risk_score = float(risk_probability)
        risk_percentage = risk_score * 100
        
        # Classification logic matching your notebook
        if risk_score < 0.3:
            classification = "LOW"
            action = "ALLOW"
        elif risk_score < 0.7:
            classification = "MEDIUM"
            action = "ALLOW_WITH_OTP"
        else:
            classification = "HIGH"
            action = "BLOCK"
        
        # Generate Filipino-specific context
        location_context = get_location_context(current_login_data['country'], current_login_data['city'])
        behavior_consistency = calculate_behavior_consistency(user_id, current_login_data)
        
        # Generate analysis factors
        analysis_factors = generate_analysis_factors(current_login_data, location_context, behavior_consistency)
        
        # Generate warnings
        warnings = generate_warnings(current_login_data, risk_score)
        
        # Generate recommendation
        recommendation = generate_recommendation(action, analysis_factors, location_context)
        
        return {
            'risk_score': risk_score,
            'risk_percentage': risk_percentage,
            'classification': classification,
            'action': action,
            'recommendation': recommendation,
            'analysis_factors': analysis_factors,
            'warnings': warnings,
            'behavior_consistency': behavior_consistency,
            'location_context': location_context
        }
        
    except Exception as e:
        print(f"Error in model prediction: {e}")
        # Return dummy prediction instead of calling self again
        return {
            'risk_score': 0.250,
            'risk_percentage': 25.0,
            'classification': 'MEDIUM',
            'action': 'ALLOW_WITH_OTP',
            'recommendation': 'ALLOW with SMS OTP: Model prediction failed - manual review required.',
            'analysis_factors': [
                'Model prediction error - using fallback',
                'Manual verification recommended'
            ],
            'warnings': ['⚠ Model prediction failed'],
            'behavior_consistency': 75,
            'location_context': 'Unknown location context'
        }

def get_location_context(country, city):
    """Provide Filipino-specific location context"""
    
    # OFW employment hubs
    ofw_hubs = {
        'United Arab Emirates': ['Dubai', 'Abu Dhabi', 'Sharjah'],
        'Saudi Arabia': ['Riyadh', 'Jeddah', 'Dammam'],
        'Qatar': ['Doha'],
        'Kuwait': ['Kuwait City'],
        'Singapore': ['Singapore'],
        'Hong Kong': ['Hong Kong'],
        'United States': ['Los Angeles', 'San Francisco', 'New York', 'Chicago'],
        'Canada': ['Toronto', 'Vancouver', 'Calgary']
    }
    
    # Known cybercrime locations
    cybercrime_locations = {
        'Nigeria': ['Lagos', 'Abuja'],
        'Russia': ['Moscow', 'St. Petersburg'],
        'China': ['Beijing', 'Shanghai'],
        'North Korea': ['Pyongyang']
    }
    
    if country in ofw_hubs and city in ofw_hubs[country]:
        return "Major OFW employment hubs in Middle East"
    elif country in cybercrime_locations:
        return "Known cybercrime and state-sponsored threat locations"
    elif country == 'Philippines':
        return "Domestic location"
    else:
        return "International location"

def calculate_behavior_consistency(user_id, current_login_data):
    """Calculate behavior consistency based on user history"""
    # This would analyze historical patterns
    # For now, return a reasonable estimate based on login characteristics
    if current_login_data['device_type'] == 0:  # mobile
        return 85  # Mobile is common
    elif current_login_data['distance'] < 100:
        return 95  # Local login
    else:
        return 70  # International login

def generate_analysis_factors(login_data, location_context, behavior_consistency):
    """Generate detailed analysis factors"""
    factors = []
    
    # Distance analysis
    if login_data['distance'] < 50:
        factors.append("Travel is plausible (Same location or local area)")
    elif login_data['distance'] < 1000:
        factors.append("Travel is plausible (Domestic travel)")
    else:
        factors.append("Long-distance travel detected")
    
    # Behavior consistency
    factors.append(f"Behavior consistency: {behavior_consistency}%")
    
    # Location context
    factors.append(f"Location: {location_context}")
    
    # Device analysis
    device_names = {0: 'mobile', 1: 'desktop', 2: 'tablet'}
    device_name = device_names.get(login_data['device_type'], 'unknown')
    factors.append(f"Device type: {device_name}")
    
    return factors

def generate_warnings(login_data, risk_score):
    """Generate warning indicators"""
    warnings = []
    
    if login_data['is_attack_ip']:
        warnings.append("⚠ Known attack IP")
    
    if not login_data['login_successful']:
        warnings.append("⚠ Failed login attempt")
    
    if login_data['latency'] > 2000:
        warnings.append("⚠ Abnormal latency")
    
    if login_data['distance'] > 10000:
        warnings.append("⚠ Impossible travel distance")
    
    if risk_score > 0.8:
        warnings.append("⚠ High risk score")
    
    return warnings

def generate_recommendation(action, analysis_factors, location_context):
    """Generate detailed recommendation text"""
    if action == "ALLOW":
        return f"ALLOW: Legitimate travel with consistent behavior."
    elif action == "ALLOW_WITH_OTP":
        return f"ALLOW with SMS OTP: Possible legitimate travel, verify with additional authentication."
    else:  # BLOCK
        return f"BLOCK: High risk detected, prevent access and require manual review."
    
def update_action(activity_id, action):
    """Legacy function - redirects to enhanced version"""
    return update_admin_action(activity_id, action)

def initialize_database():
    """Create enhanced tables with realistic sample data"""
    print("Starting database initialization...")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        print("Connected to database")
        
        # Force drop and recreate tables
        cursor.execute('DROP TABLE IF EXISTS login_activities')
        cursor.execute('DROP TABLE IF EXISTS users')
        
        print("Dropped existing tables")
        
        # Create users table
        cursor.execute('''
            CREATE TABLE users (
                user_id VARCHAR(50) PRIMARY KEY,
                username VARCHAR(100),
                email VARCHAR(255),
                home_locations TEXT,  -- JSON array
                common_devices TEXT,  -- JSON array
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        print("Created users table")
    except Exception as e:
        print(f"Error during database initialization: {str(e)}")
        raise
    
    # Create enhanced login activities table
    cursor.execute('''
        CREATE TABLE login_activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id VARCHAR(50),
            login_timestamp TIMESTAMP,
            country VARCHAR(100),
            city VARCHAR(100),
            time_diff_hrs DECIMAL(10,2),
            distance_km INTEGER,
            device_type VARCHAR(50),
            latency_ms INTEGER,
            login_successful BOOLEAN,
            is_attack_ip BOOLEAN,
            
            -- Enhanced model output fields
            risk_score DECIMAL(10,6),
            risk_percentage DECIMAL(5,2),
            risk_classification VARCHAR(10),
            recommended_action VARCHAR(20),
            recommendation_text TEXT,
            analysis_factors TEXT,  -- JSON array
            warnings TEXT,  -- JSON array
            behavior_consistency INTEGER,
            location_context VARCHAR(100),
            
            -- Admin action
            admin_action VARCHAR(100) DEFAULT 'Pending Review',
            reviewed_at TIMESTAMP,
            reviewed_by VARCHAR(100),
            
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Insert sample users with baseline data
    sample_users = [
        ('U_TEST_001', 'high_risk_vpn_001', 'highrisk001@email.com', '["Manila", "Quezon City"]', '["mobile", "desktop"]'),
        ('U_TEST_002', 'attack_pattern_002', 'attack002@email.com', '["Manila", "Cebu City"]', '["mobile", "desktop"]'),
        ('U_TEST_003', 'impossible_travel_003', 'impossible003@email.com', '["Manila"]', '["mobile"]'),
        ('U_TEST_004', 'suspicious_behavior_004', 'suspicious004@email.com', '["Makati", "Taguig"]', '["mobile", "desktop"]'),
        ('U_TEST_005', 'medium_risk_ofw_005', 'mediumrisk005@email.com', '["Dubai", "Manila"]', '["mobile"]'),
        ('U_TEST_006', 'riyadh_ofw_006', 'riyadhofw006@email.com', '["Riyadh", "Negros Oriental"]', '["mobile"]'),
        ('U_TEST_007', 'low_risk_local_007', 'lowrisk007@email.com', '["Cebu City"]', '["mobile", "desktop"]'),
        ('U_TEST_008', 'business_traveler_008', 'business008@email.com', '["Davao City", "Manila", "Cebu City"]', '["mobile", "desktop", "tablet"]'),
        ('U_TEST_009', 'flight_attendant_009', 'fa009@email.com', '["Manila", "Makati", "Pasay"]', '["mobile"]'),
        ('U_TEST_010', 'hk_ofw_010', 'hkofw010@email.com', '["Hong Kong", "Pangasinan"]', '["mobile"]')
    ]
    
    try:
        cursor.executemany('''
            INSERT OR REPLACE INTO users (user_id, username, email, home_locations, common_devices) 
            VALUES (?, ?, ?, ?, ?)
        ''', sample_users)
        conn.commit()
        print(f"✅ Successfully added {len(sample_users)} users")
    except Exception as e:
        print(f"❌ Error adding users: {e}")
        conn.rollback()
    
    # Insert realistic sample login activities with enhanced data
    sample_activities = [
# ============================================
        # U_TEST_001: HIGH RISK - VPN User (5 VPN + 5 legitimate)
        # ============================================
        ('U_TEST_001', get_ts(240), 'Philippines', 'Manila', 0.0, 0, 'mobile', 85, 1, 0,
         0.055, 5.5, 'LOW', 'ALLOW', 'ALLOW: Legitimate domestic login.',
         '["Behavior consistency: 95%", "Domestic location"]', '[]', 95, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_001', get_ts(216), 'Philippines', 'Quezon City', 24.0, 18, 'desktop', 70, 1, 0,
         0.065, 6.5, 'LOW', 'ALLOW', 'ALLOW: Legitimate travel.',
         '["Behavior consistency: 92%", "Domestic location"]', '[]', 92, 'Domestic location', 'Pending Review'),
        
        # VPN through Russia - HIGH RISK
        ('U_TEST_001', get_ts(192), 'Russia', 'Moscow', 24.0, 8500, 'desktop', 420, 1, 0,
         0.880, 88.0, 'HIGH', 'BLOCK', 'BLOCK: High risk detected from known cybercrime location.',
         '["Behavior consistency: 40%", "Known cybercrime location"]',
         '["⚠ Abnormal latency", "⚠ Impossible travel", "⚠ High risk score"]', 40, 'Known cybercrime and state-sponsored threat locations', 'True Positive - Blocked'),
        
        ('U_TEST_001', get_ts(168), 'Philippines', 'Manila', 24.0, 8500, 'mobile', 90, 1, 0,
         0.280, 28.0, 'LOW', 'ALLOW', 'ALLOW: Back to normal location.',
         '["Behavior consistency: 85%", "Domestic location"]', '[]', 85, 'Domestic location', 'Pending Review'),
        
        # VPN through Germany - HIGH RISK
        ('U_TEST_001', get_ts(144), 'Germany', 'Frankfurt', 24.0, 11000, 'desktop', 380, 1, 0,
         0.780, 78.0, 'HIGH', 'STRICT_VERIFICATION', 'HIGH RISK: Requires manual review.',
         '["Behavior consistency: 50%", "Unusual location"]',
         '["⚠ Abnormal latency", "⚠ Impossible travel distance"]', 50, 'Popular tourist and cultural destinations', 'Pending Review'),
        
        # VPN through US - MEDIUM-HIGH RISK
        ('U_TEST_001', get_ts(120), 'United States', 'New York', 24.0, 17000, 'desktop', 350, 1, 0,
         0.720, 72.0, 'HIGH', 'STRICT_VERIFICATION', 'HIGH RISK: Multiple authentication required.',
         '["Behavior consistency: 55%", "Major diaspora location"]',
         '["⚠ Abnormal latency", "⚠ Impossible travel"]', 55, 'Major Filipino diaspora communities', 'Pending Review'),
        
        ('U_TEST_001', get_ts(96), 'Philippines', 'Quezon City', 24.0, 17000, 'mobile', 88, 1, 0,
         0.250, 25.0, 'LOW', 'ALLOW', 'ALLOW: Returned to home location.',
         '["Behavior consistency: 88%", "Domestic location"]', '[]', 88, 'Domestic location', 'Pending Review'),
        
        # VPN through Singapore - MEDIUM RISK
        ('U_TEST_001', get_ts(72), 'Singapore', 'Singapore', 24.0, 2400, 'desktop', 180, 1, 0,
         0.540, 54.0, 'MEDIUM', 'ALLOW_WITH_OTP', 'MEDIUM RISK: Verify with OTP.',
         '["Behavior consistency: 70%", "Regional business center"]',
         '["⚠ Abnormal latency"]', 70, 'Regional and global business centers', 'Pending Review'),
        
        # VPN through Japan - MEDIUM RISK
        ('U_TEST_001', get_ts(48), 'Japan', 'Tokyo', 24.0, 3000, 'mobile', 220, 1, 0,
         0.500, 50.0, 'MEDIUM', 'ALLOW_WITH_OTP', 'MEDIUM RISK: Additional verification needed.',
         '["Behavior consistency: 68%", "Regional business center"]',
         '["⚠ Abnormal latency"]', 68, 'Regional and global business centers', 'Pending Review'),
        
        ('U_TEST_001', get_ts(24), 'Philippines', 'Manila', 24.0, 3000, 'mobile', 95, 1, 0,
         0.180, 18.0, 'LOW', 'ALLOW', 'ALLOW: Normal domestic login.',
         '["Behavior consistency: 90%", "Domestic location"]', '[]', 90, 'Domestic location', 'Pending Review'),
        
        # ============================================
        # U_TEST_002: HIGH RISK - Attack Pattern (7 suspicious + 3 valid)
        # ============================================
        ('U_TEST_002', get_ts(230), 'Philippines', 'Manila', 0.0, 0, 'mobile', 95, 1, 0,
         0.065, 6.5, 'LOW', 'ALLOW', 'ALLOW: Normal login.',
         '["Behavior consistency: 88%"]', '[]', 88, 'Domestic location', 'Pending Review'),
        
        # Failed login attempts
        ('U_TEST_002', get_ts(206), 'Philippines', 'Quezon City', 24.0, 18, 'desktop', 120, 0, 0,
         0.520, 52.0, 'MEDIUM', 'ALLOW_WITH_OTP', 'MEDIUM RISK: Failed login.',
         '["Behavior consistency: 65%"]', '["⚠ Failed login attempt"]', 65, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_002', get_ts(206), 'Philippines', 'Quezon City', 0.05, 0, 'desktop', 125, 0, 0,
         0.580, 58.0, 'MEDIUM', 'ALLOW_WITH_OTP', 'MEDIUM RISK: Multiple failed attempts.',
         '["Behavior consistency: 60%"]', '["⚠ Failed login attempt"]', 60, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_002', get_ts(182), 'Philippines', 'Cebu City', 24.0, 1279, 'mobile', 180, 1, 0,
         0.280, 28.0, 'LOW', 'ALLOW', 'ALLOW: Valid login after travel.',
         '["Behavior consistency: 75%"]', '[]', 75, 'Domestic location', 'Pending Review'),
        
        # Suspicious from attack IP
        ('U_TEST_002', get_ts(158), 'Philippines', 'Davao City', 24.0, 688, 'desktop', 350, 1, 1,
         0.780, 78.0, 'HIGH', 'STRICT_VERIFICATION', 'HIGH RISK: Known attack IP.',
         '["Behavior consistency: 45%"]', '["⚠ Known attack IP", "⚠ Abnormal latency"]', 45, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_002', get_ts(134), 'Philippines', 'Iloilo City', 24.0, 296, 'mobile', 250, 0, 0,
         0.640, 64.0, 'MEDIUM', 'ALLOW_WITH_OTP', 'MEDIUM RISK: Failed with high latency.',
         '["Behavior consistency: 55%"]', '["⚠ Failed login attempt", "⚠ Abnormal latency"]', 55, 'Domestic location', 'Pending Review'),
        
        # Late night suspicious activity
        ('U_TEST_002', get_ts(110), 'Philippines', 'Bacolod', 24.0, 128, 'desktop', 420, 1, 1,
         0.820, 82.0, 'HIGH', 'STRICT_VERIFICATION', 'HIGH RISK: Attack IP with abnormal behavior.',
         '["Behavior consistency: 40%"]', '["⚠ Known attack IP", "⚠ Abnormal latency"]', 40, 'Domestic location', 'True Positive - Blocked'),
        
        ('U_TEST_002', get_ts(86), 'Philippines', 'Baguio', 24.0, 410, 'mobile', 180, 0, 0,
         0.680, 68.0, 'MEDIUM', 'ALLOW_WITH_OTP', 'MEDIUM RISK: Failed login.',
         '["Behavior consistency: 50%"]', '["⚠ Failed login attempt"]', 50, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_002', get_ts(62), 'Philippines', 'Manila', 24.0, 410, 'mobile', 110, 1, 0,
         0.420, 42.0, 'MEDIUM', 'ALLOW_WITH_OTP', 'MEDIUM RISK: Valid but elevated risk.',
         '["Behavior consistency: 70%"]', '[]', 70, 'Domestic location', 'Pending Review'),
        
        # Final high-risk attempt
        ('U_TEST_002', get_ts(38), 'Philippines', 'Zamboanga', 24.0, 1800, 'desktop', 480, 1, 1,
         0.850, 85.0, 'HIGH', 'BLOCK', 'BLOCK: High risk pattern detected.',
         '["Behavior consistency: 35%"]', '["⚠ Known attack IP", "⚠ Abnormal latency", "⚠ High risk score"]', 35, 'Domestic location', 'True Positive - Blocked'),
        
        # ============================================
        # U_TEST_003: HIGH RISK - Impossible Travel
        # ============================================
        ('U_TEST_003', get_ts(220), 'Philippines', 'Manila', 0.0, 0, 'mobile', 85, 1, 0,
         0.055, 5.5, 'LOW', 'ALLOW', 'ALLOW: Normal login.',
         '["Behavior consistency: 95%"]', '[]', 95, 'Domestic location', 'Pending Review'),
        
        # Impossible travel to Russia in 1 hour
        ('U_TEST_003', get_ts(219), 'Russia', 'Moscow', 1.0, 8500, 'mobile', 2200, 0, 1,
         0.950, 95.0, 'HIGH', 'BLOCK', 'BLOCK: Impossible travel detected.',
         '["Behavior consistency: 20%"]',
         '["⚠ Known attack IP", "⚠ Failed login", "⚠ Abnormal latency", "⚠ Impossible travel distance", "⚠ High risk score"]',
         20, 'Known cybercrime and state-sponsored threat locations', 'True Positive - Blocked'),
        
        ('U_TEST_003', get_ts(196), 'Philippines', 'Manila', 23.0, 8500, 'mobile', 90, 1, 0,
         0.220, 22.0, 'LOW', 'ALLOW', 'ALLOW: Back to normal.',
         '["Behavior consistency: 88%"]', '[]', 88, 'Domestic location', 'Pending Review'),
        
        # Impossible travel to Nigeria in 2 hours
        ('U_TEST_003', get_ts(194), 'Nigeria', 'Lagos', 2.0, 15000, 'mobile', 3000, 0, 1,
         0.920, 92.0, 'HIGH', 'BLOCK', 'BLOCK: Impossible travel and attack IP.',
         '["Behavior consistency: 25%"]',
         '["⚠ Known attack IP", "⚠ Failed login", "⚠ Abnormal latency", "⚠ Impossible travel distance", "⚠ High risk score"]',
         25, 'Known cybercrime and state-sponsored threat locations', 'True Positive - Blocked'),
        
        ('U_TEST_003', get_ts(170), 'Philippines', 'Manila', 24.0, 15000, 'mobile', 88, 1, 0,
         0.195, 19.5, 'LOW', 'ALLOW', 'ALLOW: Normal domestic login.',
         '["Behavior consistency: 90%"]', '[]', 90, 'Domestic location', 'Pending Review'),
        
        # Impossible travel to China in 3 hours
        ('U_TEST_003', get_ts(167), 'China', 'Beijing', 3.0, 2800, 'mobile', 1800, 0, 1,
         0.870, 87.0, 'HIGH', 'BLOCK', 'BLOCK: Impossible travel pattern.',
         '["Behavior consistency: 30%"]',
         '["⚠ Known attack IP", "⚠ Failed login", "⚠ Abnormal latency", "⚠ Impossible travel distance"]',
         30, 'Known cybercrime and state-sponsored threat locations', 'True Positive - Blocked'),
        
        ('U_TEST_003', get_ts(143), 'Philippines', 'Manila', 24.0, 2800, 'mobile', 92, 1, 0,
         0.180, 18.0, 'LOW', 'ALLOW', 'ALLOW: Legitimate login.',
         '["Behavior consistency: 92%"]', '[]', 92, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_003', get_ts(119), 'Philippines', 'Quezon City', 24.0, 18, 'mobile', 85, 1, 0,
         0.070, 7.0, 'LOW', 'ALLOW', 'ALLOW: Local movement.',
         '["Behavior consistency: 94%"]', '[]', 94, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_003', get_ts(95), 'Philippines', 'Makati', 24.0, 12, 'mobile', 78, 1, 0,
         0.065, 6.5, 'LOW', 'ALLOW', 'ALLOW: Normal pattern.',
         '["Behavior consistency: 95%"]', '[]', 95, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_003', get_ts(71), 'Philippines', 'Manila', 24.0, 8, 'mobile', 82, 1, 0,
         0.060, 6.0, 'LOW', 'ALLOW', 'ALLOW: Consistent behavior.',
         '["Behavior consistency: 96%"]', '[]', 96, 'Domestic location', 'Pending Review'),
        
        # ============================================
        # U_TEST_004: MEDIUM-HIGH RISK - Suspicious Behavior
        # ============================================
        ('U_TEST_004', get_ts(210), 'Philippines', 'Makati', 0.0, 0, 'mobile', 85, 1, 0,
         0.060, 6.0, 'LOW', 'ALLOW', 'ALLOW: Normal login.',
         '["Behavior consistency: 93%"]', '[]', 93, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_004', get_ts(186), 'Philippines', 'Taguig', 24.0, 8, 'desktop', 70, 1, 0,
         0.075, 7.5, 'LOW', 'ALLOW', 'ALLOW: Local movement.',
         '["Behavior consistency: 90%"]', '[]', 90, 'Domestic location', 'Pending Review'),
        
        # Unusual time and device
        ('U_TEST_004', get_ts(162), 'Philippines', 'Pasig', 24.0, 15, 'desktop', 250, 1, 0,
         0.420, 42.0, 'MEDIUM', 'ALLOW_WITH_OTP', 'MEDIUM RISK: Unusual device pattern.',
         '["Behavior consistency: 68%"]', '["⚠ Abnormal latency"]', 68, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_004', get_ts(138), 'Philippines', 'Manila', 24.0, 12, 'mobile', 320, 1, 0,
         0.480, 48.0, 'MEDIUM', 'ALLOW_WITH_OTP', 'MEDIUM RISK: High latency detected.',
         '["Behavior consistency: 65%"]', '["⚠ Abnormal latency"]', 65, 'Domestic location', 'Pending Review'),
        
        # Late night access
        ('U_TEST_004', get_ts(114), 'Philippines', 'Quezon City', 24.0, 18, 'desktop', 380, 1, 0,
         0.560, 56.0, 'MEDIUM', 'ALLOW_WITH_OTP', 'MEDIUM RISK: Unusual time and behavior.',
         '["Behavior consistency: 60%"]', '["⚠ Abnormal latency"]', 60, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_004', get_ts(90), 'Philippines', 'Makati', 24.0, 18, 'mobile', 95, 1, 0,
         0.285, 28.5, 'LOW', 'ALLOW', 'ALLOW: Returned to normal.',
         '["Behavior consistency: 78%"]', '[]', 78, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_004', get_ts(66), 'Philippines', 'Taguig', 24.0, 8, 'desktop', 85, 1, 0,
         0.180, 18.0, 'LOW', 'ALLOW', 'ALLOW: Normal behavior.',
         '["Behavior consistency: 85%"]', '[]', 85, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_004', get_ts(42), 'Philippines', 'Makati', 24.0, 8, 'mobile', 78, 1, 0,
         0.150, 15.0, 'LOW', 'ALLOW', 'ALLOW: Consistent pattern.',
         '["Behavior consistency: 88%"]', '[]', 88, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_004', get_ts(18), 'Philippines', 'Manila', 24.0, 8, 'desktop', 72, 1, 0,
         0.120, 12.0, 'LOW', 'ALLOW', 'ALLOW: Normal login.',
         '["Behavior consistency: 90%"]', '[]', 90, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_004', get_ts(3), 'Philippines', 'Taguig', 15.0, 8, 'mobile', 82, 1, 0,
         0.095, 9.5, 'LOW', 'ALLOW', 'ALLOW: Recent normal activity.',
         '["Behavior consistency: 92%"]', '[]', 92, 'Domestic location', 'Pending Review'),
        
        # ============================================
        # U_TEST_005: MEDIUM RISK - Dubai OFW
        # ============================================
        ('U_TEST_005', get_ts(200), 'United Arab Emirates', 'Dubai', 0.0, 0, 'mobile', 180, 1, 0,
         0.140, 14.0, 'LOW', 'ALLOW', 'ALLOW: OFW in Dubai.',
         '["Behavior consistency: 88%"]', '[]', 88, 'Major OFW employment hubs in Middle East', 'Pending Review'),
        
        ('U_TEST_005', get_ts(176), 'United Arab Emirates', 'Dubai', 24.0, 0, 'mobile', 165, 1, 0,
         0.135, 13.5, 'LOW', 'ALLOW', 'ALLOW: Regular Dubai login.',
         '["Behavior consistency: 90%"]', '[]', 90, 'Major OFW employment hubs in Middle East', 'Pending Review'),
        
        # Travel to Philippines
        ('U_TEST_005', get_ts(152), 'Philippines', 'Manila', 24.0, 8200, 'mobile', 220, 1, 0,
         0.260, 26.0, 'MEDIUM', 'ALLOW_WITH_OTP', 'MEDIUM RISK: Long distance travel.',
         '["Behavior consistency: 82%"]', '[]', 82, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_005', get_ts(128), 'Philippines', 'Manila', 24.0, 0, 'mobile', 195, 1, 0,
         0.150, 15.0, 'LOW', 'ALLOW', 'ALLOW: In Philippines.',
         '["Behavior consistency: 85%"]', '[]', 85, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_005', get_ts(104), 'Philippines', 'Manila', 24.0, 0, 'mobile', 185, 1, 0,
         0.145, 14.5, 'LOW', 'ALLOW', 'ALLOW: Extended stay.',
         '["Behavior consistency: 87%"]', '[]', 87, 'Domestic location', 'Pending Review'),
        
        # Back to Dubai
        ('U_TEST_005', get_ts(80), 'United Arab Emirates', 'Dubai', 24.0, 8200, 'mobile', 175, 1, 0,
         0.240, 24.0, 'LOW', 'ALLOW', 'ALLOW: Return to Dubai.',
         '["Behavior consistency: 84%"]', '[]', 84, 'Major OFW employment hubs in Middle East', 'Pending Review'),
        
        ('U_TEST_005', get_ts(56), 'United Arab Emirates', 'Dubai', 24.0, 0, 'mobile', 170, 1, 0,
         0.138, 13.8, 'LOW', 'ALLOW', 'ALLOW: Regular activity.',
         '["Behavior consistency: 91%"]', '[]', 91, 'Major OFW employment hubs in Middle East', 'Pending Review'),
        
        ('U_TEST_005', get_ts(32), 'United Arab Emirates', 'Dubai', 24.0, 0, 'mobile', 162, 1, 0,
         0.142, 14.2, 'LOW', 'ALLOW', 'ALLOW: Normal pattern.',
         '["Behavior consistency: 89%"]', '[]', 89, 'Major OFW employment hubs in Middle East', 'Pending Review'),
        
        ('U_TEST_005', get_ts(8), 'United Arab Emirates', 'Dubai', 24.0, 0, 'mobile', 175, 1, 0,
         0.140, 14.0, 'LOW', 'ALLOW', 'ALLOW: Current location.',
         '["Behavior consistency: 90%"]', '[]', 90, 'Major OFW employment hubs in Middle East', 'Pending Review'),
        
        ('U_TEST_005', get_ts(1), 'United Arab Emirates', 'Dubai', 7.0, 0, 'mobile', 168, 1, 0,
         0.136, 13.6, 'LOW', 'ALLOW', 'ALLOW: Recent login.',
         '["Behavior consistency: 92%"]', '[]', 92, 'Major OFW employment hubs in Middle East', 'Pending Review'),
        
        # ============================================
        # U_TEST_006: MEDIUM RISK - Riyadh OFW
        # ============================================
        ('U_TEST_006', get_ts(190), 'Saudi Arabia', 'Riyadh', 0.0, 0, 'mobile', 165, 1, 0,
         0.140, 14.0, 'LOW', 'ALLOW', 'ALLOW: OFW in Riyadh.',
         '["Behavior consistency: 88%"]', '[]', 88, 'Major OFW employment hubs in Middle East', 'Pending Review'),
        
        ('U_TEST_006', get_ts(166), 'Saudi Arabia', 'Riyadh', 24.0, 0, 'mobile', 158, 1, 0,
         0.135, 13.5, 'LOW', 'ALLOW', 'ALLOW: Regular work.',
         '["Behavior consistency: 90%"]', '[]', 90, 'Major OFW employment hubs in Middle East', 'Pending Review'),
        
        # Travel to Philippines - MEDIUM RISK due to distance
        ('U_TEST_006', get_ts(142), 'Philippines', 'Negros Oriental', 24.0, 8920, 'mobile', 220, 1, 0,
         0.280, 28.0, 'MEDIUM', 'ALLOW_WITH_OTP', 'MEDIUM RISK: Long distance travel from Riyadh.',
         '["Behavior consistency: 82%"]', '[]', 82, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_006', get_ts(118), 'Philippines', 'Negros Oriental', 24.0, 0, 'mobile', 245, 1, 0,
         0.150, 15.0, 'LOW', 'ALLOW', 'ALLOW: Home visit.',
         '["Behavior consistency: 85%"]', '[]', 85, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_006', get_ts(94), 'Philippines', 'Negros Oriental', 24.0, 0, 'mobile', 230, 1, 0,
         0.145, 14.5, 'LOW', 'ALLOW', 'ALLOW: Extended stay.',
         '["Behavior consistency: 87%"]', '[]', 87, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_006', get_ts(70), 'Philippines', 'Negros Oriental', 24.0, 0, 'mobile', 215, 1, 0,
         0.140, 14.0, 'LOW', 'ALLOW', 'ALLOW: Still in Philippines.',
         '["Behavior consistency: 88%"]', '[]', 88, 'Domestic location', 'Pending Review'),
        
        # Return to Riyadh
        ('U_TEST_006', get_ts(46), 'Saudi Arabia', 'Riyadh', 24.0, 8920, 'mobile', 180, 1, 0,
         0.240, 24.0, 'LOW', 'ALLOW', 'ALLOW: Return to work.',
         '["Behavior consistency: 84%"]', '[]', 84, 'Major OFW employment hubs in Middle East', 'Pending Review'),
        
        ('U_TEST_006', get_ts(22), 'Saudi Arabia', 'Riyadh', 24.0, 0, 'mobile', 170, 1, 0,
         0.138, 13.8, 'LOW', 'ALLOW', 'ALLOW: Regular work routine.',
         '["Behavior consistency: 91%"]', '[]', 91, 'Major OFW employment hubs in Middle East', 'Pending Review'),
        
        ('U_TEST_006', get_ts(6), 'Saudi Arabia', 'Riyadh', 16.0, 0, 'mobile', 162, 1, 0,
         0.142, 14.2, 'LOW', 'ALLOW', 'ALLOW: Normal activity.',
         '["Behavior consistency: 89%"]', '[]', 89, 'Major OFW employment hubs in Middle East', 'Pending Review'),
        
        ('U_TEST_006', get_ts(2), 'Saudi Arabia', 'Riyadh', 4.0, 0, 'mobile', 175, 1, 0,
         0.140, 14.0, 'LOW', 'ALLOW', 'ALLOW: Recent login.',
         '["Behavior consistency: 90%"]', '[]', 90, 'Major OFW employment hubs in Middle East', 'Pending Review'),
        
        # ============================================
        # U_TEST_007: LOW RISK - Cebu Local User
        # ============================================
        ('U_TEST_007', get_ts(180), 'Philippines', 'Cebu City', 0.0, 0, 'mobile', 75, 1, 0,
         0.040, 4.0, 'LOW', 'ALLOW', 'ALLOW: Local user.',
         '["Behavior consistency: 98%"]', '[]', 98, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_007', get_ts(156), 'Philippines', 'Cebu City', 24.0, 0, 'desktop', 35, 1, 0,
         0.035, 3.5, 'LOW', 'ALLOW', 'ALLOW: Regular login.',
         '["Behavior consistency: 100%"]', '[]', 100, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_007', get_ts(132), 'Philippines', 'Cebu City', 24.0, 0, 'mobile', 80, 1, 0,
         0.038, 3.8, 'LOW', 'ALLOW', 'ALLOW: Consistent pattern.',
         '["Behavior consistency: 98%"]', '[]', 98, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_007', get_ts(108), 'Philippines', 'Cebu City', 24.0, 0, 'mobile', 70, 1, 0,
         0.042, 4.2, 'LOW', 'ALLOW', 'ALLOW: Normal activity.',
         '["Behavior consistency: 97%"]', '[]', 97, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_007', get_ts(84), 'Philippines', 'Cebu City', 24.0, 0, 'desktop', 40, 1, 0,
         0.036, 3.6, 'LOW', 'ALLOW', 'ALLOW: Work session.',
         '["Behavior consistency: 100%"]', '[]', 100, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_007', get_ts(60), 'Philippines', 'Cebu City', 24.0, 0, 'mobile', 85, 1, 0,
         0.040, 4.0, 'LOW', 'ALLOW', 'ALLOW: Regular check.',
         '["Behavior consistency: 98%"]', '[]', 98, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_007', get_ts(36), 'Philippines', 'Cebu City', 24.0, 0, 'mobile', 90, 1, 0,
         0.045, 4.5, 'LOW', 'ALLOW', 'ALLOW: Weekend login.',
         '["Behavior consistency: 95%"]', '[]', 95, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_007', get_ts(24), 'Philippines', 'Cebu City', 12.0, 0, 'desktop', 50, 1, 0,
         0.037, 3.7, 'LOW', 'ALLOW', 'ALLOW: Normal session.',
         '["Behavior consistency: 100%"]', '[]', 100, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_007', get_ts(12), 'Philippines', 'Cebu City', 12.0, 0, 'mobile', 65, 1, 0,
         0.043, 4.3, 'LOW', 'ALLOW', 'ALLOW: Recent activity.',
         '["Behavior consistency: 97%"]', '[]', 97, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_007', get_ts(4), 'Philippines', 'Cebu City', 8.0, 0, 'desktop', 45, 1, 0,
         0.035, 3.5, 'LOW', 'ALLOW', 'ALLOW: Current session.',
         '["Behavior consistency: 100%"]', '[]', 100, 'Domestic location', 'Pending Review'),
        
        # ============================================
        # U_TEST_008: LOW RISK - Business Traveler
        # ============================================
        ('U_TEST_008', get_ts(170), 'Philippines', 'Davao City', 0.0, 0, 'desktop', 95, 1, 0,
         0.055, 5.5, 'LOW', 'ALLOW', 'ALLOW: Home base.',
         '["Behavior consistency: 95%"]', '[]', 95, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_008', get_ts(146), 'Philippines', 'Manila', 24.0, 1967, 'mobile', 120, 1, 0,
         0.180, 18.0, 'LOW', 'ALLOW', 'ALLOW: Business trip to Manila.',
         '["Behavior consistency: 85%"]', '[]', 85, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_008', get_ts(122), 'Philippines', 'Makati', 24.0, 8, 'desktop', 80, 1, 0,
         0.090, 9.0, 'LOW', 'ALLOW', 'ALLOW: Business meeting.',
         '["Behavior consistency: 90%"]', '[]', 90, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_008', get_ts(98), 'Philippines', 'Cebu City', 24.0, 1279, 'mobile', 110, 1, 0,
         0.160, 16.0, 'LOW', 'ALLOW', 'ALLOW: Travel to Cebu.',
         '["Behavior consistency: 88%"]', '[]', 88, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_008', get_ts(74), 'Philippines', 'Cebu City', 24.0, 0, 'tablet', 75, 1, 0,
         0.080, 8.0, 'LOW', 'ALLOW', 'ALLOW: Business session.',
         '["Behavior consistency: 92%"]', '[]', 92, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_008', get_ts(50), 'Philippines', 'Iloilo City', 24.0, 296, 'mobile', 130, 1, 0,
         0.140, 14.0, 'LOW', 'ALLOW', 'ALLOW: Western Visayas meeting.',
         '["Behavior consistency: 85%"]', '[]', 85, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_008', get_ts(26), 'Philippines', 'Manila', 24.0, 1158, 'desktop', 95, 1, 0,
         0.170, 17.0, 'LOW', 'ALLOW', 'ALLOW: Return to Manila.',
         '["Behavior consistency: 87%"]', '[]', 87, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_008', get_ts(16), 'Philippines', 'Taguig', 10.0, 8, 'mobile', 85, 1, 0,
         0.075, 7.5, 'LOW', 'ALLOW', 'ALLOW: Hotel check-in.',
         '["Behavior consistency: 90%"]', '[]', 90, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_008', get_ts(8), 'Philippines', 'Davao City', 8.0, 1967, 'mobile', 105, 1, 0,
         0.185, 18.5, 'LOW', 'ALLOW', 'ALLOW: Return home.',
         '["Behavior consistency: 88%"]', '[]', 88, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_008', get_ts(2), 'Philippines', 'Davao City', 6.0, 0, 'desktop', 70, 1, 0,
         0.060, 6.0, 'LOW', 'ALLOW', 'ALLOW: Back to work.',
         '["Behavior consistency: 95%"]', '[]', 95, 'Domestic location', 'Pending Review'),
        
        # ============================================
        # U_TEST_009: LOW RISK - Flight Attendant (Large time gaps)
        # ============================================
        ('U_TEST_009', get_ts(160), 'Philippines', 'Manila', 0.0, 0, 'mobile', 95, 1, 0,
         0.055, 5.5, 'LOW', 'ALLOW', 'ALLOW: Home base after flight.',
         '["Behavior consistency: 95%"]', '[]', 95, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_009', get_ts(112), 'Philippines', 'Pasay', 48.0, 12, 'mobile', 110, 1, 0,
         0.070, 7.0, 'LOW', 'ALLOW', 'ALLOW: Layover rest.',
         '["Behavior consistency: 92%"]', '[]', 92, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_009', get_ts(40), 'Philippines', 'Makati', 72.0, 8, 'mobile', 85, 1, 0,
         0.060, 6.0, 'LOW', 'ALLOW', 'ALLOW: Home after international route.',
         '["Behavior consistency: 94%"]', '[]', 94, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_009', get_ts(16), 'Philippines', 'Manila', 24.0, 8, 'mobile', 100, 1, 0,
         0.065, 6.5, 'LOW', 'ALLOW', 'ALLOW: Quick check before flight.',
         '["Behavior consistency: 93%"]', '[]', 93, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_009', get_ts(-44), 'Philippines', 'Pasay', 60.0, 12, 'mobile', 90, 1, 0,
         0.075, 7.5, 'LOW', 'ALLOW', 'ALLOW: Back from long-haul.',
         '["Behavior consistency: 91%"]', '[]', 91, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_009', get_ts(-88), 'Philippines', 'Manila', 44.0, 12, 'mobile', 105, 1, 0,
         0.068, 6.8, 'LOW', 'ALLOW', 'ALLOW: Mid-range route return.',
         '["Behavior consistency: 92%"]', '[]', 92, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_009', get_ts(-184), 'Philippines', 'Pasay', 96.0, 12, 'mobile', 115, 1, 0,
         0.072, 7.2, 'LOW', 'ALLOW', 'ALLOW: Long international route.',
         '["Behavior consistency: 90%"]', '[]', 90, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_009', get_ts(-236), 'Philippines', 'Makati', 52.0, 8, 'mobile', 88, 1, 0,
         0.062, 6.2, 'LOW', 'ALLOW', 'ALLOW: Home after Asian route.',
         '["Behavior consistency: 94%"]', '[]', 94, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_009', get_ts(-304), 'Philippines', 'Manila', 68.0, 8, 'mobile', 92, 1, 0,
         0.066, 6.6, 'LOW', 'ALLOW', 'ALLOW: Middle East route return.',
         '["Behavior consistency: 93%"]', '[]', 93, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_009', get_ts(-388), 'Philippines', 'Pasay', 84.0, 12, 'mobile', 98, 1, 0,
         0.070, 7.0, 'LOW', 'ALLOW', 'ALLOW: Pacific route return.',
         '["Behavior consistency: 91%"]', '[]', 91, 'Domestic location', 'Pending Review'),
        
        # ============================================
        # U_TEST_010: LOW RISK - Hong Kong OFW
        # ============================================
        ('U_TEST_010', get_ts(150), 'Hong Kong', 'Hong Kong', 0.0, 0, 'mobile', 45, 1, 0,
         0.180, 18.0, 'LOW', 'ALLOW', 'ALLOW: Regular work day.',
         '["Behavior consistency: 90%"]', '[]', 90, 'Regional and global business centers', 'Pending Review'),
        
        ('U_TEST_010', get_ts(126), 'Hong Kong', 'Hong Kong', 24.0, 0, 'mobile', 38, 1, 0,
         0.175, 17.5, 'LOW', 'ALLOW', 'ALLOW: Weekend in HK.',
         '["Behavior consistency: 92%"]', '[]', 92, 'Regional and global business centers', 'Pending Review'),
        
        ('U_TEST_010', get_ts(102), 'Hong Kong', 'Hong Kong', 24.0, 0, 'mobile', 42, 1, 0,
         0.172, 17.2, 'LOW', 'ALLOW', 'ALLOW: Regular workday.',
         '["Behavior consistency: 93%"]', '[]', 93, 'Regional and global business centers', 'Pending Review'),
        
        ('U_TEST_010', get_ts(78), 'Hong Kong', 'Hong Kong', 24.0, 0, 'mobile', 50, 1, 0,
         0.178, 17.8, 'LOW', 'ALLOW', 'ALLOW: Normal activity.',
         '["Behavior consistency: 91%"]', '[]', 91, 'Regional and global business centers', 'Pending Review'),
        
        # Visit to Philippines
        ('U_TEST_010', get_ts(54), 'Philippines', 'Pangasinan', 24.0, 1694, 'mobile', 180, 1, 0,
         0.250, 25.0, 'LOW', 'ALLOW', 'ALLOW: Home visit from HK.',
         '["Behavior consistency: 85%"]', '[]', 85, 'Domestic location', 'Pending Review'),
        
        ('U_TEST_010', get_ts(30), 'Philippines', 'Pangasinan', 24.0, 0, 'mobile', 195, 1, 0,
         0.120, 12.0, 'LOW', 'ALLOW', 'ALLOW: Family time.',
         '["Behavior consistency: 88%"]', '[]', 88, 'Domestic location', 'Pending Review'),
        
        # Return to Hong Kong
        ('U_TEST_010', get_ts(10), 'Hong Kong', 'Hong Kong', 20.0, 1694, 'mobile', 55, 1, 0,
         0.220, 22.0, 'LOW', 'ALLOW', 'ALLOW: Back to work.',
         '["Behavior consistency: 87%"]', '[]', 87, 'Regional and global business centers', 'Pending Review'),
        
        ('U_TEST_010', get_ts(6), 'Hong Kong', 'Hong Kong', 4.0, 0, 'mobile', 40, 1, 0,
         0.170, 17.0, 'LOW', 'ALLOW', 'ALLOW: Work routine.',
         '["Behavior consistency: 94%"]', '[]', 94, 'Regional and global business centers', 'Pending Review'),
        
        ('U_TEST_010', get_ts(3), 'Hong Kong', 'Hong Kong', 3.0, 0, 'mobile', 48, 1, 0,
         0.174, 17.4, 'LOW', 'ALLOW', 'ALLOW: Weekend check.',
         '["Behavior consistency: 92%"]', '[]', 92, 'Regional and global business centers', 'Pending Review'),
        
        ('U_TEST_010', get_ts(1), 'Hong Kong', 'Hong Kong', 2.0, 0, 'mobile', 45, 1, 0,
         0.176, 17.6, 'LOW', 'ALLOW', 'ALLOW: Recent login.',
         '["Behavior consistency: 93%"]', '[]', 93, 'Regional and global business centers', 'Pending Review'),
      
    ]
    


    print(f"Inserting {len(sample_activities)} activities...")
    try:
        cursor.executemany('''
            INSERT INTO login_activities 
            (user_id, login_timestamp, country, city, time_diff_hrs, distance_km, 
            device_type, latency_ms, login_successful, is_attack_ip,
            risk_score, risk_percentage, risk_classification, recommended_action,
            recommendation_text, analysis_factors, warnings, behavior_consistency,
            location_context, admin_action)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_activities)
        print("Activities inserted successfully")
        
        conn.commit()
        print("Changes committed")
        
        conn.close()
        print("Database connection closed")
        
        print("\n✅ Fresh enhanced database initialized successfully!")
        print(f"✅ Added {len(sample_users)} users and {len(sample_activities)} login activities")
    except Exception as e:
        print(f"Error during activity insertion: {str(e)}")
        conn.rollback()
        conn.close()
        raise

def get_login_activities():
    """Get login activities with enhanced model output"""
    conn = get_connection()
    query = '''
        SELECT 
            la.id as "#",
            la.user_id as "User ID",
            la.login_timestamp as "Login Timestamp (UTC+8)",
            la.country as "Country",
            la.city as "City",
            la.time_diff_hrs as "time_diff (hrs)",
            la.distance_km as "distance (km)",
            la.device_type as "device_type",
            la.latency_ms as "latency (ms)",
            la.login_successful as "login_successful",
            la.is_attack_ip as "is_attack_ip",
            la.risk_score as "risk_score",
            la.risk_percentage as "Risk %",
            la.risk_classification as "Classification",
            la.recommended_action as "AI Action",
            la.recommendation_text as "AI Recommendation",
            la.analysis_factors as "Analysis Factors",
            la.warnings as "Warnings",
            la.behavior_consistency as "Behavior %",
            la.location_context as "Location Context",
            la.admin_action as "Admin Action"
        FROM login_activities la
        ORDER BY la.login_timestamp DESC
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Parse JSON fields
    if len(df) > 0:
        df['Analysis Factors'] = df['Analysis Factors'].apply(lambda x: json.loads(x) if x else [])
        df['Warnings'] = df['Warnings'].apply(lambda x: json.loads(x) if x else [])
    
    return df

def get_dashboard_metrics():
    """Legacy function - redirects to enhanced version"""
    return get_dashboard_metrics_enhanced()

def get_dashboard_metrics_enhanced():
    """Get enhanced dashboard metrics"""
    conn = get_connection()
    
    # Total login attempts
    total_attempts = conn.execute('SELECT COUNT(*) FROM login_activities').fetchone()[0]
    
    # High-risk activities (>= 70% risk)
    high_risk = conn.execute('SELECT COUNT(*) FROM login_activities WHERE risk_percentage >= 70').fetchone()[0]
    
    # Blocked activities
    blocked = conn.execute("SELECT COUNT(*) FROM login_activities WHERE recommended_action = 'BLOCK'").fetchone()[0]
    
    # Activities requiring OTP
    otp_required = conn.execute("SELECT COUNT(*) FROM login_activities WHERE recommended_action = 'ALLOW_WITH_OTP'").fetchone()[0]
    
    # Attack IP attempts
    attack_ips = conn.execute('SELECT COUNT(*) FROM login_activities WHERE is_attack_ip = 1').fetchone()[0]
    
    conn.close()
    
    return {
        'total_attempts': total_attempts,
        'high_risk': high_risk,
        'blocked': blocked,
        'otp_required': otp_required,
        'attack_ips': attack_ips
    }

def add_login_activity_enhanced(user_id, country, city, time_diff, distance, device_type, latency, is_attack_ip, login_successful=True):
    """Add new login activity with enhanced ML prediction"""
    
    # Prepare data for ML model
    device_encoded = 0 if device_type == 'mobile' else 1 if device_type == 'desktop' else 2
    
    login_data = {
        'time_diff': time_diff,
        'distance': distance,
        'device_type': device_encoded,
        'latency': latency,
        'is_attack_ip': 1 if is_attack_ip else 0,
        'login_successful': 1 if login_successful else 0,
        'country': country,
        'city': city
    }
    
    # Get enhanced ML prediction
    prediction = get_full_model_prediction(user_id, login_data)
    
    # Insert into database
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO login_activities 
        (user_id, login_timestamp, country, city, time_diff_hrs, distance_km, 
         device_type, latency_ms, login_successful, is_attack_ip,
         risk_score, risk_percentage, risk_classification, recommended_action,
         recommendation_text, analysis_factors, warnings, behavior_consistency,
         location_context, admin_action)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), country, city,
        time_diff, distance, device_type, latency, login_successful, is_attack_ip,
        prediction['risk_score'], prediction['risk_percentage'], 
        prediction['classification'], prediction['action'],
        prediction['recommendation'], json.dumps(prediction['analysis_factors']),
        json.dumps(prediction['warnings']), prediction['behavior_consistency'],
        prediction['location_context'], 'Pending Review'
    ))
    
    conn.commit()
    conn.close()
    
    return prediction

def update_admin_action(activity_id, action, admin_user="admin"):
    """Update admin action for a login activity"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE login_activities 
        SET admin_action = ?, reviewed_at = ?, reviewed_by = ?
        WHERE id = ?
    ''', (action, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), admin_user, activity_id))
    
    conn.commit()
    conn.close()

def get_detection_accuracy():
    """Calculate detection accuracy for dashboard"""
    conn = get_connection()
    
    # Count total reviewed items
    total_reviewed = conn.execute('''
        SELECT COUNT(*) FROM login_activities 
        WHERE admin_action IN ('False Positive', 'True Positive - Blocked', 'Confirmed Correct')
    ''').fetchone()[0]
    
    # Count correct predictions
    correct_predictions = conn.execute('''
        SELECT COUNT(*) FROM login_activities 
        WHERE (risk_percentage >= 70 AND admin_action = 'True Positive - Blocked')
           OR (risk_percentage < 70 AND admin_action = 'False Positive')
           OR (admin_action = 'Confirmed Correct')
    ''').fetchone()[0]
    
    conn.close()
    
    if total_reviewed == 0:
        return 94  # Default accuracy for new system
    
    accuracy = (correct_predictions / total_reviewed) * 100
    return round(accuracy)

def get_login_activities_enhanced():
    """Get login activities with enhanced model output"""
    conn = get_connection()
    query = '''
        SELECT 
            la.id as "#",
            la.user_id as "User ID",
            la.login_timestamp as "Login Timestamp (UTC+8)",
            la.country as "Country",
            la.city as "City",
            la.time_diff_hrs as "time_diff (hrs)",
            la.distance_km as "distance (km)",
            la.device_type as "device_type",
            la.latency_ms as "latency (ms)",
            la.login_successful as "login_successful",
            la.is_attack_ip as "is_attack_ip",
            la.risk_score as "risk_score",
            la.risk_percentage as "Risk %",
            la.risk_classification as "Classification",
            la.recommended_action as "AI Action",
            la.recommendation_text as "AI Recommendation",
            la.analysis_factors as "Analysis Factors",
            la.warnings as "Warnings",
            la.behavior_consistency as "Behavior %",
            la.location_context as "Location Context",
            la.admin_action as "Admin Action"
        FROM login_activities la
        ORDER BY la.login_timestamp DESC
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Parse JSON fields
    if len(df) > 0:
        df['Analysis Factors'] = df['Analysis Factors'].apply(lambda x: json.loads(x) if x else [])
        df['Warnings'] = df['Warnings'].apply(lambda x: json.loads(x) if x else [])
    
    return df

def get_false_positives_count():
    """Get count of false positives marked in last 7 days"""
    conn = get_connection()
    
    count = conn.execute('''
        SELECT COUNT(*) FROM login_activities 
        WHERE admin_action = 'False Positive'
        AND login_timestamp >= datetime('now', '-7 days')
    ''').fetchone()[0]
    
    conn.close()
    return count

def get_user_timeline_data(user_id):
    """Get user's login timeline data for visualization"""
    conn = get_connection()
    query = '''
        SELECT 
            login_timestamp,
            country,
            city,
            distance_km,
            device_type,
            risk_percentage,
            risk_classification,
            behavior_consistency,
            location_context,
            admin_action,
            recommended_action,
            analysis_factors,
            warnings
        FROM login_activities 
        WHERE user_id = ?
        ORDER BY login_timestamp ASC
    '''
    df = pd.read_sql_query(query, conn, params=[user_id])
    conn.close()
    
    if len(df) > 0:
        df['login_timestamp'] = pd.to_datetime(df['login_timestamp'])
        df['date'] = df['login_timestamp'].dt.date
        df['analysis_factors'] = df['analysis_factors'].apply(lambda x: json.loads(x) if x else [])
        df['warnings'] = df['warnings'].apply(lambda x: json.loads(x) if x else [])
    
    return df

def get_user_info(user_id):
    """Get user information"""
    conn = get_connection()
    query = '''
        SELECT username, email, home_locations, common_devices, created_at
        FROM users 
        WHERE user_id = ?
    '''
    result = pd.read_sql_query(query, conn, params=[user_id])
    conn.close()
    
    if len(result) > 0:
        user_data = result.iloc[0]
        user_data['home_locations'] = json.loads(user_data['home_locations'])
        user_data['common_devices'] = json.loads(user_data['common_devices'])
        return user_data
    return None

def get_user_stats(user_id):
    """Get user statistics"""
    conn = get_connection()
    
    total_logins = conn.execute('SELECT COUNT(*) FROM login_activities WHERE user_id = ?', [user_id]).fetchone()[0]
    high_risk = conn.execute('SELECT COUNT(*) FROM login_activities WHERE user_id = ? AND risk_percentage >= 70', [user_id]).fetchone()[0]
    countries = conn.execute('SELECT COUNT(DISTINCT country) FROM login_activities WHERE user_id = ?', [user_id]).fetchone()[0]
    avg_behavior = conn.execute('SELECT AVG(behavior_consistency) FROM login_activities WHERE user_id = ?', [user_id]).fetchone()[0]
    
    conn.close()
    
    return {
        'total_logins': total_logins,
        'high_risk': high_risk,
        'countries': countries,
        'avg_behavior': round(avg_behavior or 0)
    }

def get_user_location_patterns(user_id):
    """Get user's location patterns for analysis"""
    conn = get_connection()
    query = '''
        SELECT country, city, COUNT(*) as frequency,
               AVG(risk_percentage) as avg_risk,
               MIN(login_timestamp) as first_seen,
               MAX(login_timestamp) as last_seen
        FROM login_activities 
        WHERE user_id = ?
        GROUP BY country, city
        ORDER BY frequency DESC
    '''
    df = pd.read_sql_query(query, conn, params=[user_id])
    conn.close()
    return df

def get_user_device_patterns(user_id):
    """Get user's device usage patterns"""
    conn = get_connection()
    query = '''
        SELECT device_type, COUNT(*) as frequency,
               AVG(risk_percentage) as avg_risk,
               AVG(behavior_consistency) as avg_behavior
        FROM login_activities 
        WHERE user_id = ?
        GROUP BY device_type
        ORDER BY frequency DESC
    '''
    df = pd.read_sql_query(query, conn, params=[user_id])
    conn.close()
    return df

def get_user_risk_trends(user_id, days=30):
    """Get user's risk trends over time"""
    conn = get_connection()
    query = '''
        SELECT DATE(login_timestamp) as date,
               AVG(risk_percentage) as avg_risk,
               AVG(behavior_consistency) as avg_behavior,
               COUNT(*) as login_count
        FROM login_activities 
        WHERE user_id = ? AND login_timestamp >= datetime('now', '-{} days')
        GROUP BY DATE(login_timestamp)
        ORDER BY date
    '''.format(days)
    df = pd.read_sql_query(query, conn, params=[user_id])
    conn.close()
    
    if len(df) > 0:
        df['date'] = pd.to_datetime(df['date'])
    
    return df

if __name__ == "__main__":
    initialize_database()