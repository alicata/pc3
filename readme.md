![perc3ption](/docs/perc_vision.png)

# pc3 - perception stream debugger 
Tool to continuously reveal the hidden structure and failure modes in perception streams of various nature, like semiconductor depth sensing captures, embedding vectors from computer vision neural networks, etc...

## Overview
Vision sensors deployed in the field often require debugging or real-time inspection of failure modes. Common visualization tools typically render a generic structure as point cloud. This approach is unsuitable for evaluating the contribution of individual input samples to failure modes.
The pc3 tool enables to deconstruct a stream and unlocks observability of the contributing factors of failure modes. The tool works also with sensor streams encoded into an embedding vector, like in neural representations from computer vision neural networks. 

![perc3ption](/docs/pc3_stream.png)

## Features
* neural decoding of image/sensor embedding vectors 
* batch or stream processing mode
* tolerant to choppy streams
* fluid depth structure visualization
* observation: microscoping zooming, projection range, guided motions
* stream playback: pause, step-by-step, slow-down
* file stream probe

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
| file stream with observetion volume | pc3 depth_file_stream.png obs_volume.obj |
| batch      | pc3 /data/testing/*.png |

Coming soon 
|  mode    | example | 
| ------------ | ------------ |
| socket stream   | pc3 localhost|
| neural decoding | pc3 network.h5 |

[read more](./docs/readme_pc3_gpu.md)

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

[read more](./docs/architecture.md)


## Roadamp
Roadmap with lots of features.
[roadmap](/docs/roadmap.md)





