---
tag: TFA12A
kind: algorithm
slug: coordinate-descent
name: Coordinate descent
aliases:
- CCD loop closure
- Cyclic coordinate descent loop closure
- coordinate minimization
- cyclic coordinate descent
- randomized coordinate descent
- coordinate gradient descent
area: optimization/gradient-methods
level: core
summary: Minimizes the objective along one coordinate (or block) at a time, cyclically or at random.
solves: [unconstrained-smooth-minimization]
model: real-ram
complexity:
  vars: {n: the number of variables, k: the number of iterations, p: the cost of one partial derivative, β: "the largest coordinate smoothness constant L_max", μ: the PL or strong convexity constant of f, δ: "the initial gap f(x_0) - f*", ε: "the target expected gap E f(x_k) - f* ≤ ε"}
  time: {worst: O(k (p + 1))}
  space: {extra: Θ(n)}
  steps: {expected: "⌈(n β / μ) ln(δ / ε)⌉"}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2012
  people: [Yurii Nesterov, Paul Tseng, Stephen J. Wright]
  note: Coordinate minimization is old; Nesterov (2012) gave the first global rates for the randomized coordinate gradient method on large problems.
prereqs: [gradient-descent, smoothness, polyak-lojasiewicz-condition]
see_also: [gauss-seidel-method, kaczmarz-method, lasso-regression, elastic-net, sequential-minimal-optimization, composite-minimization, stochastic-gradient-descent, proximal-gradient-method]
sources:
  - paper: doi:10.1137/100802001
    title: Yurii Nesterov, Efficiency of coordinate descent methods on huge-scale optimization problems, SIAM Journal on Optimization 22(2), 2012
    locator: pages 341 to 362, the randomized coordinate gradient method with steps 1/L_i and its rates
  - paper: doi:10.1007/s10107-015-0892-3
    title: Stephen J. Wright, Coordinate descent algorithms, Mathematical Programming 151(1), 2015
    locator: pages 3 to 34, Section 3 (randomized coordinate descent, the convex and the strongly convex rates with L_max and R_0)
  - paper: doi:10.1023/A:1017501703105
    title: Paul Tseng, Convergence of a block coordinate descent method for nondifferentiable minimization, Journal of Optimization Theory and Applications 109(3), 2001
    locator: pages 475 to 494, convergence when the nonsmooth part is separable over the blocks
  - paper: doi:10.1007/BF01584660
    title: M. J. D. Powell, On search directions for minimization algorithms, Mathematical Programming 4, 1973
    locator: pages 193 to 201, a smooth function on which cyclic exact coordinate minimization cycles without converging to a stationary point
  - paper: doi:10.18637/jss.v033.i01
    title: Jerome Friedman, Trevor Hastie and Robert Tibshirani, Regularization paths for generalized linear models via coordinate descent, Journal of Statistical Software 33(1), 2010
    locator: Section 2, the cyclic coordinate update with soft thresholding for the lasso and the elastic net
  - paper: doi:10.1137/120887679
    title: Amir Beck and Luba Tetruashvili, On the convergence of block coordinate descent type methods, SIAM Journal on Optimization 23(4), 2013
    locator: pages 2037 to 2060, sublinear rates for the cyclic block order
  - paper: doi:10.1007/s10107-019-01437-5
    title: Ruoyu Sun and Yinyu Ye, Worst-case complexity of cyclic coordinate descent, O(n^2) gap with randomized version, Mathematical Programming 185, 2021
    locator: the quadratic examples on which the cyclic order is slower by a factor of order n^2
  - paper: doi:10.1007/s10107-012-0614-z
    title: Peter Richtárik and Martin Takáč, Iteration complexity of randomized block-coordinate descent methods for minimizing a composite function, Mathematical Programming 144, 2014
    locator: pages 1 to 38, rates for a smooth function plus a block-separable convex term
  - paper: doi:10.1110/ps.0242703
    title: Adrian A. Canutescu and Roland L. Dunbrack, Cyclic coordinate descent, A robotics algorithm for protein loop closure, Protein Science 12(5), 2003
    locator: pages 963 to 972, the CCD loop closure method
---

Coordinate descent minimizes a function of $n$ variables by changing one variable at a time while the others stay fixed. The variable is chosen in a cycle or at random, and it is either minimized exactly or moved by a step $1/L_i$ along its partial derivative. For [smooth](/smoothness/) $f$ with a random choice, the expected gap shrinks by the factor $1 - \mu/(nL_{\max})$ per step under the [PL condition](/polyak-lojasiewicz-condition/), and as $2nL_{\max}R_0^2/k$ for convex $f$. It is the method of choice when one partial derivative is much cheaper than the full [gradient](/gradient/), as for the [lasso](/lasso-regression/).

