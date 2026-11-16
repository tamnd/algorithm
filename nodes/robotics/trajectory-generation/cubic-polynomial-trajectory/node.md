---
tag: HEFVQT
kind: algorithm
slug: cubic-polynomial-trajectory
name: Cubic polynomial trajectory
aliases:
- third-order polynomial time scaling
area: robotics/trajectory-generation
level: intro
summary: "Fits a cubic in time to given start and end positions and velocities, the simplest smooth point-to-point motion."
solves: [trajectory-generation-problem]
model: real-ram
complexity:
  vars: {n: "the number of joints", m: "the number of segments between via points"}
  time: {worst: Θ(n m)}
  space: {extra: Θ(n m)}
properties: {deterministic: true, randomized: false, online: false, exact: true}
history:
  year: 1983
  people: [Chun-Shin Lin, Po-Rong Chang, J. Y. S. Luh]
  note: "Lin, Chang and Luh built joint trajectories of industrial robots from cubic polynomials between knots and scheduled the knot times to minimize the travel time under velocity, acceleration and jerk limits."
prereqs: [time-scaling, polynomial-interpolation]
see_also: [quintic-polynomial-trajectory, trapezoidal-velocity-profile, minimum-jerk-trajectory, cubic-hermite-spline, cubic-spline-interpolation, hermite-interpolation, cam-follower-motion-laws, trajectory-generation-problem]
sources:
  - book: isbn:9781107156302
    title: "Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017"
    locator: "Chapter 9, Section 9.2.2 (time scaling a straight-line path) and Section 9.3 (polynomial via point trajectories)"
  - book: isbn:9783540856283
    title: "Luigi Biagiotti and Claudio Melchiorri, Trajectory Planning for Automatic Machines and Robots, Springer, 2008"
    locator: "Chapter 2 (analytic expressions of elementary trajectories, polynomial trajectories)"
  - book: isbn:9781846286414
    title: "Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009"
    locator: "the chapter on trajectory planning (joint space trajectories, point-to-point motion)"
  - paper: doi:10.1109/TAC.1983.1103181
    title: "Chun-Shin Lin, Po-Rong Chang and J. Y. S. Luh, Formulation and optimization of cubic polynomial joint trajectories for industrial robots, IEEE Transactions on Automatic Control 28(12), 1983, 1066-1074"
    locator: "the whole paper (cubic splines through joint knots, and the choice of the knot times)"
---

A cubic polynomial trajectory moves one coordinate, such as a robot joint angle or one axis of a machine, from a start position to an end position in a given time $T$ along a polynomial of degree 3 in time. A cubic has four coefficients, and the four conditions are the position and the velocity at both ends. So the start and the end velocities can be set, for example to zero for a move from rest to rest, and the velocity is continuous when several moves are joined. The acceleration is not controlled: it is generally not zero at the ends, so it jumps when the motion starts and stops. The [quintic polynomial trajectory](/quintic-polynomial-trajectory/) adds the two end accelerations for this reason. The cubic is also the [time scaling](/time-scaling/) $s(t)$ that is most often used to run along a fixed path, and among all motions with the same four end conditions it is the one with the least integral of squared acceleration.

## In plain words

Suppose a joint is at 0 degrees and must be at 90 degrees two seconds later, and it must be at rest at both moments. A straight line in time would start and stop with a sudden jump in speed, which no motor can do. A cubic curve starts flat, rises, and ends flat. Its slope, the speed, starts at zero, grows to a peak in the middle, and falls to zero at the end. Four numbers describe the curve, and there are four wishes: where to start, how fast to start, where to end and how fast to end. So there is exactly one cubic that meets all four, and a short formula gives it. The price is that the push from the motor jumps from zero to a fixed value at the start, because the method has no number left to control it.

## The problem

Input: a start position $q_0$ and velocity $v_0$, an end position $q_1$ and velocity $v_1$, and a duration $T > 0$. Output: the coefficients $a_0, \dots, a_3$ of

$$q(t) = a_0 + a_1 t + a_2 t^2 + a_3 t^3, \qquad 0 \le t \le T,$$

with $q(0) = q_0$, $q'(0) = v_0$, $q(T) = q_1$ and $q'(T) = v_1$. For an arm with $n$ joints, each joint gets its own cubic with the same $T$. For a move along a fixed path, the same formula with $q_0 = 0$, $q_1 = 1$ and zero end velocities gives a time scaling $s(t)$, and the motion is $\theta(t) = \theta_{\text{start}} + s(t)(\theta_{\text{end}} - \theta_{\text{start}})$ (Lynch and Park, Section 9.2.2).

