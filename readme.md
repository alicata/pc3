![perc3ption](/docs/perc_vision.png)


Perception tool to reveal the hidden structure in high-dimensional streams from depth maps, neural encoding vectors, or other vectorized representations. 

## Use cases 
* depth stream visualization
* inspection of sensing failures 
* debugging neural representations

## Features
* fluid depth structure visualiation
* observation: zooming, projection range, guided motions
* playback: pause, step-by-step, slow-down
* file stream probe
* neural decoding of image embedding vectors 

## Setup
Run installation script,

Windows 10/11
```
install.cmd
```

Linux - cooming soon
```
install.sh
```


## Usage:
```
pc3 data/*.png
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

## Concepts: Observer, Motion Control, Probes  
The stream observer can guide the camera view through a composition of motion key commands. The view is constraint to maximize understaning of the depth structure inside an observation volume. A probe can continously poll data from a file stream, even if the file stream producer is anaware of being observed. 

## Obs Volume
System to load and observe arbitrary mesh representations into the pipeline as Effect objects

![xray](https://user-images.githubusercontent.com/10095423/103164670-27641f80-47c3-11eb-93bc-e81bda8b871d.png)
## Obs sub-systems
* mesh loading
* resource effects: rendering programs as resources
* effects selection
*  xray layer
* zoning

In-Progress:
- [ ] frame transformation: from loaded object space to world space (256x256x256)
- [ ] xray blending as layer shared across effects and graph nodes
- [x] theme: add 'dark-to-bright' dark gray-to-white color mapping theme


## Roadamp
Very rich roadmap with lots of features.
![perc3ption](/docs/roadmap.rd)





