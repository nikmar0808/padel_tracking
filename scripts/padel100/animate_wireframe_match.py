import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import numpy as np
from scripts.padel100.data_mapper import get_mens_training_sample, get_womens_training_sample
from config import WIDTH, HEIGHT

# This script animates the player's skeleton and the ball's trajectory for a specific sequence (like the first Serve).
# It acts as our "game engine" to see if the data looks like real Padel movement.
# We will animate the first Serve (Frames 20 to 50)
# This is a powerful way to visually verify that our data mapping is correct and to see the dynamics of the player's movement and ball trajectory in action.
# Note: Ensure that the frame names in the CSV and JSON match the format "frame_000022.PNG" for this to work seamlessly.
# Adjust the frame range as needed to focus on different parts of the match.
# 
# This animation will show the player's skeleton (in cyan) and the ball's position (in yellow) over time, 
# along with a label indicating the shot type and whether it was a hit or not.
# Temporal Logic: We will see the ball move toward the player and the "💥 HIT!" label trigger exactly when they meet.
# Model Feasibility: If the "dots" look like a serve, our AI can learn it. If the dots are jumping randomly, the data is corrupted.

frames_to_animate = [f"frame_{i:06d}.PNG" for i in range(20, 51)]

fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, WIDTH)
ax.set_ylim(HEIGHT, 0) # Flip Y for image coordinates
ax.set_title("PadelTracker100: Wireframe Animation (Frames 20-50)")

# Placeholders for the plot elements
player_plot = ax.scatter([], [], c='cyan', s=30, label='Player Skeleton')
ball_plot = ax.scatter([], [], c='yellow', s=60, edgecolors='orange', label='Ball')
text_label = ax.text(50, 100, "", color='white', fontsize=12, bbox=dict(facecolor='black', alpha=0.5))

def update(frame_name):
    data = get_mens_training_sample(frame_name)
    
    # Update Player
    if data['skeleton'] is not None:
        player_plot.set_offsets(data['skeleton'][:, :2])
    
    # Update Ball
    if data['ball_xy']:
        ball_plot.set_offsets([data['ball_xy']])
    else:
        ball_plot.set_offsets(np.empty((0, 2)))
        
    # Update Label
    status = "💥 HIT!" if data['is_hit'] == 1 else "Moving..."
    text_label.set_text(f"{frame_name}\nType: {data['shot_type']}\nStatus: {status}")
    
    return player_plot, ball_plot, text_label

ani = FuncAnimation(fig, update, frames=frames_to_animate, interval=100, blit=True)
plt.legend(loc='upper right')
plt.show()
