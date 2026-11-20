---
tag: TWTF98
kind: algorithm
slug: proper-generalized-decomposition
name: Proper generalized decomposition
area: scientific-computing/uncertainty-quantification
level: research
summary: Builds a separated representation of the solution as sums of products of functions of each variable by greedy alternating enrichment.
model: real-ram
complexity:
  vars: {N: the sum nx + ny of the grid sizes, M: the number of modes, s: the number of terms of the right side, I: the largest number of alternating steps per mode}
  time: {total: "O(M (M + s) (M + s + I) N)"}
  space: {extra: "O((M + s) N)"}
properties: {deterministic: true, exact: false, iterative: true, monotone-energy: true}
history:
  year: 2006
  people: [Amine Ammar, Béchir Mokdad, Francisco Chinesta, Roland Keunings]
  note: Introduced for high-dimensional equations of kinetic theory of complex fluids, where a grid in all variables is too large. The convergence of the greedy rank-one approach was analysed by Le Bris, Lelièvre and Maday in 2009.
prereqs: [galerkin-method, kronecker-product, poisson-equation]
see_also: [sylvester-equation, alternating-least-squares, pod-galerkin-reduced-model, reduced-basis-method, stochastic-galerkin-method, curse-of-dimensionality, thomas-algorithm, discrete-sine-transform]
sources:
  - paper: doi:10.1016/j.jnnfm.2006.07.007
    title: Amine Ammar, Béchir Mokdad, Francisco Chinesta and Roland Keunings, A new family of solvers for some classes of multidimensional partial differential equations encountered in kinetic theory modeling of complex fluids, Journal of Non-Newtonian Fluid Mechanics 139(3), 2006, 153-176
    locator: the separated representation and the enrichment by alternating directions
  - paper: doi:10.1007/s00365-009-9071-1
    title: Claude Le Bris, Tony Lelièvre and Yvon Maday, Results and questions on a nonlinear approximation approach for solving high-dimensional partial differential equations, Constructive Approximation 30(3), 2009, 621-651
    locator: the greedy algorithm for the Poisson problem in separated form and its convergence
  - book: isbn:978-3-319-02864-4
    title: Francisco Chinesta, Roland Keunings and Adrien Leygue, The Proper Generalized Decomposition for Advanced Numerical Simulations, A Primer, SpringerBriefs in Applied Sciences and Technology, Springer, 2014
    locator: the construction of the separated representation for the Poisson problem and the alternating directions
---

The proper generalized decomposition (PGD) computes the solution of a partial differential equation in many variables as a sum of products of functions of one variable each, $u(x, y) \approx \sum_{m=1}^M X_m(x) Y_m(y)$. It does not need the solution first. It adds one product at a time: for the current approximation it finds a new product that lowers the energy of the error, by solving in turn a small problem for $X$ with $Y$ fixed and a small problem for $Y$ with $X$ fixed. Each small problem is a one-dimensional Galerkin problem. So the cost grows with the sum of the grid sizes, not with their product, and this is the reason to use it in high dimensions, where a grid in all variables is too large.

The [POD-Galerkin model](/pod-galerkin-reduced-model/) and the [reduced basis method](/reduced-basis-method/) are a posteriori: they first compute full solutions, then compress them. PGD is a priori: it builds the separated form from the operator and the right side, and it never forms a full solution. The truncated SVD of the exact solution gives the best sum of $M$ products in the Frobenius norm, but it needs the exact solution. PGD is greedy, so at a given $M$ it is usually less accurate than the SVD, but it costs much less. [Alternating least squares](/alternating-least-squares/) also fixes one factor and solves for the other, but it fits a known matrix; PGD solves an equation whose solution is unknown.

## In plain words

You want the temperature on a square, but you write it as a short list of "a curve in $x$ times a curve in $y$". Start with nothing. Look at what the equation still misses, and find the one product that helps the most: guess the $y$ curve, find the best $x$ curve for it, then the best $y$ curve for that $x$ curve, and repeat a few times. Add the product and look again. Each step only solves problems on a line, never on the whole square.

## The problem

The model problem is $-a u_{xx} - b u_{yy} = f$ on $(0, 1)^2$ with $u = 0$ on the boundary, with central [finite differences](/finite-difference-method/) on $n_x \times n_y$ interior points. With $U_{ij} = u(x_i, y_j)$, the discrete system is the [Sylvester equation](/sylvester-equation/)

$$K_x U + U K_y = F, \qquad K_x = \frac{a}{h_x^2} \operatorname{tridiag}(-1, 2, -1), \quad K_y = \frac{b}{h_y^2} \operatorname{tridiag}(-1, 2, -1),$$

