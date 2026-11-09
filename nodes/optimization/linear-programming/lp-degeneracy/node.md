---
tag: 9P9HPV
kind: concept
slug: lp-degeneracy
name: Degeneracy in linear programming
aliases:
- degenerate basic solution
- degenerate vertex
- degenerate pivot
area: optimization/linear-programming
level: core
summary: A basic solution with more active constraints than needed, which can cause zero-length pivots and cycling.
prereqs: [basic-feasible-solution, lp-standard-form, pivot-operation]
see_also: [simplex-termination, bland-rule, ratio-test, dantzig-pivot-rule, complementary-slackness, shadow-price, assignment-problem, column-generation]
sources:
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 2.4, Degeneracy; Section 3.4, Anticycling (lexicography and Bland's rule); Chapter 7, Network flow problems (bases and spanning trees)
  - book: isbn:9780716715870
    title: Vašek Chvátal, Linear Programming, W. H. Freeman, 1983
    locator: Chapter 3, Pitfalls and how to avoid them (degeneracy, cycling, the perturbation method and the smallest subscript rule)
  - paper: doi:10.2307/1907845
    title: A. Charnes, Optimality and degeneracy in linear programming, Econometrica 20(2), 1952
    locator: the perturbation of the right-hand side by powers of a small parameter
  - paper: doi:10.1002/nav.3800020406
    title: E. M. L. Beale, Cycling in the dual simplex algorithm, Naval Research Logistics Quarterly 2(4), 1955
    locator: pages 269 to 275, the cycling example
  - paper: doi:10.1287/moor.2.2.103
    title: Robert G. Bland, New finite pivoting rules for the simplex method, Mathematics of Operations Research 2(2), 1977
    locator: pages 103 to 107, the least-index rule
---

A [basic feasible solution](/basic-feasible-solution/) is degenerate when at least one of its basic variables is zero. Geometrically, more constraints are tight at the vertex than its dimension needs, so several different bases describe the same point. At such a vertex the [simplex method](/simplex-method/) can make pivots of length zero, which change the basis but not the point, and with a careless [pivot rule](/dantzig-pivot-rule/) it can go round a loop of bases for ever.

## In plain words

A corner of a region in the plane is usually where two lines meet. If three lines pass through the same corner, the corner is degenerate: any two of the three lines fix it, so there is more than one way to describe the same point.

The simplex method keeps one such description, a basis, and moves by changing it. At a degenerate corner it can change the description without moving. Then it has made no progress, and after some changes it can come back to a description it had before and repeat the same steps for ever. This is called cycling. Simple tie rules prevent it. Degenerate corners are rare in random problems but very common in problems from combinatorics and scheduling.

## The idea

**Definition.** For the program minimize $c^\top x$ subject to $Ax = b$, $x \ge 0$, with $A$ of size $m \times n$ and rank $m$, a basis $B$ gives the basic solution $x_B = B^{-1}b$, $x_N = 0$. It is *degenerate* if $x_{B(i)} = 0$ for some $i$. Then more than $n - m$ variables are zero, so more than $n$ constraints (the $m$ equations and the zero variables) are tight at the point. For a vertex of a polyhedron in $\mathbb{R}^d$ given by inequalities, degenerate means that more than $d$ inequalities are tight there.

**Many bases, one vertex.** A vertex with $k$ basic zeros can belong to many bases: any choice of $m$ linearly independent columns that contains the positive variables gives the same point. A pivot between two such bases has step $\theta = 0$ in the [ratio test](/ratio-test/), because the leaving row has $x_{B(p)} = 0$. The value does not change.

**Cycling.** With only nondegenerate pivots the value falls at each pivot, so no basis repeats and the method stops. With degenerate pivots the value can stay the same for many pivots, and a deterministic rule that returns to a basis it has visited will repeat the same loop for ever. Beale's example shows that Dantzig's rule does this. Three standard remedies make the simplex method stop on every program (see [simplex termination](/simplex-termination/)):

- [Bland's rule](/bland-rule/): smallest index for the entering and the leaving variable.
- The lexicographic ratio test of Dantzig, Orden and Wolfe.
- Perturbation (Charnes, 1952): replace $b$ by $b + (\varepsilon, \varepsilon^2, \ldots, \varepsilon^m)$ for a tiny $\varepsilon > 0$. No basic solution of the perturbed program is degenerate, and for $\varepsilon$ small enough the order of the ratios is the lexicographic order. So the perturbation is the lexicographic rule in another form.

**Stalling.** Even without a cycle, a method can make a very long run of degenerate pivots at one vertex. The number of bases at a vertex can be exponential in the number of basic zeros, so stalling is a real cost on very degenerate programs.

**Dual degeneracy.** An optimal basis is *dual degenerate* when some nonbasic variable has [reduced cost](/reduced-cost/) $r_j = 0$. The two kinds of degeneracy control the uniqueness of the optima:

- *If an optimal basic solution is nondegenerate, the dual optimum is unique.* Every basic variable is positive, so by [complementary slackness](/complementary-slackness/) every dual optimum $p$ has $p^\top A_j = c_j$ for all $j$ in the basis. So $p^\top B = c_B^\top$, and $p = (B^{-\top}) c_B$ is the only choice.
- *If an optimal basis has $r_j > 0$ for every nonbasic $j$, the primal optimum is unique.* Every feasible $x$ has $c^\top x = z + \sum_{j \in N} r_j x_j$, so an optimal $x$ has $x_N = 0$, and then $x_B = B^{-1}b$.

So a program with several primal optima has a dual degenerate optimal basis, and a program with several dual optima has a degenerate optimal vertex. At such a vertex the [shadow prices](/shadow-price/) are one-sided: the change of the optimal value per unit of $b_i$ is different for an increase and for a decrease.

## Examples

**Three lines through a corner.** Take $x_1 \le 1$, $x_2 \le 1$, $x_1 + x_2 \le 2$ with slacks $s_1, s_2, s_3$, so $m = 3$ and $n = 5$. At the vertex $(1, 1)$ all three slacks are zero, but a basis has only three variables, and $x_1, x_2$ must be in it. So the bases $\{x_1, x_2, s_1\}$, $\{x_1, x_2, s_2\}$ and $\{x_1, x_2, s_3\}$ all give this vertex, each with one basic variable at zero. The other vertices $(0,0)$, $(1,0)$ and $(0,1)$ have exactly one feasible basis each.

**The assignment polytope.** The [assignment](/assignment-problem/) program in $n \times n$ variables has $2n$ equations of rank $2n - 1$, so a basis has $2n - 1$ variables, but a vertex, a permutation, has only $n$ positive entries. So every vertex is degenerate, with $n - 1$ basic zeros. The bases of this program are the spanning trees of the complete bipartite graph $K_{n,n}$, and the bases at a vertex are the spanning trees that contain its perfect matching. Contracting the $n$ matching edges leaves the complete graph $K_n$ with every edge doubled, so by Cayley's formula there are
$$2^{n-1} n^{n-2}$$
bases at each vertex: $2$, $12$ and $128$ for $n = 2, 3, 4$. A simplex method on this program can spend many pivots without leaving a vertex.

**Beale's example.** Minimize $-\frac34 x_4 + 20x_5 - \frac12 x_6 + 6x_7$ subject to $x_1 + \frac14 x_4 - 8x_5 - x_6 + 9x_7 = 0$, $x_2 + \frac12 x_4 - 12x_5 - \frac12 x_6 + 3x_7 = 0$, $x_3 + x_6 = 1$, $x \ge 0$. The start vertex has $x_1 = x_2 = 0$ in the basis $\{x_1, x_2, x_3\}$. Dantzig's rule, with the smallest index on ties in the ratio test, makes six pivots of step $0$ and returns to $\{x_1, x_2, x_3\}$. Bland's rule leaves the vertex after five pivots and reaches the optimum $-5/4$ after six.

## Where it is used

- **Pivot rules.** Every finite version of the simplex method, primal or [dual](/dual-simplex-method/), needs a remedy for degeneracy, and the proofs of the [fundamental theorem of LP](/fundamental-theorem-of-lp/) and of [strong duality](/strong-duality/) by the simplex method rely on one.
- **Combinatorial programs.** Assignment, transportation, set partitioning and flow programs are highly degenerate. Network simplex codes use special tree rules to limit degenerate pivots, and in [column generation](/column-generation/) degeneracy of the master problem is a main cause of slow convergence.
- **Sensitivity analysis.** At a degenerate optimum the dual solution may not be unique, and the ranges of [sensitivity analysis](/lp-sensitivity-analysis/) computed from one basis can be smaller than the true ranges.
- **Geometry.** A polytope is *simple* when no vertex is degenerate; then every vertex has exactly $d$ edges. Perturbation turns any polytope into a simple one, which is why many proofs about the simplex method assume simple polytopes.

## References
