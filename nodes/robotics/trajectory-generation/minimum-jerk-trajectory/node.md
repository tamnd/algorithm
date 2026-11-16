---
tag: V2PYYM
kind: algorithm
slug: minimum-jerk-trajectory
name: Minimum-jerk trajectory
aliases:
- Flash-Hogan minimum jerk model
area: robotics/trajectory-generation
level: core
summary: "The motion that minimizes the integral of squared jerk; for a rest-to-rest move it is a quintic, which Flash and Hogan fitted to measured human reaching."
solves: [trajectory-generation-problem]
model: real-ram
complexity:
  vars: {d: "the number of coordinates"}
  time: {worst: Θ(d)}
  space: {extra: Θ(d)}
properties: {deterministic: true, randomized: false, online: false, exact: true}
history:
  year: 1985
  people: [Tamar Flash, Neville Hogan]
  note: "Hogan proposed the jerk criterion for single-joint arm movements in 1984. Flash and Hogan extended it to planar reaching in 1985 and compared the predicted paths and speed profiles with measured movements."
prereqs: [quintic-polynomial-trajectory]
see_also: [quintic-polynomial-trajectory, minimum-snap-trajectory, cubic-polynomial-trajectory, euler-lagrange-equation, cam-follower-motion-laws, double-s-velocity-profile, dynamic-movement-primitives, trajectory-optimization]
sources:
  - paper: doi:10.1523/JNEUROSCI.05-07-01688.1985
    title: "Tamar Flash and Neville Hogan, The coordination of arm movements, an experimentally confirmed mathematical model, Journal of Neuroscience 5(7), 1985, 1688-1703"
    locator: "the minimum-jerk cost, its fifth-order polynomial solution for a rest-to-rest move, and the comparison with measured planar arm movements"
  - paper: doi:10.1523/JNEUROSCI.04-11-02745.1984
    title: "Neville Hogan, An organizing principle for a class of voluntary movements, Journal of Neuroscience 4(11), 1984, 2745-2754"
    locator: the jerk criterion for single-joint movements
  - book: isbn:9783540856283
    title: "Luigi Biagiotti and Claudio Melchiorri, Trajectory Planning for Automatic Machines and Robots, Springer, 2008"
    locator: "Chapter 2 (polynomial trajectories)"
---

A minimum-jerk trajectory is the motion from a start state to an end state in a fixed time $T$ that makes the integral of the squared jerk as small as possible. Jerk is the third derivative of the position, the rate at which the acceleration changes, and a motion with little jerk looks smooth and puts little strain on a machine. The answer is a polynomial of degree 5 in time in each coordinate. For a move from rest to rest it is $x(t) = x_0 + (x_f - x_0)(10\tau^3 - 15\tau^4 + 6\tau^5)$ with $\tau = t/T$, so the path is a straight segment and the speed has a bell shape. Flash and Hogan (1985) proposed this cost as a model of human arm movement, and the model fitted their measurements of planar reaching well. That is a measured fit, not a theorem about the brain. In robotics the same formula is used to make robot motion look natural and to give a smooth default for point-to-point moves. It is the [quintic polynomial trajectory](/quintic-polynomial-trajectory/) with a reason attached, and in cam design it is the 3-4-5 polynomial law of the [cam follower motion laws](/cam-follower-motion-laws/).

## In plain words

When you reach for a cup, your hand travels in a nearly straight line, speeds up smoothly, and slows down smoothly, with the top speed near the middle. Researchers asked what rule could produce that. One answer: the hand moves so that its acceleration changes as little and as gently as possible over the whole move. Make that idea exact, and a short calculation gives a single formula, a curve of degree five in time. The formula needs only the start point, the end point and the duration. Robots use it for the same reason people seem to: it is smooth, it is cheap to compute, and it looks natural.

## The problem

Input: a start point $x_0$ and an end point $x_f$ in $\mathbb R^d$, and a duration $T > 0$; more generally, a start state and an end state of position, velocity and acceleration in each coordinate. Output: the motion $x(t)$ on $[0, T]$ with the given end states that minimizes

$$J(x) = \int_0^T \|\dddot x(t)\|^2\, dt.$$

The end conditions fix the position, the velocity and the acceleration at both ends, six numbers per coordinate. The cost and the conditions do not couple the coordinates, so each coordinate is its own problem.

## The algorithm

```pseudo id=main
MIN-JERK(x0, xf, T, t)                        ▷ rest to rest, x0, xf in R^d
L1  τ ← t / T
L2  s ← τ³ (10 - 15τ + 6τ²)
L3  ṡ ← 30 τ² (1 - τ)² / T
L4  s̈ ← 60 τ (1 - τ)(1 - 2τ) / T²
L5  return (x0 + s (xf - x0), ṡ (xf - x0), s̈ (xf - x0))

MIN-JERK-BOUNDARY(p0, v0, c0, p1, v1, c1, T)  ▷ one coordinate, general end states
L6  return the quintic with these six end values (lines L1 to L5 of QUINTIC)
```

Lines L1 to L4 compute the normalized profile $s(\tau)$ and its time derivatives. Line L5 scales it by the displacement in every coordinate, so all coordinates arrive together along a straight line. Line L6 is the general case; its coefficients are the closed forms of the [quintic polynomial trajectory](/quintic-polynomial-trajectory/).

## Example

