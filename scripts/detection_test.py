import cv2
import numpy as np
from pypylon import pylon

# Function to detect the color
def detect_color(image, color):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    if color == "red":
        lower_red1 = np.array([0, 90, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 90, 50])
        upper_red2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = mask1 + mask2  # Combine both masks for red
    elif color == "yellow":
        lower_yellow = np.array([15, 80, 80])
        upper_yellow = np.array([45, 255, 255])
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    else:
        raise ValueError("Invalid color selection. Choose 'red' or 'yellow'.")

    return mask

# Function to analyze the grid with threshold coverage
def analyze_grid(mask, rows=4, cols=6, threshold=0.15):
    height, width = mask.shape
    cell_h, cell_w = height // rows, width // cols

    detected_cells = []  # Store cells where at least threshold is covered

    for i in range(rows):
        for j in range(cols):
            cell = mask[i * cell_h:(i + 1) * cell_h, j * cell_w:(j + 1) * cell_w]
            total_pixels = cell_h * cell_w
            detected_pixels = np.sum(cell > 0)

            if detected_pixels / total_pixels >= threshold:
                detected_cells.append((i, j))

    return detected_cells, cell_h, cell_w

# Load image from camera
camera_serial = '23984475'  # Update to your camera's serial
tl_factory = pylon.TlFactory.GetInstance()
devices = tl_factory.EnumerateDevices()
selected_device = None
for device in devices:
    if device.GetSerialNumber() == camera_serial:
        selected_device = device
        break

if selected_device is None:
    print(f"Camera with serial {camera_serial} not found.")
    exit(1)

camera = pylon.InstantCamera(tl_factory.CreateDevice(selected_device))
camera.Open()
if "BGR8" in camera.PixelFormat.GetSymbolics():
    camera.PixelFormat.SetValue("BGR8")

camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

if grab_result.GrabSucceeded():
    scene_img = grab_result.Array
    print("Scene image captured successfully.")
else:
    print("Failed to grab image.")
    camera.Close()
    exit(1)

camera.Close()

# Crop and resize
image_1 = scene_img[97:1865, 302:2916]
image = cv2.resize(image_1, (0, 0), fx=0.5, fy=0.5)

# Detect color and analyze grid
color_to_detect = "red"  # Change to "yellow" if needed
mask = detect_color(image, color_to_detect)
highlighted_cells, cell_h, cell_w = analyze_grid(mask)

# Output cell positions
if not highlighted_cells:
    print("No significant color regions detected.")
else:
    for row, col in highlighted_cells:
        print(f"Row: {row}, Column: {col} (covered ≥ threshold)")

    # Optionally draw rectangles on original image
    annotated_image = image.copy()
    for row, col in highlighted_cells:
        top_left = (col * cell_w, row * cell_h)
        bottom_right = ((col + 1) * cell_w, (row + 1) * cell_h)
        cv2.rectangle(annotated_image, top_left, bottom_right, (0, 255, 0), 2)

    # Save annotated image
    cv2.imwrite("annotated_result.png", annotated_image)
    print("Annotated image saved as 'annotated_result.png'.")

# Save the mask image
cv2.imwrite("detected_mask.png", mask)
print("Mask image saved as 'detected_mask.png'.")
