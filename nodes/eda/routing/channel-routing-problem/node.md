---
tag: 8FNZ68
kind: problem
slug: channel-routing-problem
name: Channel routing problem
aliases:
- two-layer channel routing
area: eda/routing
level: core
summary: Connect the pins on the top and bottom edges of a rectangular channel with trunks on one layer and branches on the other, in the fewest tracks.
prereqs: [detailed-routing, channel-density]
see_also: [channel-density, vertical-constraint-graph, left-edge-algorithm, dogleg-channel-routing, greedy-channel-router, yoshimura-kuh-algorithm, channel-routing-np-completeness, river-routing]
sources:
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 6, Detailed Routing, the section on channel routing (the channel model, horizontal and vertical constraints, the left-edge, dogleg and greedy routers; general locator)
  - book: isbn:9780792383932
    title: Naveed A. Sherwani, Algorithms for VLSI Physical Design Automation, third edition, Kluwer, 1999
    locator: the chapter on detailed routing, the part on channel routing (routing models, the constraint graphs and the classical channel routers; general locator)
  - paper: "A. S. LaPaugh, Algorithms for Integrated Circuit Layout, An Analytic Approach, PhD thesis, MIT, report MIT/LCS/TR-248, 1980"
    locator: the NP-completeness of channel routing without doglegs (general locator)
  - paper: doi:10.1109/TCAD.1985.1270096
    title: Thomas G. Szymanski, Dogleg channel routing is NP-complete, IEEE Transactions on Computer-Aided Design 4(1), 31 to 41, 1985
    locator: the NP-completeness of channel routing in a given number of tracks when nets may dogleg
  - paper: "D. N. Deutsch, A dogleg channel router, Proceedings of the 13th Design Automation Conference, 425 to 433, 1976"
    locator: the dogleg router and the large test channel that later papers call Deutsch's difficult example (general locator)
  - paper: "M. Burstein and R. Pelavin, Hierarchical channel router, Integration, the VLSI Journal 1, 1983"
    locator: the hierarchical router and its result on Deutsch's difficult example (general locator)
---

The channel routing problem is the classical form of [detailed routing](/detailed-routing/) in chip layout. A channel is a rectangle between two rows of cells. Pins lie on its top and bottom edges, and each pin belongs to a net. The task is to connect the pins of every net inside the channel, with horizontal wires (trunks) on one layer and vertical wires (branches) on another, so that wires of different nets never share a point of the same layer. The width of the channel is the number of horizontal tracks, and it is the objective: fewer tracks give a smaller chip. Unlike a [switchbox](/switchbox-routing/), a channel can always grow, so the question is how many tracks are needed, not whether a routing exists. The [channel density](/channel-density/) is a lower bound, and the decision version is NP-complete, with or without doglegs.

## In plain words

Picture a long corridor with doors on the north wall and on the south wall. Each door has a color, and all doors of the same color must be joined by rope. Ropes that run along the corridor lie on the lower floor, in lanes. Ropes that run across the corridor lie on the upper floor, and a rope can go between the floors through a hole.

Ropes of different colors may not touch on the same floor. The goal is to use as few lanes as possible, since each lane makes the corridor wider.

Two things make this hard. Where two colors meet at the same spot along the corridor, they need different lanes. Where one door on the north wall faces a door of another color on the south wall, the north rope must use a lane closer to the north wall.

## Definition

**Input.**

- A number of columns $n$, and for each column $c \in \{1, \ldots, n\}$ a top pin $\mathrm{top}(c)$ and a bottom pin $\mathrm{bot}(c)$. Each pin is the label of a net, or 0 for no pin.
- A net is a label that appears on at least two pins. Its interval $I_N = [l_N, r_N]$ runs from its leftmost to its rightmost pin column. Nets with all pins in one column are routed by a straight branch and are left out.

**Routing grid in the reserved two-layer model.** For $T$ tracks, the grid has the points $(c, y)$ with $1 \le c \le n$ and $0 \le y \le T + 1$. Track $t$ is the row $y = t$, numbered from the top. Row 0 is the top edge and row $T + 1$ the bottom edge.

