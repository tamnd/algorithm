---
tag: M8TKTV
kind: definition
slug: hankel-singular-values
name: Hankel singular values
aliases:
- Hankel singular values of a system
area: control/state-space-control
level: advanced
summary: "The square roots of the eigenvalues of W_c W_o, the product of the two Gramians of an asymptotically stable system. They do not depend on the realization and measure how much each state matters."
prereqs: [controllability-gramian, observability-gramian]
see_also: [balanced-realization, balanced-truncation, balanced-truncation-error-bound, model-order-reduction, minimal-realization, h-infinity-norm, lyapunov-equation, ho-kalman-algorithm]
sources:
  - paper: doi:10.1080/00207178408933239
    title: Keith Glover, All optimal Hankel-norm approximations of linear multivariable systems and their L-infinity error bounds, International Journal of Control 39(6), 1115-1193, 1984
    locator: the Hankel operator, its singular values computed from the two Gramians, and the lower bound sigma_(r+1) for approximations of order r
  - paper: doi:10.1109/TAC.1981.1102568
    title: B. C. Moore, Principal component analysis in linear systems, controllability, observability, and model reduction, IEEE Transactions on Automatic Control 26(1), 17-32, 1981
    locator: the second-order modes of a system, which are the Hankel singular values, and their invariance under change of coordinates
  - book: isbn:9780134565675
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Chapter 7, Model Reduction by Balanced Truncation; Chapter 8, Hankel Norm Approximation
  - book: isbn:9780898715293
    title: Athanasios C. Antoulas, Approximation of Large-Scale Dynamical Systems, SIAM, 2005
    locator: Chapter 7, Balancing and balanced approximations
---

The Hankel singular values of an asymptotically stable linear system are the numbers $\sigma_1 \ge \sigma_2 \ge \dots \ge \sigma_n \ge 0$ with $\sigma_i^2 = \lambda_i(W_c W_o)$, where $W_c$ and $W_o$ are the [controllability Gramian](/controllability-gramian/) and the [observability Gramian](/observability-gramian/). Each Gramian alone depends on the choice of state coordinates, but their product changes only by a similarity, so the $\sigma_i$ belong to the transfer function, not to the realization. They are the singular values of the Hankel operator, the map from past inputs to future outputs, and they measure how strongly each state direction is both reached by the input and seen at the output. The number of nonzero values is the order of a [minimal realization](/minimal-realization/). The largest one is the Hankel norm. In [model order reduction](/model-order-reduction/) they give both a lower bound, $\sigma_{r+1}$, for the error of every model of order $r$, and the upper bound of [balanced truncation](/balanced-truncation/).

## Definition

Let $\dot x = A x + B u$, $y = C x + D u$ with $A \in \mathbb{R}^{n \times n}$ [Hurwitz](/hurwitz-matrix/). The Gramians are the unique solutions of the [Lyapunov equations](/lyapunov-equation/)

$$A W_c + W_c A^T + B B^T = 0, \qquad A^T W_o + W_o A + C^T C = 0,$$

that is $W_c = \int_0^\infty e^{At} B B^T e^{A^T t} dt$ and $W_o = \int_0^\infty e^{A^T t} C^T C e^{A t} dt$. Both are symmetric positive semidefinite. The **Hankel singular values** are

$$\sigma_i = \sqrt{\lambda_i(W_c W_o)}, \qquad i = 1, \dots, n, \qquad \sigma_1 \ge \dots \ge \sigma_n \ge 0.$$

The eigenvalues of $W_c W_o$ are real and nonnegative, because $W_c W_o$ is similar to $L_c^T W_o L_c$ when $W_c = L_c L_c^T$ is invertible, and that matrix is symmetric positive semidefinite. In general, with any factors $W_c = L_c L_c^T$ and $W_o = L_o L_o^T$, the $\sigma_i$ are the ordinary singular values of $L_o^T L_c$. This is the square-root formula used in practice: it avoids forming the product and is more accurate for small $\sigma_i$.

**Invariance (theorem).** Under a change of coordinates $x = T \tilde x$ the system becomes $(T^{-1} A T, T^{-1} B, C T, D)$, the Gramians become $T^{-1} W_c T^{-T}$ and $T^T W_o T$, and their product becomes $T^{-1} W_c W_o T$. Similar matrices have the same eigenvalues, so the $\sigma_i$ do not change. They depend only on $G(s) = C(sI - A)^{-1}B + D$, and not on $D$.

**The Hankel operator (theorem).** The Hankel operator maps a past input $u$ on $(-\infty, 0]$ with finite energy to the future output $y(t) = \int_{-\infty}^0 C e^{A(t - \tau)} B u(\tau) d\tau$ for $t \ge 0$. It is the composition of the map from $u$ to $x(0)$ and the map from $x(0)$ to $y$, and its nonzero singular values are the nonzero $\sigma_i$. Its norm, the Hankel norm, is $\|G\|_H = \sigma_1$.

