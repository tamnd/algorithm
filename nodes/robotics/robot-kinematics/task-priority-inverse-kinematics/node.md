---
tag: 791J72
kind: algorithm
slug: task-priority-inverse-kinematics
name: Task-priority inverse kinematics
aliases:
- prioritized inverse kinematics
area: robotics/robot-kinematics
level: advanced
summary: Nakamura's method that solves a stack of tasks, each lower task in the null space of the higher ones.
model: real-ram
complexity:
  vars: {n: the number of joints, m: the total number of task coordinates over all levels, k: the number of iterations}
  time: {worst: Θ(k n^2 m)}
  space: {extra: Θ(n^2 + m n)}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 1987
  people: [Yoshihiko Nakamura, Hideo Hanafusa, Tsuneo Yoshikawa]
  note: Nakamura, Hanafusa and Yoshikawa gave the two-level task-priority solution with pseudoinverses for redundant arms; Siciliano and Slotine extended it to any number of levels with a recursive formula in 1991.
prereqs: [kinematic-redundancy, null-space-projection, jacobian-pseudoinverse-method]
see_also: [null-space-projection, kinematic-redundancy, hierarchical-quadratic-programming, whole-body-control, lexicographic-optimization, damped-least-squares-inverse-kinematics, pseudoinverse, singular-value-decomposition]
sources:
  - paper: doi:10.1177/027836498700600201
    title: "Yoshihiko Nakamura, Hideo Hanafusa and Tsuneo Yoshikawa, Task-priority based redundancy control of robot manipulators, The International Journal of Robotics Research 6(2), 3-15, 1987"
    locator: the two-level task-priority solution with the pseudoinverse of the projected Jacobian
  - paper: doi:10.1109/ICAR.1991.240390
    title: "Bruno Siciliano and Jean-Jacques E. Slotine, A general framework for managing multiple tasks in highly redundant robotic systems, Fifth International Conference on Advanced Robotics (ICAR), 1991"
    locator: the recursive formula for any number of priority levels
---

Task-priority inverse kinematics moves a redundant arm so that it meets several tasks with a strict order of importance.
The first task is met as well as possible.
The second task is then met as well as possible with joint motions that do not change the first task, which are the motions in the null space of the first Jacobian.
Each further task uses only the motions left over by all tasks above it.
For two tasks, the joint step is $\Delta\theta = J_1^{+}e_1 + (J_2P_1)^{+}(e_2 - J_2J_1^{+}e_1)$ with the [null space projector](/null-space-projection/) $P_1 = I - J_1^{+}J_1$.
Repeating such steps solves the tasks at the position level.

## In plain words

An arm with more joints than it needs for a job can do the job in many ways.
You can use the spare freedom for a second wish, such as keeping the elbow away from a wall.
But the wishes may conflict, and then you must say which one wins.
This method puts the wishes in a list, most important first.
It first finds the joint motion that best serves the first wish.
Then, among all the motions that leave the first wish exactly as served, it picks the one that best serves the second wish, and so on down the list.
A lower wish can never spoil a higher one.
When a lower wish cannot be met, the arm gets as close to it as the higher wishes allow.

## The problem

**Input.**

- An arm with $n$ joints and $p$ tasks $x_i = f_i(\theta)$ with Jacobians $J_i(\theta)$ of size $m_i \times n$, ordered from the highest priority $i = 1$ to the lowest $i = p$.
- The task errors $e_i = x_{i,d} - f_i(\theta)$ at the present configuration, for one step.
For the iteration, also the targets $x_{i,d}$, an initial guess $\theta^0$ and a stopping rule.

**Output of one step.** The joint step $\Delta\theta$ defined level by level.
Level 1 keeps the $\Delta\theta$ that minimize $|J_1\Delta\theta - e_1|$.
Level $i$ keeps, among the steps kept at level $i - 1$, those that minimize $|J_i\Delta\theta - e_i|$.
The output is the step of least norm among those kept at level $p$.

This is a [lexicographic](/lexicographic-optimization/) least squares problem: the tasks are ranked, not weighted.

## The algorithm

