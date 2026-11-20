---
tag: FA1SF6
kind: theorem
slug: lax-wendroff-theorem
name: Lax-Wendroff theorem
area: scientific-computing/conservation-laws-and-shock-capturing
level: core
summary: "If a conservative, consistent scheme converges boundedly almost everywhere and in L1 as the mesh is refined, the limit is a weak solution. It need not be the entropy solution."
prereqs: [weak-solution-of-conservation-law, finite-volume-method, consistency]
see_also: [lax-wendroff-method, rankine-hugoniot-conditions, lax-entropy-condition, total-variation-diminishing, godunov-method, roe-solver, harten-hyman-entropy-fix, lax-equivalence-theorem]
sources:
  - paper: doi:10.1002/cpa.3160130205
    title: P. D. Lax and B. Wendroff, Systems of conservation laws, Communications on Pure and Applied Mathematics 13(2) (1960) 217-237
    locator: the convergence theorem for schemes in conservation form
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Section 12.9 (conservation form), Section 12.10 (the Lax-Wendroff theorem, p. 239), Section 12.11 (the entropy condition), Section 12.12 (nonlinear stability)
  - paper: doi:10.1090/S0025-5718-1994-1201068-0
    title: T. Y. Hou and P. G. LeFloch, Why nonconservative schemes converge to wrong solutions, error analysis, Mathematics of Computation 62 (1994) 497-530
    locator: the error of nonconservative schemes at shocks
---

The Lax-Wendroff theorem says what a numerical scheme for a [conservation law](/hyperbolic-conservation-law/) converges to, if it converges. Take a scheme in conservation form with a consistent, Lipschitz numerical flux. If its solutions stay bounded and converge almost everywhere and in $L^1_{\text{loc}}$ as the mesh is refined, the limit is a [weak solution](/weak-solution-of-conservation-law/). So a convergent conservative scheme puts its shocks at the speeds of the [Rankine-Hugoniot conditions](/rankine-hugoniot-conditions/). The theorem has two limits that are often forgotten. It does not say that the scheme converges, and it does not say that the limit satisfies the [Lax entropy condition](/lax-entropy-condition/). It is a different result from the [Lax-Wendroff method](/lax-wendroff-method/), a second order scheme with the same authors: the theorem applies to that method, and to every other conservative scheme. Unlike the [Lax equivalence theorem](/lax-equivalence-theorem/), it gives no link between stability and convergence.

## Statement

**Setting.** Let $f : \mathbb{R}^m \to \mathbb{R}^m$ be continuous and $u_0 \in L^\infty(\mathbb{R})^m$. A scheme in **conservation form** with a stencil of $p + q + 1$ cells is

$$U_j^{n + 1} = U_j^n - \frac{\Delta t}{\Delta x}\Big(\mathcal{F}(U_{j - p + 1}^n, \dots, U_{j + q}^n) - \mathcal{F}(U_{j - p}^n, \dots, U_{j + q - 1}^n)\Big),$$

with $U_j^0$ the cell averages of $u_0$. Write $F_{j + 1/2}^n = \mathcal{F}(U_{j - p + 1}^n, \dots, U_{j + q}^n)$. The numerical flux $\mathcal{F}$ is **consistent** if $\mathcal{F}(v, \dots, v) = f(v)$ for every $v$, and it is **Lipschitz** if there is a constant $L$ such that $|\mathcal{F}(v_{-p + 1}, \dots, v_q) - f(v)| \le L\max_i|v_i - v|$ for all arguments in a bounded set. Let $U^{(k)}(x, t)$ be the piecewise constant function equal to $U_j^n$ on $[x_{j - 1/2}, x_{j + 1/2}) \times [t_n, t_{n + 1})$, computed on the $k$-th grid, with $\Delta x_k, \Delta t_k \to 0$ and $\Delta t_k/\Delta x_k = \lambda$ fixed.

**Theorem (Lax and Wendroff, 1960).** Assume that the $U^{(k)}$ are uniformly bounded and that $U^{(k)} \to u$ almost everywhere and in $L^1_{\text{loc}}(\mathbb{R} \times [0, \infty))$. Then $u$ is a weak solution: for every $\varphi \in C^1_c(\mathbb{R} \times [0, \infty))$,

$$\int_0^\infty\!\!\int_{-\infty}^\infty\big(u\,\varphi_t + f(u)\,\varphi_x\big)\,dx\,dt + \int_{-\infty}^\infty u_0\,\varphi(x, 0)\,dx = 0.$$

LeVeque (2002), Section 12.10, gives the same theorem with the bounded convergence replaced by a uniform bound on the total variation of $U^{(k)}(\cdot, t)$.

## In plain words

A conservative scheme moves each quantity from cell to cell through the cell faces, so the scheme never creates or loses any of it. The theorem says that if the computed answers settle down to some limit as the grid gets finer, that limit keeps the same balance. So the limit is a correct solution in the weak sense, and its shocks move at the correct speed.

The theorem does not promise that the answers settle down at all. And a weak solution is not always the physical one. A scheme can settle on an unphysical jump, so the theorem alone cannot tell you that the answer is right.

## Proof

Fix a test function $\varphi$ and write $\varphi_j^n = \varphi(x_j, t_n)$. Multiply the scheme by $\varphi_j^n$ and sum over all $j$ and over $n \ge 0$. The sums are finite, because $\varphi$ has compact support. Sum by parts in $n$ and in $j$:

$$\sum_{n \ge 0}\varphi_j^n(U_j^{n + 1} - U_j^n) = -\varphi_j^0U_j^0 - \sum_{n \ge 1}U_j^n(\varphi_j^n - \varphi_j^{n - 1}),$$

