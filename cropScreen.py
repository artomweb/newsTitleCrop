import cv2
import pytesseract


def crop(FILENAME, name, WORDFIND):
    SPACEY = 250
    SPACEX = int(SPACEY * (1920/1080))

    try:

        img = cv2.imread(FILENAME)
        imgOriginal = img.copy()
        imgDraw = img.copy()

        # img = img[550:1000, 400:2400]  # BBC
        img = img[550:1200, 800:2200]  # DailyMail

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Performing OTSU threshold
        ret, thresh1 = cv2.threshold(
            gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

        # Specify structure shape and kernel size.
        # Kernel size increases or decreases the area
        # of the rectangle to be detected.
        # A smaller value like (10, 10) will detect
        # each word instead of a sentence.
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 2))

        # Applying dilation on the threshold image
        dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

        # Finding contours
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_NONE)

        for i, c in enumerate(contours):
            x, y, w, h = cv2.boundingRect(c)
            x += 800
            y += 550

            if w > 100:

                cv2.rectangle(imgDraw, (x, y), (x + w,
                                                y + h), (36, 255, 12), 3)
            ROI = imgOriginal[y:y+h, x:x+w]
            cv2.imwrite("proc/ " + str(i) + ".jpg", ROI)
            txt = pytesseract.image_to_string(ROI, config="--psm 6")
            if txt.lower().strip() == WORDFIND:
                # print("found word", WORDFIND)

                imageCropped = imgOriginal[y - SPACEY:y +
                                           h + SPACEY, x - SPACEX:x+w + SPACEX]
                cv2.imwrite(f"output/{name}.png", imageCropped)
                color_coverted = cv2.cvtColor(imageCropped, cv2.COLOR_BGR2RGB)
                return [True, color_coverted]

        print("no cont")
        return [False, dilation]
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print("ERROR:", e)
        return [False, dilation]
