#!/usr/bin/env python3
"""
Production start script for Render deployment
This ensures the PORT environment variable is properly read
"""
import os
import subprocess
import sys

def main():
    # Get PORT from environment (Render sets this automatically)
    port = os.environ.get('PORT', '8000')
    
    print(f"🚀 Starting AI Plagiarism Service on port {port}")
    print(f"📡 Environment: {os.environ.get('RENDER', 'Not on Render')}")
    
    # Build gunicorn command
    cmd = [
        'gunicorn',
        'app:app',
        '--bind', f'0.0.0.0:{port}',
        '--workers', '2',
        '--timeout', '120',
        '--access-logfile', '-',
        '--error-logfile', '-'
    ]
    
    print(f"🔧 Running: {' '.join(cmd)}")
    
    # Run gunicorn
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

