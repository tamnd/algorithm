---
tag: 4VYZ43
kind: algorithm
slug: aberth-ehrlich-method
name: Aberth-Ehrlich method
aliases:
- Aberth method
- Ehrlich-Aberth iteration
- Aberth-Ehrlich iteration
area: numerical/root-finding
level: advanced
summary: Simultaneous iteration for all roots of a polynomial; each approximation takes a Newton step on p divided by the factors of the others. Order 3 at simple roots.
solves: [polynomial-root-finding]
model: real-ram
complexity:
  vars: {n: "the degree of the polynomial", K: "the number of sweeps"}
  time: {worst: "O(K n^2)", step: "O(n^2)"}
  space: {extra: Θ(n)}
  evaluations: {worst: "K n", step: "n"}
properties: {deterministic: true, recursive: false, simultaneous: true, derivative_free: false, global_convergence_proved: false}
prereqs: [durand-kerner-method, newton-raphson-method, horner-rule]
see_also: [companion-matrix-method, jenkins-traub-algorithm, polynomial-root-finding, polynomial-deflation, cauchy-root-bound, root-conditioning, wilkinson-polynomial, laguerre-method]
sources:
  - paper: "L. W. Ehrlich, A modified Newton method for polynomials, Communications of the ACM 10(2), 107-108, 1967"
    locator: the correction p/(p' - p S) and its cubic convergence
  - paper: "Oliver Aberth, Iteration methods for finding all zeros of a polynomial simultaneously, Mathematics of Computation 27(122), 339-344, 1973"
    locator: the method, its electrostatic interpretation and the starting points on a circle
  - paper: "Dario A. Bini, Numerical computation of polynomial zeros by means of Aberth's method, Numerical Algorithms 13, 179-200, 1996"
    locator: starting points from the Newton polygon, the stopping rule based on a running error bound, and the cost O(n^2) per sweep
  - paper: "Dario A. Bini and Giuseppe Fiorentino, Design, analysis, and implementation of a multiprecision polynomial rootfinder, Numerical Algorithms 23, 127-173, 2000"
    locator: MPSolve, Aberth iteration with inclusion discs and adaptive precision
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 5.1, Horner's method (the running error bound used in the stopping rule)
---

The Aberth-Ehrlich method finds all $n$ roots of a polynomial $p$ of degree $n$ at once. Each approximation $z_i$ takes a [Newton step](/newton-raphson-method/) not on $p$ but on $p(z)/\prod_{j \ne i}(z - z_j)$, which divides out the roots that the other approximations stand for. The step is
$$z_i \leftarrow z_i - \frac{N_i}{1 - N_i \sum_{j \ne i} \frac{1}{z_i - z_j}}, \qquad N_i = \frac{p(z_i)}{p'(z_i)} .$$
Near simple roots the order is 3, one more than the [Durand-Kerner method](/durand-kerner-method/), at the price of one evaluation of $p'$ alongside each evaluation of $p$. Each sweep costs $O(n^2)$ arithmetic. With good starting points it is the most effective simultaneous method in practice and the core of the MPSolve package, but like Durand-Kerner its global convergence is not proved.

## In plain words

Make one guess for each root. Each guess then runs one step of Newton's method, with a twist: it pretends the other guesses are roots already and divides them out of the polynomial first. So each guess is pushed toward its own root and pushed away from roots that another guess is already near. Think of the guesses as charged particles: they are attracted by the roots and repel each other, so two guesses do not end up on the same root. Close to the answer, the number of correct digits roughly triples each round.

## The problem

Notation on the root-finding pages: $f$ is the function, $x^*$ a root, $x_k$ the iterates and $e_k = x_k - x^*$ the error. A method has [order](/order-of-convergence/) $q$ and rate constant $C$ when $|e_{k+1}| \approx C |e_k|^q$, with $0 < C < 1$ when $q = 1$. A root has [multiplicity](/multiplicity-of-roots/) $m$ when $f(x^*) = \cdots = f^{(m-1)}(x^*) = 0 \ne f^{(m)}(x^*)$. The cost is the number of evaluations of $f$ (and of $f'$ where a method uses it). A method of order $q$ that needs $w$ evaluations in each step has efficiency index $q^{1/w}$.

Here $f = p$ is a polynomial $p(z) = a_0 z^n + a_1 z^{n-1} + \cdots + a_n$ with complex coefficients and $a_0 \ne 0$, with roots $x_1, \dots, x_n$ counted with multiplicity. The input is the coefficient list, a relative tolerance $\delta$ and a cap $K$ on the sweeps. The output is $n$ approximations and a flag. The error of a sweep is $\varepsilon_k = \max_i |z_i^{(k)} - x_i|$ for a suitable matching. Per root and sweep the method evaluates $p$ and $p'$, so $w = 2$ and the efficiency index is $3^{1/2} \approx 1.73$, against $2^{1/1} = 2$ for Durand-Kerner with one evaluation; in practice the $O(n^2)$ arithmetic of the sums dominates, and the Aberth method needs fewer sweeps.

## The algorithm

```pseudo id=main
ABERTH(a0, ..., an, delta, K):
L1   z1, ..., zn <- n distinct points on a circle about c = -a1/(n a0)
L2   for k = 1, 2, ..., K:
L3       for each active i:
L4           evaluate p(zi), p'(zi) by Horner's rule with a running error bound beta_i;  if |p(zi)| <= beta_i then freeze i
L5           S <- sum over j != i of 1/(zi - zj);  fail if some zj = zi
L6           wi <- p(zi)/(p'(zi) - p(zi) S);  fail if the denominator is 0;  zi_new <- zi - wi
L7           if |wi| <= delta |zi_new| then freeze i
L8       z <- z_new                                  // total step: all updates use the old z
L9       if no index is active then return z
L10  return z, not converged
```

Line L1 uses the same start as the Durand-Kerner page: a circle about the centroid $c$ of the roots with radius $1.5\,(|p(c)|/|a_0|)^{1/n}$ and angles $2\pi k/n + 0.4$. Line L4 runs [Horner's rule](/horner-rule/) for $p$ and $p'$ together, $p'_k = p'_{k-1}z + p_{k-1}$, and the running error bound $\beta = 4u\mu$ of Higham for $p$. Line L5 is the sum that makes the step "implicitly deflate" the other approximations. Line L6 writes the step as $p/(p' - pS)$, which equals $N/(1 - NS)$ but needs no division by $p'$, so it is defined when $p'(z_i) = 0$. Line L8 is the total step (Jacobi) form.

The step is exactly Newton's method on $g_i(z) = p(z)/\prod_{j \ne i}(z - z_j)$, because $g_i'/g_i = p'/p - \sum_{j \ne i} 1/(z - z_j)$. Since $p'/p = \sum_k 1/(z - x_k)$, the function $g_i'/g_i$ is a sum of terms $1/(z - x_k)$ over the roots minus terms $1/(z - z_j)$ over the other approximations. Its complex conjugate is the planar electric field of unit charges at the roots and opposite charges at the other approximations; this is Aberth's physical reading.

## Example

Take $p(z) = z^3 - z - 2$ with Kerner's start $z_k = (0.4 + 0.9i)^k$, $k = 0, 1, 2$, as on the [Durand-Kerner page](/durand-kerner-method/). The roots are $1.5213797068$ and $-0.7606898534 \pm 0.8578736266i$.

| sweep | $z_1$ | $z_2$ | $z_3$ | $\varepsilon_k$ |
|---|---|---|---|---|
| 0 | $1$ | $0.4 + 0.9i$ | $-0.65 + 0.72i$ | $1.6$ |
| 1 | $1.3987186 - 0.1954986i$ | $-4.7917764 + 2.9222001i$ | $-0.7818086 + 0.8260803i$ | $1.7$ |
| 2 | $1.5230870 + 0.0198963i$ | $-0.5749594 - 0.7690014i$ | $-0.7596685 + 0.8579407i$ | $2.1 \times 10^{-1}$ |
| 3 | $1.5213932 - 0.0000065i$ | $-0.7606615 - 0.8580312i$ | $-0.7606898 + 0.8578737i$ | $1.6 \times 10^{-4}$ |
| 4 | $1.5213797$ | $-0.7606899 - 0.8578736i$ | $-0.7606899 + 0.8578736i$ | $6.5 \times 10^{-14}$ |

In sweep 1, $z_2$ is pushed far out, to $-4.79 + 2.92i$, because it starts near $z_3$ and both are drawn to the same root; the repulsion term sends one of them away, and it reaches the other complex root in the next sweep. Then $\varepsilon_{k+1}/\varepsilon_k^3$ is $0.017$ and $0.016$ in sweeps 3 and 4: the order is 3. From the same start Durand-Kerner needed 6 sweeps to get below $10^{-15}$; Aberth gets to $6.5 \times 10^{-14}$ in 4 and to the rounding level in 5.

Sweeps to convergence with the start of L1, against Durand-Kerner:

| polynomial | Aberth sweeps | Durand-Kerner sweeps | Aberth error |
|---|---|---|---|
| $\prod_{k=1}^{5}(z - k)$ | 6 | 9 | $3.2 \times 10^{-14}$ |
| $z^8 - 1$ | 10 | 21 | $3.3 \times 10^{-16}$ |
| $z^{15} - 1$ | 7 | 12 | $3.4 \times 10^{-14}$ |
| $\prod_{k=1}^{10}(z - k)$ | 8 | 12 | $3.9 \times 10^{-10}$ |
| $\prod_{k=1}^{20}(z - k)$ | 11 | 33 | $1.1 \times 10^{-1}$ |
| $(z - 10^{-3})(z - 1)(z - 10^3)$ | 11 | 16 | $1.1 \times 10^{-16}$ |
| $(z - 1)^3(z + 2)$ | 18 | 30 | $7.0 \times 10^{-6}$ |

On 300 random polynomials of degree 2 to 11 with Gaussian complex roots the mean was 7.5 sweeps for Aberth and 11.4 for Durand-Kerner, and all converged.

## Correctness

If the roots are simple with separation $\sigma = \min_{i \ne j}|x_i - x_j|$ and every $|z_i - x_i| \le \varepsilon \le \sigma/(4n)$, then one sweep gives $\varepsilon' \le 3.2(n - 1)\varepsilon^3/\sigma^2$, which is less than $\varepsilon/5$, so the method converges with order 3 from there. The key is the exact error formula $e_i' = e_i^2 S_i/(1 + e_i S_i)$ with $S_i = -\sum_{j \ne i} e_j/((z_i - x_j)(z_i - z_j))$. This is local. The loop always stops, after at most $K$ sweeps. At a root of multiplicity $m$ approached by a symmetric cluster of $m$ approximations, the error is multiplied by exactly $(m - 1)/(m + 1)$ per sweep to leading order. The proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

A sweep evaluates $p$ and $p'$ at each active approximation, $O(n)$ each by Horner's rule, and forms $n$ sums of $n - 1$ terms, so $O(n^2)$ arithmetic, $n$ evaluations of $p$ and $n$ of $p'$. With a cap of $K$ sweeps, $O(Kn^2)$ time and $O(n)$ extra space. The number of sweeps is not bounded a priori; Bini's starting points from the Newton polygon keep it small in practice even for degrees in the thousands.

## Properties

- Simultaneous: all roots at once, with implicit deflation instead of explicit [deflation](/polynomial-deflation/).
- Local order 3 at simple roots (proved), with $n$ evaluations of $p$ and $n$ of $p'$ per sweep.
- Linear at a root of multiplicity $m$, with ratio $(m - 1)/(m + 1)$ for a symmetric cluster; the attainable accuracy is about $u^{1/m}$.
- Global convergence is not proved. It is observed on every start tested here.
- The stopping rule of L4 gives backward stable roots: each frozen $z_i$ is a root of a polynomial whose coefficients differ from the given ones at the level of the rounding errors of the evaluation.

## Variants and improvements

- Gauss-Seidel form: use new $z_j$ as soon as they are computed; locally it is at least as fast, and often a little faster in practice.
- Maehly's correction for Newton's method after deflation, $p/(p' - p\sum_j 1/(z - \xi_j))$ with already found roots $\xi_j$, has the same form; Aberth's method applies it to all approximations at once.
- Bini's MPSolve chooses starting points from the Newton polygon of $\log|a_k|$, freezes roots by a running error test, and raises the working precision for clusters; inclusion discs certify the result.
- [Laguerre's method](/laguerre-method/) also has order 3 and is used with deflation for one root at a time.
- The eigenvalues of the [companion matrix](/companion-matrix-method/) give all roots with a backward stable algorithm in $O(n^3)$, or $O(n^2)$ with structured QR.

## When to use it

Use it for all roots of a polynomial of moderate or large degree, especially in multiple precision, where its $O(n^2)$ cost per sweep beats the $O(n^3)$ of a dense eigenvalue solver. Use [Durand-Kerner](/durand-kerner-method/) when $p'$ is not available. Use the [companion matrix](/companion-matrix-method/) when a backward stable black box is enough and $n$ is small. Use [Newton's method](/newton-raphson-method/) or a bracketing method for one real root of a function that is not a polynomial.

## Pitfalls

- L1: a bad start costs sweeps. Starting points on one circle work for roots of similar size; for roots of very different sizes the radii should come from the Newton polygon, as in Bini's start. With the start of L1, roots $10^{-3}$, $1$ and $10^3$ still took 11 sweeps.
- L4: freezing at the rounding floor gives backward accuracy only. On the [Wilkinson polynomial](/wilkinson-polynomial/) of degree 20 the frozen roots have errors up to $0.11$; see [root conditioning](/root-conditioning/).
- L5: two equal approximations make $S$ infinite. The implementation raises an error; the repulsion term makes this rare.
- L6: writing the step as $N/(1 - NS)$ divides by $p'(z_i)$, which fails at a critical point of $p$. The form $p/(p' - pS)$ is defined there; with $p = z^2 - 1$ and start $0, 3$ it converges although $p'(0) = 0$.
- L7: at a multiple root the corrections do not fall below $\delta|z_i|$; L4 freezes instead, at errors about $u^{1/m}$.

## Implementations

## History

L. W. Ehrlich published the iteration in 1967 as "a modified Newton method for polynomials" and proved cubic convergence. Oliver Aberth derived it independently in 1973 from an electrostatic model, and proposed starting points on a circle. Earlier, H. J. Maehly (1954) had used the same correction to avoid explicit deflation in Newton's method, and Börsch-Supan (1963) had a related formula in his work on a posteriori error bounds. Dario Bini's 1996 analysis and the MPSolve package of Bini and Fiorentino (2000), later extended by Bini and Robol, made the method the standard for high-degree and multiprecision root finding.

## References
