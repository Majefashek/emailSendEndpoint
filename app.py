from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flasgger import Swagger, swag_from
from decouple import config

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'  
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = config('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = config('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = config('MAIL_USERNAME')
mail = Mail(app)

swagger = Swagger(app)

@app.route('/contact', methods=['POST'])
@swag_from({
    'tags': ['Contact'],
    'description': 'Send a message from the contact form.',
    'parameters': [
        {
            'name': 'name',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Your name'
        },
        {
            'name': 'email',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Your email address'
        },
        {
            'name': 'message',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Your message'
        }
    ],
    'responses': {
        200: {
            'description': 'Message sent successfully'
        },
        400: {
            'description': 'Invalid input'
        },
        500: {
            'description': 'Internal server error'
        }
    }
})

def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if not name or not email or not message:
        return jsonify({"error": "All fields are required."}), 400

    msg_to_recipient = Message('Contact Form Message', recipients=['info@asustudio.org'])
    msg_to_recipient.body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

    msg_to_sender = Message('Thank you for contacting us!', recipients=[email])
    msg_to_sender.body = (
        f"Hello {name},\n\n"
        "Thank you for reaching out to us. We have received your message:\n\n"
        "We will get back to you as soon as possible.\n\n"
        "Best regards,\n"
    )

    try:
        mail.send(msg_to_recipient)
        mail.send(msg_to_sender)
        return jsonify({"success":True
                        ,"message": "Message sent successfully"}), 200
    except Exception as e:
        return jsonify({"success":False,"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)