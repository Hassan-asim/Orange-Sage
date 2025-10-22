# 🚀 Quick Start - Deploy Orange Sage to Google Cloud Run

## ✅ What's Already Done

All deployment configuration is ready:
- ✅ Dockerfiles for backend and frontend
- ✅ GitHub Actions CI/CD workflows
- ✅ Docker ignore files
- ✅ Next.js production configuration
- ✅ Comprehensive deployment guide

## 📋 Quick Setup (5 Steps)

### Step 1: Run Google Cloud Setup Script

On Linux/Mac:
```bash
chmod +x setup-gcloud.sh
./setup-gcloud.sh
```

On Windows (PowerShell - use Git Bash or WSL):
```bash
bash setup-gcloud.sh
```

**Or manually run these commands:**
```bash
# Set project
gcloud config set project orangesage

# Enable APIs
gcloud services enable cloudrun.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Create Artifact Registry
gcloud artifacts repositories create orange-sage \
  --repository-format=docker \
  --location=us-central1 \
  --description="Orange Sage Docker images"

# Create Service Account
gcloud iam service-accounts create orange-sage-deployer \
  --display-name="Orange Sage Deployer"

# Get service account email
gcloud iam service-accounts list

# Grant roles (replace <SA_EMAIL> with your service account email)
gcloud projects add-iam-policy-binding orangesage \
  --member="serviceAccount:<SA_EMAIL>" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding orangesage \
  --member="serviceAccount:<SA_EMAIL>" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding orangesage \
  --member="serviceAccount:<SA_EMAIL>" \
  --role="roles/artifactregistry.admin"

gcloud projects add-iam-policy-binding orangesage \
  --member="serviceAccount:<SA_EMAIL>" \
  --role="roles/iam.serviceAccountUser"

# Create key
gcloud iam service-accounts keys create gcp-key.json \
  --iam-account=<SA_EMAIL>
```

### Step 2: Configure GitHub Secrets

Go to: `https://github.com/Hassan-asim/Orange-Sage/settings/secrets/actions`

Click **"New repository secret"** for each:

1. **GCP_SA_KEY**
   ```bash
   # Copy the entire content of gcp-key.json
   cat gcp-key.json
   ```

2. **GCP_SERVICE_ACCOUNT_EMAIL**
   ```
   orange-sage-deployer@orangesage.iam.gserviceaccount.com
   ```

3. **SECRET_KEY**
   ```bash
   # Generate a random key
   openssl rand -hex 32
   ```

4. **DATABASE_URL**
   ```
   sqlite:///./orange_sage.db
   ```

5. **BACKEND_URL** (temporary - will update after deployment)
   ```
   http://localhost:8000
   ```

### Step 3: Trigger Deployment

Option A - Push to trigger automatic deployment:
```bash
# Make a small change to trigger deployment
git commit --allow-empty -m "Trigger deployment"
git push origin main
```

Option B - Manual trigger from GitHub:
1. Go to https://github.com/Hassan-asim/Orange-Sage/actions
2. Click "Deploy Backend to Cloud Run"
3. Click "Run workflow" → Select "main" → "Run workflow"
4. Wait for backend to deploy (~3-5 minutes)
5. Then deploy frontend the same way

### Step 4: Get Backend URL & Update Secrets

After backend deploys successfully:
```bash
# Get backend URL
gcloud run services describe orange-sage-backend \
  --region=us-central1 \
  --format='value(status.url)'

# Example output: https://orange-sage-backend-abc123-uc.a.run.app
```

**Update GitHub Secret:**
1. Go to repository secrets
2. Edit **BACKEND_URL**
3. Set value to the backend URL from above

### Step 5: Update CORS & Redeploy

Edit `backend/app/core/config.py` and add your frontend URL:

```python
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://orange-sage-frontend-abc123-uc.a.run.app",  # Add this
]
```

Commit and push:
```bash
git add backend/app/core/config.py
git commit -m "Update CORS for production frontend"
git push origin main
```

## 🎯 Access Your Deployed App

Get your URLs:
```bash
# Backend
gcloud run services describe orange-sage-backend \
  --region=us-central1 \
  --format='value(status.url)'

# Frontend
gcloud run services describe orange-sage-frontend \
  --region=us-central1 \
  --format='value(status.url)'
```

Visit your frontend URL and test:
- Login with: `user@gmail.com` / `12345678`
- Create projects, run scans, generate reports

## 📊 Monitor Deployment

### GitHub Actions
- https://github.com/Hassan-asim/Orange-Sage/actions

### Cloud Run Console
- https://console.cloud.google.com/run?project=orangesage

### View Logs
```bash
# Backend logs
gcloud run services logs read orange-sage-backend \
  --region=us-central1 \
  --limit=50

# Frontend logs  
gcloud run services logs read orange-sage-frontend \
  --region=us-central1 \
  --limit=50
```

## 🐛 Troubleshooting

### "Permission Denied" errors
- Verify service account has correct roles
- Check GCP_SA_KEY secret is properly formatted

### Build fails
- Check Dockerfile syntax
- Verify all dependencies are listed

### CORS errors
- Update ALLOWED_ORIGINS in backend/app/core/config.py
- Redeploy backend

### Can't access deployed app
- Check if service is allowing unauthenticated access:
  ```bash
  gcloud run services add-iam-policy-binding orange-sage-backend \
    --region=us-central1 \
    --member="allUsers" \
    --role="roles/run.invoker"
  ```

## 💰 Expected Costs

With default configuration (512Mi RAM, 1 CPU, scales to 0):
- **Free tier**: 2 million requests/month
- **After free tier**: ~$0.00002400 per request
- **Estimated cost**: $5-20/month for moderate traffic

## 🔒 Security Checklist

- ✅ Never commit `gcp-key.json` to Git
- ✅ Use GitHub Secrets for sensitive data
- ✅ Keep `SECRET_KEY` secret
- ✅ Enable Cloud Armor for DDoS protection
- ✅ Rotate service account keys regularly
- ✅ Monitor Cloud Run logs for suspicious activity

## 📚 Next Steps

1. Set up custom domain (optional)
2. Configure Cloud CDN (optional)
3. Set up monitoring & alerts
4. Configure Cloud SQL for production database
5. Implement CI/CD for staging environment

---

**Need Help?** Check the detailed [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)

**Project:** Orange Sage Security Platform  
**Repository:** https://github.com/Hassan-asim/Orange-Sage  
**Cloud Project:** orangesage (117299588539)

