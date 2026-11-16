---
tag: CV7WDC
kind: algorithm
slug: cortes-coverage-algorithm
name: Distributed Lloyd coverage algorithm
aliases:
- Cortes-Martinez-Karatas-Bullo coverage control
area: robotics/multi-robot-systems
level: research
summary: Each robot moves toward the centroid of its Voronoi cell, which never increases the coverage cost and drives the group toward a centroidal Voronoi configuration.
solves: [coverage-control]
model: real-ram
complexity:
  vars: {r: the number of robots, n: the number of vertices of the region, s: the number of steps}
  time: {per_robot: O(r (n + r)), per_step: O(r^2 (n + r)), total: O(s r^2 (n + r))}
  space: {extra: O(r (n + r))}
properties: {deterministic: true, randomized: false, online: true}
history:
  year: 2004
  people: [Jorge Cortes, Sonia Martinez, Timur Karatas, Francesco Bullo]
  note: Cortes, Martinez, Karatas and Bullo turned the Lloyd iteration of quantization into a distributed control law for robots, in continuous and discrete time, and proved convergence to centroidal Voronoi configurations.
prereqs: [coverage-control, lloyds-algorithm, voronoi-cell]
see_also: [lloyds-algorithm, centroidal-voronoi-tessellation, voronoi-diagram, k-means, delaunay-triangulation, sutherland-hodgman, power-diagram, gradient-descent]
sources:
  - paper: doi:10.1109/TRA.2004.824698
    title: Jorge Cortes, Sonia Martinez, Timur Karatas and Francesco Bullo, Coverage control for mobile sensing networks, IEEE Transactions on Robotics and Automation 20(2), 2004
    locator: pages 243 to 255 (the cost, its gradient, the continuous and discrete laws, and convergence to centroidal Voronoi configurations)
  - paper: doi:10.1109/TIT.1982.1056489
    title: Stuart P. Lloyd, Least squares quantization in PCM, IEEE Transactions on Information Theory 28(2), 1982
    locator: the iteration that alternates nearest cells and centroids
  - paper: doi:10.1137/S0036144599352836
    title: Qiang Du, Vance Faber and Max Gunzburger, Centroidal Voronoi tessellations, applications and algorithms, SIAM Review 41(4), 1999
    locator: pages 637 to 676 (centroidal Voronoi tessellations as critical points of the energy, and Lloyd's method)
  - paper: doi:10.1109/TAC.2007.908304
    title: Sonia Martinez, Francesco Bullo, Jorge Cortes and Emilio Frazzoli, On synchronous robotic networks, Part II, Time complexity of rendezvous and deployment algorithms, IEEE Transactions on Automatic Control 52(12), 2007
    locator: pages 2214 to 2226 (the number of rounds of deployment algorithms)
  - book: isbn:9780691141954
    title: Francesco Bullo, Jorge Cortes and Sonia Martinez, Distributed Control of Robotic Networks, Princeton University Press, 2009
    locator: Chapter 5, Deployment
---

The distributed Lloyd coverage algorithm of Cortés, Martínez, Karatas and Bullo places $r$ robots in a convex region $Q$ so that each point of $Q$ is near some robot. Each robot computes its [Voronoi cell](/voronoi-cell/), the part of $Q$ that is nearer to it than to any other robot, and moves toward the [centroid](/centroid/) of that cell. This is [Lloyd's algorithm](/lloyds-algorithm/) run by the robots themselves. Each step never increases the coverage cost $H(P) = \sum_i \int_{V_i} \lVert q - p_i \rVert^2 \phi(q)\, dq$, the expected squared distance from a point of $Q$ with density $\phi$ to its nearest robot, and the robots approach a [centroidal Voronoi tessellation](/centroidal-voronoi-tessellation/), where each robot sits at the centroid of its own cell. To find its cell a robot needs only the positions of its Voronoi neighbors, so the law is distributed.

## In plain words

Some robots must watch a room, and each spot of the room is watched best by the nearest robot. Each robot owns the part of the room that is closer to it than to any other robot.

Each robot finds the middle of its own part, the balance point of that area, and moves toward it. When a robot moves, the borders between the parts move too, so the robots repeat the step.

A robot at the middle of its part is as close as it can be, on average, to the spots it owns. So each step makes the average distance from a spot to its nearest robot smaller or keeps it the same. The robots spread out by themselves and stop when each one is at the middle of its own part.

## The problem

**The model.** The region $Q$ is a convex polygon with $n$ vertices, and $\phi \ge 0$ is a density on $Q$ that says how important each point is. The implementation uses the uniform density $\phi = 1$. The robots are points $p_1, \dots, p_r$ in $Q$ with the dynamics $p_i(t+1) = p_i(t) + u_i$. Each robot knows $Q$ and $\phi$ and can learn the positions of the robots whose cells touch its own cell. The steps are synchronous.

**Input.** The region $Q$, the start positions, a gain $k$ with $0 < k \le 1$, and the number $s$ of steps.

**Output.** The positions after $s$ steps. The goal is a configuration that is a local minimum of the coverage cost $H$, see [coverage control](/coverage-control/).

**How it differs from close pages.** [Lloyd's algorithm](/lloyds-algorithm/) is the same iteration for points in a computer, where one program computes the whole diagram. [k-means](/k-means/) is the same iteration on a finite set of data points. Here the points are robots, each robot computes only its own cell, and the gain $k < 1$ lets a robot move only part of the way in each step, which is the time step of the continuous law $\dot p_i = -k (p_i - C_i)$.

## The algorithm

```pseudo id=main
COVERAGE(Q, p, k, s)
L1  for step = 1 to s do
L2      for each robot i, in parallel, do
L3          V_i ← Q
L4          for each other robot j that can bound the cell do    ▷ the Voronoi neighbors are enough
L5              V_i ← V_i ∩ { q : ‖q - p_i‖ ≤ ‖q - p_j‖ }        ▷ clip with a half-plane
L6          M_i ← mass of V_i;  C_i ← centroid of V_i
L7          p_i ← p_i + k (C_i - p_i)
L8  return p
```

Line L5 is one clip of a convex polygon with the half-plane $(p_j - p_i) \cdot q \le \frac12 (\lVert p_j \rVert^2 - \lVert p_i \rVert^2)$, as in the [Sutherland-Hodgman](/sutherland-hodgman/) method. Line L6 uses the [shoelace formula](/shoelace-formula/) for the area and the centroid, and the same kind of sum gives the polar moment $\int_{V_i} \lVert q \rVert^2 dq$, from which the cost of the cell follows. All robots read the positions at the start of the step and move together. The implementation clips with all other robots, which gives the same cell; a real robot clips only with its Voronoi neighbors, the robots joined to it in the [Delaunay triangulation](/delaunay-triangulation/).

## Example

**Three robots on a segment.** Let $Q$ be the thin strip $[0, 1] \times [0, 0.1]$, $k = 1$, and the robots at $x = 0.1$, $0.2$ and $0.9$ on the middle line. The borders of the cells are the midpoints $0.15$ and $0.55$, so the cells are $[0, 0.15]$, $[0.15, 0.55]$ and $[0.55, 1]$, with centroids $0.075$, $0.35$ and $0.775$. The robots move there. In the next step the borders are $0.2125$ and $0.5625$, and the robots move to $0.10625$, $0.3875$ and $0.78125$. They converge to $1/6$, $1/2$ and $5/6$, where each robot is at the middle of a cell of length $1/3$.

**Four robots in a square.** Let $Q$ be the unit square, $\phi = 1$, $k = 1$, and the robots start crowded in one corner.

| step | robot 1 | robot 2 | robot 3 | robot 4 | cost $H$ |
|---|---|---|---|---|---|
| 0 | (0.1, 0.1) | (0.3, 0.2) | (0.2, 0.4) | (0.4, 0.4) | 0.15792 |
| 1 | (0.1054, 0.1229) | (0.4614, 0.123) | (0.1491, 0.6404) | (0.6737, 0.5696) | 0.06414 |
| 2 | (0.1402, 0.1903) | (0.5833, 0.1641) | (0.2117, 0.7026) | (0.7306, 0.6291) | 0.04946 |
| 3 | (0.1785, 0.2253) | (0.6576, 0.194) | (0.2425, 0.7295) | (0.751, 0.6776) | 0.04417 |
| 5 | (0.2229, 0.2483) | (0.7203, 0.229) | (0.2569, 0.7482) | (0.7578, 0.7264) | 0.04194 |
| 10 | (0.2474, 0.251) | (0.7473, 0.2482) | (0.252, 0.751) | (0.752, 0.7482) | 0.04167 |
| 20 | (0.25, 0.25) | (0.75, 0.25) | (0.25, 0.75) | (0.75, 0.75) | 0.04167 |

At step 0 robot 4 owns the cell of area $0.5944$, most of the square, and its centroid $(0.6737, 0.5696)$ pulls it far out. The cost falls in every step, and the robots end at the centers of the four squares of side $1/2$. Each small square adds $\frac14 \cdot \frac{1/4 + 1/4}{12} = \frac{1}{96}$ to the cost, so the final cost is $1/24 \approx 0.04167$. The largest distance from a robot to its centroid is about $1.6 \cdot 10^{-5}$ after 20 steps and $1.4 \cdot 10^{-12}$ after 60 steps.

**A critical point that is not the best.** Two robots in the unit square at $(1/3, 2/3)$ and $(2/3, 1/3)$ have the diagonal as the border of their cells, and each robot is at the centroid of its triangle. So they never move, and the cost is $1/9 \approx 0.1111$. The two halves of the square with robots at $(0.25, 0.5)$ and $(0.75, 0.5)$ cost only $5/48 \approx 0.1042$. If one robot starts $10^{-6}$ away from the diagonal configuration, the error grows, and the robots end at two halves of the square. The diagonal configuration is a saddle of $H$.

## Correctness

The [proof](proofs/correctness/) uses two facts. For fixed robots, the Voronoi cells are the best way to divide $Q$, because each point goes to its nearest robot. For fixed cells, the parallel axis identity $\int_{W_i} \lVert q - p \rVert^2 = J_i + M_i \lVert p - C_i \rVert^2$ shows that the best point for a cell is its centroid. A step first keeps the cells and moves each robot to $p_i + k(C_i - p_i)$, which cuts the cost by $k(2 - k) \sum_i M_i \lVert p_i - C_i \rVert^2$, and then switching to the new Voronoi cells does not raise the cost. Summed over the steps, $\sum_i M_i \lVert p_i - C_i \rVert^2 \to 0$. Cortés et al. (2004) used the [LaSalle invariance principle](/lasalle-invariance-principle/) to conclude that the robots converge to the set of centroidal Voronoi configurations, and showed that the gradient of $H$ is $2 M_i (p_i - C_i)$, so the law is a [gradient descent](/gradient-descent/) with a step that depends on the robot.

## Complexity

- **Per robot and step.** Each clip in line L5 costs time linear in the size of the current cell, at most $n + r$ vertices, so a robot that clips with all others uses $O(r (n + r))$ time in the [real RAM](/real-ram/) model. A robot that knows its $d_i$ Voronoi neighbors uses $O(d_i (n + d_i))$ time.
- **Per step.** The implementation computes all cells in $O(r^2 (n + r))$ time. One Voronoi diagram for all robots, clipped to $Q$, gives all cells in $O(r \log r + n r)$ time.
- **Number of steps.** The proof gives no rate. Martínez, Bullo, Cortés and Frazzoli (2007) study the number of rounds of deployment laws of this kind. On the examples above about 20 steps reach a gap of $10^{-5}$.
- **Space.** $O(n + r)$ per cell.

## Properties

- **Distributed.** A robot needs only the positions of its Voronoi neighbors, whose number is less than 6 on average in the plane, and not the number of robots.
- **Monotone.** The cost never increases.
- **Local, not global.** The limit is a critical point of $H$. It can be a saddle or a local minimum that is not the global minimum.
- **Stays in the region.** For $0 < k \le 1$ every robot stays in its own cell, so the robots stay in $Q$ and never collide.
- **Deterministic.** The same start gives the same run.

## Variants and improvements

- **Continuous time.** The flow $\dot p_i = -k (p_i - C_i)$ is the original form, with the same cost decrease and the same limit set.
- **Nonuniform density.** With a density $\phi$ the cells are the same, but the mass and the centroid are weighted by $\phi$, and the robots gather where $\phi$ is large.
- **Limited range.** Robots that sense only within a radius use the part of the cell within that radius, which gives a related cost with the same structure and needs only robots within twice that radius.
- **Other costs.** Sensors of different quality lead to [power diagrams](/power-diagram/) instead of Voronoi cells. Nonconvex regions and unknown densities need other cells or adaptive laws.

## When to use it

Use it to spread a team of robots or sensors over a known convex region, so that the expected distance from an event to the nearest robot is small, and when each robot can talk to the robots near it. Use [coverage path planning](/coverage-path-planning/) instead when one robot must sweep every point of the region, and the [Laplacian consensus protocol](/laplacian-consensus-protocol/) when the robots must gather and not spread.

## Pitfalls

- **Saddles and local minima.** The limit depends on the start. Symmetric starts, such as robots on a line or on the diagonal of a square, stay symmetric in exact arithmetic and stop at a saddle. In floating point the rounding error can grow away from such a saddle, so runs from the same start can end at different configurations.
- **Gain.** For $k > 1$ a robot can leave its cell, and for $k \ge 2$ the cost can increase. The proof needs $0 < k < 2$, and the simple argument that robots stay apart needs $k \le 1$.
- **Nonconvex regions.** The centroid of a cell in a nonconvex region can lie outside the region or behind a wall, so the law needs changes there.
- **Neighbor discovery.** Clipping with too few robots gives a cell that is too large. A robot must know every Voronoi neighbor, which can be far away when the robots are sparse.

## Implementations

## History

Lloyd described the iteration in 1957 at Bell Labs for the design of quantizers, and it was published in 1982. Du, Faber and Gunzburger (1999) surveyed centroidal Voronoi tessellations and Lloyd's method. Cortés, Martínez, Karatas and Bullo (2004) turned the iteration into a control law for mobile sensing networks, and proved convergence with an invariance principle. The book of Bullo, Cortés and Martínez (2009) treats deployment in its own chapter.

## References
