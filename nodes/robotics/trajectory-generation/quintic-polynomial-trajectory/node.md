---
tag: JZFXGC
kind: algorithm
slug: quintic-polynomial-trajectory
name: Quintic polynomial trajectory
aliases:
- fifth-order polynomial time scaling
area: robotics/trajectory-generation
level: intro
summary: "Fits a quintic in time to given positions, velocities and accelerations at both ends, so acceleration is continuous."
solves: [trajectory-generation-problem]
model: real-ram
complexity:
  vars: {n: "the number of joints", m: "the number of segments between via points"}
  time: {worst: Θ(n m)}
  space: {extra: Θ(n m)}
properties: {deterministic: true, randomized: false, online: false, exact: true}
history:
  year: 1985
  people: [Tamar Flash, Neville Hogan]
  note: "Flash and Hogan showed that the rest-to-rest quintic is the motion of least integrated squared jerk and compared it with measured human arm movements. The quintic itself was already a standard tool for joint trajectories."
prereqs: [cubic-polynomial-trajectory]
see_also: [minimum-jerk-trajectory, cubic-polynomial-trajectory, double-s-velocity-profile, cam-follower-motion-laws, hermite-interpolation, time-scaling, trajectory-generation-problem, minimum-snap-trajectory]
sources:
  - book: isbn:9781107156302
    title: "Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017"
    locator: "Chapter 9, Section 9.2.2 (time scaling a straight-line path)"
  - book: isbn:9783540856283
    title: "Luigi Biagiotti and Claudio Melchiorri, Trajectory Planning for Automatic Machines and Robots, Springer, 2008"
    locator: "Chapter 2 (analytic expressions of elementary trajectories, polynomial trajectories)"
  - paper: doi:10.1523/JNEUROSCI.05-07-01688.1985
    title: "Tamar Flash and Neville Hogan, The coordination of arm movements, an experimentally confirmed mathematical model, Journal of Neuroscience 5(7), 1985, 1688-1703"
    locator: "the whole paper (the minimum-jerk model and its fifth-order polynomial solution)"
---

A quintic polynomial trajectory moves one coordinate, such as a robot joint angle, from a start state to an end state in a given time $T$ along a polynomial of degree 5 in time. A state here is a position, a velocity and an acceleration, so there are six end conditions, and a quintic has exactly six coefficients. This is the [cubic polynomial trajectory](/cubic-polynomial-trajectory/) with two more conditions: because the end accelerations can be set, the motion can start and stop with zero acceleration, and the acceleration is continuous when several moves are joined. The jerk, the derivative of the acceleration, is then finite everywhere. The rest-to-rest quintic $10\tau^3 - 15\tau^4 + 6\tau^5$ is also the [minimum-jerk trajectory](/minimum-jerk-trajectory/), and in cam design it is the 3-4-5 polynomial law of the [cam follower motion laws](/cam-follower-motion-laws/).

## In plain words

A cubic move sets where to start and end and how fast, but the push of the motor still jumps at the start and at the end. That jump shakes a robot arm and the load it carries. A quintic adds two more numbers to the curve, so it can also say how hard to push at both ends. Set those to zero and the motor starts pushing gently, pushes harder, then eases off, and the arm arrives with no push left. Six wishes, six numbers, so again there is exactly one curve and a short formula for it. The price is a higher peak speed than the cubic for the same move and time.

## The problem

Input: a start state $(q_0, v_0, c_0)$ and an end state $(q_1, v_1, c_1)$ of position, velocity and acceleration, and a duration $T > 0$. Output: the coefficients $a_0, \dots, a_5$ of

$$q(t) = \sum_{k=0}^{5} a_k t^k, \qquad 0 \le t \le T,$$

with $q(0) = q_0$, $q'(0) = v_0$, $q''(0) = c_0$, $q(T) = q_1$, $q'(T) = v_1$ and $q''(T) = c_1$. For an arm with $n$ joints, each joint gets its own quintic with the same $T$. With $q_0 = 0$, $q_1 = 1$ and all other end values zero, the result is a [time scaling](/time-scaling/) $s(t)$ for a move along a fixed path.

