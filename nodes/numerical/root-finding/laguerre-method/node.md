---
tag: K13QF2
kind: algorithm
slug: laguerre-method
name: Laguerre's method
aliases:
- Laguerre iteration
- Laguerre's root-finding method
area: numerical/root-finding
level: advanced
summary: "A polynomial root method that uses p, p' and p'' at each step. Cubic convergence to simple roots; global and monotone when all roots are real; finds complex roots from real starts."
solves: [polynomial-root-finding]
model: real-ram
complexity:
  vars: {n: the degree of the polynomial, δ: the tolerance on the error, C: "the rate constant ((n-1) S_2 - S_1^2) / (2(n-1)) at a simple root"}
  time: {local: "O(log log(1/(C δ)))", per_step: "O(n)"}
  space: {extra: Θ(1)}
  evaluations: {per_step: "3"}
properties: {deterministic: true, recursive: false, bracketing: false, derivative_free: false, local: true}
history:
  year: 1880
  people: [Edmond Laguerre, James H. Wilkinson, William Kahan]
  note: Laguerre proposed the method in 1880 for polynomials with real roots; Wilkinson and Parlett studied it for eigenvalue problems in the 1960s; it became a standard general-purpose polynomial solver through Numerical Recipes.
prereqs: [newton-raphson-method, polynomial-root-finding, horner-rule, order-of-convergence]
see_also: [polynomial-deflation, halley-method, muller-method, jenkins-traub-algorithm, aberth-ehrlich-method, companion-matrix-method, multiplicity-of-roots, root-conditioning]
sources:
  - paper: "E. Laguerre, Sur une méthode pour obtenir par approximation les racines d'une équation algébrique qui a toutes ses racines réelles, Nouvelles Annales de Mathématiques, 2e série, 19 (1880) 161-171 and 193-202"
    locator: the method and its monotone convergence for real-rooted polynomials
  - book: "J. H. Wilkinson, The Algebraic Eigenvalue Problem, Oxford University Press, 1965"
    locator: Chapter 7, Laguerre's method (global convergence for real roots and the cubic rate)
  - book: isbn:9780521880688
    title: W. H. Press, S. A. Teukolsky, W. T. Vetterling and B. P. Flannery, Numerical Recipes, third edition, Cambridge University Press, 2007
    locator: Section 9.5, Roots of polynomials (laguer and zroots, the derivation, limit cycles and the fractional step, polishing after deflation)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 5.1, Horner's method (the running error bound used in the residual test)
  - book: "A. M. Ostrowski, Solution of Equations and Systems of Equations, second edition, Academic Press, 1966"
    locator: Chapter 3, the efficiency index
---

