✅ Stage 1 — Basic application

React + FastAPI + SQLite

- Basic product management
- Product listing
- Order creation
- Inventory/stock reduction
- Order listing
- Basic API models
- Basic frontend

✅ Stage 2 — Docker

Learn:
- images
- containers
- Dockerfile
- Docker Compose
- container networking
- volumes
- environment variables

Containerize:
- frontend
- backend
- database

🟡 Stage 3 — Kafka

Learn:

✅producer
✅consumer
✅topic
partitions
consumer groups
offsets
✅basic delivery concepts

Then integrate it into the marketplace.

🔵 Stage 4 — Kubernetes

Learn:

✅Cluster
Done — local Kubernetes cluster running


✅Node
Done — inspected the cluster node


✅Pod
Done — inspected, deleted and replaced Pods


✅Deployment
Done — deployed the backend and Kafka


✅Replicas
Practised scaling the backend up and down


✅Service
Done — backend and Kafka have Services


✅ConfigMap
Done — Kafka configuration supplied through a ConfigMap


Secret
Created a demonstration Secret; actual use not yet implemented


✅Persistent storage
Done — PVC, database migration and data verification


Ingress
Not done


Full application deployment
Partial — frontend and consumer are not yet deployed in Kubernetes

Deploy our little application locally.

☁️ Stage 5 — GCP

Learn:

projects
regions/zones
IAM
compute
Cloud SQL
Cloud Storage
GKE
basic networking

Then deploy some/all of the project.

🟣 Stage 6 — Airflow

Build a DAG:

fetch order data
       ↓
transform
       ↓
calculate daily stats
       ↓
generate report
       ↓
store report
🧹 Stage 6 — Make it presentable
