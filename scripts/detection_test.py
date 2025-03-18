# import cv2
# import numpy as np

# # Function to detect the color
# def detect_color(image, color):
#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#     if color == "red":
#         lower_red1 = np.array([0, 120, 70])
#         upper_red1 = np.array([10, 255, 255])
#         lower_red2 = np.array([170, 120, 70])
#         upper_red2 = np.array([180, 255, 255])

#         mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
#         mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
#         mask = mask1 + mask2  # Combine both masks for red
#     elif color == "yellow":
#         lower_yellow = np.array([20, 100, 100])
#         upper_yellow = np.array([30, 255, 255])
#         mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
#     else:
#         raise ValueError("Invalid color selection. Choose 'red' or 'yellow'.")

#     return mask

# # Function to divide the image into a grid and find the most colored cells
# def analyze_grid(mask, rows=4, cols=6):
#     height, width = mask.shape
#     cell_h, cell_w = height // rows, width // cols

#     grid_count = np.zeros((rows, cols))  # Store pixel count per grid cell

#     for i in range(rows):
#         for j in range(cols):
#             cell = mask[i * cell_h:(i + 1) * cell_h, j * cell_w:(j + 1) * cell_w]
#             grid_count[i, j] = np.sum(cell)  # Sum of white pixels in mask

#     max_value = np.max(grid_count)
#     if max_value == 0:
#         print("No significant color detected.")
#         return []

#     max_indices = np.argwhere(grid_count == max_value)
#     return [(row, col) for row, col in max_indices]

# # Load image

# image = cv2.resize(cv2.imread('./img/Image__2025-03-18__08-13-15.png'), (0, 0), fx=0.5, fy=0.5)  # Change to your image path

# color_to_detect = "red"  # Change to "yellow" if needed
# mask = detect_color(image, color_to_detect)
# cv2.imshow("Mask", mask)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# # Analyze the grid and find the cells with the most detected color
# highlighted_cells = analyze_grid(mask)

# # Print out the rows and columns of the most colored boxes
# for row, col in highlighted_cells:
#     print(f"Row: {row}, Column: {col}")



import cv2
import numpy as np

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
def analyze_grid(mask, rows=4, cols=6, threshold=0.2):
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
image = cv2.resize(cv2.imread('./img/Image__2025-03-17__11-57-13.png'), (0, 0), fx=0.5, fy=0.5)

color_to_detect = "yellow"  # Change to "yellow" if needed
mask = detect_color(image, color_to_detect)

# Analyze grid with 70% threshold
highlighted_cells = analyze_grid(mask)

# Display the result
for row, col in highlighted_cells:
    print(f"Row: {row}, Column: {col} (covered ≥ 70%)")

# Show the detected mask
cv2.imshow("Color Mask", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()
