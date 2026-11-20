---
tag: 9ZYAED
kind: theorem
slug: rural-hospitals-theorem
name: Rural hospitals theorem
aliases:
- Roth's rural hospitals theorem
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: core
summary: In every stable matching each hospital fills the same number of positions and the same residents are matched. A hospital with an empty position gets the same residents in all of them.
prereqs: [hospitals-residents-problem, gale-shapley]
see_also: [lattice-of-stable-matchings, stable-matching, school-choice-problem, matching-with-couples, stable-matching-with-ties, deferred-acceptance-strategyproofness, egalitarian-stable-matching, roth-impossibility-theorem]
sources:
  - paper: doi:10.2307/1913160
    title: Alvin E. Roth, On the allocation of residents to rural hospitals, a general property of two-sided matching markets, Econometrica 54(2), 425 to 427 (1986)
    locator: the whole paper (the theorem for hospitals with empty positions)
  - paper: doi:10.1086/261272
    title: Alvin E. Roth, The evolution of the labor market for medical interns and residents, a case study in game theory, Journal of Political Economy 92(6), 991 to 1016 (1984)
    locator: the whole paper (the medical match as a stable matching algorithm, and the same matched agents in all stable matchings)
  - paper: doi:10.1007/BF01934199
    title: D. G. McVitie and L. B. Wilson, Stable marriage assignment for unequal sets, BIT 10(3), 295 to 309 (1970)
    locator: the whole paper (in the marriage problem, every stable matching matches the same agents)
  - paper: doi:10.1016/0166-218X(85)90074-5
    title: David Gale and Marilda Sotomayor, Some remarks on the stable matching problem, Discrete Applied Mathematics 11(3), 223 to 232 (1985)
    locator: the whole paper (short proofs of structural results on stable matchings)
  - book: isbn:9789814425247
    title: David F. Manlove, Algorithmics of Matching Under Preferences, World Scientific (2013)
    locator: Chapter 3 (the hospitals-residents problem and its variants)
---

The rural hospitals theorem says that in the [hospitals-residents problem](/hospitals-residents-problem/) the choice of a stable matching does not change who is matched or how many positions each hospital fills. A hospital that has an empty position in one stable matching gets exactly the same residents in every stable matching. The [lattice of stable matchings](/lattice-of-stable-matchings/) describes how stable matchings differ; this theorem describes what they all share. The name comes from the American medical match, where hospitals in rural areas often could not fill their positions, and the theorem shows that no other stable matching would help them.

## Statement

An instance of the hospitals-residents problem has residents, each with a strict order over the hospitals she finds acceptable, and hospitals, each with a capacity $q_h \ge 1$ and a strict order over the residents it finds acceptable. A matching $\mu$ assigns each resident to at most one hospital, and each hospital $h$ to a set $\mu(h)$ of at most $q_h$ residents. It is *stable* when all assignments are mutually acceptable, and there is no resident $r$ and hospital $h$ that find each other acceptable such that $r$ prefers $h$ to $\mu(r)$ (or is unmatched) and $h$ either has fewer than $q_h$ residents or prefers $r$ to one of its residents.

**Theorem (Roth 1984, 1986).** Let $\mu$ and $\mu'$ be stable matchings. Then

1. the same residents are matched in $\mu$ and $\mu'$;
2. $|\mu(h)| = |\mu'(h)|$ for every hospital $h$;
3. if $|\mu(h)| < q_h$, then $\mu(h) = \mu'(h)$.

In the marriage problem, where all capacities are 1, part 1 for both sides was proved by McVitie and Wilson (1970): every stable matching matches the same men and the same women.

## In plain words

Doctors and hospitals can be matched in many stable ways, and some stable matchings are better for the doctors while others are better for the hospitals. But some things are the same in all of them. The same doctors get jobs, and the others get none. Each hospital hires the same number of doctors. And a hospital that cannot fill all its positions hires the very same doctors in every stable matching. So a hospital in a remote area that is short of doctors cannot be helped by choosing a different stable matching. Only a change of the rules, such as dropping stability, could help it.

## Proof

Let $\mu_R$ be the resident-optimal stable matching: every resident weakly prefers $\mu_R$ to every stable matching. It exists by the theorem of Gale and Shapley, and resident-proposing [deferred acceptance](/gale-shapley/) finds it. It is enough to compare an arbitrary stable matching $\mu$ with $\mu_R$.

