---
tag: WP3VZ0
kind: algorithm
slug: sliding-mode-control
name: Sliding mode control
aliases:
- variable structure control
area: control/nonlinear-control
level: core
summary: Drives the state to a surface on which the dynamics are as wanted, with a switching control that dominates matched uncertainty.
model: real-ram
complexity:
  vars: {n: the order of the system, q: the number of arithmetic operations to evaluate the nominal drift and the input gain once}
  time: {worst: "O(n + q)"}
  space: {extra: "O(1)"}
properties: {deterministic: true, exact: true, recursive: false, online: true}
history:
  year: 1977
  people: [Vadim I. Utkin, Stanislav V. Emelyanov, Aleksei F. Filippov]
  note: "Emelyanov's group in Moscow studied switching feedback from the late 1950s; Utkin's 1977 survey made sliding modes known in the West, and Filippov's theory of discontinuous differential equations gave the solutions a meaning."
prereqs: [control-affine-system, lyapunov-function, controllable-canonical-form]
see_also: [chattering, super-twisting-algorithm, sliding-mode-observer, feedback-linearization, backstepping, bang-bang-control, model-uncertainty, relay-autotuning]
sources:
  - paper: "V. I. Utkin, Variable structure systems with sliding modes, IEEE Transactions on Automatic Control 22(2), 212-222, 1977"
    title: Variable structure systems with sliding modes
    locator: the survey of sliding modes, the equivalent control and the invariance to matched disturbances
  - book: isbn:9783540535164
    title: Vadim I. Utkin, Sliding Modes in Control and Optimization, Springer, 1992
    locator: the equivalent control method and the conditions for the existence of a sliding mode
  - book: isbn:9789027726995
    title: A. F. Filippov, Differential Equations with Discontinuous Righthand Sides, Kluwer, 1988
    locator: the definition of solutions of differential equations with a discontinuous right side
  - book: isbn:9780130408907
    title: Jean-Jacques E. Slotine and Weiping Li, Applied Nonlinear Control, Prentice Hall, 1991
    locator: Chapter 7 (Sliding Control), the sliding condition, the reaching time and the boundary layer
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 14.1, Sliding mode control
  - book: isbn:9780748406012
    title: Christopher Edwards and Sarah K. Spurgeon, Sliding Mode Control, Theory and Applications, Taylor and Francis, 1998
    locator: the introductory chapters on the sliding surface, the reaching condition and matched uncertainty
---

Sliding mode control is a feedback design for systems with uncertain models. It picks a surface $s(x) = 0$ in the state space on which the motion is the one you want, and a switching control that pushes the state onto the surface from both sides and then holds it there. The switching gain is chosen larger than a bound on the uncertainty, so any uncertainty that enters through the same channel as the input (matched uncertainty) has no effect on the motion along the surface. The price is a discontinuous control, which in a real loop causes [chattering](/chattering/).

## In plain words

Think of a car that you want to keep on the center line of a road with gusty side wind. You do not try to model the wind. You only decide which side of the line you are on, and steer hard back toward it. If your steering is stronger than the strongest gust, you reach the line in a known time and then stay on it, with the steering flipping left and right very fast. While you ride the line, the car behaves the way the line was designed to make it behave, and the wind does not matter. The design has two parts: choose a good line, and make the push toward it strong enough. The fast flipping is the weak point, because a real steering system cannot switch infinitely fast.

## The problem

**Input.** A system of order $n$ in [controllable canonical form](/controllable-canonical-form/),

$$\dot x_i = x_{i+1} \quad (i = 1, \dots, n - 1), \qquad \dot x_n = f(x) + b(x)\, u + d(t, x),$$

with a scalar input $u$, a known nominal model $\hat f$ of $f$, a known input gain $b(x) \neq 0$, and an unknown term $\delta = f - \hat f + d$ with a known bound $|\delta(t, x)| \le D$. This is a [control-affine system](/control-affine-system/) $\dot x = F(x) + G(x) u$ in which the uncertainty enters through the input column $G$ (matched uncertainty). Also coefficients $c_1, \dots, c_{n-1}$ such that the polynomial $\lambda^{n-1} + c_{n-1} \lambda^{n-2} + \dots + c_1$ is Hurwitz, a gain margin $\eta > 0$ and a switching gain $k \ge D + \eta$.

**Output.** A feedback $u(x)$ such that every solution reaches the sliding surface

$$s(x) = c_1 x_1 + \dots + c_{n-1} x_{n-1} + x_n = 0$$

within time $|s(x(0))| / \eta$, stays on it afterwards, and then goes to $0$ exponentially, for every $\delta$ that satisfies the bound.

## The algorithm

```pseudo id=main
SLIDING-MODE-CONTROL(x, c, f̂, b, k, φ)
L1  s ← c_1 x_1 + ... + c_{n-1} x_{n-1} + x_n
L2  v ← -f̂(x) - (c_1 x_2 + ... + c_{n-1} x_n)
L3  if φ > 0 then σ ← sat(s / φ)
L4  else σ ← sgn(s)
L5  u ← (v - k σ) / b(x)
L6  return u, s
```

