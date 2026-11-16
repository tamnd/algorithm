---
tag: ZEP6AG
kind: problem
slug: trajectory-optimization
name: Trajectory optimization
aliases:
- optimal trajectory planning
area: robotics/trajectory-generation
level: core
summary: "Find a state and control trajectory that minimizes a cost subject to the dynamics, limits, contacts and obstacles."
prereqs: [optimal-control-problem, trajectory-generation-problem]
see_also: [chomp, stomp, sequential-convex-trajectory-optimization, control-limited-ddp, contact-implicit-trajectory-optimization, lqr-problem, nonlinear-mpc, motion-planning]
sources:
  - paper: doi:10.2514/2.4231
    title: "John T. Betts, Survey of numerical methods for trajectory optimization, Journal of Guidance, Control, and Dynamics 21(2), 1998, 193-207"
    locator: "the whole paper (direct and indirect methods, transcription to a nonlinear program)"
  - book: isbn:9781107156302
    title: "Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017"
    locator: "Section 10.7 (motion planning by nonlinear optimization)"
  - paper: doi:10.1177/0278364913488805
    title: "Matt Zucker, Nathan Ratliff, Anca D. Dragan, Mihail Pivtoraiko, Matthew Klingensmith, Christopher M. Dellin, J. Andrew Bagnell and Siddhartha S. Srinivasa, CHOMP: Covariant Hamiltonian optimization for motion planning, The International Journal of Robotics Research 32(9-10), 2013, 1164-1193"
    locator: "the whole paper (trajectory optimization as a motion planner, and its local minima)"
  - paper: doi:10.1177/0278364914528132
    title: "John Schulman, Yan Duan, Jonathan Ho, Alex Lee, Ibrahim Awwal, Henry Bradlow, Jia Pan, Sachin Patil, Ken Goldberg and Pieter Abbeel, Motion planning with sequential convex optimization and convex collision checking, The International Journal of Robotics Research 33(9), 2014, 1251-1270"
    locator: "the whole paper (the nonconvex problem and a local method for it)"
---

Trajectory optimization chooses how a system should move over time so that a cost is as small as possible. The system can be a robot arm, a car, an aircraft or a walking robot. Its motion obeys equations of motion, its controls such as motor torques have limits, and it must avoid obstacles or make and break contact with the ground. The cost measures what we want to save: time, energy, effort, or the roughness of the motion. The answer is a full trajectory: the state at every time and the control that produces it. Unlike the [trajectory generation problem](/trajectory-generation-problem/) for a given path, trajectory optimization chooses the path and the timing together, and it uses a model of the dynamics. It is the [optimal control problem](/optimal-control-problem/) in the form robotics meets it: finite horizon, nonlinear dynamics, many constraints, and an answer needed as numbers on a time grid. Obstacles and nonlinear dynamics make the problem nonconvex, so the practical methods are local: they start from an initial guess and improve it until no small change helps. They can stop in a poor local minimum, and the result depends on the guess.

## In plain words

Imagine planning how to throw a ball into a basket, or how to swing a robot arm around a table to a shelf. There are endless ways to do it. Some are fast, some use little force, some hit the table. We write down a score for each motion, such as the total effort plus a big penalty for touching the table, and search for the motion with the best score that the arm can really do. The search usually starts with a rough guess, such as a straight move that goes through the table, and bends it step by step into a better one. This works well, but it finds the best motion near the guess, not always the best motion of all.

## Definition

**Input.**

- Dynamics $\dot x = f(x, u)$, or in discrete time $x_{k+1} = f(x_k, u_k)$, for states $x \in \mathbb R^n$ and controls $u \in \mathbb R^p$. Kinematic problems use $\dot x = u$, so the control is the velocity.
- A horizon $T$, fixed or free, or a number of steps $N$.
- Boundary conditions: the initial state $x(0) = x_0$, and a goal state or goal set.
- Path constraints $g(x(t), u(t)) \le 0$: joint and torque limits, obstacle distances, contact conditions.
- A cost $J = \phi(x(T)) + \int_0^T \ell(x(t), u(t))\, dt$, or its sum over steps.

