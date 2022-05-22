![perc3ption](/docs/perc_vision.png)


Perception tool to reveal the depth structure in streams generated from 2d and 3d sensors. 

# Observer, Motion Control, Probes.  
The stream observer can guide the camera view through a composition of motion key commands. The view is constraint to maximize understaning of the depth structure inside an observation volume. A probe can continously poll data from a file stream, even if the file stream producer is anaware of being observed. 

## Features
* fluid depth structure visualiation
* observation: zooming, projection range, guided motions
* playback: pause, step-by-step, slow-down
* file stream probe


## Usage:
```
pc3 /hardware/datastream/*.png`
```
[read more](./docs/readme_pc3_gpu.md)

## Perception-Enhancing Utilities
| utility      | description  | 
| ------------ | ------------ |
| pc3              | induce depth perception from 3-array data |
| pc3_utils        | various depth and mesh processing utilities (normals, viewer, etc..) |
| pc3_space_editor | mapping of spaces to meters, etc.. |


# Architecture
pc3 adopts a stream based processing architecture, where streams are continously and immedialy produced as file stream (local or distributed), and shared memory buffers from different sources in the local computing node. The engine contisouly process the stream, and coordinates interaction with the user interface. 

## Obs Volume
System to load and observe arbitrary mesh representations into the pipeline as Effect objects

![xray](https://user-images.githubusercontent.com/10095423/103164670-27641f80-47c3-11eb-93bc-e81bda8b871d.png)
## Obs sub-systems
* mesh loading
* resource effects: rendering programs as resources
* effects selection
*  xray layer
* zoning

- [ ] frame transformation: from loaded object space to world space (256x256x256)
- [ ] xray blending as layer shared across effects and graph nodes
- [x] theme: add 'dark-to-bright' dark gray-to-white color mapping theme


# Diversified-Integrity: Frustrum, Space, CFs, Graph Tools
Enable diverse coexistence with CPU, GPU, inter-network, inter-process parts

- [ ] cpu rendering
- [ ] perspective generator
- [ ] cf: coordinate frame selector
- [ ] data source polling
- [ ] config editor
- [ ] graph editor


# Engine Graph 

![engine_graph2](https://user-images.githubusercontent.com/10095423/103165031-8c217900-47c7-11eb-8c2f-4d4f42ed0431.jpg)

- [ ] graph pipeline composition
- [ ] graph visualization (pyflow)
- [ ] config and state machine management


## Coordinate Frames
- [ ] CFs facilitation


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
- [ ] visualization: light probe
- [ ] visualization: reflection probe
- [ ] visualization: depth probe
- [ ] visualization: occlusion detection
- [ ] automaton: event trigger
- [ ] engine: graph architecture and graph editing
- [ ] visualization: x-ray vision
- [ ] tool: remote source polling
- [ ] visualization: theme library
- [ ] engine: configuration, asset, and state management
- [ ] engine: visual pattern recogntion trigges
- [ ] engine: layers and scriptable objects
- [ ] visualization: projection tooling (panini, 1, 2, 3 vanishing points)






