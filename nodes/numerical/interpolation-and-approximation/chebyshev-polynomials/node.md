---
tag: 4QGYWN
kind: definition
slug: chebyshev-polynomials
name: Chebyshev polynomials
aliases:
- Chebyshev polynomials of the first kind
- Tchebycheff polynomials
- T_k
area: numerical/interpolation-and-approximation
level: core
summary: The polynomials T_k with T_k(cos t) = cos(kt), from T_0 = 1, T_1 = x and T_(k+1) = 2x T_k - T_(k-1). Orthogonal for the weight 1/sqrt(1 - x^2), and the monic 2^(1-k) T_k has least maximum on [-1, 1].
prereqs: [polynomial]
see_also: [chebyshev-nodes, chebyshev-series, chebyshev-interpolation, chebyshev-economization, chebyshev-equioscillation-theorem, orthogonal-polynomials, chebyshev-iteration, legendre-polynomials]
sources:
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 3, Chebyshev polynomials and series (the definition through z = exp(it), the recurrence and the Joukowsky map)
  - book: isbn:9780849303555
    title: J. C. Mason and D. C. Handscomb, Chebyshev Polynomials, Chapman and Hall/CRC, 2003
    locator: Chapter 1, Definitions (the four kinds, recurrences, shifted polynomials) and Chapter 2, Basic properties and formulae (zeros, extrema, products, derivatives, the minimax property)
  - book: isbn:9780471628965
    title: Theodore J. Rivlin, Chebyshev Polynomials, second edition, Wiley, 1990
    locator: Chapter 1, Definitions and some elementary properties, and Chapter 2, Extremal properties
  - book: isbn:9780821813744
    title: E. W. Cheney, Introduction to Approximation Theory, second edition, AMS Chelsea, 1998
    locator: Chapter 3, Tchebycheff approximation of continuous functions (the Tchebycheff polynomials and their least deviation from zero)
  - paper: "P. L. Chebyshev, Théorie des mécanismes connus sous le nom de parallélogrammes, Mémoires des savants étrangers présentés à l'Académie impériale des sciences de Saint-Pétersbourg 7 (1854)"
    locator: the problem of the polynomial of given leading coefficient that deviates least from zero on an interval
---

The Chebyshev polynomials of the first kind are the polynomials $T_k$ defined by $T_k(\cos t) = \cos(kt)$. On $[-1, 1]$ they are cosines in disguise. This one fact gives their recurrence, their zeros and extrema, their orthogonality and their extremal property: among polynomials of degree $k$ with leading coefficient $2^{k-1}$, $T_k$ has the smallest maximum on $[-1, 1]$. They are the basis of choice for polynomial approximation on an interval, through [Chebyshev nodes](/chebyshev-nodes/), [Chebyshev series](/chebyshev-series/) and [Chebyshev interpolation](/chebyshev-interpolation/).

## Definition

Notation on the interpolation and approximation pages: $f$ is a function on $[a, b]$, usually $[-1, 1]$; $\mathcal{P}_n$ is the space of polynomials of degree at most $n$; $E_n(f)$ is the best approximation error in the maximum norm; $T_k$ is the Chebyshev polynomial of degree $k$.

**Definition.** For $k = 0, 1, 2, \ldots$, the Chebyshev polynomial $T_k$ is the polynomial with
$$T_k(\cos t) = \cos(kt) \qquad \text{for all real } t.$$
Equivalently $T_k(x) = \cos(k \arccos x)$ for $x \in [-1, 1]$. That such a polynomial exists, and is unique, follows from the recurrence below: $T_0 = 1$, $T_1 = x$, and
$$T_{k+1}(x) = 2x\, T_k(x) - T_{k-1}(x), \qquad k \ge 1,$$
which holds because $\cos((k+1)t) + \cos((k-1)t) = 2 \cos t \cos(kt)$. A polynomial is determined by its values on $[-1, 1]$, so $T_k$ is unique.

**Basic properties.** Each is a short consequence of the definition with $x = \cos t$, $t \in [0, \pi]$.

