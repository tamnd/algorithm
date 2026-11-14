---
tag: 6Z081V
kind: problem
slug: global-routing
name: Global routing
aliases:
- loose routing
area: eda/routing
level: core
summary: Assign each net a route through a coarse grid of tiles so that the number of nets across each tile edge stays within its capacity.
prereqs: [steiner-tree-problem, multi-commodity-flow-problem, np-hard]
see_also: [detailed-routing, layer-assignment, negotiated-congestion-routing, rip-up-and-reroute, pattern-routing, multicommodity-flow-global-routing, rectilinear-steiner-tree-problem, edge-disjoint-paths]
sources:
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 5, Global Routing (5.2 terminology, 5.3 optimization goals, 5.4 representations of routing regions, 5.7 full-netlist routing and 5.8 modern global routing)
  - book: isbn:9780792383932
    title: Naveed A. Sherwani, Algorithms for VLSI Physical Design Automation, third edition, Kluwer, 1999
    locator: the chapter on global routing (the grid graph model, sequential and concurrent approaches; general locator)
  - paper: doi:10.1145/1353629.1353663
    title: Gi-Joon Nam, Cliff Sze and Mehmet Yildiz, The ISPD global routing benchmark suite, Proceedings of the International Symposium on Physical Design (ISPD), 2008
    locator: the benchmark format (gcell grid, layers, edge capacities, nets) and the ranking by total overflow, maximum overflow and wirelength
  - paper: "M. R. Garey and D. S. Johnson, The rectilinear Steiner tree problem is NP-complete, SIAM Journal on Applied Mathematics 32(4), 826 to 834, 1977"
    locator: the NP-completeness of the rectilinear Steiner tree problem, which gives the hardness of routing one net
  - paper: doi:10.1137/0205048
    title: S. Even, A. Itai and A. Shamir, On the complexity of timetable and multicommodity flow problems, SIAM Journal on Computing 5(4), 691 to 703, 1976
    locator: the NP-completeness of integral two-commodity flow
  - paper: doi:10.1007/BF02579324
    title: Prabhakar Raghavan and Clark D. Thompson, Randomized rounding, a technique for provably good algorithms and algorithmic proofs, Combinatorica 7(4), 365 to 374, 1987
    locator: the global wiring problem as a 0-1 multicommodity flow, its linear relaxation and the congestion bound after rounding
---

Global routing is the step of chip design, after [placement](/placement-problem/), that gives each net a coarse route. The chip is cut into a grid of rectangular tiles, called *gcells*, and each pair of neighbor tiles has a *capacity*: the number of wires that can cross their common side. A route of a net is a tree of tiles that holds all its pins, a [Steiner tree](/steiner-tree-problem/) in the grid graph. The goal is to choose one tree per net so that no tile boundary carries more nets than its capacity, and then to make the total wire length small. The problem is [NP-hard](/np-hard/), so routers are heuristics that are judged on benchmarks. This page states the problem. The methods are on the pages of the routers.

## In plain words

Think of the chip as a city of square blocks. The wires are cars, and each street between two blocks has only a few lanes. Every net is a group of houses that must be joined by roads. Global routing does not choose the exact lane of each wire. It only chooses which blocks each net passes through, like a trip plan on a map.

Two things count. First, no street may carry more cars than it has lanes. A street that carries too many is *overflowed*, and the wires there cannot be finished later. Second, among the plans with no overflow, short plans are better, because long wires are slow and use power.

The hard part is that the nets compete. The shortest plan for one net can take the last lane that another net needs.

## Definition

**Input.**

- A *global routing grid*: the grid graph $G = (V, E)$ of $W \times H$ gcells. Two gcells are joined by an edge when they share a side. Each edge $e$ has an integer capacity $c_e \ge 0$, the number of routing tracks across that side that are not blocked.
- A netlist with $m$ nets and $P$ pins, as on the [placement](/placement-problem/) page. Each pin lies in a gcell, so net $i$ gives a set $T_i \subseteq V$ of terminal gcells. Nets with $|T_i| = 1$ need no global route and are dropped.

**Feasible solution.** A *route* of net $i$ is a subtree $R_i$ of $G$ that contains every gcell of $T_i$. Only trees in which every leaf is a terminal are useful, since a leaf that is not a terminal can be cut off.

**Measures.** For a family of routes $R = (R_1, \ldots, R_m)$:

- the *usage* of edge $e$ is $u_e(R) = |\{ i : e \in R_i \}|$;
- the *overflow* of $e$ is $\max(0, u_e - c_e)$, the *total overflow* is $\mathrm{TOF}(R) = \sum_{e \in E} \max(0, u_e - c_e)$ and the *maximum overflow* is $\mathrm{MOF}(R) = \max_{e} \max(0, u_e - c_e)$;
- the *wirelength* is $\mathrm{WL}(R) = \sum_i |E(R_i)|$, in units of one gcell;
- the *congestion* is $\lambda(R) = \max_e u_e / c_e$, over the edges with $c_e > 0$.

