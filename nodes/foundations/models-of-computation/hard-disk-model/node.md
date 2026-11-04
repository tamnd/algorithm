---
tag: N39YK7
kind: model
slug: hard-disk-model
name: Hard-disk model
area: foundations/models-of-computation
level: intro
summary: Physical model of particles as hard circles moving in a box, colliding elastically with each other and the walls.
prereqs: [priority-queue]
see_also: [event-driven-simulation, collision-prediction-and-resolution, priority-queue, binary-heap, lazy-deletion, spatial-hashing, molecular-dynamics, metropolis-hastings]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Chapter 6, Section 6.1 (event-driven simulation, the classes Particle and CollisionSystem)
  - url: "https://algs4.cs.princeton.edu/61event/"
    locator: Section 6.1, Event-driven simulation, on the booksite of Sedgewick and Wayne
  - paper: doi:10.1016/0021-9991(91)90222-7
    title: Boris D. Lubachevsky, How to simulate billiards and similar systems, Journal of Computational Physics 94(2) (1991)
    locator: pp. 255 to 283 (abstract, the O(log N) cost per event with sectors)
  - paper: "B. J. Alder and T. E. Wainwright, Phase transition for a hard sphere system, Journal of Chemical Physics 27 (1957)"
    locator: pp. 1208 to 1209
  - paper: "B. J. Alder and T. E. Wainwright, Studies in molecular dynamics. I. General method, Journal of Chemical Physics 31 (1959)"
    locator: page 459 onward (the method of predicting the next collision)
  - paper: "B. J. Alder and T. E. Wainwright, Phase transition in elastic disks, Physical Review 127 (1962)"
    locator: page 359 onward
  - paper: doi:10.1063/1.1699114
    title: Nicholas Metropolis, Arianna W. Rosenbluth, Marshall N. Rosenbluth, Augusta H. Teller and Edward Teller, Equation of state calculations by fast computing machines, Journal of Chemical Physics 21 (1953)
    locator: pp. 1087 to 1092 (the method, applied to rigid disks in two dimensions)
  - paper: "Etienne P. Bernard, Werner Krauth and David B. Wilson, Event-chain Monte Carlo algorithms for hard-sphere systems, Physical Review E 80 (2009)"
    locator: article 056704
  - paper: "Etienne P. Bernard and Werner Krauth, Two-step melting in two dimensions: first-order liquid-hexatic transition, Physical Review Letters 107 (2011)"
    locator: article 155704
---

The hard-disk model is a model from physics: $N$ rigid circles (disks) move in a two-dimensional box, collide elastically with each other and with the walls, and never overlap. It is the standard example of [event-driven simulation](/event-driven-simulation/), in which a [priority queue](/priority-queue/) of predicted collisions replaces a fixed time step (Sedgewick and Wayne, Section 6.1). Alder and Wainwright used this kind of simulation from 1957 to study melting, and the two-dimensional system is still a test case of statistical physics. The words "hard disk" mean a rigid circle, not a storage device: for the cost model of a storage disk, see the [external memory model](/external-memory-model/).

## The machine

**The system.** Disk $i$ has a position $p_i \in \mathbb{R}^2$, a velocity $v_i$, a radius $r_i > 0$ and a mass $m_i > 0$. The box is the unit square $[0,1]^2$. The only force is the hard core. At all times $|p_i - p_j| \ge r_i + r_j$ for $i \ne j$, and $r_i \le x_i \le 1 - r_i$ and $r_i \le y_i \le 1 - r_i$, where $p_i = (x_i, y_i)$. Between collisions each disk moves in a straight line at constant speed, $p_i(t) = p_i(0) + t\,v_i$.

**The time of the next collision of two disks.** Write $\sigma = r_i + r_j$, $\Delta p = p_j - p_i$ and $\Delta v = v_j - v_i$, and let $b = \Delta v \cdot \Delta p$, $a = \Delta v \cdot \Delta v$ and $c = \Delta p \cdot \Delta p - \sigma^2 \ge 0$. The disks touch at the first time $t \ge 0$ with $|\Delta p + t\,\Delta v|^2 = \sigma^2$, that is, at the smaller root of

$$a t^2 + 2 b t + c = 0.$$

- If $b \ge 0$, the distance does not decrease at time 0, and because $|\Delta p + t \Delta v|^2$ is a convex function of $t$ it never decreases later. There is no collision.
- Else let $d = b^2 - a c$. If $d < 0$, the quadratic has no real root, and the disks pass each other with no contact.
- Else the disks touch at
$$t = \frac{-b - \sqrt{d}}{a} = \frac{c}{-b + \sqrt{d}}.$$

The two forms are equal because the product of the two roots is $c/a$. The second form is the one to compute (see Pitfalls).

**The time of the next wall collision.** A disk at $x$ with radius $r$ and $v_x > 0$ hits the right wall after $(1 - r - x)/v_x$. If $v_x < 0$, it hits the left wall after $(r - x)/v_x$. If $v_x = 0$, it never hits a vertical wall. The horizontal walls work the same way with $y$.

