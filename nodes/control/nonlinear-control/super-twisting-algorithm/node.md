---
tag: QDH2NE
kind: algorithm
slug: super-twisting-algorithm
name: Super-twisting algorithm
aliases:
- second-order sliding mode
- super-twisting controller
area: control/nonlinear-control
level: advanced
summary: A sliding mode law whose switching acts on the derivative of the control, so the control is continuous and the sliding variable and its derivative reach zero in finite time.
model: real-ram
complexity:
  vars: {N: the number of sampling instants}
  time: {worst: "O(N)"}
  space: {extra: "O(1)"}
properties: {deterministic: true, exact: false, recursive: false, online: true}
history:
  year: 1993
  people: [Arie Levant, Jaime A. Moreno, Marisol Osorio]
  note: "Levant (who earlier published as Levantovsky) introduced the super-twisting algorithm in 1993 among the sliding mode laws of order two, with a geometric proof of finite-time convergence; Moreno and Osorio gave a quadratic Lyapunov function for it in 2008 and 2012."
prereqs: [sliding-mode-control, chattering, lyapunov-direct-method]
see_also: [sliding-mode-observer, high-gain-observer, active-disturbance-rejection-control, pid-controller, backstepping, input-to-state-stability, lyapunov-function, describing-function]
sources:
  - paper: "A. Levant, Sliding order and sliding accuracy in sliding mode control, International Journal of Control 58(6), 1247-1263, 1993"
    title: Sliding order and sliding accuracy in sliding mode control
    locator: the definition of the super-twisting algorithm, its finite-time convergence, and the accuracy of order h^2 with sampling period h
  - paper: doi:10.1016/S0005-1098(97)00209-4
    title: "A. Levant, Robust exact differentiation via sliding mode technique, Automatica 34(3), 379-384, 1998"
    locator: the use of the super-twisting algorithm as an exact differentiator with a bound on the second derivative of the signal
  - paper: doi:10.1109/TAC.2012.2186179
    title: "J. A. Moreno and M. Osorio, Strict Lyapunov functions for the super-twisting algorithm, IEEE Transactions on Automatic Control 57(4), 1035-1040, 2012"
    locator: the quadratic form in the coordinates (|s|^(1/2) sgn s, v) and the finite-time estimate
  - book: isbn:9780748406012
    title: Christopher Edwards and Sarah K. Spurgeon, Sliding Mode Control, Theory and Applications, Taylor and Francis, 1998
    locator: the background on sliding modes, the reaching condition and matched uncertainty
---

The super-twisting algorithm is a continuous sliding mode law for a sliding variable $s$ whose derivative is $\dot s = u + d(t)$, where $d$ is an unknown disturbance with a bounded derivative, $|\dot d| \le L$. It uses the control

$$u = -k_1 |s|^{1/2} \operatorname{sgn}(s) + w, \qquad \dot w = -k_2 \operatorname{sgn}(s).$$

The switching acts on $\dot w$, not on $u$, so $u$ is a continuous function of time. For gains that are large enough compared with $L$, both $s$ and $\dot s$ reach $0$ in finite time, and the integral term $w$ then equals $-d$ exactly. Compared with the first order law of [sliding mode control](/sliding-mode-control/), it removes the discontinuity of the control and reduces [chattering](/chattering/), at the price of a stronger assumption on $d$.

## In plain words

A plain sliding mode controller pushes with full force left or right, so its output jumps all the time. The super-twisting controller has two parts. One part pushes back with a force that grows with the square root of the error, so it is strong far away and soft near the target. The other part slowly builds up a correction, like the integral part of a PID controller, but it changes at a fixed rate in the direction of the error. This slow part learns the unknown disturbance and cancels it. Because the jumps happen only in the rate of the slow part, the output itself is smooth. The controller still reaches the target exactly in a finite time, as long as the disturbance does not change too fast.

## The problem

**Input.** A measured sliding variable $s(t)$ with $\dot s = u + d(t)$, where $d$ is unknown, absolutely continuous, and $|\dot d(t)| \le L$ for almost every $t$. A sampling period $h > 0$. Gains $k_1 > 0$ and $k_2 > 0$.

**Output.** At each sampling instant $t_j = j h$, a control value $u_j$, held over $[t_j, t_{j+1})$, such that in the continuous-time limit $s = \dot s = 0$ after a finite time, and with sampling $|s| = O(h^2)$ and $|\dot s| = O(h)$ after a finite time.

The sliding variable usually comes from a surface $s = \sigma(x)$ of relative degree one with respect to the input, as in [sliding mode control](/sliding-mode-control/). Then $d$ collects the known part of $\dot s$ that is not cancelled, and the uncertainty, and the condition $|\dot d| \le L$ must hold along the motion.

## The algorithm

```pseudo id=main
SUPER-TWISTING-STEP(s, w, k_1, k_2, h)
L1  u ← -k_1 |s|^{1/2} sgn(s) + w
L2  w ← w - h k_2 sgn(s)
L3  return u
```

