from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- 1. THE DATA ---
try:
    # Try to load the CSV you made
    df = pd.read_csv('borrowers.csv')
    logger.info(f"Successfully loaded borrowers.csv with {len(df)} records")
except Exception as e:
    # Failsafe if CSV is missing - MOCK DATA
    logger.warning(f"CSV not found ({e}), using Mock Data")
    data = {
        'member_id': [101, 102, 103], 
        'annual_inc': [55000, 120000, 35000], 
        'fico_range_high': [680, 790, 550],
        'loan_amnt': [10000, 25000, 5000]
    }
    df = pd.DataFrame(data)

# --- 2. THE ENDPOINTS ---

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify service is running"""
    return jsonify({
        "status": "healthy",
        "service": "Credit Risk API",
        "records_loaded": len(df)
    }), 200

@app.route('/get_data', methods=['POST'])
def get_data():
    """Step 1: Retrieve user credit data by member_id"""
    try:
        # Validate request has JSON body
        if not request.json:
            logger.error("No JSON body provided")
            return jsonify({"error": "Request must include JSON body"}), 400
        
        content = request.json
        
        # Validate member_id is provided
        if 'member_id' not in content:
            logger.error("Missing member_id in request")
            return jsonify({"error": "member_id is required"}), 400
        
        user_id = content.get('member_id')
        logger.info(f"Received request for User: {user_id}")
        
        # Validate member_id is numeric
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            logger.error(f"Invalid member_id format: {user_id}")
            return jsonify({"error": "member_id must be a valid integer"}), 400
        
        # Look up user in DataFrame
        user = df[df['member_id'] == user_id]
        if user.empty:
            logger.warning(f"User not found: {user_id}")
            return jsonify({"error": "User not found"}), 404
        
        # Convert numpy types to native python types for JSON serialization
        result = user.iloc[0].to_dict()
        for key, val in result.items():
            if pd.isna(val):
                result[key] = None
            elif hasattr(val, 'item'):  # numpy types
                result[key] = val.item()
        
        logger.info(f"Successfully retrieved data for user {user_id}")
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Unexpected error in get_data: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/risk_score', methods=['POST'])
def risk_score():
    """Step 2: Calculate risk score based on FICO and income"""
    try:
        # Validate request has JSON body
        if not request.json:
            logger.error("No JSON body provided")
            return jsonify({"error": "Request must include JSON body"}), 400
        
        content = request.json
        
        # Validate required fields
        if 'fico_range_high' not in content:
            logger.error("Missing fico_range_high in request")
            return jsonify({"error": "fico_range_high is required"}), 400
        
        if 'annual_inc' not in content:
            logger.error("Missing annual_inc in request")
            return jsonify({"error": "annual_inc is required"}), 400
        
        # Parse and validate inputs
        try:
            fico = float(content.get('fico_range_high'))
            income = float(content.get('annual_inc'))
        except (ValueError, TypeError) as e:
            logger.error(f"Invalid numeric values: {e}")
            return jsonify({"error": "fico_range_high and annual_inc must be valid numbers"}), 400
        
        # Validate FICO range (300-850 is standard range)
        if fico < 300 or fico > 850:
            logger.warning(f"FICO score out of typical range: {fico}")
        
        # Validate income is positive
        if income < 0:
            logger.error(f"Invalid negative income: {income}")
            return jsonify({"error": "annual_inc must be positive"}), 400
        
        logger.info(f"Calculating risk for FICO: {fico}, Income: {income}")
        
        # Logic: Higher FICO = Lower Score (Risk)
        base_score = 100 - (fico / 8.5) 
        if income > 80000:
            base_score -= 15
            
        final_score = max(0, min(100, base_score))
        
        # Categorize risk: Low (0-30), Medium (30-60), High (60-100)
        if final_score < 30:
            risk_category = "Low"
        elif final_score < 60:
            risk_category = "Medium"
        else:
            risk_category = "High"
        
        logger.info(f"Risk calculated: {final_score:.2f} ({risk_category})")
        
        return jsonify({
            "risk_score": round(final_score, 2),
            "risk_category": risk_category
        }), 200
        
    except Exception as e:
        logger.error(f"Unexpected error in risk_score: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/calc_ecl', methods=['POST'])
def calc_ecl():
    """Step 3: Calculate Expected Credit Loss"""
    try:
        # Validate request has JSON body
        if not request.json:
            logger.error("No JSON body provided")
            return jsonify({"error": "Request must include JSON body"}), 400
        
        content = request.json
        
        # Validate required fields
        if 'loan_amnt' not in content:
            logger.error("Missing loan_amnt in request")
            return jsonify({"error": "loan_amnt is required"}), 400
        
        if 'risk_score' not in content:
            logger.error("Missing risk_score in request")
            return jsonify({"error": "risk_score is required"}), 400
        
        # Parse and validate inputs
        try:
            loan = float(content.get('loan_amnt'))
            score = float(content.get('risk_score'))
        except (ValueError, TypeError) as e:
            logger.error(f"Invalid numeric values: {e}")
            return jsonify({"error": "loan_amnt and risk_score must be valid numbers"}), 400
        
        # Validate loan amount is positive
        if loan < 0:
            logger.error(f"Invalid negative loan amount: {loan}")
            return jsonify({"error": "loan_amnt must be positive"}), 400
        
        # Validate risk_score range (0-100)
        if score < 0 or score > 100:
            logger.error(f"Risk score out of range: {score}")
            return jsonify({"error": "risk_score must be between 0 and 100"}), 400
        
        logger.info(f"Calculating ECL for Loan: {loan}, Risk Score: {score}")
        
        # Logic: Expected Loss = Loan * (Risk / 100)
        loss = loan * (score / 100)
        
        logger.info(f"Expected Credit Loss calculated: ${loss:.2f}")
        
        return jsonify({
            "expected_credit_loss": round(loss, 2),
            "currency": "USD"
        }), 200
        
    except Exception as e:
        logger.error(f"Unexpected error in calc_ecl: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    logger.info("="*50)
    logger.info("CREDIT RISK API SERVER STARTING")
    logger.info("="*50)
    logger.info(f"Loaded {len(df)} borrower records")
    logger.info("Endpoints available:")
    logger.info("  GET  /health      - Health check")
    logger.info("  POST /get_data    - Retrieve user data")
    logger.info("  POST /risk_score  - Calculate risk score")
    logger.info("  POST /calc_ecl    - Calculate expected credit loss")
    logger.info("="*50)
    app.run(host='0.0.0.0', port=5000, debug=False)