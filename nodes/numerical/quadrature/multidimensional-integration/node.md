---
tag: WEF7VH
kind: problem
slug: multidimensional-integration
name: Multidimensional integration
aliases:
- cubature
- numerical cubature
- multiple integration
- high-dimensional integration
area: numerical/quadrature
level: advanced
summary: Integrate functions over regions of R^d.
prereqs: [numerical-integration]
see_also: [cubature-rule, product-quadrature, sparse-grid-quadrature, monte-carlo-integration, quasi-monte-carlo-integration, koksma-hlawka-inequality, curse-of-dimensionality, importance-sampling]
sources:
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Chapter 5, Integration in two or more dimensions (product rules, rules of given degree, Monte Carlo and number-theoretic methods)
  - book: "A. H. Stroud, Approximate Calculation of Multiple Integrals, Prentice-Hall, 1971"
    locator: Chapters 1 to 3 (regions, product formulas, rules of given degree and the lower bound on the number of points)
  - paper: doi:10.1017/S0962492900002701
    title: Ronald Cools, Constructing cubature formulae, the science behind the art, Acta Numerica 6, 1997, 1-54
    locator: Sections 3 and 4 (lower bounds on the number of points and Tchakaloff's theorem)
  - paper: doi:10.1017/S0962492913000044
    title: Josef Dick, Frances Y. Kuo and Ian H. Sloan, High-dimensional integration, the quasi-Monte Carlo way, Acta Numerica 22, 2013, 133-288
    locator: Sections 1 to 3 (the problem in high dimension, Monte Carlo and quasi-Monte Carlo error)
  - paper: "Erich Novak, Deterministic and Stochastic Error Bounds in Numerical Analysis, Lecture Notes in Mathematics 1349, Springer, 1988"
    locator: Chapter 1, Section 1.3 and Chapter 2, Section 2.2 (Bakhvalov's optimal rates for C^r on the cube, deterministic and randomized)
  - paper: doi:10.1145/102782.102783
    title: Martin Dyer, Alan Frieze and Ravi Kannan, A random polynomial-time algorithm for approximating the volume of convex bodies, Journal of the ACM 38(1), 1991, 1-17
    locator: the main theorem, and the deterministic lower bound of Elekes and of Bárány and Füredi cited there
---

Multidimensional integration asks for $I(f) = \int_\Omega f(x)\,w(x)\,dx$ over a region $\Omega \subset \mathbb{R}^s$, from values of $f$ at points of the algorithm's choice. In one or two dimensions it is a mild extension of [numerical integration](/numerical-integration/) on an interval. As the dimension $s$ grows the problem changes character: grids of points become unaffordable, the region's shape matters, and the best methods are random or number-theoretic rather than polynomial. The answer to "which method" depends mostly on $s$ and on what kind of smoothness $f$ has.

## In plain words

You want the total of some quantity spread over a region with several coordinates: the mass of a plate, the probability of an event that depends on ten variables, the price of an option on fifty stocks. You can measure the quantity at any point, and each measurement costs time.

In two or three coordinates you can lay a grid of good points and add up weighted values, much as on a line. With many coordinates a grid is hopeless, because ten points per coordinate in twenty coordinates is more points than any computer can visit. Then you sample: random points give an error that shrinks slowly but does not care how many coordinates there are, and carefully spread points do better when the function is reasonably tame. The shape of the region adds its own trouble, and is usually handled by changing coordinates.

## Definition

**Input.** A region $\Omega \subset \mathbb{R}^s$ with nonempty interior, given either as a standard region (the cube $[0, 1]^s$, a box, the simplex, the ball, all of $\mathbb{R}^s$ with a weight) or by a membership test; a weight $w \ge 0$ on $\Omega$, with $w = 1$ unless stated; an oracle for $f : \Omega \to \mathbb{R}$; and a tolerance $\tau$ or a budget of $N$ evaluations.

**Output.** A number $Q_N(f)$ and, ideally, an estimate of $|I(f) - Q_N(f)|$.

**Cost.** The number $N$ of evaluations of $f$; for rules with stored nodes and weights, also their construction, which for product and sparse rules is $O(N s)$ arithmetic and for Monte Carlo is $N s$ random numbers.

**Methods.** Almost every method returns a cubature sum $Q_N(f) = \sum_{i=1}^{N} w_i f(x_i)$ with $x_i \in \Omega$. A *deterministic* method fixes the $x_i$ and $w_i$, or chooses them adaptively from earlier values. A *randomized* method draws them, and its error is a random variable, measured by its root mean square.

**Accuracy.** A deterministic method is judged by its worst-case error $\sup_{f \in F} |I(f) - Q_N(f)|$ over a class $F$ of integrands, such as the unit ball of $C^r(\overline{\Omega})$, functions of bounded Hardy-Krause variation, or a weighted Sobolev space. A randomized method is judged by $\sup_{f \in F} (\mathbb{E}|I(f) - Q_N(f)|^2)^{1/2}$. A *cubature rule of degree $d$* is one with $Q_N(p) = I(p)$ for every polynomial $p$ in $s$ variables of total degree at most $d$.

## Variants

- **Low dimension, standard region.** $s = 2$ or $3$, on a square, triangle, disc, cube, tetrahedron or ball, with smooth $f$. This is the setting of [cubature rules](/cubature-rule/) and [product quadrature](/product-quadrature/), common in finite element codes.
- **Moderate dimension.** $s$ from about 4 to 20, with smooth or mixed-smooth $f$: [sparse grids](/sparse-grid-quadrature/) and adaptive subdivision.
- **High dimension.** $s$ in the hundreds or thousands, as in finance, statistics and physics: [Monte Carlo](/monte-carlo-integration/) and [quasi-Monte Carlo](/quasi-monte-carlo-integration/), often after a change of variables that makes the early coordinates matter most.
- **Integrals over $\mathbb{R}^s$ with a weight.** Expectations $\mathbb{E}[g(Z)]$ for a Gaussian or other density; Gauss-Hermite products in low dimension, sampling in high dimension.
- **Irregular regions.** $\Omega$ given by inequalities or a membership test. Reduce to a box with an indicator, which makes $f$ discontinuous, or map the region to a standard one.
- **Singular integrands.** Singularities at a point, along an edge or along a surface, as in boundary element methods. These need singularity-adapted coordinates such as the Duffy map.
- **Volume and counting.** $f = 1$ on a convex body given by a membership oracle: computing the volume.

## Examples

**Triangle by a collapsed map.** On $T = \{x, y \ge 0,\ x + y \le 1\}$, the map $(u, v) \mapsto (u, (1 - u) v)$ from $[0, 1]^2$ has Jacobian $1 - u$, so $\int_T x y = \int_0^1\int_0^1 u (1 - u)^2 v\,du\,dv$. The integrand has degree 3 in $u$ and 1 in $v$, so the 2 by 2 product [Gauss-Legendre](/gauss-legendre-quadrature/) rule gives the exact value $1/24$ with 4 evaluations.

**Disc in polar coordinates.** $\int_{x^2 + y^2 \le 1} e^{-(x^2 + y^2)} = \int_0^{2\pi}\int_0^1 e^{-r^2} r\,dr\,d\theta = \pi (1 - e^{-1})$. A product of the periodic [trapezoidal rule](/trapezoidal-rule/) in $\theta$, exact here because the integrand is constant in $\theta$, and Gauss-Legendre in $r$ converges geometrically.

**A smooth separable integrand on the cube.** For $f(x) = e^{x_1 + \cdots + x_s}$ on $[0, 1]^s$, with $I = (e - 1)^s$, a tensor product of $n$-point Gauss-Legendre rules is excellent: with $n = 3$ the relative error is $2.4 \times 10^{-6}$ for $s = 5$ (243 points) and $4.8 \times 10^{-6}$ for $s = 10$ (59049 points). Such integrands favour product rules, since every one-dimensional factor converges geometrically.

**An integrand with kinks.** Sobol's test function $g(x) = \prod_{k=1}^{s} \frac{|4 x_k - 2| + 1}{2}$ on $[0, 1]^s$ has $I(g) = 1$ and a kink across each hyperplane $x_k = \tfrac12$. With a budget of $N$ evaluations, the relative errors of a product Gauss-Legendre rule with $n^s \le N$ points, of Monte Carlo (its exact RMS error $\sigma/\sqrt{N}$, with $\sigma^2 = (13/12)^s - 1$) and of the first $N$ points of the [Halton sequence](/halton-sequence/) are:

| $s$ | $N$ | product rule ($n^s$ points) | Monte Carlo RMS | Halton |
|---|---|---|---|---|
| 2 | $10^3$ | $1.7 \times 10^{-3}$ ($31^2$) | $1.3 \times 10^{-2}$ | $6.6 \times 10^{-4}$ |
| 2 | $10^5$ | $8.2 \times 10^{-6}$ ($316^2$) | $1.3 \times 10^{-3}$ | $1.1 \times 10^{-5}$ |
| 5 | $10^3$ | $3.0 \times 10^{-1}$ ($3^5$) | $2.2 \times 10^{-2}$ | $4.0 \times 10^{-3}$ |
| 5 | $10^5$ | $1.9 \times 10^{-2}$ ($10^5$) | $2.2 \times 10^{-3}$ | $6.4 \times 10^{-5}$ |
| 10 | $10^3$ | $1.0$ ($1^{10}$) | $3.5 \times 10^{-2}$ | $1.8 \times 10^{-2}$ |
| 10 | $10^5$ | $5.1 \times 10^{-1}$ ($3^{10}$) | $3.5 \times 10^{-3}$ | $4.2 \times 10^{-4}$ |

The product rule is competitive in dimension 2 and useless in dimension 10, Monte Carlo is slow but indifferent to $s$, and Halton points beat Monte Carlo throughout at these sizes. (Computed in double precision; the Monte Carlo column is the exact standard deviation of the estimator, not one run.)

## Known algorithms

| method | points for $N$ | error (hypothesis) | kind of result |
|---|---|---|---|
| [product rule](/product-quadrature/) of order $p$ | $n^s$ | $O(N^{-p/s})$ for $f$ with bounded derivatives of order $p$ in each variable | proved |
| [cubature rule](/cubature-rule/) of degree $d$ | fixed | $O(h^{d+1})$ composite, $f \in C^{d+1}$ | proved |
| [sparse grid](/sparse-grid-quadrature/) | $O(n (\log n)^{s-1})$ | $O(N^{-r} (\log N)^{(s-1)(r+1)})$, mixed derivatives of order $r$ bounded | proved, cited |
| [Monte Carlo](/monte-carlo-integration/) | any $N$ | RMS $\sigma(f) N^{-1/2}$, $f \in L^2$ | probabilistic |
| [quasi-Monte Carlo](/quasi-monte-carlo-integration/) (Halton, Sobol) | any $N$ | $V_{HK}(f)\, O((\log N)^s N^{-1})$ | proved (Koksma-Hlawka) |
| lattice rules | $N$ | $O(N^{-\alpha} (\log N)^{\alpha s})$ for periodic $f$ of smoothness $\alpha$ | proved, cited |
| adaptive subdivision | varies | heuristic error estimates | none in general |

Monte Carlo variants that reduce $\sigma$ rather than change the rate include [importance sampling](/importance-sampling/), [stratified sampling](/stratified-sampling/) and [Latin hypercube sampling](/latin-hypercube-sampling/). For densities known only up to a constant, Markov chain methods such as [Metropolis-Hastings](/metropolis-hastings/) produce correlated samples.

## Bounds

- **Lower bound for degree $d$ (proved).** Let $\Omega$ have nonempty interior and $w > 0$ almost everywhere on it. Every cubature rule of degree $d$ has at least $\dim \mathcal{P}_{\lfloor d/2 \rfloor} = \binom{s + \lfloor d/2 \rfloor}{s}$ nodes. *Proof.* If there were fewer nodes, the linear conditions $p(x_i) = 0$ would leave a nonzero polynomial $p$ of degree at most $\lfloor d/2 \rfloor$ vanishing at all of them. Then $p^2$ has degree at most $d$, so $\int_\Omega p^2 w = Q_N(p^2) = \sum_i w_i\, p(x_i)^2 = 0$, impossible for a nonzero polynomial on a set with interior. $\square$ This holds for any real weights.
- **Upper bound for degree $d$ (cited).** Tchakaloff's theorem: for a compact $\Omega$ with positive measure there is a rule of degree $d$ with positive weights, nodes in $\Omega$, and at most $\binom{s + d}{s}$ nodes (Cools 1997, Section 4).
- **Optimal rates for $C^r$ (cited, Bakhvalov 1959).** On the unit ball of $C^r([0, 1]^s)$, the best worst-case error of any deterministic method with $N$ evaluations is of exact order $N^{-r/s}$, and of any randomized method $N^{-r/s - 1/2}$ (Novak 1988). For fixed $r$ this is the *curse of dimensionality*: reaching error $\tau$ deterministically needs about $\tau^{-s/r}$ evaluations.
- **Dimension-free rates need other classes.** Monte Carlo's $N^{-1/2}$ holds for every $f \in L^2$ with a constant $\sigma(f)$ that need not grow with $s$. Quasi-Monte Carlo and lattice rules get rates close to $N^{-1}$ with constants independent of $s$ in weighted spaces in which later coordinates matter less (Dick, Kuo and Sloan 2013, Sections 3 to 5).
- **Volume of convex bodies (cited).** For a convex body given by a membership oracle, every deterministic polynomial-time algorithm has a ratio between its upper and lower volume estimates that grows exponentially in $s$ (Elekes 1986, Bárány and Füredi 1987), while the randomized algorithm of Dyer, Frieze and Kannan (1991) approximates the volume within a factor $1 + \varepsilon$ with high probability in time polynomial in $s$ and $1/\varepsilon$.

## Reductions

- **Fubini.** Over a box, or a region $\{a \le x_1 \le b,\ \phi(x_1) \le x_2 \le \psi(x_1), \ldots\}$, the integral is an iterated one-dimensional integral, and applying a one-dimensional rule at each level is [product quadrature](/product-quadrature/).
- **Change of variables.** A smooth bijection $T : [0, 1]^s \to \Omega$ turns $\int_\Omega f$ into $\int_{[0,1]^s} f(T(u)) |\det T'(u)|\,du$. Polar, spherical and collapsed (Duffy) coordinates are the usual choices; the inverse cumulative distribution function maps a product density on $\mathbb{R}^s$ to the cube, so expectations become cube integrals.
- **Indicator functions.** $\int_\Omega f = \int_B f \cdot \mathbf{1}_\Omega$ over a box $B \supset \Omega$. The integrand becomes discontinuous, which costs polynomial rules their rate but costs Monte Carlo nothing beyond a larger $\sigma$.
- **Expectation.** $I(f) = \mathrm{vol}(\Omega)\, \mathbb{E}[f(X)]$ for $X$ uniform on $\Omega$, which is the basis of Monte Carlo.

## Applications

- **Finance.** Option prices as expectations over Brownian paths, with $s$ equal to the number of time steps; quasi-Monte Carlo with Sobol points after a Brownian bridge reordering is standard.
- **Statistics.** Marginal likelihoods, posterior expectations and multivariate normal probabilities.
- **Physics and chemistry.** Feynman diagram integrals, partition functions, and electron repulsion integrals over pairs of points in $\mathbb{R}^3$, which is $s = 6$.
- **Finite and boundary elements.** Element integrals over triangles, tetrahedra and their products, with singular kernels in boundary elements.
- **Computer graphics.** The rendering equation integrates light over directions, pixel area, lens and time, and is solved with Monte Carlo and quasi-Monte Carlo sampling.
- **Uncertainty quantification.** Means and variances of model outputs with uncertain inputs, by sparse grids in moderate dimension and sampling beyond.

## References
