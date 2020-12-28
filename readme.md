![perc3ption](/docs/perc_vision.png)


Perception tools to reveal the depth structure in 3-arrays. 

# Observer, Motion Control, Probes.  
During array visualization the observer can guide the camera view through a composition of motion key commands. The view is constraint to maximize understaning of the depth structure inside an observation volume. A probe can continously poll data from a file stream, even if the file producer is anaware of being observed. 

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

![perc3ption](/docs/archi.png)

## Roadamp
- [ ] visualization: loading mesh as observation volume
- [ ] tool: space renderer (cpu)
- [ ] probe: inter-process data sharing with uri 'mem://topic'
- [ ] transformer: basis alignment between reference and time-lapsed frames
- [ ] visualization: volume filling by penetration
- [ ] transformer: volume shaping by screen pixel picking
- [ ] visualization: point cloud transparency
- [ ] transformer: volume shaping by surface shifting
- [ ] probe: interactive data sharing with clipboard ('clip://topic')
- [ ] probe: interactive data sharing with screenshot, mouse ('screen://topic')
- [ ] gui: imgui options and menus for parametrization
- [ ] engine: graph architecture and graph editing
- [ ] visualization: x-ray vision
- [ ] tool: remote source polling
- [ ] visualization: theme library
- [ ] engine: configuration, asset, and state management
- [ ] engine: visual pattern recogntion trigges
- [ ] engine: layers and scriptable objects
- [ ] visualization: projection tooling (panini, 1, 2, 3 vanishing points)






