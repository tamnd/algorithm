---
tag: BVKR9K
kind: problem
slug: h2-optimal-control
name: H2 optimal control
aliases:
- H2 synthesis
area: control/optimal-and-predictive-control
level: advanced
summary: Find a stabilizing controller that minimizes the H2 norm of the closed loop from disturbance to error, which reduces to LQG.
model: real-ram
prereqs: [h2-norm, linear-fractional-transformation, stabilizability, continuous-algebraic-riccati-equation, lqg-control]
see_also: [h-infinity-control-problem, dgkf-h-infinity-synthesis, kalman-bucy-filter, infinite-horizon-lqr, separation-principle, loop-transfer-recovery, lyapunov-equation, mixed-sensitivity-design]
sources:
  - paper: doi:10.1109/9.29425
    title: John C. Doyle, Keith Glover, Pramod P. Khargonekar and Bruce A. Francis, State-space solutions to standard H2 and H-infinity control problems, IEEE Transactions on Automatic Control 34(8), 831-847, 1989
    locator: the standard H2 problem, its assumptions, and its solution by two Riccati equations
  - book: isbn:0134565673
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: the chapter on H2 optimal control, with the standard assumptions, the optimal controller and the optimal cost
  - paper: doi:10.1109/TAC.1971.1099818
    title: Michael Athans, The role and use of the stochastic linear-quadratic-Gaussian problem in control system design, IEEE Transactions on Automatic Control 16(6), 529-552, 1971
    locator: the stochastic LQG problem that the H2 problem restates in terms of a transfer matrix
---

The H2 optimal control problem asks for an internally stabilizing controller that makes the [H2 norm](/h2-norm/) of the closed loop from the disturbance $w$ to the error $z$ as small as possible. The plant is a generalized plant with the inputs $w$ and $u$ and the outputs $z$ and $y$, and the controller closes the loop from $y$ to $u$. Under the standard assumptions the problem has a unique optimal controller of the same order as the plant, given by two independent Riccati equations. This controller is the [LQG](/lqg-control/) controller for the matching noise and cost data. The two problems are not the same problem: H2 is a deterministic problem about the norm of a transfer matrix, and LQG is a stochastic problem about the expected cost under white noise. They have the same solution under the standard assumptions.

## In plain words

Disturbances push a machine around, and some signals of the machine should stay small. Hit the machine with a short sharp blow in each disturbance direction, one at a time, and measure the total energy of the error signals that follow. The H2 norm adds up these energies. The H2 problem asks for the controller that makes this sum as small as possible, while the loop stays stable. The same number also measures the average size of the errors when the disturbances are random noise. That is why the answer is the best controller for random noise, which is the LQG controller: a state estimator followed by the best state feedback. The answer is good on average but gives no worst case guarantee.

## Definition

**Input.** A generalized plant with state $x \in \mathbb{R}^n$:

$$\dot x = A x + B_1 w + B_2 u, \qquad z = C_1 x + D_{12} u, \qquad y = C_2 x + D_{21} w,$$

with $w \in \mathbb{R}^{m_1}$, $u \in \mathbb{R}^{m_2}$, $z \in \mathbb{R}^{p_1}$ and $y \in \mathbb{R}^{p_2}$. There is no direct term from $w$ to $z$ ($D_{11} = 0$), since the H2 norm of the closed loop is finite only when it is strictly proper. A term $D_{22}$ from $u$ to $y$ can be moved into the controller and is taken as 0.

**Controllers.** A controller is a finite-dimensional linear time-invariant system $K$ with $u = K y$, such that the closed loop is internally stable, that is, the closed-loop $A$ matrix is Hurwitz. Such a controller exists if and only if $(A, B_2)$ is [stabilizable](/stabilizability/) and $(C_2, A)$ is [detectable](/detectability/). The closed loop from $w$ to $z$ is the lower [linear fractional transformation](/linear-fractional-transformation/) $T_{zw} = \mathcal{F}_l(P, K)$.

**Question.** Find

$$\min_K \|T_{zw}\|_2, \qquad \|T\|_2^2 = \frac{1}{2\pi} \int_{-\infty}^{\infty} \mathrm{tr}\left(T(j\omega)^* T(j\omega)\right) d\omega,$$

over all internally stabilizing $K$ for which $T_{zw}$ is strictly proper, and a controller that reaches it.

**Standard assumptions.** (A1) $(A, B_2)$ stabilizable and $(C_2, A)$ detectable. (A2) $D_{12}$ has full column rank and $D_{21}$ has full row rank. (A3) $\begin{bmatrix} A - j\omega I & B_2 \\ C_1 & D_{12} \end{bmatrix}$ has full column rank and $\begin{bmatrix} A - j\omega I & B_1 \\ C_2 & D_{21} \end{bmatrix}$ has full row rank for every real $\omega$. After a change of the input and output coordinates one can also take $D_{12}^T \begin{bmatrix} C_1 & D_{12} \end{bmatrix} = \begin{bmatrix} 0 & I \end{bmatrix}$ and $\begin{bmatrix} B_1 \\ D_{21} \end{bmatrix} D_{21}^T = \begin{bmatrix} 0 \\ I \end{bmatrix}$.

