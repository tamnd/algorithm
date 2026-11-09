---
tag: R5V6FZ
kind: algorithm
slug: nonlinear-conjugate-gradient
name: Nonlinear conjugate gradient method
aliases:
- Fletcher-Reeves method
- Polak-Ribiere method
- Polak-Ribiere-Polyak method
- PR+ conjugate gradient
area: optimization/gradient-methods
level: advanced
summary: "Search along d_k = -∇f(x_k) + β_k d_(k-1) with a line search. On a quadratic with exact steps it is linear conjugate gradient; Fletcher-Reeves and PR+ converge under strong Wolfe steps."
solves: [unconstrained-smooth-minimization]
model: real-ram
complexity:
  vars: {n: the number of variables, k: the number of iterations, m: the largest number of trial steps in one line search}
  time: {worst: O(k m n)}
  space: {extra: O(n)}
  gradients: {quadratic_exact_steps: O(n), step: O(m)}
properties: {deterministic: true, iterative: true, descent_method: true, first_order: true, finite_termination_on_quadratics: true}
history:
  year: 1964
  people: [Roger Fletcher, Colin M. Reeves, Elijah Polak, Gerard Ribière, Boris T. Polyak]
  note: Fletcher and Reeves extended the conjugate gradient method of Hestenes and Stiefel to general functions in 1964. Polak and Ribière, and independently Polyak, gave the other main rule for β in 1969.
prereqs: [conjugate-gradient-method, wolfe-conditions, gradient-descent]
see_also: [conjugate-gradient-method, bfgs, limited-memory-bfgs, wolfe-conditions, gradient-descent, krylov-subspace, momentum-method, quasi-newton-method]
sources:
  - paper: doi:10.1093/comjnl/7.2.149
    title: Roger Fletcher and Colin M. Reeves, Function minimization by conjugate gradients, The Computer Journal 7(2), 1964
    locator: pages 149 to 154
  - paper: doi:10.1051/m2an/196903R100351
    title: Elijah Polak and Gerard Ribière, Note sur la convergence de méthodes de directions conjuguées, Revue française d'informatique et de recherche opérationnelle 3(16), 1969
    locator: pages 35 to 43
  - paper: doi:10.1016/0041-5553(69)90035-4
    title: Boris T. Polyak, The conjugate gradient method in extremal problems, USSR Computational Mathematics and Mathematical Physics 9(4), 1969
    locator: pages 94 to 112
  - paper: doi:10.6028/jres.049.044
    title: Magnus R. Hestenes and Eduard Stiefel, Methods of conjugate gradients for solving linear systems, Journal of Research of the National Bureau of Standards 49(6), 1952
    locator: pages 409 to 436
  - paper: doi:10.1093/imanum/5.1.121
    title: Mehiddin Al-Baali, Descent property and global convergence of the Fletcher-Reeves method with inexact line search, IMA Journal of Numerical Analysis 5(1), 1985
    locator: pages 121 to 124 (descent and global convergence of Fletcher-Reeves under the strong Wolfe conditions with c2 < 1/2)
  - paper: doi:10.1137/0802003
    title: Jean Charles Gilbert and Jorge Nocedal, Global convergence properties of conjugate gradient methods for optimization, SIAM Journal on Optimization 2(1), 1992
    locator: pages 21 to 42 (global convergence of the PR+ rule)
  - paper: doi:10.1007/BFb0099521
    title: Michael J. D. Powell, Nonconvex minimization calculations and the conjugate gradient method, Lecture Notes in Mathematics 1066, Springer, 1984
    locator: pages 122 to 141 (an example on which Polak-Ribière with exact steps cycles without converging)
  - paper: doi:10.1007/BF01593790
    title: Michael J. D. Powell, Restart procedures for the conjugate gradient method, Mathematical Programming 12, 1977
    locator: pages 241 to 254
  - paper: doi:10.1137/030601880
    title: William W. Hager and Hongchao Zhang, A new conjugate gradient method with guaranteed descent and an efficient line search, SIAM Journal on Optimization 16(1), 2005
    locator: pages 170 to 192
  - paper: doi:10.1137/S1052623497318992
    title: Yu-Hong Dai and Yaxiang Yuan, A nonlinear conjugate gradient method with a strong global convergence property, SIAM Journal on Optimization 10(1), 1999
    locator: pages 177 to 182
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Chapter 5, Conjugate gradient methods (Section 5.1 for the linear method, Section 5.2 for the nonlinear methods, restarts and global convergence)
---

