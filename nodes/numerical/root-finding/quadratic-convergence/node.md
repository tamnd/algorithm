---
tag: PWDKN2
kind: definition
slug: quadratic-convergence
name: Quadratic convergence
aliases:
- second-order convergence
- order 2 convergence
area: numerical/root-finding
level: intro
summary: Each error is about a constant times the square of the one before, so the number of correct digits about doubles per step, as for Newton's method at a simple root.
prereqs: [order-of-convergence]
see_also: [newton-raphson-method, newton-method-for-systems, newton-square-root, multiplicity-of-roots, secant-method, steffensen-method, kantorovich-theorem, stopping-criteria]
sources:
  - book: isbn:9780898713640
    title: John E. Dennis Jr. and Robert B. Schnabel, Numerical Methods for Unconstrained Optimization and Nonlinear Equations, SIAM Classics in Applied Mathematics 16, 1996
    locator: Section 2.3 (q-quadratic convergence) and Section 2.4, Convergence of Newton's method (Theorem 2.4.3); Section 5.2, Local convergence of Newton's method (Theorem 5.2.1)
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 1, Solution of equations by iteration (Newton's method and its quadratic convergence)
  - book: isbn:9780898714616
    title: J. M. Ortega and W. C. Rheinboldt, Iterative Solution of Nonlinear Equations in Several Variables, SIAM Classics in Applied Mathematics 30, 2000
    locator: Chapter 9, Rates of convergence, general; Chapter 10 (the local convergence of Newton's method)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 25, Nonlinear systems and Newton's method (the limiting accuracy of Newton's method in floating point)
---

A sequence $x_k \to x^*$ converges *quadratically* when its errors $e_k = x_k - x^*$ satisfy $|e_{k+1}| \approx C |e_k|^2$ for a constant $C$, that is, when it has [order of convergence](/order-of-convergence/) 2. Then the number of correct digits about doubles in each step, once the error is small. [Newton's method](/newton-raphson-method/) converges quadratically to a simple root of a function with a continuous second derivative, from a starting point close enough to the root, and this is the main reason why it is used.

## Definition

Notation on the root-finding pages: $f$ is the function, $x^*$ a root, $x_k$ the iterates, $e_k = x_k - x^*$ the error, and a root is *simple* when $f(x^*) = 0 \ne f'(x^*)$.

Let $x_k \to x^*$ with $e_k \ne 0$. The sequence converges

- *Q-quadratically* when there are $C < \infty$ and $k_0$ with $|e_{k+1}| \le C |e_k|^2$ for all $k \ge k_0$;
- *with order exactly 2* and rate constant $C$ when $|e_{k+1}| / |e_k|^2 \to C$ with $0 < C < \infty$.

The first is the form that most theorems prove. If $|e_{k+1}| \le C |e_k|^2$ and $C |e_{k_0}| < 1$, then by induction $C |e_{k}| \le (C |e_{k_0}|)^{2^{k - k_0}}$, so the error falls faster than any geometric sequence. In base-10 digits, $d_k = -\log_{10} |e_k|$ satisfies $d_{k+1} \ge 2 d_k - \log_{10} C$.

**Theorem (local quadratic convergence of Newton's method).** Let $f$ be real and twice continuously differentiable on $I = [x^* - r, x^* + r]$, with $f(x^*) = 0$ and $f'(x) \ne 0$ for all $x \in I$. Let
$$M = \frac{\max_{x \in I} |f''(x)|}{2 \min_{x \in I} |f'(x)|}.$$
If $x_0 \in I$ and $M |e_0| < 1$, then the iterates $x_{k+1} = x_k - f(x_k)/f'(x_k)$ stay in $I$, satisfy $|e_{k+1}| \le M |e_k|^2$ and $|e_k| \le (M |e_0|)^{2^k} / M$, and
$$\lim_{k \to \infty} \frac{e_{k+1}}{e_k^2} = \frac{f''(x^*)}{2 f'(x^*)}$$
whenever no $e_k$ is zero.

*Proof.* Assume that $x_k \in I$. By Taylor's theorem with the Lagrange remainder, expanded at $x_k$ and evaluated at $x^*$, there is $\xi_k$ between $x_k$ and $x^*$ with
$$0 = f(x^*) = f(x_k) + f'(x_k)(x^* - x_k) + \tfrac12 f''(\xi_k)(x^* - x_k)^2.$$
Divide by $f'(x_k) \ne 0$ and rearrange: $x_k - f(x_k)/f'(x_k) - x^* = \frac{f''(\xi_k)}{2 f'(x_k)} e_k^2$, that is,
$$e_{k+1} = \frac{f''(\xi_k)}{2 f'(x_k)}\, e_k^2. \qquad (1)$$
Both $\xi_k$ and $x_k$ lie in $I$, so $|e_{k+1}| \le M |e_k|^2$. Now use induction on $k$ for the claim "$x_k \in I$ and $M |e_k| \le (M |e_0|)^{2^k}$". For $k = 0$ it holds by assumption. If it holds for $k$, then $M |e_k| \le M |e_0| < 1$, so $|e_{k+1}| \le (M |e_k|) |e_k| < |e_k| \le r$ and $x_{k+1} \in I$; and $M |e_{k+1}| \le (M |e_k|)^2 \le (M |e_0|)^{2^{k+1}}$. Since $M |e_0| < 1$, $e_k \to 0$. Then $x_k \to x^*$ and $\xi_k \to x^*$, and by the continuity of $f''$ and $f'$, (1) gives the limit. $\blacksquare$

The same proof works for complex $f$ analytic near $x^*$, with Cauchy's estimates in place of the Lagrange remainder. For systems $F : \mathbb{R}^n \to \mathbb{R}^n$, Newton's method converges quadratically when the Jacobian $J$ is Lipschitz near $x^*$ and $J(x^*)$ is nonsingular (Dennis and Schnabel, Theorem 5.2.1; see [Newton's method for systems](/newton-method-for-systems/)). The [Kantorovich theorem](/kantorovich-theorem/) gives a version that needs no knowledge of $x^*$.

## Examples and non-examples

**Newton's method for $\sqrt 2$.** Take $f(x) = x^2 - 2$ and $x_0 = 1$, in exact rational arithmetic. The rate constant is $f''(x^*)/(2 f'(x^*)) = 1/(2\sqrt 2) = 0.353553\ldots$.

| $k$ | $x_k$ | decimal value | $e_k$ | $e_k / e_{k-1}^2$ |
|---|---|---|---|---|
| 0 | $1$ | 1.00000000000000000000000000 | $-4.142 \cdot 10^{-1}$ | |
| 1 | $3/2$ | 1.50000000000000000000000000 | $8.579 \cdot 10^{-2}$ | 0.500000 |
| 2 | $17/12$ | 1.41666666666666666666666667 | $2.453 \cdot 10^{-3}$ | 0.333333 |
| 3 | $577/408$ | 1.41421568627450980392156863 | $2.124 \cdot 10^{-6}$ | 0.352941 |
| 4 | $665857/470832$ | 1.41421356237468991062629558 | $1.595 \cdot 10^{-12}$ | 0.353553 |
| 5 | | 1.41421356237309504880168962 | $8.993 \cdot 10^{-25}$ | 0.353553 |
| 6 | | 1.41421356237309504880168872 | $2.859 \cdot 10^{-49}$ | 0.353553 |

From step 3 on, each step about doubles the number of correct digits: 5, 11, 24 and 48 digits.

**In floating point.** In binary64 the same iteration gives $x_4 = 1.4142135623746899$ and $x_5 = 1.4142135623730951$, the correctly rounded $\sqrt 2$. Then the quadratic phase is over: the next iterates alternate between $1.414213562373095$ and $1.4142135623730951$, two adjacent numbers, because the computed residual $x^2 - 2$ is $\mp 4.44 \cdot 10^{-16}$, not zero. The error stops at the limiting accuracy of about $u |x^*|$, with unit roundoff $u = 2^{-53}$. A [stopping rule](/stopping-criteria/) must expect this: the test $x_{k+1} = x_k$ never holds here.

**Non-example: a double root.** For $f(x) = (x - 1)^2$, Newton's method gives $x_{k+1} - 1 = (x_k - 1)/2$. This is linear with rate $1/2$, not quadratic: the hypothesis $f'(x^*) \ne 0$ fails. See [multiplicity of roots](/multiplicity-of-roots/).

**Non-example: $f$ not twice differentiable.** For $f(x) = x + |x|^{3/2}$ the root $0$ is simple, $f'(0) = 1$, but $f''$ does not exist at $0$. For $x > 0$ Newton's step gives $x_{k+1} = \tfrac12 x_k^{3/2} / (1 + \tfrac32 x_k^{1/2})$, so $e_{k+1}/e_k^{3/2} \to 1/2$, and the order is $3/2$. From $x_0 = 0.5$ the ratio $x_{k+1}/x_k^{3/2}$ is $0.243, 0.347, 0.439, 0.486, 0.499$ in steps 1 to 5.

**Non-example: superlinear but not quadratic.** The [secant method](/secant-method/) has order $(1 + \sqrt 5)/2 \approx 1.618$, and the chord method $x_{k+1} = x_k - f(x_k)/f'(x_0)$, which keeps the first derivative, is linear with rate $|1 - f'(x^*)/f'(x_0)|$.

**Quadratic but far from the root.** The bound $|e_{k+1}| \le M |e_k|^2$ helps only when $M |e_k| < 1$. For $f(x) = \arctan x$ and $x_0 = 1.5$, Newton's iterates grow in size and diverge, although the root $0$ is simple; quadratic convergence is a local property.

## Related definitions

- [Order of convergence](/order-of-convergence/): the general definition, with Q-order, R-order and the efficiency index.
- [Multiplicity of a root](/multiplicity-of-roots/): at a multiple root Newton's method is linear, and the modified step $x - m f/f'$ restores order 2.
- [Steffensen's method](/steffensen-method/): order 2 with two evaluations of $f$ and no derivative.
- [Newton square root](/newton-square-root/): the oldest example of quadratic convergence.
- [Kantorovich theorem](/kantorovich-theorem/): quadratic convergence from conditions at the starting point.

## References
