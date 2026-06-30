import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path


DEFAULTS = {
    "region": "ap-south-1",
    "instance_type": "t2.medium",
    "volume_size": 20,
    "key_name": "Nayan",
    "pem_path": str(Path.home() / "Downloads" / "Nayan.pem"),
    "security_group_name": "kind-cluster-sg",
    "instance_name": "kind-instance",
    "ssh_user": "ubuntu",
    "ami_parameter": "/aws/service/canonical/ubuntu/server/24.04/stable/current/amd64/hvm/ebs-gp3/ami-id",
    "sg_open_ports": [22, 80, 443, 3000, 3306, 5000, 9090],
}


KIND_CONFIG = """kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
    image: kindest/node:v1.35.1
  - role: worker
    image: kindest/node:v1.35.1
  - role: worker
    image: kindest/node:v1.35.1
"""


REMOTE_INSTALL_SCRIPT = f"""#!/bin/bash
set -euo pipefail

echo "Installing Docker, kind, and kubectl..."

sudo apt-get update -y
sudo apt-get install -y ca-certificates curl

if ! command -v docker >/dev/null 2>&1; then
  sudo install -m 0755 -d /etc/apt/keyrings
  sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
  sudo chmod a+r /etc/apt/keyrings/docker.asc
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt-get update -y
  sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
fi

sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"

if ! command -v kind >/dev/null 2>&1; then
  ARCH=$(uname -m)
  if [ "$ARCH" = "x86_64" ]; then
    curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.29.0/kind-linux-amd64
  elif [ "$ARCH" = "aarch64" ]; then
    curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.29.0/kind-linux-arm64
  else
    echo "Unsupported architecture: $ARCH"
    exit 1
  fi
  chmod +x ./kind
  sudo mv ./kind /usr/local/bin/kind
fi

if ! command -v kubectl >/dev/null 2>&1; then
  ARCH=$(uname -m)
  VERSION=$(curl -Ls https://dl.k8s.io/release/stable.txt)
  if [ "$ARCH" = "x86_64" ]; then
    curl -Lo ./kubectl "https://dl.k8s.io/release/${{VERSION}}/bin/linux/amd64/kubectl"
  elif [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
    curl -Lo ./kubectl "https://dl.k8s.io/release/${{VERSION}}/bin/linux/arm64/kubectl"
  else
    echo "Unsupported architecture: $ARCH"
    exit 1
  fi
  chmod +x ./kubectl
  sudo mv ./kubectl /usr/local/bin/kubectl
fi

cat > "$HOME/config.yaml" <<'YAML'
{KIND_CONFIG.rstrip()}
YAML

docker --version
kind --version
kubectl version --client --output=yaml
"""


REMOTE_CLUSTER_SCRIPT = """#!/bin/bash
set -euo pipefail

if kind get clusters | grep -qx kind; then
  echo "kind cluster already exists."
else
  kind create cluster --config "$HOME/config.yaml"
fi

kubectl get nodes -o wide
kubectl get pods -A
"""


def run(command, *, input_text=None, check=True):
    printable = " ".join(command)
    print(f"\n$ {printable}")
    completed = subprocess.run(
        command,
        input=input_text.encode("utf-8") if input_text else None,
        capture_output=True,
        check=False,
    )
    if completed.stdout:
        sys.stdout.buffer.write(completed.stdout)
    if completed.stderr:
        sys.stderr.buffer.write(completed.stderr)
    if check and completed.returncode != 0:
        raise SystemExit(f"Command failed with exit code {completed.returncode}: {printable}")
    return completed.stdout.decode("utf-8", errors="replace").strip()


def aws_json(args):
    output = run(["aws", *args, "--output", "json"])
    return json.loads(output) if output else None


def ask(prompt, default):
    value = input(f"{prompt} [{default}]: ").strip()
    return value or default


