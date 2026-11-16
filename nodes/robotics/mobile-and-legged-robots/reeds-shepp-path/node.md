---
tag: FYPPAD
kind: algorithm
slug: reeds-shepp-path
name: Reeds-Shepp path
aliases:
- Reeds-Shepp curves
area: robotics/mobile-and-legged-robots
level: core
summary: Shortest path of a car that drives forward and backward with bounded curvature. Reeds and Shepp gave 48 candidate words; Sussmann and Tang reduced the sufficient family to 46.
solves: [kinodynamic-planning]
model: real-ram
complexity:
  vars: {w: "the number of candidate words, at most 48"}
  time: {worst: O(1)}
  space: {extra: O(1)}
properties: {deterministic: true, randomized: false, online: false, exact: true}
history:
  year: 1990
  people: [James A. Reeds, Lawrence A. Shepp]
  note: Reeds and Shepp proved in 1990 that the shortest path of a car that may reverse has at most five pieces and two cusps, in one of 48 words; Sussmann and Tang showed in 1991 that 46 of them suffice.
prereqs: [dubins-path]
see_also: [dubins-path, hybrid-a-star, state-lattice-planning, kinodynamic-planning, a-star-search, kinematic-bicycle-model, lie-algebra-rank-condition, pontryagin-maximum-principle]
sources:
  - paper: doi:10.2140/pjm.1990.145.367
    title: James A. Reeds and Lawrence A. Shepp, Optimal paths for a car that goes both forwards and backwards, Pacific Journal of Mathematics 145(2), 1990
    locator: pages 367 to 393 (the theorem with the 48 words, and Section 8 with the formulas 8.1 to 8.11 for the segment lengths)
  - paper: "Héctor J. Sussmann and Guoqing Tang, Rutgers Center for Systems and Control, report SYCON-91-10, 1991"
    title: Shortest paths for the Reeds-Shepp car, a worked out example of the use of geometric techniques in nonlinear optimal control
    locator: the whole report (a proof with the maximum principle, and the reduction of the sufficient family from 48 to 46 words)
  - book: isbn:9780521862059
    title: Steven M. LaValle, Planning Algorithms, Cambridge University Press, 2006
    locator: Section 15.3.2 (Reeds-Shepp curves, the nine base words with cusps and the 46 curves that occur) and Section 15.4 (the Reeds-Shepp car is small-time locally controllable)
  - paper: doi:10.1007/BF01258291
    title: Jean-Daniel Boissonnat, André Cérézo and Juliette Leblond, Shortest paths of bounded curvature in the plane, Journal of Intelligent and Robotic Systems 11, 1994
    locator: pages 5 to 20 (a proof of the results of Dubins and of Reeds and Shepp with the Pontryagin minimum principle)
---

A Reeds-Shepp path is a shortest path between two poses of a car that can drive forward and backward and cannot turn tighter than a radius $\rho$. A pose is $(x, y, \theta)$, a position and a heading. Reeds and Shepp proved in 1990 that a shortest path always exists, has at most five pieces (arcs of radius $\rho$ and straight segments) and at most two cusps where the car changes gear, and has one of 48 words. Sussmann and Tang showed in 1991 that two of these words are never needed, so 46 suffice. The algorithm solves each word in closed form and keeps the shortest, in constant time. It is the analytic shot to the goal of [hybrid A\*](/hybrid-a-star/) and the steering function of many parking planners.

## In plain words

You park a car in an empty lot. You may back up, and the steering wheel has a stop. The shortest way to the parking spot always uses at most five pieces: hard turns and straight runs, with at most two changes between forward and reverse. A U-turn on the spot, for example, is three short hard turns: forward left, back right, forward left.

There are only 48 patterns. Each one comes with a formula for the lengths of its pieces. You try all patterns and keep the shortest.

## The problem

**The model.** The car is the [unicycle model](/unicycle-model/) with a speed $v \in \{-1, +1\}$ and a turn rate $|\omega| \le 1/\rho$, or the rear axle of the [kinematic bicycle model](/kinematic-bicycle-model/) with $\rho = L/\tan\delta_{max}$. The length of a path is the total distance, forward and backward, and a gear change costs nothing. There are no obstacles. The machine model is the [real RAM](/real-ram/).

**Input.** A start pose $q_0$ and a goal pose $q_1$, in meters and radians, and the minimum turning radius $\rho > 0$ in meters.

**Output.** A word over $\{L, S, R\}$ and signed segment lengths, positive for forward and negative for backward, such that driving them from $q_0$ ends at $q_1$, and the sum of the absolute lengths is the least possible.

**How it differs from close pages.** The [Dubins path](/dubins-path/) is the same problem for a car that only drives forward. Every Dubins path is also a Reeds-Shepp path, so the Reeds-Shepp length is never longer, and it is often much shorter for goals behind the car. [Kinodynamic planning](/kinodynamic-planning/) adds obstacles and dynamics. A search such as [A\*](/a-star-search/) on a lattice, or [hybrid A\*](/hybrid-a-star/), handles the obstacles and calls this solver for heuristics and final connections.

