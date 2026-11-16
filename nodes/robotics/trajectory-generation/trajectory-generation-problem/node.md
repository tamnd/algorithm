---
tag: R16VFP
kind: problem
slug: trajectory-generation-problem
name: Trajectory generation
aliases:
- trajectory planning
area: robotics/trajectory-generation
level: intro
summary: "Turn a path or a set of waypoints into positions, velocities and accelerations over time that the robot can follow."
prereqs: [time-scaling, configuration-space]
see_also: [time-scaling, trajectory-optimization, time-optimal-path-parameterization, motion-planning, differential-flatness, feedrate-scheduling, cam-follower-motion-laws, kinodynamic-planning]
sources:
  - book: isbn:9781107156302
    title: "Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017"
    locator: "Chapter 9 (trajectory generation), Sections 9.1 to 9.4"
  - book: isbn:9783540856283
    title: "Luigi Biagiotti and Claudio Melchiorri, Trajectory Planning for Automatic Machines and Robots, Springer, 2008"
    locator: "Chapter 2 (polynomial and other elementary trajectories) and Chapter 3, Sections 3.2 and 3.4 (trapezoidal and double S profiles)"
  - book: isbn:9781846286414
    title: "Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009"
    locator: the chapter on trajectory planning (general locator)
---

Trajectory generation is the step between deciding where a robot should go and making its motors go there. A motion planner or a person gives a path, a list of waypoints, or just a target. The motor controllers need much more: a position, a velocity and an acceleration for every joint at every control cycle, typically every millisecond. The trajectory generator fills that gap. It must produce a motion that passes through the given points or along the given path, that is smooth enough for the mechanics, and that stays within the limits of the motors on velocity, acceleration and sometimes jerk. Within those rules it usually tries to be as fast or as smooth as possible. The problem is older than robotics: cam designers and machine tool builders solve the same problem, as in [cam follower motion laws](/cam-follower-motion-laws/) and [feedrate scheduling](/feedrate-scheduling/). It differs from its neighbors as follows. A [time scaling](/time-scaling/) is one kind of answer, the timing along a fixed path. [Trajectory optimization](/trajectory-optimization/) is the more general problem that also chooses the path and uses a model of the dynamics.

## In plain words

A plan for a robot arm often says only "go from here, through there, to over there". The motors cannot use that. They need to know, a thousand times a second, exactly where each joint should be and how fast it should be turning. Trajectory generation turns the plan into that stream of numbers. The motion must be possible: no motor can go faster than its top speed or speed up faster than its strength allows. It should also be gentle, because sudden changes in force shake the arm. And it should not waste time. Different methods trade these goals in different ways, from a single formula for a simple move to an optimization for a drone flying through many points.

## Definition

**Input.**

- A geometric description of the motion, one of: a start and a goal configuration; waypoints $q_0, \dots, q_m$ in the [configuration space](/configuration-space/), with or without times; or a path $\theta(s)$, $s \in [0, 1]$.
- Boundary states: velocities and accelerations at the start and the end, often zero (rest to rest).
- Limits on each joint, such as $|\dot q_i| \le V_i$, $|\ddot q_i| \le A_i$ and $|\dddot q_i| \le J_i$, or limits on joint torques through a dynamic model.
- A criterion: the duration $T$ is given, or $T$ is to be minimized, or a smoothness cost such as $\int \|\dddot q\|^2 dt$ is to be minimized.

**Output.** A trajectory $q : [0, T] \to \mathcal C$ that meets the boundary states, passes through the waypoints or along the path, has continuous derivatives up to a required order $k$ (usually $k = 1$ or $2$), satisfies the limits, and is optimal or good for the criterion.

**Single-letter quantities used on this page.** $D$ is the distance of a one-axis move, $V$, $A$ and $J$ are its limits on velocity, acceleration and jerk, $T$ is the duration, $m$ is the number of segments between waypoints, and $n$ is the number of joints.

## Variants

- **Point to point.** One axis or several joints move from one configuration to another, usually from rest to rest. The joints must arrive together.
- **Via points.** The trajectory passes through waypoints (interpolation) or near them (approximation), with or without given passing times.
- **Along a fixed path.** The geometry is fixed and only the [time scaling](/time-scaling/) $s(t)$ is sought. The time-optimal version under joint torque limits is [time-optimal path parameterization](/time-optimal-path-parameterization/).
- **Online.** The trajectory must be recomputed every control cycle from the current state, because the target can change: [online trajectory generation](/online-trajectory-generation/).
- **Joint space or task space.** The trajectory is planned for the joint angles, or for the end-effector pose and then mapped through inverse kinematics.
- **With moving obstacles.** The timing must avoid obstacles that move along the path: [path-velocity decomposition](/path-velocity-decomposition/).
- **Learned.** The shape comes from a demonstration and must be adapted to new goals: [dynamic movement primitives](/dynamic-movement-primitives/).

## Examples

**One axis, four profiles.** Move one joint $D = 1$ rad from rest to rest with $V = 1$ rad/s and $A = 2$ rad/s². The smallest duration that respects both limits depends on the shape of the profile:

