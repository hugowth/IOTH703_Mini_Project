import cv2
from pathlib import Path
from picamera import PiCamera
from picamera.array import PiRGBArray


def capture_face():
    try:
        name = input("please input the name:")
        Path(f"./dataset/{name}").mkdir(0o755, parents=True, exist_ok=True)

        cam = PiCamera()
        cam.resolution = (352, 352)
        cam.framerate = 24
        rawCapture = PiRGBArray(cam, size=(352, 352))
        image_count = 0
        message = "Press c to take a photo, press q to exit"
        print(message)

        while True:
            for frame in cam.capture_continuous(
                rawCapture,
                format="bgr",
                use_video_port=True,
            ):
                image = frame.array
                cv2.imshow(message, image)
                rawCapture.truncate(0)
                user_input_key = cv2.waitKey(1) % 256
                rawCapture.truncate(0)

                if user_input_key == ord("q"):
                    break
                elif user_input_key == ord("c"):
                    file_name = f"dataset/{name}/{name}_{image_count}.jpg"
                    cv2.imwrite(file_name, image)
                    print("{} written!".format(file_name))
                    image_count += 1

            if user_input_key == ord("q"):
                break

    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
