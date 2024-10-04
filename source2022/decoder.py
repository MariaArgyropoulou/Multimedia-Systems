import huffman
import numpy as np
import cv2

# Decoder gets the bitstring of each frame and:
#   - First it decodes the bitstring to the actual pixel values
#   - The result is the error-image
#   - Then it re-creates the original frame using the horizontal predictor (X=A)

print("Decoder Starts...")
print("Reading bitstring")
bitstring = open('bitstring.txt', 'r')
bitstring1 = bitstring.read()

print("Applying Huffman decoding...")
list_error_images = huffman.decoder((bitstring1))
print("Huffman decoding is done.")

# re-create the I_frame using X=A predictor

frame = []
height = 360
width = 640
pointer = 0

for i in range(len(list_error_images)):
    
    # reshape each error-image into 720x1280 matrix
    img_reshape = np.array(list_error_images[i])
    img_reshape = img_reshape.reshape(height,width)
    
    # first bitstring represents I_frame
    if i == 0:
        print("Reconstructing I-Frame")
        for j in range(len(img_reshape)):
            
            # get the first value of the image difference
            value = img_reshape[j][0]
            frame.append(value)
            pointer = 0
            
            for k in range(1,len(img_reshape[j])):            

                # calculate the next values of the image difference 
                next = img_reshape[j][k]    
                next_value = value + next
                frame.append(next_value)
                value = next_value
                pointer += 1

        frame = np.array(frame)
        frame = frame.reshape(height,width)
        reconstructed_I_frame = frame

        cv2.imshow("Reconstracted I-Frame", frame.astype(np.uint8))
        cv2.waitKey(0)

        prev_frame = frame
        frame = []


    # next bitstrings represent P_frames
    else:
        # - get the error image
        # - calculate the original image difference using X=A predictor
        # - add the image difference with the previous frame
        
        print("Recontructing P-Frame {}".format(i))
        for j in range(len(img_reshape)):
            
            # get the first value of the image difference
            value = img_reshape[j][0]
            frame.append(value)
            pointer = 0
            
            for k in range(1,len(img_reshape[j])):            

                # calculate the next values of the image difference 
                next = img_reshape[j][k]    
                next_value = value + next
                frame.append(next_value)
                value = next_value
                pointer += 1
            
        frame = np.array(frame)
        frame = frame.reshape(height,width)

        P_frame = frame + prev_frame

        prev_frame = P_frame
        frame = []

        cv2.imshow("Reconstructed P-Frame {}".format(i), P_frame.astype(np.uint8))
        cv2.waitKey(0)
        
print("Finished Deconding")
input()

video = cv2.VideoCapture('walk.mp4')
success, image = video.read()

# first frame is the l-frame
I_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

I_frame_diff = I_frame - reconstructed_I_frame

cv2.imshow("Difference between I-frame and Recontructed I-frame", I_frame_diff.astype(np.uint8))
cv2.waitKey(0)

