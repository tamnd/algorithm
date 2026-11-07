---
tag: EX63Y3
kind: theorem
slug: kantorovich-theorem
name: Kantorovich theorem
aliases:
- Newton-Kantorovich theorem
- Kantorovich convergence theorem for Newton's method
area: numerical/root-finding
level: research
summary: If the first Newton step has length η, F' is L-Lipschitz relative to F'(x0) and Lη ≤ 1/2, Newton's method converges to a root near x0 that is unique in a computable ball.
prereqs: [newton-method-for-systems, banach-fixed-point-theorem, quadratic-convergence]
see_also: [newton-raphson-method, newton-method-for-systems, banach-fixed-point-theorem, quadratic-convergence, order-of-convergence, systems-of-nonlinear-equations, fixed-point-iteration, broyden-method]
sources:
  - paper: "L. V. Kantorovich, Functional analysis and applied mathematics, Uspekhi Matematicheskikh Nauk 3 (1948), no. 6, 89-185 (in Russian)"
    locator: the section on Newton's method in normed spaces, with the condition h <= 1/2
  - book: "L. V. Kantorovich and G. P. Akilov, Functional Analysis, second edition, Pergamon Press, 1982"
    locator: Chapter XVIII, Newton's method (the majorant theorem and its corollaries)
  - book: isbn:9780898714616
    title: J. M. Ortega and W. C. Rheinboldt, Iterative Solution of Nonlinear Equations in Several Variables, SIAM Classics in Applied Mathematics 30, 2000
    locator: Section 12.6, Newton-Kantorovich theorems (Theorem 12.6.2) and Section 12.4 on majorant sequences
  - book: isbn:9780898713640
    title: John E. Dennis Jr. and Robert B. Schnabel, Numerical Methods for Unconstrained Optimization and Nonlinear Equations, SIAM Classics in Applied Mathematics 16, 1996
    locator: Section 5.3, the Kantorovich and contractive mapping theorems (Theorem 5.3.1)
  - paper: doi:10.1137/0711002
    title: "W. B. Gragg and R. A. Tapia, Optimal error bounds for the Newton-Kantorovich theorem, SIAM Journal on Numerical Analysis 11 (1974) 10-13"
    locator: the closed form of t* - t_k and its optimality
  - book: isbn:9783540210993
    title: Peter Deuflhard, Newton Methods for Nonlinear Problems, Springer Series in Computational Mathematics 35, 2004
    locator: Section 2.1, Local Newton methods for nonlinear systems (the affine covariant Newton-Kantorovich theorem)
---

