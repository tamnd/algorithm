---
tag: 45YQ3P
kind: definition
slug: partial-solution
name: Partial solution
aliases:
- partial assignment
- prefix candidate
area: techniques/backtracking
level: intro
summary: A candidate that fixes only some of the decisions needed for a complete solution.
prereqs: [constraint-satisfaction-problem]
see_also: [state-space-tree, generic-backtracking-algorithm, search-tree-pruning, chronological-backtracking, incumbent-solution, bounding-function]
sources:
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2
    locator: Section 7.2.2, Backtrack programming (partial solutions and the properties P_l)
  - paper: doi:10.1145/321296.321300
    title: Solomon W. Golomb and Leonard D. Baumert, Backtrack programming, Journal of the ACM 12(4), 1965
    locator: pp. 516 to 524
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing
    locator: Chapter 5 (partial assignments and consistency in backtracking search)
---

A partial solution is a candidate that fixes only some of the decisions of a complete solution, for example the first $k$ values $x_1, \ldots, x_k$ of a sequence of $n$ decisions, or the values of some of the variables of a [constraint satisfaction problem](/constraint-satisfaction-problem/). Partial solutions are the nodes of the [state space tree](/state-space-tree/), and [backtracking](/generic-backtracking-algorithm/) and branch and bound work by testing them. The test is useful only when it is sound: a partial solution may be rejected only when no complete solution extends it.

## Definition

Let a problem have complete candidates $x = (x_1, \ldots, x_n)$ with $x_j \in D_j$, and let $S \subseteq D_1 \times \cdots \times D_n$ be its set of solutions.

A **partial solution** of length $k$, with $0 \le k \le n$, is a sequence $(x_1, \ldots, x_k)$ with $x_j \in D_j$ for each $j \le k$. It fixes the first $k$ decisions and leaves the others open. The empty sequence is the partial solution of length 0. A complete candidate $y$ **extends** $(x_1, \ldots, x_k)$ when $y_j = x_j$ for each $j \le k$.

For a [constraint satisfaction problem](/constraint-satisfaction-problem/) the decisions need not come in a fixed order. There, a **partial assignment** is a function $a$ from a set of variables $Y \subseteq \{X_1, \ldots, X_m\}$ to values, with $a(X_i) \in D_i$. It is **consistent** when it violates no constraint whose variables all lie in $Y$.

A family of tests $P_k$ on partial solutions of length $k$ is:

- **sound** (or necessary) when, for each $k$, each partial solution $(x_1, \ldots, x_k)$ that some solution in $S$ extends satisfies $P_k$. Equivalently, $\neg P_k(x_1, \ldots, x_k)$ implies that no solution extends $(x_1, \ldots, x_k)$;
- **prefix-closed** (or monotone) when $P_{k+1}(x_1, \ldots, x_{k+1})$ implies $P_k(x_1, \ldots, x_k)$;
- **exact at the leaves** when $P_n(x_1, \ldots, x_n)$ holds if and only if $x \in S$.

With a sound family that is exact at the leaves, cutting every partial solution that fails its test loses no solution, and the leaves that survive are exactly the solutions. Consistency of a partial assignment is sound, prefix-closed and exact at the leaves for each CSP, because a constraint that is checked on a smaller assignment is also checked on each larger one.

A partial solution is **alive** (or feasible) when it satisfies its test, and **dead** when it fails it or when all its extensions have been searched.

## Examples and non-examples

- **Queens.** In the $n$-queens problem with one queen per row, the partial solution $(x_1, \ldots, x_k)$ places queens in rows 1 to $k$. The test "no two of these queens attack each other" is sound, prefix-closed and exact at the leaves. For $n = 4$, the partial solution $(1, 3)$ passes the test but has no extension that passes: each column of row 3 is attacked. A sound test does not promise that an alive partial solution extends to a solution.
- **A CSP.** With variables $X_1, X_2, X_3$ over $\{1, 2, 3\}$ and the constraints $X_1 < X_2$ and $X_2 < X_3$, the partial assignment $\{X_1 = 2, X_3 = 3\}$ is consistent, because no constraint has both its variables assigned. It has no consistent extension, because $X_2$ would have to satisfy $2 < X_2 < 3$. The partial assignment $\{X_1 = 1, X_2 = 2\}$ extends to the solution $(1, 2, 3)$.
- **Knapsack.** In the 0-1 knapsack problem, the partial solution $(x_1, \ldots, x_k) \in \{0,1\}^k$ decides items 1 to $k$. The test "the chosen weight is at most the capacity" is sound, because weights are non-negative and the items not yet decided can all be left out. Branch and bound adds a second, value-based test from a [bounding function](/bounding-function/).
- **Subset sum with a target.** For non-negative numbers $a_1, \ldots, a_n$ and the target $t$, the test $\sum_{j \le k} a_j x_j \le t$ is sound. With a negative number it is not sound: for $a = (5, -3)$ and $t = 2$, the partial solution $(1)$ has sum $5 > 2$, but the solution $(1, 1)$ extends it.
- **Non-example: a complete candidate.** A sequence with all $n$ decisions fixed is a partial solution of length $n$ only in the trivial sense. It is a leaf of the state space tree and is tested by $P_n$, the condition of the problem.
- **Non-example: a test that needs the future.** For subset sum, the test "the chosen sum equals $t$" applied at depth $k < n$ is not sound: it rejects $(1)$ for $a = (3, 4)$ and $t = 7$, although $(1, 1)$ is a solution. The equality may be tested only at the leaves.
- **Non-example: a heuristic score.** A rule "reject the partial solution if its estimated value is poor" is not a sound test unless the estimate is a proven bound. A cut by such a rule can lose the optimum.

## Related definitions

- The [state space tree](/state-space-tree/) has the partial solutions as nodes.
- [Search tree pruning](/search-tree-pruning/) cuts a partial solution and all its extensions by a sound test.
- The [generic backtracking algorithm](/generic-backtracking-algorithm/) visits exactly the partial solutions whose prefixes all pass the test, and [chronological backtracking](/chronological-backtracking/) is the same search for a CSP.
- In branch and bound, a partial solution stands for the set of its extensions, a subproblem. The [bounding function](/bounding-function/) bounds the best value of the subproblem, and the [incumbent solution](/incumbent-solution/) is the best complete solution found so far.
- A [consistent](/constraint-satisfaction-problem/) partial assignment of a CSP is the CSP form of an alive partial solution. Stronger tests such as [forward checking](/forward-checking/) and [arc consistency](/arc-consistency/) reject more partial assignments and stay sound.

## References
