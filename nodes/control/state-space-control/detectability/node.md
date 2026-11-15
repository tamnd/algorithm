---
tag: VCDG6Z
kind: definition
slug: detectability
name: Detectability
aliases:
- detectable pair
area: control/state-space-control
level: core
summary: A pair (C, A) is detectable if some observer gain L makes A - LC Hurwitz, so the estimation error goes to zero. This holds exactly when every mode the output cannot see is asymptotically stable.
prereqs: [observability, stabilizability, popov-belevitch-hautus-test]
see_also: [stabilizability, observability, state-observer, luenberger-observer, kalman-decomposition, stabilizing-riccati-solution-theorem, infinite-horizon-lqr, separation-principle]
sources:
  - paper: doi:10.1016/S1385-7258(70)80049-X
    title: M. L. J. Hautus, Stabilization, controllability and observability of linear autonomous systems, Indagationes Mathematicae (Proceedings) 73, 448-455, 1970
    locator: the eigenvalue tests for stabilizability and, by duality, for detectability
  - paper: doi:10.1137/0301010
    title: R. E. Kalman, Mathematical description of linear dynamical systems, SIAM Journal on Control 1(2), 152-192, 1963
    locator: duality between controllability and observability, and the split of a system into observable and unobservable parts
  - book: isbn:9780134565675
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Chapter 3, Linear Dynamical Systems (detectability and its eigenvalue tests)
---

A pair $(C, A)$ is detectable when some output injection gain $L$ makes $A - L C$ [Hurwitz](/hurwitz-matrix/). Then an observer driven by the output has an estimation error that goes to zero. It is weaker than [observability](/observability/): the output does not have to see every mode, but each mode that it cannot see must be asymptotically stable by itself. Detectability is the dual of [stabilizability](/stabilizability/).

## Definition

**Notation.** $\dot x = A x + B u$, $y = C x$ with $A \in \mathbb{R}^{n \times n}$ and $C \in \mathbb{R}^{p \times n}$. Pairs for observation are written $(C, A)$.

**Definition.** $(C, A)$ is *detectable* if there is an $L \in \mathbb{R}^{n \times p}$ such that $A - L C$ is Hurwitz.

**Why it matters for estimation.** The [Luenberger observer](/luenberger-observer/) $\dot{\hat x} = A \hat x + B u + L (y - C \hat x)$ has the error $e = x - \hat x$ with $\dot e = (A - L C) e$. The error goes to zero from every start if and only if $A - L C$ is Hurwitz. So some observer of this kind works exactly when $(C, A)$ is detectable.

**Equivalent tests.** The following are equivalent.

1. $(C, A)$ is detectable.
2. $(A^T, C^T)$ is stabilizable.
3. In a [Kalman decomposition](/kalman-decomposition/) for the output, $T A T^{-1} = \begin{bmatrix} A_{11} & 0 \\ A_{21} & A_{22} \end{bmatrix}$ and $C T^{-1} = [C_1, 0]$ with $(C_1, A_{11})$ observable, the block $A_{22}$ is Hurwitz.
4. $\operatorname{rank} \begin{bmatrix} A - \lambda I \\ C \end{bmatrix} = n$ for every complex $\lambda$ with $\operatorname{Re} \lambda \ge 0$ (Hautus 1970).
5. No eigenvector $v$ of $A$ ($A v = \lambda v$, $v \ne 0$) with $\operatorname{Re} \lambda \ge 0$ has $C v = 0$.

*Proof.* $(A - L C)^T = A^T - C^T L^T$, so 1 and 2 are the same statement with $K = L^T$. Tests 3, 4 and 5 are the transposes of the tests on the [stabilizability](/stabilizability/) page, proved there. $\blacksquare$

The eigenvalues of $A_{22}$ are the *unobservable eigenvalues*. They are eigenvalues of $A - L C$ for every $L$.

