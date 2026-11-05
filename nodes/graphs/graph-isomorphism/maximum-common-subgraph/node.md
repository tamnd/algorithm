---
tag: 2F5TRW
kind: problem
slug: maximum-common-subgraph
name: Maximum common subgraph
aliases:
- MCS
- maximum common induced subgraph
- maximum common edge subgraph
area: graphs/graph-isomorphism
level: core
summary: Find a largest graph that is isomorphic to a subgraph of both input graphs; NP-hard, solved exactly by clique search in the association graph or by branch and bound.
model: word-ram
complexity:
  vars: {n: the number of vertices of each graph}
  time: {worst: O(n! n^2)}
prereqs: [subgraph-isomorphism, induced-subgraph, maximum-clique]
see_also: [graph-edit-distance, clique-problem, bron-kerbosch, vf2-algorithm, ullmann-algorithm, line-graph, np-hard]
sources:
  - paper: doi:10.1016/0020-0190(76)90049-1
    title: H. G. Barrow and R. M. Burstall, Subgraph isomorphism, matching relational structures and maximal cliques, Information Processing Letters 4(4), 83 to 84 (1976)
    locator: the whole note (the association graph and the reduction to cliques)
  - paper: doi:10.1002/spe.4380120103
    title: James J. McGregor, Backtrack search algorithms and the maximal common subgraph problem, Software, Practice and Experience 12(1), 23 to 34 (1982)
    locator: the whole paper (branch and bound over vertex pairs)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A1.4, Largest common subgraph (NP-completeness by reduction from clique)
  - paper: "John W. Raymond and Peter Willett, Maximum common subgraph isomorphism algorithms for the matching of chemical structures, Journal of Computer-Aided Molecular Design 16(7), 521 to 533 (2002)"
    locator: the whole survey (induced and edge versions, clique-based and backtracking methods)
---

The maximum common subgraph problem asks for a largest graph that occurs in both of two given graphs. In the induced version, the common part is an [induced subgraph](/induced-subgraph/) of each graph and its size is counted in vertices; in the edge version, it is a subgraph and its size is counted in edges. The problem generalizes [graph isomorphism](/graph-isomorphism-problem/) (the common part is everything) and [subgraph isomorphism](/subgraph-isomorphism/) (the common part is all of the smaller graph), and it is [NP-hard](/np-hard/). The common subgraph measures how similar two graphs are, which is why chemistry uses it to compare molecules.

## In plain words

You have two networks and want to find the largest piece they share. A piece is shared when you can pick points in the first network and the same number of points in the second, and pair them up so that two picked points are linked in the first network exactly when their partners are linked in the second. The more points the shared piece has, the more alike the networks are. A second version counts shared links instead of points. Finding the best piece is hard because you have to choose which points to keep and how to pair them, both at once.

## Definition

Graphs are simple and undirected, possibly with vertex and edge labels that the common part must keep; directed graphs work the same way with arcs.

**Maximum common induced subgraph (MCIS).**
- Input: graphs $G_1 = (V_1, E_1)$ and $G_2 = (V_2, E_2)$.
- Output: sets $A \subseteq V_1$, $B \subseteq V_2$ and a bijection $f : A \to B$ with $\{u, w\} \in E_1 \iff \{f(u), f(w)\} \in E_2$ for all $u, w \in A$, with $|A|$ as large as possible.

**Maximum common edge subgraph (MCES).**
- Input: $G_1$ and $G_2$.
- Output: an injective map $f$ from a subset of $V_1$ to $V_2$ that maximizes the number of edges $\{u, w\} \in E_1$ with $\{f(u), f(w)\} \in E_2$; the common subgraph is the set of these edges.

The **decision version** asks whether a common subgraph of size at least $K$ exists. A **connected** variant asks for the largest connected common subgraph, which chemistry often prefers.

## Variants

