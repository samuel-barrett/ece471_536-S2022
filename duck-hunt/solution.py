import time
#Import numpy
import numpy as np
#Import cv2
import cv2

previous_frame = None

"""
Uses motion detection to determine where duck is based on current frame and previous frame
"""
def GetLocation(move_type, env, current_frame):
    global previous_frame
    #time.sleep(1) #artificial one second processing time

    move_type = "absolute"

    #Convert to grayscale
    current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

    if previous_frame is None:
        previous_frame = current_frame
        move_type = "absolute"
        coordinate = (env.width//2, env.height//2)
        #Return dictionary 
        return [{'coordinate' : coordinate, 'move_type' : move_type}]

    #Create motion vector using block matching
    block_size = 50
    #Crate an np array of zero tuples of size current_frame/block_size x current_frame/block_size
    motion_vector = np.zeros((current_frame.shape[0]//block_size, current_frame.shape[1]//block_size, 2), dtype=np.int32)

    R = 10 #R is the search radius


    #Loop through each block in the motion vector
    for i in range(0, current_frame.shape[0]-block_size, block_size):
        for j in range(0, current_frame.shape[1]-block_size, block_size):
            #Get the block from the current frame
            current_block = current_frame[i:i+block_size, j:j+block_size]
            #print("Current block: {},{}".format(i,j))
            #print(current_block)

            min_diff = np.sum(np.abs(current_block - previous_frame[i:i+block_size, j:j+block_size]))
            if min_diff == 0.0:
                motion_vector[i//block_size, j//block_size] = (0,0)
                continue
            motion_x = 0
            motion_y = 0
            #Search region around the current block to find the best match
            for x in range(i-R, i+R+1):
                for y in range(j-R, j+R+1):
                    #If the block is out of bounds, skip
                    if x < 0 or y < 0 or x+block_size > current_frame.shape[0] or y+block_size > current_frame.shape[1]:
                        continue
                    #Get the block from the previous frame
                    previous_block = previous_frame[x:x+block_size, y:y+block_size]
                    #Calculate the difference between the blocks
                    diff = np.sum(np.abs(current_block - previous_block))

                    #print("{}".format(diff), end=' ')

                    #If the difference is less than the current motion, set the motion to the difference
                    if diff < min_diff:
                        min_diff = diff
                        motion_x = x - i
                        motion_y = y - j
                #print()
            
            #print("Min diff: {}".format(min_diff))
            #Set the motion vector to the motion
            if min_diff < 2: #if the difference is less than 2, set the motion to 0, as there is no motion
                motion_vector[i//block_size, j//block_size] = (0,0)
            motion_vector[i//block_size][j//block_size] = (motion_x, motion_y)

    print("Motion vector:")
    for i in range(motion_vector.shape[0]):
        for j in range(motion_vector.shape[1]):
            print(motion_vector[i][j], end=",")
        print()
    #Find indices of block with most motion
    max_motion = 0
    max_motion_index = (0,0)
    for i in range(motion_vector.shape[0]):
        for j in range(motion_vector.shape[1]):
            if motion_vector[i][j][0]**2 + motion_vector[i][j][1]**2 > max_motion:
                max_motion = motion_vector[i][j][0]**2 + motion_vector[i][j][1]**2
                max_motion_index = (i,j)
    #Set coordinate to the max motion index
    print("Max motion index: {}".format(max_motion_index))
    coordinate = (max_motion_index[0]*block_size, max_motion_index[1]*block_size)

    #Return dictionary
    return [{'coordinate' : coordinate, 'move_type' : move_type}]








