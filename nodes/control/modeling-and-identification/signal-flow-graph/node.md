---
tag: P2H8AD
kind: definition
slug: signal-flow-graph
name: Signal-flow graph
aliases:
- Mason graph
area: control/modeling-and-identification
level: intro
summary: A directed graph whose nodes are signals and whose weighted edges are gains. Each node equals the sum of its incoming edge gains times their source nodes, so the graph is a set of linear equations.
prereqs: [transfer-function]
see_also: [masons-gain-formula, block-diagram-reduction, transfer-function, state-space-representation, strongly-connected-components, gaussian-elimination, symbolic-circuit-analysis, determinant]
sources:
  - paper: doi:10.1109/JRPROC.1953.274449
    title: Samuel J. Mason, Feedback theory, some properties of signal flow graphs, Proceedings of the IRE 41(9), 1953
    locator: pp. 1144 to 1156 (the definition of the graph, node equations, paths, loops and the reduction of a graph)
  - paper: doi:10.1109/JRPROC.1956.275147
    title: Samuel J. Mason, Feedback theory, further properties of signal flow graphs, Proceedings of the IRE 44(7), 1956
    locator: pp. 920 to 926 (the graph determinant and the gain formula)
  - book: isbn:9780134685717
    title: Gene F. Franklin, J. David Powell and Abbas Emami-Naeini, Feedback Control of Dynamic Systems, eighth edition, Pearson, 2019
    locator: Section 3.2, System Modeling Diagrams, and Section 3.2.3, Mason's Rule and the Signal Flow Graph (an online section)
---

