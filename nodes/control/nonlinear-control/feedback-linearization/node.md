---
tag: SVJX8V
kind: technique
slug: feedback-linearization
name: Feedback linearization
aliases:
- exact feedback linearization
area: control/nonlinear-control
level: core
summary: Cancels the nonlinearities of a system with a state feedback and a change of coordinates, so the closed loop is exactly linear in the new coordinates and a linear design finishes the job.
prereqs: [input-output-linearization, lie-bracket, controllable-canonical-form]
see_also: [input-output-linearization, feedback-linearizability-conditions, relative-degree, computed-torque-control, controllable-canonical-form, differential-flatness, backstepping, jacobian-linearization]
sources:
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Chapter 13, Feedback Linearization; Section 13.1 (Motivation), Section 13.3 (Full-State Linearization) and Section 13.4 (State Feedback Control)
  - book: isbn:9783540199168
    title: Alberto Isidori, Nonlinear Control Systems, third edition, Springer, 1995
    locator: Chapter 4 (Nonlinear feedback for single-input single-output systems), exact linearization by state feedback and change of coordinates
  - book: isbn:9780130408907
    title: Jean-Jacques E. Slotine and Weiping Li, Applied Nonlinear Control, Prentice Hall, 1991
    locator: Section 6.1.2 (input-state linearization) and Section 6.3 (input-state linearization of SISO systems)
  - paper: doi:10.1109/TAC.1983.1103137
    title: "L. R. Hunt, R. Su and G. Meyer, Global transformations of nonlinear systems, IEEE Transactions on Automatic Control 28(1), 24-31, 1983"
    locator: the conditions for linearization by feedback and change of coordinates, and the construction of the transformation
---

Feedback linearization turns a nonlinear system into a linear one by two operations: a change of state coordinates $z = T(x)$ and a state feedback $u = \alpha(x) + \beta(x) v$. In the new coordinates and with the new input $v$, the closed loop is exactly linear, usually a chain of integrators. A linear design, for example [pole placement](/pole-placement-theorem/), then finishes the job. Unlike the [Jacobian linearization](/jacobian-linearization/), nothing is neglected: the linear model is exact on the whole region where the transformation is valid. The price is that the feedback must know the nonlinear terms in order to cancel them. This page is about full-state (input-state) linearization, where the whole state becomes linear. When only the map from $v$ to an output is made linear, the method is [input-output linearization](/input-output-linearization/), and the rest of the state is left to the [zero dynamics](/zero-dynamics/).

## In plain words

Many machines are nonlinear only in a way you can undo. A pendulum has a gravity torque that depends on the sine of its angle. If your motor knows the angle, it can push against exactly that torque, and what is left behaves like a mass with no gravity. That is easy to control. Feedback linearization makes this idea general. You look for a way to measure the state, sometimes with new variables, so that the input can remove every nonlinear effect at once. Then you control what is left with the usual linear methods. It works only when such variables exist, when the model is good, and when the input is strong enough to cancel what it must.

## When it applies

- The model is $\dot x = f(x) + g(x) u$ with smooth $f$, $g$, so solutions exist and are unique by the [Picard-Lindelöf theorem](/picard-lindelof-theorem/), and the model is accurate.
- The nonlinear terms enter in the same places as the input, or can be moved there by a change of coordinates. For one input this happens if and only if some output has [relative degree](/relative-degree/) $n$. The [conditions for feedback linearizability](/feedback-linearizability-conditions/) test this with [Lie brackets](/lie-bracket/): $g, \mathrm{ad}_f g, \dots, \mathrm{ad}_f^{n-1} g$ must be linearly independent, and $\mathrm{span}\{g, \dots, \mathrm{ad}_f^{n-2} g\}$ must be involutive.
- A physical output often has relative degree $n$ by itself: a position in a mechanical system with one force or torque per degree of freedom.
- The input has enough authority to cancel the nonlinear terms over the operating region.

## The template

