---
tag: Q2BS5K
kind: model
slug: nonlinear-delay-model
name: Nonlinear delay model
aliases:
- NLDM
- table lookup delay model
area: cad/timing-and-verification
level: core
summary: A cell delay model that gives delay and output slew by interpolation in tables indexed by input slew and output load.
prereqs: [timing-graph, bilinear-interpolation]
see_also: [static-timing-analysis, arrival-and-required-time, setup-and-hold-constraints, elmore-delay, rc-tree, logical-effort, statistical-static-timing-analysis, gate-sizing]
sources:
  - book: doi:10.1007/978-0-387-93820-2
    title: J. Bhasker and Rakesh Chadha, Static Timing Analysis for Nanometer Designs, A Practical Approach, Springer, 2009
    locator: Chapter 3, Standard Cell Library (timing arcs, the non-linear delay model tables, their interpolation and the threshold settings)
  - paper: "Jessica Qian, Satyamurthy Pullela and Lawrence T. Pillage, Modeling the effective capacitance for the RC interconnect of CMOS gates, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 13(12), 1526 to 1535, 1994"
    locator: the effective capacitance that replaces an RC load by one capacitor for a table of capacitive loads
---

The nonlinear delay model (NLDM) is the standard way in which a cell library gives the timing of each logic cell to a [static timing analysis](/static-timing-analysis/) tool. For each timing arc of a cell, from an input pin to an output pin and for a rising or a falling output, the library stores two tables: the delay and the output slew (the transition time of the output). Both are indexed by the input slew and the output load capacitance. The tool finds a value by [bilinear interpolation](/bilinear-interpolation/) between the four nearest table points. The tables come from circuit simulation of each cell at a grid of slews and loads (characterization), so the model holds whatever non-linear shape the simulation finds. It does not hold the physics of the cell.

## The machine

**Cells and arcs.** A cell is a gate or a register from the library, such as `NAND2_X1`. A *timing arc* is a pair (input pin, output pin) with a *sense*: positive unate (a rising input can only make the output rise), negative unate (a rising input can only make the output fall) or non-unate (both, as in XOR). Each arc is a cell arc of the [timing graph](/timing-graph/).

**Tables.** For each arc and each output edge (rise and fall), the library has a *delay table* and a *slew table*. Each table has an index $s_1 < s_2 < \cdots < s_m$ of input slews, an index $c_1 < c_2 < \cdots < c_n$ of output loads and an $m \times n$ array of values. In the Liberty format the tables look like this, with times in ns and capacitances in pF:

```text
lu_table_template (delay_3x3) {
  variable_1 : input_net_transition;
  variable_2 : total_output_net_capacitance;
  index_1 ("0.1, 0.4, 1.0");
  index_2 ("0.01, 0.04, 0.10");
}
cell_rise (delay_3x3) {
  values ("0.10, 0.16, 0.28", \
          "0.15, 0.22, 0.35", \
          "0.22, 0.31, 0.47");
}
```

The tables `cell_rise` and `cell_fall` hold delays, and `rise_transition` and `fall_transition` hold output slews. Setup and hold checks of a register are tables of the same kind, indexed by the data slew and the clock slew.

**Thresholds.** The library states how it measures time. The delay is the time from the input crossing a threshold, usually 50 percent of the supply, to the output crossing its threshold. The slew is the time between two thresholds, for example 10 and 90 percent or 30 and 70 percent, sometimes scaled by a derating factor. A tool that mixes libraries with different thresholds must convert them.

**Lookup.** For an input slew $s$ and a load $c$, find the cell with $s_i \le s \le s_{i+1}$ and $c_j \le c \le c_{j+1}$. Let $t = (s - s_i)/(s_{i+1} - s_i)$ and $u = (c - c_j)/(c_{j+1} - c_j)$. With $D_{ij}$ the table value at $(s_i, c_j)$, the model gives
$$ D(s, c) = (1-t)(1-u) D_{i,j} + (1-t) u \, D_{i,j+1} + t (1-u) D_{i+1,j} + t u \, D_{i+1,j+1}. $$
If $s$ or $c$ is outside the index range, the same formula with the first or the last cell gives a linear extrapolation, with $t$ or $u$ outside $[0, 1]$.

**Use in a timing run.** At a cell arc from pin $a$ to pin $z$, the tool takes the slew at $a$ and the load at $z$, which is the sum of the pin capacitances of the fanout cells and the capacitance of the wire. It looks up the delay of the arc and the slew at $z$. The slew at $z$ then goes, through the net, to the inputs of the next cells. So slews travel forward through the timing graph with the arrival times.

## What it counts

The model gives two numbers for each arc, edge and operating point: a delay, which becomes the weight of the cell arc in the timing graph, and an output slew, which is an input of the next lookups. The load is one number, a lumped capacitance. Each table belongs to one corner of process, supply voltage and temperature, so a run at several corners uses several libraries.

