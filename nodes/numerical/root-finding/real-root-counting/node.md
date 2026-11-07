---
tag: XC34QE
kind: problem
slug: real-root-counting
name: Real root counting
aliases:
- counting real zeros of a polynomial
- number of real roots in an interval
area: numerical/root-finding
level: advanced
summary: Count the distinct real roots of a real polynomial in an interval, exactly and without computing them, using sign changes of Sturm sequences or Descartes' rule.
prereqs: [polynomial-root-finding, sturm-sequence, descartes-rule-of-signs]
see_also: [sturm-theorem, budan-fourier-theorem, vincent-collins-akritas, real-root-isolation, schur-cohn-test, square-free-factorization, subresultant-gcd, cylindrical-algebraic-decomposition]
sources:
  - book: isbn:9783540330981
    title: Saugata Basu, Richard Pollack and Marie-Françoise Roy, Algorithms in Real Algebraic Geometry, second edition, Springer, 2006
    locator: Chapter 2, Real closed fields (Descartes' law of signs, the Budan-Fourier theorem and Sturm's theorem); Chapter 9, Cartesian and Sturm sequences and the Cauchy index (Hermite's quadratic form and signed subresultants)
  - paper: "C. Sturm, Mémoire sur la résolution des équations numériques, Mémoires présentés par divers savants étrangers à l'Académie Royale des Sciences 6 (1835) 273-318"
    locator: the theorem on the number of real roots between two bounds, presented in 1829
  - paper: doi:10.1145/800205.806346
    title: "G. E. Collins and A. G. Akritas, Polynomial real root isolation using Descartes' rule of signs, Proceedings of SYMSAC 1976, 272-275"
    locator: counting by Descartes' rule after Möbius transformations
  - paper: doi:10.1090/S0002-9904-1943-07912-8
    title: "M. Kac, On the average number of real roots of a random algebraic equation, Bulletin of the American Mathematical Society 49 (1943) 314-320"
    locator: the asymptotic (2/π) log n for Gaussian coefficients
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 5.3, Algorithms for the symmetric eigenproblem (bisection by counting negative pivots and Sylvester's inertia theorem)
---

Real root counting asks how many real roots a real polynomial $p$ has in an interval $(a, b]$, or on the whole line, without computing them. Unlike root finding, it can be solved exactly, in rational arithmetic, by a finite computation. The classical answer is [Sturm's theorem](/sturm-theorem/): the number of distinct real roots in $(a, b]$ is $V(a) - V(b)$, where $V(x)$ counts the sign changes in the [Sturm sequence](/sturm-sequence/) of $p$ evaluated at $x$. [Descartes' rule of signs](/descartes-rule-of-signs/) gives a cheaper upper bound that becomes exact after suitable changes of variable, which is the basis of the [Vincent-Collins-Akritas method](/vincent-collins-akritas/). Counting is the decision step of [real root isolation](/real-root-isolation/), of eigenvalue bisection for symmetric matrices, and of the real algebraic geometry behind [cylindrical algebraic decomposition](/cylindrical-algebraic-decomposition/).

## In plain words

Sometimes one only needs to know how many times a curve crosses the axis between two points, not where. For polynomials this can be answered exactly, with fractions and no rounding, by a short recipe. Build a list of polynomials from $p$ and its derivative by repeated division, as in Euclid's algorithm for whole numbers. Evaluate the list at the left end and count how often the signs switch, then do the same at the right end. The difference of the two counts is the number of roots in between. Repeated halving of the interval with such counts then pins every root down.

## Definition

**Input.** A polynomial $p(x) = a_n x^n + \cdots + a_0$ with real, usually rational, coefficients, $a_n \ne 0$, and an interval $(a, b]$ with $a < b$, where $a = -\infty$ and $b = +\infty$ are allowed.

**Output.** The number of distinct real $x$ with $a < x \le b$ and $p(x) = 0$; in the variant with multiplicity, the number of roots counted with multiplicity.

Notation on the root-finding pages: $p$ is the polynomial, $n$ its degree, $x^*$ a root and $m$ its multiplicity. For a sequence of real numbers, $\operatorname{Var}$ is the number of sign changes after zeros are deleted. For a sequence of polynomials $P = (p_0, \ldots, p_r)$, $V_P(x) = \operatorname{Var}(p_0(x), \ldots, p_r(x))$. The Sturm sequence of $p$ is $p_0 = p$, $p_1 = p'$, $p_{i+1} = -\operatorname{rem}(p_{i-1}, p_i)$ until the remainder is $0$.

## Variants

- **Whole line or half-line.** Use the signs of the leading coefficients for $V(\pm\infty)$.
- **With multiplicity.** Count distinct roots of each factor of the [square-free factorization](/square-free-factorization/) and weight by multiplicity.
- **Sign conditions.** Count the roots of $p$ at which another polynomial $q$ is positive, or negative: the Sturm-Tarski theorem, which uses the sequence of $p$ and $p'q$.
- **Complex roots in a region.** Count roots in the open left half-plane (Routh-Hurwitz) or in the unit disc (the [Schur-Cohn test](/schur-cohn-test/)).
- **Characteristic polynomials.** Count the eigenvalues of a symmetric matrix below $\sigma$ without forming the polynomial: by Sylvester's law of inertia this is the number of negative pivots in the $LDL^T$ factorization of $A - \sigma I$.

## Examples

**Three real roots (computed).** For $p = x^3 - 3x + 1$ the Sturm sequence is
$$p_0 = x^3 - 3x + 1, \quad p_1 = 3x^2 - 3, \quad p_2 = 2x - 1, \quad p_3 = \tfrac94.$$
At $x = -2$ the values are $-1, 9, -5, \frac94$, with $V = 3$; at $0$ they are $1, -3, -1, \frac94$, with $V = 2$; at $2$ they are $3, 9, 3, \frac94$, with $V = 0$. So $p$ has one root in $(-2, 0]$ and two in $(0, 2]$: they are $-1.879$, $0.347$ and $1.532$. Descartes' rule gives the same answer for the positive roots: the coefficients $1, 0, -3, 1$ have 2 sign changes, so there are 2 or 0 positive roots.

**One real root (computed).** For $p = x^5 - x - 1$ the Sturm sequence is $x^5 - x - 1$, $5x^4 - 1$, $\frac45 x + 1$, $-\frac{2869}{256}$. The leading coefficients give $V(-\infty) = 2$ and $V(+\infty) = 1$, so $p$ has exactly one real root, which lies in $(0, 2]$ since $V(0) - V(2) = 2 - 1$.

**Descartes is only a bound.** For $x^2 - x + 1$ the coefficients have 2 sign changes but there are no real roots; the excess over the true count is always even.

**Random polynomials.** For $p$ with independent standard Gaussian coefficients, the expected number of real roots is $\frac{2}{\pi}\ln n + O(1)$ (Kac, 1943), so most roots of a random polynomial are not real.

## Known algorithms

| method | output | cost | notes |
|---|---|---|---|
| [Sturm sequences](/sturm-sequence/) | exact count in $(a, b]$ | $O(n^2)$ arithmetic operations to build, $O(n^2)$ per evaluation point | coefficient growth makes exact arithmetic expensive; use [subresultants](/subresultant-gcd/) (Sturm-Habicht sequences) |
| [Descartes' rule](/descartes-rule-of-signs/) | upper bound on positive roots | $O(n)$ | exact when it gives 0 or 1 |
| [Budan-Fourier theorem](/budan-fourier-theorem/) | upper bound in $(a, b]$ | $O(n^2)$ | uses the derivatives $p, p', \ldots, p^{(n)}$ |
| [Vincent-Collins-Akritas](/vincent-collins-akritas/) | exact counts by subdivision | polynomial in $n$ and the coefficient size | Descartes' rule after Möbius maps of the interval to $(0, \infty)$ |
| Hermite's quadratic form | number of distinct real roots | $O(n^2)$ for the matrix and one signature | the signature of the Hankel matrix of power sums $s_{i+j}$ of the roots |
| Negative pivot count | eigenvalues of a symmetric tridiagonal matrix below $\sigma$ | $O(n)$ | numerically stable, the basis of eigenvalue bisection |

## Bounds

- **Exactness (proved).** Sturm's theorem: if $p$ is square-free and $p(a)p(b) \ne 0$, the number of roots in $(a, b)$ is $V(a) - V(b)$; with the convention of deleted zeros the count for $(a, b]$ holds for any $a < b$, also for multiple roots, counting each distinct root once.
- **Descartes (proved).** The number of positive roots counted with multiplicity is at most $\operatorname{Var}(a_n, \ldots, a_0)$ and has the same parity. Hence a polynomial with $k$ nonzero terms has at most $2k - 1$ distinct real roots.
- **Vincent's theorem (proved).** After enough continued-fraction or bisection substitutions every interval maps to a polynomial whose Descartes count is 0 or 1, so the subdivision terminates.
- **Average (proved).** About $\frac{2}{\pi}\ln n$ real roots for Gaussian coefficients (Kac); about $\sqrt n$ for the Kostlan-Shub-Smale distribution with variances $\binom{n}{i}$.
- **Floating point.** Counts computed from rounded coefficients can be wrong near multiple or clustered roots, since an arbitrarily small change of coefficients can create or remove a pair of real roots, as in $x^2 - \varepsilon$. Exact arithmetic, or interval arithmetic with a fallback, is used when the count must be certain.

## Reductions

- **Counting to sign evaluation.** With the Sturm sequence precomputed, each count is two evaluations of the sequence and a sign count.
- **Interval to half-line.** The Möbius substitution $x = (a + bt)/(1 + t)$ maps $(a, b)$ to $t \in (0, \infty)$, after which Descartes' rule bounds the count.
- **Distinct roots to square-free.** Replace $p$ by $p/\gcd(p, p')$, which has the same distinct roots, all simple.
- **Isolation to counting.** [Real root isolation](/real-root-isolation/) bisects intervals until each count is 0 or 1.
- **Eigenvalues to counting.** The $k$-th eigenvalue of a symmetric matrix is found by bisection on $\sigma$ using the count of negative pivots of $A - \sigma I$ (Demmel, Section 5.3).

## Applications

- **Real root isolation and refinement** in computer algebra systems.
- **Eigenvalue bisection** for symmetric tridiagonal matrices, which finds selected eigenvalues to high relative accuracy.
- **Quantifier elimination and cylindrical algebraic decomposition**, where counts of real roots with sign conditions decide formulas over the reals.
- **Stability and control**, where counting roots in a half-plane or disc decides stability without computing poles.
- **Geometry and robotics**, to count real solutions of kinematic and intersection problems.

## References
