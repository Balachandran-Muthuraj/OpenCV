import os
import base64
import hashlib
import json
import cv2
import dlib
import numpy as np
from PIL import Image
from typing import Dict, Optional
import SQLiteDB as DB


# Configuration (would normally be in a config file)
FACEMODEL_DIR = os.path.join(os.path.dirname(__file__), "facemodel")
LANDMARKS_MODEL_PATH = os.path.join(FACEMODEL_DIR, "shape_predictor_5_face_landmarks.dat")
HAAR_CASCADE_PATH = os.path.join(FACEMODEL_DIR, "haarcascade_frontalface_default.xml")
VALIDATED_FOLDER = os.path.join(os.path.dirname(__file__), "photo_validation", "validated")
METADATA_FILE = os.path.join(VALIDATED_FOLDER, "validated_metadata.json")

# Ensure directories exist
os.makedirs(VALIDATED_FOLDER, exist_ok=True)

# Initialize models (would normally be done once at app startup)
try:
    face_detector = dlib.get_frontal_face_detector()
    landmark_predictor = dlib.shape_predictor(LANDMARKS_MODEL_PATH)
    face_cascade = cv2.CascadeClassifier(HAAR_CASCADE_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load face detection models: {str(e)}")


def validate_and_convert_photo_to_base64(file_path: str) -> Dict:

    filename = os.path.basename(file_path)

    try:
        # 1. Basic file validation
        if not os.path.exists(file_path):
            return generate_error_response("001", "File does not exist", filename)

        ext = os.path.splitext(file_path)[1].lower()
        if ext not in [".jpg", ".jpeg", ".png"]:
            return generate_error_response("002", "Invalid file format", filename)

        file_size = os.path.getsize(file_path)
        if file_size > 1 * 1024 * 1024:  # 1MB
            return generate_error_response("003", "File size exceeds limit", filename)

        # 2. Image validation
        try:
            image = Image.open(file_path)
            image_np = np.array(image.convert('RGB'))
            gray_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        except Exception:
            return generate_error_response("004", "Invalid image file", filename)

        # Check dimensions
        height, width = image_np.shape[:2]
        if width != 400 or height != 514:
            return generate_error_response("005", "Invalid image dimensions", filename)

        # 3. Face detection
        # First try dlib (more accurate)
        faces = face_detector(gray_image, 1)

        # Fallback to OpenCV if dlib finds nothing
        if len(faces) == 0:
            cv_faces = face_cascade.detectMultiScale(
                gray_image,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(100, 100))
            faces = [dlib.rectangle(x, y, x + w, y + h) for (x, y, w, h) in cv_faces]

            if len(faces) == 0:
                return generate_error_response("006", "No face detected", filename)
        if len(faces) > 1:
            return generate_error_response("007", "Multiple faces detected", filename)

        # 4. Facial landmarks validation
        # try:
        #     landmarks = landmark_predictor(gray_image, faces[0])
        #
        #     # Check for hair covering face
        #     if check_hair_covering_face(landmarks, gray_image):
        #         return generate_error_response("008", "Face obstructed by hair", filename)
        #
        # except Exception:
        #     return generate_error_response("009", "Face landmark detection failed", filename)

        # 5. Blur detection
        if is_image_blurry(gray_image):
            return generate_error_response("010", "Image is too blurry", filename)

        # 6. Duplicate checking
        image_hash = calculate_image_hash(file_path)
        duplicate_file = find_duplicate_image(image_hash, filename)
        if duplicate_file:
            return generate_error_response("011", f"Duplicate image found: {duplicate_file}", filename)

        # 7. Database operations
        try:
            is_duplicate, duplicate_file = DB.check_duplicate_face(file_path)
            if is_duplicate:
                return generate_error_response("012", f"Duplicate face in database: {duplicate_file}", filename)

            DB.save_face_encoding(file_path)
        except Exception as e:
            return generate_error_response("013", f"Database error: {str(e)}", filename)

        # 8. Convert to base64
        base64_image = convert_to_base64(file_path)

        # 9. Move to validated folder
        validated_path = os.path.join(VALIDATED_FOLDER, filename)
        if os.path.exists(validated_path):
            os.remove(validated_path)
        os.rename(file_path, validated_path)



        # 10. Update metadata
        update_metadata(image_hash, filename)

        return generate_success_response("000", "Validation successful", base64_image)

    except Exception as e:
        return generate_error_response("999", f"Unexpected error: {str(e)}", filename)


def check_hair_covering_face(landmarks, gray_image: np.ndarray) -> bool:
    """Check if hair is covering critical facial features"""
    critical_points = [30, 48, 54]  # Nose, lower lip, and chin
    intensity_threshold = 80

    for point in critical_points:
        x, y = landmarks.part(point).x, landmarks.part(point).y
        if gray_image[y, x] < intensity_threshold:
            return True
    return False


def is_image_blurry(gray_image: np.ndarray, threshold: float = 75.0) -> bool:
    """Check if image is blurry using Laplacian variance"""
    return cv2.Laplacian(gray_image, cv2.CV_64F).var() < threshold


def calculate_image_hash(file_path: str) -> str:
    """Calculate SHA-256 hash of file content"""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()


def find_duplicate_image(image_hash: str, current_filename: str) -> Optional[str]:
    """Check for duplicate images in metadata"""
    if not os.path.exists(METADATA_FILE):
        return None

    with open(METADATA_FILE, "r") as f:
        metadata = json.load(f)

    for hash_val, filename in metadata.items():
        if hash_val == image_hash and filename != current_filename:
            return filename
    return None


def convert_to_base64(file_path: str) -> str:
    """Convert image to base64 data URL"""
    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded}"


