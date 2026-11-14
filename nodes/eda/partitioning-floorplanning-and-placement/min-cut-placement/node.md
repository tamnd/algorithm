---
tag: S0NJTB
kind: algorithm
slug: min-cut-placement
name: Min-cut placement
aliases:
- Breuer min-cut placement
area: eda/partitioning-floorplanning-and-placement
level: core
summary: Breuer's placement that bisects the netlist and the chip region again and again with a min-cut partitioner, until each region holds a few cells.
solves: [placement-problem]
model: word-ram
complexity:
  vars: {n: the number of cells, m: the number of nets, P: the number of pins, S: the number of sites, p: the largest number of FM passes in one region}
  time: {worst: "O(p (n + m + P) log S)", average: "O(p (n + m + P) log S)", best: "O((n + m + P) log S)"}
  space: {extra: "O(n + m + P)"}
properties: {deterministic: false, recursive: true, exact: false}
history:
  year: 1977
  people: [Melvin A. Breuer]
  note: Breuer described placement by repeated min-cut bisection of the netlist and the region in 1977, at the Design Automation Conference and in a journal paper.
prereqs: [placement-problem, hypergraph-partitioning, fiduccia-mattheyses, half-perimeter-wirelength]
see_also: [terminal-propagation, placement-problem, hypergraph-partitioning, multilevel-hypergraph-partitioning, fiduccia-mattheyses, rents-rule, quadratic-placement, slicing-floorplan]
sources:
  - paper: "M. A. Breuer, Min-cut placement, Journal of Design Automation and Fault-Tolerant Computing 1(4), 343 to 362, 1977"
    locator: the placement by repeated min-cut partitioning, the cut line sequences (quadrature, bisection and slice/bisection), and the relation between the cut values and the wire length
  - paper: "M. A. Breuer, A class of min-cut placement algorithms, Proceedings of the 14th Design Automation Conference, 284 to 290, 1977"
    locator: the conference version of the min-cut placement procedures
  - paper: doi:10.1109/TCAD.1985.1270101
    title: Alfred E. Dunlop and Brian W. Kernighan, A procedure for placement of standard-cell VLSI circuits, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 4(1), 92 to 98, 1985
    locator: terminal propagation, and min-cut placement of standard cells with Kernighan-Lin style partitioning
  - paper: doi:10.1109/DAC.1982.1585498
    title: C. M. Fiduccia and R. M. Mattheyses, A linear-time heuristic for improving network partitions, 19th Design Automation Conference, 175 to 181, 1982
    locator: the partitioner used at each cut, with the balance condition
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 4, Global and Detailed Placement (min-cut placement; general locator)
---

Min-cut placement solves the [placement problem](/placement-problem/) by divide and conquer on the chip. It cuts the placement region into two halves by a line, splits the cells into two groups of the right sizes with a [hypergraph partitioner](/hypergraph-partitioning/) so that few nets cross, and does the same in each half, until each region holds one site or a few cells. Breuer introduced it in 1977. The idea is that every net that crosses a cut line adds to the wire length, so keeping the cuts small keeps the [HPWL](/half-perimeter-wirelength/) small. It is a heuristic: each cut is only locally good, and the method has no approximation guarantee.

## In plain words

You must seat many guests at a long table so that friends sit close. Split the guests into two groups with few friendships across, and give each group one half of the table. Then split each group again for its half, and so on, until each guest has a chair.

Each split looks only at the guests of one group. A guest who has a friend in the other half of the room would like to sit near that side, but a plain split cannot see this. Terminal propagation fixes that: it adds a dummy guest who stands for the friend outside and is fixed on the right side.

## The problem

The input is a netlist of $n$ unit cells and $m$ nets with $P$ pins, fixed pads with integer positions, and a rectangle of $W \times H$ unit sites at the points $(x, y)$ with $0 \le x < W$ and $0 \le y < H$, with $n \le S = W H$. The output is a legal placement: an injective map of the cells to the sites. The goal, which the method approaches but does not reach in general, is the least total HPWL of the nets. The implementation puts every pin at the position of its cell or pad, with no pin offsets. Rows of cells of different widths change only the capacity of a region; the method stays the same.