**Solution under the assumptions.** Let $X_2 \ge 0$ be the stabilizing solution of $A^T X + X A - X B_2 B_2^T X + C_1^T C_1 = 0$ and $Y_2 \ge 0$ the stabilizing solution of $A Y + Y A^T - Y C_2^T C_2 Y + B_1 B_1^T = 0$, and put $F_2 = -B_2^T X_2$ and $L_2 = -Y_2 C_2^T$. The unique optimal controller is

$$\dot{\hat x} = (A + B_2 F_2 + L_2 C_2) \hat x - L_2 y, \qquad u = F_2 \hat x,$$

and the optimal value is

$$\min_K \|T_{zw}\|_2^2 = \mathrm{tr}(B_1^T X_2 B_1) + \mathrm{tr}(F_2 Y_2 F_2^T) = \mathrm{tr}(C_1 Y_2 C_1^T) + \mathrm{tr}(L_2^T X_2 L_2).$$

**H2 and LQG.** Take the LQG data $(A, B, C, Q, R, W, V)$ and set $B_1 = \begin{bmatrix} W^{1/2} & 0 \end{bmatrix}$, $D_{21} = \begin{bmatrix} 0 & V^{1/2} \end{bmatrix}$, $C_1 = \begin{bmatrix} Q^{1/2} \\ 0 \end{bmatrix}$, $D_{12} = \begin{bmatrix} 0 \\ R^{1/2} \end{bmatrix}$. If $w$ is white noise with unit intensity, the stationary value of $\mathbb{E}\, z^T z$ in the closed loop is $\|T_{zw}\|_2^2$, and it equals the LQG cost $J$. So minimizing one minimizes the other, and $F_2 = -K$ and $L_2 = -L_o$ in the notation of the LQG page. The differences are these:

- *The question.* LQG minimizes an expected average cost of a stochastic system. H2 minimizes a norm of a transfer matrix. The H2 norm also has a deterministic meaning: its square is the sum of the energies of $z$ after unit impulses in each channel of $w$.
- *The controllers allowed.* LQG allows any causal map from past outputs to inputs, also nonlinear and time varying. H2 allows only linear time-invariant controllers. Under the Gaussian assumptions the restriction costs nothing.
- *The data.* The H2 problem is stated for any generalized plant. Frequency weights on $w$ and $z$, cross terms such as $D_{12}^T C_1 \ne 0$, and errors that are not of the form $x^T Q x + u^T R u$ fit into it directly, and the noise need not be physical.

## Variants

- **State feedback.** If $y = x$, the optimal controller is the static gain $u = F_2 x$, which is [LQR](/infinite-horizon-lqr/) with $Q = C_1^T C_1$ and $R = D_{12}^T D_{12}$, and the optimal value is $\mathrm{tr}(B_1^T X_2 B_1)$.
- **Output estimation.** If the error is $z = C_1 x - \hat z$ with an estimate as the input, the problem is optimal filtering, and the answer is the steady state [Kalman-Bucy filter](/kalman-bucy-filter/).
- **Discrete time.** The same problem with the H2 norm on the unit circle. The two Riccati equations are [discrete algebraic Riccati equations](/discrete-algebraic-riccati-equation/).
- **Singular problems.** If $D_{12}$ or $D_{21}$ loses rank, or (A3) fails, the infimum may not be reached, as in cheap control.
- **Mixed H2 and H-infinity.** Minimize the H2 norm of one channel subject to an [H-infinity](/h-infinity-control-problem/) bound on another. There is no closed form; LMI methods give an upper bound.
- **Fixed order or structure.** A controller of order below $n$, or decentralized, makes the problem nonconvex.

## Examples

**A scalar plant.** $\dot x = x + w_1 + u$, $z = (x, u)$, $y = x + w_2$. So $A = 1$, $B_1 = [1, 0]$, $B_2 = 1$, $C_1 = [1; 0]$, $D_{12} = [0; 1]$, $C_2 = 1$ and $D_{21} = [0, 1]$, and the assumptions hold in the normalized form. Both Riccati equations are $2X - X^2 + 1 = 0$, so $X_2 = Y_2 = 1 + \sqrt2$ and $F_2 = L_2 = -(1 + \sqrt2)$. The optimal value is

$$\|T_{zw}\|_2^2 = (1 + \sqrt2) + (1 + \sqrt2)^3 = 8 + 6\sqrt2 \approx 16.485, \qquad \|T_{zw}\|_2 \approx 4.060.$$

