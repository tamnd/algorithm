---
tag: E287FS
kind: algorithm
slug: trapezoidal-velocity-profile
name: Trapezoidal velocity profile
aliases:
- linear segment with parabolic blends
- LSPB
area: robotics/trajectory-generation
level: intro
summary: "Moves one axis from rest to rest in minimum time under velocity and acceleration limits: accelerate, cruise, decelerate, or a triangle if short."
solves: [trajectory-generation-problem]
model: real-ram
complexity:
  vars: {n: "the number of axes"}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, randomized: false, online: false, exact: true}
prereqs: [time-scaling]
see_also: [double-s-velocity-profile, feedrate-scheduling, cam-follower-motion-laws, bang-bang-control, cubic-polynomial-trajectory, online-trajectory-generation, time-optimal-path-parameterization, trajectory-generation-problem]
sources:
  - book: isbn:9783540856283
    title: "Luigi Biagiotti and Claudio Melchiorri, Trajectory Planning for Automatic Machines and Robots, Springer, 2008"
    locator: "Section 3.2 (trajectory with constant acceleration, the trapezoidal velocity profile), with Section 3.2.3 on synchronizing several axes"
  - book: isbn:9781107156302
    title: "Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017"
    locator: "Chapter 9, Section 9.2.2 (time scaling a straight-line path)"
  - book: isbn:9781846286414
    title: "Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009"
    locator: the chapter on trajectory planning (joint space trajectories)
---

A trapezoidal velocity profile moves one axis, such as a robot joint or a machine slide, over a distance $D$ from rest to rest in the least possible time when the speed is at most $V$ and the acceleration is at most $A$ in size. It accelerates at $A$, cruises at $V$, and decelerates at $A$, so the velocity plotted against time is a trapezoid. If the move is too short to reach $V$, that is if $D < V^2/A$, the cruise phase disappears and the profile is a triangle that peaks at $\sqrt{AD}$. The position is a parabola during the ramps and a straight line during the cruise, which is where the robotics name "linear segment with parabolic blends" comes from. The profile is the cheapest time-optimal motion there is, but its acceleration jumps between $0$ and $\pm A$, so the jerk is infinite at four instants. The [double-S velocity profile](/double-s-velocity-profile/) adds a jerk limit for this reason, and [feedrate scheduling](/feedrate-scheduling/) in machine tools uses both.

## In plain words

A car must go from one red light to the next as fast as possible, without going over the speed limit and without pressing the pedals harder than a fixed amount. The best plan is the obvious one: floor it, hold the speed limit, then brake as late as possible so the car stops exactly at the light. Plot the speed over time and you see a ramp up, a flat top and a ramp down, a trapezoid. If the lights are close, the car never reaches the limit: it speeds up until half way and then brakes, and the plot is a triangle. The page shows why no other plan is faster, and how to stretch the plan so that several axes arrive at the same moment.

## The problem

Input: a distance $D > 0$, a velocity limit $V > 0$ and an acceleration limit $A > 0$. Output: a motion $s(t)$ on $[0, T]$ with $s(0) = 0$, $s(T) = D$, $s'(0) = s'(T) = 0$, $|s'| \le V$ and $|s''| \le A$, with $T$ as small as possible. This is the rest-to-rest case on one axis. A signed move from $q_0$ to $q_1$ uses $D = |q_1 - q_0|$ and the sign of $q_1 - q_0$. Moves that start or end at a nonzero velocity are the job of [online trajectory generation](/online-trajectory-generation/).

## The algorithm

```pseudo id=main
TRAPEZOID(D, V, A)                         ▷ D, V, A > 0
L1  if D·A ≥ V² then                        ▷ the move is long enough to reach V
L2      Ta ← V / A;  vp ← V
L3      T ← D / V + V / A
    else                                     ▷ triangle
L4      Ta ← √(D / A);  vp ← A·Ta
L5      T ← 2 Ta
L6  return (Ta, vp, T)

SAMPLE(D, Ta, vp, T, t)                     ▷ A = vp / Ta
L7  if t < Ta then return (A t²/2, A t, A)
L8  if t ≤ T - Ta then return (vp (t - Ta/2), vp, 0)
L9  if t < T then r ← T - t;  return (D - A r²/2, A r, -A)
```

Line L1 compares $D$ with $V^2/A$, the distance needed to ramp up to $V$ and back down. Lines L2 and L3 give the trapezoid: each ramp takes $V/A$ and covers $V^2/(2A)$, and the cruise covers the rest, $D - V^2/A$, at speed $V$. Lines L4 and L5 give the triangle: each half takes $T_a$ and covers $AT_a^2/2 = D/2$. Lines L7 to L9 give the position, the velocity and the acceleration in the three phases.

**Several axes.** If $n$ axes must start and stop together, compute the minimum time $T_k$ of each axis and take $T = \max_k T_k$. Every other axis then covers its distance in the longer time $T$ with a slower trapezoid. Keeping the acceleration $A$, its ramp time is the smaller root of $D = A T_a (T - T_a)$:

$$T_a = \tfrac12\left(T - \sqrt{T^2 - 4D/A}\right),$$

which is real when $T \ge 2\sqrt{D/A}$, and its peak $AT_a$ is at most $V$ (proof, Lemma 4). Biagiotti and Melchiorri (Section 3.2.3) also give versions that scale the velocity and the acceleration together.

## Example

**Trapezoid.** $D = 1$ m, $V = 1$ m/s, $A = 2$ m/s². Line L1: $D A = 2 \ge V^2 = 1$, so lines L2 and L3 give $T_a = 0.5$ s and $T = 1 + 0.5 = 1.5$ s. The axis accelerates for 0.5 s and covers 0.25 m, cruises for 0.5 s and covers 0.5 m, and brakes for 0.5 s over the last 0.25 m.

