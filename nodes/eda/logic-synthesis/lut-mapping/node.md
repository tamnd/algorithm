---
tag: M3XBV5
kind: problem
slug: lut-mapping
name: LUT mapping
aliases:
- FPGA technology mapping
area: eda/logic-synthesis
level: core
summary: Cover a Boolean network with k-input lookup tables of an FPGA so that the depth or the number of tables is least.
prereqs: [technology-mapping, k-feasible-cut]
see_also: [flowmap, priority-cuts, cut-enumeration, ashenhurst-curtis-decomposition, boolean-matching, retiming, and-inverter-graph, tree-covering-technology-mapping]
sources:
  - paper: "Jason Cong and Yuzheng Ding, FlowMap: an optimal technology mapping algorithm for delay optimization in lookup-table based FPGA designs, IEEE Transactions on Computer-Aided Design 13(1), 1994"
    title: "FlowMap: an optimal technology mapping algorithm for delay optimization in lookup-table based FPGA designs"
    locator: pages 1 to 12; the formulation of LUT mapping with K-feasible cuts, and depth-optimal mapping in polynomial time
  - paper: "Amir H. Farrahi and Majid Sarrafzadeh, Complexity of the lookup-table minimization problem for FPGA technology mapping, IEEE Transactions on Computer-Aided Design 13(11), 1994"
    title: Complexity of the lookup-table minimization problem for FPGA technology mapping
    locator: pages 1319 to 1332; the NP-hardness of mapping with the fewest lookup tables (the range of K is not checked)
  - paper: doi:10.1145/275107.275118
    title: Peichen Pan and Chih-Chang Lin, A new retiming-based technology mapping algorithm for LUT-based FPGAs, FPGA 98
    locator: pages 35 to 42; LUT mapping of sequential circuits together with retiming (general locator)
  - paper: "Alan Mishchenko, Satrajit Chatterjee and Robert Brayton, Improvements to technology mapping for LUT-based FPGAs, IEEE Transactions on Computer-Aided Design 26(2), 2007"
    title: Improvements to technology mapping for LUT-based FPGAs
    locator: area recovery under a depth bound with area flow and exact area, and mapping with structural choices (general locator)
---

LUT mapping is [technology mapping](/technology-mapping/) for FPGAs whose logic blocks are lookup tables (LUTs). A $k$-input LUT is a small memory of $2^k$ bits, so it can compute any function of at most $k$ inputs, and the task is to cover a Boolean network with such tables. In the structural form used by most mappers, each table computes one node of the network from a [$k$-feasible cut](/k-feasible-cut/) of that node, and the tables wired together must compute the outputs. The usual costs are the depth, the largest number of tables on a path from an input to an output, which models the delay, and the number of tables, which models the area. Cong and Ding (1994) showed that a mapping of least depth can be found in polynomial time. Farrahi and Sarrafzadeh (1994) showed that a mapping with the fewest tables is NP-hard to find. Networks that are trees are an easy case for the area.

## In plain words

An FPGA is built from many small tables. Each table has a few inputs, often four or six, and can be set to compute any rule of them. To put a circuit on an FPGA, the circuit must be cut into pieces that each have at most that many inputs, one table per piece.

There are many ways to cut. One way gives short chains of tables from inputs to outputs, which makes the circuit fast. Another way uses fewer tables, which leaves room for more logic. The problem is to pick the cut with the shortest chains, or with the fewest tables, or with the fewest tables among the cuts with the shortest chains.

## Definition

**Input.** A Boolean network $G$, a directed acyclic graph whose sources are the primary inputs (PIs) and whose other nodes are gates, with a set of outputs, and an integer $k \ge 2$. For the depth results below, $G$ is $k$-bounded: every gate has at most $k$ fanins.

**Feasible solutions.** A mapping: a set $S$ of gates, the LUT roots, and for each $v \in S$ a set $C_v$ such that

- every output gate is in $S$;
- $C_v$ is a cut of $v$, a set of nodes that meets every path from a PI to $v$, with $v \notin C_v$ and $|C_v| \le k$;
- every gate of $C_v$ is in $S$.

The LUT of $v$ holds the function of $v$ in terms of the nodes of $C_v$. A node of $G$ can lie inside the cones of several LUTs, so logic may be copied.

**Objective.** One of:

- *depth*: the largest $D(v)$ over the outputs, where $D(u) = 0$ for a PI and $D(v) = 1 + \max_{u \in C_v} D(u)$ for $v \in S$;
- *area*: $|S|$;
- *area under a depth bound*, or depth first and area second.

**Decision version.** Given $G$, $k$ and a number $D$ or $A$, is there a mapping of depth at most $D$, or with at most $A$ LUTs?

A cut that is not minimal can be replaced by a minimal cut inside it without raising the depth or the number of LUTs, so it is enough to consider minimal cuts.

## Variants

- **Objective.** Depth, area, area under a depth bound, power (the switching activity of the LUT outputs), or the number of edges between LUTs, which models routing.
- **Delay model.** Unit delay per LUT, or a delay per LUT and per connection.
- **Copying.** Allowed by default. A *duplication-free* mapping requires the cones of the LUTs to be disjoint.
- **Sequential circuits.** Registers stay in the network, and the mapping is done together with [retiming](/retiming/) to minimize the clock period, as in Pan and Lin (1998).
- **Structural and functional.** The structural form uses cuts of the given network. The functional form allows any network of LUTs that computes the outputs, which can be smaller, and is reached by functional decomposition, such as [Ashenhurst-Curtis decomposition](/ashenhurst-curtis-decomposition/).
- **Structural choices.** The input holds several equivalent structures of the logic, and cuts may come from any of them.
- **Device features.** LUTs of several sizes, LUTs that split into two smaller ones with shared inputs, carry chains and other hard blocks.

