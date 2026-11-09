---
tag: EFNZQ1
kind: algorithm
slug: barvinok-algorithm
name: Barvinok's algorithm
aliases:
- Barvinok's short rational generating functions
- Barvinok's lattice point counting algorithm
area: combinatorics/counting-algorithms
level: research
summary: Counts lattice points in fixed dimension via short rational generating functions.
solves: [lattice-point-counting]
model: word-ram
complexity:
  vars: {L: the number of bits of the input, d: the dimension (a fixed constant)}
  time: {worst: L^O(d log d)}
  space: {extra: L^O(d log d)}
properties: {deterministic: true, recursive: false}
history:
  year: 1994
  people: [Alexander I. Barvinok]
  note: Barvinok gave the first algorithm that counts the lattice points of a rational polytope in polynomial time for each fixed dimension. Dyer and Kannan simplified the decomposition step in 1997, and De Loera and others implemented it in the program LattE in 2004.
prereqs: [lattice-point-counting, convex-polytope, generating-functions, lagrange-gauss-reduction]
see_also: [picks-theorem, lattice-points-in-non-lattice-polygon, lll-algorithm, shortest-vector-problem, integer-programming-fixed-dimension, lenstra-algorithm, unimodular-matrix, coin-change-counting]
sources:
  - paper: doi:10.1287/moor.19.4.769
    title: Alexander I. Barvinok, A polynomial time algorithm for counting integral points in polyhedra when the dimension is fixed, Mathematics of Operations Research 19(4), 769 to 779, 1994
    locator: the whole paper (the signed decomposition into unimodular cones and the main theorem)
  - paper: doi:10.24033/asens.1572
    title: Michel Brion, Points entiers dans les polyèdres convexes, Annales scientifiques de l'École normale supérieure 21(4), 653 to 663, 1988
    locator: the main theorem (the generating function of a polytope is the sum over its vertices of those of the tangent cones)
  - paper: doi:10.1287/moor.22.3.545
    title: Martin Dyer and Ravi Kannan, On Barvinok's algorithm for counting lattice points in fixed dimension, Mathematics of Operations Research 22(3), 545 to 549, 1997
    locator: the whole paper (a simpler form of the decomposition step)
  - paper: doi:10.1016/j.jsc.2003.04.003
    title: Jesús A. De Loera, Raymond Hemmecke, Jeremiah Tauzer and Ruriko Yoshida, Effective lattice point counting in rational convex polytopes, Journal of Symbolic Computation 38(4), 1273 to 1302, 2004
    locator: Section 2 (the algorithm as implemented in LattE, with the evaluation at z = 1 by a residue computation)
  - book: isbn:9783037190524
    title: Alexander Barvinok, Integer Points in Polyhedra, European Mathematical Society, 2008
    locator: the chapters on the algebra of polyhedra, polarity, Brion's theorem and the polynomial time algorithm
  - book: isbn:9781493929689
    title: Matthias Beck and Sinai Robins, Computing the Continuous Discretely, second edition, Springer, 2015
    locator: Chapter 3 (generating functions of rational cones) and Chapter 11 (Brion's theorem)
---

Barvinok's algorithm counts the integer points of a rational polytope $P \subset \mathbb{R}^d$ in time polynomial in the input size $L$, for each fixed dimension $d$. It never lists the points. Instead it writes the generating function

$$f(P; z) = \sum_{m \in P \cap \mathbb{Z}^d} z^m, \qquad z^m = z_1^{m_1} \cdots z_d^{m_d},$$

which may have exponentially many terms, as a short signed sum of rational functions of the form $z^u / \prod_{j=1}^{d} (1 - z^{b_j})$, one for each unimodular cone, and then evaluates the sum at $z = (1, \ldots, 1)$. Three facts make this work. Brion's theorem writes $f(P; z)$ as the sum over the vertices $v$ of the generating functions of the tangent cones at $v$. A cone whose generators form a basis of $\mathbb{Z}^d$ (a unimodular cone) has a one-term rational function. And Barvinok's signed decomposition writes any simplicial cone as a signed sum of unimodular cones, with only $L^{O(d \log d)}$ terms, by using short lattice vectors. The count is the constant term of the sum after the substitution $z = e^{\tau \lambda}$.

## In plain words

You want the number of grid points inside a shape with flat sides. There can be far too many to visit.

Instead of counting points, the method writes down a formula that lists them all at once, like a catalog. Near each corner, the shape looks like an endless wedge. The points of a wedge have a short catalog when the wedge is simple enough, and a famous identity says that the catalogs of all the corner wedges add up to the catalog of the shape. A wedge that is not simple is split into simple wedges, with plus and minus signs, using a short arrow on the grid; each split makes the wedges much simpler, so only a few splits are needed. In the end, a single number is read off from the sum of the short catalogs, and that number is the count.

## The problem

Input: a rational polytope $P = \{x \in \mathbb{R}^d : Ax \le b\}$ with integer $A$ and $b$, or its list of rational vertices. Output: $|P \cap \mathbb{Z}^d|$. The dimension $d$ is a constant. This is the problem of [counting lattice points](/lattice-point-counting/). The implementation on this page handles $d = 2$: a convex polygon with rational vertices.

Notation: for linearly independent $g_1, \ldots, g_d \in \mathbb{Z}^d$, $\operatorname{cone}(G) = \{\sum_i \mu_i g_i : \mu_i \ge 0\}$, where $G$ is the matrix with columns $g_i$, and $|\det G|$ is the index of the cone. The cone is unimodular if its index is 1. The dual of a cone $K$ is $K^* = \{y : y \cdot x \ge 0 \text{ for all } x \in K\}$. The tangent cone of $P$ at a vertex $v$ is the cone generated by the directions $x - v$ for $x \in P$.

## The algorithm

```pseudo id=main
BARVINOK(P)                          ▷ P ⊂ R^d a rational polytope, d fixed
L1  S ← empty list                   ▷ terms (ε, u, B) for ε z^u / ∏_{b∈B} (1 − z^b)
L2  for each vertex v of P do
L3      Q ← a triangulation of the dual of the tangent cone at v into simplicial cones, each with sign +1
L4      while Q holds (ε, cone(G)) with |det G| > 1 do
L5          find w = Gλ ∈ Z^d, w ≠ 0, with all |λ_i| ≤ |det G|^(−1/d); if all λ_i < 0 then w ← −w
L6          replace (ε, cone(G)) by (ε · sgn λ_i, cone(G with column i set to w)) for each i with λ_i ≠ 0
L7      for each (ε, C) in Q do B ← the generators of the dual cone C*, a basis of Z^d
L8          u ← B ⌈B^(−1) v⌉;  append (ε, u, B) to S        ▷ the first lattice point of v + cone(B)
L9  choose λ ∈ Z^d with λ · b ≠ 0 for every generator b of every term in S
L10 return the constant term at τ = 0 of Σ_{(ε,u,B)∈S} ε e^(τ λ·u) / ∏_{b∈B} (1 − e^(τ λ·b))
```

Line L5 exists by Minkowski's theorem: the lattice $G^{-1} \mathbb{Z}^d$ has determinant $1/|\det G|$, so the cube $\{\lambda : |\lambda_i| \le |\det G|^{-1/d}\}$ contains a nonzero point of it. The new cones of line L6 have index $|\lambda_i| \cdot |\det G| \le |\det G|^{(d-1)/d}$, which is smaller. In dimension 2, the implementation finds $\lambda$ as a shortest vector of that lattice with [Lagrange-Gauss reduction](/lagrange-gauss-reduction/), which gives $|\lambda_i| \le (4/3)^{1/4} |\det G|^{-1/2}$, enough for the index to drop when it is at least 2. In dimension 2 line L3 has nothing to triangulate.

The decomposition works on the dual cones because, modulo lower-dimensional cones, the identity of line L6 is exact for indicator functions, and the dual of a lower-dimensional cone contains a line. A polyhedron that contains a line has generating function 0, so the error terms vanish in the primal.

In line L10, the constant term of one term is $\frac{(-1)^d}{\prod_j (\lambda \cdot b_j)}$ times the coefficient of $\tau^d$ in $e^{\tau \lambda \cdot u} \prod_{j} \frac{\tau \lambda \cdot b_j}{e^{\tau \lambda \cdot b_j} - 1}$, and $\frac{x}{e^x - 1} = \sum_k B_k x^k / k!$ with the Bernoulli numbers $B_0 = 1$, $B_1 = -\frac12$, $B_2 = \frac16$. For $d = 2$, with $a = \lambda \cdot u$, $\beta = \lambda \cdot b_1$ and $\gamma = \lambda \cdot b_2$, the constant term is

$$\frac{1}{\beta \gamma} \left( \frac{a^2}{2} - \frac{a (\beta + \gamma)}{2} + \frac{\beta^2 + \gamma^2}{12} + \frac{\beta \gamma}{4} \right).$$

## Example

Let $P$ be the triangle with vertices $(0,0)$, $(2,0)$, $(0,1)$. It contains 4 lattice points: $(0,0)$, $(1,0)$, $(2,0)$, $(0,1)$.

| step | vertex | state after the step |
|---|---|---|
| L3 | $(0,0)$ | tangent cone $\operatorname{cone}((1,0), (0,1))$, index 1; its dual is also unimodular |
| L7, L8 | $(0,0)$ | term $+1$, $u = (0,0)$, $B = ((1,0), (0,1))$ |
| L3 | $(2,0)$ | tangent cone $\operatorname{cone}((-2,1), (-1,0))$, index 1 |
| L7, L8 | $(2,0)$ | term $+1$, $u = (2,0)$, $B = ((-2,1), (-1,0))$ |
| L3 | $(0,1)$ | tangent cone $\operatorname{cone}((0,-1), (2,-1))$, index 2; dual cone $\operatorname{cone}((1,0), (-1,-2))$, index 2 |
| L5 | $(0,1)$ | shortest vector gives $\lambda = (-\frac12, -\frac12)$, all negative, so $w = (0,-1)$ with $\lambda = (\frac12, \frac12)$ |
| L6 | $(0,1)$ | $+\operatorname{cone}((0,-1), (-1,-2))$ and $+\operatorname{cone}((1,0), (0,-1))$, both of index 1 |
| L7, L8 | $(0,1)$ | terms $+1$, $u = (0,1)$, $B = ((0,-1), (1,0))$ and $+1$, $u = (0,1)$, $B = ((-1,0), (2,-1))$ |
| L9 | | $\lambda = (1, 1)$ |
| L10 | | constant terms $\frac{5}{12} + \frac{53}{12} - \frac{5}{12} - \frac{5}{12} = 4$ |

At the vertex $(0,1)$, the two primal cones are the quadrant below and to the right, and the cone from direction $(-1,0)$ to direction $(2,-1)$ through the lower half-plane. Together they cover the tangent cone twice and the rest of the lower half-plane once, so their sum is the tangent cone plus a half-plane. The half-plane contains a line and contributes 0.

## Correctness

The full proof, for the implemented case $d = 2$, is in `proofs/correctness.md`. It rests on four facts.

- **Brion's theorem.** Modulo polyhedra that contain lines, the indicator function of $P$ equals the sum of the indicator functions of $v + T_v$ over the vertices $v$, where $T_v$ is the tangent cone. The map from indicator functions to rational generating functions is linear and sends polyhedra with lines to 0, so $f(P; z) = \sum_v f(v + T_v; z)$.
- **Signed decomposition.** If $w = G\lambda$ with $\lambda$ not all negative, the identity $[\operatorname{cone}(G)] = \sum_i \operatorname{sgn}(\lambda_i) [\operatorname{cone}(G_i)]$ holds modulo lower-dimensional cones, where $G_i$ is $G$ with column $i$ set to $w$. Taking duals turns lower-dimensional cones into cones that contain lines.
- **Unimodular cones.** If $B$ is a basis of $\mathbb{Z}^d$, the lattice points of $v + \operatorname{cone}(B)$ are $u + \sum_j n_j b_j$ with $n_j \ge 0$ and $u$ from line L8, so the generating function is $z^u / \prod_j (1 - z^{b_j})$.
- **Evaluation.** After the substitution $z = e^{\tau \lambda}$, the sum is $\sum_{m} e^{\tau \lambda \cdot m}$ over the lattice points, an analytic function of $\tau$ whose value at 0 is the count. The individual terms have poles at $\tau = 0$, but the poles cancel, and the constant term of the sum of the Laurent series is the count.

## Complexity

- **Number of cones.** Each step of line L6 replaces a cone of index $D$ by at most $d$ cones of index at most $D^{(d-1)/d}$. After $k$ levels the index is at most $D^{((d-1)/d)^k}$, so the depth is $O(d \log \log D)$, and the number of unimodular cones per simplicial cone is at most $d^{O(d \log \log D)} = (\log D)^{O(d \log d)}$. The index $D$ of a tangent cone has $O(L)$ bits, so there are $L^{O(d \log d)}$ terms for fixed $d$.
- **Each step.** For fixed $d$, the number of vertices and the triangulation of each tangent cone are polynomial in $L$; a short vector in line L5 takes time polynomial in $L$; the constant term in line L10 is a polynomial in the dot products, computed with $O(1)$ arithmetic operations for fixed $d$.
- **Total.** $L^{O(d \log d)}$ time and space for fixed $d$, polynomial in $L$.
- **Dimension 2.** Each index drops from $D$ to at most $(4/3)^{1/4} \sqrt{D}$, so each vertex gives $O(\log D)$ unimodular cones, and the whole algorithm is polynomial in $L$ with a small exponent.

## Properties

- **Exact.** All arithmetic is on rationals, and the result is the exact count.
- **Short output.** The intermediate result is a formula for $f(P; z)$ with $L^{O(d \log d)}$ terms, even when $P$ has $2^{\Theta(L)}$ lattice points. The formula can be reused: substitutions give weighted counts and sums of $z^m$ over the points.
- **No enumeration.** The time does not depend on the number of lattice points, only on the bit size of the input.
- **Exponent in $d$.** The time grows as $L^{O(d \log d)}$, so the method is practical only in small dimension.

## Variants and improvements

- **Primal decomposition.** Decomposing the tangent cones directly, instead of their duals, leaves lower-dimensional error terms. Köppe and Verdoolaege handle them exactly with half-open cones, which is often faster.
- **Stopping early.** An implementation can stop the decomposition at cones of small index and list the lattice points of their fundamental parallelepipeds, whose number equals the index. This is often faster in practice.
- **Ehrhart quasi-polynomials.** Running the algorithm with a symbolic dilation factor gives the Ehrhart quasi-polynomial, and with parametric right-hand sides it gives piecewise quasi-polynomials, as in the barvinok library of Verdoolaege.
- **Projections and Boolean operations.** Barvinok and Woods showed that the short rational generating functions can be intersected, combined and projected in polynomial time for fixed dimension, which counts points of projections of polytopes.
- **Optimization.** The generating function, with a linear substitution and a search over a bound, finds the optimum of an integer program.
- **Dimension 2.** For polygons, a Euclid-like recursion over sums of floor functions is simpler and equally fast, see [lattice points in a non-lattice polygon](/lattice-points-in-non-lattice-polygon/).

## When to use it

Use Barvinok's algorithm, in practice through LattE or the barvinok library, when the dimension is small, the polytope is large, and the count is too big to enumerate: contingency tables with small margins and large totals, Ehrhart polynomials, and loop nests in compilers. For a polygon with integer vertices, [Pick's theorem](/picks-theorem/) is simpler. For large dimension, the method is too slow, and the problem is #P-hard; use enumeration with pruning or a randomized [approximation](/approximate-counting/). If only feasibility is needed, use [Lenstra's algorithm](/lenstra-algorithm/).

