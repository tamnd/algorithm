# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gru4rec/. The authors are listed in prov/6CBA3Q.jsonl.

"""GRU4Rec (Hidasi, Karatzoglou, Baltrunas and Tikk, ICLR 2016), by hand.

The input of step t is the item x_t as a one-hot vector, so W x_t is the
column of W for item x_t; here the input weights are stored by item, as rows
Wz[x], Wr[x], Wh[x] of length H. The GRU of Equations 2 to 5 of the paper:

    z_t  = sigma(Wz[x_t] + Uz h_(t-1))
    r_t  = sigma(Wr[x_t] + Ur h_(t-1))
    hh_t = tanh(Wh[x_t] + Uh (r_t * h_(t-1)))
    h_t  = (1 - z_t) * h_(t-1) + z_t * hh_t

The score of item j after step t is O[j] . h_t + c[j]. The loss of step t
compares the target item i with a list of negative items j (N_S of them):

    BPR:  -(1/N_S) sum_j ln sigma(r_i - r_j)
    TOP1:  (1/N_S) sum_j sigma(r_j - r_i) + sigma(r_j^2)

`sequence_loss_and_grad` runs the forward pass over a sequence and the
backward pass through time, written by hand. Training uses session-parallel
mini-batches with the targets of the other lanes as negatives, and stops the
gradient at the step boundary (the hidden state is carried, not
differentiated through). That cut is a choice of this module, not of the
paper. The gradient check covers full sequences. The paper also uses tanh on
the output scores and Adagrad; this module uses linear scores and plain SGD.

Parameters are a dict of 2-D lists.
"""

import math
import random

Matrix = list[list[float]]
Params = dict[str, Matrix]


def sigmoid(z: float) -> float:
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


def log_sigmoid(z: float) -> float:
    if z >= 0:
        return -math.log1p(math.exp(-z))
    return z - math.log1p(math.exp(z))


def matvec(a: Matrix, v: list[float]) -> list[float]:
    return [sum(x * y for x, y in zip(row, v)) for row in a]


def tmatvec(a: Matrix, v: list[float]) -> list[float]:
    """a^T v."""
    out = [0.0] * len(a[0])
    for row, s in zip(a, v):
        if s != 0.0:
            for c, x in enumerate(row):
                out[c] += x * s
    return out


def init(n_items: int, hidden: int, seed: int = 1, scale: float = 0.3) -> Params:
    """Gaussian start. Cost O(n_items H + H^2)."""
    rng = random.Random(seed)

    def mat(r: int, c: int) -> Matrix:
        return [[rng.gauss(0.0, scale) for _ in range(c)] for _ in range(r)]

    return {
        "Wz": mat(n_items, hidden), "Wr": mat(n_items, hidden), "Wh": mat(n_items, hidden),
        "Uz": mat(hidden, hidden), "Ur": mat(hidden, hidden), "Uh": mat(hidden, hidden),
        "O": mat(n_items, hidden), "c": [[0.0] * n_items],
    }


def gru_step(p: Params, x: int, h: list[float]) -> dict:
    """One GRU step from state h with input item x. Cost O(H^2)."""
    az = [a + b for a, b in zip(p["Wz"][x], matvec(p["Uz"], h))]
    ar = [a + b for a, b in zip(p["Wr"][x], matvec(p["Ur"], h))]
    z = [sigmoid(v) for v in az]  # @line L9
    r = [sigmoid(v) for v in ar]
    rh = [a * b for a, b in zip(r, h)]
    hh = [math.tanh(a + b) for a, b in zip(p["Wh"][x], matvec(p["Uh"], rh))]  # @line L10
    new = [(1.0 - zz) * hp + zz * hc for zz, hp, hc in zip(z, h, hh)]  # @line L11
    return {"x": x, "h_prev": h, "z": z, "r": r, "rh": rh, "hh": hh, "h": new}


def scores(p: Params, h: list[float], items: list[int]) -> list[float]:
    """O[j] . h + c[j] for the listed items. Cost O(len(items) H)."""
    return [sum(a * b for a, b in zip(p["O"][j], h)) + p["c"][0][j] for j in items]


def step_loss(kind: str, rs: list[float]) -> tuple[float, list[float]]:
    """Loss and its derivative in the scores. rs[0] is the target, rs[1:] the negatives."""
    ri, neg = rs[0], rs[1:]
    ns = len(neg)
    if ns == 0:
        return 0.0, [0.0] * len(rs)
    d = [0.0] * len(rs)
    total = 0.0
    if kind == "bpr":
        for k, rj in enumerate(neg, start=1):
            total -= log_sigmoid(ri - rj) / ns
            g = sigmoid(rj - ri) / ns
            d[0] -= g
            d[k] += g
    elif kind == "top1":
        for k, rj in enumerate(neg, start=1):
            a, b = sigmoid(rj - ri), sigmoid(rj * rj)
            total += (a + b) / ns
            d[0] -= a * (1.0 - a) / ns
            d[k] += (a * (1.0 - a) + b * (1.0 - b) * 2.0 * rj) / ns
    else:
        raise ValueError("kind must be 'bpr' or 'top1'")
    return total, d


def zeros_like(p: Params) -> Params:
    return {name: [[0.0] * len(row) for row in mat] for name, mat in p.items()}


