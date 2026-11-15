---
tag: CY2X2T
kind: algorithm
slug: high-gain-observer
name: High-gain observer
aliases:
- high gain observer
area: control/nonlinear-control
level: advanced
summary: An observer for systems in observable form whose gains grow with a small parameter, so the estimation error decays as fast as wanted.
model: real-ram
complexity:
  vars: {n: the order of the system, q: the number of arithmetic operations to evaluate the nominal model once}
  time: {worst: "O(n + q)"}
  space: {extra: "O(n)"}
properties: {deterministic: true, exact: true, recursive: false, online: true}
history:
  year: 1992
  people: [Farzad Esfandiari, Hassan K. Khalil, Laurent Praly, Ahmed N. Atassi]
  note: "Esfandiari and Khalil (1992) used high-gain observers for output feedback of nonlinear systems and showed how to handle the peaking phenomenon by saturating the control; Atassi and Khalil (1999) proved a separation principle; Khalil and Praly (2014) surveyed the field."
prereqs: [state-observer, luenberger-observer, observable-canonical-form]
see_also: [sliding-mode-observer, active-disturbance-rejection-control, separation-principle, singular-perturbation-method, feedback-linearization, backstepping, extended-kalman-filter, super-twisting-algorithm]
sources:
  - paper: doi:10.1080/00207179208934355
    title: "F. Esfandiari and H. K. Khalil, Output feedback stabilization of fully linearizable systems, International Journal of Control 56(5), 1007-1037, 1992"
    locator: the high-gain observer for output feedback, the peaking phenomenon, and the saturation of the control outside a compact set
  - paper: "A. N. Atassi and H. K. Khalil, A separation principle for the stabilization of a class of nonlinear systems, IEEE Transactions on Automatic Control 44(9), 1672-1687, 1999"
    title: A separation principle for the stabilization of a class of nonlinear systems
    locator: the recovery of the state feedback performance by output feedback with a high-gain observer as the parameter goes to zero
  - paper: doi:10.1002/rnc.3051
    title: "H. K. Khalil and L. Praly, High-gain observers in nonlinear feedback control, International Journal of Robust and Nonlinear Control 24(6), 993-1015, 2014"
    locator: the survey of the observer, the scaled error equation, peaking, and the effect of measurement noise
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 14.5, High-gain observers
---

A high-gain observer is a [state observer](/state-observer/) for a nonlinear system in observable form, a chain of integrators $\dot x_i = x_{i+1}$ that ends in $\dot x_n = \phi(x, u)$, with the output $y = x_1$. It is a [Luenberger observer](/luenberger-observer/) for the chain whose gains are $\alpha_i / \varepsilon^i$ for a small parameter $\varepsilon > 0$. As $\varepsilon$ goes to $0$, the error decays on the time scale $\varepsilon$, and the effect of an error in the model $\phi$ shrinks like a power of $\varepsilon$. It does not need an exact model. The price is a large transient in the estimates, the peaking phenomenon, and a high sensitivity to measurement noise.

## In plain words

You measure a position and want the velocity, and maybe the acceleration, without a good model of the forces. You can run a model and correct it by the measured error. If you make the correction very strong, the model hardly matters: the estimate is pulled onto the measurement so fast that the forces have no time to push it away. The stronger the correction, the smaller the remaining error. But a strong correction overreacts at the start, when the estimate is far from the truth, and gives a huge, short spike in the estimated velocity. If a controller uses that spike, it can push the machine hard in the wrong direction. The usual cure is to limit the control, so the spike passes without harm. Noise on the measurement is amplified in the same way, which sets a limit on how strong the correction can be.

## The problem

**Input.** A system in observable form

$$\dot x_i = x_{i+1} \quad (i = 1, \dots, n - 1), \qquad \dot x_n = \phi(x, u), \qquad y = x_1,$$

with a measured output $y$ and a known input $u$. A nominal model $\phi_0(\hat x, u)$ of $\phi$; $\phi_0 = 0$ is allowed. Coefficients $\alpha_1, \dots, \alpha_n$ such that $s^n + \alpha_1 s^{n-1} + \dots + \alpha_n$ is Hurwitz, and a small $\varepsilon > 0$. Many systems with a well-defined [relative degree](/relative-degree/) $n$ take this form in the coordinates $y, \dot y, \dots, y^{(n-1)}$.

**Output.** The right side of the observer, which an ODE solver or a sampled implementation integrates, such that the scaled errors $\eta_i = (x_i - \hat x_i) / \varepsilon^{n-i}$ obey

$$\varepsilon \dot \eta = A_0 \eta + \varepsilon B \delta, \qquad \delta = \phi(x, u) - \phi_0(\hat x, u),$$

where $A_0$ is the companion matrix of the Hurwitz polynomial and $B = (0, \dots, 0, 1)^T$.

## The algorithm

```pseudo id=main
HIGH-GAIN-OBSERVER(x̂, y, u, ε, α, φ_0)
L1  e ← y - x̂_1
L2  for i ← 1 to n - 1
L3      ẋ̂_i ← x̂_{i+1} + (α_i / ε^i) e
L4  ẋ̂_n ← φ_0(x̂, u) + (α_n / ε^n) e
L5  return ẋ̂
```

