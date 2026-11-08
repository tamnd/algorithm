---
tag: VZ77TJ
kind: algorithm
slug: remez-algorithm
name: Remez algorithm
aliases:
- Remez exchange algorithm
- Remes algorithm
- Exchange algorithm for minimax approximation
area: numerical/interpolation-and-approximation
level: advanced
summary: Find the best uniform polynomial approximation by solving for a levelled error on n + 2 reference points and exchanging them for the extrema of the error, until the error equioscillates.
solves: [minimax-approximation]
model: real-ram
complexity:
  vars: {n: the degree, m: the size of the search grid for extrema, K: the number of iterations}
  time: {per_iteration: Θ(n^3 + m n), total: Θ(K (n^3 + m n))}
  space: {extra: Θ(n^2 + m)}
  flops: {per_iteration: "(2/3)(n+2)^3 + 4 m n"}
properties: {deterministic: true, recursive: false, iterative: true, exact_on_polynomials: true, certified_lower_bound: true}
history:
  year: 1934
  people: [Evgeny Remez]
  note: Remez published the exchange algorithm in 1934; its use on computers for function libraries dates from the late 1950s.
prereqs: [minimax-approximation, chebyshev-equioscillation-theorem, gaussian-elimination]
see_also: [chebyshev-polynomials, chebyshev-interpolation, chebyshev-economization, rational-approximation, lebesgue-constant, jackson-theorem, polynomial-interpolation, orthogonal-polynomials]
sources:
  - paper: "Evgeny Ya. Remez, Sur le calcul effectif des polynômes d'approximation de Tchebichef, Comptes Rendus de l'Académie des Sciences de Paris 199 (1934) 337-340"
    locator: the exchange algorithm for best uniform polynomial approximation
  - book: isbn:9780521295147
    title: M. J. D. Powell, Approximation Theory and Methods, Cambridge University Press, 1981
    locator: Chapter 7, The theory of minimax approximation; Chapter 8, The exchange algorithm; Chapter 9, The convergence of the exchange algorithm
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 10, Best approximation, and Chapter 16, Best and near-best (the Remez algorithm in Chebfun and the comparison with Chebyshev interpolation)
  - paper: "Ricardo Pachón and Lloyd N. Trefethen, Barycentric-Remez algorithms for best polynomial approximation in the chebfun system, BIT Numerical Mathematics 49(4) (2009) 721-741"
    locator: a robust implementation, with the reference handled in barycentric form and the extrema found by rootfinding
  - paper: "L. Veidinger, On the numerical determination of the best approximations in the Chebyshev sense, Numerische Mathematik 2 (1960) 99-105"
    locator: the proof of quadratic convergence of the multiple-exchange algorithm for smooth functions
  - book: isbn:9780821813744
    title: E. W. Cheney, Introduction to Approximation Theory, second edition, AMS Chelsea Publishing, 1998
    locator: Chapter 3, Tchebycheff approximation (the exchange algorithm and its convergence)
  - paper: "Richard S. Varga and Amos J. Carpenter, On the Bernstein conjecture in approximation theory, Constructive Approximation 1 (1985) 333-348"
    locator: high-precision best approximations of |x| and the value 0.2801694990 of Bernstein's constant
---

The Remez algorithm computes the best uniform polynomial approximation $p^*$ of degree at most $n$ to a continuous function $f$ on $[a, b]$, the polynomial that minimizes $\max_x |f(x) - p(x)|$. By the [Chebyshev equioscillation theorem](/chebyshev-equioscillation-theorem/), $p^*$ is characterized by an error that attains its maximum with alternating signs at $n + 2$ points. The algorithm guesses these points, solves a small linear system for the polynomial whose error alternates with equal size on them, and then moves the points to where the actual error peaks. It repeats until the peaks are level. It is the classical method for building the polynomial approximations in mathematical function libraries.

## In plain words

You want the polynomial whose worst mistake over an interval is as small as possible. The theory says that the best one makes its largest mistake at a certain number of places, alternately too high and too low, and all of the same size.

So guess those places. Find the polynomial that is too high and too low by exactly the same amount at them; that is a small system of equations. Then look at the whole interval. Where the mistake is actually largest, move your guessed places there and solve again. Each round, the equal mistake grows and the largest mistake shrinks, until they meet. At that point you have the best polynomial, and the round itself proves that nothing can do better.

