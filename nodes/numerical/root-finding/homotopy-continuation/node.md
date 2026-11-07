---
tag: DVD26W
kind: algorithm
slug: homotopy-continuation
name: Homotopy continuation
aliases:
- continuation method
- homotopy method
- numerical continuation
- path tracking
- polynomial homotopy continuation
area: numerical/root-finding
level: advanced
summary: Track solutions of a deformed system from an easy start system to the target. With the gamma trick it finds every isolated root of a polynomial system with probability one.
solves: [systems-of-nonlinear-equations]
model: real-ram
complexity:
  vars: {n: "the number of variables", D: "the number of paths, the product of the degrees", S: "the number of steps on one path", K: "the cap on the steps of one path"}
  time: {worst: "O(D K n^3)", average: "O(D S n^3)"}
  space: {extra: Θ(n^2)}
properties: {deterministic: false, recursive: false, bracketing: false, derivative_free: false, global: true, simultaneous: true}
prereqs: [newton-method-for-systems, systems-of-nonlinear-equations, euler-method]
see_also: [polynomial-system-solving, newton-method-for-systems, broyden-method, kantorovich-theorem, fundamental-theorem-of-algebra, durand-kerner-method, companion-matrix-method, multiplicity-of-roots]
sources:
  - book: "Eugene L. Allgower and Kurt Georg, Introduction to Numerical Continuation Methods, SIAM Classics in Applied Mathematics 45, 2003 (reprint of the 1990 Springer edition)"
    locator: the Davidenko equation, predictor-corrector methods and step length control, and the homotopy methods for polynomial systems
  - book: "Andrew J. Sommese and Charles W. Wampler, The Numerical Solution of Systems of Polynomials Arising in Engineering and Science, World Scientific, 2005"
    locator: the total degree homotopy, the gamma trick and its probability one theorem, path tracking and endgames for singular end points
  - paper: "T. Y. Li, Numerical solution of multivariate polynomial systems by homotopy continuation methods, Acta Numerica 6, 399-436, 1997"
    locator: the survey of total degree, multihomogeneous and polyhedral homotopies and the random gamma
  - paper: "C. B. Garcia and W. I. Zangwill, Finding all solutions to polynomial systems and other systems of equations, Mathematical Programming 16, 159-176, 1979"
    locator: the homotopy from a start system with known roots that reaches all solutions of a polynomial system
  - paper: "Carlos Beltrán and Luis Miguel Pardo, Fast linear homotopy to find approximate zeros of polynomial systems, Foundations of Computational Mathematics 11, 95-129, 2011"
    locator: the randomized algorithm with average polynomial running time, the answer to Smale's 17th problem in the probabilistic sense
---

