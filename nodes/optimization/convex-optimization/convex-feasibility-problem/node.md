---
tag: H1CESA
kind: problem
slug: convex-feasibility-problem
name: Convex feasibility problem
aliases:
- feasibility problem
- convex feasibility
area: optimization/convex-optimization
level: core
summary: Find a point in the intersection of finitely many closed convex sets, or decide that the intersection is empty.
prereqs: [convex-set, convex-optimization-problem]
see_also: [linear-feasibility, kaczmarz-method, projected-gradient-descent, ellipsoid-method, separation-oracle, separating-hyperplane-theorem, perceptron, admm]
sources:
  - paper: "Heinz H. Bauschke and Jonathan M. Borwein, On projection algorithms for solving convex feasibility problems, SIAM Review 38(3), 1996, 367-426"
    locator: survey of projection methods, Fejér monotonicity, regularity conditions and rates
  - paper: "Lev M. Bregman, The method of successive projection for finding a common point of convex sets, Soviet Mathematics Doklady 6, 1965, 688-692"
    locator: convergence of cyclic projections onto closed convex sets with a common point
  - paper: "L. G. Gubin, B. T. Polyak and E. V. Raik, The method of projections for finding the common point of convex sets, USSR Computational Mathematics and Mathematical Physics 7(6), 1967"
    locator: convergence and linear rates of projection methods under an interior point condition
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 11.4, Feasibility and phase I methods
---

The convex feasibility problem asks for a point in the intersection of finitely many closed [convex sets](/convex-set/), or a proof that the intersection is empty. Each [convex optimization problem](/convex-optimization-problem/) reduces to a sequence of feasibility problems by bisection on the objective value, and interior-point solvers start with a feasibility phase. When each set comes with a cheap projection, the method of cyclic projections moves a point from set to set and converges to a common point whenever one exists.

## In plain words

Several rules each allow a region of points, and each region has no dents. We want one point that obeys all the rules at once, or a proof that none exists.

A simple method is to start anywhere, move to the nearest allowed point of the first rule, then of the second rule, and so on, in a loop. Each move can only bring the point closer to every point that obeys all the rules, so the loop slowly closes in on a common point. If the regions overlap with room to spare, it gets there fast. If they only touch, it can take very long, and if they do not meet at all, it never stops on its own.

## Definition

**Input.** Closed convex sets $C_1, \dots, C_m \subseteq \mathbb{R}^n$, given in one of these forms:

- by explicit convex inequalities $C_i = \{x : f_i(x) \le 0\}$ or affine equations,
- by a *projection oracle* that returns $P_{C_i}(x) = \arg\min_{y \in C_i} \lVert y - x \rVert$,
- by a [separation oracle](/separation-oracle/) that, for $x \notin C_i$, returns a hyperplane that separates $x$ from $C_i$.

**Output.** A point $x \in C = C_1 \cap \dots \cap C_m$, or the answer that $C = \emptyset$.

With finite precision, the problem is posed with tolerances. For $\varepsilon > 0$, an *$\varepsilon$-feasible* point has $\operatorname{dist}(x, C_i) \le \varepsilon$ for each $i$. The *weak feasibility problem* asks for an $\varepsilon$-feasible point, or a proof that $C$ contains no ball of radius $r$, given a ball of radius $R$ that contains $C$.

### The method of cyclic projections

Start at $x_0$. One cycle replaces $x$ by $P_{C_m}(\cdots P_{C_2}(P_{C_1}(x)))$. The implementation in this page's folder supports half-spaces, hyperplanes, balls and boxes, whose projections have closed forms:

- half-space $\{a^T x \le b\}$: $x - \frac{\max(0, a^T x - b)}{\lVert a \rVert^2} a$,
- ball with center $c$ and radius $r$: $c + \frac{r}{\lVert x - c \rVert}(x - c)$ if $\lVert x - c \rVert > r$, and $x$ otherwise,
- box $[\ell, u]$: clip each coordinate.

It stops when $\max_i \operatorname{dist}(x, C_i) \le \varepsilon$, and reports failure after a fixed number of cycles. In floating point, $\varepsilon$ is an absolute distance, $10^{-9}$ in the tests.

**Theorem 1 (Fejér monotonicity).** Let $K$ be a nonempty closed convex set and $z \in K$. For every $x$,

$$\lVert P_K(x) - z \rVert^2 \le \lVert x - z \rVert^2 - \lVert x - P_K(x) \rVert^2.$$

