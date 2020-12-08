import cv2
from utils import cropface

'''

###################    Examples          #########################
=> Load Video And Make Dataset
video_to_image_dataset("mrinmoy", "20201208_130458.mp4")
=> Use Webcam To Create Dataset
video_to_image_dataset("tanmoy", "http://192.168.0.124:4747/video?640x480")
###################      End Of  Examples          #########################3

###   Parameters ###
name = Character Name (If it is already present then it will add those images)
source = Either file location or Video Feed
rotatemode = If you want to rotate => Values = > ["90clock","90anticlock","180"]
show_frames = Boolean If You want to show frames => Default True
save_original = Boolean If you want  to save also otiginal frames in "data" folder => Default True
two_eyes_present = Boolean False If you want to save faces where two eyes yet cannot detected => Default True
output_frame_size = (width,height) Default => It will resize to (frame_width/3, frame_height/3)

'''


rotatemodedict = {
    "90clock": cv2.ROTATE_90_CLOCKWISE,
    "90anticlock": cv2.ROTATE_90_COUNTERCLOCKWISE,
    "180": cv2.ROTATE_180
}


def video_to_image_dataset(name, source, step=5, rotatemode=None, show_frames=True, save_original=True, two_eyes_present=True, output_frame_size=None):
    cap = cv2.VideoCapture(source)
    width = cap.get(3)
    height = cap.get(4)
    frame_new_width = int(width/3)
    frame_new_height = int(height/3)
    tmp = 0
    if output_frame_size is None:
        output_frame_size = (frame_new_width, frame_new_height)
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (frame_new_width, frame_new_height))
        if rotatemode is not None:
            frame = cv2.rotate(frame, rotatemodedict[rotatemode])
        if show_frames:
            cv2.imshow(name, frame)
        if tmp % step == 0:
            cropface(frame, name, two_eyes_present=two_eyes_present,
                     save_original=save_original)
        tmp += 1
        k = cv2.waitKey(30) & 0xFF
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


# video_to_image_dataset("mrinmoy", "20201208_130458.mp4", rotatemode="90clock")
# video_to_image_dataset("tanmoy", "http://192.168.0.124:4747/video?640x480",rotatemode="90clock", two_eyes_present=False)
