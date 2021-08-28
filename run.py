import subprocess
subprocess.run("pip install poetry",  shell=True)
subprocess.run("poetry install --no-dev", shell=True)
#subprocess.run("pip install -U apscheduler", shell=True)
#subprocess.run("poetry run trade & python main.py", shell=True)
subprocess.run("python main.py & poetry run trade", shell=True)
