# 🚀 Deploy Timesheet Anomaly Radar to Render

This guide will help you deploy your Timesheet Anomaly Radar to Render for free, creating a shareable link.

## 📋 Prerequisites

1. **GitHub Account** - You'll need to push your code to GitHub
2. **Render Account** - Sign up at [render.com](https://render.com) (free)

## 🔧 Step-by-Step Deployment

### Step 1: Push to GitHub

1. **Initialize Git** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Timesheet Anomaly Radar"
   ```

2. **Create GitHub Repository**:
   - Go to [github.com](https://github.com)
   - Click "New repository"
   - Name it `timesheet-anomaly-radar`
   - Make it public
   - Don't initialize with README

3. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/timesheet-anomaly-radar.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy to Render

1. **Sign up/Login to Render**:
   - Go to [render.com](https://render.com)
   - Sign up with your GitHub account

2. **Create New Web Service**:
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repository
   - Select `timesheet-anomaly-radar`

3. **Configure the Service**:
   - **Name**: `timesheet-anomaly-radar`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

4. **Deploy**:
   - Click "Create Web Service"
   - Wait for deployment (2-3 minutes)

### Step 3: Access Your Deployed App

Once deployed, you'll get a URL like:
```
https://timesheet-anomaly-radar.onrender.com
```

## 🌐 Share Your App

### API Endpoints:
- **Health Check**: `https://your-app.onrender.com/api/health`
- **Get Anomalies**: `https://your-app.onrender.com/api/anomalies`
- **Record Decision**: `https://your-app.onrender.com/api/decision`

### Dashboard:
- **Main Dashboard**: `https://your-app.onrender.com/dashboard.html`

## 🔍 Testing Your Deployment

1. **Test Health Endpoint**:
   ```bash
   curl https://your-app.onrender.com/api/health
   ```

2. **Test Anomalies Endpoint**:
   ```bash
   curl https://your-app.onrender.com/api/anomalies
   ```

3. **Test with Filters**:
   ```bash
   curl "https://your-app.onrender.com/api/anomalies?team=Support"
   ```

## 📊 Features Available in Deployment

✅ **52 Synthetic Anomalies** - Realistic timesheet data  
✅ **Team Filtering** - Filter by Support, Engineering, Sales, Finance  
✅ **Date Filtering** - Filter by specific dates  
✅ **Decision Recording** - Approve, Escalate, or Dismiss anomalies  
✅ **Interactive Dashboard** - Beautiful web interface  
✅ **API Documentation** - Available at `/docs`  

## 🎯 Demo Scenarios

### For HR Managers:
- Review high-severity anomalies (score > 1.5)
- Filter by team to focus on specific departments
- Record decisions with notes for audit trail

### For IT Teams:
- Test API endpoints programmatically
- Integrate with existing HR systems
- Build custom dashboards

### For Business Stakeholders:
- View anomaly patterns across teams
- Understand timesheet compliance issues
- See the potential for automation

## 🔧 Customization

### Add More Anomalies:
Edit `data.csv` to add more realistic data or different anomaly types.

### Modify Anomaly Rules:
Update the anomaly detection logic in `app.py` to match your business rules.

### Custom Dashboard:
Modify `dashboard.html` to add charts, different filters, or branding.

## 🚨 Troubleshooting

### Common Issues:

1. **Build Fails**: Check that all dependencies are in `requirements.txt`
2. **App Won't Start**: Verify the start command uses `$PORT`
3. **CORS Errors**: The app includes CORS middleware for cross-origin requests
4. **Slow Loading**: Free tier has cold starts - first request may be slow

### Support:
- Check Render logs in the dashboard
- Verify all files are committed to GitHub
- Test locally first with `uvicorn app:app --reload`

## 🎉 Success!

Once deployed, you'll have a professional, shareable demo of your Timesheet Anomaly Radar that showcases:

- **Machine Learning Integration** with HR workflows
- **Modern API Design** with FastAPI
- **Beautiful User Interface** for non-technical users
- **Real-world Applicability** for HR automation

Share your link with colleagues, stakeholders, or potential clients to demonstrate the power of AI-driven HR tools! 