1. **Degree and parity.** $T_k$ has degree $k$, leading coefficient $2^{k-1}$ for $k \ge 1$, and the parity of $k$: $T_k(-x) = (-1)^k T_k(x)$.
2. **Bounds.** $|T_k(x)| \le 1$ on $[-1, 1]$, and $T_k(1) = 1$, $T_k(-1) = (-1)^k$.
3. **Zeros.** $T_k$ has the $k$ simple zeros $\cos\big((2j + 1)\pi/(2k)\big)$, $j = 0, \ldots, k - 1$, all in $(-1, 1)$: the Chebyshev points of the first kind.
4. **Extrema.** $T_k(\cos(j\pi/k)) = (-1)^j$ for $j = 0, \ldots, k$: the $k + 1$ Chebyshev points of the second kind, where $T_k$ alternates between $+1$ and $-1$.
5. **Orthogonality.** With the weight $w(x) = (1 - x^2)^{-1/2}$,
$$\int_{-1}^{1} T_j(x) T_k(x)\, \frac{dx}{\sqrt{1 - x^2}} = \int_0^\pi \cos(jt) \cos(kt)\, dt = \begin{cases} 0, & j \ne k, \\ \pi, & j = k = 0, \\ \pi/2, & j = k \ge 1. \end{cases}$$
The same relations hold for sums over the zeros of $T_{n+1}$ when $j, k \le n$ (discrete orthogonality), which is why Chebyshev coefficients are computed by a [discrete cosine transform](/discrete-cosine-transform/).
6. **Products and composition.** $2T_j T_k = T_{j+k} + T_{|j-k|}$ and $T_j(T_k(x)) = T_{jk}(x)$.
7. **Derivative.** $T_k'(x) = k\, U_{k-1}(x)$, where $U_m(\cos t) = \sin((m+1)t)/\sin t$ is the Chebyshev polynomial of the second kind. $T_k$ solves $(1 - x^2) y'' - x y' + k^2 y = 0$.
8. **Outside the interval.** For real $|x| \ge 1$ and for complex $x$, $T_k(x) = \tfrac{1}{2}(z^k + z^{-k})$ where $x = \tfrac{1}{2}(z + z^{-1})$ (the Joukowsky map, Trefethen, Chapter 3). With $|z| = \rho > 1$, the image of the circle is the Bernstein ellipse $E_\rho$, on which $|T_k| \approx \rho^k/2$. On the real line, $T_k(x) = \cosh(k \operatorname{arccosh} x)$ for $x \ge 1$, which grows like $(x + \sqrt{x^2 - 1})^k/2$.

**The minimax property.** For $k \ge 1$, the monic polynomial $\tilde T_k = 2^{1-k} T_k$ satisfies $\max_{[-1,1]} |\tilde T_k| = 2^{1-k}$, and every other monic polynomial $q$ of degree $k$ has $\max_{[-1,1]} |q| > 2^{1-k}$.

*Proof.* Suppose $q$ is monic of degree $k$ with $\max |q| \le 2^{1-k}$, and put $r = \tilde T_k - q$, of degree at most $k - 1$. At the extrema $\eta_j = \cos(j\pi/k)$, $\tilde T_k(\eta_j) = (-1)^j 2^{1-k}$, so $(-1)^j r(\eta_j) \ge 0$ for $j = 0, \ldots, k$. If the inequality is strict at every $\eta_j$, then $r$ changes sign $k$ times and has $k$ zeros, so $r = 0$. If some values $r(\eta_j)$ are zero, a count of zeros with multiplicity (a zero at an interior $\eta_j$ where $r$ does not change sign is a double zero) still gives at least $k$ zeros, so again $r = 0$ and $q = \tilde T_k$. $\square$

Equivalently, the best approximation of $x^k$ from $\mathcal{P}_{k-1}$ in the maximum norm on $[-1, 1]$ is $x^k - 2^{1-k} T_k(x)$, with the error $2^{1-k}$, which equioscillates at $k + 1$ points as the [equioscillation theorem](/chebyshev-equioscillation-theorem/) requires. This is the basis of [Chebyshev economization](/chebyshev-economization/). For interpolation it means that the node polynomial $\omega$ of $n + 1$ nodes has $\|\omega\|_\infty \ge 2^{-n}$, with equality exactly at the zeros of $T_{n+1}$ (see [Chebyshev nodes](/chebyshev-nodes/)).

**On a general interval.** On $[a, b]$ use $T_k\big((2x - a - b)/(b - a)\big)$; on $[0, 1]$ these are the shifted polynomials $T_k^*(x) = T_k(2x - 1)$.