*Step 1: every resident matched in $\mu$ is matched in $\mu_R$.* A matched resident in $\mu$ has an acceptable hospital, and she weakly prefers $\mu_R(r)$ to it, so she is matched in $\mu_R$. Hence $\sum_h |\mu(h)| \le \sum_h |\mu_R(h)|$.

*Step 2: $|\mu(h)| \ge |\mu_R(h)|$ for every hospital $h$.* Suppose $|\mu(h)| < |\mu_R(h)|$. Then $h$ has an empty position in $\mu$, because $|\mu_R(h)| \le q_h$, and there is a resident $r \in \mu_R(h) \setminus \mu(h)$. She weakly prefers $\mu_R(r) = h$ to $\mu(r)$, and $\mu(r) \ne h$, so she strictly prefers $h$. As $\mu_R$ is stable, $r$ and $h$ find each other acceptable. So $(r, h)$ blocks $\mu$, which is impossible.

*Parts 1 and 2.* By Step 2, $\sum_h |\mu(h)| \ge \sum_h |\mu_R(h)|$, and by Step 1 the reverse holds. So equality holds in Step 2 for every hospital, which is part 2, and the numbers of matched residents are equal. With the inclusion of Step 1, the same residents are matched, which is part 1.

*Part 3.* Let $|\mu(h)| < q_h$. If some $r \in \mu_R(h)$ were not in $\mu(h)$, the argument of Step 2 would make $(r, h)$ a blocking pair of $\mu$, because $h$ has an empty position in $\mu$. So $\mu_R(h) \subseteq \mu(h)$, and both sets have the same size by part 2, so $\mu(h) = \mu_R(h)$. Since this holds for every stable $\mu$, any two stable matchings give $h$ the same residents. $\blacksquare$

## Consequences

- **Rural hospitals.** In the medical match, the choice between the hospital-proposing and the resident-proposing algorithm does not change how many residents a short-staffed hospital gets, nor which ones. This was part of the debate around the redesign of the match in the 1990s.
- **Example.** Residents $r_1$: $h_1, h_2, h_3$; $r_2$: $h_2, h_1, h_3$; $r_3$: $h_3$; $r_4$: $h_1$. Hospitals $h_1$ (one position): $r_2, r_1, r_4$; $h_2$ (one position): $r_1, r_2$; $h_3$ (two positions): $r_1, r_2, r_3$. There are exactly two stable matchings: $r_1 h_1$, $r_2 h_2$, $r_3 h_3$, and $r_1 h_2$, $r_2 h_1$, $r_3 h_3$. In both, $r_4$ is unmatched and $h_3$, which has an empty position, gets only $r_3$.
- **School choice.** In the [school choice problem](/school-choice-problem/) with strict priorities, every stable assignment places the same students and fills each school to the same level.
- **Counting the size.** The size of a stable matching is fixed by the instance, so "maximum stable matching" is a trivial problem for strict orders, unlike the case with ties.

## Tightness

- **Ties.** With ties in the orders, weakly stable matchings can have different sizes, and finding one of maximum size is NP-hard; see [stable matching with ties](/stable-matching-with-ties/).
- **Full hospitals.** Part 3 does not extend to hospitals that are full: in the example, $h_1$ gets $r_1$ in one stable matching and $r_2$ in the other.
- **Couples.** In [matching with couples](/matching-with-couples/), the proof breaks because a couple's preferences link two positions, and stable matchings may not exist at all.
- **Contracts.** Hatfield and Milgrom (2005) proved a version for matching with contracts when the hospitals' choices satisfy a substitutes condition and the law of aggregate demand.

## History

McVitie and Wilson (1970) proved that in the marriage problem every stable matching matches the same agents. Roth (1984) analyzed the medical match in the United States, showed that its algorithm is equivalent to a hospital-proposing deferred acceptance algorithm, and observed that the same residents are matched and each hospital fills the same number of positions in all stable matchings. Roth (1986) proved that a hospital with an empty position gets the same residents in every stable matching, which gave the theorem its name. Gale and Sotomayor (1985) gave short proofs of related structural facts.

## References
