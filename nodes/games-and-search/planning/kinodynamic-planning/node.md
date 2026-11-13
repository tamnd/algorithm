---
tag: 3676WF
kind: problem
slug: kinodynamic-planning
name: Kinodynamic planning
aliases:
- kinodynamic motion planning
area: games-and-search/planning
level: research
summary: Find controls that move a robot with dynamics, such as velocity and acceleration bounds, from a start state to a goal state without a collision.
prereqs: [motion-planning, configuration-space]
see_also: [rapidly-exploring-random-tree, rrt-star, rrt-star-asymptotic-optimality, piano-movers-problem, euclidean-shortest-path, bvp-boundary-value-problem, shooting-method, a-star-search]
sources:
  - paper: doi:10.1145/174147.174150
    title: Bruce Donald, Patrick Xavier, John Canny and John Reif, Kinodynamic motion planning, Journal of the ACM 40(5), 1993
    locator: pages 1048 to 1066 (the problem for a point mass with velocity and acceleration bounds among polyhedra in two or three dimensions, with a safety margin; the first provably good approximation algorithm, in polynomial time)
  - paper: "John Canny, Bruce Donald, John Reif and Patrick Xavier, On the complexity of kinodynamic planning, 29th Annual Symposium on Foundations of Computer Science (FOCS), 1988, 306-316"
    locator: the conference version of the Journal of the ACM paper, and the claim that the time-optimal problem in three dimensions is NP-hard
  - paper: doi:10.1007/BF01586636
    title: Bruce R. Donald and Patrick G. Xavier, Provably good approximation algorithms for optimal kinodynamic planning, robots with decoupled dynamics bounds, Algorithmica 14(6), 1995
    locator: pages 443 to 479 (the exponent of 1/ε lowered from 6d to 3d, a trajectory as fast as the optimum with an ε loss in the safety margin, and Appendix A, a sketch of the NP-hardness in three dimensions after Canny and Reif)
  - paper: doi:10.1177/02783640122067453
    title: Steven M. LaValle and James J. Kuffner, Randomized kinodynamic planning, International Journal of Robotics Research 20(5), 2001
    locator: pages 378 to 400 (the RRT in the state space, with a step made by applying a control for a short time)
  - paper: doi:10.1109/LRA.2018.2888947
    title: Michal Kleinbort, Kiril Solovey, Zakary Littlefield, Kostas E. Bekris and Dan Halperin, Probabilistic completeness of RRT for geometric and kinodynamic planning with forward propagation, IEEE Robotics and Automation Letters 4(2), 2019
    locator: Theorem 2 (probabilistic completeness of the kinodynamic RRT with random controls and durations, under Lipschitz conditions); arXiv:1809.07051v2 (2022) corrects Lemma 3 and the proof of Theorem 2
  - paper: doi:10.1109/ICRA.2013.6631299
    title: Dustin J. Webb and Jur van den Berg, Kinodynamic RRT*, asymptotically optimal motion planning for robots with linear dynamics, IEEE International Conference on Robotics and Automation (ICRA), 2013
    locator: an exact, optimal connection between two states for linear dynamics, with a cost that trades the duration against the control effort, and closed forms when the dynamics matrix is nilpotent
  - paper: doi:10.1177/0278364915614386
    title: Yanbo Li, Zakary Littlefield and Kostas E. Bekris, Asymptotically optimal sampling-based kinodynamic planning, International Journal of Robotics Research 35(5), 2016
    locator: pages 528 to 564 (SST and SST*, asymptotically near-optimal and optimal without a solver for the two-point boundary value problem)
  - book: isbn:9780521862059
    title: Steven M. LaValle, Planning Algorithms, Cambridge University Press, 2006
    locator: Chapter 13 (differential models) and Chapter 14 (sampling-based planning under differential constraints) (general locator)
---

