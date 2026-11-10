# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/itai-rodeh/. The authors are listed in prov/Y6D4ZP.jsonl.

from itai_rodeh import itai_rodeh, unique_max_probability


def harmonic(n: int) -> float:
    return sum(1 / k for k in range(1, n + 1))


def round_bound(n: int) -> float:
    return (1 - 1 / n) ** (-n) if n > 1 else 1.0


def test_page_example() -> None:
    res = itai_rodeh(4, 0, "sync", draws=[[3, 2], [1], [3, 4], [2]])
    assert res["leaders"] == [2] and res["rounds"] == 2
    assert res["messages"] == 16 and res["elected_at"] == 8


def test_sync_schedule() -> None:
    for n in range(1, 30):
        for seed in range(10):
            res = itai_rodeh(n, seed, "sync")
            assert len(res["leaders"]) == 1 and res["elected_at"] is not None


def test_one_leader_all_schedules() -> None:
    for n in range(1, 13):
        for seed in range(40):
            for schedule in ("random", "first", "last"):
                res = itai_rodeh(n, seed, schedule)
                assert len(res["leaders"]) == 1
                assert res["active"] == res["leaders"]


def test_large_rings() -> None:
    for n in (50, 100, 200):
        for seed in range(3):
            res = itai_rodeh(n, seed)
            assert len(res["leaders"]) == 1


def test_mean_messages_within_bound() -> None:
    for n in (2, 3, 5, 8, 16, 32):
        runs = [itai_rodeh(n, seed) for seed in range(300)]
        mean_messages = sum(r["messages"] for r in runs) / len(runs)
        mean_rounds = sum(r["rounds"] for r in runs) / len(runs)
        assert mean_rounds <= round_bound(n) * 1.15
        assert mean_messages <= round_bound(n) * n * (harmonic(n) + 1)


def test_unique_max_probability_bound() -> None:
    for n in range(2, 60):
        for k in range(2, n + 1):
            assert unique_max_probability(k, n) >= (1 - 1 / n) ** k - 1e-12
        assert (1 - 1 / n) ** n >= 0.25 - 1e-12
