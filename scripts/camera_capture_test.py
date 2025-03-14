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
    Perform pattern recognition on the red plane images using ORB and BFMatcher.
    Returns the transformed corners (bounding box), rotation angle, and list of good matches.
    """
    orb = cv2.ORB_create()

    kp1, des1 = orb.detectAndCompute(template, None)
    kp2, des2 = orb.detectAndCompute(scene, None)

    if des1 is None or des2 is None:
        return None, None, []

    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    raw_matches = bf.knnMatch(des1, des2, k=2)
    
    good_matches = []
    ratio_test = 0.97  # Lowe's ratio test threshold
    for m, n in raw_matches:
        if m.distance < ratio_test * n.distance:
            good_matches.append(m)

    required_matches = int(match_ratio_threshold * len(kp1)) if kp1 else 0
    if len(kp1) > 0 and len(good_matches) < required_matches:
        print(f"Not enough good matches: {len(good_matches)}/{len(kp1)}")
        return None, None, good_matches

    if len(good_matches) >= 4:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 10.0)
        h, w = template.shape[:2]
        pts = np.float32([[0, 0], [w, 0], [w, h], [0, h]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)

        # Compute rotation angle using the vector from the first to second point.
        pt1 = dst[0][0]
        pt2 = dst[1][0]
        angle = np.degrees(np.arctan2(pt2[1] - pt1[1], pt2[0] - pt1[0]))
        return dst, angle, good_matches
    else:
        return None, None, good_matches
def main():
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

    # Capture an image
    image = capture_image(camera)
    if image is None:
        print("Failed to capture image.")
        return

    # If the captured image is grayscale, convert it to BGR.
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # ---- Extract the red channel ("red plane") from the image ----
    red_plane = image[:, :, 2]

    cropped_red_plane_scene = red_plane[:, 591:2088]
    
    # Optionally, if you want to keep the three-channel format for display or further processing:
    red_plane_color = cv2.merge([red_plane, red_plane, red_plane])
    # ---------------------------------------------------------------

    # Load the template image.
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        print(f"Template image not found at {template_path}")
        return

    # Optionally, if you want to use the red channel from the template as well:
    template_red = template[:, :, 2]
    # For instance, use template_red and red_plane for pattern recognition:
    bbox, angle, good_matches = pattern_recognition(template_red, cropped_red_plane_scene)
    
    output = cropped_red_plane_scene.copy()

    if bbox is not None:
        # Convert bounding box corners to integer coordinates
        bbox_int = np.int32(bbox)

        # Compute the center of the bounding box
        center_x = np.mean(bbox_int[:, 0, 0])
        center_y = np.mean(bbox_int[:, 0, 1])
        center_point = (int(center_x), int(center_y))

        # Compute approximate width and height by averaging distances between opposing edges.
        w1 = np.linalg.norm(bbox_int[0][0] - bbox_int[1][0])  # top edge
        w2 = np.linalg.norm(bbox_int[3][0] - bbox_int[2][0])  # bottom edge
        width = (w1 + w2) / 2.0

        h1 = np.linalg.norm(bbox_int[0][0] - bbox_int[3][0])  # left edge
        h2 = np.linalg.norm(bbox_int[1][0] - bbox_int[2][0])  # right edge
        height = (h1 + h2) / 2.0

        # Set maximum allowed dimensions: 450x450 pixels.
        MAX_WIDTH = 450
        MAX_HEIGHT = 450

        # Check if scaling is needed
        scale = 1.0
        if width > MAX_WIDTH or height > MAX_HEIGHT:
            scale = min(MAX_WIDTH / width, MAX_HEIGHT / height)
            # Scale each corner relative to the center of the bounding box.
            bbox_scaled = []
            for pt in bbox_int:
                new_x = center_x + scale * (pt[0][0] - center_x)
                new_y = center_y + scale * (pt[0][1] - center_y)
                bbox_scaled.append([[int(new_x), int(new_y)]])
            bbox_int = np.array(bbox_scaled)

        # Draw the (possibly scaled) bounding box
        cv2.polylines(output, [bbox_int], True, (0, 255, 0), 3, cv2.LINE_AA)

        # Draw the center point
        cv2.circle(output, center_point, 5, (0, 255, 255), -1)

        # Annotate the rotation angle and display center coordinates
        cv2.putText(output, f"Angle: {angle:.2f} deg", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(output, f"Center: ({int(center_x)}, {int(center_y)})", (10, 70),
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
