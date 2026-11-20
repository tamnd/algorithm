---
tag: EWBBEB
kind: problem
slug: matching-with-couples
name: Stable matching with couples
aliases:
- hospitals-residents with couples
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: advanced
summary: Stable matching of doctors to hospitals in which couples rank pairs of positions. A stable matching may not exist and the problem is NP-complete.
prereqs: [hospitals-residents-problem, np-complete]
see_also: [hospitals-residents-problem, rural-hospitals-theorem, gale-shapley, stable-roommates-problem, stable-matching-with-ties, lattice-of-stable-matchings, school-choice-problem, np-complete]
sources:
  - paper: doi:10.1086/261272
    title: Alvin E. Roth, The evolution of the labor market for medical interns and residents, a case study in game theory, Journal of Political Economy 92(6), 991 to 1016 (1984)
    locator: the whole paper (couples in the medical match, and an instance with no stable matching)
  - paper: doi:10.1016/0196-6774(90)90007-2
    title: Eytan Ronn, NP-complete stable matching problems, Journal of Algorithms 11(2), 285 to 304 (1990)
    locator: the whole paper (NP-completeness of deciding whether a stable matching with couples exists)
  - paper: doi:10.1007/s10878-009-9257-2
    title: Eric McDermid and David F. Manlove, Keeping partners together, algorithmic results for the hospitals/residents problem with couples, Journal of Combinatorial Optimization 19(3), 279 to 303 (2010)
    locator: the whole paper (hardness under restricted lists, and polynomial special cases)
  - paper: doi:10.1257/aer.89.4.748
    title: Alvin E. Roth and Elliott Peranson, The redesign of the matching market for American physicians, some engineering aspects of economic design, American Economic Review 89(4), 748 to 780 (1999)
    locator: the whole paper (the applicant-proposing algorithm with couples used by the medical match)
  - paper: doi:10.1093/qje/qjt019
    title: Fuhito Kojima, Parag A. Pathak and Alvin E. Roth, Matching with couples, stability and incentives in large markets, Quarterly Journal of Economics 128(4), 1585 to 1632 (2013)
    locator: the whole paper (existence of stable matchings with high probability in large markets with few couples)
  - paper: doi:10.1287/opre.2014.1276
    title: Itai Ashlagi, Mark Braverman and Avinatan Hassidim, Stability in large matching markets with complementarities, Operations Research 62(4), 713 to 732 (2014)
    locator: the whole paper (sharper conditions on the number of couples)
---

Stable matching with couples is the [hospitals-residents problem](/hospitals-residents-problem/) in which some residents apply as couples and rank pairs of positions, one for each partner, so that they can live in the same area. This one change destroys the good properties of the problem without couples: a stable matching may not exist, deciding whether one exists is NP-complete, and the [rural hospitals theorem](/rural-hospitals-theorem/) and the [lattice of stable matchings](/lattice-of-stable-matchings/) no longer apply. The problem is close to the [stable roommates problem](/stable-roommates-problem/), which also may have no stable matching, but there the cause is one set of agents on both sides, while here it is the joint preference of two residents. The American medical match has let couples apply together for decades, with heuristic algorithms that work well in practice.

## In plain words

Doctors look for training positions and hospitals pick doctors. When two doctors are a couple, they want positions that fit together, for example two jobs in the same city. They give one joint list of pairs of jobs. A couple may accept a pair of jobs only together, and it may prefer to stay together without jobs over taking two jobs far apart. This joint wish acts like a need for two goods at once. Because of it, every way to assign the doctors can be unstable: someone always wants to move, and the move makes someone else want to move. Also, checking if a stable way exists is a very hard computational problem. In real markets with few couples, a stable way is usually found.

## Definition

An instance has a set of hospitals, each with a capacity $q_h$ and a strict order over the residents it finds acceptable, and a set of residents. Some residents are single, with a strict order over acceptable hospitals. The others are grouped into couples $(c, c')$. A couple has a strict order over the pairs $(h, h')$ in which $h$ is a hospital or "unmatched" for $c$ and $h'$ is a hospital or "unmatched" for $c'$; the pair (unmatched, unmatched) is the outside option, and pairs below it are unacceptable.

A matching assigns residents to hospitals within capacities, with each single resident at an acceptable hospital or unmatched and each couple at an acceptable pair or unmatched. Say that hospital $h$ *would admit* resident $r$ if $h$ finds $r$ acceptable and either has a free position or prefers $r$ to one of its residents. A matching is *stable* (in the sense of Roth 1984) when no one blocks it:

