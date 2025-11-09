import cv2
import numpy as np

def triangulate_points(P1, P2, pts1, pts2):
    """Triangulate 3D points from 2D pairs."""
    pts1 = pts1.T
    pts2 = pts2.T

    pts_4d = cv2.triangulatePoints(P1, P2, pts1, pts2)
    pts_4d /= pts_4d[3]  # Convert to non-homogeneous

    return pts_4d[:3].T  # Return N × 3