The Kantorovich theorem gives conditions that can be checked at the starting point alone and that guarantee that [Newton's method](/newton-method-for-systems/) converges, that the limit is a root, and that no other root lies in a computable ball. Unlike the local convergence theorem, it does not assume that a root exists. It needs three numbers: the length $\eta$ of the first Newton step, a Lipschitz constant $L$ of the derivative measured relative to $F'(x_0)$, and the test $h = L\eta \le \frac12$. Its proof compares Newton's method for $F$ with Newton's method for the scalar quadratic $\varphi(t) = \frac L2 t^2 - t + \eta$, which turns out to be the worst case, so every constant in the theorem is sharp.

## Statement

Notation on the root-finding pages: $F$ is the map whose root is sought, $x_k$ the Newton iterates $x_{k+1} = x_k - F'(x_k)^{-1}F(x_k)$, $x^*$ a root, $B(x, r)$ and $\bar B(x, r)$ the open and closed balls.

**Theorem (Kantorovich, 1948; affine invariant form).** Let $X$ and $Y$ be Banach spaces, $D \subseteq X$ open and convex, and $F : D \to Y$ Fréchet differentiable. Let $x_0 \in D$ with $F'(x_0)$ invertible, and suppose that

1. $\|F'(x_0)^{-1}F(x_0)\| \le \eta$;
2. $\|F'(x_0)^{-1}\bigl(F'(x) - F'(y)\bigr)\| \le L\|x - y\|$ for all $x, y \in D$;
3. $h = L\eta \le \frac12$;
4. $\bar B(x_0, t^*) \subseteq D$, where $t^* = \bigl(1 - \sqrt{1 - 2h}\bigr)/L$ (and $t^* = \eta$ if $L = 0$).

Let $t^{**} = \bigl(1 + \sqrt{1 - 2h}\bigr)/L$ (and $t^{**} = \infty$ if $L = 0$). Then:

- (a) the Newton iterates are defined for all $k$, lie in $\bar B(x_0, t^*)$ and converge to a root $x^*$ of $F$ in $\bar B(x_0, t^*)$;
- (b) $\|x^* - x_k\| \le t^* - t_k$, where $t_0 = 0$ and $t_{k+1} = t_k - \varphi(t_k)/\varphi'(t_k)$ are the Newton iterates for $\varphi(t) = \frac L2 t^2 - t + \eta$; explicitly, with $\theta = t^*/t^{**}$,
$$t^* - t_k = \frac{(t^{**} - t^*)\,\theta^{2^k}}{1 - \theta^{2^k}} \quad (h < \tfrac12), \qquad t^* - t_k = 2^{-k}\,t^* \quad (h = \tfrac12);$$
- (c) $x^*$ is the only root of $F$ in $D \cap B(x_0, t^{**})$ if $h < \frac12$, and in $D \cap \bar B(x_0, t^*)$ if $h = \frac12$.

The classical form assumes $\|F'(x_0)^{-1}\| \le \beta$ and $\|F'(x) - F'(y)\| \le K\|x - y\|$, and then the theorem applies with $L = \beta K$.

## In plain words

Take one Newton step from your starting point and measure how long it is. Then measure how quickly the slope of the function can change. If the step is short compared with the distance over which the slope changes noticeably, precisely if their product is at most one half, Newton's method is guaranteed to work from that point. You also get a ball where the root must be, a larger ball containing no other root, and an error bound for every step. The worst case is a plain parabola, so none of these numbers can be improved.

## Proof

Assume $\eta > 0$ and $L > 0$; if $\eta = 0$ then $x_0$ is a root and all claims are immediate, and if $L = 0$ then $F$ is affine on $D$, $x_1$ is the unique root and the claims follow directly.

**Step 1: the scalar majorant.** Since $h \le \frac12$, $\varphi(t) = \frac L2 t^2 - t + \eta$ has real roots $t^* \le t^{**}$, with $\varphi > 0$ on $[0, t^*)$ and $\varphi'(t) = Lt - 1 < 0$ for $t < 1/L$; note $t^* \le 1/L$. If $0 \le t_k < t^*$, then $\varphi(t_k) > 0$ and $\varphi'(t_k) < 0$, so $t_{k+1} > t_k$; and by strict convexity, $0 = \varphi(t^*) > \varphi(t_k) + \varphi'(t_k)(t^* - t_k)$, which rearranges to $t_{k+1} < t^*$. So $t_k$ increases strictly and stays below $t^*$; its limit is a root of $\varphi$ in $(0, t^*]$, hence $t^*$. For the closed form, Newton's method on a quadratic with roots $t^* \le t^{**}$ satisfies $\frac{t^* - t_{k+1}}{t^{**} - t_{k+1}} = \bigl(\frac{t^* - t_k}{t^{**} - t_k}\bigr)^2$ when $t^* < t^{**}$, so the ratio equals $\theta^{2^k}$, and solving for $t^* - t_k$ gives (b). When $t^* = t^{**}$ the root is double and $t^* - t_{k+1} = \frac12 (t^* - t_k)$.

**Step 2: induction.** We show for all $k \ge 0$:

- (i) $x_k \in \bar B(x_0, t_k)$, so $\|x_k - x_0\| \le t_k < t^*$;
- (ii) $F'(x_k)$ is invertible with $\|F'(x_k)^{-1}F'(x_0)\| \le 1/(1 - Lt_k) = -1/\varphi'(t_k)$;
- (iii) $\|F'(x_0)^{-1}F(x_k)\| \le \varphi(t_k)$;
- (iv) $\|x_{k+1} - x_k\| \le t_{k+1} - t_k$.

For $k = 0$: (i) and (ii) are trivial, (iii) is hypothesis 1 since $\varphi(0) = \eta$, and (iv) follows from (ii) and (iii) as below. Assume (i) to (iv) up to $k - 1$. Then $\|x_k - x_0\| \le \sum_{j<k}(t_{j+1} - t_j) = t_k$, which is (i), so $x_k \in D$ by hypothesis 4. By hypothesis 2, $\|F'(x_0)^{-1}(F'(x_k) - F'(x_0))\| \le Lt_k < Lt^* \le 1$, and the Banach perturbation lemma gives (ii). For (iii), the Newton equation $F'(x_{k-1})(x_k - x_{k-1}) = -F(x_{k-1})$ gives
$$F(x_k) = \int_0^1 \bigl(F'(x_{k-1} + s(x_k - x_{k-1})) - F'(x_{k-1})\bigr)(x_k - x_{k-1})\,ds,$$
where the segment lies in the convex set $D$, so hypothesis 2 yields $\|F'(x_0)^{-1}F(x_k)\| \le \frac L2\|x_k - x_{k-1}\|^2 \le \frac L2(t_k - t_{k-1})^2$. For the quadratic $\varphi$, Taylor's formula and the scalar Newton equation give exactly $\varphi(t_k) = \frac L2 (t_k - t_{k-1})^2$, which proves (iii). Finally,
$$\|x_{k+1} - x_k\| = \|F'(x_k)^{-1}F'(x_0)\,F'(x_0)^{-1}F(x_k)\| \le \frac{\varphi(t_k)}{-\varphi'(t_k)} = t_{k+1} - t_k,$$
which is (iv).

