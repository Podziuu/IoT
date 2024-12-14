import cv2
import mediapipe as mp
import RPi.GPIO as GPIO
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils
LED_PIN1 = 14
LED_PIN2 = 17
LED_PIN3 = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN1, GPIO.OUT)
GPIO.setup(LED_PIN2, GPIO.OUT)
GPIO.setup(LED_PIN3, GPIO.OUT)


def detect_thumbs_up(landmarks):
    thumb_tip = landmarks[4]
    thumb_mcp = landmarks[2]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]

    if (thumb_tip.y < thumb_mcp.y and
            index_tip.y > thumb_tip.y and
            middle_tip.y > thumb_tip.y):
        return True
    return False


def detect_thumbs_down(landmarks):
    thumb_tip = landmarks[4]
    thumb_mcp = landmarks[2]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]

    if (thumb_tip.y > thumb_mcp.y and
            index_tip.y < thumb_tip.y and
            middle_tip.y < thumb_tip.y):
        return True
    return False


def detect_open_hand(landmarks):
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]

    index_mcp = landmarks[5]
    middle_mcp = landmarks[9]
    ring_mcp = landmarks[13]
    pinky_mcp = landmarks[17]

    if (index_tip.y < index_mcp.y and
            middle_tip.y < middle_mcp.y and
            ring_tip.y < ring_mcp.y and
            pinky_tip.y < pinky_mcp.y):
        return True
    return False


def light_up_led():
    GPIO.output(LED_PIN1, GPIO.LOW)
    GPIO.output(LED_PIN2, GPIO.LOW)


def light_down_led():
    GPIO.output(LED_PIN1, GPIO.HIGH)
    GPIO.output(LED_PIN2, GPIO.HIGH)


def blink(duration=0.5):
    start = time.time()
    while time.time() - start < duration:
        GPIO.output(LED_PIN3, GPIO.HIGH)
        time.sleep(1.0)
        GPIO.output(LED_PIN3, GPIO.LOW)
        time.sleep(1.0)


last_gesture = None

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Nie udało się przechwycić obrazu")
        break

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(image)
    current_gesture = None

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            if detect_thumbs_up(hand_landmarks.landmark):
                current_gesture = "Kciuk w górę!"
                light_up_led()
            elif detect_thumbs_down(hand_landmarks.landmark):
                current_gesture = "Kciuk w dół!"
                light_down_led()
            elif detect_open_hand(hand_landmarks.landmark):
                current_gesture = "Otwarta dłoń!"
                blink()
            else:
                current_gesture = "Inny gest"

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    if current_gesture != last_gesture:
        if current_gesture:
            print(current_gesture)
        last_gesture = current_gesture

    cv2.imshow('Hand Gesture Detection', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

GPIO.cleanup()

cap.release()
cv2.destroyAllWindows()
