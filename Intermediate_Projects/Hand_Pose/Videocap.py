import cv2
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()  
    if not ret:
        print("Failed to grab frame")
        break
    frame=cv2.resize(frame,(1400,800))
    text = "Brightness"
    position = (50, 50)  
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (0, 255, 0)
    thickness = 2

    cv2.putText(frame, text, position, font, font_scale, color, thickness, cv2.LINE_AA)
    cv2.rectangle(frame, (40,20), (220,70), color, thickness)
    cv2.imshow("Webcam Feed", frame) 

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
