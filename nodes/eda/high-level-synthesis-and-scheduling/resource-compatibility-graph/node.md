---
tag: 5PJXVD
kind: definition
slug: resource-compatibility-graph
name: Resource compatibility graph
aliases:
- operation compatibility graph
area: eda/high-level-synthesis-and-scheduling
level: core
summary: A graph whose vertices are operations or variables and whose edges join pairs that may share one unit or register; a binding is a partition into cliques.
prereqs: [control-data-flow-graph, clique, complement-graph]
see_also: [resource-binding, register-binding, clique-cover, perfect-graph, interval-coloring-depth-theorem, circular-arc-coloring, tseng-siewiorek-clique-partitioning, left-edge-algorithm]
sources:
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 6, Resource Sharing and Binding (the compatibility and conflict graphs of operations and of variables)
  - paper: doi:10.1109/TCAD.1986.1270207
    title: Chia-Jeng Tseng and Daniel P. Siewiorek, Automated synthesis of data paths in digital systems, IEEE Transactions on Computer-Aided Design 5(3), 379 to 395, 1986
    locator: the compatibility graphs of operations, of variables and of data transfers, and their partition into cliques
  - book: isbn:9780444515308
    title: Martin Charles Golumbic, Algorithmic Graph Theory and Perfect Graphs, second edition, Elsevier, 2004
    locator: Chapter 8, Interval Graphs (interval graphs are chordal and perfect, and their complements are comparability graphs)
---

A resource compatibility graph is an undirected graph built from a scheduled design in [high-level synthesis](/high-level-synthesis/). Its vertices are the operations of one unit type, or the variables (values) that need storage, and an edge joins two of them when they may use the same functional unit or the same register. Its [complement](/complement-graph/) is the conflict graph. A binding of the vertices to hardware instances is exactly a partition of the compatibility graph into [cliques](/clique/), so the fewest instances is the least number of cliques in such a partition.

## Definition

The model is the one of [resource-constrained scheduling](/resource-constrained-scheduling/). A sequencing graph $G = (V, E)$, part of a [control data flow graph](/control-data-flow-graph/), has a delay $d(v) \ge 1$ in steps for each operation $v$, and a schedule gives each $v$ a start step $s(v)$. There is no chaining. Two operations are *mutually exclusive* when no execution of the design runs both of them, for example because they are on the two arms of one branch.

**Busy set.** A unit that is not pipelined is busy with $v$ in the steps $B(v) = \{s(v), s(v) + 1, \ldots, s(v) + d(v) - 1\}$. A pipelined unit accepts a new operation in each step, so for it $B(v) = \{s(v)\}$.

**Operation compatibility graph.** Fix a unit type $k$, and let $V_k$ be the operations that a unit of type $k$ can execute. The compatibility graph of type $k$ is $G_k = (V_k, E_k)$ with
$$\{u, v\} \in E_k \iff B(u) \cap B(v) = \emptyset \ \text{ or } \ u \text{ and } v \text{ are mutually exclusive}.$$

**Lifetime.** A value $x$ is written at the end of step $w(x)$, the last step of the operation that makes it, and it is last read in step $r(x) > w(x)$. A register holds it in the steps
$$\ell(x) = \{w(x) + 1, \ldots, r(x)\}.$$
All reads in a step see the register contents from the start of the step, as in a [finite state machine with datapath](/finite-state-machine-with-datapath/). So a register that is read for the last time in step $r$ can be written at the end of step $r$. A primary input has $w(x) = 0$ when it is ready before step 1, and a result that leaves the design at the end has $r(x) = \lambda + 1$ for latency $\lambda$.

**Variable compatibility graph.** Its vertices are the values, and $\{x, y\}$ is an edge exactly when $\ell(x) \cap \ell(y) = \emptyset$ or $x$ and $y$ are never live in the same execution.

**Conflict graph.** The conflict graph of either kind is the complement: the same vertices, with an edge exactly when the pair is not compatible.

**Binding as a clique partition.** A binding of type $k$ maps each $v \in V_k$ to one instance of type $k$ so that two operations on one instance are never busy in the same step of any execution. The classes of a binding are cliques of $G_k$, because two members of one class are never busy together. Conversely, every partition of $V_k$ into cliques of $G_k$ is a binding with one instance per clique. In each step of each execution, at most one member of a clique is busy, since any two members are compatible. So the least number of instances of type $k$ is the clique partition number of $G_k$, which is the [chromatic number](/chromatic-number/) of the conflict graph. The same holds for registers and the variable compatibility graph. This is the [clique cover problem](/clique-cover/) on $G_k$.

