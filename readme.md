# Pathfinding Test

A simple pygame demo exemplifying real-time dynamic pathfinding within a randomly generated map.

### Overview

I wanted to do a simple game AI type project and figured this was as good a place as any to start. Rather than implement the usual A* search, I wanted to add a little bit more realism to my approach. First, line of sight to the player is detected by means of numpy's linear algebra library. If the player is visible, the enemy will chase them in a straight line. If not, the enemy will target the last known location of the player, and if they have already reached this location without finding the player, they will target a random point on the map.

Whenever line of sight with the player is broken, the enemies will refresh their weight grid (which they all share collectively). Starting from an NxN section of the map where the player was last seen, a breadth-first search is performed, incrementing every visited space to mark the distance from the target. Wandering enemies will use this grid to navigate around obstacles and find the shortest path to the target.

### Prerequisites

Python 3

Pygame

Numpy

### Installation

Navigate to the root directory and run:

```
pip install requirements.txt
```

### Running

In the same directory, run:

```
python main.py
```

### Bugs

Sometimes when there is only one obstacle between an enemy and the player, the obstacle is not caught by the line of sight algorithm, and the enemy proceeds to bump into it until the player emerges.

This implementation is very slow for large maps.

The obstacles are generated randomly, and have a slight chance of boxing you or an enemy in. If this happens, simply close the app and try again.