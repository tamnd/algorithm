# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/per-pixel-linked-lists/. The authors are listed in prov/XK6ZQN.jsonl.

"""Per-pixel linked lists for order-independent transparency.

The build pass appends each fragment to a list per pixel with two atomic
operations: a fetch-and-add on a global counter, which gives the fragment a
node in a shared pool, and an exchange on the head pointer of its pixel. The
resolve pass walks each list, sorts it by depth and blends back to front.

GPU threads are modeled as Python generators. Each `yield` ends one atomic
step, and a scheduler interleaves the steps of many threads at random, so the
tests can check the build for many interleavings. A fragment is (c, alpha, z)
with a premultiplied color c, an opacity alpha and a view depth z (smaller is
nearer). The arithmetic works on floats or fractions.Fraction values.
"""

import random
from typing import Iterator, List, Optional, Sequence, Tuple

NULL = -1
Fragment = tuple  # (c, alpha, z)


class FragmentLists:
    """The head pointer image, the atomic counter and the node pool."""

    def __init__(self, num_pixels: int, capacity: int) -> None:
        self.capacity = capacity
        self.head = [NULL] * num_pixels  # @line L1
        self.counter = 0
        self.frag: List[Optional[Fragment]] = [None] * capacity
        self.next = [NULL] * capacity
        self.exchange_log: List[Tuple[int, int]] = []  # (pixel, node), for the tests

    def atomic_add(self) -> int:
        old = self.counter
        self.counter = old + 1
        return old

    def atomic_exchange(self, q: int, value: int) -> int:
        old = self.head[q]
        self.head[q] = value
        self.exchange_log.append((q, value))
        return old


def insert(store: FragmentLists, q: int, fragment: Fragment) -> Iterator[None]:
    """One fragment-shader thread. The generator returns the node index, or
    NULL if the pool was full and the fragment was dropped."""
    idx = store.atomic_add()  # @line L2
    yield
    if idx >= store.capacity:  # @line L3
        return NULL
    store.frag[idx] = fragment  # @line L4
    yield
    old = store.atomic_exchange(q, idx)  # @line L5
    yield
    store.next[idx] = old
    return idx


def run_interleaved(threads: Sequence[Iterator[None]], rng: random.Random) -> list:
    """Run the threads to the end, one atomic step at a time, choosing the
    next thread at random. Returns the return value of each thread."""
    results = [None] * len(threads)
    live = list(range(len(threads)))
    while live:
        k = rng.randrange(len(live))
        t = live[k]
        try:
            next(threads[t])
        except StopIteration as stop:
            results[t] = stop.value
            live[k] = live[-1]
            live.pop()
    return results


def build(num_pixels: int, capacity: int, fragments: Sequence[Tuple[int, Fragment]], rng: random.Random):
    """Build the lists for (pixel, fragment) pairs with a random interleaving."""
    store = FragmentLists(num_pixels, capacity)
    threads = [insert(store, q, f) for q, f in fragments]
    nodes = run_interleaved(threads, rng)
    return store, nodes


def walk(store: FragmentLists, q: int) -> List[int]:
    out = []
    i = store.head[q]  # @line L6
    while i != NULL:  # @line L7
        out.append(i)
        i = store.next[i]
    return out


def insertion_sort_by_depth(frags: List[Fragment]) -> List[Fragment]:
    a = list(frags)
    for i in range(1, len(a)):  # @line L8
        x = a[i]
        j = i - 1
        while j >= 0 and a[j][2] > x[2]:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = x
    return a


def resolve_pixel(store: FragmentLists, q: int, background: tuple) -> tuple:
    a = insertion_sort_by_depth([store.frag[i] for i in walk(store, q)])
    result = tuple(background)
    for c, alpha, _ in reversed(a):  # @line L9
        result = tuple(ci + (1 - alpha) * ri for ci, ri in zip(c, result))
    return result  # @line L10


def resolve(store: FragmentLists, background: tuple) -> list:
    return [resolve_pixel(store, q, background) for q in range(len(store.head))]


def over_composite(frags: Sequence[Fragment], background: tuple) -> tuple:
    """The reference: Python's sort, then the over operator back to front."""
    result = tuple(background)
    for c, alpha, _ in sorted(frags, key=lambda f: f[2], reverse=True):
        result = tuple(ci + (1 - alpha) * ri for ci, ri in zip(c, result))
    return result
