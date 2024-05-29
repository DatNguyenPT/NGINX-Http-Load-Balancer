from flask import Flask
import os

app = Flask(__name__)

# Set the server ID from environment variable
serverID = os.getenv('SERVER_ID', 'Unknown')

@app.route('/')
def home():
    return f'This is server {serverID}'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
