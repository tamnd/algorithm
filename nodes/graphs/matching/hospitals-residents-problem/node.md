---
tag: ZSY727
kind: problem
slug: hospitals-residents-problem
name: Hospitals-residents problem
aliases:
- college admissions problem
- residents matching
area: graphs/matching
level: advanced
summary: Many-to-one stable matching where each hospital has a capacity.
model: word-ram
complexity:
  vars: {n: the number of residents and hospitals, m: the number of acceptable resident-hospital pairs}
  time: {worst: O(n + m)}
prereqs: [gale-shapley, stable-matching]
see_also: [stable-matching-with-ties, stable-matching-rotations, stable-roommates-problem, b-matching, bipartite-matching, np-hard, lattice, maximal-matching]
sources:
  - paper: doi:10.2307/2312726
    title: David Gale and Lloyd S. Shapley, College admissions and the stability of marriage, The American Mathematical Monthly 69(1), 9 to 15 (1962)
    locator: the whole paper (the college admissions problem with quotas, existence and the optimality of deferred acceptance)
  - paper: doi:10.1086/261272
    title: Alvin E. Roth, The evolution of the labor market for medical interns and residents, a case study in game theory, Journal of Political Economy 92(6), 991 to 1016 (1984)
    locator: the whole paper (the history of the American residency match and its equivalence to hospital-proposing deferred acceptance)
  - book: isbn:9780262071185
    title: Dan Gusfield and Robert W. Irving, The Stable Marriage Problem, Structure and Algorithms, MIT Press (1989)
    locator: Section 1.6, The hospitals/residents problem (the resident-oriented and hospital-oriented algorithms and the reduction by cloning)
  - book: isbn:9789814425247
    title: David F. Manlove, Algorithmics of Matching Under Preferences, World Scientific (2013)
    locator: Chapter 1, Preliminary definitions, results and motivation (Section 1.3 on HR) and Chapter 5, Hospitals/residents problem variants (couples, ties and lower quotas)
---

The hospitals-residents problem is the many-to-one version of the [stable matching](/stable-matching/) problem. Residents rank hospitals, hospitals rank residents, and each hospital has a capacity, the number of residents it can take. The goal is an assignment with no *blocking pair*: no resident and hospital that would both rather be matched to each other than keep what they have. Gale and Shapley introduced it as the college admissions problem in 1962 and showed that the [Gale-Shapley algorithm](/gale-shapley/) extends to it, so a stable matching always exists and is found in linear time. The graph is bipartite, residents on one side and hospitals on the other, and unweighted: preferences are orders, not numbers.

## In plain words

Young doctors apply to hospitals, and each hospital has a fixed number of places. Each doctor lists the hospitals in order of preference, and each hospital lists the doctors it would take, best first. A placement is unstable if some doctor and some hospital both prefer each other to the deal they got: the doctor would rather work there, and the hospital either has a free place or would happily drop one of its doctors for this one. Such a pair would make a side deal and break the system.

The doctors-propose procedure always ends with a stable placement. Doctors apply in turn down their lists, and each hospital keeps the best applicants it has seen so far, up to its number of places, and turns the rest away. Every doctor gets the best hospital they can get in any stable placement.

## Definition

**Input.** A set $R$ of residents and a set $H$ of hospitals, a set $E \subseteq R \times H$ of acceptable pairs, a capacity $c(h) \ge 1$ for each hospital, and strict preference lists: each resident $r$ ranks the hospitals $h$ with $rh \in E$, and each hospital $h$ ranks the residents $r$ with $rh \in E$. Write $n = |R| + |H|$ and $m = |E|$; the input has size $\Theta(n + m)$.

**Matching.** A set $M \subseteq E$ in which each resident is in at most one pair and each hospital $h$ in at most $c(h)$ pairs. A hospital with fewer than $c(h)$ residents is *undersubscribed*, one with exactly $c(h)$ is *full*. It is a [b-matching](/b-matching/) in the bipartite graph $(R \cup H, E)$ with $b = 1$ on residents and $b = c$ on hospitals.

**Blocking pair.** A pair $rh \in E \setminus M$ blocks $M$ if both

