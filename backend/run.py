import uvicorn
import os
import sys

# Ensure backend folder is in python module path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    print("Initializing MSME Decision Support System Backend server...")
    print("API interactive documentation available at http://127.0.0.1:8000/docs")
    
    # Run the uvicorn development server
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
