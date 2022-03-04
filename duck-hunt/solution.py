import numpy as np
import cv2
import os

def PreProcessFrame(current_frame):
    current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    current_frame = cv2.normalize(current_frame, None, 0, 255, cv2.NORM_MINMAX)
    current_frame = current_frame.astype(np.float32)
    cv2.imwrite("current_frame.jpg", current_frame)
    return current_frame


def GetDuck(duck_num):
    duck_path = os.path.dirname(__file__) + "/match_images"
    duck = cv2.imread(duck_path + "/duck" + str(duck_num) + ".jpg")
    if duck is None:
        raise Exception("Error: duck image not found: {}".format(duck_path + "/duck" + str(duck_num) + ".jpg"))
    duck = cv2.normalize(duck, None, 0, 255, cv2.NORM_MINMAX)
    duck = duck.astype(np.float32)
    return duck


num_ducks = 3
ducks = [GetDuck(i) for i in range(1,num_ducks+1)]


def FindMatch(duck, current_frame):
    """
    Use sift to find the best match for the duck
    """
    #Convert duck and current_frame to uint8
    duck = duck.astype(np.uint8)
    current_frame = current_frame.astype(np.uint8)
    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(duck, None)
    kp2, des2 = sift.detectAndCompute(current_frame, None)
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    #Get location of best match
    good = np.array([m for (m,n) in matches if m.distance < 0.75*n.distance])

    if len(good) == 0:
        return {'duck_num':0, 'loc':(0,0), 'duck':duck}

    locs = np.array([kp2[m.trainIdx].pt for m in good])

    median = np.median(locs, axis=0)

    return {'duck_num': len(locs), 'loc': (int(median[1]), int(median[0])), 'duck':duck}

    
    

def FindBestMatch(num_ducks, current_frame):
    global ducks
    results = []
    for duck_num in range(1,num_ducks+1):
        duck = ducks[duck_num-1]
        results.append(FindMatch(duck, current_frame))

    #print(results)
    
    #Find the best match
    best_match = max(results, key=lambda x: x['duck_num'])
    
    return (best_match['loc'], best_match['duck'])

def GetLocation(move_type, env, current_frame):
    num_ducks = 3
    results = [] 

    max_loc, duck = FindBestMatch(num_ducks, current_frame)
    if duck is None:
        max_loc = (0,0)
    
    return [{'coordinate' : max_loc, 'move_type' : "absolute"}]
    



