from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

@app.route('/check-url', methods=['POST'])
def check_url():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    try:
        response = requests.get(url, timeout=5)
        return jsonify({
            "status_code": response.status_code,
            "status_message": response.reason
        })
    except requests.exceptions.MissingSchema:
        return jsonify({"status_message": "Invalid URL format", "status_code": 400})
    except requests.exceptions.ConnectionError:
        return jsonify({"status_message": "Site can't be reached", "status_code": 503})
    except requests.exceptions.Timeout:
        return jsonify({"status_message": "Request timed out", "status_code": 504})
    except requests.exceptions.RequestException as e:
        return jsonify({"status_message": "Unknown error: " + str(e), "status_code": 500})

if __name__ == '__main__':
    app.run(debug=True)