## Examples

- **A wide AND.** The AND of 5 inputs with $k = 4$ needs 2 LUTs and has depth 2, since no LUT has 5 inputs. With $k = 5$ it needs 1 LUT.
- **Depth and area together.** Let $k = 3$, with inputs $a, b, c, d$ and gates $p = (a, c)$, $q = (b, p)$, $r = (d, q)$, $s = (b, r)$ and the output $o = (p, s)$. The output depends on 4 inputs, so it needs at least 2 LUTs and depth at least 2. The mapping with $o$ over $\{b, d, p\}$ and $p$ over $\{a, c\}$ reaches both bounds.
- **Depth and area in conflict.** Let $k = 3$, with inputs $a, b, c, d, e$, gates $p = (b, d)$, $q = (a, c)$, $r = (p, q)$, $s = (c, p)$, $t = (e, s)$, and outputs $o_1 = (c, r)$ and $o_2 = (q, t)$. An exhaustive search over all mappings gives least depth 2, and every mapping of depth 2 has at least 5 LUTs, for example $o_1$ over $\{a, c, p\}$, $o_2$ over $\{e, q, s\}$, $p$ over $\{b, d\}$, $q$ over $\{a, c\}$ and $s$ over $\{b, c, d\}$. The fewest LUTs is 4, for example $o_1$ over $\{a, c, p\}$, $o_2$ over $\{a, c, t\}$, $t$ over $\{c, e, p\}$ and $p$ over $\{b, d\}$, and every mapping with 4 LUTs has depth 3.
- **Copying.** In the last example, the mapping of depth 2 computes $q$ in its own LUT and also inside the LUT of $o_1$, whose cone holds $q$ and $r$.

## Known algorithms

- [FlowMap](/flowmap/) (Cong and Ding 1994). Least depth for $k$-bounded networks with unit delay, by a max-flow computation at each node. Exact.
- [Cut enumeration](/cut-enumeration/) with dynamic programming over the cuts of each node. Least depth when all cuts are kept; the area passes are heuristics.
- [Priority cuts](/priority-cuts/) (Mishchenko, Cho, Chatterjee and Brayton 2007). Keeps a few cuts per node; depth first, then area flow and exact area. Heuristic, with the depth of the first pass kept.
- Chortle and its successors (Francis, Rose and Vranesic, from 1990). Area mapping by decomposing the network into trees and packing each tree into LUTs.
- Exact area mapping by integer programming or SAT, with one variable per cut. Exact, with exponential time in the worst case.

## Bounds

**Upper bounds (proved).**

- Depth. For a $k$-bounded network with $n$ nodes and $m$ edges and unit delay, a mapping of least depth is found in $O(k m n)$ time (Cong and Ding 1994). The proof is on the [FlowMap](/flowmap/) page.
- Area on trees. If every gate has at most one fanout and the network has one output, the fewest LUTs are found in polynomial time for a fixed $k$. Proof: in a tree the leaves of a minimal cut of $v$ lie in disjoint subtrees, so the LUTs of a mapping inside the subtree of $v$ number at least $1 + \sum \mathrm{cost}(u)$ over the gate leaves $u$ of $C_v$. So $\mathrm{cost}(v) = \min_{C} \big(1 + \sum_{u \in C \text{ a gate}} \mathrm{cost}(u)\big)$ over the minimal $k$-feasible cuts of $v$, and a node has at most $O(n^k)$ cuts. An exhaustive search over all mappings agreed with this recurrence on 300 random trees (seed 31).
- The decision versions are in NP: a mapping is a certificate of polynomial size, and checking it takes polynomial time.

**Lower bounds (proved, as hardness).**

- Area. Finding a mapping with the fewest LUTs is NP-hard (Farrahi and Sarrafzadeh 1994), for fixed values of $k$ from a small constant on. The exact range of $k$ in their theorem was not checked for this page.
- Area under a depth bound. With a depth bound at least the number of gates, the bound has no effect, so this problem is NP-hard as well.
- Functional form. With the network given as a circuit, even the question whether an output needs no LUT at all is co-NP-hard, since it asks whether the output is a constant or an input.

**Measured.** Nothing on this page. The papers above report depth and LUT counts on benchmark sets such as the MCNC circuits, which are measurements on those sets, not bounds. The page on [priority cuts](/priority-cuts/) gives a toy measurement of the effect of the number of kept cuts.

## Reductions

- **Special case of technology mapping.** Take the library of all functions of at most $k$ inputs, each with area 1 and delay 1, and match by function.
- **Depth to max flow.** Cong and Ding reduce the test "can node $v$ have depth $p$" to a max-flow problem on the cone of $v$ with unit node capacities, by the [max-flow min-cut theorem](/max-flow-min-cut-theorem/).
- **Area to covering.** Area mapping is a binate covering problem with one 0-1 variable per cut, with constraints that each output is a root and each gate leaf of a chosen cut is a root.

## Applications

- **FPGA synthesis.** Every FPGA flow maps logic into the LUTs of the device, followed by packing, placement and routing.
- **Logic optimization.** Mapping into LUTs with small $k$ and reading the result back as a network is used as a restructuring step in synthesis.
- **Emulation and prototyping.** Large designs are mapped into many FPGAs for hardware emulation before the chip is built.

## References