## The algorithm

The regions are processed in breadth-first order with a [queue](/queue/), so that all regions of one level are cut before the next level starts. Each cell has an *estimated position*, the center of its current region, which terminal propagation uses for cells outside the region being cut.

```pseudo id=main
MIN-CUT-PLACE(cells, nets, pads, W, H)
L1  Q ← a queue with (the whole region, all cells)
L2  while Q is not empty
L3      (B, C) ← the front of Q, removed
L4      if B is one site then place the cell of C there (if any) and continue
L5      cut B across its longer side through the middle into B0 and B1, with c0 and c1 sites
L6      build the netlist of C: each net restricted to C; with terminal propagation, add a fixed terminal on side s if the other pins of the net lie on side s of the line, and drop the net if they lie on both sides
L7      t ← round(|C| c0 / (c0 + c1)); start from a random split with t cells on side 0
L8      (C0, C1) ← FM with the fixed terminals and |C0| in [max(t − 1, |C| − c1), min(t + 1, c0)]
L9      for s ∈ {0, 1}: set the estimate of each cell of C_s to the center of B_s, and add (B_s, C_s) to Q
L10 return the sites of the cells
```

Line L6 looks at each net with a pin in $C$. The pins in $C$ stay. A pin outside $C$ is a pad at its position or a cell at its estimate. If its coordinate across the cut lies exactly on the cut line, it is ignored, since it pulls to neither side. If all other outside pins are on side $s$, the net gets the fixed terminal of side $s$; if they are on both sides, the net is cut whatever the split is, so it is left out. Without terminal propagation, line L6 keeps only the pins in $C$.

Line L8 uses [Fiduccia-Mattheyses](/fiduccia-mattheyses/) passes with the two terminals fixed. A tentative move may leave the window by one cell, but only a prefix of the pass that ends inside the window is kept. So FM can still swap cells when the window has one value, as for a region of 4 cells and 4 sites. The window is never empty, and it keeps $|C_0| \le c_0$ and $|C_1| \le c_1$.

## Example

Place 8 cells on a $4 \times 2$ grid of sites. A pad $L$ at $(-1, 0)$ and a pad $R$ at $(4, 1)$. The 13 nets, all 2-pin, are

$$ L0, \; 01, \; 02, \; 12, \; 13, \; 23, \; 34, \; 45, \; 46, \; 56, \; 57, \; 67, \; 7R. $$

So cells 0 to 3 form one cluster with pad $L$, cells 4 to 7 another with pad $R$, and the net $34$ joins them. The trace is the run of the implementation with terminal propagation and `random.Random(0)`.

| step | region | cut line | cells | terminals | result | cut |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | $x \in [0, 3]$ | $x = 1.5$ | 0 to 7 | $L$ on side 0, $R$ on side 1 | $\{0,1,2,3\} \mid \{4,5,6,7\}$ | 1 |
| 2 | $x \in [0, 1]$ | $x = 0.5$ | 0 to 3 | $L$ for 0 on side 0, cell 4 at $(2.5, 0.5)$ for 3 on side 1 | $\{0,2\} \mid \{1,3\}$ | 3 |
| 3 | $x \in [2, 3]$ | $x = 2.5$ | 4 to 7 | cell 3 at $(1, 0.5)$ for 4 on side 0, $R$ for 7 on side 1 | $\{4,5\} \mid \{6,7\}$ | 3 |
| 4 | $x = 0$ | $y = 0.5$ | 0, 2 | $L$ for 0 on side 0 | 0 at $y = 0$, 2 at $y = 1$ | 1 |
| 5 | $x = 1$ | $y = 0.5$ | 1, 3 | cell 0 for 1 on side 0, cell 2 for 1 and 3 on side 1 | 1 at $y = 0$, 3 at $y = 1$ | 2 |
| 6 | $x = 2$ | $y = 0.5$ | 4, 5 | cell 3 at $(1, 1)$ for 4 on side 1 | 5 at $y = 0$, 4 at $y = 1$ | 1 |
| 7 | $x = 3$ | $y = 0.5$ | 6, 7 | cell 5 for 6 and 7 on side 0, cell 4 for 6 and $R$ for 7 on side 1 | 7 at $y = 0$, 6 at $y = 1$ | 3 |

