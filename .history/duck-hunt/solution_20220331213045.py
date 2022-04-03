import cv2
import os
from cv2 import IMREAD_GRAYSCALE
import numpy as np

class DuckHunt(object):
    """
    Class to handle components of the SIFT algorithm for finding the best match
    with the duck hunt game.
    @param num_ducks: number of ducks to hunt
    """
    def __init__(self, num_ducks):
        """
        @param num_ducks: number of ducks to hunt
        """
        self.num_ducks = num_ducks
        self.ducks = self.get_ducks()
        print("was here")
        self.sift = cv2.SIFT_create()
        self.duck_descriptors = []
        self.duck_keypoints = []
        for duck in self.ducks:
            kp1, des1 = self.sift.detectAndCompute(duck, None)
            self.duck_descriptors.append(des1)
            self.duck_keypoints.append(kp1)
        self.brute_force_matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
        self.duck_choice = 0
    
    
    def get_ducks(self):
        """
        Gets the duck images from the duck_hunt directory and returns them as a list
        @return: list of duck images
        """
        ducks = []
        for duck_num in range(1, self.num_ducks+1):
            duck_path = os.path.dirname(__file__) + "/match_images/duck" + str(duck_num) + ".jpg"
            duck = cv2.imread(duck_path, cv2.IMREAD_GRAYSCALE)
            if duck is None:
                raise ValueError("Error: duck image not found: {}".format(duck_path))
            ducks.append(duck)
        return ducks

    def update_duck_choice(self):
        """_summary_
        Updates the duck image choice to be used in the next frame for SIFT matching.
        """
        self.duck_choice += 1
        self.duck_choice %= self.num_ducks
        
    def matcher(self, kp2, des2):
        #matches = self.brute_force_matcher.knnMatch(self.duck_descriptors[self.duck_choice], des2, k=2)
        #if len(matches) == 0:
        #    return (0,0)
        #y,x = kp2[min(matches, key=lambda x: x[0].distance+x[1].distance)[0].trainIdx].pt
        #return (x, y)
        
        """Uses SIFT to find the best match between the current frame and the duck image. Best match is 
        determined using a brute force matcher. The best match is the one with the lowest distance ratio between
        descriptors.

        Args:
            kp2 (_type_): The current frame keypoints
            des2 (_type_): The current frame descriptors
        """
        
        
    
    def sift_match(self, current_frame: np.ndarray) -> tuple:
        """Uses SIFT to find the best match between the current frame and the duck image. Best match is 
        determined using a brute force matcher. The best match is the one with the lowest distance ratio between
        descriptors.

        Args:
            current_frame (np.ndarray): current frame to be matched to duck image

        Returns:
            (x,y): tuple of x and y coordinates of the best match in the current frame
        """
        kp2, des2 = self.sift.detectAndCompute(current_frame, None)
        match = self.matcher(kp2, des2)
        self.update_duck_choice()
        return match
    
    def template_match(self, current_frame: np.ndarray) ->  tuple:
        current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        duck = self.ducks[self.duck_choice]
        match = cv2.matchTemplate(current_frame, duck, cv2.TM_CCOEFF_NORMED)
        #Get location of best match (highest value)
        _, _, _, max_loc = cv2.minMaxLoc(match)
        y = max_loc[0] + int(duck.shape[0]/2)
        x = max_loc[1] + int(duck.shape[1]/2)
        self.update_duck_choice()
        return (x,y)

duck_hunt = DuckHunt(7)

def GetLocation(move_type, env, current_frame, using_multiprocessor=False):
    global duck_hunt
    
    #Sift is not working on the multiprocessor version of the game.
    #I am not sure why, but it is working fine on the multithreaded version
    #I have set it to use template matching so that it at least does something.
    if using_multiprocessor:
        print("Using multiprocessor")
        return [{'coordinate': duck_hunt.template_match(current_frame), 'move_type': 'absolute'}]
    else:
        return[{'coordinate': duck_hunt.sift_match(current_frame), 'move_type': 'absolute'}]

