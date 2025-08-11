## **Voice and Hand Pose-Based Screen & Audio Control System**

### **Overview**

This project enables **hands-free and intuitive control** of a system’s **volume** and **screen brightness** using a combination of **voice commands** and **hand gestures**.

The system listens for activation keywords via **speech recognition** and then switches to **gesture mode** for the chosen control type.

Once activated, hand gestures are used to **increase**, **decrease**, or **maintain** the selected parameter (volume or brightness). This eliminates the need for traditional input devices like keyboards or remotes, offering a seamless and modern user experience.

code : [VoiceBasedControl](https://github.com/josh-001/PYTHON_PROJECTS/blob/master/Intermediate_Projects/Hand_Pose/VoicaBasedControl.py)

---

## Installation

Speech Recognition
```bash
  pip install SpeechRecognition pyaudio
  python3 -m pip install pyaudio
```
Volume Control
```bash
  pip install pyvolume
```
## Documentation



1. **Script Initialization**
    
    The application is launched and begins listening for voice commands in the background.
    
2. **Activation via Voice Command**
    - Saying **"start"** triggers the video capture module.
    - The system activates **hand gesture detection** and waits for the control selection.
3. **Control Selection**
    - User says **"volume"** or **"brightness"** to choose the control mode.
4. **Gesture-Based Adjustment**
    - **Upward/forward gestures** → Increase volume/brightness
    - **Downward/backward gestures** → Decrease volume/brightness
    - Saying **any unrelated word** exits adjustment mode while maintaining the current level.

---

### **Planned Improvements**

1. **Voice-Controlled Session Management**
    - Say **"stop"** to halt video capture and gesture detection, reducing unnecessary CPU usage.
2. **Automatic Startup**
    - Configure the system to **run automatically at boot** for a plug-and-play experience.
3. **Front-End Integration**
    - Build an intuitive GUI instead of a pure command-line Python script.
    - Provide visual feedback during gesture control.
4. **Enhanced User Feedback**
    - Add on-screen **icons** showing active mode (volume/brightness).
    - Display real-time **level indicators** when adjusting settings.
5. **Cross-Platform Support**
    - Ensure compatibility with **Windows, Linux, and macOS**.

---

### **Potential Extensions**

- Multi-language voice recognition.
- Support for **media player control** (play/pause/skip) via gestures.
- Integration with **IoT devices** for smart home control.
- Use of **AI-based gesture recognition models** for improved accuracy.

## Contact

[Linkedin](https://www.linkedin.com/in/bhanu-josh-myprofile/)
