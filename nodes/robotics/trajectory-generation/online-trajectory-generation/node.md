---
tag: T2ZEJ5
kind: algorithm
slug: online-trajectory-generation
name: Online trajectory generation
aliases:
- Kroger-Wahl online trajectory generation
area: robotics/trajectory-generation
level: advanced
summary: "Computes in each control cycle a time-optimal motion from the current state, whatever it is, to a target state, under velocity, acceleration and often jerk limits."
solves: [trajectory-generation-problem]
model: real-ram
complexity:
  vars: {n: "the number of axes"}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, randomized: false, online: true, exact: true}
history:
  year: 2010
  people: [Torsten Kroger, Friedrich M. Wahl]
  note: "Kroger and Wahl classified online trajectory generation by the state that is given and the limits that apply, and gave decision-tree algorithms for synchronized, jerk-limited motions of several axes from arbitrary states within one control cycle."
prereqs: [trapezoidal-velocity-profile, double-s-velocity-profile]
see_also: [trapezoidal-velocity-profile, double-s-velocity-profile, bang-bang-control, model-predictive-control, time-optimal-path-parameterization, kinodynamic-planning, pontryagin-maximum-principle, trajectory-generation-problem]
sources:
  - paper: doi:10.1109/TRO.2009.2035744
    title: "Torsten Kroger and Friedrich M. Wahl, Online trajectory generation, basic concepts for instantaneous reactions to unforeseen events, IEEE Transactions on Robotics 26(1), 2010, 94-111"
    locator: "the whole paper (the types of online trajectory generation, the decision trees, inoperative time intervals and the synchronization of several axes)"
  - book: isbn:9783642051746
    title: "Torsten Kroger, On-Line Trajectory Generation in Robotic Systems, Springer Tracts in Advanced Robotics 58, Springer, 2010"
    locator: the whole book
  - paper: arxiv:2105.04830
    title: "Lars Berscheid and Torsten Kroger, Jerk-limited real-time trajectory generation with arbitrary target states, Robotics, Science and Systems, 2021"
    locator: "the whole paper (the Ruckig algorithm for jerk-limited motions to targets with nonzero velocity and acceleration)"
  - book: isbn:9783540856283
    title: "Luigi Biagiotti and Claudio Melchiorri, Trajectory Planning for Automatic Machines and Robots, Springer, 2008"
    locator: "Section 3.4.4 (online computation of the double S trajectory)"
---

Online trajectory generation computes, in every cycle of a robot controller, a new motion from the current state of the robot to a target state, and the controller follows the first cycle of it. The current state can be anything: the robot may be moving fast, even away from the target, because a sensor event or a new command arrived in the middle of a motion. The motion must respect limits on the velocity and the acceleration, and in the general method also on the jerk, and it should take the least possible time. Because the computation must finish within one cycle, often a millisecond, it uses closed-form cases rather than iterative optimization. Kroger and Wahl (2010) set up the problem and classified it by "type": Type II has velocity and acceleration limits and the state is (position, velocity), and Type IV adds a jerk limit and the acceleration to the state. Their main algorithm is Type IV. This page explains the method and gives code for one axis of Type II, where the whole case analysis fits on a page; the [double-S velocity profile](/double-s-velocity-profile/) shows what the jerk adds.

## In plain words

A robot arm is moving toward a box when a camera reports that the box has moved. The arm cannot stop and start over, because it is already moving. It needs a new plan that starts from exactly where it is and how fast it is going right now, and that reaches the new box as fast as its motors allow. The controller makes a new plan like that every thousandth of a second, so any change of target is handled at once. Each plan is short: push hard one way, maybe coast at top speed, push hard the other way. Sometimes the arm is going too fast toward a nearby target and must overshoot, turn back, and come in again.

## The problem

One axis, Type II. Input: the current state $(p_0, v_0)$, the target state $(p_T, v_T)$, and limits $V > 0$ and $A > 0$ with $|v_0|, |v_T| \le V$. Output: a motion of least duration $T^*$ from the current state to the target state with $|v| \le V$ and $|\dot v| \le A$ throughout. In the online setting this is solved again in every cycle of length $\Delta t$, from the state that the last cycle reached, and the target may change at any cycle.

