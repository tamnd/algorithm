# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fine-grained-concurrent-heap/. The authors are listed in prov/5B1WV2.jsonl.

import random
import threading
from collections import Counter

import pytest
from fine_grained_concurrent_heap import AVAILABLE, EMPTY, EMPTY_HEAP, SPIN, ConcurrentHeap, bit_reversed

# ---- deterministic interleaving driver and linearizability check ----

Op = tuple  # (thread, name, arg, result, invoke time, response time)


def interleave(threads, schedule, limit=100000):
    """Run the operations of each thread, one atomic step at a time.

    threads[t] is a list of (name, arg, make) where make() returns the step
    generator of the operation. schedule is a sequence of thread numbers; a
    pick of a thread with no work left is skipped. After the schedule, the
    remaining steps run round robin. Returns the history as a list of Op.
    """
    todo = [list(reversed(ops)) for ops in threads]
    cur: list = [None] * len(threads)
    history: list = []
    clock = 0

    def step(t):
        nonlocal clock
        if cur[t] is None:
            if not todo[t]:
                return False
            name, arg, make = todo[t].pop()
            cur[t] = (name, arg, make(), clock)
        name, arg, gen, inv = cur[t]
        clock += 1
        try:
            next(gen)
        except StopIteration as stop:
            history.append((t, name, arg, stop.value, inv, clock))
            cur[t] = None
        return True

    for t in schedule:
        step(t)
    steps = 0
    while any(cur) or any(todo):
        for t in range(len(threads)):
            step(t)
        steps += 1
        assert steps < limit, "no progress"
    return history


def linearizable(history, init, apply):
    """Wing and Gong search: is there a legal order that respects real time?

    apply(state, name, arg) returns (new state, result); states are hashable.
    """
    n = len(history)
    full = (1 << n) - 1
    seen = set()

    def dfs(done, state):
        if done == full:
            return True
        if (done, state) in seen:
            return False
        seen.add((done, state))
        for i in range(n):
            if done >> i & 1:
                continue
            inv_i = history[i][4]
            if any(not done >> j & 1 and history[j][5] < inv_i for j in range(n)):
                continue
            s2, r = apply(state, history[i][1], history[i][2])
            if r == history[i][3] and dfs(done | 1 << i, s2):
                return True
        return False

    return dfs(0, init)


def exact_apply(state, name, arg):
    """The exact sequential priority queue on a sorted tuple."""
    if name == "insert":
        return tuple(sorted(state + (arg,))), None
    if not state:
        return state, EMPTY_HEAP
    return state[1:], state[0]


def finish(gen):
    try:
        while True:
            next(gen)
    except StopIteration as stop:
        return stop.value


# ---- tests ----


def test_bit_reversed_order():
    assert [bit_reversed(n) for n in range(1, 16)] == [1, 2, 3, 4, 6, 5, 7, 8, 12, 10, 14, 9, 13, 11, 15]
    # consecutive slots of a level alternate between the left and right subtrees of the root
    assert [bit_reversed(n) < 6 for n in range(4, 8)] == [True, False, True, False]


def test_example():
    h = ConcurrentHeap(4)
    for x in (2, 5, 4, 8, 9, 6):
        h.insert(x)
    # slots 1..7: 2, 5, 4, 8, 6, 9, empty (slot 5 holds the sixth item, slot 6 the fifth)
    assert [h.slots[i].pri for i in range(1, 7)] == [2, 5, 4, 8, 6, 9]
    ins = h.insert_steps(1, me=7)
    for _ in range(6):
        next(ins)  # the item 1 is in slot 7 (bit_reversed(7)), tagged with the inserter
    assert h.slots[7].pri == 1 and h.slots[7].tag == 7
    assert finish(ins) is None  # moves up: slot 7, slot 3, slot 1
    assert [h.slots[i].pri for i in (1, 3, 7)] == [1, 2, 4]
    assert h.delete_min() == 1  # the bottom item, 4 from slot 7, goes to the root and down
    assert [h.slots[i].pri for i in range(1, 7)] == [2, 5, 4, 8, 6, 9]
    h.check_invariant()


def test_two_deletes_are_not_linearizable():
    h = ConcurrentHeap(3)
    for x in (0, 1, 13):
        h.insert(x)  # slots 1, 2, 3
    a = h.delete_min_steps()
    while h.slots[1].pri != 13:
        next(a)  # a took 13 from slot 3 and swapped it with the root, 0
    b = h.delete_min_steps()
    while next(b) != SPIN:
        pass  # b took 1 from slot 2 and waits for the root lock
    assert finish(a) == 0  # a finds slot 2 empty and stops with 13 at the root
    assert finish(b) == 13  # b returns the root, 13, and puts 1 there
    assert h.items() == [1]
    h.check_invariant()
    history = [(0, "delete_min", None, 0, 0, 3), (1, "delete_min", None, 13, 1, 4)]
    assert not linearizable(history, (0, 1, 13), exact_apply)


