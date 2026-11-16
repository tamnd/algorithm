---
tag: J6EXM0
kind: algorithm
slug: damped-least-squares-inverse-kinematics
name: Damped least squares inverse kinematics
aliases:
- DLS inverse kinematics
- Wampler's method
area: robotics/robot-kinematics
level: core
summary: Uses the step J^T (J J^T + l^2 I)^-1 e, which stays bounded near singularities at the cost of some tracking error.
model: real-ram
complexity:
  vars: {m: the number of task coordinates, n: the number of joints with m at most n, k: the number of iterations}
  time: {worst: Θ(k m^2 n)}
  space: {extra: Θ(m n)}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 1986
  people: [Charles W. Wampler, Yoshihiko Nakamura, Hideo Hanafusa]
  note: Wampler and, independently, Nakamura and Hanafusa published the damped least squares step for arms in 1986; Nakamura and Hanafusa called it singularity robust.
prereqs: [inverse-kinematics, geometric-jacobian, pseudoinverse]
see_also: [jacobian-pseudoinverse-method, tikhonov-regularization, levenberg-marquardt, kinematic-singularity, newton-raphson-inverse-kinematics, jacobian-transpose-method, singular-value-decomposition, manipulability-ellipsoid]
sources:
  - paper: doi:10.1109/TSMC.1986.289285
    title: "Charles W. Wampler II, Manipulator inverse kinematic solutions based on vector formulations and damped least-squares methods, IEEE Transactions on Systems, Man, and Cybernetics 16(1), 93-101, 1986"
    locator: the damped least squares formulation of the inverse kinematics step
  - paper: doi:10.1115/1.3143764
    title: "Yoshihiko Nakamura and Hideo Hanafusa, Inverse kinematic solutions with singularity robustness for robot manipulator control, Journal of Dynamic Systems, Measurement, and Control 108(3), 163-171, 1986"
    locator: the singularity robust inverse and its damping factor
  - book: "Samuel R. Buss, Introduction to Inverse Kinematics with Jacobian Transpose, Pseudoinverse and Damped Least Squares methods, unpublished survey, University of California, San Diego, 2004"
    locator: the sections on damped least squares and on the singular value decomposition of the step
---

Damped least squares inverse kinematics moves the joints of an arm toward a target with the step $\Delta\theta = J^{\mathsf T}(JJ^{\mathsf T} + \lambda^2I)^{-1}e$, where $J$ is the Jacobian and $e$ is the task error.
The damping factor $\lambda > 0$ makes the matrix $JJ^{\mathsf T} + \lambda^2I$ invertible at every configuration, also at a [kinematic singularity](/kinematic-singularity/).
The step is never longer than $|e|/(2\lambda)$, so the joints do not jump near a singularity, as they do with the [pseudoinverse](/jacobian-pseudoinverse-method/).
The price is that one step does not remove the whole error, even where the pseudoinverse step would.
The step is the [Tikhonov regularization](/tikhonov-regularization/) of the linear least squares problem $J\Delta\theta \approx e$.

## In plain words

To move the hand of an arm toward a target, you need to know how much to turn each joint.
At some poses of the arm, a tiny motion of the hand needs a huge turn of the joints, for example when the arm is almost straight and the target is a little farther out.
A method that insists on the exact motion then asks for wild joint motions.
Damped least squares asks for a compromise instead.
It looks for a joint motion that brings the hand close to where it should go, but it also pays a penalty for every large joint motion.
Far from such poses, the penalty hardly matters, and the result is almost the exact motion.
Near them, the penalty wins, and the joints move only a little.
Repeating such steps brings the hand to the target, if it can be reached.

## The problem

**Input.**

- A task map $x = f(\theta)$ from $n$ joint values to $m$ task coordinates, with $m \le n$, and its Jacobian $J(\theta)$, an $m \times n$ matrix.
For a full pose, $e$ is a twist error and $J$ is the matching [geometric Jacobian](/geometric-jacobian/), as in [Newton-Raphson inverse kinematics](/newton-raphson-inverse-kinematics/).
- A target $x_d$, an initial guess $\theta^0$, a damping factor $\lambda > 0$, a tolerance $\varepsilon$ and a step limit $k_{\max}$.

**Output.** A $\theta$ with $|x_d - f(\theta)| \le \varepsilon$, or the last iterate with the report that the tolerance was not met.
For a target out of reach, the last iterate is the useful answer, often an arm stretched toward the target.

**One step.** For a fixed $J$ and $e$, the damped least squares step is the unique minimizer of
$$\phi(\Delta\theta) = |J\Delta\theta - e|^2 + \lambda^2|\Delta\theta|^2.$$

## The algorithm

