import os
import cv2
from ultralytics import YOLO

# Initialize the model (YOLOv8 by default)
model = YOLO("./models/my_model.pt")  # Replace with your model path if necessary

# Set the folder where your images are stored
image_folder = "./img"

# Minimum confidence threshold
min_confidence = 0.8

# List all images in the folder
image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

cv2.namedWindow("Detection", cv2.WINDOW_NORMAL)

for image_file in image_files:
    # Read the image
    image_path = os.path.join(image_folder, image_file)
    image = cv2.imread(image_path)

    # Run inference
    results = model(image)
    boxes = results[0].boxes  # Detected boxes
    names = results[0].names  # Class names mapping

    # Collect detections that meet threshold
    valid_detections = []
    for box in boxes:
        conf = float(box.conf[0])
        if conf < min_confidence:
            continue
        cls_id = int(box.cls[0])
        valid_detections.append((box, cls_id, conf))

    # Draw and print only valid detections
    print(f"Detections for {image_file} (conf ≥ {min_confidence}):")
    for box, cls_id, conf in valid_detections:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        label = names[cls_id]
        text = f"{label}: {conf:.2f}"

        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            image, text, (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2
        )

        print(f"  - {label}: {conf:.2f}")

    # Display the filtered detections
    cv2.imshow("Detection", image)
    key = cv2.waitKey(0)
    if key == 27:  # Esc to exit
        break

cv2.destroyAllWindows()
