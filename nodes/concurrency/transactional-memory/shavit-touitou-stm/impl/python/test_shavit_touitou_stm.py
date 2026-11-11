# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shavit-touitou-stm/. The authors are listed in prov/9B9H5V.jsonl.

from shavit_touitou_stm import SUCCESS, ShavitTouitou, audit, increment, transfer
from stmsim import Memory, Run, bank, count, explore, opaque, random_run, read_sums


def setup_of(data, txs, tries=2, nprocs=None, max_attempts=None, helping=True, skip_equal=True):
    n = nprocs or len(txs)
    def setup():
        stm = ShavitTouitou(data, nprocs=n, max_attempts=max_attempts or 2 * (tries or 15), helping=helping,
                            skip_equal=skip_equal)
        return Memory(stm.memory()), [stm.run(p, *tx, tries=tries) for p, tx in enumerate(txs)]
    return setup


def check_opaque(data):
    def check(run, truncated):
        if truncated:
            return "too many steps"
        return None if opaque(run.history, data) else "not opaque"
    return check


def test_worked_example_helping():
    data = bank(3, 10)
    run = Run(setup_of(data, [transfer(0, 1, 3), transfer(1, 2, 5)]))
    run.steps(0, 6)  # p owns a0 and a1 (LL, status read and SC for each), then stops
    assert run.mem.w[("own", "a0")] == (0, 0) and run.mem.w[("own", "a1")] == (0, 0)
    assert run.finish(1)  # q fails at a1, releases, helps p's record to the end, then retries and commits
    w = run.mem.w
    assert w[("status", (0, 0))] == SUCCESS and w[("status", (1, 0))] == ("failure", "a1")
    assert (w["a0"], w["a1"], w["a2"]) == (7, 8, 15)
    assert all(w[("own", a)] is None for a in data)
    assert run.finish(0)  # p wakes up: its late steps change nothing, and it reports success
    assert (w["a0"], w["a1"], w["a2"]) == (7, 8, 15)
    assert count(run.history, "commit") == 2 and count(run.history, "abort") == 1
    assert opaque(run.history, data)


def test_exhaustive_two_increments():
    # Every interleaving of two increments with two attempts each, with failures and helping.
    # Two-word transactions are covered by random schedules: their state space has more than 10^6 states.
    opaque_check = check_opaque({"x": 0})
    def check(run, truncated):
        if run.mem.w["x"] != count(run.history, "commit"):
            return "lost update"
        return opaque_check(run, truncated)
    st = explore(setup_of({"x": 0}, [increment("x"), increment("x")], tries=2), check)
    assert st.failure is None and st.runs > 1000, st.failure


def test_without_the_value_test_an_update_is_lost():
    # A helper of p writes x = 1 and releases. p itself did its LL of x after that write, so its SC
    # still succeeds later, after q has taken x, and it wipes out q's write: two commits, x = 1.
    def check(run, truncated):
        return None if run.mem.w["x"] == count(run.history, "commit") else "lost update"
    st = explore(setup_of({"x": 0}, [increment("x"), increment("x")], tries=2, skip_equal=False), check)
    assert st.failure is not None and st.failure[0] == "lost update"


def test_two_transfers_random_schedules():
    data = bank(2, 10)
    for seed in range(300):
        run = random_run(setup_of(data, [transfer(0, 1, 3), transfer(1, 0, 5)], tries=2), seed)
        assert all(r is None for r in run.pending), seed
        assert opaque(run.history, data), seed
        assert run.mem.w["a0"] + run.mem.w["a1"] == 20


def test_bank_random_schedules():
    m, data = 3, bank(3, 10)
    for seed in range(150):
        def setup():
            stm = ShavitTouitou(data, nprocs=3, max_attempts=60)
            def proc(p):
                for k in range(3):
                    yield from stm.run(p, *transfer((p + k) % m, (p + k + 1) % m, k + 1))
                return (yield from stm.run(p, *audit(m)))
            return Memory(stm.memory()), [proc(p) for p in range(3)]
        run = random_run(setup, seed, max_steps=20000)
        assert all(r is None for r in run.pending), seed
        assert sum(run.mem.w[f"a{i}"] for i in range(m)) == 30
        assert run.out == [30, 30, 30]
        assert all(s == 30 for s in read_sums(run.history, m))
        assert all(run.mem.w[("own", f"a{i}")] is None for i in range(m))
        assert opaque(run.history, data), seed


def test_a_stopped_process_never_blocks_the_others():
    # p stops for ever after k steps, for every k. The others still finish, and the money is still all there.
    m, data = 3, bank(3, 10)
    txs = [transfer(0, 1, 3), transfer(1, 2, 5), transfer(2, 0, 7)]
    alone = Run(setup_of(data, txs[:1], tries=1, nprocs=3))
    assert alone.finish(0)
    for k in range(len(alone.trace)):
        for seed in range(5):
            run = random_run(setup_of(data, txs, tries=None), seed, crash={0: k})
            assert run.pending[1] is None and run.pending[2] is None, (k, seed)
            assert sum(run.mem.w[f"a{i}"] for i in range(m)) == 30


def test_without_helping_a_stopped_owner_blocks_the_others():
    data = bank(3, 10)
    for helping, commits in ((False, 0), (True, 1)):
        run = Run(setup_of(data, [transfer(0, 1, 3), transfer(1, 2, 5)], tries=5, helping=helping))
        run.steps(0, 6)  # p owns a0 and a1 and stops
        assert run.finish(1)
        assert count([ev for ev in run.history if ev[0][0] == 1], "commit") == commits
        if not helping:
            assert count(run.history, "abort") == 5 and run.mem.w[("own", "a1")] == (0, 0)


def test_late_helper_changes_nothing():
    # q starts to help p's record, stops just before its SC of the new value, and wakes up after p is done
    # and another transaction has changed the word. Its SC fails, because the word was written after its LL.
    data = bank(2, 10)
    stm = ShavitTouitou(data, nprocs=3, max_attempts=4)
    def helper():
        yield from stm.transaction((0, 0), False)  # the record of p, made when p started
    run = Run(lambda: (Memory(stm.memory()), [stm.run(0, *transfer(0, 1, 3)), helper(), stm.run(2, *transfer(0, 1, 1))]))
    while not (run.pending[1][0] == "sc" and run.pending[1][1] == "a0"):
        run.step(1)  # the helper acquires, decides, agrees on the old values and reaches its SC of a0
    assert run.finish(0) and run.finish(2)  # p finishes its record; then a second transfer runs
    assert (run.mem.w["a0"], run.mem.w["a1"]) == (6, 14)
    assert run.finish(1)
    assert (run.mem.w["a0"], run.mem.w["a1"]) == (6, 14)
