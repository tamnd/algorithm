---
tag: 54JWX9
kind: problem
slug: soc-test-wrapper-and-tam-design
name: Test wrapper and test access mechanism design
aliases:
- TAM optimization
- SoC test scheduling
- IEEE 1500 wrapper design
area: eda/test-and-diagnosis
level: research
summary: Design core test wrappers, divide the test access width among cores and schedule their tests so the total test time of a system on chip is least.
prereqs: [scan-design, boundary-scan, bin-packing]
see_also: [partition-problem, three-partition, makespan-minimization, strip-packing, rectangle-packing, broadcast-scan, embedded-deterministic-test, np-hard]
sources:
  - paper: doi:10.1023/A:1014916913577
    title: Vikram Iyengar, Krishnendu Chakrabarty and Erik Jan Marinissen, Test wrapper and test access mechanism co-optimization for system-on-chip, Journal of Electronic Testing, Theory and Applications 18(2), 213 to 230, 2002
    locator: the test time of a wrapped core, the wrapper design problem and its NP-hardness, and the joint choice of TAM partition, core assignment and wrapper widths
  - paper: "IEEE Std 1500-2005, IEEE Standard Testability Method for Embedded Core-based Integrated Circuits, IEEE, 2005"
    title: IEEE Standard Testability Method for Embedded Core-based Integrated Circuits, IEEE Std 1500-2005
    locator: the core wrapper, its boundary register, the wrapper instruction register and the serial and parallel test ports
  - book: isbn:9780123705976
    title: Laung-Terng Wang, Cheng-Wen Wu and Xiaoqing Wen, VLSI Test Principles and Architectures, Morgan Kaufmann, 2006
    locator: the chapter on system-on-chip test (wrappers, test access mechanisms and test scheduling)
---

A system on chip is built from cores, such as processors, memories and interfaces, often designed by different teams, each with its own test patterns. To test a core inside the chip, its pins are surrounded by a wrapper of scan cells, as in [boundary scan](/boundary-scan/), and the wrapper is fed through a test access mechanism (TAM), a set of wires from the chip pins to the cores. The chip has only $W$ TAM wires, so three questions must be answered together: how wide a TAM each core gets, how each wrapper turns that width into scan chains, and in what order the cores are tested. The goal is the least total test time. Iyengar, Chakrabarty and Marinissen (2002) stated the problem in this joint form. Even its smallest part, the design of one wrapper, contains the [partition problem](/partition-problem/), so the problem is [NP-hard](/np-hard/).

## In plain words

A chip is made of many blocks, and each block comes with its own tests. The chip has a fixed number of test wires, and each block can be tested faster when it gets more wires, because its test data then flows in more parallel lanes.

We must decide how many wires each block gets, how each block spreads its internal test chains over its wires, and which blocks share wires and so must wait for each other. The blocks that share a group of wires are tested one after another, and the groups run side by side. The chip is done when the slowest group is done. Choosing all of this to finish as early as possible is a packing puzzle.

## Definition

**A core.** Core $i$ has internal scan chains of lengths $\ell_{i,1}, \ldots, \ell_{i,m_i}$, $a_i$ functional inputs, $b_i$ functional outputs, and $p_i$ test patterns. Each input and each output gets one wrapper cell.

**A wrapper of width $w$.** The wrapper builds $w$ wrapper chains. Each internal chain is placed whole in one wrapper chain, and the input cells and output cells are spread over the $w$ chains. The scan-in length $s_{in}$ is the longest wrapper chain counting chains and input cells, and the scan-out length $s_{out}$ is the longest counting chains and output cells. A pattern is shifted in while the previous response is shifted out, so the core needs $s_{in}$ cycles for the first load, $p$ capture cycles, $p - 1$ overlapped shifts of $\max(s_{in}, s_{out})$ cycles and $s_{out}$ cycles for the last unload, which adds up to
$$T_i(w) = \big(1 + \max(s_{in}, s_{out})\big)\, p_i + \min(s_{in}, s_{out}).$$
The wrapper design problem is to choose the wrapper chains that make $T_i(w)$ least for a given $w$. Since extra wires may stay unused, the best $T_i(w)$ never increases with $w$, and it falls in steps.

**The TAM.** In the test bus form, the $W$ wires are split into buses of widths $w_1 + \cdots + w_B = W$. Each core is assigned to one bus and uses its full width, the cores on one bus are tested one after another, and all buses run at once. The test time of the chip is
$$T = \max_{b} \sum_{i \text{ on bus } b} T_i(w_b),$$
and the problem is to choose $B$, the widths, the assignment and the wrappers so that $T$ is least.

**Hardness.** Wrapper design alone is NP-hard. Take a core with chains $\ell_1, \ldots, \ell_m$, no functional inputs or outputs, one pattern and $w = 2$. Then $s_{in} = s_{out} = L$, the larger of the two chain sums, and $T = 2L + 1$. So $T \le \sum_j \ell_j + 1$ exactly when the chains split into two groups of equal sum, which is the [partition problem](/partition-problem/). With $w$ as part of the input the same argument gives [3-partition](/three-partition/), so wrapper design is NP-hard in the strong sense. The assignment of cores to buses is NP-hard too, even when the wrappers are fixed: with two buses of equal width and core times that do not depend on the width, it is again the partition problem.

## Variants

