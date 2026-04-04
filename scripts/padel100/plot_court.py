import json
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from config import ANNOT_DIR

# Ensure this matches your file name exactly
MENS_HOMOGRAPHY_FILE = '2022_BCN_FinalM_1_homography.json'
WOMENS_HOMOGRAPHY_FILE = '2022_BCN_FinalF_1_homography.json'

def plot_mens_player_on_court(frame_number):
    json_path = os.path.join(ANNOT_DIR, MENS_HOMOGRAPHY_FILE)
    
    if not os.path.exists(json_path):
        print(f"❌ File not found: {json_path}")
        return

    with open(json_path, 'r') as f:
        data = json.load(f)

    # 1. Access the list using the 'homography' key
    entries = data.get('homography', [])

    # 2. Target frame name (mens_ prefix as established)
    target_frame = f"mens_frame_{frame_number:06d}.PNG"
    
    # 3. Find the frame data
    frame_data = next((item for item in entries if item.get('file_name') == target_frame), None)

    if not frame_data:
        print(f"❌ Could not find {target_frame} in the homography list.")
        return

    # Extract raw location data
    pos_m = frame_data.get('location_m')
    
    if not pos_m:
        print(f"❌ Frame found, but 'location_m' is missing.")
        return

    # --- SAFE EXTRACTION: This replaces the problematic lines ---
    if isinstance(pos_m, dict):
        px = pos_m.get('x', 0)
        py = pos_m.get('y', 0)
    elif isinstance(pos_m, (list, tuple)):
        px = pos_m[0]
        py = pos_m[1]
    else:
        print(f"❌ Unknown format for location_m: {type(pos_m)}")
        return
       
    # --- Draw Court (Standard 10m x 20m) ---
    fig, ax = plt.subplots(figsize=(6, 10))
    
    # Outer Boundary
    court = patches.Rectangle((0, 0), 10, 20, linewidth=2, edgecolor='black', facecolor='green', alpha=0.3)
    ax.add_patch(court)
    
    # Net (at 10m)
    ax.plot([0, 10], [10, 10], color='black', linewidth=3, label='Net')
    
    # Service Lines
    ax.plot([0, 10], [3, 3], color='white', linestyle='--')
    ax.plot([0, 10], [17, 17], color='white', linestyle='--')
    
    # Plot Player using the safe px/py variables we just created
    ax.scatter(px, py, color='red', s=150, edgecolors='white', label='Player Position')
    ax.text(px, py + 0.5, f"({px:.1f}m, {py:.1f}m)", ha='center', fontweight='bold')

    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 21)
    ax.set_aspect('equal')
    ax.set_title(f"Court Mapping: {target_frame}")
    plt.legend()
    plt.show()

def plot_womens_player_on_court(frame_number):
    json_path = os.path.join(ANNOT_DIR, WOMENS_HOMOGRAPHY_FILE)
    
    if not os.path.exists(json_path):
        print(f"❌ File not found: {json_path}")
        return

    with open(json_path, 'r') as f:
        data = json.load(f)

    # 1. Access the list using the 'homography' key
    entries = data.get('homography', [])

    # 2. Target frame name (womens_ prefix as established)
    target_frame = f"womens_frame_{frame_number:06d}.PNG"
    
    # 3. Find the frame data
    frame_data = next((item for item in entries if item.get('file_name') == target_frame), None)

    if not frame_data:
        print(f"❌ Could not find {target_frame} in the homography list.")
        return

    # Extract raw location data
    pos_m = frame_data.get('location_m')
    
    if not pos_m:
        print(f"❌ Frame found, but 'location_m' is missing.")
        return

    # --- SAFE EXTRACTION: This replaces the problematic lines ---
    if isinstance(pos_m, dict):
        px = pos_m.get('x', 0)
        py = pos_m.get('y', 0)
    elif isinstance(pos_m, (list, tuple)):
        px = pos_m[0]
        py = pos_m[1]
    else:
        print(f"❌ Unknown format for location_m: {type(pos_m)}")
        return
       
    # --- Draw Court (Standard 10m x 20m) ---
    fig, ax = plt.subplots(figsize=(6, 10))
    
    # Outer Boundary
    court = patches.Rectangle((0, 0), 10, 20, linewidth=2, edgecolor='black', facecolor='green', alpha=0.3)
    ax.add_patch(court)
    
    # Net (at 10m)
    ax.plot([0, 10], [10, 10], color='black', linewidth=3, label='Net')
    
    # Service Lines
    ax.plot([0, 10], [3, 3], color='white', linestyle='--')
    ax.plot([0, 10], [17, 17], color='white', linestyle='--')
    
    # Plot Player using the safe px/py variables we just created
    ax.scatter(px, py, color='red', s=150, edgecolors='white', label='Player Position')
    ax.text(px, py + 0.5, f"({px:.1f}m, {py:.1f}m)", ha='center', fontweight='bold')

    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 21)
    ax.set_aspect('equal')
    ax.set_title(f"Court Mapping: {target_frame}")
    plt.legend()
    plt.show()

if __name__ == '__main__':
    print(f"Plotting mens player on court:")
    plot_mens_player_on_court(22)
    print(f"{'='*50}")
    print(f"Plotting womens player on court:")
    plot_womens_player_on_court(100)
    print(f"{'='*50}")
