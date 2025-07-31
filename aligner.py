import subprocess
from shutil import which

def run_alignment(input_file, output_file):
    if not which("aligner"):
        raise EnvironmentError("aligner no está en el PATH. Instálalo o colócalo en ./aligner/")
    algn_path = "./aligner.exe"
    cmd = [algn_path, "-align", input_file, "-output", output_file]
    subprocess.run(cmd, check=True)
