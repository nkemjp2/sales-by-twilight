"""
Entry point for Sales By Twilight API.
Run this file to start the Flask application.
"""

from app import create_app

# Create the Flask application instance
app = create_app()

if __name__ == '__main__':
    # Run the application
    # debug=True enables auto-reload and detailed error pages
    # host='0.0.0.0' makes the server accessible externally
    # port=5001 is the default Flask port
    app.run(debug=True, host='0.0.0.0', port=5001)