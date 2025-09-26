# Flask Movie Recommendation App - Vercel Deployment

from flask import Flask
from app import app

# Vercel expects the Flask app to be available as 'app' variable
# This file serves as the entry point for Vercel deployment

if __name__ == "__main__":
    app.run()