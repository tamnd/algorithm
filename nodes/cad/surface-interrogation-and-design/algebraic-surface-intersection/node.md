---
tag: 38DDQS
kind: algorithm
slug: algebraic-surface-intersection
name: Algebraic surface intersection
aliases:
- implicit-parametric surface intersection
area: cad/surface-interrogation-and-design
level: advanced
summary: Substitutes a parametric surface into the implicit equation of the other, so the intersection becomes a plane algebraic curve in the parameter domain that is then traced.
solves: [surface-surface-intersection]
model: real-ram
complexity:
  vars: {m: the first degree of the patch, n: the second degree of the patch, k: the degree of the implicit polynomial, T: the number of its terms, D: the larger degree of the substituted polynomial, B: the number of boxes, A: the number of arcs, S: the samples per arc, b: the bisection steps, d: the depth limit}
  time: {worst: O(T k^3 m^2 n^2 + B b D^3 + A S b D^2)}
  space: {extra: O(d D^2 + A S)}
properties: {deterministic: true, recursive: true, exact: false}
history:
  year: 1990
  people: [Nicholas M. Patrikalakis, P. V. Prakash]
  note: They wrote the algebraic curve that an algebraic surface cuts from a rational patch in the Bernstein basis over the parameter box, and split the box at turning and singular points into parts that can be traced one by one.
prereqs: [curve-surface-intersection, bezier-patch, implicit-surface, convex-hull-property]
see_also: [marching-surface-intersection, subdivision-surface-intersection, lattice-evaluation-intersection, interval-projected-polyhedron, implicitization, levin-quadric-intersection, tangential-surface-intersection, de-casteljau-algorithm]
sources:
  - book: isbn:9783540424543
    title: Nicholas M. Patrikalakis and Takashi Maekawa, Shape Interrogation for Computer Aided Design and Manufacturing, Springer, 2002
    locator: Chapter 5, Section 5.8.1, the intersection of a rational polynomial parametric surface with an implicit algebraic surface (substitution, the plane algebraic curve in the parameter box, its border, turning and singular points, and tracing)
  - paper: "N. M. Patrikalakis and P. V. Prakash, Surface intersections for geometric modeling, Journal of Mechanical Design 112(1), 100 to 107, 1990"
    title: N. M. Patrikalakis and P. V. Prakash, Surface intersections for geometric modeling, Journal of Mechanical Design 112(1), 100 to 107, 1990
    locator: the method of the abstract (the curve in the Bernstein basis over a rectangle, adaptive subdivision, turning and singular points, and tracing of the parts; general locator)
  - paper: "Rida T. Farouki, The characterization of parametric surface sections, Computer Vision, Graphics, and Image Processing 33(2), 209 to 236, 1986"
    title: Rida T. Farouki, The characterization of parametric surface sections, Computer Vision, Graphics, and Image Processing 33(2), 209 to 236, 1986
    locator: the whole paper (sections of polynomial patches by an algebraic surface as plane algebraic curves in the parameter domain; general locator)
---

Algebraic surface intersection computes the curve where a parametric patch $r(u, v)$ meets an implicit surface $f(x, y, z) = 0$ by substitution: $g(u, v) = f(r(u, v))$ is one polynomial in two unknowns, and its zero set in the parameter box is the intersection curve. The three dimensional problem becomes the problem of finding all branches of a plane algebraic curve. This page writes $g$ exactly in Bernstein form, subdivides the box until each piece is empty or holds a curve that is a graph over one parameter, and traces each piece. Unlike [lattice evaluation](/lattice-evaluation-intersection/) and [marching](/marching-surface-intersection/), it finds every closed loop, however small, and it boxes the singular points that it cannot trace.

## In plain words

One surface is drawn by a formula with two numbers, like a map. The other is a rule that says which points are on it. Put the map formula into the rule, and you get one rule on the map: the crossing line is where this rule gives zero. Now the problem is flat, a curve on a square of paper.