The controller is $u = K(s) y$ with $K(s) = -(3 + 2\sqrt2)/(s + 1 + 2\sqrt2)$, and the closed loop has a double eigenvalue at $-\sqrt2$. The [H-infinity problem](/h-infinity-control-problem/) for the same plant has $\gamma_{\rm opt} = 1 + \sqrt3 \approx 2.732$. The H2 optimal controller gives $\|T_{zw}\|_\infty \approx 5.371$, reached at $\omega = 0$: the best average is not the best worst case.

**The double integrator.** With $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $B_2 = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, $C_2 = \begin{bmatrix} 1 & 0 \end{bmatrix}$ and the LQG data $Q = I$, $R = 1$, $W = I$, $V = 1$, the optimum is $\|T_{zw}\|_2^2 = 8\sqrt3 \approx 13.856$, so $\|T_{zw}\|_2 \approx 3.722$. This is the cost $J^*$ on the [LQG page](/lqg-control/), with the controller $(2\sqrt3\, s + 1)/(s^2 + 2\sqrt3\, s + 5)$ from $y$ to $-u$.

**Not well posed.** If $D_{11} \ne 0$, every closed loop has a direct term from $w$ to $z$, and its H2 norm is infinite for every controller. If the plant has an unstable mode that $B_2$ cannot reach, no controller makes the closed loop Hurwitz.

## Known algorithms

- **Two Riccati equations** (Doyle, Glover, Khargonekar and Francis 1989): solve the two CAREs above by any method for the stabilizing solution, such as the [Schur method](/schur-method-riccati/), the matrix sign function or [Kleinman's iteration](/kleinman-iteration/), and form the controller. See [LQG control](/lqg-control/) for an implementation.
- **LMI formulation.** The H2 norm bound can be written as linear matrix inequalities in the closed-loop Lyapunov matrix, and after a change of variables the full order problem becomes a semidefinite program. This form handles the mixed H2 and H-infinity problem.
- **Frequency domain methods.** With the Youla parametrization the problem becomes a model matching problem in $RH_2$, solved by spectral factorization (the Wiener-Hopf approach). This was the form used before the state-space solution.
- **Local optimization.** For fixed order or fixed structure, gradient methods on the controller parameters, with the closed-loop Gramian from a [Lyapunov equation](/lyapunov-equation/) giving the cost and its gradient.

## Bounds

- **Order.** Under the standard assumptions the optimal controller is unique and has order $n$. A controller of higher order cannot do better (theorem).
- **Lower bounds.** The first term of each form of the optimal value is a bound: $\|T_{zw}\|_2^2 \ge \mathrm{tr}(B_1^T X_2 B_1)$, the value with the full state measured, and $\|T_{zw}\|_2^2 \ge \mathrm{tr}(C_1 Y_2 C_1^T)$, the value when the error only needs to be estimated. In the scalar example both are $1 + \sqrt2$, against the optimum $8 + 6\sqrt2$.
- **Cost.** In the real-RAM model, two Riccati solutions with a Schur-based solver cost $O(n^3)$ flops each, iterative only through the eigenvalue algorithm, and the controller formulas cost $O(n^2 (m_2 + p_2))$.
- **Structured forms.** With $B_1 = 0$ and $C_1 = 0$, every stabilizing controller gives $T_{zw} = 0$, so the problem with a fixed controller structure contains structured stabilization problems, some of which are [NP-hard](/np-hard/).

## Reductions

- **To LQG and back.** The H2 problem with white noise $w$ is the LQG problem for the noise intensities $B_1 B_1^T$ and $D_{21} D_{21}^T$ and the weights $C_1^T C_1$ and $D_{12}^T D_{12}$; under the normalization the cross terms vanish.
- **Separation.** The solution splits into a full information problem (one CARE, gain $F_2$) and an output estimation problem (one filter ARE, gain $L_2$), as in the [separation principle](/separation-principle/).
- **From H-infinity.** As $\gamma \to \infty$, the central controller of the [two-Riccati H-infinity synthesis](/dgkf-h-infinity-synthesis/) tends to the H2 optimal controller.
- **To model matching.** With the Youla parametrization, $T_{zw} = T_1 - T_2 Q T_3$ with $Q \in RH_\infty$ free, and the problem is $\min_Q \|T_1 - T_2 Q T_3\|_2$, a convex problem in $Q$.

## Applications

- LQG design, stated with a generalized plant that carries frequency weights on the noise and the errors.
- Disturbance rejection where the disturbance is broadband and the average error matters more than the worst case.
- Optimal estimation (the Kalman-Bucy filter is the H2 optimal estimator).
- [Loop transfer recovery](/loop-transfer-recovery/), which Stein and Athans (1987) read as a weighted H2 trade-off.
- The H2 part of mixed H2 and H-infinity designs.

## References
