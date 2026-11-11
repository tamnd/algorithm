# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rumor-mongering/. The authors are listed in prov/97KQKR.jsonl.

import math
import random

from rumor_mongering import (Replica, deletion_scenario, residue_equation, rumor_jump_chain, rumor_mongering,
                             sir_final_size, sir_jump_chain)


def test_residue_equation_values() -> None:
    # Demers et al.: about 20% miss the rumor at k = 1 and about 6% at k = 2.
    assert abs(residue_equation(1) - 0.2032) < 1e-4
    assert abs(residue_equation(2) - 0.0595) < 1e-4
    for k in (1, 2, 3, 5):
        s = residue_equation(k)
        assert abs(s - math.exp(-(k + 1) * (1 - s))) < 1e-12


def test_jump_chain_matches_the_equation() -> None:
    n = 1000
    for k, trials in ((1, 60), (2, 40)):
        runs = [rumor_jump_chain(n, k, random.Random(10 * k + s)) / n for s in range(trials)]
        major = [x for x in runs if x < 0.9]
        assert len(major) >= 0.8 * trials
        assert abs(sum(major) / len(major) - residue_equation(k)) < 0.012


def test_lockstep_push_variants_match_demers_tables() -> None:
    # Table 2 (blind, coin): residue 0.20 at k = 2, 0.060 at k = 3.
    # Table 1 (feedback, counter): residue 0.18 at k = 1, traffic 1.7.
    def mean(k, feedback, counter, trials=8):
        res = [rumor_mongering(1000, k, random.Random(100 * k + s), feedback=feedback, counter=counter)
               for s in range(trials)]
        return sum(o.residue for o in res) / trials, sum(o.traffic for o in res) / trials

    s, m = mean(2, False, False)
    assert abs(s - 0.20) < 0.04 and abs(m - 1.6) < 0.2
    s, m = mean(1, True, True)
    assert abs(s - 0.18) < 0.03 and abs(m - 1.7) < 0.15
    s3, _ = mean(3, True, True)
    assert s3 < 0.03


def test_residue_is_about_e_to_minus_traffic() -> None:
    # The same relation s = e^(-m) for every push variant.
    for k, fb, ct in ((2, True, True), (3, False, False), (2, True, False)):
        for seed in range(3):
            o = rumor_mongering(1000, k, random.Random(seed), feedback=fb, counter=ct)
            assert abs(o.residue - math.exp(-o.traffic)) < 0.03


def test_counter_reset_matches_table_1() -> None:
    # Table 1 at k = 2: residue 0.037, traffic 3.3. Without the reset the residue is larger.
    def mean(reset, trials=10):
        res = [rumor_mongering(1000, 2, random.Random(2000 + s), reset=reset) for s in range(trials)]
        return sum(o.residue for o in res) / trials, sum(o.traffic for o in res) / trials

    s, m = mean(True)
    assert abs(s - 0.037) < 0.01 and abs(m - 3.3) < 0.15
    s0, m0 = mean(False)
    assert s0 > s and m0 < m


def test_outcome_fields_are_consistent() -> None:
    o = rumor_mongering(500, 2, random.Random(1))
    assert 0 <= o.residue < 1 and o.t_ave <= o.t_last <= o.cycles
    assert rumor_mongering(500, 2, random.Random(1)) == o


def test_sir_final_size() -> None:
    assert abs(sir_final_size(2.0) - 0.2032) < 1e-4
    n = 1000
    for r0, trials in ((2.0, 80), (3.0, 60)):
        runs = [sir_jump_chain(n, r0, random.Random(s)) / n for s in range(trials)]
        major = [x for x in runs if x < 0.9]
        assert abs(sum(major) / len(major) - sir_final_size(r0)) < 0.015
        # A minor outbreak happens with probability about 1/r0.
        assert abs((trials - len(major)) / trials - 1 / r0) < 0.15


def test_death_certificates_prevent_resurrection() -> None:
    for seed in range(3):
        assert deletion_scenario("plain", random.Random(seed)) == 20
        assert deletion_scenario("timeout", random.Random(seed)) == 20
        assert deletion_scenario("dormant", random.Random(seed)) == 0


def test_certificate_beats_older_item_and_loses_to_newer_one() -> None:
    r = Replica(0, "dormant", tau1=5, tau2=50)
    r.write("x", "v1", 1)
    r.delete("x", 2, frozenset({0}))
    r.receive({"x": ("item", "v1", 1)}, 3, {})
    assert r.value("x") is None
    r.receive({"x": ("item", "v2", 9)}, 4, {})
    assert r.value("x") == "v2"


def test_dormant_activation_keeps_the_original_timestamp() -> None:
    r = Replica(0, "dormant", tau1=5, tau2=50)
    r.delete("x", 2, frozenset({0}))
    r.expire(10)
    assert "x" not in r.entries and r.dormant["x"] == (2, 2)
    r.receive({"x": ("item", "old", 1)}, 20, {})
    assert r.entries["x"] == ("cert", 2, 20)
    # A reinstatement written after the deletion still wins.
    r.receive({"x": ("item", "new", 15)}, 21, {})
    assert r.value("x") == "new"
