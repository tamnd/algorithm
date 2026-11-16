---
tag: 32ZJAX
kind: algorithm
slug: elastic-bands
name: Elastic bands
aliases:
- Quinlan-Khatib elastic band
area: robotics/trajectory-generation
level: advanced
summary: "Deforms a path in real time under internal contraction forces and external repulsion from obstacles, keeping it short and safe."
solves: [motion-planning]
model: real-ram
complexity:
  vars: {m: "the largest number of bubbles during the run", C: "the time of one distance query", S: "the number of sweeps"}
  time: {worst: O(S m C)}
  space: {extra: O(m)}
properties: {deterministic: true, randomized: false, online: true, exact: false}
prereqs: [motion-planning, potential-field-method]
see_also: [trajectory-optimization, chomp, stomp, random-shortcut-path-smoothing, dynamic-window-approach, signed-distance-function, distance-transform, rapidly-exploring-random-tree]
sources:
  - paper: doi:10.1109/ROBOT.1993.291936
    title: "Sean Quinlan and Oussama Khatib, Elastic bands: Connecting path planning and control, IEEE International Conference on Robotics and Automation (ICRA), 1993, vol. 2, 802-807"
    locator: "the whole paper (bubbles, the contraction and repulsion forces, and the insertion and deletion of bubbles)"
---

An elastic band takes a free path from a global planner and keeps improving it while the robot moves. The path is a chain of bubbles: each bubble is a disc around a point of the path whose radius is the distance to the nearest obstacle, so it is free space. While neighbor bubbles overlap, the path through their centers is free of collision. In each sweep, every inner bubble feels a contraction force that pulls the band tight and a repulsion force that pushes it away from close obstacles, and moves only if it still overlaps its neighbors. New bubbles fill gaps, and bubbles that are not needed are removed. The band stays safe in a fixed scene, but it is a local method with no general convergence guarantee, and it can only bend the path, not find a new route.

## In plain words

Think of a rubber band laid along a path between two pins, with soft balls threaded on it. Each ball is as large as the free space around it allows, and the band is safe while the balls touch each other. The band pulls itself tight, and obstacles push the balls away when they come close. A ball moves only if it still touches its neighbors afterwards. Where two balls are about to lose contact, a new ball goes between them; where a ball is not needed, it is taken out. When an obstacle moves a little, the band bends around it at once, with no new plan. When an obstacle moves fast or blocks the way, the band can break, and a planner must find a new path.

## The problem

Input: a start and a goal in the plane, a distance function $\rho(p)$ that gives the distance from $p$ to the nearest obstacle, and a band $b_0, \dots, b_m$ from the start to the goal that is *valid*: $\rho(b_i) > 0$ for every $i$, and neighbors overlap,

$$\|b_{i+1} - b_i\| < \rho(b_i) + \rho(b_{i+1}).$$

Output: a valid band with the same ends that is shorter and keeps some distance from the obstacles. The obstacles can change between sweeps; the band must then be valid for the new scene before the next sweep. This page uses a point robot and disc obstacles, with $\rho(p) = \min_j (\|p - o_j\| - r_j)$. For a robot with a body, $\rho$ is the distance from the body to the obstacles, as returned by a [distance query](/signed-distance-function/) or read from a [distance transform](/distance-transform/).

## The algorithm

```pseudo id=main
ELASTIC-BAND(b_0, …, b_m, ρ, S)
L1  for s ← 1 to S do
L2      for i ← 1 to m - 1 do                       ▷ inner bubbles only
L3          r ← ρ(b_i)
L4          f ← k_c (u(b_{i-1}) + u(b_{i+1})) + k_r max(0, ρ_0 - r) ∇ρ(b_i), minus its part along the band
L5          c ← b_i + h f with h = α min(r, 1), halving h at most `tries` times
L6          if ρ(c) ≥ ρ_min and c overlaps b_{i-1} and b_{i+1} then b_i ← c
L7      for each pair of neighbors a, b with ‖b - a‖ > 0.9 (ρ(a) + ρ(b)) do insert (a + b)/2 between them
L8      for each inner b_i with ‖b_{i+1} - b_{i-1}‖ < 0.5 (ρ(b_{i-1}) + ρ(b_{i+1})) do delete b_i
L9  return b
```

