---
tag: 5EREMJ
kind: algorithm
slug: heap-fpga-placement
name: HeAP FPGA placement
aliases:
- heterogeneous analytical placement
- analytical placement for heterogeneous FPGAs
area: eda/fpga-analog-and-emerging-technologies
level: research
summary: Gort and Anderson's analytical FPGA placer that solves a quadratic wirelength model and spreads LUTs, RAMs and DSP blocks into their own columns by partitioning.
solves: [placement-problem]
model: real-ram
complexity:
  vars: {n: the number of blocks, Q: the number of terminal pairs of the clique model, S: the number of sites, t: the number of conjugate gradient steps per solve, k: the number of iterations}
  time: {per_iteration: "O(t (n + Q) + S log^2 S)", total: "O(k (t (n + Q) + S log^2 S))"}
  space: {total: "O(n + Q + S)"}
properties: {deterministic: true, recursive: true, exact: false}
history:
  year: 2012
  people: [Marcel Gort, Jason H. Anderson]
  note: HeAP adapted the SimPL loop of a quadratic solve, spreading and anchors to FPGAs whose logic blocks, multipliers or DSP blocks and block RAMs sit in columns of their own type.
prereqs: [simpl-placement, quadratic-placement, island-style-fpga]
see_also: [analytical-placement, clique-net-model, conjugate-gradient-method, placement-legalization, fpga-timing-driven-annealing-placement, half-perimeter-wirelength, min-cut-placement, detailed-placement]
sources:
  - paper: doi:10.1109/FPL.2012.6339278
    title: Marcel Gort and Jason H. Anderson, Analytical placement for heterogeneous FPGAs, Proceedings of the International Conference on Field Programmable Logic and Applications (FPL), 143 to 150, 2012
    locator: the HeAP algorithm, which adapts SimPL to FPGAs with LUT-based logic blocks, multiplier or DSP blocks and block RAMs (general locator)
  - paper: doi:10.1109/TCAD.2011.2170567
    title: Myung-Chul Kim, Dong-Jin Lee and Igor L. Markov, SimPL, an effective placement algorithm, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 31(1), 50 to 60, 2012
    locator: the lower-bound and upper-bound placements, the spreading by recursive bisection and the pseudo-nets to anchors that HeAP builds on
---

HeAP is an analytical placer for heterogeneous FPGAs, a topic of FPGA CAD: it places the packed logic blocks, block RAMs and DSP blocks of a netlist on an [island-style FPGA](/island-style-fpga/) whose columns each hold one type of block. It follows [SimPL](/simpl-placement/): it minimizes a quadratic model of the wirelength by a sparse linear solve, spreads the crowded result over the legal sites, and pulls the next solve toward the spread positions with anchors of growing weight. The FPGA part is the spreading, which Gort and Anderson do separately for each block type, inside the columns of that type.

## In plain words

An FPGA chip is a grid of seats, and each column of seats takes only one kind of part: logic, memory or multiplier. The placer must give every part a seat of its kind and keep connected parts close.

HeAP first pretends that wires are springs and finds where the parts settle. That is fast, but the parts bunch up, and a memory may settle on a logic column.

So HeAP then spreads each kind of part over the seats of that kind. It cuts the seats into halves, again and again, and sends the parts to the halves in the order of where they settled. Every part now has its own seat of the right kind.

Then it ties each part to its seat with a weak spring and lets the springs settle again. The ties get stronger each round, and HeAP keeps the best spread it has seen.

## The problem

**Input.** A grid of $n_x$ columns and $n_y$ rows of sites, a type for each column (such as logic, memory or DSP), $n$ blocks with a type each, fixed pads with real positions, and a list of nets, each a set of blocks and pads.

**Output.** A legal placement: an injective map from the blocks to the sites that puts every block on a site of its own type.

**Goal.** Small total [half-perimeter wirelength](/half-perimeter-wirelength/) (HPWL), the sum over the nets of the width plus the height of the bounding box of their terminals. This is the wirelength version of the [placement problem](/placement-problem/), with the column types as an extra constraint. HeAP does not minimize it exactly.

## The algorithm

