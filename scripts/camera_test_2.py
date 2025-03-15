# import cv2
# import numpy as np
# from pypylon import pylon

# while True:
#     # --------------------------
#     # 1. Connect to Basler Camera by Serial
#     # --------------------------
#     camera_serial = '23984475'  # Replace with your camera's serial

#     # Get the transport layer factory
#     tl_factory = pylon.TlFactory.GetInstance()
#     devices = tl_factory.EnumerateDevices()

#     selected_device = None
#     for device in devices:
#         if device.GetSerialNumber() == camera_serial:
#             selected_device = device
#             break

#     if selected_device is None:
#         print(f"Camera with serial {camera_serial} not found.")
#         exit(1)

#     # Create and open the camera
#     camera = pylon.InstantCamera(tl_factory.CreateDevice(selected_device))
#     camera.Open()

#     # --------------------------
#     # 2. Capture an Image
#     # --------------------------
#     camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
#     grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

#     if grab_result.GrabSucceeded():
#         # Convert to a NumPy array
#         scene_img = grab_result.Array
#         print("Image captured successfully.")
#     else:
#         print("Failed to grab image.")
#         camera.Close()
#         exit(1)

#     grab_result.Release()
#     camera.StopGrabbing()
#     camera.Close()

#     # --------------------------
#     # 3. Load the Reference Image
#     # --------------------------
#     ref_img = cv2.imread('.\img\candy2.png', cv2.IMREAD_COLOR)
#     if ref_img is None:
#         print("Failed to load reference image. Check the path.")
#         exit(1)

#     # --------------------------
#     # 4. Convert Images to Grayscale (for ORB)
#     # --------------------------
#     # If your camera output is already grayscale, this step might be unnecessary.
#     # Check dimensions: shape[2] = 3 implies a color image.
#     if scene_img.ndim == 3 and scene_img.shape[2] == 3:
#         scene_gray = cv2.cvtColor(scene_img, cv2.COLOR_BGR2GRAY)
#     else:
#         scene_gray = scene_img  # already grayscale

#     if ref_img.ndim == 3 and ref_img.shape[2] == 3:
#         ref_gray = cv2.cvtColor(ref_img, cv2.COLOR_BGR2GRAY)
#     else:
#         ref_gray = ref_img  # already grayscale

#     # --------------------------
#     # 5. ORB Feature Detection & Description
#     # --------------------------
#     orb = cv2.ORB_create(nfeatures=5000)

#     kp_ref, des_ref = orb.detectAndCompute(ref_gray, None)
#     kp_scene, des_scene = orb.detectAndCompute(scene_gray, None)

#     if des_ref is None or des_scene is None:
#         print("Could not compute descriptors. Check your images.")
#         exit(1)

#     # --------------------------
#     # 6. Brute Force Matching
#     # --------------------------
#     bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
#     matches = bf.match(des_ref, des_scene)

#     # Sort matches by ascending distance (best matches first)
#     matches = sorted(matches, key=lambda x: x.distance)

#     # Filter out top matches (adjust the slice as needed)
#     good_matches = matches[:1000]

#     # Optional: Draw matches for visualization
#     matched_img = cv2.drawMatches(
#         ref_img, kp_ref,
#         scene_img, kp_scene,
#         good_matches, None,
#         flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
#     )
#     image_3 = cv2.resize(matched_img, (1280, 720))
#     cv2.imshow("ORB Matches (top 50)", image_3)
#     cv2.waitKey(1)  # keep the window open; 1ms wait so we can proceed

#     # --------------------------
#     # 7. Localize the Object Using Homography
#     # --------------------------
#     MIN_MATCH_COUNT = 20  # minimum number of good matches to attempt homography

#     if len(good_matches) >= MIN_MATCH_COUNT:
#         # Extract location of good matches
#         ref_pts = np.float32([kp_ref[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
#         scene_pts = np.float32([kp_scene[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

#         # Compute homography using RANSAC
#         M, mask = cv2.findHomography(ref_pts, scene_pts, cv2.RANSAC, 5.0)

#         # if M is not None:
#         #     # Get the corners of the reference image
#         #     h, w, _ = ref_img.shape
#         #     corners = np.float32([[0, 0],
#         #                         [w, 0],
#         #                         [w, h],
#         #                         [0, h]]).reshape(-1, 1, 2)

#         #     # Transform the corners to the scene
#         #     transformed_corners = cv2.perspectiveTransform(corners, M)

