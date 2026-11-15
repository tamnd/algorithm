---
tag: F4R34P
kind: algorithm
slug: balanced-truncation
name: Balanced truncation
aliases:
- Moore balanced truncation
area: control/state-space-control
level: advanced
summary: "Reduces an asymptotically stable linear system by deleting the balanced states with small Hankel singular values, with a guaranteed H-infinity error bound."
solves: [model-order-reduction]
model: floating-point-model
complexity:
  vars: {n: the number of states, m: the number of inputs, p: the number of outputs, r: the reduced order}
  time: {worst: "O(n^3 + n^2 (m + p))"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, exact: false, recursive: false, online: false}
history:
  year: 1981
  people: [Bruce C. Moore, Lars Pernebo, Leonard M. Silverman, Dale F. Enns, Keith Glover]
  note: "Moore introduced balanced truncation in 1981; Pernebo and Silverman proved in 1982 that the reduced model is asymptotically stable, and Enns and Glover proved the H-infinity error bound in 1984."
prereqs: [balanced-realization, model-order-reduction, lyapunov-equation, singular-value-decomposition]
see_also: [balanced-truncation-error-bound, hankel-singular-values, iterative-rational-krylov, singular-perturbation-method, cholesky-decomposition, backward-error-analysis, floating-point-model, h-infinity-norm]
sources:
  - paper: doi:10.1109/TAC.1981.1102568
    title: B. C. Moore, Principal component analysis in linear systems, controllability, observability, and model reduction, IEEE Transactions on Automatic Control 26(1), 17-32, 1981
    locator: the internally balanced realization and the reduced model obtained by deleting the weak states
  - paper: doi:10.1109/TAC.1982.1102945
    title: L. Pernebo and L. M. Silverman, Model reduction via balanced state space representations, IEEE Transactions on Automatic Control 27(2), 382-387, 1982
    locator: the stability and minimality of the truncated balanced model
  - paper: doi:10.1109/CDC.1984.272286
    title: Dale F. Enns, Model reduction with balanced realizations, an error bound and a frequency weighted generalization, 23rd IEEE Conference on Decision and Control, 127-132, 1984
    locator: the bound of twice the sum of the deleted Hankel singular values and the frequency-weighted version
  - paper: doi:10.1080/00207178408933239
    title: Keith Glover, All optimal Hankel-norm approximations of linear multivariable systems and their L-infinity error bounds, International Journal of Control 39(6), 1115-1193, 1984
    locator: the L-infinity error bound for balanced truncation, with each distinct Hankel singular value counted once
  - paper: doi:10.1109/TAC.1987.1104549
    title: A. J. Laub, M. T. Heath, C. C. Paige and R. C. Ward, Computation of system balancing transformations and other applications of simultaneous diagonalization algorithms, IEEE Transactions on Automatic Control 32(2), 115-122, 1987
    locator: the balancing transformation from Cholesky factors of the Gramians and an SVD of their product
  - book: isbn:9780898715293
    title: Athanasios C. Antoulas, Approximation of Large-Scale Dynamical Systems, SIAM, 2005
    locator: Chapter 7, Balancing and balanced approximations
  - book: isbn:9780134565675
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Chapter 7, Model Reduction by Balanced Truncation
---

Balanced truncation makes a small model out of a large one. It applies to an asymptotically stable linear system, given by matrices $A$, $B$, $C$, $D$ with $n$ internal states, and it returns a system with $r < n$ states whose response to every input is close to the original response. The method first measures, for each direction in the state space, how strongly the inputs drive it and how strongly the outputs show it. These two measures are matrices, the [controllability Gramian](/controllability-gramian/) and the [observability Gramian](/observability-gramian/). A change of coordinates, the [balanced realization](/balanced-realization/), makes them equal and diagonal. The diagonal entries, the [Hankel singular values](/hankel-singular-values/) $\sigma_1 \ge \dots \ge \sigma_n$, rank the states, and the method keeps the first $r$ and deletes the rest. The result is guaranteed to be asymptotically stable, with $A_r$ Hurwitz, when $\sigma_r > \sigma_{r+1}$, and its worst-case gain error over all frequencies, the [H-infinity norm](/h-infinity-norm/) of $G - G_r$, is at most twice the sum of the distinct deleted values (Enns 1984, Glover 1984). No model of order $r$ can do better than $\sigma_{r+1}$, so the method is within a factor of about $2(n - r)$ of the best possible in the worst case, and usually much closer. Moore (1981) introduced it; it is the standard method of [model order reduction](/model-order-reduction/) for dense models with up to a few thousand states.

