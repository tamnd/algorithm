---
tag: STERX3
kind: problem
slug: knapsack-problem
name: Knapsack problem
aliases:
- 0-1 knapsack problem
- 0/1 knapsack
- knapsack problem
- binary knapsack problem
area: optimization/combinatorial-optimization
level: core
summary: Choose items of given value and weight to maximize value within a capacity.
prereqs: [combinatorial-optimization-problem, weak-np-hardness, pseudo-polynomial-time]
see_also: [knapsack-dynamic-programming, greedy-fractional-knapsack, knapsack-fptas, knapsack-branch-and-bound, knapsack-decision, subset-sum-problem, unbounded-knapsack, cover-inequality]
sources:
  - book: isbn:9783540402862
    title: Hans Kellerer, Ulrich Pferschy and David Pisinger, Knapsack Problems, Springer, 2004
    locator: the chapters on basic algorithmic concepts (the dynamic programs and the greedy bound), on exact solution of the 0-1 knapsack problem, on approximation algorithms and schemes, and on the multidimensional knapsack problem
  - book: isbn:9780471924203
    title: Silvano Martello and Paolo Toth, Knapsack Problems, Algorithms and Computer Implementations, Wiley, 1990
    locator: Chapter 2, 0-1 knapsack problem (relaxations and upper bounds, approximate algorithms, branch and bound, dynamic programming)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A6, problem MP9 (Knapsack), and Section 4.2 (number problems and pseudo-polynomial time)
  - paper: doi:10.1287/opre.5.2.266
    title: George B. Dantzig, Discrete-variable extremum problems, Operations Research 5(2), 266 to 288, 1957
    locator: the knapsack problem and the solution of its linear relaxation by the ratio order
  - paper: doi:10.1145/321906.321909
    title: Oscar H. Ibarra and Chul E. Kim, Fast approximation algorithms for the knapsack and sum of subset problems, Journal of the ACM 22(4), 463 to 468, 1975
    locator: the fully polynomial time approximation scheme
  - paper: doi:10.1145/321812.321823
    title: Ellis Horowitz and Sartaj Sahni, Computing partitions with applications to the knapsack problem, Journal of the ACM 21(2), 277 to 292, 1974
    locator: the algorithm that splits the items into two halves and merges the sorted lists of subsets
  - paper: doi:10.1137/0210033
    title: Richard Schroeppel and Adi Shamir, A T = O(2^(n/2)), S = O(2^(n/4)) algorithm for certain NP-complete problems, SIAM Journal on Computing 10(3), 456 to 464, 1981
    locator: the main algorithm and its time and space bounds
  - paper: doi:10.1287/opre.9.6.849
    title: P. C. Gilmore and R. E. Gomory, A linear programming approach to the cutting-stock problem, Operations Research 9(6), 849 to 859, 1961
    locator: the knapsack problem as the pricing step of column generation
  - paper: "Richard M. Karp, Reducibility among combinatorial problems, in R. E. Miller and J. W. Thatcher (editors), Complexity of Computer Computations, Plenum Press, 1972, pages 85 to 103"
    locator: the problem KNAPSACK in the list of 21 NP-complete problems
---

The 0-1 knapsack problem asks for a set of items of largest total value whose total weight is at most a given capacity. It is [weakly NP-hard](/weak-np-hardness/): its decision version is [NP-complete](/np-complete/), but [dynamic programming](/knapsack-dynamic-programming/) solves it in $O(nW)$ time, which is [pseudo-polynomial](/pseudo-polynomial-time/), and it has a [fully polynomial-time approximation scheme](/knapsack-fptas/). It is the simplest [integer program](/binary-integer-programming/): one constraint, binary variables.

## In plain words

You have a bag that holds a fixed weight. In front of you are items, and each has a weight and a value. You may take an item or leave it, but you cannot cut it. You want the most value that still fits in the bag.

The obvious rule takes items by value per unit of weight. It often works, but it can fail badly: a light item with a good ratio can block a heavy item that is worth much more. Trying every set of items is always right, but the number of sets doubles with each item. A table over the items and the free space solves the problem fast when the capacity is a small number. When the weights are huge numbers, no fast exact method is known, but an answer within any fixed percentage of the best is fast.

## Definition

**Input.** $n$ items. Item $i$ has a weight $w_i \in \mathbb{Z}_{>0}$ and a value $v_i \in \mathbb{Z}_{>0}$. A capacity $W \in \mathbb{Z}_{\ge 0}$.

