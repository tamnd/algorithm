---
tag: F02YVH
kind: algorithm
slug: collision-prediction-and-resolution
name: Collision prediction and resolution
area: techniques/sweep-line
level: core
summary: Computing when particles will next hit a wall or each other, then updating their velocities after the collision.
model: real-ram
complexity:
  vars: {n: the number of particles, k: the number of events taken from the priority queue}
  time: {worst: O((n² + k n) log(n + k))}
  space: {extra: O(n² + k n)}
properties: {deterministic: true, online: false}
prereqs: [hard-disk-model, priority-queue, dot-product, quadratic-formula]
see_also: [event-driven-simulation, time-driven-simulation, binary-heap, lazy-deletion, collision-detection, molecular-dynamics, kinetic-heap]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 6.1, Event-driven simulation (the classes Particle and CollisionSystem)
  - paper: "B. D. Lubachevsky, How to simulate billiards and similar systems, Journal of Computational Physics 94(2) (1991), doi:10.1016/0021-9991(91)90222-7"
    locator: pages 255 to 283
  - paper: "B. J. Alder and T. E. Wainwright, Studies in molecular dynamics. I. General method, The Journal of Chemical Physics 31(2) (1959), doi:10.1063/1.1730376"
    locator: pages 459 to 466
---

Collision prediction and resolution is the pair of computations at the core of an [event-driven simulation](/event-driven-simulation/) of hard disks: *prediction* finds the first time at which a moving disk touches a wall or another disk, and *resolution* changes the velocities at that moment by an elastic bounce. Prediction solves a quadratic equation in $O(1)$ time, and resolution applies an impulse along the line of the two centres that keeps the momentum and the kinetic energy. With a [priority queue](/priority-queue/) of predicted events, a system of $n$ disks costs $O(n^2 \log n)$ to start and $O(n \log n)$ for each event. The disks follow the [hard-disk model](/hard-disk-model/).

## In plain words

Picture balls on a pool table with no friction. Each ball moves in a straight line at a constant speed until it hits a cushion or another ball. So you never need to move the balls in small steps. For each ball and each cushion, you can work out the exact moment of the hit from the position and the speed. For each pair of balls, you can work out the moment their edges first touch, or find that they never touch.

When a hit happens, the two balls push on each other only along the line through their centres. The push changes the speeds so that the total motion and the total energy stay the same. After the hit, you work out the new future hits of the two balls that changed. A queue sorted by time gives you the next hit at each step.

## The problem

Each disk $i$ has a position $r_i = (r_{x}, r_{y})$, a velocity $v_i = (v_x, v_y)$, a radius $s_i > 0$ and a mass $m_i > 0$, in the unit box $[0, 1] \times [0, 1]$. Between events, each disk moves in a straight line: $r_i(t) = r_i + t\, v_i$. A valid state has each disk inside the box ($s_i \le r_x \le 1 - s_i$ and the same for $y$) and no two disks overlapping ($|r_j - r_i| \ge s_i + s_j$).

- **Prediction.** Given a valid state, return the smallest $\Delta t \ge 0$ at which disk $i$ touches a wall, or touches disk $j$, or $\infty$ if this never happens on the straight paths.
- **Resolution.** Given two disks that touch, replace their velocities by the velocities after a perfectly elastic collision of smooth disks. A disk that touches a wall reverses the velocity component normal to the wall.
- **Simulation.** Run the system from time 0 to a time limit and process the events in time order.

## The algorithm

Write $\Delta r = r_j - r_i$, $\Delta v = v_j - v_i$ and $\sigma = s_i + s_j$. The dot is the [dot product](/dot-product/).

