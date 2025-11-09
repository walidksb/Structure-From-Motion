import cv2
import numpy as np
import glob
import os


def calibrate_camera(
    chessboard_size=(7, 9),     # (cols, rows) = inside corners → for 8×10 squares
    image_dir="Chessboard_Images",
    display=False
):
    """
    Perform camera calibration using chessboard images.

    Parameters
    ----------
    chessboard_size : tuple(int, int)
        Number of inside corners per chessboard row and column (cols, rows).
        For an 8×10 square checkerboard, use (7, 9).
    image_dir : str
        Path to directory containing calibration images.
    display : bool
        If True, displays detected corners for each image.

    Returns
    -------
    mtx : np.ndarray
        Intrinsic camera matrix.
    dist : np.ndarray
        Distortion coefficients.
    """

    # --- Prepare real-world 3D coordinates for the checkerboard pattern ---
    objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0 : chessboard_size[0], 0 : chessboard_size[1]].T.reshape(-1, 2)

    objpoints = []  # 3D points
    imgpoints = []  # 2D points

    # --- Load images ---
    base_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_path, image_dir)
    images = glob.glob(os.path.join(image_path, "*.jpg")) + glob.glob(os.path.join(image_path, "*.png"))

    if not images:
        raise FileNotFoundError(f"No calibration images found in: {image_path}")

    print(f"Found {len(images)} chessboard images.")
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # --- Detect corners ---
    for img_path in images:
        img = cv2.imread(img_path)
        if img is None:
            print(f"Cannot read {img_path}")
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print(f"Processing {os.path.basename(img_path)} with size {gray.shape}")

        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)
        if not ret:
            print(f"Chessboard not detected in {os.path.basename(img_path)}")
            continue

        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        if corners2 is not None and len(corners2) == chessboard_size[0] * chessboard_size[1]:
            objpoints.append(objp)
            imgpoints.append(corners2)

            if display:
                vis = img.copy()
                cv2.drawChessboardCorners(vis, chessboard_size, corners2, ret)
                cv2.imshow("Detected Corners", vis)
                cv2.waitKey(400)
        else:
            print(f"Corner refinement failed for {os.path.basename(img_path)}")

    cv2.destroyAllWindows()


    # --- Calibration block ---
    print("\nCalibrating camera...")

    # Convert and ensure contiguous memory layout
    objpoints = [np.ascontiguousarray(op, dtype=np.float32).reshape(-1, 1, 3) for op in objpoints]
    imgpoints = [np.ascontiguousarray(ip, dtype=np.float32).reshape(-1, 1, 2) for ip in imgpoints]


    img_shape = tuple(map(int, gray.shape[::-1]))
    print("Image size used for calibration:", img_shape)

    # Safer calibration flags (disable extra distortion parameters)
    flags = cv2.CALIB_FIX_K3

    try:
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
            objpoints, imgpoints, img_shape, None, None, flags=flags
        )
    except cv2.error as e:
        print("First calibration attempt failed:", e)
        print("Retrying with fewer images and simpler flags...")
        flags = 0
        subset = min(6, len(objpoints))
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
            objpoints[:subset], imgpoints[:subset], img_shape, None, None, flags=flags
        )

    print("Calibration successful")
    print("RMS re-projection error:", ret)
    print("Camera Matrix (intrinsic):\n", mtx)
    print("Distortion coefficients:\n", dist.ravel())

    save_path = os.path.join(base_path, "camera_calib.npz")
    np.savez(save_path, K=mtx, dist=dist, error=ret)
    print(f"Calibration saved to {save_path}")


    return mtx, dist


if __name__ == "__main__":
    calibrate_camera(display=True)
