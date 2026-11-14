---
tag: PP8KMW
kind: problem
slug: detailed-placement
name: Detailed placement
aliases:
- placement refinement
area: cad/partitioning-floorplanning-and-placement
level: core
summary: Improve a legal placement by local moves such as swaps, shifts and reordering of cells in windows, keeping it legal.
prereqs: [placement-problem, placement-legalization, local-search]
see_also: [independent-set-matching, abacus-legalization, tetris-legalization, half-perimeter-wirelength, assignment-problem, hungarian-algorithm, simulated-annealing-placement, hill-climbing]
sources:
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 4, Global and Detailed Placement (detailed placement after legalization; general locator)
  - paper: "Min Pan, Natarajan Viswanathan and Chris Chu, An efficient and effective detailed placement algorithm, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design (ICCAD), 48 to 55, 2005"
    locator: the detailed placer FastDP on a legal placement, with global swap, vertical swap, local reordering and single-segment clustering
  - paper: doi:10.1109/TCAD.2008.923063
    title: Tung-Chieh Chen, Zhe-Wei Jiang, Tien-Chang Hsu, Hsin-Chen Chen and Yao-Wen Chang, NTUplace3, an analytical placer for large-scale mixed-size designs with preplaced blocks and density constraints, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 27(7), 1228 to 1240, 2008
    locator: the detailed placement stage, with cell matching, cell swapping and reordering
  - paper: doi:10.1016/0304-3975(76)90059-1
    title: M. R. Garey, D. S. Johnson and L. Stockmeyer, Some simplified NP-complete graph problems, Theoretical Computer Science 1(3), 237 to 267, 1976
    locator: the NP-completeness of optimal linear arrangement, which gives the hardness on this page
---

Detailed placement is the last step of standard cell placement in chip design. Its input is a legal placement, usually the output of [legalization](/placement-legalization/), and its output is a legal placement with a smaller total wirelength, measured by [HPWL](/half-perimeter-wirelength/). It changes the placement by local moves: it swaps two cells, moves a cell to a free gap, reorders a few neighboring cells of a row, shifts the cells of a row segment, or permutes a set of cells over their slots. Each move keeps the placement legal, and a move is kept only if it does not increase the cost. The problem of the best legal placement is the [placement problem](/placement-problem/) itself, which is [NP-hard](/np-hard/), so detailed placers find a local optimum for their moves, not a global one. This page states the problem; the methods are on the pages of the detailed placers.

## In plain words

After legalization every part of the circuit sits on its own place in a row, but the wires are longer than they need to be, because the legalizer only tried to move the parts little. Detailed placement now looks at small groups of nearby parts and tries to rearrange them so that the wires get shorter.

It swaps two parts, slides a part into an empty gap, or tries every order of three neighbors. It keeps a change only when the wires do not get longer. Each change is small and safe, so the work never breaks the layout. But a set of small changes can get stuck: no single change helps, even though a bigger change would.

## Definition

**Input.**

- A netlist $H = (C \cup Q, N)$ with $n$ movable cells, $m$ nets, $P$ pins and net weights $w_e > 0$; each cell $c$ has the width $W_c$, a multiple of the site width $s$, and the row height $h$, and the pads $Q$ are fixed.
- Rows $y_1 < \cdots < y_K$ with sites of width $s$, and fixed blockages.
- A legal placement $(x_c, y_c)$: each cell is on a site of a row, inside the row and off the blockages, and no two cells overlap.

**Output.** A legal placement $(x^*_c, y^*_c)$ on the same rows and sites.

**Objective.** Minimize $\mathrm{WL} = \sum_{e \in N} w_e \, \mathrm{HPWL}(e)$, with pins at the cell centers unless pin offsets are given. The output must not have a larger $\mathrm{WL}$ than the input.

**Local version.** A detailed placer fixes a set $M$ of moves; each move maps a legal placement to a legal placement and changes only a few cells. The local problem is to find a legal placement $p$ that is reachable from the input by moves of $M$ and is a local minimum: no move of $M$ applied to $p$ gives a smaller $\mathrm{WL}$. Different sets $M$ give different local minima.

## Variants

The move sets in use, each defined on a legal placement:

- **Swap.** Exchange the positions of two cells of the same width, or of two cells in rows with room for each other. A global swap picks the second cell anywhere, often near the best region of the first cell, the box of the medians of its nets.
- **Move to a gap.** Move one cell to a free interval of sites, in its row or in a row above or below (a vertical move).
- **Local reordering.** Take a window of $w$ consecutive cells of one row, usually $w = 3$ or 4, and try all $w!$ orders, each packed into the same span from the left.
- **Row segment shift.** Keep the order of the cells in a segment of a row between two fixed obstacles, and choose their $x$ positions to minimize $\mathrm{WL}$ with the other cells fixed. This is a convex piecewise linear problem in the positions.
- **Matching.** Take $k$ cells of one width that share no net, and assign them to their $k$ slots by a minimum cost [assignment](/assignment-problem/). This is [independent set matching](/independent-set-matching/).
- **Other objectives.** The same moves with a cost that adds timing slack, the routing congestion of a region, or the density of a bin. Some flows also bound the movement of each cell from the input.

## Examples

