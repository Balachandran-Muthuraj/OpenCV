import os
import traceback
import logging
from flask import Flask, request, jsonify
from Photovalidator import validate_and_convert_photo_to_base64, delete_metadata_and_encodings


# Logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

app = Flask(__name__)




@app.route("/validate-photo", methods=["POST"])
def validate_photo():
    app.logger.info("Received request to validate photo.")

    file = request.files.get("file")
    if not file or file.filename == "":
        app.logger.error("No file provided or filename is empty.")
        return jsonify({"error": "No valid file provided"}), 400

    temp_path = file.filename
    file.save(temp_path)
    app.logger.info(f"File saved temporarily as {temp_path}")

    try:
        result = validate_and_convert_photo_to_base64(temp_path)
        app.logger.info("Photo validation completed.")
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error during photo validation: {str(e)}")
        return jsonify({"error": "Failed to validate the photo."}), 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            app.logger.info(f"Temporary file {temp_path} deleted.")




@app.route("/delete-file", methods=["POST"])
def delete_file():
    logging.info("Received request to delete metadata and encodings.")

    data = request.get_json()
    filename = data.get("filename") if data else None

    if not filename:
        logging.error("Filename not provided in the request.")
        return jsonify({"error": "Filename not provided"}), 400

    try:
        result = delete_metadata_and_encodings(filename)
        logging.info("Deletion completed successfully.")
        return jsonify(result)
    except Exception as e:
        logging.error(f"Error during deletion: {str(e)}")
        return jsonify({"error": "Failed to delete the metadata and encodings"}), 500


if __name__ == "__main__":
    app.run(debug=True)
