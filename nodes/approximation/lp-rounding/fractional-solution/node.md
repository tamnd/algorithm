---
tag: 61Z3TZ
kind: concept
slug: fractional-solution
name: Fractional solution
aliases:
- fractional LP solution
- fractional optimum
- vertex solution of an LP relaxation
area: approximation/lp-rounding
level: intro
summary: A feasible but non-integral solution of an LP relaxation, to be rounded; its value bounds the optimum, and a vertex solution has few fractional values.
prereqs: [lp-relaxation, linear-programming-problem, extreme-point]
see_also: [linear-programming-rounding, integrality-gap, basic-feasible-solution, half-integrality, total-unimodularity, iterative-rounding, cramers-rule, fundamental-theorem-of-lp]
sources:
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Appendix A (linear programming) and Section 11.1 (the generalized assignment problem, rounding of a sparse vertex solution)
  - book: isbn:9781107007512
    title: Lap Chi Lau, R. Ravi and Mohit Singh, Iterative Methods in Combinatorial Optimization
    locator: Chapter 2 (preliminaries, extreme point solutions and the rank lemma)
  - book: isbn:9780262046305
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 29 (linear programming) and Section 35.4 (the weighted vertex cover LP)
---

A fractional solution is a feasible point of an [LP relaxation](/lp-relaxation/) in which some variables are not integers. An optimal fractional solution has value $\text{LP}^*$, which is a lower bound on the optimum of a minimization problem and an upper bound for a maximization problem. This bound is what LP rounding compares against. Not all fractional solutions are equally useful: a vertex, or [extreme point](/extreme-point/), of the feasible region has at most as many nonzero values as there are constraints, its values are fixed by a square linear system, and for some problems they take only a few values, such as $\{0, \frac12, 1\}$. Many rounding methods need a vertex solution and fail for an arbitrary optimum.

## In plain words

When a hard choice problem allows parts of a choice, its best answer usually uses some parts. That answer is a fractional solution. It is at least as good as any real answer, so it measures how good a real answer can be.

There are many fractional solutions with the same value, and some are easier to round. The best ones sit at the corners of the region of valid answers. A corner is fixed by as many rules as there are unknowns, so it has few parts that are not whole. Most of its values are already zero or one, and only a few need rounding.

## The idea

**Definition.** Let the relaxation be $P = \{ x \in \mathbb{R}^n : A x \ge b, \; 0 \le x \le 1 \}$, where $A$ has $r$ rows. A point $x \in P$ is a *fractional solution*; it is *fractional* in the strict sense when some $x_j \notin \{0, 1\}$. Its *support* is $\{ j : x_j > 0 \}$. An optimal point $x^*$ of $\min \{ c \cdot x : x \in P \}$ has value $\text{LP}^* \le \text{OPT}$, because each integral solution is in $P$.

**Vertices.** A point $x \in P$ is a vertex if it is not the midpoint of two other points of $P$. Equivalently, among the constraints that hold with equality at $x$, there are $n$ linearly independent ones; see [basic feasible solution](/basic-feasible-solution/). By the [fundamental theorem of LP](/fundamental-theorem-of-lp/), if the LP has an optimum and $P$ has a vertex, some vertex is optimal.

**Rank lemma.** A vertex of $P$ has at most $r$ fractional coordinates.

*Proof.* At a vertex $x$ there are $n$ linearly independent tight constraints. At most $r$ of them are rows of $A x \ge b$, so at least $n - r$ are bounds $x_j = 0$ or $x_j = 1$ for different $j$. Those coordinates are integral, so at most $r$ coordinates are fractional. $\square$

The same count for $P = \{ x \ge 0 : A x \ge b \}$ shows that a vertex has at most $r$ nonzero coordinates. This is the reason that a vertex solution of an assignment LP or a configuration LP is sparse.

