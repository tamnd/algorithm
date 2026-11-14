---
tag: HA6EZ1
kind: definition
slug: k-feasible-cut
name: k-feasible cut
aliases:
- k-cut of a node
area: eda/logic-synthesis
level: core
summary: A set of at most k nodes such that every path from the inputs to a given node passes through it, so the node is a function of the cut.
prereqs: [boolean-network, directed-acyclic-graph]
see_also: [cut-enumeration, lut-mapping, flowmap, priority-cuts, aig-rewriting, and-inverter-graph, menger-theorem, vertex-disjoint-paths]
sources:
  - paper: "Jason Cong and Yuzheng Ding, FlowMap, an optimal technology mapping algorithm for delay optimization in lookup-table based FPGA designs, IEEE Transactions on Computer-Aided Design 13(1), 1 to 12, 1994"
    title: FlowMap, an optimal technology mapping algorithm for delay optimization in lookup-table based FPGA designs
    locator: the definitions of a cut (X, X-bar) of the cone of a node, of its node cut-set and of a K-feasible cut
  - paper: doi:10.1145/275107.275118
    title: Peichen Pan and Chih-Chang Lin, A new retiming-based technology mapping algorithm for LUT-based FPGAs, Proceedings of the 1998 ACM/SIGDA Sixth International Symposium on Field Programmable Gate Arrays (FPGA 98), pages 35 to 42
    locator: the computation of the K-feasible cuts of each node by combining the cuts of its fanins
  - paper: "Jason Cong, Chang Wu and Yuzheng Ding, Cut ranking and pruning, enabling a general and efficient FPGA mapping solution, Proceedings of the 1999 ACM/SIGDA Seventh International Symposium on Field Programmable Gate Arrays (FPGA 99), pages 29 to 35"
    title: Cut ranking and pruning, enabling a general and efficient FPGA mapping solution
    locator: the enumeration of all K-feasible cuts and the pruning of cuts by rank
---

A cut of a node $v$ in a [Boolean network](/boolean-network/) is a set of nodes that every path from a primary input to $v$ passes through. The cut is $k$-feasible when it has at most $k$ nodes. Once the values of the cut nodes are known, the value of $v$ is fixed, so $v$ is a Boolean function of the cut, with at most $k$ inputs. This is why cuts are the basic unit of [LUT mapping](/lut-mapping/), where a $k$-input lookup table can compute any function of $k$ inputs, and of local rewriting of [and-inverter graphs](/and-inverter-graph/). The term comes from Cong and Ding's FlowMap paper (1994), which states it in terms of a partition of the cone of the node. Later mappers list the cuts of every node, as on the [cut enumeration](/cut-enumeration/) page.

## Definition

Let $G$ be a [directed acyclic graph](/directed-acyclic-graph/) whose sources are the primary inputs (PIs) and whose other nodes are gates. Each gate $w$ has a local function of its fanins. The *cone* of a node $v$ is the set of nodes from which $v$ can be reached, $v$ included.

**Cut.** A set $C$ of nodes is a cut of $v$ if every path from a PI to $v$ contains a node of $C$. The nodes of $C$ are the *leaves* of the cut. The set $\{v\}$ is the *trivial cut* of $v$. For a PI $v$, the trivial cut is the only cut that lies in the cone of $v$.

**$k$-feasible cut.** A cut $C$ of $v$ is $k$-feasible if $|C| \le k$.

**Minimal cut.** A cut is minimal, or irredundant, if no proper subset of it is a cut of $v$. Every minimal cut lies in the cone of $v$, and a minimal cut other than $\{v\}$ does not contain $v$. Some authors use "cut" to mean a minimal cut.

**Cone of a cut.** For a cut $C$ of $v$, the cone of $v$ over $C$ is the set of nodes $w \notin C$ from which $v$ can be reached on a path with no node of $C$. Its nodes are the gates that a lookup table for $v$ over $C$ replaces. For the trivial cut the cone is empty.

**Partition form.** Cong and Ding state the same idea on the cone $N_v$ of $v$. A cut is a partition $(X, \bar{X})$ of $N_v$ with $v \in \bar{X}$ and every PI of $N_v$ in $X$. Its node cut-set is the set of nodes of $X$ that have a fanout in $\bar{X}$. The partition is $k$-feasible if its node cut-set has at most $k$ nodes. Given a cut $C$ in the set form, put the cone of $v$ over $C$ in $\bar{X}$ and the rest of $N_v$ in $X$. The node cut-set is then a subset of $C$, and it equals $C$ when $C$ is minimal and $C \ne \{v\}$.

**Cut function.** Order the leaves of a cut as $u_1, \ldots, u_m$. The cut function of $v$ over $C$ is the function $g$ of $m$ variables such that $v = g(u_1, \ldots, u_m)$ on every input of the network. In the code of this site, $g$ is a truth table stored as an integer of $2^m$ bits, with $u_1$ as the high bit of the row number.

**Basic facts.**

