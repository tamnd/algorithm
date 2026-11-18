# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dbmin/. The authors are listed in prov/DPJZ9M.jsonl.

"""DBMIN buffer management (Chou and DeWitt 1985), for read-only page requests.

The pool has N frames. Every page in memory is in the global table. A page is
owned by at most one locality set; a page with no owner is on the global free
list, which also holds the empty frames. Each file instance of an active query
has a locality set with a bound l, a current size r <= l, and a local policy
(lru, mru or fifo). A query is admitted only if the bounds of all active sets
plus its own add up to less than N.
"""

from collections import OrderedDict, deque
from typing import Deque, Dict, List, Optional, Tuple

POLICIES = ("lru", "mru", "fifo")
SetId = Tuple[object, object]   # (query, file instance)


class LocalitySet:
    def __init__(self, bound: int, policy: str) -> None:
        if bound < 1:
            raise ValueError("a locality set needs at least one buffer")
        if policy not in POLICIES:
            raise ValueError(f"unknown policy {policy}")
        self.bound = bound
        self.policy = policy
        # pages in policy order: by last use (lru, mru) or by arrival (fifo)
        self.pages: "OrderedDict[int, None]" = OrderedDict()

    @property
    def size(self) -> int:
        return len(self.pages)

    def use(self, p: int) -> None:
        if self.policy in ("lru", "mru"):
            self.pages.move_to_end(p)

    def victim(self) -> int:
        if self.policy == "mru":
            return next(reversed(self.pages))
        return next(iter(self.pages))


class DBMIN:
    def __init__(self, n_frames: int) -> None:
        self.N = n_frames
        self.owner: Dict[int, Optional[SetId]] = {}          # the global table
        self.free: Deque[Optional[int]] = deque([None] * n_frames)  # None is an empty frame
        self.sets: Dict[SetId, LocalitySet] = {}
        self.active: Dict[object, List[object]] = {}
        self.waiting: Deque[Tuple[object, Dict[object, Tuple[int, str]]]] = deque()
        self.reads = 0
        self.hits = 0

    # ------------------------------------------------------------ load control

    def demand(self) -> int:
        return sum(s.bound for s in self.sets.values())

    def start(self, q: object, files: Dict[object, Tuple[int, str]]) -> bool:
        """Admit query q with its file instances {name: (l, policy)}, or queue it."""
        if q in self.active or any(q == w for w, _ in self.waiting):
            raise ValueError(f"query {q} is already known")
        if not self.waiting and self._fits(files):           # @line L14
            self._activate(q, files)                          # @line L15
            return True
        self.waiting.append((q, files))                       # @line L16
        return False

    def _fits(self, files: Dict[object, Tuple[int, str]]) -> bool:
        return self.demand() + sum(l for l, _ in files.values()) < self.N

    def _activate(self, q: object, files: Dict[object, Tuple[int, str]]) -> None:
        self.active[q] = list(files)
        for name, (l, policy) in files.items():
            self.sets[(q, name)] = LocalitySet(l, policy)

    def finish(self, q: object) -> List[object]:
        """End query q, free its locality sets, and admit waiting queries that fit."""
        for name in self.active.pop(q):
            ls = self.sets.pop((q, name))
            for p in ls.pages:                                # @line L17
                self.owner[p] = None                          # @line L17
                self.free.append(p)                           # @line L17
        started = []
        while self.waiting and self._fits(self.waiting[0][1]):  # @line L18
            w, files = self.waiting.popleft()                 # @line L19
            self._activate(w, files)                          # @line L19
            started.append(w)
        return started

    # ------------------------------------------------------------ requests

    def request(self, q: object, name: object, p: int) -> bool:
        """Serve a request of query q on file instance name for page p. True on a hit."""
        sid = (q, name)
        ls = self.sets[sid]
        if p in self.owner:                                   # @line L1
            self.hits += 1
            if self.owner[p] == sid:                          # @line L2
                ls.use(p)                                     # @line L3
                return True                                   # @line L3
            if self.owner[p] is not None:                     # @line L4
                return True                                   # @line L5
            self.free.remove(p)                               # @line L6
            hit = True
        else:                                                 # @line L7
            old = self.free.popleft()                         # @line L8
            if old is not None:                               # @line L8
                del self.owner[old]                           # @line L8
            self.reads += 1                                   # @line L9
            hit = False
        if ls.size == ls.bound:                               # @line L10
            v = ls.victim()                                   # @line L11
            del ls.pages[v]                                   # @line L11 L12
            self.owner[v] = None                              # @line L11
            self.free.append(v)                               # @line L11
        self.owner[p] = sid                                   # @line L13
        ls.pages[p] = None                                    # @line L13
        return hit

    # ------------------------------------------------------------ checks

    def check(self) -> None:
        owned = [p for ls in self.sets.values() for p in ls.pages]
        assert len(owned) == len(set(owned)), "a page is in two locality sets"
        for sid, ls in self.sets.items():
            assert ls.size <= ls.bound
            assert all(self.owner[p] == sid for p in ls.pages)
        on_free = [p for p in self.free if p is not None]
        assert sorted(on_free + owned) == sorted(self.owner)
        assert all(self.owner[p] is None for p in on_free)
        assert len(self.free) + len(owned) == self.N
        assert self.demand() < self.N or not self.sets
