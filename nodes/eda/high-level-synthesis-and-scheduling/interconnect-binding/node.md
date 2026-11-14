---
tag: 59F7QY
kind: problem
slug: interconnect-binding
name: Interconnect binding
aliases:
- multiplexer minimization
- port assignment
area: eda/high-level-synthesis-and-scheduling
level: advanced
summary: Choose the buses, multiplexers and operand ports that connect registers and units after binding so that the number and width of multiplexer inputs is least.
prereqs: [resource-binding, register-binding, bipartite-graph]
see_also: [odd-cycle-transversal, vertex-cover, weighted-bipartite-matching-binding, tseng-siewiorek-clique-partitioning, resource-compatibility-graph, module-selection, high-level-synthesis, clique-cover]
sources:
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 6, Resource Sharing and Binding (the interconnect that sharing creates, and bus and multiplexer styles)
  - paper: doi:10.1109/TCAD.1986.1270207
    title: Chia-Jeng Tseng and Daniel P. Siewiorek, Automated synthesis of data paths in digital systems, IEEE Transactions on Computer-Aided Design 5(3), 379 to 395, 1986
    locator: the compatibility graph of data transfers and its partition into cliques, one bus per clique
  - paper: "Barry M. Pangrle, On the complexity of connectivity binding, IEEE Transactions on Computer-Aided Design 10(11), 1460 to 1465, 1991"
    locator: whole paper (the NP-completeness of connectivity binding)
  - paper: "Deming Chen and Jason Cong, Register binding and port assignment for multiplexer optimization, Proceedings of the Asia and South Pacific Design Automation Conference, 2004"
    locator: whole paper (binding and operand port choice to reduce multiplexer inputs on FPGAs)
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, Plenum (1972), 85 to 103
    locator: the list of 21 problems (Node cover)
---

Interconnect binding is the last binding step of [high-level synthesis](/high-level-synthesis/). Once every operation has a functional unit and every value has a register, the datapath still needs wires from registers to unit inputs and from unit outputs to registers. Each input that receives data from more than one place needs a multiplexer, or a bus. Interconnect binding chooses the operand ports of commutative operations, the buses and the multiplexers so that the number of multiplexer inputs is least. Even the choice of operand ports alone, for a single adder, is [NP-hard](/np-hard/).

## In plain words

After binding, we know which adder does each addition and which register holds each number. Now the wires must be drawn. An adder input that takes numbers from three different registers needs a switch with three inputs in front of it, and switches cost area and time. For an addition like x plus y, it does not matter which input gets x and which gets y, so we may flip it. Flipping some additions can make each input see fewer registers. Choosing the flips well is a hard puzzle, even for one adder. The same goal applies to the inputs of registers and to shared buses.

## Definition

**Input.** A scheduled and bound design: for each operation $v$, a unit $\beta(v)$ with operand ports $1, \ldots, p$, the registers or units that supply its operands, and the register $\rho$ that receives its result, as on the [resource binding](/resource-binding/) and [register binding](/register-binding/) pages. Some operations are commutative, such as add, multiply, and, or.

**Connections.** A *sink* is an input port of a unit or the input of a register. The *sources* of a sink are the distinct registers, units or primary inputs that ever drive it. A sink with $k \ge 2$ sources needs a $k$-input multiplexer, and a sink with one source is a plain wire.

**Feasible solutions.** For each commutative operation, a choice of which operand goes to which port of its unit. The units, registers and schedule stay fixed.

**Objective.** Minimize the total number of multiplexer inputs, $\sum_{\text{sinks with } k \ge 2} k$. A simpler objective counts all connections, $\sum_{\text{sinks}} k$, including the plain wires.

**Decision form.** Given the bound design and an integer $K$, can the operands be placed so that the cost is at most $K$?

When the bindings are not yet fixed, the problem merges with register and unit binding, and the cost depends on all three choices at once.

## Variants

- **Bus style.** Instead of a multiplexer per sink, data moves over a few shared buses. Two transfers can share a bus if they never happen in the same step, so the fewest buses is a clique partition of the compatibility graph of transfers, see [clique cover](/clique-cover/) and [Tseng-Siewiorek clique partitioning](/tseng-siewiorek-clique-partitioning/).
- **Binding with interconnect cost.** The register binding is chosen so that values from the same unit share registers, as in [weighted bipartite matching binding](/weighted-bipartite-matching-binding/).
- **Multiplexer width and depth.** On FPGAs, a multiplexer with more inputs than a lookup table takes several levels of logic, so the cost of a $k$-input multiplexer grows faster than $k$.
- **Register files with ports.** Values live in multiport register files, and the problem assigns reads and writes to file ports in each step.

## Examples

