---
tag: EKM5SR
kind: algorithm
slug: leaps-and-bounds
name: Leaps and bounds algorithm
aliases:
- Furnival-Wilson algorithm
- best subset regression
area: statistics-and-inference/regression-and-diagnostics
level: advanced
summary: "An exact branch and bound search for the subsets of each size with the smallest residual sum of squares. It cuts every branch whose bound shows that it cannot win."
model: real-ram
complexity:
  vars: {n: the number of observations, m: the number of candidate columns, v: "the number of search nodes visited, at most 2^(m+1) - 1"}
  time: {worst: "Θ(n m^2 + 2^m m^2)", best: "Θ(n m^2 + m^3)"}
  space: {extra: "Θ(m^3)"}
  flops: {worst: "n m^2 + 2 m^3 + 2 v m^2"}
properties: {deterministic: true, exact: true, online: false, recursive: true}
history:
  year: 1974
  people: [George M. Furnival, Robert W. Wilson Jr.]
  note: Furnival and Wilson combined the bound that a subset never fits better than a superset with an ordering of Gauss-Jordan pivots, and found the best subsets of each size without fitting most of the 2^m models.
prereqs: [stepwise-regression, depth-first-branch-and-bound, bounding-function, ordinary-least-squares]
see_also: [np-hard, mixed-integer-programming, lasso-regression, bayesian-information-criterion, akaike-information-criterion, feature-selection, post-selection-inference, coefficient-of-determination]
sources:
  - paper: doi:10.1080/00401706.1974.10489231
    title: "George M. Furnival and Robert W. Wilson, Jr., Regressions by leaps and bounds, Technometrics 16(4), 1974, pp. 499 to 511"
    locator: The whole paper (the bound by the residual sum of squares of a superset, the pair of search trees of pivots, and the timings)
  - paper: doi:10.1080/00401706.1967.10490502
    title: "R. R. Hocking and R. N. Leslie, Selection of the best subset in regression analysis, Technometrics 9(4), 1967, pp. 531 to 540"
    locator: The whole paper (an earlier search that skips subsets by comparing reductions in the residual sum of squares)
  - paper: doi:10.1093/biomet/54.3-4.357
    title: "E. M. L. Beale, M. G. Kendall and D. W. Mann, The discarding of variables in multivariate analysis, Biometrika 54(3/4), 1967, pp. 357 to 366"
    locator: The whole paper (an early method that avoids the full enumeration of subsets)
  - paper: doi:10.1080/00949658208810560
    title: "William J. Welch, Algorithmic complexity: three NP-hard problems in computational statistics, Journal of Statistical Computation and Simulation 15(1), 1982, pp. 17 to 25"
    locator: The whole paper (best subset regression of a given size is NP-hard)
  - paper: doi:10.1137/S0097539792240406
    title: "B. K. Natarajan, Sparse approximate solutions to linear systems, SIAM Journal on Computing 24(2), 1995, pp. 227 to 234"
    locator: The whole paper (finding the sparsest solution within a given residual norm is NP-hard)
  - paper: doi:10.1214/15-AOS1388
    title: "Dimitris Bertsimas, Angela King and Rahul Mazumder, Best subset selection via a modern optimization lens, Annals of Statistics 44(2), 2016, pp. 813 to 852"
    locator: The whole paper (best subset as a mixed integer quadratic program, solved with certificates of optimality for much larger problems)
  - paper: doi:10.1214/19-STS733
    title: "Trevor Hastie, Robert Tibshirani and Ryan Tibshirani, Best subset, forward stepwise or lasso? Analysis and recommendations based on extensive comparisons, Statistical Science 35(4), 2020, pp. 579 to 592"
    locator: The whole paper (simulations in which best subset beats the lasso at high signal to noise ratio and loses at low)
  - book: isbn:9781584881711
    title: Alan Miller, Subset Selection in Regression, second edition, Chapman and Hall/CRC, 2002
    locator: Chapter 3 (generating all subsets, branch and bound and the Furnival-Wilson method)
---