#         #     # Draw the polygon around the detected object on the scene image
#         #     scene_detected = scene_img.copy()
#         #     cv2.polylines(
#         #         scene_detected,
#         #         [np.int32(transformed_corners)],
#         #         isClosed=True,
#         #         color=(0, 255, 0),
#         #         thickness=3
#         #     )
#         #     image_4 = cv2.resize(scene_detected, (1280, 720))
#         #     cv2.imshow("Detected Object", image_4)
#         #     cv2.waitKey(0)
#         #     cv2.destroyAllWindows()

#         if M is not None:
#             # Get the corners of the reference image
#             h, w, _ = ref_img.shape
#             corners = np.float32([[0, 0],
#                                 [w, 0],
#                                 [w, h],
#                                 [0, h]]).reshape(-1, 1, 2)

#             # Transform the corners to the scene
#             transformed_corners = cv2.perspectiveTransform(corners, M)
            
#             # Compute a rotated rectangle (minimum area rectangle) for the transformed corners
#             rot_rect = cv2.minAreaRect(np.int32(transformed_corners))
#             (cx, cy), (w_box, h_box), angle = rot_rect

#             # Determine the square side length: maximum of the rectangle's dimensions, clamped between 200 and 450.
#             side = max(w_box, h_box)
#             side = max(200, min(side, 450))

#             # Compute half side length for convenience.
#             d = side / 2.0

#             # Define the square's corner offsets relative to its center
#             # The order here is: top-left, top-right, bottom-right, bottom-left.
#             square_pts = np.array([
#                 [-d, -d],
#                 [ d, -d],
#                 [ d,  d],
#                 [-d,  d]
#             ])

#             # Convert the detected angle (in degrees) to radians.
#             theta = np.deg2rad(angle)
#             # Construct a 2D rotation matrix.
#             R = np.array([[np.cos(theta), -np.sin(theta)],
#                         [np.sin(theta),  np.cos(theta)]])

#             # Rotate the square points using the rotation matrix.
#             rotated_square = np.dot(square_pts, R.T)
#             # Translate the rotated square to the detected object's center.
#             rotated_square += np.array([cx, cy])

#             # Draw the rotated square on a copy of the scene image.
#             scene_detected = scene_img.copy()
#             pts = np.int32(rotated_square).reshape((-1, 1, 2))
#             cv2.polylines(scene_detected, [pts], isClosed=True, color=(0, 255, 0), thickness=3)

#             image_4 = cv2.resize(scene_detected, (1280, 720))
#             cv2.imshow("Detected Object", image_4)
#             cv2.waitKey(0)
#             cv2.destroyAllWindows()

#         else:
#             print("Homography could not be computed. Not enough consistent matches.")
#             cv2.waitKey(0)
#             cv2.destroyAllWindows()
#     else:
#         print(f"Not enough matches for homography. Found {len(good_matches)}; need at least {MIN_MATCH_COUNT}.")
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()


# import cv2
# import numpy as np
# from pypylon import pylon
# from sklearn.cluster import DBSCAN

# while True:
#     # --------------------------
#     # 1. Connect to Basler Camera by Serial
#     # --------------------------
#     camera_serial = '23984475'  # Replace with your camera's serial

#     # Get the transport layer factory
#     tl_factory = pylon.TlFactory.GetInstance()
#     devices = tl_factory.EnumerateDevices()

#     selected_device = None
#     for device in devices:
#         if device.GetSerialNumber() == camera_serial:
#             selected_device = device
#             break

#     if selected_device is None:
#         print(f"Camera with serial {camera_serial} not found.")
#         exit(1)

#     # Create and open the camera
#     camera = pylon.InstantCamera(tl_factory.CreateDevice(selected_device))
#     camera.Open()

#     # --------------------------
#     # 2. Capture an Image
#     # --------------------------
#     camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
#     grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

#     if grab_result.GrabSucceeded():
#         # Convert to a NumPy array
#         scene_img = grab_result.Array
#         print("Image captured successfully.")
#     else:
#         print("Failed to grab image.")
#         camera.Close()
#         exit(1)

#     grab_result.Release()
#     camera.StopGrabbing()
#     camera.Close()

#     # --------------------------
#     # 3. Load the Reference Image
#     # --------------------------
#     ref_img = cv2.imread(r'.\img\candy_y2.png', cv2.IMREAD_COLOR)
#     if ref_img is None:
#         print("Failed to load reference image. Check the path.")
#         exit(1)

