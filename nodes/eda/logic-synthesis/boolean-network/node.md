---
tag: 8KEFG7
kind: model
slug: boolean-network
name: Boolean network
aliases:
- multi-level logic network
area: eda/logic-synthesis
level: core
summary: A directed acyclic graph of nodes each with a local Boolean function of its fanins, the model of multi-level logic synthesis.
prereqs: [boolean-function, directed-acyclic-graph, sum-of-products]
see_also: [multi-level-logic-synthesis, boolean-circuit, and-inverter-graph, binary-decision-diagram, kernel-extraction, observability-dont-care, technology-mapping, boolean-equivalence-checking]
sources:
  - paper: doi:10.1109/TCAD.1987.1270347
    title: Robert K. Brayton, Richard Rudell, Alberto Sangiovanni-Vincentelli and Albert R. Wang, MIS, a multiple-level logic optimization system, IEEE Transactions on Computer-Aided Design 6(6), 1987, pages 1062 to 1081
    locator: the Boolean network as the data of MIS, the local functions as sums of products, and the operations that change the network
  - paper: doi:10.1109/5.52213
    title: Robert K. Brayton, Gary D. Hachtel and Alberto L. Sangiovanni-Vincentelli, Multilevel logic synthesis, Proceedings of the IEEE 78(2), 1990, pages 264 to 300
    locator: the definition of the Boolean network, the literal count in factored form as the cost, and the network transformations
  - paper: "Ellen M. Sentovich, Kanwar Jit Singh, Luciano Lavagno, Cho Moon, Rajeev Murgai, Alexander Saldanha, Hamid Savoj, Paul R. Stephan, Robert K. Brayton and Alberto Sangiovanni-Vincentelli, SIS, a system for sequential circuit synthesis, Memorandum UCB/ERL M92/41, Electronics Research Laboratory, University of California, Berkeley, 1992"
    title: SIS, a system for sequential circuit synthesis
    locator: the Boolean network with latches for sequential circuits
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 8, Multiple-Level Combinational Logic Optimization, the models of combinational networks and their transformations
  - paper: doi:10.1002/j.1538-7305.1949.tb03624.x
    title: Claude E. Shannon, The synthesis of two-terminal switching circuits, Bell System Technical Journal 28(1), 1949, pages 59 to 98
    locator: the counting argument that most functions of n variables need large circuits
---

A Boolean network is the model of a combinational circuit that [multi-level logic synthesis](/multi-level-logic-synthesis/) works on. It is a [directed acyclic graph](/directed-acyclic-graph/) whose sources are the primary inputs, and each other node holds a local [Boolean function](/boolean-function/) of the nodes that feed it, usually as a small [sum of products](/sum-of-products/). Some nodes are marked as primary outputs. A node can hold any function, so the model sits between a single sum of products per output (two levels) and a gate-level [Boolean circuit](/boolean-circuit/) (fixed gates). The MIS system of Brayton, Rudell, Sangiovanni-Vincentelli and Wang (1987) made it the common data of logic synthesis, and the later [and-inverter graph](/and-inverter-graph/) is a Boolean network with one kind of node.

## The machine

Here the machine is the network itself: what its parts are, what function it computes, and which steps change it.

**Structure.** A Boolean network $N$ has a finite set of primary inputs $X = \{x_1, \ldots, x_n\}$, a finite set $Y$ of internal nodes, and a directed acyclic graph $G = (X \cup Y, E)$. The fanins of a node $y \in Y$ are $\mathrm{FI}(y) = \{u : (u, y) \in E\}$, and its fanouts are the nodes that it feeds. A primary input has no fanin. A list $Z = (z_1, \ldots, z_m)$ of nodes are the primary outputs. The graph must be acyclic, which makes the circuit combinational.

**Local functions.** Each node $y \in Y$ with $k$ fanins $u_1, \ldots, u_k$ holds a local function $f_y : \{0,1\}^k \to \{0,1\}$. MIS and SIS store $f_y$ as a sum of products over the literals $u_i$ and $\bar{u}_i$, so a node can use each fanin in either phase and no separate inverter node is needed.

