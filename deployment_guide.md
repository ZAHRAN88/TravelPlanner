# Deployment Guide - Kemet Travel API

This guide will help you deploy your Flask application to Render.com for free.

## Prerequisites

1. Create a [Render.com](https://render.com) account
2. Install Git if you haven't already
3. Create a GitHub repository for your project

## Step 1: Prepare Your Application

1. First, create a `requirements.txt` file in your project root:

```bash
pip freeze > requirements.txt
```

2. Create a `gunicorn_config.py` file:

```python
bind = "0.0.0.0:10000"
workers = 2
threads = 4
timeout = 120
```

3. Modify your `main.py` to use environment variables:

```python
# Add at the top of main.py
import os
from dotenv import load_dotenv

load_dotenv()

# Replace the API key configuration
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Modify the run statement at the bottom
if __name__ == '__main__':
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
```

## Step 2: Create Configuration Files

1. Create a `.gitignore` file:

```
__pycache__/
*.pyc
.env
venv/
.DS_Store
```

2. Create a `render.yaml` file:

```yaml
services:
  - type: web
    name: kemet-travel-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn main:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.8.0
      - key: GEMINI_API_KEY
        sync: false
```

## Step 3: Deploy to Render

1. Push your code to GitHub:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. Deploy on Render.com:

   a. Go to [Render Dashboard](https://dashboard.render.com)
   b. Click "New +"
   c. Select "Web Service"
   d. Connect your GitHub repository
   e. Fill in the following details:
      - Name: kemet-travel-api
      - Environment: Python
      - Build Command: `pip install -r requirements.txt`
      - Start Command: `gunicorn main:app`
   f. Add environment variables:
      - GEMINI_API_KEY: Your Google Gemini API key
   g. Click "Create Web Service"

## Step 4: Update API Documentation

Update your base URL in `api_documentation.md` to point to your Render URL:

```markdown
## Base URL
```
https://kemet-travel-api.onrender.com/api
```

## Important Notes

1. **Free Tier Limitations:**
   - The free tier may sleep after 15 minutes of inactivity
   - Limited to 750 hours per month
   - Automatic HTTPS/SSL provided
   - Limited to 100 GB bandwidth per month

2. **Environment Variables:**
   - Never commit your `.env` file
   - Set environment variables in Render.com dashboard
   - Keep your API keys secure

3. **Monitoring:**
   - Use Render's built-in logs for monitoring
   - Set up health check endpoint monitoring
   - Monitor API usage to stay within free tier limits

4. **Performance Tips:**
   - Keep response times under 30 seconds
   - Implement caching for frequently accessed data
   - Use compression for large responses

## Troubleshooting

1. **Application Not Starting:**
   - Check Render logs for errors
   - Verify environment variables are set
   - Ensure `requirements.txt` is complete

2. **API Key Issues:**
   - Verify API key is set in Render environment variables
   - Check API key permissions and quotas

3. **Performance Issues:**
   - Monitor response times in Render dashboard
   - Check for memory leaks
   - Implement caching if needed

## Maintenance

1. **Updates:**
   - Push changes to GitHub
   - Render will automatically redeploy
   - Monitor deployment logs

2. **Monitoring:**
   - Set up uptime monitoring
   - Monitor API usage
   - Check error logs regularly

3. **Backup:**
   - Keep local backups of your code
   - Document all configuration changes
   - Maintain deployment documentation

## Security Best Practices

1. **API Security:**
   - Consider adding rate limiting
   - Implement CORS properly
   - Use HTTPS only (provided by Render)

2. **Data Protection:**
   - Never expose sensitive data in logs
   - Sanitize user inputs
   - Implement request validation

3. **Access Control:**
   - Consider adding authentication
   - Implement API keys for production
   - Monitor for suspicious activity 