from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "https://charming-quokka-d15fb8.netlify.app"}}, supports_credentials=True)

EMAIL_USER = os.getenv('EMAIL_USER', 'sakthins20022002@gmail.com')
EMAIL_PASS = os.getenv('EMAIL_PASS', 'pzwh gmzy wiyt klta')
TO_EMAIL = os.getenv('TO_EMAIL', 'sakthirollins175@gmail.com')

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Flask backend is running ✅"}), 200

@app.route('/send-email', methods=['POST', 'OPTIONS'])
def send_email():
    if request.method == 'OPTIONS':
        # Handles preflight request
        response = jsonify({'message': 'CORS preflight successful'})
        response.headers.add("Access-Control-Allow-Origin", "https://charming-quokka-d15fb8.netlify.app")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response, 200

    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    subject = data.get('subject', 'New Contact Form Submission')
    message = data.get('message')

    if not name or not email or not message:
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400

    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = TO_EMAIL
        msg['Subject'] = subject

        body = f"""
        You have a new message from your portfolio contact form:

        Name: {name}
        Email: {email}
        Subject: {subject}

        Message:
        {message}
        """
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        response = jsonify({'success': True})
        response.headers.add("Access-Control-Allow-Origin", "https://charming-quokka-d15fb8.netlify.app")
        return response, 200

    except Exception as e:
        print('Error:', e)
        response = jsonify({'success': False, 'error': str(e)})
        response.headers.add("Access-Control-Allow-Origin", "https://charming-quokka-d15fb8.netlify.app")
        return response, 500


if __name__ == '__main__':
    app.run(debug=True)
