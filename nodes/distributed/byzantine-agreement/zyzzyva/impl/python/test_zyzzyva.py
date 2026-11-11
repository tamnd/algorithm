# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zyzzyva/. The authors are listed in prov/8FSV21.jsonl.

from zyzzyva import System, normal_case, random_view, scenario_1, scenario_2, violations


def test_fast_path_needs_all_3f_plus_1():
    path, msgs, delays = normal_case(4, 1)
    assert path == "fast" and delays == 3
    assert msgs == 1 + 3 + 4  # request, ORDER-REQ, spec responses


def test_two_phase_path_with_one_silent_replica():
    path, msgs, delays = normal_case(4, 1, silent=(3,))
    assert path == "two-phase" and delays == 5
    assert msgs == 1 + 2 + 3 + 3 + 3  # request, ORDER-REQ, responses, COMMIT, LOCAL-COMMIT


def test_two_silent_replicas_block_the_client():
    assert normal_case(4, 1, silent=(2, 3))[0] is None


def test_no_conflict_within_one_view():
    for seed in range(200):
        s = random_view(seed)
        assert violations(s.completed) == [], seed


def test_forged_certificate_is_rejected():
    s = System(4, 1, faulty={0})
    s.order(1, "a", [0, 1])
    fake = ("cc", 1, ("a",), frozenset({0, 1, 2}))  # replica 2 never signed (a)
    assert not s.valid_cc(fake)
    assert not s.commit(fake, [0, 1, 2, 3], "a")


def test_scenario_1_replayed():
    s = scenario_1()
    assert [(v, h, path) for v, h, _, path in s.completed] == [(2, ("b",), "fast"), (3, ("a",), "fast")]
    assert violations(s.completed) == [1]


def test_scenario_2_replayed():
    s = scenario_2()
    assert [(v, h, path) for v, h, _, path in s.completed] == [
        (2, ("b1",), "two-phase"),
        (3, ("a1", "a2"), "fast"),
    ]
    assert violations(s.completed) == [1]
