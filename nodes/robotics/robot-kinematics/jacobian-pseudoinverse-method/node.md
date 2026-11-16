---
tag: MNF4KJ
kind: algorithm
slug: jacobian-pseudoinverse-method
name: Jacobian pseudoinverse method
aliases:
- pseudoinverse inverse kinematics
area: robotics/robot-kinematics
level: core
summary: Iterates joint steps J^+ e that reduce the pose error e, giving least-norm joint motion for redundant arms.
model: real-ram
complexity:
  vars: {n: the number of joints, m: the dimension of the task, k: the number of iterations}
  time: {worst: "Θ(k m n min(m, n))"}
  space: {extra: Θ(m n)}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 1969
  people: [Daniel E. Whitney]
  note: Whitney resolved end effector rates into joint rates through the inverse Jacobian; the same linear step, with the generalized inverse of Penrose (1955) and repeated until the pose error vanishes, became the standard numerical inverse kinematics.
prereqs: [pseudoinverse, geometric-jacobian, inverse-kinematics]
see_also: [newton-raphson-inverse-kinematics, damped-least-squares-inverse-kinematics, jacobian-transpose-method, resolved-rate-motion-control, null-space-projection, gauss-newton-algorithm, newton-method-for-systems, space-and-body-jacobian]
sources:
  - paper: doi:10.1017/S0305004100030401
    title: Roger Penrose, A generalized inverse for matrices, Mathematical Proceedings of the Cambridge Philosophical Society 51(3), 406-413, 1955
    locator: the whole paper (the four equations that define the generalized inverse, and the least squares solution of least norm)
  - book: isbn:9781107156302
    title: "Kevin M. Lynch and Frank C. Park, Modern Robotics: Mechanics, Planning, and Control, Cambridge University Press, 2017"
    locator: Chapter 6, Section 6.2 (numerical inverse kinematics, the Newton-Raphson method in 6.2.1 and the numerical inverse kinematics algorithm with the body twist error and the pseudoinverse in 6.2.2)
  - book: isbn:9781846286414
    title: "Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics: Modelling, Planning and Control, Springer, 2009"
    locator: Chapter 3, Section 3.5 (the pseudoinverse solution of the differential kinematics) and Section 3.7 (inverse kinematics algorithms)
  - paper: doi:10.1109/TMMS.1969.299896
    title: Daniel E. Whitney, Resolved motion rate control of manipulators and human prostheses, IEEE Transactions on Man-Machine Systems, 1969
    locator: the whole paper (joint rates from the inverse of the Jacobian)
---

The Jacobian pseudoinverse method solves the [inverse kinematics](/inverse-kinematics/) of a robot arm by iteration.
From a guess $q$, it measures the error $e$ between the desired pose and the pose that $q$ gives, and it moves the joints by $\Delta q = J(q)^{+}e$, where $J^{+}$ is the Moore-Penrose [pseudoinverse](/pseudoinverse/) of the Jacobian, until the error is below a tolerance.
Each step is the joint motion of least norm that removes the error to first order, or, if no joint motion can, the one of least norm among those that leave the smallest error.
So the same short loop works for square, redundant and underactuated tasks, and near a solution it converges quadratically.

## In plain words

You want the hand of a robot at a certain place, and you do not know the joint angles that put it there.
Guess some angles and look at where the hand is.
The hand is off by some amount.
For small joint motions, the hand moves almost in a straight line, by a rule that you can compute at the present angles.
So ask: what is the smallest joint motion that would move the hand by exactly the missing amount, if that rule were exact?
Make that motion, look again, and repeat.
Near the answer, each repeat roughly doubles the number of correct digits.
If the arm has spare joints, picking the smallest motion keeps it from wandering.

## The problem

**Input.**

- The forward kinematics of an arm with $n$ joints, $T(q) \in SE(3)$, in the product of exponentials form $T(q) = M e^{[\mathcal B_1]q_1} \cdots e^{[\mathcal B_n]q_n}$ with the body screw axes $\mathcal B_i$.
- A desired pose $T_d$.
- An initial guess $q_0$, tolerances $\varepsilon_\omega$ for the rotation and $\varepsilon_v$ for the translation, and a maximum number of iterations $k_{\max}$.

