---
tag: V5J5TR
kind: problem
slug: multi-objective-knapsack
name: Multi-objective knapsack problem
aliases:
- multidimensional knapsack
- bi-objective knapsack
- multiobjective 0-1 knapsack
- bicriteria knapsack
area: optimization/multi-objective
level: advanced
summary: Knapsack with several profit objectives whose Pareto optimal selections are sought.
prereqs: [knapsack-problem, knapsack-dynamic-programming, pareto-front]
see_also: [knapsack-fptas, multi-objective-shortest-path, multi-objective-minimum-spanning-tree, approximate-pareto-set, weighted-sum-method, epsilon-constraint-method, pareto-front-computation]
sources:
  - paper: doi:10.1016/j.cor.2007.09.009
    title: Cristina Bazgan, Hadrien Hugot and Daniel Vanderpooten, Solving efficiently the 0-1 multi-objective knapsack problem, Computers and Operations Research 36(1), 2009
    locator: pages 260 to 279 (the dynamic program over the items with dominance relations between states)
  - paper: doi:10.1023/A:1008258310679
    title: M. Visée, J. Teghem, M. Pirlot and E. L. Ulungu, Two-phases method and branch and bound procedures to solve the bi-objective knapsack problem, Journal of Global Optimization 12(2), 1998
    locator: pages 139 to 155 (supported points by weighted sums, then the other points by branch and bound in the triangles)
  - paper: doi:10.1287/mnsc.48.12.1603.445
    title: Thomas Erlebach, Hans Kellerer and Ulrich Pferschy, Approximating multiobjective knapsack problems, Management Science 48(12), 2002
    locator: pages 1603 to 1612 (a fully polynomial approximation scheme for the Pareto set with a fixed number of objectives)
  - paper: doi:10.1109/SFCS.2000.892068
    title: Christos H. Papadimitriou and Mihalis Yannakakis, On the approximability of trade-offs and optimal access of Web sources, FOCS 2000
    locator: pages 86 to 92 (epsilon-approximate Pareto sets of polynomial size)
  - book: isbn:9783540402862
    title: Hans Kellerer, Ulrich Pferschy and David Pisinger, Knapsack Problems, Springer, 2004
    locator: the section on multiobjective knapsack problems
  - book: isbn:9783540213987
    title: Matthias Ehrgott, Multicriteria Optimization, second edition, Springer, 2005
    locator: Chapter 10 (multicriteria versions of NP-hard combinatorial problems, the knapsack problem)
---

The multi-objective knapsack problem gives each item a weight and several profits, for example money and benefit to users, and asks for all subsets that fit into the knapsack and are [Pareto optimal](/pareto-optimality/) for the profits. With one profit it is the [knapsack problem](/knapsack-problem/). With two profits the [Pareto front](/pareto-front/) can have exponentially many points, and some of them are unsupported, so a [weighted sum](/weighted-sum-method/) of the profits cannot find them. A dynamic program over the items with dominance tests between states finds the whole front in pseudo-polynomial time for a fixed number of profits, and the front has approximations of polynomial size that can be computed in polynomial time. It is not the same problem as the multidimensional knapsack problem, which has one profit and several weight constraints.

## In plain words

You pack a bag that can carry a fixed weight. Each item has a weight and two values, for example its price and how much you like it. You want both totals high. One packing beats another if it is at least as good in both totals and better in one. The task is to list every packing that fits and that no other packing that fits beats.

The packings that win are a set of trade-offs. Some of them are hidden: no fixed mix of the two values, such as "price plus twice the liking", ranks them first, though nothing beats them.

## Definition

**Convention.** On this page all objectives are **maximized**, as is usual for knapsack problems. The number of objectives is $p \ge 2$, and $y = f(x)$ is the image of $x$. A vector $u$ dominates $v$ when $u_i \ge v_i$ for each $i$ and $u \ne v$. To use the minimization convention of the other pages, negate all profits.

**Input.** $n$ items. Item $j$ has a weight $w_j \ge 0$ and a profit vector $c_j \in \mathbb{R}^p_{\ge 0}$. A capacity $W \ge 0$.

**Feasible solutions.** The vectors $x \in \{0, 1\}^n$ with $\sum_j w_j x_j \le W$, that is, the subsets of items that fit.

**Objectives.** $f_i(x) = \sum_j c_{ij} x_j$ for $i = 1, \ldots, p$.

**Output.** The nondominated set $Y_N$ of $\{f(x) : x \text{ feasible}\}$, with one feasible $x$ for each $y \in Y_N$.

