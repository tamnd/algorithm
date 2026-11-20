---
tag: NHT0PE
kind: problem
slug: consensus-halving
name: Consensus halving
aliases:
- epsilon-consensus halving
area: algorithmic-game-theory/fair-division
level: research
summary: Cut an interval with at most n cuts into two parts that each of n agents values equally. Finding an epsilon-approximate halving is PPA-complete for inverse-polynomial epsilon.
see_also: [necklace-splitting-theorem, cake-cutting-problem, proportional-division, sperner-lemma, su-rental-harmony-algorithm, end-of-the-line-problem, ppad, tfnp]
sources:
  - paper: doi:10.2307/2033900
    title: Charles R. Hobby and John R. Rice, A moment problem in L1 approximation, Proceedings of the American Mathematical Society 16(4) (1965)
    locator: pp. 665-670 (the existence of a halving with n cuts, for functions in L1)
  - paper: doi:10.1016/S0165-4896(02)00087-2
    title: Forest W. Simmons and Francis Edward Su, Consensus-halving via theorems of Borsuk-Ulam and Tucker, Mathematical Social Sciences 45(1) (2003)
    locator: pp. 15-25 (the name of the problem, and a constructive proof with Tucker's lemma)
  - paper: "Aris Filos-Ratsikas and Paul W. Goldberg, Consensus halving is PPA-complete, STOC 2018, pp. 51-64, arXiv:1711.04503"
    locator: the abstract (PPA-completeness for inverse-exponential epsilon, and the equivalence with necklace splitting)
  - paper: doi:10.1145/3313276.3316334
    title: Aris Filos-Ratsikas and Paul W. Goldberg, The complexity of splitting necklaces and bisecting ham sandwiches, STOC 2019
    locator: pp. 638-649 (PPA-completeness for inverse-polynomial epsilon)
  - paper: doi:10.1145/3519935.3520079
    title: Argyrios Deligkas, John Fearnley, Alexandros Hollender and Themistoklis Melissourgos, Constant inapproximability for PPA, STOC 2022
    locator: the abstract (PPA-completeness for a constant epsilon)
  - paper: doi:10.1137/20M1387493
    title: Aris Filos-Ratsikas, Alexandros Hollender, Katerina Sotiraki and Manolis Zampetakis, Consensus-halving, does it ever get easier?, SIAM Journal on Computing 52(2) (2023)
    locator: pp. 412-451 (two-block and single-block valuations, and consensus 1/3 division)
  - paper: doi:10.1016/j.artint.2022.103784
    title: Argyrios Deligkas, Aris Filos-Ratsikas and Alexandros Hollender, Two's company, three's a crowd, consensus-halving for a constant number of agents, Artificial Intelligence 313 (2022)
    locator: the abstract (two and three agents, monotone and general valuations, query bounds)
  - paper: "Noga Alon and Andrei Graur, Efficient splitting of measures and necklaces, arXiv:2006.16613 (2020)"
    locator: Section 1 (efficient algorithms that use more cuts)
---

Consensus halving asks for at most $n$ cuts of the interval $[0, 1]$ and a split of the pieces into two parts, labeled $+$ and $-$, such that each of $n$ agents values the two parts equally, or within $\varepsilon$ of each other in the approximate version. Such a split always exists, but finding one is hard: for inverse-polynomial $\varepsilon$ the problem is PPA-complete. The difference from the [necklace splitting theorem](/necklace-splitting-theorem/) is the object: that page is the existence theorem for a discrete necklace and any number $k$ of thieves, while this page is the computational problem for continuous valuations with two parts, where the accuracy $\varepsilon$ and the way the valuations are given decide how hard it is. The two problems are equivalent for two thieves. Unlike in [cake cutting](/cake-cutting-problem/), no agent gets a part; every agent must agree that the split is fair.

## In plain words

Two families inherit a strip of land together, and each family has several members. Every member has its own opinion of which parts of the strip are worth more. They want to split the strip into two halves, one for each family, so that every member of both families agrees that the two halves are worth the same. They can cut the strip in several places and give the pieces to the two sides in any way.

A classic result says that this always works if the number of cuts is at least the number of people. Finding the cuts is a different matter. Nobody knows a fast method, and there is good reason to believe that none exists, even if a small error is allowed.

## Definition

There are $n$ agents. Agent $i$ has a valuation $V_i$ on the interval $[0, 1]$ that is nonnegative, additive and nonatomic, with $V_i([0, 1]) = 1$, as in the [cake cutting problem](/cake-cutting-problem/).

- **Input.** The valuations $V_1, \dots, V_n$ and an accuracy $\varepsilon \ge 0$.
- **Output.** Cut points $0 \le x_1 \le \dots \le x_n \le 1$ and a label $+$ or $-$ for each of the $n + 1$ intervals $[x_{j-1}, x_j]$, with $x_0 = 0$ and $x_{n+1} = 1$. Let $A_+$ and $A_-$ be the unions of the intervals with each label.
- **Condition.** $|V_i(A_+) - V_i(A_-)| \le \varepsilon$ for every agent $i$. The exact problem has $\varepsilon = 0$.

Two adjacent intervals with the same label can be joined, so the labels can be taken to alternate, and the output is the cut points and the label of the first interval.

The measure depends on how the valuations are given. In the explicit model, each $V_i$ is part of the input, usually as a piecewise-constant density with rational break points and heights, and the measure is the running time in the input size, with $\varepsilon$ given as a rational number. In the query model, the valuations are hidden and the measure is the number of value queries.

The problem is total: a solution always exists. The complexity class PPA, for polynomial parity argument, is the class of total search problems that reduce in polynomial time to LEAF, the problem of finding a second vertex of degree 1 in a graph of degree at most 2 that is described by a circuit and has a given vertex of degree 1. PPA contains [PPAD](/ppad/), and both lie in [TFNP](/tfnp/).

## Variants

- **Exact or approximate.** The exact version asks for $\varepsilon = 0$. The approximate version fixes $\varepsilon$ as a constant, as an inverse polynomial in $n$, or as an inverse exponential.
- **Valuation classes.** Piecewise-constant densities; piecewise-uniform densities, in which each agent has the same density on a few blocks and 0 elsewhere; single-block valuations, in which each agent is uniform on one interval; and monotone valuations, which need not be additive.
- **A constant number of agents.** The number of agents is fixed and the input is the description of the valuations.
- **Consensus $1/k$ division.** Split the interval into $k$ parts that every agent values at $1/k$ each, with at most $(k - 1) n$ cuts. Simmons and Su stated this generalization; its existence is the continuous necklace splitting theorem.
- **More cuts.** Allow more than $n$ cuts to make the problem easier.

## Examples

**Two agents.** Agent 1 is uniform on $[0, 1]$. Agent 2 is uniform on $[0, 1/2]$, with density 2 there. One cut is not enough: agent 1 forces the cut to $1/2$, and then agent 2 values one part at 1 and the other at 0. Two cuts suffice. Cut at $1/4$ and $3/4$, and label $[0, 1/4]$ and $[3/4, 1]$ with $+$ and $[1/4, 3/4]$ with $-$. Agent 1 values $A_-$ at its length, $1/2$. Agent 2 values $A_-$ at $2 \cdot (1/2 - 1/4) = 1/2$. So each agent values each part at $1/2$.

**Why $n$ cuts are needed.** Let agent $i$ be uniform on $[(i - 1)/n, i/n]$. If no cut lies strictly inside this interval of agent $i$, the whole interval has one label, and agent $i$ values one part at 1 and the other at 0. So every $\varepsilon < 1$ needs a cut inside each of the $n$ intervals, and $n$ cuts in total. Cutting each interval at its middle, with alternating labels, gives an exact halving with $n$ cuts.

## Known algorithms

| method | setting | result |
|---|---|---|
| Borsuk-Ulam proof (Hobby and Rice, Alon and West) | any $n$ | existence only |
| path following with Tucker's lemma (Simmons and Su 2003) | any $n$, approximate | finite, with no polynomial bound |
| Deligkas, Filos-Ratsikas and Hollender 2022 | 2 agents, monotone | polynomial time and polynomially many queries |
| Filos-Ratsikas, Hollender, Sotiraki and Zampetakis 2023 | single-block valuations | polynomial for $\varepsilon = 1/2$; parameterized polynomial for every $\varepsilon$ |
| Alon and Graur 2020 | more than $n$ cuts | efficient algorithms |

The Simmons-Su method labels the vertices of a fine triangulation of a sphere by asking agents which part they prefer, and follows a path to a complementary edge of Tucker's lemma, much as [Su's algorithm](/su-rental-harmony-algorithm/) follows doors to a fully labeled cell of [Sperner's lemma](/sperner-lemma/). The triangulation must be finer for a smaller $\varepsilon$, and the path can visit a large part of it.

## Bounds

All entries below are theorems from the cited sources.

- **Existence.** For every $n$ nonatomic valuations, an exact halving with $n$ cuts exists (Hobby and Rice 1965, for valuations with integrable densities; the Borsuk-Ulam proof on the necklace splitting page covers all continuous measures).
- **Number of cuts.** $n$ cuts are needed in the worst case for every $\varepsilon < 1$, by the second example.
- **Membership.** The approximate problem with explicit valuations is in PPA (Filos-Ratsikas and Goldberg 2018, from the proof of Simmons and Su).
- **Hardness, inverse-exponential accuracy.** PPA-complete (Filos-Ratsikas and Goldberg, STOC 2018).
- **Hardness, inverse-polynomial accuracy.** PPA-complete (Filos-Ratsikas and Goldberg, STOC 2019).
- **Hardness, constant accuracy.** PPA-complete for every constant $\varepsilon < 1/5$ (Deligkas, Fearnley, Hollender and Melissourgos, STOC 2022).
- **Simple valuations.** Still PPA-hard for piecewise-uniform valuations with two blocks per agent. Polynomial for single-block valuations with $\varepsilon = 1/2$. The approximate consensus $1/3$ division is PPAD-hard (Filos-Ratsikas, Hollender, Sotiraki and Zampetakis 2023).
- **A constant number of agents.** With monotone valuations: polynomial time and queries for 2 agents; PPA-complete, with exponential query lower bounds, for 3 or more agents. With general valuations: PPA-complete, with exponential query lower bounds, already for 2 agents (Deligkas, Filos-Ratsikas and Hollender 2022).

## Reductions

- **Necklace splitting.** A necklace for two thieves is a consensus halving with uniform measures on the beads of each colour; the rounding step on the [necklace splitting page](/necklace-splitting-theorem/) moves the cuts to the gaps between beads. In the other direction, Filos-Ratsikas and Goldberg (2018) showed that the approximate consensus halving problem is polynomial-time equivalent to necklace splitting, which led to the PPA-completeness of necklace splitting for two thieves in 2019.
- **Tucker's lemma.** The proof of Simmons and Su reduces consensus halving to finding a complementary edge in a Tucker labeling, which puts the problem in PPA.
- **LEAF.** The hardness proofs reduce LEAF to consensus halving; the 2019 proof embeds a high-dimensional Moebius strip into the problem. This makes consensus halving a source of PPA-hardness without a circuit in its input; Filos-Ratsikas and Goldberg used it to prove that the discrete ham sandwich problem is PPA-complete.
- **Cake cutting.** A consensus $1/n$ division of a cake among $n$ agents gives each agent a share that every agent values at exactly $1/n$. Such an exact division is [proportional](/proportional-division/) and envy-free, but its parts are unions of intervals.

## Applications

- Splitting a shared resource between two groups, such as two families or two firms, when every member of each group must accept the split.
- Necklace splitting for two thieves, and the discrete ham sandwich problem, through the reductions above.
- A natural complete problem for PPA, used as the starting point of other hardness proofs.

## References
