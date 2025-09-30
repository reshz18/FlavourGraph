#!/usr/bin/env python3
"""
FlavorGraph Project Startup Script
Starts both Python backend and Next.js frontend
"""

import subprocess
import sys
import os
import time
import threading
from pathlib import Path

def run_backend():
    """Start the Python backend server"""
    print("🐍 Starting Python Backend...")
    backend_dir = Path(__file__).parent / "backend"
    
    try:
        # Change to backend directory
        os.chdir(backend_dir)
        
        # Start the backend server
        subprocess.run([sys.executable, "run.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Backend failed to start: {e}")
    except KeyboardInterrupt:
        print("🛑 Backend stopped by user")

def run_frontend():
    """Start the Next.js frontend server"""
    print("⚛️ Starting Next.js Frontend...")
    project_dir = Path(__file__).parent
    
    try:
        # Change to project directory
        os.chdir(project_dir)
        
        # Start the frontend server
        subprocess.run(["npm", "run", "dev"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Frontend failed to start: {e}")
    except KeyboardInterrupt:
        print("🛑 Frontend stopped by user")

def check_dependencies():
    """Check if all dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python dependencies
    backend_dir = Path(__file__).parent / "backend"
    requirements_file = backend_dir / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ Backend requirements.txt not found!")
        return False
    
    # Check Node.js dependencies
    project_dir = Path(__file__).parent
    package_json = project_dir / "package.json"
    node_modules = project_dir / "node_modules"
    
    if not package_json.exists():
        print("❌ Frontend package.json not found!")
        return False
    
    if not node_modules.exists():
        print("⚠️ Node modules not found. Run 'npm install' first.")
        return False
    
    print("✅ Dependencies check passed!")
    return True

def setup_backend():
    """Setup Python backend environment"""
    print("🔧 Setting up Python backend...")
    backend_dir = Path(__file__).parent / "backend"
    
    # Check if virtual environment exists
    venv_dir = backend_dir / "venv"
    if not venv_dir.exists():
        print("📦 Creating Python virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
    
    # Install requirements
    if sys.platform == "win32":
        pip_path = venv_dir / "Scripts" / "pip.exe"
        python_path = venv_dir / "Scripts" / "python.exe"
    else:
        pip_path = venv_dir / "bin" / "pip"
        python_path = venv_dir / "bin" / "python"
    
    if pip_path.exists():
        print("📦 Installing Python dependencies...")
        subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], 
                      cwd=backend_dir, check=True)
        return str(python_path)
    else:
        print("⚠️ Using system Python")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      cwd=backend_dir, check=True)
        return sys.executable

def main():
    """Main startup function"""
    print("🍳 FlavorGraph: Intelligent Recipe Navigator")
    print("=" * 50)
    print("🧠 Powered by Graph Theory, Backtracking & Greedy Algorithms")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependency check failed. Please install dependencies first.")
        print("\nFor backend:")
        print("  cd backend")
        print("  python -m venv venv")
        print("  venv\\Scripts\\activate  # Windows")
        print("  # source venv/bin/activate  # macOS/Linux")
        print("  pip install -r requirements.txt")
        print("\nFor frontend:")
        print("  npm install")
        return
    
    try:
        # Setup backend
        python_path = setup_backend()
        
        print("\n🚀 Starting FlavorGraph servers...")
        print("📍 Backend will run on: http://localhost:8000")
        print("📍 Frontend will run on: http://localhost:3000")
        print("📚 API Documentation: http://localhost:8000/api/docs")
        print("\n⚠️ Press Ctrl+C to stop both servers")
        
        # Start backend in a separate thread
        backend_thread = threading.Thread(target=run_backend, daemon=True)
        backend_thread.start()
        
        # Wait a moment for backend to start
        time.sleep(3)
        
        # Start frontend (this will block)
        run_frontend()
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down FlavorGraph servers...")
        print("👋 Thank you for using FlavorGraph!")

if __name__ == "__main__":
    main()