```pseudo id=main
TIME-TO-HIT(i, j)                          ▷ first contact of disks i and j
L1  if i = j then return ∞
L2  Δr ← r_j − r_i, Δv ← v_j − v_i
L3  b ← Δv · Δr
L4  if b ≥ 0 then return ∞                  ▷ not approaching
L5  a ← Δv · Δv, σ ← s_i + s_j
L6  d ← b² − a (Δr · Δr − σ²)
L7  if d < 0 then return ∞                  ▷ closest approach is more than σ
L8  return −(b + √d) / a

TIME-TO-HIT-VERTICAL-WALL(i)
L9  if v_x > 0 then return (1 − s_i − r_x) / v_x
L10 if v_x < 0 then return (s_i − r_x) / v_x
L11 return ∞
TIME-TO-HIT-HORIZONTAL-WALL(i)
L12 the same with r_y and v_y

BOUNCE-OFF(i, j)                           ▷ disks i and j touch
L13 Δr ← r_j − r_i, Δv ← v_j − v_i, σ ← s_i + s_j
L14 J ← 2 m_i m_j (Δv · Δr) / (σ (m_i + m_j))
L15 (J_x, J_y) ← J Δr / σ
L16 v_i ← v_i + (J_x, J_y) / m_i
L17 v_j ← v_j − (J_x, J_y) / m_j
L18 count_i ← count_i + 1, count_j ← count_j + 1
BOUNCE-OFF-VERTICAL-WALL(i)
L19 v_x ← −v_x, count_i ← count_i + 1
BOUNCE-OFF-HORIZONTAL-WALL(i)
L20 v_y ← −v_y, count_i ← count_i + 1

PREDICT(i, t, Q)                           ▷ push the future events of disk i
L21 if i = nil then return
L22 for each disk k do
L23     Δt ← TIME-TO-HIT(i, k); if t + Δt ≤ limit then INSERT(Q, (t + Δt, i, k, count_i, count_k))
L24 push the two wall events of i in the same way

SIMULATE(disks, limit)
L25 Q ← an empty min-priority queue, t ← 0
L26 for each disk i do PREDICT(i, t, Q)
L27 while Q is not empty do
L28     e ← EXTRACT-MIN(Q)
L29     if a count stored in e differs from the disk's count then continue   ▷ stale
L30     move each disk by (e.time − t) v
L31     t ← e.time
L32     resolve e: BOUNCE-OFF, or a wall bounce
L33     PREDICT(e.a, t, Q), PREDICT(e.b, t, Q)
L34 move each disk by (limit − t) v
```

Lines L1 to L8 solve $|\Delta r + \Delta v\, t| = \sigma$ for the first $t \ge 0$; the test of line L4 also covers $\Delta v = 0$, so line L8 never divides by 0. Lines L9 to L11 find when the edge of the disk reaches $x = 1$ (moving right) or $x = 0$ (moving left). Lines L14 to L17 apply an impulse $J$ along the unit normal $\Delta r / \sigma$: disk $i$ gets $+J$ and disk $j$ gets $-J$. When the disks approach, $\Delta v \cdot \Delta r < 0$, so $J < 0$: disk $i$ is pushed away from $j$, and $j$ away from $i$. The counts of line L18 make every earlier prediction about $i$ or $j$ stale. Line L29 drops a stale event when it reaches the front of the queue, which is [lazy deletion](/lazy-deletion/). Line L33 calls PREDICT for the one or two disks that changed; for a wall event one of $e.a$, $e.b$ is nil.

## Example

Disk 0 has $r = (0.2, 0.4)$, $v = (0.3, 0)$, $m = 1$. Disk 1 has $r = (0.78, 0.46)$, $v = (-0.2, 0)$, $m = 3$. Both have $s = 0.05$, so $\sigma = 0.1$.

**Prediction.** $\Delta r = (0.58, 0.06)$ and $\Delta v = (-0.5, 0)$. Then $b = -0.29$, $a = 0.25$, $\Delta r \cdot \Delta r - \sigma^2 = 0.3364 + 0.0036 - 0.01 = 0.33$, and $d = 0.0841 - 0.0825 = 0.0016$, so $\sqrt d = 0.04$. Line L8 gives $\Delta t = (0.29 - 0.04)/0.25 = 1$. The other root, $1.32$, is the time at which the paths would separate if the disks could pass through each other. The walls give $(1 - 0.05 - 0.2)/0.3 = 2.5$ for disk 0 and $(0.05 - 0.78)/(-0.2) = 3.65$ for disk 1; neither disk moves vertically.

