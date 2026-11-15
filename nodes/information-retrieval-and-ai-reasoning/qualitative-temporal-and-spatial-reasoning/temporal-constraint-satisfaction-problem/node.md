---
tag: 3ETFHM
kind: problem
slug: temporal-constraint-satisfaction-problem
name: Temporal constraint satisfaction problem
aliases:
- TCSP
- Dechter-Meiri-Pearl temporal network
area: information-retrieval-and-ai-reasoning/qualitative-temporal-and-spatial-reasoning
level: advanced
summary: Time points with binary constraints that each allow a union of intervals for the difference of two points. Consistency is NP-complete; one interval per constraint gives the polynomial STP.
prereqs: [simple-temporal-problem, constraint-satisfaction-problem]
see_also: [difference-constraints, disjunctive-temporal-problem, path-consistency, graph-coloring, difference-logic-satisfiability, temporal-planning, allens-interval-algebra]
sources:
  - paper: doi:10.1016/0004-3702(91)90006-6
    title: Rina Dechter, Itay Meiri and Judea Pearl, Temporal constraint networks, Artificial Intelligence 49(1-3), 1991
    locator: pages 61 to 95 (the TCSP and its minimal network, the NP-hardness of consistency, the decomposition into STPs in O(n^3 l^e) time, and path consistency on TCSPs)
  - paper: "Eddie Schwalb and Rina Dechter, Coping with disjunctions in temporal constraint satisfaction problems, Proceedings of AAAI-93, AAAI Press, 1993"
    locator: pages 127 to 132 (path consistency is exponential on TCSPs, and the polynomial ULT algorithm that approximates it)
  - paper: "Eddie Schwalb and Rina Dechter, Processing disjunctions in temporal constraint networks, Artificial Intelligence 93, 1997"
    locator: pages 29 to 61 (the journal version, with the fragmentation of intervals under path consistency and its approximations)
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing, Morgan Kaufmann, 2003
    locator: Chapter 12, Temporal constraint networks
---

The temporal constraint satisfaction problem (TCSP) of Dechter, Meiri and Pearl (1991) asks whether time points can be placed so that, for each constrained pair, the difference of the two times lies in one of a few given intervals. It differs from the [simple temporal problem](/simple-temporal-problem/), where each constraint is one interval, and from a system of [difference constraints](/difference-constraints/), where each constraint is one inequality and all must hold together: in a TCSP each constraint is a disjunction. That one change makes consistency NP-complete, while the STP and difference constraints are solved by shortest paths. A TCSP is consistent exactly when one of its *labelings*, a choice of one interval for every constraint, is a consistent STP.

## In plain words

Each event has an unknown time. A rule between two events no longer says "between 10 and 20 minutes later". It says "between 10 and 20 minutes later, or between 40 and 50 minutes later". Each rule gives a short list of allowed gaps.

If you pick one gap from each list, you get the simple kind of problem, which a shortest path method solves fast. So one way to solve a TCSP is to try the picks one after another. The number of picks grows very fast with the number of rules, and no method is known that always avoids this.

## Definition

A TCSP has real variables $X_1, \ldots, X_n$, the time points, and binary constraints. A constraint $T_{ij}$ is a finite set of closed intervals $\{[a_1, b_1], \ldots, [a_k, b_k]\}$ and means

$$X_j - X_i \in [a_1, b_1] \cup \cdots \cup [a_k, b_k].$$

A *solution* is an assignment of reals that meets every constraint. The TCSP is *consistent* if it has a solution. The *minimal network* gives for each pair $(i, j)$ the set of values of $X_j - X_i$ over all solutions, as a union of intervals. Write $e$ for the number of constraints and $l$ for the largest number of intervals in a constraint. Dechter, Meiri and Pearl allow open and half-open intervals as well; closed ones are enough for the results here.

The input bounds are rationals or integers. The main questions are consistency, one solution, and the minimal network.

## Variants

- **Simple temporal problem.** Every constraint has one interval ($l = 1$). Consistency and the minimal network are polynomial; see [simple temporal problem](/simple-temporal-problem/).
- **Disjunctive temporal problem.** A constraint is a disjunction of difference inequalities that may be on different pairs of points. The [disjunctive temporal problem](/disjunctive-temporal-problem/) contains the TCSP as the case where every disjunct is on the same pair.
- **Qualitative point constraints.** Relations $<, =, >$ and their unions between points form the [point algebra](/point-algebra/), which is polynomial. A point relation is a TCSP constraint with unbounded intervals, for example $X_j - X_i \in (0, \infty)$ for $X_i < X_j$.
- **Integer time.** With integer bounds, a consistent TCSP has an integer solution, since each labeling is an STP with integer data.
- **Uncertainty.** When nature sets some durations, the question becomes controllability; see [simple temporal network with uncertainty](/simple-temporal-network-with-uncertainty/).

## Examples

**A small TCSP.** Let $X_1 - X_0 \in [10, 20] \cup [40, 50]$, $X_2 - X_1 \in [30, 40]$ and $X_2 - X_0 \in [60, 70]$. It has two labelings.

