import mediapipe as mp
import cv2
import pyvolume
import speech_recognition as sr
import threading
from Brightness import bright 
text=""
trigger_event=threading.Event()
class VoiceRecog:
   def __init__(self):
      pass

   def Voice(self):
      global text
      recognizer = sr.Recognizer()
      while True:
            with sr.Microphone() as source:
                print("🎙️ Speak something...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
            try:
                print("🧠 Recognizing...")
                text = recognizer.recognize_google(audio)
                if "start" in text:
                    trigger_event.set()
                print("📝 You said: " + text)
                
            except sr.UnknownValueError:
                print("❌ Could not understand the audio.")
            except sr.RequestError as e:
                print(f"⚠️ Could not request results; {e}")

    
# class Handpose:
#    def __init__(self):
#       self.Pose()
#    def start_det(self):
#        print(text)
#        if "start" in text:
#            self.Pose()
def Pose():
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    dis=0
    trigger_event.wait()
    # capture = cv2.VideoCapture(0)
    if "start" in text:
        capture = cv2.VideoCapture(0)
        with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
            while capture.isOpened():
                print("📝 You said: " + text)
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

                        h, w, _ = image.shape  
                        
                        thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
                        index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)
                        gap=thumb_y-index_y
                        if gap<0:
                            gap *=-1
                        if "volume" in text:
                            pyvolume.custom(percent=gap)
                        elif "bright" in text:
                            bright(percent=gap)
                        dis=gap
                        cv2.circle(image, (thumb_x, thumb_y), 8, (0, 0, 255), -1)   # Red circle
                        cv2.circle(image, (index_x, index_y), 8, (255, 0, 0), -1)
            
                cv2.imshow('Webcam', image)
            
                if (cv2.waitKey(1) & 0xFF == ord('q')):
                    break
    
        capture.release()
        cv2.destroyAllWindows()

if __name__=="__main__":
    x=VoiceRecog()
    t1=threading.Thread(target=x.Voice)
    t2=threading.Thread(target=Pose)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    
