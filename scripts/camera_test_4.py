import numpy as np
import cv2
from pypylon import pylon

# ----------------------------------------------------------------
    # 1. Connect to Basler Camera by Serial and Capture an Image
    # ----------------------------------------------------------------
for x in range(100):
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
        # return

        # Create and open the camera
    camera = pylon.InstantCamera(tl_factory.CreateDevice(selected_device))
    camera.Open()

        # Start grabbing
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
    img = cv2.resize(scene_img, (0, 0), fx=0.5, fy=0.5)
    template = cv2.resize(cv2.imread('./img/candy_r2.png', 0), (0, 0), fx=0.5, fy=0.5)
    w, h = template.shape[1], template.shape[0]

    methods = [cv2.TM_SQDIFF_NORMED]
    # methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR,
                # cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]

    for method in methods:
        img2 = img.copy()

        result = cv2.matchTemplate(img2, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        threshold = 0.20
        cv2.imshow('frame', img)
        if min_val < threshold:
            top_left = min_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            center_x = top_left[0] + w // 2
            center_y = top_left[1] + h // 2
            print("Center of matched object:", (center_x, center_y))
            cv2.rectangle(img, top_left, bottom_right, 255, 5)
            cv2.circle(img, (center_x, center_y), 5, (255, 255, 255), -1)
            cv2.imshow('Match', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("No valid match found.")

# import numpy as np
# import cv2
# from pypylon import pylon

# def intersection_area(boxA, boxB):
#     """
#     Computes the intersection area between two boxes.
#     Each box is defined as (x1, y1, x2, y2) where (x1, y1) is the top-left
#     and (x2, y2) is the bottom-right corner.
#     """
#     xA = max(boxA[0], boxB[0])
#     yA = max(boxA[1], boxB[1])
#     xB = min(boxA[2], boxB[2])
#     yB = min(boxA[3], boxB[3])
#     if xB <= xA or yB <= yA:
#         return 0
#     return (xB - xA) * (yB - yA)

# for x in range(100):
#     camera_serial = '23984475'  # <-- Update to your camera's serial
#     tl_factory = pylon.TlFactory.GetInstance()
#     devices = tl_factory.EnumerateDevices()
#     selected_device = None
#     for device in devices:
#         if device.GetSerialNumber() == camera_serial:
#             selected_device = device
#             break

#     if selected_device is None:
#         print(f"Camera with serial {camera_serial} not found.")
#         continue

#     # Create and open the camera
#     camera = pylon.InstantCamera(tl_factory.CreateDevice(selected_device))
#     camera.Open()

#     # Start grabbing
#     camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
#     grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

#     if grab_result.GrabSucceeded():
#         # Convert to a NumPy array
#         scene_img = grab_result.Array
#         print("Scene image captured successfully.")
#     else:
#         print("Failed to grab image.")
#         camera.Close()
#         continue
#     camera.Close()

#     # Resize the scene image and load the template
#     img = cv2.resize(scene_img, (0, 0), fx=0.5, fy=0.5)
#     template = cv2.resize(cv2.imread('./img/candy_r4.png', 0), (0, 0), fx=0.5, fy=0.5)
#     w, h = template.shape[1], template.shape[0]

#     methods = [cv2.TM_SQDIFF_NORMED]

#     for method in methods:
#         img2 = img.copy()
#         result = cv2.matchTemplate(img2, template, method)
#         min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
#         threshold = 0.20
#         cv2.imshow('frame', img)

#         if min_val < threshold:
#             # Calculate the object's bounding box and center
#             top_left = min_loc
#             bottom_right = (top_left[0] + w, top_left[1] + h)
#             center_x = top_left[0] + w // 2
#             center_y = top_left[1] + h // 2
#             print("Center of matched object:", (center_x, center_y))

#             # Divide the image into a 6x8 grid
#             rows, cols = 4, 6
#             img_height, img_width = img.shape[:2]
#             cell_width = img_width // cols
#             cell_height = img_height // rows

#             # Define the object's bounding box as (x1, y1, x2, y2)
#             object_box = (top_left[0], top_left[1], bottom_right[0], bottom_right[1])
#             object_area = (bottom_right[0] - top_left[0]) * (bottom_right[1] - top_left[1])
#             valid_grid = False

#             # Check each grid cell to see if at least 80% of the object is contained in one cell.
#             for i in range(rows):
#                 for j in range(cols):
#                     cell_box = (j * cell_width, i * cell_height,
#                                 (j + 1) * cell_width, (i + 1) * cell_height)
#                     inter_area = intersection_area(object_box, cell_box)
#                     if object_area > 0 and (inter_area / object_area) >= 0.8:
#                         valid_grid = True
#                         break
#                 if valid_grid:
#                     break

#             if valid_grid:
#                 # Draw rectangle and center if the object is mostly contained in one grid cell
#                 cv2.rectangle(img, top_left, bottom_right, 255, 5)
#                 cv2.circle(img, (center_x, center_y), 5, (255, 255, 255), -1)
#                 cv2.imshow('Match', img)
#                 cv2.waitKey(0)
#                 cv2.destroyAllWindows()
#             else:
#                 print("Invalid match: Object is not mostly contained in one grid cell.")
#         else:
#             print("No valid match found.")
