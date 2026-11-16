---
tag: TK3VSR
kind: algorithm
slug: ando-circumcenter-algorithm
name: Ando's circumcenter algorithm
aliases:
- Ando-Oasa-Suzuki-Yamashita algorithm
area: robotics/multi-robot-systems
level: advanced
summary: Each robot moves toward the center of the smallest circle around the robots it sees, only as far as keeps every link, so a connected group converges to one point.
solves: [multi-robot-rendezvous]
model: real-ram
complexity:
  vars: {r: the number of robots, m: the number of pairs of robots that see each other, k: the number of rounds}
  time: {per_round: O(r + m) expected, total: O(k (r + m)) expected}
  space: {extra: O(r)}
properties: {deterministic: true, randomized: false, online: true}
history:
  year: 1999
  people: [Hideki Ando, Yoshinobu Oasa, Ichiro Suzuki, Masafumi Yamashita]
  note: Ando, Oasa, Suzuki and Yamashita gave the rule for oblivious robots with a limited visibility radius and proved convergence to a point. Cortes, Martinez and Bullo extended it to any dimension in 2006.
prereqs: [multi-robot-rendezvous, minimum-enclosing-circle]
see_also: [minimum-enclosing-circle, connectivity-maintenance, laplacian-consensus-protocol, convex-hull, synchronous-model, swarm-robotics, random-geometric-graph, lasalle-invariance-principle]
sources:
  - paper: doi:10.1109/70.795787
    title: Hideki Ando, Yoshinobu Oasa, Ichiro Suzuki and Masafumi Yamashita, Distributed memoryless point convergence algorithm for mobile robots with limited visibility, IEEE Transactions on Robotics and Automation 15(5), 1999
    locator: pages 818 to 828 (the algorithm, the disks around the midpoints, and convergence to a point)
  - paper: doi:10.1109/TAC.2006.878713
    title: Jorge Cortes, Sonia Martinez and Francesco Bullo, Robust rendezvous for mobile autonomous agents via proximity graphs in arbitrary dimensions, IEEE Transactions on Automatic Control 51(8), 2006
    locator: pages 1289 to 1298 (circumcenter algorithms in any dimension, constraint sets that keep the links, and convergence through an invariance principle)
  - paper: doi:10.1109/TAC.2007.908304
    title: Sonia Martinez, Francesco Bullo, Jorge Cortes and Emilio Frazzoli, On synchronous robotic networks, Part II, Time complexity of rendezvous and deployment algorithms, IEEE Transactions on Automatic Control 52(12), 2007
    locator: pages 2214 to 2226 (the number of synchronous rounds of the circumcenter algorithm)
  - book: isbn:9780691141954
    title: Francesco Bullo, Jorge Cortes and Sonia Martinez, Distributed Control of Robotic Networks, Princeton University Press, 2009
    locator: Chapter 4, Connectivity maintenance and rendezvous
---

Ando's circumcenter algorithm solves [rendezvous](/multi-robot-rendezvous/) for robots that see only the robots within a fixed distance $V$, have no memory, no identifiers, no common compass and no communication. In each round a robot looks at the robots it sees, computes the center of their [smallest enclosing circle](/minimum-enclosing-circle/), and moves toward that center. It stops early if it would otherwise move out of the disk of radius $V/2$ around the midpoint between itself and any robot it sees. The two robots of a pair use the same disk, so every pair that sees each other at the start still sees each other after every round, and a group whose visibility graph is connected stays connected. Ando, Oasa, Suzuki and Yamashita proved in 1999 that the robots converge to one point.

## In plain words

Some small robots stand in a field. Each robot sees only the robots near it. The robots must all come to the same place, but they have no map, no radio and no memory.

Each robot draws the smallest circle around itself and the robots it sees, and walks toward the middle of that circle. This pulls the outer robots in and leaves robots in the middle where they are.

There is one danger. If a robot walks too far, it can lose sight of a friend, and then the group can split. So each robot also draws, for each friend it sees, a small safe circle halfway between the two of them. It walks only as far as it stays inside every safe circle. The friend uses the same circle, so the two can never get too far apart. Step by step the group shrinks to one point.

## The problem

**The model.** There are $r$ point robots in the plane at positions $p_1, \dots, p_r$, and a visibility radius $V > 0$. Robot $i$ sees robot $j$ when $\lVert p_i - p_j \rVert \le V$; the pairs that see each other are the $m$ edges of the visibility graph, a disk graph like the [random geometric graph](/random-geometric-graph/). Robots work in rounds of look, compute and move. In the synchronous model all robots are active in every round. In the semi-synchronous model of Ando et al. an arbitrary subset is active in each round, every robot is active in infinitely many rounds, and the active robots look at the same moment and reach their targets before the next round. The robots are oblivious: the target depends only on the positions seen in the current round.

