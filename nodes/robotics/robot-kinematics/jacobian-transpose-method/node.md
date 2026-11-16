---
tag: NPCR98
kind: algorithm
slug: jacobian-transpose-method
name: Jacobian transpose method
aliases:
- Jacobian transpose inverse kinematics
area: robotics/robot-kinematics
level: core
summary: Steps the joints by a gain times J^T e, a gradient step on the squared pose error that needs no matrix inverse.
model: real-ram
complexity:
  vars: {m: the number of task coordinates, n: the number of joints, k: the number of iterations}
  time: {worst: Θ(k m n)}
  space: {extra: Θ(m n)}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 1984
  people: [William A. Wolovich, H. Elliott, A. Balestrino, G. De Maria, Lorenzo Sciavicco]
  note: Wolovich and Elliott, and Balestrino, De Maria and Sciavicco, proposed in 1984 to move the joints along the transpose of the Jacobian times the task error.
prereqs: [inverse-kinematics, geometric-jacobian, gradient-descent]
see_also: [gradient-descent, damped-least-squares-inverse-kinematics, jacobian-pseudoinverse-method, newton-raphson-inverse-kinematics, cyclic-coordinate-descent-inverse-kinematics, resolved-rate-motion-control, kinematic-singularity, singular-value-decomposition]
sources:
  - paper: doi:10.1109/CDC.1984.272258
    title: "William A. Wolovich and H. Elliott, A computational technique for inverse kinematics, Proceedings of the 23rd IEEE Conference on Decision and Control, 1359-1363, 1984"
    locator: the iteration with the transpose of the Jacobian
  - paper: doi:10.1016/S1474-6670(17)61347-8
    title: "A. Balestrino, G. De Maria and L. Sciavicco, Robust control of robotic manipulators, IFAC Proceedings Volumes (9th IFAC World Congress), 1984"
    locator: the use of the Jacobian transpose for inverse kinematics
  - book: "Samuel R. Buss, Introduction to Inverse Kinematics with Jacobian Transpose, Pseudoinverse and Damped Least Squares methods, unpublished survey, University of California, San Diego, 2004"
    locator: Section 3 (the Jacobian transpose method)
  - book: isbn:9781846286414
    title: "Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics: Modelling, Planning and Control, Springer, 2009"
    locator: Section 3.7 (inverse kinematics algorithms)
---

The Jacobian transpose method solves the inverse kinematics of an arm by repeated small joint steps $\Delta\theta = \alpha J^{\mathsf T}e$, where $J$ is the Jacobian, $e$ is the task error and $\alpha > 0$ is a gain.
For a position task, $J^{\mathsf T}e$ is the negative gradient of half the squared error, so the method is [gradient descent](/gradient-descent/) on the error.
It needs no matrix inverse and no linear solve, so each step is cheap, and it stays defined at a [kinematic singularity](/kinematic-singularity/).
The price is slow, linear convergence, and a gain that must be chosen with care.

## In plain words

Imagine the target pulls on the hand of the arm with a spring.
Each joint feels a turning push from that pull, larger when turning that joint moves the hand more toward the target.
The method turns each joint a little in the direction of its push, and then looks again.
The pushes are cheap to compute, because no system of equations is solved.
Small turns always bring the hand closer, but the hand may approach slowly.
Turns that are too large overshoot, and the arm can swing back and forth around the target.
If the target is out of reach, the arm stretches toward it and stops.

## The problem

**Input.**

- A task map $x = f(\theta)$ from $n$ joint values to $m$ task coordinates and its Jacobian $J(\theta)$, an $m \times n$ matrix.
For a full pose, $e$ is a twist error and $J$ the matching [geometric Jacobian](/geometric-jacobian/).
- A target $x_d$, an initial guess $\theta^0$, a gain $\alpha > 0$ or the rule to choose it, a tolerance $\varepsilon$ and a step limit $k_{\max}$.

**Output.** A $\theta$ with $|x_d - f(\theta)| \le \varepsilon$, or the last iterate with the report that the tolerance was not met.

The method does not need $m = n$ or a Jacobian of full rank.

## The algorithm

