---
tag: S9QP93
kind: problem
slug: coverage-control
name: Coverage control
aliases:
- locational optimization for robot networks
area: robotics/multi-robot-systems
level: advanced
summary: Place mobile sensors in a region to minimize the expected squared distance from an event, drawn from a given density, to its nearest sensor.
prereqs: [multi-robot-system, voronoi-diagram]
see_also: [cortes-coverage-algorithm, centroidal-voronoi-tessellation, lloyds-algorithm, k-means-problem, voronoi-cell, power-diagram, coverage-path-planning, art-gallery-problem]
sources:
  - paper: doi:10.1109/TRA.2004.824698
    title: Jorge Cortes, Sonia Martinez, Timur Karatas and Francesco Bullo, Coverage control for mobile sensing networks, IEEE Transactions on Robotics and Automation 20(2), 2004
    locator: pages 243 to 255 (the locational optimization cost, its gradient, and gradient laws)
  - paper: doi:10.1137/S0036144599352836
    title: Qiang Du, Vance Faber and Max Gunzburger, Centroidal Voronoi tessellations, applications and algorithms, SIAM Review 41(4), 1999
    locator: pages 637 to 676 (the energy of a tessellation and its critical points)
  - paper: doi:10.1109/TIT.1982.1056489
    title: Stuart P. Lloyd, Least squares quantization in PCM, IEEE Transactions on Information Theory 28(2), 1982
    locator: the same cost in quantization, and the iteration of cells and centroids
  - book: isbn:9780691141954
    title: Francesco Bullo, Jorge Cortes and Sonia Martinez, Distributed Control of Robotic Networks, Princeton University Press, 2009
    locator: Chapter 5, Deployment
---

Coverage control is the problem of placing $r$ mobile sensors, such as robots with cameras, in a region $Q$ so that events in $Q$ are close to some sensor. Events happen at random with a known density $\phi$, an event is served by its nearest sensor, and the quality of service falls with the distance. The standard cost, from the theory of quantization and of facility location, is the expected squared distance to the nearest sensor,

$$H(p_1, \dots, p_r) = \int_Q \min_i \lVert q - p_i \rVert^2 \, \phi(q)\, dq.$$

Its critical points are the configurations where every sensor is at the centroid of its [Voronoi cell](/voronoi-cell/), the [centroidal Voronoi tessellations](/centroidal-voronoi-tessellation/), and the robots can reach one with the distributed law of the [distributed Lloyd coverage algorithm](/cortes-coverage-algorithm/).

## In plain words

Some robots with cameras must watch a field. Things happen at random places, more often in some parts of the field than in others. When something happens, the nearest robot looks at it, and it sees better when it is close.

The question is where to put the robots so that, on average, the nearest robot is as close as possible. If all robots stand in one corner, the far side of the field is badly watched. If they spread out evenly, each robot has its own patch to watch.

The best places have a simple test. Each robot owns the part of the field that is closer to it than to the others, and it should stand at the balance point of that part, weighted by how often things happen there.

## Definition

**Input.** A convex region $Q \subset \mathbb{R}^d$, usually a polygon in the plane, a density $\phi \ge 0$ on $Q$, and the number $r$ of sensors. In the general form there is also a nondecreasing function $f$, and the cost is $\int_Q \min_i f(\lVert q - p_i \rVert)\, \phi(q)\, dq$; the standard choice is $f(x) = x^2$.

**Output.** Positions $p_1, \dots, p_r \in Q$ that minimize $H$, or, for mobile robots, a control law that drives the robots to a local minimum of $H$ using local information.

**Structure.** For fixed positions, the best assignment of points to sensors is the Voronoi partition, so $H(p) = \sum_i \int_{V_i} \lVert q - p_i \rVert^2 \phi(q)\, dq$. For a fixed partition, the best position in each cell is its centroid $C_i$, by the identity $\int_{V_i} \lVert q - p \rVert^2 \phi = \int_{V_i} \lVert q - C_i \rVert^2 \phi + M_i \lVert p - C_i \rVert^2$, where $M_i$ is the mass of the cell. The gradient is $\partial H / \partial p_i = 2 M_i (p_i - C_i)$ (Cortés et al. 2004), so the critical points are exactly the centroidal Voronoi configurations.

## Variants