The state $w$ starts at $w_0$ (often $0$) and is kept between calls. Line L1 computes the control from the current sample and the current integral state. Line L2 advances the integral state by one explicit Euler step of $\dot w = -k_2 \operatorname{sgn}(s)$. Line L3 returns the control, which is held until the next sample.

In continuous time, put $v = w + d$, so that

$$\dot s = -k_1 |s|^{1/2} \operatorname{sgn}(s) + v, \qquad \dot v = -k_2 \operatorname{sgn}(s) + \dot d(t).$$

At $s = 0$ the right side is discontinuous, and solutions are taken in the sense of Filippov. The pair $(s, v)$ reaches $(0, 0)$ in finite time, and $v = 0$ means $w = -d$.

## Example

Let $\dot s = u + \sin t$, so $L = 1$, with $s(0) = 1$, $w_0 = 0$, $k_1 = k_2 = 2$ and $h = 0.01$. The plant is integrated with 4th order Runge-Kutta with step $h$, and the control is computed at the start of each step and held. The certificate below holds, because $k_2 = 2 > L + 2L^2 / k_1^2 = 1.5$.

| $t$ | $s$ | $w$ | $-d(t)$ |
|---|---|---|---|
| 0.5 | 0.151849 | -1.00 | -0.479426 |
| 1 | 0.002585 | -0.76 | -0.841471 |
| 1.5 | -0.000131 | -1.00 | -0.997495 |
| 2 | 0.000023 | -0.92 | -0.909297 |
| 3 | -0.000031 | -0.16 | -0.141120 |
| 4 | -0.000063 | 0.76 | 0.756802 |

Measurements from this run and two more:

- $|s| \le 0.05$ for good from $t = 0.59$.
- For $t \ge 6$, the maximum of $|s|$ is $4.35 \cdot 10^{-4}$ for $h = 0.01$, $1.33 \cdot 10^{-4}$ for $h = 0.005$ and $2.97 \cdot 10^{-5}$ for $h = 0.0025$, that is between $4.3 h^2$ and $5.3 h^2$. The accuracy is of order $h^2$, as the theory says.
- $w$ follows $-\sin t$ within $0.045$ for $t \ge 6$. It moves by $h k_2 = 0.02$ per step, so it can only follow in steps of that size.
- For comparison, the first order law $u = -1.5 \operatorname{sgn}(s)$ with the same $h$ keeps $|s| \le 0.0235$, about 50 times larger, and its control jumps by $3$ at almost every step.

The Lyapunov bound on the convergence time for these gains is $132.98$, far above the measured time below $1$. The bound is a guarantee, not an estimate.

## Correctness

The full proof is in proofs/correctness.md. Its main steps:

- **Coordinates.** With $\zeta = (|s|^{1/2} \operatorname{sgn}(s), v)$ and $s \neq 0$, the closed loop is $\dot \zeta = |\zeta_1|^{-1} A(\theta) \zeta$ with $A(\theta) = \begin{bmatrix} -k_1/2 & 1/2 \\ -k_2 + \theta L & 0 \end{bmatrix}$, where $\theta = \dot d \operatorname{sgn}(s) / L \in [-1, 1]$.
- **Theorem (Lyapunov function).** Let $V = \zeta^T P \zeta$ with $P = \begin{bmatrix} 2k_2 + k_1^2/2 & -k_1/2 \\ -k_1/2 & 1 \end{bmatrix}$ (the matrix of Moreno and Osorio). Then $\dot V = -|\zeta_1|^{-1} \zeta^T Q(\theta) \zeta$, with $\det Q(\theta) = k_1^2 k_2 / 2 - \theta L k_1^2 / 2 - \theta^2 L^2$. If $k_2 > L + 2L^2 / k_1^2$, then $Q(\theta)$ is positive definite for every $\theta \in [-1, 1]$.
- **Theorem (finite time).** Under that condition, $\dot V \le -q \lambda_{\max}(P)^{-1/2} V^{1/2}$, where $q$ is the smaller of the least eigenvalues of $Q(1)$ and $Q(-1)$, so $V$ reaches $0$ before $T = 2 \lambda_{\max}(P)^{1/2} V(0)^{1/2} / q$. The set $s = 0$, $v \neq 0$ is crossed, not followed, so it does not break the argument.
- **Theorem (necessity).** If $k_2 < L$, no gain $k_1$ works: for $\dot d = L$, staying on $s = 0$ needs $v = 0$, but $\dot v \ge L - k_2 > 0$ there.
- **Theorem (accuracy with sampling).** With sampling period $h$, $|s| = O(h^2)$ and $|\dot s| = O(h)$ after a finite time (Levant 1993). The tests measure the factor in front of $h^2$.

The tests check the identity $Q(\theta) = -(A^T P + P A)$ and the formula for $\det Q$ exactly in Fraction for 200 random gains, the identity $\dot V = -|\zeta_1|^{-1} \zeta^T Q \zeta$ exactly at 200 random points, the table, the $h^2$ accuracy for three periods, the comparison with the first order law, the rule of thumb gains, and the failure for $k_2 < L$.