*Proof.* Write $p = P_K(x)$. The projection is characterized by $(x - p)^T (y - p) \le 0$ for all $y \in K$ (see Lemma 1 on the [separating hyperplane theorem](/separating-hyperplane-theorem/) page). Then $\lVert x - z \rVert^2 = \lVert x - p \rVert^2 + \lVert p - z \rVert^2 + 2 (x - p)^T (p - z)$, and the last term is $-2(x - p)^T (z - p) \ge 0$. $\square$

**Theorem 2 (convergence).** If $C \ne \emptyset$, the iterates of cyclic projections converge to a point of $C$.

*Proof.* Let $y_0 = x_0, y_1, y_2, \dots$ be the sequence of single projections, with $y_{t+1} = P_{C_{i(t)}}(y_t)$ and $i(t) = (t \bmod m) + 1$. Fix $z \in C$. By Theorem 1, $\lVert y_t - z \rVert$ is nonincreasing, so the sequence is bounded, and summing gives $\sum_t \lVert y_{t+1} - y_t \rVert^2 \le \lVert y_0 - z \rVert^2$. So $\lVert y_{t+1} - y_t \rVert \to 0$. Take a subsequence of cycle starts $y_{k_j m} \to \bar{x}$. For each $i$, the point $y_{k_j m + i}$ lies in $C_i$ and differs from $y_{k_j m}$ by at most $i$ steps, which tend to 0. So $y_{k_j m + i} \to \bar{x}$, and $\bar{x} \in C_i$ because $C_i$ is closed. Hence $\bar{x} \in C$. Apply Theorem 1 with $z = \bar{x}$: $\lVert y_t - \bar{x} \rVert$ is nonincreasing and has a subsequence that tends to 0, so it tends to 0. $\square$

If $C = \emptyset$, the iterates do not converge to a common point, and the stopping test never succeeds. For two sets the cycle then converges, under mild conditions, to a pair of nearest points of $C_1$ and $C_2$, whose distance measures the gap.

## Variants

- **Linear feasibility.** All $C_i$ are half-spaces or hyperplanes, so $C$ is a [polyhedron](/polyhedron/). See [linear feasibility](/linear-feasibility/). Cyclic projection onto hyperplanes is the [Kaczmarz method](/kaczmarz-method/), and onto half-spaces it is the relaxation method of Agmon, Motzkin and Schoenberg.
- **Conic feasibility.** Find $x$ with $Ax = b$ and $x$ in a cone: the nonnegative orthant, the second-order cone, or the cone of positive semidefinite matrices. These are the feasibility forms of linear, [second-order cone](/second-order-cone-programming/) and [semidefinite programming](/semidefinite-programming/).
- **Strict feasibility.** Find a point that satisfies all inequalities strictly. This is the search for a [Slater point](/slater-condition/), and for homogeneous linear inequalities it is the problem the [perceptron](/perceptron/) solves.
- **Best approximation.** Find the point of $C$ nearest to a given point. Plain cyclic projections find some point of $C$, not the nearest one. Dykstra's algorithm adds correction terms and finds the nearest point.
- **Split feasibility.** Find $x \in C$ with $Ax \in Q$, for convex sets $C$ and $Q$ in different spaces.

## Examples

- **A disk and a half-plane.** Let $C_1$ be the unit disk and $C_2 = \{x : x_1 + x_2 \ge 1.2\}$. From $x_0 = (2, -1)$, the first projection onto the disk gives $(0.8944, -0.4472)$, and the projection onto the half-plane gives $(1.2708, -0.0708)$, whose distance to the disk is $0.2728$. The next cycles give $(1.1270, 0.0730)$, $(1.0667, 0.1333)$ and $(1.0341, 0.1659)$, with distances $0.1294$, $0.0750$ and $0.0473$. After 57 cycles the point is within $10^{-9}$ of both sets, near $(0.97417, 0.22583)$, where the line $x_1 + x_2 = 1.2$ meets the circle.
- **Two lines at an angle of $10°$.** For two lines through the origin at angle $\theta$, each projection multiplies the norm of the point by $\cos\theta$. One cycle multiplies it by $\cos^2 \theta$, which is $0.96985$ for $\theta = 10°$. From a point at distance 1, it takes $452$ cycles to reach distance $10^{-6}$, since $\ln(10^{-6}) / \ln(0.96985) \approx 451.2$. The rate degrades as the angle closes.
- **A disk tangent to a line.** Let $C_1 = \{x_2 = 0\}$ and $C_2$ the unit disk with center $(0, 1)$, so $C = \{0\}$. From $(1, 0)$, the distance to $C$ after $k$ cycles is about $1/\sqrt{k}$: it is $0.0316$ after $10^3$ cycles and $0.0100$ after $10^4$ cycles. The sets only touch, and the convergence is sublinear.
- **Two disjoint disks.** For unit disks with centers $(0, 0)$ and $(3, 0)$, the iterates settle at the nearest points $(1, 0)$ and $(2, 0)$, at distance 1 from each other, and the implementation returns failure.

