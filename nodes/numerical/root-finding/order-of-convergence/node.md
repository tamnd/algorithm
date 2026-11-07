---
tag: W4DV73
kind: definition
slug: order-of-convergence
name: Order of convergence
aliases:
- rate of convergence
- linear and quadratic convergence
- Q-order
- convergence order
area: numerical/root-finding
level: intro
summary: "A sequence has order q and rate constant C when |e_(k+1)| / |e_k|^q tends to C. Order 1 is linear, order 2 quadratic; q^(1/w) compares methods with w evaluations per step."
prereqs: [root-finding-problem, asymptotic-notation]
see_also: [quadratic-convergence, newton-raphson-method, secant-method, bisection-method, fixed-point-iteration, multiplicity-of-roots, aitken-delta-squared, stopping-criteria]
sources:
  - book: isbn:9780898714616
    title: J. M. Ortega and W. C. Rheinboldt, Iterative Solution of Nonlinear Equations in Several Variables, SIAM Classics in Applied Mathematics 30, 2000
    locator: Chapter 9, Rates of convergence, general (Q-factors, R-factors, Q-order and R-order)
  - book: isbn:9780898713640
    title: John E. Dennis Jr. and Robert B. Schnabel, Numerical Methods for Unconstrained Optimization and Nonlinear Equations, SIAM Classics in Applied Mathematics 16, 1996
    locator: Section 2.3, Convergence of sequences of real numbers (q-linear, q-superlinear and q-order convergence)
  - book: "A. M. Ostrowski, Solution of Equations and Systems of Equations, second edition, Academic Press, 1966"
    locator: Chapter 3, Method of false position (regula falsi), the section on Horner units and the efficiency index
  - book: isbn:9780828403122
    title: J. F. Traub, Iterative Methods for the Solution of Equations, Prentice-Hall, 1964 (reprinted by AMS Chelsea)
    locator: Chapter 1, General preliminaries, and Section 2.2, Linear and superlinear convergence
  - paper: "F. A. Potra, On Q-order and R-order of convergence, Journal of Optimization Theory and Applications 63(3), 415-431, 1989"
    locator: the relations between the Q-order and the R-order of a sequence
---

The order of convergence measures how fast the errors $e_k = x_k - x^*$ of a convergent sequence shrink: a sequence has order $q$ when each error is about a constant times the $q$-th power of the one before. Order 1 is *linear* convergence, in which each step gains a fixed number of correct digits, and order 2 is [quadratic convergence](/quadratic-convergence/), in which each step about doubles the number of correct digits. Together with the number of function evaluations per step, the order decides which [root-finding](/root-finding-problem/) method is cheapest near a root.

## Definition

