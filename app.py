from flask import Flask, request, jsonify
import os
from aligner import run_alignment
import uuid
import base64

app = Flask(__name__)

# Crear carpetas si no existen
os.makedirs("in", exist_ok=True)
os.makedirs("out", exist_ok=True)

@app.route("/align", methods=["POST"])
def align():
    # Crear ruta única para input
    input_filename = f"{uuid.uuid4()}.fasta"
    input_path = os.path.join("in", input_filename)

    # Guardar input
    file = request.files["file"]
    file.save(input_path)

    # Ejecutar alineamiento → devuelve 2 paths
    muscle_path, msa_path = run_alignment(input_path, os.path.join("out", str(uuid.uuid4())))

    # Leer ambos archivos y codificarlos en base64
    with open(muscle_path, "rb") as f1, open(msa_path, "rb") as f2:
        muscle_data = base64.b64encode(f1.read()).decode('utf-8')
        msa_data = base64.b64encode(f2.read()).decode('utf-8')

    # Borrar archivos temporales
    try:
        os.remove(input_path)
        os.remove(muscle_path)
        os.remove(msa_path)
    except Exception as e:
        print(f"Error al limpiar archivos: {e}")

    # Devolver ambos como JSON base64
    return jsonify({
        "aligned_muscle.fasta": muscle_data,
        "aligned_msa.fasta": msa_data
    })

if __name__ == "__main__":
    app.run(debug=True)