**Global functions.** Each node $v$ computes a global function $g_v$ of the primary inputs. For a primary input $g_{x_i}(x) = x_i$, and for an internal node
$$g_y(x) = f_y\big(g_{u_1}(x), \ldots, g_{u_k}(x)\big).$$
This is well defined because $G$ is acyclic: the nodes can be put in [topological order](/topological-sort/), and each $g_y$ is computed after the global functions of its fanins. The network realizes the multiple-output function $x \mapsto (g_{z_1}(x), \ldots, g_{z_m}(x))$. Two networks with the same inputs and outputs are equivalent when they realize the same function.

**Steps of synthesis.** The model does not have one machine step as a model of computation does. In its place, synthesis changes the network by a few operations, each of which keeps the function of every primary output. The names below are those of MIS.

- *Eliminate.* Substitute the local function of a node into its fanouts and delete the node.
- *Decompose and factor.* Split a large local function into several nodes, for example with [algebraic division](/algebraic-division/).
- *Extract.* Make a new node for a divisor that several nodes share, as in [kernel extraction](/kernel-extraction/).
- *Substitute.* Rewrite a node with an existing node as a new fanin.
- *Simplify.* Minimize a local function with the [don't-care conditions](/dont-care-condition/) that the rest of the network allows, such as the [observability don't-cares](/observability-dont-care/).

**Sequential networks.** SIS adds latches. A network with latches may have cycles, but every cycle must pass through a latch. Cutting each latch into a new primary input and a new primary output gives a combinational network again. [Retiming](/retiming/) moves the latches of such a network.

## What it counts

A Boolean network has no single cost. Tools count these:

- **Literals.** The number of literals of all local functions. The SOP count adds the literals of each SOP. The factored-form count writes each local function as a formula of AND and OR over literals and counts its leaves. MIS uses the factored-form count as the estimate of area before technology mapping. For example, $ac + ad + bc + bd$ has 8 SOP literals, and its factored form $(a + b)(c + d)$ has 4.
- **Nodes and edges.** The size of $Y$ and of $E$. For an and-inverter graph, where every node is a 2-input AND, the node count is the main cost.
- **Depth.** The largest number of internal nodes on a path from a primary input to a primary output. It is the estimate of delay before mapping, and the [DAG longest path](/dag-longest-path/) computes it in $O(|X| + |Y| + |E|)$ time.
- **Fanout.** The number of fanouts of a node, a proxy for load and wiring.

These counts only estimate the cost of the final circuit. The real area and delay depend on [technology mapping](/technology-mapping/) and on the layout.

**Example: two networks for a full adder.** The inputs are $a, b, c$. The outputs are the sum $s$ and the carry $co$.

| node | local function | literals |
|---|---|---|
| $t$ | $a \bar{b} + \bar{a} b$ | 4 |
| $s$ | $t \bar{c} + \bar{t} c$ | 4 |
| $u$ | $a b$ | 2 |
| $v$ | $t c$ | 2 |
| $co$ | $u + v$ | 2 |

This network has 5 internal nodes, 14 literals and depth 3, on the path $a \to t \to v \to co$. Eliminating every internal node except the outputs gives the two-level network
$$s = \bar{a} \bar{b} c + \bar{a} b \bar{c} + a \bar{b} \bar{c} + a b c, \qquad co = a b + a c + b c,$$
with 2 nodes, $12 + 6 = 18$ literals and depth 1. Each SOP here is a minimum one: parity has exactly one cover, its four minterms, and a search over all covers of majority with at most three cubes finds none with fewer than 6 literals. So the multi-level network is smaller in literals and deeper. A check of all 8 input vectors confirms that both networks realize the full adder.

## Relation to other models

