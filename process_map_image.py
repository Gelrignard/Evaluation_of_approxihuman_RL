#!/usr/bin/env python3

import cv2
import numpy as np
import sys
import os
import argparse



def process_map_image(input_path, track_x=None, track_y=None):
    """
    1. Converts outside area (connected to 0,0) to black.
    2. If track_x and track_y are provided, keeps ONLY the connected component 
       containing that point (the track) and turns other white areas (infields) black.
    """
    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' not found.")
        sys.exit(1)

    print(f"Reading {input_path}...")
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    
    if img is None:
        print("Error: Failed to load image.")
        sys.exit(1)

    # 1. Threshold to binary (White > 220, else Black)
    _, binary = cv2.threshold(img, 220, 255, cv2.THRESH_BINARY)
    h, w = binary.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)

    # 2. Remove Outside: Flood fill from (0,0) with Black
    # Assumes (0,0) is outside the map.
    if binary[0,0] == 255:
        print("Flood filling outside from (0,0)...")
        cv2.floodFill(binary, mask, (0,0), 0)

    # 3. Remove Infield: Keep only the track component
    if track_x is not None and track_y is not None:
        print(f"Isolating track using seed point ({track_x}, {track_y})...")
        
        # Check if seed is valid
        if track_x < 0 or track_x >= w or track_y < 0 or track_y >= h:
            print("Error: Seed point is out of image bounds.")
            sys.exit(1)
            
        if binary[track_y, track_x] != 255:
            print(f"Warning: Seed point ({track_x}, {track_y}) is not white (value={binary[track_y, track_x]}).")
            print("Please pick a point strictly inside the white track area.")
            # We continue anyway, but floodFill might do nothing if it's black
        
        # Flood fill the TRACK with a temporary color (128 - Gray)
        # We need a new mask because the previous one was modified
        mask_track = np.zeros((h+2, w+2), np.uint8)
        cv2.floodFill(binary, mask_track, (track_x, track_y), 128)
        
        # Now:
        # 0   = Outside & Walls & Infield (if it was black)
        # 255 = Infield (still white because it wasn't connected to track)
        # 128 = Track
        
        # Turn remaining White (Infield) to Black
        binary[binary == 255] = 0
        
        # Turn Track (128) back to White
        binary[binary == 128] = 255
    else:
        print("No seed point provided. Infields might remain white.")
        print("To remove infields, run with: --x [val] --y [val]")

    # Save
    dirname, filename = os.path.split(input_path)
    name, ext = os.path.splitext(filename)
    output_filename = f"{name}_processed{ext}"
    output_path = os.path.join(dirname, output_filename)

    cv2.imwrite(output_path, binary)
    print(f"✓ Saved to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process map image to remove outside and infields.")
    parser.add_argument("image_path", help="Path to the map image")
    parser.add_argument("--x", type=int, help="X pixel coordinate on the track", default=None)
    parser.add_argument("--y", type=int, help="Y pixel coordinate on the track", default=None)
    
    args = parser.parse_args()
    process_map_image(args.image_path, args.x, args.y)