## The algorithm

Write the goal in the frame of the start and scale by $1/\rho$, so the start is $(0, 0, 0)$, the goal is $(x, y, \varphi)$ and the radius is 1. Reeds and Shepp use three transformations of the goal that map solutions to solutions:
- **Time flip** $(x, y, \varphi) \to (-x, y, -\varphi)$: drive every segment with the opposite sign. The word stays the same.
- **Reflection** $(x, y, \varphi) \to (x, -y, -\varphi)$: swap L and R. The signs stay the same.
- **Backward** $(x, y, \varphi) \to (x\cos\varphi + y\sin\varphi,\ x\sin\varphi - y\cos\varphi,\ \varphi)$: the same path read from the goal to the start, followed by a time flip. The order of the segments is reversed.

With these, nine base formulas of Section 8 of their paper give all 48 words. In the base words, $+$ is forward and $-$ is backward.

In the family names, a bar $\mid$ marks a cusp, $C_u$ marks two arcs of the same angle $u$, and $C_{\pi/2}$ an arc of angle $\pi/2$.

| Formula | Base word | Families | Uses backward |
|---|---|---|---|
| 8.1 | $L^+ S^+ L^+$ | $CSC$ | no |
| 8.2 | $L^+ S^+ R^+$ | $CSC$ | no |
| 8.3, 8.4 | $L^+ R^- L$ | $C \mid C \mid C$, $C \mid CC$, $CC \mid C$ | yes |
| 8.7 | $L^+ R^+_u L^-_u R^-$ | $CC_u \mid C_u C$ | no |
| 8.8 | $L^+ R^-_u L^-_u R^+$ | $C \mid C_u C_u \mid C$ | no |
| 8.9 | $L^+ R^-_{\pi/2} S^- L^-$ | $C \mid C_{\pi/2} S C$ and, backward, $C S C_{\pi/2} \mid C$ | yes |
| 8.10 | $L^+ R^-_{\pi/2} S^- R^-$ | $C \mid C_{\pi/2} S C$ and, backward, $C S C_{\pi/2} \mid C$ | yes |
| 8.11 | $L^+ R^-_{\pi/2} S^- L^-_{\pi/2} R^+$ | $C \mid C_{\pi/2} S C_{\pi/2} \mid C$ | no |

```pseudo id=main
REEDS-SHEPP(q0, q1, ρ)
L1  (x, y, φ) ← q1 in the frame of q0, with x and y divided by ρ
L2  best ← none
L3  (xb, yb) ← (x cos φ + y sin φ, x sin φ - y cos φ)
L4  for each base formula F and each goal g among (x, y, φ), (-x, y, -φ), (x, -y, -φ), (-x, -y, φ), and the same four for (xb, yb, φ) where F uses backward do
L5      if F(g) gives (t, u, v) within its ranges then build the signed lengths of the word; negate them for a time flip, swap L and R for a reflection, reverse their order for a backward goal
L6          ℓ ← ρ times the sum of the absolute lengths
L7          if best is none or ℓ < the length of best then best ← (word, ρ times the lengths)
L8  return best
```

Each base formula is a few lines of trigonometry. For example, 8.1 ($L^+ S^+ L^+$) puts the center of the left circle at the goal at $(x - \sin\varphi, y + \cos\varphi)$, takes $(u, t)$ as the polar coordinates of $(x - \sin\varphi, y - 1 + \cos\varphi)$, and sets $v = \varphi - t$; it accepts when $t \ge 0$ and $v \ge 0$ after wrapping to $[-\pi, \pi)$. The tests "within its ranges" of line L5 keep only the sign pattern of the base word. The implementation follows the formulas as they appear in the ReedsSheppStateSpace class of the open source OMPL library, whose source marks misprints in formulas 8.3/8.4 and 8.11 of the paper and uses corrected forms.

## Example

Let $\rho = 1$ m and the start $(0, 0, 0)$, with all lengths in meters.

**Parallel shift.** The goal is $(0, 1, 0)$: the same heading, 1 m to the left. A forward-only car needs a loop, and the [Dubins path](/dubins-path/) is LSL with a quarter turn, 1 m straight and three quarters of a turn, of length $2\pi + 1 = 7.2832$ m. The loop of lines L4 to L7 finds 8 candidates. The two shortest are:

| Word | Signed lengths (m) | Length (m) | Gear changes |
|---|---|---|---|
| $R^- L^+ R^+ L^-$ | $-0.5054, 0.8128, 0.8128, -0.5054$ | 2.6362 | 2 |
| $R^+ L^- R^- L^+$ | $0.5054, -0.8128, -0.8128, 0.5054$ | 2.6362 | 2 |

These are the two mirror images in time of the CC_u|C_uC family: back right a little, forward left and right by the same angle $u = 0.8128$ rad, and back left a little. The next family, $L R L R$ with four arcs of 0.7227, is longer at 2.8909 m.