- **Two-level logic.** A sum of products per output is a Boolean network with one internal node per output, whose fanins are all primary inputs. [Two-level logic minimization](/two-level-logic-minimization/) optimizes this special case.
- **Boolean circuit.** A [Boolean circuit](/boolean-circuit/) is a Boolean network whose local functions come from a fixed basis, such as AND, OR and NOT with two inputs. A network allows any local function. Replacing each local SOP by AND and OR gates turns a network into a circuit with at most three gates per literal: one NOT for a complemented literal, one AND to join it to its cube, and one OR to join a cube to the sum.
- **And-inverter graph and majority-inverter graph.** The [and-inverter graph](/and-inverter-graph/) allows only 2-input AND nodes and puts inverters on the edges. The [majority-inverter graph](/majority-inverter-graph/) uses 3-input majority nodes. Both are Boolean networks with a small fixed basis, which makes hashing and local rewriting simple.
- **Binary decision diagram.** A [binary decision diagram](/binary-decision-diagram/) is also a DAG, but each node is a multiplexer on one variable, and the reduced ordered form is canonical. A Boolean network is not canonical: many networks realize the same function, and the search among them is the task of synthesis.
- **Mapped netlist.** After technology mapping, each node is a cell of a library or a lookup table of an FPGA. The netlist is still a Boolean network, with the local functions fixed by the cells.

## Known results in the model

**Evaluation.** One input vector is simulated in one pass in topological order, in time linear in the number of literals and nodes. On a [word RAM](/word-ram/) with words of $w$ bits, [bit-parallel](/bit-parallelism/) simulation runs $w$ vectors at once with the same number of word operations. So the truth tables of all nodes take $O((L + |Y|) 2^n / w)$ word operations, where $L$ is the number of literals, and the depth takes linear time.

**Equivalence is co-NP-complete.** Deciding whether two networks are equivalent is [co-NP-complete](/co-np-complete/) when the local functions are given as SOPs. It is in [co-NP](/co-np/), since an input vector on which an output differs is a certificate, and it is checked by one simulation of each network. It is co-NP-hard: for a formula $\varphi$ in conjunctive normal form, build one node for each clause, whose SOP is the sum of the literals of the clause, and one output node, whose SOP is the single cube of all clause nodes. This network is equivalent to the constant 0 network exactly when $\varphi$ is unsatisfiable, and the unsatisfiable formulas form a co-NP-complete set by the [Cook-Levin theorem](/cook-levin-theorem/). [Boolean equivalence checking](/boolean-equivalence-checking/) and [SAT](/sat/) solvers decide it in practice.

**Most functions need large networks.** For $n \ge 5$, at most a fraction $2^{n - 2^n / 4}$ of the $2^{2^n}$ functions of $n$ variables are realized by a network of at most $s = \lfloor 2^n / (4n) \rfloor$ nodes with two fanins each. *Proof.* Pad a smaller network with unused nodes, so that it is enough to count networks of exactly $s$ nodes. Each node picks one of 16 local functions of two inputs and two fanins among at most $n + s$ nodes, and one of the $n + s$ nodes is the output. So there are at most $16^s (n + s)^{2s + 1}$ such networks. Since $n + s \le 2^n$, this is at most $2^{4s + (2s + 1) n} = 2^{s(2n + 4) + n}$. For $n \ge 5$, $s(2n + 4) \le 2^n (2n + 4) / (4n) \le \tfrac{3}{4} 2^n$, so at most $2^{\frac{3}{4} 2^n + n}$ functions have such a network, out of $2^{2^n}$. $\square$ Shannon (1949) introduced this counting argument for relay circuits. It shows that small networks are rare, but it names no hard function. The best explicit lower bounds for circuits are far smaller; see [circuit complexity](/circuit-complexity/).

**Optimization is hard.** Finding the smallest network that is equivalent to a given one is at least as hard as deciding equivalence, because the smallest network for a CNF formula $\varphi \wedge z$, with a new variable $z$, has no literal exactly when $\varphi$ is unsatisfiable. The [multi-level logic synthesis](/multi-level-logic-synthesis/) page gives the bounds for the main forms of the problem.

## References
