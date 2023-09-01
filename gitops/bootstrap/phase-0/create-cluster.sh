kind create cluster --name local --config local.yaml

if [ $? -ne 0 ]; then
  echo "Error creating Kubernetes cluster. Exiting."
  exit 1
fi

kubectx kind-local

if [ $? -ne 0 ]; then
  echo "kubectx returns an error. Exiting."
  exit 1
fi

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
