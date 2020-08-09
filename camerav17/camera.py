import cv2
import os
import datetime
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
global f, data, list_shape, list_shape_cx, list_shape_cy, width, height
 #新しい図形が認識されたとき1になる

#新しく認識された図形の種類と中心座標を記録
list_shape = [0]         # 0:bar 1:直方体　2:三角　3:半円　4:四角
list_shape_cx = [0]
list_shape_cy = [0]
width = 600
height = 600

#%matplotlib inline
# VideoCameraを追加
class VideoCamera():
    def __init__(self):
        for i in range(-1, 3):
            self.device_num = i
            self.video = cv2.VideoCapture(self.device_num)
            if self.video.isOpened():
                break

        self.threshold_time = 180
        self.threshold_new_block = 25
        self.threshold_block_move = 3
        self.threshold_area = 500

        self.detect_red_cx = [num*5 for num in range(self.threshold_time)]
        self.detect_red_cy = [num*5 for num in range(self.threshold_time)]
        self.detect_blue_cx = [num*5 for num in range(self.threshold_time)]
        self.detect_blue_cy = [num*5 for num in range(self.threshold_time)]
        self.detect_green_cx = [num*5 for num in range(self.threshold_time)]
        self.detect_green_cy = [num*5 for num in range(self.threshold_time)]
        self.detect_purple_cx = [num*5 for num in range(self.threshold_time)]
        self.detect_purple_cy = [num*5 for num in range(self.threshold_time)]
        self.detect_yellow_cx = [num*5 for num in range(self.threshold_time)]
        self.detect_yellow_cy = [num*5 for num in range(self.threshold_time)]
        
        # HSV色空間における"赤色"の値域を決定
        self.lower_red1 = np.array([0, 65, 0])
        self.upper_red1 = np.array([30, 255, 255])

        self.lower_red2 = np.array([122, 65, 0])
        self.upper_red2 = np.array([180, 255, 255])

        # HSV色空間における"青色"の値域を決定
        self.lower_blue = np.array([93, 90, 0])
        self.upper_blue = np.array([114, 255, 164])
        # HSV色空間における"緑色"の値域を決定
        self.lower_green = np.array([62, 90, 0])
        self.upper_green = np.array([91, 255, 164])
        # HSV色空間における"紫色"の値域を決定
        self.lower_purple = np.array([150, 70, 150])
        self.upper_purple = np.array([160, 176, 255])
        # HSV色空間における"黄色"の値域を決定
        self.lower_yellow = np.array([30, 120, 120])
        self.upper_yellow = np.array([60, 255, 255])

        self.flg = 0
        self.frame = 0
        self.frame_src = 0

    def __del__(self):
        self.video.release()

