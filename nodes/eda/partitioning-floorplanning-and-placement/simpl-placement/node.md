---
tag: S9RKW6
kind: algorithm
slug: simpl-placement
name: SimPL
aliases:
- simple placer with lookahead legalization
area: eda/partitioning-floorplanning-and-placement
level: research
summary: Kim, Lee and Markov's placer that alternates a quadratic solve with lookahead legalization by recursive spreading, and pulls cells toward the spread positions.
solves: [placement-problem]
model: real-ram
complexity:
  vars: {n: the number of movable cells, P: the number of pins, k: the number of iterations, t: the number of conjugate gradient steps per solve, K: the number of rows, S: the number of sites per row}
  time: {worst: "O(k (t (n + P) + n log n log(K S)))", average: "O(k (t (n + P) + n log n log(K S)))", best: "O(t (n + P) + n log n log(K S))"}
  space: {extra: "O(n + P)"}
properties: {deterministic: true, recursive: true, exact: false}
history:
  year: 2010
  people: [Myung-Chul Kim, Dong-Jin Lee, Igor L. Markov]
  note: SimPL was presented at ICCAD 2010 and in IEEE TCAD in 2012; it showed that a short quadratic placer with lookahead legalization matches the wirelength of far larger placers.
prereqs: [quadratic-placement, placement-legalization, conjugate-gradient-method]
see_also: [force-directed-placement, electrostatics-based-placement, analytical-placement, min-cut-placement, abacus-legalization, detailed-placement, clique-net-model, half-perimeter-wirelength]
sources:
  - paper: doi:10.1109/TCAD.2011.2170567
    title: Myung-Chul Kim, Dong-Jin Lee and Igor L. Markov, SimPL, an effective placement algorithm, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 31(1), 50 to 60, 2012
    locator: the lower-bound and upper-bound placements, lookahead legalization, the pseudo-nets to anchors, and the experiments
  - paper: doi:10.1109/ICCAD.2010.5654229
    title: Myung-Chul Kim, Dong-Jin Lee and Igor L. Markov, SimPL, an effective placement algorithm, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design (ICCAD), 649 to 656, 2010
    locator: the conference version of the method
  - paper: "Peter Spindler, Ulf Schlichtmann and Frank M. Johannes, Kraftwerk2, a fast force-directed quadratic placement approach using an accurate net model, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 27(8), 2008"
    locator: the bound to bound net model used by SimPL for the lower-bound placement (general locator)
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 4, Global and Detailed Placement (quadratic placement with spreading; general locator)
---

SimPL is a global placer for the [placement problem](/placement-problem/) of standard cells in chip design. It keeps two placements and improves them in turn. The lower-bound (LB) placement minimizes a quadratic model of the wirelength by a sparse linear solve, as in [quadratic placement](/quadratic-placement/), and ignores overlap, so its cells crowd together. The upper-bound (UB) placement spreads the LB cells over the chip by lookahead legalization, a recursive bisection that splits the cells in proportion to the free room, so it has almost no overlap. Then each cell gets a pseudo-net to its UB position, an anchor, and the next LB solve pulls it there; the anchor weights grow, so the two placements meet. The names are informal: the LB wirelength is not a proved lower bound on the optimum. Kim, Lee and Markov published SimPL in 2010; the method is short and fast and was competitive with much larger placers on the benchmarks of its time.

## In plain words

First tie all parts with rubber bands and let them go. They bunch up in the middle, which is good for the wires but not allowed. Then take that heap and spread it out: cut the board in half, send to each half as many parts as it has room for, keeping the parts on the same side as before, and repeat on each half.

Now each part has two places: where the bands want it, and where the spreading put it. Tie each part to its spread place with a new band, and let all go again. Make the new bands a little stronger every round. The two pictures come closer, and you stop when they nearly agree.

## The problem

The input is a netlist with $n$ movable cells, nets $e$ with weights $w_e$, $P$ pins and fixed pads, and $K$ rows of height 1 with $S$ sites of width 1. Cell $i$ has an integer width $W_i$, and its pin is at its center. The output is a legal placement: each cell on a site of a row, inside the row, with no overlap, and a small total [HPWL](/half-perimeter-wirelength/).