```pseudo id=main
FEEDBACK-LINEARIZE(f, g, x0)
L1  h ← FIND-OUTPUT(f, g, x0)                 ▷ any h with relative degree n at x0
L2  z ← T(x) = (h, L_f h, ..., L_f^(n-1) h)    ▷ new coordinates
L3  a(x) ← L_g L_f^(n-1) h;  b(x) ← L_f^n h
L4  u ← (v - b(x)) / a(x)                      ▷ now z' = A_c z + B_c v, a chain of n integrators
L5  v ← LINEAR-DESIGN(z)                       ▷ for example v = -K z
L6  REGION ← the set where T is one to one and a(x) ≠ 0
```

**FIND-OUTPUT (line L1).** This is the hard step. Often the physics gives $h$: the position of the mass, the angle of the arm. In general $h$ must solve the partial differential equations $L_g L_f^k h = 0$ for $k = 0, \dots, n - 2$ with $L_g L_f^{n-1} h(x_0) \neq 0$, which is the same as $dh \cdot \mathrm{ad}_f^k g = 0$ for $k \le n - 2$. The theorem of Frobenius says that such an $h$ exists exactly when the bracket conditions hold. For a linear controllable system, $h(x) = w^T x$ with $w^T$ the last row of the inverse of the controllability matrix.

**The coordinates (line L2).** The derivatives $h, L_f h, \dots, L_f^{n-1} h$ have independent differentials at $x_0$, so $T$ is a local change of coordinates. In these coordinates $\dot z_i = z_{i+1}$ for $i < n$ and $\dot z_n = b(x) + a(x) u$.

**The feedback (lines L3 and L4).** With $u = (v - b)/a$, the last equation becomes $\dot z_n = v$. The closed loop is the controllable canonical form with all coefficients zero, the Brunovsky form.

**The linear design (line L5).** Any linear method applies to $\dot z = A_c z + B_c v$. With $v = -k_0 z_1 - \dots - k_{n-1} z_n$, the closed-loop polynomial is $s^n + k_{n-1} s^{n-1} + \dots + k_0$, so the poles can be placed anywhere. For tracking, use $v = y_d^{(n)} - \sum_i k_i (z_{i+1} - y_d^{(i)})$.

**The region (line L6).** All of this holds only where $T$ is a diffeomorphism and $a \neq 0$. A result on that region becomes a global result only if the region is the whole state space and $T$ is onto $\mathbb{R}^n$.

## Classic examples

**A pendulum with a torque.** Let $\dot x_1 = x_2$, $\dot x_2 = -a \sin x_1 - b x_2 + c u$ with $c \neq 0$. The angle $h = x_1$ has relative degree $2$, the coordinates are $z = x$, and $u = (a \sin x_1 + b x_2 + v)/c$ gives $\ddot x_1 = v$. The region is the whole plane. This is the simplest case: the nonlinear terms are already in the equation of the input.

**A system that needs new coordinates.** Let $\dot x_1 = a \sin x_2$, $\dot x_2 = -x_1^2 + u$ with $a > 0$. The input does not enter the first equation, and the nonlinearity $\sin x_2$ does not enter the second. The output $h = x_1$ gives $L_g h = 0$ and $L_g L_f h = a \cos x_2$, so $z = (x_1, a \sin x_2)$, $\dot z_1 = z_2$ and $\dot z_2 = a \cos x_2 (-x_1^2 + u)$. The feedback $u = x_1^2 + v / (a \cos x_2)$ gives $\dot z_2 = v$. The region is $|x_2| < \pi/2$, where $\cos x_2 > 0$ and $x_2 \mapsto a \sin x_2$ is one to one. Textbooks use this kind of system to show that the region can be a strict part of the state space.

**Robot arms.** For a rigid arm $M(q) \ddot q + C(q, \dot q) \dot q + G(q) = \tau$, the joint positions $q$ form an output with relative degree $2$ in each joint, and the feedback $\tau = M(q) v + C(q, \dot q) \dot q + G(q)$ gives $\ddot q = v$. This is the [computed torque method](/computed-torque-control/), and its region is the whole state space, because the inertia matrix $M(q)$ is always invertible.

