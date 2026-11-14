---
tag: 280NCB
kind: problem
slug: hypergraph-partitioning
name: Hypergraph partitioning
aliases:
- netlist partitioning
- circuit partitioning
area: cad/partitioning-floorplanning-and-placement
level: core
summary: Split the vertices of a hypergraph into k balanced parts so that few hyperedges, the nets of a circuit, span more than one part.
prereqs: [hypergraph, graph-partitioning-problem, np-hard]
see_also: [graph-partitioning-problem, fiduccia-mattheyses, kernighan-lin, multilevel-hypergraph-partitioning, clique-net-model, ratio-cut, min-cut-placement, max-flow-min-cut-theorem]
sources:
  - paper: doi:10.1016/0304-3975(76)90059-1
    title: M. R. Garey, D. S. Johnson and L. Stockmeyer, Some simplified NP-complete graph problems, Theoretical Computer Science 1(3), 237 to 267, 1976
    locator: the NP-completeness of minimum bisection, which is the case of nets with two pins
  - paper: doi:10.1002/net.3230030306
    title: E. L. Lawler, Cutsets and partitions of hypergraphs, Networks 3(3), 275 to 285, 1973
    locator: the network flow computation of optimal cutsets of a hypergraph
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 2, Netlist and System Partitioning (the partitioning problem for netlists, the balance condition, and the Kernighan-Lin, Fiduccia-Mattheyses and multilevel methods)
  - paper: doi:10.1109/92.748202
    title: George Karypis, Rajat Aggarwal, Vipin Kumar and Shashi Shekhar, Multilevel hypergraph partitioning, applications in VLSI domain, IEEE Transactions on VLSI Systems 7(1), 69 to 79, 1999
    locator: the problem statement with the balance constraint and the hyperedge cut objective
  - paper: "Charles J. Alpert and Andrew B. Kahng, Recent directions in netlist partitioning, a survey, Integration, the VLSI Journal 19(1 to 2), 1 to 81, 1995"
    locator: the formulations of netlist partitioning (cut-net, sum of external degrees, ratio cut) and the survey of methods
---

Hypergraph partitioning asks to split the vertices of a [hypergraph](/hypergraph/) into $k$ parts of bounded weight so that the nets (hyperedges) that span more than one part have the least total weight. In circuit design the vertices are cells and the nets are wires that join any number of pins, so a cut net is a wire that runs between chips, between blocks or across a cut line of a placement. The case where every net has two pins is the [graph partitioning problem](/graph-partitioning-problem/), so the problem is [NP-hard](/np-hard/) already for bisection. The trap is the objective: a cut net counts once, however its pins are split, which is not what a graph model of the net counts.

## In plain words

A circuit has many parts, and each wire joins two or more of them. You must put the parts on two chips of about the same size. Every wire whose parts end up on both chips needs a pin on each chip, and pins are expensive. So you want as few such wires as possible.

What counts is the number of wires that cross, not the number of pairs of parts that are split. A wire that joins ten parts costs one pin pair if it crosses, whether one part or five parts are on the far side. That is what makes this problem different from cutting the edges of an ordinary graph.

## Definition

**Input.** A hypergraph $H = (V, E)$ with $n = |V|$ vertices, $m = |E|$ nets and $P = \sum_{e \in E} |e|$ pins; vertex weights $c(v) > 0$ (cell areas) and net weights $w(e) \ge 0$; a number of parts $k \ge 2$; and an imbalance $\varepsilon \ge 0$. Optionally, a set $F \subseteq V$ of *fixed* vertices with a given part for each.

**Output.** A partition $V = V_1 \cup \cdots \cup V_k$ into disjoint parts that puts each fixed vertex in its given part and satisfies the balance condition

$$ c(V_i) \le (1 + \varepsilon) \, \frac{c(V)}{k} \qquad (i = 1, \ldots, k). $$

**Objective.** Let $\lambda(e)$ be the number of parts that contain a pin of $e$. The two standard objectives are

$$ \text{cut-net:} \quad \mathrm{cut}(V_1, \ldots, V_k) = \sum_{e : \lambda(e) > 1} w(e), \qquad \text{connectivity:} \quad \sum_{e} w(e) \, (\lambda(e) - 1). $$

