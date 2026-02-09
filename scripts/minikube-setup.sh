#!/bin/bash
# ============================================
# Minikube Setup Script for Todo App
# Initializes Minikube and builds container images
# ============================================
set -e

echo "========================================="
echo "  Todo App - Minikube Setup"
echo "========================================="

# Step 1: Start Minikube
echo ""
echo "[1/5] Starting Minikube..."
if minikube status | grep -q "Running"; then
    echo "  Minikube is already running."
else
    minikube start --driver=docker --memory=4096 --cpus=2
    echo "  Minikube started successfully."
fi

# Step 2: Enable required addons
echo ""
echo "[2/5] Enabling Minikube addons..."
minikube addons enable ingress
minikube addons enable metrics-server
minikube addons enable dashboard
echo "  Addons enabled."

# Step 3: Configure Docker to use Minikube's daemon
echo ""
echo "[3/5] Configuring Docker environment..."
eval $(minikube docker-env)
echo "  Docker now points to Minikube's daemon."

# Step 4: Build Docker images inside Minikube
echo ""
echo "[4/5] Building Docker images..."
echo "  Building backend image..."
docker build -t todo-backend:latest ./backend

echo "  Building frontend image..."
docker build -t todo-frontend:latest \
  --build-arg NEXT_PUBLIC_API_URL=http://todo.local/api \
  ./frontend
echo "  Images built successfully."

# Step 5: Verify images
echo ""
echo "[5/5] Verifying images..."
docker images | grep todo

echo ""
echo "========================================="
echo "  Setup complete!"
echo "  Next: ./scripts/minikube-deploy.sh"
echo "========================================="
