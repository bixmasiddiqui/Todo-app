#!/bin/bash
# ============================================
# DigitalOcean DOKS Deployment Script
# Prerequisites: doctl CLI, DOKS cluster, DOCR registry
# ============================================
set -e

REGISTRY="registry.digitalocean.com/todo-app"
CLUSTER_NAME="todo-app-cluster"

echo "========================================="
echo "  Todo App - DigitalOcean DOKS Deploy"
echo "========================================="

# Step 1: Connect to DOKS cluster
echo "[1/6] Connecting to DOKS cluster..."
doctl kubernetes cluster kubeconfig save $CLUSTER_NAME

# Step 2: Build and push images to DOCR
echo "[2/6] Building and pushing images..."
docker build -t $REGISTRY/todo-backend:latest ./backend
docker build -t $REGISTRY/todo-frontend:latest \
  --build-arg NEXT_PUBLIC_API_URL=https://api.todo.yourdomain.com \
  ./frontend
docker push $REGISTRY/todo-backend:latest
docker push $REGISTRY/todo-frontend:latest

# Step 3: Create registry secret
echo "[3/6] Creating registry secret..."
doctl registry kubernetes-manifest | kubectl apply -f -

# Step 4: Install Dapr
echo "[4/6] Installing Dapr..."
dapr init -k --wait

# Step 5: Apply Dapr components
echo "[5/6] Applying Dapr components..."
kubectl apply -f dapr/config.yaml
kubectl apply -f dapr/components/

# Step 6: Deploy application
echo "[6/6] Deploying application..."
kubectl apply -f digitalocean/k8s/

echo ""
echo "Deployment complete!"
echo "Check status: kubectl get pods -n todo-app"
