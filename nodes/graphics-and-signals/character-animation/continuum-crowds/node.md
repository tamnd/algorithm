---
tag: RXA6V1
kind: algorithm
slug: continuum-crowds
name: Continuum crowds
aliases:
- continuum crowd simulation
area: graphics-and-signals/character-animation
level: advanced
summary: "Steer large crowds by a dynamic potential field on a grid, solved by fast marching from the goals with a cost that depends on density and speed."
model: real-ram
complexity:
  vars: {g: the number of grid cells, n: the number of people, k: the number of groups}
  time: {fast_march: O(g log g), step: O(k g log g + n^2)}
  space: {extra: O(g + n)}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 2006
  people: [Adrien Treuille, Seth Cooper, Zoran Popović]
  note: "Treuille, Cooper and Popović presented continuum crowds at SIGGRAPH 2006."
prereqs: [fast-marching-method, eikonal-equation, social-force-model]
see_also: [upwind-scheme, level-set-method, dijkstra, boids, reciprocal-velocity-obstacles, optimal-reciprocal-collision-avoidance, uniform-grid, particle-system]
sources:
  - paper: doi:10.1145/1141911.1142008
    title: "Adrien Treuille, Seth Cooper and Zoran Popović, Continuum crowds, ACM Transactions on Graphics 25(3) (SIGGRAPH 2006), 1160-1168"
    locator: "Section 3 (the unit cost and the potential), Section 3.2 (Eq. 7 to Eq. 10, density, terrain speed, flow speed and their blend), Section 4.1 (the density splat), Section 4.2 (the costs at the cell one moves into), Section 4.3 (fast marching and Eq. 11), Section 4.4 (the advection) and Section 4.5 (the minimum distance)"
  - paper: doi:10.1109/9.412624
    title: "John N. Tsitsiklis, Efficient algorithms for globally optimal trajectories, IEEE Transactions on Automatic Control 40(9), 1528-1538, 1995"
    locator: the Dijkstra like method for the discrete eikonal equation that the paper follows
  - paper: doi:10.1073/pnas.93.4.1591
    title: "James A. Sethian, A fast marching level set method for monotonically advancing fronts, Proceedings of the National Academy of Sciences 93(4), 1591-1595, 1996"
    locator: the fast marching method with the upwind update and a heap
---

Continuum crowds moves a large crowd by a field over the whole space instead of by rules for each person.
The people form groups, and all people of a group share a goal.
At each time step, the method spreads the people onto a grid as a density and a mean velocity.
From these it gets, for every cell and direction, the speed at which a person can walk there: the free walking speed where the crowd is thin, the speed of the crowd where it is dense.
A unit cost per distance combines the path length, the time and a discomfort field.
Each group then gets a potential $\phi$ with $\phi = 0$ in its goal and $|\nabla \phi| = C$ elsewhere, an [eikonal equation](/eikonal-equation/) solved by the [fast marching method](/fast-marching-method/).
Every person walks down the gradient of the potential of its group, at the local speed.
Adrien Treuille, Seth Cooper and Zoran Popović presented the method in 2006.

## In plain words

Think of a crowd in a station, where everybody of one group wants to reach the same exit.
For each spot on the floor, you write down how long it takes to reach the exit from there, if you walk the best way.
Where many people stand, or where the crowd moves the other way, walking is slow, so that spot counts as far away.
Then each person simply steps toward the neighboring spot with the smaller number.
Because you write the numbers again at every moment, people walk around a jam as soon as it forms.
And people who walk against a flow find it cheaper to follow others in the same direction, so lanes appear by themselves.

## The problem

The input is a 2D grid of $g$ square cells of size $\Delta x$, groups of people with positions and velocities, a goal set of cells for each group, a discomfort field $h$ (high where people do not want to walk, infinite at obstacles), and the weights $\alpha$, $\beta$, $\gamma$ of the cost.
A person who walks along a path from $x$ to the goal pays

$$\alpha \int ds + \beta \int dt + \gamma \int h\, dt ,$$

