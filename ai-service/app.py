from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

USE_SIMPLE_DETECTOR = os.getenv('USE_SIMPLE_DETECTOR', 'false').lower() == 'true'

app = Flask(__name__)
CORS(app)

# Initialize the plagiarism detector
# Note: Initialization happens at import time, but we'll handle errors gracefully
detector = None

def initialize_detector():
    """Initialize the detector - called lazily or at startup"""
    global detector
    if detector is not None:
        return detector
    
    try:
        if USE_SIMPLE_DETECTOR:
            print("Initializing Simple Plagiarism Detector (low-memory mode)...")
            from simple_plagiarism_detector import SimplePlagiarismDetector
            detector = SimplePlagiarismDetector()
            print("✅ Simple detector initialized")
        else:
            print("Initializing Enhanced Plagiarism Detector...")
            try:
                from enhanced_plagiarism_detector import EnhancedPlagiarismDetector
                detector = EnhancedPlagiarismDetector()
                print("✅ Enhanced Plagiarism Detector initialized successfully")
            except ImportError:
                # Fallback to basic detector
                from plagiarism_detector import PlagiarismDetector
                detector = PlagiarismDetector()
                print("Plagiarism Detector initialized successfully (basic mode)")
    except Exception as e:
        print(f"⚠️ Failed to initialize Plagiarism Detector: {str(e)}")
        print("Please ensure all dependencies are installed: pip install -r requirements.txt")
        import traceback
        traceback.print_exc()
        detector = None
    
    return detector

# Try to initialize on startup (non-blocking)
try:
    initialize_detector()
except Exception as e:
    print(f"⚠️ Detector initialization failed, but app will continue: {e}")
    detector = None

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    current_detector = initialize_detector()
    if current_detector is None:
        return jsonify({
            'status': 'error',
            'message': 'Plagiarism Detector not initialized',
            'model_loaded': False
        }), 500
    
    return jsonify({
        'status': 'ok',
        'message': 'AI Plagiarism Detection Service is running',
        'model_loaded': current_detector.is_model_loaded() if hasattr(current_detector, 'is_model_loaded') else True
    })

@app.route('/check', methods=['POST'])
def check_plagiarism():
    """Check text for plagiarism"""
    try:
        current_detector = initialize_detector()
        if current_detector is None:
            return jsonify({
                'error': 'Plagiarism Detector not initialized. Please check the server logs.'
            }), 503
        
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        text = data['text']
        
        if not isinstance(text, str) or len(text.strip()) == 0:
            return jsonify({'error': 'Text must be a non-empty string'}), 400
        
        if len(text) > 10000:
            return jsonify({'error': 'Text is too long. Maximum 10,000 characters allowed.'}), 400
        
        # Detect plagiarism
        import time
        start_time = time.time()
        print(f"\n{'='*60}")
        print(f"PLAGIARISM CHECK REQUEST RECEIVED")
        print(f"Text length: {len(text)} characters")
        print(f"{'='*60}\n")
        
        result = current_detector.detect_plagiarism(text)
        
        elapsed_time = time.time() - start_time
        print(f"\n{'='*60}")
        print(f"PLAGIARISM CHECK COMPLETED")
        print(f"Total time: {elapsed_time:.2f} seconds")
        print(f"Plagiarism percentage: {result.get('plagiarism_percentage', 0):.1f}%")
        print(f"Matches found: {len(result.get('matches', []))}")
        print(f"{'='*60}\n")
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"Error in check_plagiarism: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'An error occurred while checking plagiarism',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    # Render automatically sets PORT environment variable
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Starting Flask app on port {port}")
    print(f"📡 Host: 0.0.0.0")
    print(f"🐛 Debug mode: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)

