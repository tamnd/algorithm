---
tag: 07FRKR
kind: algorithm
slug: double-s-velocity-profile
name: Double-S velocity profile
aliases:
- S-curve velocity profile
- seven-segment jerk-limited profile
area: robotics/trajectory-generation
level: core
summary: "A point-to-point motion with bounded jerk, acceleration and velocity, made of up to seven segments of constant jerk."
solves: [trajectory-generation-problem]
model: real-ram
complexity:
  vars: {n: "the number of axes"}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, randomized: false, online: false, exact: true}
prereqs: [trapezoidal-velocity-profile]
see_also: [trapezoidal-velocity-profile, feedrate-scheduling, cam-follower-motion-laws, online-trajectory-generation, quintic-polynomial-trajectory, minimum-jerk-trajectory, time-optimal-path-parameterization, trajectory-generation-problem]
sources:
  - book: isbn:9783540856283
    title: "Luigi Biagiotti and Claudio Melchiorri, Trajectory Planning for Automatic Machines and Robots, Springer, 2008"
    locator: "Section 3.4 (trajectory with double S velocity profile), in particular Section 3.4.3 for null initial and final velocities and Section 3.4.4 for online computation; Section 3.5 for the fifteen segments variant"
  - paper: doi:10.1109/TRO.2009.2035744
    title: "Torsten Kroger and Friedrich M. Wahl, Online trajectory generation, basic concepts for instantaneous reactions to unforeseen events, IEEE Transactions on Robotics 26(1), 2010, 94-111"
    locator: "the whole paper (jerk-limited motions from arbitrary states, Type IV)"
---

A double-S velocity profile moves one axis over a distance $D$ from rest to rest with the velocity at most $V$, the acceleration at most $A$ and the jerk, the rate of change of the acceleration, at most $J$ in size. The jerk is piecewise constant, taking the values $+J$, $0$ and $-J$, so the acceleration is piecewise linear and continuous, and the velocity plotted against time has two smooth S-shaped bends, one when speeding up and one when slowing down. This is the [trapezoidal velocity profile](/trapezoidal-velocity-profile/) with each jump of the acceleration replaced by a ramp of slope $J$. Seven segments result: three to accelerate, one to cruise, three to decelerate. Some segments have zero length when a limit is not reached. The profile is the standard motion of servo drives and CNC machines, where [feedrate scheduling](/feedrate-scheduling/) uses it along the tool path, because the bounded jerk avoids the vibration that the trapezoid causes.

## In plain words

The trapezoid profile switches the motor force on and off at once. A machine is a little elastic, so each sudden switch makes it ring like a struck bell. The double S profile turns the force up and down gradually, at a fixed maximum rate. So a move has seven parts: force rising, force held, force falling to zero, cruising, and the same three in reverse to stop. If the move is short, some parts vanish: the force may never reach its maximum, or the speed may never reach its maximum. The price is a little time. When the speed and force limits are both reached, the move is longer than the trapezoid by exactly the time it takes to ramp the force up once.

## The problem

Input: a distance $D > 0$ and limits $V, A, J > 0$. Output: a motion $s(t)$ on $[0, T]$ with $s(0) = 0$, $s(T) = D$, zero velocity and acceleration at both ends, $|s'| \le V$, $|s''| \le A$ and $|s'''| \le J$, whose jerk is piecewise constant with values in $\{-J, 0, J\}$. The deceleration phase is the mirror image of the acceleration phase. The general form, with nonzero end velocities and different limits for speeding up and slowing down, is in Biagiotti and Melchiorri, Section 3.4; this page covers the rest-to-rest case of their Section 3.4.3.

## The algorithm

The acceleration phase has jerk $+J$ for $T_j$, jerk $0$ for $T_a - 2T_j$ and jerk $-J$ for $T_j$. It ends at the peak velocity $v_p$ and covers $v_p T_a / 2$. The cruise lasts $T_v$, and $T = 2T_a + T_v$.