| profile | smallest $T$ (s) | binding limit | jerk |
|---|---|---|---|
| [trapezoid](/trapezoidal-velocity-profile/) | 1.5 | both | unbounded at 4 instants |
| [double S](/double-s-velocity-profile/), $J = 8$ | 1.75 | all three | at most 8 |
| [cubic](/cubic-polynomial-trajectory/) | $\sqrt 3 \approx 1.732$ | acceleration | unbounded at the ends |
| [quintic](/quintic-polynomial-trajectory/) | 1.875 | velocity | about 9.1 at the ends |
| degree 7, [minimum snap](/minimum-snap-trajectory/) shape | 2.1875 | velocity | 0 at the ends |

The trapezoid is the fastest possible (a theorem). The polynomials each reach a limit at only one instant, so they are slower, but they are smoother. The numbers follow from the peak values on the linked pages: for example the cubic needs $1.5/T \le 1$ and $6/T^2 \le 2$.

**Waypoints for a drone.** A quadrotor must fly through waypoints $0, 1, 0$ at times $0, 1, 2$ s along one axis without stopping. A minimum-snap trajectory passes the middle waypoint with zero velocity and an acceleration of $-8.4$; its snap cost is about six times smaller than stopping at the waypoint. See [minimum-snap trajectory](/minimum-snap-trajectory/).

**After a sampling planner.** A [rapidly-exploring random tree](/rapidly-exploring-random-tree/) returns a jagged path. [Random shortcut path smoothing](/random-shortcut-path-smoothing/) shortens it, and a time scaling with blends turns it into a trajectory.

## Known algorithms

- **Closed forms for one axis:** [cubic](/cubic-polynomial-trajectory/) and [quintic](/quintic-polynomial-trajectory/) polynomials for a given duration; [trapezoidal](/trapezoidal-velocity-profile/) and [double-S](/double-s-velocity-profile/) profiles for minimum time under limits. All take constant time per axis.
- **Smoothness optimal:** the [minimum-jerk trajectory](/minimum-jerk-trajectory/) in closed form; the [minimum-snap trajectory](/minimum-snap-trajectory/) through waypoints by a linear system or a [quadratic program](/quadratic-programming/).
- **Online:** [online trajectory generation](/online-trajectory-generation/), time-optimal from any state in constant time per axis.
- **Time-optimal along a path:** [time-optimal path parameterization](/time-optimal-path-parameterization/), with the [Bobrow algorithm](/bobrow-time-optimal-algorithm/), [reachability analysis](/topp-reachability-analysis/) and the [convex formulation](/convex-time-optimal-path-parameterization/).
- **Learned:** [dynamic movement primitives](/dynamic-movement-primitives/).
- **Path post-processing:** [random shortcut path smoothing](/random-shortcut-path-smoothing/).
- **General optimization:** [trajectory optimization](/trajectory-optimization/), with methods such as [CHOMP](/chomp/), [STOMP](/stomp/) and [sequential convex optimization](/sequential-convex-trajectory-optimization/).

## Bounds

- **Time, one axis, rest to rest.** Under $|\dot q| \le V$ and $|\ddot q| \le A$, every motion over the distance $D$ takes at least $D/V + V/A$ if $D \ge V^2/A$, and at least $2\sqrt{D/A}$ otherwise, and the trapezoid attains it (theorem, on the [trapezoid page](/trapezoidal-velocity-profile/)).
- **Smoothness, one axis, rest to rest in time $T$.** With the end derivatives fixed to zero up to order $k - 1$, the least value of $\int_0^T (q^{(k)})^2 dt$ is $12 D^2/T^3$ for $k = 2$, $720 D^2/T^5$ for $k = 3$ and $100800 D^2/T^7$ for $k = 4$ (theorems, on the pages of the cubic, the minimum-jerk and the minimum-snap trajectories).
- **Computation.** The closed forms take $\Theta(1)$ time per axis and per segment, so $\Theta(nm)$ in all. Minimum snap with equality constraints is one linear system of size $\Theta(m)$.

## Reductions

- **Fixed path to one dimension.** Along a fixed path $\theta(s)$, the joint limits become limits on $(s, \dot s, \ddot s)$, and the problem becomes the choice of one function $s(t)$, a [time scaling](/time-scaling/).
- **Straight line in joint space to one axis.** For $\theta(s) = \theta_0 + s\Delta$ with box limits on each joint, the limits on $s$ are $\dot s \le \min_i V_i/|\Delta_i|$ and $|\ddot s| \le \min_i A_i/|\Delta_i|$, and a single trapezoid for $s$ solves the synchronized problem.
- **Equality-constrained minimum snap to a linear system.** The [KKT conditions](/kkt-conditions/) of the quadratic cost with linear constraints are one nonsingular linear system.
- **Flat systems to kinematics.** For [differentially flat](/differential-flatness/) systems such as quadrotors, a smooth trajectory of the flat outputs determines the inputs, so trajectory generation for the outputs solves the dynamic problem, as long as the input limits hold.
- **Moving obstacles to a plane.** With the path fixed, moving obstacles become forbidden regions in the plane of path position and time ([path-velocity decomposition](/path-velocity-decomposition/)).

## Applications

Industrial robot controllers generate joint trajectories for every point-to-point and linear move. CNC machines schedule the feed along tool paths. Quadrotors fly minimum-snap trajectories through waypoints. Collaborative robots replan online when a person comes close. Humanoids and animation systems use minimum-jerk and learned trajectories for human-like motion. Cam and linkage design uses the same motion laws for mechanical followers.

## References
