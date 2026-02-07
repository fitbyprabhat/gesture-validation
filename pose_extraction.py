import cv2
import mediapipe as mp
import json
import os
import sys

# --- CONFIGURATION ---
INPUT_FOLDER = r'c:\Users\IB\Desktop\try'  # Folder containing video files
VIDEO_EXTENSIONS = ('.mp4', '.avi', '.mov', '.mkv')

# Initialize MediaPipe Holistic (Body + Hands + Face)
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def process_video_to_data(video_path, output_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return

    # Data structure to hold the entire animation
    motion_data = []
    frame_count = 0

    print(f"Processing {video_path}...")

    # Start Holistic Tracking
    # min_detection_confidence: How sure the AI must be to detect a person
    # model_complexity: 1 is balanced, 2 is more accurate but slower
    with mp_holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        model_complexity=1) as holistic:

        while cap.isOpened():
            success, image = cap.read()
            if not success:
                break # End of video

            frame_count += 1
            
            # MediaPipe requires RGB images, OpenCV loads as BGR
            image.flags.writeable = False
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # The Magic: Detect landmarks
            results = holistic.process(image_rgb)

            # --- VISUALIZATION (Optional: Shows you what it sees) ---
            # image.flags.writeable = True
            # # Draw Pose (Body)
            # mp_drawing.draw_landmarks(
            #     image,
            #     results.pose_landmarks,
            #     mp_holistic.POSE_CONNECTIONS,
            #     landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            # # Draw Left Hand
            # mp_drawing.draw_landmarks(
            #     image,
            #     results.left_hand_landmarks,
            #     mp_holistic.HAND_CONNECTIONS)
            # # Draw Right Hand
            # mp_drawing.draw_landmarks(
            #     image,
            #     results.right_hand_landmarks,
            #     mp_holistic.HAND_CONNECTIONS)

            # cv2.imshow('ISL Data Extraction (Press Q to quit)', image)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
            
            # Print progress every 100 frames
            if frame_count % 100 == 0:
                print(f"Processed {frame_count} frames...")

            # --- DATA EXTRACTION ---
            # We create a dictionary for this specific frame
            frame_data = {
                "frame_index": frame_count,
                "pose": [],       # Body (Shoulders, Elbows, Knees, etc.)
                "left_hand": [],  # Detailed Fingers
                "right_hand": []  # Detailed Fingers
            }

            # Helper function to extract points safely
            def extract_coords(landmarks):
                points = []
                if landmarks:
                    for landmark in landmarks.landmark:
                        points.append({
                            "x": round(landmark.x, 4), # 0.0 to 1.0 (Relative to width)
                            "y": round(landmark.y, 4), # 0.0 to 1.0 (Relative to height)
                            "z": round(landmark.z, 4), # Depth
                            "vis": round(landmark.visibility, 2) if hasattr(landmark, 'visibility') else 1.0
                        })
                return points

            # Extract data
            frame_data["pose"] = extract_coords(results.pose_landmarks)
            frame_data["left_hand"] = extract_coords(results.left_hand_landmarks)
            frame_data["right_hand"] = extract_coords(results.right_hand_landmarks)

            motion_data.append(frame_data)

    cap.release()
    cv2.destroyAllWindows()

    # Save to JSON
    with open(output_path, 'w') as f:
        json.dump(motion_data, f, indent=None) # indent=None keeps file size smaller
    
    print(f"Success! Processed {frame_count} frames.")
    print(f"Data saved to: {output_path}")

# Run the function
if __name__ == "__main__":
    # Ensure the input folder exists
    if not os.path.exists(INPUT_FOLDER):
        print(f"Error: The folder '{INPUT_FOLDER}' does not exist.")
        sys.exit(1)

    print(f"Scanning for videos in: {INPUT_FOLDER}")
    
    # Get list of all files in directory
    files = os.listdir(INPUT_FOLDER)
    
    # Filter for video files
    video_files = [f for f in files if f.lower().endswith(VIDEO_EXTENSIONS)]
    
    if not video_files:
        print("No video files found in the specified folder.")
    else:
        print(f"Found {len(video_files)} videos: {video_files}")
        
        for video_file in video_files:
            input_path = os.path.join(INPUT_FOLDER, video_file)
            
            # Create output filename: video_name.json
            file_name_without_ext = os.path.splitext(video_file)[0]
            output_filename = f"{file_name_without_ext}.json"
            output_path = os.path.join(INPUT_FOLDER, output_filename)
            
            print(f"\n--- Processing: {video_file} ---")
            process_video_to_data(input_path, output_path)
            
        print("\nAll videos processed!")