- With $[10, 20]$: $X_2 - X_0 \le 20 + 40 = 60$ and $X_2 - X_0 \ge 60$, so $X_1 - X_0 = 20$, $X_2 - X_1 = 40$ and $X_2 - X_0 = 60$.
- With $[40, 50]$: $X_2 - X_0 \ge 40 + 30 = 70$ and $X_2 - X_0 \le 70$, so $X_1 - X_0 = 40$, $X_2 - X_1 = 30$ and $X_2 - X_0 = 70$.

Both labelings are consistent, and the minimal network is the union of their minimal networks: $X_1 - X_0 \in \{20, 40\}$, $X_2 - X_1 \in \{30, 40\}$ and $X_2 - X_0 \in \{60, 70\}$. The bounds of the convex hulls, $[20, 40]$, $[30, 40]$ and $[60, 70]$, would allow $X_1 - X_0 = 30$, which no solution has.

**Three-colouring as a TCSP.** For a graph $G$, take a point $X_0$ and a point $X_v$ for each vertex, with

$$X_v - X_0 \in [0, 0] \cup [1, 1] \cup [2, 2], \qquad X_v - X_u \in [-2, -1] \cup [1, 2] \text{ for each edge } uv.$$

The first constraint gives each vertex a colour $X_v - X_0 \in \{0, 1, 2\}$. Then $X_v - X_u$ is an integer in $\{-2, \ldots, 2\}$, and the edge constraint says it is not 0. So the TCSP is consistent exactly when $G$ is 3-colourable. A triangle gives a consistent TCSP, and the complete graph on four vertices gives an inconsistent one.

**Fragmentation.** Composing $\{[0, 0], [10, 10]\}$ with $\{[0, 0], [1, 1]\}$ gives $\{[0, 0], [1, 1], [10, 10], [11, 11]\}$. Path consistency composes and intersects such sets, so the number of intervals in a constraint can grow at each step.

## Known algorithms

| method | output | worst-case time | notes |
| --- | --- | --- | --- |
| decomposition into labelings (Dechter, Meiri and Pearl, 1991) | consistency and the minimal network | $O(n^3 l^e)$ | solve the STP of each labeling with [Floyd-Warshall](/floyd-warshall/) and take the union |
| backtracking over labelings | consistency and one solution | $O(n m \, l^e)$ for $m$ edges | test each partial labeling as an STP with [Bellman-Ford](/bellman-ford/); add [forward checking](/forward-checking/) or [conflict-directed backjumping](/conflict-directed-backjumping/) |
| [path consistency](/path-consistency/) on the TCSP | a tighter equivalent network | exponential in general | it terminates, but the number of intervals can grow (Schwalb and Dechter, 1993) |
| ULT (Schwalb and Dechter, 1993) | a tighter equivalent network | polynomial | approximates path consistency without fragmentation; used to prune the search |
| [difference logic](/difference-logic-satisfiability/) solvers | consistency and one solution | exponential in the worst case | each constraint becomes a clause of difference atoms |

The decomposition and the backtracking search are exact. Path consistency and ULT are not decision procedures on their own: they can leave an inconsistent network unchanged. They are used to shrink the constraints before or during the search.

## Bounds

**NP-completeness (Turing model, rational bounds in binary).** TCSP consistency is NP-complete. It is in NP: a labeling is a certificate of size $O(e)$, and the STP of the labeling is checked for a negative cycle in polynomial time. It is NP-hard: the three-colouring example above is a [polynomial-time reduction](/polynomial-time-reduction/) from [graph colouring](/graph-coloring/) with three colours, which is [NP-complete](/np-complete/). The hardness is already present with integer bounds of size 2 and at most three intervals per constraint. Dechter, Meiri and Pearl (1991) proved NP-hardness by a reduction of their own.

**Upper bound (word-RAM).** The decomposition method costs $O(n^3 l^e)$: there are at most $l^e$ labelings and each STP costs $O(n^3)$ with Floyd-Warshall. The minimal network is the union of the minimal networks of the consistent labelings, so the same bound covers it.

**Polynomial cases (word-RAM).** With $l = 1$ the problem is an STP, $O(n m)$ for consistency and $O(n^3)$ for the minimal network. When the constraint graph is a tree, every constraint can be met on its own, so a tree TCSP is consistent exactly when no constraint is empty; the solution is built from a root outwards.

## Reductions

- **To STPs.** A TCSP is consistent if and only if some labeling is, and each labeling is a [simple temporal problem](/simple-temporal-problem/). This is the basis of every exact method above.
- **From graph colouring.** The example above, with three intervals per vertex constraint and two per edge constraint.
- **To the disjunctive temporal problem.** A constraint $X_j - X_i \in \bigcup_t [a_t, b_t]$ is the disjunction of the conjunctions $a_t \le X_j - X_i \le b_t$. Each conjunction is two difference atoms, so a TCSP is a DTP after the standard split of each interval, or directly a set of clauses in [difference logic](/difference-logic-satisfiability/).
- **From the point algebra.** Each relation of the point algebra is a TCSP constraint with unbounded intervals, so qualitative point networks are a special case.

## Applications

- Scheduling with alternative time windows: a task that runs in the morning slot or in the afternoon slot, or a satellite pass that can be used on one of several orbits.
- [Temporal planning](/temporal-planning/), where actions may be ordered in more than one way and each order gives a different labeling.
- Combining metric and qualitative information in temporal databases and in medical and legal reasoning about events.

## References
