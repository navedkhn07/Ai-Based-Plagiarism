#!/usr/bin/env python3
"""
Quick test script to verify the AI service is working
"""

import requests
import json
import sys

AI_SERVICE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("Testing AI Service Health...")
    try:
        response = requests.get(f"{AI_SERVICE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['message']}")
            print(f"   Model loaded: {data.get('model_loaded', False)}")
            return True
        else:
            print(f"❌ Health check failed: Status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to AI service at {AI_SERVICE_URL}")
        print("   Make sure the AI service is running: cd ai-service && python app.py")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_plagiarism_check():
    """Test the plagiarism check endpoint"""
    print("\nTesting Plagiarism Check...")
    test_text = "This is a sample text to test the plagiarism checker. It contains multiple sentences to verify that the system works correctly."
    
    try:
        response = requests.post(
            f"{AI_SERVICE_URL}/check",
            json={"text": test_text},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Plagiarism check passed!")
            print(f"   Similarity Score: {data.get('similarity_score', 0):.2f}%")
            print(f"   Plagiarism Percentage: {data.get('plagiarism_percentage', 0):.2f}%")
            print(f"   Matches Found: {len(data.get('matches', []))}")
            print(f"   Analysis Items: {len(data.get('analysis', []))}")
            return True
        else:
            print(f"❌ Plagiarism check failed: Status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to AI service at {AI_SERVICE_URL}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("AI Service Test Script")
    print("=" * 50)
    
    health_ok = test_health()
    
    if health_ok:
        check_ok = test_plagiarism_check()
        
        if check_ok:
            print("\n" + "=" * 50)
            print("✅ All tests passed! AI service is working correctly.")
            print("=" * 50)
            sys.exit(0)
        else:
            print("\n" + "=" * 50)
            print("❌ Plagiarism check test failed.")
            print("=" * 50)
            sys.exit(1)
    else:
        print("\n" + "=" * 50)
        print("❌ Health check failed. Please start the AI service first.")
        print("=" * 50)
        print("\nTo start the AI service:")
        print("  cd ai-service")
        print("  python app.py")
        print("=" * 50)
        sys.exit(1)

