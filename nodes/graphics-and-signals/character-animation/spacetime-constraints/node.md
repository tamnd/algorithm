---
tag: 5ZYH4C
kind: technique
slug: spacetime-constraints
name: Spacetime constraints
aliases:
- spacetime optimization
area: graphics-and-signals/character-animation
level: advanced
summary: Find a character motion as the solution of a constrained optimization over the whole trajectory that meets key poses and minimizes muscle effort.
prereqs: [kkt-conditions, newton-method-for-systems]
see_also: [motion-retargeting, style-based-inverse-kinematics, inverse-kinematics, euler-lagrange-equation, quadratic-programming, lagrange-multiplier, footskate-cleanup, motion-warping]
sources:
  - paper: doi:10.1145/378456.378507
    title: "Andrew Witkin and Michael Kass, Spacetime constraints, SIGGRAPH 88, Computer Graphics 22(4), 159-168"
    locator: the formulation of the motion as a constrained optimization over the whole trajectory, with the states and the forces sampled in time, the dynamics as constraints and an effort objective, solved by sequential quadratic programming (general locator)
  - paper: doi:10.1145/280814.280820
    title: "Michael Gleicher, Retargetting motion to new characters, SIGGRAPH 98, 33-42"
    locator: the use of a spacetime formulation without the dynamics, with kinematic constraints over the whole motion (general locator)
---

Spacetime constraints is a way to make a motion by optimization instead of by simulation or by hand.
The unknown is the whole trajectory of the character, at all times at once, together with the forces of its muscles.
The animator gives constraints, such as a pose at the start, a pose at the end and a foot on the floor at a given time.
The laws of motion are also constraints, one for each time sample.
Among all trajectories that meet the constraints, the method picks the one that uses the least effort, usually the integral of the squared muscle forces.
Witkin and Kass (1988) introduced the idea, with a jumping lamp as the main example, and solved the problem by sequential quadratic programming (SQP).
The same frame, often without the dynamics, is the base of [motion retargeting](/motion-retargeting/) and of much later work on motion editing.

## In plain words

A simulation goes forward in time: you give the forces, and you get the motion.
But an animator often knows where the character must be and when, and does not know the forces.
Spacetime constraints turns the question around.
It writes down the position and the force at every time step as unknowns.
It says which conditions must hold: start here, land there, obey Newton's law at every step.
Many motions meet all of these conditions.
So it asks for the one that is the least tiring, the one with the smallest sum of squared forces.
That gives motions that anticipate, follow through and look natural, because a body that saves effort moves that way.
A solver for constrained optimization finds that motion.

## When it applies

- The motion has a fixed duration and known events at known times, such as a take-off and a landing.
- The character has few enough degrees of freedom, or the time is short enough, that the whole trajectory fits in one optimization. The number of unknowns is the number of degrees of freedom times the number of time samples, for the states and again for the forces.
- The constraints and the objective are smooth, so that their derivatives exist and Newton-type methods work.
- A good first guess exists, because the problem is not convex once the dynamics are nonlinear, and the solver finds a local minimum near the guess.

## The template

1. **Discretize the time.** Choose $n + 1$ samples $t_0, \ldots, t_n$ with the step $h$. The unknowns are the states $x_i$ at every sample and the forces or torques $f_i$ at the interior samples.
2. **Write the dynamics as constraints.** Replace the derivatives by finite differences, for example $\ddot x(t_i) \approx (x_{i+1} - 2 x_i + x_{i-1}) / h^2$, and write the equation of motion at each interior sample as one constraint $c_i(x, f) = 0$.
3. **Write the user constraints.** Add the poses, positions and velocities that must hold at given times, such as $x_0 = a$, a zero velocity at the start, and a foot on the floor at a contact time.
4. **Choose the objective.** The usual choice is the effort $R = \int \lVert f \rVert^2 dt \approx h \sum_i \lVert f_i \rVert^2$. Other terms, such as a smoothness term or a distance to a reference motion, are added with weights.
5. **Solve.** Use SQP: at the current guess, linearize the constraints, take a quadratic model of the Lagrangian, and solve one linear KKT system for the step and the new multipliers. Repeat until the step and the constraint values are small.
6. **Edit and solve again.** The animator changes a constraint, and the solver starts from the last solution, which is usually a good guess.

The code in `impl/python` does steps 1 to 5 for a body with one degree of freedom, with the dense KKT solve below.

```pseudo id=main
SPACETIME(n, h, dynamics, boundary, effort)
L1  z ← a first guess of all states and forces            ▷ a straight line and zero forces
L2  repeat
L3      c ← the constraint values at z, J ← their Jacobian
L4      H ← the Hessian of effort + Σ λ_i ∇²c_i
L5      solve [H Jᵀ; J 0] [Δz; λ] = [-∇effort; -c]
L6      z ← z + Δz
L7  until Δz is small
L8  return the states and forces of z
```

When the dynamics are linear and the effort is quadratic, the problem is a [quadratic program](/quadratic-programming/) with equality constraints, and the first step of line L5 is the exact solution.
For nonlinear dynamics, the terms $\lambda_i \nabla^2 c_i$ in line L4 make the step a Newton step on the [KKT conditions](/kkt-conditions/), which converges fast near a regular local minimum.

## Classic examples

