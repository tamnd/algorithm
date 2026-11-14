---
tag: WCAQB2
kind: problem
slug: floorplanning
name: Floorplanning
aliases:
- floorplan design
area: eda/partitioning-floorplanning-and-placement
level: core
summary: Place rectangular blocks of fixed or flexible shapes without overlap so the chip area and the wire length between blocks are small.
prereqs: [rectangle-packing, half-perimeter-wirelength, hypergraph]
see_also: [placement-problem, slicing-floorplan, mosaic-floorplan, floorplan-constraint-graphs, sequence-pair, b-star-tree-floorplan, wong-liu-floorplanning, strip-packing]
sources:
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 3, Chip Planning (the floorplanning problem, its objectives, and slicing and non-slicing representations; general locator)
  - paper: "D. F. Wong and C. L. Liu, A new algorithm for floorplan design, Proceedings of the 23rd ACM/IEEE Design Automation Conference, 101 to 107, 1986"
    locator: the cost of area plus weighted wire length, and simulated annealing over normalized Polish expressions
  - paper: doi:10.1109/43.552084
    title: Hiroshi Murata, Kunihiro Fujiyoshi, Shigetoshi Nakatake and Yoji Kajitani, VLSI module placement based on rectangle-packing by the sequence-pair, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 15(12), 1518 to 1524, 1996
    locator: the sequence pair, and the fact that every packing has a sequence pair whose packing is no larger
  - paper: doi:10.1109/TVLSI.2003.817546
    title: Saurabh N. Adya and Igor L. Markov, Fixed-outline floorplanning, enabling hierarchical design, IEEE Transactions on Very Large Scale Integration Systems 11(6), 1120 to 1135, 2003
    locator: the fixed-outline formulation and its difference from the minimum area formulation
  - paper: doi:10.1016/S0019-9958(83)80038-2
    title: Larry Stockmeyer, Optimal orientations of cells in slicing floorplan designs, Information and Control 57(2-3), 91 to 101, 1983
    locator: the polynomial orientation algorithm for slicing floorplans, and NP-completeness for general floorplans
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: the appendix entry for bin packing and the strong NP-completeness of 3-partition
---

Floorplanning is the first step of the physical design of a chip. The design is split into large blocks, such as processor cores, memories and analog parts, and each block has a size, or a fixed area with a choice of shapes. Floorplanning places these blocks as rectangles in the plane, with no two of them overlapping, so that the chip is small and the wires between the blocks are short. It comes before the [placement](/placement-problem/) of the standard cells, which then fill the space between and inside the blocks. The problem contains [bin packing](/bin-packing/) and [strip packing](/strip-packing/), so it is strongly NP-hard, and in practice it is solved by a search over a combinatorial representation, such as a slicing tree or a [sequence pair](/sequence-pair/), with an exact computation of the coordinates for each candidate.

## In plain words

Think of a house plan. You have a list of rooms, each with a size, and some rooms must be close to each other because people walk between them often. You want a plan in which no two rooms overlap, the house is small, and the walks are short. A chip is the same: the rooms are large circuit blocks, and the walks are the wires between them. Some blocks have a fixed size, and some can be made long and thin or short and wide. Very often the outline of the chip is given in advance, and then all blocks must fit inside it. Even small versions of this task are hard to solve exactly, so programs try many plans in a clever order and keep the best one.

## Definition

**Input.**

- Blocks $1, \ldots, n$. A *hard* block $i$ has a width $w_i$ and a height $h_i$, and may be allowed to turn by a quarter turn. A *soft* block $i$ has an area $A_i$ and limits $r_i^- \le h_i / w_i \le r_i^+$ on its aspect ratio, so its shape is free on the curve $w_i h_i = A_i$ between these limits.
- A netlist: a [hypergraph](/hypergraph/) whose vertices are the blocks and the fixed pins of the chip, and whose edges, the nets, have weights $c_e \ge 0$.
- Weights $\alpha, \beta \ge 0$ of area and wire length, or a fixed outline of width $W^*$ and height $H^*$.

**Output.** For each block a shape $(w_i, h_i)$ that it allows and a position $(x_i, y_i)$ of its lower-left corner, with $x_i, y_i \ge 0$, such that the rectangles $[x_i, x_i + w_i] \times [y_i, y_i + h_i]$ have disjoint interiors.

