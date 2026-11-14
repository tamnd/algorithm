---
tag: 8CBACT
kind: technique
slug: terminal-propagation
name: Terminal propagation
aliases:
- Dunlop-Kernighan terminal propagation
area: eda/partitioning-floorplanning-and-placement
level: core
summary: In min-cut placement, adds a fixed dummy terminal for each net with cells outside the region, so the partitioner sees the pull of those cells.
prereqs: [min-cut-placement, hypergraph-partitioning, fiduccia-mattheyses]
see_also: [min-cut-placement, placement-problem, half-perimeter-wirelength, hypergraph-partitioning, fiduccia-mattheyses, kernighan-lin, multilevel-hypergraph-partitioning, quadratic-placement]
sources:
  - paper: doi:10.1109/TCAD.1985.1270101
    title: Alfred E. Dunlop and Brian W. Kernighan, A procedure for placement of standard-cell VLSI circuits, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 4(1), 92 to 98, 1985
    locator: terminal propagation in min-cut placement of standard cells
  - paper: "M. A. Breuer, Min-cut placement, Journal of Design Automation and Fault-Tolerant Computing 1(4), 343 to 362, 1977"
    locator: the min-cut placement in which the cuts of a region ignore the cells outside it
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 4, Global and Detailed Placement (min-cut placement with terminal propagation; general locator)
---

Terminal propagation is a technique for [min-cut placement](/min-cut-placement/). When a region is cut, the partitioner sees only the cells of the region, but many nets of these cells also connect cells or pads outside the region. Terminal propagation replaces those outside pins by a fixed dummy vertex, a *terminal*, on the side of the cut line where they lie. The partitioner, for example [Fiduccia-Mattheyses](/fiduccia-mattheyses/) with fixed vertices, then pays for a split that puts a cell on the far side from its outside neighbors. Dunlop and Kernighan introduced it in 1985 for standard cells. Without it, a cut cannot even tell left from right, because a split and its mirror have the same cut.

## In plain words

You split a group of guests between the two halves of a room. Some of them have friends who already sit in another part of the house. A plain split looks only at the friendships inside the group, so it may send a guest to the half that is far from all of his other friends.

Terminal propagation puts a cardboard figure for those outside friends at the edge of the matching half, and the figure cannot move. Now a split that sends the guest away from his friends cuts a friendship with the figure, and it costs one more.

## When it applies

- **Top-down placement.** The placement is built by cutting regions one at a time, and each cut uses a [hypergraph partitioner](/hypergraph-partitioning/) on the cells of one region. This is the main use.
- **Some outside positions are known.** Pads are fixed, and cells in other regions have at least an estimate, such as the center of their region. Breadth-first order of the regions makes all estimates of one level equally fine.
- **The partitioner accepts fixed vertices.** The terminals must stay on their side and must not count for the balance.
- **The same idea** applies to top-down floorplanning, to quadrisection (with terminals in four quadrants), and to any recursive split where the parts have fixed positions in space.

## The template

For a region $B$ with the cells $C$, cut by a line into the sides 0 and 1, and with a known or estimated position for every pin outside $C$:

```pseudo id=main
TERMINAL-PROPAGATE(C, nets, line, pos)
L1  N' ← an empty netlist; T0 ← a fixed vertex on side 0; T1 ← a fixed vertex on side 1
L2  for each net e with a pin in C
L3      I ← the pins of e in C
L4      S ← the sides of the line on which the pins of e outside C lie, ignoring pins on the line
L5      if S = {0, 1} then skip e                     ▷ cut by every split
L6      else if S = {s} then add I ∪ {T_s} to N'
L7      else if |I| ≥ 2 then add I to N'
L8  return N'
```

The partitioner then splits $C$ on the netlist $N'$, with $T_0$ and $T_1$ fixed. Line L4 uses the position of a pad, or the estimate of a cell in another region. A pin exactly on the line pulls to neither side. Many placers also ignore pins *near* the line, within some distance.

**Why it counts the right thing.** Suppose that every pin outside $C$ is at its final position, and none is on the line. Let $X$ be the number of nets with a pin in $C$ that will cross the line when the cells of each part are placed on their side, and let $Z$ be the cut of $N'$. Then $X = Z + D$, where $D$ is the number of nets skipped by line L5.

*Proof.* Take a net $e$ with a pin in $C$. If it has no outside pins, it crosses the line exactly when $I$ is split, which is exactly when it is cut in $N'$ (a net with one pin is never split). If all its outside pins are on side $s$, it crosses exactly when a pin of $I$ is on side $1 - s$, which is exactly when $I \cup \{T_s\}$ is cut. If it has outside pins on both sides, it crosses the line for every split, and it is skipped. $\square$

$D$ does not depend on the split, so the splits of least cut in $N'$ are exactly the splits with the fewest crossing nets. With integer sites, the [HPWL](/half-perimeter-wirelength/) of a placement is the sum, over the lines between rows and columns of sites, of the number of nets that cross the line (see the [min-cut placement](/min-cut-placement/) page), so each cut works on one term of that sum. In a real run the outside cells sit at estimates, not at their final sites, so this is a model of the cost and gives no bound on the result.