```pseudo id=main
DOUBLE-S(D, V, A, J)                         ▷ D, V, A, J > 0
L1  if V·J ≥ A² then Tj ← A/J;  Ta ← Tj + V/A          ▷ A is reached
L2  else Tj ← √(V/J);  Ta ← 2 Tj                         ▷ A is not reached
L3  if V·Ta ≤ D then                                      ▷ V is reached
L4      Tv ← D/V - Ta;  vp ← V
    else
L5      Tv ← 0
L6      if D·J² ≥ 2A³ then Tj ← A/J;  vp ← (-A²/J + √(A⁴/J² + 4AD))/2;  Ta ← vp/A + Tj
L7      else vp ← (D² J / 4)^(1/3);  Tj ← √(vp/J);  Ta ← 2 Tj
L8  return (Tj, Ta, Tv, vp, 2 Ta + Tv)

SAMPLE(pieces, t)                            ▷ pieces = the seven (duration, jerk) pairs
L9  for each piece (d, j): if t is inside it, integrate (s, v, a) over the rest of t exactly and return
L10     else integrate (s, v, a) over the whole piece: s += v d + a d²/2 + j d³/6, v += a d + j d²/2, a += j d
```

Lines L1 and L2 build the fastest acceleration phase that reaches $V$: if $V$ is large compared with $A^2/J$, the acceleration ramps up to $A$, holds it and ramps down; if not, it ramps up and immediately down, and peaks at $\sqrt{VJ} < A$. Line L3 checks whether the two phases fit into $D$. If they do, line L4 fills the rest with a cruise at $V$. If not, lines L6 and L7 find the peak velocity $v_p < V$ for which the two phases cover exactly $D$; line L6 is the case where the acceleration still reaches $A$ (a quadratic in $v_p$), line L7 the case where it does not (a cubic). Lines L9 and L10 integrate the piecewise constant jerk exactly, so sampling has no integration error.

## Example

**All limits reached.** $D = 1$ m, $V = 1$ m/s, $A = 2$ m/s², $J = 8$ m/s³. Line L1: $VJ = 8 \ge 4$, so $T_j = 0.25$ s and $T_a = 0.75$ s. Line L3: $V T_a = 0.75 \le 1$, so line L4 gives $T_v = 0.25$ s and $T = 1.75$ s. The seven pieces last $0.25$, $0.25$, $0.25$, $0.25$, $0.25$, $0.25$, $0.25$ s. The trapezoid with the same $V$ and $A$ takes $1.5$ s; the difference is $A/J = 0.25$ s.

**Shorter moves.** With the same limits:

| $D$ (m) | case | $T_j$ (s) | $T_a$ (s) | $v_p$ (m/s) | $T$ (s) | trapezoid $T$ (s) |
|---|---|---|---|---|---|---|
| 1 | L1, L4 | 0.25 | 0.75 | 1 | 1.75 | 1.5 |
| 0.3 | L1, L6 | 0.25 | 0.53197 | 0.56394 | 1.06394 | 0.77460 |
| 0.2 | L1, L7 | 0.23208 | 0.46416 | 0.43089 | 0.92832 | 0.63246 |

For $D = 0.2$ the acceleration peaks at $\sqrt{v_p J} \approx 1.857 < A$, and the double S is $0.296$ s slower than the triangle profile, more than $A/J$.

**Low speed limit.** $D = 1$, $V = 0.25$, $A = 2$, $J = 8$. Line L2: $VJ = 2 < 4$, so $T_j = 0.17678$ s and $T_a = 0.35355$ s, and the acceleration peaks at $\sqrt{VJ} = 1.414$ m/s². Line L4 gives $T_v = 3.64645$ s and $T = 4.35355$ s, $0.229$ s more than the trapezoid.

**Machine tool numbers.** The example of [feedrate scheduling](/feedrate-scheduling/), $D = 100$ mm, $V = 50$ mm/s, $A = 500$ mm/s², $J = 10^4$ mm/s³, gives $T_j = 0.05$ s, $T_a = 0.15$ s, $T_v = 1.85$ s and $T = 2.15$ s. The code reproduces these values.

## Correctness