**Objective.** Let $W = \max_i (x_i + w_i)$ and $H = \max_i (y_i + h_i)$. The classical form minimizes

$$
\alpha \, W H + \beta \sum_{e} c_e \, \mathrm{HPWL}(e),
$$

where $\mathrm{HPWL}(e)$ is the [half-perimeter wire length](/half-perimeter-wirelength/) of the net $e$, with each block taken at its center. The fixed-outline form requires $W \le W^*$ and $H \le H^*$ and minimizes the wire length alone.

**Decision version.** Given hard blocks with integer sizes and fixed orientations and an outline $W^* \times H^*$, is there a packing of all blocks inside the outline?

## Variants

- **Hard or soft blocks.** Hard blocks give a choice of at most two shapes each, soft blocks a continuum. Mixed sets of both are common.
- **Rotation.** Hard blocks with a free orientation have two shapes, and mirror images are allowed as well when the pins of the blocks permit it.
- **Fixed outline.** The outline is given by the chip size or by the parent block in a hierarchical flow. This is the usual modern form, and it is harder for local search, since many candidates do not fit at all (Adya and Markov 2003).
- **Slicing only.** The floorplan must be a [slicing floorplan](/slicing-floorplan/). The best sizes of the blocks are then found exactly by [shape functions](/shape-function/), at the cost of some area.
- **Extra constraints.** Preplaced blocks, blocks on the boundary, alignment of blocks, a maximum distance between two blocks, and keep-out regions. Many of them are difference constraints on the coordinates and fit into the [constraint graphs](/floorplan-constraint-graphs/).
- **Other costs.** Timing on critical nets, routing congestion, power supply and heat, and the number of layers in 3D chips.

## Examples

**Three blocks.** Take $A$ of size $2 \times 2$, $B$ of size $1 \times 2$ and $C$ of size $1 \times 3$ (width times height), with no nets, so that only the area counts. The blocks have a total area of $9$.

- *Without rotation the least area is $10$.* Put $B$ at $(0, 0)$, $C$ at $(1, 0)$ and $A$ at $(0, 3)$: the chip is $2 \times 5$, with one empty unit square at $[0, 1] \times [2, 3]$. No packing has a smaller area. Every packing can be pushed down and to the left until each block touches the floor, the left wall or another block, without making the chip larger, and then $W$ and $H$ are sums of block sides, so they are integers. Since $W \ge 2$ for $A$ and $H \ge 3$ for $C$, an area at most $9$ leaves only the $3 \times 3$ square, with no empty space. There $C$ fills a whole column. If $C$ is not at a side, the two parts next to it are narrower than $2$, and $A$ fits in neither. So $C$ is at a side and $A$ and $B$ share a $2 \times 3$ part. The block $A$ fills the width of this part, so $B$ is above or below it, and the heights add up to $4 > 3$.
- *With rotation the least area is $9$.* Turn $B$ to $2 \times 1$ and put it at $(0, 0)$, $A$ at $(0, 1)$ and $C$ at $(2, 0)$: the $3 \times 3$ square is full.

**Area against wire length.** Add a net $\{A, C\}$ of weight $c$ to the rotated example. In the $3 \times 3$ packing the centers of $A$ and $C$ are at $(1, 2)$ and $(2.5, 1.5)$, so the net has length $1.5 + 0.5 = 2$ and the cost is $9 \alpha + 2 \beta c$. Now put $C$ at $(2, 0)$, $A$ at $(0, 0.5)$ and the turned $B$ at $(0, 2.5)$. The centers of $A$ and $C$ are at the same height, the net has length $1.5$, and the chip is $3 \times 3.5$, with the cost $10.5 \alpha + 1.5 \beta c$. The second packing is better exactly when $\beta c > 3 \alpha$, so the weights decide whether area or wire length wins.

**A pinwheel.** Two $1 \times 2$ blocks, two $2 \times 1$ blocks and a $1 \times 1$ block fill a $3 \times 3$ square in a pinwheel pattern, but every slicing floorplan of them with fixed orientations has area at least $10$, as the slicing floorplan page shows. So the slicing restriction can cost area.

## Known algorithms

