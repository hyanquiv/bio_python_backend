from flask import Flask, request, send_file, jsonify
import os
from aligner import run_alignment
import uuid

app = Flask(__name__)

@app.route("/align", methods=["POST"])
def align():
    try:
        file = request.files["file"]
        if not file:
            return jsonify({"error": "No file provided"}), 400

        input_path = f"tmp_{uuid.uuid4()}.fasta"
        output_path = f"aligned_{uuid.uuid4()}.fasta"

        # Guardar el archivo subido
        file.save(input_path)

        # Ejecutar alineamiento
        run_alignment(input_path, output_path)

        # Enviar archivo alineado
        return send_file(
            output_path,
            as_attachment=True,
            mimetype='text/plain'
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Limpieza de archivos temporales
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)

if __name__ == "__main__":
    app.run(debug=True)