- **Fixed or flexible width.** In the test bus form a core uses one bus for its whole test. In the flexible form, each core gets any width for a time interval, and the schedule is a packing of rectangles of width $w$ and height $T_i(w)$ into a strip of width $W$, a [strip packing](/strip-packing/) problem in which each item has a choice of shapes.
- **Daisy chains.** In the TestRail form, the cores on one TAM are chained in series and can be bypassed one at a time, so the shift length depends on which cores are tested together.
- **Power and conflicts.** Testing two cores at once adds their power, so a schedule may have a power limit, and cores that share a resource, such as a memory and its BIST engine, cannot be tested together.
- **Compression inside the core.** With [broadcast scan](/broadcast-scan/) or [embedded deterministic test](/embedded-deterministic-test/) inside a core, a few TAM wires feed many internal chains, and $T_i(w)$ depends on the compression ratio as well as the width.
- **Hierarchy.** A core may contain cores of its own, with wrappers inside wrappers, as IEEE 1500 allows.
- **Wrapper standard.** IEEE Std 1500 fixes the wrapper cells, a serial port and an instruction register, and leaves the parallel TAM and its width to the designer, which is the part optimized here.

## Examples

Take three cores and $W = 6$ wires.

| core | internal chains | inputs | outputs | patterns |
|---|---|---|---|---|
| A | 32, 24, 16, 8, 8 | 10 | 6 | 50 |
| B | 20, 20, 20 | 4 | 4 | 100 |
| C | none | 12 | 8 | 200 |

The best wrapper at each width gives these test times.

| width | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| A | 5044 | 2548 | 1732 | 1682 | 1682 | 1682 |
| B | 6564 | 4140 | 2322 | 2120 | 2120 | 2120 |
| C | 2608 | 1404 | 1003 | 802 | 802 | 602 |

At width 1, core A has one chain of $88 + 10 = 98$ cells in and $88 + 6 = 94$ out, so $T = 99 \cdot 50 + 94 = 5044$. At width 2 the chains split 48 and 40, the inputs fill them to 49 and 49, the outputs to 48 and 46, and $T = 50 \cdot 50 + 48 = 2548$. From width 4 on, the chain of 32 cells sets $s_{in} = s_{out} = 32$, and more wires do not help core A: $T = 33 \cdot 50 + 32 = 1682$.

| buses | assignment | test time |
|---|---|---|
| one bus of 6 | A, B, C in series | 1682 + 2120 + 602 = 4404 |
| 4 + 2 | B, C on 4; A on 2 | max(2120 + 802, 2548) = 2922 |
| 3 + 3 | A, C on one; B on the other | max(1732 + 1003, 2322) = 2735 |
| 1 + 2 + 3 | C on 1; A on 2; B on 3 | max(2608, 2548, 2322) = 2608 |

The last line is the best over all bus splits of 6 wires and all assignments. It gives core C a single wire: C has the shortest test at width 1, so it can afford the narrowest bus, and the wider buses go to the cores that need them. A lower bound comes from area: core $i$ uses at least $\min_w w\, T_i(w)$ wire-cycles, which is 5044 for A, 6564 for B and 2608 for C, so $T \ge (5044 + 6564 + 2608) / 6 > 2369$.

## Known algorithms

- [Longest processing time first](/longest-processing-time-first/) and [first fit decreasing](/first-fit-decreasing/), for the wrapper chains
- [List scheduling](/list-scheduling/), for cores on buses and for rectangle schedules
- [Mixed integer programming](/mixed-integer-programming/), for assignment and widths
- [Simulated annealing](/simulated-annealing/) and [genetic algorithms](/genetic-algorithm/), for the joint problem
- [Branch and bound](/branch-and-bound/), exact for small instances

## Bounds

- **NP-hard.** Wrapper design is strongly NP-hard and the assignment of cores to buses is NP-hard, as shown in the definition, so the joint problem is too.
- **Lower bounds.** $T \ge \max_i T_i(W)$, since no core can use more than all the wires, and $T \ge \frac{1}{W} \sum_i \min_w w\, T_i(w)$, since the buses hold at most $W$ wire-cycles per cycle.
- **Per-core bound.** $s_{in} \ge \max\big(\max_j \ell_j,\ \lceil (\sum_j \ell_j + a) / w \rceil\big)$, and the same for $s_{out}$ with $b$, so the longest internal chain limits the gain from width. Splitting long internal chains, when the core designer allows it, removes this floor.

## Reductions

- The [partition problem](/partition-problem/) and [3-partition](/three-partition/) reduce to wrapper design, as shown in the definition.
- With all bus widths equal and core times fixed, core assignment is [makespan minimization](/makespan-minimization/) on identical machines.
- The flexible form is [strip packing](/strip-packing/) where each item is one of several rectangles, and a fixed choice of widths makes it [rectangle packing](/rectangle-packing/) into a strip.
- For a core with no functional inputs or outputs, deciding whether a wrapper of width $w$ reaches $s_{in} \le L$ is [bin packing](/bin-packing/): can the chains be packed into $w$ bins of size $L$?

## Applications

- **Core-based chips.** Chips that combine many reused cores plan their test with wrappers and a TAM, so each core keeps its own patterns and the chip test is a schedule of them.
- **Test cost.** Tester time is a large part of the cost of a chip, and the chip-level schedule decides it once the core patterns are fixed.
- **Pin-limited test.** Chips tested with few pins, as in wafer test with low-cost probe cards, have a small $W$, and the width split matters most there.
- **Chiplets and 3D stacks.** Dies stacked or placed side by side in one package need a similar access plan across dies, with a few wires shared by many dies.

## References
