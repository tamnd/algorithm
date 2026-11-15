---
tag: 01XZZ5
kind: technique
slug: state-feedback
name: State feedback
aliases:
- full-state feedback
- state-variable feedback
area: control/state-space-control
level: intro
summary: Sets the input to u = -Kx + N r, a linear function of the measured state and the reference, which moves the closed-loop eigenvalues to those of A - BK.
prereqs: [state-space-representation, controllability]
see_also: [pole-placement-problem, pole-placement-theorem, ackermann-formula, integral-state-feedback, luenberger-observer, separation-principle, infinite-horizon-lqr, stabilizability]
sources:
  - book: isbn:9780691193984
    title: Karl J. Åström and Richard M. Murray, Feedback Systems, An Introduction for Scientists and Engineers, second edition, Princeton University Press, 2021
    locator: Chapter 7, State Feedback (the sections Stabilization by State Feedback and State Feedback Design)
  - book: isbn:9780195117776
    title: Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999
    locator: Section 8.2 (state feedback), Section 8.3 (regulation and tracking) and Section 8.6 (the multivariable case and the effect on transfer matrices)
  - book: isbn:9780134685717
    title: Gene F. Franklin, J. David Powell and Abbas Emami-Naeini, Feedback Control of Dynamic Systems, eighth edition, Pearson, 2019
    locator: Chapter 7, State-Space Design
  - paper: doi:10.1109/TAC.1967.1098739
    title: W. M. Wonham, On pole assignment in multi-input controllable linear systems, IEEE Transactions on Automatic Control 12(6), 660-665, 1967
    locator: the result that state feedback can assign every closed-loop spectrum if and only if the pair is controllable
---

State feedback is the basic design technique of state-space control. The plant is $\dot x = Ax + Bu$, $y = Cx$, with $x \in \mathbb{R}^n$, $u \in \mathbb{R}^m$, and the whole state is measured. The control law is

$$u = -Kx + Nr,$$

with a gain $K \in \mathbb{R}^{m \times n}$, a reference $r$ and a feedforward gain $N$. The closed loop is $\dot x = (A - BK)x + BNr$. Its dynamics are set by the eigenvalues of $A - BK$, and the designer chooses $K$ to put them where they should be. In discrete time the plant is $x_{k+1} = \Phi x_k + \Gamma u_k$ with sampling period $h$, and the closed-loop matrix is $\Phi - \Gamma K$. Its eigenvalues must lie inside the unit circle (a Schur matrix) instead of in the open left half plane (a [Hurwitz matrix](/hurwitz-matrix/)).

## In plain words

A controller that sees the whole state of a machine, such as both the position and the speed of a cart, can react to each part with its own weight. The input is a weighted sum of the measured state values. With the right weights, the machine settles as fast and as smoothly as the designer wants, at least on paper. The weights cannot move behavior that the input cannot reach. In practice the full state is rarely measured, so an observer often gives an estimate in its place.

## When it applies

- **Linear time-invariant model.** The design uses $A$ and $B$. For a nonlinear plant, use the linearization at an operating point; the result then holds only near that point.
- **The state is available.** Every state variable is measured, or an observer such as the [Luenberger observer](/luenberger-observer/) estimates it. The [separation principle](/separation-principle/) says that the eigenvalues of the combined loop are those of $A - BK$ and those of the observer.
- **Controllability.** If $(A, B)$ is [controllable](/controllability/), every set of $n$ eigenvalues that is closed under complex conjugation is the spectrum of $A - BK$ for some real $K$. This is the [pole placement theorem](/pole-placement-theorem/). If $(A, B)$ is only [stabilizable](/stabilizability/), the uncontrollable eigenvalues are stable but stay where they are. Otherwise no state feedback gives an asymptotically stable loop.

## The template

