---
tag: W25J11
kind: algorithm
slug: fabrik
name: FABRIK
aliases:
- forward and backward reaching inverse kinematics
area: robotics/robot-kinematics
level: advanced
summary: Solves the inverse kinematics of a chain by moving joint positions along lines in a backward and a forward pass, keeping link lengths.
model: real-ram
complexity:
  vars: {n: the number of links, k: the number of iterations}
  time: {worst: Θ(k n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 2011
  people: [Andreas Aristidou, Joan Lasenby]
  note: Aristidou and Lasenby introduced FABRIK as a heuristic that works on joint positions instead of joint angles; Aristidou, Chrysanthou and Lasenby later gave a proof of convergence for the unconstrained chain.
prereqs: [inverse-kinematics, kinematic-chain]
see_also: [cyclic-coordinate-descent-inverse-kinematics, jacobian-transpose-method, damped-least-squares-inverse-kinematics, robot-workspace, forward-kinematics, newton-raphson-inverse-kinematics]
sources:
  - paper: doi:10.1016/j.gmod.2011.05.003
    title: "Andreas Aristidou and Joan Lasenby, FABRIK: A fast, iterative solver for the Inverse Kinematics problem, Graphical Models 73(5), 243-260, 2011"
    locator: Section 4 (the algorithm for a single chain)
  - book: "Andreas Aristidou, Yiorgos Chrysanthou and Joan Lasenby, Extending FABRIK with model constraints, Computer Animation and Virtual Worlds 27(1), 35-57, 2016"
    locator: Section 3.3 (proof of convergence)
---

FABRIK (forward and backward reaching inverse kinematics) solves the inverse kinematics of a chain by working on the joint positions instead of the joint angles.
A backward pass puts the end effector on the target and pulls each joint back along a line so that each link keeps its length.
A forward pass then puts the first joint back on the base and pushes the joints out again in the same way.
Each step only finds a point on a line, so it is very cheap, and the error never increases.
Aristidou and Lasenby (2011) introduced it for computer animation.

## In plain words

Think of a chain of rigid rods joined end to end, with the first end fixed to a wall.
Grab the free end and put it on the target.
The next rod now has a gap at its far end, so drag that joint along the straight line toward its old place until the rod has its length again, and go on to the wall.
The first joint is now off the wall.
Put it back, and drag the joints in the same way from the wall out to the free end.
The free end is now near the target, and usually nearer than before.
Repeat until it is close enough.
At the end, read the joint angles off the joint positions.

## The problem

**Input.**

- The joint positions $p_0, \ldots, p_n$ of a serial chain with ball or unconstrained joints, in the plane or in space, and the link lengths $d_i = |p_i - p_{i-1}|$.
- The base $b = p_0$, which stays fixed, a target $t$, a tolerance $\varepsilon$ and an iteration limit $k_{\max}$.

**Output.** New joint positions with the same base and link lengths and $|p_n - t| \le \varepsilon$, or the stretched chain toward a target out of reach, or the last iterate with the report that the tolerance was not met.

The joint angles follow from the positions, by the direction of each link relative to the one before.

## The algorithm

```pseudo id=main
FABRIK(p_0..p_n, d_1..d_n, t, ε, k_max)
L1  b ← p_0
L2  if |t - b| > d_1 + ... + d_n then
L3      for i ← 0 to n - 1: p_{i+1} ← p_i + d_{i+1} (t - p_i) / |t - p_i|
L4      return p, with the report that t is out of reach
L5  for k ← 1 to k_max
L6      if |p_n - t| ≤ ε then return p
L7      p_n ← t; for i ← n - 1 downto 0: p_i ← p_{i+1} + d_{i+1} (p_i - p_{i+1}) / |p_i - p_{i+1}|     ▷ backward
L8      p_0 ← b; for i ← 0 to n - 1: p_{i+1} ← p_i + d_{i+1} (p_{i+1} - p_i) / |p_{i+1} - p_i|     ▷ forward
L9  return p with the report that the tolerance was not met
```

Each update at L7 and L8 puts a joint on the sphere of radius $d$ about its neighbor, at the point of that sphere nearest to the old position of the joint.
If the two points coincide, the direction is not defined, and any direction works; the code takes the first axis.

## Example

The planar chain has the lengths $(1, 0.8, 0.5)$ m, the base at the origin and the start angles $(0.3, 0.4, 0.5)$ rad, so the joints are at $(0, 0)$, $(0.955336, 0.295520)$, $(1.567210, 0.810894)$ and $(1.748389, 1.276914)$ m.
The target is $t = (1.2, 0.6)$ m, and the start error is 0.871173 m.

- The backward pass puts $p_3$ on $t$ and moves $p_2$ and $p_1$, and $p_0$ ends at $(0.066581, 0.022541)$ m, off the base.
- The forward pass puts $p_0$ back at the origin, and $p_3$ ends at $(1.142549, 0.568550)$ m.
The error is now 0.065496 m.

| iterations | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| error (m) | 0.871173 | 0.065496 | 0.058673 | 0.054112 | 0.050900 |

The first iteration removes 92 % of the error, but then progress is slow: the ratio of errors tends to 0.9007, and the error falls below $10^{-10}$ m after 232 iterations.
The final angles are $(0.377886, -0.104655, 2.838020)$ rad, and forward kinematics of these angles gives back the joint positions.
For a 2R arm, FABRIK is much faster: with lengths 1 m, the start $(0.3, 1.2)$ rad and the target $(1, 1)$ m, it reaches $\theta = (0, \pi/2)$ to $10^{-11}$ m in 2 iterations.

## Correctness

The proof page proves these facts in exact arithmetic.

- **Valid chain.** After each forward pass, the base is at $b$ and every link has its length.
- **Nearest points.** Each update moves a joint to the nearest point at the right distance from its neighbor.
- **Monotone error.** The error $|p_n - t|$ never increases from one iteration to the next.
- **Out of reach.** If $|t - b| > \sum d_i$, line L3 gives the configuration nearest to the target, stretched along the line from the base.
- **Fixed points.** A solution does not change under an iteration.
- **Stall on a line.** If the base, the target and all joints lie on one line, every iterate stays on that line.

**Convergence.** Aristidou and Lasenby (2011) observed convergence in experiments.
Aristidou, Chrysanthou and Lasenby (2016, Section 3.3) state and prove convergence for the unconstrained chain when the target is in reach.
The stall on a line shows that a start where all joints lie on the line through the base and the target must be excluded: three links of 1 m on the $x$ axis can only put the end at $x = \pm 1$ or $\pm 3$ m on that line, so for the target $(0.1, 0)$ m the error stays at 0.9 m.
Monotone error alone does not give convergence to 0, and no rate is known in general; the example shows a linear tail.

## Complexity

**Cost per iteration.** Each pass does $n$ updates, each with one distance and one square root in fixed dimension, so one iteration costs $\Theta(n)$ in the [real RAM](/real-ram/).
The test of reach at L2 costs $\Theta(n)$ once.
So $k$ iterations cost $\Theta(kn)$, with $\Theta(n)$ extra space for the positions.

**Number of iterations.** It is not bounded in general; it ranged from 2 to 232 in the examples.

## Properties

- **No angles, no matrices.** The method needs no Jacobian, no rotation matrices and no linear solves.
- **Valid output.** Every output is a valid chain with the right link lengths and base.
- **Monotone.** The error never increases.
- **Smooth poses.** The motion spreads over the whole chain, so the poses tend to look natural in animation, unlike the curled poses of [cyclic coordinate descent](/cyclic-coordinate-descent-inverse-kinematics/).
- **Positions only.** The basic method treats each joint as a ball joint; hinge axes and joint limits need extra steps.

## Variants and improvements

- **Joint limits and hinges.** After each placement, move the joint into the allowed cone or plane of the joint; Aristidou, Chrysanthou and Lasenby (2016) study such model constraints.
- **Several end effectors.** Aristidou and Lasenby (2011) treat trees of chains: each branch does its backward pass, a shared joint takes the mean of its proposals, and the forward pass goes from the root out.
- **Orientation targets.** A target orientation of the end link can be handled by a second target point for the joint before the end, at the right distance along the wanted direction.
- **Other methods.** [Cyclic coordinate descent](/cyclic-coordinate-descent-inverse-kinematics/) also updates one joint at a time, but on angles; [damped least squares](/damped-least-squares-inverse-kinematics/) moves all joints together with a Jacobian.

## When to use it

Use FABRIK for long chains and skeletons in animation and games, where the joints are close to ball joints and each frame needs a cheap update that gives natural poses.
For an industrial arm with hinge joints and a full pose target, use [Newton-Raphson inverse kinematics](/newton-raphson-inverse-kinematics/), [damped least squares](/damped-least-squares-inverse-kinematics/) or a closed form solution.

## Pitfalls

- **Degenerate starts.** A start with all joints on the line through the base and the target can stay there forever; a small bend of the start removes the stall.
- **The test of reach.** Line L2 checks only the outer radius of the [workspace](/robot-workspace/).
A target inside the inner hole, such as a point closer to the base than $|d_1 - d_2|$ for two links, passes the test, but no iteration can reach it, and the loop runs to the limit.
- **Slow tails.** As the example shows, the error can fall fast at first and then slowly; set the tolerance and the limit with care.
- **Hinge joints.** Reading angles off a 3D result for an arm with hinge joints is not valid unless the hinge constraints were applied in each pass.
- **Coincident points.** If a joint lands on its neighbor, the direction at L7 or L8 is not defined; choose one and keep the result valid.

## Implementations

## History

Aristidou and Lasenby (2011) introduced FABRIK in Graphical Models as a fast heuristic for inverse kinematics that finds each joint position by locating a point on a line.
They showed it on single chains, on chains with several end effectors and with joint limits, and compared it with Jacobian and coordinate descent methods.
Aristidou, Chrysanthou and Lasenby (2016) extended it with model constraints for human figures and gave a proof of convergence for the unconstrained chain.

## References
