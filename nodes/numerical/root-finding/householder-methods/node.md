---
tag: M9RH7W
kind: algorithm
slug: householder-methods
name: Householder's methods
aliases:
- Householder iterations
- Householder's method of order d+1
area: numerical/root-finding
level: advanced
summary: The iteration x <- x + d (1/f)^(d-1)/(1/f)^(d), which uses f, f', ..., f^(d) and has order d+1 at a simple root. d = 1 is Newton's method and d = 2 is Halley's.
solves: [root-finding-problem]
model: real-ram
complexity:
  vars: {d: "the number of derivatives used", δ: "the tolerance on the step", K: "the cap on the number of steps"}
  time: {worst: "O(K d^2)", average: "O(d^2 log log(1/δ) / log(d + 1))"}
  space: {extra: Θ(d)}
  evaluations: {worst: "K(d + 1)", step: "d + 1"}
properties: {deterministic: true, recursive: false, bracketing: false, derivative_free: false, efficiency_index: "(d + 1)^(1/(d + 1))"}
prereqs: [newton-raphson-method, halley-method, order-of-convergence]
see_also: [laguerre-method, multiplicity-of-roots, quadratic-convergence, stopping-criteria, steffensen-method, secant-method, horner-rule, newton-fractal]
sources:
  - book: "Alston S. Householder, The Numerical Treatment of a Single Nonlinear Equation, McGraw-Hill, 1970"
    locator: the chapter on iterations of higher order (the iteration built from the derivatives of 1/f and its order d+1)
  - paper: "E. Schröder, Ueber unendlich viele Algorithmen zur Auflösung der Gleichungen, Mathematische Annalen 2, 317-365, 1870"
    locator: the families of iteration functions of every order, of which Householder's are one
  - book: "J. F. Traub, Iterative Methods for the Solution of Equations, Prentice-Hall, 1964 (Chelsea reprint, 1982)"
    locator: the chapters on one-point iteration functions of higher order, the basic sequences and the informational efficiency
  - paper: "Walter Gander, On Halley's iteration method, The American Mathematical Monthly 92(2), 131-134, 1985"
    locator: the third order case and its relatives
---

