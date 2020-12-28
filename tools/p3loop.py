import cv2
import sys
import numpy as np


def loop(data, file):
    s = data['scale']
    try:
        i = cv2.imread(file);
        h, w = i.shape[0:2]
        i = cv2.resize(i, (w*s, h*s), interpolation=cv2.INTER_NEAREST)

        #1
        p0, p1 = (0*s, 75*s), ((w-1)*s, 47*s)
        cv2.line(i, p0, p1, (0,0,255))
        p0, p1 = (0*s, 82*s), ((w-1)*s, 55*s)
        cv2.line(i, p0, p1, (0,205,255))

        #2
        p0, p1 = (0*s, 67*s), ((w-1)*s, 86*s)
        cv2.line(i, p0, p1, (0,205,255))
        p0, p1 = (0*s, 63*s), ((w-1)*s, 82*s)
        cv2.line(i, p0, p1, (0,0,255))
 
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
     