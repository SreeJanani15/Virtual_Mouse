import pyautogui

class Controller:
    prev_hand_position = None
    right_clicked = False
    left_clicked = False
    double_clicked = False
    dragging = False
    hand_landmarks = None

    pinky_down = None
    pinky_up = None
    index_down = None
    index_up = None
    middle_down = None
    middle_up = None
    ring_down = None
    ring_up = None
    thumb_down = None
    thumb_up = None

    all_fingers_down = None
    all_fingers_up = None

    index_within_thumb = None
    middle_within_thumb = None
    pinky_within_thumb = None
    ring_within_thumb = None

    screen_width, screen_height = pyautogui.size()

    @staticmethod
    def update_fingers_status():
        Controller.pinky_down = Controller.hand_landmarks.landmark[20].y > Controller.hand_landmarks.landmark[17].y
        Controller.pinky_up = Controller.hand_landmarks.landmark[20].y < Controller.hand_landmarks.landmark[17].y

        Controller.index_down = Controller.hand_landmarks.landmark[8].y > Controller.hand_landmarks.landmark[5].y
        Controller.index_up = Controller.hand_landmarks.landmark[8].y < Controller.hand_landmarks.landmark[5].y

        Controller.middle_down = Controller.hand_landmarks.landmark[12].y > Controller.hand_landmarks.landmark[9].y
        Controller.middle_up = Controller.hand_landmarks.landmark[12].y < Controller.hand_landmarks.landmark[9].y

        Controller.ring_down = Controller.hand_landmarks.landmark[16].y > Controller.hand_landmarks.landmark[13].y
        Controller.ring_up = Controller.hand_landmarks.landmark[16].y < Controller.hand_landmarks.landmark[13].y

        Controller.thumb_down = Controller.hand_landmarks.landmark[4].y > Controller.hand_landmarks.landmark[13].y
        Controller.thumb_up = Controller.hand_landmarks.landmark[4].y < Controller.hand_landmarks.landmark[13].y

        Controller.all_fingers_down = Controller.index_down and Controller.middle_down and Controller.ring_down and Controller.pinky_down
        Controller.all_fingers_up = Controller.index_up and Controller.middle_up and Controller.ring_up and Controller.pinky_up

        Controller.index_within_thumb = Controller.hand_landmarks.landmark[4].y < Controller.hand_landmarks.landmark[8].y < Controller.hand_landmarks.landmark[2].y
        Controller.middle_within_thumb = Controller.hand_landmarks.landmark[4].y < Controller.hand_landmarks.landmark[12].y < Controller.hand_landmarks.landmark[2].y
        Controller.pinky_within_thumb = Controller.hand_landmarks.landmark[4].y < Controller.hand_landmarks.landmark[20].y < Controller.hand_landmarks.landmark[2].y
        Controller.ring_within_thumb = Controller.hand_landmarks.landmark[4].y < Controller.hand_landmarks.landmark[16].y < Controller.hand_landmarks.landmark[2].y

    @staticmethod
    def get_cursor_position(hand_x, hand_y):
        old_x, old_y = pyautogui.position()
        current_x = int(hand_x * Controller.screen_width)
        current_y = int(hand_y * Controller.screen_height)

        ratio = 1
        Controller.prev_hand_position = (current_x, current_y) if Controller.prev_hand_position is None else Controller.prev_hand_position
        delta_x = current_x - Controller.prev_hand_position[0]
        delta_y = current_y - Controller.prev_hand_position[1]
        
        Controller.prev_hand_position = [current_x, current_y]
        current_x, current_y = old_x + delta_x * ratio, old_y + delta_y * ratio

        threshold = 5
        current_x = max(threshold, min(current_x, Controller.screen_width - threshold))
        current_y = max(threshold, min(current_y, Controller.screen_height - threshold))

        return current_x, current_y
        
    @staticmethod
    def cursor_moving():
        landmark_index = 9
        hand_x, hand_y = Controller.hand_landmarks.landmark[landmark_index].x, Controller.hand_landmarks.landmark[landmark_index].y
        cursor_x, cursor_y = Controller.get_cursor_position(hand_x, hand_y)

        cursor_frozen = Controller.all_fingers_up and Controller.thumb_down
        if not cursor_frozen:
            pyautogui.moveTo(cursor_x, cursor_y, duration=0)
    
    @staticmethod
    def detect_scrolling():
        if Controller.pinky_up and Controller.index_down and Controller.middle_down and Controller.ring_down:
            pyautogui.scroll(120)
        elif Controller.index_up and Controller.middle_down and Controller.ring_down and Controller.pinky_down:
            pyautogui.scroll(-120)

    @staticmethod
    def detect_zooming():
        zooming = Controller.index_up and Controller.middle_up and Controller.ring_down and Controller.pinky_down
        window = 0.05
        index_touches_middle = abs(Controller.hand_landmarks.landmark[8].x - Controller.hand_landmarks.landmark[12].x) <= window

        if zooming and index_touches_middle:
            pyautogui.keyDown('ctrl')
            pyautogui.scroll(-50)
            pyautogui.keyUp('ctrl')
        elif zooming:
            pyautogui.keyDown('ctrl')
            pyautogui.scroll(50)
            pyautogui.keyUp('ctrl')

    @staticmethod
    def detect_clicking():
        left_click = Controller.index_within_thumb and Controller.middle_up and Controller.ring_up and Controller.pinky_up
        if not Controller.left_clicked and left_click:
            pyautogui.click()
            Controller.left_clicked = True
        elif not Controller.index_within_thumb:
            Controller.left_clicked = False

        right_click = Controller.middle_within_thumb and Controller.index_up and Controller.ring_up and Controller.pinky_up
        if not Controller.right_clicked and right_click:
            pyautogui.rightClick()
            Controller.right_clicked = True
        elif not Controller.middle_within_thumb:
            Controller.right_clicked = False

        double_click = Controller.ring_within_thumb and Controller.index_up and Controller.middle_up and Controller.pinky_up
        if not Controller.double_clicked and double_click:
            pyautogui.doubleClick()
            Controller.double_clicked = True
        elif not Controller.ring_within_thumb:
            Controller.double_clicked = False
    
    @staticmethod
    def detect_dragging():
        if not Controller.dragging and Controller.all_fingers_down:
            pyautogui.mouseDown(button="left")
            Controller.dragging = True
        elif not Controller.all_fingers_down:
            pyautogui.mouseUp(button="left")
            Controller.dragging = False

    @staticmethod
    def detect_exit_gesture():
        return (
            Controller.middle_within_thumb and Controller.ring_within_thumb and
            Controller.pinky_up and Controller.index_up
        )
    
    @staticmethod
    def detect_minimize():
        if Controller.pinky_within_thumb and Controller.index_up and Controller.middle_up and Controller.ring_up:
            pyautogui.hotkey('win', 'down')

    @staticmethod
    def detect_maximize():
        if Controller.index_up and Controller.middle_up and Controller.ring_down and Controller.pinky_down and Controller.thumb_up:
            pyautogui.hotkey('win', 'up')

    @staticmethod
    def detect_close():
        if Controller.index_within_thumb and Controller.middle_within_thumb and Controller.ring_up and Controller.pinky_up:
            pyautogui.hotkey('alt', 'f4')
