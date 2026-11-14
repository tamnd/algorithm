---
tag: KVYDH6
kind: problem
slug: register-binding
name: Register binding
aliases:
- register sharing in high-level synthesis
area: eda/high-level-synthesis-and-scheduling
level: core
summary: Assign the variables of a scheduled design to registers so that variables with overlapping lifetimes get different registers, with the fewest registers and multiplexers.
prereqs: [resource-compatibility-graph, interval-coloring-depth-theorem, finite-state-machine-with-datapath]
see_also: [left-edge-algorithm, interval-partitioning, circular-arc-coloring, weighted-bipartite-matching-binding, resource-binding, register-allocation-problem, chaitin-register-allocation, chordal-graph-coloring]
sources:
  - paper: doi:10.1145/37888.37920
    title: Fadi J. Kurdahi and Alice C. Parker, REAL, a program for REgister ALlocation, Proceedings of the 24th Design Automation Conference, 210 to 215, 1987
    locator: register allocation by the left-edge algorithm on value lifetimes, and its optimality for designs with no conditional branches
  - paper: doi:10.1137/0601025
    title: M. R. Garey, D. S. Johnson, G. L. Miller and C. H. Papadimitriou, The complexity of coloring circular arcs and chords, SIAM Journal on Algebraic and Discrete Methods 1(2), 216 to 227, 1980
    locator: the main results (coloring circular arcs is NP-complete when the number of colors is part of the input)
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 6, Resource Sharing and Binding (register sharing, variable lifetimes and the left-edge algorithm, and circular-arc graphs for loops)
  - book: isbn:9780444515308
    title: Martin Charles Golumbic, Algorithmic Graph Theory and Perfect Graphs, second edition, Elsevier, 2004
    locator: Chapter 8, Interval Graphs (interval graphs are chordal and perfect)
---

Register binding is the step of [high-level synthesis](/high-level-synthesis/) that maps each value of a scheduled design to a register, so that two values that are live in the same step use different registers. The main goal is the fewest registers, and the second goal is a small interconnect. For straight-line code the lifetimes are intervals, and the least number of registers is the largest number of values live in one step, which the [left-edge algorithm](/left-edge-algorithm/) reaches. When values live across the back edge of a loop, the lifetimes are arcs of a circle and the problem is [NP-complete](/np-complete/).

## In plain words

Each intermediate result must be kept somewhere from the moment it is computed until the last time it is used. Registers are the boxes that keep results. Two results can share a box if one is no longer needed when the other arrives. For code with no loops, each result needs its box during one unbroken stretch of time, and the number of boxes needed is the largest number of results that must be kept at the same moment. A simple scan from left to right reaches that number. Inside a loop, some results are kept from the end of one round into the start of the next. The stretches then wrap around like hours on a clock face, and finding the fewest boxes becomes a hard puzzle.

## Definition

The timing rules are those of the [resource compatibility graph](/resource-compatibility-graph/) page: value $x$ is written at the end of step $w(x)$, last read in step $r(x)$, and held in the steps $\ell(x) = \{w(x) + 1, \ldots, r(x)\}$. A register can be read and written in the same step, as in a [finite state machine with datapath](/finite-state-machine-with-datapath/).

**Input.** A schedule of one block of straight-line code, with no chaining, and a set $X$ of values with integers $w(x) < r(x)$.

**Feasible solutions.** A register binding $\rho : X \to \{1, 2, \ldots\}$ such that $\rho(x) = \rho(y)$ with $x \ne y$ implies $\ell(x) \cap \ell(y) = \emptyset$.

**Objective.** Minimize the number of registers $|\rho(X)|$. A second objective, used among the bindings with the fewest registers, is the interconnect: the number of distinct units that write each register plus the number of distinct unit ports that read it, summed over the registers.

**Decision form.** Given $X$ and an integer $q$, is there a binding with at most $q$ registers?