1. $r$ is unmatched, or $r$ prefers $h$ to its hospital $M(r)$, and
2. $h$ is undersubscribed, or $h$ prefers $r$ to its worst resident in $M$.

$M$ is *stable* if no pair blocks it. The task is to find a stable matching. With $c \equiv 1$ this is the stable marriage problem with incomplete lists.

**Facts.** A stable matching always exists. Among the stable matchings there is one, $M_R$, that every resident likes at least as much as every other stable matching, and one, $M_H$, that every hospital likes best in a natural sense; $M_R$ is the worst stable matching for the hospitals and $M_H$ the worst for the residents. The stable matchings form a distributive [lattice](/lattice/), as in the one-to-one case.

**Rural hospitals theorem.** Every stable matching matches the same set of residents, fills each hospital with the same number of residents, and gives an undersubscribed hospital exactly the same residents in every stable matching. So a hospital that cannot fill its places in one stable matching cannot fill them in any, which is the origin of the name: rural hospitals that are short of residents cannot be helped by choosing a different stable matching. Gale and Sotomayor, and Roth, proved these facts in the mid-1980s.

## Variants

- **Ties.** Hospitals often rank residents in groups. With ties there are weak, strong and super-stability, and a weakly stable matching of largest size is [NP-hard](/np-hard/) to find; see [stable matching with ties](/stable-matching-with-ties/).
- **Couples.** Two residents want positions at hospitals close to each other and submit a joint list of pairs of hospitals. A stable matching may not exist, and deciding whether one does is [NP-complete](/np-complete/), shown by Ronn in 1990. The American match handles couples with heuristics.
- **Lower quotas.** Some hospitals must take at least a given number of residents or close. Stable matchings that meet lower quotas may not exist, and deciding whether one does is hard in some versions.
- **Student-project allocation.** Students rank projects, lecturers offer projects and rank students, and both projects and lecturers have capacities; a three-level extension studied by Abraham, Irving and Manlove.
- **School choice.** Schools rank pupils by fixed priorities instead of preferences, so only the pupils' welfare counts; the pupil-proposing algorithm is used, and stability means that no priority is violated.
- **Many-to-many.** Both sides have capacities, as with workers who hold several part-time jobs; pairwise stability still exists under strict preferences.

## Examples

**Two stable matchings.** Residents $r_1, \ldots, r_5$, hospitals $h_1$ and $h_2$, each of capacity 2, every pair acceptable:

| agent | preference list |
|---|---|
| $r_1$ | $h_1, h_2$ |
| $r_2$ | $h_2, h_1$ |
| $r_3$ | $h_2, h_1$ |
| $r_4$ | $h_1, h_2$ |
| $r_5$ | $h_1, h_2$ |
| $h_1$ | $r_3, r_1, r_4, r_2, r_5$ |
| $h_2$ | $r_4, r_1, r_2, r_3, r_5$ |

With residents proposing in order, $r_1$ and $r_4$ apply to $h_1$, $r_2$ and $r_3$ to $h_2$, and $r_5$ to $h_1$, which is now over capacity and rejects its worst applicant, $r_5$. Then $r_5$ applies to $h_2$, which also rejects it, and $r_5$ has no hospital left. The result is $M_R = \{h_1: r_1, r_4;\ h_2: r_2, r_3\}$: $r_3$ and $r_4$ get their first choices. With hospitals proposing, $h_1$ offers to $r_3$ and $r_1$, $h_2$ to $r_4$ and $r_1$; $r_1$ keeps $h_1$ and rejects $h_2$, which then offers to $r_2$. The result is $M_H = \{h_1: r_1, r_3;\ h_2: r_2, r_4\}$, where both hospitals get their two favourites among those they can get. These are the only two stable matchings, checked by enumerating all $3^5$ assignments. In both, $r_5$ is unmatched and both hospitals are full, as the rural hospitals theorem says.

**No complete matching.** In the example above, five residents and a total capacity of 4 leave some resident unmatched in every matching, and stability decides that it is $r_5$, last on both hospitals' lists. If a resident finds no hospital acceptable, or no hospital ranks it, it has no acceptable pair and is single in every matching.