Theorem: the returned times give a profile that is admissible and covers exactly $D$. The proof first computes one acceleration phase: started at rest, it ends at the velocity $J T_j (T_a - T_j)$ and covers half of $v_p T_a$. It then checks that lines L1 and L2 reach exactly $V$ within the limit $A$, that line L4 covers $D$, and, without a cruise, that the distance of two phases is a strictly increasing function $g$ of the peak velocity, so the equation $g(v_p) = D$ has one root. The threshold $2A^3/J^2$ is the value of $g$ where the peak acceleration just reaches $A$, which selects line L6 or line L7. The [proof](proofs/correctness.md) gives every step and shows that sampling is exact.

The rest-to-rest double S is often described as the minimum-time motion under the three limits. This page does not prove that claim.

## Complexity

In the [real RAM](/real-ram/) with square and cube roots, lines L1 to L8 take $\Theta(1)$ time and space. Sampling takes $\Theta(1)$ per sample, since there are seven pieces. Synchronizing $n$ axes to the slowest one, as for the trapezoid, takes $\Theta(n)$ plus the cost of stretching each axis to the common time. That stretching has no simple closed form in general; Biagiotti and Melchiorri scale the limits instead.

## Properties

- **Bounded jerk.** The jerk takes only the values $-J$, $0$ and $+J$. The acceleration is continuous, which the trapezoid does not give.
- **Extra time over the trapezoid.** A theorem: when both $V$ and $A$ are reached, $T = D/V + V/A + A/J$, exactly $A/J$ more than the trapezoid. In the case $VJ < A^2$ with a cruise, the extra time is at most $A/J$. Without a cruise it can be larger, as the example with $D = 0.2$ shows.
- **Seven segments at most.** Pieces of zero duration appear when $A$, $V$ or both are not reached, so a profile can have three, five or seven pieces of nonzero length.
- **Symmetric.** The rest-to-rest profile with equal limits for speeding up and slowing down is symmetric in time.
- **Exact sampling.** The position is a piecewise cubic in time, so exact integration of the pieces gives exact samples.

## Variants and improvements

- **Nonzero end velocities.** Biagiotti and Melchiorri (Section 3.4) handle given start and end velocities, with checks for feasibility.
- **Online computation.** Starting from an arbitrary state with nonzero acceleration, the minimum-time jerk-limited motion needs many more cases; Kroger and Wahl solve it with decision trees (their Type IV). See [online trajectory generation](/online-trajectory-generation/).
- **Fifteen segments.** A bound on the snap, the derivative of the jerk, gives a profile of up to fifteen pieces (Biagiotti and Melchiorri, Section 3.5).
- **Smooth polynomial laws.** A [quintic](/quintic-polynomial-trajectory/) or [minimum-jerk](/minimum-jerk-trajectory/) profile is also smooth, but it reaches its limits only at single instants, so it is slower for the same limits.
- **Along a path.** [Feedrate scheduling](/feedrate-scheduling/) applies the double S to the arc length of a tool path, with extra limits from the curvature.

## When to use it

Use the double S when the jumps of the acceleration of the trapezoid cause vibration, noise or wear: CNC machining, pick and place at high speed, precise positioning stages, elevators and any servo drive that offers an "S-curve" setting. It costs a few percent more time on long moves. Use the plain trapezoid if the drive is stiff and the cycle time matters most, and online trajectory generation if the target can change during the motion.

## Pitfalls

- **Missing cases.** There are four cases (with or without $A$, with or without cruise), and code that only handles the case where everything is reached gives wrong times for short moves.
- **Wrong case test.** The test of line L6 uses $D$ and only applies without a cruise; deciding from $VJ$ alone is wrong for short moves.
- **Cube roots.** Line L7 needs a real cube root of a positive number; in floating point, use a function that is accurate there, and check the result by the distance formula, as the tests do.
- **Rounding near switch times.** Accumulated sums of piece durations differ from $T$ by rounding; clamp the final sample to $(D, 0, 0)$.
- **Jerk limit too low.** If $J$ is very small, the profile spends most of its time ramping the acceleration, and it can be much slower than the trapezoid.

## Implementations

## History

Profiles with bounded jerk replaced the trapezoid in motion controllers when machines became faster and lighter and vibration started to limit their accuracy. Biagiotti and Melchiorri (2008) give the double S in a general form, with nonzero end velocities, the rest-to-rest case and an online version. Kroger and Wahl (2010) made the jerk-limited case work from arbitrary current states for several synchronized axes, the basis of online trajectory generation.

## References