For $n$ axes that must arrive at the same time, the time-optimal duration of each axis is computed first, and the slowest one sets the common time. The other axes are then stretched to that time. This step is the hard one, because the set of feasible durations of one axis need not be an interval: Kroger and Wahl call the gaps inoperative time intervals.

## The algorithm

Let $D = p_T - p_0$. An optimal profile has at most three pieces: acceleration $\sigma A$, then cruise at velocity $\sigma V$ (possibly of zero length), then acceleration $-\sigma A$, with $\sigma = \pm 1$. If the profile does not cruise, its peak velocity $v_p$ satisfies

$$v_p^2 = r = \sigma A D + \tfrac12 (v_0^2 + v_T^2).$$

```pseudo id=main
MIN-TIME-PROFILE(p0, v0, pT, vT, V, A)         ▷ D = pT - p0
L1  C ← the candidates built by lines L2 to L8
L2  for σ in (+1, -1)
L3      r ← σAD + (v0² + vT²)/2;  if r < 0 then skip this σ
L4      for vp in (+√r, -√r)
L5          if σ(vp - v0) < 0 or σ(vp - vT) < 0 then skip this vp
L6          if |vp| ≤ V then pieces ← [(σ(vp - v0)/A, σA), (σ(vp - vT)/A, -σA)]
L7          else vc ← σV;  t2 ← (D - ramp distance)/vc;  pieces ← [(σ(vc - v0)/A, σA), (t2, 0), (σ(vc - vT)/A, -σA)]
L8          add (sum of durations, pieces) to C
L9  return the candidate in C with the least time

OTG-STEP(p, v, pT, vT, V, A, Δt)               ▷ one control cycle
L10 (T, pieces) ← MIN-TIME-PROFILE(p, v, pT, vT, V, A)
L11 if T ≤ Δt then return (pT, vT)
L12 return the state of the profile at time Δt
```

Line L3 is the distance condition for a profile with no cruise. Line L5 keeps the root only if the first piece really accelerates in direction $\sigma$ and the last piece decelerates. Line L6 builds the two-piece profile. If the peak would exceed $V$, line L7 caps it at $\sigma V$ and inserts a cruise that covers the rest of the distance; the ramp distance is $\sigma(2V^2 - v_0^2 - v_T^2)/(2A)$. Line L9 picks the fastest candidate. Lines L10 to L12 are one control cycle.

## Example

**Moving start.** $p_0 = 0$, $v_0 = 0.5$, $p_T = 1$, $v_T = 0$, $V = 1$, $A = 2$, all in SI units. For $\sigma = +1$, line L3 gives $r = 2 + 0.125 = 2.125$, and $\sqrt r \approx 1.458 > V$, so line L7 builds a cruise profile: accelerate for $(1 - 0.5)/2 = 0.25$ s, the ramps cover $(2 - 0.25)/4 = 0.4375$ m, cruise for $0.5625$ s, decelerate for $0.5$ s. $T = 1.3125$ s. For $\sigma = -1$, $r = -2 + 0.125 < 0$, so there is no other candidate. A rest-to-rest [trapezoid](/trapezoidal-velocity-profile/) from the same point would take $1.5$ s; the initial speed saves time.

**Too fast for the target.** $p_0 = 0$, $v_0 = 1$, $p_T = 0.1$, $v_T = 0$, $V = 1$, $A = 1$. Braking at once stops the axis at $0.5$, past the target. For $\sigma = +1$, $r = 0.6$, and both roots fail line L5. For $\sigma = -1$, $r = 0.4$, and only $v_p = -\sqrt{0.4} \approx -0.6325$ passes: brake for $1.6325$ s through zero velocity to $-0.6325$, then accelerate back for $0.6325$ s and stop exactly at the target. $T \approx 2.2649$ s.

**Online.** The tests run the loop of lines L10 to L12 with $\Delta t = 0.001$ s. It follows the one-shot profile within $10^{-6}$, and when the target jumps at cycle 100, the loop turns to the new target in the next cycle with no jump in the velocity.

## Correctness

