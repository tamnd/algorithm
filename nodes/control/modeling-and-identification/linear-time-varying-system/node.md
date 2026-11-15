---
tag: BP8R3V
kind: model
slug: linear-time-varying-system
name: Linear time-varying system
aliases:
- LTV system
area: control/modeling-and-identification
level: core
summary: A linear system x' = A(t)x + B(t)u whose matrices change with time, so its solution needs a state-transition matrix.
prereqs: [state-space-representation, matrix-exponential]
see_also: [state-transition-matrix, variation-of-constants-formula, lpv-system, gain-scheduling, switched-system, jacobian-linearization, exponential-stability, controllability-gramian]
sources:
  - book: isbn:9780134412054
    title: Wilson J. Rugh, Linear System Theory, second edition, Prentice Hall, 1996
    locator: Chapter 2, State Equation Representation; Chapter 3, State Equation Solution; Chapter 5, Two Important Cases (periodic systems); Chapter 6, Internal Stability; Chapter 8, Additional Stability Criteria (eigenvalue conditions and slowly varying systems)
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 4.6, Linear Time-Varying Systems and Linearization; Example 4.22
  - book: isbn:9780195117776
    title: Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999
    locator: Chapter 4 (solution of time-varying state equations) and Chapter 6 (controllability and observability of time-varying equations)
  - book: isbn:9780387984896
    title: Eduardo D. Sontag, Mathematical Control Theory, Deterministic Finite Dimensional Systems, second edition, Springer, 1998
    locator: the chapters on linear time-varying systems, their controllability and the gramian
---

A linear time-varying (LTV) system is a state model $\dot x = A(t) x + B(t) u$, $y = C(t) x + D(t) u$ whose matrices are known functions of time. It keeps linearity, so superposition holds and the solution has a closed form through the [state-transition matrix](/state-transition-matrix/) $\Phi(t, t_0)$, but it loses time invariance, so there is no transfer function and the eigenvalues of $A(t)$ at each time do not decide stability. The constant case is the linear time-invariant model of the [state-space representation](/state-space-representation/) page. An [LPV system](/lpv-system/) has the same form with matrices that depend on a parameter measured online, not on a time function known in advance.

## The machine

**Equations.** Time $t$ runs over an interval $J \subseteq \mathbb{R}$. The state is $x(t) \in \mathbb{R}^n$, the input $u(t) \in \mathbb{R}^m$ and the output $y(t) \in \mathbb{R}^p$, and

$$\dot x(t) = A(t) x(t) + B(t) u(t), \qquad y(t) = C(t) x(t) + D(t) u(t).$$

**Standing assumptions.** $A$, $B$, $C$ and $D$ are piecewise continuous on $J$, and the input is piecewise continuous (locally integrable is enough). Then for every $t_0 \in J$ and $x_0$ there is exactly one solution on all of $J$. Unlike a nonlinear system, an LTV system has no finite escape time: the right side is Lipschitz in $x$ with the constant $\|A(t)\|$, which is bounded on each compact subinterval, so the solution exists as long as the coefficients do (see [Lipschitz condition](/lipschitz-condition/) and the [Picard-Lindelöf theorem](/picard-lindelof-theorem/)).

**Solution.** With the state-transition matrix of $\dot x = A(t) x$, the [variation of constants formula](/variation-of-constants-formula/) gives

$$x(t) = \Phi(t, t_0) x_0 + \int_{t_0}^{t} \Phi(t, s) B(s) u(s)\, ds.$$

**Discrete time.** The model $x_{k+1} = A_k x_k + B_k u_k$, $y_k = C_k x_k + D_k u_k$, with $\Phi(k, j) = A_{k-1} \cdots A_j$. Here $\Phi(k, j)$ can be singular.

**Where LTV models come from.**

- *Linearization along a trajectory.* For $\dot x = f(x, u)$ with a nominal solution $(\bar x(t), \bar u(t))$, the deviations satisfy, to first order, an LTV system with $A(t) = \partial f / \partial x$ and $B(t) = \partial f / \partial u$ evaluated on the nominal solution. An equilibrium gives constant matrices, the LTI case of [linearization about an equilibrium](/jacobian-linearization/); a moving reference such as a launch trajectory or a robot path gives an LTV model.
- *Periodic coefficients.* Rotating machines, a pendulum with a moving support, and orbit dynamics give $A(t + T) = A(t)$.
- *Known schedules.* A changing mass (fuel use) or a time-varying gain set in advance.

**Example.** Let

$$\dot x_1 = -x_1 + e^{2t} x_2, \qquad \dot x_2 = -x_2.$$

Then $x_2(t) = e^{-t} x_2(0)$ and $x_1(t) = e^{-t} x_1(0) + \sinh(t)\, x_2(0)$. For $x(0) = (0, 1)$, $x_1(3) = \sinh 3 = 10.018$. The matrix $A(t) = \begin{bmatrix} -1 & e^{2t} \\ 0 & -1 \end{bmatrix}$ has the eigenvalues $-1, -1$ at every $t$, yet the solution grows like $e^t / 2$. The cause is the coupling term $e^{2t}$, which grows faster than the state decays.

## What it counts

The model predicts the state and the output trajectory for a given initial state and input. The input-output map with $x(t_0) = 0$ is

$$y(t) = \int_{t_0}^{t} G(t, s) u(s)\, ds + D(t) u(t), \qquad G(t, s) = C(t) \Phi(t, s) B(s) \text{ for } t \ge s.$$

The kernel $G(t, s)$ depends on both times, not only on $t - s$. So there is no convolution form, no single impulse response, and no transfer function: a sinusoidal input does not give a sinusoidal output at the same frequency. The analysis works directly with $\Phi$ and with integrals of it, such as gramians and Lyapunov functions $V(t, x) = x^T P(t) x$.

