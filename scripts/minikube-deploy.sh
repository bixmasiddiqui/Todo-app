#!/bin/bash
# ============================================
# Minikube Deploy Script
# Usage: ./scripts/minikube-deploy.sh [--helm]
# ============================================
set -e

USE_HELM=false
if [ "$1" == "--helm" ]; then
    USE_HELM=true
fi

echo "========================================="
echo "  Todo App - Deploying to Minikube"
echo "========================================="

# Ensure Minikube Docker env
eval $(minikube docker-env)

if [ "$USE_HELM" = true ]; then
    echo ""
    echo "Deploying with Helm..."

    # Encode DATABASE_URL from backend/.env
    if [ -f backend/.env ]; then
        DB_URL=$(grep DATABASE_URL backend/.env | cut -d '=' -f2-)
        DB_URL_B64=$(echo -n "$DB_URL" | base64)
    else
        echo "ERROR: backend/.env not found. Create it with DATABASE_URL."
        exit 1
    fi

    helm upgrade --install todo-app ./helm/todo-app \
        --namespace todo-app \
        --create-namespace \
        --set secrets.databaseUrl="$DB_URL_B64" \
        -f ./helm/todo-app/values-dev.yaml

else
    echo ""
    echo "Deploying with kubectl manifests..."

    # Create namespace
    kubectl apply -f k8s/namespace.yaml

    # Encode DATABASE_URL and apply secret
    if [ -f backend/.env ]; then
        DB_URL=$(grep DATABASE_URL backend/.env | cut -d '=' -f2-)
        DB_URL_B64=$(echo -n "$DB_URL" | base64)
        sed "s|DATABASE_URL:.*|DATABASE_URL: $DB_URL_B64|" k8s/secret.yaml | kubectl apply -f -
    else
        echo "WARNING: backend/.env not found."
        kubectl apply -f k8s/secret.yaml
    fi

    # Apply remaining resources
    kubectl apply -f k8s/configmap.yaml
    kubectl apply -f k8s/backend-deployment.yaml
    kubectl apply -f k8s/frontend-deployment.yaml
    kubectl apply -f k8s/ingress.yaml
fi

echo ""
echo "Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=todo-app \
    --namespace=todo-app --timeout=120s

MINIKUBE_IP=$(minikube ip)
echo ""
echo "========================================="
echo "  Deployment complete!"
echo ""
echo "  Add to hosts file:"
echo "    $MINIKUBE_IP todo.local"
echo ""
echo "  Access:"
echo "    Frontend: http://todo.local"
echo "    Backend:  http://todo.local/api/todos"
echo "    API Docs: http://todo.local/docs"
echo ""
echo "  NodePort (alternative):"
echo "    Frontend: http://$MINIKUBE_IP:30300"
echo "    Backend:  http://$MINIKUBE_IP:30800"
echo "========================================="