Homotopy continuation solves $F(x) = 0$ by deforming it into a problem whose solutions are known and following each solution as the deformation is undone. For a polynomial system $F = (F_1, \dots, F_n)$ in $\mathbb{C}^n$, where $F_i$ has degree $d_i$, the total degree homotopy is
$$H(x, t) = (1 - t)\,\gamma\,G(x) + t\,F(x), \qquad G_i(x) = x_i^{d_i} - 1,$$
with a random complex constant $\gamma$. At $t = 0$ the solutions are the $D = d_1 \cdots d_n$ tuples of roots of unity. As $t$ goes from 0 to 1, each one moves along a smooth path, and a predictor-corrector method tracks it. The predictor solves the Davidenko equation $H_x\,\dot x = -H_t$ and the corrector applies [Newton's method](/newton-method-for-systems/) to $H(\cdot, t)$. With probability one in $\gamma$, no path meets a singularity before $t = 1$, and every isolated solution of $F$ is the end point of a path. This makes the method the standard numerical way to find all the solutions of a polynomial system. It is the engine of Bertini, PHCpack and HomotopyContinuation.jl.

## In plain words

Newton's method needs a good starting point and finds one root. Homotopy continuation builds the starting points. It starts from an easy problem with the same number of solutions, then slowly turns the easy problem into the real one, taking many small steps and correcting with Newton at each step so that it never loses track. The random complex number $\gamma$ is the trick that makes it work: it pushes the paths off the real line in a random direction, so that with probability one no two paths ever touch, and none turns back.

## The problem

Notation on the root-finding pages: $f$ is the function, $x^*$ a root, $x_k$ the iterates and $e_k = x_k - x^*$ the error. A method has [order](/order-of-convergence/) $q$ and rate constant $C$ when $|e_{k+1}| \approx C |e_k|^q$, with $0 < C < 1$ when $q = 1$. A root has [multiplicity](/multiplicity-of-roots/) $m$ when $f(x^*) = \cdots = f^{(m-1)}(x^*) = 0 \ne f^{(m)}(x^*)$. The cost is the number of evaluations of $f$ (and of $f'$ where a method uses it). A method of order $q$ that needs $w$ evaluations in each step has efficiency index $q^{1/w}$.

Here $f = F: \mathbb{C}^n \to \mathbb{C}^n$ is a square polynomial system with Jacobian $F'$, and the goal is all its isolated solutions. A univariate polynomial is the case $n = 1$, with $G(x) = x^n - 1$. The cost of one path is counted in steps; each step costs 4 evaluations of $(H_x, H_t)$ for the predictor and 1 to 3 evaluations of $(H, H_x)$ for the corrector. The tracker of one path stops when $t$ reaches 1, when $|x|$ exceeds a radius $R$ (a solution at infinity), when the step size falls below $h_{\min}$, or after $K$ steps.

## The algorithm

```pseudo id=main
TRACK(H, x0, h0, tol, R, K):
L1   x <- x0;  t <- 0;  h <- h0
L2   while t < 1:
L3       h <- min(h, 1 - t)
L4       predictor:  y <- one Runge-Kutta step of  dx/dt = -H_x(x, t)^-1 H_t(x, t)  from (x, t) with step h
L5       corrector:  up to 3 Newton steps  y <- y - H_x(y, t+h)^-1 H(y, t+h);  accept if they contract fast and the last is <= tol (1 + |y|)
L6       if accepted:  x <- y;  t <- t + h;  after 3 acceptances in a row  h <- min(2h, 0.1)
L7       else:  h <- h / 2;  if h < h_min then return x, "failed" (or "singular-end" if 1 - t is tiny)
L8       if |x| > R then return x, "diverged"
L9       if K steps have been used then return x, "failed"
L10  return x, "success"
```

To solve $F = 0$, pick $\gamma = e^{i\theta}$ with $\theta$ uniform in $[0, 2\pi)$, run TRACK from each of the $D$ start points, and refine each end point by Newton's method on $F$. The reference code accepts an end point as a nonsingular solution when that refinement converges and the Jacobian there is well conditioned; otherwise it labels the end point "singular-end". Line L4 integrates the tangent of the path to fourth order. Line L5 pulls the prediction back onto the path. Its acceptance test does two jobs. The first Newton step must be small relative to $|y|$, and the steps must contract by a factor of 4 or more. Together these guard against path jumping, where Newton converges to a neighbouring path. Lines L6 and L7 adapt the step size. For polynomials in one variable, the reference code first scales $x$ by $|a_n/a_0|^{1/n}$, the geometric mean of the root moduli, so that the start roots have roughly the right size.

## Example

For $x^3 - 6x^2 + 11x - 6$, after scaling, the three paths start at the cube roots of unity. They take 12 steps each and end at $1, 2, 3$, with errors below $10^{-13}$ after refinement. For the system $x^2 + y^2 = 5$, $xy = 2$, Bézout's number is $2 \cdot 2 = 4$. The four paths take 12, 17, 17 and 12 steps, about 6 evaluations per step, and end at $(1, 2), (2, 1), (-1, -2), (-2, -1)$.

For $xy = 1$, $xy + x = 2$, Bézout's number is again 4, but the only solution is $(1, 1)$. The other three solutions of the homogenized system lie at infinity. One path ends at $(1, 1)$, and the other three grow without bound as $t \to 1$ and are reported as "diverged". For $(x - 1)^2(x - 2)$, two paths converge to the double root. Near $t = 1$ they approach each other like $(1 - t)^{1/2}$, the corrector's Jacobian becomes singular, and both are reported as "singular-end" with $x$ within $10^{-6}$ of 1. Over 500 random polynomials of degree 1 to 5 with roots in the square $[-2, 2]^2$, every root was the end of exactly one path. The largest error was $3 \times 10^{-14}$, and the average was 15 steps and 92 evaluations per path.

## Correctness

For one polynomial the key facts can be proved directly. The leading coefficient of $H(\cdot, t)$ vanishes for no $t \in [0, 1)$ unless $\gamma$ is a negative real. The discriminant of $G + wF$ in the parameter $w$ has finitely many roots. So for all but finitely many arguments of $\gamma$, the $n$ roots of $H(\cdot, t)$ stay simple for all $t \in [0, 1)$. They form $n$ disjoint smooth paths by the implicit function theorem, and as $t \to 1$ they converge to the roots of $p$, with exactly $m$ paths going to a root of multiplicity $m$. For systems, the same statement is the gamma trick theorem of Sommese and Wampler: with probability one, the paths are smooth and disjoint on $[0, 1)$, every isolated solution of multiplicity $\mu$ is the limit of exactly $\mu$ paths, and the remaining paths diverge or go to positive-dimensional solution sets. TRACK terminates, because each pass of L2 increases $t$ or halves $h$, and L7 and L9 bound both. Whether the heuristic step control of L5 to L7 keeps the numerical path on the right branch is observed, not proved; certified trackers based on Smale's alpha theory guarantee it. See [the correctness proof](proofs/correctness.md).

## Complexity

The total degree homotopy tracks $D = \prod d_i$ paths. This can be far more than the number of solutions. Multihomogeneous and polyhedral (BKK) homotopies track fewer paths, matching the mixed volume of the Newton polytopes. Each step costs one Runge-Kutta predictor (4 linear solves) and up to 3 Newton corrections, so $O(n^3)$ plus the evaluation cost. The number of steps $S$ depends on the conditioning along the path. It was 12 to 17 on the small examples and 15 on average for the random polynomials. In the worst case it is bounded only by the cap $K$. Beltrán and Pardo showed that a randomized linear homotopy finds an approximate zero in expected time polynomial in the input size, and Lairez later derandomized this. These are bounds on certified tracking, not on the heuristic step control here.

## Properties

- Global: needs no starting guesses and, with probability one, reaches every isolated solution of a square polynomial system.
- Paths are independent, so the method is trivially parallel.
- The randomness is only in $\gamma$. The reference code fixes the seed, so runs are reproducible.
- Locally, the predictor has order 4 (the local error of one step behaves like $h^5$, checked in the tests) and the corrector converges quadratically near a nonsingular path.
- At a root of multiplicity $m$ the end of the path is singular. Plain tracking then gives accuracy only about $u^{1/m}$, which is why practical codes use endgames.

## Variants and improvements

- **Endgames.** The power series and Cauchy endgames use the fact that, near a singular end point, the path is a Puiseux series in $(1 - t)^{1/c}$. Extrapolating along it, or integrating around a small loop, recovers multiple roots accurately.
- **Better start systems.** Multihomogeneous Bézout homotopies and polyhedral homotopies (Huber and Sturmfels; Verschelde's PHCpack) cut the number of paths to the mixed volume bound.
- **Parameter homotopies.** To solve many systems in one family, solve one generic member once, then track only its solutions to each new parameter value.
- **Certified tracking.** Step sizes chosen from alpha theory or interval arithmetic guarantee that no path jumps, at a higher cost per step.
- **Adaptive precision.** Bertini raises the working precision on ill conditioned stretches of a path.
- **Nonpolynomial problems.** Newton homotopy $H(x, t) = F(x) - (1 - t)F(x_0)$ and probability one homotopies (Chow, Mallet-Paret and Yorke) give globally convergent methods for smooth systems, without the guarantee of finding all roots.

## When to use it

Use it when you need all the isolated solutions of a polynomial system of moderate size, as in kinematics, chemical equilibrium or computer vision, or when Newton's method needs a starting point you do not have. For one polynomial in one variable, the [companion matrix method](/companion-matrix-method/) or Aberth's method is cheaper and simpler. Exact elimination methods ([polynomial system solving](/polynomial-system-solving/) with Gröbner bases) give certified answers for small systems with rational coefficients, but they blow up on larger ones.

## Pitfalls

- L4 and L5: path jumping. If the step is too long, Newton can converge to a neighbouring path. Two paths then end at the same root and another root is never found. Insist on fast contraction of the corrector and a small first correction.
- L5: on very ill conditioned problems the corrector cannot reach the tolerance at all. On the [Wilkinson polynomial](/wilkinson-polynomial/) of degree 20, the reference tracker in double precision brings only 5 of the 20 paths to a certified end, while all paths succeed on the degree 10 case. Adaptive precision is the cure.
- L7: a path that ends at a multiple root makes the step size collapse near $t = 1$. Label it as singular, refine it with an endgame, and do not report it as a failure of the method.
- L8: paths to solutions at infinity grow like $(1 - t)^{-1/c}$. Without the radius test they consume the whole step budget. Projective coordinates remove the problem.
- The choice of $\gamma$: with a real $\gamma$, or with $\gamma = 1$, paths can meet at a real singular point and the method can fail for every seed. The randomness of the argument of $\gamma$ is essential.
- Scaling: if the start system's roots are far from the target's, the paths move very fast near $t = 0$. Scaling the variables, as the reference code does for one polynomial, avoids tiny steps.

## Implementations

## History

Continuation ideas go back to the nineteenth century. Davidenko (1953) proposed solving nonlinear systems by integrating the differential equation of the path, and Kellogg, Li and Yorke (1976) and Chow, Mallet-Paret and Yorke (1978) built globally convergent probability one methods on homotopies. Drexler (1977) and Garcia and Zangwill (1979) used homotopies from start systems with known roots to compute all solutions of polynomial systems. Morgan's book (1987) and the random gamma trick made the method practical. Polyhedral homotopies came in the 1990s, Sommese, Verschelde and Wampler founded numerical algebraic geometry around 2000, and Beltrán and Pardo (2009) and Lairez (2017) resolved Smale's 17th problem with homotopy algorithms.

## References
