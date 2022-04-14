from train_model import train_model
from create_data_set import capture_face
from facial_recognition import facial_recognition


def print_menu():
    print("------------------------------------------------------------")
    print("Face Recognition in Raspberry Pi 4")
    print("------------------------------------------------------------")
    print("1. Create data set, snap shot your face")
    print("2. Train model")
    print("3. Face Recognition")
    print("------------------------------------------------------------")


def select_option():
    option = input("please enter 1 - 3:")
    if option in ["1", "2", "3"]:
        if option == "1":
            capture_face()
        if option == "2":
            train_model()
        if option == "3":
            facial_recognition()
            pass

    else:
        print("------------------------------------------------------------")
        print("wrong input, please try again")
        print_menu()
        select_option()


if __name__ == "__main__":
    print_menu()
    select_option()
