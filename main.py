import cv2
import mediapipe as mp
import time
import pyautogui
import math

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=2,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
tip_indices = [4, 8, 12, 16, 20]
pip_indices = [2, 6, 10, 14, 18]

previous_finger_status = {"Right": {finger: None for finger in finger_names},
                          "Left": {finger: None for finger in finger_names}}

screen_width, screen_height = pyautogui.size()

pinch_threshold = 50

pinch_gesture = False
clicking = False

while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks and results.multi_handedness:
        for handLms, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            h, w, c = img.shape
            hand_label = handedness.classification[0].label
            current_finger_status = {}
            finger_positions = []

            for i in range(5):
                tip_index = tip_indices[i]
                pip_index = pip_indices[i]

                tip_x, tip_y = int(handLms.landmark[tip_index].x * w), int(handLms.landmark[tip_index].y * h)
                pip_x, pip_y = int(handLms.landmark[pip_index].x * w), int(handLms.landmark[pip_index].y * h)

                if i == 0:
                    if hand_label == "Right":
                        if tip_x < pip_x:
                            current_finger_status[finger_names[i]] = "Up"
                            finger_positions.append(1)
                        else:
                            current_finger_status[finger_names[i]] = "Down"
                            finger_positions.append(0)
                    else:
                        if tip_x > pip_x:
                            current_finger_status[finger_names[i]] = "Up"
                            finger_positions.append(1)
                        else:
                            current_finger_status[finger_names[i]] = "Down"
                            finger_positions.append(0)
                else:
                    if tip_y < pip_y:
                        current_finger_status[finger_names[i]] = "Up"
                        finger_positions.append(1)
                    else:
                        current_finger_status[finger_names[i]] = "Down"
                        finger_positions.append(0)

                cv2.circle(img, (tip_x, tip_y), 5, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, (pip_x, pip_y), 5, (0, 0, 255), cv2.FILLED)

            if list(previous_finger_status[hand_label].values()) != finger_positions:
                previous_finger_status[hand_label] = {finger: status for finger, status in zip(finger_names, finger_positions)}

                if hand_label == "Left" and all(position == 0 for position in finger_positions):
                    pyautogui.leftClick()
                    clicking = True
                else:
                    clicking = False

                if hand_label == "Left":
                    thumb_tip_x, thumb_tip_y = int(handLms.landmark[tip_indices[0]].x * w), int(handLms.landmark[tip_indices[0]].y * h)
                    index_tip_x, index_tip_y = int(handLms.landmark[tip_indices[1]].x * w), int(handLms.landmark[tip_indices[1]].y * h)
                    middle_tip_x, middle_tip_y= int(handLms.landmark[tip_indices[2]].x * w), int(handLms.landmark[tip_indices[2]].y * h)
                    down_distance = calculate_distance(thumb_tip_x, thumb_tip_y, index_tip_x, index_tip_y)
                    up_distance = calculate_distance(thumb_tip_x, thumb_tip_y, middle_tip_x, middle_tip_y)
                    if down_distance < pinch_threshold:
                        pinch_gesture_down = True
                    else:
                        pinch_gesture_down = False
                    
                    if up_distance < pinch_threshold:
                        pinch_gesture_up = True
                    else:
                        pinch_gesture_up = False

                    if pinch_gesture_down and not clicking:
                        pyautogui.scroll(-10)
                    if pinch_gesture_up and not clicking:
                        pyautogui.scroll(10)

            if hand_label == "Right":
                index_finger_tip = handLms.landmark[tip_indices[1]]
                cursor_x = int(index_finger_tip.x * screen_width) 
                cursor_y = int(index_finger_tip.y * screen_height)
                pyautogui.moveTo(cursor_x, cursor_y)
            
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Hand mapped to screen", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
