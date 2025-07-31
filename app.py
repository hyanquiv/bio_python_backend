from flask import Flask, request, send_file
import os
from aligner import run_alignment
import uuid

app = Flask(__name__)

@app.route("/align", methods=["POST"])
def align():
    file = request.files["file"]
    input_path = f"tmp_{uuid.uuid4()}.fasta"
    output_path = f"aligned_{uuid.uuid4()}.fasta"

    file.save(input_path)
    run_alignment(input_path, output_path)

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