the path length, the time and the discomfort along the way.
With $dt = ds / f$ for the speed $f$, the cost per unit length in the direction $\theta$ is

$$C(x, \theta) = \frac{\alpha f(x, \theta) + \beta + \gamma\, h(x)}{f(x, \theta)} .$$

The potential $\phi$ is the cheapest cost to the goal.
It satisfies $\phi = 0$ in the goal and the eikonal equation $|\nabla \phi| = C$ elsewhere, and a person moves with the velocity $\dot x = -f(x, \theta)\, \nabla \phi / |\nabla \phi|$, where $\theta$ is the direction of $-\nabla \phi$.

The speed comes from Section 3.2 of the paper.
The density $\rho$ and the mean velocity $\bar v$ come from a splat of the people (Eq. 7).
The terrain speed $f_T$ falls from $f_{\max}$ with the slope (Eq. 8), and the flow speed is $f_v = \max(0, \bar v(x + r n_\theta) \cdot n_\theta)$, the crowd velocity a short distance $r$ ahead in the direction $n_\theta$ (Eq. 9).
The speed is $f_T$ below a density $\rho_{\min}$, $f_v$ above $\rho_{\max}$, and the linear blend $f_T + \frac{\rho - \rho_{\min}}{\rho_{\max} - \rho_{\min}} (f_v - f_T)$ between them (Eq. 10).
The paper calls this blend ad hoc, so it is a heuristic, and $\alpha$, $\beta$, $\gamma$, $\rho_{\min}$, $\rho_{\max}$ and $f_{\max}$ are tuning.

## The algorithm

One time step does, as in Section 4 of the paper:

1. **Splat.** Every person adds to the four cells around it the weights $\min(1 - \Delta_x, 1 - \Delta_y)^\lambda$, $\min(\Delta_x, 1 - \Delta_y)^\lambda$, $\min(\Delta_x, \Delta_y)^\lambda$ and $\min(1 - \Delta_x, \Delta_y)^\lambda$, where $(\Delta_x, \Delta_y)$ is its offset from the center of the lower left cell in cell units (Section 4.1). This gives $\rho$, and the same weights on the velocities give $\bar v$.
2. **Speed and cost.** For each group, for each cell $M$ and each of the four directions, compute $f$ and $C$ at the neighbor cell in that direction, the cell one moves into (Section 4.2).
3. **Potential.** Solve the discrete eikonal equation for each group by fast marching (Section 4.3), below.
4. **Advection.** Move every person by $\Delta t\, \dot x$, with $\dot x$ from upwind differences of $\phi$ (Section 4.4).
5. **Minimum distance.** Push apart every pair of people closer than $d_{\min}$, half each way (Section 4.5).

Step 3 is the core:

```pseudo id=main
FAST-MARCH(C, Γ, Δx)                       ▷ costs per cell and face, goal cells
L1  φ ← ∞ in every cell; φ ← 0 in Γ; push every goal cell into the heap H
L2  while H is not empty
L3      (p, M) ← pop the smallest entry; skip it if M is known or p > φ_M
L4      mark M known
L5      for each neighbor N of M that is not known
L6          u ← U_N(φ over the known neighbors of N)     ▷ the upwind update
L7          if u < φ_N then φ_N ← u and push (u, N) into H
L8  return φ
```

**The local update.**
For a cell $M$ with the face lengths $h_{M \to i} = \Delta x\, C_{M \to i}$ to its neighbors $i$, the code solves $G_M(x) = 1$ with

$$G_M(x) = \sum_{\text{axis}} \Big( \max_{i \text{ on the axis}} \frac{[x - \phi_i]^+}{h_{M \to i}} \Big)^2 ,$$

the upwind (Godunov) form of $|\nabla\phi| = C$.
It tries every choice of at most one neighbor per axis: $\phi_i + h_i$ for one neighbor, and the larger root of $\sum ((x - \phi_i) / h_i)^2 = 1$ for two, kept only if it is at least both $\phi_i$; the smallest candidate is $U_M$.

