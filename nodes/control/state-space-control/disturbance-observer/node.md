---
tag: 1HYDAN
kind: algorithm
slug: disturbance-observer
name: Disturbance observer
aliases:
- DOB
- disturbance observer-based control
area: control/state-space-control
level: advanced
summary: Estimates a lumped disturbance from the input and the output through a nominal inverse model and a filter, and cancels it.
solves: [state-estimation]
model: real-ram
complexity:
  vars: {n: the order of the filter (the degree of N plus k), N: the number of updates}
  time: {worst: "O(n^2 + N n^2)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, exact: true, recursive: true, online: true}
history:
  year: 1987
  people: [Kouhei Ohishi, Masato Nakao, Kouhei Ohnishi, Kunio Miyachi]
  note: "Ohishi, Nakao, Ohnishi and Miyachi used a disturbance observer for a load-insensitive DC motor position servo in 1987. Chen, Yang, Guo and Li surveyed disturbance-observer-based control in 2016."
prereqs: [transfer-function, minimum-phase, observable-canonical-form]
see_also: [unknown-input-observer, active-disturbance-rejection-control, internal-model-principle, luenberger-observer, pid-controller, sensitivity-function, model-uncertainty, state-observer]
sources:
  - paper: doi:10.1109/tie.1987.350923
    title: Kouhei Ohishi, Masato Nakao, Kouhei Ohnishi and Kunio Miyachi, Microprocessor-controlled DC motor for load-insensitive position servo system, IEEE Transactions on Industrial Electronics 34(1), 44-49, 1987
    locator: the disturbance observer of the DC motor and the cancellation of the load torque
  - paper: doi:10.1109/tie.2015.2478397
    title: Wen-Hua Chen, Jun Yang, Lei Guo and Shihua Li, Disturbance-observer-based control and related methods, an overview, IEEE Transactions on Industrial Electronics 63(2), 1083-1095, 2016
    locator: the frequency-domain disturbance observer with a Q filter, and its relation to other disturbance estimation methods
---

A disturbance observer estimates an unknown signal $d$ that enters a plant together with the control input, so that $y = P(s)(u + d)$, and subtracts the estimate from the input. It uses a nominal model $P_n(s) = N(s)/D(s)$ of the plant and a low-pass filter $Q(s)$ with $Q(0) = 1$:

$$\hat d = Q(s)\bigl(P_n(s)^{-1} y - u\bigr), \qquad u = u_c - \hat d.$$

Here $u_c$ is the output of an outer controller. The term $P_n^{-1} y$ is the input that the nominal plant needs to produce $y$, so $P_n^{-1} y - u$ is the part of the input that the model cannot explain. This lumped disturbance contains the external load and also the effect of the model error. The filter $Q$ makes $Q P_n^{-1}$ proper and sets the bandwidth of the estimate. A constant disturbance is removed with no steady-state error. An [unknown input observer](/unknown-input-observer/) solves a different task: it estimates the state with an error that does not depend on $d$, and it needs no filter, but it needs a state-space model and a rank condition. The [state observer](/state-observer/) page compares the observers of this area.

## In plain words

A motor must hold a speed, but an unknown load pulls on it. The disturbance observer asks a question at every instant: which input would a perfect motor need to move as the real one moves? The difference between that input and the input that was actually sent is the push of the unknown load. The observer smooths this difference, because the calculation needs a derivative of the measurement and would amplify noise. Then it subtracts the smoothed value from the next input, so the load is cancelled before the main controller has to react. The smoothing decides how fast the observer is and how much noise reaches the motor.

## The problem

Input: the nominal plant $P_n(s) = N(s)/D(s)$, strictly proper with relative degree $r = \deg D - \deg N \ge 1$ and with all roots of $N$ in the open left half plane, a time constant $\tau > 0$ and an integer order $k \ge r$. Output: a state-space realization $(A_f, B_f, C_f, D_f)$ of the two-input filter

$$\hat d = \frac{D(s)\, y - N(s)\, u}{N(s)\,(\tau s + 1)^k},$$

which is $Q P_n^{-1} y - Q u$ with $Q(s) = 1/(\tau s + 1)^k$, and the update that runs it in the loop $u = u_c - \hat d$.

The condition $k \ge r$ makes the transfer function from $y$ proper. The condition on $N$ makes the filter stable: its poles are the roots of $N$ and $-1/\tau$. A plant with a zero in the right half plane cannot be inverted in this way. The filter has no direct feedthrough from $u$, so the loop $u = u_c - \hat d$ has no algebraic loop.

## The algorithm

```pseudo id=main
DOB-DESIGN(N, D, tau, k)
L1  if k < deg D - deg N or N is not Hurwitz: fail   ▷ Q P_n^(-1) improper, or unstable inverse
L2  a ← N (tau s + 1)^k, divided by its leading coefficient
L3  b_y ← D / lead;  b_u ← -N / lead                  ▷ both padded to n + 1 coefficients, n = deg a
L4  A_f ← companion matrix of a in observable form;  B_f, C_f, D_f from b_y and b_u
L5  return A_f, B_f, C_f, D_f
UPDATE(x_f, y, u)
L6  x_f' ← A_f x_f + B_f [y; u]                        ▷ derivative of the filter state
L7  d_hat ← C_f x_f + D_f [y; u]
L8  u ← u_c - d_hat                                    ▷ D_f has 0 in the u column
```

Line L1 checks the Hurwitz property of $N$ by the Routh test, which is exact in rational arithmetic. Line L4 builds the observable canonical form: $A_f$ has $-a_1, \dots, -a_n$ in its first column and ones on the superdiagonal, $C_f = [1, 0, \dots, 0]$, the direct term of each input is the leading coefficient $\beta_0$ of its numerator $\beta$, and column $i$ of $B_f$ holds $\beta_i - \beta_0 a_i$. With $k > r$ the filter is strictly proper in both inputs. With $k = r$ it has a direct term from $y$. In discrete time the same filter is discretized, for example by the [zero-order hold](/zero-order-hold-discretization/) or the [bilinear transform](/bilinear-transform/).

## Example

A motor with inertia $J$ and an unknown load torque $d$ has $J\dot\omega = u + d$, so $P(s) = 1/(Js)$. The nominal model is $P_n = 1/(J_n s)$ with $J_n = 0.01$, the filter is $Q = 1/(0.01 s + 1)$ ($\tau = 0.01$, $k = 1 = r$), and the outer controller is $u_c = -0.5\,\omega$, which regulates the speed to 0. Lines L2 to L4 give

$$\dot x_f = -100\, x_f - 100\, \omega - 100\, u, \qquad \hat d = x_f + \omega,$$

that is, $\hat d = (s\,\omega - 100\, u)/(s + 100)$, which is $Q(J_n s\, \omega - u)$. A load step $d = -0.1$ at $t = 0$ gives the speeds below. The estimate in the exact case is $\hat d = -0.1(1 - e^{-100 t})$.

| $t$ | 0.01 | 0.02 | 0.05 | 0.1 | 0.2 |
|---|---|---|---|---|---|
| no observer | -0.079 | -0.126 | -0.184 | -0.199 | -0.200 |
| observer, $J = J_n$ | -0.048 | -0.047 | -0.015 | -0.0013 | -9.1e-6 |
| observer, $J = 2 J_n$ | -0.034 | -0.044 | -0.023 | 0.00059 | -2.7e-5 |

Without the observer the speed settles at $-0.1/0.5 = -0.2$: the proportional controller leaves an offset. With the observer and $J = J_n$ the speed is $\omega(t) = -0.2(e^{-50t} - e^{-100t})$, with its largest value $-0.05$ at $t = \ln 2/50 \approx 0.014$, and it returns to 0. With the true inertia twice the nominal one, the closed loop has the poles $-37.5 \pm 33.1i$, and the offset is still 0.

## Correctness

With zero initial conditions and $y = P(u + d)$, the estimate is $\hat d = Q P_n^{-1} P(u + d) - Qu$. If $P = P_n$, this is $\hat d = Qd$ for every input $u$. With $u = u_c - \hat d$ the output is

$$y = \frac{P P_n}{P_n + Q(P - P_n)}\bigl(u_c + (1 - Q)d\bigr).$$

So the observer replaces $d$ by $(1 - Q)d$, which is small where $Q$ is close to 1. At low frequency the plant seen by the outer controller is close to $P_n$. If the whole loop with the outer controller is stable, the transfer function from $d$ to $y$ has the factor $(\tau s + 1)^k - 1$ in its numerator, which is 0 at $s = 0$. By the [final value theorem](/final-value-theorem/) a constant disturbance leaves no offset, for every plant $P$ for which the loop is stable. The full proof, with the check of the realization of line L4, is in [proofs/correctness.md](proofs/correctness.md). The tests compare the transfer function of the realization with the formula at random complex points, check $\hat d = Qd$ in simulation, the zero offset with $J = J_n$ and $J = 2J_n$, a plant of relative degree 2, and the Routh test against known roots.

## Complexity

Let $n = \deg N + k$ be the order of the filter. Line L1 costs $O(n^2)$ for the Routh test, line L2 costs $O(nk)$, and lines L3 and L4 cost $O(n^2)$ to fill the dense matrices. Each update costs $O(n^2)$ with the dense matrix $A_f$, or $O(n)$ if the companion structure is used. The space is $O(n^2)$ for $A_f$, or $O(n)$ with the companion structure.

## Properties

- **Two-degree-of-freedom structure.** The observer acts as an inner loop that makes the plant behave like $P_n$ at low frequency. The outer controller is designed for $P_n$. The tracking response and the disturbance response can be tuned separately.
- **Sensitivity.** In the inner loop $1 - Q$ plays the role of the [sensitivity function](/sensitivity-function/) and $Q$ the role of the [complementary sensitivity](/complementary-sensitivity-function/). Measurement noise $\nu$ enters the estimate as $QP_n^{-1}\nu$, so a wide bandwidth of $Q$ rejects $d$ better and passes more noise.
- **Relation to integral action.** For $P_n = 1/(J_n s)$, $Q = 1/(\tau s + 1)$ and $u_c = -k_p y$, the observer and the gain together are exactly the PI controller $u = -(k_p + J_n/\tau)y - (k_p/\tau)\int y\,dt$. The tests check this. The observer gives the integral action a physical meaning: the integral state is the load estimate.
- **Model error as disturbance.** The lumped disturbance $(P_n^{-1}P - 1)(u + d) + d$ includes the effect of the model error, so the observer also reduces the effect of parameter changes at low frequency.

## Variants and improvements

- **State-space form.** Add a disturbance state with $\dot d = 0$ to the model and design a [Luenberger observer](/luenberger-observer/) for the augmented system. This is the [internal model principle](/internal-model-principle/) applied to the estimator. Models such as $\ddot d = -\omega_0^2 d$ give observers for sinusoidal disturbances.
- **Extended state observer.** [Active disturbance rejection control](/active-disturbance-rejection-control/) treats the total unknown dynamics as one extra state of a chain of integrators and estimates it with a high-gain observer. It needs less model knowledge than the disturbance observer.
- **Higher-order filters.** A larger $k$ or a filter with a numerator, such as a binomial filter with free numerator coefficients, makes $1 - Q$ small to a higher order at $s = 0$, which also removes ramp disturbances.
- **Discrete time.** The filter is discretized, or $P_n^{-1}$ is replaced by a one-step-ahead inverse of a discrete model. A delay in the loop is then explicit.
- **Nonlinear disturbance observers.** For robot manipulators and other nonlinear plants, the estimate uses the nonlinear inverse dynamics. The overview of Chen, Yang, Guo and Li describes this family.

## When to use it

Use a disturbance observer when a low-order nominal model is known, when the plant is minimum phase, and when the disturbances are slow compared with the achievable bandwidth. Typical cases are motion control of motors, positioning stages and robot joints, where load torques and friction act on the input. If the plant has a right-half-plane zero or a long delay, an [internal model control](/internal-model-control/) design or an observer for an augmented state-space model is usually better. If the state, not the disturbance, is needed with an error independent of $d$, use an [unknown input observer](/unknown-input-observer/).

## Pitfalls

- **Bandwidth and noise.** A small $\tau$ gives a fast estimate but passes noise, because $Q P_n^{-1}$ approaches a derivative of order $r$.
- **Robust stability of the inner loop.** In the first-order example the inner loop is stable for every positive $J$ and $J_n$. For plants of higher relative degree, a large model error together with a small $\tau$ can make the inner loop unstable. Check the characteristic polynomial of the whole loop, or use a [small-gain](/small-gain-theorem/) argument with a bound on the [model uncertainty](/model-uncertainty/).
- **Non-minimum-phase plants.** $P_n^{-1}$ is unstable if $N$ has a root in the right half plane. The algorithm rejects such models.
- **Saturation.** The cancellation $u = u_c - \hat d$ can ask for more input than the actuator gives. The filter then integrates a wrong residual. Use [anti-windup](/anti-windup/) measures.
- **Delay.** A delay between $u$ and $y$ that $P_n$ does not contain limits the usable bandwidth of $Q$; see [time-delay systems](/time-delay-system/).

## Implementations

## History

Ohnishi and his coworkers developed the disturbance observer for motion control of DC motors in the 1980s. Ohishi, Nakao, Ohnishi and Miyachi (1987) used it to make a position servo insensitive to the load. The method spread to hard disk drives, robot joints and many other motion systems. Chen, Yang, Guo and Li (2016) surveyed disturbance-observer-based control and its relation to the extended state observer and other methods.

## References
