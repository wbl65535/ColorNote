from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from app.config import get_config
from app.models import db

def create_app(config_name=None):
    """Application factory pattern for Flask app"""

    # Create Flask app instance
    app = Flask(__name__)

    # Load configuration
    config_class = get_config(config_name)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Enable CORS for API endpoints
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "https://*.vercel.app"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # Register error handlers
    @app.errorhandler(400)
    def bad_request(error):
        response = {
            "error": "Bad Request",
            "message": str(error) if app.config['DEBUG'] else "Invalid request data"
        }
        return jsonify(response), 400

    @app.errorhandler(404)
    def not_found(error):
        response = {
            "error": "Not Found",
            "message": "The requested resource was not found"
        }
        return jsonify(response), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        response = {
            "error": "Method Not Allowed",
            "message": "The HTTP method is not supported for this endpoint"
        }
        return jsonify(response), 405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        response = {
            "error": "Unprocessable Entity",
            "message": "Request data validation failed"
        }
        return jsonify(response), 422

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Internal server error: {error}")
        response = {
            "error": "Internal Server Error",
            "message": "An unexpected error occurred" if not app.config['DEBUG'] else str(error)
        }
        return jsonify(response), 500

    # Handle SQLAlchemy errors
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        # Log the full error for debugging
        app.logger.error(f"Unexpected error: {error}", exc_info=True)

        # Don't expose internal errors in production
        if app.config['DEBUG']:
            response = {
                "error": "Unexpected Error",
                "message": str(error),
                "type": error.__class__.__name__
            }
        else:
            response = {
                "error": "Unexpected Error",
                "message": "An unexpected error occurred. Please try again later."
            }

        return jsonify(response), 500

    # Register blueprints/routes
    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Health check endpoint
    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        return jsonify({
            "status": "healthy",
            "environment": app.config['FLASK_ENV']
        })

    # Main application route - serves the SPA
    @app.route('/')
    def index():
        """Serve the main application page"""
        return render_template('index.html')

    # Log configuration on startup
    app.logger.info(f"ColorNote app initialized with config: {config_class.__name__}")
    app.logger.info(f"Database URI configured: {'Yes' if app.config.get('SQLALCHEMY_DATABASE_URI') else 'No'}")

    return app
