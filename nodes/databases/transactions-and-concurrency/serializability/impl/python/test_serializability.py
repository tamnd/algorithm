# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/serializability/. The authors are listed in prov/YQV7PJ.jsonl.

import random

from serializability import (
    avoids_cascading_aborts,
    committed_projection,
    conflict_serializable,
    final_state_serializable,
    parse,
    reads_from,
    recoverable,
    strict,
    view_serializable,
)


def random_schedule(rng: random.Random, ntx: int, items: str, p_abort: float) -> list:
    tx = {}
    for t in range(1, ntx + 1):
        acts = [(rng.choice("rw"), t, rng.choice(items)) for _ in range(rng.randint(1, 3))]
        acts.append(("a" if rng.random() < p_abort else "c", t, None))
        tx[t] = acts
    out = []
    while any(tx.values()):
        t = rng.choice([t for t in tx if tx[t]])
        out.append(tx[t].pop(0))
    return out


def test_serializability_classes_of_examples() -> None:
    lost_update = parse("r1(x) r2(x) w1(x) w2(x) c1 c2")
    assert not final_state_serializable(lost_update)
    blind = parse("r1(x) w2(x) w1(x) w3(x) c1 c2 c3")
    assert view_serializable(blind) and not conflict_serializable(blind)
    dead_reads = parse("r2(x) w1(x) r2(x) c2 c1")
    assert final_state_serializable(dead_reads) and not view_serializable(dead_reads)
    # An aborted transaction does not count.
    assert conflict_serializable(parse("r1(x) r2(x) w1(x) w2(x) c1 a2"))


def test_recoverability_examples() -> None:
    not_rc = parse("w1(x) r2(x) c2 c1")
    assert reads_from(not_rc) == [(2, 1, 1)]
    assert not recoverable(not_rc)
    rc_not_aca = parse("w1(x) r2(x) c1 c2")
    assert recoverable(rc_not_aca) and not avoids_cascading_aborts(rc_not_aca)
    aca_not_st = parse("w1(x) w2(x) c1 c2")
    assert avoids_cascading_aborts(aca_not_st) and not strict(aca_not_st)
    st_not_csr = parse("r1(x) r2(y) w1(y) w2(x) c1 c2")
    assert strict(st_not_csr) and not conflict_serializable(st_not_csr)
    # After T2 aborts, T3 reads the value of T1 again.
    s = parse("w1(x) w2(x) a2 r3(x) c1 c3")
    assert reads_from(s) == [(3, 1, 3)]
    assert recoverable(s) and avoids_cascading_aborts(s) is False


def test_inclusions_on_random_schedules() -> None:
    rng = random.Random(12)
    counts = {"st": 0, "aca": 0, "rc": 0, "csr": 0, "vsr": 0, "fsr": 0}
    for _ in range(1500):
        s = random_schedule(rng, rng.randint(2, 3), "xy", 0.25)
        st, aca, rc = strict(s), avoids_cascading_aborts(s), recoverable(s)
        assert not st or aca
        assert not aca or rc
        csr, vsr, fsr = conflict_serializable(s), view_serializable(s), final_state_serializable(s)
        assert not csr or vsr
        assert not vsr or fsr
        for k, v in zip(counts, (st, aca, rc, csr, vsr, fsr)):
            counts[k] += v
    assert counts["st"] < counts["aca"] < counts["rc"] < 1500
    assert counts["csr"] < counts["vsr"] < counts["fsr"] < 1500


def test_projection() -> None:
    s = parse("w1(x) r2(x) a1 c2")
    assert committed_projection(s) == [("r", 2, "x")]
