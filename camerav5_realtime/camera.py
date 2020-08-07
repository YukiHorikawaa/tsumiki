import cv2
import os
import datetime
# VideoCameraを追加
class VideoCamera():
    def __init__(self):
        for i in range(-1, 3):
            self.device_num = i
            self.video = cv2.VideoCapture(self.device_num)
            if self.video.isOpened():
                break
   
    def __del__(self):
        self.video.release()

    def get_frame(self):      
        success, image = self.video.read()
        height = image.shape[0]
        width = image.shape[1]
        image = cv2.resize(image , (int(width*0.7), int(height*0.7)))
        ret, jpeg = cv2.imencode('.jpg',image)
        return jpeg.tobytes()

    def video_cap(self, path_img, dir_img):
        success, image = self.video.read()
        self.path_img = path_img
        self.dir_img = dir_img
        image_name = os.path.join(self.dir_img, self.path_img) + '.JPG'
        cv2.imwrite(image_name, image)
        

        

    
        