import cv2

def init_camera(width=640, height=480, index=0):
    camera_capture = cv2.VideoCapture(index)

    if not camera_capture.isOpened():
        raise("Error in opening the video stream.")

    camera_capture.set(3, width) # adjust width
    camera_capture.set(4, height) # adjust height
    return camera_capture