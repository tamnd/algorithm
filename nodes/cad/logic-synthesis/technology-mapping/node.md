---
tag: FYE7QJ
kind: problem
slug: technology-mapping
name: Technology mapping
aliases:
- library binding
area: cad/logic-synthesis
level: core
summary: Cover a technology-independent network with gates of a cell library or with lookup tables, minimizing area, delay or power.
prereqs: [boolean-network, directed-acyclic-graph]
see_also: [tree-covering-technology-mapping, lut-mapping, boolean-matching, instruction-selection-problem, multi-level-logic-synthesis, gate-sizing, static-timing-analysis, and-inverter-graph]
sources:
  - paper: doi:10.1145/37888.37940
    title: "Kurt Keutzer, DAGON: technology binding and local optimization by DAG matching, Proceedings of the 24th ACM/IEEE Design Automation Conference, 1987"
    locator: pages 341 to 347; the subject graph, the pattern graphs of the library, and covering as the formulation of the problem
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: chapter 10, cell-library binding (general locator, not checked)
  - paper: doi:10.1109/TCAD.2006.882484
    title: "Satrajit Chatterjee, Alan Mishchenko, Robert Brayton, Xinning Wang and Timothy Kam, Reducing structural bias in technology mapping, IEEE Transactions on Computer-Aided Design 25(12), 2006"
    locator: pages 2894 to 2903; the dependence of a cover on the structure of the subject graph, and mapping over several structures at once
  - paper: "Amir H. Farrahi and Majid Sarrafzadeh, Complexity of the lookup-table minimization problem for FPGA technology mapping, IEEE Transactions on Computer-Aided Design 13(11), 1994"
    title: Complexity of the lookup-table minimization problem for FPGA technology mapping
    locator: pages 1319 to 1332; the NP-hardness of covering a network with the fewest lookup tables
---

Technology mapping turns a circuit that is described without regard to the target technology, a [Boolean network](/boolean-network/) or an [and-inverter graph](/and-inverter-graph/), into a circuit built from the parts that the technology offers. For a chip made of standard cells, the parts are the gates of a cell library, each with a function, an area and a delay. For an FPGA, the parts are lookup tables (LUTs) with $k$ inputs, each of which can hold any function of $k$ inputs; that case has its own page, [LUT mapping](/lut-mapping/). The mapped circuit must compute the same outputs, and the goal is the least area, the least delay, the least power, or one of them under a bound on another. In the usual formulation, introduced by Keutzer in 1987, the circuit is first written in a few base gates as a subject graph, and the mapping is a cover of the subject graph by matches of library gates. Many forms of the problem are NP-hard, and only some special cases, such as trees, have polynomial exact algorithms.

## In plain words

A circuit design is first written in a simple, neutral form, with many small gates. A factory, though, offers a fixed set of gates, some small and simple, some larger ones that do more work in less area. Technology mapping rebuilds the design from the factory's gates.

The rebuilt circuit must do exactly what the design does. Among all ways to rebuild it, pick one that takes the least room on the chip, or one that makes the signals arrive soonest, or one that uses the least power. For an FPGA, the parts are small memories that can act as any gate with a few inputs.

## Definition

**Input.** A subject graph $G$: a directed acyclic graph whose sources are the primary inputs and whose other nodes are base gates, for example 2-input NAND gates and inverters, with a set of outputs. A library $\mathcal{L}$ of gates. Each gate $g$ has a function over its inputs, an area $a(g) \ge 0$, and a delay model, for example a fixed delay $d(g)$. Each gate is described by one or more pattern graphs over the same base gates, or by its function alone.

**Feasible solutions.** A cover of $G$: a set of matches, where a match of $g$ at node $v$ is a set of nodes of $G$ rooted at $v$ whose function, as a function of the match inputs, is the function of $g$ under some assignment of the inputs of $g$. Every output gate must be the root of a match, and every input of a match must be a primary input or the root of a match. A match may cover a node that is also covered by another match, which copies its logic. The matched gates, wired as their inputs say, form the mapped circuit, which computes the outputs of $G$.

