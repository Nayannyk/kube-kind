import subprocess

script = """#!/bin/bash
set -euo pipefail
echo "hello from remote"
whoami
""".replace("\r\n", "\n")

result = subprocess.run(
    ["ssh", "-o", "StrictHostKeyChecking=accept-new", "-i", "C:\\Users\\NAYAN\\Downloads\\Nayan.pem", "ubuntu@52.66.70.3", "bash -s"],
    input=script,
    text=True,
    capture_output=True,
)
print("stdout:", repr(result.stdout))
print("stderr:", repr(result.stderr))
print("rc:", result.returncode)
