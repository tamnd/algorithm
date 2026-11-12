---
tag: CNEAFW
kind: problem
slug: simple-temporal-problem
name: Simple temporal problem
aliases:
- temporal constraint network
- simple temporal network
- STN
area: logic-and-constraints/constraint-satisfaction
level: advanced
summary: Decide whether time points can meet constraints of the form a <= X_j - X_i <= b. It is consistent if and only if the distance graph has no negative cycle, and shortest paths give the minimal network.
prereqs: [constraint-satisfaction-problem, shortest-path, negative-cycle]
see_also: [difference-logic-satisfiability, floyd-warshall, bellman-ford, all-pairs-shortest-paths, path-consistency, difference-bound-matrix, allens-interval-algebra, job-shop-scheduling]
sources:
  - paper: doi:10.1016/0004-3702(91)90006-6
    title: Rina Dechter, Itay Meiri and Judea Pearl, Temporal constraint networks, Artificial Intelligence 49(1-3), 1991
    locator: pages 61 to 95 (the STP and its distance graph, the negative-cycle theorem, the minimal network by all-pairs shortest paths, decomposability, and the TCSP and its NP-hardness)
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing, Morgan Kaufmann, 2003
    locator: Chapter 12, Temporal constraint networks
  - book: isbn:9780262046305
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Section 22.4, Difference constraints and shortest paths, and Section 23.2, the Floyd-Warshall algorithm
  - paper: "Léon Planken, Mathijs de Weerdt and Roman van der Krogt, P3C: a new algorithm for the simple temporal problem, Proceedings of ICAPS 2008, pages 256 to 263"
    locator: the minimal network on a chordal graph in time that depends on the triangulation, not on n cubed
  - paper: "Paul Morris, Nicola Muscettola and Thierry Vidal, Dynamic control of plans with temporal uncertainty, Proceedings of IJCAI 2001, pages 494 to 499"
    locator: simple temporal networks with uncertainty and the polynomial test for dynamic controllability
---

The simple temporal problem (STP) asks whether events can be placed in time when each constraint bounds the time between two events: $a \le X_j - X_i \le b$. Dechter, Meiri and Pearl (1991) showed that an STP is consistent if and only if its *distance graph* has no cycle of negative weight. So [Bellman-Ford](/bellman-ford/) decides it in $O(n m)$ time, and [Floyd-Warshall](/floyd-warshall/) computes in $O(n^3)$ time the *minimal network*, the tightest bound on every difference that follows from the constraints. The minimal network is also *decomposable*: any choice of times for some events that meets it can be extended to a solution without backtracking. As a conjunction of difference constraints, the STP is the same as conjunctive [difference logic](/difference-logic-satisfiability/). The STP is the tractable core of temporal reasoning in planning and scheduling. When a constraint may be a disjunction of intervals, the problem (TCSP) is NP-hard.

## In plain words

Each event has an unknown time. Each rule says that one event comes between $a$ and $b$ minutes after another. Draw a dot for each event. A rule "$j$ is at most $b$ after $i$" is an arrow from $i$ to $j$ of length $b$. A rule "$j$ is at least $a$ after $i$" is an arrow back from $j$ to $i$ of length $-a$.

The rules can all be met exactly when no loop of arrows has a negative total length. A negative loop would say that some event happens before itself. When there is no such loop, the shortest route from $i$ to $j$ gives the latest that $j$ can be after $i$, and the shortest route back gives the earliest. These tightest bounds are the minimal network.

## Definition

An STP has time points $X_0, X_1, \ldots, X_{n-1}$, which are real variables, and a set of $m$ constraints. Each constraint has the form $a_{ij} \le X_j - X_i \le b_{ij}$, with $a_{ij} \in \mathbb{R} \cup \{-\infty\}$ and $b_{ij} \in \mathbb{R} \cup \{+\infty\}$. A constraint on one point, $a \le X_i \le b$, uses a fixed origin $X_0 = 0$ and becomes $a \le X_i - X_0 \le b$. A *solution* is an assignment of real numbers that meets every constraint. The STP is *consistent* if it has a solution.

The *distance graph* has a vertex for each time point. For each constraint it has an edge $i \to j$ with weight $b_{ij}$ and an edge $j \to i$ with weight $-a_{ij}$, leaving out infinite weights. The edge $u \to v$ with weight $w$ means $X_v - X_u \le w$.