**Output.** A pair $(x(\cdot), u(\cdot))$ that meets the dynamics, the boundary conditions and the path constraints, and minimizes $J$. Because the problem is nonconvex in general, the methods return a local minimum or a stationary point, and some return only a feasible trajectory that is better than the guess.

**Single-letter quantities used on this page.** $n$ is the state dimension, $p$ the control dimension, $N$ the number of time steps, and $d$ the dimension of the configuration space.

## Variants

- **Kinematic, with obstacles.** The variables are configurations $q_0, \dots, q_N$ with fixed ends. The cost is a smoothness term, such as the sum of $\|q_{k+1} - q_k\|^2$, plus a term that penalizes closeness to obstacles. [CHOMP](/chomp/), [STOMP](/stomp/), [sequential convex optimization](/sequential-convex-trajectory-optimization/), [GPMP2](/gaussian-process-motion-planning/) and [elastic bands](/elastic-bands/) solve this form.
- **Dynamic, with control limits.** Nonlinear dynamics and box limits on the controls, with a smooth cost. [Control-limited DDP](/control-limited-ddp/) solves it by a backward pass of quadratic models and a forward rollout.
- **Through contact.** The trajectory may make and break contact, and the contact forces are variables with complementarity conditions; see [contact-implicit trajectory optimization](/contact-implicit-trajectory-optimization/).
- **Fixed path, free timing.** With the geometry fixed, the problem reduces to [time-optimal path parameterization](/time-optimal-path-parameterization/), which is convex after a change of variables.
- **Linear and quadratic.** Linear dynamics, a quadratic cost and no inequality constraints give the [LQR problem](/lqr-problem/), solved exactly by a Riccati recursion.
- **Receding horizon.** Solve a short problem from the current state at every control cycle and apply the first control: [nonlinear model predictive control](/nonlinear-mpc/), often with one iteration per cycle as in the [real-time iteration](/real-time-iteration/).
- **Direct and indirect.** Direct methods discretize the trajectory and solve the resulting finite nonlinear program; indirect methods solve the necessary conditions of the [Pontryagin maximum principle](/pontryagin-maximum-principle/) as a boundary value problem ([indirect method](/indirect-method-optimal-control/)). Betts (1998) surveys both.

## Examples

**A point around a disc.** A point moves in the plane from $(-1, 0)$ to $(1, 0)$ and must stay outside the disc of radius $r = 1/2$ at the origin; the cost is the length. The straight line crosses the disc. There are two optimal paths, one above and one below the disc, each made of two tangent segments of length $\sqrt{1 - r^2}$ and an arc of angle $\pi - 2\arccos r$, for a total length

$$2\sqrt{1 - r^2} + r(\pi - 2\arccos r) \approx 1.7321 + 0.5236 = 2.2557.$$

The feasible set is not convex: the two optimal paths are feasible, but their average, the straight line, is not. A local method started from the straight line sees a cost gradient that is symmetric about the axis and can stay on it; a small push to one side decides which of the two optima it finds. This is the typical behavior of the obstacle variants.

**A scalar linear system.** For $x_{k+1} = x_k + u_k$ with the cost $\sum_k (x_k^2 + u_k^2)$ over an infinite horizon, the Riccati equation gives $P^2 - P - 1 = 0$, so $P = (1 + \sqrt 5)/2 \approx 1.618$, and the optimal control is $u_k = -0.618\, x_k$. Here the problem is convex and the answer is global and in closed form.

**One axis, minimum time.** Moving one joint over $D = 1$ with $|\dot q| \le 1$ and $|\ddot q| \le 2$ in the least time gives the [trapezoidal velocity profile](/trapezoidal-velocity-profile/) with $T = 1.5$. As a trajectory optimization problem the control is $\ddot q$, the cost is $T$, and the answer is [bang-bang](/bang-bang-control/) with a cruise phase.

## Known algorithms