Step 1 has $c_0 = c_1 = 4$, so the window is exactly 4; FM goes from the random start, with cut 7, to cut 1. In step 2, the split $\{0, 1\} \mid \{2, 3\}$ also has cut 3, and the random start decides. In step 5 the net $34$ is dropped, because cell 4 has the estimate $(2, 0.5)$, exactly on the line $y = 0.5$. In step 7 both splits cut 3 nets.

The placement is

| | $x = 0$ | $x = 1$ | $x = 2$ | $x = 3$ |
| --- | --- | --- | --- | --- |
| $y = 1$ | 2 | 3 | 4 | 6 |
| $y = 0$ | 0 | 1 | 5 | 7 |

with HPWL 16. The lines $x = -0.5, 0.5, 1.5, 2.5, 3.5$ are crossed by $1, 3, 1, 3, 1$ nets, and the line $y = 0.5$ by 7 nets, so $9 + 7 = 16$, as the identity below says. A brute force over all $8!$ placements gives the optimum 16 for this instance. Without terminal propagation, seeds 0 to 3 give 24, 20, 18 and 24; with it, all four give 16.

## Correctness

The [proof](proofs/correctness.md) shows the following.

- **The window.** For $|C| \le c_0 + c_1$, the window of line L8 contains $t$, so the random start lies in it, and every kept split satisfies $|C_0| \le c_0$ and $|C_1| \le c_1$.
- **Legality.** By induction on the queue, each region holds at most as many cells as it has sites. Regions of the same level are disjoint, and each cell is in exactly one of them. A region of one site holds at most one cell. So the output is an injective map to sites inside the rectangle.
- **Termination.** Each cut is through the middle of a side of length at least 2, so both parts are smaller. The queue becomes empty after at most $2S - 1$ regions.
- **HPWL as a sum of cuts.** With integer positions, the HPWL of a placement equals the sum, over the lines $x = j + \frac12$ and $y = j + \frac12$, of the number of nets with pins on both sides of the line. Each cut of line L8 tries to make one term of this sum small.
- **Terminal propagation counts exactly.** If all outside pins of every net were at their final positions, the cut of line L8 with the terminals would be the number of nets of the region that cross the line, less the number of dropped nets, which does not depend on the split. So both have the same best splits. The [terminal propagation](/terminal-propagation/) page discusses this. The estimates are only centers of regions, so in the algorithm this is a model, not a guarantee.

## Complexity

- **Levels.** A cut halves the longer side, so after at most $\lceil \log_2 W \rceil + \lceil \log_2 H \rceil$ levels every region is one site. This is $O(\log S)$.
- **One level.** The regions of a level hold disjoint cells. Building their netlists in line L6 visits each pin of each net with a pin in the region, and each net gets at most one terminal, so a level has $O(n + m + P)$ pins in total with marking of the nets. With gain buckets, an FM pass costs time linear in the size of its netlist, so a level costs $O(p (n + m + P))$ for at most $p$ passes per region.
- **Total.** $O(p (n + m + P) \log S)$ time and $O(n + m + P)$ space, since the regions of a level can be processed one by one.
- **The implementation** finds the move of largest gain by a scan, and line L6 recomputes each restricted net from the full pin list, so a region with $k$ cells costs $O(k^2 + \sum_e |e|^2)$ per FM pass. This is fine for the toy inputs of the tests.

## Properties

Min-cut placement is a heuristic for an NP-hard problem. What is proved and what is measured are kept apart.

**What is proved.** Legality, termination and the cost above; the identity between HPWL and the sum of crossing counts; and the exact count of terminal propagation, up to a constant, when the outside pins are where they are assumed to be. No approximation ratio for HPWL is known. Each cut is a local optimum of FM, not a minimum cut, and a minimum cut at one level can force a bad cut at the next.

