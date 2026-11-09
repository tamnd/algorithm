---
tag: 68EZEJ
kind: problem
slug: pareto-front-computation
name: Pareto front computation
aliases:
- Pareto query
- Pareto set computation
- Skyline query problem
- maxima of a set of vectors
- maxima query
- skyline query
- nondominated set computation
area: optimization/multi-objective
level: intro
summary: Given a finite set of vectors, find all of its non-dominated elements.
prereqs: [pareto-dominance, pareto-front]
see_also: [kung-algorithm, non-dominated-sorting, bnl-skyline, sort-filter-skyline, dominance-counting, approximate-pareto-set, multi-objective-shortest-path, multi-objective-knapsack]
sources:
  - paper: doi:10.1145/321906.321910
    title: H. T. Kung, F. Luccio and F. P. Preparata, On finding the maxima of a set of vectors, Journal of the ACM 22(4), 1975
    locator: pages 469 to 476 (the maxima problem, the upper bounds and the lower bound of log2 n! comparisons)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Section 4.1.3 (the maxima of a point set)
  - paper: doi:10.1145/322092.322095
    title: J. L. Bentley, H. T. Kung, M. Schkolnick and C. D. Thompson, On the average number of maxima in a set of vectors and applications, Journal of the ACM 25(4), 1978
    locator: pages 536 to 543 (the expected number of maxima for independent coordinates)
  - paper: doi:10.1145/323233.323246
    title: David G. Kirkpatrick and Raimund Seidel, Output-size sensitive algorithms for finding maximal vectors, Proceedings of the First Annual Symposium on Computational Geometry, 1985
    locator: pages 89 to 96 (algorithms whose time depends on the number of maxima)
  - paper: doi:10.1109/ICDE.2001.914855
    title: S. Börzsönyi, D. Kossmann and K. Stocker, The Skyline operator, Proceedings of the 17th International Conference on Data Engineering, 2001
    locator: pages 421 to 430 (the skyline query in databases and the block nested loops algorithm)
  - paper: doi:10.1109/ICDE.2003.1260846
    title: J. Chomicki, P. Godfrey, J. Gryz and D. Liang, Skyline with presorting, Proceedings of the 19th International Conference on Data Engineering, 2003
    locator: pages 717 to 719 (sort-filter-skyline)
---

Pareto front computation asks for the nondominated elements of a finite set of vectors. It is the basic step of [multi-objective optimization](/multi-objective-optimization/) once the candidate solutions are listed: keep the ones that no other candidate beats in every objective. The same problem is called the maxima problem in computational geometry, where Kung, Luccio and Preparata (1975) solved it in $O(n \log n)$ time for two and three objectives, and the skyline query in databases (Börzsönyi, Kossmann and Stocker, 2001). Comparing all pairs takes $O(p n^2)$ time; better algorithms use sorting and divide and conquer.

## In plain words

You have a list of options, and each option has a few numbers that you want small, such as price and distance. One option beats another if it is no worse in every number and better in at least one. The task is to throw away every option that some other option beats, and keep the rest.

What is left is the set of fair choices. None of them is better than another in every way, so the choice among them needs a preference. A hotel search that shows only the hotels that no other hotel beats on both price and distance to the beach solves this problem.

## Definition

**Convention.** All objectives are minimized unless a page says otherwise. The number of objectives is $p \ge 1$, and each input vector $y = f(x)$ is the image of a candidate solution $x$. A vector $a$ dominates $b$, written $a \prec b$, when $a_j \le b_j$ for each $j$ and $a \ne b$ ([Pareto dominance](/pareto-dominance/)).

**Input.** A list $Y = (y^1, \ldots, y^n)$ of vectors of $\mathbb{R}^p$. Any totally ordered values work in place of real numbers.

**Output.** The set of indices

$$N(Y) = \{\, j : \text{no } i \text{ has } y^i \prec y^j \,\},$$