```pseudo id=main
PRIORITY-STEP((J_1, e_1), ..., (J_p, e_p))
L1  Δθ ← 0 ;  P ← I                              ▷ P projects onto the motions still free
L2  for i ← 1 to p
L3      A ← J_i P                                ▷ task i seen through the free motions
L4      A⁺ ← PSEUDOINVERSE(A)
L5      r ← e_i - J_i Δθ                          ▷ what the higher levels left of task i
L6      Δθ ← Δθ + A⁺ r
L7      P ← P - A⁺ A                             ▷ remove the motions that task i uses
L8  return Δθ
```

This is the recursive form of Siciliano and Slotine.
For $p = 2$ it gives the formula of Nakamura, Hanafusa and Yoshikawa, since then $A = J_2P_1$ and $r = e_2 - J_2J_1^{+}e_1$.
The code on this page computes the pseudoinverse with a one-sided Jacobi singular value decomposition and treats singular values below $10^{-10}$ times the largest as zero.

**The iteration.** For tasks at the position level, the code repeats $\theta \leftarrow \theta + \text{PRIORITY-STEP}(\ldots)$ with the Jacobians and errors at the present $\theta$.
It stops when $|\Delta\theta| \le 10^{-12}$, not when all errors are zero, because a lower task may have no exact solution.

## Example

Take a planar arm with three revolute joints and the link lengths 1, 0.8 and 0.5 m.
The first task puts the hand at $(1.2, 0.6)$ m.
This is two coordinates for three joints, so the arm has one degree of redundancy, a curve of joint values that all reach the target.
The second task asks the elbow, the end of the first link, to be at $c = 0.5(\cos 0.5, \sin 0.5) = (0.438791, 0.239713)$ m.
The elbow always lies on the unit circle, so this task cannot be met exactly.
The best the arm can do is the elbow angle $\theta_1 = 0.5$ rad, with the elbow error 0.5 m, if the hand can still reach its target from there, which it can.

The start $\theta^0 = (0, 0.574014, 2.230016)$ rad puts the hand on its target.

| step | $\theta$ (rad) | hand error (m) | elbow error (m) |
|---|---|---|---|
| 0 | (0.000000, 0.574014, 2.230016) | 2.5e-16 | 0.610260 |
| 1 | (0.239713, 0.208759, 2.684896) | 0.0139 | 0.532620 |
| 2 | (0.368392, -0.030953, 2.862660) | 0.0121 | 0.508574 |
| 3 | (0.434006, -0.239992, 2.903268) | 0.00787 | 0.502172 |
| 4 | (0.466979, -0.390844, 2.889575) | 0.00223 | 0.500545 |
| 42 | (0.500000, -0.536467, 2.873908) | 4e-16 | 0.500000 |

The hand error is not zero during the run, because each step keeps the hand still only to first order; the next step corrects it first.
The distance of $\theta_1$ to 0.5 halves at each step, which is linear convergence.
A brute force search over the curve of joint values that reach the hand target confirms that 0.5 m is the least elbow error.

With the second task changed to put the end of the second link at $(0.5, 0.5)$ m, the iteration stops after 35 steps with that point at $(0.705025, 0.529289)$ m, the point of the circle of radius 0.5 m about the hand target that is nearest to $(0.5, 0.5)$.
If instead the two tasks are stacked into one $4 \times 3$ Jacobian and solved with one pseudoinverse per step, the hand is not kept on its target: in this run, it ends 1.53 m away from it.

## Correctness

The proof page shows by induction over the levels that, after level $i$ of the loop, the steps kept by the levels $1, \ldots, i$ form the set $\Delta\theta + \operatorname{range}(P)$.
Here $P$ is the orthogonal projector onto the motions that change none of the tasks $1, \ldots, i$, and $\Delta\theta$ is the element of least norm of this set.
Two facts carry the induction: $(J_iP)^{+}$ has its range inside the range of $P$, and $P - (J_iP)^{+}(J_iP)$ is again an orthogonal projector, onto the free motions that also leave task $i$ unchanged.

Consequences:

- **Strict priority.** The tasks of lower priority cannot change $J_j\Delta\theta$ for a task $j$ of higher priority.
- **The first task.** If $J_1$ has full row rank, $J_1\Delta\theta = e_1$ exactly.
- **Fixed points.** If the iteration stops with $\Delta\theta = 0$ at a configuration where $J_1$ has full row rank, then $e_1 = 0$, and the gradient of $\tfrac12|e_2|^2$ along the free motions is zero, so the second task is at a stationary point on the set where the first task is met.