**Input.** The positions $p_1, \dots, p_r$, the radius $V$, and the number $K$ of rounds.

**Output.** The positions after $K$ rounds. The goal is that the positions converge to one point when the visibility graph at the start is connected.

**How it differs from close pages.** The [Laplacian consensus protocol](/laplacian-consensus-protocol/) also brings robots together, but it assumes a fixed graph. When the graph comes from distances, its averaging step can break links and split the group. The circumcenter step keeps every link, which is the [connectivity maintenance](/connectivity-maintenance/) property, without any extra term in the control.

## The algorithm

```pseudo id=main
ANDO(p, V, K)
L1  for k = 1 to K do
L2      choose the active robots A                   ▷ all robots in the synchronous model
L3      for each i ∈ A, in parallel: S_i ← { j : ‖p_i - p_j‖ ≤ V }     ▷ i ∈ S_i
L4          c ← center of the smallest enclosing circle of { p_j : j ∈ S_i }
L5          t ← 1
L6          for each j ∈ S_i with j ≠ i do
L7              m ← (p_i + p_j) / 2
L8              t ← min(t, largest s ∈ [0, 1] with ‖p_i + s (c - p_i) - m‖ ≤ V/2)
L9          p_i' ← p_i + t (c - p_i)
L10     all active robots move to p_i' at the same time; return p
```

Line L4 uses Welzl's randomized incremental method, which takes expected linear time in the number of points; see [minimum enclosing circle](/minimum-enclosing-circle/). Line L8 solves a quadratic equation in $s$. Since $\lVert p_i - m \rVert = \lVert p_i - p_j \rVert / 2 \le V/2$, the value $s = 0$ is always allowed, so the robot never has to move backward. Robots that are not active keep their positions. Each robot uses only relative positions, so the rule does not need a common frame or a common unit of direction.

## Example

**Four robots on a line.** Let $V = 1$ and the robots stand at $0, 1, 2, 3$ on a line. Robot 1 sees only robot 2, so its circle has the center $0.5$, the midpoint of the two. The middle robots see both of their neighbors and stay. No safe disk cuts a step in this example.

| round | robot 1 | robot 2 | robot 3 | robot 4 |
|---|---|---|---|---|
| 0 | 0 | 1 | 2 | 3 |
| 1 | 0.5 | 1 | 2 | 2.5 |
| 2 | 0.75 | 1.25 | 1.75 | 2.25 |
| 3 | 1.25 | 1.5 | 1.5 | 1.75 |
| 4 | 1.5 | 1.5 | 1.5 | 1.5 |

In round 3 all robots see each other except the two end robots, which are 1.5 apart. In round 4 every robot sees every other one, and all robots go to the center $1.5$.

**Five robots in the plane.** Let $V = 1$ and the robots stand at $(0, 0)$, $(0.9, 0)$, $(1.7, 0.4)$, $(1.2, 1.2)$ and $(0.2, 0.9)$. The visibility graph is the path $5 - 1 - 2 - 3 - 4$ with lengths $0.922$, $0.9$, $0.8944$ and $0.9434$, and the diameter is $1.7464$.

| round | robot 1 | robot 2 | robot 3 | robot 4 | robot 5 | diameter | edges |
|---|---|---|---|---|---|---|---|
| 0 | (0, 0) | (0.9, 0) | (1.7, 0.4) | (1.2, 1.2) | (0.2, 0.9) | 1.7464 | 4 |
| 1 | (0.45, 0.3722) | (0.85, 0.2) | (1.1071, 0.5857) | (1.45, 0.8) | (0.1, 0.45) | 1.3946 | 7 |
| 2 | (0.6036, 0.5179) | (0.775, 0.625) | (0.95, 0.5861) | (1.15, 0.5) | (0.475, 0.325) | 0.6973 | 10 |
| 3 | (0.8125, 0.4125) | (0.8125, 0.4125) | (0.8125, 0.4125) | (0.8125, 0.4125) | (0.8125, 0.4125) | 0 | 10 |

The graph gains edges in every round and loses none. After round 2 all robots see each other, so in round 3 they all compute the same circle and move to its center $(0.8125, 0.4125)$.

**A safe disk that cuts the step.** Let $V = 1$, robot 1 at $(0, 0)$, and three robots at $(-0.97, 0.21)$, $(0.17, -0.71)$ and $(0.94, 0.32)$, at distances $0.9925$, $0.7301$ and $0.993$. The smallest enclosing circle of the four has the center $(-0.013, 0.2296)$ and the radius $0.9572$. The safe disk of robot $(0.17, -0.71)$ has the center $(0.085, -0.355)$ and the radius $0.5$, and the center of the circle is outside it. Line L8 gives $t \approx 0.594$, so robot 1 moves only to about $(-0.0077, 0.1363)$, on the border of that disk.