def load_settings(args):
    if args.yes:
        return DEFAULTS.copy()

    print("Press Enter to use the default value.")
    settings = DEFAULTS.copy()
    settings["region"] = ask("AWS region", settings["region"])
    settings["instance_type"] = ask("Instance type", settings["instance_type"])
    settings["volume_size"] = int(ask("Root volume size in GB", settings["volume_size"]))
    settings["key_name"] = ask("EC2 key pair name", settings["key_name"])
    settings["pem_path"] = ask("Local PEM path", settings["pem_path"])
    settings["security_group_name"] = ask("Security group name", settings["security_group_name"])
    settings["instance_name"] = ask("Instance Name tag", settings["instance_name"])
    return settings


def get_existing_instance(settings):
    data = aws_json([
        "ec2",
        "describe-instances",
        "--region",
        settings["region"],
        "--filters",
        f"Name=tag:Name,Values={settings['instance_name']}",
        "Name=instance-state-name,Values=pending,running,stopping,stopped",
        "--query",
        "Reservations[].Instances[]",
    ])
    return data[0] if data else None


def get_default_vpc(settings):
    data = aws_json([
        "ec2",
        "describe-vpcs",
        "--region",
        settings["region"],
        "--filters",
        "Name=is-default,Values=true",
        "--query",
        "Vpcs[0].VpcId",
    ])
    if not data:
        raise SystemExit("No default VPC found.")
    return data


def get_or_create_security_group(settings, vpc_id):
    data = aws_json([
        "ec2",
        "describe-security-groups",
        "--region",
        settings["region"],
        "--filters",
        f"Name=group-name,Values={settings['security_group_name']}",
        f"Name=vpc-id,Values={vpc_id}",
        "--query",
        "SecurityGroups[0].GroupId",
    ])
    if data:
        print(f"Using existing security group: {data}")
        return data

    print(f"Creating security group: {settings['security_group_name']}")
    sg_id = aws_json([
        "ec2",
        "create-security-group",
        "--region",
        settings["region"],
        "--group-name",
        settings["security_group_name"],
        "--description",
        "Security group for kind cluster",
        "--vpc-id",
        vpc_id,
        "--query",
        "GroupId",
    ])

    for port in settings["sg_open_ports"]:
        ip_permission = {
            "IpProtocol": "tcp",
            "FromPort": port,
            "ToPort": port,
            "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
        }
        aws_json([
            "ec2",
            "authorize-security-group-ingress",
            "--region",
            settings["region"],
            "--group-id",
            sg_id,
            "--ip-permissions",
            json.dumps(ip_permission),
        ])
        print(f"  Added inbound rule: {port}/tcp from 0.0.0.0/0")

    return sg_id


def get_default_subnet(settings, vpc_id):
    data = aws_json([
        "ec2",
        "describe-subnets",
        "--region",
        settings["region"],
        "--filters",
        f"Name=vpc-id,Values={vpc_id}",
        "Name=default-for-az,Values=true",
        "--query",
        "Subnets[0].SubnetId",
    ])
    if not data:
        raise SystemExit("No default subnet found.")
    return data


def get_ami_id(settings):
    return run([
        "aws",
        "ssm",
        "get-parameter",
        "--region",
        settings["region"],
        "--name",
        settings["ami_parameter"],
        "--query",
        "Parameter.Value",
        "--output",
        "text",
    ])


def describe_instance(settings, instance_id):
    return aws_json([
        "ec2",
        "describe-instances",
        "--region",
        settings["region"],
        "--instance-ids",
        instance_id,
        "--query",
        "Reservations[0].Instances[0]",
    ])


def launch_instance(settings):
    existing = get_existing_instance(settings)
    if existing:
        instance_id = existing["InstanceId"]
        state = existing["State"]["Name"]
        print(f"Found existing instance {instance_id} in state {state}.")
        if state == "stopped":
            run(["aws", "ec2", "start-instances", "--region", settings["region"], "--instance-ids", instance_id])
        return instance_id

    vpc_id = get_default_vpc(settings)
    subnet_id = get_default_subnet(settings, vpc_id)
    security_group_id = get_or_create_security_group(settings, vpc_id)
    ami_id = get_ami_id(settings)

    block_device = json.dumps([
        {
            "DeviceName": "/dev/sda1",
            "Ebs": {
                "VolumeSize": settings["volume_size"],
                "VolumeType": "gp3",
                "DeleteOnTermination": True,
            },
        }
    ])

    data = aws_json([
        "ec2",
        "run-instances",
        "--region",
        settings["region"],
        "--image-id",
        ami_id,
        "--instance-type",
        settings["instance_type"],
        "--key-name",
        settings["key_name"],
        "--security-group-ids",
        security_group_id,
        "--subnet-id",
        subnet_id,
        "--block-device-mappings",
        block_device,
        "--tag-specifications",
        f"ResourceType=instance,Tags=[{{Key=Name,Value={settings['instance_name']}}}]",
        f"ResourceType=volume,Tags=[{{Key=Name,Value={settings['instance_name']}-root}}]",
        "--query",
        "Instances[0]",
    ])
    return data["InstanceId"]


