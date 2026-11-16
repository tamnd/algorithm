---
tag: 8BG41W
kind: algorithm
slug: goldberg-part-orienting-algorithm
name: Goldberg's part orienting algorithm
aliases:
- squeeze-grasp orienting plan
area: robotics/grasping-and-manipulation
level: advanced
summary: Computes a shortest sequence of parallel-jaw squeezes that orients a polygonal part with unknown orientation, up to the symmetry of its squeeze function, in polynomial time.
model: word-ram
complexity:
  vars: {n: "the number of vertices of the convex hull of the part"}
  time: {worst: O(n^2 log n)}
  space: {extra: O(n^2)}
properties: {deterministic: true, exact: true, optimal: true}
history:
  year: 1993
  people: [Kenneth Y. Goldberg]
  note: Goldberg showed that every polygonal part can be oriented up to symmetry by squeezes alone, and gave a backward search over s-intervals that finds a shortest plan.
prereqs: [sensorless-part-orienting, convex-hull]
see_also: [quasi-static-pushing, rotating-calipers, conformant-planning, belief-space, breadth-first-search, fixture-planning, mason-voting-theorem, antipodal-grasp]
sources:
  - paper: doi:10.1007/BF01891840
    title: Kenneth Y. Goldberg, Orienting polygonal parts without sensors, Algorithmica 10, 201-225, 1993
    locator: "Section 3 (assumptions, the diameter and squeeze functions, steps closed on the left, period T), Section 4 (the algorithm and the recovery of the plan), Sections 5 and 6 (shortest plan and completeness), Section 7 (O(n^2 log n) time, plans of length O(n^2)), Section 8 (push-grasp actions)"
  - paper: doi:10.1007/BF01192046
    title: Yu-Bin Chen and Doug J. Ierardi, The complexity of oblivious plans for orienting and distinguishing polygonal parts, Algorithmica 14(5), 367-397, 1995
    locator: the whole paper (plans of O(n) squeezes, which proves Goldberg's conjecture)
  - book: isbn:9780262133968
    title: Matthew T. Mason, Mechanics of Robotic Manipulation, MIT Press, 2001
    locator: Chapter 7, Section 7.4 (parts orienting)
  - paper: doi:10.1109/56.800
    title: Michael A. Erdmann and Matthew T. Mason, An exploration of sensorless manipulation, IEEE Journal of Robotics and Automation 4(4), 369-379, 1988
    locator: the whole paper (orienting parts in a tilted tray without sensors, the setting that Goldberg's work continues)
---

Goldberg's part orienting algorithm takes the vertices of a polygonal part and returns a list of gripper angles. A parallel-jaw gripper that squeezes the part at these angles, one after the other, brings the part to one known orientation, whatever its orientation was at the start. No sensor is used. The plan is the shortest possible, and it exists for every polygonal part, but only up to the symmetry of the part's squeeze function: a square, for example, is oriented only up to quarter turns. This page is the algorithm; [sensorless part orienting](/sensorless-part-orienting/) is the general problem, with other actions such as pushes and tilted trays.

## In plain words

Put a flat part between the two jaws of a gripper and close them. The part turns until one of its sides lies flat against a jaw, because that is how it gets thinnest between the jaws. Which side ends up flat depends on how the part was turned at the start, but there are only a few possible results. Now turn the gripper by a chosen angle and squeeze again. A good angle makes several of the possible results end in the same place. Repeat, and the list of possible results gets shorter each time, until only one is left. The algorithm finds the angles. It works backward: first it finds the widest range of starting turns that one squeeze sends to a single result, then the widest range that two squeezes can handle, and so on, until the range covers every starting turn.

## The problem

The input is a list of points in the plane, the vertices of a part. Only the [convex hull](/convex-hull/) matters, because the jaws touch only hull vertices; let $n$ be the number of hull vertices. The model is the one of Goldberg (1993, Section 3): motion in the plane, slow enough that inertia does not matter ([quasi-static](/quasi-static-pushing/)); two parallel jaws that close along the direction normal to them and touch the part at the same time; no friction between the part and the jaws; a rigid part.

Angles are in radians. Let $\theta$ be the orientation of the part relative to the gripper. The *diameter function* $d(\theta)$ is the distance between the jaws when both touch the part. It has period $\pi$, because the gripper turned by $\pi$ is the same gripper. A squeeze turns the part so that $d$ decreases, until $d$ reaches a local minimum. So the *squeeze function* $s$ maps every $\theta$ between two neighbor local maxima $e_j < e_{j+1}$ of $d$ to the local minimum $m_j$ between them. As in Goldberg's paper, each step $[e_j, e_{j+1})$ is closed on the left and open on the right. The steps continue over the real line, and $s$ satisfies

$$s(\theta + T) = s(\theta) + T$$

for its smallest period $T$, which divides $\pi$. Let $r$ be the number of steps in one period. A squeeze with the gripper at the world angle $\alpha$ maps the world orientation $\varphi$ of the part to $\alpha + s(\varphi - \alpha)$.

A plan $(\alpha_1, \ldots, \alpha_k)$ *orients the part up to symmetry* if every initial orientation ends at the same orientation modulo $T$. Better is not possible: two orientations that differ by $T$ stay $T$ apart under every squeeze. The task is a shortest such plan.

## The algorithm

An *s-interval* is a union of consecutive steps, $[e_p, e_{q+1})$ with $p \le q$. Its *s-image* is the closed interval $[m_p, m_q]$, of length $m_q - m_p$. The algorithm builds a list $\Theta_1, \Theta_2, \ldots$ of s-intervals in which the s-image of $\Theta_{i+1}$ is shorter than $\Theta_i$, so that one squeeze can place it inside $\Theta_i$. Then it reads the plan off the list from the end.

```pseudo id=main
GOLDBERG-PLAN(P)                            ▷ P: the vertices of the part
L1  H ← CONVEX-HULL(P)
L2  compute d and s for H: the maxima e_j and the minima m_j, e_j < m_j < e_(j+1)
L3  T ← the smallest period of s; r ← the number of steps in one period
L4  Θ_1 ← the widest step [e_j, e_(j+1)); i ← 1
L5  while |Θ_i| < T do
L6      Θ_(i+1) ← the widest s-interval [e_p, e_(q+1)) with m_q - m_p < |Θ_i|
L7      i ← i + 1
L8  k ← i; α_1 ← 0
L9  for t ← 2 to k do
L10     [a, b) ← Θ_(k-t+1); [m_p, m_q] ← the s-image of Θ_(k-t+2)
L11     α_t ← α_(t-1) + m_p - a - ((b - a) - (m_q - m_p)) / 2
L12 return (α_1, ..., α_k) and the final orientation α_k + s(Θ_1)
```

Line L2 needs the extremes of $d$. Between two angles at which a jaw is flush with an edge, the same two vertices touch the jaws, and $d(\theta) = \langle w, (\sin\theta, \cos\theta)\rangle$ for the vector $w$ between them, a sinusoid with one maximum. At the flush angles $d$ has a convex kink, so the local minima are flush angles and the local maxima lie inside the pieces. Line L6 needs no search over all pairs: for each $p$ the best $q$ is the largest one with $m_q - m_p < |\Theta_i|$, and that $q$ grows with $p$, so two pointers find the maximum in $O(r)$ steps. Line L11 turns the gripper so that the s-image lands in the middle of the next s-interval, with half the slack on each side.

## Example

Take a rectangle of size 2 by 1, with its long side along the $x$ axis, and the jaws closing along the $y$ axis of the gripper. Then $d(\theta) = 2\lvert\sin\theta\rvert + \lvert\cos\theta\rvert$. The minima are at $0$, where $d = 1$ and the long sides touch the jaws, and at $\pi/2$, where $d = 2$. The maxima are at $\arctan 2 = 1.1071$ and $\pi - \arctan 2 = 2.0344$. The rectangle has a half-turn symmetry, so $T = \pi$ and $r = 2$.

| Step | Interval | Width | Maps to |
|---|---|---|---|
| around $\pi/2$ | $[1.1071, 2.0344)$ | $0.9273$ | $\pi/2$ |
| around $\pi$ | $[2.0344, 4.2487)$ | $2.2143$ | $\pi$ |

Line L4 picks the wider step: $\Theta_1 = [2.0344, 4.2487)$, with $\lvert\Theta_1\rvert = 2\arctan 2 = 2.2143$. In line L6, the union of both steps, $[1.1071, 4.2487)$, has the s-image $[\pi/2, \pi]$ of length $\pi/2 = 1.5708 < 2.2143$, so $\Theta_2 = [1.1071, 4.2487)$ with $\lvert\Theta_2\rvert = \pi = T$. The loop stops with $k = 2$.

Line L11 gives the slack $2.2143 - 1.5708 = 0.6435$ and the angle $\alpha_2 = 0 + \pi/2 - 2.0344 - 0.6435/2 = -0.7854 = -\pi/4$. The plan is: squeeze at $0$, then squeeze at $-45$ degrees. After the first squeeze the part is at $0$ or $\pi/2$ in the world frame. Relative to the gripper at $-\pi/4$ these are $\pi/4$ and $3\pi/4$, and both are in $\Theta_1$ modulo $\pi$, so the second squeeze sends both to the world orientation $-\pi/4 + \pi = 3\pi/4$, modulo $\pi$. The turn of the gripper may err by up to half the slack, $0.3218$ rad (18.4 degrees), and the plan still works. Goldberg's own figure gives the plan $(0, \pi/4)$ for a rectangle; it is the mirror image of this one, because the rectangle is symmetric and the tie in line L6 can be broken either way.

The quadrilateral with vertices $(-42, -41)$, $(48, -41)$, $(39, 25)$ and $(-34, 59)$ from Goldberg's paper has no symmetry, $T = \pi$ and $r = 4$. The algorithm finds s-intervals of lengths $0.8840$, $1.5739$, $2.3749$ and $\pi$, so the shortest plan has 4 squeezes, as in the paper's figure. A square and every regular polygon need one squeeze: their squeeze function has one step per period.

## Correctness

The full proof is in proofs/correctness.md. It has four parts. First, a set of orientations can be brought to one orientation by $i$ squeezes if and only if it fits in an arc of length $\lvert\Theta_i\rvert$; the proof is an induction on $i$, and the "only if" direction uses that the minima inside an arc shorter than $T$ are consecutive. Second, the lengths grow while they are below $T$. This is Goldberg's integral argument: the function $s(\theta + h) - s(\theta) - h$ has integral 0 over a period, so it is negative somewhere unless $h$ is a period, and a point where it is negative gives a longer s-interval. Third, each length is one of at most $r^2$ values, so the loop stops with $\lvert\Theta_k\rvert = T$. Fourth, the whole circle fits in an arc of length $L$ only when $L \ge T$, so no plan has fewer than $k$ squeezes, and the angles of line L11 put each s-image strictly inside the next s-interval.

## Complexity

The cost model is the word RAM of Goldberg's Section 7, in which a distance, an angle, a comparison and an addition of two numbers take $O(1)$ time. Goldberg (1993) computes the squeeze function in $O(n)$ time, notes that there are $O(n^2)$ s-intervals, sorts them by the length of their s-image, and scans the sorted list once. The sort dominates, so the algorithm runs in $O(n^2 \log n)$ time with $O(n^2)$ space. He proves that the plan has $O(n^2)$ squeezes and conjectured $O(n)$; Chen and Ierardi (1995) proved that $O(n)$ squeezes always suffice.

The implementation on this page skips the sort. It computes $s$ in $O(n^2)$ time (for each of the $O(n)$ pieces it finds the touching vertices by a scan) and each round of line L6 in $O(r)$ time with two pointers, where $r \le n$. With the $O(n)$ bound of Chen and Ierardi on the number of rounds, the total time is $O(n^2)$ and the extra space is $O(n)$.

## Properties

- **Optimal.** The plan has the least number of squeezes among all plans that orient the part up to symmetry.
- **Complete.** A plan exists for every polygonal part, because the lengths keep growing until they reach $T$.
- **Open loop.** The plan uses no sensing. The same angles work for every initial orientation, so a fixed machine can run them.
- **Margin.** Each turn of the gripper after the first has a slack, and errors below half the slack do not change the result.
- **Up to symmetry only.** The final orientation is known modulo $T$. A part whose squeeze function has period $\pi/2$ ends in one of four orientations, and no squeeze plan can tell them apart.

## Variants and improvements

- **Push-grasp actions.** Goldberg (1993, Section 8) lets one jaw touch first and push the part before the second jaw closes. The push function, from the radius function about the center of mass, composes with the squeeze function to a new step function with the same properties, and the same backward search applies. It can remove the half-turn ambiguity of pure squeezes, because the radius function has period $2\pi$ for a part without rotational symmetry.
- **Pushing only.** A fence or a pusher that turns the part to a stable edge gives a push function; the planning is the same. Mason (2001, Section 7.4) presents squeeze and push planning together.
- **Shorter worst case.** Chen and Ierardi (1995) give plans with $O(n)$ squeezes and study plans that tell different parts apart.
- **Brute force.** A [breadth-first search](/breadth-first-search/) over sets of stable orientations, with the gripper angles at the midpoints between critical angles, also finds a shortest plan. It takes exponential time in $r$, and the test of this page uses it as the reference.

## When to use it

Use it to program a parts feeder for flat parts that arrive at random orientations, when the gripper can turn between squeezes and a camera is too slow, too costly or not reliable. Use the push-grasp version when the half-turn ambiguity matters. Use a sensor when the part has symmetries of its squeeze function that the task must resolve, because no squeeze plan can resolve them.

## Pitfalls

- **Friction at the jaws.** The squeeze function assumes frictionless jaws. With friction the part can stay wedged between two vertices. Goldberg suggests a linear bearing on one jaw, and mechanical vibration helps in practice.
- **Unstable equilibria.** At a maximum of $d$ the part is in an unstable balance. The left-closed steps are a convention. A plan with a margin keeps the orientations away from the maxima after the first squeeze.
- **Symmetry of $s$, not of the part.** The period $T$ is the smallest period of the squeeze function. It can be shorter than the symmetry period of the part suggests, so compute it from $s$.
- **Floating ties.** The angles are irrational, and the comparison $m_q - m_p < \lvert\Theta_i\rvert$ can be a tie for symmetric parts. A tolerance must break ties toward the safe side, or the plan can lose its margin.
- **Relative turns.** The margin bounds the error of each turn between two squeezes, not the error of the absolute angle. An error in one angle shifts all later orientations by the same amount.

## Implementations

## History

Erdmann and Mason (1988) showed that parts can be oriented without sensors, by tilting a tray. Goldberg (1993) turned the squeeze of a parallel-jaw gripper into the step function $s$ and proved that every polygonal part can be oriented up to symmetry by squeezes alone, with a shortest plan found in $O(n^2 \log n)$ time. He conjectured that plans of $O(n)$ squeezes always exist, and Chen and Ierardi (1995) proved it. Mason (2001) gives the method as the main example of sensorless parts orienting.

## References