The nonlinear conjugate gradient method minimizes a smooth function $f$ with search directions $d_k = -\nabla f(x_k) + \beta_kd_{k-1}$ and a line search for the step. The scalar $\beta_k$ is set by a rule: Fletcher-Reeves (FR) uses $\beta_k = \|g_k\|^2/\|g_{k-1}\|^2$ and Polak-Ribière (PR) uses $\beta_k = g_k^\top(g_k - g_{k-1})/\|g_{k-1}\|^2$, with $g_k = \nabla f(x_k)$. On a strictly convex quadratic with exact steps both rules give the linear [conjugate gradient method](/conjugate-gradient-method/), which stops at the minimizer after at most $n$ steps. On general functions the method needs only a few vectors of memory, like [gradient descent](/gradient-descent/), and is often much faster. With steps that satisfy the strong [Wolfe conditions](/wolfe-conditions/) with $c_2 < \frac12$, every FR direction goes downhill and $\liminf\|\nabla f(x_k)\| = 0$.

## In plain words

Gradient descent always walks straight downhill, so in a long narrow valley it zigzags from wall to wall. Conjugate gradient remembers the last direction it walked and mixes part of it into the new downhill direction. The mixed direction cancels most of the zigzag and points more along the valley.

How much of the old direction to keep is set by a rule that compares the new slope with the old slope. On a bowl with the exact shape of a quadratic, and with each step going exactly to the lowest point along its line, the walker reaches the bottom after at most as many steps as there are variables. On other surfaces it is not exact, but it usually needs far fewer steps than walking straight downhill.

## The problem

The input is a continuously differentiable function $f : \mathbb{R}^n \to \mathbb{R}$, given by routines for $f$ and $\nabla f$, a start $x_0$, a rule (FR or PR+), an iteration limit $K$ and a gradient tolerance $\varepsilon$. The output is a point $x_k$ with $\|\nabla f(x_k)\| \le \varepsilon$, or the last point reached. This is [unconstrained smooth minimization](/unconstrained-smooth-minimization/); the method finds stationary points, which are minimizers when $f$ is convex. All arithmetic is in floating point.

## The algorithm

```pseudo id=main
NONLINEAR-CG(f, ∇f, x₀, rule, K, ε)
L1  x ← x₀; g ← ∇f(x); d ← −g
L2  for k = 0, 1, …, K − 1 while ‖g‖ > ε do
L3      α ← a step along d that satisfies the strong Wolfe conditions
L4      x ← x + α d; g⁺ ← ∇f(x)
L5      β ← ‖g⁺‖² / ‖g‖² (FR) or β ← max(0, g⁺ᵀ(g⁺ − g) / ‖g‖²) (PR+)
L6      d ← −g⁺ + β d
L7      if g⁺ᵀd ≥ 0 then d ← −g⁺                ▷ restart along the gradient
L8      g ← g⁺
L9  return x
```

Line L3 is a strong Wolfe line search: it returns $\alpha > 0$ with $f(x + \alpha d) \le f(x) + c_1\alpha g^\top d$ and $|\nabla f(x + \alpha d)^\top d| \le c_2|g^\top d|$. The implementation uses bracketing and zoom with quadratic interpolation (Nocedal and Wright, Algorithms 3.5 and 3.6), $c_1 = 10^{-4}$, $c_2 = 0.1$, first trial $\alpha = 1$ and a limit of $100$ trial points; if the limit is reached, the method stops. A small $c_2$ makes the step close to an exact line minimization, which the conjugacy argument assumes. Line L5 is the rule. PR+ is the Polak-Ribière value clipped at $0$; a value of $0$ restarts the method along $-g^+$. Line L7 is a safeguard: if the new direction does not go downhill, it is replaced by the steepest descent direction. For FR with $c_2 < \frac12$ this never happens in exact arithmetic (claim 3 below). The method stores $x$, $g$, $g^+$ and $d$, so it needs $O(n)$ memory.

## Example

Take $f(x) = \frac12(x_1^2 + 10x_2^2)$ and $x_0 = (10, 1)$, so $g_0 = (10, 10)$ and $d_0 = (-10, -10)$. The quadratic interpolation in the zoom phase finds the exact minimizer along each line, so the steps are exact:

| $k$ | $x_k$ | $g_k$ | $\alpha_k$ | $\beta_{k+1}$ |
|---|---|---|---|---|
| 0 | $(10, 1)$ | $(10, 10)$ | $2/11$ | $81/121$ |
| 1 | $(90/11, -9/11)$ | $(90/11, -90/11)$ | $0.55$ | |
| 2 | $(0, 0)$ | $(0, 0)$ | | |

