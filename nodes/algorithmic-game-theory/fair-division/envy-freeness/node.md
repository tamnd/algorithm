---
tag: A3SKTA
kind: definition
slug: envy-freeness
name: Envy-freeness
aliases:
- envy-free allocation
area: algorithmic-game-theory/fair-division
level: intro
summary: An allocation in which no agent values the piece of another agent more than its own piece.
prereqs: [cake-cutting-problem, proportional-division]
see_also: [divide-and-choose, selfridge-conway-procedure, brams-taylor-procedure, aziz-mackenzie-protocol, stromquist-impossibility-theorem, envy-freeness-up-to-one-good, adjusted-winner, rental-harmony]
sources:
  - book: isbn:9780521556446
    title: Steven J. Brams and Alan D. Taylor, Fair Division, From Cake-Cutting to Dispute Resolution, Cambridge University Press, 1996
    locator: Chapter 4 (envy-freeness and equitability for n = 2), Chapter 6, Envy-free procedures for n = 3 and n = 4 (pp. 115-128), and Chapter 7, Envy-free procedures for arbitrary n (pp. 129-157)
  - book: isbn:9781568810768
    title: Jack Robertson and William Webb, Cake-Cutting Algorithms, Be Fair If You Can, A K Peters, 1998
    locator: Chapter 10, Exact and Envy-Free Algorithms
  - book: isbn:9781107060432
    title: Felix Brandt, Vincent Conitzer, Ulle Endriss, Jerome Lang and Ariel D. Procaccia (eds.), Handbook of Computational Social Choice, Cambridge University Press, 2016
    locator: Chapter 13, Ariel D. Procaccia, Cake Cutting Algorithms, Section 13.3, classic algorithms (from p. 313), and Section 13.4, complexity of cake cutting (from p. 316)
  - paper: "Duncan K. Foley, Resource allocation and the public sector, Yale Economic Essays 7(1) (1967), 45-98"
    locator: the first definition of an allocation in which no agent prefers the bundle of another
  - paper: "Walter Stromquist, Envy-free cake divisions cannot be found by finite protocols, Electronic Journal of Combinatorics 15 (2008), R11"
    locator: the main theorem, for n at least 3 and connected pieces
---

An allocation is envy-free when every agent values its own piece at least as much as the piece of every other agent. Each agent compares by its own valuation, so no agent wants to swap its piece with anyone. For a [cake](/cake-cutting-problem/) that is given out completely, envy-freeness implies [proportional division](/proportional-division/), and for two agents the two goals are the same. For more agents envy-freeness is much harder: an envy-free division always exists, but the best known bounded protocol for $n$ agents uses a tower of exponentials of queries, and with connected pieces no finite protocol exists for $n \ge 3$.

## Definition

The cake is $[0, 1]$, and agent $i \in \{1, \dots, n\}$ has a nonnegative, additive and nonatomic valuation $V_i$ with $V_i([0, 1]) = 1$. An allocation $X_1, \dots, X_n$ is a list of disjoint pieces, each a finite union of intervals, that covers $[0, 1]$. It is envy-free when

$$V_i(X_i) \ge V_i(X_j) \quad \text{for all agents } i \text{ and } j.$$

Agent $i$ envies agent $j$ when $V_i(X_j) > V_i(X_i)$. The condition compares pieces only through the eyes of one agent at a time, so it needs no common scale of value among the agents.

The pieces must cover the cake. Without this condition the empty allocation, in which nobody gets anything, would be envy-free. With it, summing the condition over $j$ gives $n V_i(X_i) \ge \sum_j V_i(X_j) = V_i([0, 1]) = 1$, so each agent gets at least $1/n$.

The same definition applies to other resources. For a set of goods, $X_i$ is a bundle and $V_i$ is a valuation of bundles. For chores, the inequality is reversed: each agent thinks its own share of the work is the smallest.

## Examples and non-examples

- **Divide and choose.** For two agents, [divide and choose](/divide-and-choose/) gives the cutter a piece worth exactly $1/2$ and the chooser the piece it prefers. Both agents value their own piece at least $1/2$ and the other piece at most $1/2$, so there is no envy.
- **Proportional but not envy-free.** Split $[0, 1]$ into four equal segments, and let agents 1, 2 and 3 have densities $(1, 1, 1, 1)$, $(2, 1, 1, 0)$ and $(3, 1, 0, 0)$, scaled to total 1. The [last diminisher](/last-diminisher/) gives agent 3 the piece $[0, 1/9]$, agent 2 the piece $[1/9, 11/36]$ and agent 1 the piece $[11/36, 1]$. Agent 3 values its own piece at $1/3$ and the piece of agent 2 at $17/36$, so agent 3 envies agent 2. Agent 2 values its own piece at $1/3$ and the piece of agent 1 at $4/9$, so agent 2 envies agent 1.
- **Identical valuations.** If all agents have the same valuation $V$, an allocation is envy-free exactly when every piece has value $1/n$ under $V$. Then envy-free and proportional are the same.
- **Envy-free but wasteful.** Agent 1 values only $[0, 1/2]$ (density 2 there) and agent 2 values only $[1/2, 1]$. The allocation $X_1 = [0, 1/4] \cup [3/4, 1]$ and $X_2 = [1/4, 3/4]$ gives each agent the value $1/2$ for its own piece and $1/2$ for the other piece, so it is envy-free. But $X_1 = [0, 1/2]$ and $X_2 = [1/2, 1]$ gives both agents the value 1. So an envy-free allocation need not be Pareto optimal.
- **One good.** Two agents both want one indivisible good. Whoever gets it is envied by the other, so no envy-free allocation exists. This is why [envy-freeness up to one good](/envy-freeness-up-to-one-good/) is used for goods.

## Related definitions

- [Proportional division](/proportional-division/): each agent gets at least $1/n$. It is weaker when the whole cake is given out.
- Equitability: every agent gets the same value by its own measure. For two agents, the [adjusted winner procedure](/adjusted-winner/) gives an allocation that is envy-free, equitable and Pareto optimal.
- [Pareto optimality](/pareto-optimality/): no other allocation is at least as good for every agent and better for one. Envy-freeness does not imply it. For a cake, allocations that are both envy-free and Pareto optimal exist.
- Envy-free with connected pieces: each $X_i$ is one interval. Such allocations exist for all $n$ (a proof uses [Sperner's lemma](/sperner-lemma/)), and the [Stromquist moving knife](/stromquist-moving-knife/) finds one for three agents with continuous knives. The [Stromquist impossibility theorem](/stromquist-impossibility-theorem/) shows that no finite protocol finds one for $n \ge 3$.
- Envy-free protocols with general pieces: the [Selfridge-Conway procedure](/selfridge-conway-procedure/) for three agents, the [Brams-Taylor procedure](/brams-taylor-procedure/) for $n$ agents with a finite but unbounded number of queries, and the [Aziz-Mackenzie protocol](/aziz-mackenzie-protocol/) with a bounded number. Every envy-free protocol needs $\Omega(n^2)$ queries in the [Robertson-Webb query model](/robertson-webb-query-model/) (Procaccia 2009).
- Envy-free rent division: in [rental harmony](/rental-harmony/), each housemate prefers its own room at its own rent.
- [Envy-freeness up to one good](/envy-freeness-up-to-one-good/): for indivisible goods, any envy disappears after the removal of one good from the envied bundle.

## References
