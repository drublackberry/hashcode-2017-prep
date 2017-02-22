#!/usr/bin/env python

"""
Help with rules for pizza slicing.
"""

import numpy as np


QUADRANT_VEC = {'ur': [-1, +1],
                'ul': [-1, -1],
                'll': [+1, -1],
                'lr': [+1, +1],
                }


def get_valid_rects(min_cells, max_cells):
    """
    Create array of valid [height, width] combinations.
    """

    rects = []
    for height in range(1, max_cells + 1):
        for width in range(1, height):
            cells = height * width
            if (min_cells <= cells) and (cells <= max_cells):
                rects.append((height, width))
    rects += [(width, height) for (height, width) in rects]
    return np.asarray(rects)


def append_to_vertex(vert, rects, quadrant):
    """
    Returns new vertices for opposing corners.
    """
    vert2 = vert + QUADRANT_VEC[quadrant] * rects
    return vert2


def regularize_vertices(vert1, vert2):
    """
    Given arrays of origin and end vertices, makes sure that
    origin coordinates are smaller than end coordinates.
    """

    for i, (v1, v2) in enumerate(zip(vert1, vert2)):
        for j in 0, 1:
            if v2[j] < v1[j]:
                vert1[i, j], vert2[i, j] = v2[j], v1[j]


if __name__ == "__main__":
    rects = get_valid_rects(12, 14)
    #print(rects)
    v0 = 500 * np.ones([len(rects), 2], dtype=np.int32)
    added = append_to_vertex(v0, rects, 'll')
    print(added)
    regularize_vertices(v0, added)
    print(v0)
    print(added)
