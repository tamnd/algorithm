---
tag: 400TZ1
kind: technique
slug: offset-free-mpc
name: Offset-free MPC
aliases:
- disturbance model MPC
area: control/optimal-and-predictive-control
level: advanced
summary: Adds integrating disturbance states, estimated by an observer, so that a converging MPC loop has no steady-state error under constant disturbances and model error.
prereqs: [linear-mpc, luenberger-observer, detectability, internal-model-principle]
see_also: [model-predictive-control, dynamic-matrix-control, kalman-filter, disturbance-observer, integral-state-feedback, steady-state-error, popov-belevitch-hautus-test, output-regulation-problem]
sources:
  - paper: "Kenneth R. Muske and Thomas A. Badgwell, Disturbance modeling for offset-free linear model predictive control, Journal of Process Control 12(5), 617-632, 2002"
    locator: the augmented disturbance model, the detectability condition, and the conditions for offset-free control
  - paper: doi:10.1002/aic.690490213
    title: Gabriele Pannocchia and James B. Rawlings, Disturbance models for offset-free model-predictive control, AIChE Journal 49(2), 426-437, 2003
    locator: the detectability rank condition, the choice of as many disturbances as measured outputs, the target calculation and the offset-free theorem
  - book: isbn:9780975937730
    title: James B. Rawlings, David Q. Mayne and Moritz M. Diehl, Model Predictive Control, Theory, Computation, and Design, 2nd edition, Nob Hill Publishing, 2017
    locator: the treatment of disturbance models, target calculation and offset-free MPC
  - paper: doi:10.1016/S0967-0661(02)00186-7
    title: S. Joe Qin and Thomas A. Badgwell, A survey of industrial model predictive control technology, Control Engineering Practice 11(7), 733-764, 2003
    locator: the constant output disturbance of industrial MPC products
---

Offset-free MPC is the standard way to give a state-space [model predictive controller](/model-predictive-control/) integral action. Plain [linear MPC](/linear-mpc/) drives the model to the setpoint; if the plant differs from the model or a constant disturbance acts on it, the real output settles at the wrong value. Offset-free MPC adds constant disturbance states $d$ to the model, estimates them together with the state by an observer, and computes at each sampling instant a steady-state target $(x_s, u_s)$ that puts the output on the setpoint for the estimated disturbance. MPC then regulates the state to this target. If the augmented model is detectable, the number of disturbances equals the number of measured outputs, and the closed loop converges, the output reaches the setpoint with no offset, whatever the cause of the mismatch. The constant output disturbance of [DMC](/dynamic-matrix-control/) is a special case.

## In plain words

A model is never exact, and the plant feels forces that the model does not know. A plain predictive controller trusts its model, so it settles where the model says the output is right, not where it really is. Offset-free MPC adds to the model an unknown constant push, and an estimator learns its size from the gap between the measured and the predicted output. As long as the gap stays, the estimate keeps changing. At each tick the controller asks where it must hold the inputs so that the output is right with the push included, and it steers there. When everything settles, the gap must be zero, so the real output is at the setpoint. This is the same idea as the integral term of a PID controller, built into the model.

## When it applies

- A linear (or linearized) model $x_{k+1} = A x_k + B u_k$, $y_k = C x_k$, with $p$ measured outputs, used by an MPC that tracks setpoints $r$ for some controlled outputs $z = H y$.
- The plant differs from the model, or constant or slowly varying disturbances act on it, and the controlled outputs must settle exactly at the setpoints.
- The setpoints are reachable at steady state within the constraints. If a constraint is active at steady state, some output cannot reach its setpoint, whatever the controller does.

## The template

1. **Augment the model** with $n_d$ integrating disturbances:

$$\begin{bmatrix} x \\ d \end{bmatrix}_{k+1} = \begin{bmatrix} A & B_d \\ 0 & I \end{bmatrix} \begin{bmatrix} x \\ d \end{bmatrix}_k + \begin{bmatrix} B \\ 0 \end{bmatrix} u_k, \qquad y_k = \begin{bmatrix} C & C_d \end{bmatrix} \begin{bmatrix} x \\ d \end{bmatrix}_k.$$