or $(K_x \otimes I + I \otimes K_y) \operatorname{vec}(U) = \operatorname{vec}(F)$ with the [Kronecker product](/kronecker-product/). The right side is given in separated form $F = \sum_{t=1}^s f^x_t (f^y_t)^T$. The output is a list of modes $(X_m, Y_m)$ with $U_M = \sum_{m=1}^M X_m Y_m^T$. The operator $\mathcal{A}(V) = K_x V + V K_y$ is symmetric positive definite for the inner product $\langle V, W \rangle = \sum_{ij} V_{ij} W_{ij}$, so $U$ minimizes the energy

$$J(V) = \tfrac12 \langle V, \mathcal{A} V \rangle - \langle F, V \rangle, \qquad \|U - V\|_{\mathcal{A}}^2 = 2 (J(V) - J(U)).$$

## The algorithm

```pseudo id=main
PGD(K_x, K_y, separated F, M, tol)
L1  U ← 0, the empty sum of products
L2  for m = 1 to M
L3    R ← F - K_x U - U K_y, kept as a sum of products
L4    if ‖R‖_F ≤ tol ‖F‖_F then stop
L5    Y ← R^T w for a fixed w with R^T w ≠ 0
L6    repeat until X Y^T stops changing, at most I times
L7      X ← the solution of (‖Y‖² K_x + (Y^T K_y Y) I) X = R Y
L8      Y ← the solution of ((X^T K_x X) I + ‖X‖² K_y) Y = R^T X
L9    U ← U + X Y^T
L10 return the modes of U
```

