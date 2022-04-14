from imutils.video import VideoStream, FPS
import face_recognition
import imutils
import pickle
import time
import cv2
from datetime import datetime
from notification import Email


def facial_recognition():
    current_name = ""
    encodingsP = "encodings.pickle"
    unknown_image = "unknown/unknown"
    image_suffix = ".jpg"
    image_path = ""

    print("[INFO] loading encodings + face detector...")
    data = pickle.loads(open(encodingsP, "rb").read())

    vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)
    fps = FPS().start()
    
    sender = Email()
    f = open("receiver.txt", "r")
    receiver = f.read()
    f.close()
    emailSubject = ""
    emailContent = "" 
    
    try:
        while True:
            frame = vs.read()
            frame = imutils.resize(frame, width=500)

            boxes = face_recognition.face_locations(frame)
            
            face_recognition

            encodings = face_recognition.face_encodings(frame, boxes)
            names = []

            for encoding in encodings:
                matches = face_recognition.compare_faces(
                    data["encodings"],
                    encoding,
                    tolerance= 0.4
                )
                                
                if True in matches:
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}

                    for i in matchedIdxs:
                        name = data["names"][i]
                        counts[name] = counts.get(name, 0) + 1

                    name = max(counts, key=counts.get)

                    if current_name != name:
                        current_name = name
                        emailSubject = "Vistior Notification"
                        emailContent = current_name + " visited at " + str(datetime.now())
                        image_path = "vistor.jpg"
                        cv2.imwrite(image_path, frame)
                        sender.send(receiver, emailSubject, emailContent, image_path)
                else:
                    name = "Unknown"
                    if current_name != name:
                        current_name = name
                        emailSubject = "Warning: unknown visitor"
                        emailContent = "unknown visitor detected at " + str(datetime.now())
                        image_path = unknown_image+str(int(time.time()))+image_suffix
                        cv2.imwrite(image_path, frame)
                        sender.send(receiver, emailSubject, emailContent, image_path)
                        
                names.append(name)

            for ((top, right, bottom, left), name) in zip(boxes, names):
                
                if name == "Unknown":
                    labelColor = (0, 0, 255) #red
                else:
                    labelColor = (0, 128, 0) #green
                
                cv2.rectangle(
                    frame,
                    (left, top),
                    (right, bottom),
                    labelColor,
                    2,
                )
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(
                    frame,
                    name,
                    (left, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    labelColor,
                    2,
                )

            # display the image to our screen
            cv2.imshow("Facial Recognition is Running", frame)
            key = cv2.waitKey(1) & 0xFF

            # quit when 'q' key is pressed
            if key == ord("q"):
                break

            fps.update()
    except KeyboardInterrupt:
        pass
    finally:
        fps.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

        # do a bit of cleanup
        cv2.destroyAllWindows()
        vs.stop()
