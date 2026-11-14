---
tag: AAC2AJ
kind: problem
slug: design-centering
name: Design centering
aliases:
- parametric yield maximization
area: eda/power-reliability-and-manufacturability
level: core
summary: Choose the nominal values of circuit parameters so that the most process variation still meets the specifications, which maximizes parametric yield.
prereqs: [convex-set, monte-carlo-integration]
see_also: [simplicial-approximation, linear-programming-problem, importance-sampling, latin-hypercube-sampling, statistical-static-timing-analysis, gate-sizing, poisson-yield-model]
sources:
  - paper: doi:10.1109/TCS.1977.1084353
    title: Stephen W. Director and Gary D. Hachtel, The simplicial approximation approach to design centering, IEEE Transactions on Circuits and Systems CAS-24(7), 363 to 372, July 1977
    locator: the statement of design centering as placing the nominal point deep inside the acceptable region, and the inscribed hypersphere formulation
  - paper: "John W. Bandler and Shao Hua Chen, Circuit optimization: the state of the art, IEEE Transactions on Microwave Theory and Techniques 36(2), 424 to 443, February 1988"
    title: John W. Bandler and Shao Hua Chen, Circuit optimization, the state of the art, IEEE Transactions on Microwave Theory and Techniques 36(2), 424 to 443, February 1988
    locator: Section V on design centering, tolerance assignment and yield optimization, with a survey of the methods of the 1970s and 1980s
  - paper: doi:10.1109/43.273749
    title: Kurt J. Antreich, Helmut E. Graeb and Claudia U. Wieser, Circuit analysis and optimization driven by worst-case distances, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 13(1), 57 to 71, January 1994
    locator: the worst-case distance of each specification and yield optimization by maximizing these distances
  - paper: doi:10.1137/0217060
    title: Martin E. Dyer and Alan M. Frieze, On the complexity of computing the volume of a polyhedron, SIAM Journal on Computing 17(5), 967 to 974, 1988
    locator: computing the volume of a polytope given by linear inequalities is #P-hard
  - paper: "Martin Dyer, Alan Frieze and Ravi Kannan, A random polynomial-time algorithm for approximating the volume of convex bodies, Journal of the ACM 38(1), 1 to 17, 1991"
    title: Martin Dyer, Alan Frieze and Ravi Kannan, A random polynomial-time algorithm for approximating the volume of convex bodies, Journal of the ACM 38(1), 1 to 17, 1991
    locator: the main result, a randomized approximation of the volume of a convex body with a membership oracle in polynomial time
  - paper: "Andras Prekopa, On logarithmic concave measures and functions, Acta Scientiarum Mathematicarum (Szeged) 34, 335 to 343, 1973"
    title: András Prékopa, On logarithmic concave measures and functions, Acta Scientiarum Mathematicarum (Szeged) 34, 335 to 343, 1973
    locator: the theorem that integrating a log-concave function over some of its variables gives a log-concave function of the others
---

Design centering is the problem of choosing the nominal values of the parameters of a circuit so that the random deviations of manufacturing leave as many chips as possible inside the specifications. The fraction of chips that meet all specifications despite parameter variation is the *parametric yield*. It is different from the functional yield lost to spot defects, which the [Poisson yield model](/poisson-yield-model/) and its relatives describe. The problem is stated here without any algorithm. The [simplicial approximation](/simplicial-approximation/) page gives one method in detail.

## In plain words

A circuit has values that the designer picks, such as transistor widths or resistor values. The factory never makes them exactly. Each chip gets values that are a little off, at random.

For each specification, some values are good enough and some are not. Together, the good values form a region. If the designer picks a point near the edge of that region, many chips fall outside it and fail. If the point is deep inside, most of the random errors stay inside.

Design centering asks where to put the design so that the largest share of chips works. When the errors are the same size in all directions, the answer is close to the point farthest from every edge. When the errors are larger in some directions, the best point moves away from the edges in those directions.

## Definition

**Input.**

- A parameter space $\mathbb{R}^n$ of designable parameters $x$.
- An acceptable region $A = \{x : g_i(x) \le 0,\ i = 1, \ldots, p\} \subseteq \mathbb{R}^n$. Each $g_i$ is a specification, such as a delay or gain limit. Each evaluation of $g_i$ is a circuit simulation, so $A$ is known only through such tests.
- A random deviation $\xi$ with a density $f$ on $\mathbb{R}^n$, so that a chip made at the nominal point $x_0$ has the parameters $x_0 + \xi$.
- A set $X \subseteq \mathbb{R}^n$ of allowed nominal points, often a box of design limits.