#     # --------------------------
#     # 4. Convert Images to Grayscale (for ORB)
#     # --------------------------
#     # If your camera output is already grayscale, this step might be unnecessary.
#     if scene_img.ndim == 3 and scene_img.shape[2] == 3:
#         scene_gray = cv2.cvtColor(scene_img, cv2.COLOR_BGR2GRAY)
#     else:
#         scene_gray = scene_img  # already grayscale

#     if ref_img.ndim == 3 and ref_img.shape[2] == 3:
#         ref_gray = cv2.cvtColor(ref_img, cv2.COLOR_BGR2GRAY)
#     else:
#         ref_gray = ref_img  # already grayscale

#     # --------------------------
#     # 5. ORB Feature Detection & Description
#     # --------------------------
#     orb = cv2.ORB_create(nfeatures=2000)

#     kp_ref, des_ref = orb.detectAndCompute(ref_gray, None)
#     kp_scene, des_scene = orb.detectAndCompute(scene_gray, None)

#     if des_ref is None or des_scene is None:
#         print("Could not compute descriptors. Check your images.")
#         exit(1)

#     # --------------------------
#     # 6. Brute Force Matching
#     # --------------------------
#     bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
#     matches_all = bf.knnMatch(des_ref, des_scene, k=2)

#     good_matches = []
#     ratio_thresh = 0.5  # typical value, adjust as needed
#     for m, n in matches_all:
#         if m.distance < ratio_thresh * n.distance:
#             good_matches.append(m)


#     # Use the top 50 matches for further processing
#     # good_matches = matches[:50]

#     # --------------------------
#     # 7. Cluster Matches to Select One Instance
#     # --------------------------
#     # Extract scene keypoints from good matches
#     scene_points = np.float32([kp_scene[m.trainIdx].pt for m in good_matches])
#     if len(scene_points) > 0:
#         # Cluster the keypoints using DBSCAN; adjust eps and min_samples as needed
#         clustering = DBSCAN(eps=20, min_samples=3).fit(scene_points)
#         labels = clustering.labels_
#         # Choose the cluster with the highest number of points (ignore noise label -1)
#         best_cluster = None
#         best_cluster_count = 0
#         for label in set(labels):
#             if label == -1:
#                 continue
#             count = np.sum(labels == label)
#             if count > best_cluster_count:
#                 best_cluster_count = count
#                 best_cluster = label

#         if best_cluster is not None:
#             cluster_indices = [i for i, lab in enumerate(labels) if lab == best_cluster]
#             selected_matches = [good_matches[i] for i in cluster_indices]
#         else:
#             selected_matches = good_matches  # Fallback if no valid cluster is found
#     else:
#         selected_matches = good_matches

#     # Optional: Draw matches for visualization
#     matched_img = cv2.drawMatches(
#         ref_img, kp_ref,
#         scene_img, kp_scene,
#         selected_matches, None,
#         flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
#     )
#     image_3 = cv2.resize(matched_img, (1280, 720))
#     cv2.imshow("ORB Matches (selected instance)", image_3)
#     cv2.waitKey(1)  # brief wait to update the window

#     # --------------------------
#     # 8. Localize the Object Using Homography
#     # --------------------------
#     MIN_MATCH_COUNT = 10  # minimum number of good matches to attempt homography

#     if len(selected_matches) >= MIN_MATCH_COUNT:
#         ref_pts = np.float32([kp_ref[m.queryIdx].pt for m in selected_matches]).reshape(-1, 1, 2)
#         scene_pts = np.float32([kp_scene[m.trainIdx].pt for m in selected_matches]).reshape(-1, 1, 2)

#         # Compute homography using RANSAC
#         M, mask = cv2.findHomography(ref_pts, scene_pts, cv2.RANSAC, 5.0)

#         if M is not None:
#             # Get the corners of the reference image
#             h, w, _ = ref_img.shape
#             corners = np.float32([[0, 0],
#                                    [w, 0],
#                                    [w, h],
#                                    [0, h]]).reshape(-1, 1, 2)

#             # Transform the corners to the scene
#             transformed_corners = cv2.perspectiveTransform(corners, M)

