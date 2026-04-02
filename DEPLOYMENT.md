# Deployment Guide - Streamlit Cloud

This guide will help you deploy the Interview Performance Recording System to Streamlit Cloud.

## Prerequisites

- GitHub account (create one at https://github.com/signup if needed)
- Streamlit Cloud account (free tier available at https://streamlit.io/cloud)
- Git installed on your computer

## Step 1: Create a GitHub Repository

1. Go to https://github.com/new
2. Create a new repository:
   - **Repository name**: `interview-performance-system`
   - **Description**: `AI-powered interview performance recording and analysis system`
   - **Visibility**: Public
   - Click **Create repository**

## Step 2: Push Code to GitHub

In your project folder (via Terminal/PowerShell):

```powershell
# Initialize git (if not already done)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Navigate to project
cd C:\Users\Vir\Desktop\interview_performance_project\interview_performance_project

# Initialize git repo
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Interview Performance Recording System"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/interview-performance-system.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Deploy to Streamlit Cloud

1. **Visit** https://share.streamlit.io
2. **Sign in** with your GitHub account
3. **Click** "New app"
4. **Configure**:
   - **Repository**: Select `your-username/interview-performance-system`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. **Click** "Deploy"

Streamlit Cloud will:

- Install dependencies from `requirements.txt`
- Start your app automatically
- Give you a public URL (e.g., `https://interview-system.streamlit.app`)

## Step 4: Configure Streamlit Secrets (if needed)

If your app needs API keys or environment variables:

1. In Streamlit Cloud dashboard → Your app → Settings
2. Add secrets in the **Secrets** section
3. Secrets will be available as `st.secrets.get()`

## Accessing Your Deployed App

Once deployed:

- **Live URL**: https://interview-system.streamlit.app (or your custom domain)
- **Share with others**: Just share the URL!
- **Monitor logs**: Use Streamlit Cloud dashboard
- **View analytics**: Dashboard shows usage stats

## Troubleshooting

### Camera Not Working on Streamlit Cloud

Streamlit Cloud runs on Linux servers without camera hardware. The app will:

- Still load successfully
- Show a message if camera access is attempted
- Work with pre-recorded data

### Dependencies Installation Failure

If `torch` fails to install:

- Edit `requirements.txt` to remove `torch`
- Use lightweight alternatives or CPU-only version
- Streamlit Cloud deployment automatically retries

### App Runs Slowly

- Streamlit Cloud free tier has resource limits
- Consider optimizing:
  - Reduce video frame size
  - Cache computed results
  - Use smaller models

## File Structure

Required files for deployment:

```
interview-performance-project/
├── app.py                          # Main Streamlit app
├── requirements.txt                # Dependencies
├── .streamlit/
│   └── config.toml                # Streamlit config
├── .gitignore                      # Git ignore patterns
├── src/
│   ├── config.py
│   ├── predict.py
│   ├── train.py
│   └── ...
├── artifacts/
│   └── best_interview_performance_model.joblib
└── data/
    └── interview_powerbi_source.csv
```

## Updates & Redeployment

To update your deployed app:

```powershell
# Make changes locally
# Then push to GitHub:
git add .
git commit -m "Update description"
git push origin main
```

Streamlit Cloud will automatically **redeploy** within seconds!

## Support

- **Streamlit Docs**: https://docs.streamlit.io
- **Streamlit Cloud**: https://share.streamlit.io
- **Community**: https://discuss.streamlit.io

---

✅ Your app is now deployable to Streamlit Cloud!
