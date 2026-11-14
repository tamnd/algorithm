---
tag: ZDNXW1
kind: algorithm
slug: fpga-timing-driven-annealing-placement
name: Timing-driven annealing placement for FPGAs
aliases:
- VPR placement
- T-VPlace
area: eda/fpga-analog-and-emerging-technologies
level: core
summary: Betz, Marquardt and Rose's FPGA placer that swaps blocks by simulated annealing with an adaptive move range and a cost mixing wirelength and timing criticality.
solves: [timing-driven-placement]
model: word-ram
complexity:
  vars: {n: the number of blocks, P: the number of pins on all nets, F: the number of pins on the nets of the moved blocks, k: the number of temperatures}
  time: {per_move: O(F), per_temperature: O(n^(4/3) F + P), total: O(k (n^(4/3) F + P))}
  space: {total: O(n + P)}
properties: {deterministic: false, recursive: false, exact: false}
history:
  year: 2000
  people: [Alexander Marquardt, Vaughn Betz, Jonathan Rose]
  note: Betz and Rose's VPR placer of 1997 annealed the bounding box cost with an adaptive schedule and range limit. Marquardt, Betz and Rose added a timing cost weighted by criticality and a normalized mix of the two costs in 2000.
prereqs: [simulated-annealing-placement, island-style-fpga, static-timing-analysis]
see_also: [timing-driven-placement, half-perimeter-wirelength, simulated-annealing, heap-fpga-placement, fpga-packing, t-vpack, negotiated-congestion-routing, minimum-channel-width]
sources:
  - paper: doi:10.1145/329166.329208
    title: Alexander Marquardt, Vaughn Betz and Jonathan Rose, Timing-driven placement for FPGAs, Proceedings of the ACM/SIGDA International Symposium on Field Programmable Gate Arrays (FPGA '00), 203 to 213, 2000
    locator: the timing cost with the criticality exponent, the normalized cost of a move with the weight lambda, and the update of the criticalities once per temperature
  - book: isbn:9780792384601
    title: Vaughn Betz, Jonathan Rose and Alexander Marquardt, Architecture and CAD for Deep-Submicron FPGAs, Kluwer, 1999 (doi 10.1007/978-1-4615-5145-4)
    locator: Chapter 4, the VPR placer (the bounding box cost with the factor q, the initial temperature, the number of moves per temperature, the update of the temperature and of the range limit from the acceptance rate, and the exit test)
  - paper: "Vaughn Betz and Jonathan Rose, VPR, a new packing, placement and routing tool for FPGA research, Field-Programmable Logic and Applications (FPL 1997), Lecture Notes in Computer Science 1304, Springer, 1997"
    locator: the adaptive annealing schedule of VPR (general locator)
  - paper: "Chih-Liang Eric Cheng, RISA, accurate and efficient placement routability modeling, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design (ICCAD), 1994"
    locator: the factor q(n) that corrects the bounding box of a net with n terminals (general locator)
---

Timing-driven annealing placement is the placer of VPR for an [island-style FPGA](/island-style-fpga/): it puts the packed blocks on the sites of the grid by [simulated annealing](/simulated-annealing-placement/), with moves that swap two blocks or move one to an empty site. The cost of a move mixes the change of a bounding box wirelength estimate and the change of a timing cost, in which each connection's delay is weighted by its criticality, each normalized by its value at the start of the temperature. An adaptive schedule sets the temperature, the number of moves and the range of a move from the fraction of moves that are accepted. The algorithm belongs to the FPGA CAD topic of this sub-area.

## In plain words

After packing, the design is a few thousand blocks that must go onto a grid of sites. Blocks that are joined by nets should be close, so that the router needs short wires, and blocks on the slowest paths should be closest of all.

The placer starts from a random layout and then tries many small changes: move a block to a nearby site, or swap two blocks. A change that makes the layout better is kept. A change that makes it worse is sometimes kept too, more often early on, so the layout can get out of a bad corner. Over time the placer accepts fewer bad changes and makes its moves shorter, until the layout settles.

The score of a layout counts both the wire needed and the delay of the slow paths, so the placer trades a little wire for speed where it matters.

## The problem

**Input.** A grid of $n_x \times n_y$ sites, $n$ blocks, and nets, each a driver block and one or more sink blocks. A weight $\lambda \in [0, 1]$.

**Output.** A legal placement: each block on its own site.

**Goal.** Low wirelength and low critical path delay, in the sense of the [timing-driven placement](/timing-driven-placement/) problem. The algorithm minimizes a cost that stands for both; it does not find the minimum.

The model of this page has one block type, and a connection between sites $a$ and $b$ has delay $1 + |x_a - x_b| + |y_a - y_b|$. VPR uses a table of routed delays by distance and has I/O pads on the border and other block types in columns.

## The algorithm

The costs:

- **Bounding box cost.** $BB = \sum_e q(|e|) \, (\Delta x(e) + 1 + \Delta y(e) + 1)$, where $\Delta x(e)$ and $\Delta y(e)$ are the spans of the bounding box of net $e$. This is the [half-perimeter wirelength](/half-perimeter-wirelength/) counted in channels crossed. The factor $q$ from Cheng is 1 for up to three terminals and grows with more, to about 2.79 at 50, because the half-perimeter underestimates the wire of a net with many terminals.
- **Timing cost.** $T = \sum_c d(c) \, \mathrm{crit}(c)^{CE}$ over all connections $c$ from a driver to a sink, where $\mathrm{crit}(c) = 1 - \mathrm{slack}(c) / D_{max}$ comes from a [static timing analysis](/static-timing-analysis/) and $CE$ is the criticality exponent.
- **Move cost.** $\Delta C = \lambda \, \Delta T / T_{prev} + (1 - \lambda) \, \Delta BB / BB_{prev}$, with $T_{prev}$ and $BB_{prev}$ the costs at the start of the temperature.

```pseudo id=main
PLACE(blocks, nets, n_x, n_y, λ, inner)
L1  random legal placement; T ← 20 × the standard deviation of the cost over n random moves; R ← R_max = max(n_x, n_y) − 1
L2  while T ≥ 0.005 / (number of nets):
L3      timing analysis: weights crit(c)^CE; set BB_prev and T_prev to the current costs
L4      repeat inner × n^(4/3) times:
L5          pick a random block a and a random site s with |Δx|, |Δy| ≤ R; the move swaps a with the block at s, if any
L6          ΔC ← λ ΔT / T_prev + (1 − λ) ΔBB / BB_prev, from the nets and connections of the moved blocks only
L7          if ΔC ≤ 0, or a random number in [0, 1) is below exp(−ΔC / T), make the move
L8      R_acc ← accepted / tried; T ← α(R_acc) × T, with α = 0.5, 0.9, 0.95, 0.8 for R_acc > 0.96, > 0.8, > 0.15, otherwise
L9      R ← R × (1 − 0.44 + R_acc), kept in [1, R_max]; CE ← 1 + 7 (1 − (R − 1) / (R_max − 1))
L10 one more round of moves at T = 0, which accepts only moves with ΔC ≤ 0
L11 return the placement
```

The schedule aims at an acceptance rate of 0.44: the range limit grows when more moves are accepted and shrinks when fewer are, and the temperature falls slowly while the acceptance rate is in the middle band, where the cost improves most. As the range shrinks, the exponent $CE$ rises from 1 to 8, so late in the anneal only the most critical connections carry weight. The exit test of VPR is $T < 0.005 \, C / m$ for the cost $C$ and $m$ nets. With normalized costs, $C$ is about 1, which gives line L2.

## Example

Take a $3 \times 2$ grid, three blocks and two nets, $e_1 = (0, 1)$ and $e_2 = (1, 2)$, so the connections are $0 \to 1$ and $1 \to 2$. Place block 0 at $(0, 0)$, block 1 at $(2, 0)$ and block 2 at $(0, 1)$, with $\lambda = 0.5$ and $CE = 1$.

- $BB$: net $e_1$ spans $x$ from 0 to 2 and one row, so $3 + 1 = 4$; net $e_2$ spans $x$ from 0 to 2 and two rows, so $3 + 2 = 5$; $BB = 9$.
- Timing: $d(0 \to 1) = 1 + 2 = 3$ and $d(1 \to 2) = 1 + 2 + 1 = 4$. The only path has delay $D_{max} = 7$, so both connections have criticality 1 and $T = 7$.

Move block 1 to the empty site $(1, 0)$. Net $e_1$ becomes $2 + 1 = 3$ and net $e_2$ becomes $2 + 2 = 4$, so $\Delta BB = -2$; the delays become 2 and 3, so $\Delta T = -2$. Then

$$\Delta C = 0.5 \cdot \frac{-2}{7} + 0.5 \cdot \frac{-2}{9} = -\frac{16}{63} \approx -0.254,$$

and the move is made. The move back has $\Delta C = +16/63$ measured against the same normalizers; at $T = 0.1$ it is accepted with probability $e^{-2.54} \approx 0.079$.

On a toy run, 25 blocks with 30 random nets on a $5 \times 5$ grid (netlist seed 2, placer seed 3, inner $= 2$), a random placement has $BB \approx 192.7$ and a critical path delay of 34. The placer, after 79 temperatures of 146 moves each, ends with $BB \approx 135.3$ and delay 18 for $\lambda = 0.5$, and with $BB \approx 132.3$ and delay 21 for $\lambda = 0$. This is a toy run, not a benchmark result, but it shows the trade: the timing term buys a shorter critical path for a little more wire.

## Correctness

The [full proof](proofs/correctness.md) shows four things.

- **Legality.** A move to an empty site or a swap keeps each block on its own site, so every placement the algorithm visits is legal.
- **Exact incremental cost.** Only nets with a moved block and connections with a moved end change, so the costs of line L6, summed over the accepted moves, equal the costs recomputed from scratch. The tests run the placer with a recomputation after every move.
- **Criticalities.** The timing analysis gives $\mathrm{crit}(c) = \ell(c) / D_{max}$, where $\ell(c)$ is the longest path through $c$.
- **Termination.** The temperature falls by a factor of at most 0.95 per round, so the number of temperatures is $O(\log(T_0 \cdot m))$ for $m$ nets.

What is not proved is the quality of the result. Simulated annealing reaches an optimum with probability tending to 1 only under cooling schedules far slower than this one, so the placer is a heuristic. On 40 random netlists of 3 to 5 blocks on a $3 \times 2$ grid with $\lambda = 0$ (seed 1), the placer matched the exhaustive optimum of $BB$ on all 40; this is a measurement on tiny instances, not a guarantee.

## Complexity

A move touches the nets and connections of at most two blocks, so with $F$ the number of pins on those nets it costs $O(F)$. A temperature makes $\mathrm{inner} \cdot n^{4/3}$ moves and one timing analysis in $O(P)$ time, where $P$ is the number of pins of all nets, so it costs $O(n^{4/3} F + P)$. The number $k$ of temperatures depends on the acceptance rates; Lemma 4 of the proof bounds it by $O(\log(T_0 m))$, and the toy run above used 79. The space is $O(n + P)$.

VPR updates the bounding box of a net in $O(1)$ in most cases by keeping the number of terminals on each edge of the box, and recomputes it only when a terminal leaves an edge that it alone held. The implementation recomputes the boxes of the affected nets, which costs $O(F)$.

## Properties

- **Randomized.** The result depends on the seed of the random generator.
- **Adaptive.** The schedule needs no tuning per design: the starting temperature, the cooling rate and the range limit all follow the measured acceptance rate.
- **Trade-off by one weight.** $\lambda = 0$ gives the wirelength-only placer, and $\lambda$ near 1 places for delay only. Marquardt, Betz and Rose used $\lambda = 0.5$ and report a large cut in critical path delay for a small growth in wirelength over the placer without timing; that is a measured result on their benchmarks.
- **Stale timing.** Criticalities are fixed during a temperature, so a move that changes the critical path is judged with old weights until the next analysis.
- **Effort knob.** The factor inner scales the number of moves, trading run time for quality.

## Variants and improvements

- **Path-based timing cost.** Instead of weighting connections, add the delay of the critical paths. This is more exact and slower.
- **Directed moves.** Move a block toward the center of its nets, or toward a critical neighbor, instead of to a random site in range.
- **Heterogeneous arrays.** Restrict moves of a memory or DSP block to sites of its own type in its columns, as VPR does for each block type.
- **Analytical start.** Start the anneal at a low temperature from a placement found by an analytical method, such as [HeAP](/heap-fpga-placement/), and use annealing only to refine it.
- **Parallel annealing.** Split the grid into regions and anneal them in parallel, at the cost of moves that cross regions.

## When to use it

Use timing-driven annealing to place packed blocks on an FPGA when quality matters more than run time, and the design has up to some hundred thousand blocks. It handles any cost that can be evaluated per move, including timing, congestion and heterogeneous sites. For very large designs, an analytical placer is much faster, and annealing then serves as the refinement step. Run the placer with $\lambda = 0$ if only the [minimum channel width](/minimum-channel-width/) matters.

## Pitfalls

- **Costs on different scales.** $\Delta T$ and $\Delta BB$ have different units. Without the normalization by $T_{prev}$ and $BB_{prev}$, one term swamps the other, and the weight $\lambda$ means nothing.
- **Drift of the incremental cost.** Floating point totals drift after millions of moves. Recompute both costs from scratch at the start of each temperature.
- **Range limit below 1.** A range limit below 1 allows no move. Keep it at least 1.
- **Criticality without exponent.** With $CE = 1$, near-critical and non-critical connections weigh almost the same. The exponent sharpens the focus on the critical paths.
- **Too few moves.** Fewer moves per temperature save run time but lower the quality. Change the factor inner, not the exponent $4/3$, to trade the two.

## Implementations

## History

Annealing placement of standard cells goes back to [TimberWolf](/simulated-annealing-placement/) by Sechen and Sangiovanni-Vincentelli in the 1980s, with its range limiter. Betz and Rose's VPR (1997) adapted it to FPGAs with a schedule driven by the acceptance rate: the starting temperature from the spread of the cost, the cooling factor from the acceptance rate, and a range limit that keeps that rate near 0.44, and with Cheng's factor $q$ in the bounding box cost. Marquardt, Betz and Rose (2000) added the timing cost with criticality weights and the normalized mix of the two costs; this placer, often called T-VPlace, became the default of VPR and of the VTR flow.

## References