**Resolution at $t = 1$.** The disks are at $(0.5, 0.4)$ and $(0.58, 0.46)$, so $\Delta r = (0.08, 0.06)$, of length $0.1 = \sigma$. Then $\Delta v \cdot \Delta r = -0.04$ and $J = 2 \cdot 1 \cdot 3 \cdot (-0.04)/(0.1 \cdot 4) = -0.6$, so $(J_x, J_y) = (-0.48, -0.36)$.

| | before | after |
|---|---|---|
| $v_0$ | $(0.3, 0)$ | $(0.3 - 0.48, 0 - 0.36) = (-0.18, -0.36)$ |
| $v_1$ | $(-0.2, 0)$ | $(-0.2 + 0.16, 0 + 0.12) = (-0.04, 0.12)$ |
| momentum $m_0 v_0 + m_1 v_1$ | $(-0.3, 0)$ | $(-0.3, 0)$ |
| kinetic energy | $0.045 + 0.06 = 0.105$ | $0.081 + 0.024 = 0.105$ |
| $\Delta v \cdot n$, with $n = (0.8, 0.6)$ | $-0.4$ | $0.4$ |
| $\Delta v \cdot n^{\perp}$, with $n^{\perp} = (-0.6, 0.8)$ | $0.3$ | $0.3$ |

**The simulation to $t = 3$.** The start puts three events in the queue: the pair $(0, 1)$ at time 1 (from PREDICT(0)), the pair $(1, 0)$ at time 1 (from PREDICT(1)), and the wall of disk 0 at time 2.5. The wall of disk 1 at 3.65 is after the limit.

| pop | time | event | stored counts | counts now | action |
|---|---|---|---|---|---|
| 1 | 1 | disks 0, 1 | 0, 0 | 0, 0 | resolve; PREDICT(0) adds the floor of disk 0 at $1 + 0.35/0.36 \approx 1.9722$; the other new events are after 3 |
| 2 | 1 | disks 1, 0 | 0, 0 | 1, 1 | stale, skip |
| 3 | 1.9722 | floor, disk 0 | 1 | 1 | resolve: $v_0 = (-0.18, 0.36)$; no new event before 3 |
| 4 | 2.5 | right wall, disk 0 | 0 | 2 | stale, skip |

At $t = 3$ disk 0 is at $(0.14, 0.42)$ and disk 1 at $(0.50, 0.70)$. Two of the four events were stale: one was a copy of a pair event, and one was made wrong by the collision.

## Correctness

Two claims carry the method. First, when $\Delta r \cdot \Delta r > \sigma^2$, TIME-TO-HIT returns the smallest $t \ge 0$ with $|\Delta r + \Delta v\, t| = \sigma$, or $\infty$ when there is none: the squared distance minus $\sigma^2$ is the quadratic $a t^2 + 2 b t + c$ with $c > 0$, it can reach 0 at a positive time only if $b < 0$ and the discriminant $d \ge 0$, and then both roots are positive and line L8 returns the smaller. Second, BOUNCE-OFF keeps the total momentum and the total kinetic energy, keeps the tangential part of $\Delta v$, and reverses its normal part; it is the only impulse along the line of centres, other than zero, that keeps the energy. With these two facts, the main loop keeps the invariant that each valid event in the queue is the true next contact of its disks on their current paths, so the first valid event popped is the next event of the whole system. The full proofs are below.

## Complexity

Each call of TIME-TO-HIT, a wall time or a bounce is $O(1)$ arithmetic operations and one square root, in the [real RAM](/real-ram/). PREDICT does $n + 2$ predictions and at most $n + 2$ insertions.

- **Start.** Line L26 does $n(n + 2)$ predictions and puts $O(n^2)$ events in the queue. With a [binary heap](/binary-heap/) this is $O(n^2 \log n)$, since $\log(n^2) = 2 \log n$. Building the heap in one pass from the list of events lowers it to $O(n^2)$.
- **Each event.** The queue never holds more than $n(n+2) + 2(n+2)k = O(n^2 + kn)$ events, so each queue operation costs $O(\log(n + k))$. A stale event costs one EXTRACT-MIN. A valid event moves all $n$ disks in $O(n)$ time, then makes at most $2(n + 2)$ insertions.
- **In total** $O((n^2 + k n) \log(n + k))$ time for $k$ popped events, and $O(n^2 + k n)$ space, because lazy deletion leaves stale events in the queue. When $k$ is bounded by a polynomial in $n$, this is $O(n^2 \log n)$ to start and $O(n \log n)$ for each event.