## In plain words

A large model has many internal variables, but most of them matter little for what goes from the inputs to the outputs. Some are hard to move with the inputs. Others move but barely show in the outputs. A variable is worth keeping only if it is both easy to move and easy to see. The method first turns the model so that these two qualities are measured on the same scale for each internal direction. Then it sorts the directions by that common measure and throws away the weakest ones. The thrown-away measures also give a guarantee: the small model's error, for any input, is at most twice their sum.

## The problem

Input: $A \in \mathbb{R}^{n \times n}$ Hurwitz, $B \in \mathbb{R}^{n \times m}$, $C \in \mathbb{R}^{p \times n}$, $D \in \mathbb{R}^{p \times m}$ and an order $0 \le r \le n$. Output: $A_r \in \mathbb{R}^{r \times r}$, $B_r \in \mathbb{R}^{r \times m}$, $C_r \in \mathbb{R}^{p \times r}$, $D_r = D$, the Hankel singular values $\sigma_1 \ge \dots \ge \sigma_n$, and the bound

$$\|G - G_r\|_\infty \le 2 \sum_{\text{distinct } \sigma_k,\ k > r} \sigma_k,$$

where $G(s) = C(sI - A)^{-1}B + D$ and $G_r(s) = C_r(sI - A_r)^{-1}B_r + D$. The reduced model must be the truncation of a balanced realization of $G$. If $0 < r < n$ and $\sigma_r = \sigma_{r+1}$, the cut would split a repeated value; the theorem then gives no guarantee, and the implementation refuses.

## The algorithm

```pseudo id=main
BALANCED-TRUNCATION(A, B, C, D, r)
L1  W_c, W_o ← solve A W_c + W_c Aᵀ + B Bᵀ = 0 and Aᵀ W_o + W_o A + Cᵀ C = 0
L2  L_c, L_o ← factors with W_c = L_c L_cᵀ and W_o = L_o L_oᵀ
L3  U Σ Vᵀ ← SVD of L_oᵀ L_c                      ▷ σ_1 ≥ ... ≥ σ_n ≥ 0
L4  if 0 < r < n and σ_r = σ_(r+1) then fail       ▷ a gap is needed
L5  T_r ← L_c V_r Σ_r^(-1/2);  W_r ← L_o U_r Σ_r^(-1/2)
L6  A_r ← W_rᵀ A T_r;  B_r ← W_rᵀ B;  C_r ← C T_r;  D_r ← D
L7  bound ← 2 · (sum of the distinct values among σ_(r+1), ..., σ_n)
L8  return (A_r, B_r, C_r, D_r, σ, bound)
```

Line L1 solves the two [Lyapunov equations](/lyapunov-equation/) for the Gramians. Libraries use the Bartels-Stewart method or Hammarling's method, which work on a Schur form of $A$ and cost $O(n^3)$. The implementation solves the Kronecker form $(I \otimes A + A \otimes I)\operatorname{vec} W = -\operatorname{vec}(BB^T)$ directly, which costs $O(n^6)$ and is used only for the small test systems. Line L2 takes square-root factors. Libraries take [Cholesky factors](/cholesky-decomposition/), usually computed directly from the Lyapunov equation; the implementation uses $L = Q \Lambda^{1/2}$ from a symmetric eigendecomposition, which also works when a Gramian is singular. Line L3 is the square-root step of Laub, Heath, Paige and Ward (1987): the singular values of $L_o^T L_c$ are the Hankel singular values. Line L4 checks the gap, with the tolerance $\sigma_r - \sigma_{r+1} \le 10^{-9} \sigma_1$ in the code. Line L5 builds only the first $r$ columns of the balancing transformation $T = L_c V \Sigma^{-1/2}$ and of $T^{-T} = L_o U \Sigma^{-1/2}$, with $V_r$ and $U_r$ the first $r$ columns of $V$ and $U$; the full $T$ is never formed or inverted. Line L6 projects. Line L7 computes the bound, with values that agree within $10^{-9}\sigma_1$ counted once.