**Output.** Joint values $q$ such that the body twist $\mathcal V_b = \log(T(q)^{-1}T_d) = (\omega_b, v_b)$ has $|\omega_b| \le \varepsilon_\omega$ and $|v_b| \le \varepsilon_v$, or FAILURE if no such $q$ is found within $k_{\max}$ iterations.

For a position task, the error is the plain difference $e = x_d - f(q)$ of positions, and $J$ is the position Jacobian; the loop is the same.
In both cases the task has dimension $m$ ($m = 6$ for a full pose), and $J$ is $m \times n$; $n > m$ (redundant), $n = m$ and $n < m$ are all allowed.

## The algorithm

```pseudo id=main
PSEUDOINVERSE-IK(M, B_1..B_n, T_d, q0, ε_ω, ε_v, k_max)
L1  q ← q0
L2  for k ← 1 to k_max
L3      V_b ← log(T(q)^-1 T_d)                ▷ pose error as a body twist (ω_b, v_b)
L4      if |ω_b| ≤ ε_ω and |v_b| ≤ ε_v then return q
L5      J_b ← BODY-JACOBIAN(q)                 ▷ 6 × n, in the end effector frame
L6      q ← q + J_b^+ V_b                      ▷ least norm, least squares step
L7  return FAILURE
```

Line L3 uses the matrix logarithm of SE(3), the inverse of the [exponential map](/se3-exponential-map/); $\mathcal V_b$ is the twist that, followed for unit time, takes the present end effector frame to the desired one.
Line L5 is the [body Jacobian](/space-and-body-jacobian/), whose columns are the body screw axes moved to the present configuration; it is in the same frame and the same order (angular part first) as $\mathcal V_b$.
Line L6 needs $J_b^{+}V_b$, which is the least squares solution of least norm of $J_b\,\Delta q = V_b$.
The code on this page computes it from a singular value decomposition and treats singular values at or below $10^{-10}\sigma_{\max}$ as zero; that tolerance is a rule of thumb.

## Example

**A 2R arm, position task.** Planar arm with unit links, target $x_d = (1, 1)$ m, start $q_0 = (0.3, 1.2)$.

- Line L3 (position form): $f(q_0) = (1.026074, 1.293015)$, so $e = (-0.026074, -0.293015)$ and $|e| = 0.294$ m.
- Line L5: $J(q_0) = \begin{pmatrix} -1.2930 & -0.9975 \\ 1.0261 & 0.0707 \end{pmatrix}$, square and invertible, so $J^{+} = J^{-1}$.
- Line L6: $\Delta q = (-0.315572, 0.435203)$, and $q_1 = (-0.015572, 1.635203)$.

The next iterates are $(-0.001187, 1.572048)$ and then $(0.000000, 1.570797)$, which approach the solution $(0, \pi/2)$.
The error norms are

$$0.294,\quad 0.0517,\quad 0.00119,\quad 7.05 \cdot 10^{-7},\quad 2.48 \cdot 10^{-13},\quad 0,$$

and each one is about a constant times the square of the one before: quadratic convergence.
From the start $(1.3, -1.2)$ the same loop goes to the other solution, $(\pi/2, -\pi/2)$, with the error norms $0.270$, $0.0444$, $8.35 \cdot 10^{-4}$, $3.44 \cdot 10^{-7}$ and $5.92 \cdot 10^{-14}$.
The guess decides which solution the method finds.

**A redundant 3R arm.** Planar arm with three unit links, target $(1.5, 1.0)$ m, start $q_0 = (0, 0.5, 0.5)$, where $f(q_0) = (2.417885, 1.320897)$ and $|e| = 0.972$ m.
Here $J(q_0) = \begin{pmatrix} -1.3209 & -1.3209 & -0.8415 \\ 2.4179 & 1.4179 & 0.5403 \end{pmatrix}$ is $2 \times 3$, and the first step is the least norm solution $\Delta q = (-0.884752, 0.839974, 1.161099)$.
The error norms are $0.972$, $0.683$, $0.0297$, $1.99 \cdot 10^{-4}$, $1.35 \cdot 10^{-8}$ and $2.2 \cdot 10^{-16}$, and the loop ends at $q = (-0.560477, 1.141052, 1.174410)$, with $|q| = 1.7307$.
The target has a one-parameter family of solutions; the method picks one of them, and which one depends on $q_0$.

