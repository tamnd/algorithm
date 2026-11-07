---
tag: WF4CKY
kind: problem
slug: root-finding-problem
name: Root-finding problem
aliases:
- zero finding
- solving f(x)=0
- nonlinear equation in one variable
area: numerical/root-finding
level: intro
summary: Given a function f and some information about it (a bracket, a starting point, derivatives), find a point x with f(x) = 0, or a point within a stated tolerance of such a root.
prereqs: [floating-point-arithmetic, relative-error]
see_also: [bisection-method, newton-raphson-method, brent-method, order-of-convergence, stopping-criteria, root-conditioning, polynomial-root-finding, systems-of-nonlinear-equations]
sources:
  - book: isbn:9780898713640
    title: John E. Dennis Jr. and Robert B. Schnabel, Numerical Methods for Unconstrained Optimization and Nonlinear Equations, SIAM Classics in Applied Mathematics 16, 1996
    locator: Chapter 2, Nonlinear problems in one variable (Section 2.1, What is not possible; Section 2.5, globally convergent methods)
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 1, Solution of equations by iteration
  - book: isbn:9780828403122
    title: J. F. Traub, Iterative Methods for the Solution of Equations, Prentice-Hall, 1964 (reprinted by AMS Chelsea)
    locator: Chapter 1, General preliminaries (order and classes of iteration functions); Chapter 5, One-point iteration functions; Appendix C, Significant figures and computational efficiency
  - paper: "K. Sikorski, Bisection is optimal, Numerische Mathematik 40, 111-117, 1982"
    locator: the worst-case optimality of bisection over continuous functions with a sign change
  - paper: doi:10.1145/321850.321860
    title: H. T. Kung and J. F. Traub, Optimal order of one-point and multipoint iteration, Journal of the ACM 21(4), 643-651, 1974
    locator: the conjecture that a multipoint method without memory that uses n evaluations has order at most 2^(n-1)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 5.1, Horner's method (the error bound of a computed polynomial value)
---

The root-finding problem asks for a point $x^*$ with $f(x^*) = 0$, for a given function $f$ of one real or complex variable. In practice the input also holds some information about $f$, for example a [bracket](/bracketing-method/) on which $f$ changes sign, a starting point near a root, or a way to compute the derivative $f'$, and the output is a point within a stated tolerance of a root. The answer depends on this information: with a bracket and continuity, [bisection](/bisection-method/) always succeeds, and with only a starting point no method can guarantee success.

## In plain words

You have a function that you can compute but cannot invert by a formula. You want an input that makes the output zero. For example, you want the angle at which the cosine of the angle equals the angle itself. A computer cannot try every number, so a method evaluates the function at a few points and uses the answers to choose the next point. Some methods keep an interval in which the sign of the function changes, and make it smaller step by step. They are slow but safe. Other methods use the slope of the function near a guess, and jump to where a straight line through the guess crosses zero. They are very fast when the guess is good, but can go wrong when it is not. The work is counted as the number of function evaluations.

## Definition

Notation on the root-finding pages. $f$ is the function, $x^*$ a root, $x_k$ the iterates and $e_k = x_k - x^*$ the error. A method has [order](/order-of-convergence/) $q \ge 1$ and rate constant $C$ when $|e_{k+1}| \approx C |e_k|^q$, with $0 < C < 1$ when $q = 1$. A root has [multiplicity](/multiplicity-of-roots/) $m$ when $f(x^*) = \cdots = f^{(m-1)}(x^*) = 0 \ne f^{(m)}(x^*)$, and it is *simple* when $m = 1$. A *bracket* is an interval $[a, b]$ with $f(a) f(b) < 0$. The *tolerance* $\delta > 0$ and the *stopping rule* decide when the method stops ([stopping criteria](/stopping-criteria/)). For a system, $F : \mathbb{R}^n \to \mathbb{R}^n$ has Jacobian $J(x) = F'(x)$. The cost is the number of evaluations of $f$, and of $f'$ or $J$ where a method uses them. A method of order $q$ that makes $w$ evaluations in each step has *efficiency index* $q^{1/w}$ (Ostrowski).

