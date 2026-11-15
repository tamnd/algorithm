# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coverage-guided-fuzzing/. The authors are listed in prov/6GRW00.jsonl.

import random

import toyir
from coverage_guided_fuzzing import bucket, cull, edges_of, execute, fuzz, random_testing

PAGE = """
# params: a, b, c
entry:
  t = a == 17
  br t l1 out
l1:
  d = b - a
  t = d == 4
  br t l2 out
l2:
  e = c - 100
  z = a / e
  ret z
out:
  ret 0
"""

COUNT = """
# params: n
entry:
  i = 0
  jump head
head:
  t = i < n
  br t body exit
body:
  i = i + 1
  jump head
exit:
  ret i
"""


def check_coverage_properties(prog, res, nseeds):
    cfg = set(toyir.edges(prog))
    # Every covered edge is an edge of the control flow graph.
    assert edges_of(res.virgin) <= cfg
    assert edges_of(res.crash_virgin) <= cfg
    # Replaying the queue gives the same coverage, entry by entry and in total.
    union = set()
    for i, q in enumerate(res.queue):
        kind, cov, steps = execute(prog, q.args)
        assert cov == q.cov and steps == q.steps
        if i >= nseeds:
            # An entry was kept only because it added coverage.
            assert kind == "ret"
            assert cov - union
        union |= cov
    assert union == res.virgin
    # Every saved crash is a real trap, and every crash after the first
    # added coverage among the crashes.
    seen = set()
    for i, x in enumerate(res.crashes):
        assert toyir.run(prog, x) == ("trap",)
        kind, cov, _ = execute(prog, x)
        assert kind == "trap"
        assert i == 0 or cov - seen
        seen |= cov
    assert seen == res.crash_virgin
    # The favored entries cover every edge that the queue covers.
    fav = cull(res.queue)
    covered = set()
    for i in fav:
        covered |= edges_of(res.queue[i].cov)
    assert covered == edges_of(res.virgin)


def test_buckets():
    expected = {1: 1, 2: 2, 3: 3, 4: 4, 7: 4, 8: 8, 15: 8, 16: 16, 31: 16, 32: 32, 127: 32, 128: 128, 1000: 128}
    for n, b in expected.items():
        assert bucket(n) == b


def test_hit_counts():
    prog = toyir.parse(COUNT)
    kind, cov, steps = execute(prog, (10,))
    assert kind == "ret"
    assert dict(cov) == {
        ("entry", "head"): 1,
        ("head", "body"): 8,
        ("body", "head"): 8,
        ("head", "exit"): 1,
    }
    # Runs of 4 and 7 trips fall in the same buckets, so they look the same.
    assert execute(prog, (4,))[1] == execute(prog, (7,))[1]
    assert execute(prog, (3,))[1] != execute(prog, (4,))[1]


def test_page_example():
    prog = toyir.parse(PAGE)
    res = fuzz(prog, [(0, 0, 0)], max_execs=20000, seed=0)
    assert [(q.args, q.found_at) for q in res.queue] == [
        ((0, 0, 0), 1),
        ((17, 0, 0), 58),
        ((17, 21, 0), 426),
    ]
    assert res.crashes == [(17, 21, 100)]
    assert res.first_crash == 841
    assert res.execs == 20000
    check_coverage_properties(prog, res, 1)
    edges, first_crash = random_testing(prog, max_execs=20000, seed=0)
    assert first_crash is None


def test_hit_count_buckets_drive_the_queue():
    prog = toyir.parse(COUNT)
    res = fuzz(prog, [(0,)], max_execs=3000, seed=1)
    check_coverage_properties(prog, res, 1)
    seen = {b for q in res.queue for (e, b) in q.cov if e == ("head", "body")}
    assert {1, 2, 3, 4, 8, 16, 32} <= seen


def test_same_seed_same_result():
    prog = toyir.parse(PAGE)
    a = fuzz(prog, [(5, 5, 5)], max_execs=3000, seed=42)
    b = fuzz(prog, [(5, 5, 5)], max_execs=3000, seed=42)
    assert [q.args for q in a.queue] == [q.args for q in b.queue]
    assert a.crashes == b.crashes and a.virgin == b.virgin


def test_random_programs():
    rng = random.Random(20261115)
    for t in range(16):
        acyclic = t % 2 == 0
        prog = toyir.random_program(rng, rng.randint(2, 4), rng.randint(3, 8), acyclic=acyclic)
        seeds = [(0, 0), (rng.randint(-5, 5), rng.randint(-5, 5))]
        res = fuzz(prog, seeds, max_execs=1500, seed=t)
        assert res.execs <= 1500
        check_coverage_properties(prog, res, len(seeds))