The quadratic model replaces each net of $p$ terminals by a clique whose $p (p - 1) / 2$ edges each weigh $1 / (p - 1)$ (the [clique net model](/clique-net-model/)), and minimizes the weighted sum of squared edge lengths, separately in $x$ and in $y$. With anchors $a_i$ of weight $\beta$, it adds $\beta \sum_i \lVert p_i - a_i \rVert^2$. The minimum solves a sparse symmetric positive definite system, which the [conjugate gradient method](/conjugate-gradient-method/) solves.

```pseudo id=main
HEAP(grid, blocks, nets, iters, α)
L1  pos ← the minimum of the quadratic model with no anchors
L2  best ← none
L3  for k ← 1 to iters:
L4      for each block type t: SPREAD(the blocks of type t, the sites of type t, pos)
L5      if the HPWL of the spread placement is less than that of best: best ← the spread placement
L6      β ← α k
L7      pos ← the minimum of the quadratic model with each block anchored to its spread site with weight β
L8  return best
```

SPREAD$(B, S)$ is a recursive bisection. With one site, it puts the one block there. Otherwise it cuts the sites $S$ into a low and a high part along the axis on which they spread more, keeping sites with the same coordinate together where it can. It sorts the blocks $B$ by their position along the same axis and sends to the low part a share of the blocks equal to its share of the sites, rounded, but never more blocks than sites to either part. Then it recurses on both parts. Since a column has one type, the call for type $t$ only sees the columns of type $t$; for a memory type with one column, the cuts run along that column.

The implementation makes three simplifications, and says so. It uses the clique model throughout; it adds a tiny pull of weight $10^{-3}$ toward the center of the grid so that the system stays positive definite when a group of blocks has no path to a pad; and its spreading cuts sites, not area, so that the leaves of the recursion are single sites and the spread placement is already legal. SimPL spreads by area into regions and then legalizes. The net model and the exact spreading and legalization steps of HeAP are in the paper and are not repeated here.

## Example

The grid has 3 columns and 2 rows; columns 0 and 2 are logic (L), column 1 is memory (M). Blocks 0, 1 and 2 are logic and block 3 is memory. Pad $P_0$ is at $(-1, 0.5)$ and pad $P_1$ at $(3, 0.5)$. The five nets each have two terminals: $\{P_0, 0\}$, $\{0, 3\}$, $\{3, 1\}$, $\{1, P_1\}$ and $\{2, 3\}$.

**Line L1.** Every net has two terminals, so every edge weighs 1. In $x$, block 0 sits between $P_0$ and block 3, block 3 between blocks 0, 1 and 2, block 1 between block 3 and $P_1$, and block 2 only on block 3. Setting each gradient to zero gives $x_0 = 0$, $x_3 = 1$, $x_1 = 2$ and $x_2 = 1$, and every $y$ is $0.5$. So block 2 lands on top of block 3, in the memory column.

**Line L4.** The logic sites are $(0, 0), (0, 1), (2, 0), (2, 1)$. They spread more in $x$, so the cut puts column 0 low and column 2 high, two sites each. The logic blocks in $x$ order are 0, 2, 1, so the low part gets $\lfloor 3 \cdot 2 / 4 + 1/2 \rfloor = 2$ blocks, 0 and 2, and the high part gets block 1. In column 0 the cut is in $y$; both blocks have $y = 0.5$, and the tie goes to the smaller $x$, so block 0 gets $(0, 0)$ and block 2 gets $(0, 1)$. Block 1 gets $(2, 0)$, and the memory block 3 gets $(1, 0)$.

**Line L5.** The HPWL is $1.5 + 1 + 1 + 1.5 + 2 = 7$ for the nets in the order above. Trying every legal placement gives 7 as well, so on this instance the first spread is already optimal, and the later iterations keep it.

**A larger toy run.** On an 8 by 6 grid with columns L L M L L D L L, 30 logic blocks, 4 memory blocks, 3 DSP blocks, 6 pads and 43 random nets (seed 2), the HPWL of the spread placement was 189 after the first iteration and 177 after the ninth, and it stayed at 177 to iteration 20. Twenty random legal placements (seeds 100 to 119) had a mean HPWL of 282.7 and a best of 248. This is a toy run of the implementation, not a benchmark result.

## Correctness

The [full proof](proofs/correctness.md) shows the following.

