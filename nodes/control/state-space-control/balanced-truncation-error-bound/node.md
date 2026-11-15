---
tag: B8AW34
kind: theorem
slug: balanced-truncation-error-bound
name: Balanced truncation error bound
aliases:
- Enns-Glover bound
area: control/state-space-control
level: advanced
summary: "If sigma_r > sigma_(r+1), balanced truncation gives an asymptotically stable model whose H-infinity error is at most twice the sum of the distinct deleted Hankel singular values."
prereqs: [balanced-truncation, balanced-realization, lyapunov-equation]
see_also: [hankel-singular-values, h-infinity-norm, model-order-reduction, schur-complement, bounded-real-lemma, singular-perturbation-method, iterative-rational-krylov, lyapunov-function]
sources:
  - paper: doi:10.1109/CDC.1984.272286
    title: Dale F. Enns, Model reduction with balanced realizations, an error bound and a frequency weighted generalization, 23rd IEEE Conference on Decision and Control, 127-132, 1984
    locator: the bound of twice the sum of the deleted Hankel singular values
  - paper: doi:10.1080/00207178408933239
    title: Keith Glover, All optimal Hankel-norm approximations of linear multivariable systems and their L-infinity error bounds, International Journal of Control 39(6), 1115-1193, 1984
    locator: the L-infinity error bound for balanced truncation with each distinct Hankel singular value counted once, and the lower bound sigma_(r+1) for every approximation of order r
  - paper: doi:10.1109/TAC.1982.1102945
    title: L. Pernebo and L. M. Silverman, Model reduction via balanced state space representations, IEEE Transactions on Automatic Control 27(2), 382-387, 1982
    locator: the stability and minimality of the subsystems of a balanced realization
  - book: isbn:9780134565675
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Chapter 7, Model Reduction by Balanced Truncation
  - book: isbn:9780898715293
    title: Athanasios C. Antoulas, Approximation of Large-Scale Dynamical Systems, SIAM, 2005
    locator: Chapter 7, Balancing and balanced approximations
---

The balanced truncation error bound is the guarantee behind [balanced truncation](/balanced-truncation/), the standard method of [model order reduction](/model-order-reduction/). Take an asymptotically stable linear system with [Hankel singular values](/hankel-singular-values/) $\sigma_1 \ge \dots \ge \sigma_n$, write it in a [balanced realization](/balanced-realization/), and delete the last $n - r$ states. If $\sigma_r > \sigma_{r+1}$, the reduced model is again asymptotically stable, and the largest gain of the error system over all frequencies, its [H-infinity norm](/h-infinity-norm/), is at most twice the sum of the distinct deleted values. Pernebo and Silverman (1982) proved the asymptotic stability part, and Enns (1984) and Glover (1984) proved the bound. The bound is known before any reduction is done, it can be attained, and it is within a factor $2(n - r)$ of the lower bound $\sigma_{r+1}$ that holds for every model of order $r$.

## Statement

Let $G(s) = C(sI - A)^{-1}B + D$ with $A$ [Hurwitz](/hurwitz-matrix/) and $(A, B, C)$ minimal, and let $(A, B, C, D)$ be balanced, with

$$A \Sigma + \Sigma A^T + B B^T = 0, \qquad A^T \Sigma + \Sigma A + C^T C = 0, \qquad \Sigma = \operatorname{diag}(\Sigma_1, \Sigma_2),$$

$\Sigma_1 = \operatorname{diag}(\sigma_1, \dots, \sigma_r)$ and $\Sigma_2 = \operatorname{diag}(\sigma_{r+1}, \dots, \sigma_n)$. Partition $A$, $B$, $C$ to match and put $G_r(s) = C_1(sI - A_{11})^{-1}B_1 + D$. If $\sigma_r > \sigma_{r+1}$, then:

1. $A_{11}$ is Hurwitz, and $(A_{11}, B_1, C_1)$ is a minimal balanced realization with Gramians $\Sigma_1$.
2. Let $\tau_1 > \dots > \tau_k$ be the distinct values among $\sigma_{r+1}, \dots, \sigma_n$. Then
$$\|G - G_r\|_\infty \le 2 (\tau_1 + \dots + \tau_k).$$

If the realization is not minimal, apply the theorem to a minimal one; the Hankel singular values that are zero add nothing to the bound.

## In plain words

A balanced model lists its internal states from the most important to the least important, and each state comes with a number that says how much it matters. Delete the states at the bottom of the list. The theorem gives two guarantees, on one condition: the last kept number must be strictly larger than the first deleted one. First, the small model settles down after a disturbance, as the large one does. Second, for every input signal and every frequency, the small model's output differs from the large model's output by at most twice the sum of the deleted numbers, relative to the size of the input. When several deleted numbers are equal, that value is counted once.

## Proof

The full proof is in proofs/main.md. It has two parts.

**Part 1, stability.** The leading blocks of the two Lyapunov equations show that every eigenvalue $\lambda$ of $A_{11}$ satisfies $2\operatorname{Re}\lambda\; v^*\Sigma_1 v = -\|C_1 v\|^2$, so $\operatorname{Re}\lambda \le 0$. An eigenvalue $j\omega$ on the axis would give an eigenvector $v$ with $C_1 v = 0$, $B_1^T v = 0$ and $\Sigma_1 v = \sigma v$. The off-diagonal blocks of the Lyapunov equations then give $(\Sigma_2^2 - \sigma^2 I) A_{21} v = 0$. The gap makes $\Sigma_2^2 - \sigma^2 I$ invertible, so $A_{21} v = 0$, and $(v, 0)$ is an eigenvector of $A$ for $j\omega$, which is impossible.