**What is measured.** The numbers below are from the implementation of this page, on toy inputs, and are not benchmark results. Published placers based on min-cut partitioning were compared on the ISPD 2005 and 2006 placement contest benchmarks; see those contests for the numbers.

- *Tiny grids.* On 100 random instances with 6 cells on a $3 \times 2$ grid, 8 nets and 0 to 3 pads outside the grid (generator `random.Random(2026)`, run $t$ seeded with `random.Random(t)`), compared with a brute force over all placements: with terminal propagation the result was optimal in 53 instances, with mean ratio 1.036 to the optimum; without it, optimal in 7, with mean ratio 1.171.
- *A hidden grid.* 20 netlists (generator `random.Random(2027)`), each the $8 \times 8$ grid graph on 64 cells in a random order, with 112 two-pin nets and 16 pad nets to pads just outside the edge. Each net has length at least 1, and the hidden layout reaches 128, so the optimum is exactly 128. With terminal propagation the mean HPWL was 146.3, and two of the first three runs reached 128. Without it the mean was 392.4. Terminal propagation won in all 20.

## Variants and improvements

- **Cut sequences.** Breuer compared *quadrature* (alternate vertical and horizontal cuts through the middle, as here), *bisection* (cut the region into rows first, then cut each row), and *slice/bisection*. The order of the cut lines changes the result.
- **Multilevel partitioners.** Modern min-cut placers such as Capo use [multilevel hypergraph partitioning](/multilevel-hypergraph-partitioning/) for each cut, with fixed terminals, and a tolerance on the sizes.
- **Unequal cuts and whitespace.** A cut line need not be in the middle; it can follow the sizes of the two cell groups, so that the free space spreads evenly.
- **End cases.** Stop at regions of a few cells and place them by exhaustive search or by a small branch and bound, then [legalize](/placement-legalization/) and run [detailed placement](/detailed-placement/).
- **k-way cuts.** Cut a region into four parts at once (quadrisection), which sees both directions at the same time.
- **Hybrids.** Use min-cut placement to spread cells in an analytical or [quadratic placer](/quadratic-placement/), or use quadratic placement to estimate the positions for terminal propagation.

## When to use it

Use min-cut placement when you have a good hypergraph partitioner and want a placement that is legal by construction, that scales to large netlists, and that tends to keep the routing demand across each cut line small. In the ISPD 2005 and 2006 placement contests, analytical placers had the best results, so min-cut is now used mostly inside other flows, for floorplans and for the end cases. The recursive cuts also build a [slicing floorplan](/slicing-floorplan/) of the chip.

## Pitfalls

- **No terminal propagation.** Without it, each cut ignores the cells outside the region, and the two halves of a cluster can end up far apart. The toy measurements above show the size of the effect.
- **Balance too tight or too loose.** An exact window gives FM no room to move; too much slack lets one side take more cells than its sites. Bound the window by the capacities, as line L8 does.
- **Pins on the cut line.** A pin exactly on the line pulls to neither side. Counting it on one side biases the cut.
- **Nets with outside pins on both sides.** Such a net is cut in every split. Giving it two terminals adds a constant to every cut, which is harmless, but giving it one terminal is wrong.
- **Depth first order.** If the regions are cut depth first, the estimates of the cells in regions not yet cut are coarse, and terminal propagation sees less. Breadth first order makes all estimates of one level equally fine.

## Implementations

## History

Breuer (1977) proposed placing a circuit by repeated min-cut partitioning, with several orders of cut lines, and related the cut values to the wire length. Lauther (1979) used min-cut placement for building blocks. Dunlop and Kernighan (1985) added terminal propagation and applied the method to standard cells, with a Kernighan-Lin style partitioner. In the late 1990s, multilevel partitioners such as hMETIS made min-cut placement fast on large designs, and Capo (Caldwell, Kahng and Markov, 2000) was a widely used min-cut placer.

## References
