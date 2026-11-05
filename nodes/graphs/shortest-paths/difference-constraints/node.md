---
tag: X3KB9P
kind: problem
slug: difference-constraints
name: System of difference constraints
aliases:
- Difference constraints
area: graphs/shortest-paths
level: core
summary: Linear feasibility problem whose constraints each bound the difference of two variables, solvable as a shortest-paths problem on a constraint graph.
prereqs: [bellman-ford, negative-cycle, linear-programming-problem]
see_also: [bellman-ford, negative-cycle-detection, shortest-paths-lp-formulation, potential-function-reduced-costs, simple-temporal-problem, difference-bound-matrix, floyd-warshall, lp-duality]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 22.4, Difference constraints and shortest paths (the constraint graph, feasibility if and only if no negative cycle, and the solution x_i = δ(v_0, v_i))
  - paper: doi:10.1016/0004-3702(91)90006-6
    title: Rina Dechter, Itay Meiri and Judea Pearl, Temporal constraint networks, Artificial Intelligence 49(1-3), 61 to 95 (1991)
    locator: the section on the simple temporal problem (the distance graph, consistency and the minimal network by all-pairs shortest paths)
  - paper: doi:10.1007/BF01759032
    title: Charles E. Leiserson and James B. Saxe, Retiming synchronous circuitry, Algorithmica 6(1-6), 5 to 35 (1991)
    locator: the reduction of retiming to a system of difference constraints solved by Bellman-Ford
  - paper: doi:10.1145/322276.322288
    title: Robert Shostak, Deciding linear inequalities by computing loop residues, Journal of the ACM 28(4), 769 to 779 (1981)
    locator: the whole paper (systems with two variables per inequality, which generalize difference constraints)
---

A system of difference constraints is a set of linear inequalities of the form $x_j - x_i \le b_k$, each bounding the difference of two real variables by a constant, and the problem is to find values for the variables that satisfy all of them or to report that none exist. Each constraint becomes an edge $v_i \to v_j$ of weight $b_k$ in a constraint graph, and the system is feasible exactly when this graph has no [negative cycle](/negative-cycle/). Shortest-path distances from an added source are then a solution, so [Bellman-Ford](/bellman-ford/) solves a system of $m$ constraints in $n$ variables in $O(nm)$ time. This special [linear program](/linear-programming-problem/) is the model behind scheduling with time windows, the simple temporal problem, and circuit retiming.

## In plain words

Say several jobs must start at certain times, and you only know rules like "job B starts at least 3 hours after job A" or "job C starts at most 6 hours after job A". Each rule compares two start times.

Draw a dot for each job and an arrow for each rule, labeled with its number of hours. A rule that says "at most" gives an arrow that limits how far apart two times may be, just like a road limits how far you can get. Then the shortest distances in this map give start times that obey every rule.

If some loop of arrows adds up to a negative number, the rules contradict each other: following the loop says a time must come before itself. Then no schedule exists.

## Definition

**Input.** Real variables $x_1, \ldots, x_n$ and $m$ constraints, the $k$-th of the form $x_{j_k} - x_{i_k} \le b_k$ with $b_k \in \mathbb{R}$.

**Output.** A vector $x \in \mathbb{R}^n$ that satisfies every constraint, or a report that the system is infeasible, ideally with a certificate: a set of constraints whose sum gives $0 \le c$ with $c < 0$.

**Constraint graph.** The graph has a vertex $v_i$ for each variable, an extra vertex $v_0$, an edge $v_i \to v_j$ of weight $b_k$ for each constraint $x_j - x_i \le b_k$, and an edge $v_0 \to v_i$ of weight 0 for each $i$.

**Theorem.** The system is feasible if and only if the constraint graph has no negative cycle. If it is feasible, $x_i = \delta(v_0, v_i)$ is a solution.