**Output.** A nominal point $x_0 \in X$.

**Objective.** Maximize the parametric yield

$$ Y(x_0) = \Pr[\,x_0 + \xi \in A\,] = \int_{\mathbb{R}^n} \mathbf{1}_A(x_0 + \xi)\, f(\xi)\, d\xi . $$

The deviation law is fixed and does not depend on $x_0$ in this basic form. Operating conditions such as supply voltage and temperature are not random: a specification that must hold over a range of them is folded into $g_i$ as a worst case over the range.

## Variants

- **Statistical centering.** The form above. With a normal law of covariance $\Sigma$, scaling the parameters by $\Sigma^{-1/2}$ makes the law spherical, which is the setting in which inscribed balls are natural.
- **Worst-case centering.** Given a tolerance body $T$, such as the box $\prod_j [-t_j, t_j]$ or the ellipsoid $\{\xi : \xi^T \Sigma^{-1} \xi \le 1\}$, find $x_0$ and the largest $\lambda$ with $x_0 + \lambda T \subseteq A$. Every chip whose deviation lies in $\lambda T$ then works. It is the largest scaled copy of $T$ that fits in $A$.
- **Tolerance assignment.** Choose both $x_0$ and the tolerances $t_j$, at a cost that grows as the tolerances shrink, so that $x_0 + T(t) \subseteq A$ or the yield reaches a target. Bandler and Chen survey this variant together with centering.
- **Yield with mismatch.** The spread of $\xi$ depends on $x_0$, for example because the mismatch of two transistors shrinks with their area. The objective is then $\Pr[x_0 + \xi(x_0) \in A]$, and larger devices trade area for yield.
- **Yield with a cost.** Maximize the expected profit, a yield times a price minus an area or power cost, which ties centering to [gate sizing](/gate-sizing/) and other sizing problems.

## Examples

Take $n = 2$ and the triangle $A = \{(x, y) : x \ge 0,\ y \ge 0,\ x + y \le 6\}$.

**Uniform box deviations.** Let $\xi$ be uniform on the box $[-1, 1]^2$. At $x_0 = (0.5, 4)$ the shifted box is $[-0.5, 1.5] \times [3, 5]$. The part with $x < 0$ is lost. For $0 \le x \le 1$ the full height 2 is good, and for $1 \le x \le 1.5$ only $y \le 6 - x$ is good, a height of $3 - x$. The good area is $1 \cdot 2 + \int_1^{1.5} (3 - x)\, dx = 2 + 0.875 = 2.875$, so $Y = 2.875 / 4 = 23/32 \approx 0.719$. At $x_0 = (2, 2)$ the box $[1, 3]^2$ lies in $A$, since $3 + 3 = 6$, so $Y = 1$. Every point with $x \ge 1$, $y \ge 1$ and $x + y \le 4$ gives yield 1, so the optimum is not unique.

**Normal deviations.** Let $\xi$ be normal with mean 0 and covariance $\sigma^2 I$. The yield is a one-dimensional integral of normal densities and distribution functions, computed here by Simpson's rule:

| nominal point | $Y$ for $\sigma = 0.5$ | $Y$ for $\sigma = 1$ |
|---|---|---|
| (0.5, 4), near a corner | 0.8244 | 0.5494 |
| (1.757, 1.757), center of the largest inscribed disc | 0.9993 | 0.8833 |
| (2, 2), the centroid | 0.9976 | 0.8764 |
| best point on the diagonal | 0.9993 at (1.778, 1.778) | 0.8849 at (1.832, 1.832) |

The triangle is symmetric in $x$ and $y$, and $Y$ is log-concave (see Bounds), so a best point lies on the diagonal. The center of the largest inscribed disc, at radius $6 - 3\sqrt{2} \approx 1.757$, is close to the best point but not equal to it, and the gap grows with $\sigma$. The disc only sees the nearest edges, while the yield also counts how much of each tail crosses the other edges.

## Known algorithms