#             # Draw the polygon around the detected object on the scene image
#             scene_detected = scene_img.copy()
#             cv2.polylines(
#                 scene_detected,
#                 [np.int32(transformed_corners)],
#                 isClosed=True,
#                 color=(0, 255, 0),
#                 thickness=3
#             )
#             image_4 = cv2.resize(scene_detected, (1280, 720))
#             cv2.imshow("Detected Object", image_4)
#             key = cv2.waitKey(0)
#             if key == 27:  # ESC key to break out of the loop
#                 cv2.destroyAllWindows()
#                 break
#         else:
#             print("Homography could not be computed. Not enough consistent matches.")
#             cv2.waitKey(0)
#             cv2.destroyAllWindows()
#     else:
#         print(f"Not enough matches for homography. Found {len(selected_matches)}; need at least {MIN_MATCH_COUNT}.")
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()



# import cv2
# import numpy as np
# from pypylon import pylon
# from sklearn.cluster import DBSCAN  # Make sure you have scikit-learn installed

# # ... [Your camera capture and image loading code remains the same] ...

# while True:
#     # --------------------------
#     # 1. Connect to Basler Camera by Serial
#     # --------------------------
#     camera_serial = '23984475'  # Replace with your camera's serial

#     # Get the transport layer factory
#     tl_factory = pylon.TlFactory.GetInstance()
#     devices = tl_factory.EnumerateDevices()

#     selected_device = None
#     for device in devices:
#         if device.GetSerialNumber() == camera_serial:
#             selected_device = device
#             break

#     if selected_device is None:
#         print(f"Camera with serial {camera_serial} not found.")
#         exit(1)

#     # Create and open the camera
#     camera = pylon.InstantCamera(tl_factory.CreateDevice(selected_device))
#     camera.Open()

#     # --------------------------
#     # 2. Capture an Image
#     # --------------------------
#     camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
#     grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

#     if grab_result.GrabSucceeded():
#         # Convert to a NumPy array
#         scene_img = grab_result.Array
#         print("Image captured successfully.")
#     else:
#         print("Failed to grab image.")
#         camera.Close()
#         exit(1)

#     grab_result.Release()
#     camera.StopGrabbing()
#     camera.Close()

#     # --------------------------
#     # 3. Load the Reference Image
#     # --------------------------
#     ref_img = cv2.imread('.\img\candy_r.png', cv2.IMREAD_COLOR)
#     if ref_img is None:
#         print("Failed to load reference image. Check the path.")
#         exit(1)

#     # --------------------------
#     # 4. Convert Images to Grayscale (for ORB)
#     # --------------------------
#     # If your camera output is already grayscale, this step might be unnecessary.
#     # Check dimensions: shape[2] = 3 implies a color image.
#     if scene_img.ndim == 3 and scene_img.shape[2] == 3:
#         scene_gray = cv2.cvtColor(scene_img, cv2.COLOR_BGR2GRAY)
#     else:
#         scene_gray = scene_img  # already grayscale

#     if ref_img.ndim == 3 and ref_img.shape[2] == 3:
#         ref_gray = cv2.cvtColor(ref_img, cv2.COLOR_BGR2GRAY)
#     else:
#         ref_gray = ref_img  # already grayscale


# # --------------------------
# # 5. ORB Feature Detection & Description
# # --------------------------
#     orb = cv2.ORB_create(nfeatures=2000)
#     kp_ref, des_ref = orb.detectAndCompute(ref_gray, None)
#     kp_scene, des_scene = orb.detectAndCompute(scene_gray, None)

#     if des_ref is None or des_scene is None:
#         print("Could not compute descriptors. Check your images.")
#         exit(1)

#     # --------------------------
#     # 6. Brute Force Matching
#     # --------------------------
#     bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
#     matches = bf.match(des_ref, des_scene)
#     matches = sorted(matches, key=lambda x: x.distance)
#     good_matches = matches[:100]

#     # Optional: draw all matches for reference
#     matched_img = cv2.drawMatches(
#         ref_img, kp_ref,
#         scene_img, kp_scene,
#         good_matches, None,
#         flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
#     )
#     cv2.imshow("ORB Matches (top 50)", cv2.resize(matched_img, (1280, 720)))
#     cv2.waitKey(1)

#     # --------------------------
#     # 7. Clustering Matches to Handle Multiple Objects
#     # --------------------------
#     # Extract scene keypoint coordinates from good matches
#     scene_points = np.float32([kp_scene[m.trainIdx].pt for m in good_matches])

