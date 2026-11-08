---
tag: NXJSC4
kind: theorem
slug: polynomial-interpolation-error-theorem
name: Polynomial interpolation error theorem
aliases:
- Lagrange interpolation error formula
- Cauchy remainder formula for interpolation
area: numerical/interpolation-and-approximation
level: core
summary: If f has n + 1 derivatives, the error of the interpolant at n + 1 distinct nodes is f^(n+1)(xi) omega(x)/(n+1)! for some xi in the smallest interval that holds x and the nodes.
prereqs: [polynomial-interpolation, divided-differences]
see_also: [lagrange-interpolation, newton-interpolation, chebyshev-nodes, runge-phenomenon, hermite-interpolation, piecewise-linear-interpolation, lebesgue-constant, newton-cotes-formulas]
sources:
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 6, Polynomial interpolation (the error theorem and its proof by Rolle's theorem)
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Section 3.1, Polynomial interpolation theory (the error formula), and Section 3.2, Newton divided differences (the divided-difference form of the error)
  - book: isbn:9780521295147
    title: M. J. D. Powell, Approximation Theory and Methods, Cambridge University Press, 1981
    locator: Chapter 4, Polynomial interpolation (the error formula), and Chapter 5, Divided differences
  - book: isbn:9780486624952
    title: Philip J. Davis, Interpolation and Approximation, Dover, 1975 (first published 1963)
    locator: Chapter III, Remainder theory
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 11, Hermite integral formula (the complex-analytic form of the same error)
---

The polynomial interpolation error theorem gives the exact error of the interpolating polynomial $p_n$ of a smooth function: $f(x) - p_n(x) = f^{(n+1)}(\xi)\, \omega(x) / (n+1)!$, where $\omega$ is the node polynomial and $\xi$ is an unknown point in the smallest interval that contains $x$ and the nodes. It splits the error into a factor that depends on $f$ and a factor that depends only on the nodes. The second factor explains why [Chebyshev nodes](/chebyshev-nodes/) are good and equispaced nodes are bad, and it gives the error of [piecewise linear interpolation](/piecewise-linear-interpolation/), of Newton-Cotes quadrature and of finite difference formulas.

## Statement

Notation on the interpolation pages: $f$ is a real function on $[a, b]$, the nodes $x_0, \ldots, x_n \in [a, b]$ are distinct, $p_n \in \mathcal{P}_n$ is the [interpolating polynomial](/polynomial-interpolation/) with $p_n(x_i) = f(x_i)$, and $\omega(x) = \prod_{i=0}^{n} (x - x_i)$.

**Theorem.** Let $f \in C^n[a, b]$ and let $f^{(n+1)}$ exist on $(a, b)$. For each $x \in [a, b]$ let $I_x$ be the smallest closed interval that contains $x, x_0, \ldots, x_n$. Then there is a point $\xi = \xi(x)$ in the interior of $I_x$ such that
$$f(x) - p_n(x) = \frac{f^{(n+1)}(\xi)}{(n+1)!}\, \omega(x).$$
In particular, if $|f^{(n+1)}| \le M_{n+1}$ on $(a, b)$, then
$$|f(x) - p_n(x)| \le \frac{M_{n+1}}{(n+1)!}\, |\omega(x)| \quad \text{and} \quad \|f - p_n\|_\infty \le \frac{M_{n+1}}{(n+1)!}\, \|\omega\|_\infty.$$

**Divided-difference form.** With no smoothness assumption on $f$, and for $x$ different from the nodes,
$$f(x) - p_n(x) = f[x_0, \ldots, x_n, x]\; \omega(x),$$
where $f[\cdot]$ is the [divided difference](/divided-differences/). The theorem follows from this and the mean value property $f[x_0, \ldots, x_n, x] = f^{(n+1)}(\xi)/(n+1)!$.

**Hermite data.** If node $x_i$ carries the data $f(x_i), \ldots, f^{(m_i - 1)}(x_i)$ with $\sum_i m_i = n + 1$, the same formula holds with $\omega(x) = \prod_i (x - x_i)^{m_i}$ and $f \in C^{n+1}[a, b]$ ([Hermite interpolation](/hermite-interpolation/)).

## In plain words

When you replace a smooth curve by the polynomial through some of its points, the mistake you make at a place has two parts multiplied together. One part depends only on the curve: how fast it bends at the highest order that the polynomial cannot follow. The other part depends only on where you put the points: it is the product of the distances from the place to every point.

The second part is zero at every point you used, and it is large where the points are sparse or where the place is far from them. Since you control where the points go, you can make this part small everywhere by spacing them well, and the formula tells you exactly how small.

## Proof

Fix $x \in [a, b]$. If $x = x_k$ for some $k$, both sides are 0 and the formula holds with any $\xi$ (for $n \ge 1$ the interior of $I_x$ is not empty). So let $x$ differ from all nodes. Then $\omega(x) \ne 0$, and we set
$$K = \frac{f(x) - p_n(x)}{\omega(x)}, \qquad g(t) = f(t) - p_n(t) - K\, \omega(t), \quad t \in [a, b].$$

1. **Zeros of $g$.** $g(x_i) = f(x_i) - p_n(x_i) - K \cdot 0 = 0$ for $i = 0, \ldots, n$, and $g(x) = f(x) - p_n(x) - K\omega(x) = 0$ by the choice of $K$. So $g$ has $n + 2$ distinct zeros, all in $I_x$.
2. **Smoothness of $g$.** $p_n$ and $\omega$ are polynomials, so $g \in C^n[a, b]$ and $g^{(n+1)}$ exists on $(a, b)$.
3. **Rolle's theorem, repeated.** Claim: for $k = 0, 1, \ldots, n + 1$, $g^{(k)}$ has at least $n + 2 - k$ distinct zeros in $I_x$, and for $k \ge 1$ they lie in the interior of $I_x$. For $k = 0$ this is step 1. If $g^{(k)}$ with $k \le n$ has zeros $s_1 < \cdots < s_{n+2-k}$ in $I_x$, then $g^{(k)}$ is continuous on each $[s_j, s_{j+1}]$ and differentiable inside (as $k \le n$), so Rolle's theorem gives a zero of $g^{(k+1)}$ in each open interval $(s_j, s_{j+1})$. These $n + 1 - k$ zeros are distinct, since the intervals are disjoint, and they lie in the interior of $I_x$.
4. **The last derivative.** For $k = n + 1$ we get a point $\xi$ in the interior of $I_x$ with $g^{(n+1)}(\xi) = 0$. Since $\deg p_n \le n$, $p_n^{(n+1)} = 0$; since $\omega$ is monic of degree $n + 1$, $\omega^{(n+1)} = (n+1)!$. So $0 = f^{(n+1)}(\xi) - K (n+1)!$, that is $K = f^{(n+1)}(\xi)/(n+1)!$.
5. **Conclusion.** By the definition of $K$, $f(x) - p_n(x) = K\, \omega(x) = \dfrac{f^{(n+1)}(\xi)}{(n+1)!}\, \omega(x)$.

The bounds follow by taking absolute values and the maximum over $x$. $\blacksquare$

*The divided-difference form.* Add $x$ as a new node $x_{n+1} = x$. By the [Newton form](/newton-interpolation/), $p_{n+1}(t) = p_n(t) + f[x_0, \ldots, x_n, x]\, \omega(t)$, and $p_{n+1}(x) = f(x)$. Evaluating at $t = x$ gives the formula. The mean value property then follows by comparing the two forms of the error at $x$.

## Consequences

- **Bounds for standard node sets on $[-1, 1]$.** For Chebyshev points of the first kind, $x_i = \cos\frac{(2i+1)\pi}{2n+2}$, $\omega = 2^{-n} T_{n+1}$, so $\|\omega\|_\infty = 2^{-n}$ and $\|f - p_n\|_\infty \le M_{n+1}/(2^n (n+1)!)$. No other choice of $n + 1$ nodes gives a smaller $\|\omega\|_\infty$, because $2^{-n} T_{n+1}$ is the monic polynomial of degree $n + 1$ with the least maximum norm on $[-1, 1]$ (see [Chebyshev polynomials](/chebyshev-polynomials/)). For equispaced nodes with spacing $h$, $|\omega(x)| \le \tfrac{1}{4} h^{n+1} n!$, which is larger by a factor that grows exponentially near the ends of the interval.
- **Piecewise interpolation.** For $n = 1$ on an interval of length $h$, $|\omega| \le h^2/4$ and the error is at most $h^2 M_2/8$, the bound of [piecewise linear interpolation](/piecewise-linear-interpolation/). The same argument with degree $k$ pieces gives $O(h^{k+1})$ errors.
- **Quadrature and differentiation.** Integrating the formula gives the error terms of [Newton-Cotes formulas](/newton-cotes-formulas/) and of [interpolatory quadrature](/interpolatory-quadrature/); differentiating the interpolant gives the errors of finite difference formulas.
- **Limits.** For Runge's function, $M_{n+1}$ grows like $(n+1)!\, 5^{n+1}$, so the bound does not decide convergence; the [Runge phenomenon](/runge-phenomenon/) needs the complex-analytic form of the error (Trefethen, Chapter 11). For functions with only finitely many derivatives the theorem says nothing for large $n$, and the [Lebesgue constant](/lebesgue-constant/) bound $\|f - p_n\| \le (1 + \Lambda_n) E_n(f)$ takes over.

**Numbers.** On $[-1, 1]$, with maximum errors measured on a grid of 4001 points:

| $f$, $n$, nodes | $\max\lvert f - p_n\rvert$ | bound $M_{n+1}\|\omega\|_\infty/(n+1)!$ |
|---|---|---|
| $e^x$, 5, equispaced | $1.12 \times 10^{-4}$ | $2.61 \times 10^{-4}$ |
| $e^x$, 5, Chebyshev | $5.18 \times 10^{-5}$ | $1.18 \times 10^{-4}$ |
| $e^x$, 10, Chebyshev | $2.71 \times 10^{-11}$ | $6.65 \times 10^{-11}$ |
| $\sin x$, 10, equispaced | $2.10 \times 10^{-10}$ | $2.14 \times 10^{-10}$ |
| $\sin x$, 10, Chebyshev | $2.40 \times 10^{-11}$ | $2.45 \times 10^{-11}$ |

For $e^x$ the bound uses $M_{n+1} = e$, which overestimates $f^{(n+1)}$ away from $x = 1$; for $\sin$ with $n = 10$, $f^{(11)} = -\cos$ is close to its maximum 1 near the center, and the bound is almost reached.

## Tightness

The constant cannot be improved. For $f(x) = x^{n+1}$, $f - p_n$ is a monic polynomial of degree $n + 1$ that vanishes at the nodes, so $f - p_n = \omega$ exactly, and $f^{(n+1)} = (n+1)!$; the formula holds with every $\xi$, and the bound $M_{n+1}|\omega(x)|/(n+1)!$ is an equality at every $x$.

The point $\xi$ depends on $x$ and is not known in general; only bounds on $f^{(n+1)}$ make the formula usable. The hypothesis on $f^{(n+1)}$ cannot be dropped: for $f(x) = |x|$ on $[-1, 1]$ the formula has no meaning, and the equispaced interpolants of $|x|$ diverge at every point other than $-1$, $0$ and $1$, a classical result of Bernstein.

## History

The formula with an intermediate point appears in Cauchy's work on interpolation (1840), and the proof by repeated use of Rolle's theorem is the standard one in the textbooks of Davis, Powell, Atkinson, and Süli and Mayers. The complex-analytic version, the Hermite integral formula, is due to Hermite (1878) and is the basis of the modern analysis of the Runge phenomenon in Trefethen's book.

## References
