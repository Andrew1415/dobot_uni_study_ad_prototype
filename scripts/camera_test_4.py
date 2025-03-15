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
    template = cv2.resize(cv2.imread('./img/candy2.png', 0), (0, 0), fx=0.5, fy=0.5)
    h, w = template.shape

    methods = [cv2.TM_SQDIFF_NORMED]
    # methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR,
                # cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]

    for method in methods:
        img2 = img.copy()

        result = cv2.matchTemplate(img2, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        threshold = 0.5
        # cv2.imshow('frame', img)
        if min_val < threshold:
            top_left = min_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv2.rectangle(img, top_left, bottom_right, 255, 5)
            cv2.imshow('Match', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("No valid match found.")