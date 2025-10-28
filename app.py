from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)

# Allow your Netlify frontend
CORS(app, resources={r"/*": {"origins": "https://charming-quokka-d15fb8.netlify.app"}}, supports_credentials=True)

# Environment variables
BREVO_API_KEY = os.getenv('BREVO_API_KEY')   
TO_EMAIL = os.getenv('TO_EMAIL', 'sakthirollins175@gmail.com')
SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'sakthins20022002@gmail.com')  

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Flask backend is running ✅"}), 200


@app.route('/send-email', methods=['POST', 'OPTIONS'])
def send_email():
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'CORS preflight successful'})
        response.headers.add("Access-Control-Allow-Origin", "https://charming-quokka-d15fb8.netlify.app")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response, 200

    data = request.get_json()
    name = data.get('name')
    sender_email = data.get('email') 
    subject = data.get('subject', 'New Contact Form Submission')
    message = data.get('message')

    if not name or not sender_email or not message:
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400

    try:
        payload = {
            "sender": {"email": SENDER_EMAIL, "name": name}, 
            "replyTo": {"email": sender_email, "name": name}, 
            "to": [{"email": TO_EMAIL}],
            "subject": subject,
            "htmlContent": f"""
                <h3>New Contact Form Message</h3>
                <p><b>Name:</b> {name}</p>
                <p><b>Email:</b> {sender_email}</p>
                <p><b>Subject:</b> {subject}</p>
                <p><b>Message:</b><br>{message}</p>
            """
        }

        headers = {
            "accept": "application/json",
            "api-key": BREVO_API_KEY,
            "content-type": "application/json"
        }

        response = requests.post("https://api.brevo.com/v3/smtp/email", json=payload, headers=headers)

        if response.status_code == 201:
            res = jsonify({'success': True, 'message': 'Email sent successfully ✅'})
            res.headers.add("Access-Control-Allow-Origin", "https://charming-quokka-d15fb8.netlify.app")
            return res, 200
        else:
            print("❌ Brevo API error:", response.text)
            res = jsonify({'success': False, 'error': 'Email sending failed', 'details': response.text})
            res.headers.add("Access-Control-Allow-Origin", "https://charming-quokka-d15fb8.netlify.app")
            return res, 500

    except Exception as e:
        print('❌ Error:', e)
        res = jsonify({'success': False, 'error': str(e)})
        res.headers.add("Access-Control-Allow-Origin", "https://charming-quokka-d15fb8.netlify.app")
        return res, 500


if __name__ == '__main__':
    app.run(debug=True)