**Interval and circular-arc structure.** An *interval graph* is the intersection graph of a finite family of intervals of the line: one vertex per interval, and an edge when two intervals meet. For a schedule of straight-line code, with no mutually exclusive pairs, every busy set and every lifetime is a set of consecutive steps, so the conflict graph is an interval graph. Its complement, the compatibility graph, has a *transitive orientation*: direct $u \to v$ when $u$ ends before $v$ starts. If $u \to v$ and $v \to w$, then $u$ ends before $w$ starts, so $u \to w$. A graph with such an orientation is a *comparability graph*. For values that live across the back edge of a loop, the lifetimes are arcs of a circle with one point per step of the loop body, and the conflict graph is a *circular-arc graph*, the intersection graph of a family of arcs of a circle.

**Consequence for straight-line code.** Interval graphs are [chordal](/chordal-graph/) and hence [perfect](/perfect-graph/). Pairwise intersecting intervals share a common point: the largest left end lies in all of them. So the largest clique of the conflict graph is the largest number of operations busy in one step, or of values live in one step, and by the [interval coloring depth theorem](/interval-coloring-depth-theorem/) this many units or registers suffice. Circular-arc graphs are not perfect in general, and coloring them is [NP-complete](/np-complete/), see [circular-arc coloring](/circular-arc-coloring/).

## Examples and non-examples

**A small schedule.** Take unit delays except for $m_4$, and these starts:

| operation | type | start | busy set | note |
|---|---|---|---|---|
| $m_1$ | mul | 1 | $\{1\}$ | |
| $m_2$ | mul | 1 | $\{1\}$ | |
| $m_3$ | mul | 2 | $\{2\}$ | |
| $m_4$ | mul | 3 | $\{3, 4\}$ | delay 2, not pipelined |
| $a_1$ | add | 2 | $\{2\}$ | |
| $a_2$ | add | 3 | $\{3\}$ | |
| $a_3$ | add | 4 | $\{4\}$ | then arm of a branch |
| $a_4$ | add | 4 | $\{4\}$ | else arm of the same branch |

The multiplier graph has the 5 edges $m_1 m_3$, $m_1 m_4$, $m_2 m_3$, $m_2 m_4$ and $m_3 m_4$. Only $m_1 m_2$ is missing, because both are busy in step 1. The adder graph is complete on 4 vertices: $a_3$ and $a_4$ share step 4, but they are mutually exclusive. So the least binding has 2 multipliers, $\{m_1, m_3, m_4\}$ and $\{m_2\}$, and 1 adder. If the branch analysis did not detect that $a_3$ and $a_4$ exclude each other, the edge $a_3 a_4$ would be missing and 2 adders would be needed.

**A variable graph.** Let $x$ be written at the end of step 1 and last read in step 3, $y$ written at the end of step 3 and read in step 4, and $z$ written at the end of step 2 and read in step 4. Then $\ell(x) = \{2, 3\}$, $\ell(y) = \{4\}$ and $\ell(z) = \{3, 4\}$. The only edge is $xy$: $x$ is read in step 3 and $y$ is written at the end of step 3, so they can share a register. Two registers are needed, since $z$ meets both.

**Non-example: the data flow graph.** The edges of the sequencing graph are dependences. They say nothing about sharing. Two operations joined by a dependence are in different steps, so they are often compatible, and two operations with no dependence may be busy in the same step.

**Non-example: one graph for several unit types.** Let $u$ run on an adder or an ALU, $v$ on an ALU or a subtractor, and $w$ on a subtractor or an adder, all in different steps. Every pair can share some type of unit, so a graph with an edge for each such pair is a triangle. But no single unit type runs all three, so the triangle is not a valid binding. The definition fixes the unit type $k$ for this reason.

**Non-example: a loop.** A loop body of 5 steps with five values, where value $i$ is live in steps $i$ and $i + 1$, and value 5 is live in step 5 and in step 1 of the next iteration, gives the conflict graph $C_5$. Every step has 2 live values, but $C_5$ needs 3 colors. This conflict graph is a circular-arc graph that is not an interval graph, and the depth bound fails for it.

## Related definitions

- **Conflict graph.** The complement of the compatibility graph. In a compiler, the conflict graph of the values is the interference graph of the [register allocation problem](/register-allocation-problem/).
- **Clique partition.** A partition of the vertex set into cliques. The fewest cliques is the subject of the [clique cover problem](/clique-cover/), and it equals the chromatic number of the complement, see [graph coloring](/graph-coloring/).
- **Interval graph and comparability graph.** Defined above. The conflict graph of straight-line code is an interval graph, and its compatibility graph is a comparability graph. Both are perfect.
- **Circular-arc graph.** Defined above. It appears for values that cross the back edge of a loop, see [register binding](/register-binding/).
- **Weighted compatibility graph.** An edge weight measures how much interconnect two operations save when they share a unit, for example the number of common operand sources. Binders such as [Tseng-Siewiorek clique partitioning](/tseng-siewiorek-clique-partitioning/) use these weights or the number of common neighbours to choose merges.
- **Bindings that use it.** [Resource binding](/resource-binding/) for operations and [register binding](/register-binding/) for values are clique partition problems on these graphs.

## References
