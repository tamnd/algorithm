---
tag: SA0J6T
kind: technique
slug: null-space-projection
name: Null-space projection
aliases:
- self-motion projection
area: robotics/robot-kinematics
level: core
summary: Adds (I - J^+ J) z to a joint velocity, which pursues a secondary goal z without disturbing the main task.
model: real-ram
complexity:
  vars: {m: the dimension of the task, n: the number of joints}
  time: {worst: Θ(m n^2)}
  space: {extra: Θ(n^2)}
prereqs: [kinematic-redundancy, pseudoinverse]
see_also: [task-priority-inverse-kinematics, yoshikawa-manipulability-measure, jacobian-pseudoinverse-method, resolved-rate-motion-control, hierarchical-quadratic-programming, operational-space-formulation, gradient-descent, lagrange-multiplier]
sources:
  - paper: doi:10.1109/TSMC.1977.4309644
    title: Alain Liégeois, Automatic supervisory control of the configuration and behavior of multibody mechanisms, IEEE Transactions on Systems, Man, and Cybernetics 7(12), 868-871, 1977
    locator: the whole paper (the general solution with the projector I - J^+ J and the gradient of a secondary cost, used for joint limits)
  - book: isbn:9781846286414
    title: "Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics: Modelling, Planning and Control, Springer, 2009"
    locator: Chapter 3, Section 3.5 (inverse differential kinematics for redundant manipulators, the null space projector and the objective functions for joint limits, manipulability and obstacles)
  - paper: doi:10.1177/027836498700600201
    title: Yoshihiko Nakamura, Hideo Hanafusa and Tsuneo Yoshikawa, Task-priority based redundancy control of robot manipulators, The International Journal of Robotics Research 6(2), 3-15, 1987
    locator: the whole paper (a second task solved in the null space of the first)
  - book: isbn:9780201151985
    title: "Yoshihiko Nakamura, Advanced Robotics: Redundancy and Optimization, Addison-Wesley, 1991"
    locator: the chapter on differential kinematics and redundancy (the projector onto the null space and the general solution)
---

Null-space projection is the standard way to use the spare joints of a [redundant](/kinematic-redundancy/) arm.
Given a joint velocity $J^{+}\dot x$ that does the main task, it adds the term $(I - J^{+}J)\,z$, where $z$ is any joint velocity that serves a second goal and $I - J^{+}J$ is the orthogonal projector onto the null space of the Jacobian $J$.
The added motion changes only the posture of the arm, not the task, so the second goal is pursued as far as the task allows.
With $z$ the negative gradient of a cost, this is the gradient projection method of Liégeois (1977).

## In plain words

A person can hold a cup still in front of the face and still move the elbow up and down.
The hand does the task, and the elbow has freedom left over.
This technique uses that freedom on purpose.
First it finds the joint motion that does the task.
Then it takes a wish for some other motion, for example "keep the joints near the middle of their range", and removes from the wish every part that would move the hand.
What is left only changes the shape of the arm.
Adding it to the first motion gives a motion that still does the task and also goes toward the wish as far as it can.

## When it applies

- The arm is redundant for the task: $J$ is $m \times n$ with $m < n$.
- $J$ has full row rank $m$ along the path, so $J^{+} = J^{\mathsf T}(JJ^{\mathsf T})^{-1}$ exists and is bounded.
- The control is at the velocity level, as in [resolved-rate motion control](/resolved-rate-motion-control/), or at the step level of [pseudoinverse inverse kinematics](/jacobian-pseudoinverse-method/).
- The second goal can be written as a joint velocity $z$, often $z = -k_0 \nabla h(q)$ for a cost $h$ to make small, or $z = +k_0 \nabla w(q)$ for a measure $w$ to make large.
- The second goal has lower priority: when it conflicts with the task, the task wins.

## The template

Let $J$ be an $m \times n$ matrix of rank $m$, let $J^{+} = J^{\mathsf T}(JJ^{\mathsf T})^{-1}$ be its [pseudoinverse](/pseudoinverse/), and let

$$P = I - J^{+}J.$$

**Facts about $P$.**

- $JP = J - JJ^{\mathsf T}(JJ^{\mathsf T})^{-1}J = 0$, so every $Pz$ lies in $\operatorname{null}(J)$.
- $P^{\mathsf T} = P$ and $P^2 = P$, so $P$ is the orthogonal projector onto $\operatorname{null}(J)$, of rank $n - m$.
- $PJ^{+} = 0$: the least norm solution $J^{+}\dot x$ lies in $\operatorname{range}(J^{\mathsf T})$, orthogonal to the null space.

**The step.** For a task velocity $\dot x$ and a wish $z$,

$$\dot q = J^{+}\dot x + Pz.$$

