---
tag: 4DQ75R
kind: algorithm
slug: dubins-path
name: Dubins path
aliases:
- Dubins curves
area: robotics/mobile-and-legged-robots
level: core
summary: The shortest path of a forward-only car with bounded curvature, one of six words of arcs and lines, CSC or CCC.
solves: [kinodynamic-planning]
model: real-ram
complexity:
  vars: {w: "the number of candidate words, six"}
  time: {worst: O(1)}
  space: {extra: O(1)}
properties: {deterministic: true, randomized: false, online: false, exact: true}
history:
  year: 1957
  people: [Lester E. Dubins]
  note: Dubins proved in 1957 that a shortest curve of bounded curvature between two points with given directions is made of at most three pieces, each an arc of minimum radius or a line, of type CSC or CCC.
prereqs: [unicycle-model, configuration-space]
see_also: [reeds-shepp-path, hybrid-a-star, state-lattice-planning, kinodynamic-planning, a-star-search, kinematic-bicycle-model, pontryagin-maximum-principle, euclidean-shortest-path]
sources:
  - paper: doi:10.2307/2372560
    title: "Lester E. Dubins, On curves of minimal length with a constraint on average curvature, and with prescribed initial and terminal positions and tangents, American Journal of Mathematics 79(3), 1957"
    locator: pages 497 to 516 (the main theorem, the CSC and CCC types, and the middle arc of a CCC path longer than pi times the radius)
  - paper: doi:10.1016/S0921-8890(00)00127-5
    title: Andrei M. Shkel and Vladimir J. Lumelsky, Classification of the Dubins set, Robotics and Autonomous Systems 34(4), 2001
    locator: pages 179 to 202 (closed forms of the six words after the change of frame, and a rule that picks the shortest word without computing all of them when the poses are far apart)
  - book: isbn:9780521862059
    title: Steven M. LaValle, Planning Algorithms, Cambridge University Press, 2006
    locator: Section 15.3.1 (Dubins curves, the six words and the Dubins car as a control system)
  - paper: doi:10.2140/pjm.1990.145.367
    title: James A. Reeds and Lawrence A. Shepp, Optimal paths for a car that goes both forwards and backwards, Pacific Journal of Mathematics 145(2), 1990
    locator: pages 367 to 393 (the extension with reverse motion, see the Reeds-Shepp path page)
  - paper: doi:10.1007/BF01258291
    title: Jean-Daniel Boissonnat, André Cérézo and Juliette Leblond, Shortest paths of bounded curvature in the plane, Journal of Intelligent and Robotic Systems 11, 1994
    locator: pages 5 to 20 (a proof of the results of Dubins and of Reeds and Shepp with the Pontryagin minimum principle)
---

A Dubins path is a shortest path between two poses of a car that drives only forward and cannot turn tighter than a radius $\rho$. A pose is $(x, y, \theta)$: a position in the plane and a heading. Dubins proved in 1957 that such a shortest path always exists and is made of at most three pieces, each an arc of radius exactly $\rho$ (written L for a left turn and R for a right turn) or a straight segment (S). Only six words can be shortest: LSL, RSR, LSR, RSL, RLR and LRL. The algorithm computes the three segment lengths of each word in closed form and returns the shortest word, in constant time. It is the steering function of many car planners, for example [hybrid A\*](/hybrid-a-star/), and the exact cost-to-go that their heuristics approximate.

## In plain words

A car drives on an empty parking lot and must stop at a given spot, facing a given way. It cannot back up, and the steering wheel has a stop. The shortest way is always simple: turn with the wheel at the stop, drive straight, and turn with the wheel at the stop again. When the target is very close, a straight piece does not help, and the shortest way is three hard turns: one way, the other way, then the first way again.

There are only six such patterns. For each one, a little trigonometry gives the length of the three pieces. You compute all six and take the shortest.

## The problem

**The model.** The car is the [unicycle model](/unicycle-model/) with a forward speed $v = 1$ and a turn rate $|\omega| \le 1/\rho$, so its path has curvature at most $1/\rho$. In the units of the code, $x' = \cos\theta$, $y' = \sin\theta$, $\theta' = u/\rho$ with $u \in [-1, 1]$, and time equals arc length. The same paths serve the rear axle of the [kinematic bicycle model](/kinematic-bicycle-model/) with wheelbase $L$ and steering limit $\delta_{max}$, with $\rho = L / \tan \delta_{max}$. There are no obstacles. Numbers are reals and each arithmetic operation, square root and trigonometric function costs one step, as in the [real RAM](/real-ram/).

