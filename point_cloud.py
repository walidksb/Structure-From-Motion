import numpy as np
import open3d as o3d

def export_point_cloud(points, colors, filename="output.ply"):
    """Save a point cloud (.ply)."""
    pc = o3d.geometry.PointCloud()
    pc.points = o3d.utility.Vector3dVector(points)
    pc.colors = o3d.utility.Vector3dVector(colors / 255.0)

    o3d.io.write_point_cloud(filename, pc)
    print(f"✅ Point cloud saved: {filename}")