**Part 2, the bound.** First the case $\Sigma_2 = \tau I$. On the axis $s = j\omega$, the [Schur complement](/schur-complement/) $\psi = j\omega I - A_{22} - A_{21}(j\omega I - A_{11})^{-1}A_{12}$ gives $G - G_r = \tilde C \psi^{-1} \tilde B$, and the Lyapunov equations give $\tilde B \tilde B^* = \tilde C^* \tilde C = \tau(\psi + \psi^*)$. From these, the eigenvalues of $(G - G_r)^*(G - G_r)$ are $\tau^2(2 + 2\cos\theta)$ for eigenvalues $e^{i\theta}$ of $\psi^{-*}\psi$, so the error is at most $2\tau$ at every frequency. In the general case, delete the distinct values one at a time, from the smallest. Part 1 shows that every intermediate model is minimal, balanced and asymptotically stable, so each step costs at most $2\tau_i$. The triangle inequality adds the steps.

## Consequences

- **A priori error.** The bound needs only the Hankel singular values, which come from the Gramians, so one can choose $r$ for a given tolerance before computing the reduced model.
- **A bound on the norm.** With $r = 0$, $G_0 = D$, so $\|G - D\|_\infty \le 2 \sum_{\text{distinct}} \sigma_i$ for every asymptotically stable $G$.
- **Two-sided bound.** For every asymptotically stable $\hat G$ of order at most $r$, $\|G - \hat G\|_\infty \ge \sigma_{r+1}$ (Glover 1984). The reason: the $H_\infty$ norm bounds the norm of the Hankel operator, and the Hankel operator of $\hat G$ has rank at most $r$, so it is at distance at least $\sigma_{r+1}$ from that of $G$. Balanced truncation therefore has $\sigma_{r+1} \le \|G - G_r\|_\infty \le 2(\tau_1 + \dots + \tau_k) \le 2(n - r)\sigma_{r+1}$.
- **Repeated reduction.** By part 1 the reduced model is balanced, so balanced truncation applied to $G_r$ gives the same result as applied to $G$ with the smaller order, and the bounds add.
- **Related methods.** The balanced singular perturbation approximation (see [singular perturbation method](/singular-perturbation-method/)) has the same two guarantees. Frequency-weighted balanced truncation does not have them in general.

## Tightness

- **The factor 2 is attained.** For $G(s) = 1/(s + 1)$, $\sigma_1 = 1/2$, and with $r = 0$ the error is $\|G\|_\infty = 1 = 2\sigma_1$. For $G(s) = 1/(s+1) + 1/(s+3)$ with $r = 1$, the error is $0.065741 = 2\sigma_2$, at $\omega = 0$ (a measurement; see [balanced realization](/balanced-realization/)). For the chain $1/((s+1)(s+2)(s+3)(s+4))$ with $r = 3$, the error equals $2\sigma_4 = 0.00012657$ (a measurement; see [balanced truncation](/balanced-truncation/)).
- **Distinct values are counted once.** $G = \operatorname{diag}(1/(s+1), 1/(s+3), 1/(s+3))$ has $\sigma = 1/2, 1/6, 1/6$. With $r = 1$ the error is $1/3$, which equals the bound $2 \cdot 1/6$. A sum over all deleted values, $2(1/6 + 1/6) = 2/3$, would be twice too large. Likewise $G(s) = 2s/(s^2 + s + 1)$ has $\sigma_1 = \sigma_2 = 1$ and $\|G\|_\infty = 2$, which is the bound for $r = 0$.
- **The bound is often loose.** For the chain with $r = 1$, the error is $0.014601$ and the bound is $0.018816$; with $r = 0$, the error is $0.041667$ and the bound is $0.074791$. By the two-sided bound, the ratio of the bound to the error is never more than $2(n - r)$ (a theorem).
- **The gap is needed for asymptotic stability.** $A = \begin{bmatrix} 0 & 1 \\ -1 & -1 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ \sqrt 2 \end{bmatrix}$, $C = \begin{bmatrix} 0 & \sqrt 2 \end{bmatrix}$ is balanced with $\Sigma = I$, and $A$ is Hurwitz. Truncation to $r = 1$ splits the repeated value and gives $A_{11} = 0$, which has an eigenvalue on the imaginary axis. The realization is balanced for every rotation of the state, and other rotations give other reduced models, so the truncation is not even well defined.
- **The bound is not for every norm.** The $H_2$ error of balanced truncation has no bound in terms of the deleted values alone (a theorem). For $G(s) = bc/(s + a)$ and $r = 0$, $\sigma_1 = |bc|/(2a)$ but $\|G\|_2 = |bc|/\sqrt{2a} = \sigma_1 \sqrt{2a}$, which grows without bound as $a$ grows with $\sigma_1$ fixed.

## History

Moore (1981) proposed balanced truncation without an error bound. Pernebo and Silverman (1982) proved that the truncated model is asymptotically stable and minimal when the kept and deleted values are distinct. Enns (1984), in a conference paper, proved the bound of twice the sum of the deleted values. Glover (1984), in his paper on optimal Hankel-norm approximation, proved it with each distinct value counted once and gave the lower bound $\sigma_{r+1}$. The proof by the Schur complement and the identity $\tilde B \tilde B^* = \tau(\psi + \psi^*)$ is the standard one in textbooks.

## References