**Linear systems.** A controllable system $\dot x = A x + B u$ is linearizable in this sense. The output $h = w^T x$ above gives the coordinates of the [controllable canonical form](/controllable-canonical-form/), and the feedback cancels the coefficients of the characteristic polynomial. The [pole placement theorem](/pole-placement-theorem/) is this case followed by a choice of $v$.

**Output tracking with internal states.** When the chosen output has relative degree $r < n$, the same steps give [input-output linearization](/input-output-linearization/). The first $r$ coordinates become linear, and the other $n - r$ follow the internal dynamics.

## Variations

- **Several inputs.** With $m$ inputs, the target is $m$ chains of integrators with lengths given by the controllability indices. The conditions use one distribution for each bracket level (see the conditions page).
- **Input-output linearization.** Make only the output linear. This needs much weaker conditions, but the [zero dynamics](/zero-dynamics/) must be stable.
- **Dynamic feedback linearization.** Add integrators (states of the controller) before the inputs, and linearize the extended system. Systems that become linearizable this way are [differentially flat](/differential-flatness/). For one input, static and dynamic linearizability coincide.
- **Partial feedback linearization.** For underactuated mechanical systems, linearize the actuated or the unactuated coordinates only, and treat the rest separately.
- **Approximate linearization.** When the conditions fail by small terms, drop those terms and linearize the rest, accepting a small residual.

## Pitfalls

- **Cancelling useful terms.** For $\dot x = -x^3 + u$, the cancelling law $u = x^3 - x$ gives $\dot x = -x$, but it removes the damping $-x^3$, which helps, and it needs a large input for large $|x|$. The law $u = -x$ gives $\dot x = -x - x^3$, which is better in both ways. [Backstepping](/backstepping/) and passivity-based designs keep such terms.
- **Model errors.** The feedback at line L4 cancels $b(x)$ only if $b$ is known. With an error $\Delta(x)$, the closed loop is $\dot z = (A_c - B_c K) z + B_c \Delta$. A small $\Delta$ is usually tolerated, but there is no margin built in. Robust methods such as [sliding mode control](/sliding-mode-control/) are designed for this.
- **Leaving the region.** In the second example, if $x_2$ comes close to $\pm \pi/2$, $\cos x_2$ goes to zero and the input grows without bound. Line L6 must be checked along the closed-loop motion, not only at the start.
- **Trusting the Jacobian linearization.** A controllable linearization does not make the system linearizable. For $\dot x_1 = x_2 + x_3^2$, $\dot x_2 = x_3$, $\dot x_3 = u$, the linearization at $0$ is a chain of integrators, but $[g, \mathrm{ad}_f g] = (-2, 0, 0)$ is not in $\mathrm{span}\{g, \mathrm{ad}_f g\}$, so no output has relative degree 3 and the system is not feedback linearizable.
- **Saturation.** The cancelling input can be large. With limits on $u$, line L4 cannot be applied exactly, and the linear closed loop is lost.

## Exercises

1. For $\dot x_1 = x_2$, $\dot x_2 = -\sin x_1 + u$, find the feedback that puts both closed-loop poles at $-2$. *Answer:* $u = \sin x_1 - 4 x_1 - 4 x_2$, from $v = -4 z_1 - 4 z_2$ and $(s + 2)^2 = s^2 + 4 s + 4$.
2. Show that $h(x) = w^T x$, with $w^T$ the last row of $\mathcal{C}^{-1}$ and $\mathcal{C} = [B, A B, \dots, A^{n-1} B]$, has relative degree $n$. *Answer:* $w^T A^k B$ is the entry $n$ of $\mathcal{C}^{-1} \mathcal{C} e_{k+1} = e_{k+1}$, which is $0$ for $k < n - 1$ and $1$ for $k = n - 1$.
3. Show that $\dot x_1 = x_2 + x_3^2$, $\dot x_2 = x_3$, $\dot x_3 = u$ is not feedback linearizable near $0$. *Answer:* $\mathrm{ad}_f g = (-2 x_3, -1, 0)$ and $[g, \mathrm{ad}_f g] = (-2, 0, 0)$, which is not a combination of $g = (0, 0, 1)$ and $\mathrm{ad}_f g$ at any point.

## References