$$\sum_j\varphi_j^n\big(F_{j + 1/2}^n - F_{j - 1/2}^n\big) = -\sum_jF_{j + 1/2}^n(\varphi_{j + 1}^n - \varphi_j^n).$$

Multiply by $\Delta x$. The scheme becomes

$$\Delta x\,\Delta t\sum_{n \ge 1}\sum_jU_j^n\,\frac{\varphi_j^n - \varphi_j^{n - 1}}{\Delta t} + \Delta x\,\Delta t\sum_{n \ge 0}\sum_jF_{j + 1/2}^n\,\frac{\varphi_{j + 1}^n - \varphi_j^n}{\Delta x} + \Delta x\sum_j\varphi_j^0U_j^0 = 0.$$

This is the discrete form of the weak formulation. Now let $k \to \infty$.

- The difference quotients of $\varphi$ converge uniformly to $\varphi_t$ and $\varphi_x$, and their support stays in a fixed compact set $K$.
- The first sum is $\iint U^{(k)}\varphi_t\,dx\,dt$ plus an error at most $\sup|U^{(k)}|$ times $o(1)$ times the area of $K$. Since $U^{(k)} \to u$ in $L^1(K)$, it converges to $\iint u\,\varphi_t\,dx\,dt$.
- For the second sum, the Lipschitz bound gives $|F_{j + 1/2}^n - f(U_j^n)| \le L\max_i|U_{j + i}^n - U_j^n|$. The shifted functions $U^{(k)}(x + i\Delta x_k, t)$ also converge to $u$ in $L^1(K)$, because translation is continuous in $L^1$. So the piecewise constant numerical flux converges to $f(u)$ in $L^1(K)$; here the uniform bound and the convergence almost everywhere give $f(U^{(k)}) \to f(u)$ by dominated convergence, with $f$ continuous. The second sum converges to $\iint f(u)\,\varphi_x\,dx\,dt$.
- The last sum converges to $\int u_0\,\varphi(x, 0)\,dx$, because the cell averages of $u_0$ converge to $u_0$ in $L^1_{\text{loc}}$.

The limit is the weak formulation, so $u$ is a weak solution. $\square$

The proof uses conservation form in one place: the sum over $j$ of the flux differences becomes a sum of fluxes times differences of $\varphi$. A scheme that is not in conservation form gives an extra sum that does not vanish at a shock.

## Consequences

- **Correct shock speeds.** A convergent conservative scheme gives shocks at the Rankine-Hugoniot speed. This is the main reason for finite volume methods in conservation form, such as the [Godunov method](/godunov-method/). Measurement: for Burgers' equation with the data $u = 1$ for $x < 0$ and $u = 0$ for $x > 0$, the conservative upwind scheme with $\Delta t/\Delta x = 0.5$ gains exactly $\lambda f(1) = 0.25$ cells of mass in each step, so the shock moves at $\frac12$.
- **The non-conservative form gives the wrong answer.** The upwind scheme for $u_t + uu_x = 0$, $U_j^{n + 1} = U_j^n - \lambda U_j^n(U_j^n - U_{j - 1}^n)$, keeps the same data unchanged for ever: where $U_j = 0$ the update is zero, and where $U_j = 1$ the left neighbor is also 1. It converges to a stationary jump, which is not a weak solution. This is easy to check by hand. Hou and LeFloch (1994) analyse the error of such schemes.
- **With stability, convergence.** If a conservative scheme is also total variation stable, for example a [TVD](/total-variation-diminishing/) scheme, then Helly's theorem gives a subsequence that converges in $L^1_{\text{loc}}$, and the theorem says that every such limit is a weak solution (LeVeque 2002, Section 12.12).
- **With a discrete entropy inequality, the entropy solution.** If the scheme also satisfies a discrete entropy inequality with a numerical entropy flux, the same summation argument shows that the limit satisfies the entropy inequality (LeVeque 2002, Section 12.11). For a scalar law the limit is then the unique entropy solution. Monotone schemes and [entropy stable schemes](/entropy-stable-scheme/) are built for this.

## Tightness

- **No convergence is promised.** The theorem assumes convergence. It applies to the [Lax-Wendroff method](/lax-wendroff-method/), which is conservative and consistent, but it says nothing about whether the oscillations of that method near shocks go away. The stability needed for convergence must come from another argument.
- **The limit need not be the entropy solution.** For Burgers' equation with $u_L = -1$ and $u_R = 1$, the [Roe solver](/roe-solver/) has the Roe speed $\frac12(u_L + u_R) = 0$ at the jump. Its numerical flux there is $\frac12(f(-1) + f(1)) = \frac12$, the same as the flux $f(\pm 1) = \frac12$ at every other face. So the stationary jump is a steady state of the scheme on every grid. The scheme converges, the limit is a weak solution, and it is an expansion shock that fails the Lax entropy condition. The [Harten-Hyman entropy fix](/harten-hyman-entropy-fix/) removes it.
- **Conservation form is needed.** The non-conservative example above is consistent with the same smooth equation and converges, but not to a weak solution.
- **The mode of convergence is needed.** The proof passes to the limit in $f(U^{(k)})$, which needs strong convergence. Weak convergence of $U^{(k)}$ alone does not give $f(U^{(k)}) \to f(u)$ for a nonlinear $f$, as the example of rapidly oscillating functions shows.

## History

Lax and Wendroff proved the theorem in 1960, in the paper that also introduced the second order Lax-Wendroff method. LeVeque's textbook form with a total variation bound is the version that most numerical analysis courses now teach. Later work, for example Hou and LeFloch (1994), made precise how non-conservative schemes fail at shocks.

## References