**The bracketed problem.** The input is a function $f : [a, b] \to \mathbb{R}$ that is continuous, a bracket $[a, b]$ and a tolerance $\delta > 0$. The output is a point $\hat x \in [a, b]$ such that some root $x^*$ of $f$ in $[a, b]$ satisfies $|\hat x - x^*| \le \delta$. By the intermediate value theorem a root exists, so this problem always has a solution.

**The local problem.** The input is $f$, a starting point $x_0$ (or two points), and the derivative $f'$ where the method needs it. The output is a point $\hat x$ with $|\hat x - x^*| \le \delta$ for a root $x^*$, or a report of failure. The usual guarantee is local: if $f \in C^2$ near a simple root $x^*$ and $x_0$ is close enough to $x^*$, the method converges to $x^*$.

**What the output certifies.** A test $|f(\hat x)| \le \varepsilon$ on the *residual* does not bound $|\hat x - x^*|$ unless $f$ is known to be steep near the root. A bracket of width at most $2\delta$ does bound it. This difference is the subject of [root conditioning](/root-conditioning/).

## Variants

- **Find one root, or find all roots.** Most methods on these pages find one root. To find all roots in an interval, a method needs extra information, such as a bound on $|f'|$, or the structure of a polynomial ([real root isolation](/real-root-isolation/), [real root counting](/real-root-counting/)).
- **Polynomials.** For a polynomial $p$ of degree $n$, all $n$ complex roots exist and can be found together. This is [polynomial root finding](/polynomial-root-finding/).
- **Systems.** For $F : \mathbb{R}^n \to \mathbb{R}^n$, the problem is a [system of nonlinear equations](/systems-of-nonlinear-equations/). There is no bracket in more than one dimension, so global methods are much harder.
- **Fixed points.** The equation $x = g(x)$ is the root problem for $f(x) = x - g(x)$. See [fixed-point iteration](/fixed-point-iteration/).
- **Decision.** Does $f$ have a root in $[a, b]$? For a continuous $f$ given only by evaluations, this cannot be decided from finitely many values (see Bounds).

## Examples

| $f(x)$ | information | root $x^*$ | remark |
|---|---|---|---|
| $\cos x - x$ | bracket $[0, 1]$ | $0.7390851332151607$ | simple root, $f'(x^*) = -1.674$ |
| $e^x - 2$ | bracket $[0, 1]$ | $\ln 2 = 0.6931471805599453$ | simple root |
| $x^3 - x - 2$ | bracket $[1, 2]$ | $1.5213797068045676$ | the only real root |
| $E - 0.5 \sin E - 1$ | start $E_0 = 1$ | $1.4987011335178484$ | Kepler's equation, $e = 0.5$, $M = 1$ |
| $(x - 1)^2$ | none | $1$, multiplicity 2 | no sign change, so no bracket exists |
| $1/(x - 1/3)$ | signs differ on $[0, 1]$ | none | a pole, not a root |
| $x^2 + 1$ | none | $\pm i$ | no real root; complex methods find it |