Then $J\dot q = \dot x$ for every $z$.
Of all joint velocities with $J\dot q = \dot x$, this one is the closest to $z$.
The solutions form the affine set $J^{+}\dot x + \operatorname{null}(J)$, and the closest point to $z$ is $J^{+}\dot x + P(z - J^{+}\dot x) = J^{+}\dot x + Pz$, since $PJ^{+} = 0$.
Equivalently, $\dot q$ solves the problem: minimize $|\dot q - z|^2$ subject to $J\dot q = \dot x$, whose [Lagrange](/lagrange-multiplier/) condition gives the same answer.

```pseudo id=main
NULL-SPACE-STEP(J, x', z)                  ▷ J: m × n of rank m; x': task velocity; z: wish
L1  J^+ ← J^T (J J^T)^-1
L2  P ← I - J^+ J                           ▷ projector onto null(J)
L3  return J^+ x' + P z
```

**Gradient projection.** With $z = -k_0\nabla h(q)$ and $k_0 > 0$, the cost changes at the rate

$$\dot h = \nabla h^{\mathsf T}\dot q = \nabla h^{\mathsf T} J^{+}\dot x - k_0 |P\nabla h|^2.$$

When the task is to hold still, $\dot x = 0$, the cost never increases, and it stops changing exactly when $P\nabla h = 0$, that is, when $\nabla h \in \operatorname{range}(J^{\mathsf T})$.
That is the Lagrange condition for a minimum of $h$ on the self-motion set $\{q : f(q) = x\}$, so the posture slides toward a constrained local minimum of $h$.
When the task moves, the first term can raise $h$, and the second term only works against it.
A discrete controller also adds feedback on the task error, $\dot x = \dot x_d + K e$, to correct the drift of the Euler steps.

**Cost.** Line L1 costs $\Theta(m^2 n + m^3)$, and line L2 costs $\Theta(m n^2)$, which dominates since $m \le n$; the total is $\Theta(m n^2)$ time and $\Theta(n^2)$ extra space for $P$ in the [real RAM](/real-ram/).
If $P$ itself is not needed, $Pz = z - J^{+}(Jz)$ costs only $\Theta(m^2 n)$.

## Classic examples

**A hand example.** Take the planar 3R arm with unit links at $q = (0, \pi/2, -\pi/2)$, with the tip at $(2, 1)$ m.
Then

$$J = \begin{pmatrix} -1 & -1 & 0 \\ 2 & 1 & 1 \end{pmatrix}, \qquad \operatorname{null}(J) = \operatorname{span}\{\nu\},\ \nu = (1, -1, -1), \qquad P = \frac{\nu\nu^{\mathsf T}}{3} = \frac{1}{3}\begin{pmatrix} 1 & -1 & -1 \\ -1 & 1 & 1 \\ -1 & 1 & 1 \end{pmatrix}.$$

To hold the tip still while joint 3 is asked to turn at $z = (0, 0, 3)$ rad/s, the step gives $\dot q = Pz = -\nu = (-1, 1, 1)$ rad/s.
Joint 3 turns at 1 rad/s, not 3, and the other two joints move too, because the tip must not move: $J(-1, 1, 1)^{\mathsf T} = (0, 0)$.
To move the tip at $\dot x = (0.3, 0)$ m/s with no wish, the least norm solution is $J^{+}\dot x = (0, -0.3, 0.3)$ rad/s.

**Keeping the joints near zero.** Take the same arm with the cost $h(q) = |q|^2/2$, so $\nabla h = q$, and start at $q_0 = (0.2, 1.2, -0.9)$, where $h = 1.145$ and the tip is at $x_d = (2.0276, 1.6635)$.
Integrate $\dot q = J^{+}(10\,(x_d - f(q))) + P(-q)$ with Euler steps of 0.01 s.

| time | $q$ | $h$ |
|---|---|---|
| 0 s | $(0.2, 1.2, -0.9)$ | 1.145 |
| 1 s | $(-0.0096, 1.2211, -0.3829)$ | 0.8189 |
| 5 s | $(0.037, 0.6941, 0.5519)$ | 0.3939 |
| 15 s | $(0.0568, 0.6401, 0.6084)$ | 0.3916 |

The tip stays within $9.9 \cdot 10^{-5}$ m of $x_d$ the whole time, $h$ decreases at every step, and at 15 s the projected gradient $|P\nabla h|$ is $4.8 \cdot 10^{-5}$.
The length of the projected gradient does not fall at every step: it grows from 0.44 to 0.62 before it goes down, because $P$ changes with $q$.
The arm ends near a posture where $|q|$ is locally smallest among all postures that keep the tip at $x_d$; the task alone does not fix this posture.

