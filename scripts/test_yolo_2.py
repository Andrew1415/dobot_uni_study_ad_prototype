import os
import cv2
import csv
from ultralytics import YOLO

# Initialize the model (YOLOv8 by default)
model = YOLO("./models/my_model.pt")  # Replace with your model path if necessary

# Set the folder where your images are stored
image_folder = "./test_yolo"

# List all images in the folder
image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

with open('results.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write header to CSV
    writer.writerow(["Label", "Prediction Accuracy", "Image Name"])
    
    for image_file in image_files:
        # Read the image
        image_path = os.path.join(image_folder, image_file)
        image = cv2.imread(image_path)

        # Use the model to make detections
        results = model(image)

        # Get the bounding boxes, labels, and prediction confidences
        boxes = results[0].boxes  # Get the boxes of detected objects
        labels = results[0].names  # Get the names of the classes detected

        if boxes is not None:
            for box in boxes:
                # Get the label and prediction accuracy (confidence score)
                label = labels[int(box.cls[0])]
                accuracy = box.conf[0].item()  # Access confidence score directly from the box
                
                # Write the data to the CSV file
                writer.writerow([label, accuracy, image_file])

print("Detection results saved to 'results.csv'.")