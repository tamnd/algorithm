---
tag: 1YHBZH
kind: algorithm
slug: active-disturbance-rejection-control
name: Active disturbance rejection control
aliases:
- ADRC
- extended state observer
area: control/nonlinear-control
level: research
summary: Lumps unknown dynamics and disturbances into one extra state, estimates it with an observer of the extended state and cancels it in the control law.
model: real-ram
complexity:
  vars: {n: the order of the plant}
  time: {worst: "O(n)"}
  space: {extra: "O(n)"}
properties: {deterministic: true, exact: true, recursive: false, online: true}
history:
  year: 1998
  people: [Jingqing Han, Zhiqiang Gao, Bao-Zhu Guo, Zhi-Liang Zhao]
  note: "Han developed ADRC in the 1990s and presented it in English in 2009; Gao (2003) gave the linear form tuned by two bandwidths; Guo and Zhao (2011) proved convergence of the observer for nonlinear plants."
prereqs: [high-gain-observer, pid-controller, disturbance-observer]
see_also: [internal-model-principle, feedback-linearization, sliding-mode-observer, super-twisting-algorithm, model-uncertainty, routh-hurwitz-criterion, integrator-windup, two-degree-of-freedom-control]
sources:
  - paper: doi:10.1109/TIE.2008.2011621
    title: "J. Han, From PID to active disturbance rejection control, IEEE Transactions on Industrial Electronics 56(3), 900-906, 2009"
    locator: the total disturbance as an extra state, the observer of the extended state, and the nonlinear form of the controller
  - paper: doi:10.1109/ACC.2003.1242516
    title: "Z. Gao, Scaling and bandwidth-parameterization based controller tuning, Proceedings of the American Control Conference, 4989-4996, 2003"
    locator: the linear form with all observer poles at the observer bandwidth and all controller poles at the controller bandwidth
  - paper: doi:10.1016/j.sysconle.2011.03.008
    title: "B.-Z. Guo and Z.-L. Zhao, On the convergence of an extended state observer for nonlinear systems with uncertainty, Systems and Control Letters 60(6), 420-430, 2011"
    locator: convergence of the observer and of the closed loop for nonlinear plants with uncertainty
---

Active disturbance rejection control (ADRC) treats everything in a plant that the designer does not want to model as one signal, the total disturbance, and adds it to the state as an extra component. An observer of this extended state, which is a [high-gain observer](/high-gain-observer/) with one more integrator, estimates the total disturbance from the output. The control law subtracts the estimate and then applies a simple law, such as PD, to what is left: a chain of integrators. The only model data it needs are the order of the plant and a rough value $b_0$ of the input gain. Its linear form has two tuning parameters, the bandwidths of the observer and of the controller.

## In plain words

Suppose you push a cart and do not know its friction, its springs, or the wind. Lump all of these into one unknown force. You know how hard you push and you see where the cart goes, so you can work out the unknown force from the difference between how the cart actually moves and how it would move if you were the only one pushing. Once you know the force, push against it, so it cancels. What is left is a cart with no friction, no spring and no wind, which is easy to control. The faster you work out the force, the better the cancellation, but the more the noise on your measurement shakes your push.

## The problem

**Input.** A plant of order two (the method extends to order $n$)

$$\ddot y = f(t, y, \dot y) + b u,$$

where $y$ is measured, $f$ is unknown, and the input gain $b$ is known only as an estimate $b_0$ of the same sign. A reference $r$, a controller bandwidth $\omega_c > 0$ and an observer bandwidth $\omega_o > 0$. A common rule of thumb takes $\omega_o$ several times $\omega_c$, so that the observer is faster than the loop.

**Output.** A control $u(t)$ such that $y$ follows the response of the PD loop $\ddot y = \omega_c^2 (r - y) - 2 \omega_c \dot y$, with an error that shrinks as $\omega_o$ grows, and with no steady error for a constant disturbance.

The trick is to write the plant as $\ddot y = F + b_0 u$, with the total disturbance $F = f + (b - b_0) u$. The extended state is $x = (y, \dot y, F)$, with $\dot x_3 = \dot F$ unknown.

## The algorithm