**The rule of the paper.**
The paper picks, on each axis, the neighbor with the smaller $\phi_i + C_{M \to i}$ and solves its Eq. 11 with $\Delta x = 1$.
When the two faces of an axis have the same cost, this picks the neighbor with the smaller $\phi_i$, which is also the neighbor that attains the maximum in $G_M$, so the two rules agree.
With different costs on the two faces they can differ.
The code uses the rule of $G_M$, because the proofs below hold for it.

The code steps one group; with several groups, the density is shared, and each group has its own goal, cost and potential.

## Example

**By hand.**
Take a constant cost $C = 2$ on every face, $\Delta x = 0.5$, and the goal cell $(0, 0)$, so every $h = 1$.
Along an axis, each cell has one useful neighbor and $\phi = 1, 2, 3, \dots$, which is $C$ times the distance.
The cell $(1, 1)$ has the known neighbors $(1, 0)$ and $(0, 1)$, both with $\phi = 1$; the two term update gives $2 (x - 1)^2 = 1$, so $\phi_{11} = 1 + \sqrt{0.5} = 1.7071$.
The cell $(1, 2)$ uses $\phi_{02} = 2$ on one axis and $\phi_{11} = 1.7071$ on the other, and $(x - 2)^2 + (x - 1.7071)^2 = 1$ gives $\phi_{12} = 2.5453$.
The exact cost to the goal center would be $2 \cdot 0.5 \sqrt 2 = 1.4142$ and $2 \cdot 0.5 \sqrt 5 = 2.2361$; the first order grid scheme overestimates diagonal distances.

**The cost.**
With $\alpha = \beta = \gamma = 1$, no discomfort, $f_{\max} = 1.4$ m/s, $\rho_{\min} = 0.6$ and $\rho_{\max} = 1.6$: a thin crowd gives $f = 1.4$ and $C = 2.4 / 1.4 = 1.71$.
At $\rho = 1.1$ with no flow, $f = 0.7$ and $C = 1.7 / 0.7 = 2.43$.
In a dense crowd that moves toward the person, $f_v = 0$, and the code clamps $f$ to $10^{-3}$, so $C$ is about 1000; walking with a dense flow at 0.3 m/s gives $C = 1.3 / 0.3 = 4.33$.

**A measured run.**
The test puts 20 people at random in the left part of a $16 \times 16$ grid with $\Delta x = 1$ m (seed 2), with the goal column $x \in [15, 16)$, $\lambda = 2$, $d_{\min} = 0.4$ m and $\Delta t = 0.25$ s.
After 40 steps (10 s) every person has $x \ge 14.9$ m, and the closest pair over the run is 0.378 m apart, a little below $d_{\min}$ because one pass of pushes does not fix all pairs.
These are measurements of one toy.

## Correctness

The proof file shows, in exact arithmetic, that fast marching solves the discrete equation of the code.

- The equation $G_M(x) = 1$ has exactly one solution $U_M$ when $M$ has a usable neighbor, and line L6 returns it.
- The update is monotone (smaller neighbors give a smaller value) and causal (a neighbor with $\phi_i \ge U_M$ does not change $U_M$).
- So the cells are accepted at line L4 in nondecreasing order of $\phi$, and at the end every reached cell satisfies its equation over all its neighbors, while the cells that are never reached have no finite path to the goal (Theorem 1).
- The discrete system has only one solution, so fast marching and the brute force iteration of the test give the same field (Theorem 2).

It also follows from the update that every reached cell outside the goal has a neighbor with a smaller $\phi$, so the potential has no local minima: a person who walks downhill always reaches the goal.

The tests check the equality with the brute force iteration on random anisotropic grids with obstacles, the order of acceptance, the values of the hand example along the axes and at $(1, 1)$, and the two requirements of the splat in Section 4.1: a person adds at least $2^{-\lambda}$ to its own cell and at most $2^{-\lambda}$ to every other cell, and the density changes continuously with the position.

What is not proved: that the discrete potential is close to the continuous one, that people never overlap, and that the crowd looks right.
The speed blend is a heuristic, the constants are tuning, and the lanes and the flows around obstacles are observations in the paper.