- **Induced versus edge.** For graphs on the same vertex set, MCES is a subgraph question and MCIS an induced subgraph question. MCES on $G_1$ and $G_2$ is MCIS on their [line graphs](/line-graph/), except for the triangle and the star $K_{1,3}$, which have the same line graph (Whitney's theorem); tools for MCES use this reduction and repair the exception.
- **Connected MCS.** Require the common subgraph to be connected; it is still NP-hard and is often easier to search.
- **Many graphs.** Find the largest subgraph common to $k \ge 2$ graphs, used for finding a common core of a set of molecules.
- **Labeled graphs.** Vertex and edge labels restrict the pairs; atom and bond types do this in chemistry.
- **Restricted classes.** For two trees, the largest common subtree is found in polynomial time by dynamic programming with bipartite matching at each pair of vertices; on several other restricted classes the problem stays NP-hard.

## Examples

All values were computed by a search over all choices of vertex subsets and maps.

| $G_1$ | $G_2$ | MCIS (vertices) | MCES (edges) |
|---|---|---|---|
| path $P_4$ | star $K_{1,3}$ | 3, the path $P_3$ | 2 |
| triangle $K_3$ | cycle $C_4$ | 2, one edge | 2 |
| $C_6$ | $2K_3$ | 4, two disjoint edges | 4 |
| $G$ | any relabeling of $G$ | all vertices | all edges |

For $C_6$ and $2K_3$: an induced subgraph of $2K_3$ is a disjoint union of at most two cliques, and the induced subgraphs of $C_6$ with that shape and the most vertices are two disjoint edges, such as $\{0, 1\}$ and $\{3, 4\}$. For the edge version a map sends two paths of two edges each into the two triangles, keeping 4 edges.

**The association graph.** For MCIS, build the graph whose vertices are the pairs $(u, v) \in V_1 \times V_2$, with $(u, v)$ and $(u', v')$ adjacent when $u \ne u'$, $v \ne v'$, and $\{u, u'\} \in E_1 \iff \{v, v'\} \in E_2$. Cliques of this graph are exactly the common induced subgraphs with their maps. For $C_6$ and $2K_3$ it has 36 vertices, and its largest clique has 4 vertices.

## Known algorithms

| algorithm | version | time |
|---|---|---|
| all subsets and maps | both | $O(n! \cdot n^2)$ for equal sizes |
| [maximum clique](/maximum-clique/) in the association graph (Barrow and Burstall 1976), for example with [Bron-Kerbosch](/bron-kerbosch/) | MCIS; MCES via line graphs | exponential in $n_1 n_2$ in the worst case |
| McGregor's backtracking (1982) | MCES and MCIS | exponential, with bound pruning |
| McSplit (McCreesh, Prosser and Trimble 2017) | MCIS, connected MCIS | exponential, partition-based bound, fast in practice |
| integer programming and constraint programming | both | exponential |
| [graph edit distance](/graph-edit-distance/) solvers with special costs | MCIS | exponential |

The clique method turns the problem into a single maximum clique search on $n_1 n_2$ vertices. McSplit instead keeps, for each partial map, the classes of unmatched vertices with the same adjacency to the mapped ones in each graph, and bounds the remaining gain by the sum of the minimum class sizes; it uses less memory and is faster on most benchmarks.

## Bounds

- **NP-hard.** MCIS with $G_1 = K_k$ asks whether $G_2$ has a $k$-clique, so it is NP-complete in the decision version (Garey and Johnson, "Largest common subgraph"). MCES is NP-hard for the same reason with edge counts.
- **Inapproximable.** Since maximum clique is a special case, MCIS cannot be approximated within $n^{1 - \varepsilon}$ for any $\varepsilon > 0$ unless P = NP.
- **Exact upper bound.** $O(n! \cdot n^2)$ or the time of maximum clique on $n_1 n_2$ vertices.
- **Isomorphism as a special case.** $G_1 \cong G_2$ exactly when MCIS has $|V_1| = |V_2|$ vertices, so MCS is at least as hard as [graph isomorphism](/graph-isomorphism-problem/).

## Reductions

- **To maximum clique**, via the association graph (above).
- **From clique**, by $G_1 = K_k$.
- **MCES to MCIS**, via line graphs and a check for the $K_3$ and $K_{1,3}$ exception.
- **To graph edit distance.** Bunke (1997) showed that a particular cost function makes the edit distance a function of the sizes of the graphs and of the maximum common subgraph.
- **From subgraph isomorphism.** $G_1$ is isomorphic to an induced subgraph of $G_2$ exactly when MCIS has $|V_1|$ vertices.

## Applications

- Chemistry: the largest common substructure of two molecules, for similarity searching, reaction mapping and structure-activity analysis.
- Bioinformatics: comparing protein structures and interaction networks.
- Computer vision and pattern recognition: matching scene graphs to models.
- Software engineering: detecting cloned code through program dependence graphs, and comparing versions of models.
- Computing the distance $1 - \frac{|\mathrm{mcs}|}{\max(|G_1|, |G_2|)}$, a metric on graphs proposed by Bunke and Shearer (1998).

## References