Best subset regression is the problem of finding, for each size $s$, the subset of $s$ of the $m$ candidate columns whose least squares fit has the smallest residual sum of squares. The leaps and bounds algorithm of Furnival and Wilson (1974) is one exact algorithm for that problem; others are full enumeration and mixed integer programming. It is a [depth-first branch and bound](/depth-first-branch-and-bound/) search over the $2^m$ subsets. Its bound is that a subset never has a smaller residual sum of squares than a superset, so the fit of the largest model below a node bounds every model below it. Each node of the search costs one sweep of an $(m + 1) \times (m + 1)$ matrix. The answer is exactly the one that fitting all $2^m$ models would give, and in practice the search visits a small fraction of them, which makes it usable for $m$ up to about 30 to 40.

## In plain words

Suppose there are 20 candidate predictors and the goal is the best model with 5 of them. There are 15,504 such models, and the best model of every size needs about a million fits. Leaps and bounds avoids most of them. It walks a tree of choices: at each step one predictor is put in or kept out for good. Before going down a branch it fits the largest model in that branch. Removing predictors can only make a fit worse, so if even that largest model is no better than the best models found so far, nothing in the branch can be, and the branch is skipped. The result is the true best, not a guess, which is what [stepwise regression](/stepwise-regression/) gives.

## The problem

**Input.** An $n \times m$ matrix $X$ of candidate columns, a response $y \in \mathbb R^n$ with $n \ge m + 2$, and the number $k \ge 1$ of best subsets wanted per size. The columns of $X$ together with the intercept must be linearly independent.

**Model for a subset.** For $S \subseteq \{1, \dots, m\}$ the model is $y = b_0\mathbf 1 + X_Sb_S + \varepsilon$, with the coefficient vector written $b$; the intercept is always in. $\mathrm{RSS}(S)$ is the least squares residual sum of squares.

**Output.** For each $s = 0, 1, \dots, m$, the $k$ subsets of size $s$ with the smallest RSS and their RSS values. Ties are broken arbitrarily.

**Why sizes.** AIC, BIC, Mallows' $C_p$ and the adjusted $R^2$ all compare models of the same size by RSS alone: each is an increasing function of RSS for a fixed size. So the best model under any of them is among the $m + 1$ winners of the sizes, and one search serves every such criterion.

## The algorithm

The search uses the sweep operator of the stepwise page on the centered cross-product matrix $A$ of $(x_1, \dots, x_m, y)$, with $y$ as the last index. When $A$ is swept on a set $S$, its entry $A[y,y]$ is $\mathrm{RSS}(S)$; the reverse sweep removes a column again. A search node is a pair $(F, C)$ of disjoint sets: the subsets below it are the $T$ with $F \subseteq T \subseteq F \cup C$. The node carries $R$, the matrix swept on $F$, and $B$, the matrix swept on $F \cup C$. The cutoff for size $s$ is the RSS of the $k$-th best subset of size $s$ found so far, or $\infty$ if fewer than $k$ are known.

```pseudo id=main
LEAPS-AND-BOUNDS(X[1..n, 1..m], y[1..n], k)
L1  A ← centered cross-products of (x_1, ..., x_m, y)        ▷ (m + 1) × (m + 1)
L2  B ← A swept on 1, ..., m                                 ▷ B[y,y] = RSS of the full model; error if collinear
L3  record ∅ with RSS A[y,y], and {1, ..., m} with RSS B[y,y]
L4  VISIT(∅, {1, ..., m}, A, B)
L5  return the k best recorded subsets of each size

VISIT(F, C, R, B)                                            ▷ R swept on F, B swept on F ∪ C
L6  if C = ∅ then return
L7  if cutoff(s) ≤ B[y,y] for every s with |F| ≤ s ≤ |F| + |C| then return    ▷ the cut
L8  j ← the column of C with the largest B[j,y]² / (-B[j,j])                  ▷ dropping it from F ∪ C costs most
L9  R' ← R swept on j;  record F ∪ {j} with RSS R'[y,y]
L10 VISIT(F ∪ {j}, C \ {j}, R', B)
L11 B' ← B reverse swept on j;  record (F ∪ C) \ {j} with RSS B'[y,y]
L12 VISIT(F, C \ {j}, R, B')
```

