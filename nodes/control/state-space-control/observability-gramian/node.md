---
tag: ZAATA4
kind: definition
slug: observability-gramian
name: Observability Gramian
aliases:
- observability Gramian matrix
area: control/state-space-control
level: core
summary: "W_o(t), the integral of e^(A^T s)C^T C e^(As) from 0 to t, gives the output energy of each initial state and is positive definite exactly for observable pairs. For Hurwitz A it has a limit."
prereqs: [observability, controllability-gramian]
see_also: [kalman-rank-condition, lyapunov-equation, lyapunov-theorem-for-linear-systems, hankel-singular-values, balanced-realization, balanced-truncation, state-observer, h2-norm]
sources:
  - paper: doi:10.1137/0301010
    title: R. E. Kalman, Mathematical description of linear dynamical systems, SIAM Journal on Control 1(2), 152-192, 1963
    locator: observability and its duality with controllability
  - paper: doi:10.1109/TAC.1981.1102568
    title: Bruce C. Moore, Principal component analysis in linear systems, controllability, observability, and model reduction, IEEE Transactions on Automatic Control 26(1), 17-32, 1981
    locator: the two gramians as measures of how strongly each direction is reached and seen, and the balanced coordinates built from them
  - book: isbn:9780195117776
    title: Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999
    locator: Section 6.3 (the finite horizon observability gramian) and Section 7.4 (Lyapunov equations for the gramians and balanced realization)
  - book: isbn:9780898715293
    title: Athanasios C. Antoulas, Approximation of Large-Scale Dynamical Systems, SIAM, 2005
    locator: Chapter 4 (the observability gramian and the energy of the output)
---

The observability gramian of a linear system $\dot x = A x$, $y = C x$ is the symmetric matrix $W_o(t) = \int_0^t e^{A^T s} C^T C e^{As} ds$. For each initial state $x_0$, the number $x_0^T W_o(t) x_0$ is the energy of the output on $[0, t]$, so the gramian shows how strongly each direction of the state shows in the output. It is positive definite exactly when the pair $(C, A)$ is [observable](/observability/). When $A$ is [Hurwitz](/hurwitz-matrix/) the integral to infinity exists and solves the [Lyapunov equation](/lyapunov-equation/) $A^T W_o + W_o A + C^T C = 0$. It is the dual of the [controllability gramian](/controllability-gramian/).

## Definition

**Notation.** $A \in \mathbb{R}^{n \times n}$, $C \in \mathbb{R}^{p \times n}$, time $t$ in seconds. $P > 0$ means positive definite, $P \ge 0$ positive semidefinite.

**Finite horizon gramian.** For $t > 0$,

$$W_o(t) = \int_0^t e^{A^T s} C^T C e^{As}\, ds .$$

It exists for every $A$. With zero input and $x(0) = x_0$ the output is $y(s) = C e^{As} x_0$, so

$$\int_0^t |y(s)|^2 ds = x_0^T W_o(t)\, x_0 .$$

Its properties follow from those of the controllability gramian by duality: $W_o(t)$ for $(C, A)$ is the controllability gramian of $(A^T, C^T)$.

- $W_o(t)$ is symmetric, $W_o(t) \ge 0$, and it grows with $t$.
- $\ker W_o(t) = \ker [C; CA; \dots; CA^{n-1}]$ for every $t > 0$. This kernel is the unobservable subspace: the states whose zero-input output is identically zero. So $W_o(t) > 0$ if and only if $(C, A)$ is observable.
- $\dot W_o = A^T W_o + W_o A + C^T C$ with $W_o(0) = 0$.

**Infinite horizon gramian.** If $A$ is Hurwitz,

$$W_o = \int_0^\infty e^{A^T s} C^T C e^{As}\, ds$$

exists and is the unique solution of

$$A^T W_o + W_o A + C^T C = 0 .$$

Then $W_o > 0$ if and only if $(C, A)$ is observable, and $x_0^T W_o x_0$ is the total output energy from $x_0$.

**A converse.** If $(C, A)$ is observable and the equation $A^T P + P A + C^T C = 0$ has a solution $P > 0$, then $A$ is Hurwitz. Proof: let $A v = \lambda v$ with $v \ne 0$ complex. Then $v^* (A^T P + P A) v = 2 \operatorname{Re}\lambda\, v^* P v = -|C v|^2$. By the [Popov-Belevitch-Hautus test](/popov-belevitch-hautus-test/), $C v \ne 0$, and $v^* P v > 0$, so $\operatorname{Re} \lambda < 0$. This is a form of the [Lyapunov theorem for linear systems](/lyapunov-theorem-for-linear-systems/) with a semidefinite right side.

