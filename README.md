# Hand Gesture Recognition with OpenCV and Raspberry Pi
This project demonstrates how to detect hand gestures using OpenCV on a laptop and communicate with a Raspberry Pi to control an LED light based on the detected gestures.

### Table of Contents
* Overview
* Project Structure
* Hardware Requirements
* Software Requirements
* Installation
* How It Works
* Usage
* License

### Overview
The goal of this project is to detect hand gestures using a laptop camera, send the detected gesture information to a Raspberry Pi over a network connection, and perform specific actions (such as turning an LED on or off) based on the gesture.
* Laptop: Detects hand gestures using OpenCV.
* Raspberry Pi: Receives information about the gestures and controls an LED connected to one of its GPIO pins.

### Project Structure
```bash
.
├── hand_gesture_detection.py  # Detects hand gestures and sends commands to Raspberry Pi
├── raspberry_pi_listener.py   # Listens for commands on Raspberry Pi and controls the LED
├── README.md                  # Project documentation
```
### Hardware Requirements
* Raspberry Pi (any model with GPIO support)
* MicroSD card (with Raspbian OS installed)
* Laptop with a camera (to run OpenCV)
* LED (with appropriate resistor)
* Breadboard and jumper wires

### Software Requirements
* Raspberry Pi OS (Raspbian)
* Python 3.x
* OpenCV
* Mediapipe (for hand gesture detection)
* RPi.GPIO (for controlling the LED on Raspberry Pi)

### Python Libraries:
* OpenCV: pip install opencv-python
* Mediapipe: pip install mediapipe
* RPi.GPIO: Pre-installed on Raspberry Pi or install using sudo apt-get install python3-rpi.gpio

### Installation
#### 1. Setup Raspberry Pi
* Flash Raspbian OS onto a microSD card using Raspberry Pi Imager.
* Connect Raspberry Pi to your local network.
* Enable SSH on the Raspberry Pi.
* Setup GPIO pin for the LED (e.g., use GPIO 17).
#### 2. Laptop Setup
* Install Python 3.x.
* Install OpenCV and Mediapipe:
```bash
pip install opencv-python mediapipe
```
#### 3. Code Setup
* Clone this repository:
```bash
git clone https://github.com/xfl0rek/IoT.git
cd hand-gesture-raspberry-pi
```
#### 4. Setup Communication
* Ensure both the Raspberry Pi and the laptop are connected to the same network.
* On the laptop, run hand_gesture_detection.py to detect gestures and send signals to Raspberry Pi.
* On the Raspberry Pi, run raspberry_pi_listener.py to receive commands and control the LED.
### How It Works
#### 1. Gesture Detection (Laptop):
* OpenCV and Mediapipe are used to detect hand gestures from the laptop camera.
* Based on the detected gesture, a signal (e.g., LED_ON, LED_OFF) is sent to the Raspberry Pi over a TCP connection.
#### 2. Command Handling (Raspberry Pi):
* Raspberry Pi runs a listener script that waits for incoming signals from the laptop.
* Upon receiving a signal (e.g., LED_ON), the Raspberry Pi controls the GPIO pin to either turn the LED on or off.

### Usage
#### 1. Detecting Gestures
Run the hand gesture detection script on the laptop:

```bash
python3 hand_gesture_detection.py
```
This script will display the camera feed and detect hand gestures in real-time. It sends corresponding commands (`LED_ON`, `LED_OFF`) to the Raspberry Pi.

### 2. Controlling LED on Raspberry Pi
Run the listener script on the Raspberry Pi:

```bash
python3 raspberry_pi_listener.py
```
The Raspberry Pi will now listen for commands from the laptop and control the LED accordingly.

### Supported Gestures:
thumbs up: Turns the LED on.
thumbs down: Turns the LED off.
### License
This project is licensed under the MIT License. See the LICENSE file for more details.
