"""
Flask Application Factory for Sales By Twilight API.

This module creates and configures the Flask application using the
application factory pattern for flexibility and testability.
"""

from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


def create_app(config_name=None):
    """
    Create and configure the Flask application.
    
    Args:
        config_name: Optional configuration name ('development', 'testing', 'production')
    
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    
    # ==========================================================================
    # CONFIGURATION
    # ==========================================================================
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'true').lower() == 'true'
    app.config['TESTING'] = config_name == 'testing'
    
    # JSON configuration
    app.config['JSON_SORT_KEYS'] = False  # Preserve key order in JSON responses
    
    # ==========================================================================
    # SWAGGER DOCUMENTATION
    # ==========================================================================
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.yaml'
    
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Sales By Twilight API",
            'validatorUrl': None
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    # ==========================================================================
    # REGISTER BLUEPRINTS - ALL ENTITY ROUTES
    # ==========================================================================
    from app.routes.category_routes import category_bp
    from app.routes.product_routes import product_bp
    from app.routes.customer_routes import customer_bp
    from app.routes.order_routes import order_bp
    
    app.register_blueprint(category_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(order_bp)
    
    # ==========================================================================
    # ROOT ENDPOINTS
    # ==========================================================================
    @app.route('/')
    def index():
        """API welcome endpoint with links to resources."""
        return jsonify({
            'success': True,
            'data': {
                'name': 'Sales By Twilight API',
                'version': '1.0.0',
                'description': 'REST API for grocery store e-commerce',
                'documentation': '/api/docs',
                'endpoints': {
                    'categories': '/categories',
                    'products': '/products',
                    'customers': '/customers (coming soon)',
                    'orders': '/orders (coming soon)'
                }
            }
        }), 200
    
    @app.route('/health')
    def health_check():
        """Health check endpoint for monitoring."""
        return jsonify({
            'success': True,
            'data': {
                'status': 'healthy',
                'service': 'Sales By Twilight API'
            }
        }), 200
    
    # ==========================================================================
    # ERROR HANDLERS
    # ==========================================================================
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return jsonify({
            'success': False,
            'error': {
                'code': 'NOT_FOUND',
                'message': 'The requested resource was not found'
            }
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 errors."""
        return jsonify({
            'success': False,
            'error': {
                'code': 'METHOD_NOT_ALLOWED',
                'message': 'The HTTP method is not allowed for this endpoint'
            }
        }), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An unexpected error occurred'
            }
        }), 500
    
    return app