Theorem: line L9 returns a motion of least time. The [proof](proofs/correctness.md) first characterizes the reachable durations: a motion of duration $T$ exists if and only if $T \ge |v_T - v_0|/A$ and $D$ lies between the areas under two envelopes, the fastest and the slowest admissible velocity curves. At the least feasible duration $T^*$, $D$ equals one of the two areas, so the optimal velocity is an envelope: a ramp, possibly a cruise at the limit, and a ramp. Every such profile is among the candidates of lines L2 to L8, and every candidate is admissible. A second theorem: if the target does not change, re-planning in every cycle loses no time, because the remaining part of an optimal profile is optimal from the new state; the loop reaches the target after $\lceil T^*/\Delta t \rceil$ cycles. The tests check the optimality against a brute-force test of the envelope condition for 150 random states.

## Complexity

In the [real RAM](/real-ram/) with a square root, lines L1 to L9 examine at most four candidates, so one axis costs $\Theta(1)$ per cycle. For $n$ axes, computing all minimum times and the common time costs $\Theta(n)$. For Type IV, Kroger and Wahl use decision trees with many more cases, some solved with polynomial roots, but the number of operations per axis is still bounded by a constant. This is what makes the method fit into a cycle of one millisecond or less.

## Properties

- **Time-optimal from any state.** A theorem for the one-axis Type II problem: the result is the least time over all admissible motions, not only over profiles of a fixed shape.
- **Online.** A new target can be given in any cycle, and the motion stays within the limits, with continuous velocity, in every cycle.
- **No lost time.** With a fixed target, the receding plan reaches the target as fast as the one-shot plan, rounded up to a whole cycle (a theorem).
- **Bang-bang structure.** The acceleration is $+A$, $-A$, or $0$ while the speed limit is active; see [bang-bang control](/bang-bang-control/).
- **Acceleration jumps in Type II.** As with the trapezoid, the acceleration of a Type II profile jumps. Type IV removes the jumps by limiting the jerk.

## Variants and improvements

- **Type IV, jerk limited.** The state includes the acceleration and the jerk is bounded; the profiles have up to seven pieces, as the double S, and many more cases. Kroger and Wahl solve them with decision trees.
- **Arbitrary target states.** Berscheid and Kroger (2021) extended the jerk-limited case to targets with nonzero velocity and acceleration, in the open-source library Ruckig. The earlier Reflexxes library offered Type II as open source and Type IV commercially.
- **Velocity targets.** The target can be a velocity instead of a position, for jogging and for visual servoing.
- **Along a path.** Online generation in each axis does not keep the robot on a given path. Along a fixed path, use [time-optimal path parameterization](/time-optimal-path-parameterization/).
- **With a model.** [Model predictive control](/model-predictive-control/) also replans every cycle, with a model of the dynamics and a general cost, at a higher computing cost.

## When to use it

Use online trajectory generation when the target can change during a motion: sensor-guided motion, visual servoing, human-robot collaboration, switching between controllers, and emergency stops from an arbitrary state. Use it to make any command stream smooth and feasible. Use an offline [trapezoid](/trapezoidal-velocity-profile/) or double S if every motion starts and ends at rest and the target is known in advance; the result is the same with simpler code.

## Pitfalls

- **Ignoring the overshoot case.** Code that only tries the direction of the target fails when the axis is moving too fast toward a close target, as in the second example.
- **Rounding at the boundaries.** In floating point, line L5 needs a small tolerance, and a root near the limit can fall on either side of $V$. The code accepts small negative values in line L5.
- **States outside the limits.** If $|v_0| > V$, for example after a limit was lowered, there is no admissible motion. Handle this case first, by braking to the limit.
- **Synchronizing several axes naively.** Stretching each axis to the common time with a formula that assumes the feasible times form an interval fails inside an inoperative time interval.
- **Different cycle times.** The profile is computed in continuous time; evaluating it at a time other than the real cycle time makes the state drift.

## Implementations

## History

Robot controllers long used offline trajectories that start and end at rest. Kroger and Wahl (2010) gave a general framework and decision-tree algorithms that compute synchronized time-optimal motions of several axes from any state within one control cycle, with Types I to IV realized; Kroger's book of the same year gives the full treatment. Their Reflexxes library made the method widely used. Berscheid and Kroger (2021) published Ruckig, which handles jerk-limited motions to arbitrary target states.

## References