Minimize one of them. For $k = 2$ they are equal. For $k > 2$ the connectivity objective, also called the $(\lambda - 1)$ metric, counts a net once for each extra part it touches, which models the pins that a net needs on each extra chip. A third objective, the sum of external degrees, is $\sum_{e : \lambda(e) > 1} w(e) \lambda(e)$.

**Bisection.** For $k = 2$ the balance condition is often given as a window: the weight of part $V_1$ must lie in $[lo, hi]$. Exact bisection is $lo = hi = c(V)/2$.

What is fixed: the netlist, the weights, $k$, the balance bound and the fixed vertices. What is free: the part of every other vertex. A partition is legal if it meets the balance condition and the fixed assignments. Nothing else, such as the geometry of the parts, enters the problem.

## Variants

- **Cut-net against clique cut.** A graph partitioner applied to the [clique net model](/clique-net-model/) of the netlist minimizes a different objective. A net split $j : (p - j)$ costs $j (p - j)/(p - 1)$ there, and no weighting of the clique edges matches the cut-net count for nets with 4 or more pins. The example below shows that the two optima can differ.
- **Fixed vertices.** Pads, and in placement the terminals added by [terminal propagation](/terminal-propagation/), are vertices that must stay in a given part. They count in the cut but never move.
- **Ratio objectives.** The [ratio cut](/ratio-cut/) divides the cut by $|V_1| \, |V_2|$ and drops the balance condition, so the partitioner can find natural clusters of uneven size.
- **No balance.** With no balance condition and no fixed vertices, the problem is a minimum cut of the hypergraph, solvable in polynomial time by network flows (see the reduction below).
- **k-way.** Recursive bisection splits into 2, then 4 parts and so on. Direct $k$-way methods refine all $k$ parts at once.
- **Multiple constraints.** Each vertex has a vector of weights (area, power, pins) and each part must be balanced in every component.

## Examples

**A bisection that the clique model gets wrong.** Take six cells $a, \ldots, f$ and six nets of weight 1:

$$ N_1 = \{a, d, e, f\}, \; N_2 = \{a, c, d, f\}, \; N_3 = \{b, c, d, e\}, \; N_4 = \{e, f\}, \; N_5 = \{a, b, c, e\}, \; N_6 = \{c, e\}. $$

Split them into two parts of three cells. There are 10 such bisections. Two of them:

| bisection | how $N_1, \ldots, N_6$ are split | cut nets | clique cut, weight $1/(p-1)$ |
| --- | --- | --- | --- |
| $\{a, b, d\} \mid \{c, e, f\}$ | 2:2, 2:2, 2:2, not cut, 2:2, not cut | 4 | $4 \cdot \frac{4}{3} = \frac{16}{3}$ |
| $\{a, d, f\} \mid \{b, c, e\}$ | 3:1, 3:1, 1:3, 1:1, 1:3, not cut | 5 | $4 \cdot 1 + 1 = 5$ |

Checking all 10 bisections shows that the first is the only one with 4 cut nets, the least possible, and the second is the only one with clique cut 5, the least possible for the clique. A graph partitioner that solves the clique model exactly returns a bisection with 5 cut nets, 25 percent more than the optimum.

**Cut-net against connectivity.** Split $\{a, b, c, d, e, f\}$ into $\{a, b\}, \{c, d\}, \{e, f\}$ with the nets $\{a, c, e\}$, $\{a, b\}$ and $\{b, d\}$. The cut-net objective is 2: the first and the third net are cut. The connectivity objective is $(3 - 1) + 0 + (2 - 1) = 3$, because the first net needs pins in two extra parts.

## Known algorithms

All practical methods for large netlists are heuristics with no proved approximation ratio.

- **[Kernighan-Lin](/kernighan-lin/).** Swaps pairs of cells in passes. Designed for graphs, so on netlists it works on a graph model or with net-based gains. Heuristic.
- **[Fiduccia-Mattheyses](/fiduccia-mattheyses/).** Moves single cells under the balance condition and keeps the gains in buckets, so a pass takes $O(P)$ time. It works on the cut-net objective directly. Heuristic; each pass gives a local optimum for single moves.
- **[Multilevel hypergraph partitioning](/multilevel-hypergraph-partitioning/).** The hMETIS scheme: coarsen by merging cells of the same nets, partition the small hypergraph, and refine with FM on the way back. Heuristic. It is the standard for large netlists. The graph version is [multilevel graph partitioning](/multilevel-graph-partitioning/).
- **[Spectral partitioning](/spectral-partitioning/).** Uses an eigenvector of the Laplacian of a clique or star model. The bounds that come with it are for the graph model, not for the cut-net objective.
- **Flow-based methods.** Minimum cuts in the flow network below give exact unbalanced cuts and are used to refine a balanced partition.
- **[Simulated annealing](/simulated-annealing/).** Random moves with a cooling schedule. Heuristic; slow on large netlists.
- **Exact search.** Branch and bound or enumeration finds the optimum for small instances only. The test of the multilevel page compares with enumeration of all bisections for up to 14 cells.