Line L1 computes the sliding variable. Line L2 is the nominal equivalent control: with $u = v / b$ and $\delta = 0$, the derivative $\dot s$ would be exactly $0$. Lines L3 and L4 choose the switching function: $\operatorname{sgn}$ gives the ideal sliding mode, and $\operatorname{sat}(z) = \max(-1, \min(1, z))$ with a layer width $\phi > 0$ gives the boundary layer version. Line L5 adds the switching term and divides by the input gain. Along the system,

$$\dot s = \sum_{i<n} c_i x_{i+1} + \hat f + \delta + b u = \delta - k \sigma(s).$$

A computer runs the algorithm at sampling instants and holds $u$ between them. The theory assumes that it runs continuously.

## Example

Take the double integrator with a sine disturbance, $\dot x_1 = x_2$, $\dot x_2 = u + 0.5 \sin 2t$, so $\hat f = 0$, $b = 1$ and $D = 0.5$. Choose $s = x_1 + x_2$ ($c_1 = 1$), $\eta = 1$ and $k = D + \eta = 1.5$. The algorithm gives

$$u = -x_2 - 1.5 \operatorname{sgn}(x_1 + x_2), \qquad \dot s = 0.5 \sin 2t - 1.5 \operatorname{sgn}(s).$$

From $x(0) = (1, 0)$, $s(0) = 1$, so the reaching time is at most $|s(0)| / \eta = 1$. On the surface $x_2 = -x_1$, so $\dot x_1 = -x_1$ and $x_1$ decays like $e^{-t}$, whatever the disturbance does. A 4th order Runge-Kutta simulation with step $h = 0.002$, with $u$ computed at the start of each step and held over the step, gives:

| $t$ | $x_1$ | $x_2$ | $s$ |
|---|---|---|---|
| 0 | 1 | 0 | 1 |
| 0.5 | 0.85762 | -0.49318 | 0.364431 |
| 1 | 0.56424 | -0.56077 | 0.003476 |
| 1.5 | 0.34247 | -0.34532 | -0.002847 |
| 2 | 0.20759 | -0.21039 | -0.002799 |
| 3 | 0.07594 | -0.07406 | 0.001883 |
| 4 | 0.02827 | -0.02593 | 0.002349 |
| 6 | 0.00336 | -0.00233 | 0.001034 |

The sliding variable first reaches $0$ at $t = 0.858$, before the bound $1$. After that, $|s| \le 0.00399$, and the switching term changes sign 365 times in the 500 steps between $t = 2$ and $t = 3$. With $h = 0.001$ the band is $0.00200$. The simulation shows chattering of the size of the step: the band is $(k + D) h = 2h$ up to a term of order $h^2$, and it is an effect of the sampling, not of the ideal law. With the boundary layer $\phi = 0.05$ the control has no jumps, and $|s|$ stays below $\phi D / k = 0.0167$ (the measured maximum after $t = 2$ is $0.0166$).

## Correctness

The full proof is in proofs/correctness.md. Its main steps:

- **The sliding variable obeys $\dot s = \delta - k \sigma(s)$.** This is algebra: line L2 cancels the known part of $\dot s$ and line L5 divides out $b$.
- **Theorem (reaching).** With $\sigma = \operatorname{sgn}$ and $k \ge D + \eta$, $s \dot s \le -\eta |s|$ wherever $s \neq 0$ (the reaching condition). So $|s|$ decreases at rate at least $\eta$ and reaches $0$ before $t = |s(0)| / \eta$.
- **Theorem (invariance).** Solutions are understood in the sense of Filippov. After $s$ reaches $0$ it cannot leave, because on any interval where $s \neq 0$ the function $|s|$ decreases.
- **Theorem (sliding motion).** On $s = 0$, $x_n = -\sum c_i x_i$, so $(x_1, \dots, x_{n-1})$ obeys a linear system in companion form with characteristic polynomial $\lambda^{n-1} + c_{n-1} \lambda^{n-2} + \dots + c_1$. That polynomial is Hurwitz, so the reduced state goes to $0$ exponentially, and $\delta$ does not appear in the reduced system.
- **Theorem (boundary layer).** With $\sigma = \operatorname{sat}(s / \phi)$, the state enters the layer $|s| \le \phi$ in finite time, and then $|s|$ goes exponentially to the band $|s| \le \phi D / k$. The state is then ultimately bounded, not convergent.
- **Theorem (sampling).** If the switching term is held over steps of length $h$, the band $|s| \le (k + D) h$ is reached in finite time and is never left.

The tests check the identity $\dot s = \delta - k \sigma(s)$ and the reaching condition exactly in Fraction for 200 random systems with $n = 1$ to $4$, the table above, the reaching time, the band $2h$ for $h = 0.002$ and $h = 0.001$, the boundary layer bound, and a third order system with $b(x) = 2 + \cos x_1$ and $s = 2 x_1 + 3 x_2 + x_3$.

## Complexity

