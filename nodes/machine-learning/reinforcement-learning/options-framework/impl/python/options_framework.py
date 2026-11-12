# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/options-framework/. The authors are listed in prov/QWHW45.jsonl.

"""Options and SMDP value iteration on a four-rooms gridworld.

An option is (initiation set, policy, termination). Its model at a start state
s is the expected discounted reward R_o(s) until it terminates and the
discounted termination distribution P_o(x | s) = sum_k gamma^k Pr(stop at x
after k steps). Both are fixed points of linear equations and are computed by
one exact linear solve. SMDP value iteration then backs up over options:

    V(s) <- max_{o : s in I_o} R_o(s) + sum_x P_o(x | s) V(x).

Moves succeed with probability 2/3 and go in each other direction with
probability 1/9; a move into a wall stays put. Entering the goal pays 1 and
ends the episode.
"""

LAYOUT = [
    "#########",
    "#   #   #",
    "#       #",
    "#   #   #",
    "## ### ##",
    "#   #   #",
    "#       #",
    "#   #   #",
    "#########",
]
MOVES = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up, right, down, left


class FourRooms:
    def __init__(self, layout=LAYOUT, goal=(6, 7), gamma: float = 0.9) -> None:
        self.cells = [(r, c) for r, row in enumerate(layout) for c, ch in enumerate(row) if ch == " "]
        self.index = {cell: i for i, cell in enumerate(self.cells)}
        self.goal, self.gamma = goal, gamma
        self.n = len(self.cells)
        self.rooms = []
        for r0, c0 in ((1, 1), (1, 5), (5, 1), (5, 5)):
            self.rooms.append({(r, c) for r in range(r0, r0 + 3) for c in range(c0, c0 + 3)})
        self.hallways = [cell for cell in self.cells if not any(cell in room for room in self.rooms)]

    def outcomes(self, s: int, a: int):
        """List of (prob, reward, next state index, done) for primitive action a."""
        r, c = self.cells[s]
        out = []
        for b, (dr, dc) in enumerate(MOVES):
            p = 2 / 3 if b == a else 1 / 9
            nxt = (r + dr, c + dc)
            if nxt not in self.index:
                nxt = (r, c)
            if nxt == self.goal:
                out.append((p, 1.0, None, True))
            else:
                out.append((p, 0.0, self.index[nxt], False))
        return out

    def states(self):
        """All non-goal state indices (the goal is terminal)."""
        return [i for i, cell in enumerate(self.cells) if cell != self.goal]


def solve(mat, rhs):
    """Solve mat x = rhs (several right-hand sides as columns) by Gauss-Jordan."""
    k = len(mat)
    m = [list(mat[i]) + list(rhs[i]) for i in range(k)]
    w = len(m[0])
    for c in range(k):
        p = max(range(c, k), key=lambda i: abs(m[i][c]))
        m[c], m[p] = m[p], m[c]
        piv = m[c][c]
        m[c] = [x / piv for x in m[c]]
        for i in range(k):
            if i != c and m[i][c] != 0:
                f = m[i][c]
                m[i] = [x - f * y for x, y in zip(m[i], m[c])]
    return [m[i][k:w] for i in range(k)]


def primitive_option(env: FourRooms, a: int):
    """A primitive action as a one-step option: (initiation, model)."""
    model = {}
    for s in env.states():
        rew, dist = 0.0, {}
        for p, r, s2, done in env.outcomes(s, a):
            rew += p * r
            if not done:
                dist[s2] = dist.get(s2, 0.0) + env.gamma * p
        model[s] = (rew, dist)
    return model


def hallway_option(env: FourRooms, room: set, target):
    """The option that walks from inside room to the hallway cell target along a
    shortest path, and stops as soon as it leaves the interior of the room."""
    inside = [env.index[cell] for cell in sorted(room) if cell != env.goal]
    # shortest-path policy toward target, by breadth-first search over room cells
    dist = {target: 0}
    frontier = [target]
    while frontier:
        nxt = []
        for r, c in frontier:
            for dr, dc in MOVES:
                cell = (r + dr, c + dc)
                if cell in room and cell not in dist:
                    dist[cell] = dist[(r, c)] + 1
                    nxt.append(cell)
        frontier = nxt
    policy = {}
    for s in inside:
        r, c = env.cells[s]
        best = min(range(4), key=lambda a: (dist.get((r + MOVES[a][0], c + MOVES[a][1]), 99), a))
        policy[s] = best
    # model on the interior: R = r + gamma P_cont R; Pstop = gamma (P_stop + P_cont Pstop)
    pos = {s: i for i, s in enumerate(inside)}
    stops = sorted({s2 for s in inside for _, _, s2, d in env.outcomes(s, policy[s])
                    if not d and s2 not in pos})
    col = {x: j for j, x in enumerate(stops)}
    k = len(inside)
    mat = [[0.0] * k for _ in range(k)]
    rhs = [[0.0] * (1 + len(stops)) for _ in range(k)]
    for s in inside:
        i = pos[s]
        mat[i][i] += 1.0
        for p, rew, s2, done in env.outcomes(s, policy[s]):  # @line M2
            rhs[i][0] += p * rew
            if done:
                continue
            if s2 in pos:
                mat[i][pos[s2]] -= env.gamma * p  # @line M3
            else:
                rhs[i][1 + col[s2]] += env.gamma * p  # @line M4
    sol = solve(mat, rhs)  # @line M5
    model = {}
    for s in inside:
        row = sol[pos[s]]
        model[s] = (row[0], {x: row[1 + col[x]] for x in stops if row[1 + col[x]] != 0.0})
    # the option may also start at the other hallway of the room, one step outside
    for h in env.hallways:
        if h == target:
            continue
        hi = env.index[h]
        r, c = h
        moves_in = [a for a in range(4) if (r + MOVES[a][0], c + MOVES[a][1]) in room]
        if not moves_in:
            continue
        a = moves_in[0]
        rew, dist2 = 0.0, {}
        for p, rr, s2, done in env.outcomes(hi, a):  # @line M1
            rew += p * rr
            if done:
                continue
            if s2 in pos:
                r2, d2 = model[s2]
                rew += env.gamma * p * r2
                for x, q in d2.items():
                    dist2[x] = dist2.get(x, 0.0) + env.gamma * p * q
            else:
                dist2[s2] = dist2.get(s2, 0.0) + env.gamma * p
        model[hi] = (rew, dist2)
    return model


def hallway_options(env: FourRooms):
    """Two options per room, one to each of its hallways: eight in all."""
    out = []
    for room in env.rooms:
        for h in env.hallways:
            r, c = h
            if any((r + dr, c + dc) in room for dr, dc in MOVES):
                out.append(hallway_option(env, room, h))
    return out


def smdp_value_iteration(env: FourRooms, options, tol: float = 1e-12, max_iter: int = 100000):
    """SMDP value iteration over option models; returns (V, number of sweeps, history).

    history[k] is the number of states with a nonzero value after sweep k."""
    v = {s: 0.0 for s in env.states()}  # @line L1
    history = []
    for it in range(1, max_iter + 1):  # @line L2
        new = {}
        for s in v:
            best = None
            for model in options:
                if s in model:  # s is in the initiation set
                    rew, dist = model[s]
                    val = rew + sum(q * v[x] for x, q in dist.items())  # @line L3
                    best = val if best is None or val > best else best
            new[s] = best
        delta = max(abs(new[s] - v[s]) for s in v)  # @line L4
        v = new  # @line L4
        history.append(sum(1 for x in v.values() if x != 0.0))
        if delta < tol:  # @line L5
            return v, it, history  # @line L6
    return v, max_iter, history
