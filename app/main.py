import sys
from pathlib import Path

# Add the root directory (parent of main.py) to sys.path
ROOT_DIR = Path(__file__).resolve().parent
sys.path.append(str(ROOT_DIR))

# Debugging: Print sys.path to ensure the root directory is included
print("Python module search paths:", sys.path)
from flask import Flask
from routes.file_routes import file_routes
from routes.payment_routes import payment_routes
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Register routes
app.register_blueprint(file_routes, url_prefix="/files")
app.register_blueprint(payment_routes, url_prefix="/payments")

if __name__ == "__main__":
    app.run(debug=True)