```pseudo id=main
ADRC-CONTROL(z, r, ω_c, b_0)
L1  u_0 ← ω_c² (r - z_1) - 2 ω_c z_2
L2  return (u_0 - z_3) / b_0

ADRC-OBSERVER(z, y, u, ω_o, b_0)
L3  e ← y - z_1
L4  ż_1 ← z_2 + 3 ω_o e
L5  ż_2 ← z_3 + 3 ω_o² e + b_0 u
L6  ż_3 ← ω_o³ e
L7  return ż
```

Lines L1 and L2 cancel the estimate $z_3$ of $F$ and apply PD with both poles at $-\omega_c$. Lines L3 to L6 are the observer of the extended state, with the gains $(3 \omega_o, 3 \omega_o^2, \omega_o^3)$ that put all three of its poles at $-\omega_o$. In a sampled implementation, the control is computed at each sample and held, and the observer is integrated over the sample period, or replaced by a discrete observer obtained by [zero-order hold discretization](/zero-order-hold-discretization/).

## Example

The plant is $\ddot y = -y - 0.5 \dot y + d(t) + 2 u$ with a step disturbance $d = 1$ for $t \ge 5$. The controller knows none of this, except $b_0 = 1.5$ (the true $b$ is $2$). The reference is $r = 1$, $\omega_c = 2$ (so $u_0 = 4 (r - z_1) - 4 z_2$), and $\omega_o = 10$, all states start at $0$. The simulation uses 4th order Runge-Kutta with step $0.002$, with the control computed once per step and held.

| $t$ | $y$ | $z_3$ |
|---|---|---|
| 0.5 | 0.26861 | -0.04604 |
| 1 | 0.55035 | -0.55420 |
| 2 | 0.87203 | -0.76846 |
| 3 | 0.97251 | -0.76831 |
| 5 | 0.99981 | -0.75163 |
| 5.5 | 1.04458 | -0.14171 |
| 6 | 1.04424 | -0.07094 |
| 8 | 1.00524 | 0.00093 |
| 10 | 1.00016 | 0.00027 |

At rest at $y = 1$ the plant needs $u = (1 - d)/2$, so the total disturbance is $F = -1 + 0.5 u$: $-0.75$ before the step and $0$ after it. The estimate $z_3$ follows these values. After the step, $y$ moves away from $1$ by at most $0.0477$ and returns, with no steady error. The first control is $u(0) = 4 / 1.5 = 2.667$.

The ideal response is that of the PD loop, $y = 1 - (1 + 2t) e^{-2t}$. The largest deviation from it on $[0, 5)$ is $0.0514$ for $\omega_o = 10$, $0.0241$ for $\omega_o = 20$ and $0.0113$ for $\omega_o = 40$ (measurement): it falls roughly like $1/\omega_o$.

## Correctness

The full proof is in proofs/correctness.md. Its main steps:

- **Lemma (observer error).** The error $e = x - z$ obeys $\dot e_1 = e_2 - 3 \omega_o e_1$, $\dot e_2 = e_3 - 3 \omega_o^2 e_1$, $\dot e_3 = \dot F - \omega_o^3 e_1$, for any control. The tests check it exactly.
- **Theorem (size of the error).** If $|\dot F| \le M$ along the motion, then after a transient, $|e_3| = O(M / \omega_o)$, $|e_2| = O(M / \omega_o^2)$, $|e_1| = O(M / \omega_o^3)$. This is the bound of the high-gain observer with $\varepsilon = 1/\omega_o$.
- **Theorem (perturbed PD loop).** $\tilde y = y - r$ obeys $\ddot{\tilde y} + 2 \omega_c \dot{\tilde y} + \omega_c^2 \tilde y = e_3 + 2 \omega_c e_2 + \omega_c^2 e_1$ exactly, so the deviation from the PD loop is at most $\sup |e_3 + 2 \omega_c e_2 + \omega_c^2 e_1| / \omega_c^2$ after the transient.
- **Theorem (separation).** With $f = 0$ and $b = b_0$, the closed loop has the poles $-\omega_c$ (twice) and $-\omega_o$ (three times). The tests check this exactly for random values.
- **Theorem (exact rejection).** For a linear plant with a constant disturbance, if the closed loop is Hurwitz, then $y \to r$, because $z_3$ acts as an integrator. For the example, the [Routh-Hurwitz criterion](/routh-hurwitz-criterion/) confirms that the loop is Hurwitz, exactly.

The bound $|\dot F| \le M$ is not free when $b \neq b_0$, since $F$ contains $u$. For linear plants it follows from the Hurwitz test; for nonlinear plants, Guo and Zhao (2011) prove convergence under bounds on $f$, its derivatives and $b - b_0$.

