---
tag: Z1EBSJ
kind: problem
slug: minimum-volume-enclosing-ellipsoid
name: Minimum volume enclosing ellipsoid
aliases:
- MVEE
- Lowner-John ellipsoid
- minimum enclosing ellipse
- Löwner-John ellipsoid
- minimum volume covering ellipsoid
- smallest enclosing ellipsoid
area: geometry/geometric-optimization
level: advanced
summary: Find the ellipsoid of least volume that contains n points in d dimensions. It is unique, it is fixed by at most d(d+3)/2 points, and its dual is D-optimal design.
prereqs: [minimum-enclosing-ball, convex-set, convex-optimization-problem]
see_also: [khachiyans-algorithm, minimum-enclosing-ball, welzls-algorithm, lp-type-problem, coreset, semidefinite-programming, ellipsoid-method, minimum-area-enclosing-rectangle]
sources:
  - paper: "Fritz John, Extremum problems with inequalities as subsidiary conditions, Studies and Essays presented to R. Courant on his 60th Birthday, Interscience, 1948"
    locator: the optimality conditions with contact points, the bound d(d + 3)/2 on their number, and the shrinking factor d (and √d for symmetric sets)
  - paper: doi:10.1007/BFb0038202
    title: Emo Welzl, Smallest enclosing disks (balls and ellipsoids), in New Results and New Trends in Computer Science, Lecture Notes in Computer Science 555, Springer, 1991
    locator: the extension of the randomized incremental algorithm to ellipsoids, expected O(n) time for fixed d with at most d(d + 3)/2 defining points
  - paper: "Leonid G. Khachiyan, Rounding of polytopes in the real number model of computation, Mathematics of Operations Research 21(2), 1996"
    locator: the first-order algorithm on the dual and its bound of O(n d^2 (1/ε + log d + log log n)) operations
  - paper: "Michael J. Todd and E. Alper Yıldırım, On Khachiyan's algorithm for the computation of minimum-volume enclosing ellipsoids, Discrete Applied Mathematics 155(13), 2007"
    locator: Section 2 (the primal and dual problems and their optimality conditions), Theorem 4.1 (O(d(log d + 1/ε)) iterations with away steps)
  - paper: "Piyush Kumar and E. Alper Yıldırım, Minimum-volume enclosing ellipsoids and core sets, Journal of Optimization Theory and Applications 126(1), 2005"
    locator: core sets of size O(d(log d + 1/ε)), independent of n
  - paper: "Keith Ball, An elementary introduction to modern convex geometry, in Flavors of Geometry, MSRI Publications 31, Cambridge University Press, 1997"
    locator: Lecture 3, John's theorem in the form with contact points u_i and weights c_i, sum of c_i u_i u_i^T equal to the identity
  - paper: "Bernd Gärtner and Sven Schönherr, Exact primitives for smallest enclosing ellipses, Proceedings of the 13th Annual Symposium on Computational Geometry (SoCG 1997), ACM, 1997"
    locator: the exact primitives for the base cases of Welzl's algorithm in the plane
---