**Energy meaning (theorem, for a minimal realization).** The least input energy $\int_{-\infty}^0 \|u\|^2 dt$ that moves the state from $0$ at $t = -\infty$ to $x(0) = x_0$ is $x_0^T W_c^{-1} x_0$. The output energy $\int_0^\infty \|y\|^2 dt$ from $x(0) = x_0$ with $u = 0$ is $x_0^T W_o x_0$. In the [balanced realization](/balanced-realization/), where $W_c = W_o = \operatorname{diag}(\sigma_i)$, the unit vector $e_i$ costs $1/\sigma_i$ to reach and gives output energy $\sigma_i$. So a state with small $\sigma_i$ is hard to excite and hard to observe at the same time.

**Discrete time.** For $x_{k+1} = A x_k + B u_k$ with $A$ Schur stable, the Gramians solve the Stein equations $A W_c A^T - W_c + B B^T = 0$ and $A^T W_o A - W_o + C^T C = 0$, and the $\sigma_i$ are the singular values of the infinite Hankel matrix $[C A^{i + j} B]_{i, j \ge 0}$ of the [Markov parameters](/markov-parameters/).

## Examples and non-examples

- **First order.** $G(s) = c b / (s + a)$ with $a > 0$ and the realization $(-a, b, c)$ has $W_c = b^2/(2a)$, $W_o = c^2/(2a)$ and $\sigma_1 = |bc|/(2a)$. For $1/(s + 1)$ this is $1/2$, and for $1/(s + 4)$ it is $1/8$.
- **Non-example: one Gramian alone.** The same $G(s) = 1/(s + 1)$ with $b = 2$, $c = 1/2$ has $W_c = 2$ and $W_o = 1/8$. The eigenvalue of $W_c$ changed from $1/2$ to $2$, but $\sigma_1 = \sqrt{2 \cdot 1/8} = 1/2$ did not. Only the product is a property of the system.
- **Two modes.** $A = \operatorname{diag}(-1, -3)$, $B = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$, $C = \begin{bmatrix} 1 & 1 \end{bmatrix}$, so $G(s) = 1/(s+1) + 1/(s+3)$. Here $W_c = W_o = \begin{bmatrix} 1/2 & 1/4 \\ 1/4 & 1/6 \end{bmatrix}$, so $\sigma_i$ are the eigenvalues of this matrix: $\sigma = 1/3 \pm \sqrt{13}/12$, that is $0.63380$ and $0.032871$. The second mode is not negligible on its own, but most of its effect is shared with the first.
- **A chain of four sections.** $G(s) = 1/((s+1)(s+2)(s+3)(s+4))$ has $\sigma = 0.027988$, $0.0082179$, $0.0011269$, $0.0000632855$. The values fall by a factor of 3 to 18 at each step, so a model with two or three states is accurate; see the [balanced truncation](/balanced-truncation/) page. The tests of that page compare the values with the square roots of the roots of $\det(sI - W_c W_o)$.
- **Non-example: the poles nearest the axis.** $G(s) = 1/(s + 1) + 0.0001/(s + 0.01)$ has a pole 100 times closer to the imaginary axis than the other one. Its Hankel singular values are $0.50020$ and $0.0048020$, so the slow mode is the less important state, because its residue is small. Eigenvalues of $A$ alone do not rank the states.
- **A state that is not controllable.** $A = \operatorname{diag}(-1, -2)$, $B = e_1$, $C = \begin{bmatrix} 1 & 1 \end{bmatrix}$ has $\sigma = (1/2, 0)$. The zero value marks the state that is not needed; a minimal realization has one state.
- **Non-example: an unstable system.** For $G(s) = 1/(s - 1)$ the integral defining $W_c$ diverges, and the Lyapunov equation has the solution $-1/2$, which is not a Gramian. Hankel singular values are defined only for asymptotically stable systems; for unstable systems one uses those of the asymptotically stable part or of a coprime factorization.

## Related definitions

- **Gramians.** The [controllability Gramian](/controllability-gramian/) and the [observability Gramian](/observability-gramian/). $W_c$ is invertible exactly when $(A, B)$ is controllable, and $W_o$ exactly when $(C, A)$ is observable.
- **Balanced realization.** A realization with $W_c = W_o = \operatorname{diag}(\sigma_1, \dots, \sigma_n)$; it exists for every asymptotically stable minimal system. See [balanced realization](/balanced-realization/).
- **Hankel norm.** $\|G\|_H = \sigma_1$. It satisfies $\sigma_1 \le \|G\|_\infty \le 2(\sigma_1 + \dots + \sigma_n)$ for strictly proper $G$ with all poles in the open left half plane, with each distinct value counted once in the sum (see [H-infinity norm](/h-infinity-norm/) and the [error bound](/balanced-truncation-error-bound/)).
- **Lower bound for reduction.** For every $G_r$ of order at most $r$ with all poles in the open left half plane, $\|G - G_r\|_\infty \ge \|G - G_r\|_H \ge \sigma_{r+1}$ (Glover 1984).
- **Hankel matrix.** In discrete time, the singular values of the Hankel matrix of Markov parameters. Truncating its SVD is the [Ho-Kalman algorithm](/ho-kalman-algorithm/) and the [eigensystem realization algorithm](/eigensystem-realization-algorithm/).
- **Singular values of a matrix.** The $\sigma_i$ are the [singular values](/singular-value-decomposition/) of the operator $\Gamma_G$ and of the matrix $L_o^T L_c$; they are not the singular values of $A$ or of $G(i\omega)$.

## References