**Objective.** The standard objective is lexicographic: minimize $\mathrm{TOF}$, then $\mathrm{MOF}$, then $\mathrm{WL}$. The routing is *legal*, or overflow-free, when $\mathrm{TOF} = 0$, that is $u_e \le c_e$ for every edge. The decision version asks: is there a legal routing with $\mathrm{WL} \le B$?

**Three-dimensional form.** A modern grid has $L$ routing layers, each with one preferred direction. Then $V$ has $W H L$ gcells, the edges inside a layer have capacities, and an edge between two layers is a *via*. The wirelength counts each via as a fixed number of gcell units. In the ISPD 2007 contest a via cost 3 units and in the ISPD 2008 contest it cost 1 unit.

## Variants

- **Two-dimensional and three-dimensional.** Most routers solve the problem on the 2D grid, with the capacities of all layers added up, and then do [layer assignment](/layer-assignment/) to put each segment on a layer.
- **Minimum congestion.** Minimize $\lambda(R)$ instead of the total overflow. For two-pin nets this is integral [multicommodity flow](/multi-commodity-flow-problem/) with one unit of demand per net, the form that Raghavan and Thompson studied.
- **Wire widths and spacing.** Net $i$ takes $w_i$ tracks, so $u_e = \sum_{i : e \in R_i} w_i$. Wide power or clock nets and nets with extra spacing use this form.
- **Timing-driven routing.** Critical nets get routes with short source-to-sink paths, measured by path length or by the [Elmore delay](/elmore-delay/) of the tree, with slack from [static timing analysis](/static-timing-analysis/).
- **Fixed candidate routes.** Each net chooses from a short list of routes, for example the [L-shaped and Z-shaped patterns](/pattern-routing/). The problem then is to choose one route per net, an integer program with one variable per candidate.
- **FPGA routing.** The graph is the routing-resource graph of the FPGA: wire segments and switches. Each node is a resource that one net can use, so the capacities are on the nodes and every capacity is 1.
- **Other cost functions.** Some formulations add a penalty for routes through crowded gcells, for coupling between neighbor wires, or for bends.

## Examples

Write each gcell as $(x, y)$, with $x$ the column and $y$ the row, both from 0.

**Two crossing nets, overflow is forced.** Take the $2 \times 2$ grid, with the 4 edges at capacity 1. Net A joins $(0,0)$ and $(1,1)$, and net B joins $(1,0)$ and $(0,1)$. Each net has exactly two routes of 2 edges, around one side of the square or the other, and a route of A meets each route of B in exactly one edge. So all 4 combinations have $\mathrm{TOF} = 1$, $\mathrm{MOF} = 1$, $\mathrm{WL} = 4$ and congestion $\lambda = 2$. If any one edge has capacity 2, the two nets can share that edge, and the optimum becomes $\mathrm{TOF} = 0$ with $\mathrm{WL} = 4$.

**A wrong shortest route blocks another net.** Take the $3 \times 3$ grid, with the 12 edges at capacity 1. Net A joins $(1,0)$ and $(0,1)$, and net B joins the corners $(0,0)$ and $(2,2)$. Net A has 8 routes (all simple paths) and 2 of them have the least length 2: through the corner $(0,0)$ or through the center $(1,1)$. Net B has 12 routes, and 6 of them have the least length 4.

- If A goes through the corner, it uses both edges of the corner gcell $(0,0)$. Every route of B starts at $(0,0)$, so $\mathrm{TOF} \ge 1$.
- If A goes through the center, it uses the edges $(1,0)(1,1)$ and $(1,1)(0,1)$. Of the 6 shortest routes of B, only two avoid both edges: along the bottom row and up the right column, or up the left column and along the top row.

Over all $8 \cdot 12 = 96$ pairs of routes, the least $(\mathrm{TOF}, \mathrm{WL})$ is $(0, 6)$, and exactly 2 pairs reach it. The example shows the coupling of the nets: both shortest routes of A are optimal for A alone, but only one of them fits with B.

## Known algorithms

| Method | Idea | What is known |
| --- | --- | --- |
| Sequential [maze routing](/lee-maze-routing/) | route the nets one at a time by a shortest path search with costs | each net gets a cheapest route for the current costs; the result depends on the order of the nets |
| [Rip-up and reroute](/rip-up-and-reroute/) | remove the routes through overflowed edges and route those nets again | no general convergence proof; measured |
| [Pattern routing](/pattern-routing/) | try only L-shaped and Z-shaped routes for each two-pin connection | $O(1)$ and $O(W + H)$ candidates per connection; fast first routing |
| [Negotiated congestion routing](/negotiated-congestion-routing/) | reroute all nets each round, with costs raised by present and past overuse | no general convergence proof; the base of NTHU-Route 2.0, which won the ISPD 2008 contest |
| [Multicommodity flow with rounding](/multicommodity-flow-global-routing/) | solve the fractional problem with an approximation scheme, then round | fractional congestion within a factor $1 + \varepsilon$ of optimal; rounding bound of Raghavan and Thompson |
| Steiner tree construction, for example [FLUTE](/flute/) | split each multi-pin net into two-pin connections before routing | exact rectilinear Steiner trees for nets of up to 9 pins by table lookup |