Notation on the root-finding pages: $f$ is the function, $x^*$ a root, $x_k$ the iterates, $e_k = x_k - x^*$ the error; $w$ is the number of evaluations of $f$ (and of $f'$ where used) in one step.

Let $(x_k)$ be a sequence of real or complex numbers, or of vectors with a norm, with $x_k \to x^*$ and $e_k \ne 0$ for all $k$.

- **Q-order.** The sequence converges with *order* $q \ge 1$ and *rate constant* (asymptotic error constant) $C$ when
$$\lim_{k \to \infty} \frac{|e_{k+1}|}{|e_k|^q} = C, \qquad 0 < C < \infty,$$
and, in the case $q = 1$, also $C < 1$. Then $|e_{k+1}| \approx C |e_k|^q$ for large $k$.
- **Linear, superlinear, sublinear.** The sequence converges *linearly* with rate $C$ when the limit above exists for $q = 1$ with $0 < C < 1$. It converges *superlinearly* when $|e_{k+1}|/|e_k| \to 0$, and *sublinearly* when $|e_{k+1}|/|e_k| \to 1$.
- **At least order $q$.** The sequence has Q-order *at least* $q$ when there are $C$ and $k_0$ with $|e_{k+1}| \le C |e_k|^q$ for all $k \ge k_0$ (and $C < 1$ when $q = 1$). Many theorems prove this weaker form.
- **R-order.** The sequence has R-order at least $q$ when $|e_k| \le \beta_k$ for a sequence $\beta_k \to 0$ that has Q-order at least $q$. This covers methods whose error does not fall in each step but is bounded by a quantity that does, such as the [bisection method](/bisection-method/). Ortega and Rheinboldt (Chapter 9) give the general definitions by Q-factors and R-factors.
- **Efficiency index.** A method of order $q$ that makes $w$ evaluations in each step has efficiency index $E = q^{1/w}$ (Ostrowski, Chapter 3).

**The order is unique.** If the limit above exists with $0 < C < \infty$ for $q$, and $q' > q$, then
$$\frac{|e_{k+1}|}{|e_k|^{q'}} = \frac{|e_{k+1}|}{|e_k|^{q}} \cdot |e_k|^{q - q'} \to \infty,$$
because the first factor tends to $C > 0$ and $|e_k|^{q - q'} \to \infty$ as $e_k \to 0$. For $q' < q$ the same product tends to $0$. So at most one $q$ gives a finite positive limit.

**Why the efficiency index.** With order $q$, the number of correct digits $d_k = -\log_{10} |e_k|$ satisfies $d_{k+1} \approx q\, d_k - \log_{10} C$, so for large $d_k$ it grows by the factor $q$ in each step. After $N$ evaluations, that is $N/w$ steps, it has grown by the factor $q^{N/w} = (q^{1/w})^N$. So $q^{1/w}$ is the growth factor of the correct digits per evaluation, and a method with a larger index needs fewer evaluations for many digits.

**The observed order.** When three errors are known, the order is estimated by
$$q_k = \frac{\log(|e_{k+1}| / |e_k|)}{\log(|e_k| / |e_{k-1}|)}.$$
When $x^*$ is not known, the steps $x_{k+1} - x_k$ replace the errors; for a superlinear method $|x_{k+1} - x_k| / |e_k| \to 1$.

## Examples and non-examples

Take $f(x) = x^3 - x - 2$, whose real root is $x^* = 1.5213797068045675696\ldots$, and compute in 120-digit decimal arithmetic.

| $k$ | Newton, $x_0 = 1.5$: $\lvert e_k \rvert$ | $q_k$ | secant, $x_0 = 1, x_1 = 2$: $\lvert e_k \rvert$ | $q_k$ | fixed point $x \leftarrow (x + 2)^{1/3}$: $\lvert e_k \rvert$ | $q_k$ |
|---|---|---|---|---|---|---|
| 0 | $2.137971 \cdot 10^{-2}$ | | $5.213797 \cdot 10^{-1}$ | | $2.137971 \cdot 10^{-2}$ | |
| 1 | $3.594236 \cdot 10^{-4}$ | | $4.786203 \cdot 10^{-1}$ | | $3.085221 \cdot 10^{-3}$ | |
| 2 | $9.916022 \cdot 10^{-8}$ | 2.006 | $1.880464 \cdot 10^{-1}$ | | $4.444436 \cdot 10^{-4}$ | 1.001 |
| 3 | $7.550408 \cdot 10^{-15}$ | 2.000 | $5.869314 \cdot 10^{-2}$ | 1.246 | $6.400861 \cdot 10^{-5}$ | 1.000 |
| 4 | $4.377603 \cdot 10^{-29}$ | 2.000 | $9.789725 \cdot 10^{-3}$ | 1.538 | $9.218167 \cdot 10^{-6}$ | 1.000 |
| 5 | $1.471527 \cdot 10^{-57}$ | 2.000 | $4.532863 \cdot 10^{-4}$ | 1.716 | $1.327543 \cdot 10^{-6}$ | 1.000 |
| 6 | | | $3.390135 \cdot 10^{-6}$ | 1.593 | $1.911842 \cdot 10^{-7}$ | 1.000 |
| 7 | | | $1.180304 \cdot 10^{-9}$ | 1.627 | $2.753313 \cdot 10^{-8}$ | 1.000 |
| 8 | | | $3.072608 \cdot 10^{-15}$ | 1.615 | $3.965145 \cdot 10^{-9}$ | 1.000 |

- **Quadratic.** [Newton's method](/newton-raphson-method/) has order 2 at this simple root. Its rate constant is $C = |f''(x^*) / (2 f'(x^*))| = 0.76788\ldots$, and the number of correct digits about doubles in each step. With $w = 2$ (one $f$, one $f'$) its index is $2^{1/2} \approx 1.414$.
- **Superlinear of order 1.618.** The [secant method](/secant-method/) has order $\varphi = (1 + \sqrt 5)/2 \approx 1.618$ at a simple root, with $|e_{k+1}| \approx C^{\varphi - 1} |e_k|^{\varphi}$ and $C$ as for Newton. The observed $q_k$ oscillates and settles near $1.618$. With $w = 1$ its index is $1.618$, larger than Newton's.
- **Linear.** The [fixed-point iteration](/fixed-point-iteration/) $x \leftarrow g(x) = (x + 2)^{1/3}$ converges linearly with $C = |g'(x^*)| = 1/(3 x^{*2}) = 0.14401\ldots$. Each step gains about $-\log_{10} 0.144 \approx 0.84$ digits.
- **Linear at a multiple root.** Newton's method at a root of [multiplicity](/multiplicity-of-roots/) $m \ge 2$ converges linearly with $C = 1 - 1/m$, so $C = 1/2$ at a double root.
- **Sublinear.** The sequence $x_k = 1/k$ tends to $0$ with $|e_{k+1}|/|e_k| = k/(k+1) \to 1$. It has no order $q \ge 1$ in the sense above.
- **Non-example: R-linear but not Q-linear.** Let $e_{2j} = e_{2j+1} = 4^{-j}$. The ratios $|e_{k+1}|/|e_k|$ alternate between $1$ and $1/4$, so no limit exists, and the sequence is not Q-linear. But $|e_k| \le 2 \cdot 2^{-k}$, so it has R-order 1 with R-rate $1/2$. The bisection midpoints behave in this way: their errors can grow in some steps, and only the bound $(b - a)/2^{k+1}$ falls by the factor $1/2$ in each step.
- **Non-example: order 2 needs $e_k \to 0$ fast enough from the start.** The bound $|e_{k+1}| \le C |e_k|^2$ alone does not make the errors fall: it gives $|e_{k+1}| \le |e_k|$ only when $C |e_k| \le 1$. This is why local results need a starting point close enough.

## Related definitions

- [Quadratic convergence](/quadratic-convergence/): the case $q = 2$, with its proof for Newton's method.
- [Multiplicity of a root](/multiplicity-of-roots/): the main cause of a drop from order 2 to order 1.
- [Aitken's delta-squared process](/aitken-delta-squared/): turns a linearly convergent sequence into a faster one; [Steffensen's method](/steffensen-method/) builds it into an iteration of order 2.
- [Stopping criteria](/stopping-criteria/): for a superlinear method the last step $|x_{k+1} - x_k|$ is a good estimate of $|e_k|$, which a stopping rule uses.
- [Order of growth](/order-of-growth/): the order of a running time, a different notion with a similar name.

## References
