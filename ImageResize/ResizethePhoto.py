import cv2
import os

# Input & Output folders
input_folder = "input_photos"  # Folder containing original images
output_folder = "resized_photos"  # Folder to save resized images

# Target dimensions (width, height)
target_size = (400, 514)  # Customize as needed

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through all images in input folder
for filename in os.listdir(input_folder):
    if filename.endswith((".jpg", ".jpeg", ".png")):
        # Read image
        img_path = os.path.join(input_folder, filename)
        img = cv2.imread(img_path)

        if img is not None:
            # Resize image
            resized_img = cv2.resize(img, target_size)

            # Save resized image
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, resized_img)
            print(f"Resized: {filename}")
        else:
            print(f"Failed to read: {filename}")

print("All images resized successfully!")