**U-turn on the spot.** The goal is $(0, 0, \pi)$. The answer is a C|C|C word of three arcs of $\pi/3$ rad, for example forward left, backward right, forward left, with total length $\pi = 3.1416$ m. The Dubins path for the same goal is $7\pi/3 = 7.3304$ m.

**A goal in front.** For the goal $(3, 4, \pi/2)$ the answer is the forward path $L^+ S^+ L^+$ with lengths 0.9828, 3.6056 and 0.5880, the same as the Dubins path, of length 5.1763 m. The best word with reverse, $R^+ L^-_{\pi/2} S^- R^-_{\pi/2} L^+$, has 7.2344 m.

## Correctness

The [proof](proofs/correctness/) shows that the three transformations map paths to paths, so each candidate of line L5 ends at the goal when its base formula does. It proves the base formula 8.1 in full as an example and relies on Section 8 of Reeds and Shepp for the others. The implementation checks the end pose of every candidate on 1500 random pairs of poses, within $10^{-9}$ m. The optimality comes from the theorem of Reeds and Shepp, which the page uses and does not prove: a shortest path exists and has one of the 48 words, with segment lengths in the ranges that the base formulas test.

## Complexity

- **Time.** At most 9 base formulas, each on 4 or 8 goals, so a fixed number of operations: $O(1)$ in the real RAM. Measured: one call takes about 0.3 milliseconds in CPython on a loaded laptop, about 20 times a Dubins call.
- **Space.** $O(1)$.
- **Sampling.** Points along the path for collision checks cost $O(\ell / \Delta s)$ for a length $\ell$ and a spacing $\Delta s$.

## Properties

- **A metric.** Unlike the Dubins length, the Reeds-Shepp length is symmetric: a path from $q_0$ to $q_1$, driven backward in time, is a path from $q_1$ to $q_0$ of the same length. It satisfies the triangle inequality, so it is a metric on the poses.
- **Continuous.** The Reeds-Shepp car is small-time locally controllable, so the Reeds-Shepp distance is continuous in the poses (LaValle, Section 15.3.2). The best word can still jump, so the path is not continuous in the goal.
- **At most two cusps and five segments.** Every word in the family has at most two gear changes.
- **Not unique.** Mirror images in time often tie, as in the example.
- **Scale.** Lengths scale with $\rho$.

## Variants and improvements

- **Dubins paths.** Forward only; see [Dubins path](/dubins-path/).
- **46 words.** Sussmann and Tang (1991) showed that two of the 48 words are never strictly needed, so 46 suffice. LaValle (Section 15.3.2) calls these 46 the Reeds-Shepp curves. The code does not remove the two extra words; testing them costs a little time and does not change the answer.
- **Gear change cost.** Planners such as [hybrid A\*](/hybrid-a-star/) add a cost for reverse driving and for each gear change. The Reeds-Shepp path then is no longer optimal for that cost, and planners use it only as a candidate or a heuristic.
- **Continuous curvature.** Clothoid pieces replace the curvature jumps for real steering; the result is longer.
- **Differential drive.** For a robot that turns in place, the time-optimal paths are the Balkcom-Mason curves (LaValle, Section 15.3.3).

## When to use it

Use it as the local path, the distance and the final shot to the goal for car-like robots that can reverse: parking, docking, forklifts. Use its length as an admissible heuristic in an empty map. If the robot must not reverse, use the Dubins path. Do not track the path as it is, because the curvature jumps and the car must stop at each cusp.

## Pitfalls

- **Misprints in the paper.** The OMPL source marks formulas 8.3/8.4 and 8.11 of the paper as misprinted. Use a corrected version, and test every candidate by driving it to the end.
- **Sign conventions.** A backward left arc ($L^-$) turns the heading clockwise, because the heading rate is $v/\rho$ with $v < 0$. Code that changes the heading by the absolute length gets every backward arc wrong.
- **Rounding at zero segments.** As for Dubins paths, square roots of quantities near 0 give lengths near $10^{-8}$ instead of 0, and the range tests need a small tolerance (here $10^{-10}$).
- **Wrapping.** The range tests compare angles after wrapping to $[-\pi, \pi)$. Wrapping to $[0, 2\pi)$ changes which candidates pass.
- **Gear changes cost time.** The shortest path can have two cusps where the car must stop. For a real car, a slightly longer path with fewer cusps can be faster.

## Implementations

## History

Reeds and Shepp (1990) extended the result of [Dubins](/dubins-path/) to a car that may reverse, with a long geometric proof and the closed forms of Section 8. Sussmann and Tang (1991) and Boissonnat, Cérézo and Leblond (1994) reproved it with the [Pontryagin maximum principle](/pontryagin-maximum-principle/), and Sussmann and Tang removed two words. Dolgov, Thrun, Montemerlo and Diebel used Reeds-Shepp paths as the analytic expansion of hybrid A\* in the DARPA Urban Challenge of 2007.

## References
