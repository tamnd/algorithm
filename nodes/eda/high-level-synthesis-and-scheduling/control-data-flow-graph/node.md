---
tag: 6ZTK12
kind: model
slug: control-data-flow-graph
name: Control data flow graph
aliases:
- CDFG
- sequencing graph
area: eda/high-level-synthesis-and-scheduling
level: intro
summary: A graph of the operations of a behavioural description with data edges for values and control edges for branches and loops, the input of high-level synthesis.
prereqs: [control-flow-graph, directed-acyclic-graph]
see_also: [high-level-synthesis, basic-block, phi-function, asap-alap-scheduling, finite-state-machine-with-datapath, path-based-scheduling, sdc-scheduling, speculative-code-motion]
sources:
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 3, Hardware Modeling (the sequencing graph and its hierarchy); Chapter 4, Architectural Synthesis
  - book: isbn:0792391942
    title: Daniel D. Gajski, Nikil D. Dutt, Allen C.-H. Wu and Steve Y.-L. Lin, High-Level Synthesis, Introduction to Chip and System Design, Kluwer, 1992
    locator: the chapters on design representations (control flow, data flow and their combination)
  - paper: doi:10.1145/1146909.1147025
    title: Jason Cong and Zhiru Zhang, An efficient and versatile scheduling algorithm based on SDC formulation, Proceedings of the 43rd Design Automation Conference, 433 to 438, 2006
    locator: Definition 1 (a CDFG as a graph of basic blocks, each holding a data flow graph, with control edges labeled by branch conditions)
---

A control data flow graph (CDFG) is the representation that [high-level synthesis](/high-level-synthesis/) takes as input. It has two levels. The upper level is a [control flow graph](/control-flow-graph/): its nodes are [basic blocks](/basic-block/), and its edges show which block can run after which one, with a branch condition on each edge that leaves a test. The lower level is a data flow graph inside each block: its nodes are operations, such as add, multiply, compare, load and store, and its edges carry values from the operation that makes them to the operations that use them. The data flow graph of one block has no cycle, so it gives a partial order of the operations. Loops appear only at the upper level, as back edges between blocks. De Micheli calls the data flow part a sequencing graph and builds the control part as a hierarchy of sequencing graphs.

## The machine

The CDFG is a representation, not a cost model. Its assumptions are about what the order of operations means.

