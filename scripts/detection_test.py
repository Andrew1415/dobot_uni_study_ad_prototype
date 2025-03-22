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


# Function to analyze the grid with at least 70% coverage threshold
def analyze_grid(mask, rows=4, cols=6, threshold=0.15):
    height, width = mask.shape
    cell_h, cell_w = height // rows, width // cols

    detected_cells = []  # Store cells where at least 70% is covered

    for i in range(rows):
        for j in range(cols):
            cell = mask[i * cell_h:(i + 1) * cell_h, j * cell_w:(j + 1) * cell_w]
            total_pixels = cell_h * cell_w
            detected_pixels = np.sum(cell > 0)  # Count non-zero (white) pixels

            # Check if at least 70% of the cell is covered
            if detected_pixels / total_pixels >= threshold:
                detected_cells.append((i, j))

    return detected_cells

# Load image
# image = cv2.resize(cv2.imread('./img/Image__2025-03-17__11-57-13.png'),
# (0, 0), fx=0.5, fy=0.5)


camera_serial = '23984475'  # <-- Update to your camera's serial
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
    # return

    # Create and open the camera
camera = pylon.InstantCamera(tl_factory.CreateDevice(selected_device))
camera.Open()
if "BGR8" in camera.PixelFormat.GetSymbolics():
    camera.PixelFormat.SetValue("BGR8")

camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

if grab_result.GrabSucceeded():
    # Convert to a NumPy array
    scene_img = grab_result.Array
    print("Scene image captured successfully.")
else:
    print("Failed to grab image.")
    camera.Close()
    # return
camera.Close()
image_1 = scene_img[315:2041, 159:2799]
image = cv2.resize(image_1, (0, 0), fx=0.5, fy=0.5)

color_to_detect = "yellow"  # Change to "yellow" if needed
mask = detect_color(image, color_to_detect)

# Analyze grid with 70% threshold
highlighted_cells = analyze_grid(mask)
if highlighted_cells is None:
    print("Nothing found")

# Display the result
for row, col in highlighted_cells:
    print(f"Row: {row}, Column: {col} (covered ≥ 70%)")

# Show the detected mask
cv2.imshow("Color Mask", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