def sequence_loss_and_grad(
    p: Params, xs: list[int], ys: list[int], negs: list[list[int]], h0: list[float], kind: str
) -> tuple[float, Params, list[float]]:
    """Loss summed over the steps, its gradient by backpropagation through time, and the last state.

    Step t reads xs[t] and is scored on target ys[t] against the items negs[t].
    h0 is a constant. Cost O(T (H^2 + N_S H)) for T steps.
    """
    caches, total, dscores = [], 0.0, []
    h = h0
    for x, y, neg in zip(xs, ys, negs):
        c = gru_step(p, x, h)
        items = [y] + neg
        loss, d = step_loss(kind, scores(p, c["h"], items))
        total += loss
        caches.append(c)
        dscores.append((items, d))
        h = c["h"]
    g = zeros_like(p)
    dh_next = [0.0] * len(h0)
    for c, (items, d) in zip(reversed(caches), reversed(dscores)):
        dh = dh_next[:]
        for j, dj in zip(items, d):
            g["c"][0][j] += dj
            for k in range(len(dh)):
                g["O"][j][k] += dj * c["h"][k]
                dh[k] += dj * p["O"][j][k]
        x, hp, z, r, rh, hh = c["x"], c["h_prev"], c["z"], c["r"], c["rh"], c["hh"]
        dhh = [a * b for a, b in zip(dh, z)]
        dz = [a * (b - e) for a, b, e in zip(dh, hh, hp)]
        dhp = [a * (1.0 - b) for a, b in zip(dh, z)]
        dah = [a * (1.0 - b * b) for a, b in zip(dhh, hh)]
        drh = tmatvec(p["Uh"], dah)
        dr = [a * b for a, b in zip(drh, hp)]
        dhp = [a + b * e for a, b, e in zip(dhp, drh, r)]
        daz = [a * b * (1.0 - b) for a, b in zip(dz, z)]
        dar = [a * b * (1.0 - b) for a, b in zip(dr, r)]
        for name, da, inp in (("h", dah, rh), ("z", daz, hp), ("r", dar, hp)):
            gw, gu = g["W" + name][x], g["U" + name]
            for k in range(len(da)):
                gw[k] += da[k]
                for q in range(len(inp)):
                    gu[k][q] += da[k] * inp[q]
        dhp = [a + b + e for a, b, e in zip(dhp, tmatvec(p["Uz"], daz), tmatvec(p["Ur"], dar))]
        dh_next = dhp
    return total, g, h


def session_parallel_batches(sessions: list[list[int]], lanes: int) -> list[list[tuple[int, int, int, bool]]]:
    """The session-parallel mini-batches of Section 3.1.1 of the paper.

    Each batch is a list of (session index, input item, target item, reset),
    one per active lane. A lane works through its session event by event;
    when the session ends, the lane takes the next unused session and the
    hidden state is reset. Sessions shorter than 2 are skipped. Cost
    O(total events).
    """
    queue = [s for s in range(len(sessions)) if len(sessions[s]) >= 2]
    nxt = 0
    state: list[list[int] | None] = []
    for _ in range(lanes):
        if nxt < len(queue):
            state.append([queue[nxt], 0])
            nxt += 1
        else:
            state.append(None)
    batches = []
    while any(st is not None for st in state):
        batch = []
        for b in range(lanes):
            st = state[b]
            if st is None:
                continue
            s, pos = st
            seq = sessions[s]
            batch.append((s, seq[pos], seq[pos + 1], pos == 0))
            if pos + 2 < len(seq):
                state[b] = [s, pos + 1]
            elif nxt < len(queue):
                state[b] = [queue[nxt], 0]
                nxt += 1
            else:
                state[b] = None
        batches.append(batch)
    return batches


def train(
    sessions: list[list[int]], n_items: int, hidden: int, lanes: int, epochs: int, rate: float,
    kind: str = "bpr", seed: int = 1,
) -> Params:
    """SGD over session-parallel mini-batches with in-batch negatives. Cost O(E events (H^2 + lanes H))."""
    p = init(n_items, hidden, seed)  # @line L1
    for _ in range(epochs):  # @line L2
        hs: dict[int, list[float]] = {}
        for batch in session_parallel_batches(sessions, lanes):  # @line L3
            targets = [y for _, _, y, _ in batch]
            g_total = zeros_like(p)
            for s, x, y, reset in batch:
                h = [0.0] * hidden if reset else hs[s]  # @line L4
                neg = sorted({t for t in targets if t != y})
                _, g, h_new = sequence_loss_and_grad(p, [x], [y], [neg], h, kind)  # @line L5
                hs[s] = h_new
                for name, mat in g.items():  # @line L6
                    tot = g_total[name]
                    for r, row in enumerate(mat):
                        for c, v in enumerate(row):
                            tot[r][c] += v
            for name, mat in p.items():  # @line L7
                for r, row in enumerate(mat):
                    gr = g_total[name][r]
                    for c in range(len(row)):
                        row[c] -= rate * gr[c]
    return p  # @line L8


def next_items(p: Params, session: list[int], n_items: int, k: int) -> list[int]:
    """The k items with the highest score after reading the session. Cost O(T H^2 + n H)."""
    h = [0.0] * len(p["Uz"])
    for x in session:
        h = gru_step(p, x, h)["h"]
    s = scores(p, h, list(range(n_items)))
    return sorted(range(n_items), key=lambda j: (-s[j], j))[:k]