**Input.** A start pose $q_0 = (x_0, y_0, \theta_0)$, a goal pose $q_1 = (x_1, y_1, \theta_1)$, both in meters and radians, and the minimum turning radius $\rho > 0$ in meters.

**Output.** A word $w$ from the six and three lengths $(\ell_1, \ell_2, \ell_3)$, all at least 0, such that driving the three segments of $w$ from $q_0$ ends at $q_1$, and $\ell_1 + \ell_2 + \ell_3$ is the least length of any forward path with curvature at most $1/\rho$.

**How it differs from close pages.** The [Reeds-Shepp path](/reeds-shepp-path/) solves the same problem for a car that may also reverse; its shortest path is never longer and has up to five segments. [Kinodynamic planning](/kinodynamic-planning/) is the general problem with obstacles and dynamics, where a Dubins path is only a local connection between two states. The [Euclidean shortest path](/euclidean-shortest-path/) ignores the heading and the curvature. A search such as [A\*](/a-star-search/) or [hybrid A\*](/hybrid-a-star/) handles the obstacles and calls the Dubins solver as a heuristic or as a final shot to the goal.

## The algorithm

Move to a frame where the start is at the origin and the goal lies on the positive $x$ axis, and scale all lengths by $1/\rho$. Then the problem has three numbers: the scaled distance $d$, the start heading $\alpha$ and the goal heading $\beta$, both measured from the line from start to goal. Write $t$, $p$, $q$ for the three scaled segment lengths. An arc of scaled length $t$ turns the heading by $t$ radians. All angles are taken modulo $2\pi$ into $[0, 2\pi)$, written $\mathrm{mod}_{2\pi}$.

```pseudo id=main
DUBINS(q0, q1, ρ)
L1  d ← |p1 - p0| / ρ; φ ← the direction of p1 - p0
L2  α ← mod2π(θ0 - φ); β ← mod2π(θ1 - φ)
L3  best ← none
L4  for each word w in LSL, RSR, LSR, RSL, RLR, LRL do
L5      if the closed form of w gives (t, p, q) for (d, α, β) then ℓ ← ρ (t + p + q)
L6          if best is none or ℓ < the length of best then best ← (w, ρ t, ρ p, ρ q)
L7  return best
```

Line L5 uses the closed forms below, with $s_\alpha = \sin\alpha$, $c_\alpha = \cos\alpha$ and the same for $\beta$. A word does not exist when its $p^2$ is negative or its $|c|$ is above 1.

| Word | Condition | $p$ | $t$ and $q$ |
|---|---|---|---|
| LSL | $p^2 = 2 + d^2 - 2\cos(\alpha - \beta) + 2d(s_\alpha - s_\beta) \ge 0$ | $\sqrt{p^2}$ | $\gamma = \mathrm{atan2}(c_\beta - c_\alpha, d + s_\alpha - s_\beta)$, $t = \gamma - \alpha$, $q = \beta - \gamma$ |
| RSR | $p^2 = 2 + d^2 - 2\cos(\alpha - \beta) + 2d(s_\beta - s_\alpha) \ge 0$ | $\sqrt{p^2}$ | $\gamma = \mathrm{atan2}(c_\alpha - c_\beta, d - s_\alpha + s_\beta)$, $t = \alpha - \gamma$, $q = \gamma - \beta$ |
| LSR | $p^2 = -2 + d^2 + 2\cos(\alpha - \beta) + 2d(s_\alpha + s_\beta) \ge 0$ | $\sqrt{p^2}$ | $\gamma = \mathrm{atan2}(-c_\alpha - c_\beta, d + s_\alpha + s_\beta) - \mathrm{atan2}(-2, p)$, $t = \gamma - \alpha$, $q = \gamma - \beta$ |
| RSL | $p^2 = -2 + d^2 + 2\cos(\alpha - \beta) - 2d(s_\alpha + s_\beta) \ge 0$ | $\sqrt{p^2}$ | $\gamma = \mathrm{atan2}(c_\alpha + c_\beta, d - s_\alpha - s_\beta) - \mathrm{atan2}(2, p)$, $t = \alpha - \gamma$, $q = \beta - \gamma$ |
| RLR | $c = (6 - d^2 + 2\cos(\alpha - \beta) + 2d(s_\alpha - s_\beta))/8 \in [-1, 1]$ | $2\pi - \arccos c$ | $t = \alpha - \mathrm{atan2}(c_\alpha - c_\beta, d - s_\alpha + s_\beta) + p/2$, $q = \alpha - \beta - t + p$ |
| LRL | $c = (6 - d^2 + 2\cos(\alpha - \beta) + 2d(s_\beta - s_\alpha))/8 \in [-1, 1]$ | $2\pi - \arccos c$ | $t = -\alpha - \mathrm{atan2}(c_\alpha - c_\beta, d + s_\alpha - s_\beta) + p/2$, $q = \beta - \alpha - t + p$ |

