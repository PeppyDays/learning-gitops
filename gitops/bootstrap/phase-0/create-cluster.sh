kind create cluster --name local --config local.yaml
kubectx kind-local
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
