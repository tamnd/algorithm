---
tag: JDBEDR
kind: problem
slug: layer-assignment
name: Layer assignment
aliases:
- via minimization
area: eda/routing
level: core
summary: Assign the segments of 2D routes to metal layers so that capacities hold and the number of vias is small.
prereqs: [global-routing, maximum-cut]
see_also: [detailed-routing, negotiated-congestion-routing, odd-cycle-transversal, planar-graph, bipartite-graph, mixed-integer-programming, static-timing-analysis, elmore-delay]
sources:
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 5, Global Routing, the routing layers, preferred directions and vias of the gcell grid (general locator)
  - book: isbn:9780792383932
    title: Naveed A. Sherwani, Algorithms for VLSI Physical Design Automation, third edition, Kluwer, 1999
    locator: the chapter on over-the-cell routing and vias, the constrained and unconstrained versions for two layers (general locator)
  - paper: "Ron Y. Pinter, Optimal layer assignment for interconnect, Journal of VLSI and Computer Systems 1(2), 123 to 137, 1984; first presented at the IEEE International Conference on Circuits and Computers (ICCC), 398 to 401, 1982"
    locator: the reduction of the two-layer constrained problem with junctions of degree at most 3 to maximum cut in a planar graph
  - paper: "F. Hadlock, Finding a maximum cut of a planar graph in polynomial time, SIAM Journal on Computing 4(3), 1975"
    locator: the polynomial algorithm for maximum cut in planar graphs, used by Pinter (general locator)
  - paper: doi:10.1109/12.42135
    title: N. J. Naclerio, S. Masuda and K. Nakajima, The via minimization problem is NP-complete, IEEE Transactions on Computers 38(11), 1604 to 1608, 1989
    locator: the NP-completeness of the two-layer constrained problem, also on a grid, with vias only at existing junctions, and with junction degree at most 6
  - paper: doi:10.1137/0402004
    title: Hyeong-Ah Choi, Kazuo Nakajima and Chong S. Rim, Graph bipartization and via minimization, SIAM Journal on Discrete Mathematics 2(1), 1989
    locator: the NP-completeness of the two-layer constrained problem when the junction degree is at most 4 (general locator)
  - paper: doi:10.1109/TCAD.1987.1270247
    title: K. C. Chang and David H.-C. Du, Efficient algorithms for layer assignment problem, IEEE Transactions on Computer-Aided Design 6(1), 67 to 78, 1987
    locator: layer assignment for two layers with fixed wire geometry (general locator)
  - paper: "K. C. Chang and David H.-C. Du, Layer assignment problem for three-layer routing, IEEE Transactions on Computers 37(5), 625 to 632, 1988"
    locator: the three-layer version of the constrained problem and its NP-completeness (general locator)
  - paper: "M. Grötschel, M. Jünger and G. Reinelt, Via minimization with pin preassignments and layer preference, Zeitschrift für Angewandte Mathematik und Mechanik (ZAMM) 69(11), 1989"
    locator: the exact solution of two-layer instances by maximum cut with branch and cut (general locator)
  - paper: "Tsung-Hsien Lee and Ting-Chi Wang, Congestion-constrained layer assignment for via minimization in global routing, IEEE Transactions on Computer-Aided Design 27(9), 1643 to 1656, 2008"
    locator: the layer assignment of a 2D global routing under per-layer edge capacities, with the via count as the objective (general locator)
---

Layer assignment is the step of routing that decides on which metal layer each piece of wire lies. A chip has several routing layers, and on most of them the wires run in one *preferred direction*, horizontal or vertical. A wire that changes layer needs a *via*, a vertical connection between two neighbor layers. Vias add resistance, they can fail in manufacturing, and they block tracks, so the number of vias should be small. The problem has two main forms. In the global form, the input is a 2D [global routing](/global-routing/), and each segment of each route gets a layer of the right direction so that the capacity of every layer holds. In the two-layer form of [detailed routing](/detailed-routing/), the wire geometry is fixed and each piece of wire gets one of the two layers, so that wires of different nets that cross are on different layers. The two-layer form, called constrained via minimization (CVM), is NP-complete in general and polynomial when no junction has degree more than 3. The global form is solved by heuristics that are measured on benchmarks.

## In plain words

Think of a building with several floors. On some floors the corridors run east to west, and on the others north to south. A plan on a map says which blocks each wire passes through, but not on which floor. Layer assignment chooses the floor for each piece of the plan.

A wire that turns from east-west to north-south must change floor, because no floor has both directions. Each change of floor is a via, like a staircase, and each staircase costs something. A wire that goes up to a high floor to avoid a crowded corridor pays for the stairs at both ends.

Each corridor on each floor holds only a few wires. So the goal is to fit every wire on the floors without overfull corridors, with as few stairs as possible.

## Definition

**Global form.**