#     # Use DBSCAN to cluster these points. Adjust eps and min_samples as needed.
#     dbscan = DBSCAN(eps=50, min_samples=3).fit(scene_points)
#     labels = dbscan.labels_
#     unique_labels = set(labels)
#     if -1 in unique_labels:
#         unique_labels.remove(-1)  # Remove noise

#     if not unique_labels:
#         print("No clusters found. Cannot isolate a specific instance.")
#         exit(1)

#     # For example, select the cluster with the largest number of points
#     best_cluster = max(unique_labels, key=lambda l: list(labels).count(l))
#     cluster_matches = [good_matches[i] for i in range(len(good_matches)) if labels[i] == best_cluster]

#     MIN_MATCH_COUNT = 10
#     if len(cluster_matches) < MIN_MATCH_COUNT:
#         print(f"Not enough matches in the best cluster ({len(cluster_matches)}).")
#         exit(1)

#     # --------------------------
#     # 8. Localize the Object Using Homography on the Selected Cluster
#     # --------------------------
#     ref_pts_cluster = np.float32([kp_ref[m.queryIdx].pt for m in cluster_matches]).reshape(-1, 1, 2)
#     scene_pts_cluster = np.float32([kp_scene[m.trainIdx].pt for m in cluster_matches]).reshape(-1, 1, 2)

#     M, mask = cv2.findHomography(ref_pts_cluster, scene_pts_cluster, cv2.RANSAC, 5.0)
#     if M is not None:
#         # Get the corners of the reference image.
#         h, w, _ = ref_img.shape
#         corners = np.float32([[0, 0],
#                             [w, 0],
#                             [w, h],
#                             [0, h]]).reshape(-1, 1, 2)
#         transformed_corners = cv2.perspectiveTransform(corners, M)
        
#         # Get a rotated rectangle (minimum area) for the transformed corners.
#         rot_rect = cv2.minAreaRect(np.int32(transformed_corners))
#         (cx, cy), (w_box, h_box), angle = rot_rect

#         # Determine square side length: choose the maximum of the width or height and clamp it.
#         side = max(w_box, h_box)
#         side = max(200, min(side, 450))
#         d = side / 2.0

#         # Define a square centered at (0,0)
#         square_pts = np.array([
#             [-d, -d],
#             [ d, -d],
#             [ d,  d],
#             [-d,  d]
#         ])

#         # Rotate the square to match the detected object's orientation.
#         theta = np.deg2rad(angle)
#         R = np.array([[np.cos(theta), -np.sin(theta)],
#                     [np.sin(theta),  np.cos(theta)]])
#         rotated_square = np.dot(square_pts, R.T) + np.array([cx, cy])

#         # Draw the rotated square on a copy of the scene image.
#         scene_detected = scene_img.copy()
#         pts = np.int32(rotated_square).reshape((-1, 1, 2))
#         cv2.polylines(scene_detected, [pts], isClosed=True, color=(0, 255, 0), thickness=3)

#         image_4 = cv2.resize(scene_detected, (1280, 720))
#         cv2.imshow("Detected Object", image_4)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()
#     else:
#         print("Homography could not be computed for the selected cluster.")
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()


import cv2
import numpy as np
from sklearn.cluster import DBSCAN
from pypylon import pylon