**Objective.** One of:

- *area*: the sum of $a(g)$ over the matches;
- *delay*: the largest arrival time at an output, where the arrival time at a match root is the largest arrival time of an input plus the delay of the gate, and 0 at the primary inputs;
- *power*, or *area under a delay bound*, or *delay under an area bound*.

**Decision version.** Given $G$, $\mathcal{L}$ and a number $A$, is there a cover of area at most $A$? The same with delay at most $T$.

A match is *structural* if the covered nodes have the shape of a pattern graph of $g$, and *Boolean* if only the function of the covered region is compared with the function of $g$, as in [Boolean matching](/boolean-matching/). The structural form depends on the subject graph: a different decomposition of the same functions can allow different covers.

## Variants

- **Target.** A cell library, or $k$-input LUTs, where every function of at most $k$ inputs is a gate of area 1. The second is [LUT mapping](/lut-mapping/).
- **Tree covers.** Cut $G$ at every node with more than one fanout and allow only matches that stay inside one tree, so that no logic is copied. This is the setting of [tree covering](/tree-covering-technology-mapping/).
- **Matching.** Structural matches against pattern graphs, or Boolean matches of cut functions against cell functions under permutation and negation of the inputs.
- **Delay model.** Unit delay, a fixed delay per gate, or a delay that depends on the load that a gate drives. The last couples mapping with [gate sizing](/gate-sizing/) and [static timing analysis](/static-timing-analysis/).
- **Several structures.** The input holds several subject graphs for the same functions, or one graph with choice nodes, and a cover may use any of them. Chatterjee, Mishchenko, Brayton, Wang and Kam (2006) call the dependence on one structure the structural bias.
- **Sequential mapping.** Registers stay in the graph, and mapping is done together with [retiming](/retiming/).
- **Functional form.** Ask for any circuit of library gates that computes the outputs, not a cover of a given $G$. This is the setting of [exact synthesis](/exact-synthesis/), and it is much harder.

## Examples

All areas below are made-up values for a toy library: INV 2, NAND2 3, AND2 4, AOI21 4 and AOI22 5. AND2 is INV(NAND($x$, $x$)), AOI21 is INV(NAND(NAND($x$, $x$), INV($x$))) and AOI22 is INV(NAND(NAND($x$, $x$), NAND($x$, $x$))).

- **One large gate.** $o = \overline{ab + cd}$ as $\mathrm{INV}(\mathrm{NAND}(\mathrm{NAND}(a, b), \mathrm{NAND}(c, d)))$. Covers: three NAND2 and one INV, area 11; two NAND2 and one AND2, area 10; one AOI22, area 5. The least area is 5.
- **Copying pays.** $n = \mathrm{NAND}(a, b)$ feeds $o_1 = \mathrm{INV}(n)$ and $o_2 = \mathrm{INV}(\mathrm{NAND}(n, \mathrm{INV}(c)))$. A cover that does not copy $n$ needs NAND2 for $n$, INV for $o_1$ and AND2 over $n$ and $\mathrm{INV}(c)$ for $o_2$, with an INV for $\mathrm{INV}(c)$, area 11. A cover that copies $n$ uses AND2 over $a, b$ for $o_1$ and AOI21 over $a, b, c$ for $o_2$, area 8.
- **LUTs.** The AND of 5 inputs, with $k = 4$, needs 2 LUTs and has depth 2 at best, since one LUT has only 4 inputs. With $k = 5$ it needs 1 LUT.
- **Structure matters.** Add NAND3 with area 4, pattern NAND($x$, INV(NAND($x$, $x$))), and NAND4 with area 5, pattern NAND(INV(NAND($x$, $x$)), INV(NAND($x$, $x$))). The function $\overline{abcd}$ written as a balanced tree, $\mathrm{NAND}(\mathrm{INV}(\mathrm{NAND}(a, b)), \mathrm{INV}(\mathrm{NAND}(c, d)))$, is one NAND4 match, area 5. Written as a chain, $\mathrm{NAND}(\mathrm{INV}(\mathrm{NAND}(\mathrm{INV}(\mathrm{NAND}(a, b)), c)), d)$, the NAND4 pattern does not fit, and the best structural cover is NAND3 over AND2, area 8. The function is the same, and only the shape differs.

