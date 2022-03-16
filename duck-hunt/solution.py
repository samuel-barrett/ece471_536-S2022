import cv2
import os
import numpy as np
#

num_ducks = 7

def GetDuck(duck_num):
    duck_path = os.path.dirname(__file__) + "/match_images"
    duck = cv2.imread(duck_path + "/duck" + str(duck_num) + ".jpg")
    if duck is None:
        raise Exception("Error: duck image not found: {}".format(duck_path + "/duck" + str(duck_num) + ".jpg"))
    return duck


def GlobalInit():
    """
    Precompute all the sift descriptors for ducks
    """
    global num_ducks
    ducks = [GetDuck(i) for i in range(1,num_ducks+1)]
    sift = cv2.SIFT_create()
    des1s = []
    kp1s = []
    for duck in ducks:
        kp1, des1 = sift.detectAndCompute(duck, None)
        des1s.append(des1)
        kp1s.append(kp1)
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
    return sift, bf, des1s, kp1s

sift, bf, des1s, kp1s = GlobalInit()


duck_choice = 0
def GetLocation(move_type, env, current_frame):
    global num_ducks, duck_choice
    global des1s, sift, bf, kp1s
    duck_choice = (duck_choice + 1) % num_ducks

    kp2, des2 = sift.detectAndCompute(current_frame, None)
    matches = bf.knnMatch(des1s[duck_choice], des2, k=2)

    y,x = kp2[min(matches, key=lambda x: x[0].distance/x[1].distance)[0].trainIdx].pt

    return [{'coordinate':(x,y), 'move_type' : "absolute"}]