**A pose task with more equations than joints.** Write the same 2R arm as a spatial chain with $M = (I, (2, 0, 0))$ and the body screw axes $\mathcal B_1 = (0, 0, 1, 0, 2, 0)$ and $\mathcal B_2 = (0, 0, 1, 0, 1, 0)$, and ask for the pose $T_d$ with rotation $R_z(\pi/2)$ and position $(1, 1, 0)$, from $q_0 = (0.2, 1.3)$.
Now $J_b$ is $6 \times 2$, with only the rows $\omega_z$, $v_x$ and $v_y$ nonzero, and $J_b^{+}$ gives the least squares step.
The error norms $(|\omega_b|, |v_b|)$ are $(0.0708, 0.2027)$, $(0.0135, 0.0136)$, $(5.5 \cdot 10^{-6}, 5.5 \cdot 10^{-6})$ and $(7.2 \cdot 10^{-14}, 7.2 \cdot 10^{-14})$, and the loop returns $(0, \pi/2)$.

**A target out of reach.** For the target $(2.5, 0)$ m, which is beyond the reach of 2 m, from $(0.2, 0.5)$, the error norms jump between about 0.5 and 2.2 and do not settle, and the loop returns FAILURE after 50 iterations.
Near the stretched pose, which is the best the arm can do, $J$ is close to singular, and the steps are huge.

## Correctness

**The step.** By Penrose (1955), $\Delta q = J^{+}e$ is the unique vector that minimizes $|J\Delta q - e|$ and, among all minimizers, has the least norm.
If $J$ has full row rank, the minimum is 0 and $\Delta q$ is the least norm solution of $J\Delta q = e$; if $J$ is square and invertible, $\Delta q = J^{-1}e$ is the [Newton step](/newton-method-for-systems/); if $J$ has full column rank, $\Delta q = (J^{\mathsf T}J)^{-1}J^{\mathsf T}e$ is the [Gauss-Newton step](/gauss-newton-algorithm/).

**Convergence, full row rank.** Write $G(q)$ for the error (the position error or the body twist error) and suppose that on a ball around $q_0$, $\sigma_m(J(q)) \ge \sigma_0 > 0$, the second derivative of $G$ is bounded by $H$, and, for the twist error, $DG = -A\,J_b$ with $|A - I| \le L|G|$.
Then each step gives $|G(q_{k+1})| \le C|G(q_k)|^2$ with $C = L + H/(2\sigma_0^2)$.
If $\theta = C|G(q_0)| < 1$ and the ball has radius at least $|G(q_0)|/(\sigma_0(1 - \theta))$, the iterates stay in the ball, converge to a solution $q^*$, and $C|G(q_k)| \le \theta^{2^k}$.
For the position error, $L = 0$.

**Convergence, full column rank.** If a solution $q^*$ exists and $J$ has full column rank near it, then $|q_{k+1} - q^*| \le D|q_k - q^*|^2$ for a constant $D$, so the method converges quadratically from every start close enough to $q^*$.

The proof below gives the details.
The method is local: from a poor start, or when no solution exists, it can wander, cycle or stop at a singular configuration.

## Complexity

Each iteration evaluates $T(q)$ and $J_b(q)$ in $\Theta(n)$ operations for a task of fixed size, the logarithm in $\Theta(1)$, and the step $J^{+}e$.
With a [QR decomposition](/qr-decomposition/) of $J^{\mathsf T}$ (full row rank) or of $J$ (full column rank), or a [singular value decomposition](/singular-value-decomposition/) with a bounded number of sweeps, the step costs $\Theta(mn\min(m, n))$.
So $k$ iterations cost $\Theta(k\,m n \min(m, n))$ in the [real RAM](/real-ram/), with $\Theta(mn)$ extra space.
The one-sided Jacobi decomposition of the code on this page also keeps an $n \times n$ matrix of rotations, so it uses $\Theta(n^2)$ more space and $\Theta(n^2(m + n))$ operations per sweep.
Because of the quadratic convergence, a start within the basin of a solution needs only a handful of iterations to reach full precision, as the examples show.

## Properties

