---
tag: 63Y5ZR
kind: theorem
slug: separation-principle
name: Separation principle
aliases:
- separation theorem for observers
area: control/state-space-control
level: core
summary: The eigenvalues of an observer-based controller loop are those of A - BK together with those of A - LC, so the two can be designed apart.
history:
  year: 1966
  people: [David G. Luenberger]
  note: "Luenberger introduced observers in 1964 and treated observers for multivariable systems and their use in feedback in 1966."
prereqs: [state-feedback, state-observer, pole-placement-theorem]
see_also: [luenberger-observer, state-feedback, lqg-control, lqg-guaranteed-margins-counterexample, loop-transfer-recovery, high-gain-observer, kalman-bucy-filter, reduced-order-observer]
sources:
  - paper: doi:10.1109/tac.1966.1098323
    title: David G. Luenberger, Observers for multivariable systems, IEEE Transactions on Automatic Control 11(2), 190-197, 1966
    locator: the use of observers in feedback control and the eigenvalues of the combined system
  - paper: doi:10.1109/tac.1978.1101812
    title: John C. Doyle, Guaranteed margins for LQG regulators, IEEE Transactions on Automatic Control 23(4), 756-757, 1978
    locator: the example of an LQG loop with arbitrarily small gain margin
  - paper: doi:10.1109/9.788534
    title: Ahmed N. Atassi and Hassan K. Khalil, A separation principle for the stabilization of a class of nonlinear systems, IEEE Transactions on Automatic Control 44(9), 1672-1687, 1999
    locator: the semiglobal separation result with a saturated state feedback and a high-gain observer
  - book: isbn:9780195117776
    title: Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999
    locator: Section 8.5 (feedback from estimated states) and Section 8.8 (the multivariable case)
  - book: isbn:9780691193984
    title: Karl J. Åström and Richard M. Murray, Feedback Systems, An Introduction for Scientists and Engineers, second edition, Princeton University Press, 2021
    locator: Chapter 8, Output Feedback (the section Control Using Estimated State)
---

The separation principle says that a linear state feedback and a linear observer can be designed apart and then joined. If the feedback $u = -Kx$ is replaced by $u = -K\hat x$, where $\hat x$ comes from a [Luenberger observer](/luenberger-observer/), the closed-loop eigenvalues are exactly the eigenvalues of $A - BK$ together with those of $A - LC$. The theorem is about eigenvalues only. It says nothing about robustness: the joined loop can have much smaller stability margins than the full [state feedback](/state-feedback/) loop, and LQG controllers have no guaranteed margins at all. For nonlinear systems only weaker, semiglobal versions hold.

## Statement

**Theorem.** Let $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$, $C \in \mathbb{R}^{p \times n}$, $K \in \mathbb{R}^{m \times n}$, $L \in \mathbb{R}^{n \times p}$ and $N \in \mathbb{R}^{m \times q}$. Consider the plant $\dot x = Ax + Bu$, $y = Cx$, with the observer and the control law

$$\dot{\hat x} = A\hat x + Bu + L(y - C\hat x), \qquad u = -K\hat x + Nr.$$

Then:

1. The closed loop, with state $(x, \hat x) \in \mathbb{R}^{2n}$, has the characteristic polynomial $\det(sI - A + BK)\,\det(sI - A + LC)$.
2. It is asymptotically stable if and only if $A - BK$ and $A - LC$ are both Hurwitz.
3. The transfer function from $r$ to $y$ is $C(sI - A + BK)^{-1}BN$, the same as with $u = -Kx + Nr$.

If $(A, B)$ is controllable and $(C, A)$ is observable, all $2n$ eigenvalues can be chosen freely, in conjugate pairs. The same statements hold in discrete time, with Schur stability in place of Hurwitz stability, for the observer $\hat x_{k+1} = \Phi\hat x_k + \Gamma u_k + L(y_k - C\hat x_k)$. For a [reduced-order observer](/reduced-order-observer/) with error matrix $F$, the eigenvalues are those of $A - BK$ and those of $F$.

## In plain words

A controller that needs the full state can work with an estimate of the state instead. The estimate comes from an observer, which runs a copy of the model and corrects it with the measured output. The theorem says that this joint loop behaves, as far as its natural modes go, like the controller alone plus the observer alone. So the designer can choose the controller as if the state were measured, choose the observer to be fast enough, and put them together. The theorem does not promise that the joint loop is as tolerant of model errors as the controller alone. Often it is much less tolerant.

## Proof

Let $e = x - \hat x$. Then

$$\dot e = Ax + Bu - A\hat x - Bu - LC(x - \hat x) = (A - LC)e,$$

for every input $u$, and $u = -K\hat x + Nr = -Kx + Ke + Nr$. So in the coordinates $(x, e)$, obtained from $(x, \hat x)$ by the invertible map $\begin{bmatrix} I & 0 \\ I & -I \end{bmatrix}$,

