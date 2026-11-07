---
tag: W75WVA
kind: algorithm
slug: jenkins-traub-algorithm
name: Jenkins-Traub algorithm
aliases:
- Jenkins-Traub method
- cpoly
- rpoly
- three-stage algorithm
area: numerical/root-finding
level: advanced
summary: Three-stage shifted iteration for polynomial roots with guaranteed convergence. It finds the roots one at a time, smallest first, and removes each by deflation.
solves: [polynomial-root-finding]
model: real-ram
complexity:
  vars: {n: "the degree of the polynomial", K: "the cap on the total number of steps"}
  time: {worst: "O(K n)", average: "O(n^2)"}
  space: {extra: "Θ(n)"}
properties: {deterministic: true, recursive: false, bracketing: false, derivative_free: true, global: true, backward_stable: true}
prereqs: [polynomial-deflation, horner-rule, newton-raphson-method]
see_also: [companion-matrix-method, inverse-iteration, rayleigh-quotient-iteration, cauchy-root-bound, laguerre-method, durand-kerner-method, aberth-ehrlich-method, wilkinson-polynomial]
sources:
  - paper: "M. A. Jenkins and J. F. Traub, A three-stage variable-shift iteration for polynomial zeros and its relation to generalized Rayleigh iteration, Numerische Mathematik 14, 252-263, 1970"
    locator: the three stages, the convergence theorems for the fixed-shift and variable-shift stages, and the relation to Rayleigh quotient iteration
  - paper: "M. A. Jenkins and J. F. Traub, A three-stage algorithm for real polynomials using quadratic iteration, SIAM Journal on Numerical Analysis 7(4), 545-566, 1970"
    locator: the real version with quadratic factors (RPOLY)
  - paper: "M. A. Jenkins and J. F. Traub, Algorithm 419: zeros of a complex polynomial, Communications of the ACM 15(2), 97-99, 1972"
    locator: the CPOLY program, its shift rotation by 94 degrees, and its stopping rule based on a rounding error bound
  - paper: "M. A. Jenkins, Algorithm 493: zeros of a real polynomial, ACM Transactions on Mathematical Software 1(2), 178-189, 1975"
    locator: the RPOLY program
  - paper: "J. F. Traub, A class of globally convergent iteration functions for the solution of polynomial equations, Mathematics of Computation 20, 113-138, 1966"
    locator: the H-polynomial recurrence that the three-stage algorithm builds on
  - book: "William H. Press, Saul A. Teukolsky, William T. Vetterling and Brian P. Flannery, Numerical Recipes, 3rd edition, Cambridge University Press, 2007"
    locator: the section on roots of polynomials, which describes Jenkins-Traub as a standard black-box method
---

The Jenkins-Traub algorithm finds all the roots of a polynomial $p(z) = a_0z^n + \cdots + a_n$ with complex coefficients, one at a time. For each root it builds a sequence of polynomials $H^{(\lambda)}$ of degree $n - 1$ by the recurrence
$$H^{(\lambda+1)}(z) = \frac{1}{z - s_\lambda}\left(H^{(\lambda)}(z) - \frac{H^{(\lambda)}(s_\lambda)}{p(s_\lambda)}\,p(z)\right).$$
With shifts that move toward a root $\alpha_1$, the $H^{(\lambda)}$ converge to a multiple of $p(z)/(z - \alpha_1)$. So $s - p(s)/\bar H(s)$, with $\bar H$ the monic normalisation of $H$, becomes an ever better estimate of $\alpha_1$. The three stages are a few steps with shift 0, then a fixed shift on a circle near the smallest roots, then a variable shift that converges with order $1 + \varphi \approx 2.62$. Each root found is divided out ([deflation](/polynomial-deflation/)), and the roots come out roughly in order of increasing modulus, which keeps the deflation stable. Its programs CPOLY (complex coefficients) and RPOLY (real coefficients) were standard library root finders for decades.

## In plain words

Dividing $p$ by $z - \alpha$ for a root $\alpha$ leaves a polynomial of degree $n - 1$. Jenkins-Traub tries to discover that quotient without knowing $\alpha$. It starts from $p'$, which is a mix of all the quotients $p(z)/(z - \alpha_i)$, and repeatedly applies an operation that amplifies the quotient for the root closest to a chosen point $s$. Once one quotient dominates, comparing $p$ with it at $s$ tells you where the root is. Moving $s$ to that estimate makes the amplification even stronger, so the last stage converges very fast.