or the set of vectors $\{y^j : j \in N(Y)\}$, which is the [Pareto front](/pareto-front/) of the finite set $Y$. Equal vectors do not dominate each other, so the copies of a nondominated vector are all in $N(Y)$.

For $p = 1$ the answer is the set of indices of the minimum. The set $N(Y)$ is never empty when $Y$ is not empty: a vector with the least sum of coordinates is nondominated.

## Variants

- **Maxima.** Maximize every coordinate. Negate the values to get the problem above. Computational geometry uses this form.
- **Mixed directions.** Some coordinates are minimized and some maximized; database skylines also have coordinates that only must be equal (DIFF). Negate the maximized coordinates, and group by the DIFF coordinates.
- **Weakly nondominated vectors.** Keep the vectors that no vector beats strictly in every coordinate. This set contains $N(Y)$ and can be larger.
- **All fronts.** Split $Y$ into fronts, each the answer for what the earlier fronts leave. This is [non-dominated sorting](/non-dominated-sorting/).
- **Online and dynamic.** Keep the front of a stream of vectors under insertions, or under insertions and deletions. The archives of evolutionary methods such as [PAES](/paes/) do this.
- **Approximate fronts.** Keep a small subset that is within a factor $1 + \varepsilon$ of every vector. See [approximate Pareto set](/approximate-pareto-set/) and [epsilon dominance](/epsilon-dominance/).
- **Implicit sets.** The candidate set is given by a problem, such as all paths of a graph or all subsets of items, and is too large to list. See [multi-objective shortest path](/multi-objective-shortest-path/) and [multi-objective knapsack](/multi-objective-knapsack/). Those algorithms call the finite problem as a filter many times.

## Examples

Take $a = (2, 9)$, $b = (3, 6)$, $c = (4, 7)$, $d = (5, 4)$, $e = (7, 3)$, $f = (8, 5)$ and $g = (9, 1)$. Here $b \prec c$ and $d \prec f$, and no other pair is in the relation. So the answer is $\{a, b, d, e, g\}$.

| input | answer | note |
|---|---|---|
| $a, b, c, d, e, f, g$ | $a, b, d, e, g$ | $c$ and $f$ are dominated |
| $(1, 1), (1, 2), (2, 1)$ | $(1, 1)$ | one vector beats all others |
| $(0, 3), (1, 2), (2, 1), (3, 0)$ | all four | vectors on a line with negative slope |
| $(1, 2), (1, 2), (2, 2)$ | both copies of $(1, 2)$ | copies do not dominate each other |
| $(1, 2, 3), (3, 2, 1), (2, 2, 2)$ | all three | no vector is better in all three |

The fourth row shows why the test needs a strict inequality: with the test $a_j \le b_j$ for all $j$ alone, each copy would remove the other.

## Known algorithms

