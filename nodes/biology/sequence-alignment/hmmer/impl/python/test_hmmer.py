# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hmmer/. The authors are listed in prov/DR111J.jsonl.

import math
import random
from fractions import Fraction as F
from typing import Dict, List

from hmmer import (
    Calibration,
    Plan7Core,
    bits,
    calibrate,
    configure,
    core_from_msa,
    exp_surv,
    fit_gumbel,
    fit_gumbel_mu,
    forward_odds,
    gumbel_surv,
    hmmsearch,
    msv_odds,
    null_odds,
    random_core,
    random_seq,
    sample_homolog,
    viterbi_odds,
)

MSA = ["TATA-AT", "TATG-AA", "TATG-AT", "CATAGAT", "TA-A-GT", "TGTGTAC"]
UNIFORM = {a: F(1, 4) for a in "ACGT"}


def exact_core(rng: random.Random, m: int, alphabet: str) -> Plan7Core:
    def dist(keys: List[str]) -> Dict[str, F]:
        w = {key: rng.randint(1, 9) for key in keys}
        s = sum(w.values())
        return {key: F(v, s) for key, v in w.items()}

    bg = dist(list(alphabet))
    t = [{}] + [{**dist(["MM", "MI", "MD"]), **dist(["IM", "II"]), **dist(["DM", "DD"])} for _ in range(m)]
    return Plan7Core(m, alphabet, bg, [{}] + [dist(list(alphabet)) for _ in range(m)], t)


def path_weights(core: Plan7Core, x: str, L: int, msv: bool) -> List[F]:
    """Weights (odds) of all state paths of the local multihit profile, by depth-first search."""
    m, n = core.m, len(x)
    loop, move, half = F(L, L + 3), F(3, L + 3), F(1, 2)
    if msv:
        entry = [F(0)] + [F(2, m * (m + 1))] * m
    else:
        occ = [F(0), F(1)]
        for k in range(2, m + 1):
            t = core.t[k - 1]
            occ.append(occ[-1] * (t["MM"] + t["MI"]) + (1 - occ[-1]) * t["DM"])
        z = sum(occ[k] * (m - k + 1) for k in range(1, m + 1))
        entry = [F(0)] + [occ[k] / z for k in range(1, m + 1)]

    def odds(k: int, i: int) -> F:
        return core.match_emit[k][x[i]] / core.background[x[i]]

    out: List[F] = []

    def go(s: str, k: int, i: int, w: F) -> None:
        if s in "NJC":
            if i < n:
                go(s, k, i + 1, w * loop)
            if s == "C":
                if i == n:
                    out.append(w * move)
            else:
                go("B", 0, i, w * move)
        elif s == "B":
            for kk in range(1, m + 1):
                if i < n:
                    go("M", kk, i + 1, w * entry[kk] * odds(kk, i))
        elif s == "E":
            go("J", 0, i, w * half)
            go("C", 0, i, w * half)
        elif s == "M":
            go("E", 0, i, w)
            if k < m:
                if msv:
                    if i < n:
                        go("M", k + 1, i + 1, w * odds(k + 1, i))
                    return
                t = core.t[k]
                if i < n:
                    go("M", k + 1, i + 1, w * t["MM"] * odds(k + 1, i))
                    go("I", k, i + 1, w * t["MI"])
                go("D", k + 1, i, w * t["MD"])
        elif s == "I":
            t = core.t[k]
            if i < n:
                go("M", k + 1, i + 1, w * t["IM"] * odds(k + 1, i))
                go("I", k, i + 1, w * t["II"])
        elif s == "D":
            go("E", 0, i, w)
            if k < m:
                t = core.t[k]
                if i < n:
                    go("M", k + 1, i + 1, w * t["DM"] * odds(k + 1, i))
                go("D", k + 1, i, w * t["DD"])

    go("N", 0, 0, F(1))
    return out


def test_example() -> None:
    core = core_from_msa(MSA, "ACGT", UNIFORM)
    assert core.m == 6
    assert core.t[2]["MM"] == F(6, 9) and core.t[2]["MD"] == F(2, 9)
    assert core.t[3]["DM"] == F(2, 3) and core.t[4]["MI"] == F(3, 9)
    x = "GCGCTATAATGCGC"
    p = configure(core, len(x), exact=True)
    v, f, s = viterbi_odds(p, x), forward_odds(p, x), msv_odds(p, x)
    assert 0 < v < f
    assert round(bits(f, len(x)), 3) == 1.138
    assert round(bits(v, len(x)), 3) == -2.835
    assert round(bits(s, len(x)), 3) == -0.456
    assert p.entry[1] == F(1259712, 23124869)
    assert sample_homolog(core, random.Random(1))