Line L30 moves every disk at each event, which is $O(n)$ and is not the bottleneck. Sedgewick and Wayne keep this simple form. Moving a disk only when it takes part in an event, and storing for each disk the time of its last update, removes this term.

## Properties

- **Exact up to rounding.** Between events, the motion is exact; there is no time step and no truncation error. The only errors are the rounding errors of floating-point arithmetic.
- **Elastic.** Each bounce keeps the kinetic energy, so the energy of the system is constant. The walls reverse a velocity component, so the momentum of the system changes at each wall event.
- **Deterministic.** Ties in time are broken by the order of insertion into the queue.

## Variants and improvements

- **A stable root.** Since $b < 0$ and $d \ge 0$, the smaller root equals $c/(-b + \sqrt d)$ with $c = \Delta r \cdot \Delta r - \sigma^2$. This form adds two positive numbers and avoids the cancellation of $-b - \sqrt d$ when the disks are close.
- **Eager deletion.** Keep at most one event per disk in an [indexed priority queue](/indexed-priority-queue/) and replace it when a better one arrives. The queue then has $O(n)$ entries, at the cost of more bookkeeping.
- **Cells.** Divide the box into a grid of cells whose side is at least the largest diameter, and predict collisions only with the disks in the same and the adjacent cells. A *cell-crossing* event moves a disk to a new cell. When each cell holds $O(1)$ disks, each event makes $O(1)$ predictions, and its cost drops to the cost of the queue operations. See [spatial hashing](/spatial-hashing/) and [uniform grids](/uniform-grid/). Lubachevsky's method of 1991 schedules one event per disk and updates each disk only at its own events.
- **Other shapes.** Spheres in three dimensions use the same formulas with 3-vectors. Inelastic collisions multiply the normal impulse by $(1 + e)/2$ for a coefficient of restitution $0 \le e \le 1$.

## When to use it

Use event-driven collision prediction when the bodies move freely between collisions (no forces, or forces that give a closed-form path), and when you need exact contact times, for example in physics of hard spheres or a billiards model. When the bodies feel continuous forces, the paths have no closed form, and a [time-driven simulation](/time-driven-simulation/) with a numerical integrator is the practical choice. For many bodies at high density, add cells, because the $O(n)$ predictions per event dominate.

## Pitfalls

- **Overlapping disks.** If $\Delta r \cdot \Delta r < \sigma^2$ at the start, then $c < 0$, $\sqrt d > |b|$, and line L8 returns a negative time. Check that the initial state is valid, and keep line L23 from scheduling an event before the current time.
- **The wrong sign in the bounce.** Lines L16 and L17 add $J$ to the disk at $r_i$ and subtract it from the disk at $r_j$, with $\Delta r = r_j - r_i$ and $\Delta v = v_j - v_i$. If line L13 uses $\Delta r = r_j - r_i$ with $\Delta v = v_i - v_j$, then $J$ changes sign, the disks attract instead of repel, and they pass through each other.
- **No invalidation.** Without the counts of lines L18 and L29, an old prediction about a disk whose velocity has changed is processed as a real collision.
- **Strict test in line L4.** The test $b > 0$ instead of $b \ge 0$ lets $\Delta v = 0$ through, and line L8 divides by $a = 0$.
- **Rounding at contact.** After a move, two touching disks can overlap by a tiny amount because of rounding. For the pair that just bounced this is harmless, since $b > 0$ after the bounce and line L4 returns $\infty$. For a pair that still approaches, line L8 then returns a small negative time. Clamp such a $\Delta t$ to 0, so that the event is processed at once and not in the past.

## Implementations

## History

Alder and Wainwright described the general method of event-driven [molecular dynamics](/molecular-dynamics/) for hard spheres in 1959: compute the time of the next collision exactly, move all particles to it, and resolve it. Lubachevsky in 1991 gave an efficient scheme for billiards with many particles, with one scheduled event per particle and cells. Sedgewick and Wayne present the version on this page, with lazy deletion by collision counts, as an application of priority queues.

## References
