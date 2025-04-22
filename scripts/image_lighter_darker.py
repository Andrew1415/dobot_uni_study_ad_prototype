from PIL import Image, ImageEnhance
import os

# Path to the folder containing the images
folder_path = './test_img'  # Replace with your folder path

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".jpg") or filename.endswith(".png"):  # You can add more image formats
        image_path = os.path.join(folder_path, filename)
        img = Image.open(image_path)

        # Darken the image by 20%
        enhancer = ImageEnhance.Brightness(img)
        darkened_img = enhancer.enhance(0.6)  # 0.8 is 20% darker

        # Lighten the image by 20%
        lightened_img = enhancer.enhance(1.4)  # 1.2 is 20% lighter

        # Save the darkened and lightened images
        darkened_img.save(os.path.join(folder_path, f"darkened_{filename}"))
        lightened_img.save(os.path.join(folder_path, f"lightened_{filename}"))

        print(f"Processed {filename}")
