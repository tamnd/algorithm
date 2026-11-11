# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/test-and-set/. The authors are listed in prov/JZT9EK.jsonl.

from interleave import Config, explore, lasso, replay, starvation
from test_and_set import CONSENSUS_INIT, LOCK_INIT, consensus, decisions, lock_client


def test_two_process_consensus_over_all_interleavings() -> None:
    for inputs in ((0, 1), (1, 0), (0, 0), (1, 1)):
        g = explore([consensus(inputs)] * 2, CONSENSUS_INIT)
        finals = [h for h in g.histories if h is not None]
        assert finals and not g.stuck
        for h in finals:
            d = decisions(h)
            assert d[0] == d[1]  # agreement
            assert d[0] in inputs  # validity


def test_each_process_finishes_in_three_memory_steps() -> None:
    # wait-free: a process takes at most 5 steps (the inv mark, write, tas, read, the res mark)
    g = explore([consensus((0, 1))] * 2, CONSENSUS_INIT)
    depth = max(len(g.schedule(s)) for s in range(g.size()))
    assert depth == 9  # the winner skips the read


def naive_three(inputs):
    """A natural try for three processes; it must fail (Herlihy 1991 proves every try fails)."""
    inputs = tuple(inputs)

    def make(p):
        v = inputs[p]
        yield ("mark", "inv", ("propose", v))
        yield ("write", ("reg", p), v)
        lost = yield ("tas", "T")
        d = v
        if lost:
            q = (p + 1) % 3
            d = yield ("read", ("reg", q))
            if d is None:
                d = yield ("read", ("reg", (p + 2) % 3))
            del q
        yield ("mark", "res", d)
    return make


def test_three_process_attempt_disagrees() -> None:
    init = {**CONSENSUS_INIT, ("reg", 2): None}
    g = explore([naive_three((0, 1, 2))] * 3, init)
    bad = [h for h in g.histories if h is not None and len(set(decisions(h).values())) > 1]
    assert bad


def test_tas_lock_starvation_run() -> None:
    g = explore([lock_client(None)] * 2, LOCK_INIT)
    assert g.violation is None
    comps = starvation(g, 0)
    assert comps
    comp, inner = comps[0]
    # a cycle in which process 0 takes a step and process 1 enters the critical section
    prefix, cycle = lasso(g, comp, inner, [lambda s, e: e[0] == 0, lambda s, e: e[0] == 1 and e[5]])
    m = replay(Config([lock_client(None)] * 2, LOCK_INIT), prefix + cycle * 50)
    assert m.section[0] == "try"
    assert m.entries.count(1) >= 50 and 0 not in m.entries[-50:]
    assert any(p == 0 for p, _ in cycle)
