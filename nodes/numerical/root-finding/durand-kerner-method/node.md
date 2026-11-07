---
tag: VNB2F0
kind: algorithm
slug: durand-kerner-method
name: Durand-Kerner method
aliases:
- Weierstrass method
- Durand-Kerner-Weierstrass method
- Weierstrass-Durand-Kerner iteration
area: numerical/root-finding
level: advanced
summary: Simultaneous iteration that corrects all n root approximations of a polynomial at once by the Weierstrass correction. Quadratic near simple roots, linear at multiple roots.
solves: [polynomial-root-finding]
model: real-ram
complexity:
  vars: {n: "the degree of the polynomial", K: "the number of sweeps"}
  time: {worst: "O(K n^2)", step: "O(n^2)"}
  space: {extra: Θ(n)}
  evaluations: {worst: "K n", step: "n"}
properties: {deterministic: true, recursive: false, simultaneous: true, derivative_free: true, global_convergence_proved: false}
prereqs: [fundamental-theorem-of-algebra, horner-rule, newton-raphson-method]
see_also: [aberth-ehrlich-method, companion-matrix-method, jenkins-traub-algorithm, polynomial-root-finding, cauchy-root-bound, root-conditioning, wilkinson-polynomial, polynomial-deflation]
sources:
  - paper: "Immo O. Kerner, Ein Gesamtschrittverfahren zur Berechnung der Nullstellen von Polynomen, Numerische Mathematik 8, 290-294, 1966"
    locator: the simultaneous (total step) iteration and its quadratic convergence for simple roots
  - book: "Emile Durand, Solutions numériques des équations algébriques, Tome I, Masson, Paris, 1960"
    locator: the iteration for all roots at once
  - book: "Karl Weierstrass, Neuer Beweis des Satzes, dass jede ganze rationale Function einer Veränderlichen dargestellt werden kann als ein Product aus linearen Functionen derselben Veränderlichen, Sitzungsberichte der Königlich Preussischen Akademie der Wissenschaften zu Berlin, 1891"
    locator: the correction term used in a constructive proof of the fundamental theorem of algebra
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 5.1, Horner's method (the error bound and the running error bound used in the stopping rule)
  - paper: "Bernhard Reinke, Dierk Schleicher and Michael Stoll, The Weierstrass root finder is not generally convergent, Mathematics of Computation 92, 2023"
    locator: open sets of starting points that do not converge
---

The Durand-Kerner method finds all $n$ roots of a polynomial of degree $n$ at once. It keeps $n$ approximations $z_1, \dots, z_n$ and moves each by the Weierstrass correction $W_i = p(z_i) / (a_0 \prod_{j \ne i}(z_i - z_j))$. If the other $n - 1$ approximations were exact, $W_i$ would be the exact error of $z_i$; in general it is a correction that converges quadratically once every $z_i$ is close to a distinct simple root. Each sweep costs $n$ evaluations of $p$ and $O(n^2)$ arithmetic, and no derivative. It works in complex arithmetic and needs no [deflation](/polynomial-deflation/). Its global convergence from the usual circle of starting points is observed in practice but not proved, and there are open sets of starting points where it fails.

## In plain words

A polynomial of degree $n$ has $n$ roots, perhaps complex. Make $n$ guesses, one for each root. For each guess, pretend the other guesses are already right. Then the polynomial divided by the factors those other guesses give is a straight line, and the root of that line is a better guess. Do this for all guesses at once, then repeat. Far from the answer the guesses spread out and drift; close to it each sweep roughly doubles the number of correct digits. When a root is repeated, the guesses for it crowd together and progress slows to a steady crawl.

## The problem

