# pc3
Perception tools to reveal the depth structure in 3-arrays. 

# Observation Approach - Observer, Motion Control, Probes.  
During array visualization the observer can guide the camera view through a composition of motion key commands. The view is constraint to maximize understaning of the depth structure inside an observation volume. A probe can continously poll data from a file stream, even if the file producer is anaware of being observed. 

![perc3ption](/docs/archi.png)


## Features
* fluid depth structure visualiation
* observation: zooming, projection range, guided motions
* playback: pause, step-by-step, slow-down
* file stream probe


## Usage:
```
pc3 /data/*.png`
```
[read more](./docs/readme_pc3_gpu.md)

## Perception-Enhencing Utilities
| utility      | description  | 
| ------------ | ------------ |
| pc3     | induce depth perception from 3-array data |
| pc3 map | mapping of spaces to meters, etc.. |

## Roadamp
- [ ] probe: inter-process data sharing with uri 'mem://topic'
- [ ] visualization: loading mesh as observation volume
- [ ] transformer: basis alignment between reference and time-lapsed frames
- [ ] visualization: volume filling by penetration
- [ ] transformer: volume shaping by screen pixel picking
- [ ] visualization: point cloud transparency
- [ ] transformer: volume shaping by surface shifting
- [ ] probe: interactive data sharing with clipboard ('clip://topic')
- [ ] probe: interactive data sharing with screenshot, mouse ('screen://topic')