- **Local and fast.** Near a nonsingular solution, the number of correct digits roughly doubles at each iteration.
- **Least norm steps.** For a redundant arm, each step is the smallest joint motion that does the job to first order, which keeps the joints from drifting along the self-motion. The final solution is not the solution nearest to $q_0$, only the end of a path of least norm steps.
- **One answer.** The method returns one solution, the one whose basin contains $q_0$; to find others, restart from other guesses.
- **Frame consistent.** With the body twist error and the body Jacobian, both in the end effector frame, the result does not depend on the choice of the base frame.
- **Not robust at singularities.** As $\sigma_{\min}(J) \to 0$, the steps grow like $1/\sigma_{\min}$; a target out of reach drives the arm to a singular pose.

## Variants and improvements

- **Damped least squares.** Replace $J^{+}$ by $J^{\mathsf T}(JJ^{\mathsf T} + \lambda^2 I)^{-1}$, the Levenberg-Marquardt step of [damped least squares inverse kinematics](/damped-least-squares-inverse-kinematics/); it trades speed for robustness near singularities and out of reach. See also [Levenberg-Marquardt](/levenberg-marquardt/).
- **The transpose.** Use $\Delta q = \alpha J^{\mathsf T}e$, a gradient step on $|e|^2/2$, in the [Jacobian transpose method](/jacobian-transpose-method/); it needs no inverse but converges only linearly.
- **A secondary goal.** Add $(I - J^{+}J)z$ to each step to pull a redundant arm toward a preferred posture; see [null space projection](/null-space-projection/) and [task priority inverse kinematics](/task-priority-inverse-kinematics/).
- **Step control.** Scale the step or search along it to keep $|e|$ decreasing, which enlarges the basin of convergence; limit the step of each joint to keep it inside its range.
- **The space form.** The space twist error $\mathcal V_s = \operatorname{Ad}_{T(q)}\mathcal V_b$ with the space Jacobian $J_s = \operatorname{Ad}_{T(q)}J_b$ gives the same step when $J_b$ has full row rank, because then $J_s^{+} = J_b^{+}\operatorname{Ad}_{T(q)}^{-1}$; for other ranks the two steps can differ.
- **Square arms.** For $n = m$ and a nonsingular $J$, the method is the [Newton-Raphson inverse kinematics](/newton-raphson-inverse-kinematics/) iteration.
- **Rate control.** Used once per control step with a small gain in place of the full step, the same formula is [resolved-rate motion control](/resolved-rate-motion-control/).

## When to use it

Use the pseudoinverse method when an arm has no closed form inverse kinematics, or has more joints than the task, and a reasonable initial guess is at hand: the present configuration, the last solution along a path, or a guess from a coarse table.
If the target may be out of reach or close to a singularity, prefer damped least squares; if all solutions are needed, use an analytic method for the arm or many restarts.

## Pitfalls

- **Units.** For a pose task, the error mixes radians and meters, and $J^{+}$ minimizes a joint norm that mixes radians and, for prismatic joints, meters. Scale the rows and columns on purpose.
- **Frames.** $\mathcal V_b$ and $J_b$ must be in the same frame and the same order; a space twist error with a body Jacobian, or the linear part first in one and last in the other, breaks the convergence without an error.
- **The rank tolerance.** If the pseudoinverse keeps tiny singular values, the step can be huge near a singularity; if it drops singular values that are only small, the step loses a direction. The cut, here $10^{-10}\sigma_{\max}$, is a rule of thumb.
- **Joint wrapping.** Revolute joint values can grow by multiples of $2\pi$; wrap them into the range of the joints after the loop.
- **Joint limits.** The plain method does not see them, and it can return a solution outside the range of a joint.
- **No convergence.** A target out of reach, or a start far from every solution, leads to steps that jump around; bound the number of iterations and report FAILURE.

## Implementations

## History

Penrose (1955) defined the generalized inverse by four equations and showed that it gives the least squares solution of least norm, which is the step of this method.
Whitney (1969) resolved end effector rates into joint rates through the inverse of the Jacobian, and the same linear step, repeated until the pose error vanishes, solves the position problem.
Klein and Huang (1983) reviewed pseudoinverse control of redundant arms, and later work added damping near singularities.
Lynch and Park (2017) present the loop of this page, with the body twist error from the matrix logarithm, as their numerical inverse kinematics algorithm.

## References
