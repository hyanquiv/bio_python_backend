from aligner import run_alignment
from io_utils import read_fasta

input_file = "example.fasta"
output_file = "aligned_output.fasta"

print("Leyendo archivo...")
seqs = read_fasta(input_file)

print("Ejecutando alineamiento...")
run_alignment(input_file, output_file)

print(f"Alineamiento completado. Resultado en: {output_file}")
