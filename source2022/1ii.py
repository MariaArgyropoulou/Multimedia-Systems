import cv2
import numpy as np

def createMacroblocks(frame, size):
    width = frame.shape[1]
    newWidth = (width + size) - (width % size)
    height = frame.shape[0]
    newHeight = (height + size) - (height % size)
    defference = ((0, newHeight - height), (0, newWidth - width), (0, 0))
    newFrame = np.pad(frame, defference, mode='constant')

    macroblocks = []
    for newHeight_ in range(0, newHeight - size, size):
        row = []
        for newWidth_ in range(0, newWidth - size, size):
            macroblock = newFrame[newHeight_:newHeight_ + size, newWidth_:newWidth_ + size]
            row.append(macroblock)
        macroblocks.append(row)

    return np.array(macroblocks)


# def encoder():
# def decoder():
def macroblock_difference(macroblocks, prev_macroblock):
    macroblock_diff = []
    for i in range(len(macroblocks)):
        for j in range(len(macroblocks[i])):
            macroblock_diff = (macroblocks[i][j]-prev_macroblock[i][j])

            x, y = macroblock_diff.shape
            zeros = x*y - np.count_nonzero(macroblock_diff)

    if zeros >= 0.8*x*y:
        return
    else:
        return macroblock_diff

# Φορτώνουμε το βίντεο για επεξεργασία
video = cv2.VideoCapture('walk.mp4')
counter = 0
frameslist = []
# Αποθηκεύουμε μια λίστα με ολα τα πλαίσια

first=[]
prev_macroblocks = []
macroblocks = []

# First frame is the I-frame
ret, frame = video.read()
first.append(frame)
prev_macroblocks.append(createMacroblocks(frame, 32))


while video.isOpened():
    ret, frame = video.read()

    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        counter += 1
        frameslist.append(frame)

        macroblocks.append(createMacroblocks(frame, 32))
        #print(macroblocks)

        macroblock_difference(macroblocks,prev_macroblocks)
        prev_macroblocks=macroblocks
    else:
        break
video.release()
#frames = np.array(frames)
# Διαιρούμε όλα τα frames σε macroblocks μεγέθους 32x32
#macroblocks = []
#for i in range(len(frameslist)):
  #  macroblocks.append(createMacroblocks(frameslist[i], 32))
 #   np.array(macroblocks)

#print(macroblocks)