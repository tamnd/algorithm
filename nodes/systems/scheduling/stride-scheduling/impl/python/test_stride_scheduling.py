# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stride-scheduling/. The authors are listed in prov/RJMX01.jsonl.

import random

import pytest

from stride_scheduling import Stride, stride_schedule


def test_ostep_trace() -> None:
    # A, B and C hold 100, 50 and 250 tickets; stride1 = 10000 gives the
    # strides 100, 200 and 40. Ties go to the client that joined first.
    out = stride_schedule({"A": 100, "B": 50, "C": 250}, 8, stride1=10000)
    assert "".join(out) == "ABCCCACC"
    out = stride_schedule({"A": 100, "B": 50, "C": 250}, 80, stride1=10000)
    assert [out.count(x) for x in "ABC"] == [20, 10, 50]


def reference(tickets: dict[str, int], n: int) -> list[str]:
    """Linear scan over exact rational passes, no heap and no strides:
    pass_c = runs_c / t_c, ties to the earlier client."""
    from fractions import Fraction

    names = list(tickets)
    runs = {c: 0 for c in names}
    out = []
    for _ in range(n):
        c = min(names, key=lambda x: (Fraction(runs[x], tickets[x]), names.index(x)))
        runs[c] += 1
        out.append(c)
    return out


def test_matches_reference_and_error_bounds() -> None:
    rng = random.Random(1)
    for _ in range(60):
        k = rng.randrange(1, 7)
        tickets = {f"c{i}": rng.randrange(1, 21) for i in range(k)}
        total = sum(tickets.values())
        n = rng.randrange(1, 600)
        out = stride_schedule(tickets, n)
        assert out == reference(tickets, n)
        runs = {c: 0 for c in tickets}
        for q, c in enumerate(out, start=1):
            runs[c] += 1
            for i, ti in tickets.items():
                # per client: -k t_i / T <= a_i - q t_i / T <= 1
                assert -k * ti <= runs[i] * total - q * ti <= total
                for j, tj in tickets.items():
                    # pairwise: -t_i <= a_i t_j - a_j t_i <= t_j
                    assert -ti <= runs[i] * tj - runs[j] * ti <= tj


def test_pass_invariant() -> None:
    rng = random.Random(2)
    for _ in range(40):
        st = Stride(stride1=rng.choice([997, 1000, 7]))  # strides may be fractions
        for i in range(rng.randrange(1, 6)):
            st.join(f"c{i}", rng.randrange(1, 30))
        for _ in range(300):
            st.schedule()
            m = min(st.pass_.values())
            assert all(m <= st.pass_[c] <= m + st.stride[c] for c in st.pass_)


def test_error_is_constant_while_lottery_grows() -> None:
    # Two clients, 2:1. The stride error never reaches one quantum; a seeded
    # lottery on the same shares drifts by many quanta.
    out = stride_schedule({"A": 2, "B": 1}, 30000)
    worst = 0
    a = 0
    for q, c in enumerate(out, start=1):
        a += c == "A"
        worst = max(worst, abs(3 * a - 2 * q))
    assert worst < 3  # |a - 2q/3| < 1
    rng = random.Random(3)
    a, worst = 0, 0
    for q in range(1, 30001):
        a += rng.randrange(3) < 2
        worst = max(worst, abs(3 * a - 2 * q))
    assert worst > 3 * 20


def test_join_leave_and_change() -> None:
    st = Stride(stride1=60)
    st.join("A", 2)
    st.join("B", 1)
    first = [st.schedule() for _ in range(30)]
    assert first.count("A") == 20
    st.join("C", 3)  # joins at the global pass, not at pass 0
    after = [st.schedule() for _ in range(60)]
    assert abs(after.count("C") - 30) <= 2 and abs(after.count("A") - 20) <= 2
    remain = st.leave("C")
    assert remain >= 0
    later = [st.schedule() for _ in range(30)]
    assert "C" not in later and abs(later.count("A") - 20) <= 2
    st.set_tickets("B", 4)  # B now holds 4 of 6 tickets
    last = [st.schedule() for _ in range(60)]
    assert abs(last.count("B") - 40) <= 2


def test_edges() -> None:
    with pytest.raises(ValueError):
        Stride(0)
    st = Stride(10)
    with pytest.raises(ValueError):
        st.schedule()
    with pytest.raises(ValueError):
        st.join("A", 0)
    assert stride_schedule({"A": 3}, 4) == ["A"] * 4
    assert stride_schedule({}, 0) == []
