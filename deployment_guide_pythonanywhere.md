# Deploying to PythonAnywhere (Free, No Credit Card Required)

## Free Tier Features
- 512 MB storage
- One Python web app
- HTTPS/SSL included
- Custom domain support (yourusername.pythonanywhere.com)
- Always-on service (no sleep like other free tiers)
- Console access

## Step 1: Setup PythonAnywhere Account

1. Go to [PythonAnywhere](https://www.pythonanywhere.com) and create a free account
2. After signing up, you'll be taken to the dashboard

## Step 2: Upload Your Code

### Option 1: Using Git (Recommended)
1. Click on "Consoles" and start a new Bash console
2. Clone your repository:
```bash
git clone https://github.com/yourusername/your-repo-name.git
```

### Option 2: Manual Upload
1. Go to "Files" tab
2. Click "Upload a file"
3. Upload all your project files

## Step 3: Setup Virtual Environment

In the Bash console:
```bash
# Create virtual environment
mkvirtualenv --python=/usr/bin/python3.8 kemet-env

# Activate virtual environment
workon kemet-env

# Install requirements
pip install -r requirements.txt

# Additionally install gunicorn (if not in requirements.txt)
pip install gunicorn
```

## Step 4: Configure Web App

1. Go to the "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select Python 3.8
5. Note the path of your virtual environment shown in the configuration page

## Step 5: Configure WSGI File

1. Click on the WSGI configuration file link in the Web tab
2. Replace the contents with:

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/yourusername/your-repo-name'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['GEMINI_API_KEY'] = 'your_api_key_here'

# Import your Flask app
from main import app as application
```

## Step 6: Set Static Files (if any)

In the Web tab, add any static file mappings if needed:
- URL: /static/
- Directory: /home/yourusername/your-repo-name/static

## Step 7: Set Environment Variables

1. Go to the "Files" tab
2. Create a `.env` file in your project directory:
```
GEMINI_API_KEY=your_api_key_here
```

## Step 8: Update Application Code

1. Modify your `main.py` to work with PythonAnywhere:
```python
# At the bottom of main.py
if __name__ == '__main__':
    if os.getenv('PYTHONANYWHERE_SITE'):
        # Running on PythonAnywhere
        app.run()
    else:
        # Running locally
        app.run(debug=True)
```

## Step 9: Reload Web App

1. Go back to the "Web" tab
2. Click the "Reload" button for your web app

## Your API is Now Live!

Your API will be available at:
```
https://yourusername.pythonanywhere.com/api
```

## Free Tier Limitations
- 512 MB storage
- Limited CPU seconds
- One web app
- Restricted outbound network access (whitelist available)

## Maintenance Tips

1. **Updating Code:**
```bash
# In PythonAnywhere bash console
cd your-repo-name
git pull
# Then reload the web app from Web tab
```

2. **Checking Logs:**
- Access logs from the "Web" tab
- Error log and access log available

3. **Database:**
- Free MySQL database available
- Access via "Databases" tab

## Troubleshooting

1. **App Not Loading:**
- Check error logs in Web tab
- Verify virtual environment path
- Check WSGI file configuration

2. **Import Errors:**
- Verify all requirements are installed
- Check virtual environment activation
- Confirm Python version compatibility

3. **API Key Issues:**
- Verify environment variables in WSGI file
- Check .env file exists and is properly formatted

## Advantages Over Other Platforms

1. **No Credit Card Required**
2. **Always On** (no sleep after inactivity)
3. **Reliable Free Tier**
4. **Built-in SSL/HTTPS**
5. **Simple deployment process**
6. **Web-based console access**
7. **Free MySQL database**

## Updating Your API Documentation

Update your base URL in `api_documentation.md`:
```markdown
## Base URL
```
https://yourusername.pythonanywhere.com/api
```

## Additional Resources
- [PythonAnywhere Help Pages](https://help.pythonanywhere.com/)
- [PythonAnywhere Forums](https://www.pythonanywhere.com/forums/)
- [Flask on PythonAnywhere Guide](https://help.pythonanywhere.com/pages/Flask/) 