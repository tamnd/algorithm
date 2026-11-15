---
tag: Z18B8C
kind: technique
slug: integral-state-feedback
name: State feedback with integral action
aliases:
- augmented integrator design
- servo state feedback
area: control/state-space-control
level: core
summary: Adds the integral of the tracking error as an extra state and places the poles of the augmented system, so constant errors go to zero.
history:
  year: 1976
  people: [Edward J. Davison]
  note: "Davison gave the existence conditions of the robust servomechanism problem in 1976. For constant references they reduce to the rank condition on this page."
prereqs: [state-feedback, pole-placement-theorem, steady-state-error]
see_also: [state-feedback, pid-controller, anti-windup, internal-model-principle, output-regulation-problem, transmission-zero, luenberger-observer, infinite-horizon-lqr]
sources:
  - paper: doi:10.1109/TAC.1976.1101137
    title: E. J. Davison, The robust control of a servomechanism problem for linear time-invariant multivariable systems, IEEE Transactions on Automatic Control 21(1), 25-34, 1976
    locator: the existence conditions of the robust servomechanism problem, with the rank condition at the eigenvalues of the exosystem
  - book: isbn:9780691193984
    title: Karl J. Åström and Richard M. Murray, Feedback Systems, An Introduction for Scientists and Engineers, second edition, Princeton University Press, 2021
    locator: Chapter 7, State Feedback (the section Integral Action)
  - book: isbn:9780195117776
    title: Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999
    locator: Section 8.3, Regulation and Tracking, with the robust tracking and disturbance rejection design of Section 8.3.1
  - book: isbn:9780134685717
    title: Gene F. Franklin, J. David Powell and Abbas Emami-Naeini, Feedback Control of Dynamic Systems, eighth edition, Pearson, 2019
    locator: Chapter 7, State-Space Design (integral control and robust tracking)
---

[State feedback](/state-feedback/) $u = -Kx + Nr$ gives zero steady-state error for a constant reference only when the model is exact and no disturbance acts. State feedback with integral action removes this weakness. It adds the integral of the tracking error as a new state, $\dot x_i = r - y$, and feeds back the augmented state:

$$u = -Kx - K_i x_i.$$

If the closed loop is asymptotically stable, every state converges for a constant reference and a constant disturbance, so $\dot x_i \to 0$ and $y \to r$. This holds even when the model used for the design is wrong, as long as the loop stays asymptotically stable. The design is pole placement or LQR for the augmented pair. It is the state-space form of integral action in a [PID controller](/pid-controller/), and the simplest case of the [internal model principle](/internal-model-principle/).

## In plain words

A controller that only looks at the present state can leave a small, steady error, for example when a constant load pushes against it or when the model is a little wrong. Integral action keeps a running total of the error. As long as any error is left, the total keeps growing and pushes the input harder. The loop can only come to rest when the error is exactly zero. State feedback with integral action treats this running total as one more state and chooses all the feedback weights together, so that the whole loop, the integrator included, settles as the designer wants.

## When it applies

- The plant is $\dot x = Ax + Bu + Ed$, $y = Cx$, with $x \in \mathbb{R}^n$, $u \in \mathbb{R}^m$, $y \in \mathbb{R}^p$, and the reference $r$ and the disturbance $d$ are constant or change slowly.
- The state is measured or estimated, for example by a [Luenberger observer](/luenberger-observer/). The integrator state $x_i$ is computed by the controller, so it is always known.
- The augmented pair must be controllable, or at least stabilizable. With

$$A_a = \begin{bmatrix} A & 0 \\ -C & 0 \end{bmatrix}, \qquad B_a = \begin{bmatrix} B \\ 0 \end{bmatrix},$$

$(A_a, B_a)$ is controllable if and only if $(A, B)$ is controllable and

$$\operatorname{rank}\begin{bmatrix} A & B \\ C & 0 \end{bmatrix} = n + p.$$

*Proof.* Use the [PBH test](/popov-belevitch-hautus-test/) on $[\lambda I - A_a, B_a] = \begin{bmatrix} \lambda I - A & 0 & B \\ C & \lambda I & 0 \end{bmatrix}$. For $\lambda \ne 0$ the block $\lambda I$ is invertible, so the rank is $n + p$ exactly when $[\lambda I - A, B]$ has rank $n$. For $\lambda = 0$ the middle columns are zero, and the rank is that of $\begin{bmatrix} -A & B \\ C & 0 \end{bmatrix}$, which equals the rank of $\begin{bmatrix} A & B \\ C & 0 \end{bmatrix}$. At $\lambda = 0$ the condition $\operatorname{rank}[-A, B] = n$ follows from the rank $n + p$ of the larger matrix. $\square$

The rank condition needs $m \ge p$: at least as many inputs as controlled outputs. For a square plant ($m = p$) it says that $s = 0$ is not a [transmission zero](/transmission-zero/), so the plant has a nonzero static gain in every direction. Davison (1976) gave this condition, and the general one for other reference signals, for the robust servomechanism problem.

## The template

1. Check that $(A, B)$ is controllable and that $\operatorname{rank}\begin{bmatrix} A & B \\ C & 0 \end{bmatrix} = n + p$.
2. Form $A_a$ and $B_a$.
3. Choose $n + p$ closed-loop eigenvalues, or weights $Q$ and $R$ for the augmented state, and compute $K_a = [K, K_i]$ by [pole placement](/pole-placement-problem/) or by the [infinite-horizon LQR](/infinite-horizon-lqr/) for $(A_a, B_a)$.
4. Implement $\dot x_i = r - y$ and $u = -Kx - K_i x_i$. In discrete time with period $h$, use $x_{i,k+1} = x_{i,k} + h(r_k - y_k)$ and design with the discretized augmented model.
5. Add [anti-windup](/anti-windup/) if the input can saturate.
6. Optionally add a feedforward $u = -Kx - K_i x_i + Nr$. It does not change the eigenvalues or the steady state, but it adds a zero and makes the response to $r$ faster.

