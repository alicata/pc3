![perc3ption](/docs/perc_vision.png)


Perception tool to continuously reveal the hidden structure and failure modes in streams of depth sensing or procedurally generated 3d data. 

## Overview
Vision sensors deployed in the field or live experiments often require debugging or real-time inspection of failure modes. Typical visualizers are designed for offline datasets, simple localy connected device and observed as a generic blob (i.e point cloud), and ineffective tools to evaluate the contribution of individual samples to failure modes.
This tool enables to deconstruct a stream and narrow down the contributing factors to failure modes. The tool works also with sensor streams encoded into an embedding vector, like in neural representations from vision networks.

## Use cases 
* stream visualization at multiple scales
* inspection of sensing failures
* debugging neural image embeddings
* continuous observation of unreliable or laggy streams


## Features
* batch or stream processing mode
* tolerant to choppy streams
* fluid depth structure visualiation
* observation: zooming, projection range, guided motions
* playback: pause, step-by-step, slow-down
* file stream probe
* neural decoding of image/sensor embedding vectors 

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
pc3 <stream source uri>
```

|  mode    | example | 
| ------------ | ------------ |
| file stream     | pc3 depth_file_stream.png |
| socket stream   | pc3 localhost|
| batch      | pc3 /data/testing/*.png |

[read more](./docs/readme_gpu.md)

## Perception-Enhancing Utilities
| tool      | description  | 
| ------------ | ------------ |
| pc3              | engine to induce depth perception from 3-array data |
| utils        | tool with various depth, mesh, embedding processing utilities (normals, viewer, etc..) |
| space_editor | mapping of spaces to meters, etc.. |


# Architecture
pc3 adopts a fault tolerant stream based processing architecture, where streams are continously and immedialy produced as file stream (local or distributed), and shared memory buffers from different sources in the local computing node. The engine contisouly process the stream, and coordinates interaction with the user interface. 

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
Roadmap with lots of features.
[roadmap](/docs/roadmap.md)





