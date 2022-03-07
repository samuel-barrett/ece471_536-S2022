from random import random
import numpy as np
import cv2
import os

def GetDuck(duck_num):
    duck_path = os.path.dirname(__file__) + "/match_images"
    duck = cv2.imread(duck_path + "/duck" + str(duck_num) + ".jpg")
    if duck is None:
        raise Exception("Error: duck image not found: {}".format(duck_path + "/duck" + str(duck_num) + ".jpg"))
    duck = cv2.normalize(duck, None, 0, 255, cv2.NORM_MINMAX)
    duck = duck.astype(np.uint8)
    return duck

num_ducks = 7
def GlobalInit():
    global num_ducks
    ducks = [GetDuck(i) for i in range(1,num_ducks+1)]
    sift = cv2.SIFT_create()
    des1s = []
    kp1s = []
    for duck in ducks:
        kp1, des1 = sift.detectAndCompute(duck, None)
        des1s.append(des1)
        kp1s.append(kp1)
    bf = cv2.BFMatcher()
    return sift, bf, des1s, kp1s, ducks

sift, bf, des1s, kp1s,ducks = GlobalInit()
counter = 0

def FindMatch(duck_num, current_frame):
    """
    Use sift to find the best match for the duck
    """
    global des1s, sift, bf, kp1s, counter, ducks
    #Convert duck and current_frame to uint8
    current_frame = current_frame.astype(np.uint8)

    des1 = des1s[duck_num-1]
    kp2, des2 = sift.detectAndCompute(current_frame, None)
    matches = bf.knnMatch(des1, des2, k=2)

    #Get location of best match
    good = np.array([m for (m,n) in matches if m.distance < np.random.uniform(0.7, 0.85)*n.distance])

    #Show image with matches to file
    img = cv2.drawMatches(ducks[duck_num-1], kp1s[duck_num-1], current_frame, kp2, good, None, flags=2)
    cv2.imwrite("match/match" + str(counter) + ".jpg", img)
    counter += 1

    if len(good) == 0:
        return {'duck_num':0, 'loc':(0,0), 'duck':duck_num}

    locs = np.array([kp2[m.trainIdx].pt for m in good])

    median = np.median(locs, axis=0)
    
    return {'duck_num': len(locs), 'loc': (int(median[1]), int(median[0])), 'duck':duck_num}

duck_choice = 0
def GetLocation(move_type, env, current_frame):
    global num_ducks, duck_choice
    duck_choice += 1
    if duck_choice == num_ducks+1:
        duck_choice = 1
    #return [{'coordinate' : FindMatch(7, current_frame)['loc'], 'move_type' : "absolute"}]
    return [{'coordinate' : FindMatch(duck_choice, current_frame)['loc'], 'move_type' : "absolute"}]
    