def test_empty_while_an_item_is_held():
    h = ConcurrentHeap(3)
    for x in (2, 5):
        h.insert(x)  # slots 1 and 2
    d1 = h.delete_min_steps()
    while h.slots[2].tag != EMPTY:
        next(d1)  # d1 took 5 from slot 2 and holds it
    assert finish(h.delete_min_steps()) == 2  # d2 takes the root, the last slot
    assert finish(h.delete_min_steps()) == EMPTY_HEAP  # d3 sees size 0, but 5 is in d1's hands
    finish(h.insert_steps(9, 1))  # the insert puts 9 at the root
    assert finish(d1) == 9  # d1 swaps 5 into the root and returns 9
    assert h.items() == [5]
    h.check_invariant()
    # all four calls overlap d1; no order of exact calls explains EMPTY while 5 stays
    history = [
        (0, "delete_min", None, 9, 0, 9),
        (1, "delete_min", None, 2, 1, 2),
        (2, "delete_min", None, EMPTY_HEAP, 3, 4),
        (3, "insert", 9, None, 5, 6),
    ]
    assert not linearizable(history, (2, 5), exact_apply)


def test_paused_insert_whose_path_empties():
    # An insert writes its item and pauses. Deletes move the item up past its slot and
    # then empty the slots below it. The insert must climb to its item, not stop at an
    # empty parent, or the tag stays and later inserts below it wait for ever.
    for seed in (1017, 1710):
        rng = random.Random(seed)
        h = ConcurrentHeap(6)
        for _ in range(rng.randrange(3, 30)):
            h.insert(rng.randrange(0, 1000), 99)
        paused = h.insert_steps(rng.randrange(0, 1000), 1)
        while not any(s.tag == 1 for s in h.slots):
            next(paused)
        next(paused)
        for _ in range(rng.randrange(1, 15)):
            finish(h.insert_steps(rng.randrange(0, 1000), 98))
        for _ in range(rng.randrange(1, 60)):
            finish(h.delete_min_steps())
        finish(paused)
        h.check_invariant()


def test_edges():
    h = ConcurrentHeap(2)
    assert h.delete_min() == EMPTY_HEAP
    for x in (3, 1, 2):
        h.insert(x)
    with pytest.raises(OverflowError):
        h.insert(0)
    h.check_invariant()
    assert [h.delete_min() for _ in range(4)] == [1, 2, 3, EMPTY_HEAP]
    assert all(s.tag == EMPTY for s in h.slots)
    h.insert(7)
    assert h.slots[1].tag == AVAILABLE and h.items() == [7]


def test_random_against_model():
    for seed in range(30):
        rng = random.Random(seed)
        h = ConcurrentHeap(7)
        model = []
        for _ in range(500):
            if rng.random() < 0.55 and h.size < h.capacity:
                x = rng.randrange(100)
                h.insert(x)
                model.append(x)
            else:
                x = h.delete_min()
                assert x == (min(model) if model else EMPTY_HEAP)
                if model:
                    model.remove(x)
        h.check_invariant()
        assert h.items() == sorted(model)


def test_random_interleavings_conserve_items():
    for seed in range(400):
        rng = random.Random(seed)
        h = ConcurrentHeap(5)
        init = [rng.randrange(20) for _ in range(rng.randrange(0, 6))]
        for x in init:
            h.insert(x, 9)
        threads = []
        for t in range(3):
            ops = []
            for _ in range(rng.randrange(1, 4)):
                if rng.random() < 0.5:
                    x = rng.randrange(20)
                    ops.append(("insert", x, lambda x=x, t=t: h.insert_steps(x, t + 1)))
                else:
                    ops.append(("delete_min", None, h.delete_min_steps))
            threads.append(ops)
        history = interleave(threads, [rng.randrange(3) for _ in range(rng.randrange(10, 200))])
        h.check_invariant()  # a quiescent heap is a valid heap
        inserted = Counter(init) + Counter(e[2] for e in history if e[1] == "insert")
        taken = Counter(e[3] for e in history if e[1] == "delete_min" and e[3] != EMPTY_HEAP)
        assert not taken - inserted  # every item returned was inserted, and at most once
        assert Counter(h.items()) == inserted - taken  # nothing is lost
        # a call that overlaps no other call behaves like the sequential queue
        for e in history:
            if not any(f is not e and f[4] < e[5] and e[4] < f[5] for f in history):
                before = [f for f in history if f[5] <= e[4]]
                state = Counter(init) + Counter(f[2] for f in before if f[1] == "insert")
                state -= Counter(f[3] for f in before if f[1] == "delete_min" and f[3] != EMPTY_HEAP)
                if e[1] == "delete_min":
                    assert e[3] == (min(state.elements()) if state else EMPTY_HEAP)


def test_threads():
    h = ConcurrentHeap(12)
    out = [[] for _ in range(4)]

    def worker(w):
        for i in range(400):
            h.insert(w * 1000 + i, me=w + 1)
            if i % 2:
                out[w].append(h.delete_min())

    ts = [threading.Thread(target=worker, args=(w,)) for w in range(4)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    h.check_invariant()
    taken = [x for o in out for x in o]
    assert EMPTY_HEAP not in taken
    assert sorted(taken + h.items()) == sorted(w * 1000 + i for w in range(4) for i in range(400))