## Bounds

- **NP-hardness.** Hypergraph bisection is NP-hard, because a graph is a hypergraph whose nets have two pins, and minimum bisection of a graph is NP-complete (Garey, Johnson and Stockmeyer, 1976). This holds with unit weights.
- **Inherited limits.** Every hardness result for the graph problem holds here too. For $k \ge 3$ and exact balance, no polynomial algorithm has a finite approximation ratio unless P = NP (see [graph partitioning problem](/graph-partitioning-problem/)).
- **Polynomial without balance.** With no balance condition, a minimum $s$-$t$ net cut and a minimum net cut overall are found in polynomial time by maximum flow (Lawler, 1973).
- **Spectral and ratio bounds.** The lower bounds from eigenvalues hold for the graph model of the netlist under a stated normalization. For the cut-net objective, a cut net counts once, so the clique cut with weight $1/(p - 1)$ is at least the number of cut nets and at most $\lfloor p_{\max}^2/4 \rfloor / (p_{\max} - 1)$ times it, where $p_{\max}$ is the largest net size. A bound on one gives a bound on the other only up to this factor.

## Reductions

- **From graph bisection.** Keep the vertices, and turn each edge $\{u, v\}$ into a net $\{u, v\}$ of the same weight. A net with two pins is cut exactly when the edge is cut, so the two problems have the same optimal partitions and values.
- **Unbalanced cut to maximum flow (Lawler's network).** Build a directed network with a node for each vertex and two nodes $e'$ and $e''$ for each net $e$. Add an arc $e' \to e''$ of capacity $w(e)$, and arcs $v \to e'$ and $e'' \to v$ of infinite capacity for each pin $v \in e$. For vertices $s$ and $t$, the minimum capacity of an $s$-$t$ cut equals the least weight of a set of nets whose removal separates $s$ from $t$. *Proof.* Given a partition $(S, T)$ of $V$ with $s \in S$, $t \in T$, put $e'$ and $e''$ on the source side for nets inside $S$, on the sink side for nets inside $T$, and $e'$ on the source side with $e''$ on the sink side for cut nets. No infinite arc goes from the source side to the sink side, and the cut capacity is the weight of the cut nets. Conversely, in a cut of finite capacity with source side $X$, a net with a pin in $X$ has $e' \in X$, or an infinite arc $v \to e'$ would cross, and a net with a pin outside $X$ has $e'' \notin X$. So every net cut by $(X \cap V, V \setminus X)$ contributes its arc $e' \to e''$. By the [max-flow min-cut theorem](/max-flow-min-cut-theorem/), one maximum flow gives the value. Fixing $s$ and trying all $t$ gives a global minimum net cut with $n - 1$ flows.
- **To graph partitioning, with loss.** The [clique net model](/clique-net-model/) or a star model gives a graph, and a graph partitioner can be run on it. The reduction does not preserve the optimum, as the first example shows.

## Applications

- **Chip and board partitioning.** Split a design among FPGAs or chips with few signals between them, under limits on the area and on the pins of each part.
- **Placement.** [Min-cut placement](/min-cut-placement/) bisects the netlist and the chip area again and again, so that the cut at each level is the number of nets that cross a cut line. The [placement problem](/placement-problem/) page gives the context.
- **Hierarchical design and floorplanning.** Group the cells into blocks with few nets between blocks. [Rent's rule](/rents-rule/) describes how the cut grows with the block size in such a hierarchy.
- **Sparse matrices and parallel computing.** A sparse matrix is a hypergraph whose rows are nets over the columns, or the reverse. The connectivity objective then counts exactly the words of communication in a parallel matrix-vector product, which a graph model can only approximate.
- **Logic simulation and emulation.** Divide a netlist among processors or emulator boards to balance the work and reduce the messages.

## References