- **Density.** A uniform density spreads the robots evenly; a density with peaks pulls robots to the important places.
- **Other costs.** The disk covering version asks for the smallest radius $R$ such that every point of $Q$ is within $R$ of a sensor, a minimax cost. Sensors of different quality lead to weighted distances and [power diagrams](/power-diagram/).
- **Limited range.** Sensors that see only within a radius contribute only within it, which makes the law depend only on nearby robots.
- **Nonconvex regions.** Walls and holes need geodesic distances or other cells.
- **Unknown density.** Robots learn the density from measurements while they move, which leads to adaptive laws.
- **Sweep coverage.** Visiting every point of the region with one or a few moving sensors is a different problem, [coverage path planning](/coverage-path-planning/). Seeing every point from a few fixed guards inside a polygon is the [art gallery problem](/art-gallery-problem/).

## Examples

**A segment.** On $Q = [0, 1]$ with uniform density, the best positions of $r$ sensors are $p_i = (2i - 1) / (2r)$, each at the middle of a cell of length $1/r$. Each cell adds $\int_{-1/(2r)}^{1/(2r)} x^2 \, dx = 1 / (12 r^3)$, so $H = 1 / (12 r^2)$. Three robots at $0.1$, $0.2$ and $0.9$ have the cells $[0, 0.15]$, $[0.15, 0.55]$ and $[0.55, 1]$, with centroids $0.075$, $0.35$ and $0.775$, so they are not at a critical point.

**Two robots in a square.** In the unit square with uniform density, robots at $(0.25, 0.5)$ and $(0.75, 0.5)$ split the square into two halves and have the cost $5/48 \approx 0.1042$. Robots at $(1/3, 2/3)$ and $(2/3, 1/3)$ split it along the diagonal; each sits at the centroid of its triangle, so this is also a critical point, but its cost is $1/9 \approx 0.1111$. It is a saddle, not a minimum, and a gradient law started near it moves away to the halves.

**Four robots in a square.** The centers of the four squares of side $1/2$ have the cost $4 \cdot \frac{1}{96} = \frac{1}{24} \approx 0.04167$. The [distributed Lloyd coverage algorithm](/cortes-coverage-algorithm/) reaches it from robots crowded in one corner in about 20 steps.

## Known algorithms

- [Distributed Lloyd coverage algorithm](/cortes-coverage-algorithm/): each robot moves toward the centroid of its Voronoi cell, in continuous or discrete time; it never increases $H$ and approaches the set of centroidal Voronoi configurations.
- [Lloyd's algorithm](/lloyds-algorithm/): the same iteration, run by one computer on the whole diagram.
- [k-means](/k-means/): the same iteration on a finite sample of events, which solves the [k-means problem](/k-means-problem/) approximately.
- Gradient descent on $H$ with other step sizes, and Newton-type methods for faster convergence near a minimum.

## Bounds

- **Lower bound from disks.** Among all sets of area $a$ in the plane, a disk has the smallest $\int \lVert q - c \rVert^2 dq$, which is $a^2 / (2 \pi)$. For uniform density on a region of area $A$, the cell areas $a_i$ add up to $A$, and $\sum_i a_i^2 \ge A^2 / r$, so $H \ge A^2 / (2 \pi r)$. For the unit square and four robots this gives $0.0398$, below the value $0.04167$ of the grid.
- **Hexagons.** For many robots with uniform density in the plane, cells that are close to regular hexagons are best; this is a classical result of László Fejes Tóth on sums of moments.
- **Hardness of the discrete version.** With a finite set of event points in place of a density, the problem is the [k-means problem](/k-means-problem/), which is NP-hard in general, so gradient laws aim at local minima.
- **Local minima.** $H$ is not convex, and it can have many critical points; the limit of a gradient law depends on the start.

## Reductions

- **From quantization.** Coverage with $f(x) = x^2$ is the design of an optimal quantizer with $r$ levels for a source with density $\phi$, as in Lloyd (1982).
- **To the k-means problem.** Replacing the density by a finite sample of events gives the k-means problem.
- **To facility location.** Coverage is the continuous version of placing $r$ facilities to minimize the expected travel cost of customers.

## Applications

Coverage control is used to deploy mobile sensor networks for environmental monitoring, to spread surveillance robots and drones over an area with known risks, to place mobile base stations for communication, and to share a region among robots for later tasks such as search or cleaning.

## References