When the model is fitted to data, the fit minimizes a prediction error, as for LTI models, but with parameters that are functions of time. That needs more data or a parametrized form of $A(t)$, for example a polynomial or a periodic basis.

## Relation to other models

- **LTI.** The constant case. Then $\Phi(t, t_0) = e^{A(t - t_0)}$ ([matrix exponential](/matrix-exponential/)), and the results of [linear-time-invariant-system](/linear-time-invariant-system/) apply: transfer functions, eigenvalue tests, frequency response.
- **LPV.** In an [LPV system](/lpv-system/) the matrices are $A(\rho(t))$ for a scheduling parameter $\rho$ that is measured, not known in advance. Each fixed parameter trajectory gives an LTV system, and LPV analysis must hold for all admissible trajectories. [Gain scheduling](/gain-scheduling/) designs controllers for this class.
- **Switched linear systems.** A [switched system](/switched-system/) has $A(t) = A_{\sigma(t)}$ with a piecewise constant switching signal. For a fixed signal it is LTV with piecewise constant coefficients.
- **Nonlinear systems.** The linearization along a trajectory of a nonlinear system is LTV. Its exponential stability gives local exponential stability of the trajectory, under conditions on the smoothness of $f$ and on the uniformity of the bounds (Khalil 2002, Section 4.6).
- **Discrete LTV and sampled systems.** Sampling a periodic system at its period gives a time-invariant discrete system with the monodromy matrix $\Phi(T, 0)$.

## Known results in the model

- **Existence and uniqueness (theorem).** Global, as above. There is no finite escape time.
- **Solution formula (theorem).** Through $\Phi$; see the [variation of constants formula](/variation-of-constants-formula/). The Peano-Baker series and the properties of $\Phi$ are on the [state-transition matrix](/state-transition-matrix/) page.
- **Uniform exponential stability (definition and theorem).** $\dot x = A(t) x$ is uniformly exponentially stable if there are $c, \lambda > 0$ with $\|\Phi(t, \tau)\| \le c e^{-\lambda(t - \tau)}$ for all $t \ge \tau$ (Rugh 1996, Chapter 6). For bounded $A(t)$ this is equivalent to the existence of a quadratic Lyapunov function $x^T P(t) x$ with $P(t)$ bounded above and below by positive multiples of $I$ (Khalil 2002, Section 4.6). See [exponential stability](/exponential-stability/).
- **Frozen eigenvalues do not decide stability (counterexample).** Khalil (2002, Example 4.22) takes

  $$A(t) = \begin{bmatrix} -1 + 1.5 \cos^2 t & 1 - 1.5 \sin t \cos t \\ -1 - 1.5 \sin t \cos t & -1 + 1.5 \sin^2 t \end{bmatrix}.$$

  For every $t$ the characteristic polynomial is $s^2 + 0.5 s + 0.5$, with roots $-0.25 \pm 0.25\sqrt 7\, i = -0.25 \pm 0.6614 i$, so $A(t)$ is Hurwitz at every $t$. Yet $x(t) = (e^{0.5t} \cos t, -e^{0.5t} \sin t)$ is a solution: differentiate the first component, $e^{0.5t}(0.5 \cos t - \sin t)$, and compare with the first row of $A(t)$ times $x(t)$, which gives the same expression after $\cos^3 t + \sin^2 t \cos t = \cos t$. The solution grows without bound. The example above with $e^{2t}$ shows the same with real eigenvalues.
- **Slowly varying systems (theorem).** If $A(t)$ is continuously differentiable and bounded, all eigenvalues of $A(t)$ have real parts at most $-\sigma < 0$ for all $t$, and $\|\dot A(t)\| \le \mu$ for a $\mu$ that is small enough, then the system is uniformly exponentially stable (Rugh 1996, Chapter 8, slowly varying systems). The bound on $\mu$ depends on $\sigma$ and on the bound on $\|A(t)\|$. In Khalil's example $\|\dot A(t)\|$ is not small, so the theorem does not apply.
- **Periodic systems (theorem).** If $A(t + T) = A(t)$, then $\Phi(t + T, \tau + T) = \Phi(t, \tau)$, and the system is exponentially stable if and only if every eigenvalue of the monodromy matrix $\Phi(T, 0)$ has modulus less than 1 (Floquet theory; Rugh 1996, Chapter 5). Khalil's matrix has period $\pi$ and monodromy matrix $\operatorname{diag}(-e^{\pi/2}, -e^{-\pi}) = \operatorname{diag}(-4.8105, -0.0432)$, which confirms the instability.
- **Controllability (theorem).** The pair is controllable on $[t_0, t_1]$ if and only if the gramian $W(t_0, t_1) = \int_{t_0}^{t_1} \Phi(t_1, s) B(s) B(s)^T \Phi(t_1, s)^T ds$ is invertible, and then the input $u(s) = B(s)^T \Phi(t_1, s)^T W^{-1}(x_1 - \Phi(t_1, t_0) x_0)$ steers $x_0$ to $x_1$ with the least energy (see [controllability gramian](/controllability-gramian/)). Controllability can depend on the interval. The rank of $[B(t), A(t) B(t), \dots]$ at a single $t$ does not decide it; for smooth coefficients there is a sufficient rank test with derivatives of $B$ (Chen 1999, Chapter 6). Observability is dual.
- **Design.** Finite-horizon LQR and the Kalman-Bucy filter work for LTV systems with a Riccati differential equation; see [finite-horizon LQR](/finite-horizon-lqr/) and [Kalman-Bucy filter](/kalman-bucy-filter/). Pole placement has no direct analogue, because eigenvalues are not the right object.

## References