def main():
    # ----------------------------------------------------------------
    # 1. Connect to Basler Camera by Serial and Capture an Image
    # ----------------------------------------------------------------
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
        return

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
        return

    grab_result.Release()
    camera.StopGrabbing()
    camera.Close()

    # ----------------------------------------------------------------
    # 2. Load the Reference Image
    # ----------------------------------------------------------------
    ref_path = './img/candy2.png'  # <-- Update to your reference image path
    ref_img = cv2.imread(ref_path, cv2.IMREAD_COLOR)
    if ref_img is None:
        print(f"Failed to load reference image from '{ref_path}'.")
        return

    # ----------------------------------------------------------------
    # 3. Convert Images to Grayscale (if needed)
    # ----------------------------------------------------------------
    # Scene
    if scene_img.ndim == 3 and scene_img.shape[2] == 3:
        scene_gray = cv2.cvtColor(scene_img, cv2.COLOR_BGR2GRAY)
    else:
        scene_gray = scene_img  # already grayscale

    # Reference
    if ref_img.ndim == 3 and ref_img.shape[2] == 3:
        ref_gray = cv2.cvtColor(ref_img, cv2.COLOR_BGR2GRAY)
    else:
        ref_gray = ref_img  # already grayscale

    # ----------------------------------------------------------------
    # 4. ORB Feature Detection & Description
    # ----------------------------------------------------------------
    orb = cv2.ORB_create(nfeatures=10000)
    kp_ref, des_ref = orb.detectAndCompute(ref_gray, None)
    kp_scene, des_scene = orb.detectAndCompute(scene_gray, None)

    if des_ref is None or des_scene is None:
        print("Could not compute descriptors. Check your images.")
        return

    # ----------------------------------------------------------------
    # 5. Brute Force Matching
    # ----------------------------------------------------------------
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des_ref, des_scene)

    # Sort matches by ascending distance (best matches first)
    matches = sorted(matches, key=lambda x: x.distance)

    # Take top N matches (adjust as needed)
    good_matches = matches[:200]

    # Optional: visualize these top matches
    matched_img = cv2.drawMatches(
        ref_img, kp_ref,
        scene_img, kp_scene,
        good_matches, None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )
    cv2.imshow("ORB Matches (top 50)", cv2.resize(matched_img, (1280, 720)))
    cv2.waitKey(1)  # small delay so the window can update

    # ----------------------------------------------------------------
    # 6. Cluster the Good Matches to Handle Multiple Instances
    # ----------------------------------------------------------------
    # Extract the (x, y) coordinates of the matched keypoints in the scene
    scene_points = np.float32([kp_scene[m.trainIdx].pt for m in good_matches])

    # DBSCAN for clustering
    # Adjust 'eps' and 'min_samples' to match how close/far apart your objects are
    dbscan = DBSCAN(eps=50, min_samples=3).fit(scene_points)
    labels = dbscan.labels_  # Cluster labels for each point
    unique_labels = set(labels)

    # Remove the noise label (-1) if present
    if -1 in unique_labels:
        unique_labels.remove(-1)

    if not unique_labels:
        print("No valid clusters found. Cannot isolate a specific instance.")
        return

    # For example, pick the cluster with the most matches
    best_cluster = max(unique_labels, key=lambda c: list(labels).count(c))

    # Filter the matches so only those in the chosen cluster remain
    cluster_matches = [
        good_matches[i] for i in range(len(good_matches))
        if labels[i] == best_cluster
    ]

    # ----------------------------------------------------------------
    # 7. Localize the Object Using Homography on the Chosen Cluster
    # ----------------------------------------------------------------
    MIN_MATCH_COUNT = 20
    if len(cluster_matches) < MIN_MATCH_COUNT:
        print(f"Cluster has only {len(cluster_matches)} matches. Need at least {MIN_MATCH_COUNT}.")
        return

    # Compute homography from reference to scene using only the chosen cluster's matches
    ref_pts_cluster = np.float32([kp_ref[m.queryIdx].pt for m in cluster_matches]).reshape(-1, 1, 2)
    scene_pts_cluster = np.float32([kp_scene[m.trainIdx].pt for m in cluster_matches]).reshape(-1, 1, 2)

    M, _ = cv2.findHomography(ref_pts_cluster, scene_pts_cluster, cv2.RANSAC, 5.0)
    if M is None:
        print("Could not compute a valid homography for the selected cluster.")
        return

    # ----------------------------------------------------------------
    # 8. Draw the Detected Object in the Scene
    # ----------------------------------------------------------------
    # Option A: Draw the transformed corners of the reference image
    h, w, _ = ref_img.shape  # If ref_img is BGR; or use h, w = ref_img.shape if grayscale
    corners = np.float32([
        [0, 0],
        [w, 0],
        [w, h],
        [0, h]
        ]).reshape(-1, 1, 2)

    transformed_corners = cv2.perspectiveTransform(corners, M)
    scene_detected = scene_img.copy()
    x, y, w_box, h_box = cv2.boundingRect(np.int32(transformed_corners))
    # cv2.rectangle(scene_detected, (x, y), (x + w_box, y + h_box), (0, 255, 0), 3)

    # # Draw polygon around the detected instance
    
    cv2.polylines(scene_detected, [np.int32(transformed_corners)],
                  isClosed=True, color=(0, 255, 0), thickness=3)

    # Show the final result
    cv2.imshow("Detected Object (One Cluster)", cv2.resize(scene_detected, (1280, 720)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    while True:
        main()