```pseudo id=main
JACOBIAN-TRANSPOSE-IK(f, J, x_d, θ0, ε, k_max)
L1  θ ← θ0
L2  for k ← 1 to k_max
L3      e ← x_d - f(θ)
L4      if |e| ≤ ε then return θ
L5      J ← JACOBIAN(θ)
L6      g ← J^T e                                  ▷ the negative gradient of |e|^2 / 2
L7      α ← <e, J g> / |J g|^2                      ▷ or a fixed gain α
L8      θ ← θ + α g
L9  return θ with the report that the tolerance was not met
```

Line L7 is the gain of Buss and Kim.
For the linear model $e_{\mathrm{new}} = e - J\Delta\theta$, it is the gain that makes $|e - \alpha JJ^{\mathsf T}e|$ as small as possible.
When $Jg = 0$, then $g = 0$ too, since $|g|^2 = \langle e, Jg\rangle$, and the iterate is a stationary point.
A fixed gain is the other common choice, and it is simpler to analyze.

## Example

All examples use the planar 2R arm with $L_1 = L_2 = 1$ m, the target $(1, 1)$ m and the start $\theta^0 = (0.3, 1.2)$ rad.

At $\theta^0$, the hand is at $(1.026074, 1.293015)$ m and the error is $e = (-0.026074, -0.293015)$ m.
Then $J^{\mathsf T}e = (-0.266942, 0.005281)$, and the step with the gain of Buss and Kim is $(-0.099972, 0.001978)$ rad.

| gain | errors (m) at steps 0 to 4 | steps to $10^{-10}$ m | final error ratio |
|---|---|---|---|
| $\alpha = 0.1$ | 0.294, 0.272, 0.257, 0.246, 0.238 | 569 | 0.962 |
| $\alpha = 0.5$ | 0.294, 0.236, 0.200, 0.171, 0.145 | 105 | 0.809 |
| $\alpha = 2/3$ | 0.294, 0.253, 0.216, 0.178, 0.147 | 77 | 0.745 |
| Buss and Kim | 0.294, 0.237, 0.112, 0.0545, 0.0118 | 14 | 0.129 |
| $\alpha = 0.9$ | 0.294, 0.300, 0.386, 0.506, 0.733 | none | |

All runs that converge end at $(0, \pi/2)$, and their errors never increase.
At the solution, $J^{\mathsf T}J$ has the eigenvalues $\sigma_1^2 = 2.618$ and $\sigma_2^2 = 0.382$.
With a fixed gain, the error ratio tends to $\max_i|1 - \alpha\sigma_i^2|$, which gives 0.962, 0.809 and 0.745 for the first three gains, as the table shows.
The gain $2/3 = 2/(\sigma_1^2 + \sigma_2^2)$ makes this ratio as small as possible.
With $\alpha = 0.9 > 2/\sigma_1^2 = 0.764$, the solution repels the iterates, and the error swings up and down for as long as the loop runs.
For the target $(2.5, 0)$ m, out of reach, both the gain $0.1$ and the gain of Buss and Kim stretch the arm along the x axis, with the hand at $(2, 0)$ m, where $J^{\mathsf T}e = 0$ and the error stays at 0.5 m.

## Correctness

The proof page proves these facts for a position task, $e = x_d - f(\theta)$, with $E(\theta) = \tfrac12|e|^2$.

- **Gradient.** $\nabla E(\theta) = -J(\theta)^{\mathsf T}e$, so L6 is the direction of steepest descent of $E$.
- **Descent.** If $J^{\mathsf T}e \ne 0$, then $E$ decreases along the step for every small enough $\alpha > 0$.
- **The gain of Buss and Kim** is positive and minimizes $|e - \alpha JJ^{\mathsf T}e|$ over $\alpha$.
- **Global result for a fixed gain.** For an arm with revolute joints, $\nabla E$ is Lipschitz with some constant $\Lambda$ on all of joint space, and for $0 < \alpha < 2/\Lambda$ the errors never increase and $J^{\mathsf T}e \to 0$.
So every limit point of the iterates is a stationary point of $E$.
- **Local rate.** At a solution $\theta^*$ with $m = n$ and $J(\theta^*)$ invertible, and a fixed gain $0 < \alpha < 2/\sigma_{\max}^2$, the iteration converges to $\theta^*$ from every start close enough, with the error ratio tending to at most $\max_i|1 - \alpha\sigma_i^2| < 1$.

A stationary point need not be a solution.
The stretched arm aimed at a target out of reach is one, and an arm with a local minimum of the distance to the target is another.
There is no guarantee that the iteration finds a solution when one exists.

