---
tag: P77YSV
kind: algorithm
slug: leader-follower-formation-control
name: Leader-follower formation control
aliases:
- l-phi formation control
area: robotics/multi-robot-systems
level: core
summary: Each follower keeps a set distance and bearing to its leader by feedback linearization of a point ahead of its axle, so the formation is a tree of such pairs.
solves: [formation-control]
model: real-ram
complexity:
  vars: {r: the number of robots, k: the number of integration steps}
  time: {per_step: O(r), total: O(k r)}
  messages: {per_step: O(r)}
  space: {extra: O(r)}
properties: {deterministic: true, randomized: false, online: true}
history:
  year: 2001
  people: [Jaydev P. Desai, James P. Ostrowski, Vijay Kumar]
  note: Desai, Ostrowski and Kumar gave separation-bearing and separation-separation laws for formations of nonholonomic robots, with input-output linearization and an analysis of the internal heading dynamics.
prereqs: [formation-control, unicycle-model, feedback-linearization]
see_also: [distance-based-formation-control, input-output-linearization, zero-dynamics, laplacian-consensus-protocol, multi-robot-system, differential-drive-model, nonholonomic-constraint, exponential-stability]
sources:
  - paper: doi:10.1109/70.976023
    title: Jaydev P. Desai, James P. Ostrowski and Vijay Kumar, Modeling and control of formations of nonholonomic mobile robots, IEEE Transactions on Robotics and Automation 17(6), 2001
    locator: pages 905 to 908 (the separation-bearing and separation-separation controllers, input-output linearization, and the stability of the internal dynamics)
  - paper: doi:10.1016/j.automatica.2014.10.022
    title: Kwang-Kyo Oh, Myoung-Chul Park and Hyo-Sung Ahn, A survey of multi-agent formation control, Automatica 53, 2015
    locator: pages 424 to 440 (leader-follower structures among the formation control methods)
  - book: isbn:9780691140612
    title: Mehran Mesbahi and Magnus Egerstedt, Graph Theoretic Methods in Multiagent Networks, Princeton University Press, 2010
    locator: Chapter 6, Formation Control (formations defined by relative states on a graph)
---

Leader-follower formation control builds a formation of wheeled robots from pairs. One robot, the root, drives freely. Each other robot, a follower, picks one leader and keeps a target separation $l_d$ and bearing $\psi_d$ to it, measured in the frame of the leader. The followers are [unicycles](/unicycle-model/), which cannot move sideways, so the law controls a point at a distance $d > 0$ ahead of the wheel axle. For that point, the map from the inputs $(v, \omega)$ to the rates $(\dot l, \dot\psi)$ is invertible, and [feedback linearization](/feedback-linearization/) makes both errors decay exponentially for any motion of the leader. The heading of the follower is left as an internal state, and behind a leader that drives forward it converges to the heading of the leader. The robots form a tree, so the formation is set by $r - 1$ pairs of targets.

## In plain words

Think of ducklings following their mother. Each duckling does not look at the whole family. It picks one duck ahead of it and tries to stay at a fixed distance and at a fixed angle behind it, for example one step back and a little to the left. The first duck goes where it wants, and the rest of the line follows.

A wheeled robot cannot slide sideways, so it cannot fix both its distance and its angle directly with its own center. Instead it watches a point just in front of its wheels, which it can push in any direction by driving and turning. It steers that point to the right spot next to its leader. The body of the robot then lines up behind, as long as the leader keeps moving forward.

## The problem

**The model.** There are $r$ unicycle robots with states $(x_i, y_i, \theta_i)$ in meters and radians, and inputs $(v_i, \omega_i)$: $\dot x = v \cos\theta$, $\dot y = v \sin\theta$, $\dot\theta = \omega$. The robots form a directed tree: robot 1 is the root, and every other robot $F$ has one leader $L$. A follower controls its point $P_F = (x_F + d \cos\theta_F, y_F + d \sin\theta_F)$, with $d > 0$. It measures the separation $l$ and the bearing $\psi$, defined by

$$P_F - (x_L, y_L) = l\,(\cos(\theta_L + \psi), \sin(\theta_L + \psi)),$$

so $\psi$ is measured from the heading of the leader, and $\psi = \pi$ means straight behind. It also needs the relative heading $\theta_L - \theta_F$, and it receives the inputs $v_L$ and $\omega_L$ of its leader, one message per follower and per step. Time is continuous. The sign conventions of Desai, Ostrowski and Kumar differ in details; the page uses the conventions above, and the proof derives every formula from them.

**Input.** The tree, the targets $(l_d, \psi_d)$ of every follower, the gains $\alpha_1, \alpha_2 > 0$, the offset $d$, the initial states, and the inputs of the root as a function of time.

