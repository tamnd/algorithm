---
tag: 2H8X7C
kind: theorem
slug: chebyshev-equioscillation-theorem
name: Chebyshev equioscillation theorem
aliases:
- Alternation theorem
- Chebyshev alternation theorem
- equioscillation theorem
- characterization of best uniform approximation
area: numerical/interpolation-and-approximation
level: advanced
summary: A polynomial p of degree at most n is the best uniform approximation to a continuous f on [a, b] if and only if f - p attains its maximum modulus with alternating signs at n + 2 points.
prereqs: [minimax-approximation, polynomial]
see_also: [remez-algorithm, minimax-approximation, chebyshev-polynomials, chebyshev-economization, weierstrass-approximation-theorem, approximation-theory, chebyshev-interpolation, lebesgue-constant]
sources:
  - book: isbn:9780821813744
    title: E. W. Cheney, Introduction to Approximation Theory, second edition, AMS Chelsea, 1998
    locator: Chapter 3, Tchebycheff approximation (the alternation theorem, uniqueness, the Haar condition and the de la Vallée Poussin bound)
  - book: isbn:9780521295147
    title: M. J. D. Powell, Approximation Theory and Methods, Cambridge University Press, 1981
    locator: Chapter 7, The theory of minimax approximation (characterization, uniqueness and the Haar condition)
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 10, Best approximation (Theorem 10.1, equioscillation)
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 8, Polynomial approximation in the maximum norm (the oscillation theorem and the de la Vallée Poussin theorem)
  - book: isbn:9780471628965
    title: Theodore J. Rivlin, Chebyshev Polynomials, second edition, Wiley, 1990
    locator: Chapter 1 and Chapter 2, the extremal properties of T_n and best uniform approximation
  - paper: "P. L. Chebyshev, Théorie des mécanismes connus sous le nom de parallélogrammes, Mémoires des savants étrangers présentés à l'Académie de Saint-Pétersbourg 7 (1854) 539-568"
    locator: the origin of best uniform approximation and of the polynomials of least deviation from zero
  - paper: "A. Haar, Die Minkowskische Geometrie und die Annäherung an stetige Funktionen, Mathematische Annalen 78 (1918) 294-311"
    locator: uniqueness of best approximations holds for all f exactly under the Haar condition
---

The Chebyshev equioscillation theorem characterizes the best uniform approximation. A polynomial $p^*$ of degree at most $n$ minimizes $\max_{x \in [a, b]}|f(x) - p(x)|$ over all such polynomials exactly when the error $f - p^*$ reaches its largest absolute value at $n + 2$ points, with signs that alternate from one point to the next. The best approximation exists and is unique. The theorem turns an optimization problem into a set of equations that the [Remez algorithm](/remez-algorithm/) solves. Its simplest case shows that $2^{-n}T_{n+1}$ is the monic polynomial of degree $n + 1$ with the smallest maximum on $[-1, 1]$.

## Statement

Notation on the interpolation and approximation pages: $f$ is a function on $[a, b]$, usually $[-1, 1]$; $\mathcal{P}_n$ is the space of real polynomials of degree at most $n$; $\|g\| = \max_{a \le x \le b}|g(x)|$; $E_n(f) = \min_{p \in \mathcal{P}_n}\|f - p\|$ is the best approximation error; $T_k$ are the [Chebyshev polynomials](/chebyshev-polynomials/).

**Theorem.** Let $f$ be real and continuous on $[a, b]$, $a < b$, and $n \ge 0$.

1. *(Existence.)* There is a $p^* \in \mathcal{P}_n$ with $\|f - p^*\| = E_n(f)$.
2. *(Characterization.)* A polynomial $p \in \mathcal{P}_n$ satisfies $\|f - p\| = E_n(f)$ if and only if there are points $a \le \xi_0 < \xi_1 < \cdots < \xi_{n+1} \le b$ and a sign $\sigma \in \{+1, -1\}$ with
$$f(\xi_i) - p(\xi_i) = \sigma(-1)^i\|f - p\|, \qquad i = 0, 1, \ldots, n + 1.$$
3. *(Uniqueness.)* The best approximation $p^*$ is unique.

**Companion bound (de la Vallée Poussin).** If $p \in \mathcal{P}_n$ and $f - p$ takes nonzero values of alternating sign at $n + 2$ points $\xi_0 < \cdots < \xi_{n+1}$, then
$$\min_i|f(\xi_i) - p(\xi_i)| \le E_n(f) \le \|f - p\|.$$

The points $\xi_i$ are called an alternation set or reference. The theorem holds unchanged when $[a, b]$ is replaced by any compact subset of $\mathbb{R}$ with at least $n + 2$ points, for example a finite grid, and when $\mathcal{P}_n$ is replaced by any $(n + 1)$-dimensional space of continuous functions satisfying the Haar condition (every nonzero element has at most $n$ zeros on the set).

## In plain words