At $x_1$, $g_1 \perp g_0$, so the FR and PR values of $\beta_1$ are both $\|g_1\|^2/\|g_0\|^2 = 81/121$, and $d_1 = -g_1 + \frac{81}{121}d_0 = (-\frac{1800}{121}, \frac{180}{121})$. The second step lands on the minimizer, as the theory for quadratics predicts. [Exact line search](/exact-line-search/) along $-g_k$ on the same function needs $83$ steps to reach $\|\nabla f\| \le 10^{-6}$.

On the Rosenbrock function $f(x) = 100(x_2 - x_1^2)^2 + (1 - x_1)^2$ from $(-1.2, 1)$, with tolerance $\|\nabla f\| \le 10^{-6}$, the implementation needs:

| rule | $c_2 = 0.1$ | $c_2 = 0.45$ |
|---|---|---|
| FR | 305 steps | 74 steps |
| PR+ | 19 steps | 21 steps |

Steepest descent with the same line search and $c_2 = 0.1$ needs $381$ steps. FR with $c_2 = 0.1$ uses $2643$ values of $f$ in its line searches, and PR+ uses $153$. These counts are what this implementation does on this one problem; they illustrate the known slow progress of FR, which can take many short steps in a row, and are not general rates.

## Correctness

Let $g_k = \nabla f(x_k)$. The proofs are in the correctness proof of this page.

1. **Every step is downhill and meets the strong Wolfe conditions.** Line L7 makes every $d_k$ a descent direction, and the line search returns only steps that pass both tests. So $f(x_{k+1}) \le f(x_k) + c_1\alpha_kg_k^\top d_k < f(x_k)$, and the method stops after at most $K$ iterations.
2. **Quadratics with exact steps.** Let $f(x) = \frac12x^\top Ax - b^\top x$ with $A$ symmetric positive definite, and let each $\alpha_k$ minimize $f(x_k + \alpha d_k)$. Then the gradients are mutually orthogonal, the directions are mutually $A$-conjugate ($d_i^\top Ad_j = 0$ for $i \ne j$), FR, PR and PR+ give the same $\beta_k$, line L7 never acts, and the iterates are those of the linear conjugate gradient method. In exact arithmetic $g_k = 0$ for some $k \le m$, where $m \le n$ is the number of distinct eigenvalues of $A$.
3. **FR descent (Al-Baali).** If every step satisfies the strong Wolfe conditions with $0 < c_1 < c_2 < \frac12$, then every FR direction satisfies
   $$-\frac{1}{1 - c_2} \le \frac{g_k^\top d_k}{\|g_k\|^2} \le \frac{2c_2 - 1}{1 - c_2} < 0.$$
4. **FR global convergence (Al-Baali).** If in addition $f$ is bounded below and $\nabla f$ is Lipschitz continuous on an open set that contains the level set $\{x : f(x) \le f(x_0)\}$, then FR with $K = \infty$ and $\varepsilon = 0$ gives $\liminf_{k\to\infty}\|g_k\| = 0$.

For PR+, Gilbert and Nocedal proved $\liminf\|g_k\| = 0$ when the level set is bounded, $\nabla f$ is Lipschitz near it, and the line search gives the strong Wolfe conditions together with the sufficient descent condition $g_k^\top d_k \le -c\|g_k\|^2$ for a constant $c > 0$. Plain PR, without the clip at $0$, can fail: Powell built a smooth function on which PR with exact line searches cycles and never approaches a stationary point.

## Complexity

One iteration costs one line search plus $O(n)$ vector work. A line search with $m$ trial points costs $m$ values of $f$ and $\nabla f$ and $O(mn)$ arithmetic, so $k$ iterations cost $O(kmn)$ arithmetic plus the evaluations. The extra space is a fixed number of vectors, $O(n)$, against $O(n^2)$ for [BFGS](/bfgs/).

On a strictly convex quadratic with exact steps the method is the linear method (claim 2), so it stops after at most $n$ iterations in exact arithmetic, and its error in the $A$-norm falls at least like $2\left(\frac{\sqrt\kappa - 1}{\sqrt\kappa + 1}\right)^k$ with $\kappa$ the condition number of $A$ (Nocedal and Wright, Section 5.1). For general functions there is no such rate; claims 3 and 4 give only $\liminf\|g_k\| = 0$.

| claim | value |
|---|---|
| time per iteration | one line search, $O(mn)$ plus $m$ values of $f$ and $\nabla f$ |
| extra space | $O(n)$ |
| iterations on a quadratic with exact steps | at most the number of distinct eigenvalues, at most $n$ |

## Properties