**Output.** The trajectories, with $l \to l_d$ and $\psi \to \psi_d$ for every follower.

**How it differs from close pages.** In [distance-based formation control](/distance-based-formation-control/) the graph is rigid and undirected, each robot reacts to several neighbors, and convergence is local. Here the graph is a tree, the root is not influenced by anyone, and the errors decay exponentially from any start with $l > 0$, but an error of a leader passes on to all robots below it. The name "l-phi" in the alias refers to this separation-bearing pair; Desai, Ostrowski and Kumar write it with $\psi$.

## The algorithm

```pseudo id=main
LEADER-FOLLOWER(tree, targets, α1, α2, d, states, root inputs, T, h)
L1  for each step of length h until time T do
L2      for each follower F in tree order, with leader L, do
L3          measure l, ψ and γ = θ_L + ψ - θ_F; receive v_L and ω_L
L4          a ← α1 (l_d - l) + v_L cos ψ             ▷ wanted rate of l, plus the motion of the leader
L5          b ← l (α2 (ψ_d - ψ) + ω_L) - v_L sin ψ   ▷ the same for ψ, times l
L6          v_F ← a cos γ - b sin γ
L7          ω_F ← (a sin γ + b cos γ) / d
L8      move every robot with its inputs for time h
L9  return the states
```

Lines L4 to L7 invert the kinematics of the pair. The rates of $l$ and $\psi$ depend on $(v_F, \omega_F)$ through a matrix with determinant $d / l$, and lines L6 and L7 apply its inverse to the wanted rates. "Tree order" in line L2 means that a leader gets its inputs before its followers, so each follower can use the current $v_L$ and $\omega_L$. The angle difference $\psi_d - \psi$ in line L5 is wrapped to $[-\pi, \pi)$. The implementation integrates the closed loop with the classic fourth order Runge-Kutta method and a fixed step.

## Example

**One evaluation by hand.** The leader stands at the origin with $\theta_L = 0$ and drives straight with $v_L = 0.5$ m/s. The follower stands at $(-2, 0.5)$ with $\theta_F = 0$, and $d = 0.1$ m, so $P_F = (-1.9, 0.5)$. The target is $l_d = 1$ m and $\psi_d = 3\pi/4 = 2.3562$, which is behind the leader and to its left, and $\alpha_1 = \alpha_2 = 1$ per second. Then $l = \sqrt{3.86} = 1.9647$, $\psi = \pi - \arctan(0.5 / 1.9) = 2.8843$ and $\gamma = \psi = 2.8843$. Line L4 gives $a = (1 - 1.9647) + 0.5 \cos 2.8843 = -0.9647 - 0.4835 = -1.4482$, and line L5 gives $b = 1.9647 \cdot (2.3562 - 2.8843) - 0.5 \sin 2.8843 = -1.0376 - 0.1273 = -1.1648$. So $v_F = 1.6970$ m/s and $\omega_F = 7.578$ rad/s. The follower drives fast and turns hard to the left, toward its spot.

**The run.** With RK4 and $h = 0.002$ s, $l$ and $\psi$ follow $l_d + (l(0) - l_d) e^{-t}$ and $\psi_d + (\psi(0) - \psi_d) e^{-t}$:

| $t$ (s) | $l$ (m) | $\psi$ (rad) | $\theta_L - \theta_F$ (rad) | follower $(x, y)$ (m) |
|---|---|---|---|---|
| 0 | 1.9647 | 2.8843 | 0 | $(-2, 0.5)$ |
| 0.5 | 1.5851 | 2.6765 | -0.1830 | $(-1.2651, 0.6928)$ |
| 1 | 1.3549 | 2.5505 | -0.0419 | $(-0.7249, 0.7509)$ |
| 2 | 1.1306 | 2.4277 | 0.0359 | $(0.0456, 0.7439)$ |
| 4 | 1.0177 | 2.3659 | 0.0123 | $(1.1735, 0.7138)$ |
| 8 | 1.0003 | 2.3564 | 0.0003 | $(3.1925, 0.7072)$ |

At $t = 16$ s the leader is at $(8, 0)$, the follower at $(7.1929, 0.7071)$, and $P_F - p_L = (-0.7071, 0.7071)$: 1 m away at 135 degrees from the heading of the leader, with the same heading. The heading error first grows, because the follower turns to move its point, and then decays at the rate $v_L / d = 5$ per second of the zero dynamics.