| algorithm | time | notes |
|---|---|---|
| comparison of all pairs | $O(p n^2)$ | simple, and the best choice for small $n$ or large $p$ |
| sort and scan, $p = 2$ | $O(n \log n)$ | sort lexicographically, keep a vector if its $y_2$ is below every earlier $y_2$ |
| [Kung's algorithm](/kung-algorithm/) | $O(n \log n)$ for $p \le 3$, $O(n \log^{p-2} n)$ for $p \ge 4$ | divide and conquer on the coordinates |
| Kirkpatrick and Seidel (1985) | $O(n \log h)$ for $p = 2, 3$ | $h$ is the size of the answer |
| [block nested loops](/bnl-skyline/) | $O(p n^2)$ in the worst case | keeps a window of candidates, which can later be removed; made for data on disk |
| [sort-filter-skyline](/sort-filter-skyline/) | $O(n \log n + p n h)$ | sorts by a monotone score first, so no kept vector is removed later |
| Bentley, Kung, Schkolnick and Thompson (1978) | $O(n)$ expected | for independent coordinates with continuous distributions |

The two-objective scan works because, after a lexicographic sort, only earlier vectors can dominate a later one, and a vector is dominated by an earlier one exactly when some earlier $y_2$ is not larger than its own. On the example the scan keeps $a$ (least $y_2$ so far 9), $b$ (6), drops $c$ ($7 \ge 6$), keeps $d$ (4) and $e$ (3), drops $f$ ($5 \ge 3$), and keeps $g$ (1).

Sort-filter-skyline sorts by a function that every dominance increases, such as the sum of the coordinates. Then a vector can be dominated only by an earlier vector, and every vector that enters the window stays in the answer.

## Bounds

- **Lower bound.** In the model where the cost is the number of comparisons of two coordinates, Kung, Luccio and Preparata show that every algorithm needs at least $\lceil \log_2 n! \rceil = \Omega(n \log n)$ comparisons in the worst case for $p \ge 2$. So the sort and scan and Kung's algorithm are optimal for $p = 2$ and $p = 3$ in this model.
- **Output size.** The answer can have all $n$ vectors, as on the line $y_1 + y_2 = n$. So no algorithm that lists the answer is faster than $\Omega(n)$, and an algorithm whose time grows with $h$ gains only when the answer is small.
- **Expected size.** For vectors with independent coordinates drawn from continuous distributions, the expected size $A(n, p)$ satisfies $A(n, 1) = 1$ and $A(n, p) = \sum_{k=1}^{n} A(k, p - 1)/k$. So $A(n, 2) = H_n \approx \ln n$, and $A(n, p) = O(\log^{p-1} n)$. On such data the answer is small, and simple filters are fast.
- **Higher dimensions.** For $p \ge 4$ the gap between the lower bound $\Omega(n \log n)$ and the upper bound $O(n \log^{p-2} n)$ is open in the comparison model.

## Reductions

- **From sorting, for $p = 2$.** After a lexicographic sort the problem takes one linear scan. So for $p = 2$ the cost is the cost of sorting plus $O(n)$.
- **To dominance counting.** A vector is nondominated if and only if no vector dominates it. So an algorithm that counts, for every vector, the vectors that dominate it also solves this problem. See [dominance counting](/dominance-counting/).
- **To and from non-dominated sorting.** The first front of [non-dominated sorting](/non-dominated-sorting/) is the answer. Conversely, applying the problem again to what is left gives all fronts, at a cost of up to $n$ calls.
- **From implicit multi-objective problems.** When the feasible set of a combinatorial problem can be listed, its [Pareto front](/pareto-front/) is the answer for the list of images. Dynamic programming methods for multi-objective problems remove dominated labels after each step, which is this problem on small sets.
- **Maxima to minima.** Negate each coordinate. The order of dominance is reversed, so the maxima of $Y$ are the minima of $-Y$.

## Applications

- **Multi-objective optimization.** Every method that produces candidate points, such as a sweep of a [scalarization](/scalarization/) or an [evolutionary method](/multi-objective-evolutionary-algorithm/), keeps only the nondominated ones. The archives of [SPEA2](/spea2/), [PAES](/paes/) and [Pareto local search](/pareto-local-search/) are such sets.
- **Database skyline queries.** Börzsönyi, Kossmann and Stocker added a SKYLINE OF clause to SQL. A query such as "hotels that are cheap and close to the beach" returns the skyline of the table.
- **Labels in dynamic programming.** The label-setting method for [multi-objective shortest path](/multi-objective-shortest-path/) and the dynamic program for [multi-objective knapsack](/multi-objective-knapsack/) remove dominated labels at each node or stage.
- **Computational geometry.** The maxima of a set of points in the plane form a staircase. Removing the staircase again and again gives the layers of maxima, and the number of layers is the length of the longest chain of points in the order of dominance.
- **Economics and finance.** The efficient portfolios among a finite list of portfolios, with risk and the negative of the return as objectives, are the answer of this problem.

## References