Laguerre's method finds a root of a polynomial $p$ of degree $n$ by taking at each step
$$x_{k+1} = x_k - \frac{n}{G \pm \sqrt{(n-1)(nH - G^2)}}, \qquad G = \frac{p'(x_k)}{p(x_k)},\quad H = G^2 - \frac{p''(x_k)}{p(x_k)},$$
with the sign that makes the denominator larger in modulus. It converges with order 3 to every simple root. When all the roots of $p$ are real it converges from every real start, monotonically, to a neighbouring root, which no method of Newton type does. It works in complex arithmetic, finds complex roots from real starts, and is exact in one step for $p(x) = (x - r)^n$. Combined with [deflation](/polynomial-deflation/) and polishing it computes all the roots, and it is one of the standard methods for [polynomial root finding](/polynomial-root-finding/).

## In plain words

Newton's method pretends the polynomial is a straight line near the guess. Laguerre's method pretends instead that one root is near the guess and the other $n - 1$ roots all sit together somewhere else. That picture has only two unknowns, the distance to the near root and the distance to the far group, and the values of $p$, its slope and its curvature at the guess pin both down. Solving for the near distance gives the next guess. When the picture is close to the truth the step is nearly exact, so the number of correct digits about triples in each step. Each step needs $p$, $p'$ and $p''$, all three from one pass over the coefficients.

## The problem

The input is a polynomial $p(x) = a_n x^n + \cdots + a_0$ of degree $n \ge 1$, given by its real or complex coefficients, a start $x_0$, a tolerance (an absolute part $\delta_a \ge 0$ and a relative part $\delta_r \ge 0$) and a maximum number of passes $k_{\max}$. The output is an approximate root $\hat x$ and a flag. In floating point a root can only be computed up to the limiting accuracy set by the rounding error in $p(x)$, so a root is accepted as soon as $|p(x)|$ is below a bound on that error.

Notation on the root-finding pages: $x^*$ is a root, $x_k$ the iterates, $e_k = x_k - x^*$ the error, $m$ the multiplicity of a root, $u = 2^{-53}$ the unit roundoff. A method has order $q$ and rate constant $C$ when $|e_{k+1}| \approx C |e_k|^q$, and with $w$ evaluations per step its efficiency index is $q^{1/w}$. For the roots $x_1, \ldots, x_n$ of $p$ and a point $x$ that is not a root,
$$G(x) = \frac{p'(x)}{p(x)} = \sum_{i=1}^n \frac{1}{x - x_i}, \qquad H(x) = G(x)^2 - \frac{p''(x)}{p(x)} = \sum_{i=1}^n \frac{1}{(x - x_i)^2}.$$

## The algorithm

```pseudo id=main
LAGUERRE(a_n..a_0, x0, δa, δr, kmax)
L1  x ← x0
L2  for k ← 1 to kmax do
L3      compute p = p(x), p' = p'(x), p'' = p''(x) and s = Σ |a_j| |x|^j by Horner's rule
L4      if p = 0 then return (x, "root")
L5      if |p| ≤ 8 n u s then return (x, "residual")
L6      G ← p'/p;  H ← G² − p''/p
L7      r ← sqrt((n − 1)(n H − G²))          ▷ complex square root
L8      d ← G + r if |G + r| ≥ |G − r| else G − r
L9      if d = 0 then a ← (1 + |x|) e^{ik}       ▷ p' = p'' = 0 at x
L10     else a ← n / d;  x ← x − a
L11     if |a| ≤ δa + δr |x| then return (x, "converged")
L12 return (x, "kmax reached")
```

Line L3 is one sweep of [Horner's rule](/horner-rule/) that carries $p$, $p'$, $p''/2$ and the sum $s$ together, at about $3n$ multiply-adds. Line L5 is the residual test: the rounding error of the computed $p(x)$ is at most a small multiple of $n u s$ (Higham, Section 5.1), so a smaller $|p(x)|$ carries no information, and $x$ is then an exact root of a polynomial whose coefficients differ from the given ones by a relative amount of order $n u$. Lines L6 to L8 form the Laguerre step. The sign choice in line L8 makes $|d|$ as large as possible and the step as small as possible; for real $G$ and real $r$ it gives $d$ the sign of $G$. Line L9 handles the case $G = H = 0$, a point where $p'$ and $p''$ both vanish, by a step of fixed size in a direction that changes with $k$; Numerical Recipes uses the same device. Line L11 is the step test, and line L2 bounds the work. The implementation also stops with the flag "failure" when a value is NaN or infinite.

**Where the formula comes from.** Fix $x$, let $\alpha = x - x_1$ be the distance to a root $x_1$ and assume the other $n - 1$ roots are all at distance $\beta$. Then $G = 1/\alpha + (n-1)/\beta$ and $H = 1/\alpha^2 + (n-1)/\beta^2$. Eliminating $\beta$ gives a quadratic for $1/\alpha$,
$$n \Big(\frac{1}{\alpha}\Big)^2 - 2G \frac{1}{\alpha} + G^2 - (n - 1) H = 0,$$
whose roots are $1/\alpha = (G \pm \sqrt{(n-1)(nH - G^2)})/n$, and the step is $a = \alpha$. If $p(x) = (x - r)^n$ the assumption holds exactly, so one step lands on $r$.

## Example

Let $p(x) = (x - 1)(x - 2)(x - 3)(x - 4) = x^4 - 10x^3 + 35x^2 - 50x + 24$ and $x_0 = 0$. All roots are real and $x_0$ is left of all of them, so the iterates must increase monotonically to the smallest root $1$. In 200-digit decimal arithmetic:

| $k$ | $\lvert e_k \rvert$ | $\lvert e_k \rvert / \lvert e_{k-1} \rvert^3$ |
|---|---|---|
| 0 | $1$ | |
| 1 | $2.412789 \cdot 10^{-2}$ | $0.02413$ |
| 2 | $1.606601 \cdot 10^{-6}$ | $0.11438$ |
| 3 | $4.991626 \cdot 10^{-19}$ | $0.12037$ |
| 4 | $1.497082 \cdot 10^{-56}$ | $0.12037$ |

The ratio tends to the constant of the Correctness section. With $S_1 = \sum_{i \ge 2} 1/(1 - x_i) = -1 - \frac12 - \frac13 = -\frac{11}{6}$ and $S_2 = 1 + \frac14 + \frac19 = \frac{49}{36}$,
$$C = \frac{(n-1) S_2 - S_1^2}{2(n-1)} = \frac{3 \cdot 49/36 - 121/36}{6} = \frac{13}{108} = 0.120370\ldots$$
In binary64 the program returns $0.9999999999999998$ after 4 passes: $x_1 = 0.9758721061252207$, $x_2 = 0.9999983933992563$, $x_3 = 0.9999999999999998$, and in the fourth pass the computed $p(x_3)$ is exactly $0$. That is 4 Horner sweeps, each giving three values. Newton's method from the same start needs 8 steps, with 16 values, to reach the same accuracy.

From other starts the program goes to the neighbouring root in the direction of the sign of $-G$: from $2.4$ to $2$, from $2.6$ to $3$, from $10$ to $4$ and from $-7$ to $1$, in 5 passes each. For $p(x) = x^2 + 1$ and the real start $x_0 = 0$, $G = 0$ and $H = -2$, so $r = \sqrt{-4} = 2i$ and the step lands exactly on $i$; Newton's method cannot even start there, since $p'(0) = 0$, and from any other real start it stays real.

## Correctness

The claims are proved in [the correctness proof](proofs/correctness.md), except where marked.

- **Always.** The loop ends after at most $k_{\max}$ passes. A result flagged "root" is an exact zero of the computed $p$; one flagged "residual" has $|p(\hat x)|$ at the level of the rounding error of its evaluation; one flagged "converged" passed the step test.
- **Real roots, global (proved).** Let $p$ be real with only real roots, and $x_0$ real and not a root. Then $nH - G^2 \ge 0$, so every iterate is real; the step moves towards the nearest root on the side given by the sign of $-G(x_0)$, never past it, and the iterates converge monotonically to that root. This is Laguerre's theorem, and it holds also for multiple roots.
- **Local, cubic (proved).** At a simple root $x^*$ with $n \ge 2$, let $S_j = \sum_i (x^* - x_i)^{-j}$ over the other $n - 1$ roots. Then
$$e_{k+1} = C e_k^3 + O(e_k^4), \qquad C = \frac{(n-1) S_2 - S_1^2}{2(n-1)},$$
and $C \ge 0$ for real roots by the Cauchy-Schwarz inequality, with $C = 0$ when the other roots coincide. So the method converges with order 3 from starts close enough to $x^*$.
- **Multiple roots (observed).** At a root of multiplicity $m$ with $1 < m < n$ the convergence is linear; for $(x - 1)^2(x + 2)$ from $3$ the program stops by the residual test after 13 passes with error $7.1 \cdot 10^{-8}$, about $\sqrt u$.
- **Complex starts (not proved).** For general complex polynomials there is no global theorem. The method converges from almost every start in practice, but limit cycles exist; Numerical Recipes breaks them with a fractional step every few passes.

## Complexity

The cost model is the number of Horner sweeps, each of which gives $p$, $p'$ and $p''$, and the number of arithmetic operations.

- **Per step.** One sweep of about $3n$ complex multiply-adds plus one complex square root. Counting $p$, $p'$ and $p''$ as three evaluations, $w = 3$ and the efficiency index is $3^{1/3} \approx 1.442$, the same as for [Halley's method](/halley-method/) and a little above Newton's $2^{1/2} \approx 1.414$. Counted in arithmetic, the sweep costs three times the $n$ multiply-adds of $p$ alone.
- **Steps to the tolerance.** Under the local hypotheses, $|e_k|$ falls below $\delta$ after $O(\log \log (1/(C\delta)))$ steps, about $\log_3$ of the number of digits wanted once the cubic phase starts.
- **All roots.** With deflation, finding all $n$ roots takes $O(n^2)$ operations times the number of passes per root, which is small in practice; there is no proved bound on the number of passes from a fixed start.
- **Space.** $\Theta(1)$ besides the coefficients; deflation needs $O(n)$.

### Floating point

The computed $p(x)$ has an error of at most a small multiple of $n u \sum_j |a_j||x|^j$, so iterates cannot get closer to a simple root than about $n u \sum_j |a_j||x^*|^j / |p'(x^*)|$, which is $n u |x^*|$ times the [condition number](/root-conditioning/) of the root. The residual test of line L5 stops at that level, so the method cannot loop forever near a root on rounding noise. Near a root of multiplicity $m$ the limiting accuracy is about $u^{1/m}$ times a scale factor. Deflation by a computed root adds error to the remaining coefficients; it is stable when roots are removed in increasing order of modulus, and polishing each root with a few steps on the original polynomial removes most of the rest.

## Properties

- **Exact for powers.** For $p(x) = c(x - r)^n$ one step from any start lands on $r$.
- **Global for real roots.** The only classical method that converges from every real start for real-rooted polynomials and never overshoots a root.
- **Complex roots from real starts.** For a real polynomial and a real $x$, the square root in line L7 is imaginary when $nH < G^2$, so the iterates leave the real line by themselves when the nearby roots are complex.
- **Uses the degree.** Unlike Newton's and Halley's methods, the step depends on $n$, so it is a method for polynomials, not for general functions; using a larger $n$ than the true degree still gives a convergent method.
- **Invariance.** Scaling $p$ by a constant does not change the iterates, and neither does an affine change of variable.

## Variants and improvements

- **All roots by deflation and polishing.** Find a root of the current polynomial from $0$, so roots come out roughly in increasing order of modulus, divide it out, repeat, and polish each root against the original $p$; this is `zroots` in Numerical Recipes and `laguerre_all_roots` in the implementation.
- **Fractional steps.** Replace the step by a fraction of itself every few passes to break rare limit cycles.
- **Laguerre for eigenvalues.** Applied to the characteristic polynomial of a tridiagonal or Hessenberg matrix, with $p$, $p'$, $p''$ computed by recurrences from the matrix rather than from coefficients (Parlett, 1964).
- **Simultaneous Laguerre.** Use the current approximations of the other roots in the formula, giving iterations of higher order in the style of [Aberth-Ehrlich](/aberth-ehrlich-method/).
- **Modified Laguerre for multiple roots.** If the multiplicity $m$ is known, the analogous formula with $m$ and $n - m$ in place of $1$ and $n - 1$ restores cubic convergence.

## When to use it

Use Laguerre's method with deflation for all the roots of a polynomial of moderate degree when a simple, robust, self-starting method is wanted, and alone when all roots are known to be real. For high degree or many roots at once, the [companion matrix method](/companion-matrix-method/), [Aberth-Ehrlich](/aberth-ehrlich-method/) or [Jenkins-Traub](/jenkins-traub-algorithm/) are the usual choices.

## Pitfalls

- **Limiting accuracy.** A step test with $\delta_a = 0$ and a tiny $\delta_r$ may never pass because the iterates move on rounding noise; the residual test of line L5 and the bound $k_{\max}$ end the loop.
- **Multiple and clustered roots.** Convergence becomes linear and the accuracy drops to about $u^{1/m}$; the double root of $(x - 1)^2(x + 2)$ comes out with error $7 \cdot 10^{-8}$.
- **Critical points.** At a point with $p' = p'' = 0$, such as $0$ for $x^3 - 1$, the step formula has a zero denominator; line L9 handles it.
- **Deflation order.** Dividing out large roots first spoils the small ones; start each search from $0$ and always polish.
- **Ill-conditioned polynomials.** For [Wilkinson's polynomial](/wilkinson-polynomial/) no method recovers the roots from the rounded coefficients to more than a few digits, since the rounding itself moves them.

## Implementations

## History

Edmond Laguerre published the method in 1880 for polynomials with only real roots, together with the proof that it converges monotonically from any real start. It became widely used in numerical computing after Wilkinson's analysis in The Algebraic Eigenvalue Problem (1965) and Parlett's application to eigenvalues of Hessenberg matrices (1964), and it reached a wide audience as the polynomial solver of Numerical Recipes (1986).

## References
