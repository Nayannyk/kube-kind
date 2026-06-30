import subprocess

script = "#!/bin/bash\necho hello\nwhoami\n"

print("input repr:", repr(script))

result = subprocess.run(
    ["ssh", "-o", "StrictHostKeyChecking=accept-new", "-i", "C:\\Users\\NAYAN\\Downloads\\Nayan.pem", "ubuntu@52.66.70.3", "bash -s"],
    input=script,
    text=True,
    capture_output=True,
)
print("stdout:", repr(result.stdout))
print("stderr:", repr(result.stderr))
print("rc:", result.returncode)