To find all of that curve, cut the square into pieces. A piece where the rule is clearly positive everywhere, or clearly negative, holds no curve, and you drop it. A piece where the curve can only run left to right, never turning back, is easy: you find where it enters and leaves and follow it across. Any other piece is cut into four again. Only near a point where the curve crosses itself do the pieces become tiny, and those are reported as special.

## The problem

The input is a tensor product [Bézier patch](/bezier-patch/) $r$ of bidegree $(m, n)$ on $\Omega = [0, 1]^2$, given by its control net, an [implicit surface](/implicit-surface/) $f = 0$ with $f$ a polynomial of degree $k$, a depth limit $d$ and a number $S$ of samples per arc. Rational patches work the same way after multiplying by a power of the weight, see Variants.

The output is a set of polylines in the parameter box, with every vertex on the curve $Z = \{g = 0\}$ to the precision of a bisection, the closed ones repeated at the end, and a list of boxes of side $2^{-d}$ that may hold a singular point of $Z$, where $g = g_u = g_v = 0$.

Since $f$ has degree $k$ and each coordinate of $r$ has bidegree $(m, n)$, $g$ has bidegree at most $(M, N) = (km, kn)$. For a bicubic patch and a quadric that is $(6, 6)$.

## The algorithm

```pseudo id=main
ALGEBRAIC-INTERSECT(r, f, d, S)
L1  G ← the Bernstein coefficients of g = f ∘ r on Ω, computed exactly
L2  stack ← [(G, Ω, 0)]
L3  while stack is not empty: pop (G, Q, depth)
L4      if all G_ij > 0 or all G_ij < 0 then continue                      ▷ no curve in Q
L5      if all G_i,j+1 − G_ij have one strict sign, or all G_i+1,j − G_ij do then
L6          find the roots of g on the edges of Q, sort them along the free parameter, pair neighbors, trace each pair with S bisections, and continue if the count is even
L7      if depth < d then split Q and G into four by de Casteljau and push them with depth + 1
L8      else report Q as a possible singular point
L9  chain the arcs at their common ends into curves
L10 return the curves and the reported boxes
```

Line L1 computes the products of the coordinate polynomials in the Bernstein basis by the product rule $B_{i, p} B_{j, q} = \frac{\binom{p}{i} \binom{q}{j}}{\binom{p + q}{i + j}} B_{i + j, p + q}$ in each parameter, with rational numbers, so the sign tests of lines L4 and L5 are exact. Line L4 drops a box by the [convex hull property](/convex-hull-property/): $g$ lies between the least and the largest coefficient. Line L5 tests the coefficients of a derivative, which are the differences of neighboring coefficients. If $g_v$ has a strict sign, each line $u = \text{const}$ meets the curve at most once in the box, so the curve there is a graph $v = \varphi(u)$, with no loop and no turning point. Line L6 finds the edge points as roots of univariate polynomials, pairs them in order of $u$, and computes $S$ points between the ends of each pair by bisection on the monotone function $v \mapsto g(u, v)$. An odd count, from a tangency to an edge or a point at a corner, sends the box to line L7. Line L7 is the [de Casteljau algorithm](/de-casteljau-algorithm/) at $\tfrac12$ in each parameter.

## Example

Take the bicubic bump $r(u, v) = (3u, 3v, 27 u (1 - u) v (1 - v))$, with control points $(i, j, z_{ij})$, $z_{ij} = 3$ at the four inner points and $0$ elsewhere, and the plane $z = 1$. Then $f = z - 1$ has degree $1$, $g = h - 1$ has bidegree $(3, 3)$, and its Bernstein coefficients are the control heights minus $1$:

$$G = \begin{pmatrix} -1 & -1 & -1 & -1 \\ -1 & 2 & 2 & -1 \\ -1 & 2 & 2 & -1 \\ -1 & -1 & -1 & -1 \end{pmatrix}.$$

The signs are mixed, and both difference tables contain $0$, so line L7 splits $\Omega$. The quarter $[0, \tfrac12]^2$ has the coefficients

