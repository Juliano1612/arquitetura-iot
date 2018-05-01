# arquitetura-iot

dependencies:
- networkx
- matplotlib
- python-tk

Installing dependencies

``` python -m pip install networkx matplotlib && apt-get install python-tk ```

Running scenaGen

``` python scenaGen.py scenarioId X Y  ```

- X = number of messages
- Y = number of nodes

Running node

```python node.py nodeId nodeGroup networkId scenarioId nrouteTable ```

Running simple-p2p

``` python network.py networkId scenarioId ```
- *the ids need to be the same of the file in the respective folders

Running stats

``` python stats.py simulationType networkId scenarioId ```
- simulationType = simple-p2p || cache-node || cache-group