---
tag: 3HPD3P
kind: definition
slug: stabilizability
name: Stabilizability
aliases:
- stabilizable pair
area: control/state-space-control
level: core
summary: A pair (A, B) is stabilizable if some state feedback u = -Kx makes A - BK Hurwitz. This holds exactly when every mode the input cannot reach is asymptotically stable.
prereqs: [controllability, popov-belevitch-hautus-test, hurwitz-matrix]
see_also: [detectability, kalman-decomposition, pole-placement-theorem, state-feedback, stabilizing-riccati-solution-theorem, infinite-horizon-lqr, separation-principle, controllability]
sources:
  - paper: doi:10.1016/S1385-7258(70)80049-X
    title: M. L. J. Hautus, Stabilization, controllability and observability of linear autonomous systems, Indagationes Mathematicae (Proceedings) 73, 448-455, 1970
    locator: the eigenvalue test for stabilizability and detectability, restricted to the eigenvalues in the closed right half plane
  - paper: doi:10.1109/TAC.1967.1098739
    title: W. M. Wonham, On pole assignment in multi-input controllable linear systems, IEEE Transactions on Automatic Control 12(6), 660-665, 1967
    locator: arbitrary eigenvalue assignment by state feedback for controllable pairs, the step used on the controllable part
  - book: isbn:9780134565675
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Chapter 3, Linear Dynamical Systems (stabilizability and detectability and their eigenvalue tests)
---

A pair $(A, B)$ is stabilizable when some state feedback $u = -K x$ makes the closed loop matrix $A - BK$ [Hurwitz](/hurwitz-matrix/). It is weaker than [controllability](/controllability/): the input does not have to reach every mode, but each mode that it cannot reach must be asymptotically stable by itself. Stabilizability is the property that design methods such as [infinite-horizon LQR](/infinite-horizon-lqr/) need, and its dual for the output is [detectability](/detectability/).

## Definition

**Notation.** $\dot x = A x + B u$ with $A \in \mathbb{R}^{n \times n}$ and $B \in \mathbb{R}^{n \times m}$. A matrix is Hurwitz if all its eigenvalues have negative real part.

**Definition.** $(A, B)$ is *stabilizable* if there is a $K \in \mathbb{R}^{m \times n}$ such that $A - BK$ is Hurwitz.

**Equivalent tests.** The following are equivalent.

1. $(A, B)$ is stabilizable.
2. In a [Kalman decomposition](/kalman-decomposition/) for the input, $T A T^{-1} = \begin{bmatrix} A_{11} & A_{12} \\ 0 & A_{22} \end{bmatrix}$ and $T B = \begin{bmatrix} B_1 \\ 0 \end{bmatrix}$ with $(A_{11}, B_1)$ controllable, the block $A_{22}$ is Hurwitz.
3. $\operatorname{rank} [A - \lambda I, B] = n$ for every complex $\lambda$ with $\operatorname{Re} \lambda \ge 0$ (Hautus 1970). Only the eigenvalues of $A$ in the closed right half plane need checking.
4. No left eigenvector $w$ of $A$ ($w^* A = \lambda w^*$, $w \ne 0$) with $\operatorname{Re} \lambda \ge 0$ has $w^* B = 0$.

*Proof.* 1 and 2: write $\bar K = K T^{-1} = [K_1, K_2]$. Then $T (A - BK) T^{-1}$ is block upper triangular:

$$T (A - BK) T^{-1} = \begin{bmatrix} A_{11} - B_1 K_1 & A_{12} - B_1 K_2 \\ 0 & A_{22} \end{bmatrix}.$$

So the eigenvalues of $A - BK$ are those of $A_{11} - B_1 K_1$ together with those of $A_{22}$, and $A_{22}$ does not depend on $K$. If $A - BK$ is Hurwitz, so is $A_{22}$. If $A_{22}$ is Hurwitz, the [pole placement theorem](/pole-placement-theorem/) gives $K_1$ with $A_{11} - B_1 K_1$ Hurwitz, because $(A_{11}, B_1)$ is controllable (Wonham 1967 for $m > 1$); take $K_2 = 0$. 2 and 3: the rank of $[A - \lambda I, B]$ drops below $n$ exactly when $\lambda$ is an eigenvalue of $A_{22}$, as the [Popov-Belevitch-Hautus test](/popov-belevitch-hautus-test/) page shows. 3 and 4: the rank drops at $\lambda$ exactly when some $w \ne 0$ has $w^* [A - \lambda I, B] = 0$. $\blacksquare$

