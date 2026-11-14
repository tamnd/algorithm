---
tag: BTYXM7
kind: algorithm
slug: shrunk-2d
name: Shrunk-2D
aliases:
- Shrunk-2D flow
- pseudo-3D placement
area: eda/fpga-analog-and-emerging-technologies
level: research
summary: Panth, Samadi, Du and Lim's two-tier monolithic 3D flow that places and routes cells shrunk by 0.707 on a 2D die of half the area, then splits each bin between tiers.
solves: [tier-partitioning]
model: word-ram
complexity:
  vars: {n: the number of cells, p: the number of pins, P: the number of FM passes, B: the number of placement bins}
  time: {shrinking: O(n + p), split with bucket-list FM: O(P p + B), MIV count: O(p)}
  space: {total: O(n + p + B)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2014
  people: [Shreepad Panth, Kambiz Samadi, Yang Du, Sung Kyu Lim]
  note: Shrunk-2D gave the first complete RTL-to-GDSII flow for gate-level monolithic 3D ICs that handles memory macros, built on a commercial 2D place and route tool.
prereqs: [three-dimensional-integrated-circuit, tier-partitioning, fiduccia-mattheyses, half-perimeter-wirelength]
see_also: [through-silicon-via, quadratic-placement, analytical-placement, placement-problem, clock-tree-synthesis, multilevel-hypergraph-partitioning, thermal-driven-3d-floorplanning, global-routing]
sources:
  - paper: doi:10.1145/2627369.2627642
    title: "Shreepad Panth, Kambiz Samadi, Yang Du and Sung Kyu Lim, Design and CAD methodologies for low power gate-level monolithic 3D ICs, Proceedings of the International Symposium on Low Power Electronics and Design (ISLPED 2014), La Jolla"
    locator: Section 3.1 (the argument that z is negligible), Section 3.2 (scaling by 0.707, the 29.3% HPWL bound, metal width and pitch scaled with RC per unit length kept), Section 3.3 (memory as pins plus full and partial placement blockages), Section 3.5.1 (FM with area balance in each placement bin), Section 3.5.2 (leaf-level 3D clock tree), Section 3.5.3 (MIV insertion by a 2D router on a doubled metal stack), Section 4 (OpenSPARC T2 in 28 nm at 1 GHz, Tables 1 to 4)
  - paper: doi:10.1109/DAC.1982.1585498
    title: "C. M. Fiduccia and R. M. Mattheyses, A linear-time heuristic for improving network partitions, Proceedings of the 19th Design Automation Conference (DAC 1982), pages 175 to 181"
    locator: the move-based min-cut pass with bucket lists and the balance rule that lets each side be off by the largest cell (general locator)
  - paper: doi:10.1109/ASPDAC.2011.5722210
    title: "S. Bobba, A. Chakraborty, O. Thomas, P. Batude, T. Ernst, O. Faynot, D. Z. Pan and G. De Micheli, CELONCEL, effective design technique for 3-D monolithic integration targeting high performance integrated circuits, Proceedings of the 16th Asia and South Pacific Design Automation Conference (ASP-DAC 2011), pages 336 to 343"
    locator: the earlier gate-level monolithic 3D flow that Panth et al. call rudimentary, because it does not handle memory macros (general locator)
---

Shrunk-2D is a design flow for two-tier gate-level monolithic [3D ICs](/three-dimensional-integrated-circuit/), a part of 3D integration in EDA. In a monolithic 3D IC the tiers are a few micrometers apart and joined by monolithic inter-tier vias (MIVs) of about 100 nm, so the third dimension adds almost nothing to the wirelength. Shrunk-2D uses this. It scales every cell, the die and the metal pitch by $1/\sqrt{2} \approx 0.707$, so that all cells fit on a 2D die of half the area, and runs a normal 2D tool for placement, optimization, clock tree and routing. Then it gives every cell back its size, splits the cells of each small region between the two tiers with a [Fiduccia-Mattheyses](/fiduccia-mattheyses/) min-cut that keeps each region balanced, and lets a router insert the MIVs. Panth, Samadi, Du and Lim (ISLPED 2014) used it on the OpenSPARC T2 core in 28 nm and report 15.57% less total power than a 2D design at the same frequency and total silicon area.

## In plain words

Two tiers of the same size stacked on top of each other look, from above, like one die of half the area with twice as many cells per square. So you can pretend each cell is half as large, place and route everything on that small die with an ordinary 2D tool, and get wires that are as long as the wires of the real two-tier chip.

At the end you must decide which cells go up and which go down. You cut the small die into a grid of bins and, in each bin, put half the cell area on each tier, while keeping as few nets as possible split between tiers. Each split net gets a tiny vertical via. Since the bins are small, a cell does not move far, and the work of the 2D tool is kept.

## The problem

**Input.** A gate-level netlist of standard cells and memory macros with fixed places for the memories, the target footprint of the 3D design (half the area of the 2D design), a technology with its cell library and metal stack, and a timing target.

**Output.** A two-tier layout: for each cell a tier and a place, the routes in each tier, and the MIVs that join the tiers. Each tier must fit the footprint, and the design must meet timing.

**Goal.** Less power than a 2D design at the same performance and the same total silicon area. The step that this page computes is a case of [tier partitioning](/tier-partitioning/) with a balance rule in every bin; the 2D steps are done by the 2D tool.

## The algorithm

Let $s = 1/\sqrt{2}$.

```pseudo id=main
SHRUNK-2D(netlist, die, k, ε)
L1  scale the width, height and pin offsets of each cell, the die, and the metal width and pitch by s; keep the wire RC per unit length
L2  place, optimize, build the clock tree and route the shrunk design with the 2D tool
L3  give each cell back its original size at its place
L4  cut the die into k × k placement bins
L5  in each bin, put the cells on the tiers largest first, each to the tier with less area in that bin
L6  repeat
L7      FM pass: move the unlocked cell of best gain whose move keeps its bin balanced, and lock it, until no cell can move
L8      keep the prefix of the moves with the best total gain
L9  until a pass has no positive gain
L10 insert an MIV for each net with cells on both tiers
L11 return the tiers, the places, the routes and the MIVs
```

**Shrinking (line L1).** Each cell gets half its area. The die gets half its area, which is the footprint of each tier. The metal width and pitch shrink with the die, so the total track length is unchanged, which is also the track length of the two tiers together. The tool still uses the original RC per unit length, so the extracted parasitics are those of a 3D wire of the same length with the real metal geometry.

**Memory (part of line L2).** A memory macro cannot shrink, because the placer may not put cells over it. The flow splits it into its pins and its blockage. The memory footprint is shrunk to a filler cell while its pins keep their real places, so they still anchor the cells around them. The memories of both tiers are projected onto one plane. A region covered in both tiers becomes a full placement blockage. A region covered in one tier becomes a partial blockage with half the target density, because only the other tier has room there.

**Balance in each bin (lines L5 to L9).** Let $A_b$ be the original cell area in bin $b$ and $a_b$ its largest cell. A split is balanced if, in every bin, the areas of the two tiers differ by at most $\max(\varepsilon A_b,\, 2 a_b)$, which lets each tier be off half the bin area by the largest cell, as in the balance rule of Fiduccia and Mattheyses. The gain of a cell is the number of nets that its move would make uncut minus the number it would make cut. The only change from plain FM, as the paper says, is that balance is checked in each bin and not over the whole chip. Before the split, the paper moves memories to their tiers and moves cells over a partial blockage to the tier without the memory; the code has no memories.

**MIVs and the rest (lines L10 and L11).** The paper does not place MIVs itself. It doubles the metal stack in a technology file, gives each cell a version for each tier with its pins on that tier's metals, puts routing blockages in the via layer over cells, and lets the 2D router connect everything. The vias that the router uses between the two stacks are the MIVs. The router may give one net several MIVs, which the paper keeps. Then each tier is routed with its real design rules, and timing and power are signed off. The code puts one MIV per cut net at the center of the net's bounding box.

The implementation uses a stand-in for the 2D tool at line L2: a [quadratic placement](/quadratic-placement/) with the clique net model, solved by the [Gauss-Seidel method](/gauss-seidel-method/), and then a spreading step that puts the cell of rank $r$ among $n$ at $(r + 1/2)/n$ of the die side in each direction. It does no legalization into rows, no routing, no memory handling and no clock tree. FM scans all cells for the best move, where the original uses bucket lists.

## Example

**Shrinking.** A cell of $2 \times 1$ µm becomes $1.414 \times 0.707$ µm, of area 1 µm². A die of $100 \times 100$ µm becomes $70.7 \times 70.7$ µm, the footprint of each tier. If the placer puts every cell at the same relative place, a net with a half-perimeter wirelength of 30 µm gets $30 \cdot 0.707 = 21.2$ µm, which is 29.3% less.

**Why the balance is per bin.** Take eight cells $a, \ldots, h$ of unit area. After placement, $a, b, c, d$ are in the left bin and $e, f, g, h$ in the right one. The nets are $\{a, b, c, d\}$, $\{e, f, g, h\}$ and $\{d, e\}$. Let $\varepsilon = 0.1$, so in each bin the tiers may differ by at most $\max(0.4, 2) = 2$, and each tier gets one to three of the four cells.

- With balance over the whole chip, the best split puts $a, b, c, d$ on tier 0 and $e, f, g, h$ on tier 1. Only $\{d, e\}$ is cut, so one MIV. But then the left half of tier 0 holds the cell area of the whole left bin of the shrunk die, twice the density that the 2D tool planned, and the left half of tier 1 is empty. The placement is lost.
- With balance per bin, each four-cell net must be split, since no bin may put all four cells on one tier. Line L5 gives $a, c$ and $e, g$ to tier 0 and $b, d$ and $f, h$ to tier 1, which cuts all three nets. FM then moves $d$, which uncuts $\{d, e\}$, so the result cuts 2 nets. Now the left bin has $a, c, d$ on tier 0 and $b$ on tier 1, a difference of 2, which the rule allows. An exhaustive search over all 256 splits confirms that 2 is the least cut that keeps both bins balanced. Each tier has 1 to 3 of the 4 cells of each bin, so its density stays close to what the 2D tool planned.

The test file checks this example.

## Correctness

The [full proof](proofs/correctness.md) shows four things. First, if the placer commutes with scaling, which quadratic placement does because its equations are linear and which the code's rank spreading does too, then the shrunk placement is the 2D placement times $s$, and every half-perimeter wirelength is $s$ times its 2D value: the 29.3% bound of the paper. Second, line L5 leaves every bin balanced, because adding a cell to the lighter tier never makes the difference larger than the largest cell. Third, every FM move keeps its bin balanced and each pass keeps a prefix of nonnegative total gain, so the cut never grows, and the loop ends because each repeated pass lowers the cut by at least one. Fourth, every cut net gets an MIV, so the two tiers implement the same netlist. The proof does not show that the cut is the least one; that problem is NP-hard (see [tier partitioning](/tier-partitioning/)).

## Complexity

Shrinking takes $O(n + p)$ for $n$ cells and $p$ pins. With bucket lists, an FM pass takes $O(p)$ time, so the split takes $O(P p + B)$ for $P$ passes and $B$ bins; the number of passes is small in practice, and at most the number of nets, since each pass but the last lowers the cut. Counting the MIVs takes $O(p)$. The 2D place and route is the cost of the 2D tool, and it dominates. The code is slower than this bound, because it scans all cells for each move ($O(n^2)$ moves and gains per pass, times the net sizes) and runs Gauss-Seidel to a fixed tolerance; for the small tests this does not matter.

## Properties

**What is proved.** With a placer that commutes with scaling, the shrunk wirelength is exactly $1/\sqrt{2}$ times the 2D wirelength. The split is balanced in every bin, its cut is at most the cut of line L5, the loop ends, and each cut net has an MIV. These hold for any netlist and any number of bins.

**What is cited.** Panth et al. (2014, Section 4) report, for OpenSPARC T2 in a 28 nm technology at 1 GHz with timing closed: the shrunk 2D design has 27.05% less wirelength than the 2D design, close to the 29.3% bound (Table 3). The monolithic 3D design has 20.40% less wirelength, 22.33% fewer buffers, 8.03% fewer gates and 15.57% less total power, with zero total silicon area overhead; the face-to-face version has 15.27% less power. With dual-Vt libraries the reduction is 16.08% (Table 4); the abstract rounds the result to 16%. Keeping several MIVs per net instead of one cuts the wirelength of the monolithic design by 8.43%, from 15.61 m to 14.29 m, and its total power by 2.25% (Table 1). The leaf-level clock tree, with the clock backbone on tier 0, uses 29.82% less clock power than one clock tree per tier (Table 2).

**What is measured.** The tests compare the cut of the split with an exhaustive search over all balanced splits, on 200 random designs of 6 to 10 cells in $2 \times 2$ bins (seed 0). The split reaches the least cut on 180 of them and is at most 3 nets worse on the others. On 300 random splits of 4 to 40 cells (seed 1), FM keeps every bin balanced and never cuts more nets than line L5. These are toy designs; they test the code, not the power results of the paper.

## Variants and improvements

- **Multiple MIVs per net.** The paper keeps all MIVs that the router inserts, which shortens the wires. A flow that optimizes timing tier by tier needs one MIV per net, because each MIV becomes an I/O port of a tier with its own timing constraint.
- **Leaf-level 3D clock tree.** The paper builds the clock tree in the shrunk design, fixes the clock buffers and clock gates on tier 0, and lets only the flip-flops move between tiers, so MIVs follow the leaf buffers. The usual way builds one clock tree per tier and joins them with an MIV near the clock source.
- **Face-to-face stacking.** The same flow works for two dies bonded face to face. The metal stack of the upper die is put in reverse order in the technology file, and the bond vias may go over cells, because they use only the top metal.
- **Partitioning for timing or heat.** Other flows split with a cost for critical paths, or put cells of high power next to the heat sink, as in [thermal-driven 3D floorplanning](/thermal-driven-3d-floorplanning/) at the block level.

## When to use it

Use Shrunk-2D when the vertical links are small enough to be used on most nets, which is monolithic 3D or fine-pitch face-to-face bonding, and when you want to reuse a 2D tool and its timing optimization. It does not suit TSV-based stacks: each [TSV](/through-silicon-via/) is large and needs a keep-out zone, so splitting at the gate level would need far more TSVs than the area allows, and partitioning is done at the block level there.

## Pitfalls

- **The 29.3% is a bound for an ideal placer.** Real placers legalize into rows and optimize timing, so the wirelength does not scale exactly. The paper measures 27.05% for the shrunk design and 20.40% for the final monolithic design, after the split and MIV insertion.
- **Global balance.** Balance over the whole chip lets FM put whole regions on one tier, which doubles the density there and breaks the placement. The balance must be checked in each bin.
- **Parasitics.** If the RC per unit length were scaled with the metal width, the extracted RC would be that of the thinner shrunk wires, not of the real ones. The flow keeps the original values on purpose.
- **Memory macros.** Shrinking a memory would let cells overlap it in the tier where it sits. The flow needs the pin and blockage split described above.
- **Timing in each tier.** After the split, each tier is routed again with real rules, and the paper derives timing constraints for each tier from a top-level analysis. Without this step, the sign-off timing of the tiers does not match the shrunk design.
- **Tool flags.** MIVs must not go over cells, which the flow ensures with routing blockages in the via layer; face-to-face vias may.

## Implementations

## History

Earlier gate-level monolithic 3D flows, such as CELONCEL of Bobba et al. (ASP-DAC 2011), placed cells on several tiers but could not handle memory macros, so they did not apply to real designs. Panth, Samadi, Du and Lim gave Shrunk-2D at ISLPED 2014, built on Cadence Encounter for placement and routing and Synopsys PrimeTime for sign-off, with the per-bin FM split, MIV insertion by a 2D router and a leaf-level clock tree. Later gate-level 3D studies often compare with it, and later flows change the way the cells are placed before the split or partition for timing.

## References
