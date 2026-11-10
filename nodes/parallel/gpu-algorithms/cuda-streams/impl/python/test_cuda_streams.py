# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cuda-streams/. The authors are listed in prov/GVJ1ZR.jsonl.
import random
from fractions import Fraction as F

from cuda_streams import best_chunks, chunked_ops, engine_of, makespan, pipeline_time, simulate


def test_one_stream_is_serial():
    ops = [(0, "h2d", 4), (0, "kernel", 4), (0, "d2h", 4)]
    assert makespan(ops) == 12
    assert makespan(chunked_ops(1, 4, 4, 4)) == 12


def test_worked_example_issue_order():
    # job: 4 ms in, 4 ms kernel, 4 ms out, in 4 chunks of 1 ms each
    assert makespan(chunked_ops(4, 4, 4, 4, "depth"), copy_engines=2) == 6
    assert makespan(chunked_ops(4, 4, 4, 4, "breadth"), copy_engines=2) == 6
    assert makespan(chunked_ops(4, 4, 4, 4, "depth"), copy_engines=1) == 12
    assert makespan(chunked_ops(4, 4, 4, 4, "breadth"), copy_engines=1) == 8


def test_pipeline_formula_matches_simulation():
    rng = random.Random(3)
    for _ in range(200):
        m = rng.randrange(1, 12)
        h, k, d = (F(rng.randrange(1, 40)) for _ in range(3))
        o = F(rng.randrange(0, 5), 10)
        assert makespan(chunked_ops(m, h, k, d, "depth", o), 2) == pipeline_time(m, h, k, d, o)


def test_schedule_is_valid_and_bounded():
    rng = random.Random(11)
    for _ in range(200):
        ops = []
        for _ in range(rng.randrange(1, 15)):
            ops.append((rng.randrange(3), rng.choice(["h2d", "kernel", "d2h"]), F(rng.randrange(1, 9))))
        ce = rng.choice([1, 2])
        times = simulate(ops, ce)
        for i, (si, ti) in enumerate(times):
            assert ti - si == ops[i][2]
            for j in range(i):
                sj, tj = times[j]
                same_stream = ops[i][0] == ops[j][0]
                same_engine = engine_of(ops[i][1], ce) == engine_of(ops[j][1], ce)
                if same_stream or same_engine:
                    assert si >= tj            # in order, no overlap
        span = makespan(ops, ce)
        for e in {engine_of(kd, ce) for _, kd, _ in ops}:
            assert span >= sum(t for _, kd, t in ops if engine_of(kd, ce) == e)


def test_best_chunk_count_with_overhead():
    o = F(1, 10)
    assert pipeline_time(1, 4, 4, 4, o) == F(123, 10)
    assert pipeline_time(4, 4, 4, 4, o) == F(66, 10)
    assert pipeline_time(8, 4, 4, 4, o) == 6
    assert pipeline_time(9, 4, 4, 4, o) == F(539, 90)
    assert pipeline_time(10, 4, 4, 4, o) == 6
    assert best_chunks(4, 4, 4, o, 64) == 9
    assert pipeline_time(4, 4, 4, 4) == 6 and pipeline_time(1000, 4, 4, 4) > 4