## Example

**A chain of four first-order sections.** $A = \begin{bmatrix} -1 & 1 & 0 & 0 \\ 0 & -2 & 1 & 0 \\ 0 & 0 & -3 & 1 \\ 0 & 0 & 0 & -4 \end{bmatrix}$, $B = e_4$, $C = e_1^T$, $D = 0$, so $G(s) = 1/((s+1)(s+2)(s+3)(s+4))$. Line L3 gives $\sigma = (0.0279876, 0.00821788, 0.00112693, 0.0000632855)$. The norm of $G$ is $\|G\|_\infty = G(0) = 1/24 = 0.041667$. The table lists, for each $r$, the error measured on a frequency grid, the lower bound $\sigma_{r+1}$, the bound of line L7, the poles of $G_r$ and its gain at $s = 0$.

| $r$ | $\sigma_{r+1}$ | $\|G - G_r\|_\infty$ (grid) | bound (L7) | poles of $G_r$ | $G_r(0)$ |
| --- | --- | --- | --- | --- | --- |
| 0 | 0.027988 | 0.041667 | 0.074791 | none | 0 |
| 1 | 0.0082179 | 0.014601 | 0.018816 | $-0.21816$ | 0.055975 |
| 2 | 0.0011269 | 0.0021479 | 0.0023804 | $-0.65319 \pm 0.60793i$ | 0.039539 |
| 3 | 0.0000632855 | 0.00012657 | 0.00012657 | $-0.87126$, $-1.64055 \pm 1.07396i$ | 0.041793 |

Every error lies between $\sigma_{r+1}$ and the bound, as the theorems require. For $r = 3$ the error on the grid equals $2\sigma_4$ within $10^{-12}$, so the bound is attained (a measurement; the tests check it). The reduced poles are not a subset of the original poles $-1, -2, -3, -4$: balanced truncation does not keep modes, it keeps directions. With $r = 2$ the model has two states and a relative error of $0.0021479 / 0.041667 = 5.2$ percent. The gain at $s = 0$ is not kept: for $r = 1$ it is $0.056$ instead of $0.042$.

**Two modes.** For $G(s) = 1/(s+1) + 1/(s+3)$, the [balanced realization](/balanced-realization/) page gives the balanced form; truncation to $r = 1$ gives $G_1(s) = 1.83205/(s + 1.44530)$ with error $0.065741 = 2\sigma_2$, again the bound, attained at $\omega = 0$.

## Correctness

The full proof is in proofs/correctness.md. Its steps are theorems:

1. **The values are right.** The singular values of $L_o^T L_c$ are the square roots of the eigenvalues of $L_c^T L_o L_o^T L_c$, which has the same nonzero eigenvalues as $L_c L_c^T L_o L_o^T = W_c W_o$.
2. **The projection is oblique and exact.** From $L_o^T L_c V_r = U_r \Sigma_r$ and $L_c^T L_o U_r = V_r \Sigma_r$ follows $W_r^T T_r = \Sigma_r^{-1/2} U_r^T L_o^T L_c V_r \Sigma_r^{-1/2} = I_r$.
3. **The reduced model is balanced.** $W_c W_r = T_r \Sigma_r$ and $W_o T_r = W_r \Sigma_r$. Multiplying the full Lyapunov equations by $W_r^T$ and $W_r$, or by $T_r^T$ and $T_r$, gives $A_r \Sigma_r + \Sigma_r A_r^T + B_r B_r^T = 0$ and $A_r^T \Sigma_r + \Sigma_r A_r + C_r^T C_r = 0$.
4. **It is the truncation of a balanced realization.** When the system is minimal, $T = L_c V \Sigma^{-1/2}$ balances it, $T_r$ is its first $r$ columns and $W_r^T$ the first $r$ rows of $T^{-1}$, so $(A_r, B_r, C_r)$ is the leading block of the balanced realization.
5. **Stability and the bound.** If $\sigma_r > \sigma_{r+1}$, $A_r$ is Hurwitz (Pernebo and Silverman 1982) and the bound of line L7 holds (Enns 1984, Glover 1984). The proof is on the [error bound](/balanced-truncation-error-bound/) page.

