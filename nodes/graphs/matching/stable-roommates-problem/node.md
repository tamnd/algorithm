---
tag: CAH9JF
kind: problem
slug: stable-roommates-problem
name: Stable roommates problem
aliases:
- stable roommates
area: graphs/matching
level: core
summary: Stable matching in a non-bipartite graph where every agent ranks all others.
model: word-ram
complexity:
  vars: {n: the number of agents, m: the total length of the preference lists}
  time: {worst: O(n + m)}
prereqs: [stable-matching, undirected-graph]
see_also: [irving-stable-roommates, gale-shapley, stable-matching-rotations, stable-matching-with-ties, maximum-matching, hospitals-residents-problem, np-complete, perfect-matching]
sources:
  - paper: doi:10.1016/0196-6774(85)90033-1
    title: Robert W. Irving, An efficient algorithm for the stable roommates problem, Journal of Algorithms 6(4), 577 to 595 (1985)
    locator: the whole paper (the two-phase algorithm and its proof)
  - paper: doi:10.2307/2312726
    title: David Gale and Lloyd S. Shapley, College admissions and the stability of marriage, The American Mathematical Monthly 69(1), 9 to 15 (1962)
    locator: the section on the roommates problem (the example with no stable matching)
  - book: isbn:9780262071185
    title: Dan Gusfield and Robert W. Irving, The Stable Marriage Problem, Structure and Algorithms, MIT Press (1989)
    locator: Chapter 4, The Stable Roommates Problem
  - book: isbn:9789814425247
    title: David F. Manlove, Algorithmics of Matching Under Preferences, World Scientific (2013)
    locator: Chapter 4, The Stable Roommates Problem
  - paper: "Jimmy J. M. Tan, A necessary and sufficient condition for the existence of a complete stable matching, Journal of Algorithms 12(1), 154 to 178 (1991)"
    locator: the whole paper (stable partitions)
  - paper: "Eytan Ronn, NP-complete stable matching problems, Journal of Algorithms 11(2), 285 to 304 (1990)"
    locator: the whole paper (roommates with ties)
---

