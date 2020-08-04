import cv2

# VideoCameraを追加
class VideoCamera():
    def __init__(self):
        self.video = cv2.VideoCapture(2)
   
    def __del__(self):
        self.video.release()

    def get_frame(self):      
        success, image = self.video.read()
        height = image.shape[0]
        width = image.shape[1]
        image = cv2.resize(image , (int(width*0.7), int(height*0.7)))
        ret, jpeg = cv2.imencode('.jpg',image)
        return jpeg.tobytes()

        

    
        