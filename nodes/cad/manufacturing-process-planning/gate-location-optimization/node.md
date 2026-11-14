---
tag: 1H7J0S
kind: problem
slug: gate-location-optimization
name: Gate location optimization
aliases:
- injection gate placement
area: cad/manufacturing-process-planning
level: advanced
summary: Choose where melt enters an injection mold so the cavity fills evenly, with short flow lengths and weld lines away from critical regions.
prereqs: [black-box-optimization]
see_also: [local-search, simulated-annealing, genetic-algorithm, eccentricity, k-center-problem, finite-element-method, conformal-cooling-design, manufacturability-analysis]
sources:
  - paper: doi:10.1002/pen.760301502
    title: I. Pandelidis and Q. Zou, Optimization of injection molding design. Part I, Gate location optimization, Polymer Engineering and Science 30(15), 1990, 873 to 882
    locator: a quality function of the filling result built from temperature differences, overpacking and frictional (shear) heating, evaluated by flow simulation for candidate gates
  - title: B. H. Lee and B. H. Kim, Automated selection of gate location based on desired quality of injection molded part, Polymer-Plastics Technology and Engineering 35(2), 1996, 253 to 269
    locator: the search over gate candidates that evaluates the nodes next to the current gate with a flow simulation (general locator)
  - paper: doi:10.1081/PTE-200048523
    title: Ming Zhai, Y. C. Lam, C. K. Au and D. S. Liu, Automated selection of gate location for plastic injection molding processing, Polymer-Plastics Technology and Engineering 44(2), 2005, 229 to 242
    locator: the injection pressure at the end of filling at a constant flow rate as the objective, and a search that moves the gate along the largest pressure gradient, compared with a flow path search
  - title: M. Zhai, Y. C. Lam and C. K. Au, Algorithms for two gate optimization in injection molding, International Polymer Processing 20(1), 2005, 14 to 18
    locator: the extension of the gate search to two gates (general locator)
---

Gate location optimization chooses the point, or the points, where molten plastic enters the cavity of an injection mold. The gate decides how the melt front moves through the cavity, and so where the last regions fill, where two fronts meet in a weld line, where air is trapped, how high the injection pressure must be, and how the part shrinks and warps. None of these has a closed form for a real part. They come from a flow simulation, so the problem is to minimize an objective that is the output of a simulation over a set of candidate gates. The known methods are heuristic searches around the simulator. They are compared by what they measure and how many simulations they need, and there is no standard benchmark.

## In plain words

Plastic parts are made by pushing hot plastic into a hollow mold through a small hole, the gate. Where the gate is matters. If it is at one end of a long part, the plastic has far to go, needs high pressure and may cool before it reaches the other end. Where two streams of plastic meet around a hole, they leave a weak line. If the last place to fill is closed in, air is trapped there.

To choose the gate, an engineer runs a computer simulation of the filling for a few places and compares the results. Programs do the same thing automatically: they try a place, simulate, and move the gate in the direction that looks better.

## Definition

**Input.**

- The cavity of the part, usually a thin-walled part given as a mid-surface mesh with thicknesses, or as a 3D mesh.
- A set $G$ of allowed gate positions, usually mesh nodes on surfaces where a gate mark is allowed and the mold can feed them.
- The material, the process settings (flow rate or pressure, melt and mold temperatures), and a flow simulator $F$. For a gate $g$, $F(g)$ returns fields over the cavity: the fill time $t(x)$, the pressure, the temperature, the shear rate, and derived results such as weld line and air trap positions.
- An objective $J(F(g))$, to be minimized, and constraints such as a largest allowed injection pressure.

**Output.** A gate $g^* \in G$ with the least $J$, or for $k$ gates a set of $k$ positions.

**What is measured.** Each objective in the literature is a choice by its authors, built from the fields of $F$:

- Pandelidis and Zou (1990) use a quality function of the filling result from temperature differences in the melt, overpacking (regions that fill early and are packed further while the rest fills) and frictional heating.
- Lee and Kim (1996) use a quality target for the molded part and search the nodes next to the current gate.
- Zhai, Lam, Au and Liu (2005) use the injection pressure at the end of filling at a constant flow rate, and report it as the better objective on their numerical examples.
- Other common terms are the spread of fill times at the ends of the flow paths (flow balance), the length of the longest flow path, and the position of weld lines and air traps relative to regions that the designer marks as critical.

The problem is only defined once $J$ is chosen, and different $J$ give different gates.

## Variants

