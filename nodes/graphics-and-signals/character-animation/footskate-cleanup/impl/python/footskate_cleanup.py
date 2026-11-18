# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/footskate-cleanup/. The authors are listed in prov/QJ3V2G.jsonl.
"""Footskate cleanup in the spirit of Kovar, Schreiner and Gleicher (2002).

The character lives in the sagittal plane (x forward, y up). A frame holds
the root (hip) position and, for each leg, the world angle of the thigh
(measured from straight down, counterclockwise) and the relative knee
angle. The thigh has length l1 and the shin length l2; the ankle is

    ankle = root + l1 e(phi) + l2 e(phi + knee),  e(a) = (sin a, -cos a).

The input also lists the plant intervals of each leg: runs of frames in
which the foot must stay still. The cleanup:
  1. picks one target ankle position per plant (here the mean of the
     ankle positions over the plant);
  2. moves the root as little as possible so that every planted target is
     within the longest allowed leg, (1 + eps)(l1 + l2);
  3. solves each planted leg in closed form (two-bone IK, knee on the side
     of the original knee), and stretches both bones by the same factor,
     at most 1 + eps, when the target is beyond l1 + l2;
  4. blends the root offset and the leg changes off over b frames before
     and after each plant with a smooth weight, so the motion stays
     continuous.
"""

import math


def e(a):
    return (math.sin(a), -math.cos(a))


def leg_points(root, phi, knee, l1, l2):
    k = (root[0] + l1 * math.sin(phi), root[1] - l1 * math.cos(phi))
    a = (k[0] + l2 * math.sin(phi + knee), k[1] - l2 * math.cos(phi + knee))
    return k, a


def two_bone(root, target, l1, l2, bend_sign):
    """Planar two-bone IK: thigh angle and knee angle so that the ankle is
    at target. bend_sign = -1 bends the knee backward (knee < 0)."""
    dx, dy = target[0] - root[0], target[1] - root[1]
    d = math.hypot(dx, dy)
    # world angle of the line root -> target, measured from straight down
    base = math.atan2(dx, -dy)
    if d >= (l1 + l2) * (1.0 - 1e-12):
        # straight leg; acos near -1 would lose half the digits
        return base, 0.0
    d = max(d, abs(l1 - l2) + 1e-12)
    c =(l1 * l1 + l2 * l2 - d * d) / (2 * l1 * l2)
    inner = math.acos(max(-1.0, min(1.0, c)))
    knee = bend_sign * (math.pi - inner)
    ca = (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d)
    alpha = math.acos(max(-1.0, min(1.0, ca)))
    phi = base - bend_sign * alpha
    return phi, knee


def project_root(h, disks):
    """The point nearest to h inside every disk (center, radius), for one
    or two disks. Return None if the disks do not meet."""
    def inside(p, tol=1e-12):
        return all(math.dist(p, c) <= r + tol for c, r in disks)

    if inside(h):
        return h
    cands = []
    for c, r in disks:
        d = math.dist(h, c)
        p = (c[0] + (h[0] - c[0]) * r / d, c[1] + (h[1] - c[1]) * r / d)
        if inside(p):
            cands.append(p)
    if len(disks) == 2:
        (c1, r1), (c2, r2) = disks
        d = math.dist(c1, c2)
        if 0 < d <= r1 + r2 and d >= abs(r1 - r2):
            a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
            hh = math.sqrt(max(0.0, r1 * r1 - a * a))
            mx = c1[0] + a * (c2[0] - c1[0]) / d
            my = c1[1] + a * (c2[1] - c1[1]) / d
            for s in (1, -1):
                cands.append((mx + s * hh * (c2[1] - c1[1]) / d, my - s * hh * (c2[0] - c1[0]) / d))
    cands = [p for p in cands if inside(p, 1e-9)]
    if not cands:
        return None
    return min(cands, key=lambda p: math.dist(p, h))


def smooth_weight(delta, b):
    """1 at delta = 0, 0 for delta >= b + 1, smooth in between."""
    if delta >= b + 1:
        return 0.0
    s = delta / (b + 1.0)
    return 1.0 - s * s * (3.0 - 2.0 * s)


def cleanup(frames, plants, l1, l2, eps=0.05, b=4):
    """frames: list of dicts {"root": (x, y), "L": (phi, knee), "R": (phi, knee)}.
    plants: dict leg -> list of (start, end), inclusive.
    Return (new frames, targets) where each new frame also has the bone
    lengths per leg in "len_L" and "len_R"."""
    f = len(frames)
    legs = ("L", "R")
    targets = {leg: [] for leg in legs}
    planted = [dict() for _ in range(f)]
    for leg in legs:
        for s, t in plants.get(leg, []):
            pts = [leg_points(frames[i]["root"], *frames[i][leg], l1, l2)[1] for i in range(s, t + 1)]
            c = (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))  # @line L1
            targets[leg].append(((s, t), c))
            for i in range(s, t + 1):
                planted[i][leg] = c
    reach = (1.0 + eps) * (l1 + l2)
    # solve the constrained frames
    root_off = [None] * f
    leg_new = [dict() for _ in range(f)]
    for i in range(f):
        if not planted[i]:
            continue
        h = frames[i]["root"]
        hn = project_root(h, [(c, reach) for c in planted[i].values()])  # @line L2
        if hn is None:
            raise ValueError("the planted feet are too far apart at frame %d" % i)
        root_off[i] = (hn[0] - h[0], hn[1] - h[1])
        for leg, c in planted[i].items():
            d = math.dist(hn, c)
            s = max(1.0, d / (l1 + l2))  # @line L3
            phi0, knee0 = frames[i][leg]
            sign = -1.0 if knee0 <= 0 else 1.0
            phi, knee = two_bone(hn, c, s * l1, s * l2, sign)  # @line L4
            leg_new[i][leg] = (phi - phi0, knee - knee0, s)
    # blend the changes off around the constraints
    const = [i for i in range(f) if planted[i]]
    out = []
    for i in range(f):
        fr = frames[i]
        if root_off[i] is not None:
            off = root_off[i]
        else:
            off = (0.0, 0.0)
            if const:
                j = min(const, key=lambda c: (abs(c - i), c))
                w = smooth_weight(abs(j - i), b)  # @line L5
                off = (w * root_off[j][0], w * root_off[j][1])
        new = {"root": (fr["root"][0] + off[0], fr["root"][1] + off[1])}
        for leg in legs:
            phi, knee = fr[leg]
            if leg in leg_new[i]:
                dphi, dknee, s = leg_new[i][leg]
                w = 1.0
            else:
                js = [j for j in const if leg in leg_new[j]]
                if js:
                    j = min(js, key=lambda c: (abs(c - i), c))
                    dphi, dknee, s = leg_new[j][leg]
                    w = smooth_weight(abs(j - i), b)
                else:
                    dphi = dknee = 0.0
                    s, w = 1.0, 0.0
            new[leg] = (phi + w * dphi, knee + w * dknee)  # @line L6
            new["len_" + leg] = ((1 + w * (s - 1)) * l1, (1 + w * (s - 1)) * l2)
        out.append(new)
    return out, targets


def ankle(frame, leg, l1=None, l2=None):
    a, b = frame.get("len_" + leg, (l1, l2))
    return leg_points(frame["root"], *frame[leg], a, b)[1]
