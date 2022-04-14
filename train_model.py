from imutils import paths
import face_recognition
import pickle
import cv2
import os


def train_model():
    print("Start training model")
    image_path_list = list(paths.list_images("dataset"))
    if not image_path_list:
        print("there are not dataset")
    else:
        encoding_list = []
        name_list = []

        for (i, image_path) in enumerate(image_path_list):
            print("Training {}/{}".format(i + 1, len(image_path_list)))
            name = image_path.split(os.path.sep)[-2]

            image = cv2.imread(image_path)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            boxes = face_recognition.face_locations(rgb, model="hog")
            encodings = face_recognition.face_encodings(rgb, boxes)

            for encoding in encodings:
                encoding_list.append(encoding)
                name_list.append(name)

        data = {"encodings": encoding_list, "names": name_list}
        f = open("encodings.pickle", "wb")
        f.write(pickle.dumps(data))
        f.close()