#-----------------------ずっと回っているとこーーーーーーーーーーーーーーー
    def get_frame(self):      
        font = cv2.FONT_HERSHEY_DUPLEX


        #動画のフレーム数をカウント
        f = 0
        self.flg = 0

        #図形の認識に用いる閾値
        # self.threshold_time = 180
        # self.threshold_new_block = 25
        # self.threshold_block_move = 3
        # self.threshold_area = 500

       

        # self.detect_red_cx = [num*5 for num in range(self.threshold_time)]
        # self.detect_red_cy = [num*5 for num in range(self.threshold_time)]
        # self.detect_blue_cx = [num*5 for num in range(self.threshold_time)]
        # self.detect_blue_cy = [num*5 for num in range(self.threshold_time)]
        # self.detect_green_cx = [num*5 for num in range(self.threshold_time)]
        # self.detect_green_cy = [num*5 for num in range(self.threshold_time)]
        # self.detect_purple_cx = [num*5 for num in range(self.threshold_time)]
        # self.detect_purple_cy = [num*5 for num in range(self.threshold_time)]
        # self.detect_yellow_cx = [num*5 for num in range(self.threshold_time)]
        # self.detect_yellow_cy = [num*5 for num in range(self.threshold_time)]

        # # HSV色空間における"赤色"の値域を決定
        # self.lower_red1 = np.array([0, 65, 0])
        # self.upper_red1 = np.array([30, 255, 255])

        # self.lower_red2 = np.array([122, 65, 0])
        # self.upper_red2 = np.array([180, 255, 255])

        # # HSV色空間における"青色"の値域を決定
        # self.lower_blue = np.array([93, 90, 0])
        # self.upper_blue = np.array([114, 255, 164])
        # # HSV色空間における"緑色"の値域を決定
        # _green = np.array([62, 90, 0])
        # self.upper_green = np.array([91, 255, 164])
        # # HSV色空間における"紫色"の値域を決定
        # self.lower_purple = np.array([150, 70, 150])
        # self.upper_purple = np.array([160, 176, 255])
        # # HSV色空間における"黄色"の値域を決定
        # self.lower_yellow = np.array([30, 120, 120])
        # self.upper_yellow = np.array([60, 255, 255])

        # self.flg = 0
        f += 1
        #ーーーーーーーーーーーーーーーーーーーーーーーーーーself.videoのカメラ映像取得ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
        ret, self.frame = self.video.read()

        # resize the window
        height = self.frame.shape[0]
        width = self.frame.shape[1]
        self.frame = cv2.resize(self.frame , (int(width*0.5), int(height*0.5)))
            
    #     windowsize = (300, 300)
    #     self.frame = cv2.resize(self.frame, windowsize)
        self.frame = cv2.flip(self.frame, 1)
    #---------------------------------------------------------webカメラからの映像------------------------------------------------
        self.frame_src = self.frame.copy()
        
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        
        # ウェブカメラからの"赤色"の検出----------------------------------------------------
        mask_red1 = cv2.inRange(hsv, self.lower_red1, self.upper_red1)
        
        mask_red2 = cv2.inRange(hsv, self.lower_red2, self.upper_red2)
        
        mask_red = mask_red1 + mask_red2
        
        # マスク画像をブロブ解析
        # 2値画像のラベリング処理
        label = cv2.connectedComponentsWithStats(mask_red)

        # ブロブ情報を項目別に抽出
        n = label[0] - 1
        #label[2]は各図形のバウンティンぐボックスとオブジェクトのサイズを保存
        data = np.delete(label[2], 0, 0)
                
        center = np.delete(label[3], 0, 0)

        # 検出した図形の面積から一定の大きさのものだけ抽出
        data2 = np.zeros((0, 5), dtype = "int32")
        center2 = np.zeros((0, 2), dtype = "float64")
        
        for i in range(n):
            if data[i, 4] > self.threshold_area:
                data2 = np.r_[data2, data[i:i+1,:]]
                center2 = np.r_[center2, center[i:i+1,:]]

        if data2.shape[0] != 0:
            for i in range(data2.shape[0]):
                
            # ブロブ面積最大のインデックス
            #max_index = np.argmax(data[:, 4])

                detected_blob = {}
        
                # 各ブロブの各種情報を取得
                detected_blob["upper_left"] = (data2[:, 0][i], data2[:, 1][i]) # 左上座標
                detected_blob["width"] = data2[:, 2][i]  # 幅
                detected_blob["height"] = data2[:, 3][i]  # 高さ
                detected_blob["area"] = data2[:, 4][i]   # 面積
                detected_blob["center"] = center2[i]  # 中心座標
        
                # ブロブの中心座標を取得
                center_red_x = int(detected_blob["center"][0])
                center_red_y = int(detected_blob["center"][1])
                
                cv2.putText(self.frame, "bar",  (center_red_x, center_red_y), font, 1, (0), 2)
                cv2.drawMarker(self.frame, (center_red_x, center_red_y), (0, 0, 0), markerSize=10, thickness=10)
        
                #過去に同じ座標で認識しているとき
                for k in range(len(list_shape_cx)):
                    if( abs(list_shape_cx[k] - center_red_x) < self.threshold_new_block ) and ( abs(list_shape_cy[k] - center_red_y) < self.threshold_new_block ):
                        #print('already detected red'+str(center_red_x)+', '+str(center_red_y))
                        break
                    else:
                        continue
                else:
                    self.detect_red_cx.append(center_red_x)
                    self.detect_red_cy.append(center_red_y)
                    for i_c in range(self.threshold_time):
                        #print("i_c:",i_c)
                        #print("self.detect_red_cx[-1]:",self.detect_red_cx[-1])
                        if (abs( self.detect_red_cx[-1] - self.detect_red_cx[ -(2+i_c) ] ) < self.threshold_block_move):
                            if ( abs(self.detect_red_cy[-1] - self.detect_red_cy[ -(2+i_c) ] )) < self.threshold_block_move:
                                if i_c == (self.threshold_time-1):
                                    #print("bar")
                                    list_shape.append(0)
                                    list_shape_cx.append(center_red_x)
                                    list_shape_cy.append(center_red_y) 
                                    #cv2.imwrite(path+"/new_object_"+str(f)+".jpg", self.frame)
                                    self.flg = 1
                                else:
                                    continue
                            else:
                                break
                        else:
                            break
                    else:
                        break
                continue
        
        # ウェブカメラからの"青色"の検出----------------------------------------------------
        mask_blue = cv2.inRange(hsv, self.lower_blue, self.upper_blue)
        
        # マスク画像を
        # 2値画像のラベリング処理
        label = cv2.connectedComponentsWithStats(mask_blue)

        # ブロブ情報を項目別に抽出
        n = label[0] - 1
        #label[2]は各図形のバウンティンぐボックスとオブジェクトのサイズを保存
        data = np.delete(label[2], 0, 0)
                
        center = np.delete(label[3], 0, 0)

        # 検出した図形の面積から一定の大きさのものだけ抽出
        data2 = np.zeros((0, 5), dtype = "int32")
        center2 = np.zeros((0, 2), dtype = "float64")
        
        for i in range(n):
            if data[i, 4] > self.threshold_area:
                data2 = np.r_[data2, data[i:i+1,:]]
                center2 = np.r_[center2, center[i:i+1,:]]

        if data2.shape[0] != 0:
            for i in range(data2.shape[0]):
                
            # ブロブ面積最大のインデックス
            #max_index = np.argmax(data[:, 4])

                detected_blob = {}
        
                # 各ブロブの各種情報を取得
                detected_blob["upper_left"] = (data2[:, 0][i], data2[:, 1][i]) # 左上座標
                detected_blob["width"] = data2[:, 2][i]  # 幅
                detected_blob["height"] = data2[:, 3][i]  # 高さ
                detected_blob["area"] = data2[:, 4][i]   # 面積
                detected_blob["center"] = center2[i]  # 中心座標
        
                # ブロブの中心座標を取得
                center_blue_x = int(detected_blob["center"][0])
                center_blue_y = int(detected_blob["center"][1])
                
                cv2.putText(self.frame, "box",  (center_blue_x, center_blue_y), font, 1, (0), 2)
                cv2.drawMarker(self.frame, (center_blue_x, center_blue_y), (0, 0, 0), markerSize=10, thickness=10)

                #過去に同じ座標で認識しているとき
                for k in range(len(list_shape_cx)):
                    if( abs(list_shape_cx[k] - center_blue_x) < self.threshold_new_block ) and ( abs(list_shape_cy[k] - center_blue_y) < self.threshold_new_block ):
                        #print('already detected')
                        break
                    else:
                        continue
                else:
                    self.detect_blue_cx.append(center_blue_x)
                    self.detect_blue_cy.append(center_blue_y)
                    for i_c in range(self.threshold_time):
                        #print("i_c",i_c)
                        #print("self.detect_blue_cx[-1]:",self.detect_blue_cx[-1])
                        if (abs( self.detect_blue_cx[-1] - self.detect_blue_cx[ -(2+i_c) ] ) < self.threshold_block_move):
                            if (abs( self.detect_blue_cy[-1] - self.detect_blue_cy[ -(2+i_c) ] ) < self.threshold_block_move):
                                if i_c == (self.threshold_time-1):
                                    #print("box")
                                    list_shape.append(5)
                                    list_shape_cx.append(center_blue_x)
                                    list_shape_cy.append(center_blue_y) 
                                    #cv2.imwrite(path+"/new_object_"+str(f)+".jpg", self.frame)
                                    self.flg = 1
                                else:
                                    continue
                            else:
                                break
                        else:
                            break
                    else:
                        break
                continue
        
        # ウェブカメラからの"緑色"の検出----------------------------------------------------
        mask_green = cv2.inRange(hsv, self.lower_green, self.upper_green)
        # マスク画像をブロブ解析
        # 2値画像のラベリング処理
        label = cv2.connectedComponentsWithStats(mask_green)

        # ブロブ情報を項目別に抽出
        n = label[0] - 1
        #label[2]は各図形のバウンティンぐボックスとオブジェクトのサイズを保存
        data = np.delete(label[2], 0, 0)
                
        center = np.delete(label[3], 0, 0)

        # 検出した図形の面積から一定の大きさのものだけ抽出
        data2 = np.zeros((0, 5), dtype = "int32")
        center2 = np.zeros((0, 2), dtype = "float64")
        
        for i in range(n):
            if data[i, 4] > self.threshold_area:
                data2 = np.r_[data2, data[i:i+1,:]]
                center2 = np.r_[center2, center[i:i+1,:]]

        if data2.shape[0] != 0:
            for i in range(data2.shape[0]):
            
            # ブロブ面積最大のインデックス
            #max_index = np.argmax(data[:, 4])

                detected_blob = {}
        
                # 各ブロブの各種情報を取得
                detected_blob["upper_left"] = (data2[:, 0][i], data2[:, 1][i]) # 左上座標
                detected_blob["width"] = data2[:, 2][i]  # 幅
                detected_blob["height"] = data2[:, 3][i]  # 高さ
                detected_blob["area"] = data2[:, 4][i]   # 面積
                detected_blob["center"] = center2[i]  # 中心座標
        
                # ブロブの中心座標を取得
                center_green_x = int(detected_blob["center"][0])
                center_green_y = int(detected_blob["center"][1])
                
                cv2.putText(self.frame, "triangle",  (center_green_x, center_green_y), font, 1, (0), 2)
                cv2.drawMarker(self.frame, (center_green_x, center_green_y), (0, 0, 0), markerSize=10, thickness=10)    
        
                #過去に同じ座標で認識しているとき
                for k in range(len(list_shape_cx)):
                    if( abs(list_shape_cx[k] - center_green_x) < self.threshold_new_block ) and ( abs(list_shape_cy[k] - center_green_y) < self.threshold_new_block ):
                        #print('already detected green:'+str(center_green_x)+', '+str(center_green_y))
                        break
                    else:
                        continue
                else:
                    self.detect_green_cx.append(center_green_x)
                    self.detect_green_cy.append(center_green_y)
                    for i_c in range(self.threshold_time):
                        #print("i_c:",i_c)
                        #print("self.detect_green_cx[-1]:",self.detect_green_cx[-1])
                        if (abs( self.detect_green_cx[-1] - self.detect_green_cx[ -(2+i_c) ] ) < self.threshold_block_move):
                            if (abs( self.detect_green_cy[-1] - self.detect_green_cy[ -(2+i_c) ] ) < self.threshold_block_move):
                                if i_c == (self.threshold_time-1):
                                    #print("triangle")
                                    list_shape.append(3)
                                    list_shape_cx.append(center_green_x)
                                    list_shape_cy.append(center_green_y) 
                                    #cv2.imwrite(path+"/new_object_"+str(f)+".jpg", self.frame)
                                    self.flg = 1
                                else:
                                    continue
                            else:
                                break
                        else:
                            break
                    else:
                        break
                continue
        
        # ウェブカメラからの"紫色"の検出----------------------------------------------------
        mask_purple = cv2.inRange(hsv, self.lower_purple, self.upper_purple)
        
        # マスク画像をブロブ解析
        # 2値画像のラベリング処理
        label = cv2.connectedComponentsWithStats(mask_purple)

        # ブロブ情報を項目別に抽出
        n = label[0] - 1
        #label[2]は各図形のバウンティンぐボックスとオブジェクトのサイズを保存
        data = np.delete(label[2], 0, 0)
                
        center = np.delete(label[3], 0, 0)

        # 検出した図形の面積から一定の大きさのものだけ抽出
        data2 = np.zeros((0, 5), dtype = "int32")
        center2 = np.zeros((0, 2), dtype = "float64")
        
        for i in range(n):
            if data[i, 4] > self.threshold_area:
                data2 = np.r_[data2, data[i:i+1,:]]
                center2 = np.r_[center2, center[i:i+1,:]]

        if data2.shape[0] != 0:
            for i in range(data2.shape[0]):
                
            # ブロブ面積最大のインデックス
            #max_index = np.argmax(data[:, 4])

                detected_blob = {}
        
                # 各ブロブの各種情報を取得
                detected_blob["upper_left"] = (data2[:, 0][i], data2[:, 1][i]) # 左上座標
                detected_blob["width"] = data2[:, 2][i]  # 幅
                detected_blob["height"] = data2[:, 3][i]  # 高さ
                detected_blob["area"] = data2[:, 4][i]   # 面積
                detected_blob["center"] = center2[i]  # 中心座標
        
                # ブロブの中心座標を取得
                center_purple_x = int(detected_blob["center"][0])
                center_purple_y = int(detected_blob["center"][1])
                
                cv2.putText(self.frame, "half-circle",  (center_purple_x, center_purple_y), font, 1, (0), 2)
                cv2.drawMarker(self.frame, (center_purple_x, center_purple_y), (0, 0, 0), markerSize=10, thickness=10)

                #過去に同じ座標で認識しているとき
                for k in range(len(list_shape_cx)):
                    if( abs(list_shape_cx[k] - center_purple_x) < self.threshold_new_block ) and ( abs(list_shape_cy[k] - center_purple_y) < self.threshold_new_block ):
                        #print('already detected purple:'+str(center_purple_x)+', '+str(center_purple_y))
                        break
                    else:
                        continue
                else:
                    self.detect_purple_cx.append(center_purple_x)
                    self.detect_purple_cy.append(center_purple_y)
                    for i_c in range(self.threshold_time):
                        #print("i_c:",i_c)
                        #print("self.detect_purple_cx[-1]:",self.detect_purple_cx[-1])
                        if (abs( self.detect_purple_cx[-1] - self.detect_purple_cx[ -(2+i_c) ] ) < self.threshold_block_move):
                            if( abs( self.detect_purple_cy[-1] - self.detect_purple_cy[ -(2+i_c) ] ) < self.threshold_block_move):
                                if i_c == (self.threshold_time-1):
                                    #print("half-circle")
                                    list_shape.append(3)
                                    list_shape_cx.append(center_purple_x)
                                    list_shape_cy.append(center_purple_y) 
                                    #cv2.imwrite(path+"/new_object_"+str(f)+".jpg", self.frame)
                                    self.flg = 1
                                else:
                                    continue
                            else:
                                break
                        else:
                            break
                    else:
                        break
                continue

        # ウェブカメラからの"黄色"の検出----------------------------------------------------
        mask_yellow = cv2.inRange(hsv, self.lower_yellow, self.upper_yellow)
        
        # マスク画像をブロブ解析
        # 2値画像のラベリング処理
        label = cv2.connectedComponentsWithStats(mask_yellow)

        # ブロブ情報を項目別に抽出
        n = label[0] - 1
        #label[2]は各図形のバウンティンぐボックスとオブジェクトのサイズを保存
        data = np.delete(label[2], 0, 0)
                
        center = np.delete(label[3], 0, 0)

        # 検出した図形の面積から一定の大きさのものだけ抽出
        data2 = np.zeros((0, 5), dtype = "int32")
        center2 = np.zeros((0, 2), dtype = "float64")
        
        for i in range(n):
            if data[i, 4] > self.threshold_area:
                data2 = np.r_[data2, data[i:i+1,:]]
                center2 = np.r_[center2, center[i:i+1,:]]

        if data2.shape[0] != 0:
            for i in range(data2.shape[0]):
                
            # ブロブ面積最大のインデックス
            #max_index = np.argmax(data[:, 4])

                detected_blob = {}
        
                # 各ブロブの各種情報を取得
                detected_blob["upper_left"] = (data2[:, 0][i], data2[:, 1][i]) # 左上座標
                detected_blob["width"] = data2[:, 2][i]  # 幅
                detected_blob["height"] = data2[:, 3][i]  # 高さ
                detected_blob["area"] = data2[:, 4][i]   # 面積
                detected_blob["center"] = center2[i]  # 中心座標
        
                # ブロブの中心座標を取得
                center_yellow_x = int(detected_blob["center"][0])
                center_yellow_y = int(detected_blob["center"][1])
                
                cv2.putText(self.frame, "square",  (center_yellow_x, center_yellow_y), font, 1, (0), 2)
                cv2.drawMarker(self.frame, (center_yellow_x, center_yellow_y), (0, 0, 0), markerSize=10, thickness=10)

                #過去に同じ座標で認識しているとき
                for k in range(len(list_shape_cx)):
                    if( abs(list_shape_cx[k] - center_yellow_x) < self.threshold_new_block ) and ( abs(list_shape_cy[k] - center_yellow_y) < self.threshold_new_block ):
                        #print('already detected yellow:'+str(center_yellow_x)+', '+str(center_yellow_y))
                        break
                    else:
                        continue
                else:
                    self.detect_yellow_cx.append(center_yellow_x)
                    self.detect_yellow_cy.append(center_yellow_y)
                    for i_c in range(self.threshold_time):
                        #print("i_c:",i_c)
                        #print("self.detect_yellow_cx[-1]:",self.detect_yellow_cx[-1])
                        if (abs( self.detect_yellow_cx[-1] - self.detect_yellow_cx[ -(2+i_c) ] ) < self.threshold_block_move):
                            #print("a")
                            if (abs( self.detect_yellow_cy[-1] - self.detect_yellow_cy[ -(2+i_c) ] ) < self.threshold_block_move):
                            #print("b")
                                if i_c == (self.threshold_time-1):
                                    #print("square")
                                    list_shape.append(4)
                                    list_shape_cx.append(center_yellow_x)
                                    list_shape_cy.append(center_yellow_y) 
                                    #cv2.imwrite(path+"/new_object_"+str(f)+".jpg", self.frame)
                                    self.flg = 1
                                else:
                                    continue
                            else:
                                break
                        else:
                            break
                    else:
                        break
                continue
        
    #     print('self.frame:'+str(f))
        # cv2.imshow('mask_purple', mask_purple)
        # cv2.imshow('mask_red', mask_red)
        # cv2.imshow('mask_blue', mask_blue)
        # cv2.imshow('mask_green', mask_green)
        # cv2.imshow('mask_yellow', mask_yellow)
        # cv2.imshow('main',self.frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

        # capture.release()
        # cv2.destroyAllWindows()


        #htmlに送る用のコード
        ret, jpeg = cv2.imencode('.jpg',self.frame)
        if self.flg == 0:
            shape = 0
            vec = [0, 0]
        else:
            shape = list_shape[-1]
            vec = [list_shape_cx[-1], list_shape_cy[-1]]

        x = np.random.randint(100, 400)

        return jpeg.tobytes(), self.flg, shape, vec, x

    def input_shape(self):
        # global self.flg, list_shape
        if self.flg == 0:
            shape = 0
        else:
            shape = list_shape[-1]
        return shape

    def input_vec(self):
        # global self.flg, list_shape_cx, list_shape_cy
        if self.flg == 0:
            vec = [0, 0]
        else:
            vec = [list_shape_cx[-1], list_shape_cy[-1]]
        return vec

    def flag(self):
        # global self.flg
        return self.flg 

    def frame_size(self):
        ret, self.frame = self.video.read()

        # resize the window
        height = self.frame.shape[0]
        width = self.frame.shape[1]
        self.frame_vec = [width*0.5, height*0.5]
        return self.frame_vec

    def video_cap(self, path_img, dir_img):
        success, image = self.video.read()
        self.path_img = path_img
        self.dir_img = dir_img
        image_name = os.path.join(self.dir_img, self.path_img) + '.JPG'
        cv2.imwrite(image_name, image)
        