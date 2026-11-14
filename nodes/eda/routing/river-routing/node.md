---
tag: JET387
kind: problem
slug: river-routing
name: River routing
aliases:
- single-layer planar routing
area: eda/routing
level: advanced
summary: Connect two rows of terminals in order by non-crossing wires on one layer. Leiserson and Pinter and others give exact tests of separation in linear time.
prereqs: [channel-routing-problem]
see_also: [channel-density, detailed-routing, vertex-disjoint-paths, planar-graph, max-flow-min-cut-theorem, channel-routing-np-completeness, switchbox-routing, escape-routing]
sources:
  - paper: doi:10.1137/0212029
    title: Charles E. Leiserson and Ron Y. Pinter, Optimal placement for river routing, SIAM Journal on Computing 12(3), 447 to 462, 1983
    locator: the conditions for routing two rows of terminals in a channel of given width, and the optimal offset of the two rows (general locator)
  - paper: doi:10.1016/0022-0000(81)90010-6
    title: Martin Tompa, An optimal solution to a wire-routing problem, Journal of Computer and System Sciences 23(2), 127 to 150, 1981
    locator: the least width of a single-layer channel for terminals in order on two sides; first presented at STOC 1980, 161 to 176 (general locator)
  - book: isbn:9780792383932
    title: Naveed A. Sherwani, Algorithms for VLSI Physical Design Automation, third edition, Kluwer, 1999
    locator: the chapter on detailed routing, the part on single-layer routing (general locator)
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 6, Detailed Routing (general locator; single-layer routing as a special case of channel routing)
---

River routing is the form of [channel routing](/channel-routing-problem/) with only one layer. Two rows of terminals face each other across a channel, terminal $i$ on the top must be joined to terminal $i$ on the bottom, and the wires may not cross or touch, since there is no second layer to pass over. The name comes from the picture of wires that flow side by side like a river. The terminals must be in the same order on both sides, or no routing exists. Unlike two-layer channel routing, which is NP-complete, river routing has exact answers in linear time: whether a channel of a given width is wide enough, how wide it must be, and how far one row may be shifted against the other. Leiserson and Pinter in 1983 and Tompa in 1980 gave such results.

## In plain words

Picture two rows of posts on the two banks of a river, numbered from left to right. Each post on the north bank must be joined by a string to the post with the same number on the south bank. The strings lie flat on the ground and may not cross or touch, and they may only run north to south or east to west, on the lines of a grid.

If a post on the north bank is far to the left of its partner, its string must run across the river at a slant, in steps. Strings next to it must then make the same steps, and a group of strings that all go the same way needs room. The question is how wide the river must be so that all strings fit.

## Definition

**Input.**

- Two sequences of integers $a_1 < a_2 < \cdots < a_n$ and $b_1 < b_2 < \cdots < b_n$, the columns of the top terminals and of the bottom terminals.
- A width $h \ge 1$, the number of rows inside the channel.

**Grid.** The routing grid is the unit grid graph on the points $(x, y)$ with $x$ any integer and $0 \le y \le h + 1$. Rows 1 to $h$ are the inside of the channel. Top terminal $i$ is the point $(a_i, h + 1)$, and bottom terminal $i$ is the point $(b_i, 0)$. The channel is open to the left and to the right, so its length is not limited.

**Feasible solution.** For each $i$, a path in the grid from $(b_i, 0)$ to $(a_i, h + 1)$ whose other points are all inside the channel, such that the $n$ paths are vertex-disjoint. This is the one-layer Manhattan model.

**Questions.**

- *Routability.* Given $a$, $b$ and $h$, does a feasible solution exist?
- *Least width.* Given $a$ and $b$, find the least $h$ that is routable.
- *Offset.* Given the two rows up to a shift $s$ of the top row (so $a_i + s$ in place of $a_i$), find the shifts for which a width $h$ is routable, or the least width over all shifts. Leiserson and Pinter call this the placement problem for river routing.

**Order.** Terminal $i$ is joined to terminal $i$. A layout with wires on one layer is a planar drawing, and two wires that connect the rows in a different order would have to cross, so the order condition is part of the definition, not an extra rule.

## Variants

- **Fixed length.** The channel has a given length as well as a given width. Wires must then stay between the outer columns.
- **Several rows of terminals.** Terminals on more than two sides, or on blocks inside the region. The general one-layer routing of many nets around obstacles is harder.
- **Other wire shapes.** Wires at 45 degrees, or in the Euclidean plane, with a minimum distance between wires. The width bounds change, but the method of cuts below stays.
- **Minimum wire length or bends.** Among routings in the least width, minimize the total length or the number of bends.
- **Two-layer channel routing.** With a second layer the order condition goes away, and the problem becomes the [channel routing problem](/channel-routing-problem/).

## Examples

**A shift by one.** Top $a = (2, 3, 4, 5)$, bottom $b = (1, 2, 3, 4)$. Each wire must move one column to the right, into the column where the next wire starts. For $h = 3$ the cut condition fails, since $b_4 - a_1 = 2 < 3$, so four wires would have to pass a diagonal with three points. The least width is 4, one row for the step of each wire: wire 4 turns in row 1, wire 3 in row 2, and so on.

**Rows far apart.** Top $a = (1, 2, 3)$, bottom $b = (4, 5, 6)$. For $h = 1$ and $h = 2$ the cut condition fails ($a_2 - b_1 = -2$ and $a_3 - b_1 = -1$), and for $h = 3$ there is nothing to check, so the least width is 3. Wire 1 turns left in row 1, wire 2 in row 2 and wire 3 in row 3.