## The problem

Notation on the interpolation pages: $f$ is continuous on $[a, b]$ (often $[-1, 1]$); $\mathcal{P}_n$ is the space of polynomials of degree at most $n$; $E_n(f) = \min_{p \in \mathcal{P}_n} \|f - p\|_\infty$; $T_k$ are the Chebyshev polynomials. A **reference** is a set of $n + 2$ points $x_0 < x_1 < \cdots < x_{n+1}$ in $[a, b]$.

The input is $f$ (as a routine that evaluates it), $n$, $[a, b]$ and a tolerance. The output is $p \in \mathcal{P}_n$ and its maximum error, with $\|f - p\|_\infty \le E_n(f)/(1 - \text{tol})$ when the extrema of the error are located correctly. The best approximation exists and is unique ([minimax approximation](/minimax-approximation/)).

The two facts that drive the algorithm:

- **Levelled interpolation.** For any reference there is a unique $p \in \mathcal{P}_n$ and number $h$ with
$$f(x_i) - p(x_i) = (-1)^i h, \qquad i = 0, \ldots, n + 1,$$
a linear system of $n + 2$ equations in the $n + 1$ coefficients of $p$ and $h$.
- **de la Vallée Poussin's bound.** If $f - p$ alternates in sign on a reference, then $\min_i |f(x_i) - p(x_i)| \le E_n(f) \le \|f - p\|_\infty$. For the levelled $p$ this reads $|h| \le E_n(f) \le \|f - p\|_\infty$, so every iteration brackets the unknown $E_n(f)$.

## The algorithm

```pseudo id=main
REMEZ(f, n, a, b, tol)
L1  x ← the n + 2 Chebyshev extreme points mapped to [a, b]
L2  repeat
L3      solve Σ_j c_j T_j(x_i) + (−1)^i h = f(x_i), i = 0..n+1, for c and h
L4      e ← f − p, where p = Σ_j c_j T_j
L5      find the local extrema of e on [a, b], one per run of constant sign
L6      if max |e| − |h| ≤ tol · max |e| then
L7          return p, max |e|
L8      choose n + 2 consecutive extrema of alternating sign that include the global maximum
L9      x ← those n + 2 points
```

Line L1 starts from the reference that is optimal for $f = x^{n+1}$, which is close to optimal for many smooth $f$. Line L3 writes $p$ in the Chebyshev basis of $[a, b]$, which keeps the system well conditioned; the monomial basis would make it as ill-conditioned as a [Vandermonde matrix](/vandermonde-matrix/). Line L5 is the expensive and delicate step: the implementation scans a grid of $m$ points, keeps the largest $|e|$ in each run of constant sign, and refines it by golden-section search; Chebfun finds the extrema as roots of $e'$ instead. Line L6 compares the two sides of de la Vallée Poussin's bracket. Line L8 is the **multiple exchange** (Remez's second algorithm): all points move at once. The **single exchange** (Remez's first algorithm) swaps only the global maximum into the reference, keeping alternation; the implementation uses it as a fallback when the reference is degenerate, for example when symmetry forces $h = 0$.

## Example

**$e^x$ on $[-1, 1]$, $n = 6$.** The iterations give

| iteration | $\lvert h\rvert$ | $\max\lvert e\rvert$ | gap |
|---|---|---|---|
| 1 | $3.198436 \times 10^{-6}$ | $3.222885 \times 10^{-6}$ | $2.4 \times 10^{-8}$ |
| 2 | $3.210871 \times 10^{-6}$ | $3.210884 \times 10^{-6}$ | $1.3 \times 10^{-11}$ |
| 3 | $3.210877 \times 10^{-6}$ | $3.210877 \times 10^{-6}$ | below $10^{-16}$ |

so $E_6(e^x) = 3.210877 \times 10^{-6}$. The relative gap goes from $7.6 \times 10^{-3}$ to $4 \times 10^{-6}$ to rounding level, roughly squaring each time, which is the quadratic convergence expected for smooth $f$. The Chebyshev extreme points are already a good reference, so the first iterate is within 1% of optimal.