**The LB placement.** For a coordinate, the bound to bound (B2B) net model joins the two extreme pins of a net of $p$ pins to each other and joins each inner pin to both of them. Each edge between pins $a$ and $b$ has the weight $\frac{2 w_e}{(p - 1) \max(|c_a - c_b|, \varepsilon)}$, computed at the current coordinates $c$. At those coordinates, the quadratic cost $\sum w_{ab} (c_a - c_b)^2$ of the net is exactly twice its weighted span $w_e (\max c - \min c)$, if no two of its pins are closer than $\varepsilon$. With anchors $(\hat x_i, \hat y_i)$ and a weight $\alpha$, the LB step minimizes

$$ \sum_{\text{edges}} w_{ab} (x_a - x_b)^2 + \alpha \sum_i (x_i - \hat x_i)^2 $$

and the same in $y$. This is a positive definite linear system, solved by the [conjugate gradient method](/conjugate-gradient-method/). The B2B weights depend on the positions, so the solve is repeated a few times with new weights.

**The UB placement.** Lookahead legalization takes the LB positions and a region, starting with the whole chip. If the region has more than one row, it cuts the rows in half, sorts the cells by $y$, and gives the lower half the prefix of cells whose width is closest to the share of the lower half in the room, among the prefixes that fit in both halves. In a single row it cuts the sites in half and splits the cells sorted by $x$ in the same way. A row segment with one cell, or with no split that fits, is packed: the cells keep their $x$ order and go to the nearest free sites. SimPL's own lookahead legalization works on the overfilled regions only and stops at regions of a few bins, where it spreads the cells by scaling their coordinates. The version here cuts down to single rows, so its UB placement is legal.

## The algorithm

```pseudo id=main
SIMPL(netlist, pads, K rows, S sites)
L1  put all cells near the center of the chip
L2  LB ← the B2B quadratic solve, repeated with new weights, with no anchors
L3  for k = 1, 2, ...
L4      UB ← lookahead legalization of LB by recursive bisection
L5      record HPWL(UB) and keep the best UB so far
L6      the anchor of each cell ← its position in UB
L7      LB ← the B2B quadratic solve with a pseudo-net of weight α k from each cell to its anchor
L8      compute HPWL(LB)
L9      if HPWL(UB) − HPWL(LB) ≤ gap · HPWL(UB) then stop
L10 return the best UB
```

Line L2 alone is quadratic placement with the B2B model. Line L7 is the same solve with one more term per cell, the pull of its anchor; the weight grows linearly with $k$, so late iterations change the cells less and less. In SimPL the final UB placement then goes to a legalizer and a [detailed placer](/detailed-placement/).

## Example

**One lookahead legalization.** Two rows of 4 unit sites, and six unit cells $a, \ldots, f$ whose LB centers are

| cell | $a$ | $b$ | $c$ | $d$ | $e$ | $f$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | 1.2 | 1.5 | 1.8 | 2.1 | 2.4 | 2.0 |
| $y$ | 0.9 | 1.1 | 0.8 | 1.2 | 1.0 | 0.6 |

All six lie in a $1.2 \times 0.6$ box near the center. Lookahead legalization first cuts the two rows. In $y$ order the cells are $f, c, a, e, b, d$, and each row holds 4 of the total width 6, so the share of the lower row is 3: row 0 gets $f, c, a$ and row 1 gets $e, b, d$. Row 0 is cut at site 2. In $x$ order its cells are $a$ (1.2), $c$ (1.8), $f$ (2.0); the share of the left half is $\frac32$, and the prefixes of width 1 and 2 both fit and are equally close, so the first, $\{a\}$, goes left. The left half then packs $a$ at site 1, nearest to its left edge $0.7$. The right half $\{c, f\}$ is cut once more, and $c$ goes to site 2 and $f$ to site 3. Row 1 in the same way gives $b$ site 1, $d$ site 2 and $e$ site 3.

| row | site 0 | site 1 | site 2 | site 3 |
| --- | --- | --- | --- | --- |
| 1 | | $b$ | $d$ | $e$ |
| 0 | | $a$ | $c$ | $f$ |

Each cell moved less than 1.5 in $x$, and the cells kept their relative order in each cut. The tests check this result.

**The B2B weights.** A net of weight 1 on three pins at $x = 0, 3, 5$ gets the edges $(0, 5)$ with weight $\frac{2}{2 \cdot 5} = \frac15$, $(3, 0)$ with $\frac13$ and $(3, 5)$ with $\frac12$. The quadratic cost is $\frac15 \cdot 25 + \frac13 \cdot 9 + \frac12 \cdot 4 = 10$, twice the span 5.

## Correctness