## Complexity

One step forms $J^{\mathsf T}e$ in $\Theta(mn)$ and $Jg$ for the gain in $\Theta(mn)$, in the [real RAM](/real-ram/), plus the cost of $f$ and $J$, which is $\Theta(mn)$ for a serial chain.
So $k$ steps cost $\Theta(kmn)$, with no $\Theta(m^3)$ solve as in [damped least squares](/damped-least-squares-inverse-kinematics/).
The extra space is the Jacobian, $\Theta(mn)$.
The number of steps $k$ is not bounded in general.
Near a regular solution with a fixed gain, the number of steps to reach $\varepsilon$ grows like $\log(1/\varepsilon)/\log(1/\rho)$ with $\rho = \max_i|1 - \alpha\sigma_i^2|$, which becomes large when $\sigma_{\min} \ll \sigma_{\max}$.

## Properties

- **No inverse.** No solve and no factorization, only products with $J$ and $J^{\mathsf T}$.
- **Always defined.** The step exists at singularities and for targets out of reach.
- **Linear convergence.** The rate depends on the condition of $J^{\mathsf T}J$ at the solution, and it is slow for an ill conditioned arm.
- **Not invariant.** The step changes with the units and the scaling of the task coordinates and of the joints, unlike the Newton step.
- **Stationary points.** The method can stop at any point with $J^{\mathsf T}e = 0$, which includes singular configurations with $e$ orthogonal to the range of $J$.
- **Redundant arms.** For $m < n$, the step lies in the row space of $J$, so it has no null space component.

## Variants and improvements

- **Gain choice.** A fixed gain, the gain of Buss and Kim, or a [backtracking line search](/backtracking-line-search/) on $E$; the line search keeps the global descent property with no bound $\Lambda$ to know in advance.
- **A gain matrix.** A step $KJ^{\mathsf T}e$ with a symmetric positive definite $K$ keeps the descent property and can scale the joints.
- **Continuous time.** The control law $\dot\theta = KJ^{\mathsf T}e$ makes $\tfrac12|e|^2$ a Lyapunov function for a fixed target, since its derivative is $-e^{\mathsf T}JKJ^{\mathsf T}e \le 0$; this is the closed loop form in textbooks such as Siciliano et al.
- **Damped least squares and the pseudoinverse.** Replacing $J^{\mathsf T}$ with $J^{\mathsf T}(JJ^{\mathsf T} + \lambda^2I)^{-1}$ gives [damped least squares](/damped-least-squares-inverse-kinematics/), and with $\lambda = 0$ the [pseudoinverse method](/jacobian-pseudoinverse-method/); both converge faster per step.
- **Joint by joint.** [Cyclic coordinate descent](/cyclic-coordinate-descent-inverse-kinematics/) also descends on the error, but it minimizes over one joint at a time exactly.

## When to use it

Use the Jacobian transpose method when each step must be very cheap, for example for a long chain in an animation, or when a simple and robust closed loop law is wanted and the speed of convergence matters little.
When a solution must be found fast and accurately, use [damped least squares](/damped-least-squares-inverse-kinematics/) or [Newton-Raphson inverse kinematics](/newton-raphson-inverse-kinematics/).

## Pitfalls

- **Gain too large.** A fixed gain above $2/\sigma_{\max}^2$ near the solution makes the iteration swing and fail, as in the example.
- **Gain too small.** A small fixed gain is safe but can need hundreds of steps for a 2R arm.
- **Scaling.** Mixing positions in m and orientations in rad in $e$ changes the direction of the step; scale the task coordinates on purpose.
- **Stopping at the wrong place.** A small step does not mean a small error; check $|e|$, not $|\Delta\theta|$, before you accept the result.
- **Moving targets.** In closed loop use, a fixed gain gives a tracking lag that grows with the speed of the target.

## Implementations

## History

Wolovich and Elliott (1984) and Balestrino, De Maria and Sciavicco (1984) proposed to move the joints along $J^{\mathsf T}e$ as an inverse kinematics method that needs no inverse of the Jacobian.
The method is the gradient method of optimization applied to the squared task error.
It became popular in computer animation, and the survey of Buss (2004) compared it with the pseudoinverse and damped least squares methods.
Buss and Kim (2005) gave the gain of line L7 together with their selectively damped least squares method.

## References
