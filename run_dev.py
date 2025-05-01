# run_dev.py
import subprocess
import os
import time
import signal
import sys

def main():
    print("Starting development servers...")
    print(f"Current directory: {os.getcwd()}")
    
    # Check if directories exist
    if not os.path.exists('Backend'):
        print("ERROR: 'Backend' directory not found!")
        return
    if not os.path.exists('Frontend'):
        print("ERROR: 'Frontend' directory not found!")
        return
    
    # Start the backend process
    print("Starting Flask server...")
    try:
        backend = subprocess.Popen(['python3', 'Backend/app.py'])
        print(f"Flask server started with PID: {backend.pid}")
    except Exception as e:
        print(f"Failed to start Flask server: {e}")
        return
    
    # Give the backend time to start
    time.sleep(2)
    
    # Start the frontend process
    print("Starting React development server...")
    try:
        os.chdir('Frontend')
        frontend = subprocess.Popen(['npm', 'start'])
        print(f"React server started with PID: {frontend.pid}")
        os.chdir('..')
    except Exception as e:
        print(f"Failed to start React server: {e}")
        backend.terminate()
        return
    
    print("Both servers started. Press Ctrl+C to stop.")
    
    # Handle graceful shutdown
    def signal_handler(sig, frame):
        print('\nShutting down...')
        backend.terminate()
        frontend.terminate()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('\nShutting down...')
        backend.terminate()
        frontend.terminate()
        sys.exit(0)

if __name__ == '__main__':
    main()