## In plain words

Picture a field with hills and valleys, and only two controls: one moves you east and west, the other north and south. You turn one control until you can go no lower, then the other, and you repeat. Each turn is a simple one-variable problem.

This works well when changing one variable is cheap and the variables do not interact too strongly. It can get stuck when the bottom is at a corner that you can only reach by moving two controls at the same time.

## The problem

The basic problem is [unconstrained smooth minimization](/unconstrained-smooth-minimization/): minimize a differentiable $f : \mathbb{R}^n \to \mathbb{R}$ with infimum $f^*$. Each partial derivative is Lipschitz along its own coordinate: $\lvert\partial_i f(x + te_i) - \partial_i f(x)\rvert \le L_i\lvert t\rvert$. Notation: $L_{\max} = \max_i L_i$, $\mu$ is the PL or strong convexity constant, $R_0$ is the largest distance from a point of the level set $\{f \le f(x_0)\}$ to the set of minimizers, and $\varepsilon$ is the target accuracy. The method extends to $F = f + \sum_i h_i(x_i)$ with each $h_i$ convex, which is [composite minimization](/composite-minimization/) with a separable nonsmooth part.

## The algorithm

```pseudo id=main
COORDINATE-DESCENT(∂f, L₁..Lₙ, x₀, K)
L1  x ← x₀
L2  for k ← 0 to K − 1 do
L3      i ← a coordinate: uniform at random, or k mod n for the cyclic order
L4      x_i ← x_i − ∂_i f(x) / L_i        ▷ the other coordinates do not change
L5  return x
```

For a quadratic $f(x) = \frac{1}{2}x^\top Qx - c^\top x$, $L_i = Q_{ii}$ and line L4 is the exact minimization along coordinate $i$. The cyclic version is then the [Gauss-Seidel method](/gauss-seidel-method/) for $Qx = c$. For the lasso, $\frac{1}{2}\lVert Ax - b\rVert^2 + \lambda\lVert x\rVert_1$, the exact minimization along coordinate $j$ is

$$x_j \leftarrow \frac{S_\lambda\big(a_j^\top(b - Ax + a_jx_j)\big)}{\lVert a_j\rVert^2}, \qquad S_\lambda(v) = \operatorname{sign}(v)\max(\lvert v\rvert - \lambda, 0),$$

where $a_j$ is column $j$ of $A$. With the residual $Ax - b$ kept up to date, each update costs $O(m)$ for $m$ rows, which is $1/n$ of a full gradient.

## Example

Minimize $f(x) = \frac{1}{2}x^\top Qx - c^\top x$ with $Q = \begin{pmatrix} 2 & 1 \\ 1 & 2\end{pmatrix}$ and $c = (3, -1)$, from $x_0 = (0, 0)$, in the cyclic order. The minimizer is $x^* = Q^{-1}c = (7/3, -5/3)$ with $f^* = -13/3$.

| step | coordinate | $x$ | $f(x) - f^*$ |
|---|---|---|---|
| 0 | | (0, 0) | 4.333 |
| 1 | 1 | (1.5, 0) | 2.083 |
| 2 | 2 | (1.5, −1.25) | 0.5208 |
| 3 | 1 | (2.125, −1.25) | 0.1302 |
| 4 | 2 | (2.125, −1.5625) | 0.03255 |
| 5 | 1 | (2.28125, −1.5625) | 0.008138 |
| 6 | 2 | (2.28125, −1.64062) | 0.002035 |

After the first step, each update divides the gap by exactly $4$. For the random order, Theorem 1 below with $\mu = 1$ (the smallest eigenvalue of $Q$), $L_{\max} = 2$ and $n = 2$ guarantees the expected factor $1 - 1/4 = 3/4$ per step.

## Correctness

Along one coordinate, $f$ is a function of one variable with an $L_i$-Lipschitz derivative, so the step $1/L_i$ decreases $f$ by at least $(\partial_i f(x))^2/(2L_i)$. Averaged over a uniform random $i$, this is at least $\lVert\nabla f(x)\rVert^2/(2nL_{\max})$: a gradient step in expectation, $n$ times shorter. Under the PL condition this gives the linear rate at once. For convex $f$, the bound $f(x) - f^* \le R_0\lVert\nabla f(x)\rVert$ on the level set gives the recursion $\varphi_{k+1} \le \varphi_k - \varphi_k^2/(2nL_{\max}R_0^2)$ for the expected gap, and from it the $O(1/k)$ rate. The full proofs are below.

