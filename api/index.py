"""
Vercel API Entry Point for ColorNote
"""

from app import create_app

# Create Flask application instance for Vercel
app = create_app()

# Vercel will automatically handle the Flask app
# This file serves as the entry point for all API routes