A signal-flow graph is a directed graph that encodes a set of linear equations. Each node is a signal (a variable), each edge carries a gain, and the value of a node is the sum, over its incoming edges, of the edge gain times the value at the start of the edge. Samuel Mason introduced the graphs in 1953 to describe feedback circuits. In control, the gains are usually [transfer functions](/transfer-function/) in $s$, and the graph is a compact form of a block diagram. The graph is useful because the gain from an input node to an output node can be read from its paths and loops with [Mason's gain formula](/masons-gain-formula/), with no matrix algebra by hand.

## Definition

**Notation.** Gains are elements of a field, usually the rational functions $\mathbb{R}(s)$ or the real numbers. An edge from node $j$ to node $i$ with gain $a$ is written $j \xrightarrow{a} i$.

**Definition.** A signal-flow graph is a finite directed graph with nodes $x_1, \dots, x_n$ and one or more *source nodes* $u_1, \dots, u_m$ that have no incoming edges, together with a gain on each edge. Parallel edges between the same two nodes are merged into one edge whose gain is the sum. The graph stands for the *node equations*

$$x_i = \sum_{j} w_{ij}\, x_j + \sum_{k} b_{ik}\, u_k, \qquad i = 1, \dots, n,$$

where $w_{ij}$ is the gain of the edge $x_j \to x_i$ (zero if there is no edge) and $b_{ik}$ is the gain of the edge $u_k \to x_i$. In matrix form, with $W = (w_{ij})$ and $B = (b_{ik})$,

$$(I - W)\, x = B\, u.$$

The graph is *well posed* if $\det(I - W) \ne 0$ (as an element of the field). Then every node has a unique value $x = (I - W)^{-1} B u$, and the gain from $u_k$ to $x_i$ is the entry $\bigl((I - W)^{-1} B\bigr)_{ik}$.

**Terms used with the graph.**

- A *path* is a sequence of edges along their direction with no node visited twice. Its gain is the product of the edge gains.
- A *forward path* is a path from a source node to the chosen output node.
- A *loop* is a closed path that visits no node twice except its first node, which is also its last. A self-loop $x_i \to x_i$ is a loop of length one.
- Two loops, or a loop and a path, *touch* if they have a node in common.
- The *graph determinant* is $\Delta = 1 - \sum L_a + \sum L_a L_b - \sum L_a L_b L_c + \cdots$, where the sums are over the loops, over the pairs of loops that do not touch, over the triples of loops that do not touch each other, and so on. Mason's gain formula shows $\Delta = \det(I - W)$.

**Structure.** Every loop lies inside one [strongly connected component](/strongly-connected-components/) of the graph. If the nodes are listed so that the components come in topological order, $I - W$ is block triangular, so $\Delta$ is the product of the determinants of the components. A graph with no loops (a directed acyclic graph) has $\Delta = 1$, and the gain from a source to a node is the sum of the gains of all paths between them.

**From equations to a graph.** Any square linear system $M x = b$ gives a graph: write it as $x = (I - M)x + b$, so that $w_{ij} = \delta_{ij} - m_{ij}$, and $\Delta = \det M$. Often one first solves equation $i$ for $x_i$, which divides row $i$ by $m_{ii}$ and removes the self-loops. A block diagram gives a graph directly: each signal line is a node, each block is an edge, and each summing junction is a node with several incoming edges (a minus sign at a junction goes into the gain of the edge). So the two pictures carry the same information, and [block diagram reduction](/block-diagram-reduction/) on one is graph reduction on the other.

## Examples and non-examples

- **A state-space model.** Take $x_1' = x_2$, $x_2' = -2 x_1 - 3 x_2 + u$, $y = x_1$, as in a [state-space representation](/state-space-representation/). In the Laplace domain at rest, use the nodes $u$, $v = s X_2$, $X_2$ and $X_1$, with the edges $u \xrightarrow{1} v$, $v \xrightarrow{1/s} X_2$, $X_2 \xrightarrow{1/s} X_1$, $X_2 \xrightarrow{-3} v$ and $X_1 \xrightarrow{-2} v$. The loops are $v \to X_2 \to v$ with gain $-3/s$ and $v \to X_2 \to X_1 \to v$ with gain $-2/s^2$. They touch at $v$, so $\Delta = 1 + 3/s + 2/s^2$. The single forward path $u \to v \to X_2 \to X_1$ has gain $1/s^2$ and touches both loops, so $Y/U = (1/s^2)/\Delta = 1/(s^2 + 3s + 2)$.
- **A unity feedback loop.** The nodes $r$, $e$, $y$ with the edges $r \xrightarrow{1} e$, $e \xrightarrow{G} y$, $y \xrightarrow{-1} e$ give $e = r - y$ and $y = G e$. The one loop has gain $-G$, so $\Delta = 1 + G$ and $Y/R = G/(1 + G)$.
- **A circuit.** In nodal analysis of a linear circuit, the node voltages are the nodes of the graph and the admittances divided by the node self-admittances are the gains; [symbolic circuit analysis](/symbolic-circuit-analysis/) uses such graphs to get transfer functions as formulas.
- **Non-example: a nonlinear node.** A node whose value is $x_j^2$, or the product of two signals, is not allowed. The node equations must be linear in the node values, so a multiplier or a saturation must be removed by [Jacobian linearization](/jacobian-linearization/) first.
- **Non-example: an ill-posed graph.** A node with a self-loop of gain 1 and an input $u$ gives $x = x + u$, which has no solution for $u \ne 0$. Here $\det(I - W) = 0$. In a block diagram this is an algebraic loop with loop gain 1, for example a feedback loop around a constant gain $-1$.
## Related definitions

- [Mason's gain formula](/masons-gain-formula/): the gain from a source to a node, $\sum_k P_k \Delta_k / \Delta$, read off the graph.
- [Block diagram reduction](/block-diagram-reduction/): the same algebra done by rules on a block diagram.
- [Transfer function](/transfer-function/): the gain of an edge in a graph of a linear time-invariant system.
- [Gaussian elimination](/gaussian-elimination/): the matrix method that solves $(I - W)x = Bu$ in $O(n^3)$ steps for numeric gains.
- [Determinant](/determinant/): $\Delta = \det(I - W)$.
- [Strongly connected components](/strongly-connected-components/): the parts of the graph that hold the loops; $\Delta$ factors over them.

## References
