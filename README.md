# 🎯 Gesture Validation App

A real-time gesture recognition and validation tool using MediaPipe Holistic. Record hand gestures and compare them against reference gestures using Dynamic Time Warping (DTW) for speed-invariant matching.

## ✨ Features

- **Real-time Hand & Body Tracking** - Uses MediaPipe Holistic for 33 pose + 21 hand landmarks per hand
- **DTW Comparison** - Dynamic Time Warping ignores speed differences in gesture matching
- **Specific Feedback** - Get detailed feedback like "Left thumb is too low"
- **Toggle Landmarks** - Show/hide skeleton overlay on video
- **Load Custom Gestures** - Import JSON gesture files for validation

## 🚀 Live Demo

[View on Netlify](https://your-app-name.netlify.app) *(Update after deployment)*

## 🛠️ Usage

### Online
Just visit the live demo URL and:
1. Load a reference gesture JSON file
2. Click "Start Recording" and perform the gesture
3. Click "Stop Recording" to get DTW analysis
4. View your similarity score and specific feedback!

### Local Development
```bash
# Start a local server (required for camera access)
npx http-server . -p 8080 -o
```

## 📁 Files

| File | Description |
|------|-------------|
| `index.html` | Entry point (redirects to app) |
| `hand_tracking.html` | Main gesture validation app |
| `pose_extraction.py` | Python script to extract gestures from videos |
| `Apple.json` | Sample gesture data |

## 🔧 Creating Reference Gestures

Use the Python script to extract gestures from video files:

```bash
python pose_extraction.py your_video.mp4
```

This creates a JSON file with frame-by-frame landmark data.

## 📊 Scoring System

| Score | Result |
|-------|--------|
| 90%+ | ✅ Perfect! |
| 70-89% | 👍 Good |
| <70% | 💪 Keep practicing |

## 🧠 How DTW Works

Dynamic Time Warping aligns two gesture sequences regardless of timing differences:
- You can perform the gesture 2x faster or 3x slower
- DTW finds the optimal alignment between sequences
- Only the **shape and movement pattern** matter, not speed

## 📝 License

MIT License - Feel free to use and modify!
