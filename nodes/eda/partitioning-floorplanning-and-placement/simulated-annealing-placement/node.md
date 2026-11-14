---
tag: ZEMFMQ
kind: algorithm
slug: simulated-annealing-placement
name: Simulated annealing placement
aliases:
- TimberWolf placement
area: eda/partitioning-floorplanning-and-placement
level: core
summary: Sechen and Sangiovanni-Vincentelli's placement by annealing over moves and swaps of cells with a cost of wire length and overlap, with a shrinking range limiter.
solves: [placement-problem]
model: real-ram
complexity:
  vars: {n: the number of cells, P: the number of pins, K: the number of rows, S: the number of sites per row, L: the number of temperatures, M: the number of moves per cell at each temperature, D: "the largest number of pins on the nets of one cell, plus its width"}
  time: {worst: "O(L M n D + n (n + K) + K S + P)", average: "O(L M n D + n (n + K) + K S + P)", best: "O(L M n D + n log n + K S + P)"}
  space: {extra: "O(n + P + K S)"}
properties: {deterministic: false, randomized: true, exact: false}
history:
  year: 1985
  people: [Carl Sechen, Alberto Sangiovanni-Vincentelli]
  note: TimberWolf, published in 1985, made annealing the standard of quality for standard-cell placement for about ten years.
prereqs: [placement-problem, simulated-annealing, half-perimeter-wirelength]
see_also: [metropolis-criterion, cooling-schedule, simulated-annealing-convergence, min-cut-placement, quadratic-placement, placement-legalization, detailed-placement, independent-set-matching]
sources:
  - paper: doi:10.1109/JSSC.1985.1052337
    title: Carl Sechen and Alberto Sangiovanni-Vincentelli, The TimberWolf placement and routing package, IEEE Journal of Solid-State Circuits SC-20(2), 510 to 522, 1985
    locator: the cost function with an overlap penalty, the displacement and exchange moves, the range limiter, and the cooling schedule
  - paper: doi:10.1126/science.220.4598.671
    title: Scott Kirkpatrick, C. Daniel Gelatt and Mario P. Vecchi, Optimization by simulated annealing, Science 220(4598), 671 to 680, 1983
    locator: the annealing method and its first use on placement and wiring
  - paper: doi:10.1287/moor.13.2.311
    title: Bruce Hajek, Cooling schedules for optimal annealing, Mathematics of Operations Research 13(2), 311 to 329, 1988
    locator: the main theorem on logarithmic cooling schedules
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 4, Global and Detailed Placement (simulated annealing placement; general locator)
---

Simulated annealing placement solves the [placement problem](/placement-problem/) of standard cells by [simulated annealing](/simulated-annealing/). It starts from a random placement and repeats small random changes: move one cell to another place, or swap two cells. A change that lowers the cost is kept. A change that raises it by $\Delta$ is kept with the probability $e^{-\Delta / T}$, the [Metropolis criterion](/metropolis-criterion/), where the temperature $T$ falls slowly. The cost is the wirelength plus a penalty for overlap, so cells may overlap early and are pushed apart later. A range limiter makes the moves shorter as $T$ falls. Sechen and Sangiovanni-Vincentelli built this into TimberWolf in 1985. For about ten years it gave the best placements, at a high cost in run time, until analytical and min-cut placers matched its quality much faster.

## In plain words

Put the parts on the board anywhere, even on top of each other. Now pick a part at random and try to move it a little, or to swap it with a nearby part. If the wires get shorter, or parts stop overlapping, keep the change. If things get worse, still keep it sometimes, by a coin toss that is generous at first and stingy later.

Early on, parts jump far and bad moves are often kept, so the placement can leave a poor arrangement. Later, parts only take short steps and almost only good ones, so the placement settles. At the end, push the parts in each row side by side so nothing overlaps.

## The problem

The input is a netlist with $n$ cells, nets $e$ with weights $w_e$, $P$ pins and fixed pads, and $K$ rows of height 1 with $S$ unit sites. Cell $i$ has an integer width $W_i$, sits in a row $r_i$ with its left edge on a site $x_i$, and has its pin at its center. The output is a legal placement with a small total [HPWL](/half-perimeter-wirelength/).

During the annealing, overlap is allowed. The cost of a placement is

$$ C = 2 \sum_e w_e \operatorname{HPWL}(e) + \mu \cdot \text{overlap}, $$