**Blocks.** The control part is a directed graph $C = (B, F)$ with an entry block and an exit block. An edge $(b, b') \in F$ means that $b'$ can run directly after $b$. When $b$ ends with a test on a value $c$, each edge that leaves $b$ has a condition, such as $c$ or $\lnot c$, and exactly one of these conditions is true in each run. A run of the program follows one path from the entry to the exit.

**Operations.** Each block $b$ holds a data flow graph $G_b = (V_b, E_b)$ with no cycle. Each operation $v$ has a type $\tau(v)$. A data edge $(u, v)$ means that $v$ reads a value that $u$ writes. The graph can also hold order edges that carry no value: between a store and a later load or store that may touch the same address, and between operations on a variable that the program writes twice, when the variables are not renamed. Two operations of one block with no path between them may run in either order or at the same time, and the result is the same.

**Values across blocks.** A value that one block writes and another block reads goes through a variable, which becomes a register in the circuit. When two paths join, the value that a later block reads depends on the path. A [phi function](/phi-function/) at the join, or a multiplexer in the circuit, selects it.

**Sequencing graph.** In De Micheli's form, each graph has a source and a sink that do nothing, so that it has one start and one end. A vertex can also stand for a whole subgraph: a call, a branch whose arms are subgraphs, or a loop whose body is a subgraph. This hierarchy holds the same information as the control flow graph of blocks, but only for structured control flow: one entry and one exit for each branch and loop.

**What the model leaves out.** The CDFG gives no delays, no clock period and no units. These come from a library, and the schedule adds them. It also does not say how many times a loop runs, unless the trip count is a constant or a profile gives it.

## What it counts

The CDFG gives the quantities that bound and guide the schedule.

- **Operations per type.** The count $n_k$ of operations of type $k$ in a block. With $a_k$ units of type $k$ and unit delays, the block needs at least $\lceil n_k / a_k \rceil$ steps.
- **Critical path.** The largest sum of delays on a path of $G_b$, a [longest path in a DAG](/dag-longest-path/). No schedule of the block is shorter. The ASAP start of each operation is the longest path to it, as on the [ASAP and ALAP](/asap-alap-scheduling/) page.
- **Width.** The largest set of operations of $G_b$ with no path between any two of them. It is the most parallel work that one step can use.
- **Live values.** For a cut of a schedule between two steps, the number of values made before the cut and read after it. It is a lower bound on the registers of that schedule.
- **Paths.** The number of paths from the entry to the exit of an acyclic control part. [Path-based scheduling](/path-based-scheduling/) works path by path, so this count is its cost.

Take the code

```
if (a > b) x = a - b; else x = b - a;
y = x * c;
```

It has four blocks: $b_1$ holds the compare $a > b$; $b_2$ holds $a - b$; $b_3$ holds $b - a$; $b_4$ holds a phi that picks $x$ and the multiply $x \cdot c$. The control edges are $b_1 \to b_2$ with condition $a > b$, $b_1 \to b_3$ with condition $a \le b$, $b_2 \to b_4$ and $b_3 \to b_4$. The counts are:

| quantity | value |
|---|---|
| blocks, control edges | 4, 4 |
| paths from $b_1$ to $b_4$ | 2 |
| operations on each path | compare, subtract, multiply |
| critical path, unit delays, blocks in sequence | 3 steps |
| critical path if both subtracts run before the compare is known | 2 steps |

The last row moves the two subtracts into $b_1$, where they do not depend on the compare, and makes the phi a multiplexer. This is [speculative code motion](/speculative-code-motion/). It needs two subtract units or one more step, and it spends energy on a result that is thrown away.

## Relation to other models

- **Control flow graph.** The upper level of a CDFG is the [control flow graph](/control-flow-graph/) of a compiler. The CDFG adds the data flow graph inside each block, which a compiler keeps as a list of instructions.
- **Data flow graph alone.** A program with no branch and no loop has one block, and the CDFG is one data flow graph. Most scheduling pages, such as [force-directed scheduling](/force-directed-scheduling/), work on this case.
- **Synchronous dataflow.** A [synchronous dataflow](/synchronous-dataflow/) graph has actors that fire again and again and edges that are queues with fixed rates. It describes a stream with no control flow. A CDFG describes one run of a program.
- **Finite state machine with datapath.** The CDFG is the input of synthesis and the [FSMD](/finite-state-machine-with-datapath/) is its output. A schedule maps the operations of each block to states, and the control edges become state transitions.
- **Dataflow analysis.** The facts that a compiler finds by [dataflow analysis](/dataflow-analysis/) on the control flow graph, such as live variables and value ranges, carry over to the CDFG and feed [bitwidth analysis](/bitwidth-analysis/).

## Known results in the model

- **Critical path is a lower bound.** In any schedule of a block that meets the data edges, an operation starts after its predecessors end. By induction along a path, the last operation of a path ends no earlier than the sum of the delays on the path. So the latency of the block is at least its critical path, and ASAP scheduling meets this bound when units are not limited.
- **Paths grow as a power of two.** A control part made of $k$ if-then-else statements in sequence has $2^k$ paths from the entry to the exit, because each run chooses one arm in each statement and each choice gives a different path. So any method that lists all paths, such as path-based scheduling, can take time exponential in the size of the CDFG. Loops make the number of paths infinite, so these methods cut the back edges first.
- **Renaming removes false order.** If every variable is written once, as in static single assignment form, the only order edges left between operations on variables are data edges. Order edges through memory stay unless an analysis shows that two addresses never match.
- **Moving across blocks needs dominance.** An operation can move from block $b$ to an earlier block $b'$ only if its operands are ready in $b'$. It runs on every path through $b'$, so if $b'$ does not lie on every path to $b$, the operation runs on paths where the program did not run it. It must then have no side effect. The [dominator tree](/dominator-tree/) of the control part gives the blocks that lie on every path from the entry to $b$.
- **A loop body is a block graph with a back edge.** Scheduling the body alone gives a latency per iteration. Overlapping iterations, as in [SDC modulo scheduling](/sdc-modulo-scheduling/), needs the distances of the edges that cross iterations, which the CDFG must then record.

## References