- **Smoothness plus obstacle cost, gradient based:** [CHOMP](/chomp/), a covariant gradient method that uses the smoothness metric. [Elastic bands](/elastic-bands/), which deform a path by internal and external forces and keep collision-free bubbles around it.
- **Sampling based, gradient free:** [STOMP](/stomp/), which samples noisy trajectories and averages them by their costs. The [cross-entropy method](/cross-entropy-method/) is a related general optimizer.
- **Sequential convex programming:** [TrajOpt](/sequential-convex-trajectory-optimization/), which convexifies the collision constraints, solves a [quadratic program](/quadratic-programming/) in a box around the current trajectory, and enlarges or shrinks the box.
- **Probabilistic inference:** [GPMP2](/gaussian-process-motion-planning/), which sets a [Gaussian process](/gaussian-process/) prior on trajectories and solves the resulting [factor graph](/factor-graph/) by [Gauss-Newton](/gauss-newton-algorithm/) or [Levenberg-Marquardt](/levenberg-marquardt/) steps.
- **Dynamic programming in the neighborhood of a trajectory:** [control-limited DDP](/control-limited-ddp/), with a box-constrained quadratic program for each step of the backward pass.
- **Through contact:** [contact-implicit trajectory optimization](/contact-implicit-trajectory-optimization/), which keeps contact forces and complementarity conditions as constraints of one nonlinear program.
- **Convex special cases:** the [LQR problem](/lqr-problem/) by the Riccati recursion; [time-optimal path parameterization](/time-optimal-path-parameterization/) by the [convex formulation](/convex-time-optimal-path-parameterization/).
- **General constrained optimization:** [penalty](/penalty-method/) and [augmented Lagrangian](/augmented-lagrangian-method/) methods applied to the transcribed problem.

## Bounds

- **No global guarantee in general.** Deciding whether any collision-free path exists for a robot with many degrees of freedom among obstacles is PSPACE-hard in the generalized form of the [piano movers' problem](/piano-movers-problem/). A method that always found a global optimum would also decide this question, so the practical methods aim at local minima.
- **Convergence of the local methods.** The methods on the pages of this group come with local results of different strengths: a decrease of the cost at each step, convergence to a stationary point under assumptions, or no guarantee at all. Each page states the result separately from its cost per iteration.
- **Cost per iteration.** The trajectory structure makes the linear algebra banded. A Newton or Gauss-Newton step on $N$ steps with $n$ states costs $O(N n^3)$ by a block tridiagonal or Riccati solve, instead of $O(N^3 n^3)$ for a dense solve. CHOMP with a finite-difference smoothness metric solves a banded system in $O(N d)$ per iteration.

## Reductions

- **To a finite nonlinear program.** Discretizing the states and controls on a time grid, and imposing the dynamics as equality constraints between neighboring steps, turns the problem into a nonlinear program with a sparse, banded structure. This is direct transcription in Betts (1998).
- **To LQR locally.** A second-order model of the cost and a first-order model of the dynamics in the neighborhood of a trajectory give an [LQR problem](/lqr-problem/) for the correction. DDP and its relatives solve one such problem per iteration.
- **From motion planning.** A [motion planning](/motion-planning/) algorithm such as a [rapidly-exploring random tree](/rapidly-exploring-random-tree/) gives a feasible but rough path; trajectory optimization then smooths and shortens it. This combination covers the weakness of each: the planner explores globally, the optimizer refines locally.
- **Fixed path to a convex program.** For a fixed path, the change of variables $b = \dot s^2$ makes the time-optimal problem convex ([convex formulation](/convex-time-optimal-path-parameterization/)).

## Applications

Robot arms use trajectory optimization to plan smooth collision-free motions in cluttered cells and kitchens. Legged robots and humanoids plan motions through contact, such as walking, jumping and climbing. Aircraft, rockets and spacecraft follow optimal ascent, reentry and transfer trajectories, which is where many of the numerical methods began. Autonomous cars optimize their path and speed in a receding horizon. Animation systems use the same methods to make characters move in a physically plausible way.

## References
