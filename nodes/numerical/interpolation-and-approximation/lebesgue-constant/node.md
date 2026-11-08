---
tag: GWREAK
kind: concept
slug: lebesgue-constant
name: Lebesgue constant
aliases:
- Lebesgue function
- Lebesgue constant of interpolation
- norm of the interpolation operator
area: numerical/interpolation-and-approximation
level: advanced
summary: Λ_n = max over x of Σ|ℓ_j(x)|, the norm of interpolation as a map from data to polynomial. It bounds both the distance to the best approximation and the amplification of data errors.
prereqs: [lagrange-interpolation, minimax-approximation]
see_also: [chebyshev-nodes, runge-phenomenon, chebyshev-interpolation, barycentric-interpolation, condition-number, polynomial-interpolation-error-theorem, chebyshev-equioscillation-theorem, cubic-spline-interpolation]
sources:
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 15, Lebesgue constants (Theorem 15.1, the Lebesgue inequality; Theorem 15.2, bounds for Chebyshev and equispaced points)
  - book: isbn:9780521295147
    title: M. J. D. Powell, Approximation Theory and Methods, Cambridge University Press, 1981
    locator: Chapter 4 (the norm of the Lagrange interpolation operator) and Chapter 17 (the uniform boundedness theorem and lower bounds for projections)
  - book: isbn:9780821813744
    title: E. W. Cheney, Introduction to Approximation Theory, second edition, AMS Chelsea, 1998
    locator: Chapter 6, Approximating operators (projections, their norms and the Lebesgue inequality)
  - paper: "L. Brutman, Lebesgue functions and Lebesgue constants in polynomial interpolation, Journal of Inequalities and Applications 1 (1997) 321-334"
    locator: survey of asymptotics for equispaced, Chebyshev and optimal nodes
  - paper: "A. Schönhage, Fehlerfortpflanzung bei Interpolation, Numerische Mathematik 3 (1961) 62-71"
    locator: the asymptotic formula for equispaced nodes
  - paper: "P. Erdős, Problems and results on the theory of interpolation II, Acta Mathematica Academiae Scientiarum Hungaricae 12 (1961) 235-244"
    locator: the lower bound (2/π) log n - C for all node sets
  - paper: doi:10.1137/S0036144502417715
    title: "Jean-Paul Berrut and Lloyd N. Trefethen, Barycentric Lagrange interpolation, SIAM Review 46(3) (2004) 501-517"
    locator: Section 4 and Section 5, Lebesgue constants and the role of Λ_n in the stability of barycentric evaluation
---

The Lebesgue constant $\Lambda_n$ of a set of interpolation nodes measures how much polynomial interpolation can amplify. It is the maximum over the interval of the Lebesgue function $\lambda_n(x) = \sum_j|\ell_j(x)|$, the sum of the absolute values of the Lagrange basis polynomials. Equivalently, it is the norm of the interpolation operator in the maximum norm. It enters two basic inequalities: the interpolant is within $1 + \Lambda_n$ times the best possible error, and data errors of size $\epsilon$ can produce interpolant errors of size $\Lambda_n\epsilon$. For Chebyshev points $\Lambda_n$ grows like $\frac2\pi\log n$, which is nearly optimal. For equispaced points it grows like $2^n/(n\log n)$, which explains the [Runge phenomenon](/runge-phenomenon/).

## In plain words

When you draw a polynomial through a set of points, each data value pulls on the curve everywhere, not only at its own point. The Lebesgue function adds up, at each place, how strongly all the data values together can pull on the curve there. Its largest value is the Lebesgue constant. If it is small, the curve behaves well: errors in the data stay small, and the curve is nearly as good as any polynomial could be. If it is large, a tiny wobble in one data value can make the curve swing wildly somewhere. Where you put the points decides how big this number is. Points crowded toward the ends of the interval keep it small. Evenly spaced points make it explode as you add more of them.

## The idea

Notation on the interpolation and approximation pages: $f$ is continuous on $[a, b]$, usually $[-1, 1]$; the nodes are distinct $x_0, \ldots, x_n$ with data $y_i = f(x_i)$; $\ell_j(x) = \prod_{i \ne j}(x - x_i)/(x_j - x_i)$ are the [Lagrange](/lagrange-interpolation/) basis polynomials; $p_n = I_nf = \sum_jf(x_j)\ell_j$ is the interpolant of degree at most $n$; $E_n(f)$ is the best approximation error in the maximum norm $\|\cdot\|$.

