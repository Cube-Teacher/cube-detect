import cv2 as cv
import numpy as np
import math

if __name__ == "__main__":

    cam = cv.VideoCapture(0)
    while(1):
        _, img = cam.read()
        originImg = img
        img = cv.GaussianBlur(originImg, (5, 5), 0)

        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # cv.imwrite(image_blur, img)
        # img = blur image

        cannyimg = cv.Canny(img, 100, 200)
        ret, thresh1 = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
        thresh2 = cv.adaptiveThreshold(
            img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
        # cannyimg: canny
        # thresh1 : thresholding
        # thresh2 : adaptive threasholding

        kernel = np.ones((3, 3), np.uint8)
        cannyimg = cv.dilate(cannyimg, kernel, iterations=1)
        kernel = np.ones((5, 5), np.uint8)
        thresh2 = cv.dilate(thresh2, kernel, iterations=1)

        # contour, hierarchy = cv.findContours(thresh2, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        cannyContour, hierarchy = cv.findContours(
            cannyimg, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        cannyContourExternal, hierarchy = cv.findContours(
            cannyimg, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        thresoldContour, hierarchy = cv.findContours(
            thresh2, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        thresoldContourExternal, hierarchy = cv.findContours(
            thresh2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        # cannyimg = cv.cvtColor(cannyimg, cv.COLOR_GRAY2BGR)
        # thresh2 = cv.cvtColor(thresh2, cv.COLOR_GRAY2BGR)
        thresh1 = thresh2
        cannyimg2 = cannyimg

        for pic, contour in enumerate(cannyContourExternal):
            area = cv.contourArea(contour)
            if(area > 200):
                # print("counter num:",len(contour))
                epsilon = 0.1*cv.arcLength(contour, True)
                approx = cv.approxPolyDP(contour, epsilon, True)
                # box = cv.minAreaRect(contour)
                # box = np.int0(cv.boxPoints(box))
                # cv.drawContours(cannyimg2, [box], -1, (0, 255, 0), 2)
                if(len(approx) == 4):
                    a = []
                    dis = []
                    for tmp in approx:
                        a.append(tmp[0][0])
                        a.append(tmp[0][1])
                    sidelen = []
                    sideangle = []
                    for tmp in dis:
                        print(tmp)

                    for j in range(0, 4):
                        if j == 3:
                            k = 0
                        else:
                            k = 1+j
                        print(a[k*2], a[j*2], a[k*2+1], a[j*2+1],
                              np.sqrt(pow(abs(a[k*2]-a[j*2]), 2)+pow(abs(a[k*2+1]-a[j*2+1]), 2)))
                        sidelen.append(
                            np.sqrt(pow(abs(a[k*2]-a[j*2]), 2)+pow(abs(a[k*2+1]-a[j*2+1]), 2)))
                    flag = 1
                    print()

                    maxlen = max(sidelen)
                    minlen = min(sidelen)

                    sidelen.append(
                        np.sqrt(pow(abs(a[2]-a[6]), 2)+pow(abs(a[3]-a[7]), 2)))

                    sidelen.append(
                        np.sqrt(pow(abs(a[0]-a[4]), 2)+pow(abs(a[1]-a[5]), 2)))

                    sideangle.append(math.degrees(np.arccos(
                        (sidelen[0]**2+sidelen[3]**2-sidelen[4]**2)/(2*sidelen[0]*sidelen[3]))))
                    sideangle.append(math.degrees(np.arccos(
                        (sidelen[0]**2+sidelen[1]**2-sidelen[5]**2)/(2*sidelen[0]*sidelen[1]))))
                    sideangle.append(math.degrees(np.arccos(
                        (sidelen[1]**2+sidelen[2]**2-sidelen[4]**2)/(2*sidelen[1]*sidelen[2]))))
                    sideangle.append(math.degrees(np.arccos(
                        (sidelen[2]**2+sidelen[3]**2-sidelen[5]**2)/(2*sidelen[2]*sidelen[3]))))

                    # print(np.arccos(sideangle[0]))
                    # print(maxlen,minlen)
                    # print( )

                    for tmp in sideangle:
                        print(tmp)

                    maxangle = max(sideangle)
                    minangle = min(sideangle)
                    print(maxangle, " ", minangle)

                    if(maxlen-minlen > 5 or maxangle > 93 or minangle < 87):
                        flag = 0
                    if(flag):
                        cv.drawContours(
                            originImg, [approx], -1, (0, 255, 0), 2)
                # x, y, w, h = cv.boundingRect(contour)
                # imageFrame = cv.rectangle(
                #     cannyimg2, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # cv.imwrite(Cannycontour, cannyimg)
        # cv.imwrite(ContourExternal, cannyimg2)
        # cv.imwrite(Thresoldcontour, thresh1)
        # cv.imwrite(ThresoldcontourExternal, thresh2)
        cv.imshow("frame", originImg)
        if cv.waitKey(10) & 0xFF == ord('q'):
            cam.release()
            cv.destroyAllWindows()
            break
