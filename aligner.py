import subprocess
from shutil import which

def run_alignment(input_file, output_file):
    if not which("muscle"):
        raise EnvironmentError("MUSCLE no está en el PATH. Instálalo o colócalo en ./muscle/")

    cmd = ["muscle", "-in", input_file, "-out", output_file]
    subprocess.run(cmd, check=True)