- **Single gate.** One point in $G$. With $\lvert G \rvert$ candidates, an exhaustive search needs $\lvert G \rvert$ simulations.
- **Several gates.** A set of $k$ gates fills a large part with lower pressure, but adds weld lines where the fronts meet. The positions of the weld lines then enter $J$. The group of Zhai and Lam also has a paper on the placement of two gates.
- **Gate type and size.** The kind of gate (edge, pin, submarine, hot runner nozzle) and its size change the pressure drop and the shear, and are chosen with the position.
- **Runner balance.** In a mold with several cavities, the runners are sized so that all cavities fill at the same time. This is a related design problem on the feed system, not on the cavity.
- **Geometric proxy.** Replace $F$ by the distance in the part from the gate: in a thin part of even thickness the melt front moves roughly with this distance. Minimizing the largest flow length is then the [eccentricity](/eccentricity/) problem on the mesh graph, and with $k$ gates it is the [k-center problem](/k-center-problem/). The proxy is exact to compute, but it ignores thickness changes, cooling and the flow rate, so its answer is a start point for the simulation.

## Examples

**Flow length on a plate.** A flat plate of $100 \times 50$ mm and even thickness, with the gate on its mid-plane. For a convex plate the flow length to a point is the straight distance. A gate at the centre has the longest flow length $\sqrt{50^2 + 25^2} = 55.9$ mm, to the corners. A gate at the middle of a long edge has $\sqrt{50^2 + 50^2} = 70.7$ mm. A gate at the middle of a short edge has $\sqrt{100^2 + 25^2} = 103.1$ mm. The proxy prefers the centre, but the centre leaves a gate mark on the face. If the face must be clean, $G$ holds only edge nodes, and the best edge gate has a flow length 26 percent larger.

**A plate with a hole.** With a hole in the plate, the melt flows around the hole on both sides and meets behind it in a weld line. Moving the gate moves the weld line, but no gate removes it. An objective that penalizes weld lines in a marked region chooses a gate that puts the weld line elsewhere. This is a choice that only the designer can weigh against flow length.

## Known algorithms

- **Exhaustive evaluation.** Simulate every candidate and keep the best. Exact for the chosen $J$ and $F$, but it costs $\lvert G \rvert$ simulations, so it is used for a few candidates chosen by an engineer.
- **Local search on the mesh.** Start at a gate, simulate the candidates next to it, and move to the best one while $J$ falls, as in Lee and Kim. This is [hill climbing](/hill-climbing/) on the node graph and stops at a local minimum.
- **Search along a field of the simulation.** Zhai and coauthors move the gate in the direction of the largest pressure gradient from the last simulation, which needs fewer simulations than a search along the flow paths on their examples.
- **Global heuristics.** [Simulated annealing](/simulated-annealing/) and [genetic algorithms](/genetic-algorithm/) over the candidates, with the simulator as the fitness, are used to escape local minima. They need many simulations.
- **Proxy first.** Compute the geodesic flow lengths with [Dijkstra's algorithm](/dijkstra/) on the mesh graph, or with the [fast marching method](/fast-marching-method/) on the surface, choose a few gates with small eccentricity, and simulate only those.

## Bounds

There are no complexity bounds for the problem as stated, because $J \circ F$ is a black box, as in [black-box optimization](/black-box-optimization/). The cost of a method is the number of simulations it runs, and each simulation is a [finite element](/finite-element-method/) or finite volume solve over the cavity. The geometric proxy has exact bounds: the eccentricity of all $V$ nodes of a mesh graph with $E$ edges takes $V$ runs of Dijkstra's algorithm, $O(V (E + V \log V))$ time, and the $k$-center version is NP-hard, with a factor-2 approximation by the [Gonzalez algorithm](/gonzalez-k-center/).

**No standard benchmark.** Each paper uses its own parts, its own simulator and settings and its own $J$. So the numbers they report, such as the injection pressure of the best gate or the number of simulations, cannot be compared from one paper to another, and this page does not quote them.

## Reductions

- With the flow length proxy, single gate placement is the 1-center problem on the mesh graph, and several gates is the [k-center problem](/k-center-problem/). With the sum of flow lengths in place of the largest, it is a [facility location](/facility-location-problem/) problem.
- With the simulator, it is a [black-box optimization](/black-box-optimization/) over a discrete set with a graph structure.

## Applications

Gate placement is part of mold design for injection molded parts, done with mold flow software during the design of the part, so that changes to wall thickness, ribs and gate marks are still possible. A [manufacturability analysis](/manufacturability-analysis/) of a molded part reports the expected weld lines and pressure for the chosen gate. The gate also sets the hot regions of the mold, which the cooling layout must reach, as in [conformal cooling design](/conformal-cooling-design/).

## References
