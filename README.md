# WSN Simulator
A wireless sensor network simulator is software for conducting simulation processes that use different routing methods and optimization techniques with real-time device status display. 
## Routing protocols
This software supports four different routing schemes:
- Direct Communication. In this mode, each node sends information directly to the base station.
- MTE. Each node sends information through other nodes along the shortest path to the base station, which is calculated by Dijkstra's algorithm.
- LEACH. Based on the probability calculated for each node, the head nodes are selected, which collect and aggregate information from the nodes closest to them.
- Fuzzy C-Means. Fuzzy clustering technique, which distributes all of the devices in the network in the optimal amount of clusters. The head node in this scheme is selected depending on the residual energy and location relative to the base station.
## Sleep scheduling system
For each routing scheme, a sleep scheduling system based on the particle swarm method is provided, which allows some nodes in the network to periodically move to sleep. The calculation is based on the given fitness function and energy values, coordinates and other device parameters.
## Requirements
- Python 3.8
### Libraries
- knead
- matplotlib
- numpy
- scikit-learn
- pyswarms
- tkinter
- scikit-fuzzy
- dijkstar
## Install and Run
### Linux Operating Systems
Install

```bash
. ./install.sh
```

Run

```bash
./run.sh
```

