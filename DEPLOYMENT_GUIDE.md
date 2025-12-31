# Deployment Guide - Website Organizer

## 🚀 Deploy to Render (Recommended - FREE)

### Step 1: Prepare Your Code
Your app is now ready for deployment! All necessary files are configured.

### Step 2: Push to GitHub
1. Create a new repository on GitHub
2. Initialize git in your project folder:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - ready for deployment"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

### Step 3: Deploy on Render
1. Go to [render.com](https://render.com) and sign up (free)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: website-organizer (or any name)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free
5. Add environment variable:
   - Key: `SECRET_KEY`
   - Value: Generate a random string (or use: `python -c "import secrets; print(secrets.token_hex(32))"`)
6. Click "Create Web Service"

Your app will be live at: `https://your-app-name.onrender.com`

**Note**: Free tier sleeps after 15 minutes of inactivity. First request after sleep takes ~30 seconds.

---

## 🐍 Alternative: Deploy to PythonAnywhere (FREE)

### Step 1: Sign Up
1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Create a free account (Beginner account)

### Step 2: Upload Your Files
1. Go to "Files" tab
2. Upload all your project files (or use git clone)

### Step 3: Setup Virtual Environment
Open a Bash console and run:
```bash
mkvirtualenv --python=/usr/bin/python3.10 myenv
pip install -r requirements.txt
```

### Step 4: Configure Web App
1. Go to "Web" tab → "Add a new web app"
2. Choose "Manual configuration" → Python 3.10
3. Set source code directory: `/home/yourusername/website-organizer`
4. Edit WSGI configuration file and replace content with:
```python
import sys
import os

project_home = '/home/yourusername/website-organizer'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

os.environ['SECRET_KEY'] = 'your-secret-key-here'

from app import app as application
```
5. Set virtualenv path: `/home/yourusername/.virtualenvs/myenv`
6. Click "Reload" button

Your app will be live at: `https://yourusername.pythonanywhere.com`

---

## ✈️ Alternative: Deploy to Fly.io (FREE with limitations)

### Step 1: Install Fly CLI
```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex
```

### Step 2: Login and Launch
```bash
fly auth login
fly launch
```

### Step 3: Configure
- Choose app name
- Select region closest to your users
- Don't add PostgreSQL (we're using SQLite)
- Deploy: Yes

Your app will be live at: `https://your-app-name.fly.dev`

---

## 📝 Important Notes

### Database Persistence
- **Render/Fly.io**: SQLite data may be lost on redeployment. For persistence, upgrade to PostgreSQL (paid) or use external database.
- **PythonAnywhere**: SQLite persists perfectly on free tier.

### Free Tier Limitations
- **Render**: 750 hours/month, sleeps after inactivity
- **PythonAnywhere**: Always on, but limited CPU
- **Fly.io**: 3 shared VMs, limited resources

### Environment Variables
Always set `SECRET_KEY` in production:
```python
# Generate secure key:
python -c "import secrets; print(secrets.token_hex(32))"
```

### Troubleshooting
- **App won't start**: Check logs on the platform dashboard
- **Database errors**: Ensure database is created (tables auto-create on first run)
- **Static files not loading**: Check static file paths in platform settings

---

## 🎉 You're Live!

Share your app URL with users. They can now:
- Organize their email IDs
- Track websites and accounts
- Never miss submission deadlines
- Plan their daily tasks

Need help? Check platform-specific documentation or create an issue on GitHub.
