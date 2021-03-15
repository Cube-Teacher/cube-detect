import cv2 as cv
import numpy as np

if __name__ == "__main__":

    cam = cv.VideoCapture(0)
    while(1):
        _,img = cam.read()
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
        kernel = np.ones((3, 3), np.uint8)
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

        cannyimg = cv.cvtColor(cannyimg, cv.COLOR_GRAY2BGR)
        thresh2 = cv.cvtColor(thresh2, cv.COLOR_GRAY2BGR)
        thresh1 = thresh2
        cannyimg2 = cannyimg

        for pic, contour in enumerate(cannyContourExternal):
            area = cv.contourArea(contour)
            if(area > 1000):
                box = cv.minAreaRect(contour)
                box = np.int0(cv.boxPoints(box)) 
                cv.drawContours(originImg, [box], -1, (0, 255, 0), 2)
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