- *Input.* A gcell grid as on the [global routing](/global-routing/) page, with 2D edges $E$. There are $L$ layers, numbered $1, \ldots, L$ from the bottom, and layer $\ell$ has a direction $\mathrm{dir}(\ell) \in \{\mathrm{H}, \mathrm{V}\}$. A 2D edge $e$ of direction $\mathrm{dir}(e)$ has an integer capacity $c_{e,\ell} \ge 0$ on each layer $\ell$ with $\mathrm{dir}(\ell) = \mathrm{dir}(e)$. Each net $i$ has a 2D route $R_i$, a tree in the grid, and each of its pins has a pin layer, usually layer 1.
- *Feasible solution.* For each net $i$, a map $a_i$ from the edges of $R_i$ to layers with $\mathrm{dir}(a_i(e)) = \mathrm{dir}(e)$.
- *Usage and overflow.* The usage of layer $\ell$ on edge $e$ is $u_{e,\ell} = |\{ i : e \in R_i,\ a_i(e) = \ell \}|$. The assignment is *legal* when $u_{e,\ell} \le c_{e,\ell}$ for all $e$ and $\ell$.
- *Vias.* For net $i$ and gcell $v$, let $\Lambda_i(v)$ be the set of layers of the edges of $R_i$ at $v$, together with the pin layer when $v$ holds a pin of net $i$. The net needs a stack of vias at $v$ from $\min \Lambda_i(v)$ to $\max \Lambda_i(v)$, so it has $\max \Lambda_i(v) - \min \Lambda_i(v)$ vias there, or 0 if $\Lambda_i(v)$ is empty. The via count is the sum over all nets and gcells.
- *Objective.* Find a legal assignment with the least via count. When no legal assignment exists, first minimize the total overflow $\sum_{e,\ell} \max(0, u_{e,\ell} - c_{e,\ell})$.

**Two-layer form with fixed geometry (CVM).**

- *Input.* A routed layout in the plane: for each net, a set of wire pieces that connect its pins, with the points where they meet (*junctions*) and the points where the wires of different nets cross. The *degree* of a junction is the number of pieces that meet there. A set of points where a via is allowed.
- *Feasible solution.* A layer, 1 or 2, for each part of each wire, where a wire can change layer only at an allowed via point. Two parts of different nets that cross or overlap must be on different layers.
- *Objective.* Minimize the number of points where a wire changes layer, that is, the number of vias.

The *unconstrained* version also chooses the wire geometry, so it is a full two-layer routing problem.

## Variants

- **Number of layers.** Two layers with preferred directions leave no choice in the global form: horizontal edges go to the H layer and vertical edges to the V layer. The problem needs three or more layers to have choices.
- **No preferred direction.** Some layers, often on boards, allow both directions. Then an edge can go on any layer, and a turn does not force a via.
- **Via capacity.** A via stack from layer 1 to layer 5 passes through layers 2, 3 and 4 and blocks part of their tracks in that gcell. Some formulations count this usage against the capacity of the gcell.
- **Timing-driven assignment.** Upper layers are thicker and have less resistance per unit length, so critical nets go to upper layers. The cost then includes the delay of the net, for example its [Elmore delay](/elmore-delay/), with the slack from [static timing analysis](/static-timing-analysis/).
- **Pin layers and stacked via limits.** Pins can lie on different layers, and design rules can limit the height of a via stack.
- **Three-layer and multilayer CVM.** The fixed-geometry form with more than two layers.

## Examples

**Moving a long net up is cheaper than moving a short net.** Take three layers: layer 1 horizontal, layer 2 vertical and layer 3 horizontal. Every layer edge has capacity 1, and all pins are on layer 1. Gcells are $(x, y)$.

- Net A has pins at $(0,0)$ and $(2,1)$, and its 2D route is $(0,0)$, $(1,0)$, $(2,0)$, $(2,1)$: two horizontal edges and one vertical edge.
- Net B has pins at $(1,0)$ and $(2,0)$, and its 2D route is the one horizontal edge between them.

The edge $(1,0)(2,0)$ carries both nets, and it has capacity 1 on layer 1 and 1 on layer 3. So one of the two nets must use layer 3 there. The vertical edge of A goes to layer 2. Each net has at most two horizontal edges with two choices each, so there are 8 assignments, and 4 of them are legal:

| A on $(0,0)(1,0)$ | A on $(1,0)(2,0)$ | B | vias of A | vias of B | total |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 1 | 2 at $(1,0)$, 1 at $(2,0)$, 1 at $(2,1)$: 4 | 0 | 4 |
| 3 | 3 | 1 | 2 at $(0,0)$, 1 at $(2,0)$, 1 at $(2,1)$: 4 | 0 | 4 |
| 1 | 1 | 3 | 1 at $(2,0)$, 1 at $(2,1)$: 2 | 2 at each pin: 4 | 6 |
| 3 | 1 | 3 | 2, 2, 1 and 1: 6 | 4 | 10 |

The least via count is 4, and two assignments reach it. Without the capacity, both nets stay on layers 1 and 2 with 2 vias. So the capacity costs 2 extra vias. Moving B costs 4, because B has a pin at each end of its only segment and each pin needs a stack of 2 vias to layer 3. Moving A costs only 2.