All the full-netlist routers in this table are heuristics for the problem as stated. What is proved is about single steps: a shortest path per connection, or an approximation of the fractional relaxation. Their quality on the whole problem is measured on benchmarks, mostly the ISPD 2007 and 2008 global routing suites.

## Bounds

**Hardness.** The problem is NP-hard in two separate ways.

- With one net and large capacities, an optimal route is a minimum Steiner tree of $T_1$ in the grid graph. This contains the [rectilinear Steiner tree problem](/rectilinear-steiner-tree-problem/) for terminals with integer coordinates. Garey and Johnson (1977) proved it NP-complete in the [strong sense](/strong-np-hardness/), so it stays NP-complete when the coordinates are bounded by a polynomial, and then the grid graph has polynomial size.
- With two-pin nets on a general graph and all capacities 1, a legal routing is a set of [edge-disjoint paths](/edge-disjoint-paths/), one per pair. Integral two-commodity flow is NP-complete (Even, Itai and Shamir, 1976), so deciding whether $\mathrm{TOF} = 0$ is NP-complete on general graphs.

**Wirelength lower bound.** A route of net $i$ is a connected set of gcells that holds $T_i$, so it has at least $\mathrm{hpwl}(T_i)$ edges, the [half-perimeter wirelength](/half-perimeter-wirelength/) of the bounding box in gcell units. So $\mathrm{WL}(R) \ge \sum_i \mathrm{hpwl}(T_i)$ for every $R$. For a net with 2 or 3 terminals and no overflow constraint, the bound is reached.

**Cut lower bound.** Let $S \subseteq V$, let $\delta(S)$ be the set of edges with one end in $S$, and let $k_S$ be the number of nets with terminals both in $S$ and outside $S$. Each such route is connected, so it uses at least one edge of $\delta(S)$. So $\sum_{e \in \delta(S)} u_e \ge k_S$, and

$$\mathrm{TOF}(R) \ \ge\ \sum_{e \in \delta(S)} (u_e - c_e) \ \ge\ k_S - \sum_{e \in \delta(S)} c_e.$$

**Relaxation bound.** For two-pin nets, let $\lambda^*$ be the optimum of the fractional relaxation, in which each net may split into paths with weights that add up to 1. Then $\lambda^* \le \lambda(R)$ for every routing $R$. The gap can be a factor 2: in the crossing example above, each net takes each of its two routes with weight $1/2$, every edge carries load 1, so $\lambda^* = 1$, while every integral routing has $\lambda = 2$. In the other direction, randomized rounding of the fractional solution gives congestion $O(\log m' / \log \log m') \cdot \max(\lambda^*, 1)$ with high probability, where $m'$ is the number of edges of the graph (Raghavan and Thompson, 1987; the proof is on the [randomized rounding](/randomized-rounding/) page).

## Reductions

- **From Steiner tree.** A [Steiner tree](/steiner-tree-problem/) instance in a grid graph is a global routing instance with one net and every capacity at least 1.
- **From edge-disjoint paths.** Pairs $(s_j, t_j)$ in a graph become two-pin nets on the same graph, with capacity 1 on each edge. A legal routing is a set of edge-disjoint paths.
- **To integer programming.** Give each net $i$ a set $\mathcal{R}_i$ of candidate routes and a 0-1 variable $x_{iR}$ per candidate. Then $\sum_{R \in \mathcal{R}_i} x_{iR} = 1$ for each net, and $\sum_i \sum_{R \ni e} x_{iR} \le c_e + o_e$ with an overflow variable $o_e \ge 0$ per edge. Minimizing $\sum_e o_e$ gives the total overflow over the candidates. The [LP relaxation](/lp-relaxation/) of this program, over all paths of two-pin nets, is a fractional multicommodity flow.
- **To detailed routing.** The routes of global routing are the input of [detailed routing](/detailed-routing/): each net must get exact tracks and vias inside the gcells that its route passes.

## Applications

- **Physical design flow.** Global routing runs after placement and before [detailed routing](/detailed-routing/). A legal global routing is the plan that the detailed router must follow, and an overflowed edge is a spot where detailed routing will likely fail.
- **Congestion estimation.** Placers call a fast global router to find crowded regions and to move cells away from them.
- **Layer and via planning.** The 2D routes are input to [layer assignment](/layer-assignment/), which decides the layers and the vias.
- **FPGA and board routing.** The same model, with the routing-resource graph or the board grid, routes nets on FPGAs and on printed circuit boards.

## References