1. Write the model $\dot x = Ax + Bu$, $y = Cx$, and check that $(A, B)$ is controllable, for example with the [Kalman rank condition](/kalman-rank-condition/).
2. Choose the closed-loop behavior. Either choose $n$ eigenvalues from specifications such as the settling time and the damping (see [step response specifications](/step-response-specifications/)), or choose weights $Q$ and $R$ of a quadratic cost.
3. Compute $K$. For chosen eigenvalues this is the [pole placement problem](/pole-placement-problem/): use [Ackermann's formula](/ackermann-formula/) for one input and small $n$, or [robust pole placement](/robust-pole-placement/) for several inputs or larger $n$. For a quadratic cost, use the [infinite-horizon LQR](/infinite-horizon-lqr/).
4. Choose $N$ so that the static gain from $r$ to $y$ is 1. For one input and one output, with $A - BK$ Hurwitz,

$$N = \frac{1}{C(BK - A)^{-1}B}.$$

The denominator is the static gain of the loop without $N$. It is 0 exactly when the plant has a zero at $s = 0$, and then no $N$ exists.

5. Check the result in simulation: the size of $u$ against the actuator limits, the effect of noise, and the effect of model error. If $r$ is constant but the model is not exact, $N$ does not remove the steady-state error. Add [integral action](/integral-state-feedback/) for that.

## Classic examples

**Double integrator.** $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, $C = [1, 0]$, a mass with position and speed. With $K = [k_1, k_2]$,

$$A - BK = \begin{bmatrix} 0 & 1 \\ -k_1 & -k_2 \end{bmatrix}, \qquad \det(sI - A + BK) = s^2 + k_2 s + k_1.$$

For the eigenvalues $-1 \pm i$ the wanted polynomial is $s^2 + 2s + 2$, so $K = [2, 2]$. Then $(A - BK)^{-1}B = [-1/2, 0]^T$, the static gain without $N$ is $1/2$, and $N = 2$. The law $u = -2x_1 - 2x_2 + 2r$ is a PD controller on the position error $r - x_1$.

**A stable plant made faster.** $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, with eigenvalues $-1$ and $-2$. The closed loop has $\det(sI - A + BK) = s^2 + (3 + k_2)s + (2 + k_1)$. For the eigenvalues $-4$ and $-5$, the polynomial is $s^2 + 9s + 20$, so $K = [18, 6]$.

**LQR as a check.** For the double integrator with $Q = I$ and $R = 1$, the algebraic Riccati equation has the solution $P = \begin{bmatrix} \sqrt 3 & 1 \\ 1 & \sqrt 3 \end{bmatrix}$, so $K = B^T P = [1, \sqrt 3]$. The closed loop has $s^2 + \sqrt 3\, s + 1$, with damping ratio $\sqrt 3/2$. The gain comes from a cost, not from a list of eigenvalues, but it is still a state feedback.

**A mode that does not move.** $A = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$. Here $A - BK = \begin{bmatrix} 1 & 0 \\ -k_1 & -1 - k_2 \end{bmatrix}$ has the eigenvalue 1 for every $K$. The pair is not stabilizable, and no state feedback gives an asymptotically stable loop. If the first diagonal entry is $-1$ instead, the pair is stabilizable but still not controllable: the eigenvalue $-1$ stays, and only the second one moves.

## Variations

- **Pole placement and LQR.** The two common ways to choose $K$; see above.
- **Discrete time.** The same template with $\Phi - \Gamma K$. Putting all eigenvalues at 0 gives [deadbeat control](/deadbeat-control/), which reaches the origin in at most $n$ steps.
- **Integral action.** Augment the state with the integral of the error, and design the feedback for the augmented system: [state feedback with integral action](/integral-state-feedback/).
- **Observer-based feedback.** Replace $x$ by an estimate $\hat x$ from an observer. The [separation principle](/separation-principle/) keeps the eigenvalues; the robustness can change a lot. With noise models this is [LQG control](/lqg-control/).
- **Static output feedback.** $u = -Ky$ uses only the outputs. Its eigenvalues cannot in general be placed freely, and the problem is much harder.
- **Two degrees of freedom.** $N r$ is the simplest feedforward. A [two-degree-of-freedom](/two-degree-of-freedom-control/) design shapes the reference response separately from the feedback.

## Pitfalls

- **Zeros do not move.** For one input and one output, the transfer function from $r$ to $y$ is $N\,b(s)/\alpha(s)$, where $b(s)$ is the numerator of $C(sI - A)^{-1}B$ and $\alpha(s) = \det(sI - A + BK)$. State feedback changes the poles and keeps the zeros. A zero near a slow pole or in the right half plane still shapes the response.
- **Fast poles cost input.** Eigenvalues far to the left need large gains. The input then saturates, and noise in the measured state is amplified. A rule of thumb: do not move a pole much further than needed, and look at the input in simulation.
- **N is not robust.** The feedforward gain depends on the model. A small error in $A$ or $B$ can give a steady-state error for a step in $r$, and a constant disturbance gives one too. Integral action removes it.
- **Uncontrollable modes.** No $K$ moves them. Check controllability first, and with a numerical rank test that is reliable; see the [Kalman decomposition](/kalman-decomposition/).
- **Eigenvalues are not robustness.** Two gains with the same eigenvalues can have very different sensitivity to model errors. With several inputs, use the freedom in $K$ as [robust pole placement](/robust-pole-placement/) does.

## Exercises

1. For the double integrator, find $K$ for the eigenvalues $-2$ and $-3$. (Answer: $s^2 + 5s + 6$, so $K = [6, 5]$ and $N = 6$.)
2. Show that for one input and one output the zeros of $C(sI - A + BK)^{-1}B$ are those of $C(sI - A)^{-1}B$. (Hint: write $B$ and $A - BK$ in [controllable canonical form](/controllable-canonical-form/); $K$ changes only the last row of the matrix.)
3. For $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$, $B = [0, 1]^T$, $C = [1, 0]$ and $K = [18, 6]$, compute $N$. (Answer: the static gain of $1/(s^2 + 9s + 20)$ is $1/20$, so $N = 20$.)
4. The plant $\dot x = x + u$ in discrete time with $h = 1$ has $\Phi = e$ and $\Gamma = e - 1$. Find the deadbeat gain. (Answer: $\Phi - \Gamma K = 0$, so $K = e/(e - 1)$.)

## References
