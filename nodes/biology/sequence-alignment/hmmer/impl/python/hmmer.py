# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hmmer/. The authors are listed in prov/DR111J.jsonl.
"""A small model of the HMMER3 search pipeline (hmmsearch): MSV filter, Viterbi filter, Forward.

The core model is a Plan 7 profile HMM with m nodes. Node k has a match state Mk, an insert
state Ik (k < m) and a delete state Dk, and seven transitions to node k + 1 or to itself:
MM, MI, MD, IM, II, DM, DD. There is no D -> I and no I -> D.

The search profile is the local multihit configuration of HMMER3:
  N -> N, J -> J, C -> C with probability L / (L + 3), and N -> B, J -> B, C -> T with 3 / (L + 3);
  B -> Mk with occ[k] / sum_i occ[i] (m - i + 1); Mk -> E and Dk -> E with odds 1 (local exit);
  E -> C and E -> J with 1/2 each.
N, C, J and the insert states emit with the background distribution, so their odds are 1.
All dynamic programming runs in odds space (probabilities divided by the background), which
works with float or Fraction numbers. The bit score is log2(odds / null), where the null model
emits L residues with P = (L / (L + 1))^L / (L + 1) in odds space.

Left out on purpose: the bias filter, the domain definition step and the null2 correction,
and the SIMD vector code. The filters here are the generic (scalar) recurrences.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Callable, Dict, List, Optional, Sequence, Tuple, Union

Num = Union[float, Fraction]
TKEYS = ("MM", "MI", "MD", "IM", "II", "DM", "DD")


@dataclass
class Plan7Core:
    """Core Plan 7 model. match_emit[k] and t[k] are used for k = 1..m (t[m] is ignored)."""

    m: int
    alphabet: str
    background: Dict[str, Num]
    match_emit: List[Dict[str, Num]]
    t: List[Dict[str, Num]]


def core_from_msa(msa: Sequence[str], alphabet: str, background: Dict[str, Num], symfrac: float = 0.5, pseudo: int = 1) -> Plan7Core:
    """Count states and transitions in an alignment, add `pseudo` to each count, normalize.

    A column is a match column when its fraction of residues is at least symfrac. Residues
    before the first or after the last match column are left out (the N and C states model
    them), and a D next to an I is not counted, because Plan 7 has no such transition.
    Cost O(rows * columns + m * |alphabet|).
    """
    rows = len(msa)
    matches = [c for c in range(len(msa[0])) if sum(r[c] != "-" for r in msa) >= symfrac * rows]
    m = len(matches)
    if m == 0:
        raise ValueError("no match columns")
    emit = [{a: Fraction(pseudo) for a in alphabet} for _ in range(m + 1)]
    tc = [{key: Fraction(pseudo) for key in TKEYS} for _ in range(m + 1)]
    is_match = set(matches)
    for row in msa:
        states: List[Tuple[str, int]] = []
        k = 0
        for c, ch in enumerate(row):
            if c in is_match:
                k += 1
                states.append(("M", k) if ch != "-" else ("D", k))
                if ch != "-":
                    emit[k][ch] += 1
            elif ch != "-" and 0 < k < m:
                states.append(("I", k))
        for (a, k), (b, _) in zip(states, states[1:]):
            key = a + b
            if key in TKEYS:
                tc[k][key] += 1
    t: List[Dict[str, Num]] = []
    for k in range(m + 1):
        row_t: Dict[str, Num] = {}
        for src in "MID":
            keys = [key for key in TKEYS if key[0] == src]
            total = sum(tc[k][key] for key in keys)
            for key in keys:
                row_t[key] = tc[k][key] / total
        t.append(row_t)
    match_emit = [{a: v / sum(e.values()) for a, v in e.items()} for e in emit]
    match_emit[0] = {}
    return Plan7Core(m, alphabet, dict(background), match_emit, t)


def random_core(rng: random.Random, m: int, alphabet: str, background: Dict[str, Num], sharp: float = 3.0) -> Plan7Core:
    """A random core model whose match states each prefer one residue. For tests and examples."""

    def dist(weights: Dict[str, float]) -> Dict[str, float]:
        s = sum(weights.values())
        return {a: w / s for a, w in weights.items()}

    match_emit: List[Dict[str, Num]] = [{}]
    t: List[Dict[str, Num]] = [{}]
    for _ in range(m):
        fav = rng.choice(alphabet)
        match_emit.append(dist({a: (sharp if a == fav else 0.0) + rng.random() for a in alphabet}))
        w = {"MM": 8 + rng.random(), "MI": rng.random() * 0.5, "MD": rng.random() * 0.5}
        wi = {"IM": 2 + rng.random(), "II": rng.random()}
        wd = {"DM": 2 + rng.random(), "DD": rng.random()}
        t.append({**dist(w), **dist(wi), **dist(wd)})
    return Plan7Core(m, alphabet, dict(background), match_emit, t)


def occupancy(core: Plan7Core) -> List[Num]:
    """occ[k], the probability that a global path through the core uses Mk. Cost O(m)."""
    occ: List[Num] = [0, core.match_emit[1][core.alphabet[0]] * 0 + 1] if core.m >= 1 else [0]
    for k in range(2, core.m + 1):
        tp = core.t[k - 1]
        occ.append(occ[k - 1] * (tp["MM"] + tp["MI"]) + (1 - occ[k - 1]) * tp["DM"])
    return occ


@dataclass
class Profile:
    """The local multihit search profile of a core model, configured for a target length L."""

    core: Plan7Core
    L: int
    entry: List[Num]  # B -> Mk, k = 1..m
    loop: Num  # N -> N, J -> J, C -> C
    move: Num  # N -> B, J -> B, C -> T
    msc: List[Dict[str, Num]] = field(default_factory=list)  # match odds e_k(a) / f(a)


def configure(core: Plan7Core, L: int, exact: bool = False) -> Profile:
    """Local multihit configuration for length L. Cost O(m |alphabet|)."""
    one: Num = Fraction(1) if exact else 1.0
    occ = occupancy(core)
    z = sum(occ[k] * (core.m - k + 1) for k in range(1, core.m + 1))
    entry = [one * 0] + [one * occ[k] / z for k in range(1, core.m + 1)]
    loop = one * L / (L + 3)
    move = one * 3 / (L + 3)
    msc = [{}] + [{a: one * core.match_emit[k][a] / core.background[a] for a in core.alphabet} for k in range(1, core.m + 1)]
    return Profile(core, L, entry, loop, move, msc)


def null_odds(L: int, one: Num = 1.0) -> Num:
    """P(x | null) / prod f(x_i): the null model has one state with self-loop L / (L + 1)."""
    return (one * L / (L + 1)) ** L / (L + 1)


def msv_odds(p: Profile, x: str) -> Num:
    """MSV: best sum of ungapped local segments (Viterbi without I and D, M -> M = 1).

    Uniform entry 2 / (m (m + 1)), E -> J = E -> C = 1/2. Cost O(m L) time, O(m) space.
    """
    m = p.core.m
    zero = p.loop * 0
    half = zero + Fraction(1, 2) if isinstance(zero, Fraction) else 0.5
    tbm = (zero + 2) / (m * (m + 1))
    prev = [zero] * (m + 1)
    n_, j_, c_ = zero + 1, zero, zero
    b_ = n_ * p.move
    for ch in x:
        cur = [zero] * (m + 1)
        for k in range(1, m + 1):
            cur[k] = p.msc[k][ch] * max(prev[k - 1], b_ * tbm)  # @line L20
        e_ = max(cur[1:]) if m else zero  # @line L21
        j_ = max(j_ * p.loop, e_ * half)  # @line L22
        c_ = max(c_ * p.loop, e_ * half)
        n_ = n_ * p.loop  # @line L23
        b_ = max(n_, j_) * p.move
        prev = cur
    return c_ * p.move


def _dp(p: Profile, x: str, op: Callable[[Sequence[Num]], Num]) -> Num:
    """Forward (op = sum) or Viterbi (op = max) on the local multihit Plan 7 profile.

    Cost O(m L) time and O(m) space (two rows).
    """
    core, m = p.core, p.core.m
    zero = p.loop * 0
    half = zero + Fraction(1, 2) if isinstance(zero, Fraction) else 0.5
    pm, pi, pd = [zero] * (m + 1), [zero] * (m + 1), [zero] * (m + 1)
    n_, j_, c_ = zero + 1, zero, zero  # @line L10
    b_ = n_ * p.move
    for ch in x:  # @line L11
        cm, ci, cd = [zero] * (m + 1), [zero] * (m + 1), [zero] * (m + 1)
        for k in range(1, m + 1):  # @line L12
            terms = [p.entry[k] * b_]
            if k > 1:
                t = core.t[k - 1]
                terms += [pm[k - 1] * t["MM"], pi[k - 1] * t["IM"], pd[k - 1] * t["DM"]]
            cm[k] = p.msc[k][ch] * op(terms)  # @line L13
            if k < m:
                t = core.t[k]
                ci[k] = op([pm[k] * t["MI"], pi[k] * t["II"]])  # @line L14
            if k > 1:
                t = core.t[k - 1]
                cd[k] = op([cm[k - 1] * t["MD"], cd[k - 1] * t["DD"]])  # @line L15
        e_ = op([cm[k] for k in range(1, m + 1)] + [cd[k] for k in range(2, m + 1)]) if m else zero  # @line L16
        j_ = op([j_ * p.loop, e_ * half])  # @line L17
        c_ = op([c_ * p.loop, e_ * half])
        n_ = n_ * p.loop  # @line L18
        b_ = op([n_ * p.move, j_ * p.move])
        pm, pi, pd = cm, ci, cd
    return c_ * p.move  # @line L19


def forward_odds(p: Profile, x: str) -> Num:
    """Sum over all local multihit alignments of x, in odds space. Cost O(m L)."""
    return _dp(p, x, sum)


def viterbi_odds(p: Profile, x: str) -> Num:
    """Best single local multihit alignment of x, in odds space. Cost O(m L)."""
    return _dp(p, x, max)


def bits(odds: Num, L: int) -> float:
    """Bit score log2(P(x | profile) / P(x | null))."""
    if odds <= 0:
        return -math.inf
    return math.log2(odds) - math.log2(null_odds(L, type(odds)(1)))


def mean_relative_entropy(core: Plan7Core) -> float:
    """Mean over match states of the relative entropy to the background, in bits."""
    tot = 0.0
    for k in range(1, core.m + 1):
        tot += sum(float(e) * math.log2(float(e) / float(core.background[a])) for a, e in core.match_emit[k].items() if e > 0)
    return tot / core.m


def hmmer_lambda(core: Plan7Core) -> float:
    """lambda = ln 2 + 1.44 / (m H), the value of p7_Lambda in HMMER3."""
    return math.log(2) + 1.44 / (core.m * mean_relative_entropy(core))


def gumbel_surv(x: float, mu: float, lam: float) -> float:
    """P(S > x) for a Gumbel distribution."""
    return -math.expm1(-math.exp(-lam * (x - mu)))


def exp_surv(x: float, tau: float, lam: float) -> float:
    """P(S > x) for an exponential tail that starts at tau; 1 below tau."""
    return 1.0 if x <= tau else math.exp(-lam * (x - tau))


def fit_gumbel_mu(xs: Sequence[float], lam: float) -> float:
    """Maximum likelihood location of a Gumbel with known lambda."""
    lo = min(xs)
    s = sum(math.exp(-lam * (x - lo)) for x in xs) / len(xs)
    return lo - math.log(s) / lam


def fit_gumbel(xs: Sequence[float]) -> Tuple[float, float]:
    """Maximum likelihood (mu, lambda) of a Gumbel; bisection on the likelihood equation for lambda."""
    mean, lo = sum(xs) / len(xs), min(xs)

    def g(lam: float) -> float:
        w = [math.exp(-lam * (x - lo)) for x in xs]
        return 1 / lam - mean + sum(wi * x for wi, x in zip(w, xs)) / sum(w)

    a, b = 1e-4, 1.0
    while g(b) > 0 and b < 1e6:
        a, b = b, b * 2
    for _ in range(200):
        c = (a + b) / 2
        if g(c) > 0:
            a = c
        else:
            b = c
    lam = (a + b) / 2
    return fit_gumbel_mu(xs, lam), lam


def random_seq(rng: random.Random, background: Dict[str, Num], L: int) -> str:
    letters = list(background)
    weights = [float(background[a]) for a in letters]
    return "".join(rng.choices(letters, weights, k=L))


@dataclass
class Calibration:
    lam: float
    mu_msv: float
    mu_vit: float
    tau_fwd: float


def calibrate(core: Plan7Core, rng: random.Random, n_msv: int = 200, l_msv: int = 200, n_vit: int = 200, l_vit: int = 200, n_fwd: int = 200, l_fwd: int = 100, tailp: float = 0.04) -> Calibration:
    """Fit the score distributions on random sequences, as hmmbuild does (defaults of HMMER3).

    Cost O(m (n_msv l_msv + n_vit l_vit + n_fwd l_fwd)).
    """
    lam = hmmer_lambda(core)
    p = configure(core, l_msv)
    xs = [bits(msv_odds(p, random_seq(rng, core.background, l_msv)), l_msv) for _ in range(n_msv)]
    mu_msv = fit_gumbel_mu(xs, lam)
    p = configure(core, l_vit)
    xs = [bits(viterbi_odds(p, random_seq(rng, core.background, l_vit)), l_vit) for _ in range(n_vit)]
    mu_vit = fit_gumbel_mu(xs, lam)
    p = configure(core, l_fwd)
    xs = [bits(forward_odds(p, random_seq(rng, core.background, l_fwd)), l_fwd) for _ in range(n_fwd)]
    gmu, glam = fit_gumbel(xs)
    tau = gmu - math.log(-math.log(1 - tailp)) / glam + math.log(tailp) / lam
    return Calibration(lam, mu_msv, mu_vit, tau)


@dataclass
class Hit:
    name: str
    msv: float
    vit: float
    fwd: float
    pvalue: float
    evalue: float


@dataclass
class SearchResult:
    hits: List[Hit]
    passed: Dict[str, int]


def hmmsearch(core: Plan7Core, targets: Sequence[Tuple[str, str]], cal: Calibration, f1: float = 0.02, f2: float = 1e-3, f3: float = 1e-5, report_e: float = 10.0) -> SearchResult:
    """Score each target with the filter pipeline. Use f1 = f2 = f3 = 1 to turn the filters off.

    A target is reported when it passes all three filters and its E-value is at most report_e.
    Cost O(m L) per target that reaches a stage, with L the target length.
    """
    z = len(targets)  # @line L1
    lam = cal.lam  # @line L2
    mu_msv, mu_vit, tau = cal.mu_msv, cal.mu_vit, cal.tau_fwd  # @line L3
    passed = {"msv": 0, "vit": 0, "fwd": 0}
    hits: List[Hit] = []
    for name, x in targets:  # @line L4
        L = len(x)
        p = configure(core, L)  # @line L5
        s_msv = bits(msv_odds(p, x), L)  # @line L6
        if gumbel_surv(s_msv, mu_msv, lam) > f1:
            continue
        passed["msv"] += 1
        s_vit = bits(viterbi_odds(p, x), L)  # @line L7
        if gumbel_surv(s_vit, mu_vit, lam) > f2:
            continue
        passed["vit"] += 1
        s_fwd = bits(forward_odds(p, x), L)  # @line L8
        pv = exp_surv(s_fwd, tau, lam)
        if pv > f3:
            continue
        passed["fwd"] += 1
        ev = pv * z  # @line L9
        if ev <= report_e:
            hits.append(Hit(name, s_msv, s_vit, s_fwd, pv, ev))
    hits.sort(key=lambda h: h.evalue)
    return SearchResult(hits, passed)


def sample_homolog(core: Plan7Core, rng: random.Random) -> str:
    """Emit one sequence from the core model by a global path M1 .. Mm (with inserts and deletes)."""
    out: List[str] = []
    state, k = "M", 1
    while k <= core.m:
        if state == "M":
            e = core.match_emit[k]
            out.append(rng.choices(list(e), [float(v) for v in e.values()])[0])
        elif state == "I":
            out.append(random_seq(rng, core.background, 1))
        if k == core.m:
            break
        t = core.t[k]
        opts = [key for key in TKEYS if key[0] == state]
        nxt = rng.choices(opts, [float(t[key]) for key in opts])[0][1]
        if nxt != "I":
            k += 1
        state = nxt
    return "".join(out)