def test_edges() -> None:
    core = core_from_msa(MSA, "ACGT", UNIFORM)
    p = configure(core, 0, exact=True)
    assert forward_odds(p, "") == 0 and viterbi_odds(p, "") == 0 and msv_odds(p, "") == 0
    assert bits(F(0), 5) == -math.inf
    one = core_from_msa(["A", "A"], "AC", {"A": F(1, 2), "C": F(1, 2)})
    p = configure(one, 1, exact=True)
    # N -> B -> M1 -> E -> C -> T: move * 1 * (3/2) * 1/2 * move
    assert forward_odds(p, "A") == F(3, 4) * F(3, 4) * F(3, 2) * F(1, 2)
    assert null_odds(1, F(1)) == F(1, 4)
    assert exp_surv(0.0, 1.0, 0.7) == 1.0
    assert math.isclose(gumbel_surv(0.0, 0.0, 1.0), 1 - math.exp(-1))


def test_against_enumeration() -> None:
    rng = random.Random(2)
    for _ in range(500):
        alphabet = "AB" if rng.random() < 0.6 else "ACG"
        core = exact_core(rng, rng.randint(1, 3), alphabet)
        x = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 3)))
        L = rng.choice([len(x), 5, 100])
        p = configure(core, L, exact=True)
        ws = path_weights(core, x, L, msv=False)
        assert forward_odds(p, x) == sum(ws)
        assert viterbi_odds(p, x) == (max(ws) if ws else 0)
        ws = path_weights(core, x, L, msv=True)
        assert msv_odds(p, x) == (max(ws) if ws else 0)


def test_gumbel_fit() -> None:
    rng = random.Random(4)
    mu, lam = 3.0, 0.7
    xs = [mu - math.log(-math.log(rng.random())) / lam for _ in range(4000)]
    gmu, glam = fit_gumbel(xs)
    assert abs(glam - lam) < 0.05 and abs(gmu - mu) < 0.1
    assert abs(fit_gumbel_mu(xs, lam) - mu) < 0.1


def test_pipeline() -> None:
    rng = random.Random(8)
    bg = {a: 0.25 for a in "ACGT"}
    core = random_core(rng, 25, "ACGT", bg, sharp=10.0)
    cal = calibrate(core, rng, n_msv=60, l_msv=60, n_vit=60, l_vit=60, n_fwd=60, l_fwd=60)
    assert isinstance(cal, Calibration) and cal.lam > math.log(2)
    targets = [("r%d" % i, random_seq(rng, bg, rng.randint(20, 60))) for i in range(150)]
    for i in range(3):
        h = sample_homolog(core, rng)
        targets.append(("h%d" % i, random_seq(rng, bg, 15) + h + random_seq(rng, bg, 15)))
    full = hmmsearch(core, targets, cal, f1=1.0, f2=1.0, f3=1.0, report_e=math.inf)
    assert len(full.hits) == len(targets)
    filt = hmmsearch(core, targets, cal, report_e=math.inf)
    assert filt.passed["msv"] >= filt.passed["vit"] >= filt.passed["fwd"] == len(filt.hits)
    by_name = {h.name: h for h in full.hits}
    for h in filt.hits:
        g = by_name[h.name]
        assert (h.msv, h.vit, h.fwd, h.pvalue) == (g.msv, g.vit, g.fwd, g.pvalue)
        assert h.pvalue <= 1e-5
    names = {h.name for h in filt.hits}
    want = {
        h.name for h in full.hits
        if gumbel_surv(h.msv, cal.mu_msv, cal.lam) <= 0.02 and gumbel_surv(h.vit, cal.mu_vit, cal.lam) <= 1e-3 and h.pvalue <= 1e-5
    }
    assert names == want
    assert names & {"h0", "h1", "h2"}
    for h in full.hits:
        assert h.vit <= h.fwd + 1e-9
        assert math.isclose(h.evalue, h.pvalue * len(targets))