- **The solve is exact for its model.** The matrix of the quadratic model is symmetric positive definite, so the model has one minimum, and conjugate gradients reach it in at most $n$ steps in exact arithmetic. In floating point the solve stops at a tolerance; the tests compare it with exact Gaussian elimination.
- **Spreading is legal.** If a type has no more blocks than sites, SPREAD gives each block a distinct site of that type. The proof is an induction on the number of sites: both parts of a cut are nonempty, and the clamped share never sends more blocks to a part than it has sites.
- **The result is legal and its cost is a true upper bound.** Every spread placement is legal, since columns of different types share no sites, and HEAP returns the one of least HPWL. So its HPWL is at least the optimum.

Nothing bounds the gap to the optimum, and nothing proves that the iterations converge or that the HPWL falls each round. On 60 seeded instances on a 3 by 2 grid (seed 1), the result was optimal on 20, and the mean ratio to the exhaustive optimum was about 1.10, with a worst case of about 1.44. These are measured on toy instances.

## Complexity

Let $Q$ be the number of terminal pairs of the clique model, the sum of $p (p - 1) / 2$ over the nets. Building the system takes $O(n + Q)$ time, and each conjugate gradient step is one product with a matrix of $O(n + Q)$ nonzeros, so a solve with $t$ steps takes $O(t (n + Q))$. SPREAD sorts the sites and the blocks at each level of the recursion; the levels have $O(\log S)$ depth and each level sorts at most $S$ items in all, so a spread of all types takes $O(S \log^2 S)$. The HPWL takes $O(\sum p)$, which is within $O(n + Q)$ for nets of at least two terminals. In total, $k$ iterations take $O(k (t (n + Q) + S \log^2 S))$ time and $O(n + Q + S)$ space. The clique model makes $Q$ quadratic in the size of a net, which is why large placers use sparser net models.

## Properties

- **Legal at every iteration.** Each spread placement is legal, so the algorithm can stop at any iteration with a usable result.
- **Deterministic.** There is no randomness; ties are broken by position and then by block index.
- **Types are separate.** Each type is spread only over its own columns, so a memory block never takes a logic site, and the logic blocks are spread around the memory and DSP columns, not over them.
- **Not exact.** The quadratic model is not HPWL, and the spreading follows the order of the solve, so the result can be worse than the optimum, as the toy runs show.

## Variants and improvements

- **Net models.** The clique model costs $O(p^2)$ per net. SimPL uses the bound-to-bound model of Kraftwerk2, with $O(p)$ edges per net, whose weights make the quadratic cost of a net equal to its HPWL at the current positions; see [analytical placement](/analytical-placement/).
- **Area-based spreading and legalization.** SimPL spreads by area into regions and then [legalizes](/placement-legalization/); this keeps fine detail of the solve that a site-by-site cut loses.
- **Detailed placement.** A short [detailed placement](/detailed-placement/) after the global placement, such as low-temperature annealing or pairwise swaps, recovers wirelength that the spreading lost.
- **Timing.** Weights on critical nets, as in [timing-driven annealing placement](/fpga-timing-driven-annealing-placement/), pull critical connections shorter.

## When to use it

Use an analytical placer like HeAP for large FPGA designs where an annealer is too slow, and where the device has columns of memory and DSP blocks among the logic. The quadratic solve scales well, and spreading per type handles the columns directly. For small designs, or when the last few percent of wirelength matter, anneal the result or use the annealing placer alone.

## Pitfalls

- **Spreading all types together.** A spreading step that ignores types puts memory blocks on logic sites. Spread each type over its own columns.
- **A singular system.** If a group of blocks has no path to a pad and no anchor, the matrix is only positive semidefinite and the solve has no unique answer. Add anchors, a small diagonal term, or fix some blocks.
- **Anchors too strong too soon.** A large first anchor weight freezes the first spread, which follows a crowded solve. Grow the weight slowly.
- **Reading the quadratic minimum as a bound.** The wirelength of the unspread solve is not a proved lower bound on the optimal HPWL; it is the minimum of a different objective.

## Implementations

## History

Kim, Lee and Markov (2010) showed with SimPL that a short loop of a quadratic solve, a spreading step and anchors could match far larger placers for standard cells. Gort and Anderson (2012) adapted that loop to heterogeneous FPGAs with LUT-based logic blocks, multiplier or DSP blocks and block RAMs, where each block type has its own columns, and named it HeAP. At the time, the standard academic FPGA placer was the [annealing placer](/fpga-timing-driven-annealing-placement/) of VPR; analytical placers for FPGAs have since become common.

## References