The implementation returns a legal placement whenever lookahead legalization finds a split at every multi-row cut: every leaf is a row segment whose cells fit, and the packing of a segment never overlaps or leaves it. The returned HPWL is the least over the UB placements it computed, so it is at least the optimum of the placement problem, and on small instances the tests compare it with the exhaustive optimum. Each LB step solves its linear system exactly up to the tolerance of the conjugate gradient method, because the anchors make the matrix positive definite. See the [proof](proofs/correctness.md).

Nothing proves that the LB wirelength is below the optimum, or that the gap closes. The B2B cost matches HPWL only at the point where the weights were built, and the anchors add a cost that HPWL does not have.

## Complexity

- **LB step.** The B2B model has at most $2P$ edges. Building them and the matrix costs $O(n + P)$, and $t$ conjugate gradient steps cost $O(t (n + P))$. A constant number of weight updates keeps this bound.
- **UB step.** The recursion has depth $O(\log K + \log S)$, and each level sorts at most $n$ cells, $O(n \log n)$ per level, plus the packing of the rows, $O(n \log n)$ in total.
- **HPWL.** $O(P)$ per placement.

So $k$ iterations cost $O(k (t (n + P) + n \log n \log(K S)))$ time, and the space is $O(n + P)$. Nothing bounds $k$ or $t$ in terms of the input; both are limits that the user sets.

## Properties

**What is proved.**

- At the coordinates where they are built, the B2B weights give a quadratic cost equal to twice the weighted span of each net, when no two of its pins are closer than $\varepsilon$.
- With $\alpha > 0$ the LB system is positive definite, so the LB step has a unique solution.
- The packing of a row segment whose cells fit is legal, so each UB placement is legal when lookahead legalization succeeds, and so is the result.
- The result is legal, so its HPWL is at least the optimum; the method stops after the iteration limit.

**What is measured.** The numbers come from the implementation of this page on toy inputs, not from benchmarks. On 20 random netlists of 6 unit cells in 2 rows of 4 sites (seed 10), the result equals the exhaustive optimum on 3 and is on average 1.20 times the optimum. On 10 random netlists of 30 cells of width 1 or 2 in 6 rows of 10 sites (seed 11, 20 iterations), the first UB placement has a mean HPWL of 189.7, the best UB 158.8, and the last LB 93.3; the gap does not close, because the LB placement still has overlap. SimPL's paper reports HPWL and run times on the ISPD 2005 and 2006 benchmarks that match or beat the placers of its time; see the paper for the numbers.

## Variants and improvements

- **ComPLx.** Kim and Markov (2012) recast SimPL as a primal-dual Lagrangian method, with the anchors as the projection onto a feasible set, which explains the growing anchor weights.
- **MAPLE and POLAR.** Later placers keep the LB and UB loop but use nonlinear wirelength models or better spreading.
- **Region expansion.** SimPL's lookahead legalization finds clusters of overfilled bins, expands each until it has enough room, and bisects only those regions. This changes cells far from crowds less.
- **Other net models.** The [clique](/clique-net-model/) or star model can replace B2B; B2B is closer to HPWL.
- **Routability.** Later versions inflate cells in congested regions before lookahead legalization.

## When to use it

Use SimPL, or its loop of a quadratic solve and a spreading step, when you need a fast, simple and robust global placer for standard cells. It needs only a sparse linear solver and a recursive bisection. For the smallest wirelength on large designs, nonlinear placers such as [electrostatics-based placement](/electrostatics-based-placement/) do somewhat better at more cost per iteration. For mixed-size designs with many macros, the macros need separate handling.

## Pitfalls

- **Calling LB a lower bound.** The LB wirelength is a heuristic estimate. It can even exceed the optimum, because B2B and the anchors are not HPWL.
- **B2B weights with coincident pins.** Two pins at the same place give a division by zero. Use a floor $\varepsilon$ on the distance.
- **Anchor weights that grow too fast.** The LB placement then freezes on the first UB placement, and the result is no better than one round of spreading.
- **A full chip.** If the rows are nearly full, the area split may not fit both halves, as in [legalization](/placement-legalization/); the version here then fails. Leave some free room or use a full legalizer at the end.

## Implementations

## History

Kim, Lee and Markov presented SimPL at ICCAD 2010 and in IEEE TCAD in 2012. The idea of spreading by anchors in a quadratic placer was older, in FastPlace and Kraftwerk; SimPL's point was that a short, plain loop of a lower-bound solve and a lookahead legalization was enough to match the best placers of the ISPD contests. Kim and Markov then gave the loop a Lagrangian form in ComPLx (2012).

## References