**One adder, three registers.** Registers $R_1, R_2, R_3$ hold three values, and one adder performs $R_1 + R_2$, $R_2 + R_3$ and $R_3 + R_1$ in three steps. Written as given, port 1 receives $R_1, R_2, R_3$ and port 2 receives $R_2, R_3, R_1$: two 3-input multiplexers, 6 inputs. Flipping the third addition to $R_1 + R_3$ gives port 1 the sources $R_1, R_2$ and port 2 the sources $R_2, R_3$: two 2-input multiplexers, 4 inputs. Fewer is impossible. Each register must reach a port. If each reached only one port, two of the three registers would share a port, but every two of them are added together, so they must reach different ports. Hence some register reaches both ports, and the best is $3 + 1 = 4$.

**A case with nothing to gain.** If the adder only computes $R_1 + R_2$ and $R_1 + R_3$, put $R_1$ on port 1 both times: port 1 has one source and needs no multiplexer, and port 2 has a 2-input multiplexer.

## Known algorithms

- **Clique partitioning of transfers.** For the bus style, the greedy of [Tseng-Siewiorek clique partitioning](/tseng-siewiorek-clique-partitioning/) groups transfers into buses.
- **Operand swapping heuristics.** Visit the commutative operations and flip each one that lowers the count, until no flip helps. Each pass is linear, and the result is a local optimum.
- **Joint binding.** Binders that weigh shared sources, such as the [weighted bipartite matching](/weighted-bipartite-matching-binding/) binder, reduce the interconnect while they bind registers.
- **Integer programming.** A 0-1 variable per operation for its port order and per pair of source and sink gives the optimum for small designs.
- **Odd cycle transversal methods.** For one two-port unit, the problem is exactly [odd cycle transversal](/odd-cycle-transversal/), as shown below, so its exact and parameterized algorithms apply.

## Bounds

Fix one commutative unit with two ports, and let $n$ be the number of distinct registers it reads. Every placement uses between $n$ and $2n$ port connections, since each register reaches one or both ports.

**One two-port unit: the exact count.** Build a graph $G$ on the $n$ registers, with an edge $\{R, R'\}$ for each operation $R + R'$ with $R \ne R'$. A placement of the operands puts each edge's two ends on the two ports. Let $S_1$ and $S_2$ be the registers that reach port 1 and port 2. The connections number $|S_1| + |S_2| = n + |S_1 \cap S_2|$. Then
$$\min |S_1 \cap S_2| = \mathrm{oct}(G),$$
the fewest vertices whose removal leaves a [bipartite graph](/bipartite-graph/). Proof: removing $T = S_1 \cap S_2$ leaves each edge with one end only in $S_1$ and one end only in $S_2$, so $G - T$ is bipartite with sides $S_1 \setminus S_2$ and $S_2 \setminus S_1$. Conversely, let $G - T$ be bipartite with sides $A$ and $B$. Put the $A$ end of each edge on port 1, the $B$ end on port 2, and for an edge inside $T$ choose either way. Then $S_1 \subseteq A \cup T$ and $S_2 \subseteq B \cup T$, so $S_1 \cap S_2 \subseteq T$. The triangle example has $\mathrm{oct} = 1$ and costs $3 + 1$.

## Reductions

**Vertex cover to odd cycle transversal.** Take a graph $H$. Build $G$ from $H$ by adding, for each edge $uv$ of $H$, a new vertex $w_{uv}$ joined to $u$ and $v$. Then $\mathrm{oct}(G)$ equals the least [vertex cover](/vertex-cover/) of $H$. If $C$ covers $H$, then $G - C$ has no edge between two old vertices, and each new vertex is joined only to old ones, so $G - C$ is bipartite. If $T$ breaks every odd cycle of $G$, it meets each triangle $u v w_{uv}$. Replace each $w_{uv} \in T$ by $u$: afterwards $w_{uv}$ has at most one neighbour left and lies on no cycle, so the new set still works and is no larger. It contains an end of each edge of $H$, so it is a cover.

**Interconnect binding is NP-complete.** By the two steps above, given $H$ and $q$, build $G$, make one register per vertex of $G$ and one addition per edge of $G$ on one adder, in different steps. The least number of port connections is $|V(G)| + \mathrm{oct}(G) = |V(G)| + \mathrm{vc}(H)$, so it is at most $|V(G)| + q$ exactly when $H$ has a vertex cover of size $q$. Vertex cover is NP-complete (Karp 1972). The result register of each addition adds the same fixed count in every placement. If $H$ has two disjoint edges, every port of $G$'s adder sees at least two sources in every placement, so every connection is a multiplexer input and the same reduction works for the multiplexer count. A placement is checked in polynomial time, so the decision form is in NP. Pangrle (1991) studied the complexity of the general connectivity binding problem.

## Applications

- **Datapath area.** In FPGA designs, multiplexers can take more area than the shared units, so a binding that saves one adder but adds many multiplexer inputs can lose.
- **Clock period.** A wide multiplexer in front of a unit lengthens the critical path, so reducing multiplexer inputs also helps timing.
- **Bus-based architectures.** Datapaths with a few shared buses use the transfer compatibility graph to decide which transfers ride on which bus.

## References
