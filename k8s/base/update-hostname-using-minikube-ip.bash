MINIKUBE_IP=$(minikube ip)
sed "s/<MINIKUBE_IP>/$MINIKUBE_IP/" webserver-ingress.yaml | kubectl apply -f -