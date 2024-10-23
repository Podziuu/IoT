import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils


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


cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Nie udało się przechwycić obrazu")
        break

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(image)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            if detect_thumbs_up(hand_landmarks.landmark):
                print("Kciuk w górę!")
            elif detect_thumbs_down(hand_landmarks.landmark):
                print("Kciuk w dół!")
            elif detect_open_hand(hand_landmarks.landmark):
                print("Otwarta dłoń!")
            else:
                print("Inny gest")

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('Hand Gesture Detection', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
