---
tag: XNS6ZX
kind: algorithm
slug: resolved-rate-motion-control
name: Resolved-rate motion control
aliases:
- resolved motion rate control
area: robotics/robot-kinematics
level: core
summary: Whitney's scheme that turns a desired end effector velocity into joint rates through the inverse or pseudoinverse Jacobian.
model: real-ram
complexity:
  vars: {n: the number of joints, m: the dimension of the task, N: the number of control steps}
  time: {worst: Θ(N m^2 n)}
  space: {extra: Θ(m n)}
properties: {deterministic: true, online: true, recursive: false}
history:
  year: 1969
  people: [Daniel E. Whitney]
  note: Whitney proposed to command the end effector velocity and to resolve it into joint rates through the inverse of the Jacobian, for manipulators and arm prostheses.
prereqs: [geometric-jacobian, pseudoinverse]
see_also: [jacobian-pseudoinverse-method, null-space-projection, damped-least-squares-inverse-kinematics, jacobian-transpose-method, kinematic-singularity, image-based-visual-servoing, euler-method, inverse-kinematics]
sources:
  - paper: doi:10.1109/TMMS.1969.299896
    title: Daniel E. Whitney, Resolved motion rate control of manipulators and human prostheses, IEEE Transactions on Man-Machine Systems, 1969
    locator: the whole paper (the end effector velocity command resolved into joint rates by the inverse Jacobian)
  - book: isbn:9781846286414
    title: "Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics: Modelling, Planning and Control, Springer, 2009"
    locator: Chapter 3, Section 3.5 (inverse differential kinematics, the inverse and the pseudoinverse) and Section 3.7.1 (the Jacobian inverse algorithm with feedback of the task error)
  - book: isbn:9781107156302
    title: "Kevin M. Lynch and Frank C. Park, Modern Robotics: Mechanics, Planning, and Control, Cambridge University Press, 2017"
    locator: Chapter 6, Section 6.3 (inverse velocity kinematics, joint rates from the pseudoinverse of the Jacobian)
  - paper: doi:10.1109/TSMC.1983.6313123
    title: Charles A. Klein and Ching-Hsiang Huang, Review of pseudoinverse control for use with kinematically redundant manipulators, IEEE Transactions on Systems, Man, and Cybernetics 13, 245-250, 1983
    locator: the whole paper (pseudoinverse rate control of redundant arms and the lack of repeatability for closed task paths)
---

Resolved-rate motion control moves the end effector of a robot arm along a desired path by commanding joint velocities, not joint positions.
At each control step it reads the joint values $q$, forms the [Jacobian](/geometric-jacobian/) $J(q)$, and solves $J\dot q = v$ for the joint rates, where $v$ is the desired end effector velocity plus a correction for the present error.
For a square, nonsingular $J$ the solution is $J^{-1}v$; for a redundant arm it is the least norm solution $J^{+}v$ with the [pseudoinverse](/pseudoinverse/).
Daniel Whitney introduced the scheme in 1969, and it is still the basic way to drive an arm in Cartesian coordinates, for example from a joystick.

## In plain words

You want the hand of a robot to move in a straight line, but you can only tell each motor how fast to turn.
At this moment, a small turn of each motor moves the hand in some known direction.
So you ask: which mix of motor speeds moves the hand exactly the way I want right now?
That is a small system of linear equations, and you solve it.
A moment later the arm has a new shape, so you ask again, and you keep doing this many times each second.
Because each answer is only right for an instant, the hand slowly drifts away from the path.
A small correction, which pulls the hand back toward where it should be, removes the drift.

## The problem

**Input.**

- A forward kinematics map $x = f(q)$ from joint values $q \in \mathbb{R}^n$ to task coordinates $x \in \mathbb{R}^m$, with $m \le n$, and its Jacobian $J(q) = \partial f / \partial q$.
- A desired task path $x_d(t)$ for $0 \le t \le T$, with its velocity $\dot x_d(t)$.
- A start configuration $q_0$, a gain matrix $K$ (often $kI$ with $k \ge 0$), a time step $\Delta t$ and a number of steps $N$.