Notation on the root-finding pages: $f$ is the function, $x^*$ a root, $x_k$ the iterates and $e_k = x_k - x^*$ the error. A method has [order](/order-of-convergence/) $q$ and rate constant $C$ when $|e_{k+1}| \approx C |e_k|^q$, with $0 < C < 1$ when $q = 1$. A root has [multiplicity](/multiplicity-of-roots/) $m$ when $f(x^*) = \cdots = f^{(m-1)}(x^*) = 0 \ne f^{(m)}(x^*)$. The cost is the number of evaluations of $f$ (and of $f'$ where a method uses it). A method of order $q$ that needs $w$ evaluations in each step has efficiency index $q^{1/w}$.

Here $f = p$ is a polynomial $p(z) = a_0 z^n + a_1 z^{n-1} + \cdots + a_n$ with complex coefficients and $a_0 \ne 0$. By the [fundamental theorem of algebra](/fundamental-theorem-of-algebra/) it has roots $x_1, \dots, x_n$, counted with multiplicity. The input is the coefficient list, a relative tolerance $\delta$ and a cap $K$ on the sweeps. The output is $n$ approximations and a flag. In one sweep the method updates all $n$ approximations, so the error of a sweep is $\varepsilon_k = \max_i |z_i^{(k)} - x_i|$ for a suitable matching of approximations to roots. Since a sweep costs $n$ evaluations, its efficiency index per evaluation is $2^{1/n}$; counted per root, each root costs one evaluation per sweep and gains order 2.

## The algorithm

```pseudo id=main
DURAND-KERNER(a0, ..., an, delta, K):
L1   z1, ..., zn <- n distinct points on a circle about c = -a1/(n a0)
L2   for k = 1, 2, ..., K:
L3       for each active i:
L4           evaluate p(zi) by Horner's rule with a running error bound beta_i;  if |p(zi)| <= beta_i then freeze i
L5           d <- a0 * prod over j != i of (zi - zj);  fail if d = 0
L6           Wi <- p(zi)/d;  zi_new <- zi - Wi
L7           if |Wi| <= delta |zi_new| then freeze i
L8       z <- z_new                                 // all updates use the old z (total step)
L9       if no index is active then return z
L10  return z, not converged
```

Line L1 places the starting points on a circle about the centroid $c = -a_1/(n a_0)$ of the roots, of radius $1.5\,(|p(c)|/|a_0|)^{1/n}$, which is 1.5 times the geometric mean of the distances from $c$ to the roots, capped by the [Fujiwara bound](/cauchy-root-bound/). The angles $2\pi k/n + 0.4$ avoid a start that is symmetric with the roots. Line L4 is [Horner's rule](/horner-rule/) with the running error bound of Higham: alongside $p_k = p_{k-1} z + a_k$ it accumulates $\mu_k = \mu_{k-1}|z| + |p_k|$, and $\beta = 4u\mu_n$ bounds the rounding error of the computed $p(z)$. A root whose residual is below $\beta$ cannot be improved in this arithmetic and is frozen. Line L5 forms the denominator, which is $p'$-free: it is the derivative at $z_i$ of the monic product of the current approximations, scaled by $a_0$. Line L8 makes this the total step (Jacobi) form of Kerner; the single step (Gauss-Seidel) form uses new values as soon as they are computed.

Kerner observed a neat identity: for any $n$ distinct points, $\sum_i W_i = \sum_i z_i + a_1/a_0$, by the Lagrange interpolation of $p/a_0 - \prod(z - z_j)$. So after one total step with no frozen roots, $\sum_i z_i^{\text{new}} = -a_1/a_0$, the sum of the roots, and it stays so.

## Example

Take $p(z) = z^3 - z - 2$ with Kerner's classic start $z_k = (0.4 + 0.9i)^k$ for $k = 0, 1, 2$. The roots are $1.5213797068$ and $-0.7606898534 \pm 0.8578736266i$.

| sweep | $z_1$ | $z_2$ | $z_3$ | $\varepsilon_k$ |
|---|---|---|---|---|
| 0 | $1$ | $0.4 + 0.9i$ | $-0.65 + 0.72i$ | $1.6$ |
| 1 | $1.1803867 + 1.0111151i$ | $-0.8185621 - 1.8991622i$ | $-0.3618246 + 0.8880471i$ | $1.1$ |
| 2 | $1.3050734 - 0.0062184i$ | $-0.6448359 - 1.0475523i$ | $-0.6602375 + 1.0537707i$ | $2.2 \times 10^{-1}$ |
| 3 | $1.5243365 - 0.0001376i$ | $-0.7618841 - 0.8615343i$ | $-0.7624524 + 0.8616720i$ | $4.2 \times 10^{-3}$ |
| 4 | $1.5213862 - 0.0000002i$ | $-0.7606918 - 0.8578864i$ | $-0.7606944 + 0.8578866i$ | $1.4 \times 10^{-5}$ |
| 5 | $1.5213797$ | $-0.7606899 - 0.8578736i$ | $-0.7606899 + 0.8578736i$ | $1.4 \times 10^{-10}$ |
| 6 | $1.5213797$ | $-0.7606899 - 0.8578736i$ | $-0.7606899 + 0.8578736i$ | below $10^{-15}$ |

The sum of the three approximations is $0.75 + 1.62i$ at the start and $0$ (to rounding) from sweep 1 on, as the identity says, since $a_1 = 0$. From sweep 3 on the error squares: $4.2 \times 10^{-3}$, $1.4 \times 10^{-5}$, $1.4 \times 10^{-10}$. The seventh sweep freezes all three roots, for 21 evaluations of $p$ in total.

On $\prod_{k=1}^{5}(z - k)$ from the circle start of L1, the method stops after 9 sweeps and 45 evaluations with error $1.2 \times 10^{-14}$, and the errors $8.3 \times 10^{-3}$, $6.9 \times 10^{-5}$, $4.8 \times 10^{-9}$, $9.3 \times 10^{-13}$ give $\log \varepsilon_{k+1}/\log \varepsilon_k = 2.0$. On $(z - 1)^3 (z + 2)$ the error falls by a factor close to $2/3$ per sweep and stops near $9 \times 10^{-6}$, about $u^{1/3}$.

## Correctness

If all roots are simple, with minimum separation $\sigma = \min_{i \ne j}|x_i - x_j|$, and every approximation satisfies $|z_i - x_i| \le \varepsilon \le \sigma/(4n)$, then one sweep gives $\varepsilon' \le 3.3(n - 1)\varepsilon^2/\sigma$ and $\varepsilon' \le 0.83\,\varepsilon$, so the method converges with order 2 from there. The key is the exact error formula $z_i' - x_i = -(z_i - x_i)\left(\prod_{j \ne i}\left(1 + \frac{z_j - x_j}{z_i - z_j}\right) - 1\right)$. This is a local result. The loop always terminates, since it runs at most $K$ sweeps and freezes each root at most once. The proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

Each sweep evaluates $p$ at every active approximation, $n$ Horner evaluations of $O(n)$ each, and forms $n$ products of $n - 1$ factors, so $O(n^2)$ arithmetic and at most $n$ evaluations of $p$ per sweep. With a cap of $K$ sweeps the cost is $O(Kn^2)$ time and $O(n)$ extra space. The number of sweeps is not bounded a priori: far from the roots the circle of approximations contracts slowly, and the quadratic phase starts only near the roots. Observed with the start of L1: 9 sweeps for degree 5, 12 for degree 10, 21 for the 8th roots of unity, 33 for the Wilkinson polynomial of degree 20.

## Properties

- Simultaneous: all roots at once, with no deflation and so no growth of deflation errors.
- Derivative-free: the denominator plays the role of $p'(z_i)$; it is the Newton step for the system of Vieta's equations.
- Local order 2 at simple roots (proved), linear at a root of multiplicity $m$ with observed ratio close to $(m - 1)/m$ and attainable accuracy about $u^{1/m}$.
- Global convergence: not proved; Reinke, Schleicher and Stoll (2023) showed open sets of starting points that never converge.
- Easy to parallelise, since the total step updates are independent.

## Variants and improvements

- The single step (Gauss-Seidel) form uses each new $z_i$ at once; it is still quadratic locally and often a little faster.
- The [Aberth-Ehrlich method](/aberth-ehrlich-method/) uses $p'$ and has order 3 per sweep; it is the basis of MPSolve.
- Börsch-Supan's variant $z_i - W_i / (1 + \sum_{j \ne i} W_j/(z_i - z_j))$ has order 3 without $p'$, and Nourein's modification of it has order 4.
- Starting points from the Newton polygon of $|a_k|$ adapt the radii to roots of very different sizes.
- For the eigenvalue route instead, see the [companion matrix method](/companion-matrix-method/).

## When to use it

Use it when you want all roots of a moderate degree polynomial with short, parallel code and no derivative. For production work, prefer the [Aberth-Ehrlich method](/aberth-ehrlich-method/) with good starting points, the [companion matrix](/companion-matrix-method/) eigenvalues for a backward stable black box, or the [Jenkins-Traub algorithm](/jenkins-traub-algorithm/) for one root at a time with deflation.

## Pitfalls

- L1: a symmetric start can trap the iteration. With radius factor 1 instead of 1.5, so that the start circle passes through the roots of $z^8 - 1$, the error jumped to $3.9 \times 10^3$ in sweep 4 and took 72 sweeps in all, against 21 with factor 1.5. No choice of start is proved to work for every polynomial.
- L4: freezing at the rounding floor gives a backward stable answer, not an accurate one. For the [Wilkinson polynomial](/wilkinson-polynomial/) of degree 20 the frozen roots have residuals at the floor but errors up to $0.15$, because the roots are very sensitive to the coefficients; see [root conditioning](/root-conditioning/).
- L5: two approximations that meet make the denominator zero. With $p = z^2 - 4z + 2$ and start $0, 1$, both move to $2$ in the first sweep; the implementation raises an error instead of dividing by zero.
- L7: at a multiple root the corrections stay large relative to the attainable accuracy, so freezing happens at L4 instead, with errors about $u^{1/m}$.
- L6 with huge coefficients: the products in L5 can overflow. Scale the polynomial, $z \mapsto sz$, before calling.

## Implementations

## History

Karl Weierstrass used the correction in 1891 in a constructive proof of the fundamental theorem of algebra. The iteration as a numerical method was given by Emile Durand in his 1960 book on the numerical solution of algebraic equations and by Immo Kerner in 1966, who proved local quadratic convergence of the total step form and noted that it is Newton's method for the Vieta equations. It is also attributed to Dochev (1962). In 2023 Reinke, Schleicher and Stoll showed that, unlike what had long been conjectured, the method is not generally convergent.

## References
