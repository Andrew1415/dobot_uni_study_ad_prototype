# import os
# import cv2
# from ultralytics import YOLO

# # Initialize the model (YOLOv8 by default)
# model = YOLO("./models/my_model.pt")  # Replace with your model path if necessary

# # Set the folder where your images are stored
# image_folder = "./test_img"

# # Minimum confidence threshold
# min_confidence = 0.5

# # Grid size: 4 rows × 6 columns
# GRID_ROWS, GRID_COLS = 4, 6

# # List all images in the folder
# image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# cv2.namedWindow("Detection", cv2.WINDOW_NORMAL)
# cv2.namedWindow("Grid Overview", cv2.WINDOW_NORMAL)

# for image_file in image_files:
#     # Read the image
#     image_path = os.path.join(image_folder, image_file)
#     image = cv2.imread(image_path)
#     h, w = image.shape[:2]

#     # --- 1) Build the grid overview image ---
#     cell_h = h // GRID_ROWS
#     cell_w = w // GRID_COLS

#     # Crop out each cell and store in row lists
#     rows = []
#     for r in range(GRID_ROWS):
#         cells = []
#         for c in range(GRID_COLS):
#             y1 = r * cell_h
#             y2 = (r + 1) * cell_h if r < GRID_ROWS - 1 else h
#             x1 = c * cell_w
#             x2 = (c + 1) * cell_w if c < GRID_COLS - 1 else w
#             crop = image[y1:y2, x1:x2]
#             # Optionally draw the cell index on each crop:
#             cv2.putText(crop, f"{r},{c}", (5,15),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
#             cells.append(crop)
#         # horizontally stack cells of this row
#         rows.append(cv2.hconcat(cells))
#     # vertically stack the 4 rows to make the full grid overview
#     grid_overview = cv2.vconcat(rows)

#     # --- 2) Run detection and draw boxes above threshold ---
#     results = model(image)
#     boxes = results[0].boxes
#     names = results[0].names

#     valid = []
#     for box in boxes:
#         conf = float(box.conf[0])
#         if conf < min_confidence:
#             continue
#         valid.append(box)

#     for box in valid:
#         x1, y1, x2, y2 = map(int, box.xyxy[0])
#         cls_id = int(box.cls[0])
#         label = names[cls_id]
#         conf = float(box.conf[0])
#         text = f"{label}: {conf:.2f}"
#         cv2.rectangle(image, (x1, y1), (x2, y2), (0,255,0), 2)
#         cv2.putText(image, text, (x1, y1-10),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)

#     # Print detections to console
#     print(f"Detections for {image_file} (conf ≥ {min_confidence}):")
#     for box in valid:
#         cls_id = int(box.cls[0])
#         print(f"  - {names[cls_id]}: {float(box.conf[0]):.2f}")

#     # --- 3) Display both windows ---
#     cv2.imshow("Detection", image)
#     cv2.imshow("Grid Overview", grid_overview)

#     key = cv2.waitKey(0)
#     if key == 27:  # Esc to exit
#         break

# cv2.destroyAllWindows()


import os
import cv2
from ultralytics import YOLO

# Initialize the model (YOLOv8 by default)
model = YOLO("./models/my_model_new1.pt")  # Replace with your model path if necessary

# Set the folder where your images are stored
image_folder = "./test_img"

# Minimum confidence threshold
min_confidence = 0.5

# Grid size: 4 rows × 6 columns
GRID_ROWS, GRID_COLS = 4, 6

# List all images in the folder
image_files = [f for f in os.listdir(image_folder)
               if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

for image_file in image_files:
    # Read the image
    image_path = os.path.join(image_folder, image_file)
    image = cv2.imread(image_path)
    h, w = image.shape[:2]

    # Compute cell size
    cell_h = h // GRID_ROWS
    cell_w = w // GRID_COLS

    # 1) Display each grid cell independently
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            y1 = r * cell_h
            y2 = (r + 1) * cell_h if r < GRID_ROWS - 1 else h
            x1 = c * cell_w
            x2 = (c + 1) * cell_w if c < GRID_COLS - 1 else w

            cell = image[y1:y2, x1:x2]
            window_name = f"cell_{r}_{c}"
            cv2.imshow(window_name, cell)
            # Wait for key press, then close this cell window
            cv2.waitKey(0)
            cv2.destroyWindow(window_name)

    # 2) Run detection and draw boxes above threshold
    results = model(image)
    boxes = results[0].boxes
    names = results[0].names

    valid = []
    for box in boxes:
        conf = float(box.conf[0])
        if conf < min_confidence:
            continue
        valid.append(box)

    for box in valid:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cls_id = int(box.cls[0])
        label = names[cls_id]
        conf = float(box.conf[0])
        text = f"{label}: {conf:.2f}"
        cv2.rectangle(image, (x1, y1), (x2, y2), (0,255,0), 2)
        cv2.putText(image, text, (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)

    # Print detections to console
    print(f"Detections for {image_file} (conf ≥ {min_confidence}):")
    for box in valid:
        cls_id = int(box.cls[0])
        print(f"  - {names[cls_id]}: {float(box.conf[0]):.2f}")

    # 3) Finally, show the full-image detections
    cv2.namedWindow("Detection", cv2.WINDOW_NORMAL)
    cv2.imshow("Detection", image)
    key = cv2.waitKey(0)
    if key == 27:  # Esc to exit early
        break
    cv2.destroyWindow("Detection")

cv2.destroyAllWindows()