**A Lyapunov test.** If $(C, A)$ is detectable and $A^T P + P A + C^T C = 0$ has a solution $P \ge 0$, then $A$ is Hurwitz. Proof: let $A v = \lambda v$ with $v \ne 0$ and suppose $\operatorname{Re} \lambda \ge 0$. Then $2 \operatorname{Re} \lambda\, v^* P v = -|C v|^2$. The left side is $\ge 0$ and the right side is $\le 0$, so $C v = 0$. By test 5 this is impossible, so $\operatorname{Re} \lambda < 0$. The same argument, with $C^T C$ replaced by $Q + K^T R K$, is how detectability enters the proofs for the LQR.

**Discrete time.** For $x_{k+1} = A x_k$, $y_k = C x_k$, detectable means $A - L C$ is Schur for some $L$, and the tests use $|\lambda| \ge 1$ in place of $\operatorname{Re} \lambda \ge 0$.

**Where it is needed.** In the [infinite-horizon LQR](/infinite-horizon-lqr/) with cost $\int_0^\infty (x^T Q x + u^T R u)\, dt$, the condition that $(Q^{1/2}, A)$ is detectable makes the optimal closed loop asymptotically stable. A mode that the cost cannot see and that does not decay could be left alone by the optimal input, since leaving it alone costs nothing. Together with stabilizability of $(A, B)$, detectability gives the [stabilizing Riccati solution theorem](/stabilizing-riccati-solution-theorem/). For output feedback, the [separation principle](/separation-principle/) needs $(A, B)$ stabilizable and $(C, A)$ detectable.

## Examples and non-examples

- **An unseen mode that decays.** $A = \operatorname{diag}(1, -2)$, $C = [1, 0]$. The state $x_2$ never shows in $y$, so the pair is not observable. It is detectable: $L = (2, 0)^T$ gives $A - L C = \operatorname{diag}(-1, -2)$, and the observer error in $x_2$ decays like $e^{-2t}$ without help.
- **A hidden mode in a transfer function.** $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$, $C = [1, 1]$. The unobservable subspace is spanned by $(1, -1)$, the eigenvector for $-1$. The only unobservable eigenvalue is $-1$, so the pair is detectable.
- **An unseen mode that grows (non-example).** $A = \operatorname{diag}(-1, 2)$, $C = [1, 0]$. The eigenvector $(0, 1)$ for $\lambda = 2$ has $C v = 0$. The error in $x_2$ grows like $e^{2t}$ whatever $L$ is.
- **Speed without position (non-example).** The double integrator $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$ with velocity measured, $C = [0, 1]$. The position axis $v = (1, 0)$ has $A v = 0$ and $C v = 0$, so the eigenvalue $0$ is unobservable and the pair is not detectable. An error in the initial position estimate never decays.
- **The LQR without detectability (non-example).** Scalar $a = 1$, $b = 1$, $q = 0$, $r = 1$, so $(Q^{1/2}, A) = (0, 1)$ is not detectable. The Riccati equation $2 a p - p^2 b^2 / r + q = 0$ reads $2 p - p^2 = 0$, with the solutions $p = 0$ and $p = 2$. The cost is $\int u^2 dt$, so $u = 0$ is optimal with cost $0$. That is the solution $p = 0$, and its closed loop $\dot x = x$ is not asymptotically stable. The solution $p = 2$ gives the gain $k = 2$ and $\dot x = -x$; it is the stabilizing solution, but it is not the unconstrained optimum.

## Related definitions

- [Observability](/observability/): the stronger property, in which every eigenvalue of $A - L C$ can be placed.
- [Stabilizability](/stabilizability/): the dual property for the input.
- [State observer](/state-observer/) and [Luenberger observer](/luenberger-observer/): the estimators whose error decays exactly for detectable pairs.
- [Popov-Belevitch-Hautus test](/popov-belevitch-hautus-test/): the eigenvalue test, of which test 4 is the restriction to the closed right half plane.
- [Kalman decomposition](/kalman-decomposition/): the coordinates that show the unobservable block $A_{22}$.
- [Kalman filter](/kalman-filter/): the stochastic estimator; its steady state error dynamics are asymptotically stable under detectability and a stabilizability condition on the noise input.

## References