## Known algorithms

- [Tree covering technology mapping](/tree-covering-technology-mapping/) (Keutzer 1987). Exact for tree covers of the given subject graph, in time linear in the graph for a fixed library, for area and for a fixed delay per gate.
- [FlowMap](/flowmap/). Exact for the least depth in LUT mapping, in polynomial time.
- [Cut enumeration](/cut-enumeration/) with dynamic programming over the cuts of each node, and [priority cuts](/priority-cuts/). Cut-based mappers for LUTs, and with [Boolean matching](/boolean-matching/) for cells. The area passes are heuristics.
- Exact covering by integer programming or SAT, with one variable per match. Exact, with exponential time in the worst case.
- The methods of compiler code generation for the same covering problem, such as [BURS](/burs/) and [maximal munch](/maximal-munch/), from the [instruction selection problem](/instruction-selection-problem/).

## Bounds

**Upper bounds (proved).**

- Tree covers. For area, and for delay with a fixed delay per gate, the best tree cover of a subject graph is found in time linear in the graph for a fixed library, by dynamic programming over each tree.
- Depth of LUT mappings. For a $k$-bounded network and unit delay per LUT, a mapping of least depth is found in polynomial time (Cong and Ding 1994, see [FlowMap](/flowmap/)).
- The decision version with structural matches is in NP: a cover is a certificate of polynomial size, and its area and delay are checked in polynomial time.

**Lower bounds (proved, as hardness).**

- Covering a network with the fewest $k$-input LUTs is NP-hard (Farrahi and Sarrafzadeh 1994). So area-optimal mapping with copying allowed is NP-hard for that library, which has every function of $k$ inputs.
- For cell libraries, area-optimal covering of a general DAG is stated to be NP-hard in the mapping literature. This page does not give a proof or a precise source for a particular library.
- With Boolean matches, a single match test contains a co-NP-hard question when the functions are given as circuits, see [Boolean matching](/boolean-matching/). With functions given as truth tables of a few inputs, as in practice, the test is fast.
- In the functional form, with the network given as a circuit, even the question whether an output needs no gate at all is co-NP-hard, since it asks whether the output is a constant or an input.

**Measured.** Mappers are compared on benchmark circuits such as the MCNC and ISCAS sets, and the papers report area and delay on those sets. These are measurements on those sets, not bounds. The second example above shows the kind of gap that tree covers can have on one small graph.

## Reductions

- **LUT mapping is a special case.** Take the library of all functions of at most $k$ inputs, each with area 1 and delay 1, with Boolean matches.
- **To set covering.** A DAG cover is a covering problem with one 0-1 variable per match and constraints that each output is covered and each input of a chosen match is covered, a binate covering problem.
- **Instruction selection.** Selecting machine instructions for the expression DAG of a program is the same covering problem, with instructions as the library and their cost as the area.
- **Boolean matching as a subproblem.** Each Boolean match test is an instance of [Boolean matching](/boolean-matching/).

## Applications

- **Standard cell synthesis.** Every ASIC flow maps the optimized logic into the cells of a library before placement.
- **FPGA synthesis.** Every FPGA flow maps the logic into LUTs, carry chains and other blocks of the device.
- **Resynthesis.** Mapping into a library of small gates, then reading the mapped circuit back as a network, is also used as a logic optimization step.

## References