The values of $t$ and $q$ are reduced with $\mathrm{mod}_{2\pi}$. These are the forms of Shkel and Lumelsky (2001), which LaValle also gives in Section 15.3.1. Each one comes from the circles of radius 1 that the car follows at the start and at the goal. For LSL, the left circles have centers $(-s_\alpha, c_\alpha)$ and $(d - s_\beta, c_\beta)$, the straight part is their outer common tangent, and its length is the distance between the centers, which is the $p$ of the table. For LSR, the straight part is an inner common tangent, so $p^2$ is the squared distance of the centers minus 4. For RLR and LRL, the middle circle touches both end circles, so its center is at distance 2 from both, and $c$ is the cosine that the law of cosines gives in the triangle of the three centers.

## Example

Let $\rho = 1$ m, the start $q_0 = (0, 0, 0)$ and the goal $q_1 = (3, 4, \pi/2)$, with lengths in meters. Line L1 gives $d = 5$ and $\varphi = \mathrm{atan2}(4, 3) = 0.9273$ rad. Line L2 gives $\alpha = 2\pi - 0.9273 = 5.3559$ and $\beta = \pi/2 - 0.9273 = 0.6435$. The loop of lines L4 to L6 finds five words. RLR does not exist, because $c < -1$: the two right circles are more than 4 m apart.

| Word | $\ell_1$ (m) | $\ell_2$ (m) | $\ell_3$ (m) | Length (m) |
|---|---|---|---|---|
| LSL | 0.9828 | 3.6056 | 0.5880 | 5.1763 |
| LRL | 3.0014 | 4.0373 | 2.6066 | 9.6453 |
| RSL | 5.4734 | 5.0000 | 0.7610 | 11.2344 |
| LSR | 1.0550 | 4.5826 | 5.7674 | 11.4050 |
| RSR | 5.3871 | 6.4031 | 5.6084 | 17.3987 |

The answer is LSL. You can check it by hand. The left circle at the start has center $(0, 1)$ and the left circle at the goal has center $(2, 4)$. The line between the centers has direction $\mathrm{atan2}(3, 2) = 0.9828$ rad, so the car first turns left by 0.9828 rad, drives $\sqrt{2^2 + 3^2} = \sqrt{13} = 3.6056$ m, and turns left by $\pi/2 - 0.9828 = 0.5880$ rad.

A second case shows a CCC word. For the U-turn on the spot from $(0, 0, 0)$ to $(0, 0, \pi)$ with $\rho = 1$ m, the CSC words LSL and RSR have length 11.4248 m, and LSR and RSL do not exist. RLR and LRL both give arcs of $\pi/3$, $5\pi/3$ and $\pi/3$ rad, a total of $7\pi/3 = 7.3304$ m. The middle arc is longer than $\pi$, as Dubins' theorem says it must be.

## Correctness

The [proof](proofs/correctness/) has two parts. The first is a check of the closed forms: for each word, the three segments of line L5 start at $q_0$ and end at $q_1$, because the straight part is a common tangent of the two end circles, or the middle arc lies on a circle that touches both. The second part is Dubins' theorem, which the page uses and does not prove: a shortest path exists, has one of the six words, and has a middle arc longer than $\pi\rho$ when it is CCC. For each word, the path with arcs in $[0, 2\pi)$ (and a middle arc in $[\pi, 2\pi]$ for CCC) is unique, so the candidate set contains the shortest path, and lines L3 to L7 return it.

## Complexity

- **Time.** Six words, each with a fixed number of operations, so $O(1)$ in the real RAM. Measured: in the implementation, one call with all six words takes about 15 microseconds in CPython on a laptop. Shkel and Lumelsky give a rule that picks the shortest word from $(\alpha, \beta)$ when $d$ is large, without computing the others; it saves a constant factor.
- **Space.** $O(1)$.
- **Sampling.** Drawing the path or checking it against obstacles needs points along it. With a spacing $\Delta s$, that costs $O(\ell / \Delta s)$ for a path of length $\ell$, and this is usually the larger cost.