Line L7 is the bound: every $T$ below the node has $\mathrm{RSS}(T) \ge \mathrm{RSS}(F \cup C) = B[y,y]$, and if that is already no better than the cutoff of every size the node covers, no subset below can enter a list. Line L8 puts the column that matters most into the "in" branch first, so good subsets are found early and the cutoffs fall fast; the "out" branch then has a larger bound and is cut more often. The quantity $B[j,y]^2/(-B[j,j])$ is the increase of RSS when $j$ is dropped from $F \cup C$. Furnival and Wilson organize the same nodes as a pair of trees of pivots that share work between them; the binary tree here has the same bound and the same answer.

## Example

Take the data of the stepwise page ($n = 10$, $x_1$, $x_2$, $x_3$ and $y$) and add a fourth column $x_4 = (-2, -1, -3, 2, 0, 0, -2, -3, -3, -3)$, with $k = 1$. The trace of the search, in depth-first order, with RSS(F) and the bound RSS(F ∪ C):

| node $F$; $C$ | RSS($F$) | bound | action |
|---|---|---|---|
| $\emptyset$; $\{1,2,3,4\}$ | 44.900 | 4.147 | branch on $x_1$ |
| $\{1\}$; $\{2,3,4\}$ | 44.899 | 4.147 | branch on $x_2$ |
| $\{1,2\}$; $\{3,4\}$ | 19.358 | 4.147 | branch on $x_3$ |
| $\{1,2,3\}$; $\{4\}$ | 4.169 | 4.147 | two leaves |
| $\{1,2\}$; $\{4\}$ | 19.358 | 8.829 | two leaves |
| $\{1\}$; $\{3,4\}$ | 44.899 | 18.785 | branch on $x_4$, four leaves below |
| $\emptyset$; $\{2,3,4\}$ | 44.900 | 20.283 | branch on $x_3$ |
| $\{3\}$; $\{2,4\}$ | 22.854 | 20.283 | branch on $x_2$ |
| $\{2,3\}$; $\{4\}$ | 20.340 | 20.283 | **cut**: cutoffs 19.358 (size 2) and 4.169 (size 3) are below 20.283 |
| $\{3\}$; $\{4\}$ | 22.854 | 22.040 | two leaves |
| $\emptyset$; $\{2,4\}$ | 44.900 | 25.734 | branch on $x_4$ |
| $\{4\}$; $\{2\}$ | 25.796 | 25.734 | **cut**: cutoffs 22.854 (size 1) and 19.358 (size 2) are below 25.734 |
| $\emptyset$; $\{2\}$ | 44.900 | 36.928 | two leaves |

The best subsets are $\emptyset$ (44.900), $\{3\}$ (22.854), $\{1, 2\}$ (19.358), $\{1, 2, 3\}$ (4.169) and $\{1, 2, 3, 4\}$ (4.147). The search visits 27 of the 31 nodes of the full tree. With four columns the two cuts save only leaves, because both subsets at a cut node were already recorded when the node was made. The saving grows quickly with $m$.

**Measured node counts.** For random data with $n = 4m$, normal columns with all correlations 0.5, slopes 1 on the first third of the columns, 0.3 up to half of them and 0 on the rest, normal noise with standard deviation 2, $k = 1$ and `random.Random(20261114)`:

| $m$ | 10 | 15 | 20 | 25 |
|---|---|---|---|---|
| nodes visited | 173 | 751 | 2707 | 26207 |
| fraction of $2^m$ | 0.169 | 0.023 | 0.0026 | 0.00078 |
| time of the Python code | under 0.01 s | 0.02 s | 0.14 s | 1.93 s |

The counts depend on the data: when many subsets of a size have nearly equal RSS, few nodes are cut. The worst case is the full tree.

## Correctness

The proof in this folder first shows the bound: if $T \subseteq U$ then $\mathrm{RSS}(T) \ge \mathrm{RSS}(U)$, because the column space of the larger model contains that of the smaller, and least squares over a larger space cannot fit worse. It then uses the sweep identities of the stepwise proof to show that $R$ and $B$ stay swept on $F$ and $F \cup C$, so every recorded RSS is exact. Every node has had both $F$ and $F \cup C$ recorded when it is visited, and branching splits the subsets below a node into those with $j$ and those without. So each subset is either recorded or lies below a cut node, and at a cut its RSS is at least the bound, which is at least the cutoff then, which is at least the final cutoff, because cutoffs only fall. Hence no unrecorded subset is strictly better than the $k$-th recorded one of its size, and the lists are exact.