The minimum volume enclosing ellipsoid problem asks for the ellipsoid of least volume that contains $n$ given points in $\mathbb{R}^d$. It is the ellipsoid form of the [minimum enclosing ball](/minimum-enclosing-ball/), and unlike the ball it does not change its relation to the points under an invertible affine map. The ellipsoid is unique, and John (1948) showed that at most $d(d + 3)/2$ points on its boundary fix it and that, shrunk by the factor $d$ about its center, it fits inside the [convex hull](/convex-hull/) of the points. The problem is a [convex optimization problem](/convex-optimization-problem/) whose dual is the D-optimal design problem of statistics. In fixed dimension it is an [LP-type problem](/lp-type-problem/) and takes expected $O(n)$ time; in high dimension one uses [Khachiyan's algorithm](/khachiyans-algorithm/) and its descendants, which give a $(1 + \varepsilon)$-approximation in volume.

## In plain words

You have a cloud of points and want the smallest egg shape that holds them all, where the egg can be stretched and tilted in any direction. Smallest means least volume, or least area in the plane.

The answer is unique. It touches a few of the points, and those few decide it: in the plane at most five, because an ellipse has five free numbers. The touching points surround the center in a balanced way, so the egg cannot slide or squeeze to get smaller.

If you stretch or shear the points, the best egg is stretched or sheared in the same way. So a long thin cloud is no harder than a round one. The best egg is never too loose: shrink it toward its center by the number of dimensions and it fits inside the cloud's outline.

## Definition

Notation: $P = \{a_1, \ldots, a_n\} \subset \mathbb{R}^d$, $n = |P|$. An ellipsoid is $E(c, M) = \{x : (x - c)^\top M (x - c) \le 1\}$ with $c \in \mathbb{R}^d$ and $M$ symmetric positive definite; its volume is $\omega_d \det(M)^{-1/2}$, where $\omega_d$ is the volume of the unit ball. The problem assumes that $P$ spans $\mathbb{R}^d$ affinely. If it does not, every ellipsoid that contains $P$ has positive volume but the infimum is 0 and is not attained; one then solves the problem in the affine hull of $P$.

**Input.** A finite set $P \subset \mathbb{R}^d$ that spans $\mathbb{R}^d$ affinely.

**Output.** The center $c^*$ and the matrix $M^*$ of the ellipsoid $E^* = E(c^*, M^*)$ that contains $P$ and has the least volume:

$$\min_{c,\ M \succ 0} \ -\log\det M \quad \text{subject to} \quad (a_i - c)^\top M (a_i - c) \le 1, \quad i = 1, \ldots, n.$$

With the change of variables $A = M^{1/2}$ and $b = A c$, the constraints become $|A a_i - b| \le 1$, which are convex, and $-\log\det A$ is convex on positive definite matrices. So the problem is convex.

**Theorem (John 1948, in the form of Ball 1997).** (a) $E^*$ exists and is unique. (b) Apply an affine map that sends $E^*$ to the unit ball $B$. Then there are points $u_1, \ldots, u_m$ of the image of $P$ on the unit sphere and weights $\lambda_1, \ldots, \lambda_m > 0$ with

$$\sum_j \lambda_j u_j = 0, \qquad \sum_j \lambda_j u_j u_j^\top = I_d,$$

and conversely, if $B$ contains the points and such $u_j$ and $\lambda_j$ exist, then $B$ is the minimum volume enclosing ellipsoid. (c) One can choose $m \le d(d + 3)/2$. (d) $c^* + \frac{1}{d}(E^* - c^*) \subseteq \operatorname{conv} P$; if $P$ is symmetric about the origin, $c^* = 0$ and $\frac{1}{\sqrt{d}} E^* \subseteq \operatorname{conv} P$.

Taking the trace in (b) gives $\sum_j \lambda_j = d$. Part (c) is a count: the conditions in (b) are $d + d(d + 1)/2 = d(d + 3)/2$ linear equations in the weights, so [Carathéodory's theorem](/caratheodory-theorem/) bounds the support. In the plane this is 5.

**Duality.** Lift each point to $q_i = (a_i, 1) \in \mathbb{R}^{d+1}$. For weights $p$ in the simplex let $\Lambda(p) = \sum_i p_i q_i q_i^\top$, $c_p = \sum_i p_i a_i$ and $S_p = \sum_i p_i (a_i - c_p)(a_i - c_p)^\top$; then $\det\Lambda(p) = \det S_p$. The dual problem is

$$\max_{p \ge 0,\ \sum p_i = 1} \ \log\det \Lambda(p).$$

Weak duality: for every enclosing ellipsoid $E(c, M)$ and every $p$, $\mathrm{tr}(M S_p) \le \sum_i p_i (a_i - c)^\top M (a_i - c) \le 1$, and the inequality of arithmetic and geometric means on the eigenvalues of $M^{1/2} S_p M^{1/2}$ gives $\mathrm{vol}\, E(c, M) \ge \omega_d \det(d\, S_p)^{1/2}$. Strong duality holds: at the optimal $p^*$, $E^* = \{x : (x - c_{p^*})^\top (d\, S_{p^*})^{-1} (x - c_{p^*}) \le 1\}$. The optimality condition is that $w_i = q_i^\top \Lambda(p^*)^{-1} q_i \le d + 1$ for all $i$, with equality where $p^*_i > 0$. This is the Kiefer-Wolfowitz equivalence theorem for D-optimal designs, and the full proofs of weak duality and of the role of $w_i$ are in the [correctness proof of Khachiyan's algorithm](/khachiyans-algorithm/).

**Degeneracies.** No general position is needed. Many points may lie on the boundary of $E^*$, and the contact points and weights in (b) need not be unique, but $E^*$ is. Points inside $\operatorname{conv} P$ never matter, so one may first reduce $P$ to the vertices of its convex hull.

## Variants

- **Fixed center.** The center is given, say the origin. Then the problem is $\max \log\det \sum_i p_i a_i a_i^\top$ without the lift; for sets symmetric about the origin this is the same as the free problem, and the shrinking factor is $\sqrt{d}$.
- **Maximum volume inscribed ellipsoid.** For a convex body, often a polytope given by inequalities, find the largest ellipsoid inside it. This is the other half of John's theorem, with the same factor $d$; it is the rounding step in some methods for convex optimization and volume estimation.
- **Enclosing ellipsoids of other sets.** The smallest ellipsoid that contains given ellipsoids or balls; it is a [semidefinite program](/semidefinite-programming/) with a log-determinant objective.
- **Outliers.** The minimum volume ellipsoid estimator of robust statistics asks for the smallest ellipsoid that covers $h$ of the $n$ points; this is a much harder combinatorial problem.
- **Plane.** $d = 2$ is the minimum area enclosing ellipse, fixed by at most 5 points.
- **Ball.** If the ellipsoid must be a ball, the problem is the [minimum enclosing ball](/minimum-enclosing-ball/), whose answer changes under affine maps.

## Examples

All values are exact. An ellipsoid is given by its center $c$ and its matrix $M$.

| points | $c$ | $M$ | area | contact points |
|---|---|---|---|---|
| the square $(\pm 1, \pm 1)$, with any points inside | $(0, 0)$ | $\frac{1}{2} I$ | $2\pi$ | the 4 corners |
| the rectangle $(0, 0)$, $(4, 0)$, $(4, 2)$, $(0, 2)$ | $(2, 1)$ | $\mathrm{diag}(1/8, 1/2)$ | $4\pi$ | the 4 corners |
| the triangle $(0, 0)$, $(4, 0)$, $(0, 4)$ | $(4/3, 4/3)$ | $\frac{3}{32}\begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$ | $32\pi/(3\sqrt{3})$ | the 3 vertices |
| the cube $(\pm 1, \pm 1, \pm 1)$ | $(0, 0, 0)$ | $\frac{1}{3} I$ | volume $4\sqrt{3}\,\pi$ | the 8 corners |

The rectangle is the image of the square under $(x, y) \mapsto (2x + 2, y + 1)$, and its ellipse is the image of the circle of radius $\sqrt{2}$, with semi-axes $2\sqrt{2}$ and $\sqrt{2}$. For the triangle the answer is the Steiner circumellipse, whose center is the centroid; the weights are $1/3$ each, $S_p = \frac{16}{9}\begin{pmatrix} 2 & -1 \\ -1 & 2 \end{pmatrix}$, and $M = (2 S_p)^{-1}$. One checks $(0, 0)$: $v = (-4/3, -4/3)$ and $v^\top M v = \frac{3}{32} \cdot \frac{16}{9} \cdot 6 = 1$. Its area is $\frac{4\pi}{3\sqrt{3}}$ times the area 8 of the triangle, as for every triangle.

The first row shows a trap. An ellipse built from the sample covariance of all the points, then scaled until it contains them, is not the answer in general, because the covariance depends on the inner points and on repeated points. The minimum volume ellipse depends only on the hull vertices: for the square it stays the circle of radius $\sqrt{2}$ whatever points are added inside.

For the six points $(0, 0)$, $(10, 0)$, $(0, 6)$, $(4, 8)$, $(9, 7)$, $(5, 3)$, Khachiyan's algorithm with $\varepsilon = 10^{-4}$ gives an ellipse of area $99.37$ and a dual lower bound of $99.35$, so the minimum area lies between these values; the inner point $(5, 3)$ gets weight close to 0.

## Known algorithms

| algorithm | time | kind |
|---|---|---|
| the ellipsoid of every subset of at most $d(d + 3)/2$ points; the answer is the largest one | polynomial in $n$ for fixed $d$, of degree about $d^2/2$ | exact, brute force, needs a solver for small sets |
| [Welzl's algorithm](/welzls-algorithm/) (1991) | expected $O(n)$ for fixed $d$, with a constant that grows fast with $d$ | randomized, exact base cases needed |
| [Clarkson's algorithm](/clarksons-algorithm/) and other [LP-type](/lp-type-problem/) solvers | expected $O(n)$ for fixed $d$ | randomized |
| [Khachiyan's algorithm](/khachiyans-algorithm/) (1996) | $O(n d^2 (1/\varepsilon + \log d + \log\log n))$ | $(1 + \varepsilon)$-approximation of the dual conditions |
| Kumar-Yıldırım (2005) | $O(n d^2 (1/\varepsilon + \log d))$ | same, with a better start, and a core set |
| Todd-Yıldırım (2007), with away steps | $O(n d^2 (1/\varepsilon + \log d))$ | same, and faster in practice |
| [interior-point methods](/interior-point-method/) | polynomial in $n$, $d$ and $\log(1/\varepsilon)$ | high accuracy |

In these bounds $\varepsilon$ is the tolerance of the relaxed condition $w_i \le (1 + \varepsilon)(d + 1)$; the volume factor is then at most $(1 + \varepsilon)^{(d+1)/2}$. In the plane, Gärtner and Schönherr give exact primitives for the base cases of Welzl's algorithm; the case with four boundary points is the hard one.

## Bounds

- **Fixed dimension.** $\Theta(n)$ expected time: every point must be read, and LP-type algorithms reach $O(n)$.
- **John's bounds.** $\mathrm{vol}(\operatorname{conv} P) \le \mathrm{vol}(E^*) \le d^d\, \mathrm{vol}(\operatorname{conv} P)$, by part (d). The factor $d$ in (d) is tight for a simplex, and $\sqrt{d}$ is tight for a cube.
- **Contact points.** At least $d + 1$ points of $P$ lie on the boundary of $E^*$ (the $u_j$ in (b) must span, and their weighted mean is the center), and some at most $d(d + 3)/2$ of them suffice.
- **Core sets.** For every $\varepsilon$ there is a subset of $O(d(\log d + 1/\varepsilon))$ points whose minimum volume ellipsoid, suitably enlarged, contains $P$, independent of $n$ (Kumar and Yıldırım 2005). A $0$-core set of $d(d + 3)/2$ points always exists, by (c).

## Reductions

- **To a log-determinant program.** The primal above, in the variables $A \succ 0$ and $b$, is a [semidefinite program](/semidefinite-programming/) with constraints $|A a_i - b| \le 1$ and objective $\max \log\det A$.
- **Dual: D-optimal design.** Maximizing $\log\det \sum_i p_i q_i q_i^\top$ over the simplex is the D-optimal design problem for the regression vectors $q_i$; the optimal design weights give $E^*$.
- **As an LP-type problem.** The constraints are the points, the value of a subset is the volume of its ellipsoid, and the combinatorial dimension is $d(d + 3)/2$.
- **To the convex hull.** Only the vertices of $\operatorname{conv} P$ matter, so a [convex hull](/convex-hull/) step can shrink the input first.
- **Affine invariance.** For an invertible affine map $T$, the minimum ellipsoid of $T(P)$ is $T(E^*)$. So one may first map $P$ to a well-rounded position.

## Applications

- **Rounding.** Khachiyan's motivation: an ellipsoid $E$ with $\frac{1}{d} E \subseteq \operatorname{conv} P \subseteq E$, approximately, rounds a polytope for the [ellipsoid method](/ellipsoid-method/), volume estimation and sampling.
- **Optimal experimental design.** The dual is D-optimal design; the support points are where to measure.
- **Bounding volumes.** Ellipsoids fit elongated objects better than balls, for [collision detection](/collision-detection/) and for culling.
- **Statistics and outliers.** The ellipsoid gives a shape-aware notion of how far a point is from a cloud, and a robust variant underlies the minimum volume ellipsoid estimator.
- **Control and estimation.** Ellipsoidal sets bound the uncertainty in state estimation.

## References