## Properties

- **Exact.** The result is the true optimum, not an approximation, up to rounding.
- **Not symmetric in the poses.** The path from $q_0$ to $q_1$ differs from the path from $q_1$ to $q_0$. Its length equals the length from $(x_1, y_1, \theta_1 + \pi)$ to $(x_0, y_0, \theta_0 + \pi)$, because that is the same curve driven in the other direction. The Dubins length is a quasi-metric, not a metric.
- **Not continuous.** A small change of the goal can switch the best word and make the path jump. For example, a goal just behind the car needs a loop, and a goal just in front does not. The length is also discontinuous where the goal is very close to the start.
- **Scale.** Lengths scale with $\rho$: the path for $\rho$ and goal $(x, y)$ is $\rho$ times the path for radius 1 and goal $(x/\rho, y/\rho)$.
- **Curvature jumps.** The path is $C^1$, with a continuous heading, but its curvature jumps between $0$ and $\pm 1/\rho$ at the joints. A real car cannot steer that fast; see Pitfalls.

## Variants and improvements

- **Reeds-Shepp paths.** Allow reverse motion; see the [Reeds-Shepp path](/reeds-shepp-path/) page.
- **Fast word choice.** Shkel and Lumelsky (2001) split the $(\alpha, \beta)$ square into regions and give the shortest word in each region when $d$ is large enough. It avoids computing all six words.
- **Dubins paths in planners.** [Hybrid A\*](/hybrid-a-star/) uses Dubins or Reeds-Shepp lengths in an empty map as an admissible heuristic, and a Dubins or Reeds-Shepp path as a last shot to the goal. RRT and RRT\* for cars use the Dubins path as the steering function and the Dubins length as the distance; see [kinodynamic planning](/kinodynamic-planning/).
- **Curvature-continuous paths.** Replace the jumps of curvature by clothoid pieces of bounded curvature rate. The result is no longer the shortest path of the original problem.
- **Three dimensions.** The Dubins airplane adds an altitude with a bounded climb rate. It is a different problem with more cases.

## When to use it

Use it as the local path of a car-like robot that cannot or should not reverse: fixed-wing aircraft at constant altitude, boats, cars on a road. Use it as a lower bound on the length of any forward path between two poses, for example as the heuristic of a search. Do not use it as a trajectory to track without smoothing, because the curvature jumps. If the robot can reverse, the Reeds-Shepp path is shorter and also costs constant time.

## Pitfalls

- **Rounding near zero segments.** When a straight part has length 0 (the two circles touch, or are the same circle), $p$ is the square root of a rounded $p^2$ near 0. A rounding error of $10^{-16}$ in $p^2$ gives $p \approx 10^{-8}$, and an angle that should be 0 can come out just below $2\pi$, which adds a full loop. The implementation clamps small negative $p^2$ to 0, snaps angles within $10^{-10}$ of $2\pi$ to 0, and treats two equal circles as a single arc.
- **The direction of the angles.** $\mathrm{mod}_{2\pi}$ must return a value in $[0, 2\pi)$. Python's `math.fmod` returns a negative value for a negative input, and the C `fmod` does too.
- **CCC middle arc.** Of the two middle circles that touch both end circles, only the one with a middle arc longer than $\pi$ can be optimal. The formula $p = 2\pi - \arccos c$ picks it. Taking $\arccos c$ instead gives a valid but longer path.
- **Not every word exists.** CCC words need $d < 4$ after scaling. Code that does not test the conditions takes the square root of a negative number.
- **Ties.** LSR and RSL, or RLR and LRL, can tie, as in the U-turn above. Then the word chosen depends on the order of the loop.
- **Radius and steering.** For a car, $\rho = L/\tan\delta_{max}$ holds for the rear axle in the kinematic bicycle model. Tire slip makes the true radius larger at speed.

## Implementations

## History

Dubins (1957) proved the existence of shortest curves with an upper bound on average curvature, and showed that they are of type CSC or CCC, or parts of these. His proof is geometric. Reeds and Shepp (1990) solved the problem with reverse motion. Sussmann and Tang (1991) and Boissonnat, Cérézo and Leblond (1994) gave proofs of both results with the [Pontryagin maximum principle](/pontryagin-maximum-principle/). Shkel and Lumelsky (2001) gave the closed forms used here and the rule that picks the shortest word. LaValle's book of 2006 made the Dubins car a standard example of a nonholonomic system in motion planning.

## References