- **Low memory.** Only four vectors of length $n$, so it fits problems where an $n \times n$ matrix does not.
- **Descent method.** With the safeguard of line L7, $f$ decreases at every step.
- **Finite termination on quadratics** in exact arithmetic with exact steps, by conjugacy.
- **Not invariant to scaling.** Like gradient descent, it depends on the coordinates; a preconditioner changes the behavior.
- **Needs an accurate line search.** Conjugacy rests on $g_{k+1}^\top d_k \approx 0$, which the strong Wolfe test with small $c_2$ provides.

## Variants and improvements

- **Other rules for β.** Hestenes-Stiefel uses $\beta_k = g_k^\top(g_k - g_{k-1})/(d_{k-1}^\top(g_k - g_{k-1}))$. Dai and Yuan use $\beta_k = \|g_k\|^2/(d_{k-1}^\top(g_k - g_{k-1}))$ and prove convergence under the standard Wolfe conditions. Hager and Zhang's method (CG_DESCENT) gives sufficient descent independent of the line search. Hybrid rules such as $\max(0, \min(\beta^{PR}, \beta^{FR}))$ combine the robustness of FR with the speed of PR.
- **Restarts.** Restart along $-g_k$ every $n$ iterations, or, following Powell, when $|g_k^\top g_{k-1}| \ge \nu\|g_k\|^2$ for a fixed fraction $\nu$ such as $0.1$ or $0.2$, which signals that successive gradients are far from orthogonal.
- **Preconditioning.** Replace $g$ by $Pg$ for a symmetric positive definite $P$ that approximates the inverse Hessian, as in the preconditioned linear method.
- **First trial step.** Start the line search at $\alpha_{k-1}g_{k-1}^\top d_{k-1}/(g_k^\top d_k)$, which assumes the first-order change along the line is the same as at the last step, in place of $\alpha = 1$.
- **Memoryless quasi-Newton view.** With exact steps, the direction $-H g_k$ where $H$ is the [BFGS](/bfgs/) update of the identity with the last pair $(s, y)$ is the Hestenes-Stiefel direction. Keeping more than one pair leads to [L-BFGS](/limited-memory-bfgs/).

## When to use it

Use nonlinear conjugate gradient for large smooth problems where gradients are cheap and $O(n^2)$ memory is too much, for example in image reconstruction, partial differential equation constrained problems and large energy minimizations. Use PR+ or Hager-Zhang rather than FR. If memory for a few more vectors is available, [L-BFGS](/limited-memory-bfgs/) is usually at least as fast and less sensitive to the line search. For a quadratic objective, use the linear [conjugate gradient method](/conjugate-gradient-method/) directly.

## Pitfalls

- **Inexact steps with FR.** FR with $c_2 \ge \frac12$ can produce an uphill direction; claim 3 needs $c_2 < \frac12$. Even with $c_2 < \frac12$, FR can take many tiny steps when $d_k$ is nearly orthogonal to $g_k$, as in the Rosenbrock example.
- **Plain PR without the clip.** Powell's example shows that PR can cycle. Clip $\beta$ at $0$ or restart.
- **A weak line search.** Backtracking with the Armijo condition alone does not bound $|g_{k+1}^\top d_k|$, so the new direction need not go downhill. Use a strong Wolfe search.
- **Loss of conjugacy in floating point.** On quadratics, rounding destroys exact conjugacy, and the method needs more than $n$ steps on ill-conditioned problems; it then behaves like an iterative method, not a direct one.
- **Stopping on $f$.** Small changes in $f$ do not mean the gradient is small; stop on $\|\nabla f\|$.

## Implementations

The Python module has the method with the FR and PR+ rules, a strong Wolfe line search by bracketing and zoom, and an option to pass a step rule, such as the exact step on a quadratic, in place of the line search. It returns the iterates and, for each step, the step length, the direction and the gradient. SciPy's `minimize(method="CG")` is a Polak-Ribière method with a Wolfe line search.

## History

Hestenes and Stiefel published the conjugate gradient method for symmetric positive definite linear systems in 1952. Fletcher and Reeves extended it to general functions in 1964, with $\beta_k = \|g_k\|^2/\|g_{k-1}\|^2$. In 1969 Polak and Ribière, and independently Polyak, proposed the rule $\beta_k = g_k^\top(g_k - g_{k-1})/\|g_{k-1}\|^2$. Powell studied restart rules in 1977 and in 1984 gave his example on which PR cycles. Al-Baali proved in 1985 that FR with a strong Wolfe search with $c_2 < \frac12$ always goes downhill and converges in the sense of $\liminf$. Gilbert and Nocedal proved convergence of PR+ in 1992. Dai and Yuan in 1999 and Hager and Zhang in 2005 gave rules with stronger guarantees.

## References
