---
tag: 5EDA9W
kind: definition
slug: timing-graph
name: Timing graph
aliases:
- timing DAG
area: eda/timing-and-verification
level: core
summary: A DAG whose vertices are pins of a circuit and whose edges are cell arcs and nets with delays, cut open at registers, on which timing is computed.
prereqs: [directed-acyclic-graph, boolean-circuit]
see_also: [static-timing-analysis, arrival-and-required-time, setup-and-hold-constraints, false-path, nonlinear-delay-model, topological-sort, critical-path-method, boolean-network]
sources:
  - book: doi:10.1007/978-0-387-93820-2
    title: J. Bhasker and Rakesh Chadha, Static Timing Analysis for Nanometer Designs, A Practical Approach, Springer, 2009
    locator: Chapter 2, STA Concepts (timing arcs, unateness, timing paths, start points and endpoints)
  - book: isbn:9789048195909
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, Springer, 1st edition, 2011
    locator: Chapter 8, Timing Closure, Section 8.2.1, Static Timing Analysis (the timing graph)
  - paper: doi:10.1147/rd.261.0100
    title: Robert B. Hitchcock, Gordon L. Smith and David D. Cheng, Timing analysis of computer hardware, IBM Journal of Research and Development 26(1), 100 to 105, 1982
    locator: the block and path model of the network that the IBM TA program analyzes
---

A timing graph is the directed graph on which [static timing analysis](/static-timing-analysis/) computes the times of a digital circuit. It has a vertex for each pin of each cell and for each port of the design, and an edge for each *cell arc*, from an input pin to an output pin of the same cell, and for each *net arc*, from the driver pin of a net to one of its load pins. Each edge carries a delay. Registers cut the circuit open, so the timing graph of a synchronous circuit with no combinational loop is a [directed acyclic graph](/directed-acyclic-graph/), even though the circuit itself has cycles through its registers.

## Definition

**Netlist.** A gate-level netlist is a set of *cells* (gates and registers), each with input and output *pins*, a set of *ports* (primary inputs and primary outputs), and a set of *nets*. Each net connects one *driver* (an output pin or a primary input) to one or more *loads* (input pins or primary outputs). As a combinatorial object the netlist is a [hypergraph](/hypergraph/) with a net per hyperedge.

**Timing graph.** The timing graph of a netlist is the directed graph $G = (V, E)$ with:

- $V$ = the set of all pins and ports;
- a *net arc* $(u, v)$ for each net and each load $v$ of the net, where $u$ is the driver of the net;
- a *cell arc* $(a, y)$ for each input pin $a$ and output pin $y$ of a combinational cell such that the cell library has a timing arc from $a$ to $y$ (for usual gates, every input to every output);
- for each register, a *clock-to-output arc* from its clock pin $CK$ to its output pin $Q$, and no arc that leaves its data pin $D$.

Each edge $e$ has a delay $d(e)$. In a full model the delay is a pair of numbers, one for a rising and one for a falling output, and a pair of early (minimum) and late (maximum) values. A cell arc also has a *sense*: *positive unate* if a rising input can only cause a rising output (a buffer, an AND input), *negative unate* if it can only cause a falling output (an inverter, a NAND input), and *non-unate* if it can cause both (an XOR input). The delays come from a delay model, for example the [nonlinear delay model](/nonlinear-delay-model/) for cell arcs and the [Elmore delay](/elmore-delay/) for net arcs.

**Start points and endpoints.** A *timing path* is a directed path from a *start point* to an *endpoint*. The start points are the primary inputs and the clock pins of the registers, and the endpoints are the primary outputs and the data pins of the registers. In the graph above, the start points are exactly the vertices with no in-edge and the endpoints are exactly the vertices with no out-edge, once the clock network is cut off at the register clock pins.

**Acyclicity.** Suppose every directed cycle of the netlist passes through the data pin $D$ of some register. Then $G$ is acyclic. *Proof.* Take a directed cycle in $G$. Each of its edges is an arc of a cell or a net of the netlist, so the cycle is also a cycle of the netlist, and it passes through some data pin $D$. But no edge of $G$ leaves a data pin, so the cycle cannot continue after $D$. This is a contradiction. $\square$