$$\begin{pmatrix} -1 & -1 & -1 & -1 \\ -1 & -\tfrac14 & \tfrac18 & \tfrac18 \\ -1 & \tfrac18 & \tfrac{11}{16} & \tfrac{11}{16} \\ -1 & \tfrac18 & \tfrac{11}{16} & \tfrac{11}{16} \end{pmatrix},$$

again mixed, with zero differences in the last row and column, so it is split as well, and so are the other three quarters. Of the $16$ boxes of side $\tfrac14$, the $4$ at the corners of $\Omega$ have only negative coefficients and are dropped. The $8$ boxes along the edges of the inner square are monotone, and each holds one arc. For instance on $[0.5, 0.75] \times [0, 0.25]$ the curve is a graph over $u$ from $(0.5, 0.180858)$ to $(0.729061, 0.25)$. The $4$ boxes $[0.25, 0.5] \times [0.25, 0.5]$ and its mirror images are split once more, and of their $16$ children $12$ are dropped and $4$ hold one arc each. In all, $37$ boxes are visited and $12$ arcs found, and line L9 chains them into one closed curve. With $S = 4$ it has $61$ vertices, each with $|27 u (1 - u) v (1 - v) - 1| < 10^{-14}$.

With the plane $z = 1.68$ the curve is a loop of width $\tfrac{1}{15}$ in $u$ around the top. Lattice evaluation with $3$ lines in each direction misses it. Here the subdivision visits $85$ boxes and returns it as one closed curve. On the saddle $z = 9 (u - \tfrac12)(v - \tfrac12)$ cut by $z = 0$, the curve is the two lines $u = \tfrac12$ and $v = \tfrac12$, which cross at a singular point. With $d = 6$ the method returns four curves, each from an edge of $\Omega$ to the reported boxes, and the four boxes of side $\tfrac{1}{64}$ around $(\tfrac12, \tfrac12)$.

## Correctness

The [full proof](proofs/correctness.md) has five parts. A box dropped by line L4 holds no point of the curve, because $g$ is a convex combination of its Bernstein coefficients. The differences that line L5 tests are positive multiples of the Bernstein coefficients of $g_v$ or $g_u$, so a strict sign there means a strict sign of the derivative on the whole box. In such a box the curve is a graph over the other parameter, its ends are exactly the edge roots, and pairing them in sorted order gives the arcs, provided the edge roots are simple and the curve does not touch the box only at a corner. Together, the arcs and the boxes of line L8 cover the whole curve, and every closed loop is returned as a closed curve.

The last part is termination. If a box of side $h$ is split, then $|g|$, $|g_u|$ and $|g_v|$ are all at most a constant times $h$ at every point of it, with constants computed from the coefficients of the derivatives on $\Omega$. So if the curve has no singular point, every box smaller than a positive number $\mu$ is decided, and only boxes around singular points reach the depth limit. The proof uses only Bernstein facts that it proves. What is not exact are the edge roots and the traced points, which are floating point bisections from exact coefficients. The tests check the substitution exactly with rational numbers, and check on random bicubic patches cut by planes and spheres that the number of times the polylines cross $20$ fixed parameter lines equals the number of sign changes of $g$ in $2000$ samples on each line.

## Complexity

Line L1 makes, for each of the $T$ terms of $f$, at most $k$ products of Bernstein arrays of size at most $(km + 1)(kn + 1)$ by arrays of size $(m + 1)(n + 1)$, which costs $O(T k^3 m^2 n^2)$ operations on rational numbers. Each box costs $O(D^3)$ for the split, with $D = \max(km, kn)$, and $O(D^2)$ for the sign tests. A monotone box costs $O(b D^3)$ for the roots on its four edges, and each arc $O(S b D^2)$ for the tracing, with $b$ about $60$ bisection steps. With $B$ boxes and $A$ arcs, the total is $O(T k^3 m^2 n^2 + B b D^3 + A S b D^2)$ operations. The proof of termination bounds the depth by $\lceil \log_2 (1 / \mu) \rceil$ when the curve has no singular point, so $B \le \frac{4}{3} \cdot 4^{\lceil \log_2 (1 / \mu) \rceil}$, a bound that is far from tight: boxes away from the curve are dropped early, and for a regular curve the number of boxes grows with its length divided by the box size. The stack is depth first, so it holds at most $3$ boxes per level, $O(d D^2)$ coefficients for the depth limit $d$, and the output takes $O(A S)$. The cost of the rational numbers grows with the depth, since each halving adds a factor of $2$ to the denominators.