**Non-example of a well-posed output.** Take $p(x) = x^3 - 3x^2 + 3x - 1 = (x - 1)^3$, evaluated by [Horner's rule](/horner-rule/) in binary64. On the grid $1 + j \cdot 10^{-7}$, $|j| \le 2000$, the computed value is zero or has the wrong sign at 57 points, and these spread over the interval from $1 - 5.5 \cdot 10^{-6}$ to $1 + 5.5 \cdot 10^{-6}$. So no method that uses the computed values of $p$ can place the triple root more closely than about $10^{-5}$, although the unit roundoff is $u = 2^{-53} \approx 1.1 \cdot 10^{-16}$. For a simple root the same effect is smaller: the computed values can be wrong in sign only on an interval of radius about $\varepsilon_f / |f'(x^*)|$, where $\varepsilon_f \approx u \max |f|$ over the terms, is the rounding error of the computed $f$.

## Known algorithms

Bracketing methods, which keep a sign change and converge for each continuous $f$:

- [Bisection](/bisection-method/): one evaluation per step, the bracket halves; linear with rate $1/2$.
- [Regula falsi](/regula-falsi/): the secant point of the ends; linear, can be slow. The [Illinois method](/illinois-method/) fixes it with order $3^{1/3} \approx 1.442$ per evaluation.
- [Ridders' method](/ridders-method/): two evaluations per step, order 2 per step, index $2^{1/2}$.
- [Dekker's method](/dekker-method/), [Brent's method](/brent-method/) and [Chandrupatla's method](/chandrupatla-method/): fast interpolation steps with a bisection safeguard; superlinear at a simple root.
- [Newton bisection hybrid](/newton-bisection-hybrid/): Newton steps inside a bracket.

Open methods, which need a good start and converge locally:

- [Newton's method](/newton-raphson-method/): order 2 at a simple root, $w = 2$ (one $f$ and one $f'$), index $2^{1/2} \approx 1.414$.
- [Secant method](/secant-method/): order $(1 + \sqrt 5)/2 \approx 1.618$, $w = 1$, index $1.618$.
- [Steffensen's method](/steffensen-method/): order 2 without derivatives, $w = 2$.
- [Muller's method](/muller-method/): order about $1.839$, $w = 1$; finds complex roots from real starts.
- [Halley's method](/halley-method/) and [Householder's methods](/householder-methods/): order 3 and higher with more derivatives.
- [Inverse quadratic interpolation](/inverse-quadratic-interpolation/): order about $1.839$, $w = 1$.
- [Fixed-point iteration](/fixed-point-iteration/): linear when $|g'(x^*)| < 1$.

## Bounds

- **No guarantee without a bracket.** Let a method evaluate a continuous $f$ at finitely many points and see only nonzero values of one sign. Then a continuous function with the same values and a root exists, and so does one with no root. So no such method can decide whether a root exists, and no method can guarantee to find one (Dennis and Schnabel, Section 2.1).
- **Bisection is optimal for continuous functions.** Sikorski (1982) proved that, over all continuous $f$ on $[a, b]$ with $f(a) f(b) < 0$, no method that uses $n$ values of $f$, adaptively chosen or not, has a smaller worst-case error than bisection, which reaches $(b - a)/2^{n+1}$. This is a lower bound in the worst case over the class.
- **Order and information.** For one-point methods without memory that use $f, f', \ldots, f^{(s-1)}$ at the current point, the order is at most $s$ (Traub, Chapter 5). Kung and Traub (1974) gave multipoint methods without memory with $n$ evaluations and order $2^{n-1}$, and conjectured that no such method has a higher order. The conjecture is open in general.
- **Limiting accuracy.** In floating point with unit roundoff $u$, a method that sees only computed values of $f$ cannot in general find a simple root more closely than about $\varepsilon_f / |f'(x^*)|$, and a root of multiplicity $m$ more closely than about $(m!\, \varepsilon_f / |f^{(m)}(x^*)|)^{1/m}$. Here $\varepsilon_f$ is the error of the computed $f$; for a polynomial by Horner's rule it is at most $\gamma_{2n} \sum_i |a_i| |x|^i$ (Higham, Section 5.1).

## Reductions

- **To a fixed-point problem.** $f(x) = 0$ if and only if $x = x - \lambda(x) f(x)$, for any $\lambda$ with $\lambda(x) \ne 0$. Newton's method is the choice $\lambda = 1/f'$.
- **To minimization.** The roots of $f$ are the global minima of $f^2$ with value 0. The converse fails: a local minimum of $f^2$ with a positive value is not a root, and descent methods can stop there.
- **From inversion.** To compute $g^{-1}(y)$, find the root of $f(x) = g(x) - y$. Square roots ([Newton square root](/newton-square-root/)) and reciprocals ([Newton-Raphson division](/newton-raphson-division/)) are this case.
- **From eigenvalues and to eigenvalues.** The roots of a monic polynomial are the eigenvalues of its companion matrix ([companion matrix method](/companion-matrix-method/)). Conversely, the eigenvalues of a matrix are the roots of its characteristic polynomial, but that route is numerically poor ([Wilkinson's polynomial](/wilkinson-polynomial/)).

## Applications

- Square roots, reciprocals and other elementary functions in floating-point libraries.
- Kepler's equation $M = E - e \sin E$ for the position of a body in an orbit.
- The internal rate of return of a cash flow, a root of $\sum_k c_k (1 + r)^{-k}$.
- Inverse distribution functions in statistics and random number generation.
- Implicit steps in methods for differential equations, which solve a nonlinear system in each step.
- Ray and surface intersection in computer graphics.

## References