$B_d$ and $C_d$ choose where the disturbances enter: at the inputs ($B_d = B$, $C_d = 0$), at the outputs ($B_d = 0$, $C_d = I$), or in between.

2. **Check detectability** (theorem, Muske and Badgwell 2002; Pannocchia and Rawlings 2003). The augmented pair is [detectable](/detectability/) if and only if $(C, A)$ is detectable and

$$\operatorname{rank} \begin{bmatrix} A - I & B_d \\ C & C_d \end{bmatrix} = n + n_d.$$

The matrix has $n + p$ rows, so this needs $n_d \le p$. Choose $n_d = p$ for offset-free control.

3. **Estimate** $(\hat x, \hat d)$ with an observer for the augmented model, for example a steady-state [Kalman filter](/kalman-filter/) or a [Luenberger observer](/luenberger-observer/), such that the estimation error dynamics are Schur.

4. **Compute the target** at each sampling instant from $\hat d$ and $r$:

$$\begin{bmatrix} A - I & B \\ H C & 0 \end{bmatrix} \begin{bmatrix} x_s \\ u_s \end{bmatrix} = \begin{bmatrix} -B_d \hat d \\ r - H C_d \hat d \end{bmatrix},$$

or, with constraints or more inputs than controlled outputs, a small QP that finds the closest admissible steady state.

5. **Regulate** with MPC on the deviations $x - x_s$, $u - u_s$, starting from $\hat x$, with the disturbance $\hat d$ in the prediction model, and apply the first input.

**Offset-free theorem** (Pannocchia and Rawlings 2003). Suppose $n_d = p$, the augmented model is detectable, the observer is Schur, the target problem is feasible, and the closed loop of plant, observer and MPC converges to a steady state with no constraint active, under constant $r$ and constant disturbances. Then $H y = r$ at the steady state. Proof sketch: at steady state the observer update must be zero, $L_d (y - C \hat x - C_d \hat d) = 0$, and for $n_d = p$ a Schur observer has a nonsingular $L_d$, so $y = C \hat x + C_d \hat d$. With no active constraint, MPC stops at its target, $\hat x = x_s$, and then $H y = H C x_s + H C_d \hat d = r$ by the target equations. The plant model is not used in the argument, so any model error that keeps the loop convergent is allowed.

**Cost per sampling instant.** One observer update, $O((n + n_d)^2 + (n + n_d) p)$; one target computation, a linear solve or a small QP in $n + m$ variables; and the MPC QP of [linear MPC](/linear-mpc/), with $N m$ variables and $c$ rows, solved by an active set or interior point method.

## Classic examples

**Model error on a scalar plant** (measurement with a short script). The model is $x_{k+1} = 0.8\, x_k + 0.2\, u_k$, $y = x$ (gain 1); the plant has $0.25$ instead of $0.2$ (gain 1.25). The unconstrained MPC uses $Q = R = 1$ and the Riccati terminal cost, so it is the LQR law $u = u_s - K (x - x_s)$ with $K = 0.3508$. The setpoint is $r = 1$ from $x_0 = 0$.

- **Plain MPC** uses the target $x_s = 1$, $u_s = 1$ of the model. The output settles at $y = 1.1738$: an offset of 17 percent.
- **Offset-free MPC** with an output disturbance ($B_d = 0$, $C_d = 1$, so $n_d = p = 1$). The rank matrix is $\begin{bmatrix} -0.2 & 0 \\ 1 & 1 \end{bmatrix}$, of rank 2, so the model is detectable. The observer corrects only $\hat d$, with gain 1, so $\hat d = y - \hat x$ with $\hat x$ the model output, exactly the DMC estimate. The target is $x_s = r - \hat d$, $u_s = x_s$.

