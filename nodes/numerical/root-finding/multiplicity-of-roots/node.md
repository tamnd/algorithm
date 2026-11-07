---
tag: 87Y35G
kind: definition
slug: multiplicity-of-roots
name: Multiplicity of a root
aliases:
- multiple root
- algebraic multiplicity
- order of a zero
- repeated root
area: numerical/root-finding
level: intro
summary: A root x* of f has multiplicity m when f and its first m - 1 derivatives vanish at x* and the m-th does not. Multiple roots make Newton's method linear and are ill-conditioned.
prereqs: [root-finding-problem, order-of-convergence]
see_also: [newton-raphson-method, secant-method, root-conditioning, square-free-factorization, polynomial-gcd, bisection-method, wilkinson-polynomial, quadratic-convergence]
sources:
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 1, Solution of equations by iteration (Newton's method at a multiple root, exercises)
  - book: isbn:9780828403122
    title: J. F. Traub, Iterative Methods for the Solution of Equations, Prentice-Hall, 1964 (reprinted by AMS Chelsea)
    locator: Chapter 7, Multiple roots
  - book: "A. M. Ostrowski, Solution of Equations and Systems of Equations, second edition, Academic Press, 1966"
    locator: Chapter 5, Further discussion of iterations, multiple zeros
  - book: "J. H. Wilkinson, Rounding Errors in Algebraic Processes, Prentice-Hall, 1963 (reprinted by Dover, 1994)"
    locator: Chapter 2, Computations involving polynomials (the sensitivity of multiple and clustered zeros)
---

A root $x^*$ of a function $f$ has *multiplicity* $m$ when $f$ and its first $m - 1$ derivatives are zero at $x^*$ and the $m$-th derivative is not. A root of multiplicity 1 is *simple*; a root of multiplicity 2 or more is *multiple*. Multiplicity matters in computation for three reasons: [Newton's method](/newton-raphson-method/) and the [secant method](/secant-method/) become linear at a multiple root, a root of even multiplicity gives no sign change and so no [bracket](/bracketing-method/), and a multiple root moves by much more than the size of a small change of $f$ ([root conditioning](/root-conditioning/)).

## Definition

Notation on the root-finding pages: $f$ is the function, $x^*$ a root, $x_k$ the iterates, $e_k = x_k - x^*$ the error; $q$ and $C$ are the [order and rate constant](/order-of-convergence/) of a method.

Let $f$ be real or complex, $m \ge 1$ an integer, and $f$ of class $C^m$ near $x^*$. The point $x^*$ is a root of multiplicity $m$ when
$$f(x^*) = f'(x^*) = \cdots = f^{(m-1)}(x^*) = 0 \quad\text{and}\quad f^{(m)}(x^*) \ne 0.$$

**Factor form.** For $f \in C^m$ near $x^*$, $x^*$ has multiplicity $m$ if and only if $f(x) = (x - x^*)^m g(x)$ with $g$ continuous near $x^*$ and $g(x^*) \ne 0$. *Proof.* If the derivatives vanish, Taylor's theorem with the integral remainder gives $f(x) = (x - x^*)^m g(x)$ with
$$g(x) = \frac{1}{(m-1)!} \int_0^1 (1 - t)^{m-1} f^{(m)}\bigl(x^* + t(x - x^*)\bigr)\, dt,$$
which is continuous, with $g(x^*) = f^{(m)}(x^*)/m! \ne 0$. Conversely, if $f = (x - x^*)^m g$ with $g(x^*) \ne 0$, then $f(x)/(x - x^*)^m \to g(x^*)$, while Taylor's theorem gives $f(x) = \sum_{j < m} f^{(j)}(x^*)(x - x^*)^j / j! + O(|x - x^*|^m)$; the limit is finite only if all $f^{(j)}(x^*)$ with $j < m$ are zero, and then it equals $f^{(m)}(x^*)/m!$, which is therefore nonzero. $\square$

**Polynomials.** For a polynomial $p$ over a field, $x^*$ has multiplicity $m$ when $(x - x^*)^m$ divides $p$ and $(x - x^*)^{m+1}$ does not. Over $\mathbb{R}$ or $\mathbb{C}$ this agrees with the definition by derivatives. Counted with multiplicity, a polynomial of degree $n$ has exactly $n$ complex roots ([fundamental theorem of algebra](/fundamental-theorem-of-algebra/)). The multiple roots of $p$ are the roots of $\gcd(p, p')$, so [square-free factorization](/square-free-factorization/) splits $p$ into factors with only simple roots, in exact arithmetic.

**Consequences for methods.**

- *Sign.* With $f = (x - x^*)^m g$, $g(x^*) \ne 0$ and $f$ real, $f$ changes sign at $x^*$ if and only if $m$ is odd. So a root of even multiplicity cannot be found by [bisection](/bisection-method/).
- *Newton is linear.* Let $f \in C^{m+1}$ near $x^*$ with multiplicity $m \ge 2$. Then $g \in C^1$, $f'(x) = (x - x^*)^{m-1}\bigl(m g(x) + (x - x^*) g'(x)\bigr)$, and Newton's step gives
$$e_{k+1} = e_k - \frac{e_k\, g(x_k)}{m g(x_k) + e_k g'(x_k)} = e_k\, \frac{(m-1) g(x_k) + e_k g'(x_k)}{m g(x_k) + e_k g'(x_k)}.$$
The factor tends to $(m - 1)/m < 1$ as $e_k \to 0$, so it is at most some $\rho < 1$ on a small interval around $x^*$, and Newton's method converges there linearly with rate $C = 1 - 1/m$.
- *Repairs.* If $m$ is known, the step $x_{k+1} = x_k - m f(x_k)/f'(x_k)$ has order 2. If $m$ is not known, Newton's method on $u = f/f'$, which has a simple root at $x^*$, has order 2 but needs $f''$. Traub (Chapter 7) gives both and more.
- *The secant method* is linear at a double root, with rate $(\sqrt 5 - 1)/2 \approx 0.618$.
- *Conditioning.* If $f$ is changed to $f - \varepsilon$, the root moves to about $x^* + (m!\, \varepsilon / f^{(m)}(x^*))^{1/m}$, which for small $\varepsilon$ is far larger than $\varepsilon$ when $m \ge 2$. In floating point a multiple root is found only to about $u^{1/m}$ relative accuracy, with unit roundoff $u$.

## Examples and non-examples

**A double root.** $p(x) = x^3 - 3x + 2 = (x - 1)^2 (x + 2)$ has the root $1$ of multiplicity 2, since $p(1) = p'(1) = 0$ and $p''(1) = 6$, and the simple root $-2$. Iterations from $x_0 = 2$, in exact rational arithmetic:

| $k$ | Newton $e_k$ | Newton $e_{k+1}/e_k$ | $x - 2p/p'$: $e_k$ | secant ($x_0 = 2$, $x_1 = 1.5$) $e_k$ | secant $e_{k+1}/e_k$ |
|---|---|---|---|---|---|
| 0 | 1.0 | 0.5556 | 1.0 | | |
| 1 | 0.5556 | 0.5362 | 0.1111 | 0.5 | 0.7200 |
| 2 | 0.2979 | 0.5216 | $1.949 \cdot 10^{-3}$ | 0.36 | 0.6147 |
| 3 | 0.1554 | 0.5120 | $6.327 \cdot 10^{-7}$ | 0.2213 | 0.6439 |
| 4 | 0.07956 | 0.5064 | $6.672 \cdot 10^{-14}$ | 0.1425 | 0.6244 |
| 5 | 0.04029 | 0.5033 | | 0.08898 | 0.6262 |

Newton's ratio tends to $1/2 = 1 - 1/m$. The modified step with $m = 2$ about doubles the correct digits in each step. The secant ratio tends to $0.618$.

**A triple root.** $(x - 1)^3$ has the root $1$ of multiplicity 3. It changes sign, so bisection finds it, at its usual rate. Newton's method has rate $2/3$. The perturbed equation $(x - 1)^3 = 10^{-12}$ has the real root $1 + 10^{-4}$: a change of $10^{-12}$ in $f$ moves the root by $10^{-4}$.

**Even multiplicity and no bracket.** $(x - 1)^2 + 10^{-20}$ has no real root, while $(x - 1)^2$ has a double root. For neither function do the ends of any interval have opposite signs, so no bracketing method applies to either of them.

**Non-example: infinite multiplicity.** $f(x) = e^{-1/x^2}$ for $x \ne 0$ and $f(0) = 0$ is $C^\infty$, and all its derivatives are zero at $0$. The root $0$ has no finite multiplicity, and Newton's step $x_{k+1} = x_k - x_k^3/2$ converges to $0$ only sublinearly.

**Non-example: no integer multiplicity.** $f(x) = x^{1/3}$ has a root at $0$ where $f'$ does not exist, so the definition does not apply. Newton's step gives $x_{k+1} = -2 x_k$, which diverges from each $x_0 \ne 0$.

## Related definitions

- [Order of convergence](/order-of-convergence/) and [quadratic convergence](/quadratic-convergence/): what a multiple root changes.
- [Root conditioning](/root-conditioning/): the sensitivity $\varepsilon^{1/m}$ of an $m$-fold root, and of a cluster of close roots.
- [Square-free factorization](/square-free-factorization/) and [polynomial GCD](/polynomial-gcd/): remove multiple roots of a polynomial in exact arithmetic.
- [Wilkinson's polynomial](/wilkinson-polynomial/): simple roots that are as sensitive as multiple ones.

## References