## Known algorithms

| Method | Access to the sets | Guarantee |
|---|---|---|
| Cyclic projections (Bregman 1965; Gubin, Polyak and Raik 1967) | projections | convergence when $C \ne \emptyset$ (Theorem 2); linear when the sets are regular, for example when $C$ has an interior point |
| [Kaczmarz method](/kaczmarz-method/) | hyperplanes | linear rate for consistent systems; randomized version with rate set by a condition number |
| Simultaneous projections (Cimmino) | projections | average of the projections; also converges when $C \ne \emptyset$ |
| Dykstra's algorithm | projections | converges to the projection of the start point onto $C$ |
| Douglas-Rachford and [ADMM](/admm/) | projections of two sets | converges for two sets; often faster than alternating projections in practice |
| [Ellipsoid method](/ellipsoid-method/) | separation oracle | weak feasibility in $O(n^2 \log(R / r))$ iterations |
| [Cutting-plane methods](/cutting-plane-method/) | separation oracle | center-of-gravity and analytic-center variants with $O(n \log(R/r))$ oracle calls for the best ones |
| Phase I of [interior-point methods](/interior-point-method/) | inequalities $f_i(x) \le 0$ | minimize $s$ subject to $f_i(x) \le s$; a negative optimum gives a strictly feasible point |

## Bounds

- **With a separation oracle.** The [ellipsoid method](/ellipsoid-method/) solves weak feasibility with $O(n^2 \log(R / r))$ oracle calls, which is polynomial in $n$ and in the bit length of $R / r$. With only a separation oracle, $\Omega(n \log(R / r))$ calls are needed in the worst case, and the best cutting-plane methods match this up to constant factors.
- **With projections.** If $C$ contains a ball of radius $r$ and $\lVert x_0 - z \rVert \le R$ for some $z \in C$, the distance from the iterates to $C$ decreases at a linear rate that depends on $r / R$ (Gubin, Polyak and Raik). Without such a regularity condition there is no rate: the tangent example above converges like $1/\sqrt{k}$, and the two-line example shows that the linear rate tends to 1 as the angle closes.
- **Exact feasibility.** Deciding exact feasibility of a system of convex polynomial inequalities with integer data is harder than the weak version. A feasible set can be nonempty but contain only points with enormous coordinates, as for the constraints $x_1 \ge 2$ and $x_k^2 \le x_{k+1}$, which force $x_n \ge 2^{2^{n-1}}$ (see the [convex optimization problem](/convex-optimization-problem/) page). For semidefinite feasibility, membership in NP or co-NP is open in the Turing model.

## Reductions

- **Optimization to feasibility.** To minimize a convex $f_0$ over $C$, bisect on $t$ and ask whether $C \cap \{f_0 \le t\}$ is nonempty. Each test is a convex feasibility problem, and $\log_2((u - \ell)/\varepsilon)$ tests reach accuracy $\varepsilon$ from bounds $\ell \le p^* \le u$. The same bisection works for [quasiconvex](/quasiconvex-function/) objectives.
- **Feasibility to optimization.** $C$ is nonempty if and only if the optimal value of minimizing $s$ subject to $f_i(x) \le s$ is at most 0. This is the phase I problem of Boyd and Vandenberghe, Section 11.4.
- **Linear programming.** An LP optimum is a feasible point of the system formed by the primal constraints, the dual constraints, and the equality of the two objective values. So LP reduces to linear feasibility by [LP duality](/lp-duality/).
- **Certificates of infeasibility.** For two convex sets, emptiness of the intersection is certified by a separating hyperplane, by the [separating hyperplane theorem](/separating-hyperplane-theorem/). For linear systems the certificate is given by [Farkas' lemma](/farkas-lemma/). For convex inequalities with a Slater-type condition, it is a $\lambda \ge 0$ with $\inf_x \sum_i \lambda_i f_i(x) > 0$.

## Applications

- **Tomography.** Image reconstruction from projections solves a large linear feasibility problem. The algebraic reconstruction technique used in early computed tomography is the Kaczmarz method.
- **Signal and image recovery.** The method of projections onto convex sets (POCS) restores signals that must satisfy several convex constraints at once, such as a known band limit, nonnegativity and consistency with measurements.
- **Interior-point solvers.** Phase I finds a strictly feasible starting point.
- **Linear classification.** Finding a separating hyperplane for labeled data is a linear feasibility problem in the weights, solved by the [perceptron](/perceptron/) when a margin exists.
- **Engineering design.** Many specifications are convex constraints, and any point that meets all of them is acceptable, for example in filter design and in control.

## References
