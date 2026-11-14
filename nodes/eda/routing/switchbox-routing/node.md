---
tag: 7Q2FNA
kind: problem
slug: switchbox-routing
name: Switchbox routing
aliases:
- switch box routing
area: eda/routing
level: advanced
summary: Route nets in a rectangle with pins fixed on all four sides, which unlike a channel cannot grow, so a router may fail.
prereqs: [detailed-routing, channel-routing-problem]
see_also: [channel-density, vertical-constraint-graph, greedy-channel-router, dogleg-channel-routing, channel-routing-np-completeness, lee-maze-routing, rip-up-and-reroute, layer-assignment]
sources:
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 6, Section 6.4 Switchbox Routing (terminology and switchbox routing algorithms)
  - book: isbn:9780792383932
    title: Naveed A. Sherwani, Algorithms for VLSI Physical Design Automation, third edition, Kluwer, 1999
    locator: the chapter on detailed routing, the part on switchbox routing (general locator)
  - paper: doi:10.1109/43.3208
    title: James P. Cohoon and Patrick L. Heck, BEAVER, a computational-geometry-based tool for switchbox routing, IEEE Transactions on Computer-Aided Design 7(6), 684 to 697, 1988
    locator: the switchbox router that applies several simple routers in turn and its results on benchmark switchboxes (general locator)
  - paper: "W. K. Luk, A greedy switch-box router, Integration, the VLSI Journal 3(2), 129 to 149, 1985"
    locator: the extension of the greedy channel router to pins on four sides (general locator)
  - paper: doi:10.1109/DAC.1984.1585792
    title: Gordon T. Hamachi and John K. Ousterhout, A switchbox router with obstacle avoidance, Proceedings of the 21st Design Automation Conference, 173 to 179, 1984
    locator: switchbox routing around obstacles inside the box (general locator)
  - paper: "Thomas G. Szymanski, Dogleg channel routing is NP-complete, IEEE Transactions on Computer-Aided Design 4(1), 1985"
    locator: the NP-completeness of routing a channel in a given number of tracks, which is a switchbox with no pins on the left and right sides (general locator)
---

Switchbox routing is a form of [detailed routing](/detailed-routing/) inside a rectangle whose four sides all carry fixed pins. The rectangle has a fixed number of columns and rows of tracks, and the router must connect the pins of every net inside it, with wires on two or more layers and vias between them. A switchbox appears where two channels meet, or where the cells around a region fix the pins on every side. In a [channel](/channel-routing-problem/), with pins on two sides only, the router can always add tracks until all nets fit. A switchbox cannot grow: its width and its height are fixed, so the question is whether a routing exists at all. That question is NP-complete. Switchbox routers are heuristics, and they are compared on a small set of benchmark switchboxes.

## In plain words

Think of a small square room with doors on all four walls. Each door has a color, and doors of the same color must be joined by a rope laid on the floor. Ropes of different colors may not touch, but there are two floors: on the lower floor ropes run only east to west, and on the upper floor only north to south. A rope can go up or down through a hole in the floor.

In a long corridor with doors on two walls only, you can always make the corridor wider until the ropes fit. The room cannot be made larger, because the walls of the room are fixed by the rooms around it. So it can happen that no way to lay the ropes exists, even though no wall looks too crowded.

## Definition

**Input.**

- A box of $w$ columns and $h$ rows. The grid points are $(x, y)$ with $0 \le x < w$ and $0 \le y < h$.
- Two layers in the *reserved-layer* model: on layer H, wires join $(x, y)$ and $(x+1, y)$; on layer V, wires join $(x, y)$ and $(x, y+1)$. A via joins the two layers at one grid point.
- Pins on the four sides. A top pin at column $x$ enters at $(x, h-1)$ on layer V, and a bottom pin at $(x, 0)$ on layer V. A left pin at row $y$ enters at $(0, y)$ on layer H, and a right pin at $(w-1, y)$ on layer H. Each pin has a net label, or is empty.

**Feasible solution.** For each net, a connected set of grid points on the two layers, joined by wire edges and vias, that holds the entry point of each of its pins. No grid point on one layer belongs to two nets.

**Objective.** The decision version asks whether a feasible routing exists. The optimization version minimizes the total number of wire edges, and then the number of vias. The values $w$ and $h$ are part of the input and may not change.

## Variants

- **Unreserved layers.** Each layer can hold wires in both directions. This allows more routings, and a net can turn without a via.
- **More than two layers.** The box has $L$ layers with alternating directions, as in a gcell of a modern router.
- **Obstacles and pins inside the box.** Some grid points are blocked, or some pins lie inside the box, as in the router of Hamachi and Ousterhout.
- **Gridless switchboxes.** Wires may have different widths and lie at any position that meets the spacing rules.
- **Channels.** A switchbox with no pins on its left and right sides and with $h$ free to grow is a [channel](/channel-routing-problem/).

## Examples

**One point.** Take $w = h = 1$. There is one grid point and four pins: top T, bottom B, left L and right R.