Householder's method of order $d + 1$ solves $f(x) = 0$ with the step
$$x_{k+1} = x_k + d\,\frac{(1/f)^{(d-1)}(x_k)}{(1/f)^{(d)}(x_k)} ,$$
using $f, f', \dots, f^{(d)}$ at the current point. With $d = 1$ it is [Newton's method](/newton-raphson-method/), with $d = 2$ it is [Halley's method](/halley-method/), and in general it converges with order $d + 1$ near a simple root: each step multiplies the number of correct digits by about $d + 1$. Each step costs $d + 1$ values, so when every derivative costs as much as $f$ the efficiency index is $(d + 1)^{1/(d+1)}$, which is largest at $d = 2$ and falls for larger $d$. The higher members pay off only when derivatives are cheap, as in Taylor-mode automatic differentiation or for functions given by a differential equation. Like Newton, the methods are local.

## In plain words

The function $1/f$ has a pole at a simple root, and near a pole the derivatives of $1/f$ grow by a factor of about $n / e$ each time you differentiate, where $e$ is the distance to the pole. So the ratio of two consecutive derivatives tells you the distance to the root. The more derivatives you use, the less the rest of the function spoils the estimate: with $d$ derivatives the error after one step is about the $(d + 1)$-th power of the error before. You trade more work per step for fewer steps.

## The problem

Notation on the root-finding pages: $f$ is the function, $x^*$ a root, $x_k$ the iterates and $e_k = x_k - x^*$ the error. A method has [order](/order-of-convergence/) $q$ and rate constant $C$ when $|e_{k+1}| \approx C |e_k|^q$, with $0 < C < 1$ when $q = 1$. A root has [multiplicity](/multiplicity-of-roots/) $m$ when $f(x^*) = \cdots = f^{(m-1)}(x^*) = 0 \ne f^{(m)}(x^*)$. The cost is the number of evaluations of $f$ (and of $f'$ where a method uses it). A method of order $q$ that needs $w$ evaluations in each step has efficiency index $q^{1/w}$.

Input: a routine that returns $f(x), f'(x), \dots, f^{(d)}(x)$, the order parameter $d \ge 1$, a start $x_0$, a tolerance $\delta$ and a cap $K$. Here $q = d + 1$ and $w = d + 1$ when each derivative counts as one evaluation. The [stopping rule](/stopping-criteria/) is on the step, $|x_{k+1} - x_k| \le \delta(1 + |x_{k+1}|)$, together with $f(x_k) = 0$ exactly and the cap $K$.

## The algorithm

The derivatives of $1/f$ blow up near the root, so the code never forms them. Write $a_j = f^{(j)}(x)/j!$ for the Taylor coefficients of $f$ at $x$ and $\beta_n = f(x)^{n+1}(1/f)^{(n)}(x)/n!$. Comparing coefficients in $f \cdot (1/f) = 1$ gives a recurrence with no division, and the step becomes $a_0\beta_{d-1}/\beta_d$.

```pseudo id=main
HOUSEHOLDER(derivs, d, x0, delta, K):
L1   for k = 1, 2, ..., K:
L2       (f_0, ..., f_d) <- derivs(x);  a_j <- f_j / j!;  fail if any is not finite
L3       if a_0 = 0 then return x, "exact"
L4       beta_0 <- 1;  for n = 1..d:  beta_n <- -(a_1 beta_{n-1} + a_2 a_0 beta_{n-2} + ... + a_n a_0^{n-1} beta_0)
L5       if beta_d = 0 then return x, "zero-denominator"
L6       s <- a_0 beta_{d-1} / beta_d;  if s = 0 then return x, "stalled"
L7       x <- x + s
L8       if |s| <= delta (1 + |x|) then return x, "converged"
L9   return x, "max-iter"
```

Line L4 is the recurrence. With $d = 1$ it gives $\beta_1 = -a_1$ and the step $-f/f'$; with $d = 2$ it gives $\beta_2 = a_1^2 - a_0a_2$ and the step $-2ff'/(2f'^2 - ff'')$, Halley's. For $d = 3$ the step is $a_0(a_1^2 - a_0a_2)/(2a_0a_1a_2 - a_1^3 - a_0^2a_3)$. Near the root $\beta_d \approx (-a_1)^d$, so line L5 fires there only if $f'(x^*) = 0$. Line L6 reports a zero step as "stalled", which for $d \ge 2$ happens at a zero of $f'$, instead of claiming convergence.

## Example

Take Wallis's cubic $f(x) = x^3 - 2x - 5$, with root $x^* = 2.0945514815423265\ldots$, and $x_0 = 2$, so $e_0 = -0.0946$. In 600-digit decimal arithmetic the errors $|e_k|$ are:

| $d$ | order | $\lvert e_1 \rvert$ | $\lvert e_2 \rvert$ | $\lvert e_3 \rvert$ | $e_{k+1}/e_k^{d+1}$ limit |
|---|---|---|---|---|---|
| 1 | 2 | $5.45 \times 10^{-3}$ | $1.66 \times 10^{-5}$ | $1.56 \times 10^{-10}$ | 0.562979 |
| 2 | 3 | $2.12 \times 10^{-4}$ | $2.16 \times 10^{-12}$ | $2.30 \times 10^{-36}$ | 0.227351 |
| 3 | 4 | $6.95 \times 10^{-6}$ | $1.81 \times 10^{-22}$ | $8.28 \times 10^{-89}$ | 0.077554 |
| 4 | 5 | $1.99 \times 10^{-7}$ | $7.36 \times 10^{-36}$ | $5.03 \times 10^{-178}$ | 0.023292 |

The observed orders $\log(e_{k+1}/e_k)/\log(e_k/e_{k-1})$ are 2.000, 3.000, 4.000, 5.000 to three decimals, and the ratios match the constant $(-1)^d f'(x^*)\psi_d$ of the correctness proof. In double precision with $\delta = 10^{-14}$, $d = 1, 2, 3, 4$ need 5, 4, 3, 3 steps, that is 10, 12, 12, 15 values. Under equal costs Newton is the cheapest on this example, and Halley and $d = 3$ tie: at double precision the higher orders overshoot the accuracy that is needed.

## Correctness

If $f \in C^{d+1}$ near a simple root $x^*$, then with $\psi = (x - x^*)/f(x)$, which is $C^d$, the error satisfies the exact identity
$$e_{k+1} = \frac{(-1)^d\,\psi^{(d)}(x_k)}{d!\,T_d(x_k)}\,e_k^{d+1}, \qquad T_d(x_k) \to \psi(x^*) = 1/f'(x^*),$$
so $e_{k+1}/e_k^{d+1} \to (-1)^d f'(x^*)\psi^{(d)}(x^*)/d!$, and the iteration converges from every start close enough to $x^*$. At a root of multiplicity $m$ with $f = (x - x^*)^m h$, $h \in C^d$, $h(x^*) \ne 0$, the convergence is linear with rate $(m - 1)/(m + d - 1)$. The loop stops after at most $K$ steps. The proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

Each step costs one call of the derivative routine ($d + 1$ values) and $O(d^2)$ arithmetic for the recurrence at L4. From a start in the region of order $d + 1$, the number of steps to reach error $\delta$ is about $\log_{d+1}(\log(1/\delta)/\log(1/|e_0|))$. With all values counted equally the efficiency index $(d + 1)^{1/(d+1)}$ is

| $d$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| index | 1.414 | 1.442 | 1.414 | 1.380 | 1.348 |

so Halley's method ($d = 2$) is the best member under that cost model, and Newton's and $d = 3$ tie. If the derivatives cost a fraction of $f$, as when $f$ satisfies a linear differential equation whose recurrence gives all derivatives from two of them, the effective $w$ is near 1 and larger $d$ gains.

## Properties

- Order $d + 1$ at simple roots (local, proved), with the error constant above.
- Linear at multiple roots with rate $(m - 1)/(m + d - 1)$ (local, proved); for $f = x^m$ the iterates shrink by exactly that factor.
- Not bracketing and not globally convergent; on $x^2 + 1$ it wanders until $K$.
- The step uses no division by $f$ or $f'$ except the single division at L6.
- Generic in the number type: the reference code runs unchanged on floats, decimals and fractions.

## Variants and improvements

- The same iteration is often credited to Julius König (1884) and called König's method. Schröder's family of the first kind (1870), the Euler-Chebyshev iterations, is a different family of every order built from $f, \dots, f^{(d)}$; its $d = 2$ member is Chebyshev's method, not Halley's.
- For a root of known multiplicity $m$, Householder's method on $f^{1/m}$ restores order $d + 1$.
- [Laguerre's method](/laguerre-method/) uses $p, p', p''$ of a polynomial and the degree $n$; it has order 3 like $d = 2$ but much better global behaviour for polynomials.
- Multipoint methods such as [Steffensen's](/steffensen-method/), Ostrowski's and King's reach order 4 or more with values of $f$ and $f'$ at several points instead of higher derivatives.

## When to use it

Use $d = 2$ ([Halley](/halley-method/)) or $d = 1$ ([Newton](/newton-raphson-method/)) for ordinary functions. Use larger $d$ when many derivatives come almost free: polynomials evaluated with all derivatives by [Horner's rule](/horner-rule/) in high precision, Taylor-series solvers for differential equations, and multiple precision computation of constants and inverse functions, where fewer steps at full precision save time.

## Pitfalls

- L2: wrong derivative values silently destroy the order; test the routine, or generate the derivatives by automatic differentiation. In floating point, high derivatives of a polynomial can lose relative accuracy.
- L4: with large $|a_0|$ and large $d$ the powers $a_0^{n-1}$ can overflow far from the root; the code raises an error at L6 when the step is not finite.
- L5: for $d = 1$ a zero of $f'$ makes $\beta_1 = 0$ and the method stops with "zero-denominator"; for $d = 2$, starting at $x_0 = 0$ on $x^2 - 2$ gives a zero step and "stalled".
- L7 at a multiple root: the rate is linear, and in floating point the iteration stops near error $u^{1/m}$. For $(x - 1)^2(x + 2)$ from 2 the double precision runs ended with error about $5 \times 10^{-9}$ after 28, 18, 14, 12 steps for $d = 1, \dots, 4$.
- L8: a small step proves nothing far from a root; check $|f(x)|$ afterwards.

## Implementations

## History

Ernst Schröder in 1870 built iterations of every order from the first derivatives of $f$, in a paper that went little noticed for a long time. Alston Householder's 1970 book on single nonlinear equations presented the family based on the derivatives of $1/f$ that now carries his name, with Newton's and Halley's methods as its first two members. Traub's 1964 book had already set out the theory of order, error constants and informational efficiency used to compare such methods.

## References
