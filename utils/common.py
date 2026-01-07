import subprocess

def cmd(command):
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while running : {command} : {e}")
        exit(1)