The *minimal network* is the STP that has, for each pair $i, j$, the constraint $[\min (X_j - X_i), \max (X_j - X_i)]$, where the minimum and maximum are over all solutions. It has the same solutions and the tightest possible intervals.

The questions are: is the STP consistent; find a solution; and compute the minimal network.

## Variants

- **TCSP.** Each constraint is a disjunction of intervals, $X_j - X_i \in [a_1, b_1] \cup \cdots \cup [a_k, b_k]$. Deciding consistency is NP-hard (Dechter, Meiri and Pearl, 1991). A TCSP is solved by search over the choice of one interval for each constraint, which leaves an STP for each choice.
- **DTP.** Disjunctive temporal problems allow disjunctions of difference constraints over different pairs. This is the full [difference logic](/difference-logic-satisfiability/), and it is NP-complete.
- **STNU.** Some durations are set by nature, not by the planner. The question is whether a strategy for the other time points always works. Dynamic controllability can be decided in polynomial time (Morris, Muscettola and Vidal, 2001).
- **Incremental and dynamic STP.** Constraints are added or removed one at a time, as in a planner. A new constraint needs only a local update when the old network is consistent.
- **Qualitative temporal reasoning.** [Allen's interval algebra](/allens-interval-algebra/) uses relations such as "before" and "overlaps" between intervals. It is NP-hard in general, but some of its fragments map to STPs.

## Examples

The examples were checked by the implementation.

**A consistent STP.** $X_0$ is 7:00, $X_1$ is the time John leaves home, $X_2$ the time he arrives at work and $X_3$ the start of a meeting, all in minutes after 7:00:

- $0 \le X_1 - X_0 \le 30$: he leaves between 7:00 and 7:30.
- $30 \le X_2 - X_1 \le 40$: the trip takes 30 to 40 minutes.
- $10 \le X_3 - X_2 \le 20$: the meeting starts 10 to 20 minutes after he arrives.
- $60 \le X_3 - X_0 \le 65$: the meeting starts between 8:00 and 8:05.

Floyd-Warshall on the distance graph gives the matrix $d$, with $d_{ij}$ the shortest distance from $X_i$ to $X_j$:

| | $X_0$ | $X_1$ | $X_2$ | $X_3$ |
|---|---|---|---|---|
| $X_0$ | 0 | 25 | 55 | 65 |
| $X_1$ | 0 | 0 | 40 | 60 |
| $X_2$ | $-40$ | $-30$ | 0 | 20 |
| $X_3$ | $-60$ | $-40$ | $-10$ | 0 |

The diagonal is 0, so there is no negative cycle and the STP is consistent. The minimal constraint on $X_j - X_i$ is $[-d_{ji}, d_{ij}]$. So John leaves between 7:00 and 7:25, not 7:30, since after 7:25 even the fastest trip and the shortest wait put the meeting after 8:05. He arrives between 7:40 and 7:55. The row of $X_0$ gives the latest times $(0, 25, 55, 65)$ and the column of $X_0$, negated, gives the earliest times $(0, 0, 40, 60)$. Both are solutions.

**An inconsistent STP.** Change the last constraint to $30 \le X_3 - X_0 \le 35$. The cycle $X_0 \to X_3 \to X_2 \to X_1 \to X_0$ has weight $35 - 10 - 30 - 0 = -5$. Adding the constraints on it gives $X_3 - X_0 \ge 40$, against $X_3 - X_0 \le 35$.

## Known algorithms

| method | output | worst-case time | notes |
|---|---|---|---|
| [Bellman-Ford](/bellman-ford/) from a virtual source | consistency and one solution | $O(n m)$ | the solution is the vector of distances |
| [Floyd-Warshall](/floyd-warshall/) | minimal network | $O(n^3)$ | $d_{ii} < 0$ for some $i$ if and only if inconsistent |
| [Johnson's algorithm](/johnson/) | minimal network | $O(n m + n^2 \log n)$ | better for sparse graphs |
| [path consistency](/path-consistency/), [PC-2](/pc-2/) | minimal network | $O(n^3)$ for STP | on an STP, path consistency is Floyd-Warshall in another form, and it is exact |
| P3C and other chordal methods (Planken and colleagues, 2008) | minimal network on the edges of a chordal supergraph | depends on the triangulation | for sparse networks |
| incremental update | the minimal network after one new constraint | $O(n^2)$ | relaxes each pair through the new edge |

Path consistency composes and intersects the intervals on each triangle. On an STP, the composition of $[a, b]$ and $[c, e]$ is $[a + c, b + e]$ and intersection keeps one interval, so path consistency is a form of the all-pairs shortest path computation. This is why path consistency decides the STP exactly, while for general binary CSPs it does not.

## Bounds

**Theorem 1 (Dechter, Meiri and Pearl, 1991).** An STP is consistent if and only if its distance graph has no negative cycle.

*Proof.* If a solution exists, take any cycle $v_0 \to v_1 \to \cdots \to v_k = v_0$. Each edge $v_{t-1} \to v_t$ with weight $w_t$ says $X_{v_t} - X_{v_{t-1}} \le w_t$. Adding these inequalities, the left sides cancel to 0, so $0 \le \sum_t w_t$.

If there is no negative cycle, add a vertex $s$ with an edge of weight 0 to every vertex. No cycle goes through $s$, so there is still no negative cycle, and each shortest distance $\delta(v)$ from $s$ is finite. For each edge $u \to v$ with weight $w$, $\delta(v) \le \delta(u) + w$, so $X_v := \delta(v)$ meets $X_v - X_u \le w$. So $\delta$ is a solution. $\square$

**Theorem 2 (minimal network).** If the STP is consistent and $d_{ij}$ is the shortest distance from $i$ to $j$ in the distance graph, then over all solutions the maximum of $X_j - X_i$ is $d_{ij}$ and the minimum is $-d_{ji}$ (with $+\infty$ and $-\infty$ when there is no path).

*Proof.* Every solution has $X_j - X_i \le d_{ij}$, by adding the inequalities along a shortest path from $i$ to $j$. For the other direction, let $d_{ij}$ be finite. Take the vertices $v$ that $i$ reaches, and set $X_v := d_{iv}$. For the other vertices, take a solution $Y$ of the STP and set $X_v := Y_v + C$ for a large constant $C$. Every edge $u \to v$ with both ends reached from $i$ has $d_{iv} \le d_{iu} + w$. No edge goes from a reached vertex to an unreached one. An edge from an unreached $u$ to a reached $v$ needs $d_{iv} - Y_u - C \le w$, which holds for $C$ large. Edges between unreached vertices hold since $Y$ is a solution. So $X$ is a solution, and $X_j - X_i = d_{ij} - 0$. The minimum follows from the maximum of $X_i - X_j$, which is $d_{ji}$. $\square$

So both questions are polynomial: consistency in $O(n m)$ and the minimal network in $O(n^3)$. When all bounds are integers, the distances are integers, so an integer solution exists whenever a real one does, and the bounds of the minimal network are reached by integer solutions. The tests check this by brute force over small integer domains.

**Decomposability.** Dechter, Meiri and Pearl (1991) also show that the minimal network of an STP is decomposable: any assignment to a subset of the time points that meets the constraints of the minimal network among them extends to a solution. So a solution can be built one time point at a time without backtracking, by choosing each value inside the bounds that the earlier choices leave.

**Hardness of the TCSP.** With two intervals in some constraints, deciding consistency is NP-hard, by a reduction in Dechter, Meiri and Pearl (1991). So the gap between STP and TCSP is the gap between one interval and two.

## Reductions

- **To shortest paths.** Theorems 1 and 2 reduce the STP to [negative cycle detection](/negative-cycle-detection/) and to [all-pairs shortest paths](/all-pairs-shortest-paths/).
- **Equal to conjunctive difference logic.** Each STP constraint is a pair of difference atoms $X_j - X_i \le b$ and $X_i - X_j \le -a$, and each atom is a one-sided STP constraint. So the STP and the theory part of [difference logic](/difference-logic-satisfiability/) are the same problem. The two names come from different fields.
- **To linear programming.** The STP is a [linear programming](/linear-programming-problem/) feasibility problem whose matrix is the transpose of a graph incidence matrix. It is totally unimodular, which gives a second proof that integer data have integer solutions.
- **In timed systems.** The minimal network is the canonical [difference bound matrix](/difference-bound-matrix/) used for the zones of timed automata.

## Applications

- Planning and scheduling with time windows and durations, as in the plan executives of spacecraft, where a dispatcher uses the minimal network to choose times while the plan runs.
- Project scheduling with minimum and maximum time lags between activities.
- The subproblem that solvers for TCSP, DTP and [job shop scheduling](/job-shop-scheduling/) check at each node of their search.

## References