## Complexity

Count real operations at unit cost, with the square root as one operation, as in the real RAM. Each sample costs $O(1)$ time: one square root, one sign, and a few products and sums. The state is the single number $w$, so the extra space is $O(1)$. A run of $N$ samples costs $O(N)$ time.

## Properties

- **Continuous control.** $u$ is a continuous function of $s$ and $w$, and $w$ is continuous in time. The jump happens in $\dot w$.
- **Finite-time convergence.** Both $s$ and $\dot s$ reach $0$ in finite time. The bound from the Lyapunov function is conservative.
- **Exact disturbance estimate.** After convergence $w = -d$, so the algorithm also estimates the disturbance. This is why it serves as a differentiator and as an observer.
- **Homogeneity.** With the weights $2$ for $s$ and $1$ for $v$, the vector field is homogeneous of degree $-1$. This explains the finite-time convergence and the accuracy $O(h^2)$ and $O(h)$ (Levant 1993).
- **Needs the relative degree one.** $s$ must have relative degree one with respect to $u$. The algorithm does not need $\dot s$ to be measured.
- **Stronger assumption than first order sliding.** It needs a bound on $\dot d$, not on $d$. A disturbance that jumps is not covered.

## Variants and improvements

- **Rule of thumb gains.** The choice $k_1 = 1.5 \sqrt{L}$, $k_2 = 1.1 L$, which Levant (1998) uses for the differentiator, works well in practice. It is a rule of thumb, not a certificate: for $L = 1$ it fails the condition $k_2 > L + 2L^2/k_1^2 = 1.89$ of this page, but the example converges with it by $t = 0.92$.
- **Exact differentiator.** Run the algorithm on $s = z - f(t)$ with $\dot z = u$. Then $u$ converges to $\dot f$ in finite time when $|\ddot f| \le L$ (Levant 1998).
- **Observer.** The same law drives a [sliding mode observer](/sliding-mode-observer/) for mechanical systems, where it estimates the velocity from the position.
- **Linear terms.** Adding $-k_3 s$ to $u$ and $-k_4 s$ to $\dot w$ gives the generalized super-twisting algorithm, which handles disturbances that grow with $s$ and converges faster far from the surface. Moreno and Osorio's Lyapunov method extends to it.
- **Adaptive gains.** Gains that increase while the sliding mode is lost and decrease while it holds avoid a conservative $L$.
- **Higher order.** Laws of order three and more drive $s, \dot s, \ddot s, \dots$ to $0$ for a sliding variable of higher relative degree.

## When to use it

Use it when a first order [sliding mode controller](/sliding-mode-control/) would work but its switching control is not acceptable, and the disturbance is smooth enough that $|\dot d| \le L$ holds with a moderate $L$. It is a common choice in electric drives, hydraulic and pneumatic actuators and aircraft control, and as a robust differentiator. If the disturbance can jump, use the first order law or a boundary layer. If $d$ is smooth and well modeled, a linear observer with a [PID controller](/pid-controller/) or [active disturbance rejection control](/active-disturbance-rejection-control/) may be simpler to tune.

## Pitfalls

- **k_2 too small at line L2.** If $k_2 \le L$, the integral state cannot follow the disturbance, and $s$ drifts away (test case: $d = t$, $k_2 = 0.5$, and $s$ grows to $4.3$ by $t = 10$).
- **Large L from a crude bound.** The required gains grow with $L$, and with them the chattering. Use the smallest $L$ that the plant really has.
- **Relative degree two.** If $u$ enters $\ddot s$ and not $\dot s$, the algorithm does not apply. Use a different surface or an algorithm of higher order.
- **Integral windup at line L2.** With input limits, $w$ keeps growing while the actuator is saturated. Limit $w$ in the same way as in [anti-windup](/anti-windup/) schemes.
- **Unmodeled actuator dynamics.** A fast actuator still causes chattering, now in $\dot u$, of smaller size. The algorithm reduces chattering, it does not remove it.
- **Explicit Euler at line L2.** For large $h k_2$ the integral state moves in large steps. Choose $h$ so that $h k_2$ is small compared with the size of $d$.

## Implementations

## History

Arie Levant (who published earlier as Levantovsky) introduced the super-twisting algorithm in his 1993 paper on sliding order and sliding accuracy, among other laws that keep $s$ and $\dot s$ at zero. His proofs used the geometry of the phase plane, and he showed that sampling with period $h$ gives an accuracy of order $h^2$. In 1998 he used the same law as a robust exact differentiator, which made it popular in observers and output feedback. A Lyapunov function for the algorithm was missing until Moreno and Osorio presented a quadratic form in the coordinates $(|s|^{1/2} \operatorname{sgn} s, v)$ in 2008 and extended it to strict Lyapunov functions in 2012. This made the usual tools of Lyapunov analysis available, such as convergence time estimates and robustness margins.

## References
