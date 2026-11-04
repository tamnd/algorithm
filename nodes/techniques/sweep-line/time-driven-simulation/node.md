---
tag: WBCPCC
kind: technique
slug: time-driven-simulation
name: Time-driven simulation
area: techniques/sweep-line
level: intro
summary: Simulation method that advances the system in fixed small time steps and checks for events at each step.
prereqs: [hard-disk-model, euler-method]
see_also: [event-driven-simulation, collision-prediction-and-resolution, collision-detection, numerical-integration, molecular-dynamics, verlet-integration, uniform-grid]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 6.1, Event-driven simulation (the discussion of time-driven simulation that opens the section)
  - paper: "L. Verlet, Computer \"experiments\" on classical fluids. I. Thermodynamical properties of Lennard-Jones molecules, Physical Review 159(1) (1967), doi:10.1103/PhysRev.159.98"
    locator: pages 98 to 103
---

Time-driven simulation advances a system by a fixed time step $\Delta t$: at each step it moves every object by $\Delta t$, then checks the new state for events such as overlaps and fixes them. It is the simplest way to simulate motion, and it is the natural method when objects feel forces that change at every instant. For colliding particles it has two costs that the [event-driven simulation](/event-driven-simulation/) avoids: a check of all pairs at each step, and collisions that it misses or detects late when $\Delta t$ is too large. Sedgewick and Wayne use it as the starting point for their particle-collision simulation.

## In plain words

Think of a film camera. It takes one picture every small interval of time, and between two pictures it sees nothing. A time-driven simulation works the same way. It moves each object a little, as if time had jumped forward by one interval. Then it looks at the new picture and asks whether two objects now overlap.

If the interval is small, the picture changes only a little at each step, and the program catches each collision soon after it happens. But it needs many pictures, and each picture has a cost for each pair of objects. If the interval is large, two fast objects can pass through each other between two pictures, and the program never sees the collision. The choice of the interval is a trade between speed and accuracy.

## When it applies

- The objects feel forces (gravity, springs, electric charges) that change all the time, so the path between events has no closed form, and a numerical integrator must advance the state anyway.
- Events are frequent compared with the step: each object interacts at almost every step, so jumping from event to event would save little.
- A display or a control loop needs the state at regular times, as in games and real-time physics.
- An approximate answer is acceptable, and the error can be made small by a smaller step.

When the objects move freely between rare, exact events (hard disks, billiard balls, queues with arrival and service times), use the [event-driven simulation](/event-driven-simulation/) instead.

## The template

```pseudo id=main
TIME-DRIVEN-SIMULATION(state, Δt, T)
L1  t ← 0
L2  while t < T do
L3      ADVANCE(state, Δt)                ▷ hole: move each object by one step
L4      t ← t + Δt
L5      for each pair (i, j) of objects do
L6          if OVERLAP(state, i, j) then  ▷ hole: the event test
L7              RESOLVE(state, i, j)      ▷ hole: fix the event that was found
L8      for each object i do
L9          handle the boundary of i      ▷ hole: walls, periodic box, absorption
L10     OUTPUT(state, t)                  ▷ hole: draw, record, or measure
```

The holes are the parts that change from one use to another.

- **ADVANCE** moves the state by $\Delta t$. For particles with no forces, $r \leftarrow r + \Delta t\, v$ is exact. With forces it is a step of an integrator: the [Euler method](/euler-method/) sets $r \leftarrow r + \Delta t\, v$ and $v \leftarrow v + \Delta t\, a(r)$, with a global error of order $\Delta t$; [Verlet integration](/verlet-integration/) and the [symplectic Euler method](/symplectic-euler-method/) keep the energy close to constant over long runs. See [numerical integration](/numerical-integration/).
- **OVERLAP** detects an event that has already happened: for disks, $|r_j - r_i| < s_i + s_j$.
- **RESOLVE** repairs the event, for example by an elastic bounce as in [collision prediction and resolution](/collision-prediction-and-resolution/), often after pushing the two objects apart.
- **Boundary**: a disk with $r_x < s$ or $r_x > 1 - s$ is outside the box and reverses $v_x$.

The loop of lines L5 to L7 tests all $n(n-1)/2$ pairs. The run has $\lceil T/\Delta t \rceil$ steps, so the total cost is $\Theta\big((T/\Delta t)\, n^2\big)$ for the collision checks, plus the cost of ADVANCE. The cost grows when $\Delta t$ shrinks, whatever the number of collisions.

## Classic examples

### Hard disks in a box (Sedgewick and Wayne, Section 6.1)

This is the [hard-disk model](/hard-disk-model/) with ADVANCE as a straight move, OVERLAP as the distance test, and RESOLVE as a bounce. Sedgewick and Wayne point out three faults. There are $n^2$ overlap checks per step. The step must be very small, which slows the simulation. And a collision can be missed when two disks do not overlap at any of the times when the program looks.

**A worked case of tunnelling.** Two disks of radius $0.01$ (so $\sigma = 0.02$) lie on the line $y = 0.5$, with centres at $x = 0.40$ and $x = 0.47$, and move toward each other with $v_x = 1$ and $v_x = -1$. The gap between the centres at time $t$ is $0.07 - 2t$. They touch at $t = 0.025$, and on straight paths they overlap while $|0.07 - 2t| < 0.02$, that is, for $0.025 < t < 0.045$, a window of length $2\sigma/|\Delta v| = 0.02$.

