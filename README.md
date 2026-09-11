# Priyanka Priyadarshini Dalai Portfolio

A modern portfolio website built with Flask, HTML, CSS, and a small React-powered section. The project includes a contact form that sends emails through Gmail SMTP.

## Features

- Responsive portfolio landing page
- About, Projects, Skills, Education, and Contact sections
- Contact form for messages and project inquiries
- GitHub and LinkedIn links
- Dark/light theme toggle
- Flask backend with API routes
- Gmail SMTP email delivery support

## Project Structure

- `app.py` — Flask application entry point
- `templates/` — HTML templates
- `static/assets/` — CSS, JavaScript, and static files
- `api/index.py` — Vercel serverless entry point
- `.env` — local environment variables (not committed)
- `.env.example` — sample environment file
- `requirements.txt` — Python dependencies
- `vercel.json` — Vercel deployment configuration

## Local Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file based on `.env.example`:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_google_app_password
MAIL_RECEIVER=your_receiver_email@gmail.com
```

4. Run the app:

```bash
python app.py
```

The app will be available at:

```text
http://127.0.0.1:5000
```

## Gmail SMTP Setup

Use a Google App Password for `SMTP_PASSWORD`.

1. Enable 2-Step Verification on your Google account.
2. Go to: https://myaccount.google.com/apppasswords
3. Generate a new app password for Mail
4. Copy the generated 16-character code into `SMTP_PASSWORD`

## Deployment

This project includes a Vercel configuration in `vercel.json` and a Python serverless entry in `api/index.py`.

Before deploying to Vercel, add these environment variables in the Vercel dashboard:

- `SMTP_SERVER`
- `SMTP_PORT`
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `MAIL_RECEIVER`

## License

This project is for personal portfolio use.