**Evaluation in floating point.** The three-term recurrence evaluates $T_0(x), \ldots, T_n(x)$ at one point in $2n$ multiplications and $n$ subtractions. For $x \in [-1, 1]$ it is stable in practice, and a sum $\sum c_k T_k(x)$ is best evaluated by Clenshaw's backward recurrence in $O(n)$ operations, without forming monomial coefficients. Converting a Chebyshev sum to monomial form is unstable for large $n$: the monomial coefficients of $T_k$ grow like $(1 + \sqrt{2})^k$, so cancellation destroys the value. Outside $[-1, 1]$ the polynomials grow and relative accuracy is the right measure.

## Examples and non-examples

**The first few.**

| $k$ | $T_k(x)$ |
|---|---|
| 0 | $1$ |
| 1 | $x$ |
| 2 | $2x^2 - 1$ |
| 3 | $4x^3 - 3x$ |
| 4 | $8x^4 - 8x^2 + 1$ |
| 5 | $16x^5 - 20x^3 + 5x$ |

Check of $T_3$: $\cos 3t = 4\cos^3 t - 3 \cos t$, the triple angle formula. At $x = 1/2 = \cos(\pi/3)$, $T_3(1/2) = 4/8 - 3/2 = -1 = \cos \pi$.

**Least deviation.** The monic cubic $x^3$ has maximum 1 on $[-1, 1]$, while $\tilde T_3 = x^3 - \tfrac{3}{4}x$ has maximum $1/4$, reached with alternating signs at $1, \tfrac{1}{2}, -\tfrac{1}{2}, -1$. So the best linear approximation of $x^3$ on $[-1, 1]$ is $\tfrac{3}{4}x$, with error $1/4$.

**Growth outside the interval.** $T_{10}(1.01) \approx 2.18$ and $T_{10}(1.1) \approx 42.2$, against $|T_{10}| \le 1$ on $[-1, 1]$. The value at $1.1$ agrees with $\tfrac{1}{2}(\rho^{10} + \rho^{-10})$ for $\rho = 1.1 + \sqrt{0.21} \approx 1.558$. Among all polynomials of degree $k$ bounded by 1 on $[-1, 1]$, $T_k$ is the largest at every real point outside the interval (Rivlin, Chapter 2); this is why Chebyshev polynomials give the optimal acceleration in the [Chebyshev iteration](/chebyshev-iteration/).

**Non-example: Legendre polynomials.** The [Legendre polynomials](/legendre-polynomials/) $P_0 = 1$, $P_1 = x$, $P_2 = (3x^2 - 1)/2$ are orthogonal for the weight 1, not for $(1 - x^2)^{-1/2}$. They also satisfy $|P_k| \le 1$ on $[-1, 1]$, but they reach the value 1 in absolute value only at $\pm 1$, so they do not equioscillate and do not have the minimax property: the monic $P_2$ is $x^2 - 1/3$, with maximum $2/3$, against $1/2$ for $\tilde T_2 = x^2 - 1/2$.

**Non-example: $\cos(kx)$.** The function $\cos(kx)$ is not a polynomial in $x$; the identity holds only after the change of variables $x = \cos t$. Likewise $T_k(x) = \cos(k \arccos x)$ is a correct formula only on $[-1, 1]$ if $\arccos$ is the real function.

## Related definitions

- [Chebyshev nodes](/chebyshev-nodes/): the zeros of $T_{n+1}$ (first kind) and the extrema of $T_n$ (second kind).
- [Chebyshev series](/chebyshev-series/): the expansion $f = \sum a_k T_k$, the orthogonal expansion for the weight $(1 - x^2)^{-1/2}$.
- [Orthogonal polynomials](/orthogonal-polynomials/): $T_k$ is the case $\alpha = \beta = -1/2$ of the Jacobi family; $U_k$ is the case $\alpha = \beta = 1/2$.
- [Chebyshev interpolation](/chebyshev-interpolation/) and [Chebyshev economization](/chebyshev-economization/): algorithms built on the properties above.
- [Clenshaw-Curtis quadrature](/clenshaw-curtis-quadrature/): integrates the Chebyshev interpolant term by term, using $\int_{-1}^1 T_k = 2/(1 - k^2)$ for even $k$.
- [Chebyshev equioscillation theorem](/chebyshev-equioscillation-theorem/): the general characterization of best approximations, of which the minimax property of $T_k$ is the simplest case.

## References
