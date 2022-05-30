![perc3ption](/docs/perc_vision.png)
![perc3ption](/video1.gif)
# pc3 - perception stream debugger 
Tool to continuously reveal the hidden structure and failure modes in perception streams from 3d sensors or synthetically generated data. 

## Overview
3d vision sensors deployed in the field often require debugging or real-time inspection of failure modes. Generic point cloud visualizer are unsuitable for evaluating the contribution of individual input samples to failure modes.

This tool enables inspecting and deconstructing a stream and unlocks observability of the contributing factors of failure modes.  

![xray](https://user-images.githubusercontent.com/10095423/103164670-27641f80-47c3-11eb-93bc-e81bda8b871d.png)

## Features
* enhanced observation: microscoping zooming, projection range, guided motions
* batch or stream processing mode
* tolerant to choppy streams from remote devices
* fluid depth structure visualization
* stream playback: pause, step-by-step, slow-down

## Upcoming Features
* observation volumes to track event in regions of intereset  
* neural decoding for structure analysis / debugging

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

## Observation Volume
Load arbitrary mesh / volume shapes and observe changes or events that occur within it.  The volume representation loads into the pipeline as ModernGL GPU effect objects.

![perc3ption](/docs/pc3_stream.png)



[read more](./docs/architecture.md)


## Roadamp
Roadmap with lots of features.
[roadmap](/docs/roadmap.md)





