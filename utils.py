import cv2
import os

face_cascade = cv2.CascadeClassifier(
    './haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_eye.xml')
original_images_dir = '/data/'
cropped_images_dir = '/cropped/'


def get_cropped_image_if_1_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) >= 1:
        for (x, y, w, h) in faces:
            roi_color = img[y:y+h, x:x+w]
            return roi_color
    else:
        print(f'{len(faces)} face are present ')
    return None


def get_cropped_image_if_1_face_and_2_eyes(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) == 1:
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            if len(eyes) >= 2:
                return roi_color
            else:
                print(f'{len(eyes)} eye are present')
    else:
        print(f'{len(faces)} face are present')
    return None


def read_count(dir_name):
    try:
        with open(os.getcwd()+f'/{dir_name}/'+"log.txt") as f:
            return int(f.read())
    except:
        return 0


def write_count(dir_name, present_count):
    with open(os.getcwd()+f'/{dir_name}/'+"log.txt", "w") as f:
        f.write(str(present_count))


def cropface(img, name, two_eyes_present=True, save_original=False):
    count = read_count(name)+1
    # Check root folder
    if os.path.exists(os.getcwd()+f'/{name}'):
        pass
    else:
        os.mkdir(os.getcwd()+f'/{name}/')
    # Check If Original Files Folder Exsists else Create
    if save_original:
        if os.path.exists(os.getcwd()+f'/{name}'+original_images_dir):
            pass
        else:
            os.mkdir(os.getcwd()+f'/{name}'+original_images_dir)
    # Check If Cropped Files Folder Exsists else Create
    if os.path.exists(os.getcwd()+f'/{name}'+cropped_images_dir):
        pass
    else:
        os.mkdir(os.getcwd()+f'/{name}'+cropped_images_dir)
    # Conditions Checking To Check If it is human
    if two_eyes_present:
        tmp = get_cropped_image_if_1_face_and_2_eyes(img)
    else:
        tmp = get_cropped_image_if_1_face(img)
    # Checking Face Found OR Not
    if tmp is None:
        pass
    else:
        cv2.imwrite(os.getcwd()+f'/{name}' +
                    original_images_dir+str(count)+".jpg", img)
        write_count(name, count)
        try:
            filename = os.getcwd()+f'/{name}' + \
                cropped_images_dir+str(count)+".jpg"
            cv2.imwrite(filename, tmp)
            write_count(name, count)
        except:
            print("Save Failed")
