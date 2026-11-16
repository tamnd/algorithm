# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/photometric-stereo/. The authors are listed in prov/QKJF6P.jsonl.

"""Lambertian photometric stereo with known distant lights (Woodham).

Vectors are in the height-field frame: x right, y in the image plane, z toward
the viewer. Image k has a light s_k (a 3-vector whose length is the light
strength), and a Lambertian point with albedo rho and unit normal n has the
brightness I_k = max(0, rho n . s_k). The unknown per pixel is g = rho n.
Images are lists of rows, img[v][u].
"""

import math


def solve3(M, b):
    """Solve the 3 x 3 system M x = b by Gaussian elimination with partial pivoting.
    Returns None if M is singular (relative to its size)."""
    A = [list(M[r]) + [b[r]] for r in range(3)]
    scale = max(abs(A[r][c]) for r in range(3) for c in range(3))
    if scale == 0.0:
        return None
    for c in range(3):
        piv = max(range(c, 3), key=lambda r: abs(A[r][c]))
        if abs(A[piv][c]) <= 1e-12 * scale:
            return None
        A[c], A[piv] = A[piv], A[c]
        for r in range(c + 1, 3):
            m = A[r][c] / A[c][c]
            for k in range(c, 4):
                A[r][k] -= m * A[c][k]
    x = [0.0, 0.0, 0.0]
    for r in (2, 1, 0):
        x[r] = (A[r][3] - sum(A[r][k] * x[k] for k in range(r + 1, 3))) / A[r][r]
    return x


def photometric_stereo(images, lights, threshold=0.0):
    """Per pixel least squares for g = rho n. Readings with I <= threshold are
    treated as shadow and dropped. Returns (albedo, normals) as images; a pixel
    with fewer than three usable readings, or with lights that do not span 3D,
    gets None in both."""
    height, width = len(images[0]), len(images[0][0])
    albedo = [[None] * width for _ in range(height)]
    normals = [[None] * width for _ in range(height)]
    for v in range(height):  # @line L1
        for u in range(width):
            use = [k for k in range(len(images)) if images[k][v][u] > threshold]  # @line L2
            if len(use) < 3:  # @line L3
                continue
            M = [[sum(lights[k][r] * lights[k][c] for k in use) for c in range(3)] for r in range(3)]  # @line L4
            b = [sum(images[k][v][u] * lights[k][r] for k in use) for r in range(3)]
            g = solve3(M, b)  # @line L5
            if g is None:
                continue
            rho = math.sqrt(g[0] ** 2 + g[1] ** 2 + g[2] ** 2)  # @line L6
            if rho == 0.0:
                continue
            albedo[v][u] = rho
            normals[v][u] = [g[0] / rho, g[1] / rho, g[2] / rho]
    return albedo, normals  # @line L7


def render(albedo, normals, lights):
    """Lambertian images with attached shadows: I = max(0, rho n . s)."""
    images = []
    for s in lights:
        img = []
        for arow, nrow in zip(albedo, normals):
            img.append([max(0.0, a * (n[0] * s[0] + n[1] * s[1] + n[2] * s[2]))
                        for a, n in zip(arow, nrow)])
        images.append(img)
    return images


def gradients(normal):
    """Surface slopes p = dz/dx and q = dz/dy from a normal (-p, -q, 1) / |.|."""
    nx, ny, nz = normal
    return -nx / nz, -ny / nz