- Layer H holds trunks: edges from $(c, t)$ to $(c + 1, t)$ for $1 \le t \le T$.
- Layer V holds branches: edges from $(c, y)$ to $(c, y + 1)$.
- A via joins the two layers at one point $(c, t)$.
- The top pin of column $c$ is the point $(c, 0)$ on layer V, and the bottom pin is $(c, T + 1)$ on layer V. The edge rows hold no other wire.

**Feasible solution.** For each net, a set of points on the two layers, with edges and vias, that is connected and holds all the pins of the net. No point of a layer belongs to two nets. This is the Manhattan model: wires run only horizontally and vertically.

**Objective.** Minimize $T$. The decision version asks, for a given $k$, whether a feasible routing with $T \le k$ exists.

**Constraints that every routing meets.**

- *Horizontal.* Two nets whose intervals meet need different tracks in each column that both cross.
- *Vertical.* If column $c$ has top pin $a$ and bottom pin $b \ne a$, the branch of $a$ comes down from row 0 and the branch of $b$ comes up from row $T + 1$ in the same column. So the point where $a$ leaves the column must be above the point where $b$ leaves it. These constraints form the [vertical constraint graph](/vertical-constraint-graph/).

## Variants

- **No doglegs.** Each net uses exactly one trunk on one track. A solution is a map from nets to tracks. This is the model of the [left-edge algorithm](/left-edge-algorithm/) and of the [Yoshimura-Kuh algorithm](/yoshimura-kuh-algorithm/).
- **Doglegs at pin columns.** A net may change track only in a column where it has a pin. This is the model of [dogleg channel routing](/dogleg-channel-routing/).
- **Unrestricted doglegs.** A net may change track in any column, if the branch layer is free there. The [greedy channel router](/greedy-channel-router/) works in this model.
- **Extension columns.** Wires may leave the channel through its open left and right ends. The greedy router uses this to finish every channel.
- **Unreserved layers.** Both layers carry wires in both directions, and wires may cross on different layers at a point. The knock-knee model, where two nets may bend at the same point, is a further relaxation.
- **More layers.** Three-layer channels use HVH or VHV, with two trunk layers or two branch layers.
- **Secondary objectives.** Among routings with the fewest tracks, minimize the total wire length or the number of vias.
- **One layer.** With one layer, no crossings are possible at all, and the pins must be in the same order on both sides. This is [river routing](/river-routing/).

## Examples

**Four nets in two tracks.** Take $n = 8$ with

| column | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| top | 1 | 0 | 2 | 1 | 3 | 0 | 4 | 0 |
| bottom | 0 | 2 | 0 | 3 | 0 | 4 | 0 | 3 |

The intervals are $I_1 = [1, 4]$, $I_2 = [2, 3]$, $I_3 = [4, 8]$ and $I_4 = [6, 7]$, and the density is 2. The only vertical constraint comes from column 4: net 1 is on top and net 3 at the bottom, so net 1 must be on a higher track than net 3. One optimal routing is

| track | trunks |
| --- | --- |
| 1 | net 1 on columns 1 to 4, net 4 on columns 6 to 7 |
| 2 | net 2 on columns 2 to 3, net 3 on columns 4 to 8 |

and each pin gets a branch from its edge to the trunk of its net. In column 4, the branch of net 1 runs from row 0 to track 1, and the branch of net 3 from row 3 to track 2, so they do not meet. One track is not enough, because columns 2 and 3 hold two nets each.

**A channel with no routing without doglegs.** Take $n = 2$, with top pins $1, 2$ and bottom pins $2, 1$. Column 1 needs net 1 above net 2, and column 2 needs net 2 above net 1. No map from nets to tracks meets both, for any number of tracks. With jogs in any column and one extra column past the right end, three tracks are enough. The page on [channel density](/channel-density/) shows that two tracks are never enough, so the optimum in that model is 3, while the density is 2.

**Deutsch's difficult example.** A channel published by Deutsch in 1976 became the standard test case of the field. Its density is 19. Burstein and Pelavin reported in 1983 that their hierarchical router routed it in 19 tracks, and that the routers known to them needed 20 or more. These are measured results on one instance, not proved bounds for a method.

## Known algorithms

