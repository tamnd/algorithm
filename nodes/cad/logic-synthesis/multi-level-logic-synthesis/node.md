---
tag: 9VJ3K1
kind: problem
slug: multi-level-logic-synthesis
name: Multi-level logic synthesis
aliases:
- multi-level logic optimization
area: cad/logic-synthesis
level: core
summary: Restructure a Boolean network into an equivalent one with fewer literals, less depth or less power, by factoring, extraction and don't-care optimization.
prereqs: [boolean-network, sum-of-products, two-level-logic-minimization]
see_also: [kernel-extraction, observability-dont-care, and-inverter-graph, aig-rewriting, aig-balancing, ashenhurst-curtis-decomposition, technology-mapping, exact-synthesis]
sources:
  - paper: doi:10.1109/TCAD.1987.1270347
    title: Robert K. Brayton, Richard Rudell, Alberto Sangiovanni-Vincentelli and Albert R. Wang, MIS, a multiple-level logic optimization system, IEEE Transactions on Computer-Aided Design 6(6), 1987, pages 1062 to 1081
    locator: the optimization of a Boolean network for literal count and its operations of factoring, extraction, substitution and simplification
  - paper: doi:10.1109/5.52213
    title: Robert K. Brayton, Gary D. Hachtel and Alberto L. Sangiovanni-Vincentelli, Multilevel logic synthesis, Proceedings of the IEEE 78(2), 1990, pages 264 to 300
    locator: the statement of the multilevel problem, its cost functions, and the algebraic and Boolean methods
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 8, Multiple-Level Combinational Logic Optimization
  - paper: doi:10.1016/j.jcss.2010.06.011
    title: David Buchfuhrer and Christopher Umans, The complexity of Boolean formula minimization, Journal of Computer and System Sciences 77(1), 2011, pages 142 to 153
    locator: the Sigma_2^p-completeness under Turing reductions of the Minimum Equivalent Expression problem
  - paper: doi:10.1145/335305.335314
    title: Valentine Kabanets and Jin-Yi Cai, Circuit minimization problem, Proceedings of the 32nd ACM Symposium on Theory of Computing (STOC), 2000, pages 73 to 79
    locator: the circuit minimization problem for a truth table input, and the consequences of a proof of its NP-completeness
  - paper: doi:10.1145/1146909.1147048
    title: Alan Mishchenko, Satrajit Chatterjee and Robert Brayton, DAG-aware AIG rewriting, a fresh look at combinational logic synthesis, Proceedings of the 43rd Design Automation Conference, 2006, pages 532 to 535
    locator: the and-inverter graph as the form of multi-level synthesis, with node count and depth as the costs
---

Multi-level logic synthesis takes a [Boolean network](/boolean-network/), a circuit of nodes with local functions, and looks for an equivalent network that costs less: fewer literals or nodes, which estimate area, or fewer levels, which estimate delay. It is the step of a chip design flow between the description of the logic and [technology mapping](/technology-mapping/). Unlike [two-level logic minimization](/two-level-logic-minimization/), the result may have any number of levels, so a function can share and reuse its parts, and the search space is much larger. The problem is hard in each common form: deciding whether a network can lose all its literals is already co-NP-hard, and minimum formulas are $\Sigma_2^p$-complete under Turing reductions (Buchfuhrer and Umans 2011). All practical methods are heuristics that change the network in small steps, each of which keeps the function. The MIS system (Brayton, Rudell, Sangiovanni-Vincentelli and Wang 1987) set the pattern with algebraic factoring and don't-care simplification, and later tools such as ABC work on [and-inverter graphs](/and-inverter-graph/).

## In plain words

A circuit is a set of small logic blocks, where each block reads some wires and drives a new wire. Many different circuits do the same job. Some use fewer parts, and some give their answer after fewer steps. The task is to take a working circuit and find a cheaper one that gives the same answer for every input. A tool does this in small moves. It pulls out a part that two blocks both compute and builds it once. It writes a block in a shorter form, like taking out a common factor in algebra. It uses the inputs where a block's answer is never seen to make the block simpler. Each move keeps the answers the same, so the tool can stop at any time with a correct circuit. No known method finds the cheapest circuit for large designs.

## Definition