**Definition.** The Lebesgue function and constant of the nodes are
$$\lambda_n(x) = \sum_{j=0}^n|\ell_j(x)|, \qquad \Lambda_n = \max_{a \le x \le b}\lambda_n(x).$$
Since $\sum_j\ell_j \equiv 1$, $\lambda_n \ge 1$ everywhere, with equality at the nodes, so $\Lambda_n \ge 1$.

**$\Lambda_n$ is the operator norm (proved).** $I_n$ is a linear map from $C[a, b]$ to the polynomials of degree at most $n$, and $\|I_n\| = \sup_{\|f\| \le 1}\|I_nf\| = \Lambda_n$. The upper bound is $|I_nf(x)| \le \sum|f(x_j)||\ell_j(x)| \le \|f\|\lambda_n(x)$. For the lower bound, take $x^*$ where $\lambda_n$ is largest and a continuous $f$ with $\|f\| = 1$ and $f(x_j) = \operatorname{sign}\ell_j(x^*)$, for example piecewise linear.

**The Lebesgue inequality (proved).** For every continuous $f$,
$$\|f - p_n\| \le (1 + \Lambda_n)\,E_n(f).$$
*Proof.* Let $p^*$ be the best approximation. $I_np^* = p^*$ by [uniqueness](/interpolating-polynomial-uniqueness/), so $f - I_nf = (f - p^*) - I_n(f - p^*)$, and $\|f - I_nf\| \le (1 + \Lambda_n)\|f - p^*\|$. $\square$ The same argument works for any linear projection, with $\Lambda$ replaced by the norm of the projection.

**Conditioning (proved).** If the data are perturbed to $\tilde y_j = y_j + \epsilon_j$, the interpolant changes by $\sum\epsilon_j\ell_j$, and
$$\|p_n - \tilde p_n\| \le \Lambda_n\max_j|\epsilon_j|,$$
with equality for the worst choice of signs. So $\Lambda_n$ is the absolute condition number of interpolation from values to function. It concerns the problem, not any algorithm: rounding errors in $f(x_j)$ of size $u\|f\|$ are amplified by $\Lambda_n$ in any method. The barycentric formula achieves this bound up to a modest factor (Higham 2004), while the monomial basis loses far more through the [Vandermonde](/vandermonde-matrix/) condition number.

**Growth for particular nodes (proved unless marked).**

| Nodes on $[-1, 1]$ | $\Lambda_n$ | Source |
|---|---|---|
| any nodes | $\ge \frac2\pi\log(n + 1) + 0.5212$ | Erdős (1961) for the form, Brutman (1978) for the constant |
| Chebyshev points $\cos(j\pi/n)$ | $\le \frac2\pi\log(n + 1) + 1$; $\sim \frac2\pi\log n$ | ATAP Theorem 15.2 |
| Chebyshev zeros $\cos\frac{(2j+1)\pi}{2n+2}$ | $\frac2\pi\log(n + 1) + 0.9625 + o(1)$ | Ehlich and Zeller (1966), Rivlin |
| Legendre (Gauss) points | $O(\sqrt n)$ | Szegő |
| equispaced points | $\sim \dfrac{2^{n+1}}{e\,n\log n}$ | Turetskii (1940), Schönhage (1961) |

**Optimal nodes (proved).** Bernstein and Erdős conjectured that the nodes minimizing $\Lambda_n$ are those for which all the local maxima of $\lambda_n$ between nodes are equal. Kilgore (1978) and de Boor and Pinkus (1978) proved it. The optimal constant is only slightly below that of the Chebyshev zeros: asymptotically it is $\frac2\pi(\log n + \gamma + \log\frac4\pi) + o(1) = \frac2\pi\log n + 0.5212 + o(1)$ (Vértesi 1990), against $\frac2\pi(\log n + \gamma + \log\frac8\pi) = \frac2\pi\log n + 0.9625$ for the zeros, a gap of $\frac2\pi\log2 = 0.441$.

**Unboundedness and Faber's theorem (proved).** Since $\Lambda_n \to \infty$ for every node scheme, the uniform boundedness principle gives, for each scheme, a continuous $f$ whose interpolants are unbounded (Faber 1914 for the original form). Interpolation cannot converge for all continuous functions. With Chebyshev points, the logarithmic growth is so slow that convergence holds whenever $E_n(f)\log n \to 0$, for example for every Lipschitz or Dini-Lipschitz function.