**Cost.** Lines L2 to L7 visit each pin of each net with a pin in $C$ once, with a mark per net, and add at most one pin per net. So they cost $O(P_C)$ time, where $P_C$ is the number of pins of the nets of $C$, and $N'$ has at most $P_C$ pins plus one per net.

### Example

Take the instance of the [min-cut placement](/min-cut-placement/) page: 8 cells on a $4 \times 2$ grid, a pad $L$ at $(-1, 0)$, a pad $R$ at $(4, 1)$, and the 2-pin nets $L0$, $01$, $02$, $12$, $13$, $23$, $34$, $45$, $46$, $56$, $57$, $67$, $7R$. The first cut, at $x = 1.5$, puts cells 0 to 3 left and 4 to 7 right. The second cut splits the left region $x \in [0, 1]$ at the line $x = 0.5$. Cell 4 is estimated at the center $(2.5, 0.5)$ of the right region.

- Net $L0$: the pad $L$ has $x = -1 < 0.5$, so the net becomes $\{0, T_0\}$.
- Net $34$: cell 4 has $x = 2.5 > 0.5$, so the net becomes $\{3, T_1\}$.
- The nets $01, 02, 12, 13, 23$ have no outside pins and stay as they are.

The six splits with two cells on side 0 have these cuts.

| cells on side 0 | cut without terminals | cut with terminals |
| --- | --- | --- |
| 0, 1 | 3 | 3 |
| 0, 2 | 3 | 3 |
| 0, 3 | 4 | 5 |
| 1, 2 | 4 | 5 |
| 1, 3 | 3 | 5 |
| 2, 3 | 3 | 5 |

Without terminals, $\{2, 3\}$ on the left is as good as $\{0, 1\}$, though it sends cell 0 away from $L$ and cell 3 away from cell 4. With terminals, only the two splits that keep cell 0 on the left and cell 3 on the right are best. Later, when the column $x = 0$ is cut at $y = 0.5$, cell 1 is estimated at $(1, 0.5)$, exactly on the line, so it is ignored for the nets $01$ and $12$.

On this instance, the implementation of the min-cut placement page gives HPWL 16, the optimum by brute force, for the seeds 0 to 3 with terminal propagation, and 24, 20, 18 and 24 without it. Its other measurements on toy inputs, with sizes and seeds, are on that page. They are not benchmark results.

## Classic examples

- **Standard cell placement** (Dunlop and Kernighan 1985). Min-cut placement with a Kernighan-Lin style partitioner, where the outside connections of each region are propagated to its boundary as fixed terminals.
- **Min-cut placers with multilevel partitioners.** Placers such as Capo bisect each region with a [multilevel hypergraph partitioner](/multilevel-hypergraph-partitioning/) that accepts fixed vertices, and the terminals are those fixed vertices.
- **Top-down floorplanning.** Blocks are assigned to the parts of a recursively cut chip, and the nets to blocks already assigned elsewhere give terminals in the same way.
- **Quadrisection.** A region is cut into four parts at once, and each outside pin gives a terminal in one of the four quadrants.

## Variations

- **Where the outside pins are.** Use the center of the region of each outside cell, its projection on the boundary of the current region, or the position from a [quadratic placement](/quadratic-placement/).
- **A dead zone.** Ignore outside pins within a band around the cut line, not only those exactly on it, since their side is uncertain.
- **Both sides.** A net with outside pins on both sides can be skipped, or given both terminals. Both terminals add 1 to every cut, which does not change the best split.
- **Weights.** Give a terminal a weight that grows with the number of outside pins it stands for, or with the distance to them.
- **Repartitioning.** After a level is done, the estimates are better. Cut the regions of the level again with the new terminals, and keep the result if it is better.
- **Cut order.** Breadth-first order gives estimates of the same quality to all regions of a level. Depth-first order gives poor estimates for the regions not yet cut.

## Pitfalls

- **One terminal for a net with pins on both sides.** The net is cut in every split, so it must not pull toward one side. Skip it or give it both terminals.
- **Counting a pin on the line.** It has no side. Putting it on one side by a rule such as "less than or equal" biases every cut in one direction.
- **Movable terminals or terminals in the balance.** The terminals must stay fixed, and they must not count for the sizes of the sides, or the balance window is wrong.
- **Too much trust in the estimates.** The estimate of a cell is only the center of its region. The exact count above holds only for final positions, so terminal propagation is a model and not a guarantee.
- **Forgetting the pads.** Pads are the only exact outside positions at the first levels. If they are left out, the first cuts have no orientation at all.

## Exercises

1. Prove that without terminals, a split and its mirror (the two sides exchanged) have the same cut. What does this mean for the first cut of a chip with pads?
2. In the example, verify the six cuts in the table with and without terminals.
3. Show that giving a net with outside pins on both sides both terminals adds exactly 1 to the cut of every split.
4. Take a region whose cells all belong to one net with one outside pin. With center estimates, when does terminal propagation pull the cells toward that pin, and when does it ignore it?

## References
