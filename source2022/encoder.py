import cv2
import numpy as np
import huffman

# I-frame will be compressed and saved as lossless jpeg:
#   - Convert BGR image to grayscale
#   - Calculate prediction-image using horizontal predictor X=A
#   - Calculate the prediction error-image (original image - prediction image)
#   - Entropy encoding on the result (huffman encoding)
#
# P-frames are predicted from the previous frame:
#   - Convert BGR image to grayscale
#   - Calculate the absolute image difference between the previous frame and the target frame (target frame - previous frame)
#   - Calculate the prediction-image using horizontal predictor X=A
#   - Calculate the prediction error-image (image difference - prediction-image)
#   - Entropy encoding on the result (huffman encoding)

# read frame in grayscale
video = cv2.VideoCapture('walk.mp4')
success, image = video.read()
total_frames=0

# first frame is the I-frame
I_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

cv2.imshow("I-frame", I_frame)
cv2.waitKey(0)

# calculate width and height of frame
width = len(I_frame[0])
height = len(I_frame)

img_diff_prediction = []

# roll each row as X=A
for i in range(height):
    img_diff_prediction.append(np.roll(I_frame[i],1))
    # setting first value of each row 0
    img_diff_prediction[i][0] = 0

# calculate probabilities for each unique number in the frame
# calculate the error image
error_image = I_frame-img_diff_prediction

cv2.imshow("I-frame error image", error_image)
cv2.waitKey(0)

# get the probabilities of unique values in the I-frame difference 
uniq, counts = np.unique(error_image,return_counts=True)

# convert probabilities into dictionary
probabilities = dict(np.asarray((uniq,counts)).T)
# sort dictionary by ascending order
probabilities = {k: v for k, v in sorted(probabilities.items(), key=lambda item: item[1])}
# generate huffman code
codes = huffman.encode(probabilities)
# scan error-image and convert each value to it's huffman code
bitstring = ''
for i in range(len(error_image)):
    for j in range(len(error_image[i])):
        bitstring += codes[error_image[i][j]]
        
f = (open('bitstring.txt', 'a'))
# l frame will not add " - " only p frames will write " - " before the bitstring
f.write(bitstring + " | " + str(codes))
f.close

prev_frame = I_frame

#while success:
while total_frames <= 4:
    success, P_frame = video.read()
    P_frame = cv2.cvtColor(P_frame, cv2.COLOR_BGR2GRAY)

    print('read a new frame:', success)
    total_frames += 1
    image_difference = abs(P_frame - prev_frame)
    
    cv2.imshow("Image-Difference {}".format(total_frames),image_difference)
    cv2.waitKey(0)

    img_diff_prediction = []
    # roll each row as X=A
    for i in range(height):
        img_diff_prediction.append(np.roll(image_difference[i],1))
        # setting first value of each row 0
        img_diff_prediction[i][0] = 0

    # calculate the error image
    error_image = image_difference-img_diff_prediction

    cv2.imshow("Error-Image {}".format(total_frames),error_image)
    cv2.waitKey(0)

    # get probabilities of unique values in the l-frame difference 
    uniq, counts = np.unique(error_image,return_counts=True)

    # convert probabilities into dictionary
    probabilities = dict(np.asarray((uniq,counts)).T)
    # sort dictionary by ascending order
    probabilities = {k: v for k, v in sorted(probabilities.items(), key=lambda item: item[1])}
    # generate huffman code
    codes = huffman.encode(probabilities)
    # scan error image and convert each value to it's huffman code
    bitstring = ''
    for i in range(len(error_image)):
        for j in range(len(error_image[i])):
            bitstring += codes[error_image[i][j]]
            
    f = (open('bitstring.txt', 'a'))
    # l frame will not add " - " only p frames will write " - " before the bitstring
    f.write(" - " + bitstring + " | " + str(codes))
    f.close


    prev_frame = P_frame