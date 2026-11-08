---
tag: 8XFA0K
kind: concept
slug: kolmogorov-width
name: Kolmogorov n-width
aliases:
- Kolmogorov width
- n-width
- Kolmogorov diameter
area: numerical/interpolation-and-approximation
level: research
summary: d_n(K) is the smallest possible worst-case error over a class K when approximating from the best n-dimensional linear subspace. It sets the limit for every linear approximation method.
prereqs: [approximation-theory, singular-value-decomposition]
see_also: [jackson-theorem, function-approximation, least-squares-approximation, chebyshev-series, compressed-sensing, principal-component-analysis, curse-of-dimensionality, lebesgue-constant]
sources:
  - paper: doi:10.2307/1968691
    title: "A. Kolmogoroff, Über die beste Annäherung von Funktionen einer gegebenen Funktionenklasse, Annals of Mathematics 37(1) (1936) 107-110"
    locator: the definition of the width and its exact value for periodic Sobolev classes in L2
  - book: isbn:9783642698965
    title: Allan Pinkus, n-Widths in Approximation Theory, Springer, 1985
    locator: Chapter I (definitions and basic properties), Chapter IV (n-widths of compact operators in Hilbert space via singular values) and Chapter VII (Sobolev classes)
  - book: isbn:9780521295147
    title: M. J. D. Powell, Approximation Theory and Methods, Cambridge University Press, 1981
    locator: Chapter 1 (best approximation from subspaces), as background for comparing subspaces
  - paper: "B. S. Kashin, Diameters of some finite-dimensional sets and classes of smooth functions, Mathematics of the USSR Izvestiya 11(2) (1977) 317-333"
    locator: the widths of octahedra and the gap between Kolmogorov and linear widths
  - paper: doi:10.1137/100795772
    title: "Peter Binev, Albert Cohen, Wolfgang Dahmen, Ronald DeVore, Guergana Petrova and Przemyslaw Wojtaszczyk, Convergence rates for greedy algorithms in reduced basis methods, SIAM Journal on Mathematical Analysis 43(3) (2011) 1457-1472"
    locator: greedy reduced bases achieve the polynomial decay rate of the Kolmogorov width
  - paper: "Ronald DeVore, Guergana Petrova and Przemyslaw Wojtaszczyk, Greedy algorithms for reduced bases in Banach spaces, Constructive Approximation 37 (2013) 455-466"
    locator: comparison of greedy errors with n-widths, polynomial and exponential cases
---

The Kolmogorov $n$-width $d_n(K)$ of a set $K$ of functions measures how well $K$ can be approximated by any linear space of dimension $n$. For each candidate space, take the worst approximation error over $K$. The width is the smallest such worst error over all candidate spaces. It is a property of the class, not of a method. No method that represents its answers in some $n$-dimensional linear space, whether polynomials, splines, Fourier modes or a reduced basis, can do better on all of $K$. Kolmogorov introduced it in 1936 and computed it for periodic Sobolev balls, where trigonometric polynomials are optimal. For an ellipsoid in a Hilbert space it equals the $(n+1)$-th singular value, and the leading singular vectors span an optimal space. Widths explain when polynomial and spectral methods are optimal, when the curse of dimensionality is unavoidable, and when reduced basis methods can work.

## In plain words

Suppose you must describe every function in some family using only $n$ building blocks, mixed in any amounts, and you get to choose the blocks in advance. However well you choose, some function in the family will be described worst. The Kolmogorov width is the error for that worst function when the blocks are chosen as well as possible. If the width shrinks fast as $n$ grows, a few well-chosen blocks capture the whole family. If it shrinks slowly, no fixed set of blocks can, and you need adaptive or nonlinear methods instead.

## The idea

Notation on the interpolation and approximation pages: $f$ is a function in a normed space $X$ (usually $C[a, b]$ or $L^2$), $\|\cdot\|$ its norm, and $E_n(f)$ the best approximation error from polynomials of degree at most $n$.

