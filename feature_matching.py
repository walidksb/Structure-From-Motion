import cv2
import numpy as np

def find_sift_matches(img1, img2, ratio=0.75):
    """Extract SIFT features and return matching points."""
    sift = cv2.SIFT_create()

    kp1, desc1 = sift.detectAndCompute(img1, None)
    kp2, desc2 = sift.detectAndCompute(img2, None)

    matcher = cv2.BFMatcher()
    raw_matches = matcher.knnMatch(desc1, desc2, k=2)

    good_matches = [m for m, n in raw_matches if m.distance < ratio * n.distance]

    pts1 = np.float32([kp1[m.queryIdx].pt for m in good_matches])
    pts2 = np.float32([kp2[m.trainIdx].pt for m in good_matches])

    return pts1, pts2