Suppose you want the polynomial of a given degree whose graph stays as close as possible to a curve everywhere at once, so that the worst gap is as small as it can be. The theorem says how to recognize the winner: its error curve swings back and forth between the same largest value above and below zero, touching those two levels alternately at least two more times than the degree. If the error peaks are uneven, or do not alternate often enough, you can always nudge the polynomial to shave down the largest peaks, so it was not the best. There is exactly one winner.

## Proof

Write $e = f - p$ and $E = \|e\|$.

**Existence.** Fix $p_0 \in \mathcal{P}_n$. A best approximation, if any, lies in $K = \{p \in \mathcal{P}_n : \|f - p\| \le \|f - p_0\|\}$. This set is closed and bounded (by $\|p\| \le \|f\| + \|f - p_0\|$ in the maximum norm on $[a, b]$, which is a norm on the finite-dimensional space $\mathcal{P}_n$), hence compact, and $p \mapsto \|f - p\|$ is continuous. So the minimum over $K$ is attained.

**Sufficiency and the de la Vallée Poussin bound.** Let $e(\xi_i)$ alternate in sign at $\xi_0 < \cdots < \xi_{n+1}$, and suppose some $q \in \mathcal{P}_n$ had $\|f - q\| < \min_i|e(\xi_i)|$. Then $q - p = (f - p) - (f - q)$ has the sign of $e(\xi_i)$ at every $\xi_i$, because $|f - q| < |e|$ there. So $q - p$ changes sign between consecutive points, which gives $n + 1$ distinct zeros of a polynomial of degree at most $n$, and $q = p$. That contradicts $\|f - q\| < |e(\xi_0)| \le \|f - p\|$. Hence $E_n(f) \ge \min_i|e(\xi_i)|$. If the alternation is at the level $\|e\|$, this says $E_n(f) \ge \|f - p\|$, so $p$ is best.

**Necessity.** Let $p$ be a best approximation with $E > 0$ (if $E = 0$, then $e \equiv 0$ and any $n + 2$ points serve). By uniform continuity choose a partition of $[a, b]$ into closed subintervals on each of which $e$ varies by less than $E/2$. Call a subinterval *marked* if it contains a point with $|e| = E$. On a marked subinterval $|e| > E/2$, so $e$ has one sign there. Two touching marked subintervals cannot have opposite signs, since $e$ would be both $> E/2$ and $< -E/2$ at the shared endpoint.

List the marked subintervals from left to right and group consecutive ones with the same sign into maximal runs $R_1, \ldots, R_k$; the signs of the runs alternate. If $k \ge n + 2$, picking one point with $|e| = E$ in each of the first $n + 2$ runs gives the required alternation set. Suppose instead $k \le n + 1$. Between the last subinterval of $R_j$ and the first of $R_{j+1}$ there is a gap (they have opposite signs, so they do not touch), and we choose a point $z_j$ in it, $j = 1, \ldots, k - 1$. No $z_j$ lies in a marked subinterval. Let
$$r(x) = \pm\prod_{j=1}^{k-1}(x - z_j),$$
with the sign chosen so that $r$ has the sign of $e$ on $R_1$. Then $r \in \mathcal{P}_{k-1} \subseteq \mathcal{P}_n$, $r$ changes sign exactly at the $z_j$, and so $r$ has the sign of $e$ on every marked subinterval. Let $M$ be the union of the marked subintervals and $\delta = \min_M|r| > 0$; let $K$ be the union of the unmarked ones, on which $|e| < E$, so $E' = \max_K|e| < E$ (if $K$ is empty, ignore it). For $0 < \lambda < \min\big(E/(2\|r\|), (E - E')/\|r\|\big)$:

- on $M$, $e$ and $r$ have the same sign and $\lambda|r| < E/2 < |e|$, so $|e - \lambda r| = |e| - \lambda|r| \le E - \lambda\delta < E$;
- on $K$, $|e - \lambda r| \le E' + \lambda\|r\| < E$.

So $\|f - (p + \lambda r)\| < E$, contradicting the optimality of $p$. Hence $k \ge n + 2$.

**Uniqueness.** Let $p$ and $q$ both be best, with error $E$. Then $h = \frac12(p + q)$ satisfies $\|f - h\| \le E$, so $h$ is best, and by necessity there are $n + 2$ points with $|f(\xi_i) - h(\xi_i)| = E$. At such a point $\frac12\big((f - p)(\xi_i) + (f - q)(\xi_i)\big) = \pm E$ with both terms in $[-E, E]$, which forces $(f - p)(\xi_i) = (f - q)(\xi_i)$. So $p - q$ has $n + 2$ zeros and $p = q$. $\square$

The proof uses only two facts about $\mathcal{P}_n$: a nonzero element has at most $n$ zeros, and there are elements with prescribed sign changes at any $k - 1 \le n$ points. Both hold for any Haar space, which gives the general version.

## Consequences

**Least deviation from zero.** The best approximation to $x^{n+1}$ on $[-1, 1]$ from $\mathcal{P}_n$ is $x^{n+1} - 2^{-n}T_{n+1}(x)$, since the error $2^{-n}T_{n+1}$ attains $\pm2^{-n}$ alternately at the $n + 2$ points $\cos(j\pi/(n + 1))$. Equivalently, $2^{-n}T_{n+1}$ has the smallest maximum norm on $[-1, 1]$ among monic polynomials of degree $n + 1$, which is why the zeros of $T_{n+1}$ minimize the node polynomial $\|\omega\|$ ([Chebyshev nodes](/chebyshev-nodes/)), and why dropping one term of a Chebyshev series is optimal ([Chebyshev economization](/chebyshev-economization/)).

