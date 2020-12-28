import cv2
import sys
import numpy as np


def loop(data, file):
    s = data['scale']
    try:
        i = cv2.imread(file);
        h, w = i.shape[0:2]
        i = cv2.resize(i, (w*s, h*s), interpolation=cv2.INTER_NEAREST)
        cv2.imshow(file, i);
        key = cv2.waitKey(100)

        if key == ord('s'):
            data['scale'] = ((data['scale'] + 1) % 4) + 1

        if key == ord('q'):
            exit(0)


    except Exception as e:
        err = str(e)
        pass


def main():
    data = {'scale' : 2}
    file = sys.argv[1]
    while True:
        loop(data, file)

main()
     