## Complexity

One step costs one partial derivative and $O(1)$ more work, if the method keeps auxiliary data such as a residual. The memory is $\Theta(n)$.

- **PL or strongly convex.** $\mathbb{E}f(x_k) - f^* \le (1 - \mu/(nL_{\max}))^k(f(x_0) - f^*)$, so $\lceil(nL_{\max}/\mu)\ln(\delta/\varepsilon)\rceil$ steps give an expected gap of at most $\varepsilon$, where $\delta$ is the initial gap.
- **Convex.** $\mathbb{E}f(x_k) - f^* \le 2nL_{\max}R_0^2/k$.
- **Against gradient descent.** $n$ coordinate steps cost about one gradient. Their guaranteed contraction is $e^{-\mu/L_{\max}}$ against $1 - \mu/L_f$ for one gradient step, and $L_{\max} \le L_f$, so the coordinate method gains when $L_{\max}$ is much smaller than $L_f$.
- **Cyclic order.** It decreases $f$ at every step, but its known worst-case rates are weaker. Sun and Ye (2021) give quadratics on which it is slower than the random order by a factor of order $n^2$.

## Properties

- **Monotone.** With the step $1/L_i$ or exact minimization, $f$ never increases, for any order.
- **Needs no global step size.** Each coordinate has its own $L_i$, which is often easy to compute ($Q_{ii}$, or $\lVert a_j\rVert^2$ for least squares).
- **Randomized.** The rates are in expectation over the choice of coordinates.
- **Separable nonsmooth terms are fine.** Tseng (2001) proved convergence of cyclic block minimization for a smooth $f$ plus a block-separable convex term, which covers the lasso and the [elastic net](/elastic-net/).

## Variants and improvements

- **Block coordinate descent.** Update a block of variables at once, by a block gradient step or by exact minimization over the block.
- **Importance sampling.** Pick $i$ with probability $L_i/\sum_jL_j$. The rate then depends on the average $\bar{L}$ instead of $L_{\max}$ (Nesterov 2012).
- **Proximal coordinate descent.** For $f + \sum_ih_i(x_i)$, replace line L4 by a one-variable prox step (Richtárik and Takáč 2014).
- **Gauss-Southwell rule.** Pick the coordinate with the largest $\lvert\partial_if\rvert$. It needs the full gradient, so it pays only when the gradient is cheap to keep up to date.
- **Accelerated and parallel versions.** Momentum gives a rate with $\sqrt{\kappa}$ in place of $\kappa$, and several coordinates can be updated in parallel when they interact weakly.
- **Dual coordinate ascent.** Coordinate ascent on the dual of a regularized loss, as in [sequential minimal optimization](/sequential-minimal-optimization/) for support vector machines.

## When to use it

Use coordinate descent when one partial derivative costs about $1/n$ of the gradient and the coordinates are not strongly coupled: the lasso and the elastic net along a path of $\lambda$ values (Friedman, Hastie and Tibshirani 2010), support vector machines through the dual, and large sparse quadratics. In robotics and protein modeling, the cyclic version rotates one joint at a time to close a chain, which is the CCD loop closure method (Canutescu and Dunbrack 2003). Avoid it when a coupled nonsmooth term, such as a total variation penalty, ties the coordinates together.

## Pitfalls

- **Coupled nonsmooth terms.** On $f(x, y) = x^2 + y^2 + 2\lvert x - y\rvert$, the point $(1, 1)$ minimizes $f$ along each axis, with $f = 2$, but the minimum is $f(0, 0) = 0$. Exact coordinate minimization never leaves $(1, 1)$.
- **Nonconvex cycling.** Powell (1973) gave a smooth nonconvex function on which cyclic exact coordinate minimization cycles near points that are not stationary.
- **Recomputing the gradient.** If each step computes $\nabla f$ from scratch, coordinate descent is $n$ times slower than gradient descent. Keep the residual or a similar structure up to date.
- **Badly scaled coordinates.** A single global step for all coordinates loses the main advantage. Use the per-coordinate $L_i$.

## Implementations

## History

Minimization along one coordinate at a time is one of the oldest methods of optimization, and the Gauss-Seidel method for linear systems is its quadratic case. Powell (1973) showed that the cyclic exact version can fail on smooth nonconvex functions, and Tseng (2001) proved convergence when the nonsmooth part is separable. Friedman, Hastie and Tibshirani (2010) made the cyclic version a standard solver for the lasso. Nesterov (2012) proved global rates for the randomized coordinate gradient method, and Richtárik and Takáč (2014) extended them to composite functions. Wright (2015) surveys the field.

## References