The tests check the Gramians by their Lyapunov residuals, the values against the square roots of the roots of $\det(sI - W_c W_o)$ on 500 random systems, the invariance under a change of coordinates, the balanced Gramians and the stability of $A_r$, the error between $\sigma_{r+1}$ and the bound on a grid, and the cases where the bound is attained.

## Complexity

With dense matrices, and counting floating-point operations:

- Line L1 costs $O(n^3 + n^2 (m + p))$ by the Bartels-Stewart method; the Kronecker solve of the implementation costs $O(n^6)$ time and $O(n^4)$ space.
- Lines L2 and L3 cost $O(n^3)$, for the factorizations and the SVD.
- Lines L5 and L6 cost $O(n^2 r + n r (m + p))$.
- Line L7 costs $O(n)$ after the sort.

So the time is $O(n^3 + n^2(m + p))$ and the extra space is $O(n^2)$. The dense cost limits the method to about $n \le 10^4$ on one computer. For large sparse $A$, low-rank factors $L_c$ and $L_o$ with few columns come from iterative Lyapunov solvers, and lines L3 to L6 then cost $O(n k^2)$ for factors with $k$ columns.

**Rounding.** In the [floating-point model](/floating-point-model/) with unit roundoff $u$, the SVD in line L3 is backward stable in the 2-norm: the computed values are the exact singular values of $L_o^T L_c + E$ with $\|E\|_2 = O(u \|L_o\|_2 \|L_c\|_2)$, so each computed $\sigma_i$ has absolute error $O(u\, \sigma_1)$ relative to the computed factors (a theorem, see [backward error analysis](/backward-error-analysis/)). The Lyapunov solvers give small residuals but are not backward stable in the Frobenius norm in general (Higham's analysis of the Sylvester equation). So values below about $u\, \sigma_1$ carry no information, and a cut there is not meaningful (a rule of thumb). Line L3 avoids forming $W_c W_o$, whose eigenvalues $\sigma_i^2$ would lose the small values below $\sqrt{u}\, \sigma_1$ instead.

## Properties

- **Asymptotic stability is kept**, with $A_r$ Hurwitz, when $\sigma_r > \sigma_{r+1}$ (a theorem). Without the gap the truncated model can have poles on the imaginary axis.
- **The error bound holds** in the $H_\infty$ norm, with each distinct value counted once (a theorem). The error is also at least $\sigma_{r+1}$, as for every model of order $r$ (a theorem).
- **The reduced model is balanced and minimal**, with Hankel singular values $\sigma_1, \dots, \sigma_r$ (a theorem). So reducing further from $G_r$ gives the same result as reducing from $G$.
- **It does not depend on the realization.** A change of coordinates of $(A, B, C)$ changes the Gramians by congruences and leaves $G_r$ the same, up to the sign freedom of the balanced realization (a theorem).
- **High frequencies are matched.** $G_r(\infty) = D = G(\infty)$, and the error tends to zero as $\omega \to \infty$. The gain at $s = 0$ is not matched in general.
- **Not optimal.** The result is not the best model of order $r$ in the $H_\infty$, $H_2$ or Hankel norm. On the chain example, the [iterative rational Krylov algorithm](/iterative-rational-krylov/) gives slightly smaller $H_2$ errors for $r = 1, 2, 3$ (a measurement).

## Variants and improvements

- **Balanced singular perturbation approximation.** Partition the balanced system and set $\dot x_2 = 0$ instead of $x_2 = 0$ (see [singular perturbation method](/singular-perturbation-method/)). The result matches $G(0)$, keeps asymptotic stability and has the same error bound. Use it when the steady-state gain matters.
- **Balancing-free square-root method.** Replace $T_r$ and $W_r$ by orthonormal bases of the same column spaces, which gives a better conditioned projection with the same $G_r$.
- **Frequency-weighted balanced truncation** (Enns 1984). Use the Gramians of the system with input and output weights. It is used for controller reduction. The general bound does not hold for it, and asymptotic stability can be lost unless the method is modified.
- **Low-rank balanced truncation.** For large sparse systems, compute low-rank Cholesky factors of the Gramians with alternating direction implicit or rational Krylov iterations, and apply lines L3 to L6 to them.
- **Unstable systems.** Split off the unstable part, which is kept, or use LQG balanced truncation, which uses Riccati equations and has a bound in a gap metric (see [nu-gap metric](/nu-gap-metric/)).
- **Discrete time.** Replace the Lyapunov equations by Stein equations. The same bound holds for $\|G - G_r\|_\infty$ on the unit circle.
- **Hankel-norm approximation** (Glover 1984). Not a truncation, but built from the same Gramians. It reaches the best possible Hankel norm error $\sigma_{r+1}$ (a theorem).

## When to use it

Use balanced truncation when the model is linear, asymptotically stable and of moderate size, up to a few thousand states, and when a guaranteed error bound in the worst-case gain is wanted, for example to reduce a plant model before a robust control design, or to reduce a controller of high order. Look at the Hankel singular values first: a fast decay means a small accurate model exists, and the gap condition tells you where to cut. Use it with low-rank Gramians for large sparse models. Use the [iterative rational Krylov algorithm](/iterative-rational-krylov/) instead when the model is very large and only solves with $sI - A$ are affordable, or when the $H_2$ error matters more than the $H_\infty$ error. Use the singular perturbation variant when the gain at $s = 0$ must be exact.

## Pitfalls

- **Line L4 skipped.** If $\sigma_r = \sigma_{r+1}$ and the cut splits the pair, the bound and the stability proof fail. For $G = \operatorname{diag}(1/(s+1), 1/(s+3), 1/(s+3))$ the values are $1/2, 1/6, 1/6$, and the implementation refuses $r = 2$. Choose $r$ at a gap.
- **Line L1 on an unstable $A$.** The Lyapunov equation can still have a solution, but it is not a Gramian and need not be positive semidefinite; for $1/(s - 1)$ it is $-1/2$. The implementation does not check that $A$ is Hurwitz; the caller must. Split off the unstable part first.
- **Line L3 on the product.** Computing $\sigma_i = \sqrt{\lambda_i(W_c W_o)}$ with an eigenvalue routine works in exact arithmetic but squares the range of the values, and the small $\sigma_i$, the ones that decide the cut, lose their accuracy. Use the SVD of $L_o^T L_c$.
- **Line L5 with the full inverse.** Forming $T$ and then $T^{-1} A T$ requires inverting a matrix with condition number up to $\kappa_2(L_c)\sqrt{\sigma_1/\sigma_n}$. The formulas of line L5 avoid the inverse.
- **Line L6 changes the gain at $s = 0$.** $D_r = D$ matches $G$ at infinite frequency, not at zero frequency. A reduced plant used for steady-state design can have the wrong static gain, as for $r = 1$ in the example. Use the singular perturbation variant.
- **Line L7 with a loose tolerance.** Values that are close but not equal are distinct, and each must be counted. Counting a cluster as one value gives a bound that is too small. The code merges only values within $10^{-9}\sigma_1$.

## Implementations

## History

Moore (1981) introduced internally balanced realizations, by analogy with principal component analysis, and proposed to delete the weakly controllable and weakly observable states. Pernebo and Silverman (1982) proved that the truncated model is asymptotically stable and minimal. Enns (1984) proved the bound of twice the sum of the deleted values and proposed the frequency-weighted version, and Glover (1984), in his paper on optimal Hankel-norm approximation, proved the bound with each distinct value counted once. Laub, Heath, Paige and Ward (1987) gave the square-root computation from Cholesky factors and an SVD, which is the form used in numerical libraries.

## References