**Not the multidimensional knapsack problem.** The name "multidimensional knapsack" is sometimes used for this problem by mistake. The multidimensional knapsack problem has one profit and several weight constraints $\sum_j w_{kj} x_j \le W_k$, and asks for one optimal subset. The two problems meet only in the [epsilon-constraint method](/epsilon-constraint-method/): turning all profits but one into constraints $\sum_j c_{ij} x_j \ge \varepsilon_i$ gives a knapsack problem with several constraints.

## Variants

- **Bi-objective knapsack.** The case $p = 2$, the most studied one.
- **Several constraints.** Several objectives and several weight constraints together: the multi-objective multidimensional knapsack problem, a common test problem for evolutionary methods.
- **Unbounded and bounded versions.** Each item can be taken several times, up to a bound or without one.
- **Multi-objective subset sum and assignment.** Close relatives with the same kind of dynamic program.
- **Weighted sum.** Maximize $\sum_i \lambda_i f_i(x)$ with $\lambda > 0$: a knapsack problem with the profits $\sum_i \lambda_i c_{ij}$. It finds only supported points.
- **Approximate front.** Find a set of feasible subsets such that every point of $Y_N$ is reached within the factor $1 - \varepsilon$ in every objective by one of them. See [approximate Pareto set](/approximate-pareto-set/).

## Examples

Take four items and the capacity $W = 8$:

| item | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| weight | 2 | 3 | 4 | 5 |
| profits | $(5, 1)$ | $(4, 3)$ | $(2, 6)$ | $(1, 8)$ |

The subsets that fit and their profits are $\emptyset = (0, 0)$, $\{1\} = (5, 1)$, $\{2\} = (4, 3)$, $\{3\} = (2, 6)$, $\{4\} = (1, 8)$, $\{1, 2\} = (9, 4)$, $\{1, 3\} = (7, 7)$, $\{1, 4\} = (6, 9)$, $\{2, 3\} = (6, 9)$ and $\{2, 4\} = (5, 11)$. The front is

$$Y_N = \{(9, 4),\ (7, 7),\ (6, 9),\ (5, 11)\}.$$

The point $(6, 9)$ comes from two subsets. The points $(7, 7)$ and $(6, 9)$ are unsupported: the segment from $(9, 4)$ to $(5, 11)$ has the second coordinate $7.5$ at $y_1 = 7$ and $9.25$ at $y_1 = 6$, so both points lie below it. For weights $\lambda > 0$, the weighted sum of one of the end points is larger, so no weighted sum finds them, while the [epsilon-constraint method](/epsilon-constraint-method/) "maximize $y_1$ subject to $y_2 \ge 7$" finds $(7, 7)$.

**Exponentially many points.** For $i = 0, \ldots, k - 1$ take two items of weight $2^i$, one with profits $(2^i, 0)$ and one with profits $(0, 2^i)$, and let $W = 2^k - 1$. Every feasible subset has $y_1 + y_2$ equal to its weight, so at most $2^k - 1$. Taking exactly one item of each pair gives the weight $2^k - 1$ and the profits $(\sigma, 2^k - 1 - \sigma)$, where $\sigma$ can be any of the $2^k$ integers from $0$ to $2^k - 1$. These points all lie on the line $y_1 + y_2 = 2^k - 1$, so none dominates another, and every other feasible point is below that line and dominated by one of them. So $|Y_N| = 2^k$ for $2k$ items. The implementation checks this for $k \le 5$.

## Known algorithms

**Dynamic programming over the items.** A *state* is a triple: a weight, a profit vector, and the subset that gives them. Start with the empty subset. For item $j$, extend each state by item $j$ when it still fits. Then remove each state that another state beats: a weight that is not larger and a profit vector that is $\geqq$, with a difference. Removing it is safe because every set of later items that completes the removed state also completes the other state, with a weight that is not larger and profits that are $\geqq$.

```pseudo id=main
MO-KNAPSACK-DP(w, c, W)
L1  S ← {(0, 0, ∅)}                                   ▷ states (weight, profit vector, subset)
L2  for j ← 1 to n do
L3      N ← {(ω + w_j, v + c_j, T ∪ {j}) : (ω, v, T) ∈ S and ω + w_j ≤ W}
L4      S ← the states of S ∪ N that no other state beats, one for each pair (weight, profit vector)
L5  V ← the profit vectors of S, one subset each, without those that another profit vector dominates
L6  return V
```

On the example, the states after the four items have the weights and profits $(0; 0, 0)$, $(2; 5, 1)$, $(3; 4, 3)$, $(4; 2, 6)$, $(5; 9, 4)$, $(5; 1, 8)$, $(6; 7, 7)$, $(7; 6, 9)$ and $(8; 5, 11)$. Item 4 makes the state $(7; 6, 9)$ again from $\{1, 4\}$, and line L4 keeps one copy. Line L5 then keeps the four points of $Y_N$.