**Estimating the state.** Observe $y(s) = C e^{As} x_0 + w(s)$ on $[0, t]$. The least squares estimate is $\hat x_0 = W_o(t)^{-1} \int_0^t e^{A^T s} C^T y(s)\, ds$. If $w$ is white noise of intensity $\sigma^2 I$, the error covariance is $\sigma^2 W_o(t)^{-1}$. So the directions along eigenvectors of $W_o(t)$ with small eigenvalues are the ones that noise hides. In practice a [state observer](/state-observer/) or a [Kalman filter](/kalman-filter/) does this job online.

**Coordinates.** Under $\bar x = T x$ the pair becomes $(C T^{-1}, T A T^{-1})$ and the gramian becomes $T^{-T} W_o T^{-1}$. The product $W_c W_o$ becomes $T W_c W_o T^{-1}$, so its eigenvalues do not change. Their square roots are the [Hankel singular values](/hankel-singular-values/). A [balanced realization](/balanced-realization/) chooses $T$ so that both gramians are equal to the same diagonal matrix, and [balanced truncation](/balanced-truncation/) then removes the states that are both hard to reach and hard to see (Moore 1981).

**Discrete time.** For $x_{k+1} = A x_k$, $y_k = C x_k$, $W_o(N) = \sum_{k=0}^{N-1} (A^T)^k C^T C A^k$, and $\sum_{k=0}^{N-1} |y_k|^2 = x_0^T W_o(N) x_0$. If $A$ is Schur, the sum to infinity converges and solves the Stein equation $A^T W_o A - W_o + C^T C = 0$.

**Norms.** For $G(s) = C (sI - A)^{-1} B$ with $A$ Hurwitz, the [H2 norm](/h2-norm/) satisfies $\|G\|_2^2 = \operatorname{trace}(B^T W_o B)$, which equals $\operatorname{trace}(C W_c C^T)$.

## Examples and non-examples

- **Scalar.** $a = -1$, $c = 1$: $y = e^{-s} x_0$, so $W_o(t) = (1 - e^{-2t})/2$ and $W_o = 1/2$, which solves $-2 W + 1 = 0$. The output energy from $x_0$ is $x_0^2/2$.
- **A two-state system.** $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$ (eigenvalues $-1$, $-2$) and $C = [1, 0]$. The solution of $A^T W + W A + C^T C = 0$ is $W_o = \begin{bmatrix} 11/12 & 1/4 \\ 1/4 & 1/12 \end{bmatrix}$, with $\det W_o = 1/72 > 0$. To check it, $A^T W_o = \begin{bmatrix} -1/2 & -1/6 \\ 1/6 & 0 \end{bmatrix}$, and adding its transpose gives $\begin{bmatrix} -1 & 0 \\ 0 & 0 \end{bmatrix} = -C^T C$. From $x_0 = (1, 0)$ the output is $y = 2 e^{-t} - e^{-2t}$, and $\int_0^\infty y^2 dt = 2 - 4/3 + 1/4 = 11/12$, the $(1, 1)$ entry. With $B = (0, 1)^T$, $W_c = \operatorname{diag}(1/12, 1/6)$, and the eigenvalues of $W_c W_o$ are $(13 \pm \sqrt{153})/288$, so the Hankel singular values are about $0.29680$ and $0.04681$. Also $B^T W_o B = 1/12$, the same $\|G\|_2^2$ that the controllability gramian gives.
- **A hidden mode (non-example of a positive definite gramian).** The same $A$ with $C = [1, 1]$ gives $W_o = \frac{1}{4} \begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}$. It is singular. Its kernel is spanned by $(1, -1)$, the eigenvector for the eigenvalue $-1$ that $C$ does not see, and the transfer function from $B = (0, 1)^T$ is $1/(s + 2)$.
- **Double integrator.** $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $C = [1, 0]$: $C e^{As} = [1, s]$, so $W_o(t) = \begin{bmatrix} t & t^2/2 \\ t^2/2 & t^3/3 \end{bmatrix}$ with determinant $t^4/12$. The pair is observable. $A$ is not Hurwitz, so there is no infinite gramian.
- **Positive definite solution without observability (non-example for the converse).** Scalar $A = 0$, $C = 0$: the equation reads $0 = 0$, so every $P > 0$ solves it, but $A$ is not Hurwitz. The converse needs observability.

## Related definitions

- [Controllability gramian](/controllability-gramian/): the dual object, $\int e^{As} B B^T e^{A^T s} ds$.
- [Observability](/observability/) and [Kalman rank condition](/kalman-rank-condition/): the gramian and the observability matrix have the same kernel.
- [Lyapunov equation](/lyapunov-equation/): the linear equation that the infinite gramian solves.
- [Hankel singular values](/hankel-singular-values/): the square roots of the eigenvalues of $W_c W_o$, invariant under a change of coordinates.
- [Balanced realization](/balanced-realization/) and [balanced truncation](/balanced-truncation/): coordinates in which the two gramians are equal and diagonal, and the model reduction built on them.
- [Detectability](/detectability/): the weaker property that the states in the kernel of $W_o(t)$ decay by themselves.

## References
