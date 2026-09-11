import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

from flask import Flask, jsonify, render_template, request


def load_env_file():
    env_file = Path(__file__).resolve().parent / '.env'
    if not env_file.exists():
        return

    for line in env_file.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = [part.strip() for part in line.split('=', 1)]
        if value and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        os.environ.setdefault(key, value)


load_env_file()

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/health')
def health():
    return jsonify({
        'status': 'ok',
        'framework': 'Flask',
        'message': 'Portfolio API is running.'
    })


@app.route('/api/portfolio')
def portfolio():
    return jsonify({
        'name': 'Priyanka Priyadarshini Dalai',
        'title': 'AI & ML BTech Student',
        'bio': 'I build calm, practical AI experiences that turn ideas into tools people can use.',
        'projects': [
            {
                'name': 'Smart Resume Insight Dashboard',
                'description': 'A resume analysis tool that highlights strengths, skill gaps, and role-fit signals for candidates and recruiters.',
                'tags': ['Python', 'PyTorch', 'Flask']
            },
            {
                'name': 'AI Career Guidance App',
                'description': 'An interactive recommendation platform that maps skills, interests, and goals to career possibilities and learning paths.',
                'tags': ['React', 'Node.js', 'MongoDB']
            },
            {
                'name': 'Predictive Learning Analytics',
                'description': 'A machine learning system for understanding student performance patterns and forecasting improvement opportunities.',
                'tags': ['scikit-learn', 'Pandas', 'SQL']
            }
        ]
    })


@app.route('/api/contact', methods=['POST'])
def contact():
    payload = request.get_json(silent=True) or request.form or {}

    name = str(payload.get('name', '')).strip()
    email = str(payload.get('email', '')).strip()
    subject = str(payload.get('subject', '')).strip() or 'New portfolio inquiry'
    message = str(payload.get('message', '')).strip()
    query = str(payload.get('query', '')).strip()

    if not name or not email or not message:
        return jsonify({
            'success': False,
            'message': 'Name, email, and message are required.'
        }), 400

    full_message = query or 'No additional query provided.'

    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_user = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')
    recipient = os.getenv('MAIL_RECEIVER', 'priyankapriyadarshinidalai67@gmail.com')

    if not smtp_server or not smtp_user or not smtp_password:
        return jsonify({
            'success': False,
            'message': 'Email delivery is not configured yet. Add SMTP_SERVER, SMTP_USERNAME, and SMTP_PASSWORD in the .env file.'
        }), 500

    try:
        email_msg = EmailMessage()
        email_msg['Subject'] = f"Portfolio Contact: {subject}"
        email_msg['From'] = smtp_user
        email_msg['To'] = recipient
        email_msg.set_content(
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Subject: {subject}\n"
            f"Query: {full_message}\n\n"
            f"Message:\n{message}"
        )
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(email_msg)
    except Exception as exc:
        print(f'Email send failed: {exc}')
        return jsonify({
            'success': False,
            'message': 'Email delivery failed. Check your Gmail app password and SMTP settings.'
        }), 500

    print('--- New contact message ---')
    print(f'Name: {name}')
    print(f'Email: {email}')
    print(f'Subject: {subject}')
    print(f'Query: {full_message}')
    print(f'Message:\n{message}')

    return jsonify({
        'success': True,
        'message': 'Your message has been sent successfully. I will get back to you soon.'
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
