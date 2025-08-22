# README
## Virtual Mosuse
This is a Python project for controlling a computer's mouse cursor using hand actions.  
The program recognizes hand actions through a webcam using the **Mediapipe** library and controls the mouse cursor via the **PyAutoGUI** library.

The project is divided into two main files:
- `app.py` → contains the main program logic.
- `controller.py` → responsible for handling the mouse cursor movement, actions, and window control events.

There is an file, `requirements.txt`, which you can use to install all the required libraries for this project.

## Requirements
To run the program, the following libraries are required:
- OpenCV
- Mediapipe
- PyAutoGUI

You can install these libraries using pip:
- pip install opencv-python mediapipe pyautogui

Or you can use the following command using pip to avoid any library version issue:
- pip install -r requirements.txt

## How to run the application

After installing the required libraries, run the app.py file in a Python environment with a webcam. The program will start capturing video from the webcam, and the mouse cursor can be controlled using the following hand actions:

- Cursor moving: Raise index finger and move your hand to move the cursor.

- Cursor freezing: Raise all fingers but fold thumb.

- Drag and drop: Close your hand into a fist and move it to drag/drop objects.

- Left-click: Touch index finger to thumb.

- Right-click: Touch middle finger to thumb.

- Double-click: Touch ring finger to thumb.

- Scroll up: Raise little finger while others down.

- Scroll down: Raise index finger while others down.

- Zoom in: Raise index + middle fingers (spread apart).

- Zoom out: Raise index + middle fingers (close together).

- Minimize Window: Touch little finger to thumb.

- Maximize Window: Index + middle up, ring + little down, thumb up.

- Close Window: Index + middle touch thumb.

- Exit Application: index + little up, middle + ring touching thumb.

## Demo Actions
All example images/GIFs are stored in the actions folder.