**Output.** Joint rates $\dot q_j$ for the steps $j = 0, \dots, N - 1$, and the joint values $q_j$ that they produce, such that $f(q_j)$ stays close to $x_d(t_j)$, with $t_j = j\Delta t$.

The scheme needs $J(q)$ to have full row rank $m$ along the path.
For a position task, $f$ is the position of the end effector.
For a full pose, $v$ is a twist and the error is a twist too, for example the body twist of the logarithm of $T(q)^{-1}T_d(t)$, and $J$ must be the Jacobian in the same frame and the same order as $v$.

## The algorithm

```pseudo id=main
RESOLVED-RATE(FK, JACOBIAN, q0, x_d, x_d', K, Δt, N)
L1  q ← q0
L2  for k ← 0 to N - 1
L3      t ← k Δt
L4      e ← x_d(t) - FK(q)                    ▷ task error
L5      J ← JACOBIAN(q)
L6      v ← x_d'(t) + K e                     ▷ feedforward plus feedback
L7      q' ← J^+ v                            ▷ least norm solution of J q' = v
L8      q ← q + Δt q'                         ▷ the joint servos run q' for one step
L9  return q_0, q_1, ..., q_N
```

Line L7 uses $J^{+} = J^{\mathsf T}(JJ^{\mathsf T})^{-1}$, which is $J^{-1}$ when $m = n$; it is computed by solving the $m \times m$ system $(JJ^{\mathsf T})y = v$ and setting $\dot q = J^{\mathsf T}y$.
On a real robot, line L8 is done by the joint velocity servos; in simulation it is one explicit [Euler step](/euler-method/).
With $K = 0$, the scheme is open loop, as in Whitney's paper.
With $K$ positive definite, it is the closed-loop form of Siciliano et al., which keeps the error small.

## Example

Take a planar 2R arm with unit links and the position task $f(q) = (\cos q_1 + \cos(q_1 + q_2),\ \sin q_1 + \sin(q_1 + q_2))$.
The tip must go around the circle with center $(1, 0.8)$ m and radius 0.3 m at 1 rad/s:

$$x_d(t) = (1 + 0.3\cos t,\ 0.8 + 0.3\sin t), \qquad \dot x_d(t) = (-0.3\sin t,\ 0.3\cos t), \qquad 0 \le t \le 2 \text{ s}.$$

The start is the [inverse kinematics](/inverse-kinematics/) solution with $q_2 > 0$ at $x_d(0) = (1.3, 0.8)$: $q_0 = (-0.150864, 1.405038)$.

- Line L4: $e = 0$.
- Line L5: $J(q_0) = \begin{pmatrix} -0.8 & -0.950293 \\ 1.3 & 0.311358 \end{pmatrix}$, with $\det J = \sin q_2 = 0.986294$, far from singular.
- Line L6: $v = \dot x_d(0) = (0, 0.3)$ m/s.
- Line L7: $\dot q = J^{-1}v = (0.289050, -0.243335)$ rad/s.
- Line L8: with $\Delta t = 0.01$ s, $q_1 = (-0.147974, 1.402605)$.

The table gives the tip error $|x_d(2) - f(q_N)|$ at the end of the run.

| gain $k$ | $\Delta t = 0.02$ s | $\Delta t = 0.01$ s | $\Delta t = 0.005$ s |
|---|---|---|---|
| 0 (open loop) | $3.83 \cdot 10^{-3}$ m | $1.92 \cdot 10^{-3}$ m | $9.58 \cdot 10^{-4}$ m |
| 10 s⁻¹ | | $1.10 \cdot 10^{-4}$ m | $5.49 \cdot 10^{-5}$ m |

Open loop, the error grows along the path and halves when the step halves: it is the first order drift of the Euler steps.
With $k = 10$, the error stays bounded by about $\Delta t$ times a constant over $k$, and at $\Delta t = 0.005$ s the final joint values are $(0.08035, 1.61239)$, against the exact $(0.08030, 1.61242)$.