**Undersubscribed hospital.** Keep the hospital lists above, give $h_2$ capacity 4, and let every resident rank $h_1$ first. Then $h_1$ takes its two favourites $r_3$ and $r_1$, since either would otherwise block with $h_1$, and $h_2$ takes $r_2, r_4, r_5$. This is the only stable matching, and $h_2$ is undersubscribed with the same three residents in it, as the rural hospitals theorem requires.

**The empty instance.** With no residents, no hospitals, or no acceptable pairs, the empty matching is the only matching and it is stable.

**One-to-one.** With all capacities 1 the problem is stable marriage, where the classic instance with two men and two women whose preferences cross has exactly two stable matchings.

## Known algorithms

- **Resident-oriented Gale-Shapley.** Each free resident who still has a hospital on its list applies to the next one; the hospital holds the applicant if it is undersubscribed or prefers it to its worst current resident, rejecting that one; otherwise it rejects the applicant. The result is $M_R$. Each acceptable pair is proposed at most once, so with rank tables and, for each hospital, a pointer to its worst current resident that only moves up its list, the time is $O(n + m)$.
- **Hospital-oriented Gale-Shapley.** Each undersubscribed hospital offers places to the next residents on its list; a resident holds its best offer and rejects the rest. The result is $M_H$, also in $O(n + m)$ time.
- **Cloning.** Replace each hospital $h$ by $c(h)$ copies $h^1, \ldots, h^{c(h)}$ with the list of $h$, and replace $h$ in every resident's list by $h^1, \ldots, h^{c(h)}$ in this order. Stable matchings of the stable marriage instance correspond to stable matchings of the original, so any stable marriage algorithm applies, but the instance can grow by a factor of $\max_h c(h)$.
- **All stable matchings.** The rotation structure of [stable matching rotations](/stable-matching-rotations/) carries over, and Gusfield and Irving list all stable matchings with polynomial delay; optimal stable matchings for linear objectives, such as the egalitarian one, are found by a closure computation.
- **Couples and ties.** Integer programming, constraint programming and the Roth-Peranson heuristic are used in practice, since these variants are hard.

## Bounds

- **Upper bound.** $O(n + m)$ on the [word RAM](/word-ram/) by either Gale-Shapley variant, linear in the input size.
- **Lower bound.** $\Omega(n + m)$, since every list entry can matter; for complete lists the Ng and Hirschberg lower bound for stable marriage applies, as that problem is the special case $c \equiv 1$.
- **Number of stable matchings.** It can be exponential in $n$, as in the one-to-one case.
- **Strategy.** The resident-oriented mechanism is strategyproof for residents: no resident gets a better hospital by submitting a false list. Roth showed in 1985 that no stable mechanism is strategyproof for hospitals, and that a hospital can gain by misreporting even under the hospital-oriented algorithm, because a hospital with capacity greater than 1 acts like several agents. In this respect many-to-one differs from one-to-one.

## Reductions

- **From stable marriage.** Set every capacity to 1.
- **To stable marriage,** by cloning, as above, with the same stable matchings up to relabelling the copies.
- **To stable roommates,** through stable marriage, putting all agents in one set; see the [stable roommates problem](/stable-roommates-problem/).
- **Ignoring preferences.** Dropping stability leaves a maximum [b-matching](/b-matching/) in a bipartite graph, a [max-flow](/max-flow-problem/) problem. A stable matching is a [maximal](/maximal-matching/) b-matching, so it has at least half the maximum size.

## Applications

- **Medical residency.** The National Resident Matching Program in the United States has run a centralized match since 1952. Roth showed in 1984 that its procedure is equivalent to the hospital-oriented algorithm, which explains why it worked where earlier schemes failed. In 1998 it switched to a resident-oriented algorithm by Roth and Peranson that also handles couples. Similar schemes run in Canada, Japan, the United Kingdom and elsewhere, and the Scottish Foundation Allocation Scheme used algorithms of this kind for junior doctors.
- **School choice.** Boston and New York City adopted student-proposing deferred acceptance for public schools in the 2000s, following the work of Abdulkadiroğlu, Pathak, Roth and Sönmez.
- **University admissions.** Several countries assign students to university programmes by variants of deferred acceptance with quotas.
- **Other markets.** Allocation of students to projects and supervisors, cadets to military branches, and workers to firms.

## References
