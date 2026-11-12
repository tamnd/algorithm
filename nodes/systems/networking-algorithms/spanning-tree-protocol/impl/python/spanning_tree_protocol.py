# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spanning-tree-protocol/. The authors are listed in prov/6GA09P.jsonl.

"""The Spanning Tree Protocol of IEEE 802.1D (Perlman, 1985), in
synchronous rounds.

A bridged LAN is a set of bridges and a set of LANs (segments). A port
joins one bridge to one LAN and has an id, unique on its bridge, and a path
cost. Bridges exchange configuration BPDUs that carry the priority vector
(root id, root path cost, sender bridge id, sender port id) and a message
age. Smaller vectors are better. Each bridge picks the root, its root port
and its designated ports from the BPDUs it has stored; all other ports are
blocked. Stored information expires when its message age reaches MAXAGE,
which removes the information of a bridge that has failed.
"""

import heapq

ROOT, DESIGNATED, BLOCKED = "root", "designated", "blocked"


class Port:
    __slots__ = ("bridge", "lan", "pid", "cost", "info", "age", "fresh")

    def __init__(self, bridge, lan, pid, cost):
        self.bridge, self.lan, self.pid, self.cost = bridge, lan, pid, cost
        self.info = None     # stored vector (root, cost, bridge, port)
        self.age = 0         # its message age, advanced each round
        self.fresh = False   # a BPDU arrived on this port in the last round


class BridgedLAN:
    def __init__(self, ports, maxage=20):
        """ports: list of (bridge id, lan, port id, path cost)."""
        self.maxage = maxage
        self.ports = [Port(*p) for p in ports]
        self.bridges = sorted({p.bridge for p in self.ports})
        self.lans = sorted({p.lan for p in self.ports}, key=repr)
        self.by_bridge = {b: [p for p in self.ports if p.bridge == b] for b in self.bridges}
        self.by_lan = {l: [p for p in self.ports if p.lan == l] for l in self.lans}
        self.alive = set(self.bridges)
        self.root = {b: b for b in self.bridges}
        self.cost = {b: 0 for b in self.bridges}
        self.rootport = {b: None for b in self.bridges}
        self.role = {id(p): DESIGNATED for p in self.ports}
        self.rounds = 0

    def _decide(self, b):
        for p in self.by_bridge[b]:
            if p.info is not None and p.age >= self.maxage:
                p.info = None  # @line L1
        best, rp = (b, 0, b, 0, 0), None  # @line L2
        for p in self.by_bridge[b]:  # @line L3
            if p.info is not None:
                R, C, S, P = p.info
                cand = (R, C + p.cost, S, P, p.pid)
                if cand < best:
                    best, rp = cand, p  # @line L4
        self.root[b], self.cost[b] = best[0], best[1]  # @line L5
        self.rootport[b] = rp
        for p in self.by_bridge[b]:
            if p is rp:
                self.role[id(p)] = ROOT
            elif p.info is None or (best[0], best[1], b, p.pid) < p.info:
                self.role[id(p)] = DESIGNATED  # @line L6
            else:
                self.role[id(p)] = BLOCKED

    def step(self):
        """One round: every live bridge decides, then sends BPDUs."""
        self.rounds += 1
        for b in self.bridges:
            if b in self.alive:
                self._decide(b)
        out = []
        for b in self.bridges:
            if b not in self.alive:
                continue
            rp = self.rootport[b]
            if rp is None:
                age = 0
            elif rp.fresh:
                age = rp.age + 1
            else:
                continue                          # nothing to relay
            for p in self.by_bridge[b]:  # @line L7
                if self.role[id(p)] == DESIGNATED:
                    out.append((p, (self.root[b], self.cost[b], b, p.pid), age))  # @line L8
        for p in self.ports:
            p.fresh = False
            if p.info is not None:
                p.age += 1
        for src, vec, age in out:
            for q in self.by_lan[src.lan]:
                if q is src or q.bridge not in self.alive:
                    continue
                if (q.info is None or vec < q.info
                        or vec[2:] == q.info[2:]):  # @line L9
                    q.info, q.age, q.fresh = vec, age, True  # @line L10

    def fail_bridge(self, b):
        self.alive.discard(b)
        for p in self.by_bridge[b]:
            p.info = None

    def snapshot(self):
        return (tuple(sorted(self.root.items())), tuple(sorted(self.cost.items())),
                tuple(sorted((id(p), r) for p in self.ports for r in [self.role[id(p)]])))

    def run(self, max_rounds=1000, stable_for=None):
        """Run until the state has not changed for stable_for rounds."""
        stable_for = stable_for or self.maxage + 2
        last, same = None, 0
        for _ in range(max_rounds):
            self.step()
            s = self.snapshot()
            same = same + 1 if s == last else 0
            last = s
            if same >= stable_for:
                return True
        return False

    def active_edges(self):
        """(bridge, lan) pairs of the forwarding ports of live bridges."""
        return sorted(((p.bridge, p.lan) for p in self.ports
                       if p.bridge in self.alive and self.role[id(p)] != BLOCKED),
                      key=repr)


def centralized_tree(ports, alive=None):
    """The tree that 802.1D should reach, computed directly: the root is the
    least live bridge id of each component; root path costs by Dijkstra
    (crossing a LAN into bridge y costs y's port cost on it); each LAN's
    designated port is the least (cost, bridge, port); each other bridge's
    root port is the least (cost via that LAN, designated bridge,
    designated port, own port). Returns (root, cost, roles)."""
    ps = [p for p in ports if alive is None or p[0] in alive]
    bridges = sorted({p[0] for p in ps})
    on_lan, of_bridge = {}, {b: [] for b in bridges}
    for p in ps:
        on_lan.setdefault(p[1], []).append(p)
        of_bridge[p[0]].append(p)
    root, cost = {}, {}
    for r in bridges:          # the first bridge not yet reached is the
        if r in root:          # least id of its component
            continue
        dist, pq = {r: 0}, [(0, r)]
        while pq:
            d, x = heapq.heappop(pq)
            if d > dist[x]:
                continue
            for (_, lan, _, _) in of_bridge[x]:
                for (y, _, _, c) in on_lan[lan]:
                    if y != x and d + c < dist.get(y, float("inf")):
                        dist[y] = d + c
                        heapq.heappush(pq, (d + c, y))
        for x, d in dist.items():
            root[x], cost[x] = r, d
    desig = {lan: min((cost[b], b, pid) for (b, _, pid, _) in lst)
             for lan, lst in on_lan.items()}
    roles = {}
    for b in bridges:
        cands = []
        for (_, lan, pid, c) in of_bridge[b]:
            C, D, DP = desig[lan]
            if D != b:
                cands.append((C + c, D, DP, pid))
        rp = min(cands)[3] if root[b] != b else None
        for (_, lan, pid, c) in of_bridge[b]:
            if pid == rp:
                roles[(b, pid)] = ROOT
            elif desig[lan][1:] == (b, pid):
                roles[(b, pid)] = DESIGNATED
            else:
                roles[(b, pid)] = BLOCKED
    return root, cost, roles
