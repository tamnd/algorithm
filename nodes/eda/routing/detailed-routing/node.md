---
tag: GC4JSE
kind: problem
slug: detailed-routing
name: Detailed routing
aliases:
- final routing
area: eda/routing
level: core
summary: Give each net exact tracks, layers and vias inside the regions chosen by global routing, so that all design rules hold.
prereqs: [global-routing, vertex-disjoint-paths]
see_also: [switchbox-routing, channel-routing-problem, layer-assignment, lee-maze-routing, rip-up-and-reroute, design-rule-checking, multiple-patterning-decomposition, channel-routing-np-completeness]
sources:
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 6, Detailed Routing (6.1 terminology, 6.3 channel routing, 6.4 switchbox routing, 6.5 over-the-cell and gcell routing, 6.6 modern challenges), and Section 7.1 Area Routing
  - book: isbn:9780792383932
    title: Naveed A. Sherwani, Algorithms for VLSI Physical Design Automation, third edition, Kluwer, 1999
    locator: the chapters on detailed routing (channel and switchbox routing, the routing models and their constraints; general locator)
  - paper: doi:10.1145/1061425.1061430
    title: James F. Lynch, The equivalence of theorem proving and the interconnection problem, ACM SIGDA Newsletter 5(3), 31 to 36, 1975
    locator: the NP-completeness of connecting given pairs of points by disjoint paths (general locator)
  - paper: "M. R. Kramer and J. van Leeuwen, The complexity of wire-routing and finding minimum area layouts for arbitrary VLSI circuits, in F. P. Preparata (editor), Advances in Computing Research 2, VLSI Theory, JAI Press, 129 to 146, 1984"
    locator: the NP-completeness of routing two-pin nets by disjoint paths in a two-dimensional grid
  - paper: "Thomas G. Szymanski, Dogleg channel routing is NP-complete, IEEE Transactions on Computer-Aided Design 4(1), 1985"
    locator: the NP-completeness of deciding whether a channel can be routed in a given number of tracks in the two-layer model with doglegs (general locator)
---

Detailed routing is the step of chip design that turns the coarse plan of [global routing](/global-routing/) into real wires. Global routing says which tiles (gcells) a net passes through. Detailed routing chooses, for each net, the exact routing tracks on each metal layer and the exact positions of the vias between layers. The wires of different nets must not touch, and every design rule of the manufacturing process must hold: spacing, width, minimum area of a shape, and the rules for vias. The output is the final geometry that goes to the mask. Even its simplest form, disjoint paths for two-pin nets in a grid, is NP-complete. Detailed routers are heuristics, and they are judged on benchmarks by the number of rule violations that they leave, the wire length and the number of vias.

## In plain words

Global routing is like planning a trip on a road map: it picks the streets. Detailed routing is like choosing the exact lane on each street and the exact place where you change from one road to another. Two cars may not use the same lane at the same spot.

A chip has several layers of wires stacked on top of each other. On one layer two wires cannot cross, so to cross another wire a net goes up or down to another layer through a via. Vias are small, but each one costs space and can fail.

The factory also has rules: wires must keep a minimum distance, shapes must have a minimum size, and some patterns are not allowed. A routing that breaks a rule cannot be made. Detailed routing must connect every net and break no rule.

## Definition

**Input.**

- A routing graph $G = (V, E)$ for $L$ layers. The nodes are the points where a track of a layer meets a track of the layer above or below. Edges join neighbor points on the same track of one layer (*wire edges*) and the same point on two neighbor layers (*via edges*). On most layers the tracks run in one preferred direction.
- A set of nets. Each net $i$ has pins, each pin a set $P_{i,j} \subseteq V$ of nodes where the wire may touch it. Obstacles and the pins of other nets block nodes.
- Optionally, a *route guide* for each net: the gcells of its global route. The net should stay inside them.
- A set of design rules, given as conditions on the shapes of the wires and vias.

**Feasible solution.** For each net $i$, a connected subgraph $S_i$ of $G$ that meets each pin of the net, such that:

- no node is in two subgraphs $S_i$ and $S_j$ with $i \ne j$ (no *shorts*);
- the shapes of the wires and vias, drawn with their widths, satisfy every design rule.

**Objective.** The decision version asks for a feasible routing. In practice a router rarely finds one at once, so the objective is lexicographic: first the number of nets that are not connected (*opens*) and the number of rule violations, then the total wire length, the number of vias and the length outside the route guides. A routing with no opens, no shorts and no violations is *clean*.

**Gridded and gridless.** In the gridded form above, every wire lies on a track and the rules are checked between tracks. In the gridless form, wires can lie at any position that satisfies the rules, and the routing graph is built from the shapes.

## Variants

- **Channel routing.** The region is a rectangle with pins on two opposite sides, and the number of tracks can grow. See the [channel routing problem](/channel-routing-problem/).
- **Switchbox routing.** The region is a rectangle with pins on all four sides, and its size is fixed. See [switchbox routing](/switchbox-routing/).
- **Area routing.** The whole region of a block or a gcell window is one routing graph, as in [maze routing](/lee-maze-routing/).
- **Over-the-cell routing.** Some wires run over the standard cells on upper layers, instead of in the channels between cell rows.
- **Reserved-layer and unreserved models.** In the reserved model each layer has only one direction. In the unreserved model a layer can hold both directions.
- **Rules of advanced nodes.** End-of-line spacing, minimum area, via enclosure, rules that depend on the width or the length of parallel runs, and rules for [multiple patterning](/multiple-patterning-decomposition/), where the shapes of one layer must be split among several masks.

