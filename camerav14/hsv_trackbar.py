# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 07:09:08 2020

@author: Kazuma
"""
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import time

def nothing(x):
    pass

cv2.namedWindow("Tracking")
cv2.createTrackbar("LH", "Tracking", 0, 255, nothing)
cv2.createTrackbar("LS", "Tracking", 0, 255, nothing)
cv2.createTrackbar("LV", "Tracking", 0, 255, nothing)
cv2.createTrackbar("UH", "Tracking", 255, 255, nothing)
cv2.createTrackbar("US", "Tracking", 255, 255, nothing)
cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)

def red_detect(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    l_h = cv2.getTrackbarPos("LH", "Tracking")
    l_s = cv2.getTrackbarPos("LS", "Tracking")
    l_v = cv2.getTrackbarPos("LV", "Tracking")

    u_h = cv2.getTrackbarPos("UH", "Tracking")
    u_s = cv2.getTrackbarPos("US", "Tracking")
    u_v = cv2.getTrackbarPos("UV", "Tracking")
    
    hsv_min = np.array([l_h,l_s,l_v])
    hsv_max = np.array([u_h,u_s,u_v])
    mask2 = cv2.inRange(hsv, hsv_min, hsv_max)
    return mask2
"""
    # 赤色のHSVの値域1
    hsv_min = np.array([0,l_s,l_v])
    hsv_max = np.array([30,u_s,u_v])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    # 赤色のHSVの値域2
    hsv_min = np.array([150,l_s,l_v])
    hsv_max = np.array([179,u_s,u_v])
    mask2 = cv2.inRange(hsv, hsv_min, hsv_max)
"""    



# ブロブ解析
def analysis_blob(binary_img):
    # 2値画像のラベリング処理
    label = cv2.connectedComponentsWithStats(binary_img)

    # ブロブ情報を項目別に抽出
    n = label[0] - 1
    data = np.delete(label[2], 0, 0)
    center = np.delete(label[3], 0, 0)

    # ブロブ面積最大のインデックス
    max_index = np.argmax(data[:, 4])

    # 面積最大ブロブの情報格納用
    maxblob = {}

    # 面積最大ブロブの各種情報を取得
    maxblob["upper_left"] = (data[:, 0][max_index], data[:, 1][max_index]) # 左上座標
    maxblob["width"] = data[:, 2][max_index]  # 幅
    maxblob["height"] = data[:, 3][max_index]  # 高さ
    maxblob["area"] = data[:, 4][max_index]   # 面積
    maxblob["center"] = center[max_index]  # 中心座標
    
    return maxblob

def main():
    # 開始時間
    start = time.time()
    # データ格納用のリスト
    data_csv = []

    # カメラのキャプチャ
#     cap = cv2.VideoCapture(videofile_path)
    cap = cv2.VideoCapture(0)
#     ret, frame = cap.read()
    while(cap.isOpened()):
        # フレームを取得
        ret, frame = cap.read()

        # 赤色検出
        mask = red_detect(frame)

        # マスク画像をブロブ解析（面積最大のブロブ情報を取得）
        target = analysis_blob(mask)

        # 面積最大ブロブの中心座標を取得
        center_x = int(target["center"][0])
        center_y = int(target["center"][1])

        # フレームに面積最大ブロブの中心周囲を円で描く
        cv2.circle(frame, (center_x, center_y), 30, (0, 200, 0),
                   thickness=3, lineType=cv2.LINE_AA)
        
        # 経過時間, x, yをリストに追加
        data_csv.append([time.time() - start, center_x, center_y])


        # 結果表示
        cv2.imshow("Frame", frame)
        cv2.imshow("Mask", mask)

        # qキーが押されたら途中終了
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    
    # CSVファイルに保存
    #np.savetxt("color_tracking_data.csv", np.array(data_csv), delimiter=",")
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main() 