**Worked lookup.** With the table above, take $s = 0.25$ and $c = 0.07$. Then $i$ and $j$ are the first and the second cell, $t = (0.25 - 0.1)/0.3 = 1/2$ and $u = (0.07 - 0.04)/0.06 = 1/2$, so the delay is the mean of the four corners, $(0.16 + 0.28 + 0.22 + 0.35)/4 = 0.2525$ ns. At a table point, such as $(0.4, 0.04)$, the model returns the table value $0.22$ exactly.

**Cost.** A lookup is a binary search in each index, $O(\log m + \log n)$ comparisons, and a constant number of operations. A timing run makes a constant number of lookups per cell arc, so with the NLDM the forward pass of STA stays linear in the size of the timing graph, apart from these searches.

## Relation to other models

- **Linear delay model.** Older libraries used $d = d_0 + k_s s + R \, c$: an intrinsic delay, a slew term and a drive resistance times the load. The NLDM is a table of such values, so it can express the curvature that the linear model misses. A table of a cell whose delay is exactly of the form $a + b s + e c + f s c$ is exact under the NLDM.
- **Logical effort.** [Logical effort](/logical-effort/) writes the delay of a gate as $g h + p$, linear in the load and with no slew. It is a model for design by hand. The NLDM is a model for sign-off timing.
- **Interconnect models.** The NLDM covers the cell. The delay of the wire after it comes from an [RC tree](/rc-tree/) model, for example the [Elmore delay](/elmore-delay/) or a reduced-order model. A resistive wire also shields part of its capacitance from the driver, so a lumped load is pessimistic. The *effective capacitance* of Qian, Pullela and Pillage (1994) is a single capacitor that gives the driver the same delay as its real RC load, so that the tables can still be used.
- **Current source models.** For small technologies, the composite current source (CCS) model and the effective current source model (ECSM) store the output current or voltage waveform instead of two numbers, and handle RC loads and noise better. They are extensions of the same table idea.
- **Statistical libraries.** Tables of the standard deviation of the delay next to the mean delay feed [statistical static timing analysis](/statistical-static-timing-analysis/).

## Known results in the model

These are facts about bilinear interpolation of the tables. They are proved below. How well the tables match the silicon is a matter of measurement, not of proof.

**Exactness.** The interpolant is exact at the table points and on every function $a + b s + e c + f s c$, because the formula is linear in $t$ and in $u$ separately.

**Error bound.** Let the true delay $f(s, c)$ have continuous second derivatives in a table cell of size $h_s \times h_c$. Then, inside the cell,
$$ |f - D| \le \frac{h_s^2}{8} \max |f_{ss}| + \frac{h_c^2}{8} \max |f_{cc}|. $$
*Proof.* Let $I_s$ and $I_c$ be linear interpolation in $s$ and in $c$ at the cell edges. Then $D = I_s I_c f$ and $f - D = (f - I_s f) + I_s (f - I_c f)$. Linear interpolation of a function $g$ on an interval of length $h$ has error at most $h^2 \max |g''| / 8$, and $I_s$ does not increase the maximum of the absolute value, since it takes convex combinations. $\square$ So the error is small where the delay is close to linear, and a library puts more index points where the curvature is large, often at small slews and loads.

**Monotonicity inside the table.** If the table values are non-decreasing along each index, then $D(s, c)$ is non-decreasing in $s$ and in $c$ in the whole range of the table. *Proof.* In one cell, $\partial D / \partial s = \big((1-u)(D_{i+1,j} - D_{i,j}) + u (D_{i+1,j+1} - D_{i,j+1})\big)/(s_{i+1} - s_i) \ge 0$, and in the same way for $c$. $D$ is continuous across cell edges, so it is non-decreasing on each line in the table. $\square$ The example table has this property.

**Slew merging is safe under monotonicity.** At a pin with several incoming arcs, STA keeps the latest arrival time and the largest slew, which can come from different arcs. If all delays and output slews of the library, and the slew at the end of each wire, are non-decreasing in the input slew, then this gives an upper bound on all later arrival times. *Proof.* By induction in topological order: each later lookup gets an input slew at least as large as the real one, so its delay and its output slew are at least as large. $\square$ For the early mode the tool keeps the smallest slew instead.

**Extrapolation is not safe.** Outside the table the formula is linear extrapolation, and none of the facts above hold. For example, if the rise slew at a fixed input slew is $0.02$ ns at load $0.01$ pF and $0.10$ ns at $0.04$ pF, linear extrapolation to load 0 gives $0.02 - 0.08/3 = -1/150 \approx -0.0067$ ns, a negative slew. Extrapolation in the other direction can be too small or too large, depending on the curvature. Tools warn when a lookup leaves the table, and a good library has index ranges that cover the real slews and loads of the design.

## References
