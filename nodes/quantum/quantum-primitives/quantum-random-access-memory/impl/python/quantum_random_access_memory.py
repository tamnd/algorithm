# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-random-access-memory/. The authors are listed in prov/Q40QQ0.jsonl.
"""A bucket-brigade QRAM for N = 2^n classical bits (Giovannetti, Lloyd and Maccone 2008), simulated exactly.

The query maps |i>|b> to |i>|b xor x_i> for every address i in superposition.

Hardware. N - 1 routers in heap order: router 1 is the root, and router k has children 2k (direction 0)
and 2k + 1 (direction 1). Child number c >= N is memory cell c - N. Each router is a qutrit with the
states W (wait, inactive), 0 (route left) and 1 (route right). Between queries every router is W.

Query, for each basis state of the address register (bit n - 1 is the most significant):
1. Load: for j = 0 .. n - 1, the address qubit of bit n - 1 - j travels from the root along the active
   routers to the first W router, at depth j, and is swapped into it. After this the n routers on the
   path to cell i are active and the address slots hold W.
2. Copy: the bus qubit travels down the path, is flipped if x_i = 1, and travels back.
3. Unload: steps 1 in reverse, which returns the address qubits and resets every router to W.

Every step maps basis configurations to basis configurations one to one, so the query is a permutation
of the basis of (address slots, bus, routers), extended linearly to superpositions. The simulator applies
it branch by branch to a sparse state {configuration: amplitude}.

Qubit order on the interface: the address i is an integer whose bit 0 is the least significant, as in
qsim.py; the state is a dict {(i, b): amplitude}.
"""

W = 2  # the wait state of a router qutrit; 0 and 1 are the routing directions


class QRAM:
    def __init__(self, n: int, data: list[int] | None = None) -> None:
        if n < 1:
            raise ValueError("need at least one address qubit")
        self.n = n
        self.size = 1 << n
        self.data = [0] * self.size if data is None else [int(x) for x in data]
        if len(self.data) != self.size or any(x not in (0, 1) for x in self.data):
            raise ValueError("data must be N = 2^n bits")
        self.routers = [W] * self.size  # index 0 unused; routers 1 .. N - 1
        self.last_stats: dict = {}

    # classical interface
    def write(self, i: int, bit: int) -> None:
        if not 0 <= i < self.size or bit not in (0, 1):
            raise ValueError("bad address or bit")
        self.data[i] = bit

    def read(self, i: int) -> int:
        return self.data[i]

    def check_invariant(self) -> None:
        assert len(self.data) == self.size and all(x in (0, 1) for x in self.data)
        assert all(r == W for r in self.routers[1:]), "a router is still active between queries"

    # one basis branch of the bucket brigade
    def _follow(self, routers: list[int], depth: int) -> int:
        """Follow active routers from the root for depth hops; return the node reached."""
        node = 1
        for _ in range(depth):
            if routers[node] == W:
                raise RuntimeError("the path is broken")
            node = 2 * node + routers[node]
        return node

    def _branch(self, i: int, b: int, stop_after_load: bool = False):
        n = self.n
        slots = [(i >> (n - 1 - j)) & 1 for j in range(n)]  # slot j holds address bit n - 1 - j
        routers = list(self.routers)
        steps = 0
        active_max = 0
        for j in range(n):  # load, most significant bit first
            node = self._follow(routers, j)
            if routers[node] != W:
                raise RuntimeError("the target router is busy")
            routers[node], slots[j] = slots[j], W
            steps += j + 1  # j hops and one swap
            active_max = max(active_max, sum(1 for r in routers[1:] if r != W))
        if stop_after_load:
            return tuple(slots), b, tuple(routers)
        leaf = self._follow(routers, n - 1)
        cell = 2 * leaf + routers[leaf] - self.size
        b ^= self.data[cell]  # the bus goes down n hops, is flipped by the cell, and comes back
        steps += 2 * n + 1
        for j in reversed(range(n)):  # unload, in reverse order
            node = self._follow(routers, j)
            routers[node], slots[j] = W, routers[node]
            steps += j + 1
        if any(s == W for s in slots) or any(r != W for r in routers[1:]):
            raise RuntimeError("the query did not clean up")
        i_out = sum(s << (n - 1 - j) for j, s in enumerate(slots))
        return i_out, b, steps, active_max, cell

    def query(self, state: dict) -> dict:
        """Apply |i>|b> -> |i>|b xor x_i> to a sparse state {(i, b): amplitude}."""
        self.check_invariant()
        out: dict = {}
        steps = active = 0
        for (i, b), amp in state.items():
            if not 0 <= i < self.size or b not in (0, 1):
                raise ValueError("bad basis state")
            i2, b2, s, a, _ = self._branch(i, b)
            out[(i2, b2)] = out.get((i2, b2), 0) + amp
            steps, active = max(steps, s), max(active, a)
        self.last_stats = {"steps": steps, "active_routers": active}
        self.check_invariant()
        return out

    def router_state_after_load(self, i: int) -> tuple:
        """The router configuration in the middle of a query on address i (for the tests)."""
        return self._branch(i, 0, stop_after_load=True)[2]


def serial_steps(n: int) -> int:
    """Hops and swaps of one query without pipelining: n(n + 1) for load and unload, 2n + 1 for the bus."""
    return n * (n + 1) + 2 * n + 1


def oracle(data: list[int], state: dict) -> dict:
    """The reference map |i>|b> -> |i>|b xor x_i>."""
    out: dict = {}
    for (i, b), amp in state.items():
        key = (i, b ^ data[i])
        out[key] = out.get(key, 0) + amp
    return out