**Collisions.** At a vertical wall, $v_x$ changes sign. At a horizontal wall, $v_y$ changes sign. When disks $i$ and $j$ touch, so that $|\Delta p| = \sigma$, they exchange momentum along the line through their centres. The impulse is

$$J = \frac{2 m_i m_j\,(\Delta v \cdot \Delta p)}{\sigma (m_i + m_j)},$$

and the new velocities are $v_i + \frac{J}{m_i}\frac{\Delta p}{\sigma}$ and $v_j - \frac{J}{m_j}\frac{\Delta p}{\sigma}$ (Sedgewick and Wayne, Section 6.1). This keeps the total momentum and the total kinetic energy. For equal masses, the two disks swap the parts of their velocities along the line through the centres, and the other parts do not change.

**Example: a head-on collision.** In an open plane, two disks of radius $1/2$ and mass 1 start at $(0, 0)$ and $(4, 0)$ with velocities $(1, 0)$ and $(-1, 0)$. Then $\sigma = 1$, $b = -8$, $a = 4$, $c = 15$ and $d = 64 - 60 = 4$, so $t = 15/(8 + 2) = 3/2$. The gap between the centres closes from 4 to 1 at a speed of 2, which also gives $3/2$. After the collision the velocities are $(-1, 0)$ and $(1, 0)$.

**Example: an oblique collision.** Disk $i$ starts at $(0, 0)$ with velocity $(1, 0)$, and disk $j$ is at rest at $(2.6, 0.8)$. Both have radius $1/2$ and mass 1. Then $b = -2.6$, $a = 1$, $c = 6.4$ and $d = 0.36$, so $t = 6.4/(2.6 + 0.6) = 2$. At $t = 2$, disk $i$ is at $(2, 0)$, so $\Delta p = (0.6, 0.8)$ and $\Delta v \cdot \Delta p = -0.6$. Then $J = -0.6$, the new velocities are $v_i = (0.64, -0.48)$ and $v_j = (0.36, 0.48)$. Their sum is $(1, 0)$, the sum of the squared speeds is $0.64 + 0.36 = 1$, and the two velocities are perpendicular, as they must be for equal masses when one disk starts at rest.

## What it counts

A simulation is measured by the work it does per unit of simulated time, on a [word RAM](/word-ram/) with each floating-point operation counted as one step. There are two ways to run the system.

**Time-driven simulation.** Move every disk by $v_i\,\Delta t$, test each pair for overlap, and repeat. A step costs $\Theta(N^2)$ pair tests, so one unit of time costs $\Theta(N^2/\Delta t)$. A large $\Delta t$ misses collisions. Example: two disks of radius $0.01$ at $x = 0$ and $x = 0.06$ on the same line move toward each other at speeds 1 and $-1$, and $\Delta t = 0.05$. They touch at $t = 0.02$. At $t = 0.05$ their centres are at $0.05$ and $0.01$, at distance $0.04 > 0.02$, so the test finds no overlap, and the disks have passed through each other. A small $\Delta t$ makes the simulation slow, and no fixed $\Delta t$ is correct for every input.

**Event-driven simulation.** Compute the times of future collisions and jump from one collision to the next. The state between events is known exactly, so no collision is missed. The algorithm keeps a [priority queue](/priority-queue/) of events keyed by time.

1. For each disk, predict its collision with each wall and with each other disk, and insert each event with a finite time. This is $O(N^2)$ predictions.
2. Remove the event with the smallest time $t$.
3. If the event is no longer valid, discard it and go to step 2.
4. Move all disks to time $t$, and change the velocities of the disks in the event.
5. For each disk in the event, predict its new collisions with the walls and with all other disks, and insert them. Go to step 2.

**Invalid events.** A predicted event is no longer valid when one of its disks has had a collision since the prediction, because the path of that disk changed. The algorithm does not search the queue to remove such events. It stores, with each event, the collision count of each of its disks at the time of the prediction, and in step 3 it compares them with the current counts. This is [lazy deletion](/lazy-deletion/).

**Cost of the simple method.** With a [binary heap](/binary-heap/), step 1 costs $O(N^2 \log N)$. Each collision inserts $O(N)$ events. Invalid events stay in the heap until they reach the top. At any time, at most two valid events exist for each pair of disks (the two predictions of step 1, and later only the prediction made at the last collision of either disk), and at most two for each disk and the walls (one vertical and one horizontal wall). So at most $V = N(N-1) + 2N$ events are valid. To keep the heap small, rebuild it from its valid events each time it holds $2V$ events. A rebuild by bottom-up [heap construction](/heap-construction/) takes $O(V)$ time and leaves at most $V$ events, so at least $V$ insertions happen between two rebuilds, and the rebuilds add $O(1)$ amortized time to each insertion. The heap then always holds $O(N^2)$ events, and an insertion or a removal costs $O(\log N)$. Each event is removed at most once, so the removal of an invalid event can be charged to its insertion. Each collision therefore costs $O(N \log N)$ amortized time for the predictions, plus $O(N)$ for step 4.