**Triangle.** $D = 0.25$ m with the same limits. Line L1: $0.5 < 1$, so lines L4 and L5 give $T_a = \sqrt{0.125} \approx 0.3536$ s, a peak of $0.7071$ m/s, and $T \approx 0.7071$ s.

**Two axes.** Axis 1 moves 1 m and axis 2 moves 0.5 m, both with $V = 1$ and $A = 2$. Alone, axis 2 would take $0.5 + 0.5 = 1$ s. Both must take $T = 1.5$ s, so axis 2 uses $T_a = (1.5 - \sqrt{2.25 - 1})/2 \approx 0.1910$ s and peaks at $0.3820$ m/s. Check: $2 \cdot 0.1910 \cdot (1.5 - 0.1910) \approx 0.5$.

**Machine tool numbers.** With the example of [feedrate scheduling](/feedrate-scheduling/), $D = 100$ mm, $V = 50$ mm/s, $A = 500$ mm/s², the trapezoid takes $100/50 + 50/500 = 2.1$ s. The double-S profile with a jerk limit of $10^4$ mm/s³ takes $2.15$ s.

## Correctness

Theorem: the profile is admissible, covers exactly $D$, and no admissible motion is faster. The proof bounds the velocity of any admissible motion of duration $T$ by the envelope $\min(At, V, A(T - t))$, because the velocity starts and ends at zero and cannot change faster than $A$. The area under the envelope is the most distance that time $T$ allows, and it grows strictly with $T$. The profile of lines L1 to L5 is the envelope itself, with area exactly $D$, so any shorter time covers less than $D$. In optimal control terms, the acceleration is "bang-bang": it is always $+A$ or $-A$, except while the speed limit is active, where it is $0$. The [proof](proofs/correctness.md) gives the four lemmas and the synchronization formula.

## Complexity

In the [real RAM](/real-ram/) with a square root, lines L1 to L6 take $\Theta(1)$ operations and lines L7 to L9 take $\Theta(1)$ per sample. Synchronizing $n$ axes costs $\Theta(n)$ time and space. This is why the profile is used in controllers with cycle times of a millisecond or less.

## Properties

- **Time-optimal.** A theorem, for one axis, rest to rest, under velocity and acceleration limits.
- **Two shapes.** Trapezoid if $D \ge V^2/A$, triangle otherwise. The time is $D/V + V/A$ or $2\sqrt{D/A}$, a continuous function of $D$.
- **Velocity continuous, acceleration not.** The acceleration takes the values $A$, $0$ and $-A$ and jumps between them, so the jerk is unbounded at the switching times. This excites vibration in elastic machines.
- **Symmetric.** The deceleration phase mirrors the acceleration phase.
- **Several axes.** Stretching every axis to the slowest one gives the least common time for the separate limits $|q_k'| \le V_k$, $|q_k''| \le A_k$, because no axis can be faster than alone. It does not handle limits that couple the axes, such as a limit on the speed of the tool along its path, and the axes then do not move along a straight line in joint space unless their profiles are scaled copies of each other.

## Variants and improvements

- **Double S.** A jerk limit $J$ replaces each jump of the acceleration by a ramp: the [double-S velocity profile](/double-s-velocity-profile/), with up to seven phases.
- **Nonzero end velocities.** From an arbitrary current state, the minimum-time motion can overshoot or have the opposite sign of acceleration first; this is the job of [online trajectory generation](/online-trajectory-generation/) (Type II in the terms of Kroger and Wahl).
- **Along a path.** The same "accelerate as hard as you may, as late as you may brake" idea along a curved path, with limits that depend on the position, gives [time-optimal path parameterization](/time-optimal-path-parameterization/).
- **Cam laws.** In cam design the same profile is the constant acceleration law, one of the [cam follower motion laws](/cam-follower-motion-laws/).
- **Via points.** In the robotics form "linear segments with parabolic blends", straight segments in each joint are joined by parabolic blends. The blends round the corners, so the joint passes near the via points but in general not through them.

## When to use it

Use the trapezoid for point-to-point moves of motors and slides that must be fast and simple, where the drives can absorb the jumps of the acceleration: pick and place, axis jogging, conveyor indexing, and as the default move of many motion controllers. Use the triangle formula for short moves; do not cap a short move at $V$ if it cannot reach it. Use the double-S profile when vibration matters, and a [cubic](/cubic-polynomial-trajectory/) or a quintic when the duration is fixed in advance and the limits are loose.

## Pitfalls

- **Forgetting the triangle case.** Using $T = D/V + V/A$ for $D < V^2/A$ gives a profile that never reaches the cruise and does not cover $D$.
- **Rounding at the switch times.** In floating point, sample at $t$ near $T_a$ or $T - T_a$ with care: test intervals as lines L7 to L9 do, and clamp the last sample to $(D, 0, 0)$.
- **Nonzero start velocity.** The formulas are for rest to rest. Starting a new trapezoid from a moving state with these formulas causes a jump of the velocity.
- **Different limits in each direction.** Some drives brake harder than they accelerate. Then the two ramps have different times, and the formulas change.
- **Jerk.** The jump of the acceleration is a real force jump. On light or elastic machines it causes ringing at the end of the move.

## Implementations

## History

The profile is the bang-bang solution of the minimum-time problem for a double integrator with a bound on the input, extended by a cruise phase at the velocity bound; this is a classical result of optimal control (see [bang-bang control](/bang-bang-control/)). It became the default motion of point-to-point motor controllers and of the first robot controllers, and textbooks present it as "linear segments with parabolic blends". Biagiotti and Melchiorri (2008) treat it in detail, with its synchronized multi-axis versions.

## References