Count real operations at unit cost, as in the real RAM. Let $q$ be the cost to evaluate $\hat f$ and $b$ once. Lines L1 and L2 take $O(n)$ operations each, and the rest is $O(1)$, so one evaluation costs $O(n + q)$ time and $O(1)$ extra space. A simulation with $N$ steps and a held control evaluates the algorithm $N$ times; a simulation that evaluates it inside the right side evaluates it $4N$ times with RK4.

## Properties

- **Robust to matched uncertainty.** Any $\delta$ with $|\delta| \le D$ is rejected on the surface, without a model of $\delta$. This is an invariance property, not only robustness.
- **Not robust to unmatched uncertainty.** A term that enters $\dot x_i$ for $i < n$ is not in the input channel, and the switching cannot cancel it. It changes the motion on the surface.
- **Finite-time reaching.** The surface is reached in finite time, with a bound that depends only on $|s(0)|$ and $\eta$.
- **Reduced order motion.** On the surface the system has order $n - 1$, and its dynamics are set by the $c_i$ alone, as in [pole placement](/pole-placement-problem/) for a system of order $n - 1$.
- **Discontinuous.** The control jumps on $s = 0$. The closed loop is a differential equation with a discontinuous right side, and classical existence and uniqueness results such as the [Picard-Lindelöf theorem](/picard-lindelof-theorem/) do not apply. Filippov's theory gives the solutions.

## Variants and improvements

- **Boundary layer.** Replace $\operatorname{sgn}$ by $\operatorname{sat}(s / \phi)$ (line L3). The control is continuous, and the exact sliding becomes the bound $|s| \le \phi D / k$ (Slotine and Li 1991, Chapter 7).
- **State-dependent gain.** If the bound $D(x)$ depends on the state, use $k(x) \ge D(x) + \eta$. This keeps the gain small where the uncertainty is small and reduces the chattering.
- **Uncertain input gain.** If only bounds $0 < b_{\min} \le b(x) \le b_{\max}$ are known, divide by an estimate $\hat b$ and raise $k$ to cover the ratio $b / \hat b$ (Slotine and Li 1991, Chapter 7).
- **Integral sliding mode.** Add an integral term to $s$ so that the sliding mode starts at $t = 0$ and the reaching phase disappears.
- **Terminal sliding mode.** A nonlinear surface such as $x_2 + c |x_1|^{1/2} \operatorname{sgn}(x_1) = 0$ makes the motion on the surface reach the origin in finite time too.
- **Higher order sliding modes.** The [super-twisting algorithm](/super-twisting-algorithm/) acts on $\dot u$ instead of $u$, gives a continuous control and rejects disturbances with a bounded derivative.
- **Observers.** The same idea, with the switching term in an observer, gives the [sliding mode observer](/sliding-mode-observer/).

## When to use it

Use it when the model has large matched uncertainty with a known bound, when you need a guaranteed reaching time, and when the actuator can tolerate fast switching or a boundary layer is acceptable. It suits electric drives and power converters, where the actuator is a switch anyway, and robot joints with friction and payload uncertainty. If the model is accurate, [feedback linearization](/feedback-linearization/) or [backstepping](/backstepping/) give smooth controls with fewer tuning trade-offs. If the actuator is slow or the plant has light resonances that the switching can excite, prefer a smooth robust design, or use the super-twisting algorithm. If the uncertainty is unmatched, the method alone is not enough.

## Pitfalls

- **Gain too small at line L5.** If $k < D$ at some time, the reaching condition fails, and $s$ can move away from the surface. The bound $D$ must cover the worst case of the model error and the disturbance together.
- **Gain too large at line L5.** The size of the chattering grows with $k$. A gain far above $D + \eta$ wastes actuator effort and excites fast unmodeled dynamics.
- **Wrong surface at line L1.** If the polynomial in the $c_i$ is not Hurwitz, the state reaches the surface and then diverges along it.
- **Small b(x) at line L5.** The control is divided by $b(x)$, so it becomes large where $b$ is small. If $b$ changes sign, the method fails.
- **Hidden chattering in simulation.** A fixed step simulation of the discontinuous law shows chattering of the size of the step. A variable step solver can become very slow near $s = 0$ or report a wrong smooth result. State the step with every result.
- **Relative degree.** The construction needs the input to appear in $\dot s$. If $s$ has relative degree two or more with respect to $u$, $u$ does not appear in $\dot s$, and the design fails; choose $s$ so that its relative degree is one.

## Implementations

## History

Switching feedback with sliding motions was studied from the late 1950s in the Soviet Union, in the group of Stanislav Emelyanov in Moscow, with Vadim Utkin as a main contributor. Utkin's 1977 survey in IEEE Transactions on Automatic Control presented the equivalent control and the invariance to matched disturbances to a Western audience, and his 1992 book gave the full theory. Aleksei Filippov's work on differential equations with discontinuous right sides, collected in his 1988 book, gave the solutions of the closed loop a precise meaning. Slotine (1984) introduced the boundary layer to trade exactness for a continuous control, and Levant (1993) started the line of higher order sliding modes.

## References