def update_metadata(image_hash: str, filename: str):
    """Update metadata file with new validated image"""
    metadata = {}
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r") as f:
            metadata = json.load(f)

    metadata[image_hash] = filename

    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f, indent=2)


def generate_success_response(code: str, message: str, data: str) -> Dict:
    return {
        "code": code,
        "data": data,
        "msg": message,
        "result": 1,
        "success": True
    }


def generate_error_response(code: str, message: str, data: str) -> Dict:
    return {
        "code": code,
        "data": data,
        "msg": message,
        "result": 0,
        "success": False
    }


def delete_metadata_and_encodings(filename: str) -> Dict:
    """
    Deletes a file's metadata and face encodings from the system.

    Args:
        filename: Name of the file to delete

    Returns:
        Dictionary with operation results
    """
    if not filename:
        return generate_error_response("001", "Filename is required", "")

    removed_from_db = False
    removed_from_metadata = False

    try:
        # 1. Remove from database
        DB.delete_face_encoding(filename)
        removed_from_db = True
    except Exception as e:
        return generate_error_response("002", f"Database deletion failed: {str(e)}", filename)

    # 2. Remove from metadata
    if os.path.exists(METADATA_FILE):
        try:
            with open(METADATA_FILE, "r") as f:
                metadata = json.load(f)

            # Find the hash for this filename
            hash_to_remove = None
            for hash_val, fname in metadata.items():
                if fname == filename:
                    hash_to_remove = hash_val
                    break

            if hash_to_remove:
                del metadata[hash_to_remove]
                removed_from_metadata = True

                with open(METADATA_FILE, "w") as f:
                    json.dump(metadata, f, indent=2)

        except Exception as e:
            if removed_from_db:
                # If we removed from DB but failed to update metadata,
                # the system will be in an inconsistent state
                return generate_error_response("003",
                                               f"Metadata update failed after DB deletion: {str(e)}",
                                               filename)
            return generate_error_response("004", f"Metadata access failed: {str(e)}", filename)

    # 3. Remove the actual file if it exists
    file_path = os.path.join(VALIDATED_FOLDER, filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            return generate_error_response("005",
                                           f"File deletion failed after metadata/DB removal: {str(e)}",
                                           filename)

    if not removed_from_db and not removed_from_metadata:
        return generate_error_response("006", "File not found in system", filename)

    return generate_success_response("000", "Deletion successful", filename)