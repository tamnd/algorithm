---
tag: N39YK7
kind: model
slug: hard-disk-model
name: Hard-disk model
area: foundations/models-of-computation
level: intro
summary: Physical model of particles as hard circles moving in a box, colliding elastically with each other and the walls.
prereqs: [priority-queue]
see_also: [event-driven-simulation, priority-queue, binary-heap, lazy-deletion, spatial-hashing, metropolis-hastings, external-memory-model]
sources:
  - url: "https://algs4.cs.princeton.edu/61event/"
    locator: Section 6.1, Event-driven simulation, on the booksite of Sedgewick and Wayne
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 6.1 (event-driven simulation)
  - paper: "B. J. Alder and T. E. Wainwright, Phase transition for a hard sphere system, Journal of Chemical Physics 27 (1957)"
    locator: page 1208
  - paper: "B. J. Alder and T. E. Wainwright, Studies in molecular dynamics. I. General method, Journal of Chemical Physics 31 (1959)"
    locator: page 459
  - paper: "B. J. Alder and T. E. Wainwright, Phase transition in elastic disks, Physical Review 127 (1962)"
    locator: page 359
  - paper: "Boris D. Lubachevsky, How to simulate billiards and similar systems, Journal of Computational Physics 94 (1991)"
    locator: pages 255 to 283
  - paper: "Nicholas Metropolis, Arianna W. Rosenbluth, Marshall N. Rosenbluth, Augusta H. Teller and Edward Teller, Equation of state calculations by fast computing machines, Journal of Chemical Physics 21 (1953)"
    locator: page 1087
  - paper: "Etienne P. Bernard, Werner Krauth and David B. Wilson, Event-chain Monte Carlo algorithms for hard-sphere systems, Physical Review E 80 (2009)"
    locator: article 056704
  - paper: "E. P. Bernard and W. Krauth, Two-step melting in two dimensions: first-order liquid-hexatic transition, Physical Review Letters 107 (2011)"
    locator: article 155704
---

The hard-disk model is a model from physics: $N$ circles (disks) move in a two-dimensional box, collide elastically with each other and with the walls, and never overlap. On this site it is the standard example of [event-driven simulation](/event-driven-simulation/), where a [priority queue](/priority-queue/) of predicted collisions replaces a fixed time step. The words "hard disk" mean a rigid circle, not a storage device. For the cost model of a storage disk, see the [external memory model](/external-memory-model/).

## The machine

**The system.** Each disk $i$ has a position $p_i$, a velocity $v_i$, a radius $r_i$ and a mass $m_i$. The box is the unit square. The only force is the hard core: the distance between the centres of disks $i$ and $j$ is never less than $r_i + r_j$, and no disk crosses a wall. Between collisions each disk moves in a straight line at constant speed.

**Collisions.** When disk $i$ touches a vertical wall, the sign of the $x$ part of its velocity changes. A horizontal wall changes the $y$ part. When disks $i$ and $j$ touch, they exchange momentum along the line through their centres. With $\sigma$, $\Delta p$ and $\Delta v$ as defined below, measured at the time of contact, the impulse is $J = 2 m_i m_j (\Delta v \cdot \Delta p) / (\sigma (m_i + m_j))$, and the new velocities are $v_i + (J/m_i)\,\Delta p/\sigma$ and $v_j - (J/m_j)\,\Delta p/\sigma$. For equal masses, this swaps the parts of the two velocities along the line through the centres, and the other parts do not change.

**The time of the next collision.** Let $\sigma = r_i + r_j$, $\Delta p = p_j - p_i$ and $\Delta v = v_j - v_i$. The disks do not overlap, so $\Delta p \cdot \Delta p \ge \sigma^2$. They touch at the first time $t \ge 0$ with $|\Delta p + t\,\Delta v| = \sigma$. This is a quadratic equation in $t$. Let
$$d = (\Delta v \cdot \Delta p)^2 - (\Delta v \cdot \Delta v)(\Delta p \cdot \Delta p - \sigma^2).$$
If $\Delta v \cdot \Delta p \ge 0$, the disks do not move toward each other, and they do not collide. If $d < 0$, they pass each other with no contact. Otherwise
$$t = -\frac{\Delta v \cdot \Delta p + \sqrt{d}}{\Delta v \cdot \Delta v}.$$
A wall is simpler: a disk at $x$ with radius $r$ and $v_x > 0$ hits the right wall after $(1 - r - x)/v_x$. If $v_x < 0$, it hits the left wall after $(r - x)/v_x$. If $v_x = 0$, it never hits a vertical wall. The horizontal walls are the same with $y$ in place of $x$.

*Example.* In an open plane, with no walls, two disks of radius $1/2$, so $\sigma = 1$, start at $(0, 0)$ and $(4, 0)$ with velocities $(1, 0)$ and $(-1, 0)$. Then $\Delta p = (4, 0)$, $\Delta v = (-2, 0)$, $\Delta v \cdot \Delta p = -8$, $\Delta v \cdot \Delta v = 4$, $\Delta p \cdot \Delta p = 16$, and $d = 64 - 4 \cdot 15 = 4$. So $t = -(-8 + 2)/4 = 3/2$. This agrees with a direct count: the gap between the centres must close from $4$ to $1$ at a speed of $2$. After the collision the two velocities swap, to $(-1, 0)$ and $(1, 0)$.

## What it counts

A simulation is measured by the work it does for each unit of simulated time. There are two ways to run the system.