```pseudo id=main
DLS-IK(f, J, x_d, θ0, λ, ε, k_max)
L1  θ ← θ0
L2  for k ← 1 to k_max
L3      e ← x_d - f(θ)
L4      if |e| ≤ ε then return θ
L5      J ← JACOBIAN(θ)
L6      solve (J J^T + λ^2 I) y = e               ▷ an m by m system, positive definite
L7      Δθ ← J^T y
L8      θ ← θ + Δθ
L9  return θ with the report that the tolerance was not met
```

Lines L6 and L7 can also be written $\Delta\theta = (J^{\mathsf T}J + \lambda^2I)^{-1}J^{\mathsf T}e$, an $n \times n$ system with the same result.
Use the smaller of the two systems.
With the singular value decomposition $J = \sum_i \sigma_iu_iv_i^{\mathsf T}$, the step is
$$\Delta\theta = \sum_i \frac{\sigma_i}{\sigma_i^2 + \lambda^2}(u_i^{\mathsf T}e)\,v_i.$$
The pseudoinverse uses the factor $1/\sigma_i$, which grows without bound as $\sigma_i \to 0$.
The damped factor $\sigma_i/(\sigma_i^2 + \lambda^2)$ is close to $1/\sigma_i$ when $\sigma_i \gg \lambda$, goes to 0 when $\sigma_i \to 0$, and is at most $1/(2\lambda)$, with equality at $\sigma_i = \lambda$.

## Example

All examples use the planar 2R arm with $L_1 = L_2 = 1$ m, with the hand at $(\cos\theta_1 + \cos(\theta_1 + \theta_2), \sin\theta_1 + \sin(\theta_1 + \theta_2))$.

**One step near a singularity.** At $\theta = (0, 0.01)$ rad the arm is almost straight, the hand is at $(1.999950, 0.009999)$ m and $\det J = 0.0099998$.
For the target $(1.9, 0.2)$ m the error is $e = (-0.099950, 0.190000)$ m, with $|e| = 0.2147$ m.

| step | $\Delta\theta$ (rad) | $\lvert\Delta\theta\rvert$ (rad) | residual $\lvert e - J\Delta\theta\rvert$ (m) |
|---|---|---|---|
| exact solve $J^{-1}e$ | $(-9.804667, 19.799833)$ | 22.09 | 0 |
| DLS, $\lambda = 0.01$ | $(-1.570567, 3.331712)$ | 3.683 | 0.0823 |
| DLS, $\lambda = 0.1$ | $(0.056365, 0.077488)$ | 0.0958 | 0.0986 |
| DLS, $\lambda = 0.5$ | $(0.071818, 0.037885)$ | 0.0812 | 0.0992 |

The exact step turns the elbow by almost 20 rad, which is useless, since the linear model is only valid for small steps.
The damped steps are small and point the right way.

**Iteration to a reachable target.** For the target $(1, 1)$ m from $\theta^0 = (0.3, 1.2)$ rad, both damping factors end at the solution $(0, \pi/2)$.

| $\lambda$ | errors (m) at steps 0 to 4 | steps to $10^{-10}$ |
|---|---|---|
| 0.1 | 0.294, 0.0415, 0.00138, 3.45e-5, 8.8e-7 | 7 |
| 0.5 | 0.294, 0.123, 0.051, 0.0206, 0.00823 | 24 |

The convergence is linear.
At the solution, $J^{\mathsf T}J$ has the eigenvalues $(3 \pm \sqrt 5)/2$, so the least singular value is $\sigma_{\min} = 0.618$.
The proof page shows that the error ratio tends to $\lambda^2/(\sigma_{\min}^2 + \lambda^2)$, which is 0.0255 for $\lambda = 0.1$ and 0.396 for $\lambda = 0.5$, and these are the ratios that the iteration shows.

**A target out of reach.** For the target $(2.5, 0)$ m, which is beyond the reach of 2 m, start at $(0.2, 0.5)$ rad.
With $\lambda = 0.5$, the errors are 1.132, 0.5404, 0.5021, 0.5001, and the arm stops stretched along the x axis, with the hand at $(2, 0)$, the nearest point to the target.
With $\lambda = 0.1$, the iteration does not settle: the error jumps between about 0.51 and 1.48 m for as long as it runs, and every step still obeys the bound $|\Delta\theta| \le |e|/(2\lambda)$.
With $\lambda = 0.2$ it falls into a cycle of two bent poses, mirror images of each other, with the error 0.601 m.
These are measured results on this one arm, not general rules.

## Correctness

The proof page proves these facts for $\lambda > 0$.