**Size.** $|V|$ is the number of pins $P$ plus the number of ports. There is one net arc per load pin, so fewer than $P$ net arcs, and a cell with $k$ inputs and one output has $k$ cell arcs. So $|E| = O(P)$ when each cell has a bounded number of outputs, and the timing graph is linear in the size of the netlist.

## Examples and non-examples

**A three-gate circuit.** Take the primary inputs $a, b, c$, the gates $G1$ with inputs $A, B$ driven by $a$ and $b$, $G2$ with inputs $A, B$ driven by $b$ and $c$, and $G3$ with inputs $A, B$ driven by $G1/Y$ and $G2/Y$, and the primary output $y$ driven by $G3/Y$. The timing graph has 13 vertices: the 4 ports and the 9 gate pins. It has 7 net arcs and 6 cell arcs:

| arc | kind | delay |
| --- | --- | --- |
| $a \to G1/A$, $b \to G1/B$, $c \to G2/B$, $G1/Y \to G3/A$, $G2/Y \to G3/B$, $G3/Y \to y$ | net | 1 |
| $b \to G2/A$ | net | 2 |
| $G1/A \to G1/Y$ | cell | 3 |
| $G1/B \to G1/Y$ | cell | 1 |
| $G2/A \to G2/Y$, $G3/A \to G3/Y$ | cell | 2 |
| $G2/B \to G2/Y$, $G3/B \to G3/Y$ | cell | 3 |

The net of $b$ has two loads, so $b$ has two out-edges. The start points are $a, b, c$ and the only endpoint is $y$. There are 4 timing paths, one for each input pin of $G1$ and $G2$, with delays 8 (from $a$), 6 (from $b$ through $G1$), 9 (from $b$ through $G2$) and 9 (from $c$). For example, the path $b \to G2/A \to G2/Y \to G3/B \to G3/Y \to y$ has delay $2 + 2 + 1 + 3 + 1 = 9$. The [static timing analysis](/static-timing-analysis/) page computes the times on this graph.

**A register in a loop.** A register $R$ whose output $Q$ drives an incrementer whose output drives $D$ forms a cycle $Q \to \dots \to D \to Q$ in the netlist. In the timing graph the edge $D \to Q$ is missing, so the graph has the path $CK \to Q \to \dots \to D$ and no cycle. The path starts at the clock pin and ends at the data pin of the same register, and the [setup and hold constraints](/setup-and-hold-constraints/) of $R$ apply to it.

**Non-example: a combinational loop.** Two NAND gates with the output of each driving an input of the other (a set and reset latch built from gates) form a cycle with no register. Its timing graph has the cycle $N1/A \to N1/Y \to N2/A \to N2/Y \to N1/A$, so it is not a DAG, and arrival times are not defined by the max formula. Timing tools cut such a loop at one arc and report that they did so.

**Non-example: the netlist hypergraph.** The hypergraph with a vertex per cell and a hyperedge per net, used in [graph partitioning](/graph-partitioning-problem/) and placement, has no direction and no delays, and it puts all pins of a cell in one vertex. It loses the difference between the arc $A \to Y$ and the arc $B \to Y$ of the same gate, which can have different delays.

## Related definitions

- **Gate-level timing graph.** A smaller graph has one vertex per net (or per gate output) and one edge per gate input. It merges the net arc and the cell arc into one edge. It is enough when wire delays are zero or are added to the cell delays, and it is the form used in many papers on [retiming](/retiming/) and [gate sizing](/gate-sizing/).
- **Arrival and required times.** The [arrival time](/arrival-and-required-time/) of a vertex is the longest delay from a start point, and the required time is the latest time that meets all endpoint constraints. Both are defined on the timing graph.
- **Activity network.** The [critical path method](/critical-path-method/) uses the same kind of weighted DAG for projects, with tasks in place of arcs. The [DAG longest path](/dag-longest-path/) problem is the common core.
- **Boolean network.** A [Boolean network](/boolean-network/) also has a vertex per gate, but it carries a Boolean function at each vertex and no delays. The timing graph keeps only the structure and the delays, which is why timing analysis can report a [false path](/false-path/).
- **Constraint graph.** For [clock skew scheduling](/clock-skew-scheduling/) and [retiming](/retiming/), the vertices are registers and the edges are setup and hold inequalities between them. That graph is built from the longest and shortest paths of the timing graph, and it can have cycles.

## References