**Time-driven simulation.** Move every disk by $v_i\,\Delta t$, then test each pair for overlap, and repeat. Each step costs $\Theta(N^2)$ pair tests, so one unit of time costs $\Theta(N^2/\Delta t)$. A large $\Delta t$ misses collisions: two fast disks can pass through each other between two steps. A small $\Delta t$ makes the simulation slow. No choice of $\Delta t$ is correct for every input.

**Event-driven simulation.** Compute the times of future collisions and jump from one collision to the next. The state between events is known exactly, so no collision is missed. The algorithm keeps a [priority queue](/priority-queue/) of events keyed by time:

1. For each disk, predict its collision with each wall and with each other disk, and insert each event with a finite time. This is $O(N^2)$ predictions.
2. Remove the event with the smallest time $t$.
3. If the event is no longer valid, discard it and go to step 2.
4. Move all disks to time $t$, and change the velocities of the disks in the event.
5. For each disk in the event, predict its new collisions with the walls and with the other disks, and insert them. Go to step 2.

**Invalid events.** A predicted event is no longer valid when a disk in it has had a collision since the prediction, because the path of that disk changed. This holds for a wall event too. The algorithm does not search the queue to remove such events. It stores, with each event, the number of collisions of each disk at the time of the prediction, and in step 3 it compares these numbers with the current ones. This is [lazy deletion](/lazy-deletion/).

**Cost.** With a [binary heap](/binary-heap/), step 1 costs $O(N^2 \log N)$. Each collision adds $O(N)$ events. Invalid events stay in the heap until they reach the top, so after $k$ collisions the heap can hold $\Theta(N^2 + kN)$ events, and an insertion costs $O(\log(N + k))$. At any time at most two events for each pair of disks are valid (one from the prediction of each disk), and at most two for each disk and the walls (one vertical wall and one horizontal wall), so at most $V = N(N-1) + 2N$ events are valid. To keep the heap small, rebuild it from its valid events each time it holds $2V$ events. A rebuild by bottom-up heap construction takes $O(V)$ time and leaves at most $V$ events, so at least $V$ insertions come between two rebuilds, and the rebuilds add $O(1)$ amortized time to each insertion. The heap always holds $O(N^2)$ events, so an insertion costs $O(\log N)$. Each event is inserted once and removed at most once, so the removals of invalid events cost $O(\log N)$ each and can be charged to their insertions. Each collision then costs $O(N \log N)$ amortized. Step 4 costs $O(N)$ in this simple form. Lubachevsky (1991) reduced the cost: each disk keeps its own time, so step 4 moves only the disks in the event, and the box is divided into cells, so a disk predicts collisions only with disks in the cells next to it. A crossing of a cell boundary is one more kind of event. At a fixed density, each event then costs $O(\log N)$ time (see [spatial hashing](/spatial-hashing/) for the grid of cells).

**Cost for each mean free time.** The mean free time is the mean time between two collisions of one disk. In each mean free time, each disk has one collision on average, so the system has $\Theta(N)$ collisions. The simple event-driven method then costs $O(N^2 \log N)$ for each mean free time, and the method of Lubachevsky costs $O(N \log N)$ at a fixed density. In the unit square with a fixed packing fraction, the radius of a disk is $\Theta(N^{-1/2})$, so the mean free time is $\Theta(N^{-1/2})$ for a fixed mean speed. One unit of time then holds $\Theta(N^{3/2})$ collisions, and the simple method costs $O(N^{5/2} \log N)$ for it.

**Rounding.** With floating-point numbers, a predicted time can be slightly earlier than the current time, and two disks can overlap by a tiny amount after a collision. Then a pair can collide again at once, and the simulation can stall. Implementations treat a predicted time slightly before the current time as the current time, and they predict a collision only when $\Delta v \cdot \Delta p < -\varepsilon$ for a small $\varepsilon > 0$.

## Relation to other models

- **Other event-driven systems.** The same loop of remove, check and predict runs any simulation in which the state changes only at discrete events: queues of customers, digital circuits, and network packets. The hard-disk system is the usual teaching example, because the events are easy to compute and easy to see.
- **Monte Carlo.** A second way to study the system does not follow the motion. A step moves one disk by a small random vector and rejects the move if two disks overlap. This is a [Markov chain](/markov-chain/) that samples the legal configurations uniformly, and it is the [Metropolis algorithm](/metropolis-hastings/) for this system. Event-chain Monte Carlo (Bernard, Krauth and Wilson, 2009) moves one disk until it touches another, then continues with the disk it touched, so no move is rejected. It is much faster than the Metropolis algorithm on dense systems.
- **Cost models of this area.** The model is a physical system, not a model of computation. The cost of a simulation of it is measured in the usual way on the [word RAM](/word-ram/), with each floating-point operation counted as one step.

## Known results in the model

- Metropolis, Rosenbluth, Rosenbluth, Teller and Teller (1953) introduced the Metropolis Monte Carlo method on a system of rigid disks in two dimensions.
- Alder and Wainwright (1957) found a transition between a fluid and a solid in a system of hard spheres, and Alder and Wainwright (1959) described the event-driven method of molecular dynamics, which predicts the next collision and jumps to it.
- Alder and Wainwright (1962) used molecular dynamics on hard disks in two dimensions and found a transition between the fluid and the solid.
- Lubachevsky (1991) gave the event-driven algorithm with cells and a time for each disk, with $O(\log N)$ cost for each event at fixed density.
- Bernard and Krauth (2011) used event-chain Monte Carlo and found that the hard-disk system melts in two steps: a first-order transition from the liquid to an intermediate phase, called the hexatic phase, and a continuous transition from the hexatic phase to the solid.

## References