**Cost of the cell method.** Lubachevsky (1991) gave each disk its own time, so that step 4 moves only the disks in the event, and divided the box into sectors (cells), so that a disk predicts collisions only with the disks in nearby cells. A crossing of a cell boundary is one more kind of event. If the disks are spread evenly enough that each cell and its neighbours hold $O(1)$ disks, each event costs $O(\log N)$ time. See [spatial hashing](/spatial-hashing/) for the grid of cells.

**Cost per unit of time.** The *mean free time* is the mean time between two collisions of one disk. In one mean free time the system has $\Theta(N)$ collisions. Fix the packing fraction (the fraction of the box covered by disks) below the jamming density and fix the mean speed. Then the radius of a disk is $\Theta(N^{-1/2})$, the mean free path is $\Theta(1/(N \cdot N^{-1/2})) = \Theta(N^{-1/2})$, and so is the mean free time. One unit of time then holds $\Theta(N^{3/2})$ collisions. The simple method costs $O(N^{5/2} \log N)$ for it, and the cell method costs $O(N^{3/2} \log N)$.

## Relation to other models

- **Other event-driven systems.** The same loop of remove, check and predict runs any simulation in which the state changes only at discrete events: queues of customers, digital circuits and network packets. The hard-disk system is the usual teaching example, because its events are easy to compute and easy to see. See [collision prediction and resolution](/collision-prediction-and-resolution/).
- **Molecular dynamics.** Hard disks and hard spheres are the simplest systems of [molecular dynamics](/molecular-dynamics/). With smooth forces, such as the Lennard-Jones force, the motion between events is not a straight line, and simulations integrate it with a time step instead.
- **Monte Carlo.** A second way to study the system does not follow the motion. A step moves one random disk by a small random vector and rejects the move if two disks would overlap. This is a [Markov chain](/markov-chain/) whose stationary distribution is uniform on the legal configurations that it can reach, and it is the [Metropolis algorithm](/metropolis-hastings/) for this system. Event-chain Monte Carlo (Bernard, Krauth and Wilson 2009) moves one disk in a fixed direction until it touches another, then goes on with the disk that it touched, so no move is rejected. The authors report much faster convergence than the local Metropolis algorithm in dense systems.
- **Cost models of this area.** The hard-disk model is a physical system, not a model of computation. It is on this page list because its simulation is a standard exercise in the cost of event-driven algorithms.

## Known results in the model

- Metropolis, Rosenbluth, Rosenbluth, Teller and Teller (1953) introduced the Metropolis Monte Carlo method, and applied it first to a system of rigid disks in two dimensions.
- Alder and Wainwright (1957) found a transition between a fluid and a solid in a system of hard spheres with event-driven molecular dynamics. Their 1959 paper describes the general method, which predicts the next collision and jumps to it.
- Alder and Wainwright (1962) found a transition between a fluid and a solid for hard disks in two dimensions.
- Lubachevsky (1991) gave the event-driven algorithm with cells and a separate time for each disk, with $O(\log N)$ cost per event when the disks are spread evenly.
- Sedgewick and Wayne (Section 6.1) give the event-driven algorithm with a binary heap and collision counts for lazy deletion, as described above.
- Bernard and Krauth (2011) used event-chain Monte Carlo on systems of about one million disks and found that hard disks melt in two steps: a first-order transition from the liquid to the *hexatic* phase, and a continuous transition from the hexatic phase to the solid.

### Pitfalls

- **The name.** "Hard disk" here means a rigid circle. The cost model of disk storage is the [external memory model](/external-memory-model/).
- **A fixed time step.** A time-driven loop misses collisions between fast or small disks, as in the example with $\Delta t = 0.05$ above, and the disks pass through each other.
- **Cancellation in the collision time.** The form $(-b - \sqrt{d})/a$ subtracts two nearly equal numbers when $c$ is small, which happens when two disks are close. With $a = 1$, $b = -1$ and $c = 10^{-12}$ in double precision, it gives $t$ with a relative error of about $9 \times 10^{-5}$, while $c/(-b + \sqrt{d})$ gives a relative error of about $10^{-17}$. See [numerical stability](/numerical-stability/) and the [quadratic formula](/quadratic-formula/).
- **Rounding at contact.** After a collision, rounding can leave two disks overlapping by a tiny amount, with $c < 0$. The formula then gives a collision at a time slightly before now, and the pair collides again and again. Implementations predict a collision only when $b < -\varepsilon$ for a small $\varepsilon > 0$, and they treat a predicted time slightly before the current time as the current time.
- **Forgetting to invalidate.** Each collision must increase the collision count of each disk in it, wall collisions included. Without this, the queue returns events for paths that no longer exist.
- **Predicting against everything after each event.** The simple method predicts against all $N - 1$ other disks after each collision. For large $N$ this dominates the cost. Use cells, and add the cell-crossing events.
- **Simultaneous events.** Two events can have the same time, for example a disk that touches two others at once. Process them one at a time in a fixed order. The second event is then usually invalid and is discarded, and its pair is predicted again from the new velocities.

## References
