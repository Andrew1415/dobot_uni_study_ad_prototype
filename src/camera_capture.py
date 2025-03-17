import cv2
import numpy as np
from pypylon import pylon


def capture_img(camera_serial: str):
    """
    Captures an image from a Basler USB camera found by serial number.
    
    :param camera_serial: The serial number of the camera to use.
    :return: The captured image in OpenCV (RGB) format.
    """
    try:
        # Find all connected cameras
        tl_factory = pylon.TlFactory.GetInstance()
        devices = tl_factory.EnumerateDevices()

        # Search for the camera by its serial number
        camera = None
        for device in devices:
            if device.GetSerialNumber() == camera_serial:
                camera = pylon.InstantCamera(tl_factory.CreateDevice(device))
                break

        if camera is None:
            raise ValueError(f"Camera with serial number {camera_serial} not found!")

        # Open camera and grab one image
        camera.Open()
        camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if grab_result.GrabSucceeded():
            # Convert image to OpenCV format
            img = grab_result.Array
            img = cv2.cvtColor(img, cv2.COLOR_BAYER_BG2RGB)  # Convert to RGB if needed
            grab_result.Release()
        else:
            raise RuntimeError("Failed to capture image")

        # Close camera connection
        camera.Close()

        return img

    except Exception as e:
        print(f"Error capturing image: {e}")
        return None


def find_candy(img, template_img):
    
    method = cv2.TM_SQDIFF_NORMED

    template = template_img
    h, w = template.shape

    

    # You'll add the real implementation later
    return "10.0,15.2,5.5,0.0"


def find_leaflet_z():
    """
    Placeholder function for finding the Z coordinate of a leaflet.

    :return: The Z coordinate as a float.
    """
    # You'll add the real implementation later
    return 5.0


if __name__ == "__main__":
    # Example usage
    candy_cam_serial = "12345678"  # Replace with actual serial number
    leaflet_cam_serial = "87654321"  # Replace with actual serial number

    # Capture an image from the candy camera
    candy_img = capture_img(candy_cam_serial)
    if candy_img is not None:
        print("Candy camera image captured successfully.")

    # Capture an image from the leaflet camera
    leaflet_img = capture_img(leaflet_cam_serial)
    if leaflet_img is not None:
        print("Leaflet camera image captured successfully.")

    # Find candy coordinates
    candy_coords = find_candy()
    print(f"Candy found at: {candy_coords}")

    # Find leaflet Z coordinate
    leaflet_z = find_leaflet_z()
    print(f"Leaflet Z coordinate: {leaflet_z}")
