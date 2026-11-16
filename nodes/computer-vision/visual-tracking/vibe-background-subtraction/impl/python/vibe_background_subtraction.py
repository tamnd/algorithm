# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vibe-background-subtraction/. The authors are listed in prov/2FRG4D.jsonl.
"""ViBe, the visual background extractor (Barnich and Van Droogenbroeck 2011), gray values.

Each pixel keeps N past sample values. A value v is background if at least
min_matches samples s have |v - s| < R. A background pixel then, with
probability 1 / phi, replaces one of its own samples chosen at random by v,
and, with probability 1 / phi, replaces a random sample of a random
8-connected neighbor by v. Foreground pixels update nothing (a conservative
update). The model starts from one frame: each sample is the value of a
random pixel of the 3 by 3 neighborhood.

This file classifies the whole frame first and then updates, so the result of
a frame does not depend on the order in which the pixels are visited.
An image is a list of rows of gray values. Cost per frame: O(P N) for P pixels.
"""

import random

NEIGHBORS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


class ViBe:
    def __init__(self, first_frame, n=20, radius=20, min_matches=2, phi=16, seed=0):
        self.n = n
        self.radius = radius
        self.min_matches = min_matches
        self.phi = phi
        self.rng = random.Random(seed)
        self.h = len(first_frame)
        self.w = len(first_frame[0])
        self.samples = [[self._init_samples(first_frame, y, x) for x in range(self.w)] for y in range(self.h)]

    def _init_samples(self, img, y, x):
        out = []
        for _ in range(self.n):  # @line L1
            dy, dx = self.rng.choice([(0, 0)] + NEIGHBORS)
            yy = min(max(y + dy, 0), self.h - 1)
            xx = min(max(x + dx, 0), self.w - 1)
            out.append(img[yy][xx])
        return out

    def is_background(self, v, samples):
        count = 0
        for s in samples:  # @line L2
            if abs(v - s) < self.radius:
                count += 1
                if count >= self.min_matches:
                    return True
        return False

    def neighbors(self, y, x):
        return [(y + dy, x + dx) for dy, dx in NEIGHBORS if 0 <= y + dy < self.h and 0 <= x + dx < self.w]

    def apply(self, frame):
        """Returns the foreground mask of the frame (1 = foreground) and updates the model."""
        mask = [[0 if self.is_background(frame[y][x], self.samples[y][x]) else 1  # @line L3
                 for x in range(self.w)] for y in range(self.h)]
        rng = self.rng
        for y in range(self.h):
            for x in range(self.w):
                if mask[y][x]:
                    continue  # @line L4
                v = frame[y][x]
                if rng.randrange(self.phi) == 0:  # @line L5
                    self.samples[y][x][rng.randrange(self.n)] = v
                if rng.randrange(self.phi) == 0:  # @line L6
                    nb = self.neighbors(y, x)
                    if nb:
                        yy, xx = rng.choice(nb)
                        self.samples[yy][xx][rng.randrange(self.n)] = v
        return mask