**Correctness.** By induction on $j$, for every feasible subset $T$ of the first $j$ items, $S$ holds a state with a weight not larger than that of $T$ and a profit vector $\geqq$ that of $T$. For $j = n$ this means that every point of $Y_N$ is $\leqq$ the profit vector of some state, and since that vector is feasible, it equals the point. Line L5 removes the rest.

**Cost.** Every state of $S$ after line L4 is a different pair of weight and profit vector. For $p = 2$ with integer weights and profits, two kept states with the same weight and first profit have the same second profit, so $|S| \le (W + 1)(n C + 1)$, where $C$ is the largest profit. So the method is pseudo-polynomial for a fixed $p$, but exponential in the input size, as the example with $2^k$ points requires. Bazgan, Hugot and Vanderpooten (2009) add more dominance tests that remove states that cannot reach the front, for example by bounds on the best completion, and solve bi-objective instances with hundreds of items.

**Two-phase method.** For $p = 2$, phase one finds the supported extreme points with a dichotomic search of weighted sums, each one a knapsack problem. Phase two searches each triangle between two neighboring supported points for the unsupported points, by branch and bound (Visée, Teghem, Pirlot and Ulungu, 1998).

**Epsilon constraint.** Maximize $f_1$ subject to $f_i(x) \ge \varepsilon_i$ for $i \ge 2$, a knapsack problem with several constraints, and move the bounds as in the [epsilon-constraint method](/epsilon-constraint-method/).

**Approximation.** For a fixed $p$, Erlebach, Kellerer and Pferschy (2002) give a fully polynomial approximation scheme: in time polynomial in $n$ and $1/\varepsilon$, it finds a set of feasible subsets such that every point of $Y_N$ is within the factor $1 - \varepsilon$ in every objective of one of them. The existence of such sets of polynomial size follows from Papadimitriou and Yannakakis (2000). The method rounds the profits to a geometric grid, as the single-objective [FPTAS for knapsack](/knapsack-fptas/) rounds them to a linear one.

## Bounds

- **Hardness of one point.** With $p = 1$ the problem is the [knapsack problem](/knapsack-problem/), which is NP-hard. So deciding whether some feasible $x$ has $f(x) \geqq b$ is NP-complete for every $p \ge 1$.
- **Size of the front.** The example with pairs of items gives $|Y_N| = 2^k$ with $n = 2k$ items, so the front can be exponential in $n$, for $p = 2$ already. No algorithm lists it in polynomial time.
- **Pseudo-polynomial size.** With integer profits at most $C$, the points of $Y_N$ have different values of $(y_1, \ldots, y_{p-1})$, each coordinate in $\{0, \ldots, n C\}$, so $|Y_N| \le (n C + 1)^{p-1}$.
- **Approximation.** For fixed $p$ and $\varepsilon > 0$, an approximate front of size polynomial in $n$ and $1/\varepsilon$ exists and can be computed in polynomial time. For the version with several weight constraints, a fully polynomial scheme does not exist unless P = NP, because the single-objective problem with two constraints already has none.

## Reductions

- **To the knapsack problem.** The weighted sum, the lexicographic version and each step of the two-phase method are single-objective knapsack problems.
- **To a path problem.** Build a layered acyclic graph with one layer of $W + 1$ weight values for each item. Taking item $j$ is an arc that adds $w_j$ to the weight and $c_j$ to the profits; leaving it is an arc that adds nothing. The front of the knapsack problem is the front of the longest paths from the start to the last layer, a [multi-objective shortest path](/multi-objective-shortest-path/) problem after negating the profits. The dynamic program above is the label method on this graph.
- **From subset sum.** The construction with pairs of items shows how a front point $(T, \sum_i a_i - T)$ exists exactly when some subset of the numbers $a_i$ sums to $T$, as in the reduction from [subset sum](/subset-sum-problem/).
- **To finite Pareto filtering.** Line L4 and line L5 are instances of [Pareto front computation](/pareto-front-computation/).

## Applications

- **Capital budgeting.** Choose projects within a budget with several returns, such as profit, social benefit and low risk.
- **Portfolio and product selection.** Pick items within a budget with several measures of value.
- **Test problems for evolutionary methods.** The multi-objective knapsack problem with several constraints is a standard test for [SPEA2](/spea2/), [NSGA-II](/nsga-ii/) and [MOEA/D](/moea-d/).
- **Subproblems.** Bi-objective knapsack problems appear inside column generation and decomposition methods for larger problems with several objectives.

## References