**$|x|$ with $n = 2$.** The initial reference $-1, -\tfrac12, \tfrac12, 1$ is symmetric, and since $|x|$ is even the levelled system gives $h = 0$. A single exchange brings in $x = 0$, and after six iterations the algorithm returns $p^*(x) = x^2 + \tfrac18$, with $E_2 = \tfrac18$ and error $-\tfrac18, \tfrac18, -\tfrac18, \tfrac18, -\tfrac18$ at $-1, -\tfrac12, 0, \tfrac12, 1$: five alternation points, one more than required, because $p^*$ is also the best cubic.

**Rates.** For $|x|$, $n\,E_n(|x|)$ is $0.2705$, $0.2775$, $0.2795$ and $0.2800$ for $n = 4, 8, 16, 32$, approaching Bernstein's constant $0.2801694990$ computed by Varga and Carpenter (1985). For Runge's function $1/(1 + 25x^2)$, $E_n = 0.0659$, $9.04 \times 10^{-3}$ and $1.70 \times 10^{-4}$ for $n = 10, 20, 40$, after 6, 6 and 10 iterations; the [Chebyshev interpolant](/chebyshev-interpolation/) at first-kind points has errors $0.109$, $0.0153$ and $2.90 \times 10^{-4}$, larger by a factor of only about 1.7.

## Correctness

Three facts, proved in the correctness proof below, make the algorithm correct whenever it stops.

1. **The levelled system is nonsingular.** If $p(x_i) + (-1)^i h = 0$ for all $i$ with $h \ne 0$, then $p$ alternates in sign at $n + 2$ points and has $n + 1$ zeros, so $p = 0$ and then $h = 0$; if $h = 0$, $p$ has $n + 2$ zeros and is 0. This uses only that $\mathcal{P}_n$ is a Haar space: a nonzero element has at most $n$ zeros.
2. **de la Vallée Poussin.** If $\|f - q\|_\infty < \min_i |f(x_i) - p(x_i)|$ for some $q \in \mathcal{P}_n$, then $q - p = (f - p) - (f - q)$ has the sign of $f - p$ at every $x_i$, hence alternates, hence has $n + 1$ zeros and is 0, a contradiction. So $|h| \le E_n(f)$.
3. **The stopping test certifies.** If line L6 succeeds with $M = \max|e|$, then $M - |h| \le \text{tol}\cdot M$ and $|h| \le E_n(f)$ give $M \le E_n(f)/(1 - \text{tol})$. If $M$ is the true maximum of $|f - p|$, then $p$ is within this factor of optimal.

The last condition is the honest limit of any implementation: the certificate is only as good as the search for the maximum in line L5. A grid can miss a narrow peak between grid points.

**Convergence** is a separate matter. For the single-exchange algorithm, $|h|$ increases strictly at each step and the iterates converge to $p^*$ for every continuous $f$, at least linearly (Powell, Chapters 8 and 9). For the multiple exchange, Veidinger (1960) proved quadratic convergence near the solution when $f$ is smooth and the error of $p^*$ has exactly $n + 2$ nondegenerate extrema. The rule in line L8 is the standard choice in practice; its global convergence is not covered by these proofs in every degenerate case, which is why the implementation falls back to a single exchange.

## Complexity

- **Per iteration.** Forming the system costs $(n + 2)(n + 1)$ evaluations of $T_j$, and Gaussian elimination costs about $\tfrac23 (n + 2)^3$ flops. The search costs $m$ evaluations of $f$ and of $p$; Clenshaw's recurrence evaluates $p$ in about $4n$ flops, so about $4mn$ flops in total. Golden-section refinement adds a fixed number (60 here) of evaluations per extremum. The grid must resolve the $n + 2$ oscillations of the error, so $m$ grows at least linearly in $n$; the implementation uses $m = \max(2001, 40(n + 2))$. Total: $\Theta(n^3 + mn)$ operations and $\Theta(m)$ evaluations of $f$.
- **Iterations.** Observed: 1 to 10 for the examples above. With quadratic convergence, $K$ is $O(\log\log(1/\text{tol}))$ once the iterates are close.
- **Space.** $\Theta(n^2)$ for the system and $\Theta(m)$ for the grid.

