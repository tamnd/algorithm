---
tag: FTMZNF
kind: definition
slug: balanced-realization
name: Balanced realization
aliases:
- internally balanced realization
area: control/state-space-control
level: advanced
summary: "A realization of an asymptotically stable system whose two Gramians are equal and diagonal, with the Hankel singular values on the diagonal. It exists exactly for minimal realizations."
prereqs: [hankel-singular-values, minimal-realization]
see_also: [balanced-truncation, hankel-singular-values, balanced-truncation-error-bound, controllability-gramian, observability-gramian, singular-value-decomposition, cholesky-decomposition, model-order-reduction]
sources:
  - paper: doi:10.1109/TAC.1981.1102568
    title: B. C. Moore, Principal component analysis in linear systems, controllability, observability, and model reduction, IEEE Transactions on Automatic Control 26(1), 17-32, 1981
    locator: the internally balanced realization, its construction from the two Gramians, and its use for model reduction
  - paper: doi:10.1109/TAC.1982.1102945
    title: L. Pernebo and L. M. Silverman, Model reduction via balanced state space representations, IEEE Transactions on Automatic Control 27(2), 382-387, 1982
    locator: the stability of the subsystems of a balanced realization
  - paper: doi:10.1109/TAC.1987.1104549
    title: A. J. Laub, M. T. Heath, C. C. Paige and R. C. Ward, Computation of system balancing transformations and other applications of simultaneous diagonalization algorithms, IEEE Transactions on Automatic Control 32(2), 115-122, 1987
    locator: the computation of the balancing transformation from Cholesky factors of the Gramians and an SVD
  - book: isbn:9780898715293
    title: Athanasios C. Antoulas, Approximation of Large-Scale Dynamical Systems, SIAM, 2005
    locator: Chapter 7, Balancing and balanced approximations
  - book: isbn:9780134565675
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Chapter 7, Model Reduction by Balanced Truncation
---

A balanced realization of an asymptotically stable linear system is a choice of state coordinates in which the [controllability Gramian](/controllability-gramian/) and the [observability Gramian](/observability-gramian/) are equal and diagonal: $W_c = W_o = \Sigma = \operatorname{diag}(\sigma_1, \dots, \sigma_n)$ with $\sigma_1 \ge \dots \ge \sigma_n > 0$, the [Hankel singular values](/hankel-singular-values/). In these coordinates each state is exactly as easy to reach from the input as it is to see at the output, and the states are sorted by importance. Moore (1981) introduced it, by analogy with principal component analysis. Every asymptotically stable [minimal realization](/minimal-realization/) can be balanced by a change of coordinates computed from two square-root factors and one [singular value decomposition](/singular-value-decomposition/). Dropping the last states of a balanced realization is [balanced truncation](/balanced-truncation/), the standard method of [model order reduction](/model-order-reduction/) with an a priori error bound.

## Definition

Let $(A, B, C, D)$ be a realization of $G(s) = C(sI - A)^{-1}B + D$ with $A$ [Hurwitz](/hurwitz-matrix/), and let $W_c$ and $W_o$ solve

$$A W_c + W_c A^T + B B^T = 0, \qquad A^T W_o + W_o A + C^T C = 0.$$

The realization is **balanced** if

$$W_c = W_o = \Sigma = \operatorname{diag}(\sigma_1, \dots, \sigma_n), \qquad \sigma_1 \ge \sigma_2 \ge \dots \ge \sigma_n > 0.$$

Then the $\sigma_i$ are the Hankel singular values, since $W_c W_o = \Sigma^2$.

**Existence (theorem).** An asymptotically stable realization has a balanced form $(T^{-1} A T, T^{-1} B, C T, D)$ for some invertible $T$ if and only if it is minimal. *Proof.* If it is minimal, $W_c$ and $W_o$ are positive definite. Take factors $W_c = L_c L_c^T$ and $W_o = L_o L_o^T$, for example [Cholesky factors](/cholesky-decomposition/), and an SVD $L_o^T L_c = U \Sigma V^T$. Then $\Sigma$ is invertible, and

$$T = L_c V \Sigma^{-1/2}, \qquad T^{-1} = \Sigma^{-1/2} U^T L_o^T.$$

Indeed $T^{-1} T = \Sigma^{-1/2} U^T (U \Sigma V^T) V \Sigma^{-1/2} = I$. The new Gramians are $T^{-1} W_c T^{-T} = \Sigma^{-1/2} U^T (U\Sigma V^T)(V \Sigma U^T) U \Sigma^{-1/2} = \Sigma$ and $T^T W_o T = \Sigma^{-1/2} V^T (V\Sigma U^T)(U\Sigma V^T) V \Sigma^{-1/2} = \Sigma$. Conversely, a balanced realization has positive definite Gramians, so it is controllable and observable, and a similarity does not change this. $\blacksquare$

**Uniqueness (theorem).** If the $\sigma_i$ are distinct, the balanced realization is unique up to the signs of the states: two balancing transformations differ by $\operatorname{diag}(\pm 1)$. If some values are repeated, the freedom is an orthogonal transformation inside each block of equal values. *Reason:* a transformation $S$ between two balanced forms satisfies $S^{-1} \Sigma S^{-T} = \Sigma$ and $S^T \Sigma S = \Sigma$, so $S^T \Sigma^2 S^{-T} = \Sigma^2$; thus $S^T$ commutes with $\Sigma^2$, and $S$ is block diagonal on the eigenspaces of $\Sigma$, where it is orthogonal.

