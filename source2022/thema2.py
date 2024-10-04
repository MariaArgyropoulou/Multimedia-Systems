import numpy as np
import cv2

def createMacroblocks(frame, size=16):

    # Υπολογίζουμε νεο πλάτος και υψος για να διαιρειτε σε μπλοκ 16*16
    width = frame.shape[0]
    newWidth = (width + size) - (width % size)
    height = frame.shape[1]
    newHeight = (height + size) - (height % size )
    defference = ((0, newWidth - width), (0, newHeight - height) , (0, 0))
    newFrame = np.pad(frame, defference, mode='constant')

    # Δημιουργούμε τα macroblock
    macroblocks = []
    for newWidth_ in range(0, newWidth - size, size):
        row = []
        for newHeight_ in range(0, newHeight - size, size):
            macroblock = newFrame[newWidth_:newWidth_ + size, newHeight_:newHeight_ + size]
            row.append(macroblock)
        macroblocks.append(row)

    return macroblocks


def restoreFrame(macroblocks):
    # Εννόνουμε τα macroblocks για κάθε γραμμή και επιστρέφουμε το καινούργιο πλαίσιο
    rows = []
    for row in macroblocks:
        rows.append(np.concatenate([macroblock for macroblock in row], axis=1))

    frame = np.concatenate([row for row in rows], axis=0)
    return frame

# Φορτώνουμε το βίντεο για επεξεργασία
video = cv2.VideoCapture('walk.mp4')
flag = False
previous= None
counter = 0

while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break

    #Φτιάχνουμε macroblocks μεγέθους 16*16
    Macroblock = createMacroblocks(frame)

    # Εξερούμε το πρωτο πλαισιο.
    if not flag:
        flag = True
        previous = Macroblock
        continue

    # Αντικαθηστούμε τα macroblcoks ωστε να εξαφανισουμε το αντικείμενο.
    for i in range(1, 22):
        Macroblock[i] = previous[i]


    newFrame = restoreFrame(Macroblock)
    frameSize = ( newFrame.shape[1],newFrame.shape[0])

    if counter==0:
        out = cv2.VideoWriter('trim_video.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, frameSize)
        counter+=1
    else:
        out.write(newFrame)

    cv2.imshow('Original', frame)
    cv2.imshow('Trimmed video', newFrame)

    # Αποθηκέυουμε το προηγούμενο macroblock
    previous = Macroblock
    cv2.waitKey(25)

video.release()
out.release()
cv2.destroyAllWindows()

