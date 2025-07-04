# opentelemetry-py
A Flask-based web server instrumented with OpenTelemetry, designed to demonstrate observability best practices across the software delivery lifecycle—from local development to production-ready deployments in Kubernetes.

This repository highlights a progressive approach to implementing distributed tracing, metrics, and logging with modern tooling and automation.

## Project Overview
This project is designed to:

* Showcase practical use of OpenTelemetry (tracing, metrics, logging)
* Demonstrate containerization and Kubernetes deployment patterns
* Implement CI/CD pipelines using GitOps tools
* Integrate a full observability stack suitable for modern microservices

## Staged Roadmap
### Stage 1: Local Instrumentation
- Develop a minimal Flask web server
- Instrument the application with OpenTelemetry SDK:

    - Traces
    - Metrics
    - Logs

- Output telemetry data to the console

<b> Objective: </b>
Demonstrate local observability integration using a lightweight Python service.

### Stage 2: Containerization and Deployment
- Dockerize the application
- Define Kubernetes manifests or Helm charts
- Deploy to a Kubernetes cluster
- Integrate ArgoCD for GitOps-driven continuous deployment

<b> Objective: </b>
Transition to a production-like environment with automated infrastructure management.

### Stage 3: Full Observability Integration
- Export telemetry data to an OpenTelemetry Collector
- Integrate with backends:
    - Traces: Jaeger or Tempo
    - Metrics: Prometheus
    - Visualization: Grafana

- Implement contextual logging and custom application metrics

<b> Objective: </b>
Establish a complete observability pipeline across the application and infrastructure layers.

### Stage 4: Production Readiness
- Add application health endpoints and probes
- Secure communication with TLS/mTLS where appropriate
- Configure Kubernetes RBAC and network policies

<b> Objective: </b>
Enhance reliability and security to meet production-grade standards.

### Stage 5: Performance and Optimization
- Conduct load testing using tools like Locust or k6
- Use trace and metrics data to identify performance bottlenecks
- Optimize application code and Kubernetes resources based on findings

<b> Objective: </b>
Apply telemetry-driven insights to improve performance and scalability.

### Stage 6: Autoscaling and Alerting
- Enable Horizontal Pod Autoscaling based on Prometheus metrics
- Define Service Level Objectives (SLOs) and Indicators (SLIs)
- Configure alerting rules and integrate with notification systems

<b> Objective: </b>
Make observability actionable by enabling dynamic scaling and proactive monitoring.

## Project structure
```bash
opentelemetry-py/
├── app/                    # Flask application code
├── test/                   # Unit, load and other tests
├── Dockerfile              # Container build file
├── k8s/                    # Kubernetes manifests or Helm charts
├── ci/                     # CI/CD pipeline definitions
├── telemetry/              # OpenTelemetry Collector and backend config
└── README.md
````

## Tech Stack

- Language: Python (Flask)
- Observability: OpenTelemetry SDK, Jaeger, Prometheus, Grafana
- Infrastructure: Docker, Kubernetes (minikube)
- CI/CD: ArgoCD, GitHub Actions or Google Cloud Build
- Load Testing: k6, Locust

## How to Build and Run

This project includes both a Flask app instrumented with OpenTelemetry and an OpenTelemetry Collector configured to receive and export telemetry data.

### Using Docker Compose 

To build and run both services in local docker:

```bash
docker-compose up --build
````

This will:

- Build the Flask application container
- Start both flask-app and otel-collector services
- Bind the Flask app to http://localhost:8080

### Using minikube 

To build and run the services within Minikube:

```bash
eval $(minikube docker-env)
minikube start
docker build -t opentelemetry-py:latest . #Now you can build image and it will go into minikube registry
````

To enable a dashboard for better visibility:

```bash
minikube dashboard
````

Then deploy Kubernetes manifests under k8s/base folder using default namespace:

```bash
kubectl apply -f k8/base/
````

To access local services:

```bash
kubectl port-forward svc/opentelemetry-py-svc 8080:8080
kubectl port-forward svc/otel-collector 8889:8889
````

Finally access: http://localhost:8080

## How to secure the app for external traffic

Install cert-manager:

```bash
cd k8s/tls
bash cert-manager-installation.bash
````

Install NGINX Ingress Controller ( reverse proxy and load balancer):

```bash
minikube addons enable ingress
kubectl get svc -n ingress-nginx
````

Create ClusterIssuer for Let's Encrypt:

```bash
cd k8s/tls

# Remember to update script with your email before running
bash lets-encrypt-email-replacement.bash
````

Update webserver-ingress.yaml with minikube IP and apply changes:

```bash
cd k8s/base

# Remember to update script with your email before running
bash update-hostname-using-minikube-ip.bash
````

Finally, create a tunnel to expose Load Balancer IP:

```bash
minikube tunnel
````

Try access: https://opentelemetry-py.<MINIKUBE_IP>.nip.io

### Deploying via Argo CD 
If Argo CD is already installed, publish the application using:

```bash
kubectl apply -f ci/
````

To access the Argo CD UI locally:

```bash
kubectl port-forward svc/argocd-server -n argocd 8090:443
````

Then log in:

```bash
argocd login localhost:8090 --username admin --password <password> --insecure
````

## Scrape otel-collector with Prometheus and visualization with Grafana

Install prometheus-community chart

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace
````

Create a serviceMonitor to scrape OpenTelemetry Collector:
```bash
kubectl apply -f k8s/monitor/otel-collector-monitor.yaml
````

Start grafana using:
```bash
kubectl port-forward svc/kube-prometheus-stack-grafana -n monitoring 3000:80
````

Access Grafana: http://localhost:3000

Start prometheus using:
```bash
kubectl port-forward svc/kube-prometheus-stack-prometheus -n monitoring 9090:9090
````

Access Prometheus: http://localhost:9090

## Troubleshooting and monitoring

To verify traces, metrics and logs are being received by otel-collector:

```bash
kubectl logs deployment/otel-collector -f 
````

To analize issues with certificates and challenges:

```bash
kubectl get certificates
kubectl describe certificate flask-tls

kubectl get orders
kubectl describe order <name>

kubectl get challenges
kubectl describe challenge <name>

kubectl get certificaterequests
kubectl describe certificaterequest <name>

kubectl logs -n cert-manager -l app.kubernetes.io/name=cert-manager --follow
````