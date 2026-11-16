---
tag: Y06X09
kind: theorem
slug: lqr-stability-margins
name: LQR stability margins
aliases:
- return difference inequality
- Kalman inequality
area: control/optimal-and-predictive-control
level: advanced
summary: "For continuous-time LQR with one input, |1 + L(j omega)| >= 1, so the loop has gain margin (1/2, infinity) and phase margin at least 60 degrees."
prereqs: [infinite-horizon-lqr, gain-margin, phase-margin, nyquist-stability-criterion]
see_also: [lqg-guaranteed-margins-counterexample, loop-transfer-recovery, sensitivity-function, kalman-yakubovich-popov-lemma, circle-criterion, continuous-algebraic-riccati-equation, discrete-algebraic-riccati-equation, lqr-problem]
sources:
  - paper: doi:10.1115/1.3653115
    title: R. E. Kalman, When is a linear control system optimal?, Journal of Basic Engineering 86(1), 51-60, 1964
    locator: Theorem 6, a stable single-input control law is optimal if and only if its return difference has modulus at least one at all frequencies
  - paper: doi:10.1109/TAC.1977.1101470
    title: Michael G. Safonov and Michael Athans, Gain and phase margin for multiloop LQG regulators, IEEE Transactions on Automatic Control 22(2), 173-179, 1977
    locator: the gain and phase margins of multiloop linear quadratic state feedback regulators
  - book: isbn:9780486457666
    title: Brian D. O. Anderson and John B. Moore, Optimal Control, Linear Quadratic Methods, Prentice Hall, 1990 (Dover reprint, 2007)
    locator: the chapters on the properties of regulators, with the return difference equality and the gain and phase margins
---

A continuous-time [LQR](/infinite-horizon-lqr/) state feedback loop is robust without any design for robustness. Kalman (1964) showed that the return difference $1 + L(j\omega)$ of a single-input LQR loop has modulus at least one at every frequency. The Nyquist plot of the loop gain therefore stays out of the unit disk centered at $-1$. From this follow the guaranteed margins: the closed loop stays stable when the loop gain is multiplied by any factor in $(1/2, \infty)$, and the [phase margin](/phase-margin/) is at least 60 degrees. Safonov and Athans (1977) showed that the same margins hold in every input channel at the same time when $R$ is diagonal. The result is for continuous-time state feedback only. It is false for discrete-time LQR, and Doyle (1978) showed that an [LQG](/lqg-control/) loop with an observer has no guaranteed margins at all; see the [LQG counterexample](/lqg-guaranteed-margins-counterexample/).

## Statement

**Data.** $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$, $Q = Q^T \ge 0$, $R = R^T > 0$, with $(A, B)$ stabilizable and $(Q^{1/2}, A)$ detectable. Let $P$ be the stabilizing solution of the [CARE](/continuous-algebraic-riccati-equation/) $A^T P + P A - P B R^{-1} B^T P + Q = 0$ and $K = R^{-1} B^T P$, so that $u = -K x$ is the optimal control. Break the loop at the plant input. The loop transfer matrix is $L(s) = K \Phi(s)$ with $\Phi(s) = (s I - A)^{-1} B$.

**Theorem.**

1. *Return difference equality.* For every $s$ that is not an eigenvalue of $A$ or $-A$,
$$\left(I + L(-s)\right)^T R \left(I + L(s)\right) = R + \Phi(-s)^T Q\, \Phi(s).$$
2. *Return difference inequality.* For real $\omega$ with $j\omega$ not an eigenvalue of $A$, $(I + L(j\omega))^* R (I + L(j\omega)) \ge R$. For one input ($m = 1$) this is $|1 + L(j\omega)| \ge 1$.
3. *Margins, one input.* For $m = 1$, the closed loop $\dot x = (A - \beta B K) x$ is stable for every real $\beta > 1/2$, and for every complex $\beta = e^{-j\varphi}$ with $|\varphi| < 60°$. So the [gain margin](/gain-margin/) is $(1/2, \infty)$ and the phase margin is at least 60 degrees.
4. *Margins, several inputs.* If $R$ is diagonal, $A - B \Delta K$ is Hurwitz for every real diagonal $\Delta = \operatorname{diag}(\beta_1, \dots, \beta_m)$ with all $\beta_i > 1/2$: each channel can change its gain independently.

## In plain words

The optimal state feedback cannot be fragile. If the actuator turns out to be half as strong as modeled, or arbitrarily stronger, or adds up to 60 degrees of phase lag at the crossover, the loop is still stable. The reason is that the optimal loop never makes the return difference smaller than one, so the loop gain never comes close to $-1$. A designer gets these margins for any choice of the weights $Q$ and $R$, as long as all states are measured.

