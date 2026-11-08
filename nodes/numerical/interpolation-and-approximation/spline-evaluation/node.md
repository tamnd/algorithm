---
tag: J5PHVM
kind: problem
slug: spline-evaluation
name: Spline evaluation
aliases:
- Evaluating a B-spline series
- Spline function evaluation
area: numerical/interpolation-and-approximation
level: advanced
summary: Evaluate a spline, or its derivatives, at a given point efficiently. The work is a knot interval search plus O(k^2) stable convex combinations, or O(k) after converting to piecewise polynomial form.
prereqs: [b-spline]
see_also: [de-boor-algorithm, horner-rule, cubic-spline-interpolation, smoothing-spline, bernstein-polynomials, tensor-product-interpolation, binary-search, piecewise-linear-interpolation]
sources:
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter VII, A representation for piecewise polynomial functions (pp-form and PPVALU); Chapter X, The stable evaluation of B-splines and splines (BSPLVB and BVALUE)
  - paper: "Carl de Boor, On calculating with B-splines, Journal of Approximation Theory 6 (1972) 50-62"
    locator: the recurrence for B-splines and the evaluation algorithm for a B-spline series
  - paper: "Maurice G. Cox, The numerical evaluation of B-splines, IMA Journal of Applied Mathematics 10 (1972) 134-149"
    locator: the stable recurrence and its rounding error analysis
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Chapter 2, B-spline basis functions (span search and the basis function algorithms), and Chapter 3, B-spline curves and surfaces (curve point and derivative evaluation)
  - book: isbn:9780521880688
    title: William H. Press, Saul A. Teukolsky, William T. Vetterling and Brian P. Flannery, Numerical Recipes, The Art of Scientific Computing, third edition, Cambridge University Press, 2007
    locator: Section 3.1, searching an ordered table (bisection, and hunting for correlated queries)
---

Spline evaluation is the task of computing $s(x)$, and often $s'(x)$, $s''(x)$ or $\int s$, for a spline $s$ given in some representation, at one point or at many. It sounds trivial, but the representation decides the cost and the accuracy: the B-spline form is evaluated stably by de Boor's algorithm in $O(k^2)$ operations after locating the knot interval, the piecewise polynomial form by Horner's rule in $O(k)$, and the truncated power form, though simple to write down, loses digits quickly as the number of knots grows.

## In plain words

A spline is a chain of polynomial pieces joined smoothly. To find its value at a point you first find which piece the point lies in, then evaluate that piece. Finding the piece is a search in a sorted list of joints, done by halving the list, or, when the points come in order, by stepping from the previous position.

Evaluating the piece is where representations differ. Some forms take repeated averages of nearby coefficients, which is very safe against rounding. Others store each piece as an ordinary polynomial, which is faster. One tempting form, a single formula for the whole curve, adds and subtracts huge numbers and should be avoided.

## Definition

Notation on the interpolation pages: a spline $s$ has degree $k$ (order $k + 1$) and nondecreasing knots $t_0 \le t_1 \le \cdots \le t_{n+k}$; $B_{j,k}$ are the B-splines of degree $k$ on these knots, and $s = \sum_{j=0}^{n-1} c_j B_{j,k}$ on $[t_k, t_n]$; $m$ is the number of distinct knot intervals.

**Problem.** Given a representation of $s$ and a point $x$ (or points $x_1, \ldots, x_M$), compute $s^{(r)}(x)$ for $r = 0, 1, \ldots$ up to some $r \le k$.

**Representations.**

- **B-spline form:** knots $t$ and coefficients $c$. Each $x \in [t_\mu, t_{\mu+1})$ lies in the support of only $B_{\mu-k}, \ldots, B_\mu$, so $s(x) = \sum_{j=\mu-k}^{\mu} c_j B_{j,k}(x)$.
- **Piecewise polynomial (pp) form:** breakpoints $\xi_1 < \cdots < \xi_{m+1}$ and local coefficients, $s(x) = \sum_{r=0}^{k} a_{i,r} (x - \xi_i)^r$ on $[\xi_i, \xi_{i+1})$.
- **Hermite form:** values and derivatives at the breakpoints ([cubic Hermite splines](/cubic-hermite-spline/)).
- **Truncated power form:** $s(x) = \sum_{r=0}^{k} b_r x^r + \sum_i a_i (x - \xi_i)_+^k$.

## Variants

- **One point or many.** Many sorted points allow a linear-time sweep instead of a search per point.
- **Derivatives and integrals.** The derivative of a B-spline series is a B-spline series of degree $k - 1$ with coefficients $k (c_j - c_{j-1}) / (t_{j+k} - t_j)$; the integral is a series of degree $k + 1$ with partial sums of scaled coefficients.
- **Uniform knots.** On equally spaced knots, each interval uses the same basis polynomials; evaluation on a fine regular grid is a short convolution (four taps for cubics), as in image resampling.
- **Curves, surfaces and NURBS.** Vector coefficients (control points), tensor-product surfaces ([tensor-product interpolation](/tensor-product-interpolation/)), and rational splines evaluated in homogeneous coordinates.
- **Interval or exact arithmetic,** for robust geometric computations.

## Examples

