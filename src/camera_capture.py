import cv2
import numpy as np
from pypylon import pylon 

def detect_color(image, color) -> bool:
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    if color == "red":
        lower_red1 = np.array([0, 90, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 90, 50])
        upper_red2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = mask1 + mask2
    elif color == "yellow":
        lower_yellow = np.array([15, 80, 80])
        upper_yellow = np.array([45, 255, 255])
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    else:
        raise ValueError("Invalid color selection. Choose 'red' or 'yellow'.")

    return mask

def analyze_grid(mask, rows=4, cols=6, threshold=0.15) -> bool:
    height, width = mask.shape
    cell_h, cell_w = height // rows, width // cols

    detected_cells = [] 

    for i in range(rows):
        for j in range(cols):
            cell = mask[i * cell_h:(i + 1) * cell_h, j * cell_w:(j + 1) * cell_w]
            total_pixels = cell_h * cell_w
            detected_pixels = np.sum(cell > 0) 

            if detected_pixels / total_pixels >= threshold:
                detected_cells.append((i, j))

    return detected_cells

def take_image () -> bool:
    camera_serial = '23984475'
    tl_factory = pylon.TlFactory.GetInstance()
    devices = tl_factory.EnumerateDevices()
    selected_device = None
    for device in devices:
        if device.GetSerialNumber() == camera_serial:
            selected_device = device
            break

    if selected_device is None:
        print(f"Camera with serial {camera_serial} not found.")

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
    camera.Close()
    image_1 = scene_img[255:2007, 252:2901]


    return image_1

def find_candy (candy) -> bool: 
    rows=4
    cols=6
    image = take_image()
    if candy == 0 :
        color_to_detect = "red"
    elif candy == 1 :
        color_to_detect = "yellow"
    else :
        return None
    mask = detect_color(image, color_to_detect)
    highlighted_cells = analyze_grid(mask)
    if not highlighted_cells:
        print("No candy detected with sufficient coverage.")
        return None

    center_row = rows / 2
    center_col = cols / 2
    best_distance = float('inf')
    best_cell = None
    for (i, j) in highlighted_cells:
        distance = (i - center_row) ** 2 + (j - center_col) ** 2 
        if distance < best_distance:
            best_distance = distance
            best_cell = (i, j)
    if best_cell is None:
        return None

    # the cell at row 3, column 5 yields box number 3 * 6 + 5 = 23.
    box_number = best_cell[0] * cols + best_cell[1]
    return best_cell