import sqlite3
import face_recognition
import numpy as np
import os

# Paths
ROOT_FOLDER = os.path.join(os.path.dirname(__file__), "photo_validation")
INPUT_FOLDER = os.path.join(ROOT_FOLDER, "input")
VALIDATED_FOLDER = os.path.join(ROOT_FOLDER, "validated")
DATABASE_FILE = os.path.join(VALIDATED_FOLDER, "face_encodings.db")

# Constants
TOLERANCE = 0.3
DISTANCE_THRESHOLD = 0.5


def create_db():
    """
    Create SQLite database and table for storing face encodings.
    """
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS face_encodings (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            filename TEXT UNIQUE,
                            encoding BLOB
                          )''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error creating database: {e}")


def save_face_encoding(image_path):
    """
    Saves the face encoding of the validated image to the SQLite database.
    :param image_path: Path to the input image.
    """
    if not os.path.exists(DATABASE_FILE):
        create_db()

    input_image = face_recognition.load_image_file(image_path)
    input_encodings = face_recognition.face_encodings(input_image)

    if len(input_encodings) == 0:
        print(f"No face found in {image_path}")
        return

    input_encoding = input_encodings[0]
    encoding_blob = np.array(input_encoding).tobytes()

    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO face_encodings (filename, encoding)
            VALUES (?, ?)
        ''', (os.path.basename(image_path), encoding_blob))
        conn.commit()
        print(f"Face encoding saved for {os.path.basename(image_path)}.")
    except sqlite3.Error as e:
        print(f"Error saving face encoding: {e}")
    finally:
        conn.close()


def check_duplicate_face(image_path, tolerance=TOLERANCE, distance_threshold=DISTANCE_THRESHOLD):
    """
    Checks if a duplicate face exists in the database.
    :param image_path: Path to the input image.
    :return: (is_duplicate, matching_filename) -> Tuple[bool, Optional[str]]
    """
    create_db()

    input_image = face_recognition.load_image_file(image_path)
    input_encodings = face_recognition.face_encodings(input_image)

    if len(input_encodings) == 0:
        print(f"No face found in {image_path}")
        return False, None

    input_encoding = input_encodings[0]
    input_filename = os.path.basename(image_path)

    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT filename, encoding FROM face_encodings')

        for stored_filename, encoding_blob in cursor:
            if stored_filename == input_filename:
                continue  # Skip self-comparison

            stored_encoding = np.frombuffer(encoding_blob, dtype=np.float64)
            matches = face_recognition.compare_faces([stored_encoding], input_encoding, tolerance=tolerance)
            if matches[0]:
                distance = face_recognition.face_distance([stored_encoding], input_encoding)[0]
                if distance < distance_threshold:
                    return True, stored_filename

    except sqlite3.Error as e:
        print(f"Error checking duplicates: {e}")
    finally:
        conn.close()

    return False, None
def delete_face_encoding(filename):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM face_encodings WHERE filename = ?", (filename,))
    conn.commit()
    conn.close()