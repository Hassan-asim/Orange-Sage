#!/bin/bash
set -e

echo "🚀 Starting Orange Sage with Litestream..."

# Restore database from Google Cloud Storage if it exists
if [ -n "$LITESTREAM_GCS_BUCKET" ]; then
    echo "📦 Restoring database from GCS bucket: $LITESTREAM_GCS_BUCKET"
    litestream restore -if-replica-exists -config /app/litestream.yml /app/orange_sage.db || echo "⚠️  Restore failed or no backup exists, will create new DB"
    echo "✅ Database restored (or created if first run)"
else
    echo "⚠️  LITESTREAM_GCS_BUCKET not set, running without replication"
fi

# Initialize demo user (don't fail if user already exists)
echo "👤 Creating demo user..."
python init_demo_user.py || echo "⚠️  Demo user creation failed (may already exist)"

# Start Litestream replication in background
if [ -n "$LITESTREAM_GCS_BUCKET" ]; then
    echo "🔄 Starting Litestream replication..."
    litestream replicate -config /app/litestream.yml &
    LITESTREAM_PID=$!
    echo "✅ Litestream running (PID: $LITESTREAM_PID)"
fi

# Start the FastAPI application
echo "🌟 Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}