## Properties

- **Complete.** Every point of the curve is in a returned arc or a returned box, with the conditions of the proof. Small loops are not lost.
- **Exact decisions.** The tests that drop boxes and that find monotone boxes use exact rational arithmetic, so they are never wrong because of rounding.
- **Isolates singular points.** Boxes around a crossing of the curve reach the depth limit, so the method reports where it could not decide.
- **Local work.** Boxes are independent, and the work is spent near the curve.

## Variants and improvements

- **Characteristic points first.** Patrikalakis and Prakash compute the border points, the turning points where $g = g_u = 0$ or $g = g_v = 0$, and the singular points, and then split the box at them into parts that are traced one at a time. The monotone boxes of this page play the role of those parts: a box with a strict sign of $g_v$ holds no point where $g_v = 0$. The characteristic points can be found with the [interval projected polyhedron](/interval-projected-polyhedron/) method.
- **Rational patches.** For $r = (X, Y, Z) / W$ use the numerator $W^k f(X / W, Y / W, Z / W)$, the homogenized $f$ at $(X, Y, Z, W)$. It has the same zeros where $W > 0$.
- **Marching on the plane curve.** Trace the curve from the border and turning points with a predictor and corrector step in the plane, as in [marching](/marching-surface-intersection/), using the characteristic points to guarantee that all branches are found.
- **Two parametric patches.** When both surfaces are parametric, the [implicitization](/implicitization/) of one of them gives an implicit equation, and this method applies. The degree of the implicit form, up to $2mn$, makes this practical only for low degrees.
- **Quadrics.** When both surfaces are quadrics, [Levin's method](/levin-quadric-intersection/) gives a parametrization of the curve instead of a traced one.

## When to use it

Use it when one surface is implicit, such as a plane, a quadric, a torus or an offset of one, and the other is a patch: plane sections for slicing and contouring, cuts by cylinders and spheres in machining, and Booleans between primitives and freeform faces. It is the method of choice when no loop may be lost. When both surfaces are freeform of high degree, use [subdivision](/subdivision-surface-intersection/) or marching instead.

## Pitfalls

- **Coefficient growth.** The degree of $g$ is $k$ times that of the patch. A bicubic and a quartic, such as a torus, give bidegree $(12, 12)$, $169$ coefficients, and the rationals grow with the depth.
- **Tangential intersections.** Where the two surfaces touch, $g$ has a double zero along the curve, so $g$, $g_u$ and $g_v$ all vanish there, and every box along the curve reaches the depth limit. The method then returns a chain of boxes, not a curve. See [tangential surface intersection](/tangential-surface-intersection/).
- **Dyadic coincidences.** A curve that passes through a corner of the dyadic subdivision without entering a box, or is tangent to a line $u = i / 2^j$, gives an odd count in a monotone box, and that box is split down to the depth limit. Symmetric test cases hit this often.
- **Parameter space only.** The curve is computed in the parameter box of $r$. Points in space are $r(u, v)$, and a short distance in the box can be a long one in space where the patch is stretched.
- **Floating point coefficients.** Running the sign tests in floating point makes them unreliable when coefficients are near $0$, which is exactly near the curve. Exact or interval arithmetic keeps line L4 from dropping a box that holds the curve.

## Implementations

## History

Farouki (1986) studied the sections of polynomial patches by algebraic surfaces as plane algebraic curves in the parameter domain. Patrikalakis and Prakash (1990) combined the Bernstein form of that curve over a rectangle, adaptive subdivision, and the computation of turning and singular points, so that each part of the domain could be traced independently, and the approach was extended by Kriezis, Prakash and Patrikalakis in the same year. Patrikalakis and Maekawa (2002) give it as the method for a rational patch against an implicit algebraic surface in their book.

## References