**Properties of the balanced form (theorem).** Write $b_i$ for row $i$ of $B$ and $c_i$ for column $i$ of $C$. The diagonal entries of the two Lyapunov equations give $2 a_{ii} \sigma_i + \|b_i\|^2 = 0$ and $2 a_{ii} \sigma_i + \|c_i\|^2 = 0$. So $\|b_i\| = \|c_i\|$ and $a_{ii} = -\|b_i\|^2 / (2\sigma_i) < 0$. Every leading subsystem $(A_{11}, B_1, C_1)$ of order $r$ is again balanced, with Gramians $\operatorname{diag}(\sigma_1, \dots, \sigma_r)$, and it is asymptotically stable, with $A_{11}$ Hurwitz, when $\sigma_r > \sigma_{r+1}$ (Pernebo and Silverman 1982); see the [error bound](/balanced-truncation-error-bound/) page.

## Examples and non-examples

- **First order.** $G(s) = 1/(s + 1)$ with $(A, B, C) = (-1, 1, 1)$ is balanced: $W_c = W_o = 1/2$. The realization $(-1, 2, 1/2)$ of the same $G$ is not balanced, with $W_c = 2$ and $W_o = 1/8$; the change $x = 2 \tilde x$ balances it.
- **Two modes.** $A = \operatorname{diag}(-1, -3)$, $B = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$, $C = \begin{bmatrix} 1 & 1 \end{bmatrix}$, so $G(s) = 1/(s+1) + 1/(s+3)$. Both Gramians equal $\begin{bmatrix} 1/2 & 1/4 \\ 1/4 & 1/6 \end{bmatrix}$, but this matrix is not diagonal, so the realization is not balanced. The Hankel singular values are $1/3 \pm \sqrt{13}/12 = 0.63380, 0.032871$. A balanced form, as the implementation of [balanced truncation](/balanced-truncation/) returns it, is
$$\tilde A = \begin{bmatrix} -2 + 2/\sqrt{13} & -3/\sqrt{13} \\ -3/\sqrt{13} & -2 - 2/\sqrt{13} \end{bmatrix} = \begin{bmatrix} -1.44530 & -0.83205 \\ -0.83205 & -2.55470 \end{bmatrix}, \qquad \tilde B = \tilde C^T = \begin{bmatrix} 1.35353 \\ 0.40982 \end{bmatrix},$$
with $\tilde b_i = \sqrt{1 \pm 3/\sqrt{13}}$. The check $a_{11} = -\tilde b_1^2 / (2\sigma_1) = -1.83205 / 1.26759 = -1.44530$ agrees. Other balanced forms differ by the sign of a state. Truncating to the first state gives $G_1(s) = 1.83205 / (s + 1.44530)$ with $H_\infty$ error $0.065741 = 2\sigma_2$, the bound of the [error bound](/balanced-truncation-error-bound/) theorem, attained here at $\omega = 0$ (a measurement on a frequency grid).
- **Non-example: diagonal but not equal.** A realization with $W_c = I$ and $W_o = \Sigma^2$ is *input normal*, and one with $W_c = \Sigma^2$ and $W_o = I$ is *output normal*. They differ from the balanced form by the scaling $\Sigma^{1/2}$, and they are used in some algorithms, but they are not balanced.
- **Non-example: a realization that is not minimal.** $A = \operatorname{diag}(-1, -2)$, $B = e_1$, $C = \begin{bmatrix} 1 & 1 \end{bmatrix}$ has $W_c = \operatorname{diag}(1/2, 0)$, and $\sigma_2 = 0$. No change of coordinates gives $\Sigma$ with positive entries. Remove the state that is not controllable first, with the [Kalman decomposition](/kalman-decomposition/).
- **Non-example: an unstable system.** For $1/(s - 1)$ the Gramians are not defined. One balances the asymptotically stable part, or uses LQG balancing, which works with Riccati equations instead of Lyapunov equations.

## Related definitions

- **Hankel singular values.** The diagonal of $\Sigma$; see [Hankel singular values](/hankel-singular-values/).
- **Balanced truncation and residualization.** Keep the first $r$ balanced states, either by deleting the others ([balanced truncation](/balanced-truncation/)) or by setting their derivatives to zero (balanced singular perturbation approximation, see [singular perturbation method](/singular-perturbation-method/)).
- **Other balancings.** LQG balancing uses the solutions of the control and filter Riccati equations; stochastic balancing aims at a small relative error and keeps a minimum phase system minimum phase; positive real balancing and bounded real balancing keep passivity and contractivity of the system; frequency-weighted balancing uses Gramians of the system with input and output weights. All of them diagonalize two positive definite matrices at once by the same formula $T = L_c V \Sigma^{-1/2}$.
- **Simultaneous diagonalization.** The construction is the general way to diagonalize two symmetric positive definite matrices $P$ and $Q$ with one congruence, $T^{-1} P T^{-T} = T^T Q T$. Laub, Heath, Paige and Ward (1987) compute it from Cholesky factors and an SVD, without forming $W_c W_o$.
- **Principal component analysis.** Moore's motivation: the SVD of $L_o^T L_c$ ranks the state directions as [principal component analysis](/principal-component-analysis/) ranks the directions of a data set.
- **Condition of the transformation.** Since $V$ is orthogonal, the [condition number](/condition-number/) in the 2-norm satisfies $\kappa_2(T) \le \kappa_2(L_c) \sqrt{\sigma_1 / \sigma_n}$, and $T$ can be ill conditioned when $\sigma_n$ is tiny. Balancing-free and square-root methods avoid forming $T$ in full for this reason.

## References