The iteration has no global guarantee.
A far start can give large steps, and near an algorithmic singularity the steps can be very large, as explained under Pitfalls.

## Complexity

One step with $p$ levels and $m = \sum_i m_i$ task coordinates forms $J_iP$ in $\Theta(m_in^2)$, computes a pseudoinverse of an $m_i \times n$ matrix, and updates $P$ in $\Theta(m_in^2)$, in the [real RAM](/real-ram/).
With a pseudoinverse that costs $\Theta(m_i^2n)$, for example through a factorization of $AA^{\mathsf T}$ when $A$ has full row rank, one step costs $\Theta(n^2m)$, and $k$ steps cost $\Theta(kn^2m)$.
A [singular value decomposition](/singular-value-decomposition/) by Jacobi sweeps, as in the code, costs $\Theta(m_in^2)$ per sweep, with a number of sweeps that is small in practice but not bounded by a formula.
The extra space is $P$ and the Jacobians, $\Theta(n^2 + mn)$.
The number of iterations $k$ is not bounded in general; in the example it is 42.

## Properties

- **Strict hierarchy.** A higher task is never traded for a lower one, unlike a weighted sum of the task errors.
- **Least norm.** Among all steps that serve the tasks in order, the method takes the shortest one.
- **Equality tasks only.** The basic method handles tasks of the form $J_i\Delta\theta = e_i$; inequalities, such as joint limits, need a [hierarchical quadratic program](/hierarchical-quadratic-programming/).
- **Local.** At the position level, the iteration is a local method, like the other Jacobian methods.

## Variants and improvements

- **Two levels with a gradient.** A common special case keeps one task and adds $(I - J_1^{+}J_1)z$ with $z$ the negative gradient of a cost, such as the distance to joint limits; this is the classical [null space projection](/null-space-projection/).
- **Many levels.** Siciliano and Slotine gave the recursive formula of lines L1 to L8 for any number of levels.
- **Robust to algorithmic singularities.** Chiaverini (1997) drops the term $-J_2J_1^{+}e_1$ for the lower task and uses damped least squares for the projected Jacobian, which removes the large steps at the cost of exact priority.
- **Damping.** Replacing each pseudoinverse by a [damped least squares](/damped-least-squares-inverse-kinematics/) inverse bounds the steps near singularities, and the priority is then only approximate.
- **Inequalities.** Hierarchical quadratic programming solves a stack of equality and inequality tasks in priority order, and it is the usual tool in [whole-body control](/whole-body-control/).

## When to use it

Use task-priority inverse kinematics on a redundant arm or a humanoid when some tasks must be met exactly, such as the hand pose, and others are wishes, such as a posture, a gaze direction or the distance to an obstacle.
When the tasks are equally important and a trade-off is wanted, weight them in one least squares problem instead.
When there are inequalities, use hierarchical quadratic programming.

## Pitfalls

- **Algorithmic singularities.** $J_2P_1$ can lose rank even when $J_1$ and $J_2$ both have full rank, when the two tasks need the same motion.
Near such a configuration, $(J_2P_1)^{+}$ gives very large steps; use a damped inverse or the form of Chiaverini.
- **Rank tolerance.** The pseudoinverse needs a threshold on the singular values; a threshold that is too small lets near-singular directions blow up, and one that is too large drops real motions.
- **Weights do not give priority.** Stacking the tasks into one Jacobian with weights only trades the errors against each other, and the first task is not met, as in the example.
- **Units.** Each level compares only errors of its own task, but a task that mixes positions and angles still needs a choice of scale.
- **The order of the product.** $P_1$ must multiply $J_2$ on the right, $J_2P_1$; the range of $(J_2P_1)^{+}$ is then inside the null space of $J_1$.

## Implementations

## History

Redundant arms had been controlled with the pseudoinverse plus a null space term since the 1970s.
Nakamura, Hanafusa and Yoshikawa (1987) gave the task-priority formulation, with the second task solved in the null space of the first and the pseudoinverse of the projected Jacobian $J_2P_1$, and studied the singularities it brings.
Siciliano and Slotine (1991) extended it to any number of levels with the recursive formula.
Chiaverini (1997) proposed a form that stays bounded at algorithmic singularities.
Later work, such as hierarchical quadratic programming, added inequality tasks to the hierarchy.

## References
