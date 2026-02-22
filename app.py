from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import resend
import os


# Load environment variables


app = Flask(__name__, static_folder='.')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('.', path)

# Email configuration


resend.api_key = os.getenv("RESEND_API_KEY")

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        if not all([name, email, message]):
            return jsonify({"status": "error", "message": "Missing fields"}), 400

        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to":"dilfakottayil@gmail.com",
            "subject": f"New Portfolio Message from {name}",
            "html": f"""
                <h3>New Portfolio Message</h3>
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Message:</strong><br>{message}</p>
            """
        })

        return jsonify({"status": "success", "message": "NEW VERSION RUNNING"}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