The eigenvalues of $A_{22}$ are the *uncontrollable eigenvalues*. They are fixed: they are eigenvalues of $A - BK$ for every $K$. So stabilizability asks that every fixed eigenvalue already lies in the open left half plane.

**Discrete time.** For $x_{k+1} = A x_k + B u_k$, the pair is stabilizable if $A - BK$ is Schur for some $K$, that is, all eigenvalues have modulus less than 1. The tests are the same with "$\operatorname{Re} \lambda \ge 0$" replaced by "$|\lambda| \ge 1$". Every controllable pair is stabilizable, and in discrete time a pair that is controllable to the origin is stabilizable too, since the eigenvalues that the input cannot move are then $0$.

**Where it is needed.** The [stabilizing Riccati solution theorem](/stabilizing-riccati-solution-theorem/): if $(A, B)$ is stabilizable and $(Q^{1/2}, A)$ is detectable, the algebraic Riccati equation has exactly one stabilizing solution, and the LQR gain makes the closed loop Hurwitz. Without stabilizability no gain can do that. With output feedback, a plant $\dot x = A x + B u$, $y = C x$ can be made asymptotically stable by a dynamic controller if and only if $(A, B)$ is stabilizable and $(C, A)$ is detectable. The [separation principle](/separation-principle/) gives such a controller: an observer and the state feedback $u = -K \hat x$.

## Examples and non-examples

- **An unreachable mode that decays.** $A = \operatorname{diag}(1, -2)$, $B = (1, 0)^T$. The pair is not controllable, because $x_2$ obeys $\dot x_2 = -2 x_2$ for every input. It is stabilizable: $K = [2, 0]$ gives $A - BK = \operatorname{diag}(-1, -2)$. The PBH test at the only eigenvalue with $\operatorname{Re} \lambda \ge 0$, $\lambda = 1$, gives $[A - I, B] = \begin{bmatrix} 0 & 0 & 1 \\ 0 & -3 & 0 \end{bmatrix}$, rank 2.
- **An unreachable mode that grows (non-example).** $A = \operatorname{diag}(-1, 2)$, $B = (1, 0)^T$. Now $x_2 = e^{2t} x_2(0)$ for every input, and the eigenvalue $2$ stays in $A - BK$ for every $K$. At $\lambda = 2$, $[A - 2I, B] = \begin{bmatrix} -3 & 0 & 1 \\ 0 & 0 & 0 \end{bmatrix}$ has rank 1.
- **An unreachable mode on the imaginary axis (non-example).** $A = \begin{bmatrix} 0 & 1 \\ -1 & 0 \end{bmatrix}$, $B = 0$. The eigenvalues $\pm i$ are fixed, and the oscillation never decays. The test counts $\operatorname{Re} \lambda = 0$ as bad for this reason.
- **Controllable implies stabilizable.** The double integrator $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $B = (0, 1)^T$ with $K = [1, 2]$ gives $A - BK = \begin{bmatrix} 0 & 1 \\ -1 & -2 \end{bmatrix}$, with characteristic polynomial $s^2 + 2s + 1$ and both eigenvalues at $-1$.
- **No input at all.** If $A$ is Hurwitz, $(A, 0)$ is stabilizable with $K = 0$, although nothing is controllable.

## Related definitions

- [Controllability](/controllability/): the stronger property, in which every eigenvalue of $A - BK$ can be placed.
- [Detectability](/detectability/): the dual property. $(C, A)$ is detectable if and only if $(A^T, C^T)$ is stabilizable.
- [Popov-Belevitch-Hautus test](/popov-belevitch-hautus-test/): the eigenvalue test, of which test 3 is the restriction to the closed right half plane.
- [Kalman decomposition](/kalman-decomposition/): the coordinates that show the uncontrollable block $A_{22}$.
- [State feedback](/state-feedback/) and [pole placement theorem](/pole-placement-theorem/): how the gain $K$ is found for the controllable part.
- [Stabilizing Riccati solution theorem](/stabilizing-riccati-solution-theorem/): the main place where stabilizability is an assumption.

## References
