---
tag: 8E9VQA
kind: problem
slug: tier-partitioning
name: 3D IC tier partitioning
aliases:
- tier assignment
- 3D partitioning
area: eda/fpga-analog-and-emerging-technologies
level: advanced
summary: Assign the cells or blocks of a design to the tiers of a 3D IC so that area is balanced and inter-tier vias, wirelength, delay and temperature are low.
prereqs: [hypergraph-partitioning, three-dimensional-integrated-circuit]
see_also: [fiduccia-mattheyses, kernighan-lin, multilevel-hypergraph-partitioning, shrunk-2d, thermal-driven-3d-floorplanning, through-silicon-via, compact-thermal-model, np-hard]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A, problem [ND17] Minimum Cut into Bounded Sets (NP-complete, also for equal halves)
  - paper: doi:10.1145/2627369.2627642
    title: "Shreepad Panth, Kambiz Samadi, Yang Du and Sung Kyu Lim, Design and CAD methodologies for low power gate-level monolithic 3D ICs, Proceedings of the International Symposium on Low Power Electronics and Design (ISLPED 2014)"
    locator: Section 3 (the tier partitioning of a shrunk 2D placement by min-cut in placement bins, with area balance in each bin)
  - paper: doi:10.1109/ICCAD.2004.1382591
    title: "Jason Cong, Jie Wei and Yan Zhang, A thermal-driven floorplanning algorithm for 3D ICs, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design (ICCAD 2004), pages 306 to 313"
    locator: Sections 2 and 3 (the assignment of blocks to device layers inside a floorplanner, with costs for area, wirelength, interlayer vias and temperature)
  - paper: doi:10.1137/S0097539701387660
    title: "Uriel Feige and Robert Krauthgamer, A polylogarithmic approximation of the minimum bisection, SIAM Journal on Computing 31(4), 1090 to 1118, 2002"
    locator: the O(log^1.5 n) approximation of minimum bisection (general locator)
  - paper: doi:10.1145/1374376.1374415
    title: "Harald Räcke, Optimal hierarchical decompositions for congestion minimization in networks, Proceedings of the 40th ACM Symposium on Theory of Computing (STOC 2008), pages 255 to 264"
    locator: the O(log n) approximation of minimum bisection, one of the applications of the tree decompositions (general locator)
---

Tier partitioning is the step of a [3D IC](/three-dimensional-integrated-circuit/) flow that decides on which tier each cell or block goes. The tiers must have about the same area, because the footprint of the stack is the area of the largest tier. A net whose cells are on different tiers needs vertical links, [through-silicon vias](/through-silicon-via/) or monolithic inter-tier vias, which cost area, capacitance and yield. The cut also changes wirelength, delay and temperature, so practical versions add those to the cost. With two tiers and only the cut as the cost, the problem is the balanced bisection of a hypergraph, which is NP-hard.

## In plain words

You have a circuit and a building with a few floors of equal size. Every part of the circuit must go on some floor, and each floor must be about as full as the others. Wires that stay on one floor are cheap. A wire that goes between floors needs a vertical link, and links are costly. So you want to split the parts so that few wires go between floors.

That alone is the classic problem of cutting a network into equal halves with few cut wires, and it is already hard. Real tools also look at how hot each floor gets, how long the critical paths are, and how far the wires on each floor run.

## Definition

**Input.** A hypergraph $H = (V, E)$ whose vertices are cells or blocks and whose hyperedges are nets, an area $a(v) > 0$ for each vertex, a number of tiers $L \ge 2$, and a balance tolerance $\varepsilon \ge 0$. Let $A = \sum_v a(v)$.

**Output.** An assignment $t : V \to \{1, \ldots, L\}$ such that every tier has area at most $(1 + \varepsilon) A / L$:

$$\sum_{v : t(v) = i} a(v) \le (1 + \varepsilon) \frac{A}{L} \quad \text{for } i = 1, \ldots, L.$$

**Objective (the via count).** The tiers form a stack, so a net with cells on tiers $i < j$ crosses each boundary between them. The basic cost is

$$\mathrm{cost}(t) = \sum_{e \in E} \left( \max_{v \in e} t(v) - \min_{v \in e} t(v) \right),$$

the number of tier boundaries that the nets cross, which is a lower bound on the number of vertical links if each crossing needs at least one. For $L = 2$ it is the number of cut nets. The full cost in a tool is a weighted sum of this term and others: estimated wirelength in each tier, delay of the critical paths, and the peak temperature from a [thermal model](/compact-thermal-model/).

**Decision version.** Given also a bound $k$, is there a balanced assignment with $\mathrm{cost}(t) \le k$? It is in NP, because an assignment is a certificate that can be checked in linear time.

## Variants