**An odd cycle of crossings forces a via.** In the two-layer form, take three straight wires of three nets, $a$, $b$ and $c$, laid out like the sides of a triangle with long ends, so that each wire crosses the other two. Without vias, each wire has one layer, and the three crossings ask for three pairwise different layers out of two, which is impossible. One via on $a$, between its crossing with $b$ and its crossing with $c$, is enough: put the part of $a$ that crosses $b$ on layer 2, $b$ on layer 1, $c$ on layer 2 and the part of $a$ that crosses $c$ on layer 1. Every crossing now joins two different layers, so the least number of vias is 1.

In general, the parts of the wires and the crossings between them form a *conflict graph*, and a solution with no vias exists exactly when this graph is [bipartite](/bipartite-graph/). Each via cuts a wire into two parts, so the problem asks for the fewest cuts that make the conflict graph bipartite. This is close to [odd cycle transversal](/odd-cycle-transversal/).

## Known algorithms

| Method | Form | What is known |
| --- | --- | --- |
| Forced assignment | global form, two layers with preferred directions | no choice; the via count is fixed by the 2D routes |
| Dynamic programming over the tree of one net | global form, one net, the other nets fixed | optimal for that net, in time polynomial in the size of the tree and $L$ |
| Net by net assignment with dynamic programming (Lee and Wang 2008) | global form, many nets | heuristic; measured on global routing benchmarks |
| [Integer programming](/mixed-integer-programming/) with one 0-1 variable per net, edge and layer | global form, small instances | exact, with exponential worst-case time |
| Reduction to maximum cut in a [planar graph](/planar-graph/) (Pinter 1982) | CVM, two layers, junction degree at most 3 | optimal, in polynomial time |
| [Maximum cut](/maximum-cut/) by branch and cut (Grötschel, Jünger and Reinelt 1989) | CVM, general | exact on the instances tried, with no polynomial bound |

What is proved: the two-layer CVM with junctions of degree at most 3 is solved exactly in polynomial time, and so is the global form for a single net. What is only measured: every method for the global form with many nets and capacities. Those methods are compared by their via counts and overflow on routing benchmarks, mostly the ISPD 2007 and 2008 global routing suites.

## Bounds

**Overflow-free assignment.** Ignore the vias. The edges are then independent, so a legal assignment exists exactly when, for every 2D edge $e$, the number of nets on $e$ is at most $\sum_{\ell : \mathrm{dir}(\ell) = \mathrm{dir}(e)} c_{e,\ell}$. So the hard part of the global form is the via count, not the capacity alone.

**Via lower bounds in the global form.**

- At a gcell where the route of a net has both a horizontal and a vertical edge, the layers in $\Lambda_i(v)$ have both directions, so they differ and the net needs at least 1 via there.
- At a pin on layer $p$, the net needs at least $\min_\ell |\ell - p|$ vias, where $\ell$ runs over the layers with the direction of an edge of the route at that pin.

Taking the larger of the two bounds at each gcell and adding over all nets and gcells gives a lower bound for every assignment. In the first example above, the bound is 2, the value without capacities.

**Hardness of the two-layer form.**

- CVM with junctions of degree at most 3 reduces to maximum cut in a planar graph, which Hadlock (1975) solved in polynomial time. So this case is in P (Pinter 1982, 1984).
- CVM is NP-complete in general (Naclerio, Masuda and Nakajima, 1989). It stays NP-complete when the layout lies on a grid, when vias may lie only at existing junctions, and when no junction has degree more than 6.
- Choi, Nakajima and Rim (1989) lowered the degree bound to 4. So the line between polynomial and NP-complete lies between degree 3 and degree 4, unless P = NP.
- Chang and Du (1988) showed that the three-layer version is NP-complete.

**Hardness of the global form.** With many nets, capacities and three or more layers, no polynomial exact method is known, and the published routers do not claim one.

## Reductions

- **From global routing.** The 2D routes of [global routing](/global-routing/) are the input of the global form. The edge capacities of the 2D grid are the sums of the per-layer capacities.
- **CVM with degree at most 3 to planar maximum cut.** The layer choices of the wire parts become the two sides of a cut in a planar graph built from the layout, and a cheapest set of vias corresponds to a maximum cut (Pinter).
- **CVM to graph bipartization.** Delete the fewest vertices or cut the fewest wires so that the conflict graph becomes bipartite; this is the form that Choi, Nakajima and Rim study, and it is close to [odd cycle transversal](/odd-cycle-transversal/).
- **To integer programming.** A 0-1 variable $x_{i,e,\ell}$ for each net, edge and layer, with $\sum_\ell x_{i,e,\ell} = 1$, capacity rows $\sum_i x_{i,e,\ell} \le c_{e,\ell}$ and via variables at each gcell, gives an exact [integer program](/mixed-integer-programming/).

## Applications

- **3D global routing.** Many global routers route on the 2D grid with the capacities of all layers added up, and then run layer assignment to get a 3D routing. This is faster than routing on the 3D grid directly.
- **Timing closure.** Critical nets go to the upper layers, which have lower resistance, and nets that are not critical stay low.
- **Yield and reliability.** Each via is a point that can fail, so fewer vias give a more reliable chip. Routers also add redundant vias where there is room.
- **Two-layer boards.** On printed circuit boards with two signal layers, the fixed-geometry form decides which side of the board each trace takes.

## References
