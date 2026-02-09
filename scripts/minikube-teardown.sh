#!/bin/bash
# ============================================
# Cleanup - removes all Todo app resources
# ============================================
set -e

echo "Removing Todo App from Minikube..."

# Try Helm first
if helm list -n todo-app 2>/dev/null | grep -q todo-app; then
    echo "Uninstalling Helm release..."
    helm uninstall todo-app -n todo-app
else
    echo "Removing kubectl resources..."
    kubectl delete -f k8s/ --namespace=todo-app --ignore-not-found=true
fi

# Delete namespace
kubectl delete namespace todo-app --ignore-not-found=true

echo "Cleanup complete."