## Properties

- **Certified bracket.** Every iteration gives $|h| \le E_n(f) \le \max|e|$, a lower bound that is rigorous up to rounding and an upper bound that is rigorous if the search is.
- **Exact on polynomials.** If $f \in \mathcal{P}_n$, the first levelled system gives $p = f$ and $h = 0$.
- **Affine invariance.** The result for $\alpha f + q$, with $q \in \mathcal{P}_n$, is $\alpha p^* + q$; mapping $[a, b]$ affinely maps the reference.
- **Smoothness matters.** For analytic $f$ convergence is fast and robust. For $f$ with a kink or a near-singularity the error has sharp peaks that the search must resolve; for discontinuous $f$ the problem is ill-posed ($E_n(\text{sign}) = 1$ for every $n$) and the algorithm cannot converge.
- **Rounding.** The levelled system in the Chebyshev basis at well-spread references is well conditioned. In the monomial basis, high degrees lose many digits, which is why robust codes (Pachón and Trefethen 2009) use the Chebyshev or barycentric representation.

## Variants and improvements

- **Single and multiple exchange.** Remez's first algorithm exchanges one point per step, with guaranteed monotone increase of $|h|$; the second exchanges all of them and converges faster.
- **Barycentric Remez.** Represent $p$ by its values on the reference and evaluate it by a barycentric formula, which avoids the linear solve and is more stable for large $n$ (Pachón and Trefethen 2009).
- **Rational Remez.** For $r = p/q$ of type $(m, n)$, the levelled equations $f(x_i) - p(x_i)/q(x_i) = (-1)^i h$ are nonlinear in $h$ and become a generalized eigenvalue problem; the method can fail when the best approximation is degenerate. See [rational approximation](/rational-approximation/).
- **Weighted and relative error.** Minimize $\max|w(x)(f(x) - p(x))|$, for example $w = 1/|f|$ for relative error, as function libraries do. The theory is the same with a positive continuous weight.
- **Discrete Remez and linear programming.** On a finite point set the problem is a linear program; the exchange algorithm is then the simplex method applied to the dual program (Stiefel 1959).
- **Filter design.** The Parks-McClellan algorithm for linear-phase FIR filters is a Remez exchange for trigonometric polynomials with a weight.
- **Near-best alternatives.** [Chebyshev interpolation](/chebyshev-interpolation/) and [Chebyshev economization](/chebyshev-economization/) give errors within a factor $1 + \Lambda_n$ of $E_n(f)$ with no iteration, and are often good enough.

## When to use it

Use the Remez algorithm when the last factor of 2 in the maximum error matters and the approximation will be evaluated many times: elementary function libraries, hardware function units, and digital filters. Use a weighted version for relative error. When an approximation within a small factor of the best suffices, Chebyshev interpolation is simpler, needs no iteration, and is nearly as good for smooth $f$.

## Pitfalls

- **Missing a peak.** A grid that is too coarse misses narrow extrema of the error, and the algorithm then reports convergence with a wrong maximum. Refine the grid with $n$, or find extrema as roots of $e'$.
- **Monomial basis.** Solving the levelled system in powers of $x$ loses accuracy quickly with $n$. Use the Chebyshev basis or barycentric form.
- **Symmetric references for symmetric $f$.** An even $f$ and an even number of symmetric reference points give $h = 0$ and no alternation; a single exchange or a perturbation of the reference is needed.
- **Non-smooth $f$.** Kinks give many sharp peaks and slow convergence; jumps make the problem ill-posed. Smooth or split the interval first.
- **Endpoints.** The maximum of the error is often at $a$ or $b$; the search must include them.
- **Rational case.** Rational Remez can fail to converge or produce spurious poles; good starting points (for example from Carathéodory-Fejér approximation) help.

## Implementations

## History

Remez published the exchange algorithm in 1934, building on Chebyshev's characterization of best approximations (1854) and de la Vallée Poussin's lower bound (around 1910). With the first computers it became the tool for designing the polynomial and rational approximations of function libraries, and Veidinger (1960) proved its quadratic convergence. Parks and McClellan adapted it to filter design in 1972. Pachón and Trefethen (2009) made it robust for high degrees in Chebfun.

## References