## The algorithm

Let $h = q_1 - q_0$.

```pseudo id=main
CUBIC(q0, v0, q1, v1, T)                    ▷ T > 0, h = q1 - q0
L1  a0 ← q0
L2  a1 ← v0
L3  a2 ← (3h - (2 v0 + v1) T) / T²
L4  a3 ← (-2h + (v0 + v1) T) / T³
L5  return (a0, a1, a2, a3)

CUBIC-EVAL(a, t)
L6  q ← a0 + t (a1 + t (a2 + t a3))          ▷ Horner's rule
L7  q' ← a1 + t (2 a2 + 3 a3 t)
L8  q'' ← 2 a2 + 6 a3 t
L9  return (q, q', q'')
```

Lines L1 and L2 read the start conditions off the polynomial at $t = 0$. Lines L3 and L4 solve the two remaining equations $a_2 T^2 + a_3 T^3 = h - v_0 T$ and $2a_2 T + 3a_3 T^2 = v_1 - v_0$, a $2 \times 2$ linear system. Lines L6 to L8 evaluate the position, the velocity and the acceleration.

For via points $q_0, \dots, q_m$ at times $t_0 < \dots < t_m$ with chosen velocities $v_0, \dots, v_m$, call CUBIC once per interval with $T = t_{i+1} - t_i$, in local time $t - t_i$ (Lynch and Park, Section 9.3). The velocities at the inner via points are a design choice: a common rule of thumb takes the mean of the slopes of the two neighboring intervals, or zero where the slope changes sign.

## Example

**The standard time scaling.** With $q_0 = 0$, $q_1 = 1$, $v_0 = v_1 = 0$ and $T = 1$, lines L3 and L4 give $a_2 = 3$ and $a_3 = -2$:

$$s(t) = 3t^2 - 2t^3, \qquad s'(t) = 6t - 6t^2, \qquad s''(t) = 6 - 12t.$$

The peak velocity is $s'(1/2) = 1.5$, at the middle, and the acceleration is $6$ at $t = 0$ and $-6$ at $t = 1$. For a distance $D$ and a time $T$, these become $1.5 D/T$ and $6 D/T^2$. A joint that turns $D = \pi/2$ rad in $T = 2$ s reaches $1.18$ rad/s at $t = 1$ s, and needs $2.36$ rad/s² at the start and the end.

**Nonzero start velocity.** Take $q_0 = 0$ m, $v_0 = 1$ m/s, $q_1 = 2$ m, $v_1 = 0$ and $T = 2$ s, so $h = 2$.

- L3: $a_2 = (6 - (2 + 0) \cdot 2)/4 = 0.5$.
- L4: $a_3 = (-4 + (1 + 0) \cdot 2)/8 = -0.25$.

So $q(t) = t + 0.5t^2 - 0.25t^3$. Check: $q(2) = 2 + 2 - 2 = 2$ and $q'(2) = 1 + 2 - 3 = 0$. The velocity $q'(t) = 1 + t - 0.75t^2$ has its peak $4/3$ m/s at $t = 2/3$ s, where $q = 22/27$ m. The acceleration $q''(t) = 1 - 1.5t$ goes from $1$ m/s² at the start to $-2$ m/s² at the end.

**Via points.** Through $0, 1, 3$ m at $0, 1, 3$ s with velocities $0, 1, 0$ m/s, the first cubic is $2t^2 - t^3$ and the second is $1 + t + 0.5t^2 - 0.25t^3$ in local time. Both have position 1 and velocity 1 at the via point, but the acceleration jumps there from $-2$ to $1$ m/s².

## Correctness

Putting $t = 0$ and $t = T$ into the polynomial and its derivative and using the formulas of lines L3 and L4 gives back the four end conditions. No other polynomial of degree at most 3 meets them: the difference of two would have double roots at $0$ and $T$, so it would be divisible by $t^2 (t - T)^2$, of degree 4, and so zero.

