# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/thermal-driven-3d-floorplanning/. The authors are listed in prov/RF40PK.jsonl.

"""Thermal-driven 3D floorplanning by simulated annealing, after Cong, Wei and Zhang.

A block is (w, h, q): width, height and power density. Blocks may rotate.
A net is a list of block indices. Layer 0 is next to the heat sink.

A floorplan keeps, for each layer, a sequence pair of the blocks on it, plus
a rotation flag per block. Cong, Wei and Zhang use a transitive closure
graph (TCG) for each layer and add a bucket structure over the stack; this
code uses a sequence pair for each layer, which the paper allows, and builds
the buckets again after every move instead of every 20 moves.

The cost is a * wl + b * area + c * vias + d * tmax, each term divided by
its value at the start. The thermal model is a TOY: the closed-form vertical
model of CBA-T-Fast on a g x g grid of tiles, with the same resistances in
every tile and no lateral heat flow. It is not a calibrated model.
"""

import math

SINK = 27.0


# ---------- sequence pair packing ----------

def pack_layer(gp, gm, dims):
    """Lower-left corners of the blocks of one sequence pair.

    a is left of b if a is before b in both orders, and a is below b if b
    is before a in gp and a is before b in gm.
    """
    pos_p = {b: i for i, b in enumerate(gp)}
    pos_m = {b: i for i, b in enumerate(gm)}
    x, y = {}, {}
    for b in gp:
        x[b] = 0.0
        for a in gp[:pos_p[b]]:
            if pos_m[a] < pos_m[b]:
                x[b] = max(x[b], x[a] + dims[a][0])
    for b in gm:
        y[b] = 0.0
        for a in gm[:pos_m[b]]:
            if pos_p[a] > pos_p[b]:
                y[b] = max(y[b], y[a] + dims[a][1])
    return x, y


class Floorplan:
    def __init__(self, layers, rot):
        self.layers = layers  # list of (gp, gm)
        self.rot = rot

    def copy(self):
        return Floorplan([(list(p), list(m)) for p, m in self.layers], list(self.rot))


def dims_of(blocks, rot):
    return [(h, w) if r else (w, h) for (w, h, _), r in zip(blocks, rot)]


def realize(blocks, fp):
    """Return x, y, layer and dims of every block."""
    dims = dims_of(blocks, fp.rot)
    n = len(blocks)
    x, y, lay = [0.0] * n, [0.0] * n, [0] * n
    for k, (gp, gm) in enumerate(fp.layers):
        px, py = pack_layer(gp, gm, dims)
        for b in gp:
            x[b], y[b], lay[b] = px[b], py[b], k
    return x, y, lay, dims


# ---------- the terms of the cost ----------

def footprint(x, y, dims):
    return max(x[i] + dims[i][0] for i in range(len(x))), max(y[i] + dims[i][1] for i in range(len(y)))


def wirelength(x, y, dims, nets):
    total = 0.0
    for net in nets:
        cx = [x[i] + dims[i][0] / 2 for i in net]
        cy = [y[i] + dims[i][1] / 2 for i in net]
        total += max(cx) - min(cx) + max(cy) - min(cy)
    return total


def via_count(lay, nets):
    """Device layers crossed by the nets: max layer minus min layer, summed."""
    return sum(max(lay[i] for i in net) - min(lay[i] for i in net) for net in nets)


def tile_powers(blocks, x, y, lay, dims, n_layers, g):
    """Mean power density of each tile (layer, i, j).

    It is the sum over blocks of power density times overlap area, divided
    by the tile area. With resistances given per unit area (K area / W),
    the temperatures then do not depend on the size of the tiles.
    """
    W, H = footprint(x, y, dims)
    tw, th = W / g, H / g
    p = [[[0.0] * g for _ in range(g)] for _ in range(n_layers)]
    for b, (_, _, q) in enumerate(blocks):
        x0, x1, y0, y1 = x[b], x[b] + dims[b][0], y[b], y[b] + dims[b][1]
        for i in range(max(0, int(x0 / tw)), min(g, int(math.ceil(x1 / tw)))):
            ox = min(x1, (i + 1) * tw) - max(x0, i * tw)
            if ox <= 0:
                continue
            for j in range(max(0, int(y0 / th)), min(g, int(math.ceil(y1 / th)))):
                oy = min(y1, (j + 1) * th) - max(y0, j * th)
                if oy > 0:
                    p[lay[b]][i][j] += q * ox * oy / (tw * th)
    return p