$$\frac{d}{dt}\begin{bmatrix} x \\ e \end{bmatrix} = \begin{bmatrix} A - BK & BK \\ 0 & A - LC \end{bmatrix}\begin{bmatrix} x \\ e \end{bmatrix} + \begin{bmatrix} BN \\ 0 \end{bmatrix} r, \qquad y = \begin{bmatrix} C & 0 \end{bmatrix}\begin{bmatrix} x \\ e \end{bmatrix}.$$

A change of coordinates does not change the eigenvalues, and the determinant of a block triangular matrix is the product of the determinants of its diagonal blocks. This gives item 1, and item 2 follows. For item 3, $e$ is not driven by $r$, so with zero initial state $e \equiv 0$, and $x$ then satisfies $\dot x = (A - BK)x + BNr$. Equivalently, the modes of $A - LC$ are uncontrollable from $r$ and cancel in the transfer function. The last claim follows from the [pole placement theorem](/pole-placement-theorem/) for $(A, B)$ and for the dual pair $(A^T, C^T)$. In discrete time the same computation holds with $k + 1$ in place of the derivative. For a reduced-order observer, the error $e$ of the estimated part satisfies $\dot e = Fe$, and the same block triangular argument applies. $\square$

## Consequences

- **The controller as one transfer function.** With $r = 0$ the controller is $\dot{\hat x} = (A - BK - LC)\hat x + Ly$, $u = -K\hat x$, so $u = -K(sI - A + BK + LC)^{-1}L\,y$. Its poles are the eigenvalues of $A - BK - LC$, which the theorem does not control. A stable closed loop can contain an unstable controller.
- **Example.** For the double integrator $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, $C = [1, 0]$, take $K = [2, 2]$ (eigenvalues $-1 \pm i$) and $L = [5, 6]^T$ (eigenvalues $-2$ and $-3$). The controller is $u = -\dfrac{22s + 12}{s^2 + 7s + 18}\,y$. The closed-loop polynomial is $s^2(s^2 + 7s + 18) + 22s + 12 = s^4 + 7s^3 + 18s^2 + 22s + 12$, which equals $(s^2 + 2s + 2)(s^2 + 5s + 6)$, as the theorem says.
- **Certainty equivalence in LQG.** In [LQG control](/lqg-control/) the optimal controller uses the LQR gain on the Kalman filter estimate. That is a stochastic separation result about optimality. The eigenvalue statement on this page is a deterministic fact about any $K$ and $L$.
- **Rule of thumb, not part of the theorem.** A common choice is to make the observer eigenvalues two to five times faster than those of $A - BK$, so that the estimate converges before the controller acts on it. Faster observers amplify measurement noise.
- **Robustness is not separated.** The margins of the loop are not those of the state feedback. In the example above, the full state feedback $u = -Kx$ has the loop transfer function $(2s + 2)/s^2$ at the plant input. A gain $k$ there gives $s^2 + 2ks + 2k$, which is Hurwitz for every $k > 0$: the upper gain margin is infinite. With the observer, a gain $k$ at the plant input gives $s^4 + 7s^3 + 18s^2 + 22ks + 12k$. The Routh test shows that it is Hurwitz exactly for $0 < k < 546/121 \approx 4.51$. Doyle (1978) showed that for LQG controllers no margin is guaranteed at all; see the [LQG margins counterexample](/lqg-guaranteed-margins-counterexample/). [Loop transfer recovery](/loop-transfer-recovery/) is one way to regain the margins of the state feedback, for minimum-phase square plants.

## Tightness

- **The observer must use the true model.** If the observer uses $(A_m, B_m, C_m)$ different from the plant, the $e$ equation picks up terms in $x$ and $u$, the matrix is no longer block triangular, and the eigenvalues are not the union. The gain $k$ in the example above is such a model error. At $k = 2$ the closed-loop eigenvalues are about $-4.96$, $-0.69$ and $-0.67 \pm 2.55i$, not $-1 \pm i$, $-2$ and $-3$.
- **The same input must drive both.** If the input that reaches the plant differs from the one the observer uses, for example because of saturation, the error equation gets the extra term $B(u_{\text{plant}} - u)$.
- **Nonlinear systems.** For $\dot x = f(x, u)$, a globally stabilizing state feedback and a globally convergent observer do not in general give a globally stable loop: the state can escape to infinity in finite time before the estimate has converged. Atassi and Khalil (1999) proved a separation principle for a class of nonlinear systems with a saturated state feedback and a [high-gain observer](/high-gain-observer/). It is semiglobal: for every compact set of initial states, a fast enough observer recovers the stability and the trajectories of the state feedback.

## History

Luenberger (1964) introduced observers that reconstruct the state of a linear system from its input and output. In 1966 he treated observers for systems with several outputs and their use in feedback control, where the eigenvalues of the controller and of the observer separate. The stochastic counterpart, certainty equivalence in the linear quadratic Gaussian problem, was developed in the same period. Doyle (1978) showed with a two-state example that the LQG controller, which joins two designs with good margins, can have arbitrarily small gain margins. Atassi and Khalil (1999) gave a separation principle for nonlinear systems with high-gain observers.

## References