where overlap is the sum over all sites of the number of cells on the site minus one, when that is positive. The factor 2 keeps all values integer, because the centers are at half sites. The weight $\mu$ sets the price of overlap against wire.

A **move** is either a displacement, where one cell goes to a new row and site, or a swap, where two cells take each other's places. The **range limiter** keeps moves inside a window of $w_x$ sites and $w_r$ rows around the cell; the window shrinks with $\log T$, so that late moves are short.

## The algorithm

```pseudo id=main
SA-PLACE(netlist, pads, K rows, S sites, T₀, T_end, α, M, μ)
L1  put each cell at a random site of a random row; compute C and the site counts
L2  T ← T₀; while T > T_end
L3      window wx ← max(1, round(S·f)), wr ← max(1, round(K·f)) with f = log(T/T_end) / log(T₀/T_end)
L4      repeat M·n times
L5          pick a cell; propose a displacement inside the window, or a swap with a cell inside the window
L6          apply the move; Δ ← the change of C, from the nets of the moved cells and the sites they leave and take
L7          if Δ > 0 and random() ≥ e^(−Δ/T) then undo the move
L8      T ← α·T
L9  move cells out of overfull rows to the nearest row with room, pack each row in x order, and return
```

Line L6 does not recompute the cost from scratch. Only the nets that contain a moved cell change, and only the sites under the moved cells change their counts, so $\Delta$ costs $O(D)$. Without a given $T_0$, the implementation sets it so that about 90 percent of the uphill moves are accepted at the start: $T_0 = \bar\Delta / \ln(1/0.9)$, where $\bar\Delta$ is the mean uphill $\Delta$ of $4n$ trial moves. Line L9 is a simple legalizer, as in [placement legalization](/placement-legalization/); if the cost has driven the overlap to zero and no row is overfull, it does not move any cell.

TimberWolf itself differs in details. It also changes the orientation of cells, it adds a penalty for rows that are longer or shorter than the target, it changes $\alpha$ during the run, and it ends with a second stage that removes the overlap and refines the result.

## Example

One row of 4 sites, three unit cells $a, b, c$ at sites 0, 1 and 2, a pad $p$ at $(0, 0)$, nets $\{a, c\}$ and $\{b, p\}$, and $\mu = 8$. The centers are at $0.5, 1.5, 2.5$ in $x$ and $0.5$ in $y$.

| step | placement | HPWL of $\{a, c\}$ | HPWL of $\{b, p\}$ | overlap | $C$ | $\Delta$ |
| --- | --- | --- | --- | --- | --- | --- |
| start | $a, b, c$ at 0, 1, 2 | 2 | 1.5 + 0.5 | 0 | 8 | |
| swap $a$ and $b$ | $b, a, c$ at 0, 1, 2 | 1 | 0.5 + 0.5 | 0 | 4 | $-4$ |
| move $c$ to site 3 | $b, a, c$ at 0, 1, 3 | 2 | 1 | 0 | 6 | $+2$ |
| move $c$ to site 1 | $c$ on top of $a$ | 0 | 1 | 1 | 10 | $+4$ |

The swap is always kept. The move of $c$ to site 3 is kept with probability $e^{-2/T}$: 0.37 at $T = 2$, but only 0.018 at $T = 0.5$. The move of $c$ onto $a$ shortens the net $\{a, c\}$ to zero, but the overlap costs 8, so at $T = 0.5$ it is kept with probability $e^{-8} \approx 0.0003$. The tests check these values of $\Delta$.

## Correctness

The returned placement is legal whenever line L9 finds room for every cell from an overfull row, which always holds for unit cells that fit the chip. Each row then has at most $S$ sites of cells, and the packing of a row places them on distinct sites inside it. Its HPWL is therefore at least the optimum. Line L6 computes the exact change of $C$, so the annealing follows the Metropolis rule for the stated cost. See the [proof](proofs/correctness.md).

Nothing in the run proves that the result is optimal or near optimal. Hajek's theorem ([convergence of simulated annealing](/simulated-annealing-convergence/)) says that the state converges in probability to the set of global minima when $T_k = c / \log(k + 1)$ with $c$ at least the depth of the deepest local minimum that is not global, and only then. No placer uses such a schedule: it needs a number of moves far beyond practice. The geometric schedule $T \leftarrow \alpha T$ of line L8, and of TimberWolf, is a heuristic.

## Complexity