- If T and B belong to net 1 and L and R to net 2, net 1 uses layer V and net 2 uses layer H at the point. The routing is feasible with no vias.
- If T and L belong to net 1 and B and R to net 2, then net 1 needs both layers at the point, because its pins enter on V and on H. Net 2 also needs both layers there. So no routing exists.

**Two nets that swap rows.** Take $h = 2$ and any width $w \ge 2$. Net A has a left pin on row 0 and a right pin on row 1. Net B has a left pin on row 1 and a right pin on row 0. There are no top or bottom pins.

- *Cuts.* Each vertical cut between two columns is crossed by both nets and has $h = 2$ horizontal tracks. The horizontal cut between the rows is crossed by both nets and has $w \ge 2$ vertical tracks. So no cut is too crowded.
- *No routing exists.* A wire on layer H stays in its row, and the only way to change rows is a vertical edge on layer V in some column. With two rows, net A must use row 0 from column 0 to some column $a$, a vertical edge in column $a$, and row 1 from column $a$ to column $w - 1$. In the same way, net B uses row 1 from column 0 to some column $b$, and row 0 from column $b$ to column $w - 1$. On row 1, the parts $[a, w-1]$ of A and $[0, b]$ of B are disjoint, so $b < a$. On row 0, the parts $[0, a]$ of A and $[b, w-1]$ of B are disjoint, so $a < b$. Both cannot hold.
- *A larger box.* With $w = h = 3$, the left and right pins still on rows 0 and 1 and row 2 free, a routing exists. A runs on row 0 from column 0 to column 1, up column 1 to row 1, and on row 1 to column 2. B goes up column 0 from row 1 to row 2, along row 2 to column 2, and down column 2 to row 0. This uses 8 wire edges and 6 vias, and an exhaustive search finds no routing with fewer wire edges. With $w = 2$ and $h = 3$, the search finds no routing.

The second example shows that the cut conditions are necessary but not sufficient. A channel router facing the same conflict adds a track. A switchbox router cannot, so it fails.

## Known algorithms

| Method | Idea | What is known |
| --- | --- | --- |
| Exhaustive search, or integer programming and [SAT](/sat/) formulations | try all routings, or encode them as constraints | exact; exponential worst-case time; used only for small boxes |
| Greedy switchbox router (Luk 1985) | extend the [greedy channel router](/greedy-channel-router/) to pins on four sides | heuristic; measured on benchmark switchboxes |
| BEAVER (Cohoon and Heck 1988) | apply several simple routers in turn, then a maze router for the rest | heuristic; measured on benchmark switchboxes |
| [Maze routing](/lee-maze-routing/) with [rip-up and reroute](/rip-up-and-reroute/) | route the nets one at a time, then remove and reroute the nets that block others | heuristic; may fail on a routable box |

What is proved: the decision problem is NP-complete, and the cut conditions below are necessary. What is only measured: every practical switchbox router. Their papers report which benchmark switchboxes they complete and with how many vias and how much wire.

## Bounds

**Hardness.** A channel with a given number $t$ of tracks and no pins on its ends is a switchbox with $h = t$ and no left or right pins. Deciding whether a channel can be routed in $t$ tracks is NP-complete in the two-layer reserved model with doglegs (Szymanski, 1985), and the switchbox model above allows doglegs, since a net may use any connected set of points. So the switchbox decision problem is NP-complete. See [channel routing NP-completeness](/channel-routing-np-completeness/).

**Cut conditions.** Cut the box by a vertical line between two columns. Every net with pins on both sides of the line must cross it, and in the reserved model each crossing uses a horizontal track of its own. So the number of such nets is at most $h$. In the same way, the number of nets crossing a horizontal cut is at most $w$. This is the switchbox form of the [channel density](/channel-density/) bound. The conditions are necessary for every routing, but the examples above show that they are not sufficient.

**Wire length and vias.** Each net needs at least the length of a shortest rectilinear tree on its pins inside the box. In the reserved model, a net with both a horizontal and a vertical part needs at least one via, since the two parts lie on different layers.

## Reductions

- **From channel routing.** A channel instance with $t$ tracks is a switchbox instance with $h = t$ and empty left and right sides.
- **To integer programming.** A 0-1 variable for each net and each wire edge or via, with flow constraints for connectivity and one constraint per grid point and layer, gives an exact [integer program](/mixed-integer-programming/).
- **Inside detailed routing.** A detailed router that cuts the area into channels and switchboxes routes the channels first, which fixes the pins on the sides of the switchboxes, and then routes each switchbox.

## Applications

- **Building-block and macro layouts.** Where two routing channels meet, in an L or T shape, the region at the junction is a switchbox. Its pins are fixed by the channels that were already routed.
- **Gcell routing.** A gcell of a modern detailed router, with the global routes fixing where each net enters and leaves, is a small switchbox on several layers.
- **FPGA switch boxes.** The name is shared with the programmable switch boxes of FPGAs, where fixed wires on four sides meet. There the switches are fixed, and the routing problem is the choice of switch settings.

## References