## Correctness

The [proof](proofs/correctness/) shows four facts. First, the step of line L8 is well defined, because each safe disk contains the start point of the robot. Second, every pair that sees each other before a round sees each other after it: both robots end in the same disk of radius $V/2$, and robots that do not move are in it already. Third, the center of a smallest enclosing circle lies in the [convex hull](/convex-hull/) of the points, so the new positions lie in the convex hull of the old ones, and the diameter of the group and the radius of its enclosing circle never grow. Fourth, if the whole group fits in a circle of radius $V/2$, all robots meet at its center in one synchronous round.

That the diameter goes to zero is harder. Ando et al. (1999) proved convergence to a point in the semi-synchronous model, and Cortés, Martínez and Bullo (2006) gave a proof with an invariance principle for set-valued maps, in the style of the [LaSalle invariance principle](/lasalle-invariance-principle/), that holds in any dimension.

## Complexity

- **Per robot and round.** If the robot knows the $d_i$ robots it sees, line L4 takes expected $O(d_i)$ time and lines L6 to L8 take $O(d_i)$ time in the [real RAM](/real-ram/) model. One synchronous round costs expected $O(r + m)$ in total. The implementation finds the visible robots by checking all robots, which costs $O(r^2)$ per round.
- **Rounds.** Martínez, Bullo, Cortés and Frazzoli (2007) show that the synchronous circumcenter algorithm on a line needs $\Theta(r)$ rounds. The runs of the implementation on robots at unit spacing with $V = 1$ needed 1, 2, 4, 5, 8, 9, 12, 13, 15, 16 and 19 rounds for $r = 2, \dots, 12$, which is a measurement and not a bound.
- **Space.** Each robot stores $O(d_i)$ numbers during one round and nothing between rounds.

## Properties

- **Oblivious and local.** The step uses only the positions seen in the current round.
- **Keeps every link.** A pair that sees each other never loses sight, in the synchronous and the semi-synchronous model.
- **Contracting.** The group never leaves its convex hull, so its diameter does not grow.
- **Invariant under rigid motion and scaling.** If the positions and $V$ are rotated, moved or scaled, the targets change in the same way, so robots need no common compass.
- **Not average preserving.** The meeting point depends on the shape of the group, not on the mean of the start positions.
- **Fixed point.** Robots that are all at one point stay there.

## Variants and improvements

- **Any dimension.** Cortés, Martínez and Bullo (2006) used the same rule in $\mathbb{R}^d$, with the safe disks replaced by balls, and also with other proximity graphs.
- **Constraint sets.** The step can be taken toward the circumcenter of the visible robots inside any convex set that keeps the links, not only the intersection of the disks around midpoints.
- **Asynchronous robots.** With fully asynchronous robots, where a robot can move on old observations, the same guarantees need further assumptions, and the gathering literature of distributed computing treats this case.
- **Rendezvous with limited sensing.** Lin, Morse and Anderson (2007) studied rendezvous of agents with a sensing radius, in a synchronous and an asynchronous part, with rules of the same kind; see [rendezvous](/multi-robot-rendezvous/).

## When to use it

Use it when the robots must meet, see only nearby robots, have no communication and no common frame, and must not split into groups. Use the [Laplacian consensus protocol](/laplacian-consensus-protocol/) when the communication graph is fixed and does not depend on distances, or when the meeting point must be the average of the start positions.

## Pitfalls

- **Skipping the safe disks.** If a robot moves straight to the center of its circle, a robot at the edge of the group can lose sight of its only neighbor, and the group splits.
- **A disconnected start.** Each connected group meets on its own, and the groups never join.
- **Rounding.** The test $\lVert p_i - p_j \rVert \le V$ is at the border for pairs at distance exactly $V$. Use a small tolerance in both the visibility test and line L8, or a pair at distance $V$ can be lost by rounding.
- **Slow on lines.** On long thin groups the number of rounds grows with $r$, because the end robots move only a little in each round.
- **Not the finite time gathering of distributed computing.** Results there ask that robots reach the same point in finite time; the guarantee proved here is convergence.

## Implementations

## History

Ando, Oasa, Suzuki and Yamashita published the algorithm in 1999, for anonymous and oblivious robots with limited visibility in a semi-synchronous model, and proved convergence to a point. Cortés, Martínez and Bullo (2006) studied a family of circumcenter rules of this kind, proved their convergence in any dimension, and showed that they are robust. Martínez, Bullo, Cortés and Frazzoli (2007) counted the rounds in the synchronous model. The book of Bullo, Cortés and Martínez (2009) treats the algorithm in its chapter on rendezvous.

## References
