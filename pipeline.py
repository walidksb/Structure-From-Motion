import cv2
import numpy as np
from calibration import calibrate_camera
from feature_matching import find_sift_matches
from triangulation import triangulate_points
from point_cloud import export_point_cloud
import os

def run_sfm(image_folder):
    K, dist = calibrate_camera(image_dir="Chessboard_Images", display=False)
    img_paths = sorted([image_folder + "/" + f for f in os.listdir(image_folder)])

    img1 = cv2.imread(img_paths[0])
    img2 = cv2.imread(img_paths[1])

    pts1, pts2 = find_sift_matches(img1, img2)

    E, mask = cv2.findEssentialMat(pts1, pts2, K)
    _, R, t, mask = cv2.recoverPose(E, pts1, pts2, K)

    P1 = K @ np.hstack((np.eye(3), np.zeros((3, 1))))
    P2 = K @ np.hstack((R, t))

    pts3d = triangulate_points(P1, P2, pts1, pts2)

    # Get point color from image
    colors = img1[pts1[:, 1].astype(int), pts1[:, 0].astype(int)]

    export_point_cloud(pts3d, colors, "output.ply")