- **[Simplicial approximation](/simplicial-approximation/)** (Director and Hachtel 1977) for convex $A$: an inner polytope from boundary points and the center of its largest inscribed ball. It certifies a ball inside $A$ with a radius that never decreases. It solves the worst-case variant for a ball, not the statistical one, and it fails on nonconvex regions.
- **Linear programming.** When $A$ is a polytope $\{x : a_i \cdot x \le b_i\}$ given explicitly, the worst-case variant is a [linear program](/linear-programming-problem/) for a ball or a box: $x_0 + \lambda T \subseteq A$ if and only if $a_i \cdot x_0 + \lambda\, h_T(a_i) \le b_i$ for all $i$, with $h_T(a) = \|a\|_2$ for the unit ball and $h_T(a) = \sum_j |a_j| t_j$ for the box. This is exact.
- **[Monte Carlo](/monte-carlo-integration/) yield estimation with optimization.** Sample $\xi$, simulate, and count the passing samples. The estimate is unbiased, and its standard error is $\sqrt{Y(1 - Y)/N}$ for $N$ samples. Gradient and response-surface methods move $x_0$ to raise the estimate. [Importance sampling](/importance-sampling/) and [Latin hypercube sampling](/latin-hypercube-sampling/) lower the number of simulations for the same accuracy, and importance sampling is needed when the yield is very close to 1.
- **The center of gravity method** of Soin and Spence (1980, IEE Proceedings; the issue and pages were not checked) moves $x_0$ toward the mean of the passing Monte Carlo samples. It is a heuristic.
- **Worst-case distances** (Antreich, Graeb and Wieser 1994). For each specification, find the nearest failing point in the scaled parameter space by a local optimization. Its distance $\beta_i$ gives the approximation $\Phi(\beta_i)$ of the yield of that specification after linearization, and the method maximizes the smallest distances. It is exact for linear specifications and normal deviations, and approximate otherwise.
- **The ellipsoidal technique** of Abdel-Malek and Hassan (1991, IEEE TCAD; the issue and pages were not checked) approximates $A$ by ellipsoids and inscribes the tolerance ellipsoid in them.

## Bounds

- **Evaluating the yield exactly is #P-hard.** Dyer and Frieze (1988) proved that computing the volume of a polytope given by linear inequalities is #P-hard. Given such a polytope $Q$, compute a bounding box $B$ by linear programming, let $\xi$ be uniform on $B - c$ with $c$ the center of $B$, and let $A = Q$. Then $Y(c) = \mathrm{vol}(Q) / \mathrm{vol}(B)$. So an exact yield for polytope regions and uniform deviations gives the volume, and the objective of design centering is #P-hard to evaluate in general dimension.
- **Approximation is possible for convex regions.** Dyer, Frieze and Kannan (1991) gave a randomized algorithm that approximates the volume of a convex body to any relative accuracy in time polynomial in the dimension and the accuracy, with a membership oracle. Plain Monte Carlo needs a number of samples that grows only with the accuracy wanted, not with $n$, but its relative error is poor when $Y$ is close to 0 or 1.
- **Log-concavity.** If $A$ is convex and $f$ is log-concave, as a normal or a uniform density on a convex set is, then $Y$ is log-concave in $x_0$. Proof: $(z, x_0) \mapsto \mathbf{1}_A(z) f(z - x_0)$ is log-concave in $(z, x_0)$ as a product of log-concave functions, and by Prékopa's theorem (1973) its integral over $z$, which is $Y(x_0)$, is log-concave. So every local maximum of $Y$ is global, and the set of maximizers is convex. This is the main reason that local optimization works on centering problems with convex regions.
- **No such structure without convexity.** If $A$ is not convex, $Y$ can have several local maxima. Take $A$ as the union of two disjoint discs and a small spread: each disc center is a local maximum.

## Reductions

- Yield evaluation is the integral of an indicator against a density, so every method of [Monte Carlo integration](/monte-carlo-integration/) applies, and exact evaluation contains polytope volume as a special case.
- Worst-case centering of a ball in a polytope is the Chebyshev center problem, a linear program. Simplicial approximation reduces centering in an unknown convex region to a sequence of these programs.
- With a normal law and linear specifications $g_i(x) = a_i \cdot x - b_i$, the yield of each single specification is $\Phi((b_i - a_i \cdot x_0) / \sqrt{a_i^T \Sigma a_i})$. Maximizing the smallest of these arguments is the worst-case variant for the ellipsoid $T$ defined by $\Sigma$. So in this case statistical centering of one specification at a time and worst-case centering agree.

## Applications

- Analog circuits, such as amplifiers and filters, whose specifications are sensitive to component values and process parameters. Design centering began in this setting in the 1970s.
- Memory cells, where a cell fails when mismatch moves its parameters out of a narrow region, and the yield of an array needs per-cell failure probabilities near $10^{-6}$ or smaller.
- Digital timing, where the parameter variations change path delays and [statistical static timing analysis](/statistical-static-timing-analysis/) gives the distribution of the clock period that the design meets.
- Process windows in manufacturing, such as the range of focus and dose in lithography where the printed features stay within limits.

## References
