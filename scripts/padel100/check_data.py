import pandas as pd
import sys, os
from config import MENS_SHOTS, WOMENS_SHOTS, BASE_DIR

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def verify_mens_csv():
    if not os.path.exists(MENS_SHOTS):
        print(f"❌ Error: File not found at {MENS_SHOTS}")
        return

    # Use sep=';' because PadelTracker100 CSVs use semicolons
    df = pd.read_csv(MENS_SHOTS, sep=';')
    
    print("✅ MENS CSV Loaded Successfully!")
    print(f"Total Frames: {len(df)}")
    
    # Check for shots (has_shot == 1)
    shots = df[df['has_shot'] == 1]
    print(f"Total Shot Events Found: {len(shots)}")
    print("\nSample Shot Data:")
    print(shots.head())

def verify_womens_csv():
    if not os.path.exists(WOMENS_SHOTS):
        print(f"❌ Error: File not found at {WOMENS_SHOTS}")
        return

    # Use sep=';' because PadelTracker100 CSVs use semicolons
    df = pd.read_csv(WOMENS_SHOTS, sep=';')
    
    print("✅ WOMENS CSV Loaded Successfully!")
    print(f"Total Frames: {len(df)}")
    
    # Check for shots (has_shot == 1)
    shots = df[df['has_shot'] == 1]
    print(f"Total Shot Events Found: {len(shots)}")
    print("\nSample Shot Data:")
    print(shots.head())

if __name__ == "__main__":
    print(f"Checking BASE_DIR: {BASE_DIR}")
    verify_mens_csv()
    print(f"{'='*50}")
    verify_womens_csv()
    print(f"{'='*50}")