## Pitfalls

- **Lower-dimensional pieces.** The identity of line L6 holds only modulo lower-dimensional cones. Applying it to the tangent cones themselves, instead of their duals in line L3, counts lattice points on the shared rays more than once or not at all.
- **All coefficients negative.** If all $\lambda_i$ are negative, the cones of line L6 together with $\operatorname{cone}(G)$ cover the whole space, and the identity fails by the whole space, which is not a lower-dimensional cone. Line L5 must replace $w$ by $-w$. In the example, keeping $w = (0, 1)$ with signs $-1, -1$ gives a wrong decomposition.
- **The first lattice point.** Line L8 must round up, $\lceil B^{-1} v \rceil$, so that $u$ lies in the cone. Rounding down or to nearest gives a point outside the closed cone when $v$ is not a lattice point, and shifts the generating function by a factor $z^{b_j}$.
- **The direction of evaluation.** Line L9 needs $\lambda \cdot b \ne 0$ for every generator. With $\lambda \cdot b = 0$, a factor $1 - e^{\tau \lambda \cdot b}$ is identically 0, and the term is undefined.
- **Rounding.** The constant terms in line L10 are fractions with large cancellation. Floating point gives a wrong count; use exact rationals.

## Implementations

## History

Michel Brion proved his formula for the generating function of a polytope in 1988. Alexander Barvinok combined it with a signed decomposition of cones into unimodular cones, driven by short vectors from lattice basis reduction, and in 1994 gave the first algorithm that counts lattice points in polynomial time for each fixed dimension. Dyer and Kannan simplified the decomposition in 1997, and Barvinok and Pommersheim surveyed the theory in 1999. De Loera, Hemmecke, Tauzer and Yoshida implemented the algorithm as LattE in 2004, and Verdoolaege extended it to parametric polytopes for compilers. Barvinok and Woods extended the short generating functions to projections in 2003.

## References
