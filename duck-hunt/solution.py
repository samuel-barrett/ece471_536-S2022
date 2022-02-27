import time
import numpy as np

"""
Replace following with your own algorithm logic

Two random coordinate generator has been provided for testing purposes.
Manual mode where you can use your mouse as also been added for testing purposes.
"""
def GetLocation(move_type, env, current_frame):
    time.sleep(1) #artificial one second processing time

    move_type = "absolute"
    
    #Use relative coordinates to the current position of the "gun", defined as an integer below
    if move_type == "relative":
        """
        North = 0
        North-East = 1
        East = 2
        South-East = 3
        South = 4
        South-West = 5
        West = 6
        North-West = 7
        NOOP = 8
        """
        #coordinate = env.action_space.sample()
        coordinate = 3
    #Use absolute coordinates for the position of the "gun", coordinate space are defined below
    else:
        """
        (x,y) coordinates
        Upper left = (0,0)
        Bottom right = (W, H) 
        """
        #Find bird shaped object in current frame
        coordinate = (np.random.randint(0, env.width-1), np.random.randint(0, env.height-1))


        print("coordinate: ", coordinate)
        
    
    return [{'coordinate' : coordinate, 'move_type' : move_type}]