**Loop form.** A loop body has $C$ steps and runs again and again, and the binding is the same in every iteration. A value written at the end of step $w(x)$ and last read in step $r(x)$ of the same iteration ($r(x) > w(x)$), or of the next iteration ($r(x) \le w(x)$), is held in the steps $\ell(x) = \{w(x) + 1, \ldots, r(x)\}$ taken modulo $C$, with step 0 meaning step $C$ of the previous iteration. Each lifetime is an arc of a circle with $C$ points, and two values conflict when their arcs meet.

[Resource binding](/resource-binding/) is the same kind of problem for operations and units, with busy sets in place of lifetimes. [Interconnect binding](/interconnect-binding/) takes the registers as given and chooses the multiplexers and operand ports.

## Variants

- **Fewest registers, then least interconnect.** Among the bindings with the fewest registers, choose one that shares sources and destinations. [Weighted bipartite matching binding](/weighted-bipartite-matching-binding/) does this step by step.
- **Conditional code.** Values on exclusive branches can share a register even if their steps overlap. The conflict graph is then no longer an interval graph.
- **Loops and pipelines.** In a pipelined loop with initiation interval $II$, a lifetime can be longer than $II$, and copies of one value from different iterations are live together. Unrolling the loop, or renaming the registers in turn, gives each copy its own register.
- **Register files.** Values go to a few multiport register files instead of single registers. Then the number of read and write ports per step is also limited.
- **Compiler register allocation.** A compiler has a fixed number of registers and must spill values to memory when they do not fit. See the [register allocation problem](/register-allocation-problem/) and [Chaitin's allocator](/chaitin-register-allocation/). In synthesis, the number of registers is chosen, so nothing is spilled.

## Examples

**Straight-line code.** Seven values in a schedule of 5 steps:

| value | $w$ | $r$ | lifetime |
|---|---|---|---|
| $a$ | 0 | 2 | $\{1, 2\}$ |
| $b$ | 0 | 1 | $\{1\}$ |
| $c$ | 1 | 3 | $\{2, 3\}$ |
| $g$ | 1 | 3 | $\{2, 3\}$ |
| $d$ | 2 | 5 | $\{3, 4, 5\}$ |
| $e$ | 3 | 4 | $\{4\}$ |
| $f$ | 4 | 5 | $\{5\}$ |

The live values per step number 2, 3, 3, 2 and 2, so at least 3 registers are needed. The left-edge algorithm takes the values in order of the first step of their lifetime and fills one register at a time: register 1 gets $a$ and then $d$, register 2 gets $b$, $c$, $e$ and $f$, and register 3 gets $g$. That is 3 registers.

**A loop where the live count is not enough.** A loop body of 5 steps has five values $x_1, \ldots, x_5$. For $i \le 4$, $x_i$ is written at the end of step $i - 1$ and last read in step $i + 1$. $x_5$ is written at the end of step 4 and last read in step 1 of the next iteration, and $x_1$ is written at the end of step 5 of the previous iteration. The lifetimes are $\{1, 2\}, \{2, 3\}, \{3, 4\}, \{4, 5\}, \{5, 1\}$. Every step has exactly 2 live values, but the conflict graph is the 5-cycle, so 3 registers are needed. If the loop is unrolled twice, the 10 values have lifetimes of 2 consecutive steps on a circle of 10 steps, the conflict graph is the 10-cycle, and 2 registers suffice for two iterations.

## Known algorithms

- **Left-edge algorithm.** Exact for straight-line code, in $O(n \log n)$ time for sorting plus one pass per register. Kurdahi and Parker used it in the REAL program (1987). See the [left-edge algorithm](/left-edge-algorithm/) and [interval partitioning](/interval-partitioning/), which assigns each value to any free register in order of start.
- **Weighted bipartite matching binding.** Reaches the fewest registers for straight-line code, and chooses among the free registers by an [assignment problem](/assignment-problem/) per step to save interconnect. Heuristic for the interconnect. See [weighted bipartite matching binding](/weighted-bipartite-matching-binding/).
- **Clique partitioning.** [Tseng-Siewiorek clique partitioning](/tseng-siewiorek-clique-partitioning/) on the variable compatibility graph. Heuristic: it can need more registers than the live count, even on straight-line code.
- **Chordal coloring.** Exact whenever the conflict graph is [chordal](/chordal-graph/), which covers interval graphs. See [chordal graph coloring](/chordal-graph-coloring/).
- **Circular arcs.** For loops, cut the circle at one step and color the rest as intervals, which gives at most twice the live count, see [circular-arc coloring](/circular-arc-coloring/). For a fixed number of registers, Garey, Johnson, Miller and Papadimitriou give a polynomial test.
- **Integer programming.** Exact for small designs, with any interconnect cost.

## Bounds

Let $L$ be the largest number of values live in one step: $L = \max_t |\{x : t \in \ell(x)\}|$.

**Lower bound.** Every binding uses at least $L$ registers, because the values live in one step pairwise conflict.

**Straight-line code: the bound is exact.** The lifetimes are intervals of consecutive steps, so the conflict graph is an interval graph. Pairwise intersecting intervals share a step, so the largest clique has $L$ values. The [interval coloring depth theorem](/interval-coloring-depth-theorem/) shows that intervals of depth $L$ can be colored with $L$ colors, and the left-edge algorithm finds such a coloring. Proof for left-edge: it sorts the values by the first step of their lifetime and fills registers one at a time, adding a value when its first step is after the last step of the value placed last. Let $x$ be the first value of the last register $k$ it opens, with first step $t$. In each register $j < k$, $x$ was skipped, so the value $y_j$ placed last in $j$ at that moment ends at step $t$ or later. It comes before $x$ in the order, so it starts at step $t$ or earlier, and it is live in step $t$. The values $y_1, \ldots, y_{k-1}$ are distinct, and with $x$ they give $k$ values live in step $t$, so $k \le L$. So the least number of registers is exactly $L$, and finding it takes polynomial time.

**Loops.** The least number lies between $L$ and $2L$: the values live in one fixed step take at most $L$ registers, and the rest are intervals once the circle is cut at that step, so $L$ more registers suffice. The 5-cycle example has $L = 2$ and needs 3.

## Reductions

**Straight-line code to interval coloring.** A binding is a proper coloring of the interval graph of the lifetimes, and the reverse holds too. So straight-line register binding is the coloring of an interval graph, see [graph coloring](/graph-coloring/).

**Circular-arc coloring to loop register binding.** Garey, Johnson, Miller and Papadimitriou (1980) proved that deciding whether a family of circular arcs can be colored with $q$ colors is NP-complete when $q$ is part of the input. Each family of $n$ arcs can be drawn with endpoints among $C = 2n$ points of a circle, keeping the same pairs of meeting arcs. Take such a family. An arc that covers the whole circle meets every other arc and needs a color of its own, so remove each such arc and lower $q$ by one. For each other arc $\{a, a + 1, \ldots, b\}$ taken modulo $C$, make a value written at the end of step $a - 1$ (step $C$ of the previous iteration when $a = 1$) and last read in step $b$, in the same iteration if $b \ge a$ and in the next one if $b < a$. Its lifetime is exactly the arc. Two values conflict exactly when their arcs meet, so the loop needs at most $q$ registers exactly when the arcs can be colored with $q$ colors. The construction takes polynomial time, and a binding is checked in polynomial time. So loop register binding is NP-complete.

**To compiler register allocation.** Register binding of straight-line code is register allocation without spills on an interval interference graph, see the [register allocation problem](/register-allocation-problem/).

## Applications

- **Datapath synthesis.** Every high-level synthesis flow binds values to registers after scheduling, often with the left-edge algorithm as the first step.
- **Loop pipelines.** Values that cross iterations in DSP loops need the circular-arc view, or unrolling to reach the live count.
- **Power.** A register that holds fewer values toggles less, so some binders trade registers for lower switching activity.

## References
