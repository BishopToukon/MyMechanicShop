import sys
import os

# Add project directory to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from App import create_app
from App.models import db

# Create Flask app
app = create_app()

if __name__ == "__main__":
    # Default port
    port = 5000

    # Allow overriding the port from the command line
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 5000.")

    # Create all tables
    with app.app_context():
        db.create_all()
        #db.drop_all()
        print("Database tables created.")

    print("Starting Flask app...")
    print(f"Running on http://127.0.0.1:{port}/ (Press CTRL+C to quit)")

    # Start Flask with chosen port
    app.run(debug=True, port=port)

