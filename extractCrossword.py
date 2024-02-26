import numpy as np
import cv2

crossword_size = 13 # Set to dimension of crossword (standard 15 x 15)

# 1. Loading the Image
img = cv2.imread('Crossword\image1.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # 2. Grayscale conversion

# 3. Thresholding
ret, thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV) 
thresh2 = cv2.bitwise_not(thresh)

# 4. Finding Countours
contours,hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, 1)

max_area = -1

# 4. Finding Countours
for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt,True), True)
    if len(approx) == 4:
        if cv2.contourArea(cnt) > max_area:
            max_area = cv2.contourArea(cnt)
            max_cnt = cnt
            max_approx = approx

# 5. Identifying crossword region
x,y,w,h = cv2.boundingRect(max_cnt)
cross_rect = thresh2[y:y+h, x:x+w]
cross_rect = cv2.resize(cross_rect,(crossword_size*10,crossword_size*10)) # 6. Resizing


cross = np.zeros((crossword_size,crossword_size))

# 7. Creating Binary Matrix
for i in range(crossword_size):
    for j in range(crossword_size):
        box = cross_rect[i*10:(i+1)*10, j*10:(j+1)*10]
        if cv2.countNonZero(box) > 50:
            cross.itemset((i,j),1)

            

np.savetxt('crossword_binary_matrix.txt', cross, fmt='%d')

print(cross)



