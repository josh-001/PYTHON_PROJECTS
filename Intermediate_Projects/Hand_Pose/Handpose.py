import mediapipe as mp
import cv2
import pyvolume

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
dis=0
capture = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
  while capture.isOpened():
      ret, frame = capture.read()
      frame = cv2.flip(frame, 1)
      image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
      detected_image = hands.process(image)
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
  
      if detected_image.multi_hand_landmarks:
          for hand_lms in detected_image.multi_hand_landmarks:
            # #   print(("nly two slicing:",detected_image.multi_hand_landmarks[0:2]))
            #   mp_drawing.draw_landmarks(image, hand_lms,
            #                             mp_hands.HAND_CONNECTIONS,
            #                             landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(
            #                                 color=(255, 0, 255), thickness=4, circle_radius=2),
            #                             connection_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(
            #                                 color=(20, 180, 90), thickness=2, circle_radius=2)
            #                             )
            # Get landmark 4 (thumb tip) and 8 (index tip)
            thumb_tip = hand_lms.landmark[4]
            index_tip = hand_lms.landmark[8]

            h, w, _ = image.shape  # Get image dimensions
            
            # Convert normalized coordinates to pixel values
            thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
            index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)
            gap=thumb_y-index_y
            if gap<0:
               gap *=-1
            # print(gap)
            if dis>gap:
               print(gap,"decreasing")
            #    pyvolume.custom(percent=gap)
            else:
               print(gap,"increasing")
            pyvolume.custom(percent=gap)
            dis=gap
            # Draw circles on the thumb tip and index tip
            cv2.circle(image, (thumb_x, thumb_y), 8, (0, 0, 255), -1)   # Red circle
            cv2.circle(image, (index_x, index_y), 8, (255, 0, 0), -1)
  
      cv2.imshow('Webcam', image)
  
      if cv2.waitKey(1) & 0xFF == ord('q'):
          break

capture.release()
cv2.destroyAllWindows()





# import cv2
# import mediapipe as mp

# # Initialize MediaPipe Hands
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(
#     static_image_mode=False,
#     max_num_hands=1,
#     min_detection_confidence=0.7,
#     min_tracking_confidence=0.7
# )
# mp_drawing = mp.solutions.drawing_utils

# # Open webcam
# cap = cv2.VideoCapture(0)

# while cap.isOpened():
#     success, image = cap.read()
#     if not success:
#         print("Ignoring empty camera frame.")
#         continue

#     # Flip the image horizontally for a natural selfie-view display.
#     image = cv2.flip(image, 1)

#     # Convert the BGR image to RGB.
#     image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#     # Process the image and find hand landmarks.
#     results = hands.process(image_rgb)

#     # Draw the hand annotations on the image.
#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             mp_drawing.draw_landmarks(
#                 image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

#             # Example: Basic gesture recognition (e.g., counting fingers)
#             # This part would be expanded for more complex gesture recognition
#             # based on landmark positions and relationships.
#             # For instance, check if specific finger tips are above or below
#             # certain y-coordinates relative to the palm base.

#     # Display the image.
#     cv2.imshow('Hand Gesture Recognition', image)

#     # Exit on 'q' press.
#     if cv2.waitKey(5) & 0xFF == ord('q'):
#         break

# # Release the webcam and destroy all windows.
# cap.release()
# cv2.destroyAllWindows()