## Proof

*Part 1.* Since $P B = K^T R$, we have $P B R^{-1} B^T P = K^T R K$, and the CARE reads $-A^T P - P A = Q - K^T R K$. Add and subtract $s P$:
$$(-s I - A^T) P + P (s I - A) = Q - K^T R K.$$
Multiply by $\Phi(-s)^T = B^T (-s I - A^T)^{-1}$ on the left and by $\Phi(s) = (s I - A)^{-1} B$ on the right:
$$B^T P\, \Phi(s) + \Phi(-s)^T P B = \Phi(-s)^T Q\, \Phi(s) - \Phi(-s)^T K^T R K\, \Phi(s).$$
With $B^T P = R K$ the left side is $R L(s) + L(-s)^T R$, and the last term is $-L(-s)^T R L(s)$. Move it to the left and add $R$ to both sides. The left side becomes $(I + L(-s))^T R (I + L(s))$, which is part 1.

*Part 2.* Put $s = j\omega$. As $A$, $B$ and $K$ are real, $L(-j\omega)^T = L(j\omega)^*$ and $\Phi(-j\omega)^T = \Phi(j\omega)^*$. So the right side is $R + \Phi^* Q \Phi \ge R$. For $m = 1$, $R = r > 0$ is a number and $r |1 + L(j\omega)|^2 \ge r$.

*Part 3.* Let $m = 1$, $a(s) = \det(s I - A)$ and $b(s) = K \operatorname{adj}(s I - A) B$, so $L = b / a$. By the determinant formula for a rank one update, the closed loop polynomial is
$$p_\beta(s) = \det(s I - A + \beta B K) = a(s) + \beta\, b(s).$$
It is monic of degree $n$ for every complex $\beta$, so its roots depend continuously on $\beta$. For $\beta = 1$ all roots are in the open left half plane, because $P$ is stabilizing. Take a path of values of $\beta$ from 1 to the target value: the real segment from 1 to $\beta > 1/2$, or the arc $e^{-j\theta}$, $\theta$ between 0 and $\varphi$. A root can leave the left half plane only by passing through a point $j\omega$ of the imaginary axis, so it suffices to show $p_\beta(j\omega) \ne 0$ for all $\beta$ on the path and all real $\omega$.

Suppose $p_\beta(j\omega) = 0$. If $a(j\omega) = 0$, then $b(j\omega) = 0$ (as $\beta \ne 0$), so $p_1(j\omega) = 0$, which is false. So $a(j\omega) \ne 0$ and $L(j\omega) = -1/\beta$. Then part 2 gives $|1 - 1/\beta| \ge 1$. For real $\beta > 1/2$ we have $0 < 1/\beta < 2$, so $|1 - 1/\beta| < 1$. For $\beta = e^{-j\theta}$ with $|\theta| < 60°$ we have $|1 - e^{j\theta}| = 2 |\sin(\theta / 2)| < 1$. Both contradict part 2. Hence the roots stay in the left half plane along the path.

*Part 4.* Let $A_\Delta = A - B \Delta K$. With $P B = K^T R$,
$$A_\Delta^T P + P A_\Delta = A^T P + P A - K^T (\Delta R + R \Delta) K = -Q - K^T (\Delta R + R \Delta - R) K.$$
As $R$ and $\Delta$ are diagonal, $\Delta R + R \Delta - R = \operatorname{diag}((2 \beta_i - 1) r_i)$, which is positive definite when all $\beta_i > 1/2$. Let $A_\Delta v = \lambda v$ with $v \ne 0$ and $\operatorname{Re} \lambda \ge 0$. Then $2 \operatorname{Re}(\lambda)\, v^* P v = -v^* Q v - (K v)^* (\Delta R + R \Delta - R) (K v)$. The left side is at least 0 because $P \ge 0$, and the right side is at most 0, so $Q v = 0$ and $K v = 0$. Then $A v = A_\Delta v = \lambda v$ with $Q v = 0$, which detectability excludes. So $A_\Delta$ is Hurwitz. The same computation with $m = 1$ gives a second proof of the gain part of part 3. $\blacksquare$

## Consequences

### A check by hand