**Why the error goes to zero.** With $u = -K_a x_a$, the closed loop is $\dot x_a = (A_a - B_a K_a)x_a + \begin{bmatrix} 0 \\ I \end{bmatrix} r + \begin{bmatrix} E \\ 0 \end{bmatrix} d$. If $A_a - B_a K_a$ is Hurwitz and $r$ and $d$ are constant, $x_a(t)$ converges to the unique equilibrium. At the equilibrium $\dot x_i = r - Cx = 0$. The argument uses only the stability of the true closed loop, not the values of $A$, $B$ or $E$. So a model error that keeps the loop asymptotically stable leaves the steady-state error at 0.

## Classic examples

**Double integrator.** $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, $C = [1, 0]$, with the disturbance on the input, $E = B$. The rank condition holds: $\begin{bmatrix} A & B \\ C & 0 \end{bmatrix} = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ 1 & 0 & 0 \end{bmatrix}$ is a permutation matrix. With $K_a = [k_1, k_2, k_i]$,

$$\det(sI - A_a + B_a K_a) = \det\begin{bmatrix} s & -1 & 0 \\ k_1 & s + k_2 & k_i \\ 1 & 0 & s \end{bmatrix} = s^3 + k_2 s^2 + k_1 s - k_i.$$

For the triple eigenvalue $-2$ the wanted polynomial is $(s + 2)^3 = s^3 + 6s^2 + 12s + 8$, so $K = [12, 6]$ and $K_i = -8$. The law is

$$u = -12y - 6\dot y + 8\int_0^t (r - y)\,d\tau,$$

a PID controller with the derivative on the measurement. The transfer function from $r$ to $y$ is $8/(s + 2)^3$, with static gain 1 and no overshoot. The transfer function from $d$ to $y$ is $s/(s + 2)^3$, which is 0 at $s = 0$. A unit step in $d$ gives $y(t) = \tfrac12 t^2 e^{-2t}$, with the largest value $e^{-2}/2 \approx 0.068$ at $t = 1$, and then $y \to 0$. In the steady state with $r = 1$ and $d$ constant, $x_i = (12 - d)/8$: the integrator holds exactly the input that cancels $d$.

**Without the integrator.** For the same plant, $u = -12x_1 - 6x_2 + 12r$ has static gain 1, but a constant $d$ leaves $y = r + d/12$. The integrator removes this offset.

**A plant where integral action fails.** $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, $C = [0, 1]$, so $G(s) = s/((s + 1)(s + 2))$. Then $\begin{bmatrix} A & B \\ C & 0 \end{bmatrix} = \begin{bmatrix} 0 & 1 & 0 \\ -2 & -3 & 1 \\ 0 & 1 & 0 \end{bmatrix}$ has two equal rows and rank 2 < 3. The plant has a zero at $s = 0$ and static gain 0, so no constant input holds $y$ at a nonzero constant, and the augmented pair is not controllable.

## Variations

- **LQR with integral action.** Use the [infinite-horizon LQR](/infinite-horizon-lqr/) for $(A_a, B_a)$ with a weight on $x_i$. This is often called LQI.
- **Observer-based form.** Estimate $x$ with an observer and keep the exact $x_i$. By the [separation principle](/separation-principle/), the eigenvalues are those of $A_a - B_a K_a$ and those of the observer.
- **Other reference signals.** Replace the integrator by a model of the signal, for example a double integrator for ramps or an oscillator for sinusoids of a known frequency. This is the servocompensator of Davison and the [output regulation problem](/output-regulation-problem/). The rank condition is then required at each eigenvalue of the signal model.
- **Disturbance estimation instead.** Augment the observer with a constant disturbance state and cancel the estimate. This also gives zero offset and is the state-space form of a [disturbance observer](/disturbance-observer/).
- **Discrete time.** Use the sum of the errors. With all eigenvalues of the augmented loop at 0 one gets a deadbeat servo.

## Pitfalls

- **Windup.** When the input saturates, the integrator keeps integrating and causes a large overshoot. Use [anti-windup](/anti-windup/), for example by stopping the integration while the input is saturated.
- **The rank condition.** With fewer inputs than outputs, or with a zero at $s = 0$, no integral design exists. Choose fewer controlled outputs, or change the actuators.
- **Sensor offset.** The integrator drives the measured output to $r$. A constant bias in the sensor then becomes an error in the true output, and integral action cannot see it.
- **The extra pole.** The augmented loop has $p$ more eigenvalues. If they are placed too slowly, the error goes to zero slowly. If they are placed too fast, the input is large.
- **Only constant signals.** An integrator removes the steady-state error for constant $r$ and $d$. A ramp leaves a constant error, and a sinusoid leaves a sinusoidal error, unless the signal model is extended.

## Exercises

1. For the double integrator above, place all three eigenvalues at $-1$. (Answer: $(s + 1)^3 = s^3 + 3s^2 + 3s + 1$, so $K = [3, 3]$ and $K_i = -1$.)
2. Show that the steady state of the double integrator example has $x_2 = 0$, $x_1 = r$ and $x_i = (12 - d)/8$.
3. For $\dot x = -x + u$, $y = x$, design $u = -kx - k_i x_i$ with both closed-loop eigenvalues at $-2$. (Answer: $\det = s^2 + (1 + k)s - k_i$, so $k = 3$ and $k_i = -4$.)
4. Show that for $m < p$ the rank of $\begin{bmatrix} A & B \\ C & 0 \end{bmatrix}$ is less than $n + p$. (Hint: count the columns.)

## References