*Proof.* If there is no negative cycle, all distances from $v_0$ are finite (each $v_i$ is reachable by its edge of weight 0) and satisfy $\delta(v_0, v_j) \le \delta(v_0, v_i) + b_k$ for each edge, which is the constraint. If there is a negative cycle, it does not use $v_0$, which has no entering edge; adding the constraints of its edges, each variable on the cycle appears once with $+$ and once with $-$, and the sum reads $0 \le w(C) < 0$, which no $x$ satisfies. $\blacksquare$

**Weight assumptions.** The constants $b_k$ are any real numbers; negative ones are common (they express "at least") and must be allowed, so the solver must handle negative weights and detect negative cycles. There is no nonnegativity or integer assumption. If all $b_k$ are integers, the distances are integers, so the system has an integer solution whenever it has any.

## Variants

- **Equalities.** $x_j - x_i = b$ is the pair $x_j - x_i \le b$ and $x_i - x_j \le -b$.
- **Bounds on one variable.** $x_i \le c$ and $x_i \ge c$ use a variable $x_0$ fixed at 0: $x_i - x_0 \le c$ and $x_0 - x_i \le -c$. Then the solution must be shifted so that $x_0 = 0$.
- **Strict inequalities.** Over the integers, $x_j - x_i < b$ is $x_j - x_i \le b - 1$. Over the reals, strict constraints need weights of the form $(b, -\varepsilon)$ compared lexicographically, as in the difference-bound matrices of [timed automata](/timed-automata/).
- **Tightest bounds between all pairs.** All-pairs distances $\delta(v_i, v_j)$ give the largest possible value of $x_j - x_i$ over all solutions. This is the minimal network of the [simple temporal problem](/simple-temporal-problem/), computed by [Floyd-Warshall](/floyd-warshall/), and the canonical form of a [difference-bound matrix](/difference-bound-matrix/).
- **Two variables per inequality.** Constraints $a x_i + b x_j \le c$ with any coefficients generalize the problem. They remain solvable in polynomial time, but by different methods (Shostak 1981 and later work).
- **Integer solutions.** With integer constants, a feasible system of difference constraints always has an integer solution, the distances. For two-variable constraints with other coefficients this fails, and finding an integer solution is [NP-hard](/np-hard/) in general.

## Examples

**A schedule.** Four jobs with start times $x_1, \ldots, x_4$ and the rules: job 2 starts at least 3 after job 1, job 3 at least 2 after job 2, job 3 at most 6 after job 1, job 4 at least 1 after job 3, job 4 at most 7 after job 1.

| rule | constraint | edge |
|---|---|---|
| $x_2 \ge x_1 + 3$ | $x_1 - x_2 \le -3$ | $v_2 \to v_1$, $-3$ |
| $x_3 \ge x_2 + 2$ | $x_2 - x_3 \le -2$ | $v_3 \to v_2$, $-2$ |
| $x_3 \le x_1 + 6$ | $x_3 - x_1 \le 6$ | $v_1 \to v_3$, $6$ |
| $x_4 \ge x_3 + 1$ | $x_3 - x_4 \le -1$ | $v_4 \to v_3$, $-1$ |
| $x_4 \le x_1 + 7$ | $x_4 - x_1 \le 7$ | $v_1 \to v_4$, $7$ |

With $v_0$ and its edges of weight 0, Bellman-Ford gives $\delta(v_0, \cdot) = (-6, -3, -1, 0)$. Check: $x_2 - x_1 = 3$, $x_3 - x_2 = 2$, $x_3 - x_1 = 5 \le 6$, $x_4 - x_3 = 1$, $x_4 - x_1 = 6 \le 7$. Adding 6 to every value gives the schedule $(0, 3, 5, 6)$, which also works, since the constraints only see differences.