Double integrator, $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, $Q = I$, $R = 1$. The optimal gain is $K = \begin{bmatrix} 1 & \sqrt 3 \end{bmatrix}$, and $\Phi(s) = \begin{bmatrix} 1/s^2 \\ 1/s \end{bmatrix}$, so
$$L(s) = \frac{\sqrt 3\, s + 1}{s^2}, \qquad 1 + L(s) = \frac{s^2 + \sqrt 3\, s + 1}{s^2}.$$
At $s = j\omega$, $|1 + L|^2 = ((1 - \omega^2)^2 + 3 \omega^2) / \omega^4 = 1 + (1 + \omega^2)/\omega^4$, and $\Phi^* Q \Phi = 1/\omega^4 + 1/\omega^2$ is the same excess, as part 1 says. At $\omega = 1$ both sides are 3; at $\omega = 2$ both are $1.3125$. The loop gain is 1 where $\omega^4 = 3 \omega^2 + 1$, at $\omega \approx 1.8174$, and there the phase of $L$ is $-107.6°$: the phase margin is $72.4°$. The closed loop polynomial with gain $\beta$ is $s^2 + \sqrt 3 \beta s + \beta$, stable for every $\beta > 0$, so the true gain margin here is larger than the guarantee.

A small script checks the identity at many frequencies:

```python
import math
for w in [0.1, 0.5, 1.0, 2.0, 10.0]:
    s = 1j * w
    L = (math.sqrt(3) * s + 1) / s**2
    lhs = abs(1 + L) ** 2
    rhs = 1 + abs(1 / s**2) ** 2 + abs(1 / s) ** 2
    assert abs(lhs - rhs) <= 1e-9 * rhs and lhs >= 1
```

### What follows from the inequality

- **Sensitivity.** For $m = 1$ the [sensitivity function](/sensitivity-function/) $S = 1/(1 + L)$ satisfies $|S(j\omega)| \le 1$ at all frequencies, so the LQR state feedback loop does not amplify a disturbance at the plant input at any frequency.
- **Nonlinear and time-varying gains.** The Lyapunov computation of part 4 does not need constant gains. If each channel gain varies with time or with the state but stays in $[1/2 + \epsilon, \infty)$, then $V = x^T P x$ still does not increase along trajectories. Safonov and Athans state margins of this kind for memoryless nonlinear time-varying gains. This ties the result to the [circle criterion](/circle-criterion/).
- **Inverse optimality.** Kalman's paper proves the converse too: a stable single-input state feedback whose return difference has modulus at least one is optimal for some $Q \ge 0$.
- **Recovery.** Observers destroy the margins in general. [Loop transfer recovery](/loop-transfer-recovery/) tunes the [Kalman filter](/kalman-filter/) so that the LQG loop approaches the LQR loop and gets the margins back.

## Tightness

- **The lower limit $1/2$ is sharp.** Take $n = m = 1$, $a > 0$, $b = r = 1$. The CARE $2 a p - p^2 + q = 0$ gives $K = p = a + \sqrt{a^2 + q}$. The loop $a - \beta K$ is stable exactly for $\beta > a / K$, and $a / K \to 1/2$ as $q \to 0$. For $a = 1$, $q = 1$ the limit is $0.414$; for $q = 0.01$ it is $0.4988$.
- **60 degrees is sharp.** In the same example, $L(s) = K / (s - a)$ has $|L(j\omega)| = 1$ at $\omega = \sqrt{K^2 - a^2}$, and the phase margin is $\arctan(\omega / a)$. As $q \to 0$, $K \to 2 a$ and the margin tends to $\arctan \sqrt 3 = 60°$. For $a = 1$, $q = 0.01$ it is $60.08°$.
- **Discrete time has smaller margins.** For the [discrete-time](/discrete-algebraic-riccati-equation/) scalar plant $x_{k+1} = 2 x_k + u_k$ with $r = 1$ and $q \to 0$, the DARE gives $p = 3$ and $K = 1.5$. The loop $2 - 1.5 \beta$ is stable only for $2/3 < \beta < 2$, a finite upper gain margin. The discrete return difference identity has $R + B^T P B$ in place of $R$, and the margins depend on the data.
- **Several inputs need diagonal $R$.** For a general $R > 0$ the inequality of part 2 holds in the norm weighted by $R$, and the channel by channel margins of part 4 can fail. The proof of part 4 works for every real $\Delta$ with $\Delta R + R \Delta - R$ positive definite, which for diagonal $R$ and $\Delta$ means $\beta_i > 1/2$.
- **Output feedback.** The guarantee needs the full state. With an observer in the loop the margins can be arbitrarily small (Doyle 1978).

## History

Kalman (1964) asked when a given linear control law is optimal for a quadratic cost and found the answer in the frequency domain: for one input, exactly when the return difference has modulus at least one. The gain and phase margins that follow from it are standard textbook material, for example in Anderson and Moore. Safonov and Athans (1977) extended the margins to multiloop regulators, channel by channel. Doyle (1978) then showed with a short example that the margins do not carry over to LQG, which started the work on robust multivariable control and loop transfer recovery.

## References