A hand moves from $x_0 = (0, 0)$ m to $x_f = (0.3, 0.4)$ m in $T = 1$ s, a distance $D = 0.5$ m.

- At $t = 0.25$ s: $\tau = 0.25$ and $s = 0.015625 \cdot 6.625 \approx 0.1035$, so the hand is at $(0.0311, 0.0414)$ m, about a tenth of the way.
- At $t = 0.5$ s: $s = 0.5$, the hand is half way, and the speed is at its peak $1.875 \cdot 0.5 = 0.9375$ m/s.
- The acceleration peaks at $\tau = (3 - \sqrt 3)/6 \approx 0.211$ with $(10/\sqrt 3) \cdot 0.5 \approx 2.887$ m/s², and the jerk is $60 \cdot 0.5 = 30$ m/s³ at both ends.
- The cost is $720 D^2 / T^5 = 180$ m²/s⁵.

The bell-shaped speed $30\tau^2(1 - \tau)^2$ is symmetric about the middle and starts and ends with zero slope, because the acceleration is zero at both ends.

## Correctness

Theorem: for its six end conditions, the quintic of line L6 is the unique minimizer of $J$ among all motions with square-integrable jerk. The [proof](proofs/correctness.md) writes any competitor as $x^* + \eta$, where $\eta$ and its first two derivatives vanish at both ends. Three integrations by parts show that the cross term $\int x^{*\prime\prime\prime} \eta'''$ is zero, because the sixth derivative of a quintic is zero. So $J(x^* + \eta) = J(x^*) + J(\eta)$, and $J(\eta) > 0$ unless $\eta = 0$. This is the [Euler-Lagrange equation](/euler-lagrange-equation/) $x^{(6)} = 0$ of the cost, and the identity shows directly that its solution is the minimum. The proof also computes the cost $720 D^2 / T^5$ of the rest-to-rest move.

## Complexity

In the [real RAM](/real-ram/), one sample of a rest-to-rest move in $d$ coordinates costs $\Theta(d)$ operations, and line L6 costs $\Theta(1)$ per coordinate. No optimization is run: the calculus of variations has solved the problem once, in closed form.

## Properties

- **Straight line, bell-shaped speed.** For a rest-to-rest move, the path is the segment from $x_0$ to $x_f$, and the speed is $\frac{D}{T} 30\tau^2(1 - \tau)^2$, with peak $1.875\, D/T$ at the middle (theorems).
- **Cost.** $J = 720 D^2 / T^5$ for a rest-to-rest move of length $D$: halving the time multiplies the cost by 32.
- **Fit to human reaching.** Flash and Hogan reported that the model predicts the straight paths and the bell-shaped speed profiles of their subjects' planar reaching movements. This is a measurement on their data, and other costs have been proposed for movements that it fits less well.
- **Kinematic only.** The model uses no masses, torques or motor limits. It does not guarantee that a robot can follow it.
- **Duration is an input.** The cost decreases without bound as $T$ grows, so the model cannot choose $T$.

## Variants and improvements

- **Via points.** Flash and Hogan also treated movements through a via point. The optimum is then a piecewise polynomial of degree 5, and the time at the via point is part of the optimization.
- **Minimum snap.** Replace the third derivative by the fourth. For a quadrotor the snap is linked to the motor inputs, which gives the [minimum-snap trajectory](/minimum-snap-trajectory/).
- **Minimum acceleration.** Replace it by the second derivative: the [cubic](/cubic-polynomial-trajectory/) is the minimizer for its four end conditions.
- **Limits.** If velocity, acceleration and jerk limits must be met in minimum time, use the [double-S velocity profile](/double-s-velocity-profile/) instead.
- **Learning motions.** [Dynamic movement primitives](/dynamic-movement-primitives/) are often tested on minimum-jerk demonstrations; they reproduce a motion and adapt it to new goals.
- **General costs.** [Trajectory optimization](/trajectory-optimization/) minimizes any cost with any dynamics and limits numerically.

## When to use it

Use the minimum-jerk formula for smooth point-to-point motions of a robot arm or hand where the duration is given and the limits are loose: service and social robots, robots that move near people, and animation. Use it as a model or a baseline in studies of human movement. Use the double S or a time-optimal method if the motion must be as fast as possible under limits.

## Pitfalls

- **Comparing costs with different end conditions.** A [cubic](/cubic-polynomial-trajectory/) rest-to-rest move has the constant jerk $12D/T^3$ inside $(0, T)$, so its integral is $144 D^2/T^5$, smaller than $720 D^2/T^5$. That does not beat the theorem: the cubic does not meet the zero end accelerations, and its acceleration jumps at the ends, so its jerk there is unbounded.
- **Assuming it is time-optimal.** It is not. With the same peak velocity, a trapezoid or a double S is faster.
- **Applying it in joint space and expecting a straight hand path.** The straight-line result holds in the space where the cost is computed. In joint space, the hand path of an arm is curved.
- **Treating the human fit as a law.** The fit is a measurement on a class of movements, not a principle that holds for every task.

## Implementations

## History

Hogan (1984) proposed that single-joint arm movements minimize the integrated squared jerk. Flash and Hogan (1985) extended the model to planar multi-joint reaching, solved it in closed form, and compared the predicted paths and speed profiles with measured movements, including movements through a via point. The model became a standard reference in motor control and a common way to generate human-like robot motion. In cam design, the same polynomial was already in use as the 3-4-5 law.

## References