**Step 3: convergence.** By (iv), $\|x_m - x_k\| \le t_m - t_k$ for $m > k$. Since $t_k$ converges, $(x_k)$ is Cauchy and converges to some $x^*$ with $\|x^* - x_k\| \le t^* - t_k$ and $x^* \in \bar B(x_0, t^*) \subseteq D$. By (iii), $\|F'(x_0)^{-1}F(x_k)\| \le \varphi(t_k) \to \varphi(t^*) = 0$, and $F$ is continuous, so $F(x^*) = 0$. This proves (a) and (b).

**Step 4: uniqueness.** Let $y \in D$ with $F(y) = 0$ and $r_k = \|y - x_k\|$. As in Step 2, since $F(y) = 0$,
$$y - x_{k+1} = F'(x_k)^{-1}\bigl(F(y) - F(x_k) - F'(x_k)(y - x_k)\bigr),$$
so (ii) and hypothesis 2 give $r_{k+1} \le L r_k^2 / \bigl(2(1 - Lt_k)\bigr)$. The quadratic $\varphi$ satisfies the same relation with equality: $t^{**} - t_{k+1} = L(t^{**} - t_k)^2/\bigl(2(1 - Lt_k)\bigr)$, from $\varphi(t^{**}) = 0$ and Taylor's formula. Put $\lambda_k = r_k/(t^{**} - t_k)$, which is defined since $t_k < t^* \le t^{**}$. Dividing, $\lambda_{k+1} \le \lambda_k^2$, so $\lambda_k \le \lambda_0^{2^k}$. If $h < \frac12$ and $y \in B(x_0, t^{**})$, then $\lambda_0 = r_0/t^{**} < 1$, so $\lambda_k \to 0$ and $r_k \to 0$ since $t^{**} - t_k$ is bounded. If $h = \frac12$ and $y \in \bar B(x_0, t^*)$, then $\lambda_0 \le 1$, so $r_k \le t^* - t_k \to 0$. In both cases $x_k \to y$, so $y = x^*$. $\square$

## Consequences