## The problem

Notation on the root-finding pages: $f$ is the function, $x^*$ a root, $x_k$ the iterates and $e_k = x_k - x^*$ the error. A method has [order](/order-of-convergence/) $q$ and rate constant $C$ when $|e_{k+1}| \approx C |e_k|^q$, with $0 < C < 1$ when $q = 1$. A root has [multiplicity](/multiplicity-of-roots/) $m$ when $f(x^*) = \cdots = f^{(m-1)}(x^*) = 0 \ne f^{(m)}(x^*)$. The cost is the number of evaluations of $f$ (and of $f'$ where a method uses it). A method of order $q$ that needs $w$ evaluations in each step has efficiency index $q^{1/w}$.

Here $f = p$ is a polynomial of degree $n \ge 1$ with complex coefficients, $a_0 \ne 0$, all finite. The task is to return its $n$ roots as a list with multiplicity. The iterates are the shifts $s_\lambda$, and the error is $e_\lambda = s_\lambda - \alpha_1$. A step evaluates $p$ and $H$ at the same point by [Horner's rule](/horner-rule/), and the synthetic division that does this also gives the next $H$. So $w = 2$ evaluations of polynomials of degree at most $n$ per step, which is $O(n)$ arithmetic. With order $q = 1 + \varphi$ in the third stage, the efficiency index is $(1 + \varphi)^{1/2} = \varphi \approx 1.62$. A root is accepted when $|p(s)| \le 20u\sum_k |a_k||s|^{n-k}$, with $u = 2^{-53}$: the value of $p$ is then within a small multiple of the rounding error bound of Horner's rule, and further steps cannot be trusted to improve it. The run stops after $K$ steps in total in any case.

## The algorithm

```pseudo id=main
JENKINS-TRAUB(a_0..a_n, M, L, max_shifts, K):
L1   roots <- []; strip zero roots (trailing zero coefficients); make p monic
L2   while deg p >= 2:
L3       H <- p'/n;  do M no-shift steps (shift s = 0)                                   (stage 1)
L4       beta <- the Cauchy lower bound on |roots of p|;  theta <- 49 degrees
L5       for attempt = 1 .. max_shifts:
L6           theta <- theta + 94 degrees;  s <- beta e^(i theta)
L7           repeat up to L * attempt times: step with fixed shift s, t <- s - p(s)/H(s)      (stage 2)
L8               if |t_(λ+1) - t_λ| <= |t_λ|/2 and |t_λ - t_(λ-1)| <= |t_(λ-1)|/2: run up to 10 steps with s <- t (stage 3) until |p(s)| <= 20 u sum |a_k||s|^(n-k)
L9           if stage 3 accepted a root then leave the loop
L10      if no root was accepted then return roots, status "failed" (or "max-iter" after K steps)
L11      append the root s to roots;  p <- p / (z - s)
L12  if deg p = 1 then append -p_1/p_0;  return roots, status "done"
```

Line L3 starts from $H^{(0)} = p'/n$, which is a combination of all the quotients $p(z)/(z - \alpha_i)$ with positive weights, the multiplicities. The steps with shift 0 multiply each weight by $1/\alpha_i$ (up to a common factor), which favours the small roots. Line L4 computes $\beta$, the positive root of $|a_0|x^n + \cdots + |a_{n-1}|x - |a_n|$. Every root has modulus at least $\beta$ (see the [Cauchy bound](/cauchy-root-bound/)), so the shift circle of radius $\beta$ lies inside the smallest root circle. Line L6 picks the shift on that circle, with an angle that rotates by 94 degrees on each new attempt, so that the attempts are spread out and no two are symmetric. In stage 2 (L7), each step multiplies the weight of $\alpha_i$ by $1/(\alpha_i - s)$, so the root closest to $s$ wins at a linear rate. The test at L8 waits until two successive estimates agree to within half their size, then switches to the variable shift, which updates $s$ at every step. If stage 3 does not reach the rounding level within 10 steps, or $|p(s)|$ grows by a factor of 10, control returns to stage 2, and after $L \cdot \text{attempt}$ steps a new shift is tried. Line L11 deflates. The reference code reuses $H$ from the previous attempt and counts every evaluation of $p$ or $H$.

## Example

Take $p(z) = (z - 1)(z - 2)(z - 3) = z^3 - 6z^2 + 11z - 6$. The lower bound is $\beta \approx 0.435$, and stage 1 runs 5 steps with shift 0. After a few fixed-shift steps on the circle of radius $0.435$, the estimates settle near 1, and stage 3 starts from $t = 1.00357 - 0.00122i$. Its shifts have errors
$$3.8 \times 10^{-3},\quad 9.0 \times 10^{-8},\quad 3 \times 10^{-16},$$
and the last one meets the stopping rule. Deflation leaves $z^2 - 5z + 6$, for which stage 3 gives errors
$$3.9 \times 10^{-2},\quad 8.9 \times 10^{-5},\quad 2.6 \times 10^{-13},\quad 1.8 \times 10^{-15}.$$
The last root, 3, comes from the remaining linear factor. The whole run takes 21 steps and 49 evaluations of $p$ or $H$. The ratios $\log e_{k+1}/\log e_k$ in such runs are about 2.3 to 2.5 in the observed steps, approaching the order $1 + \varphi$ only as the error shrinks. On 500 random polynomials of degree 2 to 10 with roots at least 0.1 apart in the square $[-2, 2]^2$, all runs succeed. The worst root error is $7 \times 10^{-12}$, the worst backward error $|p(z)|/\sum|a_k||z|^{n-k}$ for the original polynomial is $2 \times 10^{-14}$, and the mean is 85 steps per polynomial. For the Wilkinson polynomial with roots $1, \dots, 20$, the roots come back with errors up to $4 \times 10^{-3}$: this is the conditioning of that polynomial, not a failure of the method (see [Wilkinson's polynomial](/wilkinson-polynomial/)).

## Correctness

Assume first that $p$ has distinct roots $\alpha_1, \dots, \alpha_r$ with multiplicities $m_1, \dots, m_r$, and write $P_i(z) = p(z)/(z - \alpha_i)$. Then $p' = \sum m_i P_i$, and a short computation shows that the recurrence maps $\sum c_iP_i$ to $\sum c_i P_i/(\alpha_i - s)$. So after stage 1 and $\lambda$ steps of stage 2, the weight of $\alpha_i$ is $m_i\alpha_i^{-M}(\alpha_i - s)^{-\lambda}$, up to normalisation. If $\alpha_1$ is the unique root closest to $s$, its weight dominates, and the estimate $t_\lambda$ converges to $\alpha_1$ linearly with ratio $\max_{i \ge 2}|\alpha_1 - s|/|\alpha_i - s|$. In stage 3 the error $e$ and the relative weight $\rho$ of the other roots satisfy $e_{\lambda+1} = O(e_\lambda\rho_{\lambda+1})$ and $\rho_{\lambda+1} = O(\rho_\lambda e_\lambda)$. This gives order $(3 + \sqrt5)/2 = 1 + \varphi$. These are local statements in exact arithmetic. Their hypotheses are a unique closest root, and for stage 3 a stage 2 run long enough. Jenkins and Traub prove the convergence of the whole scheme under these conditions. The algorithm does not check them, but it changes the shift when progress stalls. Termination is unconditional, because the steps are capped. The derivations are in [the correctness proof](proofs/correctness.md).

## Complexity

Each step costs one synthetic division of $p$ and one of $H$ by $z - s$, plus the update of $H$: $O(n)$ arithmetic for 2 evaluations. Stage 1 is a fixed $M = 5$ steps, stage 2 typically takes a handful of steps, and stage 3 takes 2 to 4. So each root costs $O(n)$ arithmetic with a modest constant in practice, and all $n$ roots cost $O(n^2)$, which is observed but not proved. In the worst case the cap $K$ bounds the work by $O(Kn)$. The memory is a few arrays of length $n + 1$. Compared with the [companion matrix method](/companion-matrix-method/), which costs $O(n^3)$, it is much cheaper for large $n$. But it finds roots sequentially and relies on deflation, so it does not parallelise like [Durand-Kerner](/durand-kerner-method/) or [Aberth-Ehrlich](/aberth-ehrlich-method/).

## Properties

- Global in the following sense: it needs no starting guess, and its convergence from the chosen shifts is proved under the hypothesis that the closest root is unique.
- Derivative free: $p'$ is used only once per root, as the start $H^{(0)}$. After that only values of $p$ and $H$ are needed.
- Roots come out roughly in increasing order of modulus, which is the stable order for forward deflation. The computed roots have small backward error in the observed runs, though each later root carries the error of the earlier deflations.
- Multiple roots do not slow the iteration in exact arithmetic, because the weights simply start at $m_i$. In floating point they are found only to about $u^{1/m}$, as with any method.
- It is equivalent to a shifted inverse power iteration on the companion matrix, with stage 3 a generalized Rayleigh quotient iteration. This is the relation in the title of the 1970 paper.

## Variants and improvements

- **RPOLY.** For real coefficients, the real version iterates with quadratic factors $z^2 + uz + v$ instead of linear ones, so complex conjugate pairs are found in real arithmetic. It is about four times faster than CPOLY on real polynomials.
- **CPOLY details.** The production code scales the coefficients by a power of the radix to avoid overflow, uses a sharper rounding error bound, and treats clusters of roots by taking a small extra step when $|p(s)|$ stalls. The reference code omits these.
- **Polishing.** Each root found after deflation can be refined by a few [Newton](/newton-raphson-method/) steps on the original polynomial, which removes the accumulated deflation error for simple roots.
- **Rayleigh iteration view.** Seen as inverse iteration on the companion matrix, stage 2 is [inverse iteration](/inverse-iteration/) with a fixed shift and stage 3 is [Rayleigh quotient iteration](/rayleigh-quotient-iteration/) with a rank one change.

## When to use it

Use it as a black box for all roots of a single polynomial of moderate degree, when the coefficients are known in double precision and $O(n^2)$ cost matters. For real polynomials, the real variant is the classic choice. When you need all roots at once with good parallelism, or certified results, or very high degree, prefer [Aberth-Ehrlich](/aberth-ehrlich-method/) iterations (as in MPSolve) or eigenvalue methods with structured QR. When the roots are badly conditioned, no method in double precision will do better than the conditioning allows.

## Pitfalls

- L1: zero roots are stripped only when the trailing coefficients are exactly 0. A tiny but nonzero $a_n$ is treated as a genuine small root.
- L4: the bound $\beta$ is a lower bound on all root moduli. If the shift circle has two roots at the same distance from $s$, stage 2 does not converge. The next attempt at L6 rotates $s$ by 94 degrees, which breaks such ties except in contrived cases.
- L7: if $p(s) = 0$ exactly, the step cannot divide by $p(s)$. The reference code accepts $s$ as a root, and sets $H$ to the exact limit $p(z)/(z - s)$.
- L8: the weak convergence test can pass before the closest root dominates. Stage 3 then wanders and is abandoned when $|p(s)|$ grows by a factor of 10 or after 10 steps, and stage 2 resumes.
- L8: the stopping rule compares $|p(s)|$ with the rounding error bound of Horner's rule. Asking for more, for example $|p(s)| \le 10^{-20}$, can loop until the cap, because rounding makes $|p(s)|$ stall at that bound.
- L11: deflation by a root with error $\epsilon$ perturbs the remaining coefficients by about $\epsilon$ times their size. Taking small roots first keeps this small, but for ill-conditioned polynomials later roots can be visibly worse. Polish them on the original polynomial if it matters.

## Implementations

## History

Joseph Traub studied the H-polynomial recurrence in 1964 to 1966 as a family of globally convergent iterations for polynomials. Michael Jenkins, his doctoral student at Stanford, turned it into the three-stage algorithm in his 1969 thesis. They published the complex version and its convergence theory in Numerische Mathematik in 1970, and the real version with quadratic iteration in SIAM Journal on Numerical Analysis the same year. The programs CPOLY (CACM Algorithm 419, 1972) and RPOLY (ACM TOMS Algorithm 493, 1975) became the polynomial root finders in IMSL, NAG and many other libraries, and Numerical Recipes calls the method practically a standard among black-box polynomial root finders.

## References