**The spacetime toy.**
A unit mass moves from $x(0) = 0$ to $x(1) = 1$, at rest at both ends, and the force is $f = \ddot x$.
The effort is $\int_0^1 \ddot x^2 dt$.
The [Euler-Lagrange equation](/euler-lagrange-equation/) of this functional is $x'''' = 0$, so $x$ is a cubic, and the four end conditions give $x(t) = 3t^2 - 2t^3$.
Then $\ddot x = 6 - 12t$ and the minimum is $\int_0^1 (6 - 12t)^2 dt = 36 \int_0^1 (1 - 2t)^2 dt = 12$.
The force pushes forward in the first half and brakes in the second half, which is the anticipation and follow through of the classic principles of animation, found here by the optimization.

With the velocity conditions written as $(x_1 - x_0)/h = 0$ and $(x_n - x_{n-1})/h = 0$, the discrete minimum is exactly $12 n^2 / ((n - 1)(n - 2))$, which is $16.667$ for $n = 10$, $14.035$ for $n = 20$ and $12.955$ for $n = 40$.
It tends to 12 at the rate $O(h)$, because the one-sided velocity conditions are first order.

| $n$ | discrete minimum | largest error of $x$ against $3t^2 - 2t^3$ |
|---|---|---|
| 10 | 16.667 | 0.0373 |
| 20 | 14.035 | 0.0163 |
| 40 | 12.955 | 0.0076 |

**Gravity.**
Under a constant gravity $g$, the force is $f = \ddot x + g$, and the effort is $\int (\ddot x + g)^2 dt = \int \ddot x^2 dt + 2 g [\dot x]_0^1 + g^2 = \int \ddot x^2 dt + g^2$.
The middle term is zero because the body is at rest at both ends.
So the optimal path is the same cubic, and the minimum is $12 + g^2$.
The discrete problem behaves the same: the path does not change, and the effort grows by exactly $g^2 h (n - 1)$.

**A pendulum.**
For an angle $\theta$ with $\ddot \theta + k \sin \theta = f$, the dynamics are nonlinear.
In the code, a swing from $0$ to $1$ radian in one second with $k = 9.81$ and $n = 20$ converges in 4 SQP steps from a straight line guess, and a swing up from $0$ to $\pi$ in two seconds converges in 9 steps.
These are measurements of this toy, not bounds.

**The jumping lamp.**
The main example of Witkin and Kass is a desk lamp made of a few rigid links with hinge joints, which jumps by pushing with its joints.
The constraints are the start pose, the end pose after the landing, and the contact of the base with the floor before the take-off and after the landing.
The optimal jumps show a crouch before the take-off and a squash at the landing, without the animator asking for them.

## Variations

- **Kinematic spacetime.** Drop the dynamics and keep the kinematic constraints over the whole motion, with an objective that keeps the motion close to a given one. [Motion retargeting](/motion-retargeting/) by Gleicher (1998) works this way, with the change written as a smooth displacement curve.
- **Subsets of time.** Optimizing a long motion at once is slow. Later work, for example the spacetime windows of Cohen (1992), optimizes a part of the time at a time.
- **Other bases.** The trajectory can be written with B-spline control points instead of samples, which reduces the number of unknowns and keeps the motion smooth.
- **Other objectives.** A distance to a reference motion, a smoothness term or the work of the joints can replace or join the effort term. Each changes the motion that the method finds.
- **Inverse kinematics.** [Style-based inverse kinematics](/style-based-inverse-kinematics/) solves one pose at a time under constraints, with a learned objective. It is a pose problem, not a trajectory problem, but it uses the same idea of constraints plus a preference.

## Pitfalls

- **Local minima.** With nonlinear dynamics or contact, the problem has many local minima, and the result depends on the first guess. Start from a plausible motion, or from the solution of an easier problem.
- **Size.** The KKT system has one row per unknown and per constraint. A dense solve, as in the toy code, costs the cube of that size. Use the band or sparse structure: each constraint touches only a few neighboring samples.
- **Contacts and events at fixed times.** The method needs to know when each contact starts and ends. If the times are wrong, the motion is forced into an odd shape. Choose them with care, or add them as unknowns with extra work.
- **Time step.** A coarse step makes the finite differences poor, and the discrete optimum can differ much from the continuous one, as the table of the toy shows for small $n$.
- **Scaling.** States, forces and constraints with very different sizes make the KKT system ill conditioned. Scale the units first.

## Exercises

1. Show that $x(t) = 3t^2 - 2t^3$ meets the four end conditions of the toy, and compute $\int_0^1 \ddot x^2 dt$. *Answer:* $x(0) = 0$, $x(1) = 1$, $\dot x = 6t - 6t^2$ is zero at 0 and 1, and the integral of $(6 - 12t)^2$ is 12.
2. Show that a constant gravity does not change the optimal path of the toy. *Answer:* the effort is $\int \ddot x^2 + 2 g (\dot x(1) - \dot x(0)) + g^2$, and the middle term is zero for every path that meets the end conditions, so the effort differs from the toy by the constant $g^2$.
3. Derive the discrete minimum $12 n^2 / ((n - 1)(n - 2))$. *Answer:* with $s_i = x_{i+1} - 2x_i + x_{i-1}$, the end conditions give $\sum_{i=1}^{n-1} s_i = 0$ and $\sum_{i=1}^{n-1} (n - i) s_i = 1$. The least norm $s$ under these two conditions is linear in $i$, and its squared norm is $1 / \sum_{j=1}^{n-1} (j - n/2)^2 = 12 / (n (n - 1)(n - 2))$. The effort is $h \sum (s_i / h^2)^2 = n^3 \sum s_i^2$.

## References