Line L1 is the output error. Lines L2 and L3 copy the chain of integrators and add the correction with gain $\alpha_i / \varepsilon^i$. Line L4 uses the nominal model for the last equation. In matrix form the observer is $\dot{\hat x} = A \hat x + B \phi_0(\hat x, u) + L_o (y - C \hat x)$, with $A$ the shift matrix, $C = (1, 0, \dots, 0)$ and $L_o = (\alpha_1 / \varepsilon, \dots, \alpha_n / \varepsilon^n)^T$. The eigenvalues of $A - L_o C$ are the roots of the Hurwitz polynomial divided by $\varepsilon$.

## Example

**Van der Pol oscillator with no model.** Let $\dot x_1 = x_2$, $\dot x_2 = -x_1 + (1 - x_1^2) x_2$, $y = x_1$, $x(0) = (2, 0)$. The observer uses $\phi_0 = 0$, so it knows nothing about the dynamics except the chain, with $\alpha = (2, 1)$ (both roots at $-1/\varepsilon$) and $\hat x(0) = (0, 0)$. The joint system is integrated with 4th order Runge-Kutta with step $0.002$.

| $\varepsilon$ | $\max_{t \ge 2} \lvert e_1 \rvert$ | $\max_{t \ge 2} \lvert e_2 \rvert$ | peak of $\lvert e_2 \rvert$ | $\lvert e_1(0) \rvert / (e \varepsilon)$ |
|---|---|---|---|---|
| 0.04 | 0.00742 | 0.372 | 18.46 | 18.39 |
| 0.02 | 0.00189 | 0.189 | 36.82 | 36.79 |
| 0.01 | 0.000475 | 0.0950 | 73.59 | 73.58 |

The remaining errors scale like $\varepsilon^2$ in $x_1$ and $\varepsilon$ in $x_2$, as the scaled error equation predicts ($e_1 = \varepsilon \eta_1$, $e_2 = \eta_2$, $\eta = O(\varepsilon)$). The peak grows like $1/\varepsilon$. For $\delta = 0$ the error is $e_2(t) = -(t/\varepsilon) e^{-t/\varepsilon} e_1(0)/\varepsilon$, whose largest value $|e_1(0)| / (e \varepsilon)$ at $t = \varepsilon$ is the last column. At $\varepsilon = 0.02$ and $t = 0.02$ the true velocity is $-0.039$ and the estimate is $36.78$.

**Peaking in output feedback.** Let $\dot x_1 = x_2$, $\dot x_2 = x_2^3 + u$, with the state feedback $u = -x_2^3 - x_1 - x_2$, which makes the origin globally asymptotically stable. Put the estimates of the observer (with $\phi_0 = \hat x_2^3 + u$) into the feedback, from $x(0) = (0.1, 0)$ and $\hat x(0) = 0$, with RK4 and step $0.0005$. Without saturation, $|x|$ reaches $0.758$ and $|u|$ reaches $52$ for $\varepsilon = 0.01$; $3.08$ and $393$ for $\varepsilon = 0.005$; and for $\varepsilon = 0.0025$ the state escapes to infinity before $t = 0.02$. A smaller $\varepsilon$ makes it worse. With $u$ and the $\hat x_2$ inside $\phi_0$ clipped to $[-1, 1]$, the state never exceeds its initial size $0.1$ for $\varepsilon = 0.0025$, and at $t = 5$ it is within $0.01$ of $0$, as with state feedback.

## Correctness

The full proof is in proofs/correctness.md. Its main steps:

- **The scaled error equation.** Subtracting the observer from the plant and dividing $x_i - \hat x_i$ by $\varepsilon^{n-i}$ gives $\varepsilon \dot \eta = A_0 \eta + \varepsilon B \delta$. This is algebra, and the tests check it exactly in Fraction for 150 random cases with $n = 1$ to $4$.
- **Theorem (exponential decay and ultimate bound).** Let $P_0$ solve the [Lyapunov equation](/lyapunov-equation/) $P_0 A_0 + A_0^T P_0 = -I$ and let $|\delta| \le M$ along the motion. Then $W = \eta^T P_0 \eta$ satisfies $\varepsilon \dot W \le -\|\eta\|^2 + 2 \varepsilon M \|P_0 B\| \|\eta\|$, with $\|\cdot\|$ the Euclidean norm. So $\eta$ decays exponentially with rate of order $1/\varepsilon$ until $\|\eta\|$ is of order $\varepsilon M$, and then stays there. In the original coordinates, $x_i - \hat x_i = O(\varepsilon^{n+1-i})$ after a transient of length $O(\varepsilon \ln(1/\varepsilon))$.
- **Theorem (peaking).** $\|\eta(0)\|$ is of order $\|e(0)\| / \varepsilon^{n-1}$, so the estimates of $x_2, \dots, x_n$ have transients of size up to $1/\varepsilon^{n-1}$. For $n = 2$ and $\alpha = (2, 1)$ the peak is exactly $|e_1(0)| / (e \varepsilon)$ when $\delta = 0$.
- **Theorem (separation, cited).** For a state feedback that makes the origin asymptotically stable, saturated outside a compact set of interest, output feedback with a high-gain observer recovers the region of attraction and the trajectories of state feedback as $\varepsilon \to 0$ (Atassi and Khalil 1999). This page does not reprove it; the example shows it.