- **Set up.** The random start, the site counts and the first cost cost $O(n W_{\max} + K S + P)$.
- **Annealing.** There are $L = \lceil \log(T_{\text{end}} / T_0) / \log \alpha \rceil$ temperatures and $M n$ moves at each. A move costs $O(D)$: it rescans the nets of at most two cells and updates the sites under them.
- **Packing.** Each cell leaves an overfull row at most once, and finding it and a row with room costs $O(n + K)$; packing the rows costs $O(n \log n)$.

So the time is $O(L M n D + n (n + K) + K S + P)$, and the space is $O(n + P + K S)$. The annealing term dominates in practice, because $L M$ is large: with $\alpha = 0.9$ and $M = 20$, a fall of $T$ by a factor of 1000 takes 66 temperatures and 1320 moves per cell.

## Properties

**What is proved.**

- The incremental $\Delta$ of line L6 equals the change of $C$ computed from scratch.
- At $T$ close to 0 no uphill move is kept, so the cost never rises.
- When line L9 returns, the placement is legal and its HPWL is at least the optimum.
- With a logarithmic schedule and a large enough constant, annealing converges in probability to an optimum (Hajek); the schedule of line L8 does not have this guarantee.

**What is measured.** The numbers come from the implementation of this page on toy inputs, not from benchmarks. On 20 random netlists of 6 unit cells in 2 rows of 4 sites (seed 10), the result equals the exhaustive optimum on 16 and is on average 1.013 times the optimum. On 10 random netlists of 30 cells of width 1 or 2 in 6 rows of 10 sites (seed 11, $\alpha = 0.9$, $M = 20$, $\mu = 8$), the mean HPWL is 120.35 for annealing, 130.6 for the same code at temperature near 0 (a greedy descent), and 281.35 for a random start packed into rows. With $\mu = 4$ the mean is 139.45: overlap costs only as much as two units of wire, so the annealing ends with overlap, and the packing of line L9 makes the wires longer.

## Variants and improvements

- **Other schedules.** Adaptive schedules set $\alpha$ and the number of moves from the spread of the cost at each temperature; TimberWolf used a fixed table of $\alpha$ values. See [cooling schedules](/cooling-schedule/).
- **TimberWolfSC versions.** Later versions by Sechen and his students added better net models, hierarchical annealing on clusters of cells, and faster schedules.
- **Annealing inside other placers.** Some placers use annealing only as a final step on small windows, or on the clusters of a [min-cut](/min-cut-placement/) placer, where the moves are few and the gain is local.
- **Detailed placement.** At low temperature with only swaps, annealing becomes a randomized [detailed placer](/detailed-placement/); deterministic moves such as [independent set matching](/independent-set-matching/) are faster for that job.
- **Floorplanning.** Annealing over a representation of block positions is still a common method for floorplans of a few hundred blocks.

## When to use it

Use annealing placement for small or medium instances, for unusual costs that are hard to make smooth, such as costs with many hard rules, or as a reference of quality when run time does not matter. For large standard-cell designs, use an analytical placer such as [quadratic placement](/quadratic-placement/) or [electrostatics-based placement](/electrostatics-based-placement/), then legalization and detailed placement; they reach similar or better wirelength in a small part of the time.

## Pitfalls

- **An overlap weight that is too small.** If overlap is cheap, the annealing keeps it, and the final packing destroys the wirelength. The measurement above shows this.
- **Recomputing the full cost per move.** That costs $O(P)$ per move instead of $O(D)$ and makes the method far slower.
- **A start temperature that is too low or too high.** Too low, and the run is a greedy descent; too high, and many temperatures are a random walk. Set $T_0$ from the uphill $\Delta$ of trial moves.
- **Swaps of cells of different width.** A swap must clamp each cell inside its new row, and the overlap it makes must enter $\Delta$.
- **Expecting the theory to hold.** The convergence theorem needs a logarithmic schedule; a geometric schedule gives no guarantee.

## Implementations

## History

Kirkpatrick, Gelatt and Vecchi introduced simulated annealing in 1983 and used placement and wiring of circuits as an example. Sechen and Sangiovanni-Vincentelli built TimberWolf on it in 1985, with an overlap penalty, a range limiter and a tuned schedule, and it gave the best standard-cell placements for about a decade. Hajek proved in 1988 when logarithmic schedules converge. From the late 1990s, multilevel min-cut placers and then analytical placers matched annealing's wirelength at a small part of its run time, and annealing moved to floorplanning and to small local steps.

## References