Here $u(q)$ is the unit vector from $b_i$ toward the neighbor $q$. The code uses $k_c = 1$, $k_r = 4$, $\rho_0 = 0.3$, $\alpha = 0.3$, $\rho_{\min} = 10^{-3}$ and four tries.

Line L4 computes the force. The contraction part is the sum of the unit vectors toward the two neighbors; it is zero when the three points are on a line and points inward at a bend, so it straightens the band. The repulsion part pushes away from the nearest obstacle when it is closer than $\rho_0$. The part of the force along the band is removed, because it would only slide bubbles along the band and bunch them up. This is a simple form of the forces; the original paper uses forces of the same kind, and other versions scale the contraction by the distance to the neighbors.

Line L5 scales the step by the radius of the bubble, so a bubble in open space moves far and a bubble near an obstacle moves a little. Line L6 is the safety test: the new bubble must be free and overlap both current neighbors. If the test fails, the step is halved, and after the last try the bubble stays where it was.

Line L7 inserts a bubble where two neighbors are close to losing contact. The midpoint of two overlapping bubbles always overlaps both, so this step needs no test (proof, Lemma 5). Line L8 removes a bubble whose two neighbors overlap well by themselves; this keeps the band short and the number of bubbles small.

## Example

A point moves from $(-1, 0)$ to $(1, 0)$ around one disc of radius $0.5$ at the origin. A global planner returned the polyline through $(-0.8, 0.9)$ and $(0.8, 0.9)$, which is resampled to 19 points at most $0.2$ apart. The table gives the band after each number of sweeps. The clearance of the path is sampled at 21 points on each segment; it is smaller than the smallest bubble, because a segment passes closer to the disc than its ends.

| sweeps | bubbles | length | smallest bubble | clearance of the path | highest point |
|---|---|---|---|---|---|
| 0 | 19 | 3.4439 | 0.400 | 0.400 | 0.900 |
| 1 | 10 | 2.9376 | 0.311 | 0.310 | 0.867 |
| 2 | 10 | 2.7305 | 0.292 | 0.288 | 0.811 |
| 3 | 10 | 2.6376 | 0.269 | 0.253 | 0.769 |
| 5 | 10 | 2.5780 | 0.235 | 0.217 | 0.737 |
| 10 | 10 | 2.5591 | 0.225 | 0.207 | 0.727 |
| 20 | 10 | 2.5579 | 0.225 | 0.207 | 0.727 |

In the first sweep the band drops from 19 to 10 bubbles, because the bubbles far from the disc are large and overlap well without their neighbors. After about twenty sweeps the band does not change at four decimals, and the band is valid after every sweep. The shortest path around the disc, made of two tangents and an arc on the disc, has length $2.2556$; the band stays longer, because the repulsion holds it about $0.21$ away from the disc, where it balances the contraction. With the disc moved far away, the band becomes the straight segment of length $2$ with only its two ends.

Then a second disc of radius $0.15$ comes down at $x = -0.4$ from height $1.5$ to height $0.75$, with one sweep after each step. At a speed of $0.03$ per step the band bends away and stays valid at every step, with a smallest clearance of $0.088$; at $0.01$ per step the smallest clearance is $0.076$. At $0.1$ per step, the band is already cut by the new disc when it reaches height $0.8$, before the sweep can react. The guarantee holds only when the band is valid for the scene it is updated in.

## Correctness

The [proof](proofs/correctness.md) shows that a valid band stays valid. A bubble contains no obstacle point, and two overlapping bubbles cover the segment between their centers, so the polyline of a valid band is free of collision. A move of line L6 is tested against the current neighbors. A midpoint inserted by line L7 always overlaps both neighbors, because the distance function changes by at most the distance moved. A deletion of line L8 happens only when the two new neighbors overlap. The ends never move. So in a fixed scene every sweep returns a valid band. Nothing is proved about convergence, about the length going down, or about reaching the shortest path; with moving obstacles, the band is safe only if it is valid for the new scene before the sweep.

