from PIL import Image
import os

def rotate_all(input_path):
    # Load original image
    img = Image.open(input_path)
    
    # Extract base name (without extension) for naming
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    
    # Create an output directory named "<base_name>_rotated"
    output_dir = f"{base_name}_rotated"
    os.makedirs(output_dir, exist_ok=True)
    print(f"Saving rotated images into folder: {output_dir}")
    
    # Rotate and save for each degree 0–359
    for degree in range(360):
        # Always rotate from the original image
        rotated = img.rotate(degree, expand=True)
        
        # Build output filename: "<base_name>_<degree>.png"
        out_filename = f"{base_name}_{degree}.png"
        out_path = os.path.join(output_dir, out_filename)
        
        # Save as PNG
        rotated.save(out_path, format='PNG')
        print(f"  • Saved {out_filename}")

if __name__ == "__main__":
    # Replace with the path to your image file
    input_image_path = "./img/candy_3.png"
    rotate_all(input_image_path)