**Definition.** For a subset $K$ of a normed space $X$ and $n \ge 0$,
$$d_n(K, X) = \inf_{\dim X_n \le n}\ \sup_{f \in K}\ \inf_{g \in X_n}\|f - g\|,$$
the infimum taken over all linear subspaces $X_n$ of dimension at most $n$. A subspace attaining the infimum is called optimal. Always $d_0(K) = \sup_K\|f\|$, since the only subspace of dimension $0$ is $\{0\}$, and $d_n$ is nonincreasing in $n$. For bounded $K$, $d_n(K) \to 0$ if and only if $K$ is totally bounded (relatively compact when $X$ is complete).

**What the width compares.** For polynomials of degree $n - 1$ (dimension $n$), $\sup_{f \in K}E_{n-1}(f)$ is at least $d_n(K)$. When the two have the same order, polynomials are an optimal choice for $K$, and theorems like [Jackson's](/jackson-theorem/) are best possible among all linear methods. When the width is much smaller, a better basis exists.

**Hilbert space and the SVD (proved).** Let $A$ be a compact linear operator between Hilbert spaces with singular values $\sigma_1 \ge \sigma_2 \ge \cdots$ and left singular vectors $u_1, u_2, \ldots$, and let $K = \{Ax : \|x\| \le 1\}$, an ellipsoid. Then
$$d_n(K) = \sigma_{n+1},$$
and $\operatorname{span}(u_1, \ldots, u_n)$ is optimal. For matrices it is the spectral-norm form of the Eckart-Young (Schmidt-Mirsky) theorem, and the optimal space is the one used by [principal component analysis](/principal-component-analysis/) and proper orthogonal decomposition. For a finite set of snapshots the picture differs: the SVD minimizes the sum of squared errors, which is not the same as the worst-case error that defines $d_n$.

**Known widths (proved, up to constants where marked $\asymp$).**

| Class $K$ | Space | $d_n(K)$ | Optimal or near-optimal subspace |
|---|---|---|---|
| $2\pi$-periodic $f$ with $\lVert f^{(r)}\rVert_2 \le 1$ | $L^2$ | $d_{2k-1} = d_{2k} = k^{-r}$, $k \ge 1$ | trigonometric polynomials of degree $< k$, dimension $2k - 1$ (Kolmogorov 1936) |
| periodic $f$ with $\lVert f^{(r)}\rVert_\infty \le 1$ | $C$ | $d_{2k-1} = d_{2k} = K_r k^{-r}$, $K_r$ the Favard constant | trigonometric polynomials (Tikhomirov 1960) |
| Hölder ball $\operatorname{Lip}\alpha$ on $[0, 1]^d$ | $C$ | $\asymp n^{-\alpha/d}$ | piecewise constants or splines on a uniform mesh |
| Sobolev ball $W_2^r$ on $[0, 1]$, $r > 1/2$ | $L^q$, $2 < q < \infty$ | $\asymp n^{-r}$ | exists (Kashin 1977), but every linear operator of rank $n$ has worst error of the larger order $n^{-r + 1/2 - 1/q}$ |
| $f$ analytic and $\lvert f\rvert \le 1$ in the Bernstein ellipse $E_\rho$ | $C[-1, 1]$ | $\asymp \rho^{-n}$ | Chebyshev polynomials of degree $< n$ |

The third row is the curse of dimensionality for linear methods: halving the error on a Hölder class in $d$ dimensions needs $2^{d/\alpha}$ times as many parameters, whatever subspace is used. The fourth row is Kashin's discovery: for $q > 2$ good subspaces exist, but no linear projection onto them achieves their quality, so the Kolmogorov width can be of strictly smaller order than the linear width.

**Related widths.**

- *Linear width* $\delta_n$: the infimum over linear operators of rank $n$ of the worst error. $\delta_n \ge d_n$, with equality in Hilbert space.
- *Gelfand width* $d^n$: the infimum over subspaces of codimension $n$ of the largest norm of $K$ on them. It measures recovery from $n$ linear measurements and is the theoretical basis of [compressed sensing](/compressed-sensing/): the Gelfand widths of the $\ell_1$ ball (Kashin 1977; Garnaev and Gluskin 1984) in $\ell_2^N$ are of order $\min\{1, \sqrt{\log(eN/n)/n}\}$.
- *Entropy numbers*: the smallest radius for which $2^n$ balls cover $K$. They measure the information content of $K$ and give lower bounds for nonlinear methods with stable parameter selection.
- *Nonlinear and manifold widths* (DeVore, Howard and Micchelli 1989): approximation from nonlinear families with continuous parameter selection, which is the setting of free-knot splines, rational functions and neural networks.

## Examples

**An exact width: integrals of $L^2$ functions.** Let $K = \{g : g(0) = 0,\ \|g'\|_{L^2(0,1)} \le 1\}$, the image of the unit ball under $(Vf)(x) = \int_0^xf$. The operator $VV^*$ has eigenfunctions $\sin((k - \frac12)\pi x)$ with eigenvalues $1/((k - \frac12)\pi)^2$, so in $L^2(0, 1)$
$$d_n(K) = \frac{1}{(n + \frac12)\pi},$$
attained by $\operatorname{span}\{\sin((k - \frac12)\pi x) : k = 1, \ldots, n\}$. Polynomials of degree $n - 1$, the same dimension, give a worst-case error (largest singular value of $(I - P_n)V$, computed on a 400-point grid by power iteration):

| $n$ | 1 | 2 | 3 | 5 | 8 | 10 |
|---|---|---|---|---|---|---|
| $d_n(K)$ | 0.2122 | 0.1273 | 0.0909 | 0.0579 | 0.0374 | 0.0303 |
| polynomials of degree $n - 1$ (observed) | 0.3183 | 0.1592 | 0.1113 | 0.0715 | 0.0475 | 0.0391 |

Polynomials are within a factor 1.5 of optimal and have the same order $1/n$. For $n = 1$ the optimal one-dimensional space is $\operatorname{span}\{\sin(\pi x/2)\}$, not the constants, because every $g \in K$ vanishes at $0$.

**Analytic versus finitely smooth.** For functions analytic in a Bernstein ellipse $E_\rho$, the width decays like $\rho^{-n}$, and Chebyshev truncation achieves it up to a constant ([Chebyshev series](/chebyshev-series/)). For a Sobolev class of smoothness $r$, the width decays only like $n^{-r}$. This is why spectral methods are exponentially accurate for analytic data and only algebraically accurate otherwise, and no choice of basis changes that.

**Reduced basis methods.** In a parametric PDE $\mathcal{L}(\mu)u = f$, the solution set $\mathcal{M} = \{u(\mu)\}$ is the class $K$. If $d_n(\mathcal{M})$ decays fast, a few solutions at chosen parameters span a space that approximates every solution. The weak greedy algorithm, which adds the worst-approximated snapshot at each step, achieves the same polynomial rate: if $d_n \le Cn^{-\alpha}$, its error is at most $C'n^{-\alpha}$ (Binev, Cohen, Dahmen, DeVore, Petrova and Wojtaszczyk, 2011, proved), and an exponential rate $e^{-cn^\beta}$ becomes $e^{-c'n^\beta}$ (DeVore, Petrova and Wojtaszczyk 2013, proved). For elliptic problems with smooth parameter dependence the width decays exponentially (proved under analyticity assumptions). For a transported discontinuity $u(x, \mu) = H(x - \mu)$, the width in $L^2$ decays only like $n^{-1/2}$ (proved; Ohlberger and Rave 2016), which is why linear model reduction struggles with advection-dominated problems.

## Where it is used

- **Optimality of numerical methods.** Comparing the error of polynomials, splines, wavelets or finite elements with $d_n$ shows whether a method is optimal for a class. Spline and finite element spaces on uniform meshes have the optimal order for many Sobolev classes, though not in Kashin's cases with $q > 2$.
- **Lower bounds.** Widths prove that some error rates are impossible for any linear method, as in the curse of dimensionality for Hölder and Sobolev classes in high dimension.
- **Model order reduction.** Reduced basis methods and proper orthogonal decomposition are justified by fast width decay of the solution set, and greedy constructions are certified against $d_n$.
- **Compressed sensing and information-based complexity.** Gelfand widths give the optimal recovery error from $n$ linear measurements, and Kashin's results underpin sparse recovery guarantees.
- **Nonlinear approximation and neural networks.** Comparing linear widths with nonlinear widths and entropy numbers shows when adaptivity, free knots or neural networks can beat every fixed basis.
- **Data compression.** For an ellipsoidal class, the optimal basis is the singular basis, the principle behind the Karhunen-Loève transform.

## References