- no single resident $r$ and hospital $h$ such that $r$ prefers $h$ to her assignment and $h$ would admit $r$;
- no couple $(c, c')$ and pair $(h, h')$ that the couple prefers to its assignment such that each named hospital would admit its member, keeping the partner's current position if only one member moves, and admitting both if $h = h'$;
- no hospital that is assigned an unacceptable resident, and no couple at an unacceptable pair.

The decision problem asks whether a stable matching exists; the search problem asks for one. Other papers use slightly different definitions of stability, which differ in how a couple that moves frees its old positions.

## Variants

- **Responsive couples.** If the couple's joint order agrees with two separate individual orders (a pair improves when one member's hospital improves and the other's stays), stable matchings exist (Klaus and Klijn 2005); in effect the couple behaves like two singles.
- **Couples who must be at the same hospital.** Each couple ranks hospitals for both members together.
- **Short lists and bounded capacities.** McDermid and Manlove (2010) showed that the problem stays NP-complete under strong restrictions on the lengths of the lists, and gave polynomial algorithms for some special cases.

## Examples

All capacities are 1. The couple $(c_1, c_2)$ accepts only the pair $(h_1, h_2)$: $c_1$ at $h_1$ and $c_2$ at $h_2$. The single resident $s$ ranks $h_1$ above $h_2$. Hospital $h_1$ ranks $c_1$ above $s$, and hospital $h_2$ ranks $s$ above $c_2$.

| matching | blocked by |
|---|---|
| couple at $(h_1, h_2)$, $s$ unmatched | $s$ and $h_2$: $s$ wants $h_2$, and $h_2$ prefers $s$ to $c_2$ |
| $s$ at $h_1$, couple unmatched | the couple and $(h_1, h_2)$: $h_1$ prefers $c_1$ to $s$, and $h_2$ is free |
| $s$ at $h_2$, couple unmatched | $s$ and $h_1$: $s$ prefers $h_1$, and $h_1$ is free |
| everyone unmatched | $s$ and $h_1$ |

These are all the matchings, so no stable matching exists. Each step of a deferred acceptance run moves to the next row of a cycle: the couple displaces $s$ at $h_1$, $s$ displaces $c_2$ at $h_2$, the couple then gives up both positions, and $s$ goes back to $h_1$.

## Known algorithms

- **Roth-Peranson algorithm.** The medical match since 1998 uses an applicant-proposing deferred acceptance algorithm that processes couples by withdrawing and re-entering applicants as needed. It may cycle in principle, so it has no guarantee, but in the computations of Roth and Peranson (1999) on the match data it found stable matchings.
- **Exact search.** Integer programming, constraint programming and SAT models solve small and medium instances exactly or prove that no stable matching exists. Their running time is exponential in the worst case.
- **Brute force.** Trying all matchings decides existence in exponential time; the problem is in NP because stability of a given matching is checked in polynomial time.

## Bounds

- Deciding whether a stable matching exists is NP-complete (Ronn 1990). It is in NP because checking every possible blocking resident or couple with every hospital or pair of hospitals takes polynomial time.
- The problem stays NP-complete with severe restrictions on the lists (McDermid and Manlove 2010).
- In large random markets, stable matchings exist with high probability when there are few couples. Kojima, Pathak and Roth (2013) proved this when the number of couples grows slowly relative to the market, and Ashlagi, Braverman and Hassidim (2014) sharpened the condition on the number of couples.

## Reductions

- Without couples, the problem is the [hospitals-residents problem](/hospitals-residents-problem/), solved by [deferred acceptance](/gale-shapley/) in linear time.
- Deciding existence is [NP-complete](/np-complete/), so a polynomial reduction from any problem in NP exists; no polynomial algorithm is known.
- Couples act like bidders who want two goods at once. As in a [combinatorial auction](/combinatorial-auction/) with complements, equilibria need not exist, which is the same failure as the loss of [gross substitutes](/gross-substitutes/).

## Applications

The American National Resident Matching Program lets couples rank pairs of positions, because couples who could not do so tended to find jobs outside the match. Roth (1984) pointed out that stable matchings may not exist with couples. The redesign by Roth and Peranson (1999), adopted in 1998, handles couples explicitly, and similar algorithms run in other medical matches and in the market for clinical psychologists, whose data Kojima, Pathak and Roth (2013) used to support their large-market results.

## References