def wait_for_instance(settings, instance_id):
    run(["aws", "ec2", "wait", "instance-running", "--region", settings["region"], "--instance-ids", instance_id])
    instance = describe_instance(settings, instance_id)
    public_ip = instance.get("PublicIpAddress")
    if not public_ip:
        raise SystemExit("Instance is running but has no public IP address.")
    print(f"Instance is running: {instance_id} public IP {public_ip}")
    return public_ip


def ssh_command(settings, public_ip, command, *, input_text=None, check=True):
    ssh_target = f"{settings['ssh_user']}@{public_ip}"
    if input_text:
        input_text = input_text.replace("\r\n", "\n")
    return run([
        "ssh",
        "-o",
        "StrictHostKeyChecking=accept-new",
        "-i",
        settings["pem_path"],
        ssh_target,
        command,
    ], input_text=input_text, check=check)


def wait_for_ssh(settings, public_ip):
    print("Waiting for SSH...")
    ssh_target = f"{settings['ssh_user']}@{public_ip}"
    for attempt in range(1, 31):
        completed = subprocess.run(
            [
                "ssh",
                "-o",
                "StrictHostKeyChecking=accept-new",
                "-i",
                settings["pem_path"],
                ssh_target,
                "true",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode == 0:
            print("SSH is ready.")
            return
        time.sleep(10)
        print(f"SSH not ready yet, retry {attempt}/30...")
    raise SystemExit("SSH did not become ready in time.")


def apply(settings):
    pem = Path(settings["pem_path"])
    if not pem.exists():
        raise SystemExit(f"PEM file not found: {pem}")

    instance_id = launch_instance(settings)
    public_ip = wait_for_instance(settings, instance_id)
    wait_for_ssh(settings, public_ip)

    ssh_command(settings, public_ip, "bash -s", input_text=REMOTE_INSTALL_SCRIPT)
    print("Opening a fresh SSH session so Docker group membership is active.")
    ssh_command(settings, public_ip, "bash -s", input_text=REMOTE_CLUSTER_SCRIPT)

    print("\nApply complete.")
    print(f"Instance ID: {instance_id}")
    print(f"Public IP: {public_ip}")
    print(f"SSH: ssh -i \"{settings['pem_path']}\" {settings['ssh_user']}@{public_ip}")


def destroy(settings):
    existing = get_existing_instance(settings)
    if not existing:
        print(f"No instance found with Name tag {settings['instance_name']}.")
        return

    instance_id = existing["InstanceId"]
    state = existing["State"]["Name"]
    print(f"Found instance {instance_id} in state {state}.")
    confirm = input(f"Terminate {instance_id}? Type yes to continue: ").strip().lower()
    if confirm != "yes":
        print("Destroy cancelled.")
        return

    run(["aws", "ec2", "terminate-instances", "--region", settings["region"], "--instance-ids", instance_id])
    run(["aws", "ec2", "wait", "instance-terminated", "--region", settings["region"], "--instance-ids", instance_id])
    print(f"Destroyed instance {instance_id}.")


def main():
    parser = argparse.ArgumentParser(description="Create or destroy an EC2-hosted kind cluster.")
    parser.add_argument("action", choices=["apply", "destroy"], help="apply creates/reuses the instance and cluster; destroy terminates it")
    parser.add_argument("-y", "--yes", action="store_true", help="use defaults without prompting")
    args = parser.parse_args()

    settings = load_settings(args)
    if args.action == "apply":
        apply(settings)
    else:
        destroy(settings)


if __name__ == "__main__":
    main()