The stable roommates problem is the one-set form of [stable matching](/stable-matching/). There is one set of agents, each agent ranks some of the others, and the task is to pair agents so that no two agents who are not paired with each other both prefer each other to their partners. The acceptable pairs form a general [undirected graph](/undirected-graph/), not a bipartite one, and the graph has no weights. Unlike the two-set problem, a stable matching may not exist. [Irving's algorithm](/irving-stable-roommates/) finds one or reports that none exists in time linear in the size of the lists.

## In plain words

A group of students must share rooms, two to a room. Each student ranks the others as roommates. A plan is unstable if two students who are not roommates both prefer each other to the roommates the plan gives them, because they would swap rooms.

In the problem with two sides, such as students and schools, a stable plan always exists. With one group it can fail. If three students each like one of the others best and a fourth student is everyone's last choice, then the student who rooms with the fourth always finds a better partner who also prefers them. So the first task is to decide whether a stable plan exists, and the second is to find one.

## Definition

The input is a finite set $V$ of agents, with $n = |V|$, and for each agent $a$ a strict preference list, best first, of some other agents. A pair $ab$ is *acceptable* if each is on the list of the other. The acceptable pairs are the edges of a graph $G$ on $V$, which is general, may have odd cycles, and has no weights; $m$ is the total length of the lists.

A *matching* $M$ is a set of acceptable pairs in which no agent occurs twice; $M(a)$ is the partner of $a$. An acceptable pair $ab \notin M$ *blocks* $M$ if each of $a$ and $b$ is single in $M$ or prefers the other to its partner. $M$ is *stable* if no pair blocks it.

- **Input:** $V$ and the preference lists.
- **Output:** a stable matching, or the answer that none exists.

The *classical* case has $n$ even and complete lists, in which each agent ranks all $n - 1$ others; then every stable matching is perfect.

**Basic facts.**

- *Two sets are a special case.* If the agents split into sets $P$ and $R$ and each list holds only agents of the other set, the problem is the stable marriage problem, and a stable matching exists.
- *Existence can fail.* There are instances with complete lists and no stable matching, the first given by Gale and Shapley.
- *The same agents are matched.* If stable matchings exist, they all match the same set of agents, as in the two-set case.
- *Stability implies maximality.* A stable matching is a [maximal matching](/maximal-matching/) of $G$, so its size is at least half that of a [maximum matching](/maximum-matching/).
- *Stable partitions.* Tan proved that each instance has a *stable partition*, a permutation of the agents with an exchange property, in which odd cycles of length at least 3 play the part of pairs. A stable matching exists if and only if a stable partition has no odd cycle. This gives a certificate for the answer "none exists".

## Variants

- **Complete or incomplete lists.** The definition allows incomplete lists; the classical case has complete lists. Irving's algorithm handles both in linear time.
- **Ties.** If lists may contain ties, deciding whether a weakly stable matching exists is NP-complete, by Ronn, even with complete lists. Super-stable matchings, which also forbid pairs where one agent is indifferent, can be found in linear time when they exist.
- **Almost stable.** If no stable matching exists, find a matching with the fewest blocking pairs. This is NP-hard.
- **Many-to-many and capacities.** Each agent may take up to $b(a)$ partners, the stable $b$-matching problem; Irving's method extends to it.
- **All stable matchings.** The stable matchings of a solvable instance are described by rotations, as in the [two-set case](/stable-matching-rotations/); they no longer form a distributive lattice, and finding an egalitarian stable matching is NP-hard.

## Examples

**An instance with no stable matching.** Let $V = \{A, B, C, D\}$ with lists

| agent | list |
|---|---|
| $A$ | $B, C, D$ |
| $B$ | $C, A, D$ |
| $C$ | $A, B, D$ |
| $D$ | any order of $A, B, C$ |

Each perfect matching pairs $D$ with one agent, and that agent has $D$ last.

- $D$ with $A$: then $BC$ is a pair. $C$ prefers $A$ to $B$, and $A$ prefers $C$ to $D$, so $AC$ blocks.
- $D$ with $B$: then $AC$ is a pair. $A$ prefers $B$ to $C$, and $B$ prefers $A$ to $D$, so $AB$ blocks.
- $D$ with $C$: then $AB$ is a pair. $B$ prefers $C$ to $A$, and $C$ prefers $B$ to $D$, so $BC$ blocks.

A matching that is not perfect has two single agents who are acceptable to each other, so it is blocked too. The agents $A$, $B$, $C$ form an odd cycle of preferences, which is the obstacle that stable partitions capture.

**An instance with two stable matchings.** Let the lists be

| agent | list |
|---|---|
| $A$ | $B, D, C$ |
| $B$ | $C, D, A$ |
| $C$ | $A, D, B$ |
| $D$ | $C, B, A$ |

Of the three perfect matchings, $\{AB, CD\}$ and $\{AC, BD\}$ are stable. The third, $\{AD, BC\}$, is blocked by $CD$: $C$ prefers $D$ to $B$, and $D$ prefers $C$ to $A$.

**Odd number of agents.** With complete lists and $n$ odd, one agent is single in any stable matching; with $n = 3$ and lists that form a cycle, as $A$, $B$, $C$ above without $D$, every matching is blocked, so none is stable.

**The empty instance.** With no agents, or with no acceptable pair, the empty matching is stable.

## Known algorithms

| algorithm | output | time |
|---|---|---|
| [Irving's algorithm](/irving-stable-roommates/) | a stable matching or "none exists" | $O(n + m)$, which is $O(n^2)$ with complete lists |
| Tan's algorithm | a stable partition, so a stable matching or a certificate that none exists | $O(n^2)$ with complete lists |
| brute force over all matchings | all stable matchings | exponential |

Irving's algorithm has two phases. Phase 1 is a proposal sequence like [Gale-Shapley](/gale-shapley/) in which each agent both proposes and receives; it shortens the lists. Phase 2 repeatedly finds and removes a cyclic structure called a rotation. If some list becomes empty, no stable matching exists.

## Bounds

- **Upper bound.** $O(n + m)$ on the [word RAM](/word-ram/).
- **Lower bound.** $\Omega(n^2)$ for complete lists, because the stable marriage problem is a special case and has this lower bound.
- **Random instances.** For complete lists chosen uniformly at random, the probability that a stable matching exists decreases as $n$ grows, according to experiments and to the analysis of Pittel and Irving.

## Reductions

- **From stable marriage.** Keep both sets and all lists; pairs inside one set are not acceptable. So every algorithm for this problem solves the [stable matching](/stable-matching/) problem.
- **Not to bipartite matching.** The doubling trick that turns [maximum matching](/maximum-matching/) into a bipartite problem does not preserve stability, which is why a separate algorithm is needed.
- **Ties.** The weakly stable version with ties is [NP-complete](/np-complete/), by a reduction from a satisfiability problem in Ronn's paper.

## Applications

- **Pairing in one pool.** Assigning roommates, pairing players or workers who rank each other, and pairing peers in file sharing networks.
- **Kidney exchange.** Patient and donor pairs that can donate to each other form a one-set market with preferences, and pairwise exchanges are stable matchings of a roommates instance.
- **Coalition formation.** Stable roommates is the case of hedonic coalition formation games in which each coalition has at most two agents.

## References
