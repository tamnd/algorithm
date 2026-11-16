# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shape-from-focus/. The authors are listed in prov/09NTD3.jsonl.

"""Shape from focus with the sum-modified-Laplacian (Nayar and Nakagawa).

A focal stack is a list of N gray images img[v][u] taken at focus positions
d_0 + k * delta for k = 0..N-1. For each pixel the method picks the frame with
the largest focus measure and refines the position with a Gaussian fit to the
measure at the best frame and its two neighbors. Borders are handled by
clamping the coordinates to the image.
"""

import math


def modified_laplacian(img, step=1):
    """ML(u, v) = |2I - I(u-s, v) - I(u+s, v)| + |2I - I(u, v-s) - I(u, v+s)|."""
    height, width = len(img), len(img[0])
    out = []
    for v in range(height):
        row = []
        up, down = img[max(v - step, 0)], img[min(v + step, height - 1)]
        for u in range(width):
            c = 2.0 * img[v][u]
            left, right = img[v][max(u - step, 0)], img[v][min(u + step, width - 1)]
            row.append(abs(c - left - right) + abs(c - up[u] - down[u]))
        out.append(row)
    return out


def window_sum(values, radius):
    """Sum over the (2r+1) x (2r+1) window of each pixel, cut at the border (integral image)."""
    height, width = len(values), len(values[0])
    S = [[0.0] * (width + 1) for _ in range(height + 1)]
    for v in range(height):
        acc = 0.0
        for u in range(width):
            acc += values[v][u]
            S[v + 1][u + 1] = S[v][u + 1] + acc
    out = []
    for v in range(height):
        v0, v1 = max(v - radius, 0), min(v + radius + 1, height)
        row = []
        for u in range(width):
            u0, u1 = max(u - radius, 0), min(u + radius + 1, width)
            row.append(S[v1][u1] - S[v0][u1] - S[v1][u0] + S[v0][u0])
        out.append(row)
    return out


def sum_modified_laplacian(img, step=1, radius=2, t1=0.0):
    """SML: the window sum of the ML values that are at least t1."""
    ml = modified_laplacian(img, step)
    return window_sum([[x if x >= t1 else 0.0 for x in row] for row in ml], radius)


def gaussian_peak_offset(f_prev, f_mid, f_next):
    """Offset in frames of the peak of the Gaussian through three equally spaced samples,
    or None if the samples have no interior maximum or are not positive."""
    if min(f_prev, f_mid, f_next) <= 0.0:
        return None
    a, b, c = math.log(f_prev), math.log(f_mid), math.log(f_next)
    den = a - 2.0 * b + c
    if den >= 0.0:
        return None
    return 0.5 * (a - c) / den


def shape_from_focus(stack, d0=0.0, delta=1.0, step=1, radius=2, t1=0.0):
    """Depth (focus position) per pixel, and the index of the best frame."""
    n = len(stack)
    focus = []
    for k in range(n):  # @line L1
        focus.append(sum_modified_laplacian(stack[k], step, radius, t1))  # @line L2
    height, width = len(stack[0]), len(stack[0][0])
    depth = [[0.0] * width for _ in range(height)]
    best = [[0] * width for _ in range(height)]
    for v in range(height):  # @line L3
        for u in range(width):
            m = max(range(n), key=lambda k: focus[k][v][u])  # @line L4
            offset = 0.0
            if 0 < m < n - 1:  # @line L5
                o = gaussian_peak_offset(focus[m - 1][v][u], focus[m][v][u], focus[m + 1][v][u])
                if o is not None:
                    offset = o
            best[v][u] = m
            depth[v][u] = d0 + delta * (m + offset)  # @line L6
    return depth, best  # @line L7


def defocus_stack(texture, depth_index, frames, blur_per_frame, radius=3):
    """A synthetic focal stack: frame k blurs the texture at pixel (u, v) with a
    Gaussian of standard deviation blur_per_frame * |k - depth_index[v][u]|.
    The texture repeats at the border (periodic)."""
    height, width = len(texture), len(texture[0])
    stack = []
    for k in range(frames):
        img = []
        for v in range(height):
            row = []
            for u in range(width):
                sigma = blur_per_frame * abs(k - depth_index[v][u])
                if sigma < 1e-9:
                    row.append(float(texture[v][u]))
                    continue
                total, wsum = 0.0, 0.0
                for dv in range(-radius, radius + 1):
                    for du in range(-radius, radius + 1):
                        w = math.exp(-(du * du + dv * dv) / (2.0 * sigma * sigma))
                        total += w * texture[(v + dv) % height][(u + du) % width]
                        wsum += w
                row.append(total / wsum)
            img.append(row)
        stack.append(img)
    return stack
