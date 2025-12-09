#!/usr/bin/env python3

import rosbag
import rospy
import numpy as np
import sys
import os
from f110_msgs.msg import WpntArray, Wpnt

def raceline_csv_to_bag(csv_path, bag_path):
    """
    Convert raceline CSV to ROS bag format matching TC-Driver structure
    
    F1TENTH racetracks format: s_m; x_m; y_m; psi_rad; kappa_radpm; vx_mps; ax_mps2
    """
    
    # Load raceline CSV with semicolon delimiter, skip 3 header lines
    data = np.loadtxt(csv_path, delimiter=';', skiprows=3)
    
    print(f"Loaded {len(data)} waypoints from {csv_path}")
    print(f"CSV columns: {data.shape[1]}")
    
    # Create WpntArray message
    wpnt_array = WpntArray()
    wpnt_array.header.frame_id = "map"
    wpnt_array.header.stamp = rospy.Time(0)
    
    for i, row in enumerate(data):
        wpnt = Wpnt()
        
        # Column mapping for f1tenth_racetracks format:
        # 0: s_m (cumulative distance)
        # 1: x_m
        # 2: y_m  
        # 3: psi_rad (heading)
        # 4: kappa_radpm (curvature)
        # 5: vx_mps (velocity)
        # 6: ax_mps2 (acceleration)
        
        wpnt.s_m = float(row[0])
        wpnt.x_m = float(row[1])
        wpnt.y_m = float(row[2])
        wpnt.psi_rad = float(row[3])
        wpnt.vx_mps = float(row[5])
        
        # Track widths are NOT in this CSV format
        # Use default values (you'll need to add these manually or use centerline)
        wpnt.d_right = 1.0  # Default 1 meter
        wpnt.d_left = 1.0   # Default 1 meter
        
        wpnt_array.wpnts.append(wpnt)
    
    print(f"Track length: {data[-1, 0]:.2f} meters")
    print(f"Speed range: {data[:, 5].min():.2f} - {data[:, 5].max():.2f} m/s")
    
    # Write to bag
    bag = rosbag.Bag(bag_path, 'w')
    try:
        bag.write('/global_waypoints', wpnt_array)
        print(f"✓ Successfully created {bag_path} with {len(data)} waypoints")
    finally:
        bag.close()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 convert_tracks.py <raceline.csv> <output.bag>")
        print("Example: python3 convert_tracks.py f1tenth_racetracks/Austin/Austin_raceline.csv F110_ROS_Simulator/maps/Austin/global_wpnts.bag")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    bag_path = sys.argv[2]
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(bag_path), exist_ok=True)
    
    raceline_csv_to_bag(csv_path, bag_path)