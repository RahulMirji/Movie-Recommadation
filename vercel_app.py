# Flask Movie Recommendation App - Vercel Deployment Entry Point

# Import the Flask application from our main app.py file
from app import app

# Vercel expects the Flask app to be available as 'app' variable
# This file serves as the entry point for Vercel serverless deployment

# The app is already configured in app.py, we just need to expose it
# No need to run app.run() here as Vercel handles the server

if __name__ == "__main__":
    # This will only run locally, not on Vercel
    app.run(debug=False)