- **Existence from computation.** Evaluating $F(x_0)$, solving one linear system and bounding $L$ proves that a root exists. With interval arithmetic for $\eta$ and $L$ this becomes a computer-assisted existence proof.
- **Local convergence.** Near a simple root $x^*$, $\eta \to 0$ as $x_0 \to x^*$ while $L$ stays bounded, so $h \le \frac12$ holds in a neighbourhood: the theorem implies the standard local [quadratic convergence](/quadratic-convergence/) theorem.
- **Quadratic convergence with explicit constants.** For $h < \frac12$ the bound in (b) decreases like $\theta^{2^k}$, which is quadratic convergence with an explicit constant; for $h = \frac12$ only linear convergence with ratio $\frac12$ is guaranteed, which is what happens at a double root.
- **Stopping rules.** Applied at $x_k$ instead of $x_0$, the theorem gives an a posteriori bound: with $\eta_k = \|x_{k+1} - x_k\|$ and a constant $L_k$ for a ball around $x_k$, if $h_k = L_k\eta_k \le \frac12$ then $\|x^* - x_{k+1}\| \le t_k^* - \eta_k = \frac{L_k}{2}\eta_k^2\,(1 + O(h_k))$, which justifies stopping on the step length.
- **Variants.** The same majorant argument handles the simplified Newton method with $F'(x_0)$ fixed (linear convergence), inexact Newton methods and Newton's method in function spaces for differential equations.

## Tightness

**The constants are attained (computed).** Take $X = Y = \mathbb{R}$, $x_0 = 0$ and $F = \varphi$ itself. Then $F'(0) = -1$, so hypothesis 1 holds with equality, hypothesis 2 holds with the constant $L$, and the Newton iterates are exactly the $t_k$. So the error bound (b) is attained at every step, $t^*$ is the actual distance to the root and $t^{**}$ the distance to the second root, so the uniqueness radius in (c) cannot be enlarged. If $h > \frac12$, $\varphi$ has no real root, so the condition $h \le \frac12$ cannot be weakened in terms of $\eta$ and $L$ alone.

**An instance.** For $F(x) = x^2 - 2$ and $x_0 = 2$: $\eta = |F(2)/F'(2)| = \frac12$ and $L = 2/|F'(2)| = \frac12$, so $h = \frac14$, $t^* = 2 - \sqrt2 = 0.5858$ and $t^{**} = 2 + \sqrt2 = 3.414$. The root $\sqrt2$ lies exactly at distance $t^*$ and the other root $-\sqrt2$ exactly at distance $t^{**}$.

**A typical, non-extremal case (computed in double precision).** For $F(x) = \cos x - x$, $x_0 = 1$ and $L = 1/|F'(1)|$ (since $|F''| \le 1$): $\eta = 0.249636$, $L = 0.543044$, $h = 0.135563$, $t^* = 0.269332$. The true errors and the bounds $t^* - t_k$ are

| $k$ | $\lvert x_k - x^* \rvert$ | $t^* - t_k$ |
|---|---|---|
| 0 | $2.61 \times 10^{-1}$ | $2.69 \times 10^{-1}$ |
| 1 | $1.13 \times 10^{-2}$ | $1.97 \times 10^{-2}$ |
| 2 | $2.78 \times 10^{-5}$ | $1.22 \times 10^{-4}$ |
| 3 | $1.70 \times 10^{-10}$ | $4.72 \times 10^{-9}$ |

The bound is sharp at the start and loses accuracy later because it uses one global $L$ instead of the local value $|F''(x^*)|/|F'(x^*)| = 0.40$.

**The Lipschitz constant must hold on the ball.** If hypothesis 2 holds only near $x_0$ and not on $\bar B(x_0, t^*)$, the iterates may leave the region and the conclusion can fail; hypothesis 4 cannot be dropped.

## History

Newton's method in several variables goes back to Simpson (1740), and convergence proofs assuming a root existed were given by Fine (1916) and Bennett (1916). L. V. Kantorovich proved the theorem in Banach spaces in 1948, using the scalar majorant, and expanded it with G. P. Akilov in their *Functional Analysis*. Ostrowski gave related results for one and several variables. The optimal closed-form error bounds are due to Gragg and Tapia (1974). Deuflhard and Heindl (1979) introduced the affine invariant form stated above, and Smale's alpha theory (1986) gave an analogous test for analytic maps that uses only data at $x_0$, with no Lipschitz constant on a region.

## References