**Output.** A set $S \subseteq \{1, \ldots, n\}$ with $\sum_{i \in S} w_i \le W$ that maximizes $\sum_{i \in S} v_i$. As an [integer program](/binary-integer-programming/):

$$ \max \sum_{i=1}^n v_i x_i \quad \text{subject to} \quad \sum_{i=1}^n w_i x_i \le W, \qquad x \in \{0,1\}^n. $$

The empty set is always feasible, so an optimal solution always exists. Items with $w_i > W$ can be removed first, and if $\sum_i w_i \le W$ all items fit. So assume $w_i \le W$ for each $i$ and $\sum_i w_i > W$. Write $f^*$ for the optimal value, $v_{\max} = \max_i v_i$ and $V = \sum_i v_i$. The input length is $\Theta(n (\log W + \log v_{\max}))$, so a running time polynomial in $W$ is exponential in the input length.

**Decision version** ([knapsack decision](/knapsack-decision/)). Given also a target $k$, is there a feasible $S$ with $\sum_{i \in S} v_i \ge k$?

## Variants

- **[Fractional knapsack](/fractional-knapsack/).** $x \in [0,1]^n$. This is the [LP relaxation](/lp-relaxation/) of the 0-1 problem. The [ratio greedy](/greedy-fractional-knapsack/) solves it exactly in $O(n \log n)$ time, or $O(n)$ with a weighted median.
- **[Bounded knapsack](/bounded-knapsack/).** Item $i$ has $b_i$ copies, $x_i \in \{0, 1, \ldots, b_i\}$. Splitting $b_i$ into powers of two reduces it to 0-1 knapsack with $O(\sum_i \log b_i)$ items.
- **[Unbounded knapsack](/unbounded-knapsack/).** $x_i \in \mathbb{Z}_{\ge 0}$. A one-dimensional table solves it in $O(nW)$ time.
- **[Subset sum](/subset-sum-problem/).** $v_i = w_i$: find the largest total weight at most $W$, or decide whether $W$ is reached exactly.
- **[Multiple knapsack](/multiple-knapsack-problem/).** Several bags with their own capacities. It is strongly NP-hard, even with equal capacities, because [3-partition](/three-partition/) is a special case.
- **Multidimensional knapsack.** $d$ constraints $A x \le b$ with $A \ge 0$. For each fixed $d \ge 2$ it has a PTAS but no FPTAS unless P = NP (Kellerer, Pferschy and Pisinger, chapter on the multidimensional knapsack problem).
- **[Online knapsack](/online-knapsack-problem/)** and **[multi-objective knapsack](/multi-objective-knapsack/)** change the information model and the objective.

## Examples

**A small instance.** $W = 10$ and four items:

| item $i$ | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| weight $w_i$ | 5 | 4 | 6 | 3 |
| value $v_i$ | 10 | 40 | 30 | 50 |
| ratio $v_i / w_i$ | 2 | 10 | 5 | 50/3 |

Of the 16 subsets, 10 are feasible. The optimum is $S^* = \{2, 4\}$ with weight 7 and value $f^* = 90$. The fractional relaxation takes items 4 and 2 whole and half of item 3, for $50 + 40 + 15 = 105$. So the [LP relaxation](/lp-relaxation/) bound is 105, and the gap to 90 is what a [branch and bound](/knapsack-branch-and-bound/) search must close.

**The ratio greedy fails.** Take $W = 100$, item 1 with $w_1 = 1$, $v_1 = 2$, and item 2 with $w_2 = 100$, $v_2 = 100$. The ratio order takes item 1 (ratio 2), and then item 2 does not fit. The greedy value is 2 and $f^* = 100$. With $W = M$, $w_2 = v_2 = M$, the ratio is $2/M$, which tends to 0.

**The LP bound can be twice the optimum.** Take two items with $w_i = M + 1$ and $v_i = 1$, and $W = 2M$. Only one item fits, so $f^* = 1$. The relaxation takes $2M/(M+1)$ units, so the bound is $2M/(M+1)$, which tends to 2. So the [integrality gap](/integrality-gap/) of the natural formulation is 2.

## Known algorithms

