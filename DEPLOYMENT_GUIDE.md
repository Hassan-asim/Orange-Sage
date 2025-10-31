# 🚀 Orange Sage - Google Cloud Run Deployment Guide

This guide will help you deploy the Orange Sage application to Google Cloud Run using GitHub Actions.

## 📋 Prerequisites

1. **Google Cloud Project**
   - Project ID: `orangesage`
   - Project Number: `117299588539`
   - Region: `us-central1`

2. **Required APIs** (Enable these in Google Cloud Console)
   ```bash
   gcloud services enable cloudrun.googleapis.com
   gcloud services enable artifactregistry.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable secretmanager.googleapis.com
   ```

3. **Service Account** (Create with these roles)
   - Cloud Run Admin
   - Storage Admin
   - Artifact Registry Administrator
   - Service Account User

## 🔧 Setup Steps

### Step 1: Create Artifact Registry Repository

```bash
gcloud artifacts repositories create orange-sage \
  --repository-format=docker \
  --location=us-central1 \
  --description="Orange Sage Docker images"
```

### Step 2: Create Service Account

```bash
# Create service account
gcloud iam service-accounts create orange-sage-deployer \
  --display-name="Orange Sage Deployer"

# Get service account email
export SA_EMAIL=$(gcloud iam service-accounts list \
  --filter="displayName:Orange Sage Deployer" \
  --format='value(email)')

# Grant necessary roles
gcloud projects add-iam-policy-binding orangesage \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding orangesage \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding orangesage \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/artifactregistry.admin"

gcloud projects add-iam-policy-binding orangesage \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/iam.serviceAccountUser"

# Create and download key
gcloud iam service-accounts keys create key.json \
  --iam-account=$SA_EMAIL
```

### Step 3: Configure GitHub Secrets

Add these secrets to your GitHub repository (`Settings` → `Secrets and variables` → `Actions`):

#### Required Secrets:

1. **GCP_SA_KEY**
   - Content: Copy the entire content of `key.json`
   - This authenticates GitHub Actions with Google Cloud

2. **GCP_SERVICE_ACCOUNT_EMAIL**
   - Content: The service account email (from Step 2)
   - Example: `orange-sage-deployer@orangesage.iam.gserviceaccount.com`

3. **SECRET_KEY**
   - Content: A random secret key for JWT tokens
   - Generate with: `openssl rand -hex 32`
   - Example: `09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7`

4. **DATABASE_URL**
   - Content: Your database connection string
   - For SQLite (development): `sqlite:///./orange_sage.db`
   - For PostgreSQL (production): `postgresql://user:password@host:port/database`

5. **BACKEND_URL**
   - Content: Your backend URL (will be updated after first deployment)
   - Initial: `https://orange-sage-backend-<hash>.a.run.app`
   - You'll get this after first backend deployment

### Step 4: Update Backend CORS Settings

After deploying the backend, update `backend/app/core/config.py`:

```python
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://orange-sage-frontend-<your-hash>.a.run.app",  # Add your frontend URL
]
```

## 📦 Deployment Process

### Automatic Deployment

The application will automatically deploy when you push to the `main` branch:

- **Backend**: Triggers on changes to `backend/**`
- **Frontend**: Triggers on changes to `frontend/**`

### Manual Deployment

You can also trigger deployment manually from GitHub Actions:

1. Go to `Actions` tab in your repository
2. Select `Deploy Backend to Cloud Run` or `Deploy Frontend to Cloud Run`
3. Click `Run workflow`
4. Select the `main` branch
5. Click `Run workflow`

## 🔍 Verification

### Check Deployment Status

1. **GitHub Actions**
   - Go to `Actions` tab
   - View workflow runs and logs

2. **Google Cloud Console**
   ```bash
   # List Cloud Run services
   gcloud run services list --region=us-central1
   
   # Get backend URL
   gcloud run services describe orange-sage-backend \
     --region=us-central1 \
     --format='value(status.url)'
   
   # Get frontend URL
   gcloud run services describe orange-sage-frontend \
     --region=us-central1 \
     --format='value(status.url)'
   ```

3. **Test Endpoints**
   ```bash
   # Test backend health
   curl https://orange-sage-backend-<hash>.a.run.app/api/v1/health
   
   # Test frontend
   curl https://orange-sage-frontend-<hash>.a.run.app
   ```

## 🐛 Troubleshooting

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

### Common Issues

1. **Authentication Errors**
   - Verify `GCP_SA_KEY` is correct in GitHub Secrets
   - Check service account has necessary permissions

2. **Build Failures**
   - Check Dockerfile syntax
   - Verify dependencies in requirements.txt / package.json

3. **CORS Errors**
   - Update ALLOWED_ORIGINS in backend config
   - Redeploy backend after updating

4. **Database Connection**
   - Verify DATABASE_URL secret is correct
   - For Cloud SQL, ensure Cloud SQL Admin API is enabled

## 📊 Monitoring

### Cloud Run Metrics

View metrics in Google Cloud Console:
- Request count
- Request latency
- Container instance count
- Memory and CPU usage

### Set Up Alerts

```bash
# Create alert policy for high error rate
gcloud alpha monitoring policies create \
  --notification-channels=<CHANNEL_ID> \
  --display-name="High Error Rate" \
  --condition-display-name="Error rate > 5%" \
  --condition-threshold-value=0.05 \
  --condition-threshold-duration=300s
```

## 🔒 Security Best Practices

1. **Environment Variables**
   - Never commit secrets to Git
   - Use GitHub Secrets for sensitive data
   - Use Google Secret Manager for production secrets

2. **Service Accounts**
   - Use least-privilege principle
   - Rotate keys regularly
   - Use Workload Identity when possible

3. **Network Security**
   - Enable Cloud Armor for DDoS protection
   - Use VPC connectors for private resources
   - Implement rate limiting

## 💰 Cost Optimization

1. **Set Instance Limits**
   - Min instances: 0 (scales to zero)
   - Max instances: 10 (adjust based on traffic)

2. **Resource Allocation**
   - CPU: 1 vCPU
   - Memory: 512Mi
   - Timeout: 300s

3. **Monitor Costs**
   ```bash
   # View billing
   gcloud billing accounts list
   gcloud billing projects describe orangesage
   ```

## 🔄 CI/CD Pipeline

### Workflow Overview

1. **Code Push** → GitHub detects changes
2. **Build** → Docker image is built
3. **Push** → Image pushed to Artifact Registry
4. **Deploy** → Cloud Run service is updated
5. **Test** → Health check performed
6. **Notify** → Deployment status reported

### Customize Workflows

Edit `.github/workflows/deploy-backend.yml` or `.github/workflows/deploy-frontend.yml` to:
- Add tests before deployment
- Configure notifications (Slack, email)
- Add staging environment
- Implement blue-green deployment

## 📚 Additional Resources

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

## 🆘 Support

If you encounter issues:
1. Check GitHub Actions logs
2. Check Cloud Run logs
3. Verify all secrets are configured
4. Review this deployment guide
5. Contact the development team

---

**Project:** Orange Sage Security Platform  
**Cloud Provider:** Google Cloud Platform  
**Region:** us-central1  
**Last Updated:** $(date)

