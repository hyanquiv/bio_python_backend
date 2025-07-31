from flask import Flask, request, send_file
import os
from aligner import run_alignment
import uuid
import io

app = Flask(__name__)

@app.route("/align", methods=["POST"])
def align():
    file = request.files["file"]
    input_path = f"tmp_{uuid.uuid4()}.fasta"
    output_path = f"aligned_{uuid.uuid4()}.fasta"

    # Guardar input
    file.save(input_path)

    # Ejecutar alineamiento
    run_alignment(input_path, output_path)

    # Leer el archivo de salida a memoria
    with open(output_path, "rb") as f:
        data = f.read()

    # Borrar archivos temporales
    os.remove(input_path)
    os.remove(output_path)

    # Enviar contenido como archivo descargable
    return send_file(
        io.BytesIO(data),
        as_attachment=True,
        download_name="aligned_output.fasta",
        mimetype="text/plain"
    )

if __name__ == "__main__":
    app.run(debug=True)