**Zero dynamics.** If the follower starts exactly at its target $l$ and $\psi$ with a heading error $e(0)$, the errors stay zero, and $e = \theta_L - \theta_F$ obeys $\dot e = -(v_L / d) \sin e$, so $\tan(e/2) = \tan(e(0)/2)\, e^{-v_L t / d}$. The tests check this closed form within $10^{-6}$ for $e(0) = 0.5$, $2$ and $-2.8$.

## Correctness

The [proof](proofs/correctness/) derives the rates $\dot l$ and $\dot\psi$ of the pair from the unicycle model, and shows that lines L6 and L7 invert them, because the input matrix has determinant $d / l > 0$. The closed loop is then $\dot l = \alpha_1 (l_d - l)$ and $\dot\psi = \alpha_2 (\psi_d - \psi)$, so both errors decay exponentially for any motion of the leader, and $l$ stays positive. On a tree, the same holds for every edge. The heading of the follower is the internal state. On the set where the outputs are at their targets, behind a leader that drives straight forward, it obeys $\dot e = -(v_L / d) \sin e$ and converges to zero from every $|e(0)| < \pi$. The stability of the internal dynamics from other starts and for turning leaders is the analysis of Desai, Ostrowski and Kumar, and the proof does not repeat it.

## Complexity

- **Per step.** Each follower does $O(1)$ work and receives one message with $(v_L, \omega_L)$, so a step costs $O(r)$ operations in the [real RAM](/real-ram/) model and $r - 1$ messages. The tree is fixed, so there is no other communication.
- **Rate, proved.** The separation and bearing errors decay as $e^{-\alpha_1 t}$ and $e^{-\alpha_2 t}$ for every follower, independent of the depth of the tree.
- **Propagation.** Errors in the targets do not decay down the tree: a follower at depth $k$ is placed by $k$ pairs of targets, so its position error relative to the root is the sum of $k$ terms, and a disturbance of the root reaches every robot. This is a structural property, not a bound in the source.

## Properties

- **Exponential tracking of separation and bearing**, for any motion of the leader, as long as $d > 0$ and $l > 0$.
- **Uses one leader per follower.** The graph is a directed tree, so the sensing load is one neighbor per robot.
- **Needs the inputs of the leader.** The law uses $v_L$ and $\omega_L$; a follower that only sees its leader must estimate them.
- **Internal heading dynamics.** They are stable behind a leader that moves forward, and unstable when the leader moves backward.
- **Deterministic and continuous time.** In a sampled implementation the step must be short compared with $d / v_L$ and $1/\alpha$.

## Variants and improvements

- **Separation-separation (l-l) control.** A follower keeps two distances to two leaders, which places it by two circles instead of a distance and an angle (Desai, Ostrowski and Kumar 2001).
- **Switching formations.** The tree and the targets can change, for example to pass a narrow gap in a column and to spread out after it.
- **Estimation of the leader motion.** Observers or sliding mode terms replace the received $v_L$ and $\omega_L$ when there is no communication.
- **Virtual leaders.** The root can be a virtual point that moves along a planned path, so that every real robot is a follower.
- **Distance-based and consensus-based laws.** These spread the work over an undirected graph and avoid a single point of failure, at the cost of global or local convergence conditions; see [formation control](/formation-control/).

## When to use it

Use leader-follower control for wheeled robots that must drive in a column, a wedge or a line behind one robot that a person or a planner controls, and when each robot can see one other robot and receive its speed and turn rate. It is simple to tune and has an exact exponential rate. Use [distance-based formation control](/distance-based-formation-control/) when no robot should depend on a single other robot, and consensus-based control when the robots share a compass.

## Pitfalls

- **Small offset.** The input $\omega_F$ is divided by $d$. A small $d$ gives large turn rates, as the 7.58 rad/s in the example shows, and real robots saturate.
- **Reverse driving.** When the leader drives backward the internal heading dynamics are unstable, and the follower can spin even while $l$ and $\psi$ look correct.
- **Bearing near the wrap.** If $\psi_d$ is near $\pi$, the measured bearing jumps between $\pi$ and $-\pi$. Wrap the difference $\psi_d - \psi$, not $\psi$ alone, as line L5 does.
- **Error propagation.** A long chain amplifies disturbances of the root, so the robots far down the tree see larger transients.
- **Collisions.** The law keeps the point $P_F$ at its target, but nothing stops two followers or a follower and its leader from touching during the transient.

## Implementations

## History

Desai, Ostrowski and Kumar (2001) modeled formations of nonholonomic robots as graphs of leader-follower pairs and gave two laws: one that keeps a separation and a bearing to one leader, and one that keeps two separations to two leaders. They used input-output linearization of an off-axis point and studied the stability of the remaining heading dynamics. Later work, summarized in the survey of Oh, Park and Ahn (2015), added estimation of the leader motion, switching between formations and undirected alternatives.

## References