**Values at a vertex.** A vertex is the unique solution of a square system $A' x = b'$ of tight constraints. By [Cramer's rule](/cramers-rule/), each $x_j$ is a ratio of two subdeterminants of the constraint data. If the matrix is [totally unimodular](/total-unimodularity/), each subdeterminant is $0$ or $\pm 1$ and each vertex is integral, so the LP has no gap. For the vertex cover LP, each vertex is in $\{0, \frac12, 1\}^n$; see [half-integrality](/half-integrality/).

**From any optimum to a vertex.** An interior point method returns a point in the relative interior of the optimal face, which is not a vertex when the optimum is not unique. Take an optimal $x$ whose tight constraints have rank less than $n$. Some direction $d \ne 0$ keeps all tight constraints tight, and $x \pm \varepsilon d$ is feasible for small $\varepsilon$. Optimality of both points forces $c \cdot d = 0$. Move along $d$ until a new constraint becomes tight. The rank of the tight set grows by at least one, so at most $n$ moves reach an optimal vertex, in polynomial time. The [simplex method](/simplex-method/) returns a vertex directly.

## Examples

- **Knapsack.** Values $60, 100, 120$, weights $10, 20, 30$, capacity $W = 50$. The LP $\max \sum_j v_j x_j$ subject to $\sum_j w_j x_j \le 50$ and $0 \le x \le 1$ is solved by taking items in order of value per weight, $6, 5, 4$: $x^* = (1, 1, \frac23)$ with value $240$. The integral optimum is $220$, from items 2 and 3. The LP has one constraint besides the bounds, and the vertex has one fractional value, as the rank lemma says. Rounding it down gives $160$, and the better of $160$ and the fractional item alone, $120$, is at least $\text{LP}^*/2$.
- **An optimum that is not a vertex.** For vertex cover on the 4-cycle with unit weights, $x = (\frac12, \frac12, \frac12, \frac12)$ is optimal with value 2. It is the midpoint of the two integral covers $(1, 0, 1, 0)$ and $(0, 1, 0, 1)$, so it is not a vertex. A rounding that needs a vertex must first move to one of them.
- **A fractional vertex.** For vertex cover on a triangle with unit weights, $x = (\frac12, \frac12, \frac12)$ is the unique optimum, with $\text{LP}^* = \frac32$ and OPT $= 2$. The three edge constraints are tight, and their matrix $\left(\begin{smallmatrix} 1 & 1 & 0 \\ 0 & 1 & 1 \\ 1 & 0 & 1 \end{smallmatrix}\right)$ has determinant 2, so the point is a vertex, and its denominator 2 is that determinant.
- **Bipartite matching.** The incidence matrix of a [bipartite graph](/bipartite-graph/) is totally unimodular, so each vertex of the [matching](/bipartite-matching/) LP is integral. On the triangle, which is not bipartite, the point with $\frac12$ on each edge is a fractional vertex of the perfect matching LP.

## Where it is used

- **LP rounding.** Each rounding method starts from a fractional solution and compares its output with $\text{LP}^*$; see [LP rounding](/linear-programming-rounding/), [threshold rounding](/threshold-rounding/) and [randomized rounding](/randomized-rounding/).
- **Sparse vertices.** A vertex of the assignment LP for [unrelated machine scheduling](/unrelated-machine-scheduling-makespan/) and the [generalized assignment problem](/generalized-assignment-problem/) has a support graph that is a forest plus at most one extra edge in each connected component, which lets a matching round the few fractional jobs. A vertex of the [configuration LP](/configuration-lp/) in [Karmarkar-Karp bin packing](/karmarkar-karp-bin-packing/) uses at most as many configurations as there are item sizes.
- **Iterative rounding.** At each vertex some variable is 0, is 1, or is large, which drives [iterative rounding](/iterative-rounding/), [iterative relaxation](/iterative-relaxation/) and [Jain's 2-approximation](/jain-iterative-rounding-network-design/).
- **Kernels.** The half-integral vertex of the vertex cover LP gives a kernel with at most $2k$ vertices; see the [Nemhauser-Trotter theorem](/nemhauser-trotter-theorem/) and [LP kernelization](/lp-kernelization/).
- **Measuring the relaxation.** The ratio between the integral and the fractional optimum, over all instances, is the [integrality gap](/integrality-gap/).
- **Exact integer programming.** Branch and bound for [mixed integer programming](/mixed-integer-programming/) branches on a fractional variable of the current LP optimum.

## References