Kinodynamic planning asks for a motion of a robot that avoids the obstacles and also obeys the laws of its dynamics, such as bounds on velocity, acceleration or force. The unknown is not a path in the [configuration space](/configuration-space/) but a control signal, and the motion is the solution of a differential equation $\dot{x} = f(x, u)$ in the *state space*, which holds the velocities as well as the configuration. Canny, Donald, Reif and Xavier posed it in this form in 1988, for a point mass with velocity and acceleration bounds among polyhedra, and gave the first provably good approximation algorithm. The time-optimal version in three dimensions is NP-hard, and the general problem contains geometric [motion planning](/motion-planning/), so it is PSPACE-hard when the number of degrees of freedom grows.

## In plain words

Plain motion planning asks for a route that misses the walls. A real car cannot follow every such route. It cannot turn in place, it cannot stop at once, and it cannot go sideways. A drone cannot change its speed in an instant.

Kinodynamic planning asks for a route that the machine can really drive. You do not choose the route directly. You choose how to push the pedals and turn the wheel over time, and the laws of motion give the route.

So the state of the robot is not only where it is, but also how fast it moves. Two robots at the same place can have very different futures. One that moves fast toward a wall may already be unable to stop, even if it has not hit the wall yet.

## Definition

**The model.** A *state* $x$ lies in a state space $\mathcal{X}$. For a robot with configuration $q \in \mathcal{C}$ and second-order dynamics, $x = (q, \dot{q})$, so $\dim \mathcal{X} = 2 \dim \mathcal{C}$. A *control* $u(t)$ takes values in a set $U$, such as a box of accelerations or torques. The motion obeys

$$\dot{x}(t) = f(x(t), u(t)).$$

The free state set $\mathcal{X}_{free}$ holds the states whose configuration is free of collision and whose velocity obeys its bounds.

**Input.** The dynamics $f$, the control set $U$, the obstacles that define $\mathcal{X}_{free}$, a start state $x_{init}$ and a goal set $\mathcal{X}_{goal}$.

**Output.** A time $T \ge 0$ and a control $u : [0, T] \to U$, usually piecewise constant, such that the solution $x(t)$ of the dynamics with $x(0) = x_{init}$ stays in $\mathcal{X}_{free}$ for all $t \in [0, T]$ and ends with $x(T) \in \mathcal{X}_{goal}$. Or a report that none exists.

**The optimal version.** Minimize a cost, often the time $T$, or the control effort $\int_0^T \lVert u(t) \rVert^2 \, dt$, or a weighted sum of the two. Donald, Xavier, Canny and Reif minimize the time and ask the trajectory to keep a safety margin from the obstacles that grows with the speed.

**How it differs from motion planning.** In geometric [motion planning](/motion-planning/) any free path is a solution, and a robot can follow it at any speed and in either direction. Here three things change. A path in $\mathcal{C}$ is a solution only if some control makes the robot follow it in time. The dynamics usually have drift, so a motion from $a$ to $b$ does not give one from $b$ to $a$, and a tree grown from the goal backward needs the dynamics run backward. And there are *states of inevitable collision*: free states from which every control leads to a collision.

**The steering problem.** A planner often needs a local step from a state $x_1$ to a state $x_2$. This is a two-point [boundary value problem](/bvp-boundary-value-problem/) for $\dot{x} = f(x, u)$, which has a closed form only for special systems. In general it needs a numerical method such as the [shooting method](/shooting-method/), or the planner avoids it and only runs the dynamics forward from $x_1$.

## Variants

