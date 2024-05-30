import cv2 as cv

face_cascade = cv.CascadeClassifier('haarcascade_frontalface_alt2.xml')

cap = cv.VideoCapture(0)

while True:
    _, frame = cap.read()

    face_rects = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=4)

    for (x, y, w, h) in face_rects:
        face = cv.blur(frame[y:y + h, x:x + w], (25, 25))
        frame[y:y + h, x: x + w] = face
        cv.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)

    cv.imshow('frame', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
