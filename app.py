from flask import Flask, request, send_file
import os
from aligner import run_alignment
import uuid
import io

app = Flask(__name__)

# Crear carpetas si no existen
os.makedirs("in", exist_ok=True)
os.makedirs("out", exist_ok=True)

@app.route("/align", methods=["POST"])
def align():
    # Rutas de archivos
    input_filename = f"{uuid.uuid4()}.fasta"
    output_filename = f"{uuid.uuid4()}.fasta"
    input_path = os.path.join("in", input_filename)
    output_path = os.path.join("out", output_filename)

    # Guardar input
    file = request.files["file"]
    file.save(input_path)

    # Ejecutar alineamiento
    run_alignment(input_path, output_path)

    # Leer el archivo de salida a memoria
    with open(output_path, "rb") as f:
        data = f.read()

    # Enviar contenido como archivo descargable
    return send_file(
        io.BytesIO(data),
        as_attachment=True,
        download_name="aligned_output.fasta",
        mimetype="text/plain"
    )

if __name__ == "__main__":
    app.run(debug=True)
