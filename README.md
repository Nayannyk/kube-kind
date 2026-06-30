# Kube Kind

A project containing two components: a **Flask web app** that renders an SVG sketch of the Taj Mahal, and a **kind cluster automation** tool that provisions an AWS EC2 instance and bootstraps a local kind Kubernetes cluster.

---

## Directory Tree

```
kube-kind/
├── python/
│   ├── kind_cluster_automation.py   # AWS EC2 + kind cluster automation CLI
│   ├── test_ssh2.py                 # SSH connectivity test
│   └── test_ssh3.py                 # SSH connectivity test
├── k8s/                             # Placeholder for Kubernetes manifests
├── Dockerfile                       # Docker image for the Flask app
├── gunicorn.conf.py                 # Gunicorn server configuration
├── main.py                          # Flask application (Taj Mahal SVG)
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

---

## Part 1: Flask Taj Mahal Web App

A Python Flask application that serves an SVG illustration of the Taj Mahal using Gunicorn as the WSGI server.

### Prerequisites

- Python 3.8+
- pip
- Docker (optional, for containerized deployment)

### Setup & Run Locally

```bash
# Create virtual environment (recommended)
python -m venv venv
.\venv\Scripts\Activate   # Windows
# source venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Run the Flask dev server
python main.py

# Or run with Gunicorn (production-style)
gunicorn --bind :8080 --workers 2 --threads 25 main:app
```

Open http://localhost:8080 in your browser.

### Run with Docker

```bash
# Build the image
docker build -t kube-kind-app .

# Run the container
docker run -d -p 8080:8080 kube-kind-app
```

### Application Dependencies

| Package   | Version | Purpose              |
|-----------|---------|----------------------|
| Flask     | 2.3.3   | Web framework        |
| gunicorn  | 21.2.0  | WSGI HTTP server     |
| futures   | 3.0.5   | Thread pool (compat) |

> The Dockerfile strips `futures` via `grep -v` since it is unnecessary on Python 3.

---

## Part 2: Kind Cluster Automation

A CLI tool that automates provisioning an AWS EC2 Ubuntu instance and bootstrapping a kind Kubernetes cluster with 1 control-plane and 2 worker nodes.

### Prerequisites

- AWS CLI installed and configured (`aws configure`)
- An EC2 key pair (default name: `Nayan`)
- Python 3.8+
- SSH client

### Usage

```bash
cd python

# Create the EC2 instance and kind cluster
python kind_cluster_automation.py apply

# Use defaults without prompts
python kind_cluster_automation.py apply -y

# Terminate the EC2 instance and destroy the cluster
python kind_cluster_automation.py destroy
```

### How It Works

1. **Launch** a `t2.medium` Ubuntu 24.04 EC2 instance (defaults to `ap-south-1`)
2. **Install** Docker, kind (v0.29.0), and kubectl (latest stable) on the instance
3. **Create** a kind cluster with a 3-node config (1 control-plane + 2 workers) using `kindest/node:v1.35.1`
4. **Outputs** the instance ID, public IP, and SSH command for further access

### Configuration Defaults

| Setting              | Default Value                                   |
|----------------------|-------------------------------------------------|
| AWS region           | `ap-south-1`                                    |
| Instance type        | `t2.medium`                                     |
| Root volume size     | 20 GB (gp3)                                     |
| Key pair name        | `Nayan`                                         |
| PEM file path        | `~/Downloads/Nayan.pem`                         |
| Security group       | `kind-cluster-sg` (ports 22,80,443,3000,3306,5000,9090) |
| SSH user             | `ubuntu`                                        |
| Instance name tag    | `kind-instance`                                 |

### SSH Connectivity Tests

Two test scripts are included to verify SSH access to a running instance:

```bash
cd python
python test_ssh2.py
python test_ssh3.py
```

> **Note:** These scripts hardcode the IP `52.66.70.3` — update it to match your instance's public IP.
