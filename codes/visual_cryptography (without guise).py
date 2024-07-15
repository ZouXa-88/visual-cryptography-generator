import random
import sys
import cv2
import numpy


def blackNum(pattern_1, pattern_2) -> int:
    count = 0
    for i in range(4):
        if pattern_1[i] or pattern_2[i]:
            count += 1

    return count


def writePixel(i, j, img, share):
    img[i * 2, j * 2] = (not share[0]) * 255
    img[i * 2, j * 2 + 1] = (not share[1]) * 255
    img[i * 2 + 1, j * 2] = (not share[2]) * 255
    img[i * 2 + 1, j * 2 + 1] = (not share[3]) * 255


def stack(i, j, share_1, share_2, stacked):
    stacked[i * 2, j * 2] = (not(share_1[0] or share_2[0])) * 255
    stacked[i * 2, j * 2 + 1] = (not(share_1[1] or share_2[1])) * 255
    stacked[i * 2 + 1, j * 2] = (not(share_1[2] or share_2[2])) * 255
    stacked[i * 2 + 1, j * 2 + 1] = (not(share_1[3] or share_2[3])) * 255


def main():
    if len(sys.argv) != 3:
        return

    try:
        white_shares = [[1, 1, 0, 0], [0, 0, 1, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 0, 1], [0, 1, 1, 0]]
        size = int(sys.argv[1])
        cv2.black = 0
        
        # read images
        secret = cv2.imread(sys.argv[2], cv2.IMREAD_GRAYSCALE)

        # threshold
        ret, secret = cv2.threshold(secret, 127, 255, cv2.THRESH_BINARY)

        # generate fake images
        fakeImg_1 = numpy.zeros((size * 2, size * 2), dtype=numpy.uint8)
        fakeImg_2 = numpy.zeros((size * 2, size * 2), dtype=numpy.uint8)
        realImg = numpy.zeros((size * 2, size * 2), dtype=numpy.uint8)
        
        for i in range(size):
            for j in range(size):
                share_1, share_2 = [], []

                # pick share1
                share_1 = random.choice(white_shares)

                # pick share2
                while (not share_2) or \
                        ((secret[i, j] == cv2.black) and (blackNum(share_1, share_2) != 4)) or \
                        ((secret[i, j] != cv2.black) and (blackNum(share_1, share_2) != 3)):
                    share_2 = random.choice(white_shares)

                # write
                writePixel(i, j, fakeImg_1, share_1)
                writePixel(i, j, fakeImg_2, share_2)
                stack(i, j, share_1, share_2, realImg)

        # show
        cv2.imshow("fakeImg_1", fakeImg_1)
        cv2.imshow("fakeImg_2", fakeImg_2)
        cv2.imshow("realImg", realImg)
        cv2.imwrite("fakeImg_1.png", fakeImg_1)
        cv2.imwrite("fakeImg_2.png", fakeImg_2)
        cv2.imwrite("realImg.png", realImg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