- The matrices $JJ^{\mathsf T} + \lambda^2I$ and $J^{\mathsf T}J + \lambda^2I$ are positive definite, so L6 always has one solution, and the two forms of the step are equal.
- The step is the unique minimizer of $\phi$.
- The step has the singular value form above, so $|\Delta\theta| \le |e|/(2\lambda)$ for every $J$.
- As $\lambda \to 0$, the step tends to the pseudoinverse step $J^{+}e$, for every $J$.
- The residual after one linear step is $e - J\Delta\theta = \lambda^2(JJ^{\mathsf T} + \lambda^2I)^{-1}e$, which is not zero unless $e = 0$.
This is the tracking error that the damping costs.
- If $J$ has full row rank, the step is zero only when $e = 0$, so the iteration can stop only at a solution.
- If $m = n$ and $J(\theta^*)$ is invertible at a solution $\theta^*$, the iteration converges to $\theta^*$ from every start close enough, and the error falls by a factor that tends to at most $\lambda^2/(\sigma_{\min}^2 + \lambda^2) < 1$ per step.

There is no global guarantee.
From a far start, or for a target out of reach, the iteration can cycle, as in the example.

## Complexity

One step forms $JJ^{\mathsf T}$ in $\Theta(m^2n)$, solves the $m \times m$ system in $\Theta(m^3)$, and forms $J^{\mathsf T}y$ in $\Theta(mn)$, in the [real RAM](/real-ram/).
With $m \le n$, this is $\Theta(m^2n)$ per step, plus the cost of $f$ and $J$, which is $\Theta(mn)$ for a serial chain.
So $k$ steps cost $\Theta(km^2n)$.
The extra space is the Jacobian and the $m \times m$ matrix, $\Theta(mn)$.
The number of steps $k$ is not bounded in general; near a regular solution, it grows like $\log(1/\varepsilon)$ with the rate above.

## Properties

- **Always defined.** The step exists at every configuration and for every error, also at singularities and for targets out of reach.
- **Bounded steps.** $|\Delta\theta| \le |e|/(2\lambda)$.
- **Slower than Newton.** Near a regular solution the convergence is linear, not quadratic, and slower for larger $\lambda$.
- **A trade-off in one number.** Small $\lambda$ gives accurate but possibly large steps; large $\lambda$ gives small steps and slow progress.
- **Redundant arms.** For $m < n$, the step has no component in the null space of $J$, as for the pseudoinverse.

## Variants and improvements

- **Variable damping.** Nakamura and Hanafusa let the damping grow as the arm approaches a singularity and vanish far from it, using a measure of the distance to the singularity such as the [manipulability](/yoshikawa-manipulability-measure/).
- **Damping only where needed.** Using the singular value form, one can damp only the small singular values, or add damping only along the directions of the least singular vectors.
- **Selectively damped least squares.** Buss and Kim (2005) choose a separate damping for each singular direction from the size of the joint motion it would cause.
- **Levenberg-Marquardt.** Choosing $\lambda$ at each step from the decrease of the error gives the [Levenberg-Marquardt](/levenberg-marquardt/) method, which behaves like Newton near a regular solution and like gradient descent far from it.
- **With a secondary task.** For a redundant arm, a [null space](/null-space-projection/) term $(I - J^{+}J)z$ can be added to the step.
If the projector is built from the damped inverse instead of $J^{+}$, the term is no longer exactly in the null space.

## When to use it

Use damped least squares when the arm may pass near a singularity, or when the target may be out of reach, and a smooth, bounded joint motion matters more than exact tracking at each step.
This is the usual case for real time control of an arm and for character animation.
Use [Newton-Raphson inverse kinematics](/newton-raphson-inverse-kinematics/) when the solution is regular and a fast final convergence matters.
Use the [Jacobian transpose method](/jacobian-transpose-method/) when even the small linear solve is too costly.

## Pitfalls

- **Choosing $\lambda$.** The damping factor is a tuning parameter, and no value is best for all arms and tasks.
Nakamura and Hanafusa make it depend on the distance to a singularity, and Buss says that it must be chosen for the arm and the targets at hand.
- **Units.** The penalty $\lambda^2|\Delta\theta|^2$ and the error $|J\Delta\theta - e|^2$ mix rad and m, so the value of $\lambda$ changes with the units of the task.
- **Oscillation.** A small $\lambda$ with a target out of reach can make the arm jump back and forth, as in the example; a larger $\lambda$ or a limit on the step length helps.
- **Tracking error.** In real time control, each step leaves the residual $\lambda^2(JJ^{\mathsf T} + \lambda^2I)^{-1}e$, so the hand lags behind a moving target.
- **The wrong form.** The $n \times n$ form is wasteful for a redundant arm with $n \gg m$; use the $m \times m$ form.

## Implementations

## History

Wampler (1986) and Nakamura and Hanafusa (1986) brought the damped least squares step to the inverse kinematics of arms in the same year, independently.
Wampler derived it as the minimizer of a sum of the squared error and the squared joint motion.
Nakamura and Hanafusa called it the singularity robust inverse and studied its behavior near singularities with a damping that changes with the configuration.
The same regularization was known much earlier in numerical analysis as Tikhonov regularization, and in nonlinear least squares as the Levenberg-Marquardt method.
Buss (2004) compared the transpose, pseudoinverse and damped least squares methods in a survey that is often cited in computer animation.

## References