## Complexity

Count real operations at unit cost, as in the real RAM. One evaluation of the right side costs $O(n)$ operations for the chain and the corrections, plus $q$ for $\phi_0$. The gains $\alpha_i / \varepsilon^i$ can be computed once. The estimate takes $O(n)$ space. The observer is stiff: its eigenvalues are of size $1/\varepsilon$, so an explicit integrator needs a step of order $\varepsilon$ (here $0.2 \varepsilon$ or less), and a run over a time $T$ costs $O((n + q) T / \varepsilon)$.

## Properties

- **Model free in the limit.** The model error $\delta$ enters multiplied by $\varepsilon$, so even $\phi_0 = 0$ works, with an error that is a power of $\varepsilon$.
- **Asymptotic, not finite time.** The error decays exponentially, and with $\delta \neq 0$ it stays at a size of order $\varepsilon M$ in $\eta$. A [sliding mode observer](/sliding-mode-observer/) reaches zero error in finite time instead.
- **Peaking.** The transient grows like $\varepsilon^{1-n}$ in $\hat x_n$. This is not a numerical artifact; it follows from the pole placement at $-1/\varepsilon$ with a fixed initial error.
- **Noise amplification.** Measurement noise of size $\mu$ produces an error of size about $\mu / \varepsilon^{i-1}$ in $\hat x_i$, while the model error term shrinks like $\varepsilon^{n+1-i}$. So there is a best $\varepsilon$ for given noise and model error (Khalil and Praly 2014).
- **Linear in the output.** The correction is linear, so the observer is a linear filter of $y$ when $\phi_0 = 0$. It is then an approximate differentiator of $y$.

## Variants and improvements

- **Extended high-gain observer.** Add one more integrator state for $\delta$. The observer then estimates the model error, which a controller can cancel. This is the observer of [active disturbance rejection control](/active-disturbance-rejection-control/).
- **Saturating the estimates.** Instead of the control, clip each estimate to the range it takes under state feedback. Either clipping protects the plant from the peak.
- **Switched or adaptive gain.** Start with a moderate $\varepsilon$ and lower it after the transient, or adapt it to the noise level, to trade peaking and noise against accuracy.
- **Low-power observers.** Observers whose gains grow like $1/\varepsilon$ or $1/\varepsilon^2$ only, built from cascades of small blocks, reduce the size of the gains for large $n$.
- **Multi-output systems.** Apply the construction to each chain of a system in a block observable form.

## When to use it

Use it for output feedback of nonlinear systems that are in observable form or can be brought to it, such as mechanical systems where only positions are measured, when the model is uncertain and the measurement noise is small. It is the standard tool for proving that a state feedback design, such as [feedback linearization](/feedback-linearization/) or [backstepping](/backstepping/), still works with output feedback. If the noise is large, prefer a stochastic filter such as the [extended Kalman filter](/extended-kalman-filter/). If you need exact estimates in finite time and the model error has a known bound, prefer a [sliding mode observer](/sliding-mode-observer/).

## Pitfalls

- **Peaking into the plant.** Using the estimates of lines L3 and L4 in a feedback without saturation can destabilize the plant, and making $\varepsilon$ smaller makes it worse (example 2).
- **Peaking inside the observer at line L4.** If $\phi_0$ grows fast, such as $\hat x_2^3$, the peak in $\hat x_2$ can make the observer itself escape. Evaluate $\phi_0$ at clipped estimates.
- **Too small an eps.** The noise amplification grows like $1/\varepsilon^{n-1}$, and the observer becomes stiff. An explicit integrator with a step that is not small compared with $\varepsilon$ diverges.
- **Sampled implementation.** A discrete-time observer needs a sampling period that is small compared with $\varepsilon$, or a discretization that is exact for the linear part, such as the [zero-order hold discretization](/zero-order-hold-discretization/).
- **Wrong form.** The construction relies on the chain $\dot x_i = x_{i+1}$. If the system is not in this form, the coordinate change must be found first, and the observer of the original state needs its inverse.

## Implementations

## History

High-gain observers appeared in several forms in the 1980s, in the work of Gauthier and others on observers for uniformly observable systems and in the work of Khalil and his students on output feedback. Esfandiari and Khalil (1992) showed that output feedback with a high-gain observer can destabilize a system because of peaking, and that saturating the control outside a compact set solves the problem. Atassi and Khalil (1999) proved a separation principle: as $\varepsilon \to 0$, the output feedback loop recovers the asymptotic stability, the region of attraction and the trajectories of the state feedback loop. Khalil and Praly (2014) surveyed the theory, including the effect of noise and the extended observers that also estimate disturbances.

## References
