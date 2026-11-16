---
tag: 85CD1Z
kind: algorithm
slug: newton-raphson-inverse-kinematics
name: Newton-Raphson inverse kinematics
aliases:
- numerical inverse kinematics
area: robotics/robot-kinematics
level: core
summary: Solves the pose equations by Newton steps with the body Jacobian and the matrix logarithm of the pose error, from an initial guess.
model: real-ram
complexity:
  vars: {n: the number of joints and of task coordinates, k: the number of iterations}
  time: {worst: Θ(k n^3)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 1968
  people: [Donald L. Pieper]
  note: Pieper's thesis on the kinematics of manipulators studied Newton-Raphson iteration as a general numerical method for arms with no closed form solution.
prereqs: [inverse-kinematics, space-and-body-jacobian, newton-method-for-systems]
see_also: [newton-method-for-systems, quadratic-convergence, jacobian-pseudoinverse-method, damped-least-squares-inverse-kinematics, jacobian-transpose-method, paden-kahan-subproblems, kinematic-singularity, se3-exponential-map]
sources:
  - book: isbn:9781107156302
    title: "Kevin M. Lynch and Frank C. Park, Modern Robotics: Mechanics, Planning, and Control, Cambridge University Press, 2017"
    locator: Chapter 6, Section 6.2 (numerical inverse kinematics with the body Jacobian and the matrix logarithm)
  - book: "Donald L. Pieper, The Kinematics of Manipulators under Computer Control, PhD thesis, Stanford University, 1968 (Stanford Artificial Intelligence Memo AIM-72)"
    locator: Chapter IV, Section 4.1 (the Newton-Raphson method)
---

Newton-Raphson inverse kinematics finds joint values $\theta$ with $T(\theta) = T_d$ for a target pose $T_d$, starting from a guess $\theta^0$.
At each step it measures the pose error as a twist $\mathcal V_b$, the matrix logarithm of $T(\theta)^{-1}T_d$.
Then it solves a linear system with the body Jacobian $J_b(\theta)$ for a joint step and adds the step to $\theta$.
Near a solution where $J_b$ is invertible, the error falls quadratically, so a few steps reach full machine precision.
The method finds one solution, the one that the guess leads to, and it can fail from a poor guess or at a [kinematic singularity](/kinematic-singularity/).

## In plain words

You want the arm to put its hand at a given place and in a given direction.
You start from a guess for the joints and look at where the hand is now.
The gap between where the hand is and where it should be tells you how to turn the joints, if the arm moved in straight lines.
The arm does not move in straight lines, so one correction is not exact, but it brings the hand much closer.
You repeat the correction.
When the guess is already close, each correction roughly doubles the number of correct digits.
When the guess is far, the corrections can jump around, and the hand may end at another of the poses that reach the target, or nowhere.

## The problem

**Input.**

- An arm with $n$ joints in the body form of the [product of exponentials](/product-of-exponentials-formula/), $T(\theta) = Me^{[\mathcal B_1]\theta_1}\cdots e^{[\mathcal B_n]\theta_n}$.
Here $M$ is the home pose of the end effector and $\mathcal B_i = (\omega_i, v_i)$ is the screw axis of joint $i$ in the end effector frame, with the angular part first.
- A target pose $T_d$ and an initial guess $\theta^0$.
- Tolerances $\varepsilon_\omega$ and $\varepsilon_v$, and a step limit $k_{\max}$.

**Output.** A $\theta$ with $|\omega_b| \le \varepsilon_\omega$ and $|v_b| \le \varepsilon_v$, where $(\omega_b, v_b) = \log(T(\theta)^{-1}T_d)$, or FAILURE.

The algorithm below is for a full pose with $n = 6$, so that $J_b$ is square.
For a position task $x(\theta) = x_d$ with as many joints as coordinates, the same loop uses the error $x_d - x(\theta)$ and the Jacobian of $x$.
For an arm with more joints than task coordinates, the linear solve is replaced by a pseudoinverse, which is the [Jacobian pseudoinverse method](/jacobian-pseudoinverse-method/) used as an iteration.

## The algorithm

```pseudo id=main
NEWTON-RAPHSON-IK(M, B_1..B_n, T_d, θ0, ε_ω, ε_v, k_max)
L1  θ ← θ0
L2  for k ← 1 to k_max
L3      V_b ← log(T(θ)^-1 T_d)                    ▷ the pose error as a body twist (ω_b, v_b)
L4      if |ω_b| ≤ ε_ω and |v_b| ≤ ε_v then return θ
L5      J_b ← BODY-JACOBIAN(θ)
L6      solve J_b Δθ = V_b
L7      if J_b is singular then return FAILURE
L8      θ ← θ + Δθ
L9  return FAILURE
```

Line L3 uses the [exponential map of SE(3)](/se3-exponential-map/) in reverse: $\mathcal V_b$ is the twist that, followed for unit time from the present pose, gives the target pose.
Line L5 builds the [body Jacobian](/space-and-body-jacobian/) column by column, with $J_{b,n} = \mathcal B_n$ and $J_{b,i} = \mathrm{Ad}_{e^{-[\mathcal B_n]\theta_n}\cdots e^{-[\mathcal B_{i+1}]\theta_{i+1}}}\mathcal B_i$.
Line L6 is one Gaussian elimination with partial pivoting.
In floating point, L7 means that a pivot is zero or close to zero.

## Example

**A planar arm.** Take the 2R arm with link lengths $L_1 = L_2 = 1$ m, with the hand at $x(\theta) = (\cos\theta_1 + \cos(\theta_1 + \theta_2), \sin\theta_1 + \sin(\theta_1 + \theta_2))$.
The target $(1, 1)$ m has two solutions, $(0, \pi/2)$ and $(\pi/2, -\pi/2)$.
At $(0, \pi/2)$ the Jacobian is $[[-1, -1], [1, 0]]$ with determinant 1.

Start at $\theta^0 = (0.3, 1.2)$ rad.
The hand is at $(1.026073, 1.293015)$, so the error is $(-0.026073, -0.293015)$ with norm $0.294$.
The Jacobian is $[[-1.2930, -0.9975], [1.0261, 0.0707]]$, and the step is $\Delta\theta = (-0.315572, 0.435203)$.

| step | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| error (m) | 0.294 | 0.0517 | 0.00119 | 7.05e-7 | 2.48e-13 |

The iteration ends at $(0, \pi/2)$.
Each error is about a constant times the square of the one before, which is quadratic convergence.
From $\theta^0 = (1.3, -1.2)$ the errors are 0.270, 0.0444, 8.35e-4, 3.44e-7 and 5.92e-14, and the iteration ends at the other solution $(\pi/2, -\pi/2)$.

**An elbow arm.** Take the 6R elbow arm of the [Paden-Kahan subproblems](/paden-kahan-subproblems/) page, with $M = (I, (0, 2.5, 1))$ in m.
Its body screw axes are $\mathcal B_1 = (0, 0, 1, -2.5, 0, 0)$, $\mathcal B_2 = (-1, 0, 0, 0, 0, -2.5)$, $\mathcal B_3 = (-1, 0, 0, 0, 0, -1.5)$, $\mathcal B_4 = (0, 0, 1, -0.5, 0, 0)$, $\mathcal B_5 = (-1, 0, 0, 0, 0, -0.5)$ and $\mathcal B_6 = (0, 1, 0, 0, 0, 0)$.
The target is the pose of $\theta^* = (0.3, -0.4, 0.9, 0.5, 0.7, -0.6)$ rad, with the position $(-0.748090, 1.797966, 0.466418)$ m.

- From $(0.5, -0.6, 1.1, 0.3, 0.9, -0.8)$, the norms $|\mathcal V_b|$ are 0.504, 0.0412, 8.27e-4, 7.14e-7 and 6.02e-13, and the iteration ends at $\theta^*$.
- From $(0, 0, 0.5, 0, 0.5, 0)$, the norms are 1.6, 0.366, 1.22, 0.402, 0.0235, 2.98e-4, 6.9e-8 and 6.83e-15.
The error grows at the third step, and then the quadratic phase starts; the iteration ends at $\theta^*$.
- From $(1, 1, 1, 1, 1, 1)$, the iteration takes 11 evaluations and ends at angles that wrap to $(0.3, -0.4, 0.9, -2.641593, 2.441593, 2.541593)$.
This is the wrist flip of $\theta^*$, another of the 8 solutions in the table of the Paden-Kahan page.
The raw angles before wrapping are as large as 524 rad, so wrap the output into the joint range.
- From $\theta = 0$ the arm is stretched out and $\det J_b = 0$, so the loop returns FAILURE at L7 after one evaluation.

**A target out of reach.** For the 2R arm and the target $(2.5, 0)$ m, which is farther than the reach of 2 m, the error never goes below 0.4 m and the loop returns FAILURE at L9.

## Correctness

**What a returned $\theta$ means.** The loop returns $\theta$ only at L4, where $|\mathcal V_b|$ is within the tolerances.
Since $\exp(\log X) = X$, the pose $T(\theta)e^{[\mathcal V_b]} = T_d$ is reached by a twist of size at most the tolerance from $T(\theta)$.

**Local quadratic convergence.** Let $\theta^*$ be a solution with $J_b(\theta^*)$ invertible, and let $g(\theta) = \log(T(\theta)^{-1}T_d)$.
Then $g(\theta^*) = 0$, and near $\theta^*$ the derivative of $g$ is $Dg(\theta) = -A(g(\theta))J_b(\theta)$, where $A$ is a smooth $6 \times 6$ matrix function with $A(0) = I$.
So the step of L6 differs from the exact Newton step for $g = 0$ by a matrix that is $I + O(|g(\theta)|)$.
The proof page shows that there are $r > 0$ and $K$ with $|\theta^{k+1} - \theta^*| \le K|\theta^k - \theta^*|^2$ for every $\theta^k$ within $r$ of $\theta^*$.
So the errors go to zero quadratically when $K|\theta^0 - \theta^*| < 1$.
For the position task, $g(\theta) = x_d - x(\theta)$ and $Dg = -J$ exactly, and this is the plain [Newton method for systems](/newton-method-for-systems/).

**What is not claimed.** There is no guarantee from a far start: the iteration can cycle, diverge, stop at a singular $J_b$, or converge to a solution other than the nearest one.
If the target is out of reach, there is no solution and the loop cannot succeed.
The radius $r$ depends on the arm, the target and the bound on $|J_b^{-1}|$, and it shrinks to zero as $\theta^*$ approaches a singularity.

## Complexity

One iteration computes $T(\theta)$ with $n$ matrix exponentials and products, $J_b$ with $n$ adjoint maps, one SE(3) logarithm, and one linear solve.
The first three cost $\Theta(n)$ in the [real RAM](/real-ram/), and the solve costs $\Theta(n^3)$ for an $n \times n$ system, so $k$ iterations cost $\Theta(kn^3)$, and $\Theta(k)$ for a fixed arm.
The extra space is the Jacobian, $\Theta(n^2)$.
The number of iterations $k$ is not bounded in general.
Near a regular solution, quadratic convergence means that the number of iterations from a close start grows like $\log\log(1/\varepsilon)$, which is why the examples above end in 4 or 5 steps once the error is small.
The step counts in the examples are measured, not bounds.

## Properties

- **One solution.** The method returns at most one solution, the one in whose basin of attraction the guess lies.
- **Local.** Convergence is local and quadratic near a regular solution, with no global guarantee.
- **No tuning.** Apart from the tolerances and the step limit, there is no step size, gain or damping to choose.
- **Frame of the error.** The error and the Jacobian are both in the end effector frame; the space form with $\mathcal V_s = \mathrm{Ad}_{T}\mathcal V_b$ and $J_s$ gives the same steps.
- **Singularities.** At a singular $J_b$ the step is not defined, and near one the steps are very large.

## Variants and improvements

- **Redundant arms.** With more joints than task coordinates, replace the solve with the pseudoinverse step $\Delta\theta = J_b^{+}\mathcal V_b$, the [Jacobian pseudoinverse method](/jacobian-pseudoinverse-method/).
- **Damping.** [Damped least squares](/damped-least-squares-inverse-kinematics/) solves $(J^{\mathsf T}J + \lambda^2I)\Delta\theta = J^{\mathsf T}e$ and stays defined at singularities, at the cost of slower convergence; with $\lambda$ chosen per step it is the [Levenberg-Marquardt](/levenberg-marquardt/) method.
- **Steepest descent.** The [Jacobian transpose method](/jacobian-transpose-method/) uses $\Delta\theta = \alpha J^{\mathsf T}e$, which needs no solve but converges linearly.
- **Line search.** Scaling the step by $\alpha \in (0, 1]$ so that $|\mathcal V_b|$ decreases makes the iteration more robust from a far start.
- **Restarts.** Running the iteration from many random guesses finds several solutions, but with no guarantee of finding all of them.
- **Joint limits.** Clamping or projecting $\theta$ after each step keeps the joints in range, but it can stop the convergence.

## When to use it

Use Newton-Raphson inverse kinematics when the arm has no closed form solution, a good guess is known, and the solution is regular, for example to refine an analytic solution, or to track a target that moves a little between calls, starting from the last solution.
When the arm has a closed form, such as an arm with a spherical wrist, use [kinematic decoupling](/kinematic-decoupling/) or the [Paden-Kahan subproblems](/paden-kahan-subproblems/), which return all solutions.
When the arm may pass near a singularity, use damped least squares.

## Pitfalls

- **The error.** The error must be $\log(T^{-1}T_d)$, or an equivalent twist, not the difference $T_d - T$ of the matrices, which has 12 entries and does not match the 6 columns of $J$.
- **The frames.** The body twist goes with the body Jacobian, and the space twist with the space Jacobian; a mixed pair gives wrong steps away from the solution.
- **Units.** $\varepsilon_\omega$ is in rad and $\varepsilon_v$ in m, so one tolerance on $|\mathcal V_b|$ mixes units; keep two.
- **Angles that grow.** The output angles can be far outside $(-\pi, \pi]$; wrap them, and then check joint limits.
- **Far starts.** A step from a far guess can be huge and land in another basin; limit the step size or use a line search.
- **The logarithm at $\pi$.** When the rotation error is close to $\pi$, the logarithm is not smooth; a start with such a large rotation error needs care.

## Implementations

## History

Pieper (1968) studied the kinematics of computer controlled arms in his Stanford thesis.
Besides the closed form solution for arms with three intersecting axes, he described numerical methods for general arms, among them Newton-Raphson iteration.
Iterative methods with the Jacobian then became the usual tool for arms with no closed form, in the forms of the pseudoinverse, the transpose and damped least squares.
Lynch and Park (2017) give the modern form with the product of exponentials, the body Jacobian and the matrix logarithm of the pose error.

## References
