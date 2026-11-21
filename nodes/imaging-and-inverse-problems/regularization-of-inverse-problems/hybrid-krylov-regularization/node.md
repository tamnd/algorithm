---
tag: WCZ0JJ
kind: algorithm
slug: hybrid-krylov-regularization
name: Hybrid Krylov regularization
aliases:
- hybrid LSQR method
- hybrid projection method
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: research
summary: Project the problem onto a growing Krylov subspace by bidiagonalization and apply Tikhonov regularization to the small projected problem at each step.
solves: [fredholm-integral-equation-first-kind]
model: real-ram
complexity:
  vars: {m: "the number of data values", n: "the number of unknowns", a: "the cost of one product with A plus one product with A*", k: "the number of steps"}
  time: {per_iteration: "O(a + k (m + n) + k^3)", total: "O(k a + k^2 (m + n) + k^4)"}
  space: {extra: "O(k (m + n))"}
properties: {deterministic: true, iterative: true, matrix_free: true, linear_in_data: false, reorthogonalization: full, parameter_rules: "discrepancy principle, weighted GCV, fixed"}
history:
  year: 1981
  people: [Dianne P. O'Leary, John A. Simmons]
  note: O'Leary and Simmons proposed to regularize the small bidiagonal problem built by the Lanczos bidiagonalization instead of the large original problem.
prereqs: [lsqr, tikhonov-regularization, krylov-subspace]
see_also: [semi-convergence, cgls, generalized-cross-validation, morozov-discrepancy-principle, golub-kahan-svd-algorithm, truncated-svd, l-curve-method, image-deblurring]
sources:
  - paper: "D. P. O'Leary and J. A. Simmons, A bidiagonalization-regularization procedure for large scale discretizations of ill-posed problems, SIAM Journal on Scientific and Statistical Computing 2(4), 1981, 474 to 489"
    locator: the idea of regularizing the projected bidiagonal problem (general locator)
  - paper: "M. E. Kilmer and D. P. O'Leary, Choosing regularization parameters in iterative methods for ill-posed problems, SIAM Journal on Matrix Analysis and Applications 22(4), 2001, 1204 to 1221"
    locator: parameter choice rules applied to the projected problem (general locator)
  - paper: "J. Chung, J. G. Nagy and D. P. O'Leary, A weighted GCV method for Lanczos hybrid regularization, Electronic Transactions on Numerical Analysis 28, 2008, 149 to 167"
    locator: the weighted GCV function of the projected problem and the choice of its weight (general locator)
  - paper: doi:10.1145/355984.355989
    title: Christopher C. Paige and Michael A. Saunders, LSQR, an algorithm for sparse linear equations and sparse least squares, ACM Transactions on Mathematical Software 8(1), 1982, 43 to 71
    locator: the Golub-Kahan bidiagonalization and its relations
  - book: isbn:9780898716962
    title: Per Christian Hansen, Discrete Inverse Problems, Insight and Algorithms, SIAM, 2010
    locator: Chapter 6 (iterative regularization with Krylov methods) (general locator)
---

A hybrid Krylov method solves a large ill-posed least squares problem $\min_x \|A x - y^\delta\|$ by combining two kinds of regularization. Like [LSQR](/lsqr/), it runs the Golub-Kahan bidiagonalization, which after $k$ steps gives an orthonormal basis $V_k$ of the Krylov space $\mathcal{K}_k(A^* A, A^* y^\delta)$ and a small $(k+1) \times k$ bidiagonal matrix $B_k$. Unlike LSQR, it does not solve the projected least squares problem as it stands. It applies [Tikhonov regularization](/tikhonov-regularization/) to it, with a parameter $\lambda_k$ chosen anew at every step from the small problem alone, by the [discrepancy principle](/morozov-discrepancy-principle/) or by a weighted form of [GCV](/generalized-cross-validation/). The result $x_k = V_k z_k$ is exactly the minimizer of the Tikhonov functional $\|A x - y^\delta\|^2 + \lambda_k\|x\|^2$ over the Krylov space. Plain LSQR shows [semi-convergence](/semi-convergence/), so its result depends strongly on the stopping index. In the hybrid method the error levels off instead, and the stopping index matters much less. The parameter choice costs only work on $k \times k$ matrices.

## In plain words

Krylov methods such as LSQR build a small model of a large problem, one direction at a time, using only products with the forward operator and its adjoint. The small model captures the large, well-measured features first. If one runs too long, the model starts to include noisy directions, and the answer gets worse.

A hybrid method adds a safety brake inside the small model. At every step it solves the small model with a Tikhonov penalty, and it picks the penalty weight from the small model, which is cheap. Noisy directions that enter the model later get damped by the penalty. So the answer stops getting worse, and you can run a few extra steps without harm. This makes the method much easier to use than plain LSQR on large imaging problems.

## The problem

Given a linear operator $A$ ($m \times n$ matrix, or operator between Hilbert spaces) available only through the products $x \mapsto A x$ and $r \mapsto A^* r$, data $y^\delta$ with $\|y^\delta - A x^\dagger\| \le \delta$, and a rule for the Tikhonov parameter, compute for $k = 1, 2, \dots$
$$x_k = \operatorname*{argmin}_{x \in \mathcal{K}_k} \|A x - y^\delta\|^2 + \lambda_k \|x\|^2, \qquad \mathcal{K}_k = \mathrm{span}\{A^* y^\delta, (A^* A) A^* y^\delta, \dots, (A^* A)^{k-1} A^* y^\delta\},$$
where $\lambda_k$ is chosen by the rule from information about the projected problem only. The rules here are a fixed $\lambda$, the discrepancy principle $\|A x_k - y^\delta\| = \tau\delta$ (which needs $\delta$), and weighted GCV (which does not).

## The algorithm

```pseudo id=main
HYBRID-LSQR(A, y, K, rule)           ▷ rule: "dp" (needs δ, τ), "wgcv" (weight ω) or a fixed λ ≥ 0
L1  β₁ u₁ ← y;  α₁ v₁ ← A* u₁                    ▷ β₁, α₁ norms; u₁, v₁ unit vectors
L2  for k ← 1 to K do
L3      β_{k+1} u_{k+1} ← A v_k - α_k u_k          ▷ reorthogonalize against u₁, …, u_k
L4      α_{k+1} v_{k+1} ← A* u_{k+1} - β_{k+1} v_k  ▷ reorthogonalize against v₁, …, v_k
L5      P Σ Qᵀ ← SVD of B_k                        ▷ B_k: α₁…α_k on the diagonal, β₂…β_{k+1} below
L6      λ_k ← rule applied to (Σ, β₁ Pᵀ e₁)
L7      z_k ← argmin ‖B_k z - β₁ e₁‖² + λ_k ‖z‖²
L8      x_k ← V_k z_k                              ▷ V_k = [v₁, …, v_k]
L9  return x_K and the history (x_j, λ_j, ‖y - A x_j‖)
```

Lines L1, L3 and L4 are the Golub-Kahan bidiagonalization, as in [LSQR](/lsqr/). In exact arithmetic they give $A V_k = U_{k+1} B_k$ and $y = \beta_1 U_{k+1} e_1$. The code reorthogonalizes each new vector twice against all previous ones (classical Gram-Schmidt, run twice). Without this the bases lose orthogonality in floating point, and the small problem no longer matches the large one.

Line L5 computes the SVD $B_k = P \Sigma Q^T$ of the small matrix, with $P$ of size $(k+1) \times k$, singular values $s_1 \ge \dots \ge s_k$, and coefficients $g_i = \beta_1 (P^T e_1)_i$. Every quantity the rules need is then a short sum. The projected solution and its residual are
$$z(\lambda) = \sum_i \frac{s_i g_i}{s_i^2 + \lambda} q_i, \qquad \|B_k z(\lambda) - \beta_1 e_1\|^2 = \sum_i \Big(\frac{\lambda g_i}{s_i^2 + \lambda}\Big)^2 + \Big(\beta_1^2 - \sum_i g_i^2\Big).$$

Line L6 chooses $\lambda_k$:

- **Discrepancy principle ("dp").** The residual grows with $\lambda$, so bisection on $\log\lambda$ finds the $\lambda$ with residual $\tau\delta$. If even $\lambda = 0$ gives a residual above $\tau\delta$, the Krylov space is still too small to fit the data to the noise level, and the code takes $\lambda_k = 0$, a plain LSQR step.
- **Weighted GCV ("wgcv").** Minimize $G(\lambda) = \|B_k z(\lambda) - \beta_1 e_1\|^2 / \big(k + 1 - \omega\sum_i s_i^2/(s_i^2 + \lambda)\big)^2$, first on a grid of 81 values of $\log\lambda$ and then by golden section. With $\omega = 1$ this is GCV for the small problem. Chung, Nagy and O'Leary (2008) introduced the weight $\omega$ because plain GCV on the projected problem often picks a $\lambda$ that is too small.
- **Fixed $\lambda$.** Then $x_k$ converges, as $k$ grows, to the Tikhonov solution of the full problem.

Lines L7 and L8 compute $z_k = z(\lambda_k)$ and $x_k = V_k z_k$. The loop also stops if $\alpha_{k+1}$ or $\beta_{k+1}$ is zero (to rounding), because then the Krylov space is invariant and later steps add nothing. The function `HybridResult.solve(λ)` gives $V_k z(\lambda)$ for any other $\lambda$ without new products with $A$.

## Example

The test problem of the code: the $48 \times 48$ matrix of the integration operator ($A_{ij} = h$ for $j \le i$, $h = 1/48$), the true solution $x^\dagger(t) = e^{-((t - 0.5)/0.15)^2}$ at the cell centers, and Gaussian noise drawn with `random.Random(8)` and scaled to $\delta = 0.01\,\|A x^\dagger\| = 0.01237$. The table gives the relative error $\|x_k - x^\dagger\|/\|x^\dagger\|$ and the chosen $\lambda_k$ (a measurement).

| $k$ | plain LSQR ($\lambda = 0$) | hybrid, dp ($\tau = 1.01$) | $\lambda_k$ (dp) | hybrid, wgcv $\omega = 1$ | hybrid, wgcv $\omega = 1.5$ |
|---|---|---|---|---|---|
| 1 | 0.7433 | 0.7433 | 0 | 0.7494 | |
| 3 | 0.1887 | 0.1887 | 0 | 0.1972 | |
| 4 | 0.0738 | 0.0738 | 0 | 0.0762 | |
| 5 | 0.0466 | 0.0514 | $3.7 \cdot 10^{-4}$ | 0.0467 | 0.4394 |
| 6 | 0.0614 | 0.0579 | $4.8 \cdot 10^{-4}$ | 0.0572 | |
| 8 | 0.1786 | 0.0818 | $5.3 \cdot 10^{-4}$ | 0.1387 | 0.2447 |
| 10 | 0.2459 | 0.0820 | $5.3 \cdot 10^{-4}$ | 0.2335 | 0.1866 |
| 15 | 0.2634 | 0.0821 | $5.3 \cdot 10^{-4}$ | 0.2633 | 0.1155 |
| 30 | 0.2635 | 0.0821 | $5.3 \cdot 10^{-4}$ | 0.2635 | 0.0787 |

Plain LSQR is best at $k = 5$ (error $0.0466$) and then grows by a factor of more than $5$. For $k \le 4$ even $\lambda = 0$ leaves a residual above $\tau\delta$, so the discrepancy rule takes plain LSQR steps. From $k = 5$ on it takes $\lambda_k \approx 5.3 \cdot 10^{-4}$, and the error stays at $0.0821$ for all later $k$. For comparison, Tikhonov on the full problem with the best $\lambda$ on a grid gives $0.0786$, at $\lambda \approx 7.9 \cdot 10^{-4}$. Plain GCV ($\omega = 1$) fails on this data set: its $\lambda_k$ falls to $10^{-14}$ and the iterates follow plain LSQR. With $\omega = 1.5$, weighted GCV over-smooths at first and reaches $0.0787$ at $k = 30$. A good weight depends on the problem, which is why Chung, Nagy and O'Leary choose $\omega$ adaptively.

## Correctness

The proofs are in proofs/correctness.md, in exact arithmetic, as long as no breakdown ($\alpha_j = 0$ or $\beta_j = 0$) has occurred.

- **Bidiagonalization (theorem).** $U_{k+1}$ and $V_k$ have orthonormal columns, $A V_k = U_{k+1} B_k$, $y = \beta_1 U_{k+1} e_1$, and the columns of $V_k$ span $\mathcal{K}_k(A^* A, A^* y)$.
- **Projection (theorem).** For $x = V_k z$, $\|A x - y\|^2 + \lambda\|x\|^2 = \|B_k z - \beta_1 e_1\|^2 + \lambda\|z\|^2$. So line L8 returns the minimizer of the Tikhonov functional over the Krylov space, and the projected residual equals the true residual.
- **Special cases (theorem).** $\lambda = 0$ gives the LSQR (and [CGLS](/cgls/)) iterate. If the Krylov space is invariant under $A^* A$ (at the latest at $k = \mathrm{rank}(A)$ for a matrix), $x_k$ is the Tikhonov solution of the full problem.
- **Discrepancy rule (theorem).** The projected residual is a continuous nondecreasing function of $\lambda$ with limit $\beta_1 = \|y\|$, so if $\|B_k z(0) - \beta_1 e_1\| < \tau\delta < \|y\|$, the bisection finds a $\lambda$ with residual $\tau\delta$ to any accuracy.
- **Termination (theorem).** The loop runs at most $K$ times, and the bisection and the golden section search run a fixed number of steps.

That the hybrid method with the discrepancy rule converges as $\delta \to 0$ at the rate of Tikhonov regularization is not proved here. Once the Krylov space is invariant, the method is Tikhonov with the discrepancy principle, whose rates are on the page [Tikhonov convergence rates](/tikhonov-convergence-rates/).

## Complexity

- **Per step.** Lines L3 and L4 cost one product with $A$ and one with $A^*$, plus $O(k(m + n))$ for the reorthogonalization. Line L5 costs $O(k^3)$ for the SVD of $B_k$ (an SVD that uses the bidiagonal structure would cost $O(k^2)$). Line L6 costs $O(k)$ per evaluation of the residual or of $G$, times a fixed number of evaluations. Line L8 costs $O(n k)$.
- **Total.** $O(k a + k^2(m + n) + k^4)$ time for $k$ steps, where $a$ is the cost of one product with $A$ plus one with $A^*$, and $O(k(m + n))$ space for the two bases.
- **In practice** $k$ is a few tens to a few hundred, much less than $n$, so the products with $A$ and the reorthogonalization dominate. Plain LSQR without reorthogonalization needs only $O(m + n)$ space, which is the price of the hybrid method's stability.

## Properties

- **Stable in $k$.** Once the Krylov space contains the components that the data determine well, $\lambda_k$ settles and the error levels off (the table above). The method keeps the cheap Krylov projection and adds a guard against semi-convergence.
- **Nonlinear in the data.** Both the Krylov space and $\lambda_k$ depend on $y^\delta$.
- **Matrix-free.** Only products with $A$ and $A^*$.
- **The parameter is cheap.** Trying another $\lambda$ costs $O(k^2)$, with no product with $A$.
- **Rules without $\delta$ are heuristics.** Weighted GCV does not use $\delta$, so by the [Bakushinskii veto](/bakushinskii-veto/) it cannot work for all noise; the example shows it failing with $\omega = 1$.

## Variants and improvements

- **Other projected rules.** The L-curve, the discrepancy principle with an estimated $\delta$, or UPRE, each applied to the small problem.
- **Truncated SVD of the small problem.** Replace Tikhonov at line L7 by truncating the SVD of $B_k$.
- **General-form penalty.** For a penalty $\|L x\|$ with $L \ne I$, transform the problem to standard form first, or use a joint bidiagonalization.
- **Arnoldi hybrids.** For square $A$, use the Arnoldi process (as in GMRES) instead of Golub-Kahan, which avoids products with $A^*$.
- **Flexible and sparse hybrids.** Iteratively reweighted penalties give hybrid methods for $\ell_1$ and total variation regularization.
- **Without reorthogonalization.** Cheaper, but the projected problem then has repeated copies of singular values, and the rules can be misled.

## When to use it

Use a hybrid method for large problems, such as [image deblurring](/image-deblurring/) and tomography, where $A$ is available only through products and an SVD of $A$ is out of reach, and where you do not want to tune the stopping index of LSQR by hand. With a good estimate of $\delta$, use the discrepancy rule. Without one, use weighted GCV and check the result. For small dense problems, Tikhonov with the [SVD](/truncated-svd/) is simpler. If memory for the bases is short, use plain [LSQR](/lsqr/) or [CGLS](/cgls/) with a stopping rule.

## Pitfalls

- **No reorthogonalization at lines L3 and L4.** In floating point the bases lose orthogonality after a few tens of steps on ill-conditioned problems, and the projected residual is no longer the true residual.
- **Plain GCV on the projected problem.** It tends to pick a $\lambda$ that is too small, as in the example. Use a weight or check the result.
- **A residual target that is never reached.** If $\tau\delta$ is below the smallest residual possible in the full space (for example because $\delta$ is underestimated), the rule takes $\lambda = 0$ at every step, and the method is plain LSQR with its semi-convergence.
- **Stopping too early.** For small $k$ the Krylov space misses part of the solution, and no choice of $\lambda$ can fix that. Run until $\lambda_k$ and $x_k$ have settled.
- **A wrong adjoint.** The theory needs $A^*$ to be the true adjoint of the code for $A$. Check $\langle A x, r\rangle = \langle x, A^* r\rangle$ on random vectors.

## Implementations

## History

O'Leary and Simmons (1981) proposed to regularize the small bidiagonal problem from the Lanczos bidiagonalization instead of the large problem. Paige and Saunders (1982) published LSQR on the same bidiagonalization. Later work studied how to choose the parameter of the projected problem; Kilmer and O'Leary (2001) compared several rules, and Chung, Nagy and O'Leary (2008) introduced weighted GCV. Hybrid methods are now a standard tool in large-scale imaging.

## References