## Examples

Take a $3 \times 3$ grid of points $(x, y)$, $0 \le x, y \le 2$. Net A has pins at $(0,1)$ and $(2,1)$, on the middle of the left and right sides. Net B has pins at $(1,0)$ and $(1,2)$, on the middle of the bottom and top sides. All pins are on layer 1.

- **One layer.** A path of A goes from column 0 to column 2, so it has a node in column 1. Two of the three nodes of column 1 are the pins of B, so A must pass through $(1,1)$. In the same way, a path of B goes from row 0 to row 2, so it has a node in row 1, and the three nodes of row 1 are the two pins of A and the node $(1,1)$ that A uses. So no routing on one layer exists. A search over the 9 simple paths of A confirms it.
- **Two layers, both directions allowed.** Net A runs straight along the middle row on layer 1. Net B goes up a via at $(1,0)$, runs along the middle column on layer 2 through $(1,1)$, and goes down a via at $(1,2)$. This uses 4 wire edges and 2 vias.
- **Two vias are needed.** Some net must leave layer 1, because one layer is not enough. A net with all its pins on layer 1 that uses layer 2 goes up and comes back down, so it has at least 2 vias. A search over all 3498 simple paths of A on the two-layer grid, each with the best path of B around it, confirms the least cost: 2 vias and 4 wire edges.

The example shows why layers and vias are part of the problem: on one layer, the crossing nets are impossible, and the cost of a second layer is counted in vias.

## Known algorithms

| Method | Region | What is known |
| --- | --- | --- |
| [Left-edge algorithm](/left-edge-algorithm/) and [dogleg](/dogleg-channel-routing/) variants | channel | optimal number of tracks when there are no vertical constraints; heuristic otherwise |
| [Greedy channel router](/greedy-channel-router/) | channel | always finishes, by adding columns at the end of the channel if needed; measured on benchmark channels |
| [Lee maze routing](/lee-maze-routing/) and [line-probe routing](/line-probe-routing/) | area, one net at a time | a shortest path for each net, given the nets already routed |
| [Rip-up and reroute](/rip-up-and-reroute/), with search and repair of violations | area, gcell windows | no guarantee of a clean routing; measured |
| Switchbox routers such as BEAVER | switchbox | heuristic; measured on benchmark switchboxes |
| Integer programming and [SAT](/sat/) formulations | small windows, cell pins | exact with exponential worst-case time |

What is proved: hardness results, optimal track counts for special channel instances, and shortest paths for one net at a time. What is only measured: the quality of every full detailed router, on benchmark designs, by the counts of violations, the wire length and the vias.

## Bounds

**Hardness.**

- Connecting given pairs of nodes by vertex-disjoint paths is NP-complete in general graphs (Lynch, 1975), and it stays NP-complete in two-dimensional grid graphs (Kramer and van Leeuwen, 1984). A one-layer gridded detailed routing of two-pin nets is such a problem, so detailed routing is NP-hard already without design rules.
- Deciding whether a channel can be routed in a given number of tracks is NP-complete in the two-layer model with doglegs (Szymanski, 1985), and also without doglegs; see [channel routing NP-completeness](/channel-routing-np-completeness/).

**Lower bounds.**

- *Wire length.* Each net needs at least the length of a shortest tree that connects its pins, which is at least its half-perimeter wirelength.
- *Density.* In a channel, each column cut is crossed by every net with pins on both sides, and each net uses its own track there, so the number of tracks is at least the [channel density](/channel-density/). The same cut argument applies to every cut of a switchbox or a window.
- *Vias.* A net whose pins are all on layer 1 and that uses another layer has at least 2 vias, as in the example.

**Capacity from global routing.** A legal global routing keeps the number of nets across each gcell side within the number of tracks there. This is necessary for a clean detailed routing, but not sufficient: the nets must also fit inside each gcell, and the design rules can block tracks.

## Reductions

- **From vertex-disjoint paths in a grid.** Pairs of grid points become two-pin nets on one layer with no design rules. A routing is a set of [vertex-disjoint paths](/vertex-disjoint-paths/), so the NP-complete grid problem is a special case.
- **From global routing.** The route guides of [global routing](/global-routing/) restrict each net to a region, which splits the problem into smaller windows or channels.
- **To channel and switchbox routing.** Older flows cut the routing area into channels and switchboxes and route each one on its own, as in the [channel routing problem](/channel-routing-problem/) and [switchbox routing](/switchbox-routing/).
- **Layer choice.** When the 2D geometry of the wires is fixed, the choice of layers is the two-layer form of [layer assignment](/layer-assignment/).

## Applications

- **Physical design flow.** Detailed routing runs after global routing and before signoff checks. Its output is checked by [design rule checking](/design-rule-checking/), and the extracted wires go to timing analysis.
- **Engineering changes.** A small change of the netlist late in the design is routed by a detailed router on top of the existing wires.
- **Boards and packages.** The same problem, with board rules, routes printed circuit boards after [escape routing](/escape-routing/) of dense components.

## References