def stack_top_temperature(powers, r_layers, r_base):
    """Closed form of one tile stack: Tsink + Rb * sum P + sum_i P_i * sum_{j <= i} R_j.

    Layer 0 is next to the sink. This is the top node of a chain of
    resistors, where resistor j carries the power of layers j and above.
    """
    t = SINK + r_base * sum(powers)
    acc = 0.0
    for p_i, r_i in zip(powers, r_layers):
        acc += r_i
        t += p_i * acc
    return t


def max_temperature(blocks, x, y, lay, dims, n_layers, g, r_layers, r_base):
    p = tile_powers(blocks, x, y, lay, dims, n_layers, g)
    return max(stack_top_temperature([p[k][i][j] for k in range(n_layers)], r_layers, r_base)
               for i in range(g) for j in range(g))


def terms(blocks, nets, fp, model):
    x, y, lay, dims = realize(blocks, fp)
    W, H = footprint(x, y, dims)
    t = max_temperature(blocks, x, y, lay, dims, len(fp.layers), *model)
    return W * H, wirelength(x, y, dims, nets), float(via_count(lay, nets)), t - SINK


def cost(blocks, nets, fp, model, weights, norm):
    vals = terms(blocks, nets, fp, model)
    return sum(w * v / max(nv, 1e-12) for w, v, nv in zip(weights, vals, norm))


# ---------- moves ----------

def z_neighbor(blocks, fp, j, alpha=1.0, beta=1.0, buckets=3):
    """Block on another layer that shares a bucket with j, of least cost
    alpha * |A_k - A_j| + beta * (|x_k - x_j| + |y_k - y_j|)."""
    x, y, lay, dims = realize(blocks, fp)
    W, H = footprint(x, y, dims)
    bw, bh = W / buckets, H / buckets

    def cells(b):
        i0, i1 = int(x[b] / bw), min(buckets - 1, int((x[b] + dims[b][0]) / bw - 1e-9))
        j0, j1 = int(y[b] / bh), min(buckets - 1, int((y[b] + dims[b][1]) / bh - 1e-9))
        return {(i, k) for i in range(i0, i1 + 1) for k in range(j0, j1 + 1)}

    mine = cells(j)
    best, best_c = None, None
    for k in range(len(blocks)):
        if lay[k] == lay[j] or not (cells(k) & mine):
            continue
        c = alpha * abs(dims[k][0] * dims[k][1] - dims[j][0] * dims[j][1]) + beta * (abs(x[k] - x[j]) + abs(y[k] - y[j]))
        if best_c is None or c < best_c:
            best, best_c = k, c
    return best


def layer_of(fp, b):
    for k, (gp, _) in enumerate(fp.layers):
        if b in gp:
            return k
    raise ValueError(b)


def swap_blocks(fp, a, b):
    for gp, gm in fp.layers:
        for seq in (gp, gm):
            for i, v in enumerate(seq):
                if v == a:
                    seq[i] = b
                elif v == b:
                    seq[i] = a