| $k$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | $\infty$ |
|---|---|---|---|---|---|---|---|---|
| plain MPC | 0.3377 | 0.5782 | 0.7496 | 0.8716 | 0.9586 | 1.0205 | 1.0646 | 1.1738 |
| offset-free MPC | 0.3377 | 0.5614 | 0.7095 | 0.8076 | 0.8726 | 0.9156 | 0.9441 | 1 |

The input of the offset-free loop settles at $0.8 = 1 / 1.25$, the input that the real plant needs. With the observer gain 0.5 instead of 1 the output also settles at 1.

**The output disturbance fails for an integrator** (theorem). For $A = 1$, $B = 1$, $C = 1$ and $B_d = 0$, $C_d = 1$, the rank matrix is $\begin{bmatrix} 0 & 0 \\ 1 & 1 \end{bmatrix}$, of rank $1 < 2$: a constant output offset and a constant state offset give the same measurements, so $\hat d$ cannot be estimated. The input disturbance $B_d = 1$, $C_d = 0$ gives $\begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$, of rank 2, and works. This is one reason why the constant output disturbance of DMC does not suit integrating plants.

**Industrial MPC.** [DMC](/dynamic-matrix-control/) and the products based on it use a constant output disturbance, the difference between the measured and the model output (Qin and Badgwell 2003).

## Variations

- **Input disturbance models** ($B_d = B$) work for integrating plants. Rule of thumb: they also reject disturbances that enter at the inputs faster than an output disturbance model does.
- **Velocity form.** Writing the model in the increments $\Delta u$ and $\Delta x$ also removes offset, without a separate disturbance state; [GPC](/generalized-predictive-control/) gets its integral action this way, from the factor $\Delta$ in its model.
- **Target QP.** With constraints or extra inputs, the target is the solution of a QP that minimizes the distance to the setpoints or to preferred input values; this layer is often called steady-state target optimization.
- **Nonlinear offset-free MPC.** The same augmentation works for a nonlinear model $f(x, u) + B_d d$, with an extended Kalman filter or moving horizon estimation; see [nonlinear MPC](/nonlinear-mpc/).
- **Disturbance observers** in classical control estimate a lumped disturbance at the input for the same purpose; see [disturbance observer](/disturbance-observer/).

## Pitfalls

- **Too few disturbances.** With $n_d < p$, some measured output has no disturbance to absorb its mismatch, and in general that output has an offset.
- **A model that is not detectable.** If the rank test fails, no observer is Schur. Check the rank before tuning, as in the integrator example.
- **Infeasible targets.** If the setpoint cannot be held within the input limits for the estimated disturbance, the target equations have no admissible solution. Use a target QP that moves the target to the closest admissible point.
- **Slow observer, slow rejection.** The disturbance estimate sets how fast offsets vanish. A gain that is too large amplifies measurement noise. Rule of thumb: tune the disturbance part of the observer like the integral action of a PI controller.
- **Not a stability guarantee.** The offset-free theorem assumes that the loop converges. Model error can still make the loop lose asymptotic stability; check robustness separately.
- **Unmeasured controlled outputs.** The theorem is about the measured outputs. A controlled output that is not measured can still have an offset.

## Exercises

1. Prove the detectability condition: the augmented pair is detectable if and only if $(C, A)$ is detectable and the rank condition holds. Use the [PBH test](/popov-belevitch-hautus-test/) at the eigenvalue 1.
2. For the scalar example, find the offset of plain MPC as a function of the plant gain $b_p / 0.2$, and check the value 1.1738 for $b_p = 0.25$.
3. Show that with $n_d = p$ and a Schur observer the gain $L_d$ is nonsingular.
4. For $A = 1$, $B = 1$, $C = 1$, use the input disturbance model and write the target equations. What are $x_s$ and $u_s$ for a setpoint $r$ and an estimate $\hat d$?
5. A plant has two outputs and one input. Explain why at most one controlled output can be offset-free, whatever the disturbance model.

## References
