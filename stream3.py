"""capture app to record and playback depth stream.

    cfg inputs,
    command: mode, action:
        - mode  : bag or png
        - action: record or playback

    example usage: python capture record data/frame*.png

"""
import pyrealsense2 as rs
import cv2
import numpy as np
import time
import glob
import collections
import os
import sys


try:
    cmd = sys.argv[1]
    cfg['recording_file'] = sys.argv[2]
except:
    print('usage: capture [record|playback] [bag filepath|png folder]')
    print('example: python capture record data/frame*.png')
    exit(0)

cfg = {}
cfg['recording_file'] = 'tmp/test*.png'
cfg['max_duration'] = 8 
cfg['fps'] = 15

mode = os.path.splitext(cfg['recording_file'])[1].split('.')[1]

if cmd in ['record']:
    os.makedirs(os.path.dirname(cfg['recording_file']), exist_ok=True)

pipeline = rs.pipeline()
config = rs.config()

mode_setter = collections.defaultdict(lambda : {}) 
mode_setter['bag']['record']   = lambda f : config.enable_record_to_file(f) 
mode_setter['bag']['playback'] = lambda f : config.enable_device_from_file(file_name=f) 
mode_setter['png']['record']   = lambda f : None 
mode_setter['png']['playback']   = lambda f : None 

mode_setter[mode][cmd](cfg['recording_file'])
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, cfg['fps'])

to_numpy = lambda x : None if ( x is None) else np.asanyarray(x.get_data())

print('starting ' + cmd + ' ' + mode)
files = glob.glob(cfg['recording_file'])
if (cmd in ['playback'] and mode in ['png']) is False:
    pipeline.start(config)

time.sleep(0.1)
start = time.time()
frame_no = 0

try:
    while (time.time() - start) < cfg['max_duration']:

        if (cmd in ['playback'] and mode in ['png']) is False:
            frames = pipeline.wait_for_frames()
            np_array = to_numpy(frames.get_depth_frame())
        else:
            try:
                file = files[frame_no]
                print(file)
                np_array = cv2.imread(file)
                frame_no += 1
            except:
                break
          
        if np_array is not None:
            if cmd in ['playback']:
                cv2.imshow('playback ' + mode, np_array)
                cv2.waitKey(33)

            if mode in ['png'] and cmd in ['record']:
                filepath = 'test' + str(time.time()) + '.png' 
                print(filepath)
                cv2.imwrite(filepath, np_array, [cv2.IMWRITE_PNG_COMPRESSION, 0])
            
        time.sleep(1.0/cfg['fps'])

finally:
    try:
        pipeline.stop()
    except:
        print("completed.")