**Rows that interleave.** Top $a = (1, 3, 5)$, bottom $b = (2, 4, 6)$. A width of 1 is enough: wire $i$ goes up from $(2i, 0)$ to row 1, left to column $2i - 1$, and up to the top. The wires use the columns $2i - 1$ and $2i$ in row 1, which are all different.

**A mixed case.** Top $a = (1, 2, 6, 7)$, bottom $b = (3, 4, 5, 6)$. A width of 1 fails, because $a_2 - b_1 = -1 < 1$: wires 1 and 2 start at columns 3 and 4 and end at columns 1 and 2, so both must pass the single point $(3, 1)$ of the diagonal. For $h = 2$ the four differences $a_3 - b_1$, $a_4 - b_2$, $b_3 - a_1$ and $b_4 - a_2$ are 3, 3, 4 and 4, all at least 2, so the least width is 2.

**Out of order.** If the top row lists the nets as 1, 2 and the bottom row as 2, 1, no width is enough, while a two-layer channel routes the same pins.

## Known algorithms

The exact algorithms are in the cited papers, and this page does not list their steps.

| Question | What is known |
| --- | --- |
| Routability for given $h$ | decided in linear time (Leiserson and Pinter 1983); the cut condition below takes $O(n)$ time for one $h$ |
| Least width | found exactly (Tompa 1980 and 1981); with the cut condition, a binary search over $h$ takes $O(n \log n)$ time |
| Offset | the shifts of one row that allow a given width are found in linear time (Leiserson and Pinter 1983) |
| Routability for any width, by brute force | a maximum flow on the grid, as in the reductions below; correct but slow |

## Bounds

**Cut condition.** If width $h$ is routable, then for every $i$ with $i + h \le n$,
$$ a_{i + h} - b_i \ge h \quad\text{and}\quad b_{i + h} - a_i \ge h. $$

*Proof of the first inequality.* Suppose $a_{i+h} - b_i \le h - 1$. Let $D$ be the set of grid points with $x - y = b_i - 1$. Inside the channel, $D$ has exactly $h$ points, $(b_i - 1 + y, y)$ for $1 \le y \le h$. The bottom terminals $b_i, \ldots, b_{i+h}$ have $x - y = b_j \ge b_i$, so they lie on the side $x - y > b_i - 1$. The top terminals $a_i, \ldots, a_{i+h}$ have $x - y = a_j - h - 1 \le a_{i+h} - h - 1 \le b_i - 2$, so they lie on the side $x - y < b_i - 1$. Each step of a grid path changes $x - y$ by 1, so each of the $h + 1$ wires $i, \ldots, i + h$ passes through a point of $D$. Its only points in rows 0 and $h + 1$ are its own ends, which are not on $D$, so that point is inside the channel. The wires are disjoint, so $D$ would need $h + 1$ points inside the channel. The second inequality follows in the same way with the diagonal $x + y = a_i + h$, which has $h$ points inside the channel: if $b_{i+h} - a_i \le h - 1$, the bottom terminals $b_i, \ldots, b_{i+h}$ have $x + y \le a_i + h - 1$ and the top terminals $a_i, \ldots, a_{i+h}$ have $x + y \ge a_i + h + 1$. $\square$

**Width formula.** The terminals are strictly increasing integers, so if the cut condition holds for $h$ it holds for $h + 1$. The least width is therefore the least $h \ge 1$ that meets the cut condition. Necessity is proved above. That the cut condition is also sufficient is the content of the cited works, and this page does not prove it. The form given here agrees with an exhaustive search by maximum flow on every instance with $n \le 5$ and terminals in columns 0 to 7. That is a test on small cases, not a proof.

**Upper bound.** For $h = n$ the cut condition has no pairs to check, so by the formula width $n$ is always enough.

**Relation to cuts in general.** The routing is a set of [vertex-disjoint paths](/vertex-disjoint-paths/) in a grid, which is a [planar graph](/planar-graph/). The diagonals $D$ are vertex cuts in the sense of the [max-flow min-cut theorem](/max-flow-min-cut-theorem/), and the width formula says that in this setting the diagonal cuts are the only ones that matter.

## Reductions

- **To disjoint paths in a planar grid.** River routing is a case of the vertex-disjoint paths problem with all sources on one face and all sinks on another, in order. Here, unlike the general problem, the cut condition is enough.
- **To maximum flow.** For a fixed $h$, joining a super source to all bottom terminals and a super sink to all top terminals, with unit capacities on the grid points, gives a flow of value $n$ exactly when the routing exists. Disjoint paths that cross the strip from the bottom row to the top row keep their order from left to right, so the $i$-th path from the left joins $b_i$ to $a_i$. This is a correct but slow test.
- **From two-layer channels.** The order condition shows the gap to the two-layer [channel routing problem](/channel-routing-problem/): a second layer allows any order, at the price of NP-hardness ([NP-completeness of channel routing](/channel-routing-np-completeness/)).

## Applications

- **Joining blocks on one metal layer.** When two blocks of a chip face each other with their pins in the same order, for example a data path and its memory, a river route on one layer joins them without vias.
- **Placement of blocks.** The offset question tells how far apart, and how much shifted, two blocks must be placed so that one layer is enough between them.
- **Power and clock lines, and packages.** Wiring that must stay on one layer, such as some power lines, and the fan-out from a chip to a package, use the same model, with the [escape routing](/escape-routing/) of pin arrays as a related problem.

## References
