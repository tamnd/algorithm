# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/micali-vazirani-algorithm/. The authors are listed in prov/ZG9QWA.jsonl.

INF = float("inf")


def micali_vazirani_algorithm(n: int, edges: list[tuple[int, int]]) -> list[int]:
    """A maximum matching of a general graph without weights.

    The vertices are 0, ..., n - 1. The result is the list of mates, with -1
    for an unmatched vertex. Each phase finds a maximal set of vertex-disjoint
    shortest augmenting paths, as in the algorithm of Micali and Vazirani.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    adj: list[list[int]] = [[] for _ in range(n)]
    seen = set()
    for u, v in edges:
        if not (0 <= u < n and 0 <= v < n):
            raise ValueError("edge endpoint out of range")
        if u == v:
            raise ValueError("self-loops are not allowed")
        key = (min(u, v), max(u, v))
        if key not in seen:
            seen.add(key)
            adj[u].append(v)
            adj[v].append(u)
    mate = [-1] * n
    while _Phase(n, adj, mate).run():  # @line L1
        pass
    return mate  # @line L10


class _Phase:
    """One phase: level search, bridges, double depth-first search, augmentation."""

    def __init__(self, n, adj, mate):
        self.n, self.adj, self.mate = n, adj, mate
        self.lev = [[INF, INF] for _ in range(n)]  # [evenlevel, oddlevel]
        self.pred = [[] for _ in range(n)]
        self.succ = [[] for _ in range(n)]
        self.pred_left = [0] * n
        self.erased = [False] * n
        self.scanned = set()
        self.cand: dict[int, list[int]] = {}
        self.bridges: dict[int, list[tuple[int, int]]] = {}
        self.pending = [[] for _ in range(n)]  # bridges waiting for a level of this vertex
        self.bud = [-1] * n  # bud of the petal of a vertex, -1 if in no petal
        self.petal_of = [-1] * n
        self.petals = []  # (bud, red endpoint, green endpoint, parity of bridge, arrivals at bud)
        self.color = [0] * n  # 1 red, 2 green, inside a petal
        self.tree = [None] * n  # (parent, witness predecessor) inside the petal's DFS tree
        self.star = list(range(n))  # union-find for bud*

    # ---- levels -------------------------------------------------------
    def minlevel(self, v):
        return min(self.lev[v])

    def set_level(self, v, parity, value):
        self.lev[v][parity] = value
        self.cand.setdefault(value, []).append(v)
        waiting, self.pending[v] = self.pending[v], []
        for u, w, p in waiting:
            self.add_bridge(u, w, p)

    def add_bridge(self, u, w, parity):
        """Insert the bridge uw (parity 0: unmatched, 1: matched) once both levels are known."""
        a, b = self.lev[u][parity], self.lev[w][parity]
        if a == INF:
            self.pending[u].append((u, w, parity))
        elif b == INF:
            self.pending[w].append((u, w, parity))
        else:
            self.bridges.setdefault((a + b) // 2, []).append((u, w))

    def find(self, v):
        root = v
        while self.star[root] != root:
            root = self.star[root]
        while self.star[v] != root:
            self.star[v], v = root, self.star[v]
        return root

    # ---- the phase ----------------------------------------------------
    def run(self):
        for v in range(self.n):  # @line L2
            if self.mate[v] == -1:
                self.set_level(v, 0, 0)
        for i in range(2 * self.n + 2):  # @line L3
            self.min_step(i)  # @line L4
            found = self.max_step(i)  # @line L5
            if found:  # @line L9
                return True
        return False

    def min_step(self, i):
        par = i % 2
        for u in self.cand.get(i, []):
            if par == 0:
                nbrs = [v for v in self.adj[u] if v != self.mate[u]]
            else:
                nbrs = [self.mate[u]] if self.mate[u] != -1 else []
            for v in nbrs:
                key = (min(u, v), max(u, v))
                if key in self.scanned:
                    continue
                self.scanned.add(key)
                if self.minlevel(v) >= i + 1:  # a prop
                    if self.lev[v][1 - par] == INF:
                        self.set_level(v, 1 - par, i + 1)
                    self.pred[v].append(u)
                    self.succ[u].append(v)
                    self.pred_left[v] += 1
                else:  # a bridge
                    self.add_bridge(u, v, par)

    def max_step(self, i):
        found = False
        lst = self.bridges.get(i, [])
        k = 0
        while k < len(lst):
            u, v = lst[k]
            k += 1
            if self.erased[u] or self.erased[v]:
                continue
            parity = 0 if self.mate[u] != v else 1
            result = self.ddfs(u, v)
            if result is None:
                continue
            if result[0] == "petal":  # @line L6
                self.make_petal(i, u, v, parity, result)
            else:  # @line L7
                path = self.augmenting_path(u, v, parity, result)
                self.augment(path)  # @line L8
                found = True
        return found

    # ---- double depth-first search -----------------------------------
    def ddfs(self, s_red, s_green):
        r0, g0 = self.find(s_red), self.find(s_green)
        if r0 == g0 or self.erased[r0] or self.erased[g0]:
            return None
        color = {r0: 1, g0: 2}
        parent = {r0: None, g0: None}
        stack = {1: [r0], 2: [g0]}
        ptr = {}
        lv = self.minlevel

        def step(side):
            """One DFS move. Returns ('met', w, arrival) on a meeting, None otherwise."""
            st = stack[side]
            c = st[-1]
            preds = self.pred[c]
            j = ptr.get(c, 0)
            while j < len(preds):
                p = preds[j]
                j += 1
                ptr[c] = j
                if self.erased[p]:
                    continue
                w = self.find(p)
                if self.erased[w]:
                    continue
                if w not in color:
                    color[w] = side
                    parent[w] = (c, p)
                    st.append(w)
                    return None
                other = stack[3 - side]
                if other and other[-1] == w:
                    return ("met", w, (c, p))
            ptr[c] = j
            st.pop()
            return None

        def search(side, w):
            """Backtrack from w and look for another vertex at level <= level(w)."""
            st = stack[side]
            while st:
                c = st[-1]
                if c != w and lv(c) <= lv(w):
                    return True
                step(side)
            return False

        while True:
            cr, cg = stack[1][-1], stack[2][-1]
            if cr != cg and lv(cr) == 0 and lv(cg) == 0:
                return ("path", parent, cr, cg)
            side = 1 if lv(cr) >= lv(cg) else 2
            res = step(side)
            if not stack[side]:
                raise AssertionError("a DFS lost its stack outside a meeting")
            if res is None:
                continue
            _, w, arrival = res
            owner = 3 - side
            arr = {side: arrival, owner: parent[w]}
            stack[owner].pop()
            if search(2, w):
                color[w], parent[w] = 1, arr[1]
                stack[1].append(w)
            elif search(1, w):
                color[w], parent[w] = 2, arr[2]
                stack[2].append(w)
            else:
                del color[w]
                return ("petal", w, color, parent, arr)

    def make_petal(self, i, s_red, s_green, parity, result):
        _, b, color, parent, arr = result
        pid = len(self.petals)
        self.petals.append((b, s_red, s_green, parity, arr))
        for w, c in color.items():
            self.bud[w] = b
            self.petal_of[w] = pid
            self.color[w] = c
            self.tree[w] = parent[w]
            self.star[w] = b
        for w in color:
            even, odd = self.lev[w]
            if even == INF:
                self.set_level(w, 0, 2 * i + 1 - odd)
            elif odd == INF:
                self.set_level(w, 1, 2 * i + 1 - even)

    # ---- paths --------------------------------------------------------
    def rep(self, v, pid, b):
        """Follow buds from v up to a vertex of petal pid or its bud b."""
        while v != b and self.petal_of[v] != pid:
            v = self.bud[v]
            if v == -1:
                raise AssertionError("left the petal")
        return v

    def open(self, x, b, par):
        """An alternating path x, ..., b on which x has parity par and b is used as even."""
        path = [x]
        while x != b:
            pid = self.petal_of[x]
            seg = self.open_petal(x, pid, par)
            path.extend(seg[1:])
            x, par = self.petals[pid][0], 0
        return path

    def down(self, x, b):
        """Follow predecessors from x down to the bud b of its petal."""
        pid = self.petal_of[x]
        path = [x]
        while x != b:
            nxt = None
            for p in self.pred[x]:
                if self.erased[p]:
                    continue
                r = self.rep(p, pid, b)
                if not self.erased[r]:
                    nxt = (p, r)
                    break
            if nxt is None:
                raise AssertionError("no predecessor left")
            p, r = nxt
            path.extend(self.open(p, r, 1 - self.minlevel(x) % 2))
            x = r
        return path

    def tree_path(self, top, x, parent):
        """The DFS tree path from top down to x, with petals opened."""
        chain = [x]
        while chain[-1] != top:
            chain.append(parent[chain[-1]][0])
        chain.reverse()
        path = [top]
        for k in range(1, len(chain)):
            c, p = parent[chain[k]]
            path.extend(self.open(p, chain[k], 1 - self.minlevel(c) % 2))
        return path

    def open_petal(self, x, pid, par):
        b, s_red, s_green, bpar, arr = self.petals[pid]
        if par == self.minlevel(x) % 2:
            return self.down(x, b)
        if self.lev[x][par] == INF:
            raise AssertionError("wrong parity")
        parent = self.tree
        mine = self.color[x]
        s_mine, s_other = (s_red, s_green) if mine == 1 else (s_green, s_red)
        r_mine = self.rep(s_mine, pid, b)
        r_other = self.rep(s_other, pid, b)
        up = self.open(s_mine, r_mine, bpar)[:-1] + self.tree_path(r_mine, x, parent)
        up.reverse()
        if r_other == b:
            rest = self.open(s_other, b, bpar)
        else:
            c, p = arr[3 - mine]
            rest = self.open(s_other, r_other, bpar)[:-1] + self.tree_path(r_other, c, parent)
            rest += self.open(p, b, 1 - self.minlevel(c) % 2)
        return up + rest

    def augmenting_path(self, s_red, s_green, bpar, result):
        _, parent, f_red, f_green = result
        sides = []
        for s, free in ((s_red, f_red), (s_green, f_green)):
            root = self.find(s)
            sides.append(self.open(s, root, bpar)[:-1] + self.tree_path(root, free, parent))
        return sides[0][::-1] + sides[1]

    def augment(self, path):
        mate = self.mate
        if len(set(path)) != len(path) or mate[path[0]] != -1 or mate[path[-1]] != -1:
            raise AssertionError("not an augmenting path")
        for k in range(0, len(path) - 1):
            a, b = path[k], path[k + 1]
            if b not in self.adj[a] or (mate[a] == b) != (k % 2 == 1):
                raise AssertionError("not alternating")
        for k in range(0, len(path) - 1, 2):
            a, b = path[k], path[k + 1]
            mate[a], mate[b] = b, a
        stack = list(path)
        while stack:
            v = stack.pop()
            if self.erased[v]:
                continue
            self.erased[v] = True
            for s in self.succ[v]:
                self.pred_left[s] -= 1
                if self.pred_left[s] == 0:
                    stack.append(s)
