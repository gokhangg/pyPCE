import numpy as np


def GaussHermite(level):
    level = int(level)
    vect = np.sqrt(range(1, level), dtype = 'float')
    matrix = np.diag(vect, k = -1) + np.diag(vect, k = 1)
    w, v = np.linalg.eigh(matrix)
    nodes, indices = np.sort(w), np.argsort(w)
    if not level % 2 == 0:
        nodes[int((level - 1) / 2)] = 0
    return nodes, v[0, indices] ** 2