## The algorithm

Let $h = q_1 - q_0$.

```pseudo id=main
QUINTIC(q0, v0, c0, q1, v1, c1, T)          ▷ T > 0, h = q1 - q0
L1  a0 ← q0;  a1 ← v0;  a2 ← c0 / 2
L2  a3 ← (20h - (8 v1 + 12 v0) T - (3 c0 - c1) T²) / (2T³)
L3  a4 ← (-30h + (14 v1 + 16 v0) T + (3 c0 - 2 c1) T²) / (2T⁴)
L4  a5 ← (12h - 6 (v1 + v0) T + (c1 - c0) T²) / (2T⁵)
L5  return (a0, ..., a5)

QUINTIC-EVAL(a, t, k)
L6  for each derivative order 0, 1, ..., k, evaluate it by Horner's rule

REST-TO-REST(q0, q1, T, t)
L7  τ ← t / T;  return q0 + (q1 - q0)(10τ³ - 15τ⁴ + 6τ⁵)
```

Line L1 reads the start state off the polynomial at $t = 0$. Lines L2 to L4 are the solution of the remaining $3 \times 3$ linear system for the end state at $t = T$, written out in closed form. Line L7 is the special case with zero end velocities and accelerations.

## Example

**The rest-to-rest profile.** With $T = 1$ and a unit move, lines L2 to L4 give $a_3 = 10$, $a_4 = -15$, $a_5 = 6$:

$$s(\tau) = 10\tau^3 - 15\tau^4 + 6\tau^5, \qquad s'(\tau) = 30\tau^2(1 - \tau)^2, \qquad s''(\tau) = 60\tau(1 - \tau)(1 - 2\tau).$$

The peak velocity is $s'(1/2) = 15/8 = 1.875$. The peak acceleration is $10/\sqrt 3 \approx 5.774$ at $\tau = (3 - \sqrt 3)/6 \approx 0.2113$. The jerk is $60$ at both ends. Compare the cubic $3\tau^2 - 2\tau^3$: its peak velocity is $1.5$ and its acceleration is $6$ at the ends, so the quintic is faster in the middle but starts with zero acceleration.

**Nonzero start velocity.** Take $q_0 = 0$ m, $v_0 = 1$ m/s, $q_1 = 2$ m, the other end values zero, and $T = 2$ s, so $h = 2$.

- L1: $a_0 = 0$, $a_1 = 1$, $a_2 = 0$.
- L2: $a_3 = (40 - 12 \cdot 2)/16 = 1$.
- L3: $a_4 = (-60 + 16 \cdot 2)/32 = -7/8$.
- L4: $a_5 = (24 - 6 \cdot 2)/64 = 3/16$.

So $q(t) = t + t^3 - \tfrac78 t^4 + \tfrac{3}{16} t^5$. Check: $q(2) = 2 + 8 - 14 + 6 = 2$. The acceleration $q''(t) = 6t - \tfrac{21}{2}t^2 + \tfrac{15}{4}t^3 = \tfrac{3}{4} t (5t - 4)(t - 2)$ is zero at both ends, as required, and also at $t = 0.8$ s, where the velocity has its peak $1.512$ m/s. The cubic with the same positions and velocities has the acceleration $1$ m/s² at the start and $-2$ m/s² at the end.

## Correctness

Putting $t = 0$ and $t = T$ into $q$, $q'$ and $q''$ with the coefficients of lines L1 to L4 gives back the six end conditions, which is a direct check. No other polynomial of degree at most 5 meets them: the difference of two would have triple roots at $0$ and $T$, so $t^3 (t - T)^3$, of degree 6, would divide it, and it would be zero. The [proof](proofs/correctness.md) gives the coefficient check and derives the values of the rest-to-rest example. The same uniqueness argument with the cost $\int q'''^2$ shows that the quintic is the motion of least integrated squared jerk for its six end conditions; that is the theorem of the [minimum-jerk trajectory](/minimum-jerk-trajectory/) page.