## Complexity

Fast marching accepts each of the $g$ cells once, and each acceptance updates at most four neighbors with at most nine candidates each, plus a heap push of $O(\log g)$.
So it costs $O(g \log g)$ time and $O(g)$ space.
The splat costs $O(n + g)$, the speed and cost fields $O(g)$ per group, and the advection $O(n)$.
With $k$ groups a step costs $O(k g \log g + n)$, plus the minimum distance pass, which is $O(n^2)$ in the code over all pairs and $O(n)$ expected with a [uniform grid](/uniform-grid/) at bounded density.
The planning cost depends on the grid and the number of groups, not on the number of people, which is what makes large crowds cheap.

## Properties

- **Global planning.** The potential sees the whole space, so people walk around jams and obstacles far ahead, not only around their neighbors.
- **No local minima.** In the discrete field every reached cell has a lower neighbor (proved above).
- **Dynamic.** The field is solved again at every step, so it reacts to the moving crowd.
- **Group based.** All people of a group follow one field; the cost grows with the number of groups.
- **Not exact.** The grid scheme is first order and overestimates diagonal costs, the advection is explicit Euler, and the minimum distance pass leaves small overlaps.
- **Deterministic.** The same input gives the same crowd.

## Variants and improvements

- **Fast sweeping.** Gauss Seidel sweeps in alternating orders solve the same discrete equation in $O(g)$ per sweep; the paper chose fast marching instead.
- **Dijkstra.** [Dijkstra's algorithm](/dijkstra/) on the grid graph solves a similar problem in the same time, but its paths move only along the axes, so diagonal distances are too large by up to a factor $\sqrt 2$.
- **Local avoidance.** Add [reciprocal velocity obstacles](/reciprocal-velocity-obstacles/) or [ORCA](/optimal-reciprocal-collision-avoidance/) for the near range, where the grid is too coarse to keep people apart.
- **Incompressible crowds.** Later work treats a very dense crowd as a fluid with a limit on the density, solved on the grid, so that the density cannot exceed a maximum.
- **Forces.** The [social force model](/social-force-model/) moves each person by forces toward a straight line goal; it has no global planning but handles contacts and pushing.

## When to use it

Use continuum crowds for large, dense crowds with a few shared goals, such as evacuations, stadiums or streets, where people must route around jams and form lanes.
It is a poor fit when every person has its own goal, because each goal needs its own potential, and when close contact or the shape of a single path matters, where agent methods such as [boids](/boids/), [ORCA](/optimal-reciprocal-collision-avoidance/) or the [social force model](/social-force-model/) are simpler.

## Pitfalls

- **The face rule.** The paper's argmin rule and the upwind max rule differ when the two faces of an axis have different costs; the proofs above hold for the max rule.
- **Zero speed.** In a dense counter flow $f_v = 0$, and the cost is infinite; clamp the speed to a small positive value, or the field breaks at such cells.
- **Grid size.** Cells much larger than a person blur the density, and cells much smaller give a noisy field; the splat exponent $\lambda$ sets how sharp each person is.
- **Overlaps.** One pass of pushes does not separate all pairs, as the measured run shows; use more passes or a local avoidance method if overlap matters.
- **Discretization error.** The first order scheme overestimates diagonal costs, by about 21 percent at the diagonal neighbor of the goal in the hand example; a finer grid reduces it.
- **Cost per step.** A full fast marching per group per step is the main cost; with many goals, group people or update the fields less often.

## Implementations

## History

Adrien Treuille, Seth Cooper and Zoran Popović presented continuum crowds at SIGGRAPH 2006.
They took the idea of a potential field over the space from robot motion planning and from models of pedestrians as a continuum, and solved its eikonal equation with the Dijkstra like method of Tsitsiklis (1995), which Sethian (1996) had made known as fast marching.
Earlier crowd methods in graphics were agent based, from [boids](/boids/) (1987) to the [social force model](/social-force-model/) (1995); continuum crowds showed that one field per group could plan for a whole large crowd at once.

## References
