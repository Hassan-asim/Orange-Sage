#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🗄️  Setting up Litestream with Google Cloud Storage${NC}"
echo ""

# Configuration
PROJECT_ID="orangesage"
BUCKET_NAME="orange-sage-litestream-db"
REGION="us-central1"
SERVICE_ACCOUNT_EMAIL="orange-sage-deployer@orangesage.iam.gserviceaccount.com"

echo -e "${YELLOW}Configuration:${NC}"
echo "  Project ID: $PROJECT_ID"
echo "  Bucket Name: $BUCKET_NAME"
echo "  Region: $REGION"
echo "  Service Account: $SERVICE_ACCOUNT_EMAIL"
echo ""

# Step 1: Create GCS bucket
echo -e "${BLUE}📦 Step 1: Creating GCS bucket...${NC}"
if gsutil ls -b gs://$BUCKET_NAME 2>/dev/null; then
    echo -e "${GREEN}✅ Bucket already exists${NC}"
else
    gsutil mb -p $PROJECT_ID -l $REGION gs://$BUCKET_NAME
    echo -e "${GREEN}✅ Bucket created${NC}"
fi

# Step 2: Set bucket permissions for service account
echo -e "${BLUE}🔐 Step 2: Setting bucket permissions...${NC}"
gsutil iam ch serviceAccount:$SERVICE_ACCOUNT_EMAIL:roles/storage.objectAdmin gs://$BUCKET_NAME
echo -e "${GREEN}✅ Permissions set${NC}"

# Step 3: Enable versioning (for backup safety)
echo -e "${BLUE}🔄 Step 3: Enabling versioning...${NC}"
gsutil versioning set on gs://$BUCKET_NAME
echo -e "${GREEN}✅ Versioning enabled${NC}"

# Step 4: Set lifecycle rule (optional - keep last 30 days of backups)
echo -e "${BLUE}🗑️  Step 4: Setting lifecycle rules...${NC}"
cat > /tmp/lifecycle.json << EOF
{
  "lifecycle": {
    "rule": [
      {
        "action": {
          "type": "Delete"
        },
        "condition": {
          "age": 30,
          "isLive": false
        }
      }
    ]
  }
}
EOF
gsutil lifecycle set /tmp/lifecycle.json gs://$BUCKET_NAME
rm /tmp/lifecycle.json
echo -e "${GREEN}✅ Lifecycle rules set (keeps old versions for 30 days)${NC}"

echo ""
echo -e "${GREEN}✅ Litestream GCS setup complete!${NC}"
echo ""
echo -e "${YELLOW}📝 Next steps:${NC}"
echo "1. Add this GitHub Secret:"
echo "   Name: LITESTREAM_GCS_BUCKET"
echo "   Value: $BUCKET_NAME"
echo ""
echo "2. Run: git add . && git commit -m 'Add Litestream for SQLite persistence' && git push origin main"
echo ""
echo -e "${BLUE}💰 Cost estimate: ~\$0.02/month for storage${NC}"

