#!/usr/bin/env python3
"""
FlavorGraph Backend Startup Script
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    print("🍳 Starting FlavorGraph Backend Server...")
    print(f"📍 Server will run on: http://{host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/api/docs")
    print(f"🔄 Debug Mode: {debug}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info" if not debug else "debug"
    )