| Method | Model | What is known |
| --- | --- | --- |
| [Left-edge algorithm](/left-edge-algorithm/) (Hashimoto and Stevens 1971) | no doglegs | optimal, with $d$ tracks, when there are no vertical constraints; with constraints a heuristic that fails on a cycle |
| [Dogleg channel routing](/dogleg-channel-routing/) (Deutsch 1976) | doglegs at pin columns | heuristic; breaks some cycles of the constraint graph |
| [Yoshimura-Kuh algorithm](/yoshimura-kuh-algorithm/) (1982) | no doglegs, with a dogleg form | heuristic that merges nets to keep the longest constraint path short |
| [Greedy channel router](/greedy-channel-router/) (Rivest and Fiduccia 1982) | unrestricted doglegs, extension columns | always finishes; the track count is measured, not bounded |
| Hierarchical channel router (Burstein and Pelavin 1983) | doglegs | heuristic; measured on Deutsch's difficult example |
| Exhaustive search, branch and bound, integer programming | any | exact; exponential in the worst case |

What is proved: the density bound, the constraint graph bound in the model without doglegs, the optimality of left-edge without vertical constraints, the completion of the greedy router, and the NP-completeness results below. What is only measured: the track counts of every heuristic on channels with vertical constraints.

## Bounds

**Lower bounds.**

- *Density.* Every routing in the reserved two-layer model uses at least $d$ tracks, with or without doglegs. The proof is on the page on [channel density](/channel-density/).
- *Longest constraint path.* Without doglegs, if the vertical constraint graph has a path through $k$ nets, those nets lie on $k$ different tracks in a fixed order, so $T \ge k$. Doglegs can beat this bound, so it does not hold in the dogleg models.

**Feasibility without doglegs.** A routing without doglegs exists if and only if the vertical constraint graph has no cycle. If there is a cycle $N_1 \to N_2 \to \cdots \to N_k \to N_1$, the tracks would have to satisfy $t(N_1) < t(N_2) < \cdots < t(N_1)$. If there is no cycle, put the nets on tracks $1, 2, \ldots$ in a [topological order](/topological-sort/), one net per track. Every horizontal constraint holds because no two nets share a track, and every vertical constraint holds because of the order. So $N$ tracks always suffice for an acyclic channel with $N$ nets.

**Feasibility with extension columns.** With jogs in any column and wires allowed past the ends, every channel can be routed. The [greedy channel router](/greedy-channel-router/) is a proof by construction.

**Hardness.** Deciding whether a channel can be routed in $k$ tracks is NP-complete without doglegs (LaPaugh 1980) and with doglegs (Szymanski 1985). The statements and the proof outline are on the page on the [NP-completeness of channel routing](/channel-routing-np-completeness/). So no polynomial algorithm is known that always finds the fewest tracks, and none exists unless P = NP.

**Polynomial cases.** With no vertical constraints, the problem without doglegs is [interval partitioning](/interval-partitioning/), solved exactly in $O(N \log N)$ time, and the optimum is $d$. If every two intervals meet, each net needs its own track, so the optimum without doglegs is $N$ when the constraint graph is acyclic.

## Reductions

- **To interval partitioning.** Without vertical constraints and without doglegs, a track is a set of disjoint intervals, and the problem is to partition the intervals into the fewest such sets.
- **To switchbox routing.** A channel with $T$ tracks is a [switchbox](/switchbox-routing/) of height $T$ with no pins on its left and right sides. So hardness results for channels carry over to switchboxes.
- **From detailed routing.** Flows of the 1970s and 1980s cut the routing area into channels and switchboxes. A global router chose the channel of each net, and the channel router then fixed the tracks.
- **One layer.** With one layer instead of two, the problem becomes [river routing](/river-routing/), which has exact linear-time tests.

## Applications

- **Standard-cell and gate-array layout.** In layouts with two or three metal layers, the cells sit in rows with routing channels between them. The total area depends on the sum of the channel widths.
- **Building-block layout.** Between large blocks, the free space is cut into channels and switchboxes, and each channel is routed on its own.
- **Teaching and analysis.** In designs with many metal layers, most routing runs over the cells, and gridded area routers replaced channel routers. The channel model stays the simplest setting in which the density bound, constraint graphs and NP-hardness of routing can be stated exactly.

## References