To see the feedback act on a start error, move the start to $q_0 + (0.1, -0.1)$, which puts the tip $0.09996$ m away from $x_d(0)$.
Open loop, the error stays near 0.1 m for the whole run, and it is $0.102$ m at the end.
With $k = 20$ and $\Delta t = 0.01$ s, the error decays like $e^{-20t}$ and stays below $6 \cdot 10^{-5}$ m from $t = 1$ s on.

## Correctness

**The step.** If $J$ has full row rank, then $\dot q = J^{+}v$ satisfies $J\dot q = JJ^{\mathsf T}(JJ^{\mathsf T})^{-1}v = v$, and among all solutions it has the least norm, because every other solution differs from it by a vector of $\operatorname{null}(J)$, which is orthogonal to $J^{+}v \in \operatorname{range}(J^{\mathsf T})$.

**Continuous time.** If the joints follow $\dot q = J^{+}(\dot x_d + Ke)$ exactly, then the error $e = x_d - f(q)$ satisfies

$$\dot e = \dot x_d - J\dot q = \dot x_d - (\dot x_d + Ke) = -Ke.$$

So the error obeys a linear equation with no coupling to the arm: $e(t) = e^{-Kt}e(0)$.
With $K = kI$ and $k > 0$, every error decays at the rate $k$; with $K = 0$ the error stays at $e(0)$, so the open-loop scheme tracks the path exactly from an exact start, and keeps any start error.

**Discrete time.** The proof below shows the following bound for $K = \kappa I$.
Let $\sigma_{\min}(J(q)) \ge \sigma_0 > 0$ on a neighborhood of the path, let $A$ bound $|\ddot x_d|$, let $H$ bound the second derivative of $f$, and let $V$ bound $|\dot x_d|$.
Then for $0 < \kappa\Delta t \le 1$ and $\Delta t$ small enough,

$$|e_N| \le (1 - \kappa\Delta t)^N |e_0| + \frac{c\,\Delta t}{\kappa}, \qquad c = \frac{A + H\rho^2}{2},$$

where $\rho$ bounds the joint rates.
For $K = 0$, $|e_N| \le |e_0| + c\,t_N\Delta t$.
Both bounds match the example: the open-loop error grows with $t$ and is proportional to $\Delta t$, and the closed-loop error is proportional to $\Delta t / \kappa$.

## Complexity

Each step evaluates $f$ and $J$, which costs $\Theta(n)$ for a serial arm with a task of fixed size, forms $JJ^{\mathsf T}$ in $\Theta(m^2 n)$, solves an $m \times m$ system in $\Theta(m^3)$, and multiplies by $J^{\mathsf T}$ in $\Theta(mn)$.
Since $m \le n$, a step costs $\Theta(m^2 n)$, and $N$ steps cost $\Theta(N m^2 n)$ in the [real RAM](/real-ram/).
The extra space is $\Theta(mn)$ for $J$ and its products, plus $\Theta(Nn)$ if the whole joint path is kept.
For a 6-joint arm and a 6-dimensional task, a step is a few hundred arithmetic operations, small enough for a control loop that runs many hundreds of times per second.

## Properties

- **Online.** Each step needs only the present $q$ and the present values of $x_d$ and $\dot x_d$; the path can come from a joystick or a sensor as it goes.
- **Local.** The scheme follows the path step by step; it does not plan, and it does not see joint limits or obstacles unless a [null space](/null-space-projection/) term is added.
- **Linear error dynamics.** In continuous time, the task error obeys $\dot e = -Ke$ whatever the arm, as long as $J$ has full row rank.
- **Least norm rates.** For a redundant arm, $J^{+}v$ is the smallest joint velocity that gives $v$; this is a choice, and other inverses give other motions with the same task velocity.
- **Not repeatable.** For a redundant arm, a closed task path in general does not give a closed joint path with pseudoinverse rates; Klein and Huang (1983) discussed this lack of repeatability.
- **Fails at singularities.** As $\sigma_{\min}(J) \to 0$, the joint rates for a fixed $v$ grow like $1/\sigma_{\min}$, and at a [kinematic singularity](/kinematic-singularity/) line L7 is undefined.

