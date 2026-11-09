---
tag: V5H45Q
kind: algorithm
slug: exact-line-search
name: Exact line search
aliases:
- exact minimization along a direction
- optimal step
- Cauchy step
area: optimization/gradient-methods
level: core
summary: Choose the step α that minimizes f(x + αd). Quadratics have a closed form; otherwise bracket the minimizer and shrink the bracket by golden-section search to a stated tolerance.
solves: [step-size-selection]
model: real-ram
complexity:
  vars: {n: the number of variables, a: the minimizer of φ, h: the first trial step, w: the width of the bracket, τ: the tolerance on the step}
  time: {worst: O(log(2 + a/h) + log(w/τ))}
  space: {extra: O(1)}
  quadratic: {time: O(n^2)}
properties: {deterministic: true, iterative: true, needs_unimodal_line_function: true}
history:
  year: 1847
  people: [Augustin-Louis Cauchy, Haskell B. Curry, Hirotugu Akaike]
  note: Cauchy's 1847 note on the gradient method already chose the step that minimizes the function along the direction. Akaike analysed the zigzag of steepest descent with exact steps in 1959.
prereqs: [gradient-descent, golden-section-search]
see_also: [backtracking-line-search, wolfe-conditions, golden-section-search, step-size-selection, gradient-descent, conjugate-gradient-method, condition-number-of-an-optimization-problem, nonlinear-conjugate-gradient]
sources:
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Section 3.1, Step length, and Section 3.3, Rate of convergence (steepest descent with exact line searches on a convex quadratic, Theorem 3.3)
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 9.2, Descent methods (exact line search), and Section 9.3.1, Convergence analysis (gradient method with exact line search)
  - paper: doi:10.1007/BF01831719
    title: Hirotugu Akaike, On a successive transformation of probability distribution and its application to the analysis of the optimum gradient method, Annals of the Institute of Statistical Mathematics 11, 1959
    locator: pages 1 to 16
  - paper: doi:10.1090/S0002-9939-1953-0055639-3
    title: Jack Kiefer, Sequential minimax search for a maximum, Proceedings of the American Mathematical Society 4(3), 1953
    locator: pages 502 to 506 (Fibonacci and golden-section search for a unimodal function)
  - paper: doi:10.4171/dms/6/27
    title: Claude Lemaréchal, Cauchy and the gradient method, Documenta Mathematica, Extra Volume Optimization Stories, 2012
    locator: pages 251 to 254 (Cauchy's 1847 note and the choice of the step)
  - paper: doi:10.1090/qam/10667
    title: Haskell B. Curry, The method of steepest descent for non-linear minimization problems, Quarterly of Applied Mathematics 2(3), 1944
    locator: pages 258 to 261
---

Exact line search chooses the step $\alpha$ along a descent direction $d$ at a point $x$ that minimizes $\varphi(\alpha) = f(x + \alpha d)$ over $\alpha \ge 0$. For a quadratic $f(x) = \frac12 x^\top Ax - b^\top x$ with $A$ positive definite, the answer has the closed form $\alpha = -\nabla f(x)^\top d/(d^\top Ad)$. For other functions it is found to a tolerance $\tau$: first bracket the minimizer by doubling the step, then shrink the bracket by [golden-section search](/golden-section-search/). Used with [gradient descent](/gradient-descent/), it gives the classical method of steepest descent, whose error on a quadratic shrinks by at most the factor $((\kappa - 1)/(\kappa + 1))^2$ per step, and this bound is attained.

## In plain words

You stand on a hillside and have chosen a direction to walk. Exact line search walks along that straight line to the lowest point on it and stops there. Then a new direction is chosen.

To find the lowest point on the line, first walk further and further, doubling the distance, until the ground starts to rise again: the lowest point is now between two marks. Then keep cutting this stretch at two inner points and throwing away the part that cannot hold the lowest point, until the stretch is very short.

For a bowl-shaped quadratic hill, the lowest point on the line can be computed directly by a formula.

## The problem

The input is a function $\varphi : [0, \infty) \to \mathbb{R}$, usually $\varphi(\alpha) = f(x + \alpha d)$ with $\nabla f(x)^\top d < 0$, a first trial step $h > 0$ and a tolerance $\tau > 0$. The function $\varphi$ must be *strictly unimodal*: there is $a^* \ge 0$ such that $\varphi$ is strictly decreasing on $[0, a^*]$ and strictly increasing on $[a^*, \infty)$ ([unimodal function](/unimodal-function/)). This holds for every strictly convex $\varphi$ that has a minimizer on $[0, \infty)$, so for every strictly convex coercive $f$. The output is a step $\hat{\alpha}$ and a bracket $[lo, hi]$ with $a^* \in [lo, hi]$, $hi - lo \le \tau$ and $|\hat{\alpha} - a^*| \le \tau/2$. All arithmetic is in floating point.

## The algorithm

```pseudo id=main
EXACT-LINE-SEARCH(φ, h, τ)
L1  if φ(h) ≥ φ(0) then (lo, hi) ← (0, h)          ▷ the minimizer is in [0, h]
L2  else
L3      (lo, mid, hi) ← (0, h, 2h)
L4      while φ(hi) < φ(mid) do                        ▷ still going down: double
L5          (lo, mid, hi) ← (mid, hi, 2·hi)
L6  r ← (√5 − 1)/2                                    ▷ r² = 1 − r
L7  while hi − lo > τ do
L8      u ← hi − r(hi − lo);  v ← lo + r(hi − lo)       ▷ lo < u < v < hi
L9      if φ(u) < φ(v) then hi ← v else lo ← u
L10 return (lo + hi)/2
```

Lines L1 to L5 are the bracketing phase. If the first trial step does not go down, the minimizer is before it. Otherwise the steps $h, 2h, 4h, \ldots$ are tried while $\varphi$ keeps decreasing; when it stops, the last three points satisfy $\varphi(mid) < \varphi(lo)$ and $\varphi(mid) \le \varphi(hi)$, so the minimizer is between $lo$ and $hi$. Lines L6 to L9 are golden-section search. Each pass keeps the part of the bracket that must contain the minimizer, which is a fraction $r \approx 0.618$ of it.

For a quadratic $f(x) = \frac12x^\top Ax - b^\top x$ with $g = \nabla f(x) = Ax - b$, the function $\varphi(\alpha) = f(x) + \alpha g^\top d + \frac{\alpha^2}{2}d^\top Ad$ is a parabola, and the whole search is replaced by

$$\alpha^* = -\frac{g^\top d}{d^\top Ad}.$$

With $d = -g$ this is $\alpha^* = g^\top g/(g^\top Ag)$, the Cauchy step.

## Example

Take $f(x) = \frac12(x_1^2 + 10x_2^2)$, so $A = \operatorname{diag}(1, 10)$, $\mu = 1$, $L_f = 10$, $\kappa = 10$, and start at $x_0 = (10, 1)$ with $d = -\nabla f(x_0) = (-10, -10)$. Then $\varphi(\alpha) = 55 - 200\alpha + 550\alpha^2$ and the exact step is $\alpha^* = 200/1100 = 2/11$.

**The search.** With $h = 1$, $\varphi(1) = 405 \ge 55$, so the bracket is $[0, 1]$. Golden-section search with $\tau = 10^{-8}$ needs $39$ passes, since $0.618^{38} > 10^{-8} \ge 0.618^{39}$, and returns $2/11$ to within $5 \cdot 10^{-9}$.

**Steepest descent with exact steps.** The new point is $x_1 = (10, 1) - \frac{2}{11}(10, 10) = \frac{9}{11}(10, -1)$. By the symmetry of the problem, the step is $2/11$ again at every iteration, and

$$x_k = \left(\tfrac{9}{11}\right)^k\left(10, (-1)^k\right), \qquad f(x_k) = \left(\tfrac{9}{11}\right)^{2k}f(x_0).$$

The iterates zigzag across the narrow valley, and the error shrinks by exactly $(9/11)^2 = ((\kappa - 1)/(\kappa + 1))^2$ per step, the worst case allowed by the Kantorovich bound below. The gradient norm falls below $10^{-6}$ after $83$ steps: the same as the fixed step $2/(\mu + L_f)$ and fewer than the $153$ steps of the fixed step $1/L_f$. Successive directions are orthogonal, $\nabla f(x_{k+1})^\top\nabla f(x_k) = 0$.

## Correctness

The full proofs are in the correctness proof of this page. In summary:

1. **Bracketing.** If $\varphi$ is strictly unimodal with minimizer $a^*$, the body of the loop of L4 runs at most $\max(0, \lceil\log_2(a^*/h)\rceil)$ times, and after the loop the minimizer lies in $[lo, hi]$. *Reason:* $\varphi(mid) < \varphi(lo)$ rules out $a^* \le lo$, and $\varphi(hi) \ge \varphi(mid)$ rules out $a^* \ge hi$. Once $mid \ge a^*$, $\varphi$ is increasing beyond $mid$, so the loop stops.
2. **Golden-section invariant.** Each pass of L9 keeps $a^* \in [lo, hi]$: if $\varphi(u) < \varphi(v)$ then $a^* < v$, else $a^* > u$. The width is multiplied by $r$, so after $\lceil\log_{1/r}(w/\tau)\rceil$ passes it is at most $\tau$, and the midpoint is within $\tau/2$ of $a^*$.
3. **Quadratic closed form.** $\varphi'(\alpha) = g^\top d + \alpha d^\top Ad$ vanishes only at $\alpha^* = -g^\top d/(d^\top Ad)$, which is positive since $g^\top d < 0$.
4. **Orthogonality.** At an exact step, $\varphi'(\alpha^*) = \nabla f(x + \alpha^*d)^\top d = 0$: the new gradient is orthogonal to the old direction.

For steepest descent $x_{k+1} = x_k - \alpha_k\nabla f(x_k)$ with exact steps:

5. **Quadratics (Kantorovich).** If $f(x) = \frac12(x - x^*)^\top A(x - x^*) + f^*$ with the eigenvalues of $A$ in $[\mu, L]$, then $f(x_{k+1}) - f^* \le \left(\frac{\kappa - 1}{\kappa + 1}\right)^2(f(x_k) - f^*)$ with $\kappa = L/\mu$, and the example attains it.
6. **Strongly convex functions.** If $f$ is $\mu$-strongly convex and $L_f$-smooth, then $f(x_{k+1}) - f^* \le (1 - \mu/L_f)(f(x_k) - f^*)$, because the exact step does at least as well as the step $1/L_f$.
7. **Convex functions.** If $f$ is convex and $L_f$-smooth, and the level set $\{x : f(x) \le f(x_0)\}$ lies within distance $D_0$ of a minimizer $x^*$, then $f(x_k) - f^* \le 2L_fD_0^2/k$.

## Complexity

**Evaluations.** The bracketing phase uses $2$ values of $\varphi$ if $\varphi(h) \ge \varphi(0)$, and otherwise $O(\log(2 + a^*/h))$ values. The golden-section phase uses $\lceil\log_{1/r}(w/\tau)\rceil \approx 2.08\log_2(w/\tau)$ passes, where $w = hi - lo$ after bracketing. The code evaluates $\varphi$ twice per pass; because $r^2 = 1 - r$, one of the two points of the next pass is a point of the current pass, so a careful version needs one new value per pass. Each value of $\varphi$ is one value of $f$ plus $O(n)$ work to form $x + \alpha d$. The extra space is $O(1)$ beyond the vectors $x$ and $d$.

**Quadratics.** The closed form costs one product $Ad$, so $O(n^2)$ for a dense $A$ or one Hessian-vector product, and $O(n)$ more work.

**Steepest descent.** On a quadratic, the Kantorovich bound gives at most $\left\lceil\ln(\varepsilon_0/\varepsilon)/\ln\left(\frac{\kappa + 1}{\kappa - 1}\right)^2\right\rceil \approx \frac{\kappa}{4}\ln(\varepsilon_0/\varepsilon)$ steps for the error to drop from $\varepsilon_0$ to $\varepsilon$. This is the same factor as the fixed step $2/(\mu + L_f)$; exact steps do not remove the dependence on $\kappa$.

| claim | value |
|---|---|
| values of $\varphi$, bracketing | $O(\log(2 + a^*/h))$ |
| values of $\varphi$, golden section | $O(\log(w/\tau))$ |
| quadratic closed form | one product with $A$ |
| steepest descent on quadratics, factor per step | $((\kappa - 1)/(\kappa + 1))^2$ |

## Properties

- **Best decrease along the line.** No step along $d$ gives a lower value, so on every iteration exact line search does at least as well as any other step rule with the same direction. This does not make the whole method faster: on quadratics steepest descent with exact steps has the same worst-case factor as the fixed step $2/(\mu + L_f)$.
- **Orthogonal steps.** Successive steepest descent directions are orthogonal, which produces the zigzag in narrow valleys.
- **Strong Wolfe for free.** Since $\varphi'(\alpha^*) = 0$, the exact step meets the [Wolfe](/wolfe-conditions/) curvature condition for every $c_2$; for a convex parabola it also meets the [Armijo condition](/armijo-condition/) for every $c \le \frac12$.
- **Finite termination with conjugate directions.** On a quadratic in $\mathbb{R}^n$, exact steps along conjugate directions reach the minimizer in at most $n$ steps. This is the basis of the [conjugate gradient method](/conjugate-gradient-method/) and of the quadratic termination of [BFGS](/bfgs/).

## Variants and improvements

- **Reuse in golden section.** Keep the value at the inner point that survives, so each pass needs one new value of $\varphi$ in place of two.
- **Fibonacci search.** With a fixed number of evaluations, the Fibonacci ratios give the smallest final bracket (Kiefer, 1953); golden section is its limit.
- **Brent's method and safeguarded interpolation.** Fit a parabola through three points and use its minimizer when it lies safely inside the bracket, with a golden-section step as a fallback. This converges superlinearly on smooth $\varphi$.
- **Derivative-based search.** When $\varphi'$ is cheap, use bisection or the secant method on $\varphi'(\alpha) = 0$.
- **Inexact searches.** In practice, the [Wolfe conditions](/wolfe-conditions/) or [backtracking](/backtracking-line-search/) replace exact minimization: they cost a few values of $f$ and keep the global convergence theory.

## When to use it

Use the closed form whenever $f$ is quadratic, or when $\varphi$ is quadratic for another reason (for example least squares along a line). This is how the [conjugate gradient method](/conjugate-gradient-method/) chooses its steps. Use an accurate line search when one evaluation of $\varphi$ is much cheaper than a new direction, as in some coordinate and subspace methods. For general smooth problems with gradient or quasi-Newton directions, an inexact Wolfe or Armijo search is cheaper and works as well.

## Pitfalls

- **A function that is not unimodal on the line.** If $\varphi$ has several local minima, the search returns one of them, not necessarily the global minimizer along the line, and the bracketing phase may jump over a valley.
- **A function that is unbounded below on the line.** Then the bracketing loop never stops. The code raises an error after $200$ doublings.
- **Rounding limits the accuracy.** Near the minimizer, $\varphi(\alpha) - \varphi(a^*) \approx \frac12\varphi''(a^*)(\alpha - a^*)^2$, so two values of $\varphi$ differ by less than the rounding error of $\varphi$ when $|\alpha - a^*|$ is about $\sqrt{u}$ times the scale of the problem, with $u = 2^{-53}$. A tolerance below about $10^{-8}$ relative to $a^*$ is then useless. A small loss of accuracy in $f$ itself, such as $\log\cosh z$ computed as $\log(\cosh z)$ for small $z$, makes this worse.
- **Exact steps do not cure ill conditioning.** On the example the iterates zigzag with the factor $(9/11)^2$ per step. A better direction ([conjugate gradient](/nonlinear-conjugate-gradient/), [quasi-Newton](/quasi-newton-method/), [momentum](/momentum-method/)) is the remedy, not a better step.

## Implementations

The Python module has the bracketing and golden-section search for a general $\varphi$, the closed form for quadratics, and steepest descent with each of them.

## History

In his 1847 note, Cauchy proposed to move along the negative gradient and to choose the step so that the function becomes a minimum along that line (Lemaréchal, 2012). Curry studied the method for nonlinear functions in 1944 and also took the first local minimum along the line. The bound $((\kappa - 1)/(\kappa + 1))^2$ for quadratic functions follows from the inequality of Kantorovich, and it is the standard textbook rate of the method (Nocedal and Wright, Section 3.3). Akaike showed in 1959 that on a quadratic the iterates of steepest descent with exact steps end up alternating between two directions in the plane spanned by the eigenvectors of the smallest and the largest eigenvalues, which explains the zigzag. Kiefer introduced Fibonacci search and its limit, golden-section search, in 1953.

## References
