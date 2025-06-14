from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import os, re
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "ktp" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
                file = request.files["ktp"]
                    filename = datetime.now().strftime("%Y%m%d%H%M%S") + "_" + file.filename
                        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                            file.save(filepath)

                                image = Image.open(filepath)
                                    text = pytesseract.image_to_string(image, lang="ind")

                                        patterns = {
                                                "NIK": r"NIK\s*[:\-]?\s*(\d{16})",
                                                        "Nama": r"Nama\s*[:\-]?\s*(.+)",
                                                                "TTL": r"Tempat/Tgl Lahir\s*[:\-]?\s*(.+)",
                                                                        "Alamat": r"Alamat\s*[:\-]?\s*(.+)",
                                                                                "Agama": r"Agama\s*[:\-]?\s*(\w+)",
                                                                                        "Status": r"Status\s*Perkawinan\s*[:\-]?\s*(.+)",
                                                                                            }

                                                                                                data = {k: (re.search(p, text).group(1).strip() if re.search(p, text) else "Tidak ditemukan")
                                                                                                            for k, p in patterns.items()}

                                                                                                                return jsonify(data)

                                                                                                                if __name__ == "__main__":
                                                                                                                    app.run(host="0.0.0.0", port=5000)