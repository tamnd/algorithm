---
tag: J2HSDJ
kind: algorithm
slug: bairstow-method
name: Bairstow's method
aliases:
- Bairstow's quadratic factor method
- Lin-Bairstow method
- Bairstow-Hitchcock method
area: numerical/root-finding
level: advanced
summary: Newton's method on the remainder of p modulo a trial quadratic x^2 - ux - v. It finds real quadratic factors, so complex conjugate roots come out in real arithmetic, quadratically near a factor.
solves: [polynomial-root-finding]
model: real-ram
complexity:
  vars: {n: "the degree of the polynomial", K: "the cap on the steps for one factor", R: "the cap on the restarts for one factor"}
  time: {worst: "O(n^2 K R)", average: "O(n^2)"}
  space: {extra: Θ(n)}
  evaluations: {worst: "n K R", step: "1"}
properties: {deterministic: true, recursive: false, bracketing: false, derivative_free: true, real_arithmetic: true}
prereqs: [newton-method-for-systems, horner-rule, polynomial-deflation]
see_also: [polynomial-root-finding, durand-kerner-method, aberth-ehrlich-method, jenkins-traub-algorithm, laguerre-method, muller-method, wilkinson-polynomial, cauchy-root-bound]
sources:
  - paper: "L. Bairstow, Investigations relating to the stability of the aeroplane, Reports and Memoranda No. 154, Advisory Committee for Aeronautics, London, 1920"
    locator: the appendix on solving the stability quartic by successive quadratic factors
  - paper: "Shih-Nge Lin, A method of successive approximations of evaluating the real and complex roots of cubic and higher-order equations, Journal of Mathematics and Physics 20, 231-242, 1941"
    locator: the quadratic factor iteration without derivatives (Lin's method), whose start is used here
  - book: isbn:9780521880688
    title: William H. Press, Saul A. Teukolsky, William T. Vetterling and Brian P. Flannery, Numerical Recipes, third edition, Cambridge University Press, 2007
    locator: Section 9.5, Roots of Polynomials (Bairstow's method and the routine qroot)
  - book: "Anthony Ralston and Philip Rabinowitz, A First Course in Numerical Analysis, second edition, McGraw-Hill, 1978 (Dover reprint, 2001)"
    locator: the chapter on roots of polynomial equations (the Bairstow and Lin methods and the derivation of the Jacobian by a second synthetic division)
---

Bairstow's method finds the roots of a real polynomial $p$ by finding its real quadratic factors $x^2 - ux - v$. Dividing $p$ by a trial quadratic leaves a linear remainder whose two coefficients depend on $(u, v)$; the method applies [Newton's method for systems](/newton-method-for-systems/) to drive both to zero. A second synthetic division supplies the Jacobian, so a step costs about $4n$ multiplications and no complex arithmetic. Each factor gives two roots, real or complex conjugate, and the quotient is [deflated](/polynomial-deflation/) and processed in the same way. Near a factor that shares no root with its cofactor the convergence is quadratic. Far from one, the iteration can wander or meet a singular Jacobian, so practical codes restart from new trial factors.

## In plain words

Complex roots of a real polynomial come in pairs, and each pair is the root set of a real quadratic. So instead of hunting one complex root, hunt one real quadratic that divides the polynomial. Guess the quadratic, divide, and look at the remainder. If it is zero, you are done; if not, adjust the two numbers that describe the quadratic with a Newton step, which needs the derivatives of the remainder, and those come from dividing once more. When a factor is found, read off its two roots, divide it out and repeat on what is left.

## The problem

Notation on the root-finding pages: $f$ is the function, $x^*$ a root, $x_k$ the iterates and $e_k = x_k - x^*$ the error. A method has [order](/order-of-convergence/) $q$ and rate constant $C$ when $|e_{k+1}| \approx C |e_k|^q$, with $0 < C < 1$ when $q = 1$. A root has [multiplicity](/multiplicity-of-roots/) $m$ when $f(x^*) = \cdots = f^{(m-1)}(x^*) = 0 \ne f^{(m)}(x^*)$. The cost is the number of evaluations of $f$ (and of $f'$ where a method uses it). A method of order $q$ that needs $w$ evaluations in each step has efficiency index $q^{1/w}$.

Here $f = p(x) = a_0x^n + a_1x^{n-1} + \cdots + a_n$ with real $a_i$, $a_0 \ne 0$. The unknown is the pair $(u, v)$, and the iterates and errors are those of the pair: $e_k = |u_k - u^*| + |v_k - v^*|$ for a factor $x^2 - u^*x - v^*$ of $p$. One evaluation is one double synthetic division. For a factor search the stopping rule is: the remainder is exactly zero, or it is below its rounding floor (defined at L3), or the step satisfies $|\Delta u| + |\Delta v| \le \delta(1 + |u| + |v|)$, or $K$ steps have passed. Output: all $n$ roots, or the status "failed" after $R$ restarts on one factor.

## The algorithm

Synthetic division by $x^2 - ux - v$ is the recurrence $b_k = a_k + ub_{k-1} + vb_{k-2}$ for $k = 0, \dots, n$, with $b_{-1} = b_{-2} = 0$. It gives
$$p(x) = (x^2 - ux - v)(b_0x^{n-2} + \cdots + b_{n-2}) + b_{n-1}(x - u) + b_n,$$
so $x^2 - ux - v$ divides $p$ exactly when $b_{n-1} = b_n = 0$. The same recurrence applied to the $b$'s gives $c_k = b_k + uc_{k-1} + vc_{k-2}$, and $\partial b_k/\partial u = c_{k-1}$, $\partial b_k/\partial v = c_{k-2}$.

```pseudo id=main
FACTOR(a, u, v, delta, K):            -- needs n >= 3
L1   for k = 1, 2, ..., K:
L2       b_j <- a_j + u b_{j-1} + v b_{j-2}  for j = 0..n
L3       if b_{n-1} = b_n = 0 then return "exact";  if both lie below the rounding floor then return "converged"
L4       c_j <- b_j + u c_{j-1} + v c_{j-2}  for j = 0..n-1
L5       J <- c_{n-2}^2 - c_{n-1} c_{n-3};  if J = 0 then return "singular"
L6       du <- (b_n c_{n-3} - b_{n-1} c_{n-2}) / J;   dv <- (b_{n-1} c_{n-1} - b_n c_{n-2}) / J
L7       u <- u + du;  v <- v + dv
L8       if |du| + |dv| <= delta (1 + |u| + |v|) then return "converged"
L9   return "max-iter"
ROOTS(a):
L10  while deg a >= 3:  start from Lin's (u, v) = (-a_{n-1}/a_{n-2}, -a_n/a_{n-2}); run FACTOR, and on failure restart from a pseudo-random quadratic, at most R times
L11      append the two roots of x^2 - u x - v
L12      a <- (b_0, ..., b_{n-2})
L13  append the roots of the remaining linear or quadratic polynomial
```

Line L2 is the division; L4 differentiates it; L5 and L6 solve the $2 \times 2$ Newton system $c_{n-2}\Delta u + c_{n-3}\Delta v = -b_{n-1}$, $c_{n-1}\Delta u + c_{n-2}\Delta v = -b_n$ by Cramer's rule. The rounding floor at L3 is $\gamma\mu_k$ with $\mu_k = |a_k| + |u|\mu_{k-1} + |v|\mu_{k-2}$ and $\gamma = 4(n + 1)u_{\text{mach}}$, a running bound of the kind used for Horner's rule: below it the remainder carries no information, and further steps only shuffle rounding errors. Line L11 solves the quadratic in the stable form, $x_1 = (u + \operatorname{sign}(u)\sqrt{u^2 + 4v})/2$ and $x_2 = -v/x_1$ when the roots are real, and $u/2 \pm i\sqrt{-(u^2 + 4v)}/2$ when they are not.

## Example

Take $p(x) = x^4 + 3x^2 + 6x + 10 = (x^2 + 2x + 2)(x^2 - 2x + 5)$, with roots $-1 \pm i$ and $1 \pm 2i$. Lin's start is $u_0 = -6/3 = -2$, $v_0 = -10/3$. The factor reached is $x^2 + 2x + 2$, that is $(u^*, v^*) = (-2, -2)$:

| $k$ | $u_k$ | $v_k$ | $b_3$ | $b_4$ | $e_k$ |
|---|---|---|---|---|---|
| 0 | $-2$ | $-3.333333$ | $5.33$ | $-12.9$ | $1.33$ |
| 1 | $-1.908178$ | $-1.808704$ | $0.230$ | $0.820$ | $2.83 \times 10^{-1}$ |
| 2 | $-2.002431$ | $-2.002920$ | $-1.51 \times 10^{-2}$ | $1.96 \times 10^{-3}$ | $5.35 \times 10^{-3}$ |
| 3 | $-2.0000006775$ | $-1.9999965494$ | $-2.13 \times 10^{-5}$ | $4.74 \times 10^{-5}$ | $4.13 \times 10^{-6}$ |
| 4 | $-1.999999999998$ | $-1.999999999993$ | $-7.43 \times 10^{-12}$ | $4.96 \times 10^{-11}$ | $8.59 \times 10^{-12}$ |
| 5 | $-2$ to 16 digits | $-2$ | $3.1 \times 10^{-15}$ | $-3.6 \times 10^{-15}$ | $2.2 \times 10^{-16}$ |

The errors square from step to step, as Newton's method promises. At step 5 the remainder is under its rounding floor, so FACTOR stops with "converged" after 6 divisions. The quotient is $x^2 - 2x + 5$ (to rounding), L11 gives $-1 \pm i$, and L13 gives $1 \pm 2i$, all to within one unit in the last place.

## Correctness

The division identity holds exactly, so $(u^*, v^*)$ is a factor if and only if $F(u^*, v^*) = (b_{n-1}, b_n) = 0$, and the $c$ recurrence computes the Jacobian of $F$ exactly. The Jacobian at a factor $D^* = x^2 - u^*x - v^*$ with cofactor $q^*$ is nonsingular if and only if $\gcd(D^*, q^*) = 1$, that is, the roots of $D^*$ are not roots of $q^*$; a double real root that is a root of $p$ of multiplicity exactly 2 is allowed. Under that condition Newton's theorem for systems gives local quadratic convergence of $(u_k, v_k)$, since $F$ is a polynomial map. Each FACTOR run stops within $K$ steps, ROOTS removes two degrees per factor, and the restarts are capped, so ROOTS ends after at most $(R + 1)Kn/2$ steps. Nothing is claimed about convergence from a given start: the global behaviour is not guaranteed and is observed only. The proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

One step is two synthetic divisions, about $4n$ multiplications and $4n$ additions, plus $O(1)$ for the $2 \times 2$ solve. Once in the quadratic region a factor takes $O(\log\log(1/\delta))$ steps, so with a bounded number of steps per factor the whole run costs $O(n^2)$ operations; with the caps the worst case is $O(n^2KR)$. On 600 random real polynomials of degree 3 to 8 with roots at least 0.3 apart in the box $[-3, 3] \times [-3, 3]$, ROOTS found every root with error below $3 \times 10^{-12}$, used about 35 divisions on average, and restarted 39 times in total.

## Properties

- Works in real arithmetic only, yet finds complex roots in conjugate pairs.
- Quadratic convergence near a factor coprime to its cofactor (local, proved), including a factor $(x - r)^2$ for a root of multiplicity exactly 2; Newton's method on $p$ itself is only linear there.
- Not globally convergent: the iterates can cycle or diverge, and the Jacobian can vanish (on $x^4 + 1$ from $u = v = 0$ it does at once).
- Deflation makes later factors inherit the rounding errors of earlier ones.

## Variants and improvements

- Lin's method (1941) drops the second division and uses the remainder alone to update $(u, v)$; it is linear at best. Lin's ratios are the start used here.
- Hitchcock (1944) made the same quadratic factor Newton iteration popular in the form used today, so the method is sometimes called the Bairstow-Hitchcock method.
- [Jenkins and Traub's](/jenkins-traub-algorithm/) real algorithm also extracts real quadratic factors, with a global convergence theory, and is the standard choice in libraries.
- Polishing each root by [Newton's method](/newton-raphson-method/) on the undeflated $p$ removes most of the deflation error.
- Simultaneous methods such as [Durand-Kerner](/durand-kerner-method/) and [Aberth-Ehrlich](/aberth-ehrlich-method/) avoid deflation but need complex arithmetic.

## When to use it

Use it for real polynomials of modest degree when only real arithmetic is available or wanted, and when good trial factors are at hand, as in tracking the roots of a characteristic polynomial while a parameter changes slowly. For general use, the [companion matrix method](/companion-matrix-method/), Jenkins-Traub or Aberth's method are more robust.

## Pitfalls

- L3: a step test with a relative tolerance near machine precision can loop until $K$ when rounding noise in $(u, v)$ is larger than the tolerance. With $\delta = 10^{-14}$ the noise on the factor $(x - 1)(x - 10)$ of the degree-10 [Wilkinson polynomial](/wilkinson-polynomial/) stays near $3 \times 10^{-11}$; the rounding floor test stops the run there.
- L5: a singular Jacobian is not a failure of the polynomial but of the start; restart rather than divide by zero.
- L10: a fixed start for every factor can fail on symmetric polynomials; without the capped restarts the method has no guarantee of stopping with all roots.
- L12: deflation spreads errors. On the degree-10 Wilkinson polynomial the computed roots have errors up to about $7 \times 10^{-8}$; polish the roots on the original polynomial.
- L11: computing both roots of the quadratic with the plain formula loses the small root to cancellation.

## Implementations

## History

Leonard Bairstow described the method in 1920 in an aeronautical report, where it served to factor the quartic stability polynomial of an aircraft into quadratics. Shih-Nge Lin published a simpler derivative-free factor iteration in 1941, and F. L. Hitchcock's 1944 paper, building on Lin's, gave the Newton form wide circulation; the method appears in textbooks as Bairstow's, Lin-Bairstow or Bairstow-Hitchcock. It was a standard polynomial solver of early computers before eigenvalue methods and the Jenkins-Traub algorithm took its place.

## References