Line L3 never forms $R$ as an $n_x \times n_y$ matrix. It is the list of the $s$ terms of $F$ and the $2(m-1)$ terms $-(K_x X_k) Y_k^T$ and $-X_k (K_y Y_k)^T$. Then $R Y = \sum_t p_t (q_t^T Y)$ and $R^T X$ cost $O((s + m) N)$, and line L4 uses $\|R\|_F^2 = \sum_{t, t'} (p_t^T p_{t'}) (q_t^T q_{t'})$. Lines L7 and L8 are the conditions that the derivative of $J(U + X Y^T)$ with respect to $X$, and then $Y$, is 0. Each matrix is a positive combination of a tridiagonal matrix and the identity, so the [Thomas algorithm](/thomas-algorithm/) solves it in $O(N)$. Line L5 picks $w = (1, \ldots, 1)$, or a unit vector if that gives 0, so that $R Y \ne 0$.

## Example

**By hand.** Let $F = s_k s_l^T$ be a product of eigenvectors, $K_x s_k = \lambda_k s_k$ and $K_y s_l = \mu_l s_l$. Then $R = F$ and line L5 gives $Y = (s_k^T w) s_l = c\, s_l$. Line L7 reads $c^2 \|s_l\|^2 (K_x + \mu_l I) X = c \|s_l\|^2 s_k$, so $X = s_k / (c (\lambda_k + \mu_l))$, and $X Y^T = s_k s_l^T / (\lambda_k + \mu_l)$. This is the exact solution, so the next residual is 0 and the method stops after one mode. The test file checks this on a $10 \times 7$ grid.

**The unit load.** Take $a = b = 1$, $f = 1$ (one term, $s = 1$) and a $30 \times 30$ grid. The reference is the exact discrete solution by the [discrete sine transform](/discrete-sine-transform/) in each direction. The table compares PGD with the truncated SVD of the reference, which is the best possible in the Frobenius norm. These numbers come from the test file and a scratch run.

| $M$ | relative energy error of PGD | relative Frobenius error of PGD | relative Frobenius error of the SVD | alternating steps |
|---|---|---|---|---|
| 1 | $3.20 \times 10^{-2}$ | $9.19 \times 10^{-3}$ | $9.15 \times 10^{-3}$ | 6 |
| 2 | $3.48 \times 10^{-3}$ | $7.12 \times 10^{-4}$ | $5.04 \times 10^{-4}$ | 7 |
| 3 | $8.04 \times 10^{-4}$ | $3.79 \times 10^{-4}$ | $4.62 \times 10^{-5}$ | 11 |
| 4 | $3.73 \times 10^{-4}$ | $2.16 \times 10^{-4}$ | $4.40 \times 10^{-6}$ | 30 |
| 6 | $2.05 \times 10^{-5}$ | $1.66 \times 10^{-6}$ | | 6 |
| 8 | $5.17 \times 10^{-7}$ | $1.10 \times 10^{-7}$ | | 9 |

The energy error goes down at each mode, as the proof shows. One mode is almost as good as the best rank one, but later modes are far from the SVD: a greedy sum of the best single products is not the best sum. Eight modes store $8 \cdot 60 = 480$ numbers, against 900 for the grid; in $d$ dimensions with $n$ points each the ratio is $M d n$ against $n^d$.

## Correctness

The proof file shows, in exact arithmetic, that lines L7 and L8 each give the unique minimizer of $J(U + X Y^T)$ over one factor with the other fixed, so $J$ does not increase inside the loop. The first step of line L7 lowers $J$ by $\tfrac12 (R Y)^T G^{-1} (R Y) > 0$, where $G$ is its matrix. With the identity $\|U - V\|_{\mathcal{A}}^2 = 2(J(V) - J(U))$, the energy error goes down strictly at each mode while $R \ne 0$. It also shows that the method stops after one mode when $F$ is a product of eigenvectors. Convergence of the energy error to 0 as $M$ grows is proved by Le Bris, Lelièvre and Maday for the greedy method with the best rank-one product at each step. The alternating steps find a stationary point, not always the best product, so the page cites this result and does not claim it for the implementation.

## Complexity

In the [real RAM](/real-ram/) model, with $N = n_x + n_y$: at mode $m$ the residual has $s + 2m$ terms. One alternating step costs $O((s + m) N)$ for $R Y$ or $R^T X$ and $O(N)$ for the tridiagonal solves. The norm check costs $O((s + m)^2 N)$. Over $M$ modes with at most $I$ steps each, the time is $O(M (M + s)(M + s + I) N)$. The memory is $O((M + s) N)$ for the modes and the right side. A direct solve on the grid needs $n_x n_y$ unknowns, and in $d$ dimensions $n^d$; PGD needs $O(M d n)$.

## Properties

- **A priori.** It needs the operator and the right side, not snapshots of the solution.
- **Monotone in energy.** The energy error does not grow when a mode is added, for a symmetric positive definite operator.
- **Linear in the dimension.** The cost per mode grows with $\sum_k n_k$, not with $\prod_k n_k$.
- **Not optimal.** The sum of $M$ greedy modes is usually worse than the best rank-$M$ approximation.
- **Separated input.** The right side and the operator must have a separated form with few terms.

## Variants and improvements

- **More than two variables.** For $u(x_1, \ldots, x_d)$, add products $X^{(1)}(x_1) \cdots X^{(d)}(x_d)$, and update each factor in turn with the others fixed. Parameters and time can be extra variables, which gives a solution for all parameter values at once.
- **Update of the earlier modes.** After adding a mode, recompute the coefficients, or all factors in one direction, by a Galerkin projection on the current modes. This improves the accuracy per mode.
- **Non-symmetric problems.** For an operator that is not symmetric, the Galerkin conditions no longer minimize an energy. Minimal residual or Petrov-Galerkin versions keep a monotone error.
- **Nonlinear problems.** Linearize, for example by a fixed point or Newton iteration, and apply PGD at each step.
- **Other tensor formats.** Tensor-train or hierarchical Tucker formats replace the sum of products when the canonical sum needs too many terms.

## When to use it

Use PGD when the equation has many variables, or when you want the solution as an explicit function of parameters, and when the operator and the data have a separated form with few terms. It fits the forward problems of [stochastic Galerkin](/stochastic-galerkin-method/) type, where the random variables are extra coordinates. For a problem in two or three space variables only, a direct or multigrid solver on the grid is usually better. When you can afford full solutions at chosen parameters, the [reduced basis method](/reduced-basis-method/) gives certified errors.

## Pitfalls

- **Not separable data.** A right side or a coefficient with no short separated form, such as a load on a disc, needs many terms, and the cost grows with $s$.
- **Slow convergence.** For rough data the modes decay slowly. For a random right side of rank 3 on an $8 \times 6$ grid in the tests, the relative energy error after 10 modes is still $1.07 \times 10^{-3}$, although the exact solution has rank at most 6.
- **Stagnation of the alternating steps.** The loop can need many steps or stop at a poor product. Limit the steps, and do not expect the best product.
- **The residual floor.** The Gram formula for $\|R\|_F^2$ computes a square, so cancellation limits the relative residual to about the square root of the machine precision, near $10^{-8}$. Do not set the tolerance below that.
- **Scaling of the factors.** $X Y^T$ does not change when $X$ is multiplied by $c$ and $Y$ by $1/c$. Compare products, not factors, when you test for a fixed point.

## Implementations

## History

Ammar, Mokdad, Chinesta and Keunings introduced the method in 2006 to solve high-dimensional equations of the kinetic theory of complex fluids, where a grid in all configuration variables is too large. In 2009 Le Bris, Lelièvre and Maday analysed the greedy rank-one algorithm for the Poisson problem in separated form and proved its convergence. Chinesta, Keunings and Leygue wrote a primer on the method in 2014.

## References
