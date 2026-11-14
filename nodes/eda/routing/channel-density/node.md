---
tag: JH1V52
kind: definition
slug: channel-density
name: Channel density
area: eda/routing
level: intro
summary: The largest number of nets that cross one column of a channel. Every routing with trunks on one layer needs at least this many tracks.
prereqs: [maximum-overlap]
see_also: [channel-routing-problem, vertical-constraint-graph, left-edge-algorithm, interval-coloring-depth-theorem, sweep-maximum-overlap, interval-partitioning, switchbox-routing, greedy-channel-router]
sources:
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 6, Detailed Routing, the section on channel routing (horizontal constraints and the channel density as a lower bound; general locator)
  - book: isbn:9780792383932
    title: Naveed A. Sherwani, Algorithms for VLSI Physical Design Automation, third edition, Kluwer, 1999
    locator: the chapter on detailed routing, the part on channel routing (the density of a channel and the lower bound on tracks; general locator)
  - paper: "A. Hashimoto and J. Stevens, Wire routing by optimizing channel assignment within large apertures, Proceedings of the 8th Design Automation Workshop, 155 to 169, 1971"
    locator: the left-edge assignment of intervals to tracks, which meets the largest number of intervals over one column when there are no vertical constraints (general locator)
---

The channel density is the first number that a channel router computes. A [channel](/channel-routing-problem/) is a rectangle with pins on its top and bottom edges. Each net, a set of pins that must be joined, spans the columns from its leftmost pin to its rightmost pin. The *local density* at a column is the number of nets whose span holds that column. The *channel density* $d$ is the largest local density over all columns. In the usual two-layer model, where horizontal wires use one layer, every net that crosses a column needs its own track there, so no routing uses fewer than $d$ tracks. The [left-edge algorithm](/left-edge-algorithm/) meets this bound when no column has pins of two different nets, and the bound is the yardstick against which channel routers report their results.

## Definition

**Channel.** A channel has columns $1, \ldots, n$. Each column $c$ has a top pin $\mathrm{top}(c)$ and a bottom pin $\mathrm{bot}(c)$, each the label of a net or 0 for no pin. A net is a label that appears on at least two pins in at least two different columns. A net with all its pins in one column is routed by a straight vertical wire and is left out of the definitions below.

**Interval of a net.** For a net $N$, let $l_N$ be the smallest and $r_N$ the largest column that holds a pin of $N$. The interval of $N$ is the closed set of columns $I_N = [l_N, r_N]$.

**Local density.** The local density at column $c$ is
$$ d(c) = \lvert \{ N : l_N \le c \le r_N \} \rvert, $$
the number of nets whose interval holds $c$.

**Channel density.** The channel density is $d = \max_{1 \le c \le n} d(c)$. In the terms of intervals, $d$ is the depth of the family $\{I_N\}$, the [maximum overlap](/maximum-overlap/) of the intervals.

**Lower bound.** In the *reserved two-layer model*, trunks (horizontal wire) run on layer H along tracks $1, \ldots, T$, and branches (vertical wire) run on layer V along the columns. Two nets may not share a grid point on the same layer. Then every legal routing has $T \ge d$, also when nets may change track (doglegs).

*Proof.* Fix a column $c$ and a net $N$ with $l_N \le c \le r_N$. If $l_N < c$, then $N$ has a pin left of $c$ and a pin at or right of $c$, so its wire contains a horizontal edge from column $c - 1$ to column $c$. If $l_N = c$, then $r_N > c$ and the wire contains a horizontal edge from column $c$ to column $c + 1$. In both cases $N$ uses a grid point $(c, t)$ on layer H for some track $t$. The $d(c)$ nets that cross $c$ use $d(c)$ different such points, since no point holds two nets, and column $c$ has only $T$ points on layer H. So $T \ge d(c)$ for every $c$, and $T \ge d$. $\square$

**Computing it.** The local densities of all columns come from one sweep. Add 1 at column $l_N$ and subtract 1 after column $r_N$ for each net, and take prefix sums. This takes $O(n + P)$ time for $P$ pins, as in the [sweep for maximum overlap](/sweep-maximum-overlap/).

## Examples and non-examples

**A channel with four nets.** Take $n = 8$ columns with

| column | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| top | 1 | 0 | 2 | 1 | 3 | 0 | 4 | 0 |
| bottom | 0 | 2 | 0 | 3 | 0 | 4 | 0 | 3 |

The intervals are $I_1 = [1, 4]$, $I_2 = [2, 3]$, $I_3 = [4, 8]$ and $I_4 = [6, 7]$. The local densities are

| column | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nets that cross | 1 | 1, 2 | 1, 2 | 1, 3 | 3 | 3, 4 | 3, 4 | 3 |
| $d(c)$ | 1 | 2 | 2 | 2 | 1 | 2 | 2 | 1 |

so $d = 2$. Two tracks are enough: nets 1 and 4 on the upper track, nets 2 and 3 on the lower one. Column 4 has net 1 on top and net 3 at the bottom, and net 1 is on the upper track, so the two branches in column 4 do not meet.

**Closed intervals count shared end columns.** Net 1 ends in column 4 and net 3 starts there, and $d(4) = 2$. The two nets cannot share a track, because both need the point of that track in column 4. With half-open intervals the count at column 4 would be 1, which is not a valid bound in this model.

**The bound is not always met.** Take $n = 2$, with top pins $1, 2$ and bottom pins $2, 1$. Then $d = 2$. Without doglegs, net 1 must be above net 2 because of column 1, and below net 2 because of column 2, so no number of tracks works. Doglegs at pin columns do not help either, since each net has only two pins. With jogs in any column, two tracks are still too few: in column 1 the two branches fill the whole column, so net 1 must reach column 2 on track 1 and net 2 on track 2, and in column 2 the branch of net 2 must then pass track 1 to reach track 2, which leaves no room for the branch of net 1 from the bottom. The [greedy channel router](/greedy-channel-router/) routes this channel with three tracks and one column past the right end. The [vertical constraint graph](/vertical-constraint-graph/) records the constraints that cause this gap.

**Not the density: the number of nets.** A channel with $N$ nets always has $d \le N$, and $d$ can be much smaller. Nets $1, \ldots, N$ with $I_k = [2k - 1, 2k]$ have $d = 1$, and all of them fit on one track.

**Not the density: the pins in a column.** A column holds at most two pins, but many nets can cross it. In the example above, columns 6 and 7 each hold one pin and have $d(c) = 2$.

## Related definitions

- [Channel routing problem](/channel-routing-problem/): the problem in which the density is the first lower bound.
- [Vertical constraint graph](/vertical-constraint-graph/): its longest path gives a second lower bound in the model without doglegs. The number of tracks must be at least the larger of the two bounds.
- [Interval coloring depth theorem](/interval-coloring-depth-theorem/): intervals can be colored with as many colors as their depth, so the density is reached when there are no vertical constraints. The [left-edge algorithm](/left-edge-algorithm/) builds such a coloring track by track.
- *Zones.* The sets of nets that cross one column, kept only when they are maximal, are the zones of the [Yoshimura-Kuh algorithm](/yoshimura-kuh-algorithm/). The largest zone has $d$ nets.
- *Switchbox cut bound.* In a [switchbox](/switchbox-routing/), the same argument bounds the nets across every vertical and every horizontal cut by the number of tracks across it.
- *Unreserved layers.* If both layers may hold trunks, two nets can cross a column on the same track on different layers, and the bound becomes $\lceil d/2 \rceil$.

## References