## Variants and improvements

- **Damped least squares.** Replace $J^{+}$ by $J^{\mathsf T}(JJ^{\mathsf T} + \lambda^2 I)^{-1}$, which bounds the joint rates near singularities at the price of a tracking error; see [damped least squares inverse kinematics](/damped-least-squares-inverse-kinematics/).
- **The transpose.** Replace $J^{+}$ by $\alpha J^{\mathsf T}$, which needs no inverse; for $\dot x_d = 0$ and $K = kI$ it gives $\dot e = -\alpha k JJ^{\mathsf T}e$, so $|e|$ never increases; see the [Jacobian transpose method](/jacobian-transpose-method/).
- **A null space term.** For a redundant arm, add $(I - J^{+}J)z$ to pursue a second goal, as in [null space projection](/null-space-projection/).
- **Orientation.** For a full pose, use the twist error from the matrix logarithm of $T(q)^{-1}T_d$ with the body Jacobian, or Euler angle errors with the [analytic Jacobian](/analytic-jacobian/).
- **Acceleration level.** Resolved acceleration control differentiates once more and commands joint accelerations, which a [computed torque](/computed-torque-control/) loop turns into torques.
- **Rate limits.** If $\dot q$ exceeds a joint speed limit, scaling the whole vector down keeps the direction of the end effector motion and slows it.
- **Visual servoing.** [Image-based visual servoing](/image-based-visual-servoing/) uses the same law with the interaction matrix of image features in place of $J$.

## When to use it

Use resolved-rate control to drive an end effector in Cartesian coordinates in real time: teleoperation with a joystick or a master arm, small corrections from a force or vision sensor, and smooth paths that stay away from singularities.
Add feedback ($K \ne 0$) whenever the controller integrates the rates itself, to remove the drift.
For a single goal pose with no path to follow, the [Jacobian pseudoinverse method](/jacobian-pseudoinverse-method/) of inverse kinematics is the same step used as an iteration.
Near singularities, use damped least squares; for paths with joint limits and obstacles, plan the path first.

## Pitfalls

- **Singularities.** A path that passes near a singularity asks for huge joint rates. Watch $\sigma_{\min}$ or the [manipulability](/yoshikawa-manipulability-measure/), and switch to damping or slow down; the threshold is a rule of thumb for each arm.
- **Open-loop drift.** With $K = 0$, the Euler steps and the servo errors add up, and the tip leaves the path. Use $K \ne 0$.
- **Gain and step.** For the discrete loop, the error of a fixed target follows $e_{j+1} \approx (1 - k\Delta t)e_j$, which changes sign at every step for $k\Delta t > 1$ and diverges for $k\Delta t > 2$. Keep $k\Delta t$ well below 1.
- **Frames and order.** The velocity $v$ and the Jacobian must be in the same frame and use the same order of the angular and the linear parts; a space twist with a body Jacobian gives wrong motion without an error.
- **Mixed units.** For a pose task, $J^{+}$ minimizes a sum of squares of joint rates, but the gain $K$ mixes rad and m; scale the angular and the linear errors on purpose.
- **Joint limits.** The scheme does not see them; a joint can reach its limit while the task is still feasible for another posture.

## Implementations

## History

Whitney (1969) proposed to command the velocity of the end effector and to resolve it into joint rates through the inverse of the Jacobian, for manipulators and for arm prostheses, and named the method resolved motion rate control.
Liégeois (1977) added the projection onto the null space for redundant arms, and Klein and Huang (1983) reviewed pseudoinverse rate control of redundant arms and its lack of repeatability.
Textbooks such as Siciliano et al. (2009) present it with feedback of the task error as the Jacobian inverse algorithm of closed-loop inverse kinematics, and Lynch and Park (2017) as inverse velocity kinematics.

## References
