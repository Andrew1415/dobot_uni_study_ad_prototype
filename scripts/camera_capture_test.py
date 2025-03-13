import cv2
import numpy as np
import argparse
from pypylon import pylon

def connect_camera(serial_number):
    """
    Connect to a Basler USB camera using its serial number.
    """
    # Get the transport layer factory and enumerate all connected devices.
    tl_factory = pylon.TlFactory.GetInstance()
    devices = tl_factory.EnumerateDevices()

    camera = None
    for device in devices:
        if device.GetSerialNumber() == serial_number:
            camera = pylon.InstantCamera(tl_factory.CreateDevice(device))
            break

    if camera is None:
        raise Exception(f"Camera with serial number {serial_number} not found")
    
    return camera

def capture_image(camera):
    """
    Capture a single image from the camera.
    """
    camera.Open()
    # Start grabbing one image with the latest image strategy.
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    # Retrieve one image with a timeout.
    result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    
    if result.GrabSucceeded():
        image = result.Array
    else:
        image = None

    result.Release()
    camera.StopGrabbing()
    camera.Close()
    return image

def pattern_recognition(template, scene, match_ratio_threshold=0.50):
    """
    Perform pattern recognition to find the template in the scene.
    Uses ORB to detect keypoints and BFMatcher with Lowe's ratio test.
    The function checks if at least `match_ratio_threshold` (75% by default)
    of the template's keypoints have good matches.
    Returns the transformed corners (bounding box), rotation angle,
    and the list of good matches if sufficient matches are found.
    """
    # Initialize ORB detector.
    orb = cv2.ORB_create()

    # Detect keypoints and compute descriptors for both images.
    kp1, des1 = orb.detectAndCompute(template, None)
    kp2, des2 = orb.detectAndCompute(scene, None)

    if des1 is None or des2 is None:
        return None, None, []

    # Use BFMatcher with knnMatch for Lowe's ratio test.
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    raw_matches = bf.knnMatch(des1, des2, k=2)
    
    good_matches = []
    for m, n in raw_matches:
        # Lowe's ratio test: here we use 0.75 (can be adjusted if needed)
        if m.distance < 0.95 * n.distance:
            good_matches.append(m)

    # Check if at least 75% of the template's keypoints have been matched.
    if len(kp1) > 0 and len(good_matches) < match_ratio_threshold * len(kp1):
        print(f"Insufficient pattern recognition: only {len(good_matches)}/{len(kp1)} keypoints matched.")
        return None, None, good_matches

    if len(good_matches) >= 4:
        # Extract location of good matches.
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1,1,2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1,1,2)
        # Compute homography using RANSAC.
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        h, w = template.shape[:2]
        # Define template image corners.
        pts = np.float32([[0,0], [w,0], [w,h], [0,h]]).reshape(-1,1,2)
        # Transform the template corners to scene coordinates.
        dst = cv2.perspectiveTransform(pts, M)

        # Compute rotation angle using the vector from the first to second point.
        pt1 = dst[0][0]
        pt2 = dst[1][0]
        angle = np.degrees(np.arctan2(pt2[1] - pt1[1], pt2[0] - pt1[0]))
        return dst, angle, good_matches
    else:
        return None, None, good_matches

def main():
    # Parse command-line arguments.
    parser = argparse.ArgumentParser(description="Basler Camera Capture and Pattern Recognition")
    parser.add_argument("serial_number", help="Basler camera serial number")
    parser.add_argument("template_path", help="Path to the template image for pattern recognition")
    args = parser.parse_args()

    serial_number = args.serial_number
    template_path = args.template_path

    try:
        camera = connect_camera(serial_number)
    except Exception as e:
        print(e)
        return

    # Capture an image from the camera.
    image = capture_image(camera)
    if image is None:
        print("Failed to capture image.")
        return

    # Load the template image.
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        print(f"Template image not found at {template_path}")
        return
    # Convert template to grayscale if your captured image is also grayscale
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # Run pattern recognition.
    bbox, angle, good_matches = pattern_recognition(template_gray, image)
    output = image.copy()

    if bbox is not None:
        # Draw bounding box around detected template.
        bbox = np.int32(bbox)
        cv2.polylines(output, [bbox], True, (0, 255, 0), 3, cv2.LINE_AA)
        # Annotate rotation angle.
        cv2.putText(output, f"Angle: {angle:.2f} deg", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        cv2.putText(output, "Not enough matches found", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the result.
    image_3 = cv2.resize(output, (1280, 720))
    cv2.imshow("Detected Pattern", image_3)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    while True:
        main()