**Input.** A Boolean network $N$ with primary inputs $x = (x_1, \ldots, x_n)$ and primary outputs $z_1, \ldots, z_m$, with global functions $g_{z_j}$. Optionally, an external don't-care set $E_j \subseteq \{0,1\}^n$ for each output.

**Feasible solutions.** A Boolean network $N'$ on the same inputs and outputs, with global functions $g'_{z_j}$, such that
$$g'_{z_j}(x) = g_{z_j}(x) \quad \text{for all } j \text{ and all } x \notin E_j.$$
With no external don't-cares, $N'$ is equivalent to $N$.

**Objective.** Minimize a cost $c(N')$. The classic cost is the number of literals of all local functions in factored form. Other costs are the number of nodes of an and-inverter graph, the depth, a weighted sum, or the literal count under a bound on the depth.

**Decision version.** Given $N$, the don't-care sets and an integer $k$, is there a feasible $N'$ with $c(N') \le k$?

## Variants

- **By the cost.** Area (literals in factored form, or AIG nodes), delay (depth, or depth with a delay per node), or power (an estimate of the switching activity of each node).
- **By the node functions.** Any local function, as in MIS and SIS. A fixed basis, such as 2-input AND with inverted edges in an [and-inverter graph](/and-inverter-graph/), or 3-input majority in a [majority-inverter graph](/majority-inverter-graph/). With a complete basis of 2-input gates, the problem is the minimum circuit problem.
- **By the input form.** A network, a set of SOPs, or a truth table. The input form changes the complexity, as under Bounds.
- **Technology-independent or mapped.** The classic problem ignores the cell library. When the cost is the area or delay of library cells or lookup tables, the problem becomes [technology mapping](/technology-mapping/) or [LUT mapping](/lut-mapping/), usually solved after this one.
- **Sequential.** With latches, the latches may also move, as in [retiming](/retiming/), and the unreachable states give extra don't-cares.
- **Exact on small functions.** For functions of a few inputs, [exact synthesis](/exact-synthesis/) finds a minimum network over a fixed basis.

## Examples

Each example was checked on all input vectors by a script.

- **Factoring.** The single node $f = a b + a c + b d + c d$ has 8 literals. Since $a b + a c + d b + d c = (a + d)(b + c)$, the factored form has 4.
- **Extraction across outputs.** The nodes $f = a c + b c + e$ and $g = a d + b d + \bar{e}$ have 10 literals. The new node $x = a + b$ gives $f = x c + e$ and $g = x d + \bar{e}$, with $2 + 3 + 3 = 8$ literals. Finding $x$ is the job of [kernel extraction](/kernel-extraction/).
- **Boolean beats algebraic.** The node $f = a b + \bar{a} c + b c$ has 6 literals. The algebraic methods treat $a$ and $\bar{a}$ as unrelated letters and never drop a cube. The best algebraic factored form has 5 literals, $b(a + c) + \bar{a} c$: a search over all factored forms with at most 4 leaves over the literals $a, \bar{a}, b, c$ found none that multiplies out to these three cubes. The cube $b c$ is the consensus of $a b$ and $\bar{a} c$, so $f = a b + \bar{a} c$ as a function, with 4 literals. Removing it needs Boolean reasoning, such as a two-level minimizer.
- **Don't-cares.** With $y = a + b$ and the only output $z = y \bar{a}$, the node $y$ is never seen when $a = 1$, and it can become the wire $b$. The [observability don't-care](/observability-dont-care/) page works this out.
- **Depth.** The AND of $a, b, c, d$ as the chain $((a b) c) d$ has 3 nodes and depth 3. The tree $(a b)(c d)$ has 3 nodes and depth 2. [AIG balancing](/aig-balancing/) makes this change.
- **A network that loses every literal.** For a CNF formula $\varphi$ and a new variable $z$, build the network of $\varphi \wedge z$ with one node per clause. It has an equivalent network with no literal, a constant, exactly when $\varphi$ is unsatisfiable. If $\varphi$ has a satisfying assignment, the function depends on $z$.

## Known algorithms

All of these are heuristics for the full problem: each step keeps the function, and none has a proved bound on the distance to the optimum.

- [Algebraic division](/algebraic-division/), [algebraic kernels](/algebraic-kernel/) and [kernel extraction](/kernel-extraction/). Treat each SOP as a polynomial, divide it by kernels, and pull out divisors that several nodes share. Fast, and blind to Boolean identities such as $a \bar{a} = 0$.
- Node simplification with [observability don't-cares](/observability-dont-care/). Minimize each local SOP with [Espresso](/espresso/) and the don't-cares from the rest of the network.
- [Ashenhurst-Curtis decomposition](/ashenhurst-curtis-decomposition/). Split a function by the distinct columns of a decomposition chart, often for lookup tables.
- [AIG balancing](/aig-balancing/) and [AIG rewriting](/aig-rewriting/). Reduce the depth or the node count of an and-inverter graph by local changes on small cuts, with precomputed small networks.
- [SAT sweeping](/sat-sweeping/). Find nodes with the same function by simulation and SAT, and merge them.
- [Exact synthesis](/exact-synthesis/). Optimal for a few inputs over a fixed basis, in time exponential in the size of the result.

Tools such as MIS, SIS and ABC run these steps in scripts. Their results are measured on benchmark circuits and are not proved.

## Bounds

**Upper bounds (proved).**

- Every function of $n$ inputs has a network. Its minterm SOP is one node with at most $n 2^n$ literals, and the [Shannon expansion](/shannon-expansion/) $f = \bar{x}_1 f_0 + x_1 f_1$, applied to the subfunctions level by level, gives a network of fewer than $2^n$ nodes with 4 literals each.
- For a network input and a literal cost, the decision version is in $\Sigma_2^p$ of the [polynomial hierarchy](/polynomial-hierarchy/): guess $N'$ with at most $k$ literals, and check for all $x$ that it agrees with $N$ off the don't-care sets. The check is in co-NP.
- For a truth table input and a fixed basis of 2-input gates, the decision version is in [NP](/np/), since a circuit with at most $k \le 2^n$ gates is a certificate checked in time polynomial in $2^n$. This is the minimum circuit size problem.

**Lower bounds (proved, as hardness).**

- For a network input, the decision version is [co-NP-hard](/co-np-complete/), even for $k = 0$, by the last example above and the co-NP-completeness of unsatisfiability.
- For formulas, the Minimum Equivalent Expression problem, given a formula and $k$, is there an equivalent formula of size at most $k$, is $\Sigma_2^p$-complete under [Turing reductions](/turing-reduction/) (Buchfuhrer and Umans 2011). A network in which every node has one fanout is a formula, so this is the fanout-free case of the problem.
- The two-level case is NP-hard for a truth table input and $\Sigma_2^p$-complete for a DNF input; see [two-level logic minimization](/two-level-logic-minimization/).
- For a truth table input, it is not known whether the minimum circuit size problem is NP-complete. Kabanets and Cai (2000) showed that a proof of NP-completeness by the usual kind of reduction would give circuit lower bounds for exponential time that are beyond the known methods.
- For $n \ge 5$, most functions of $n$ inputs need more than $2^n / (4n)$ nodes with two fanins. The [Boolean network](/boolean-network/) page proves this by counting.

**Measured.** The papers on MIS, SIS, ABC and AIG rewriting report literal counts, node counts and depths on benchmark circuits. These are measurements on those sets, not bounds.

## Reductions

- **From unsatisfiability.** The construction in the examples reduces the complement of [SAT](/sat/) to the decision version with $k = 0$, in linear time.
- **To two-level minimization, by collapsing.** Eliminating every internal node gives one SOP per output, which two-level methods can minimize. The SOP can be exponentially larger than the network, as for parity of $n$ inputs, which has a network of $n - 1$ XOR nodes and needs $2^{n-1}$ cubes in two levels.
- **To SAT, for exact synthesis.** The question "is there a network of $r$ nodes for $f$" for a small truth table becomes a SAT instance, which is how [exact synthesis](/exact-synthesis/) works.
- **To and from circuits.** A network becomes a circuit of 2-input gates with at most three gates per literal, and a circuit is a network with small local functions.

## Applications

- **Chip design.** ASIC flows run technology-independent optimization before [technology mapping](/technology-mapping/), and FPGA flows run it before [LUT mapping](/lut-mapping/).
- **Verification.** The same AIG rewriting and [SAT sweeping](/sat-sweeping/) make equivalence and model checking problems smaller before a solver runs.
- **High-level synthesis output.** The logic that a scheduler and binder produce is a network that this step cleans up.

## References