**Best constant.** For $n = 0$, $p^* = \frac12(\max f + \min f)$, with alternation at a maximizer and a minimizer.

**Best line for $e^x$ on $[-1, 1]$.** By convexity the error has alternation points $-1$, $\xi$, $1$, so $p^*(x) = a + bx$ with $e^{-1} - a + b = E$, $e^\xi - a - b\xi = -E$, $e - a - b = E$, and $\xi$ an interior extremum, $e^\xi = b$. Solving gives $b = \sinh 1 = 1.17520$, $\xi = \log\sinh 1 = 0.161439$, $E_1 = \frac12(e^{-1} + \sinh 1 \cdot \log\sinh 1) = 0.278802$ and $a = 1.26428$. The chord through $(\pm1, e^{\pm1})$, which is interpolation at the two Chebyshev extreme points, has error exactly $2E_1$: the factor $1 + \Lambda_1 = 2$ of the near-best bound is attained.

**$|x|$ on $[-1, 1]$.** The best approximation of degree 2, and also of degree 3, is $x^2 + \frac18$: the error $|x| - x^2 - \frac18$ takes the values $-\frac18, \frac18, -\frac18, \frac18, -\frac18$ at $-1, -\frac12, 0, \frac12, 1$, five alternation points, which is $n + 2$ for $n = 3$. So $E_2(|x|) = E_3(|x|) = \frac18$.

**Interpolation.** Between consecutive alternation points the error changes sign, so $p^*$ interpolates $f$ at $n + 1$ points in $(a, b)$. Best approximation is a kind of interpolation at nodes that depend on $f$.

**Algorithms.** The [Remez algorithm](/remez-algorithm/) solves the $n + 2$ alternation equations on a trial reference and exchanges points until the levels agree; the de la Vallée Poussin bound gives a certified bracket $[\min_i|e(\xi_i)|, \|e\|]$ for $E_n(f)$ at each step. Linear programming solves the discrete problem on a grid, where the same theorem holds.

**Error estimates.** Near-best methods are measured against $E_n(f)$: [Chebyshev interpolation](/chebyshev-interpolation/) has $\|f - p_n\| \le (1 + \Lambda_n)E_n(f)$ with the [Lebesgue constant](/lebesgue-constant/) $\Lambda_n = O(\log n)$, and the coefficient bound $|a_{n+1}| \le 2E_n(f)$ for the Chebyshev series gives a lower bound on $E_n$ that is easy to compute.

## Tightness

- **$n + 2$ cannot be lowered.** For $f(x) = x$ on $[-1, 1]$ and $n = 0$, the constant $p = \frac12$ has error $x - \frac12$ with maximum modulus $\frac32$ attained only at $x = -1$; it alternates at one point ($n + 1$), but the best constant is $0$ with $E_0 = 1$.
- **The Haar condition is needed.** Haar (1918) proved that the best approximation from an $(n + 1)$-dimensional subspace of $C[a, b]$ is unique for every $f$ if and only if the subspace satisfies the Haar condition. The span of $\{x\}$ on $[-1, 1]$ fails it, since its nonzero element $x$ vanishes at $0$. Approximating $f(x) = 1 - |x|$ by $cx$ gives $\|f - cx\| = \max(1, |c|)$, so every $c$ with $|c| \le 1$ is a best approximation.
- **Several variables.** By the Mairhuber theorem (1956), a compact set in $\mathbb{R}^d$ that carries a Haar space of dimension at least 2 is homeomorphic to a subset of a circle. In particular no Haar space of dimension $\ge 2$ exists on a square, and multivariate minimax polynomials need not be unique or characterized by alternation.
- **Other norms.** In $L^1$ or $L^2$ the best approximations are characterized differently (sign conditions or orthogonality), and the alternation property does not characterize them.
- **Continuity.** For discontinuous $f$ the maximum may not be attained and the best approximation need not be unique.
- **Rational functions.** For rational approximation of type $(m, n)$ the count becomes $m + n + 2 - d$, where $d$ is the defect, and degenerate cases occur ([rational approximation](/rational-approximation/)).

## History

Chebyshev studied best uniform approximation from 1853 onward, motivated by the design of linkages such as Watt's parallelogram, and in 1854 he stated the alternation condition and found the polynomials of least deviation from zero that now bear his name. Complete proofs of the characterization were given by Kirchberger (dissertation, Göttingen, 1902) and Borel (Leçons sur les fonctions de variables réelles, 1905). De la Vallée Poussin gave the lower bound named after him around 1910, and Haar (1918) identified the exact condition on the approximating space for uniqueness. Remez (1934) turned the theorem into an algorithm, and Mairhuber (1956) showed that the theory does not extend to several variables.

## References
