import numpy as np

def distance(x1, y1, x2, y2):
    v1 = np.array((x1, y1))
    v2 = np.array((x2, y2))
    dist = np.sqrt(np.sum((v1 - v2) ** 2))
    return dist