| $\Delta t$ | sample times | gaps $x_2 - x_1$ at the samples | result |
|---|---|---|---|
| 0.01 | 0.01, 0.02, 0.03 | 0.05, 0.03, 0.01 | overlap found at $t = 0.03$, depth 0.01, 0.005 after the contact |
| 0.03 | 0.03 | 0.01 | overlap found at $t = 0.03$, the same depth |
| 0.05 | 0.05, 0.10 | $-0.03$, $-0.13$ | no sample overlaps: the disks pass through each other |

With $\Delta t = 0.05$ the disks swap sides and never collide. With $\Delta t = 0.01$ the program finds the collision, but the disks overlap by half the sum of the radii, and the bounce happens at the wrong time and place. For a head-on approach at relative speed $u$ every collision is seen when $\Delta t$ is less than the window $2\sigma/u$. A glancing collision has a shorter window, down to 0 for disks that only graze, so no fixed step catches every collision.

**The cost.** With $n = 1000$ disks there are $n(n-1)/2 = 499{,}500$ pair checks per step. A run to $T = 10$ with $\Delta t = 0.001$ has 10,000 steps, so about $5 \times 10^9$ checks, whether the disks collide or not.

### Molecular dynamics with continuous forces

In [molecular dynamics](/molecular-dynamics/) with a smooth potential such as Lennard-Jones, the force on each atom changes at each instant, so there are no discrete events to predict. The standard method is time-driven, with a fixed step and an integrator such as [Verlet integration](/verlet-integration/); Verlet used it in 1967 for a fluid of Lennard-Jones atoms. The pair loop becomes a force sum, and at a bounded density, a cut-off radius with neighbour lists or [cells](/uniform-grid/) brings it near $O(n)$ per step.

### Games and real-time physics

A game engine advances its world at a fixed rate, such as 60 steps per second, and runs [collision detection](/collision-detection/) on each frame. A broad phase with a [uniform grid](/uniform-grid/), [spatial hashing](/spatial-hashing/) or a [bounding volume hierarchy](/bounding-volume-hierarchy/) replaces the all-pairs loop. Fast objects such as bullets use a swept test between two frames, which is a local form of collision prediction.

### Integration of an ordinary differential equation

The [Euler method](/euler-method/) for $y' = f(t, y)$ is a time-driven simulation with ADVANCE $= y \leftarrow y + \Delta t\, f(t, y)$ and no events. For $y' = -y$, $y(0) = 1$ and $\Delta t = 0.1$, ten steps give $0.9^{10} \approx 0.3487$ against the exact $e^{-1} \approx 0.3679$. With $\Delta t = 0.01$, a hundred steps give $0.99^{100} \approx 0.3660$. The error falls about in proportion to the step.

## Variations

- **Sub-stepping.** Split each step into smaller steps for the fast objects only, or when an overlap is found, step back and repeat with a smaller $\Delta t$.
- **Adaptive steps.** Choose $\Delta t$ at each step from the largest speed: with $\Delta t \le \sigma_{\min}/u_{\max}$, where $u_{\max}$ bounds the relative speed of two objects and $\sigma_{\min}$ is the smallest sum of radii, a head-on pass cannot be missed; glancing pairs can still be missed, as above.
- **Continuous collision detection.** For each pair close enough to matter, solve for the contact time inside the step, as in [collision prediction](/collision-prediction-and-resolution/). This mixes the time-driven loop with event-driven prediction.
- **Back-off.** After an overlap, move the two objects back along their velocities to the contact time, bounce them, and move them forward again for the rest of the step.
- **Neighbour structures.** Replace lines L5 to L7 by a grid or a hash of cells, so that each object is tested only against nearby objects.

## Pitfalls

- **Tunnelling.** A step that is long compared with the time two objects spend overlapping lets them pass through each other unseen. The worked case above has a window of 0.02 and a step of 0.05.
- **Detection after the fact.** OVERLAP finds a collision only after the objects interpenetrate. A bounce at the detected position is at the wrong place, and with a small relative speed the two objects can still overlap after the bounce, bounce again at the next step and stick together. Separate them or bounce only when they approach ($\Delta v \cdot \Delta r < 0$).
- **The step in the cost.** Halving $\Delta t$ doubles the number of steps, and each step costs $\Theta(n^2)$ with the all-pairs loop, even when nothing happens.
- **Energy drift.** The forward Euler method does not keep the energy of an oscillator: for $x'' = -x$ each step multiplies the energy by $1 + \Delta t^2$. Over long runs, use a symplectic integrator such as Verlet.
- **Order of updates.** Testing pairs while some objects have already moved to the next step mixes two times. Move every object first (line L3), then test (lines L5 to L7).
- **Floating time.** Adding $\Delta t$ many times accumulates rounding. Compute $t$ as $k \Delta t$ from the step count $k$.

## Exercises

1. Two disks of radius $s$ approach head-on with relative speed $u$. Show that a fixed step $\Delta t$ always finds their overlap when $\Delta t < 4s/u$, and give a start position that makes it miss with $\Delta t = 4s/u$.
2. Give two disks whose paths overlap for a time shorter than any chosen $\Delta t > 0$. Conclude that no fixed step detects every collision.
3. For $x'' = -x$ with $x(0) = 1$, $x'(0) = 0$, show that one step of forward Euler multiplies $x^2 + x'^2$ by $1 + \Delta t^2$, and compute the energy after $1/\Delta t$ steps as $\Delta t \to 0$.
4. Compare the number of pair checks of a time-driven simulation with $\Delta t = 10^{-3}$ and the number of predictions of an event-driven simulation, for 100 disks that collide 10 times per unit of time in total, over 100 units of time.

## References
