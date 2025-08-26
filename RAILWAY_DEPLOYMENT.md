# 🚀 Railway Deploy**Manual start:**
```bash
python -m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
```

## 📋 Prerequisiteside

This guide will help you deploy the Text-to-PowerPoint Generator to Railway.

## �️ Local Development

Before deploying, you can test locally:

**Windows:**
```bash
run_local.bat
```

**Unix/Linux/Mac:**
```bash
chmod +x run_local.sh
./run_local.sh
```

**Manual start:**
```bash
cd backend
python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

## �📋 Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **Git**: Make sure git is installed locally

## 🎯 Quick Deploy

### Option 1: Deploy from GitHub (Recommended)

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Text-to-PowerPoint Generator"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

2. **Deploy on Railway**:
   - Visit [railway.app](https://railway.app)
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will automatically detect the configuration and deploy

### Option 2: Railway CLI Deploy

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and Deploy**:
   ```bash
   railway login
   railway init
   railway up
   ```

## ⚙️ Configuration Files

The following files have been created for Railway deployment:

- **`railway.toml`**: Railway-specific configuration
- **`Dockerfile`**: Container configuration (backup method)
- **`nixpacks.toml`**: Nixpacks build configuration
- **`.gitignore`**: Excludes temporary files and secrets

## 🔧 Environment Variables

Railway will automatically set the `PORT` environment variable. No additional environment variables are required for the basic functionality.

## 🌐 Access Your Deployed App

After deployment:
1. Railway will provide you with a URL like `https://your-app-name.railway.app`
2. Access your application at that URL
3. The API health check will be available at `/api/health`

## 📝 Application Structure

```
your-domain.railway.app/
├── /                    # Frontend interface
├── /api/health         # Health check endpoint
└── /api/generate       # PowerPoint generation endpoint
```

## 🔒 Security Notes

- **API Keys**: Users provide their own API keys through the interface
- **No Storage**: API keys and uploaded files are not stored permanently
- **HTTPS**: Railway provides automatic HTTPS for all deployments

## 🐛 Troubleshooting

### Build Issues
- Check the Railway build logs in your dashboard
- Ensure `requirements.txt` includes all dependencies
- Verify Python version compatibility (using Python 3.11)
- Run `python test_railway.py` locally to test imports

### Runtime Issues
- Check the Railway deployment logs for detailed error messages
- Verify the health check endpoint responds: `/api/health`
- Ensure the PORT environment variable is being used correctly
- Look for import errors or missing dependencies in the logs

### Healthcheck Failures
If the healthcheck fails:
1. Check Railway logs for startup errors
2. Verify the app is binding to `0.0.0.0:$PORT`
3. Test locally with: `PORT=8000 python railway_start.py`
4. Ensure `/api/health` endpoint is accessible

### File Upload Issues
- Railway has file size limits for uploads
- Large PowerPoint templates (>10MB) may cause issues
- Consider optimizing template file sizes

## 📊 Monitoring

Railway provides:
- **Logs**: Real-time application logs
- **Metrics**: CPU, memory, and network usage
- **Health Checks**: Automatic monitoring of `/api/health`

## 💡 Production Tips

1. **Custom Domain**: Add your own domain in Railway dashboard
2. **Environment Variables**: Add any custom configuration through Railway UI
3. **Scaling**: Railway automatically handles scaling based on traffic
4. **Backups**: Keep your GitHub repository as your source of truth

## 🆘 Support

- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **Railway Discord**: Active community support
- **GitHub Issues**: Report application-specific issues

## 🎉 Post-Deployment

After successful deployment:
1. Test the application with sample content
2. Verify both OpenAI and Gemini providers work
3. Test PowerPoint generation with different templates
4. Share your deployed URL!

---

**Your app will be live at**: `https://[your-project-name].railway.app`
