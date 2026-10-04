import uvicorn
import os
import sys

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  🚀 PRAHAAR-AI | SIH26184 - Ministry of Home Affairs / I4C")
    print("  Predictive Analytics & ATM Cashout Interception Command Server")
    print("="*70)
    print("  📡 Tactical Cyber Command Center: http://localhost:8000")
    print("  📱 Field Beat Officer Interface: http://localhost:8000/field_officer.html")
    print("  📚 API Documentation: http://localhost:8000/docs")
    print("="*70 + "\n")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