**De Boor's algorithm on a small cubic.** For $k = 1$ (a broken line) with knots $0, 0, 1, 2, 2$ and coefficients $c = (1, 3, 2)$, the point $x = 1.5$ lies in $[t_2, t_3) = [1, 2)$; one convex combination gives $s(1.5) = \tfrac12 c_1 + \tfrac12 c_2 = 2.5$, the piecewise linear interpolant of the values $1, 3, 2$ at $0, 1, 2$. For cubics, three levels of such combinations, $3 + 2 + 1 = 6$ in all, produce $s(x)$; see [de Boor's algorithm](/de-boor-algorithm/).

**Accuracy of the representations.** Take a clamped cubic spline on $[0, 1]$ with $m$ equal intervals and B-spline coefficients $c_j = (-1)^j$, so $|s| \le 1$. Convert it exactly to truncated power form and evaluate both forms in double precision at about 140 points, against exact rational values:

| $m$ | de Boor's algorithm | truncated power form | largest truncated power coefficient |
|---|---|---|---|
| 10 | $1.7 \times 10^{-15}$ | $1.0 \times 10^{-12}$ | $5.3 \times 10^{3}$ |
| 40 | $2.7 \times 10^{-15}$ | $7.8 \times 10^{-11}$ | $3.4 \times 10^{5}$ |
| 160 | $8.3 \times 10^{-15}$ | $4.8 \times 10^{-9}$ | $2.2 \times 10^{7}$ |

The truncated power coefficients grow like $m^3$ and the evaluation cancels them, while de Boor's algorithm takes only convex combinations and stays at rounding level (the small growth comes from rounding the knots $j/m$).

## Known algorithms

- **Interval search.** Binary search for $\mu$ with $t_\mu \le x < t_{\mu+1}$ costs $\lceil \log_2 m \rceil$ comparisons ([binary search](/binary-search/)); for correlated queries, "hunting" from the previous interval costs $O(\log \delta)$ for a jump of $\delta$ intervals, and $O(1)$ amortized for sorted points.
- **[De Boor's algorithm](/de-boor-algorithm/).** $k$ levels of convex combinations of the $k + 1$ active coefficients: $\tfrac{k(k+1)}{2}$ combinations, about $k(k+1)$ multiplications and $k(k+1)/2$ divisions. Derivatives come from differenced coefficients or by stopping the recurrence early.
- **B-spline basis values (Cox-de Boor recurrence).** Compute the $k + 1$ nonzero $B_{j,k}(x)$ in $O(k^2)$ and take the dot product with the coefficients; the basis values are needed anyway for fitting and for Jacobians, and all derivatives come together in $O(k^2)$ more.
- **Conversion to pp-form.** Once, in $O(m k^2)$ operations, then each point costs a search plus $k$ multiply-adds by [Horner's rule](/horner-rule/); the method of choice when a spline is evaluated very many times.
- **Uniform B-splines on regular grids.** Precompute the basis weights for the fixed fractional offsets and apply them as a filter.
- **Bézier extraction and subdivision.** Insert knots to multiplicity $k$ to get Bernstein pieces, then use [Bernstein polynomial](/bernstein-polynomials/) evaluation (de Casteljau) on each piece; standard in graphics.

## Bounds

- **Search lower bound.** In the comparison model, locating $x$ among $m$ intervals needs $\lceil \log_2 m \rceil$ comparisons in the worst case for an arbitrary query; for $M$ sorted queries, a merge needs $O(M + m)$ in total.
- **Local work.** Any method that uses the B-spline coefficients directly must read the $k + 1$ active ones; de Boor's $O(k^2)$ is optimal up to the constant for fixed $k$ without preprocessing, and $O(k)$ is achievable with pp-form preprocessing.
- **Rounding error (proved).** For $x$ inside the basic interval, de Boor's algorithm computes $s(x)$ with absolute error at most about $c_k\, u \sum_j |c_j| B_{j,k}(x) \le c_k\, u \max |c_j|$ with a modest constant $c_k$ depending only on $k$ (Cox 1972), because every step is a convex combination. Horner's rule on the local pp-form has error bounded by $u$ times a similar sum with $|a_{i,r}| h^r$; it is reliable when the local coefficients are not much larger than the values.
- **Condition of the B-spline basis.** The B-spline basis is well conditioned: $\max|c_j| \le D_k \|s\|_\infty$ with a constant depending only on $k$, not on the knots (de Boor), which is why the B-spline form is the stable reference representation.

## Reductions

- **To polynomial evaluation.** After the interval search, each piece is a polynomial; the pp-form reduces evaluation to Horner's rule.
- **To knot insertion.** De Boor's algorithm is $k$-fold insertion of the knot $x$ (Boehm's algorithm), which leaves a single coefficient equal to $s(x)$; blossoming makes this precise.
- **To searching.** The interval search is predecessor search in a sorted array.
- **From interpolation.** Spline interpolation and smoothing produce a representation that must then be evaluated; e.g. [cubic spline interpolation](/cubic-spline-interpolation/) delivers values and second derivatives at the knots, a form evaluated directly by the cubic formula on each interval.

## Applications

- Plotting and sampling of curves and surfaces in CAD, graphics and font rendering (NURBS, B-spline curves).
- Evaluating fitted and smoothed functions in data analysis and regression ([smoothing splines](/smoothing-spline/), P-splines).
- Lookup tables in simulation codes: equations of state, interpolated tabulated data, spline-based special function approximations.
- Collocation and Galerkin methods for differential equations with spline bases, and isogeometric analysis, which evaluate splines and derivatives at quadrature points.
- Image and signal resampling with cubic B-splines.

## References