## Complexity

The cross-products cost about $nm^2$ flops and the sweeps of line L2 about $2m^3$. Each visited node other than the root costs one sweep and one copy of an $(m + 1) \times (m + 1)$ matrix, $\Theta(m^2)$, plus $O(m)$ for lines L7 and L8. So the time is $\Theta(nm^2 + vm^2)$ with $v$ visited nodes. In the worst case nothing is cut and $v = 2^{m+1} - 1$. At least one node is needed per size, so $v \ge m$ in every case. The recursion holds two matrices per level and the depth is at most $m$, so the extra space is $\Theta(m^3)$. No algorithm is known to be polynomial in the worst case: best subset regression of a given size is NP-hard (Welch 1982; Natarajan 1995), cited here and not proved, so an exact method must expect exponential time on some inputs.

## Properties

- **Exact.** The output equals that of full enumeration, up to ties. This is the difference from stepwise regression.
- **Exact arithmetic is possible.** Only field operations are used, so with rational input the search and its RSS values are exact. With floating point the cut compares numbers with rounding error, so a subset whose RSS is within rounding of the cutoff can be lost; such a subset is a near tie.
- **One search, many criteria.** Every criterion that is increasing in RSS for each size is minimized by one of the size winners.
- **Wider lists.** With $k > 1$ the search returns the $k$ best of each size, which shows how many subsets are nearly as good as the winner; there are often many.

## Variants and improvements

- **Furnival and Wilson's two trees.** The original arranges the pivots so that the subsets are produced in an order that reuses work, and reports the best subsets by RSS, by adjusted $R^2$ or by $C_p$.
- **Bound on the criterion.** If only the best single model under a criterion $c$ is wanted, cut when $c(B[y,y], s) \ge$ the best value found for every $s$ the node covers. This cuts more than the per-size rule.
- **Mixed integer programming.** Bertsimas, King and Mazumder (2016) write best subset of size $s$ as a [mixed integer](/mixed-integer-programming/) quadratic program with big-M constraints and solve it with a modern solver, warm started by a first-order heuristic. This reaches much larger $m$ than leaps and bounds, often with a proof of optimality.
- **Convex relaxations.** The [lasso](/lasso-regression/) replaces the count of columns by the sum of absolute coefficients and is solved in polynomial time. It selects a different, shrunken model; Hastie, Tibshirani and Tibshirani (2020) found best subset better at high signal to noise ratio and the lasso better at low.

## When to use it

Use leaps and bounds when $m$ is at most about 30 to 40, the model is linear least squares, and the best subsets of each size are wanted, for example to see how the fit changes with size or how many subsets are nearly equally good. For larger $m$ use mixed integer programming or a penalized method. Remember that the best subset of a sample is a selected model: its RSS is optimistic, and its tests are not valid without a correction for the search (see [post-selection inference](/post-selection-inference/)). Choose the size by a criterion such as [BIC](/bayesian-information-criterion/) or by cross-validation of the whole search.

## Pitfalls

- **Over-reading the winner.** With many candidates, many subsets fit nearly as well as the best, and the winner changes with small changes of the data. Look at the $k$ best, not only the first.
- **Collinear columns.** The full model of line L2 must be of full rank. Remove exact duplicates first; nearly collinear columns make the sweeps inaccurate in floating point.
- **Generalized linear models.** The bound uses the exact RSS of least squares. For logistic or Poisson models the deviance of a subset is not obtained by a sweep; the usual workaround runs the search on the weighted least squares problem of the last IRLS step, which is an approximation.
- **Grouped columns.** The dummy columns of one factor should enter together; the plain search treats them as separate columns.

## Implementations

## History

Programs of the 1960s fitted all $2^m$ subsets in an order in which each subset is one pivot away from the one before. Beale, Kendall and Mann (1967) and Hocking and Leslie (1967) gave the first searches that skip subsets by bounding their fit. Furnival and Wilson (1974) combined the superset bound with an ordering of the pivots, found the best subsets of each size for far more columns than full enumeration allows, and their method became the standard all-subsets routine. Welch (1982) proved that the problem is NP-hard. Bertsimas, King and Mazumder (2016) brought mixed integer programming to the problem.

## References