- **[Dynamic programming over capacities](/knapsack-dynamic-programming/)**. A table $V[i][c]$, the best value with items $1..i$ and capacity $c$. $\Theta(nW)$ time, $\Theta(W)$ space for the value.
- **Dynamic programming over values.** $M[i][p]$, the least weight that reaches value exactly $p$ with items $1..i$. $O(nV) = O(n^2 v_{\max})$ time. This is the [profit-indexed dynamic program](/profit-indexed-dynamic-programming/) behind the FPTAS.
- **[FPTAS](/knapsack-fptas/)** (Ibarra and Kim 1975). Scale the values to $\lfloor v_i / K \rfloor$ with $K = \varepsilon v_{\max} / n$, and run the value DP. The result is at least $(1 - \varepsilon) f^*$, in $O(n^3 / \varepsilon)$ time in the textbook form. Later schemes are faster. See [rounding and scaling](/rounding-and-scaling/).
- **Greedy with the best single item.** Take the items in ratio order while they fit; return the better of this set and the most valuable single item. Its value is at least $f^*/2$. Proof: let $k$ be the first item that does not fit. The fractional optimum is at most $v(\{1, \ldots, k-1\}) + v_k$, and both terms are at most the returned value.
- **[Branch and bound](/knapsack-branch-and-bound/)** with the fractional bound of Dantzig (1957). Exponential in the worst case, but it solves most random instances with thousands of items fast. The codes of Martello, Toth and Pisinger add core problems and dynamic programming.
- **Meet in the middle** (Horowitz and Sahni 1974). Split the items into two halves, list the $2^{n/2}$ subsets of each half with their Pareto-optimal (weight, value) pairs, and combine the two sorted lists. $O(n 2^{n/2})$ time.

## Bounds

**NP-hardness.** The decision version is NP-complete (Karp 1972, by reduction from exact cover; it is problem MP9 in Garey and Johnson). So the optimization problem is NP-hard. A reduction from [subset sum](/subset-sum-problem/) is direct: set $v_i = w_i$ and $k = W$; a set reaches value $W$ within capacity $W$ if and only if its weights sum to exactly $W$.

**Weak, not strong.** The capacity DP runs in time polynomial in $n$ and the magnitude $W$. So the problem is solvable in polynomial time when the numbers are written in unary, and it is not [strongly NP-hard](/strong-np-hardness/) unless P = NP. This is the meaning of [weakly NP-hard](/weak-np-hardness/).

**Approximation.** The FPTAS gives $(1 - \varepsilon) f^*$ in time polynomial in $n$ and $1/\varepsilon$. This is the best possible kind of approximation result for an NP-hard problem: an algorithm that is exact and polynomial in $n$ and $\log W$ would give P = NP. A strongly NP-hard problem with integer values bounded by a polynomial cannot have an FPTAS unless P = NP ([no FPTAS for strongly NP-hard problems](/no-fptas-for-strongly-np-hard-problems/)), which is why multiple knapsack has none. The multidimensional knapsack with a fixed $d \ge 2$ is only weakly NP-hard, and its lack of an FPTAS needs a different reduction.

**Integrality gap.** The fractional bound $f_{LP}$ satisfies $f^* \le f_{LP} < 2 f^*$ once each item fits alone, by the greedy argument above, and the example above shows the factor 2 is tight.

**Exact exponential time.** $O(n 2^{n/2})$ by meet in the middle. Schroeppel and Shamir (1981) kept the time and reduced the space to $O(2^{n/4})$.

## Reductions

- **From [subset sum](/subset-sum-problem/) and [partition](/partition-problem/).** As above, with $v_i = w_i$. These are the standard sources of NP-hardness.
- **To integer programming.** Knapsack is a [binary integer program](/binary-integer-programming/) with one constraint. In the other direction, each valid inequality of a knapsack row, such as a [cover inequality](/cover-inequality/), is valid for any integer program that contains the row, which is why solvers study the knapsack polytope.
- **To shortest and longest paths.** The capacity DP is a longest path in a [DAG](/dag-dynamic-programming/) with vertices $(i, c)$ and $O(nW)$ edges.
- **As a subproblem.** The pricing problem of [column generation](/column-generation/) for the [cutting stock problem](/cutting-stock-problem/) is a knapsack problem (Gilmore and Gomory). [Lagrangian relaxation](/lagrangian-relaxation/) of many problems leaves a knapsack per resource.

## Applications

- **Capital budgeting.** Choose projects of given cost and return under a budget.
- **Cutting and loading.** Cut a roll or fill a container, and the pricing step of cutting stock.
- **Cutting planes.** Cover and lifted cover inequalities from single rows of integer programs.
- **Cryptography.** The [Merkle-Hellman cryptosystem](/merkle-hellman-knapsack-cryptosystem/) used hard subset sum instances, and was broken by Shamir and by lattice methods.

## References