**An infeasible schedule.** Change the third rule to "job 3 at most 4 after job 1". The cycle $v_1 \to v_3 \to v_2 \to v_1$ has weight $4 - 2 - 3 = -1$. Adding its constraints: $(x_3 - x_1) + (x_2 - x_3) + (x_1 - x_2) \le 4 - 2 - 3$, that is $0 \le -1$. Job 3 must start at least 5 after job 1 and at most 4 after it. Bellman-Ford finds a relaxable edge in its last pass and reports this cycle.

**No unreachable vertices.** The source $v_0$ reaches every $v_i$ by an edge of weight 0, so every distance is finite. Without $v_0$, a run from $v_1$ would leave $\delta = +\infty$ at variables that no constraint chain links to $x_1$, such as a variable that only appears as $x_1 - x_5 \le 2$ (an edge $v_5 \to v_1$). Such variables are free in one direction, and $v_0$ gives them the value 0.

## Known algorithms

| algorithm | time | notes |
|---|---|---|
| [Bellman-Ford](/bellman-ford/) from $v_0$ | $O(nm)$ | returns a solution or a negative cycle as certificate |
| [SPFA](/spfa/) or [Goldberg-Radzik](/goldberg-radzik/) | $O(nm)$ | faster in practice |
| [Goldberg's scaling algorithm](/goldberg-scaling-sssp/) | $O(\sqrt{n}\, m \log N)$ | integer constants $b_k \ge -N$ |
| [Near-linear negative SSSP](/near-linear-negative-sssp/) | $O(m \log^{O(1)} n \log N)$ | integer constants |
| [Floyd-Warshall](/floyd-warshall/) | $\Theta(n^3)$ | all tightest bounds $\max(x_j - x_i)$ |
| General [linear programming](/linear-programming-problem/) | polynomial | ignores the structure |

## Bounds

Bellman-Ford gives $O(nm)$ for real constants, where $n$ is the number of variables and $m$ the number of constraints. For integer constants with $|b_k| \le N$, near-linear algorithms solve the problem in $O(m \log^{O(1)} n \log N)$. Any algorithm must read every constraint, so $\Omega(n + m)$ is a lower bound. The problem is equivalent to negative cycle detection (see Reductions), so its complexity is exactly that of [negative cycle detection](/negative-cycle-detection/).

## Reductions

- **To shortest paths.** The constraint graph above, one vertex per variable plus $v_0$ and one edge per constraint.
- **From negative cycle detection.** A weighted graph has no negative cycle if and only if the system $x_v - x_u \le w(u, v)$, one constraint per edge, is feasible. So the two problems are the same.
- **Feasible potentials.** A solution $x$ is exactly a [potential](/potential-function-reduced-costs/) under which every reduced cost $w(u, v) + x_u - x_v$ is nonnegative. This is how [Johnson's algorithm](/johnson/) uses Bellman-Ford.
- **Linear programming duality.** The system is an LP whose matrix is the transpose of an incidence matrix. Its dual is a circulation problem, and by [LP duality](/lp-duality/) infeasibility is witnessed by a negative cycle; see the [LP formulation of shortest paths](/shortest-paths-lp-formulation/).
- **Extremal solutions.** Among the solutions with $x_i \le 0$, the distances from $v_0$ are the largest in every coordinate, and they maximize $\sum_i x_i$.

## Applications

- **Scheduling with time windows.** Precedence with delays and deadlines, as in the example; the [simple temporal problem](/simple-temporal-problem/) of AI planning is exactly this.
- **Circuit retiming.** Leiserson and Saxe reduce the question of whether registers can be moved to meet a clock period to a system of difference constraints in the retiming lags.
- **Layout compaction.** In VLSI layout, spacing rules between pairs of features are difference constraints in their coordinates.
- **Verification of timed systems.** Zones of clock values in [timed automata](/timed-automata/) are sets of difference constraints, kept in canonical form by all-pairs shortest paths.
- **Program analysis.** Abstract domains of differences (the "zone" domain) bound $x - y$ for program variables in the same way.

## References
