# 🧱 Structure from Motion (SfM) — Python + OpenCV + NumPy + Open3D

This project implements a full **Structure-from-Motion (SfM)** pipeline using Python and OpenCV. It reconstructs a **3D point cloud** from multiple 2D images of a static scene by estimating camera poses and triangulating 3D points.

The pipeline includes:
- ✅ Camera calibration
- ✅ Feature detection and matching (SIFT)
- ✅ Essential matrix and pose recovery
- ✅ Triangulation of 3D points
- ✅ Optional bundle adjustment for refinement
- ✅ Exporting the final 3D point cloud (.ply)

---

## 🚀 Overview

**Structure from Motion (SfM)** is a computer vision technique that reconstructs a 3D scene from multiple 2D images taken from different viewpoints. This implementation follows the classical SfM workflow:

1. **Camera Calibration** — Estimate intrinsic parameters (K, distortion) using checkerboard images.
2. **Feature Extraction & Matching** — Detect keypoints with SIFT and match across image pairs.
3. **Pose Estimation** — Recover relative rotation (R) and translation (t) using the essential matrix.
4. **Triangulation** — Compute 3D coordinates of matched feature points.
5. **Bundle Adjustment** — (Optional) Refine camera parameters and 3D structure.
6. **Point Cloud Generation** — Save the resulting 3D structure as a `.ply` file viewable in Meshlab or Open3D.

---

## 📁 Project Structure

```
SfM-Project/
│
├── main.py                # Entry point – runs the SFM pipeline
├── pipeline.py            # Main pipeline logic (calls all modules)
├── calibration.py         # Camera calibration using chessboard images
├── feature_matching.py    # SIFT-based keypoint detection & matching
├── triangulation.py       # 3D point triangulation from image pairs
├── point_cloud.py         # Export final point cloud using Open3D
├── bundle_adjustment.py   # (Optional) Non-linear optimization
├── Chessboard_Images/     # Folder for calibration photos
├── photos/                # Folder with scene images for reconstruction
└── camera_calib.npz       # Saved calibration parameters (auto-generated)
```

---

## ⚙️ Installation

### 🧩 Requirements
- Python ≥ 3.9
- NumPy
- OpenCV ≥ 4.8.1 (use conda-forge build)
- Open3D
- SciPy
- Matplotlib
- tqdm

### 📦 Setup

Using **conda**:
```bash
conda create -n sfm python=3.10
conda activate sfm
conda install -c conda-forge opencv numpy open3d scipy matplotlib tqdm
```

---

## 🧠 How It Works

### 🪄 1. Camera Calibration
Uses a chessboard pattern (8×10 squares → 7×9 inner corners):
```bash
python calibration.py
```
Outputs:
- `camera_calib.npz` containing:
  - `K`: intrinsic camera matrix
  - `dist`: distortion coefficients
  - `error`: RMS reprojection error

### 🪞 2. Run the SfM Pipeline
After calibration, run the full reconstruction:
```bash
python main.py
```
This executes the following steps (from `pipeline.py`):
1. Load calibration parameters (`K`, `dist`)
2. Load two consecutive images
3. Find SIFT matches (`feature_matching.py`)
4. Estimate camera pose from essential matrix
5. Triangulate 3D points (`triangulation.py`)
6. Export the resulting 3D model as `output.ply`

---

## 🧱 Example Output

```
🔍 Found 10 chessboard images.
🖼️ Image size used for calibration: (780, 1040)
✅ Calibration successful
RMS re-projection error: 0.32
Camera Matrix:
[[1034.5    0.   512.1]
 [   0. 1033.2   384.5]
 [   0.     0.     1. ]]
Distortion coefficients:
[ 0.11 -0.08  0.00  0.00  0.02]
✅ Point cloud saved: output.ply
```

You can open the resulting `output.ply` in **Meshlab** or **Open3D** to visualize the 3D reconstruction.

---

## 🔧 Modules Breakdown

| File | Description |
|------|--------------|
| **calibration.py** | Detects checkerboard corners and computes intrinsic camera parameters |
| **feature_matching.py** | Extracts and matches SIFT features between image pairs |
| **triangulation.py** | Converts 2D point correspondences into 3D coordinates |
| **bundle_adjustment.py** | Performs optimization of poses and structure using least squares |
| **point_cloud.py** | Exports reconstructed 3D points and colors to `.ply` |

---

## 🌐 Example Visualization (using Open3D)

```python
import open3d as o3d
pcd = o3d.io.read_point_cloud("output.ply")
o3d.visualization.draw_geometries([pcd])
```

---

## 🧾 Notes
- Make sure your input photos have **overlapping fields of view** and **good texture**.
- Calibration should be done once per camera setup.
- Use **diverse angles** in chessboard photos to avoid instability.
- For better results, increase the number of images and optionally enable bundle adjustment.

---

## 🧑‍💻 Author
**Developed by:** Walid Kesbi and Kamilia Bouamara  
**Project:** Structure-from-Motion (SfM) Pipeline  
**University:** University of Science and Technology Houari Boumediene (USTHB)

---

## 🪪 License
This project is released under the **MIT License** — free for academic and personal use.

---

> 💡 Tip: You can extend this pipeline with multi-view reconstruction, dense matching, or camera pose graph optimization for a complete SfM system.