- **Granularity.** *Block-level* partitioning assigns large blocks, often inside a floorplanner that also places them, as in [thermal-driven 3D floorplanning](/thermal-driven-3d-floorplanning/). *Gate-level* partitioning assigns standard cells, which only makes sense with small vertical links such as monolithic vias; [Shrunk-2D](/shrunk-2d/) does it after a 2D placement. *Transistor-level* partitioning puts the two transistor types of a gate on different tiers.
- **Placement-aware.** The cells are first placed in 2D, and then each small region is split between tiers, so that the cells of a region stay above one another and the wirelength in the plane is kept. Shrunk-2D does this with a balanced min-cut in each placement bin.
- **Timing-driven.** The cost weights the nets on critical paths, either to keep them in one tier or to use a vertical link where it is shorter than a long planar wire.
- **Thermal.** The cost includes the peak temperature, which favors putting blocks of high power in the tier next to the heat sink and spreading power within each tier.
- **Heterogeneous tiers.** The tiers use different processes, for example memory on one and logic on another, and some vertices are fixed to a tier in advance.
- **Via budget.** The number of TSVs is a constraint rather than a cost, and the objective is wirelength or delay.

## Examples

**A small bisection.** Take six cells $a, \ldots, f$ of unit area, $L = 2$ and $\varepsilon = 0$, so each tier gets three cells. The nets are $\{a, b, c\}$, $\{d, e, f\}$, $\{a, b\}$, $\{e, f\}$, $\{c, d\}$ and $\{b, e\}$.

The assignment $\{a, b, c\}$ to tier 1 and $\{d, e, f\}$ to tier 2 cuts $\{c, d\}$ and $\{b, e\}$, so its cost is 2. No assignment does better. If the net $\{a, b, c\}$ is not cut, its three cells fill one tier, so the other tier is exactly $\{d, e, f\}$, and the cost is 2 as above. If $\{a, b, c\}$ is cut, then $\{d, e, f\}$ is cut too, since it could only be uncut by filling a tier, which would force $\{a, b, c\}$ to fill the other. So every other assignment cuts both triples, and the cost is at least 2.

**The cost of spanning tiers.** With $L = 3$, a net with cells on tiers 1 and 3 costs 2, because it crosses both boundaries, and in a stack of dies joined face to back it passes through the substrate of tier 2. Moving one of its cells to tier 2 lowers its cost to 1, but may break the balance.

## Known algorithms

- **Move-based min-cut.** [Fiduccia-Mattheyses](/fiduccia-mattheyses/) and [Kernighan-Lin](/kernighan-lin/) improve a balanced cut by moving or swapping cells, and the [multilevel](/multilevel-hypergraph-partitioning/) scheme makes them work on millions of cells. With $L > 2$ they are applied recursively or with a cost that counts the span.
- **Partitioning after a 2D placement.** [Shrunk-2D](/shrunk-2d/) (Panth, Samadi, Du and Lim, 2014) places the design on a 2D die of half the area, divides it into bins, and runs a balanced min-cut in each bin, so that each tier gets half the cell area of every region.
- **Partitioning inside floorplanning.** [Thermal-driven 3D floorplanning](/thermal-driven-3d-floorplanning/) (Cong, Wei and Zhang, ICCAD 2004) anneals the layer of each block together with its place, with moves that change the layer.
- **Analytical 3D placement.** A placer treats the tier index as a continuous coordinate, spreads cells in all three directions and then rounds the coordinate to a tier.

## Bounds

The problem is NP-hard for $L = 2$ with unit areas, $\varepsilon = 0$ and nets of two cells, by the reduction below. Minimum bisection of a graph with $n$ vertices has a polynomial-time approximation within $O(\log^{1.5} n)$ (Feige and Krauthgamer, 2002), and a later $O(\log n)$ bound is known (Räcke, 2008). In practice, multilevel move-based methods find good cuts for the balanced cut, but the extra terms of timing and temperature have no guarantees, and tools report only measured results.

A simple lower bound on the cost is the size of a minimum cut between any two cells that are fixed to different tiers, which max-flow computes. Without fixed cells, the bound is 0, and no simple lower bound is tight in general.

## Reductions

**From minimum bisection.** Minimum Cut into Bounded Sets ([ND17] in Garey and Johnson) asks for a split of a graph into two sets with sizes at most a bound $B$ and at most $k$ cut edges, and it stays NP-complete with $B = |V|/2$, the minimum bisection problem. Given a graph $G = (V, E)$ with $|V|$ even, make a cell of unit area for each vertex and a two-pin net for each edge, and set $L = 2$, $\varepsilon = 0$. A tier assignment is then a bisection of $G$, and its cost is the number of cut edges. So the decision version of tier partitioning is NP-complete, and the optimization version is [NP-hard](/np-hard/).

**To hypergraph partitioning.** With $L = 2$ and the cut as the only cost, tier partitioning is exactly balanced [hypergraph partitioning](/hypergraph-partitioning/), so any partitioner for that problem solves it. With $L > 2$, the span cost is the cost of partitioning into $L$ ordered parts, which a $k$-way partitioner handles only if it knows the order of the parts.

## Applications

Tier partitioning is the first 3D step of every 3D IC flow. For TSV-based stacks, it is usually done at the block level, often together with the floorplan, because each TSV is large. For monolithic 3D, it is done at the gate level, as in Shrunk-2D, where Panth et al. report 15.57% lower total power than 2D for the OpenSPARC T2 core in 28 nm. The result also fixes the number of [TSVs](/through-silicon-via/), and with it a large part of the area, capacitance and test cost of the stack.

## References
