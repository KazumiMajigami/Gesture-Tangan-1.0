import cv2
import mediapipe as mp
import math
import time

# ======================
# INIT
# ======================
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)

cap = cv2.VideoCapture(0)

# 🔥 Biar resolusi gede
cap.set(3, 1280)
cap.set(4, 720)

# 🔥 Window fullscreen
cv2.namedWindow("Gesture AI", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Gesture AI", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# ======================
# CONFIG
# ======================
STABLE_TIME = 0.8

# ======================
# UTILS
# ======================
def distance(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

def get_finger_status(hand_landmarks):
    tips_ids = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    for i in range(1, 5):
        if hand_landmarks.landmark[tips_ids[i]].y < hand_landmarks.landmark[tips_ids[i]-2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

# ======================
# TRANSLATE
# ======================
def translate_gesture(hand_landmarks):
    fingers = get_finger_status(hand_landmarks)

    thumb = hand_landmarks.landmark[4]
    index = hand_landmarks.landmark[8]

    if fingers == [1,0,0,0,0]:
        return "AKU"

    if fingers == [1,1,1,1,1]:
        return "MAU"

    if distance(thumb, index) < 0.05:
        return "MAKAN"

    if fingers == [0,1,0,0,0]:
        return "KAMU"

    if fingers == [0,0,0,0,0]:
        return "JANGAN"

    if fingers == [1,0,0,0,1]:
        return "LUPA"

    if fingers == [0,1,1,0,0]:
        return "YA"

    return ""

# ======================
# TEXT WRAP (biar gak kepotong)
# ======================
def draw_subtitle(img, text):
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 1.2
    thickness = 3

    max_width = img.shape[1] - 40
    words = text.split(" ")

    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        (w, h), _ = cv2.getTextSize(test_line, font, scale, thickness)

        if w > max_width:
            lines.append(current_line)
            current_line = word + " "
        else:
            current_line = test_line

    lines.append(current_line)

    y = img.shape[0] - 100

    for line in reversed(lines):
        (w, h), _ = cv2.getTextSize(line, font, scale, thickness)
        x = (img.shape[1] - w) // 2

        # background biar jelas
        cv2.rectangle(img, (x-10, y-h-10), (x+w+10, y+10), (0,0,0), -1)

        cv2.putText(img, line, (x, y),
                    font, scale, (0,255,0), thickness)

        y -= h + 20

# ======================
# STATE
# ======================
last_gesture = ""
gesture_start_time = 0
sentence = []

# ======================
# MAIN LOOP
# ======================
while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    current_gesture = ""

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            current_gesture = translate_gesture(handLms)

    # ======================
    # STABILIZER
    # ======================
    if current_gesture != "":
        if current_gesture != last_gesture:
            last_gesture = current_gesture
            gesture_start_time = time.time()
        else:
            if time.time() - gesture_start_time > STABLE_TIME:
                if len(sentence) == 0 or sentence[-1] != current_gesture:
                    sentence.append(current_gesture)
                    gesture_start_time = time.time()

    # ======================
    # DISPLAY
    # ======================
    final_text = " ".join(sentence)

    draw_subtitle(img, final_text)

    cv2.imshow("Gesture AI", img)

    key = cv2.waitKey(1) & 0xFF

    if key == 27:  # ESC
        break

    if key == ord('c'):  # clear
        sentence = []

cap.release()
cv2.destroyAllWindows()