**A local minimum for swaps.** One full row of 5 sites $0, \ldots, 4$, five unit cells $a, b, c, d, e$, and three 2-pin nets of weight 1: $\{a, b\}$, $\{a, c\}$ and $\{b, d\}$. Cell $e$ has no net. With pins at the cell centers, the HPWL of a net is the distance between the sites of its two cells. The input order on sites 0 to 4 is $c, a, e, b, d$.

| placement on sites 0 to 4 | $\{a, b\}$ | $\{a, c\}$ | $\{b, d\}$ | $\mathrm{WL}$ |
| --- | --- | --- | --- | --- |
| $c, a, e, b, d$ (input) | 2 | 1 | 1 | 4 |
| $c, a, b, e, d$ (swap $e, b$) | 1 | 1 | 2 | 4 |
| $c, e, a, b, d$ (swap $a, e$) | 1 | 2 | 1 | 4 |
| $c, a, b, d, e$ (reorder sites 2 to 4) | 1 | 1 | 1 | 3 |

By enumeration of all 10 swaps of two cells, none gives a $\mathrm{WL}$ below 4, so the input is a local minimum for swaps. Local reordering of the window on sites 2 to 4, from $e, b, d$ to $b, d, e$, moves three cells at once and reaches $\mathrm{WL} = 3$. This is the least $\mathrm{WL}$ over all $5! = 120$ placements, because the three nets need at least 1 each. So the set of moves decides which local minima exist.

**A matching step.** The page of [independent set matching](/independent-set-matching/) has an example of three cells in one row whose best permutation over their slots moves all three cells and lowers $\mathrm{WL}$ from $\frac{17}{2}$ to $\frac32$. No single swap of two of them reaches that value.

## Known algorithms

- **FastDP** (Pan, Viswanathan and Chu 2005). Repeats global swap, vertical swap, local reordering and single-segment clustering (a row segment shift) until the gain is small.
- **[Independent set matching](/independent-set-matching/).** Solves an assignment problem for each set of cells of one width with no shared net; used in NTUplace3 (2008) and other placers. Each step gives the best permutation of its set, so it never increases $\mathrm{WL}$.
- **Annealing in the end phase.** A [simulated annealing placer](/simulated-annealing-placement/) at a low temperature is a randomized detailed placer; at zero temperature it becomes [hill climbing](/hill-climbing/) on its moves.
- **Legalizers with a fixed order.** [Abacus](/abacus-legalization/) and the row segment shift both place the cells of a row for a fixed order; Abacus minimizes the movement, the shift the wirelength.

Detailed placers are compared on the ISPD 2005 and 2006 placement contest benchmarks by the HPWL after detailed placement and by the run time. Those gains are measured. What is proved is only per move: each accepted move keeps the placement legal and does not increase $\mathrm{WL}$, so a run with a bound on the number of passes stops.

## Bounds

- **NP-hard.** Deciding whether a legal placement with $\mathrm{WL} \le B$ exists is NP-hard already for one full row, unit cells and 2-pin nets, by the linear arrangement reduction below. A legal input is trivial to give there (any order), so the input does not make the problem easier.
- **Local minima are easy to check.** For a move set of polynomial size, such as all swaps or all windows of a constant size $w$, one test of a local minimum costs polynomial time: $O(n^2)$ swaps, or $n$ windows of $w!$ orders, each with the cost of the HPWL change of the moved cells.
- **Termination.** If each accepted move strictly decreases $\mathrm{WL}$, and the weights, widths, row heights and positions are integers, then every pin at a cell center has coordinates in multiples of $\frac12$, so $\mathrm{WL}$ is a nonnegative multiple of $\frac12$ that decreases by at least $\frac12$, and the number of accepted moves is at most twice the input $\mathrm{WL}$. No polynomial bound on the number of moves is known in general.
- **One row, fixed order.** The row segment shift is a convex piecewise linear problem, solved exactly by a linear program or by a merge of clusters of cells.

## Reductions

- **From optimal linear arrangement.** Given a graph $G$ on $n$ vertices and a bound $B$, make one row of $n$ unit sites, a unit cell per vertex and a 2-pin net of weight 1 per edge, with the cells in any order as the legal input. Every legal placement is a bijection $\pi$ from the vertices to $\{0, \ldots, n - 1\}$, and $\mathrm{WL} = \sum_{\{u, v\} \in E} |\pi(u) - \pi(v)|$. So a legal placement with $\mathrm{WL} \le B$ exists if and only if $G$ has a linear arrangement of cost at most $B$, which is NP-complete (Garey, Johnson and Stockmeyer 1976).
- **Matching to assignment.** For cells of one width that share no net, the $\mathrm{WL}$ is a constant plus a sum of a cost of each cell at each slot, so the best permutation is an [assignment problem](/assignment-problem/), solved by the [Hungarian algorithm](/hungarian-algorithm/).
- **From legalization.** [Legalization](/placement-legalization/) gives the legal input. Its objective is movement, a stand-in for wirelength; detailed placement then works on the wirelength directly.

## Applications

- **Every standard cell flow.** After global placement and legalization, detailed placement recovers part of the wirelength that legalization lost, before routing.
- **Timing and routability fixes.** With timing or congestion in the cost, the same moves repair a few critical nets or crowded regions without a new global placement.
- **Engineering changes.** After a small change to the netlist, detailed placement improves the area around the change and leaves the rest alone.

## References