## Complexity

One sweep with $m$ bubbles makes $O(m)$ distance queries: a bounded number of tries per bubble in lines L5 and L6, and a constant number of queries per pair in lines L7 and L8. So one sweep costs $O(mC)$, and $S$ sweeps cost $O(SmC)$ with $m$ the largest number of bubbles during the run. Line L7 can at most double the number of bubbles in one sweep. The memory is $O(m)$.

There is no bound on the number of sweeps to reach a resting band. The twenty sweeps of the example are a measurement, not a bound. In practice the band runs a fixed number of sweeps per control cycle and never "finishes".

## Properties

- **Safe in a fixed scene.** Every sweep keeps the band valid, so the path is always free of collision.
- **Local.** The band can only deform the path it has; it does not find a route on the other side of an obstacle.
- **Reactive.** A sweep is cheap, so it can run in every control cycle and follow slowly moving obstacles.
- **Adaptive resolution.** Bubbles are small and many near obstacles and big and few in open space.
- **Deterministic.** The same band and scene give the same result.
- **No convergence guarantee.** The resting band depends on the gains and on $\rho_0$, and the band need not settle at all.

## Variants and improvements

- **Elastic strips.** For mobile manipulators, the bubbles become protective volumes around the whole body of the robot along the path.
- **Timed elastic band.** Each point gets a time step as well, and the band is deformed by an optimizer with costs for time, velocity and acceleration; this is widely used as a local planner for mobile robots.
- **Other forces.** The contraction can depend on the distance to the neighbors, like a spring, and the repulsion can use a smooth function of $\rho$, in the spirit of [potential fields](/potential-field-method/).
- **Optimization view.** Seen as gradient steps on length plus an obstacle cost, the band is close to [CHOMP](/chomp/) and other methods of [trajectory optimization](/trajectory-optimization/); the difference is the safety test of line L6 instead of a soft cost.

## When to use it

Use an elastic band between a global planner and the controller, when the path must stay smooth and safe while obstacles move slowly and the robot cannot wait for a new plan. It is simple, cheap per cycle, and easy to reason about in a fixed scene. It does not replace a planner: when an obstacle blocks the band or moves fast, call a planner such as an [RRT](/rapidly-exploring-random-tree/) again. To smooth a path once, offline, [random shortcutting](/random-shortcut-path-smoothing/) or trajectory optimization is simpler. For velocity commands near moving obstacles, see the [dynamic window approach](/dynamic-window-approach/).

## Pitfalls

- **Fast obstacles.** The tests of lines L6 and L8 assume that the band is valid before the sweep. If an obstacle jumps onto the band between two sweeps, nothing repairs it; check the band against the new scene first and replan if it is cut.
- **Step size.** If the step of line L5 is too big, most candidates fail the test of line L6 and the band stalls; if it is too small, the band follows obstacles too slowly.
- **Insertion and deletion thresholds.** If the factor of line L8 is close to the factor of line L7, a bubble can be inserted and deleted again in every sweep. Keep them well apart, as $0.9$ and $0.5$ here.
- **Gains are tuning.** The gains $k_c$, $k_r$ and the influence distance $\rho_0$ of line L4 are rules of thumb; they set how far from the obstacles the band rests, and other robots need other values.
- **Distance quality.** The safety argument needs a true lower bound on the distance in line L3. A distance that is too large, for example from a coarse grid, can let the band pass through an obstacle.

## Implementations

## History

Sean Quinlan and Oussama Khatib at Stanford introduced elastic bands at ICRA 1993, as a link between a global planner, which finds a path once, and a controller, which must react to obstacles in real time. Their bubbles are regions of free space found from distance information, and the band is deformed by internal contraction and external repulsion forces while new bubbles are added and old ones removed. Khatib and his students later extended the idea to whole-body motion of mobile manipulators as elastic strips, and the timed elastic band, which adds time to each point, became a common local planner in robot navigation software.

## References