## Complexity

In the [real RAM](/real-ram/), one call of QUINTIC costs a fixed number of operations, about 40, so $\Theta(1)$ time and space. Evaluating all derivatives up to order 3 costs about 20 multiplications. An arm with $n$ joints and $m$ segments needs $\Theta(nm)$ time and stores $6nm$ coefficients.

## Properties

- **Acceleration continuous.** Joined quintics are $C^2$ at via points when each via point gets one velocity and one acceleration. The jerk is finite but jumps, from 0 to 60 $D/T^3$ at the start of a rest-to-rest move.
- **Minimum integrated squared jerk.** A theorem (Flash and Hogan 1985): for its six end conditions, the quintic is the unique minimizer of $\int q'''^2$.
- **Peaks of the rest-to-rest move.** For a distance $D$ in time $T$: velocity $1.875\, D/T$, acceleration $5.774\, D/T^2$, jerk $60\, D/T^3$. These are exact values (theorems), from the example.
- **Linear in the data.** For a fixed $T$, the coefficients are linear in the six end values.
- **Overshoot.** Large end velocities or accelerations compared with $h/T$ make the motion leave the interval between $q_0$ and $q_1$.

## Variants and improvements

- **Higher degree.** A polynomial of degree 7 also sets the end jerks; it is the single-segment [minimum-snap trajectory](/minimum-snap-trajectory/). Each step up raises the peak velocity: $1.5$, $1.875$ and $35/16 = 2.1875$ times $D/T$ for degrees 3, 5 and 7.
- **Via points.** One quintic per segment with given velocities and accelerations at the via points. Choosing them to minimize a cost over all segments gives smoothing splines such as the minimum-snap method.
- **Jerk-limited profiles.** If the move must be as fast as possible under limits on the velocity, the acceleration and the jerk, the [double-S velocity profile](/double-s-velocity-profile/) is faster, because it can spend most of the time at the limits.
- **Choosing T.** For a rest-to-rest move under $|q'| \le V$ and $|q''| \le A$, the smallest feasible time is $T = \max(1.875\, D/V, \sqrt{5.774\, D/A})$.

## When to use it

Use a quintic for point-to-point moves of a joint or as the time scaling of a path when the acceleration must be continuous, for example with an elastic arm, a heavy load, or liquid in a container. It is also the standard model of a human-like reaching motion, and a common choice for a short motion primitive that must join another motion at a given state. If the motion must be as fast as possible under fixed limits, use a [trapezoidal](/trapezoidal-velocity-profile/) or a double-S profile instead; a quintic reaches its limits only at one instant.

## Pitfalls

- **Same T for all joints.** If each joint gets its own duration, the joints do not arrive together, and the path is not the intended one.
- **Check the limits after choosing T.** The formulas accept any $T > 0$; the peaks grow as $1/T$, $1/T^2$ and $1/T^3$.
- **Typing the closed form.** The coefficients of lines L2 to L4 are easy to mistype. Test them with exact fractions against the six end conditions, as the tests of this page do.
- **Local time.** Each segment uses its own local time $t - t_i$; evaluate it there.
- **Floating point for small T.** The divisions by $T^5$ amplify rounding when $T$ is small and the end values are large. Scale time to $\tau = t/T$ in that case.

## Implementations

## History

Polynomials in time were the standard way to plan joint trajectories in the first robot controllers, and the quintic was used where the cubic gave unacceptable acceleration jumps; its first use is not traced here. Flash and Hogan (1985) proposed that human arm movements minimize the integrated squared jerk, showed that for a rest-to-rest move the optimum is the quintic $10\tau^3 - 15\tau^4 + 6\tau^5$, and compared it with measured planar arm movements. Lynch and Park (2017) present the quintic as the fifth-order polynomial time scaling.

## References