The cubic is also optimal for a natural cost. Among all motions $x$ with the same four end conditions, it minimizes $\int_0^T x''(t)^2\, dt$, and it is the only minimizer. If $x = q + \eta$, two integrations by parts show that the cross term $\int q'' \eta''$ is zero, because $\eta$ and $\eta'$ vanish at the ends and $q'''' = 0$. So the cost of $x$ is the cost of $q$ plus the cost of $\eta$. The [proof](proofs/correctness.md) gives every step. For the rest-to-rest move the minimum is $12 D^2 / T^3$.

## Complexity

In the [real RAM](/real-ram/), one call of CUBIC costs a fixed number of operations, about 15, so $\Theta(1)$ time and space. One evaluation costs about 10 multiplications. An arm with $n$ joints and $m$ segments needs $\Theta(nm)$ time and stores $4nm$ coefficients. This is the cheapest smooth trajectory, which is why controllers that replan every cycle often use it.

## Properties

- **Velocity continuous, acceleration not.** Joined cubics are $C^1$ at via points. The acceleration jumps there, and it jumps from 0 at the start and the end of a rest-to-rest move.
- **Minimum squared acceleration.** A theorem: the cubic is the unique minimizer of $\int x''^2$ for its four end conditions, so it uses the least "effort" in this sense.
- **Symmetric rest-to-rest profile.** For $v_0 = v_1 = 0$, $s(t) = 3\tau^2 - 2\tau^3$ with $\tau = t/T$, and the path rises without overshoot, since $s' \ge 0$.
- **Linear in the data.** The coefficients are linear in $(q_0, v_0, q_1, v_1)$ for a fixed $T$. Scaling the time by $c$ divides the velocity by $c$ and the acceleration by $c^2$.
- **Overshoot with large end velocities.** If $|v_0|$ or $|v_1|$ is large compared with $h/T$, the cubic can leave the interval between $q_0$ and $q_1$.

## Variants and improvements

- **Quintic.** Add the end accelerations as two more conditions: the [quintic polynomial trajectory](/quintic-polynomial-trajectory/). The rest-to-rest quintic is the [minimum-jerk trajectory](/minimum-jerk-trajectory/).
- **Cubic splines.** If only the via positions are given, choose the inner velocities so that the acceleration is also continuous. This gives a tridiagonal system, the [cubic spline](/cubic-spline-interpolation/); Lin, Chang and Luh used it for joint trajectories. With the velocities given, the method on this page is the [cubic Hermite spline](/cubic-hermite-spline/).
- **Linear segments with blends.** For long moves, a constant velocity middle part with short blends is faster under the same limits: the [trapezoidal velocity profile](/trapezoidal-velocity-profile/).
- **Choosing T.** For a rest-to-rest move under the limits $|q'| \le V$ and $|q''| \le A$, the smallest feasible time is $T = \max(1.5 D/V, \sqrt{6 D/A})$, because the peaks are $1.5 D/T$ and $6 D/T^2$.

## When to use it

Use a cubic for short point-to-point moves of a joint where the velocities at the ends matter and the acceleration jump is acceptable, for example in teaching, in simulation, and in simple controllers. Use it as the time scaling $s(t)$ of a straight-line move in task space. If the robot is stiff or the load is heavy, the acceleration jump excites vibration; use a quintic or a [double-S profile](/double-s-velocity-profile/). If the move must be as fast as possible under velocity and acceleration limits, use a [trapezoidal profile](/trapezoidal-velocity-profile/).

## Pitfalls

- **Jerk is infinite at the start and the end.** The acceleration jumps from 0 to $6D/T^2$. Do not use a cubic where a smooth start matters.
- **Different T per joint.** If each joint gets its own duration, the joints do not finish together and the end-effector path is not straight. Use one $T$ for all joints, set by the slowest one.
- **T too small.** The formulas work for any $T > 0$, but the peaks grow as $1/T$ and $1/T^2$. Check the limits after you choose $T$.
- **Wrong via velocities.** Choosing the inner velocities badly makes the motion overshoot between via points.
- **Local time.** Each segment is written in its own local time $t - t_i$. Mixing local and global time gives wrong values at every segment but the first.

## Implementations

## History

Polynomials in time were the standard way to plan joint trajectories in the first robot controllers, and the textbooks of the 1980s present the cubic for point-to-point moves and via points. Lin, Chang and Luh (1983) built joint trajectories from cubic splines through knots and gave an algorithm that chooses the time intervals between knots to minimize the total travel time under limits on the joint velocities, accelerations and jerks. Lynch and Park (2017) present the cubic as the third-order polynomial time scaling and as the building block of polynomial via point trajectories.

## References