1. *A node is a function of each of its cuts.* Fix values at the leaves of $C$. Evaluate the nodes of the cone of $v$ over $C$ in topological order. Each fanin of such a node is a leaf or a node of the cone, since a path to $v$ that avoids $C$ would reach a PI. So the value of $v$ depends only on the leaves, and $g$ exists. If two inputs of the network give the same leaf values, they give the same value of $v$.
2. *Unions of fanin cuts are cuts.* If $v$ has fanins $w_1, \ldots, w_d$ and $C_i$ is a cut of $w_i$, then $C_1 \cup \cdots \cup C_d$ is a cut of $v$, because a path from a PI to $v$ enters $v$ through some $w_i$. Each minimal cut of $v$ other than $\{v\}$ is such a union. This is the merge rule of [cut enumeration](/cut-enumeration/).
3. *Testing a cut.* A search from $v$ along fanin edges that stops at the nodes of $C$ tests whether $C$ is a cut: $C$ is a cut exactly when the search reaches no PI outside $C$. It takes time linear in the size of the cone.
4. *Smallest cut.* For a gate $v$, the least size of a cut of $v$ that does not contain $v$ is the largest number of paths from the PIs to $v$ that share no node other than $v$, by [Menger's theorem](/menger-theorem/) on the graph with a new source joined to every PI. It is a max-flow value with unit node capacities, as in [FlowMap](/flowmap/).
5. *Counting.* A node of a network with $n$ nodes has at most $\sum_{i \le k} \binom{n}{i}$ $k$-feasible cuts, which is polynomial in $n$ for a fixed $k$. Without the bound $k$, the count can grow very fast. The root of a complete binary tree of AND gates of depth $d$ has $N(d) = N(d-1)^2 + 1$ minimal cuts, with $N(0) = 1$, so 1, 2, 5, 26 and 677 for $d = 0$ to 4. For the tree of depth 4 there are 9 minimal 4-feasible cuts and 49 minimal 6-feasible cuts.

## Examples and non-examples

Take the network with inputs $a, b, c, d$ and the AND gates $e = a b$, $f = b c$, $g = e f$, $h = f d$ and $o = g h$. Node $f$ feeds both $g$ and $h$.

- **The 3-feasible cuts of $o$.** The minimal ones are $\{o\}$, $\{g, h\}$, $\{d, e, f\}$, $\{d, f, g\}$ and $\{e, f, h\}$. For example, every path into $o$ passes through $g$ or $h$, and every path into $g$ or $h$ passes through $e$, $f$ or $d$.
- **The 4-feasible cuts of $o$.** There are 12 minimal ones. The seven new ones are $\{a, b, c, d\}$, $\{a, b, c, h\}$, $\{a, b, d, f\}$, $\{a, b, f, h\}$, $\{b, c, d, e\}$, $\{b, c, d, g\}$ and $\{b, c, e, h\}$. Over all nine nodes the network has 21 minimal 3-feasible cuts and 28 minimal 4-feasible cuts.
- **Cut functions.** Over $\{g, h\}$, $o = g h$, the table 1000. Over $\{d, e, f\}$, $o = e f \cdot f d = d e f$, the table 10000000. Over $\{a, b, c, d\}$ the function is $a b c d$, with only the top bit of 16 set.
- **Not a cut.** $\{d, g\}$ is not a cut of $o$: the path $b \to f \to h \to o$ avoids it. $\{e, h\}$ is not a cut either: the path $b \to f \to g \to o$ avoids it.
- **A cut that is not minimal.** $\{e, f, g, h\}$ is a cut of $o$, but it contains the cut $\{g, h\}$. A LUT over it would have an input that it does not need. The merge of fanin cuts can make such a set: in the network with $a = x y$, $b = x a$ and $v = a b$, the union of the cut $\{a\}$ of $a$ and the cut $\{x, y\}$ of $b$ is $\{a, x, y\}$, which contains the cut $\{a, x\}$.
- **Not $k$-feasible.** $\{a, b, c, d\}$ is a cut of $o$, but it is not 3-feasible.

## Related definitions

- **[Cut enumeration](/cut-enumeration/).** Lists all minimal $k$-feasible cuts of every node, by fact 2.
- **[LUT mapping](/lut-mapping/).** A mapping picks one $k$-feasible cut for each LUT root. The cut is the set of LUT inputs.
- **[FlowMap](/flowmap/).** Finds, by max-flow, a $k$-feasible cut of least height, where the height is the largest depth label of the cut.
- **[Priority cuts](/priority-cuts/).** Keeps only a few $k$-feasible cuts of each node.
- **Maximum fanout-free cone.** The nodes of the cone of a cut that no logic outside the cone uses, as on the [AIG rewriting](/aig-rewriting/) page.
- **[Menger's theorem](/menger-theorem/) and [vertex-disjoint paths](/vertex-disjoint-paths/).** Relate the smallest cut to the largest set of disjoint paths.
- **Boolean network.** The [Boolean network](/boolean-network/) and the [and-inverter graph](/and-inverter-graph/) are the graphs on which cuts are taken.

## References