**Joint limits.** Liégeois (1977) used the gradient of a cost on the joint values to keep each joint away from its limits.
A common form of such a cost, as in Siciliano et al., is $h(q) = \sum_i \big((q_i - \bar q_i)/(q_{i,\max} - q_{i,\min})\big)^2$, where $\bar q_i$ is the middle of the range of joint $i$.

**Singularities.** With $z = k_0 \nabla w$, where $w$ is the [Yoshikawa measure](/yoshikawa-manipulability-measure/), the self-motion moves the arm toward postures of large manipulability; Yoshikawa (1985) suggested this use, and Siciliano et al. list it with joint limits and obstacle distance as standard objectives.

## Variations

- **Weighted norm.** With a [positive definite](/positive-definite-matrix/) weight $W$, $J^{+}_W = W^{-1}J^{\mathsf T}(JW^{-1}J^{\mathsf T})^{-1}$ and $P_W = I - J^{+}_W J$. Then $P_W$ is a projector onto $\operatorname{null}(J)$ that is orthogonal in the inner product of $W$, not in the plain one.
- **Several tasks.** [Task priority inverse kinematics](/task-priority-inverse-kinematics/) (Nakamura, Hanafusa and Yoshikawa, 1987) replaces $z$ by the best solution of a second task inside $\operatorname{null}(J_1)$: $\dot q = J_1^{+}\dot x_1 + (J_2 P_1)^{+}(\dot x_2 - J_2 J_1^{+}\dot x_1)$. Nested projectors give a full hierarchy, and [hierarchical quadratic programming](/hierarchical-quadratic-programming/) adds inequality constraints.
- **Torque level.** In the [operational space formulation](/operational-space-formulation/), the projector acts on torques, $\tau = J^{\mathsf T}F + (I - J^{\mathsf T}\bar J^{\mathsf T})\tau_0$, with a pseudoinverse $\bar J$ weighted by the inertia matrix, so that $\tau_0$ does not cause a task acceleration.
- **Without forming $P$.** $Pz = z - J^{+}(Jz)$, or $Pz = z - Q Q^{\mathsf T}z$ with an orthonormal basis $Q$ of $\operatorname{range}(J^{\mathsf T})$ from a [QR decomposition](/qr-decomposition/) of $J^{\mathsf T}$.
- **Position level.** In pseudoinverse inverse kinematics, adding $P\,z$ to each Newton step pulls the solution toward a preferred posture.

## Pitfalls

- **Near a singularity of $J$.** $(JJ^{\mathsf T})^{-1}$ blows up, $J^{+}\dot x$ asks for huge rates, and at the singular point the null space jumps to a larger dimension. A pseudoinverse that drops singular values below a tolerance, or [damped least squares](/damped-least-squares-inverse-kinematics/), keeps the rates bounded; the tolerance or damping is a rule of thumb, and with damping $JP \ne 0$, so the second goal leaks into the task.
- **Drift.** $Pz$ is in $\operatorname{null}(J)$ only to first order, so Euler steps move the tip a little. In the example above, without the feedback term the tip drifts by up to $1.7 \cdot 10^{-3}$ m over the 15 s; with a gain of 10 the error stays below $10^{-4}$ m.
- **Only part of the wish.** $Pz$ is the part of $z$ that the task allows; when $z$ is nearly in $\operatorname{range}(J^{\mathsf T})$, almost nothing is left. The goal is reached only if the self-motion can reach it.
- **Local minima.** Gradient projection stops at any constrained stationary point of $h$, which can be a local minimum or a saddle.
- **The gain $k_0$.** A large $k_0$ speeds the second goal but raises joint rates and can make Euler steps unstable; its value is set by trial for each arm.
- **A cost on the wrong variables.** $h$ must be a function of $q$; a cost on the task variables has a gradient in $\operatorname{range}(J^{\mathsf T})$, and its projection is zero.

## Exercises

1. Show that $P = I - J^{+}J$ is symmetric and idempotent, that $JP = 0$, and that $\operatorname{rank}P = n - m$.
2. Show that $\dot q = J^{+}\dot x + Pz$ minimizes $|\dot q - z|$ subject to $J\dot q = \dot x$, first with the projection argument and then with a Lagrange multiplier.
3. For the 3R arm at $q = (0, \pi/2, -\pi/2)$, compute $Pz$ for $z = (1, 0, 0)$ and check that $J\,Pz = 0$.
4. Show that with $\dot x = 0$ and $z = -k_0\nabla h$, $h$ is nonincreasing, and that $P\nabla h = 0$ is the Lagrange condition for a minimum of $h$ on the self-motion set.
5. Show that $P_W = I - J^{+}_W J$ satisfies $P_W^2 = P_W$ and $W P_W = P_W^{\mathsf T}W$, and give an example where $P_W$ is not symmetric.

## References