## Complexity

Count real operations at unit cost, as in the real RAM. For a plant of order $n$, the observer has $n + 1$ states, and one evaluation of the control law and the observer costs $O(n)$ operations and $O(n)$ space. The observer poles are at $-\omega_o$, so an explicit integrator needs a step that is small compared with $1/\omega_o$; here $\omega_o h \le 0.08$.

## Properties

- **Little model needed.** Only the order and $b_0$; the rest is estimated. A wrong $b_0$ is absorbed into $F$. In the example, with $b_0 = 1.5$, the loop is Hurwitz for $b = 1/100$ and $b = 8$ and not for $b = 8.5$ (theorem, by the exact Routh test); a bisection puts the limit near $b = 8.01$ (measurement). The gain error it tolerates is not symmetric.
- **Integral action built in.** The estimate $z_3$ integrates the output error, so constant disturbances are rejected with zero steady error, like the I term of a [PID controller](/pid-controller/).
- **Two parameters.** $\omega_c$ sets the speed of the response; $\omega_o$ sets how fast disturbances are estimated. The noise in $u$ grows with $\omega_o$.
- **Asymptotic, not exact, for varying disturbances.** A disturbance that changes leaves an error of order $|\dot F| / \omega_o$ in the estimate.
- **Linear for linear plants.** The linear form is a linear controller of order $n + 1$ for the plant, which can be analyzed with transfer functions.

## Variants and improvements

- **Nonlinear ADRC.** Han's original form replaces the linear gains by nonlinear functions of the error with a fractional power near zero, and adds a tracking differentiator that shapes the reference. It can give faster convergence with smaller gains but has more parameters.
- **Higher order.** For $y^{(n)} = f + b u$ the observer has $n + 1$ states with gains from $(s + \omega_o)^{n+1}$, and the control is a state feedback with poles at $-\omega_c$.
- **Discrete and sampled forms.** A discrete observer, a prediction of one sample, or a current estimator for systems with delay.
- **Models in the observer.** If part of $f$ is known, add it to line L5, so the observer only estimates the rest. This makes $F$ and $\dot F$ smaller.
- **Generalized observers.** More integrators in the extended state, for disturbances that are ramps or polynomials in time, or a sliding mode observer in place of the high-gain one.

## When to use it

Use it for plants of known order with large uncertainty in the dynamics and slowly changing disturbances, where a model is costly and [PID](/pid-controller/) tuning is not good enough, such as motion control, motors and process control. Compared with a [disturbance observer](/disturbance-observer/) built around a nominal model, it needs less model. If the plant has a good model and the disturbance has a known form, use the [internal model principle](/internal-model-principle/) or model based design instead. If the measurement noise is large, the observer bandwidth must stay low, and the benefit shrinks.

## Pitfalls

- **Peaking at the start.** If $z(0)$ is far from the state, the observer estimates at lines L4 to L6 have a large transient and $u$ peaks. Start with $z_1(0) = y(0)$, or limit $u$, or raise $\omega_o$ gradually.
- **Wrong sign of b0.** Line L2 then adds the disturbance instead of cancelling it, and the loop is unstable.
- **Too large a gain error.** The loop tolerates only a range of $b / b_0$; in the example, about $5.3$ at most. Check it on the linearized loop.
- **Actuator limits.** When $u$ saturates, the cancellation at line L2 fails and $z_3$ keeps integrating, as in [integrator windup](/integrator-windup/). Feed the saturated $u$, not the computed one, to line L5.
- **Noise and sampling.** The noise in $u$ grows with $\omega_o$ to a high power, and the sampling period must be small compared with $1/\omega_o$.
- **Not a model of F.** $z_3$ includes $(b - b_0) u$ and the unmodeled dynamics; it is not a measurement of the physical disturbance alone.

## Implementations

## History

Jingqing Han developed ADRC in China in the 1990s, as an alternative to PID that keeps its independence of models but estimates and cancels the disturbance actively. His English paper of 2009 summarizes the ideas: the tracking differentiator, the observer of the extended state, and nonlinear feedback. Zhiqiang Gao (2003) proposed the linear form in which all observer poles are placed at one bandwidth and all controller poles at another, which reduced tuning to the choice of two numbers. Guo and Zhao (2011) proved convergence of the observer and the closed loop for a class of nonlinear plants with uncertainty.

## References