def perturb(blocks, fp, rng, p_global):
    """Return a new floorplan after one of the seven moves, and its name."""
    fp = fp.copy()
    n = len(blocks)
    if rng.random() < p_global:
        kind = rng.choice(["rotation", "swap", "interlayer swap"])
    else:
        kind = rng.choice(["reverse", "move", "z-neighbor swap", "z-neighbor move"])
    b = rng.randrange(n)
    k = layer_of(fp, b)
    gp, gm = fp.layers[k]
    if kind == "rotation":
        fp.rot[b] = not fp.rot[b]
    elif kind in ("swap", "reverse"):
        if len(gp) < 2:
            return fp, None
        a = rng.choice([v for v in gp if v != b])
        if kind == "swap":
            swap_blocks(fp, a, b)
        else:  # exchange the two blocks in gp only, which flips their relation
            i, j = gp.index(a), gp.index(b)
            gp[i], gp[j] = gp[j], gp[i]
    elif kind == "move":
        if len(gp) < 2:
            return fp, None
        for seq in (gp, gm):
            seq.remove(b)
            seq.insert(rng.randrange(len(seq) + 1), b)
    elif kind == "interlayer swap":
        others = [v for v in range(n) if layer_of(fp, v) != k]
        if not others:
            return fp, None
        swap_blocks(fp, b, rng.choice(others))
    else:
        z = z_neighbor(blocks, fp, b)
        if z is None and kind == "z-neighbor move" and len(fp.layers) > 1:
            # No block of another layer is near b, for example because the
            # other layers are empty: put b at a random place on another
            # layer, so that an empty layer can be filled again.
            k2 = rng.choice([i for i in range(len(fp.layers)) if i != k])
            gp.remove(b)
            gm.remove(b)
            for seq in fp.layers[k2]:
                seq.insert(rng.randrange(len(seq) + 1), b)
            return fp, kind
        if z is None:
            return fp, None
        if kind == "z-neighbor swap":
            swap_blocks(fp, b, z)
        else:  # z-neighbor move: put b next to z on z's layer, to its right or above it
            gp.remove(b)
            gm.remove(b)
            zp, zm = fp.layers[layer_of(fp, z)]
            if rng.random() < 0.5:
                zp.insert(zp.index(z) + 1, b)
                zm.insert(zm.index(z) + 1, b)
            else:
                zp.insert(zp.index(z), b)
                zm.insert(zm.index(z) + 1, b)
    return fp, kind


# ---------- the annealing ----------

def thermal_floorplan(blocks, nets, n_layers=2, weights=(1.0, 1.0, 1.0, 1.0),
                      model=(10, (1.0, 1.0), 0.5), seed=0, t0=None, t_stop=1e-3,
                      cooling=0.9, moves_per_t=None, norm=None):
    """Return the best floorplan, its cost and the four values that divide the terms."""
    import random
    rng = random.Random(seed)
    n = len(blocks)
    layers = [([], []) for _ in range(n_layers)]
    order = list(range(n))
    rng.shuffle(order)
    for i, b in enumerate(order):  # @line L1
        layers[i % n_layers][0].append(b)
    for gp, gm in layers:
        gm.extend(gp)
        rng.shuffle(gm)
    fp = Floorplan(layers, [False] * n)
    if norm is None:
        norm = terms(blocks, nets, fp, model)
    cur = cost(blocks, nets, fp, model, weights, norm)  # @line L2
    best, best_cost = fp, cur
    moves = moves_per_t or 20 * n
    if t0 is None:  # accept an average uphill move with probability 0.9 at the start
        ups = []
        for _ in range(40):
            new, kind = perturb(blocks, fp, rng, 0.5)
            if kind is not None:
                d = cost(blocks, nets, new, model, weights, norm) - cur
                if d > 0:
                    ups.append(d)
        t0 = (sum(ups) / len(ups) if ups else 1.0) / -math.log(0.9)
    t = t0
    while t > t_stop * t0:  # @line L3
        for _ in range(moves):  # @line L4
            new, kind = perturb(blocks, fp, rng, p_global=0.3 + 0.4 * t / t0)  # @line L5
            if kind is None:
                continue
            c = cost(blocks, nets, new, model, weights, norm)  # @line L6
            if c <= cur or rng.random() < math.exp(-(c - cur) / t):  # @line L7
                fp, cur = new, c
                if c < best_cost:  # @line L8
                    best, best_cost = new, c
        t *= cooling
    return best, best_cost, norm  # @line L9
