import cv2
import os

image_path = r"C:\Users\andri\OneDrive - ku.lt\Uni_HomeWork\Bakis\kode\pi-dobot-gui\img\test_img2.png"

if not os.path.exists(image_path):
    print(f"Error: File {image_path} not found!")
    exit()

image = cv2.imread(image_path)
if image is None:
    print("Error: OpenCV failed to load the image!")
    exit()

cv2.imshow("Loaded Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
