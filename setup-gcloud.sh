#!/bin/bash

# Orange Sage - Google Cloud Setup Script
# This script sets up the necessary Google Cloud resources for deployment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID="orangesage"
PROJECT_NUMBER="117299588539"
REGION="us-central1"
SERVICE_ACCOUNT_NAME="orange-sage-deployer"
ARTIFACT_REPO="orange-sage"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Orange Sage - Google Cloud Setup${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI is not installed${NC}"
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

echo -e "${YELLOW}1. Setting project...${NC}"
gcloud config set project $PROJECT_ID

echo -e "${YELLOW}2. Enabling required APIs...${NC}"
gcloud services enable cloudrun.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable secretmanager.googleapis.com
echo -e "${GREEN}✓ APIs enabled${NC}"

echo -e "${YELLOW}3. Creating Artifact Registry repository...${NC}"
if gcloud artifacts repositories describe $ARTIFACT_REPO --location=$REGION &> /dev/null; then
    echo -e "${GREEN}✓ Artifact Registry repository already exists${NC}"
else
    gcloud artifacts repositories create $ARTIFACT_REPO \
      --repository-format=docker \
      --location=$REGION \
      --description="Orange Sage Docker images"
    echo -e "${GREEN}✓ Artifact Registry repository created${NC}"
fi

echo -e "${YELLOW}4. Creating service account...${NC}"
if gcloud iam service-accounts describe ${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com &> /dev/null; then
    echo -e "${GREEN}✓ Service account already exists${NC}"
else
    gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME \
      --display-name="Orange Sage Deployer"
    echo -e "${GREEN}✓ Service account created${NC}"
fi

SERVICE_ACCOUNT_EMAIL="${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

echo -e "${YELLOW}5. Granting IAM roles...${NC}"
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
  --role="roles/run.admin" \
  --quiet

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
  --role="roles/storage.admin" \
  --quiet

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
  --role="roles/artifactregistry.admin" \
  --quiet

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
  --role="roles/iam.serviceAccountUser" \
  --quiet

echo -e "${GREEN}✓ IAM roles granted${NC}"

echo -e "${YELLOW}6. Creating service account key...${NC}"
KEY_FILE="gcp-key.json"
if [ -f "$KEY_FILE" ]; then
    echo -e "${YELLOW}⚠ Key file already exists. Skipping key creation.${NC}"
else
    gcloud iam service-accounts keys create $KEY_FILE \
      --iam-account=$SERVICE_ACCOUNT_EMAIL
    echo -e "${GREEN}✓ Service account key created: $KEY_FILE${NC}"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo ""
echo "1. Add the following secrets to your GitHub repository:"
echo "   (Settings → Secrets and variables → Actions → New repository secret)"
echo ""
echo -e "   ${YELLOW}GCP_SA_KEY${NC}"
echo "   Copy the entire content of: $KEY_FILE"
echo ""
echo -e "   ${YELLOW}GCP_SERVICE_ACCOUNT_EMAIL${NC}"
echo "   Value: $SERVICE_ACCOUNT_EMAIL"
echo ""
echo -e "   ${YELLOW}SECRET_KEY${NC}"
echo "   Generate with: openssl rand -hex 32"
echo ""
echo -e "   ${YELLOW}DATABASE_URL${NC}"
echo "   For SQLite: sqlite:///./orange_sage.db"
echo "   For PostgreSQL: postgresql://user:password@host:port/database"
echo ""
echo -e "   ${YELLOW}BACKEND_URL${NC}"
echo "   (Will be updated after first deployment)"
echo ""
echo "2. Push your code to the main branch to trigger deployment"
echo ""
echo "3. After backend deploys, get the URL with:"
echo "   gcloud run services describe orange-sage-backend \\"
echo "     --region=$REGION --format='value(status.url)'"
echo ""
echo "4. Update the BACKEND_URL secret with the backend URL"
echo ""
echo "5. Redeploy frontend to pick up the new backend URL"
echo ""
echo -e "${RED}⚠ IMPORTANT: Keep $KEY_FILE secure and never commit it to Git!${NC}"
echo ""

