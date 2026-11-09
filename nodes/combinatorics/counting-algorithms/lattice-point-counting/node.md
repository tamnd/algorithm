---
tag: TGBF28
kind: problem
slug: lattice-point-counting
name: Counting lattice points in polytopes
aliases:
- integer point counting in polytopes
- lattice point enumeration
- '#IP'
area: combinatorics/counting-algorithms
level: research
summary: Counts integer points inside a rational polytope.
prereqs: [convex-polytope, polyhedron, picks-theorem, generating-functions]
see_also: [barvinok-algorithm, lattice-points-in-non-lattice-polygon, integer-programming-fixed-dimension, lenstra-algorithm, coin-change-counting, counting-perfect-matchings, counting-subset-sum, fpras]
sources:
  - paper: doi:10.1287/moor.19.4.769
    title: Alexander I. Barvinok, A polynomial time algorithm for counting integral points in polyhedra when the dimension is fixed, Mathematics of Operations Research 19(4), 769 to 779, 1994
    locator: the main theorem (polynomial time in fixed dimension)
  - paper: doi:10.1287/moor.22.3.545
    title: Martin Dyer and Ravi Kannan, On Barvinok's algorithm for counting lattice points in fixed dimension, Mathematics of Operations Research 22(3), 545 to 549, 1997
    locator: the whole paper (a simpler form of the decomposition step)
  - book: isbn:9781493929689
    title: Matthias Beck and Sinai Robins, Computing the Continuous Discretely, second edition, Springer, 2015
    locator: Chapter 2 (Pick's theorem), Chapter 3 (Ehrhart polynomials and quasi-polynomials) and Chapter 4 (reciprocity)
  - book: isbn:9783037190524
    title: Alexander Barvinok, Integer Points in Polyhedra, European Mathematical Society, 2008
    locator: the chapters on generating functions of rational cones and on the polynomial time algorithm
  - paper: doi:10.1016/j.jsc.2003.04.003
    title: Jesús A. De Loera, Raymond Hemmecke, Jeremiah Tauzer and Ruriko Yoshida, Effective lattice point counting in rational convex polytopes, Journal of Symbolic Computation 38(4), 1273 to 1302, 2004
    locator: the whole paper (the LattE implementation of Barvinok's algorithm, with examples on contingency tables and magic squares)
  - url: https://oeis.org/A002817
    title: OEIS A002817, Doubly triangular numbers
    locator: the comment that a(n+1) is the number of 3 x 3 nonnegative integer matrices with all row and column sums n
---

Counting lattice points in a polytope asks for the number of integer points $|P \cap \mathbb{Z}^d|$ in a bounded rational polyhedron $P = \{x \in \mathbb{R}^d : Ax \le b\}$. Many counting problems have this form: ways to make change, contingency tables with given margins, magic squares, perfect matchings of bipartite graphs, and the iterations of nested loops in a program. In the plane, the count of a lattice polygon follows from [Pick's theorem](/picks-theorem/). In any fixed dimension $d$, [Barvinok's algorithm](/barvinok-algorithm/) counts in time polynomial in the input size. When $d$ is part of the input, the problem is #P-hard, since it contains the count of perfect matchings of bipartite graphs. For the dilations $tP$ of a lattice polytope, the count is a polynomial in $t$, the Ehrhart polynomial, whose leading coefficient is the volume of $P$.

## In plain words

Draw a shape with straight sides on squared paper, and count the grid crossings that lie inside it or on its edge. In higher dimensions it is the same, with flat faces instead of straight sides.

Many questions are of this kind. The number of ways to pay an amount with given coins is the number of grid points in a slanted region. The number of tables of whole numbers with fixed row and column totals is another such count.

Counting one by one is too slow when the shape is large. In the plane, a simple rule relates the count to the area and to the points on the edge. In any fixed number of dimensions, there is a fast method that cuts the shape into simple corners and adds up formulas for them. When the number of dimensions grows, no fast exact method is expected.

## Definition

Notation: $d$ is the dimension. A rational polyhedron is $P = \{x \in \mathbb{R}^d : Ax \le b\}$ with $A \in \mathbb{Z}^{m \times d}$ and $b \in \mathbb{Z}^m$; it is a rational polytope if it is bounded. The input size $L$ is the number of bits needed to write $A$ and $b$. A lattice polytope is a polytope whose vertices are in $\mathbb{Z}^d$.

**Problem.** Given $A$ and $b$ with $P$ bounded, compute $|P \cap \mathbb{Z}^d|$.

The answer can be exponential in $L$: the box $[0, N]^d$ has $(N + 1)^d$ points and is written with $O(d \log N)$ bits. So listing the points is not polynomial, even for $d = 1$, and a polynomial algorithm must count without listing.

**Ehrhart's theorem.** For a lattice polytope $P$ of dimension $d$ and integers $t \ge 0$, $L_P(t) = |tP \cap \mathbb{Z}^d|$ is a polynomial in $t$ of degree $d$, with leading coefficient the volume of $P$ and constant term 1. For a rational polytope, $L_P(t)$ is a quasi-polynomial: a polynomial whose coefficients are periodic in $t$, with a period that divides the least common denominator of the vertex coordinates.

**Pick's theorem.** For a lattice polygon $P$ whose boundary is a simple closed curve, with $I$ interior and $B$ boundary lattice points, the area is $I + B/2 - 1$, so $|P \cap \mathbb{Z}^2| = \operatorname{area}(P) + B/2 + 1$.

## Variants

- **Fixed or varying dimension.** With $d$ fixed, the problem is polynomial. With $d$ part of the input, it is #P-hard.
- **Ehrhart polynomial.** Compute $L_P(t)$ as a polynomial or quasi-polynomial in $t$. For a lattice polytope, $d + 1$ values of $L_P$ fix it by interpolation.
- **Generating function.** Compute $f(P; z) = \sum_{m \in P \cap \mathbb{Z}^d} z^m$ as a short sum of rational functions. This is what Barvinok's algorithm produces, and the count is its value at $z = (1, \ldots, 1)$.
- **Weighted counts.** Sum a polynomial weight $w(m)$ over the lattice points, for example to compute the sum of a linear function over $P \cap \mathbb{Z}^d$.
- **Parametric polytopes.** Count $|\{x \in \mathbb{Z}^d : Ax \le b(p)\}|$ as a function of a parameter vector $p$. The answer is a piecewise quasi-polynomial, used in compilers.
- **Projections and Boolean combinations.** Count points of the form $\{y : \exists x, (x, y) \in P \cap \mathbb{Z}^{d}\}$, or of unions and differences of polytopes.
- **Approximate counting.** Estimate the count within a factor $1 \pm \varepsilon$ with a randomized algorithm when $d$ is large, see [approximate counting](/approximate-counting/).

## Examples

- **A triangle.** $P = \{(x, y) : x \ge 0, y \ge 0, 3x + 4y \le 12\}$ has vertices $(0,0)$, $(4,0)$, $(0,3)$ and area 6. Its boundary has $4 + 1 + 3 = 8$ lattice points, since the hypotenuse from $(4,0)$ to $(0,3)$ has $\gcd(4, 3) = 1$ step. Pick's theorem gives $6 + 4 + 1 = 11$ points. By rows: $y = 0, 1, 2, 3$ give $5, 3, 2, 1$ points.
- **Making change.** The number of ways to pay 10 with coins of values 1, 2 and 5 is the number of $(a, b, c) \in \mathbb{Z}_{\ge 0}^3$ with $a + 2b + 5c = 10$, a polytope of dimension 2. There are 10 ways: $c = 0, 1, 2$ give $6, 3, 1$. See [coin change counting](/coin-change-counting/).
- **Standard simplex.** For $\Delta_d = \{x \in \mathbb{R}^d : x \ge 0, \sum x_i \le 1\}$, $L_{\Delta_d}(t) = \binom{t + d}{d}$. The leading coefficient is $1/d!$, the volume of $\Delta_d$.
- **Magic squares.** The $3 \times 3$ matrices of nonnegative integers with all row and column sums $t$ are the lattice points of $t B_3$, where $B_3$ is the Birkhoff polytope of doubly stochastic matrices, of dimension 4. MacMahon's formula gives $H_3(t) = \binom{t+4}{4} + \binom{t+3}{4} + \binom{t+2}{4}$; for example $H_3(2) = 21$. These numbers are entry $t + 1$ of OEIS A002817.
- **A rational segment.** For $P = [0, 1/2]$, $L_P(t) = \lfloor t/2 \rfloor + 1$, a quasi-polynomial of period 2.
- **Non-example.** A polygon with irrational vertices is not a rational polytope. Its count can still be computed in the plane, with sums of floor functions, but Ehrhart's theorem does not apply.

## Known algorithms

- **Enumeration.** Scan the bounding box, or recurse on the last coordinate and count the integer points of each slice. The time is proportional to the number of slices, which can be exponential in $L$.
- **Dimension 1 and 2.** In dimension 1, $|[\alpha, \beta] \cap \mathbb{Z}| = \lfloor \beta \rfloor - \lceil \alpha \rceil + 1$. In dimension 2, Pick's theorem counts a lattice polygon from its area and boundary, and a rational polygon reduces to sums $\sum_{x} \lfloor (ax + b)/c \rfloor$, computed by a Euclid-like recursion in a number of steps logarithmic in the coefficients, see [lattice points in a non-lattice polygon](/lattice-points-in-non-lattice-polygon/).
- **Barvinok's algorithm.** For fixed $d$, write $f(P; z)$ as a sum over the vertices of $P$ of the generating functions of their tangent cones (Brion's theorem), cut each cone into unimodular cones with a signed decomposition that uses short vectors from [lattice basis reduction](/lattice-basis-reduction/), and evaluate at $z = (1, \ldots, 1)$ through a limit. The time is polynomial in $L$ for each fixed $d$. See [Barvinok's algorithm](/barvinok-algorithm/).
- **Ehrhart quasi-polynomials.** Barvinok's method extends to dilations and to parametric polytopes, and gives the Ehrhart quasi-polynomial in a compact form with fractional-part functions. For a rational simplex, Barvinok also showed that a fixed number of the top coefficients can be computed in polynomial time even when $d$ varies.
- **Decision version.** Deciding whether $P \cap \mathbb{Z}^d$ is nonempty is [integer programming feasibility](/integer-programming-fixed-dimension/). It is NP-complete in general and polynomial for fixed $d$ by [Lenstra's algorithm](/lenstra-algorithm/).
- **Software.** LattE implements Barvinok's algorithm, and the barvinok library by Verdoolaege handles parametric polytopes.

## Bounds

- **Output size.** The count can be $2^{\Theta(L)}$. The vertices of $P$ are solutions of $d \times d$ subsystems of $Ax = b$, so by Cramer's rule their coordinates have absolute value $2^{O(L)}$, and the count has $O(dL)$ bits.
- **Fixed dimension.** Barvinok's algorithm runs in time polynomial in $L$ for each fixed $d$, with an exponent that grows with $d$.
- **Hardness.** With $d$ part of the input, the problem is #P-hard, even for polytopes with 0-1 vertices given by totally unimodular inequalities (see the reductions). Deciding nonemptiness is NP-complete.
- **Volume.** For a full-dimensional lattice polytope, $L_P(t) = \operatorname{vol}(P) t^d + O(t^{d-1})$, so for large dilations the count is close to the volume. The second coefficient of $L_P$ is half the sum of the relative volumes of the facets, each measured in the lattice of its own affine span.

## Reductions

- **From counting bipartite perfect matchings.** For a bipartite graph with edge set $E$, the perfect matchings are the integer points of $\{x \in [0,1]^E : \sum_{e \ni v} x_e = 1 \text{ for every vertex } v\}$. Counting them is #P-complete ([counting perfect matchings](/counting-perfect-matchings/)), so lattice point counting in varying dimension is #P-hard.
- **From counting knapsack solutions.** The 0-1 vectors with $a \cdot x \le b$ are the lattice points of $\{x \in [0,1]^n : a \cdot x \le b\}$, which contains [counting subset sum](/counting-subset-sum/).
- **To the decision problem.** The count is positive if and only if the integer program is feasible, so an exact counting algorithm decides feasibility.
- **To optimization.** With the generating function in hand, the maximum of a linear function $c \cdot x$ over $P \cap \mathbb{Z}^d$ can be found by binary search on a bound added as one more inequality, with counts as the oracle.
- **Ehrhart polynomial and counting.** For a lattice polytope, a counting oracle on $d + 1$ dilations gives $L_P$ by interpolation, and $L_P$ gives the count at $t = 1$.

## Applications

- **Statistics.** Counting contingency tables with fixed row and column sums, used for exact tests of independence.
- **Representation theory.** Kostka numbers and Littlewood-Richardson coefficients are numbers of lattice points in certain polytopes.
- **Compilers.** The number of iterations of a loop nest with affine bounds, the number of distinct memory locations touched, and the number of cache misses, as functions of the problem size.
- **Combinatorics.** Magic squares, partitions with restricted parts, and [coin change counting](/coin-change-counting/), which are Ehrhart quasi-polynomials of rational polytopes.
- **Integer programming.** Barvinok's generating functions are also used to optimize over the integer points and to test feasibility.

## References
