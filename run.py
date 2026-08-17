import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables
load_dotenv()

# Get configuration from environment
config_name = os.environ.get('FLASK_ENV', 'development')

# Create app
app = create_app(config_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