**The same idea elsewhere.** Any linear approximation scheme has a Lebesgue constant, its operator norm: for truncated Fourier series it is $\frac{4}{\pi^2}\log n + O(1)$, for Chebyshev projections it is the same, for piecewise linear interpolation it is 1, and for cubic spline interpolation on uniform or quasi-uniform meshes it is bounded independently of $n$. For multivariate and scattered-data interpolation, the Lebesgue constant measures the quality of a point set, for example of Fekete points.

## Examples

**Computed Lebesgue constants** (the maximum of $\lambda_n$ located by search on each subinterval, double precision):

| $n$ | 5 | 10 | 20 | 40 | 80 |
|---|---|---|---|---|---|
| equispaced | 3.106 | 29.90 | 1.099e4 | 4.692e9 | |
| asymptotic $2^{n+1}/(en\log n)$ | 2.93 | 32.7 | 1.29e4 | 5.48e9 | |
| Chebyshev zeros | 2.104 | 2.489 | 2.901 | 3.327 | 3.760 |
| Chebyshev points | 1.989 | 2.421 | 2.868 | 3.310 | 3.752 |
| upper bound $\frac2\pi\log(n + 1) + 1$ | 2.141 | 2.527 | 2.938 | 3.364 | 3.798 |
| lower bound $\frac2\pi\log(n + 1) + 0.5212$ | 1.662 | 2.048 | 2.459 | 2.885 | 3.319 |

For equispaced points the Lebesgue function is near 1 in the middle of the interval and huge near the ends, which is where the Runge oscillations appear. For Chebyshev points its local maxima are nearly equal across the interval.

**What the numbers mean.** With 41 equispaced points, rounding errors of size $10^{-16}$ in the data can change the interpolant by up to about $4.7 \times 10^{-7}$, and data with errors of $10^{-10}$ give an interpolant that can be wrong by about $0.47$. With 81 Chebyshev points, errors in the data are amplified by at most $3.75$, and the interpolant is within a factor $4.75$ of the best polynomial approximation of degree 80, whatever $f$ is.

**Two points.** For $n = 1$ on $[-1, 1]$ with nodes $\pm1$, $\ell_0 = \frac{1 - x}2$ and $\ell_1 = \frac{1 + x}2$ are nonnegative, so $\lambda_1 \equiv 1$ and $\Lambda_1 = 1$. The inequality $\|f - p_1\| \le 2E_1(f)$ is attained for $e^x$ (see the [equioscillation theorem](/chebyshev-equioscillation-theorem/)). With nodes $\pm\frac12$ instead, $\lambda_1(\pm1) = 2$ and $\Lambda_1 = 2$: moving nodes inward makes extrapolation to the ends worse.

## Where it is used

- **Choosing nodes.** Small $\Lambda_n$ is the main reason to use [Chebyshev nodes](/chebyshev-nodes/) and [Chebyshev interpolation](/chebyshev-interpolation/), and to avoid high-degree interpolation on equispaced grids.
- **Explaining the Runge phenomenon.** The exponential growth of $\Lambda_n$ for equispaced nodes, together with the location of the large values of $\lambda_n$ near the ends, accounts for both the divergence for some analytic $f$ and the extreme sensitivity to noise.
- **Stability analysis.** The forward error of barycentric interpolation is bounded by a multiple of $u\Lambda_n$ times the data (Higham 2004), which is the best one can expect from a problem with condition number $\Lambda_n$.
- **Near-best approximation.** The Lebesgue inequality converts bounds on $E_n(f)$, such as those of Jackson's theorem, into bounds for interpolation, quadrature rules and spectral methods.
- **Projection theory.** The Kharshiladze-Lozinski theorem says that every bounded projection of the continuous periodic functions onto trigonometric polynomials of degree $n$ has norm at least that of the Fourier projection, about $\frac4{\pi^2}\log n$; a similar $\log n$ lower bound holds for algebraic polynomials on an interval. So no linear method is near-best with a bounded constant.
- **Multivariate and scattered data.** Lebesgue constants measure the quality of point sets on triangles, spheres and other domains (Fekete and Leja points), and of radial basis function and sparse grid interpolation.

## References