- **Simulated annealing over slicing trees.** Wong and Liu (1986) search over normalized Polish expressions with [simulated annealing](/simulated-annealing/), and size each candidate with shape functions ([Wong-Liu floorplanning](/wong-liu-floorplanning/), [Stockmeyer floorplan sizing](/stockmeyer-floorplan-sizing/)).
- **Non-slicing representations.** The [sequence pair](/sequence-pair/) (Murata and others, 1995), the [O-tree](/o-tree-floorplan/) (Guo and others, 1999), the [B*-tree](/b-star-tree-floorplan/) (Chang and others, 2000) and the corner block list (Hong and others, 2000) each map a code to a packing in $O(n \log n)$ or $O(n)$ time, and annealing or other local search moves between codes.
- **Exact search.** Every packing has a sequence pair whose packing is no wider and no higher (Murata and others). So a search over all $(n!)^2$ sequence pairs, with all orientations, finds the least area exactly, but only for small $n$.
- **Integer programming.** For each pair of blocks, four binary choices say which of left, right, below and above holds, and big-M constraints turn the chosen relation into a linear inequality. This gives a [mixed integer program](/mixed-integer-programming/) whose size is $O(n^2)$, solved exactly for small $n$ or used to refine a part of a floorplan.
- **Fixed-outline floorplanners.** Parquet (Adya and Markov 2003) and later tools change the cost so that the search is pushed into the outline first, and then reduce the wire length.
- **Analytical and hierarchical methods.** Blocks are first spread by a smooth model of wire length and density, as in [analytical placement](/analytical-placement/), or split by [min-cut partitioning](/min-cut-placement/), and then made legal by a packing step.

## Bounds

- **NP-complete.** The decision version is NP-complete in the strong sense. It is in NP: a certificate is the relation (left, right, below or above) of each pair of blocks, and the longest paths in the two [constraint graphs](/floorplan-constraint-graphs/) check it in polynomial time, because any packing gives such relations and the longest path placement for them is no larger. The reduction from bin packing below gives the hardness.
- **Orientation.** For a fixed slicing floorplan, the best orientation of all hard blocks is found in $O(n d)$ time for a tree of depth $d$. For a general floorplan, given by its constraint graphs, the same question is NP-complete (Stockmeyer 1983).
- **Area lower bound.** The area is at least $\sum_i w_i h_i$, and at least $\max_i w_i \cdot \max_i h_i$. The examples above show that neither bound is always attained.
- **Size of the search spaces.** There are $n! \, S_{n-1}$ normalized Polish expressions, with the large Schröder numbers $S_{n-1}$, $n! \, B(n)$ labeled [mosaic floorplans](/mosaic-floorplan/), with the Baxter numbers $B(n)$, and $(n!)^2$ sequence pairs. The growth rates of $S_{n-1}$ and $B(n)$ are $3 + 2 \sqrt{2}$ and $8$ ([Baxter number theorem](/mosaic-floorplan-baxter-theorem/)).

## Reductions

- **From bin packing.** Take a bin packing instance with integer item sizes $s_1, \ldots, s_n$, bin capacity $C$ and $m$ bins. Make hard blocks $s_i \times 1$ with fixed orientation and the outline $C \times m$. If the items fit into $m$ bins, put bin $j$ in the row $[0, C] \times [j - 1, j]$. Conversely, given a packing in the outline, push each block straight down, in the order of increasing $y$, until it touches the floor or a block below it. By induction all $y$ values become integers, and the height does not grow. Then each row $[j - 1, j]$ holds blocks with disjoint $x$-intervals in $[0, C]$, which is a bin. Bin packing is strongly NP-complete, through [3-partition](/three-partition/), so the decision version of floorplanning is too ([strong NP-hardness](/strong-np-hardness/)).
- **To and from strip packing.** With a fixed width, no rotation, no nets and the height as the cost, floorplanning is exactly [strip packing](/strip-packing/), whose approximation results then apply.
- **To longest paths.** Once the relation of each pair of blocks is fixed, the coordinates are the [longest paths](/dag-longest-path/) in two directed acyclic graphs, which is how every representation above computes its packing.

## Applications

- **Chip planning.** Floorplanning fixes the places of large blocks and macros, the outline of the chip, and the regions for standard cells, before placement and routing.
- **Hierarchical design.** Each level of a large design is floorplanned inside the outline given by the level above it, which is why the fixed-outline form is the usual one.
- **FPGA and 3D chips.** The same problem appears with a grid of resources on an FPGA and with blocks spread over the layers of a 3D chip.
- **Layout of rooms and plants.** Facility layout in buildings and plants asks the same question with departments in place of blocks and the flow of goods in place of wires.

## References