| variant | dynamics | status |
|---|---|---|
| point mass, bounded velocity and acceleration (the original setting) | $\ddot{q} = u$ in $\mathbb{R}^2$ or $\mathbb{R}^3$, $L_\infty$ bounds | approximation in polynomial time (Donald, Xavier, Canny and Reif); time-optimal in 3D is NP-hard |
| one dimension | point mass on a line | exact algorithm (Ó'Dúnlaing, cited by Donald and Xavier) |
| plane, exact | point mass in $\mathbb{R}^2$ | exact algorithm in exponential time and polynomial space (Canny, Rege and Reif, cited by Donald and Xavier) |
| Cartesian robots and open-chain manipulators | decoupled or coupled dynamics bounds | approximation algorithms (Donald and Xavier, 1995) |
| linear systems | $\dot{x} = A x + B u$ | exact optimal steering, used by kinodynamic RRT\* (Webb and van den Berg) |
| nonholonomic robots | car with a turning radius, rolling contact | first-order constraints on $\dot{q}$ that cannot be integrated into constraints on $q$ |
| general systems | $\dot{x} = f(x, u)$ with a simulator for $f$ | sampling methods with forward propagation |

The *nonholonomic* case is a special case where the constraint is on the velocity only, such as a car that cannot move sideways. It can still be studied in $\mathcal{C}$ itself, since the state has no velocity part.

## Examples

**Minimum time on a line.** A point mass starts at rest at $0$ and must stop at rest at $D = 1$, with $|\ddot{q}| \le A = 1$ and $|\dot{q}| \le V$. The fastest control is to accelerate at full force, coast at speed $V$ if the bound is reached, and brake at full force. The time is $2 \sqrt{D/A}$ if $D \le V^2/A$, and $D/V + V/A$ otherwise. A simulation of this control with a time step of $10^{-5}$ gives the same times and stops at $1.0$.

| $V$ | minimum time | the speed bound is reached |
|---|---|---|
| 0.25 | 4.25 | yes |
| 0.5 | 2.5 | yes |
| 1 | 2.0 | just at the middle |
| no bound | 2.0 | no |

The geometric path is the same segment in every row. Only the dynamics change the answer. This is why a shortest path in $\mathcal{C}$ need not be a fastest motion.

**States of inevitable collision.** A point mass moves at speed $v$ toward a wall, with braking $|\ddot{q}| \le 1$. It needs a distance $v^2/2$ to stop: $0.5$ for $v = 1$, $2$ for $v = 2$ and $4.5$ for $v = 3$. So at a distance of 2 from the wall, the state with $v = 1$ is safe and the state with $v = 3$ is free but doomed. A planner in $\mathcal{C}$ cannot tell these two states apart.

**A steering function.** For the double integrator $\ddot{q} = u$ on a line, the control that moves from rest at $0$ to rest at $D$ in time $T$ with the least effort $\int_0^T u^2 \, dt$ is $u(t) = 6D/T^2 - 12 D t/T^3$, with effort $12 D^2 / T^3$. A numeric integration with $2 \times 10^5$ steps for $D = 1$ ends at position $1.0$ and velocity $0.0$ and gives the efforts below. The bang-bang control $u = 4$ then $u = -4$ also connects the two states in time 1, with effort $16.0$, more than $12.0$.

| $T$ | effort | peak control |
|---|---|---|
| 0.5 | 96.0 | 24.0 |
| 1 | 12.0 | 6.0 |
| 2 | 1.5 | 1.5 |

The effort falls fast with $T$. A cost that trades the time against the effort, as in kinodynamic RRT\*, picks a $T$ between these extremes. For linear systems such controls have closed forms. For a car or an arm they do not, which is the main practical difficulty.

## Known algorithms

| method | promise | notes | page |
|---|---|---|---|
| search on a grid of short constant-control motions | trajectory close to time-optimal, time polynomial in $1/\varepsilon$ and in the obstacle complexity, for a fixed dimension | Donald, Xavier, Canny and Reif; Donald and Xavier lowered the exponent of $1/\varepsilon$ from $6d$ to $3d$ | |
| kinodynamic RRT | probabilistically complete with random controls and durations, under Lipschitz conditions | steps by forward propagation, needs no steering function | [RRT](/rapidly-exploring-random-tree/) |
| kinodynamic RRT\* | asymptotically optimal for linear dynamics | needs an exact optimal steering function | [RRT\*](/rrt-star/), [asymptotic optimality](/rrt-star-asymptotic-optimality/) |
| SST, SST\* | asymptotically near-optimal and optimal | forward propagation only, keeps a sparse set of nodes | |
| plan a path, then time it | depends on the first stage | a geometric path is found first and then timed to obey the dynamics, so it can miss solutions | [motion planning](/motion-planning/) |
| trajectory optimization | local | solves a boundary value problem from an initial guess, for example by shooting | [shooting method](/shooting-method/) |

The probabilistic completeness of the kinodynamic RRT has a history of its own. LaValle and Kuffner gave the method and an argument in 2001. Kleinbort, Solovey, Littlefield, Bekris and Halperin gave a proof under weaker assumptions in 2019, and in 2022 corrected an error in their own kinodynamic proof, with the main result unchanged.

## Bounds

- **Lower bound by reduction from geometric planning.** Take $f(x, u) = u$ with $\lVert u \rVert \le 1$ and no other constraint. A free path of finite length can be followed at unit speed, and in the semi-algebraic setting of the exact problem two free configurations that a path joins are also joined by a free path of finite length. So the problem has a solution if and only if the geometric problem has one. So kinodynamic planning is at least as hard as the [piano movers' problem](/piano-movers-problem/), which is PSPACE-hard when the number of degrees of freedom grows (Reif).
- **NP-hardness of the time-optimal problem in three dimensions.** Canny, Donald, Reif and Xavier claimed in 1988 that the time-optimal problem for a point mass in $\mathbb{R}^3$ among polyhedra is [NP-hard](/np-hard/). Donald and Xavier sketch the proof in Appendix A of their 1995 paper. It extends the proof of Canny and Reif that the [Euclidean shortest path](/euclidean-shortest-path/) problem in three dimensions is NP-hard, by showing that an acceleration bound large enough to make the two problems agree can be written with a polynomial number of bits. They also show that finding a path in the homotopy class of the optimal one is NP-hard.
- **Upper bound by approximation.** For the point mass, a trajectory $\varepsilon$-close to the optimal time can be found in time polynomial in $1/\varepsilon$ and in the obstacle complexity, for a fixed dimension (Donald, Xavier, Canny and Reif). Donald and Xavier also find a trajectory as fast as the optimum, with the safety margin relaxed by a factor that depends on $\varepsilon$.
- **No worst-case bounds for sampling methods.** The sampling methods give only probabilistic promises, with no bound on the time to a first solution in the worst case.

## Reductions

- **From geometric motion planning**, as in the first bound: any geometric instance is a kinodynamic instance with $\dot{x} = u$.
- **From the Euclidean shortest path in three dimensions** to the time-optimal problem, as in the second bound.
- **To a graph search.** Fix a time step and a finite set of controls, such as the corners of the control box. The states reached from $x_{init}$ by sequences of these controls form a graph, and a search on it, such as [A\* search](/a-star-search/), returns an approximate solution. The algorithm of Donald, Xavier, Canny and Reif is of this type, with a step size chosen from $\varepsilon$.
- **The local step is a boundary value problem.** Connecting two given states is a two-point [boundary value problem](/bvp-boundary-value-problem/). Planners that need it, such as kinodynamic RRT\*, are limited to systems where it can be solved, and planners that avoid it, such as the kinodynamic RRT and SST, only integrate the dynamics forward.

## Applications

- **Cars and mobile robots**, which cannot turn in place and need distance to stop.
- **Aircraft and quadrotors.** In the arXiv version of their paper, Webb and van den Berg run kinodynamic RRT\* on a quadrotor with linearized dynamics in a 10-dimensional state space.
- **Manipulators with torque limits**, where a fast motion must respect the forces the motors can give.
- **Any robot that moves fast compared with its braking distance**, where a geometric path that ignores the speed can lead to a state of inevitable collision.

## References
