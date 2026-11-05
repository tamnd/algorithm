---
tag: 8X75AV
kind: problem
slug: subgraph-isomorphism
name: Subgraph isomorphism
aliases:
- induced subgraph isomorphism
- subgraph isomorphism problem
area: graphs/graph-isomorphism
level: intro
summary: Decide whether a pattern graph occurs as a subgraph, or as an induced subgraph, of a host graph; NP-complete in general, polynomial for a fixed pattern.
model: word-ram
complexity:
  vars: {n: the number of vertices of the host graph, k: the number of vertices of the pattern}
  time: {worst: O(n^k k^2)}
prereqs: [graph-isomorphism-definition, subgraph, induced-subgraph, np-complete]
see_also: [ullmann-algorithm, vf2-algorithm, graph-isomorphism-problem, maximum-common-subgraph, clique-problem, hamiltonian-cycle, color-coding, network-motif]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 3.2.1 (the NP-completeness of subgraph isomorphism by restriction to clique) and Appendix A1.4, Subgraph isomorphism and Largest common subgraph
  - paper: doi:10.1145/321921.321925
    title: J. R. Ullmann, An algorithm for subgraph isomorphism, Journal of the ACM 23(1), 31 to 42 (1976)
    locator: the whole paper (backtracking with refinement of the candidate matrix)
  - paper: doi:10.1145/210332.210337
    title: Noga Alon, Raphael Yuster and Uri Zwick, Color-coding, Journal of the ACM 42(4), 844 to 856 (1995)
    locator: the whole paper (patterns of bounded treewidth, and paths and cycles of length k)
  - paper: doi:10.7155/jgaa.00014
    title: David Eppstein, Subgraph isomorphism in planar graphs and related problems, Journal of Graph Algorithms and Applications 3(3), 1 to 27 (1999)
    locator: the whole paper (linear time for a fixed pattern in a planar host)
---

Subgraph isomorphism asks whether a pattern graph $H$ occurs inside a host graph $G$: whether there is an injective map from the vertices of $H$ to the vertices of $G$ that sends each edge of $H$ to an edge of $G$. In the induced version the map must also send non-edges to non-edges. The problem is [NP-complete](/np-complete/), because it contains the [clique problem](/clique-problem/) and the [Hamiltonian cycle problem](/hamiltonian-cycle/) as special cases; for a pattern of fixed size it takes polynomial time. It is the core of graph pattern matching in chemistry, biology and graph databases, and practical solvers such as [Ullmann's algorithm](/ullmann-algorithm/) and [VF2](/vf2-algorithm/) solve it by backtracking.

## In plain words

You have a small drawing, the pattern, and a large network, the host. You want to know whether the pattern appears somewhere in the network: whether you can place each point of the pattern on a different point of the network so that every line of the pattern lands on a line of the network. The network may have extra lines between the chosen points; if you forbid those extra lines, you ask for an induced copy. Checking a proposed placement is easy. Finding one can take a very long time, because a pattern can be as hard as "a group where everyone knows everyone" or "a round trip through all points".

## Definition

Graphs are simple and undirected unless a variant says otherwise. Let $H = (V_H, E_H)$ with $|V_H| = k$ be the pattern and $G = (V_G, E_G)$ with $|V_G| = n$ the host.

**Subgraph isomorphism (non-induced).**
- Input: $H$ and $G$.
- Output: yes when there is an injective map $\varphi : V_H \to V_G$ with
$$\{u, v\} \in E_H \implies \{\varphi(u), \varphi(v)\} \in E_G \quad \text{for all } u, v \in V_H;$$
otherwise no. Such a $\varphi$ is a *monomorphism*, or an *embedding*; $H$ is then isomorphic to a subgraph of $G$.

**Induced subgraph isomorphism.** The same, with $\iff$ in place of $\implies$. Then $H$ is isomorphic to the [induced subgraph](/induced-subgraph/) $G[\varphi(V_H)]$.

The search version asks for one $\varphi$; the enumeration version lists all of them; the counting version counts them. When $k = n$ and $|E_H| = |E_G|$, both versions become [graph isomorphism](/graph-isomorphism-problem/).

## Variants

- **Directed, colored and labeled graphs.** The map must keep arc directions, vertex colors and edge labels. Chemistry and graph databases use labels; the algorithms are the same, with label checks added to each feasibility test.
- **Fixed pattern.** For each fixed $H$, the problem is polynomial: try all $O(n^k)$ maps. Its fine-grained complexity depends on $H$: for $H = K_k$ it is $k$-clique, for a path or cycle of length $k$ color coding gives $2^{O(k)} \cdot n^{O(1)}$ time.
- **Parameterized by $k$.** The problem is W[1]-hard, since $k$-clique is a special case.
- **Restricted hosts.** For a fixed pattern and a planar host, linear time (Eppstein 1999); more generally on hosts of bounded expansion. If both graphs are trees, polynomial ([subtree isomorphism](/tree-isomorphism/)). If the pattern is a forest and the host a tree, NP-complete.
- **Homomorphism.** Drop injectivity. A homomorphism from $K_3$ to $G$ exists exactly when $G$ has a triangle, and a homomorphism from $H$ to the host $K_3$ exists exactly when $H$ is [3-colorable](/three-coloring/).
- **Maximum common subgraph.** The optimization problem of finding the largest graph that embeds in both; see [maximum common subgraph](/maximum-common-subgraph/).

## Examples

| pattern $H$ | host $G$ | non-induced embeddings | induced embeddings |
|---|---|---|---|
| path $P_3$ (3 vertices) | cycle $C_5$ | 10 | 10 |
| cycle $C_4$ | complete graph $K_4$ | 24 | 0 |
| cycle $C_5$ | Petersen graph | 120 | 120 |
| triangle $K_3$ | Petersen graph | 0 | 0 |

The $C_4$ row shows the difference: every injective map of the 4-cycle into $K_4$ keeps the edges, but $K_4$ has the two diagonals, which the 4-cycle lacks, so no copy is induced. The Petersen graph has 12 five-cycles, and each gives 10 embeddings (5 rotations times 2 directions); its girth is 5, so it has no triangle.

**Reductions as examples.** With $H = K_k$, the question "is $K_k$ a subgraph of $G$" is the clique problem. With $H = C_n$, the cycle on all $n$ vertices of $G$, it is the Hamiltonian cycle problem.

## Known algorithms

| algorithm | handles | worst-case time |
|---|---|---|
| brute force over injective maps | both versions | $O(n^k k^2)$ |
| [Ullmann's algorithm](/ullmann-algorithm/) (1976) | non-induced, induced with a change | exponential; refinement prunes well |
| [VF2](/vf2-algorithm/) (2004) and VF3 | both versions, mainly induced | exponential; little memory |
| [Color coding](/color-coding/) (Alon, Yuster and Zwick 1995) | patterns of treewidth $t$ | $2^{O(k)} n^{t+1} \log n$, randomized or derandomized |
| matrix multiplication (Nešetřil and Poljak 1985) | $H = K_k$ | $O(n^{\omega k / 3})$ for $k$ divisible by 3 |
| Eppstein (1999) | planar host, fixed pattern | $O(n)$ for each fixed $k$ |
| constraint solvers (Glasgow Subgraph Solver, RI) | both versions | exponential, fast in practice |

For [maximum clique](/maximum-clique/) as a special case, see [Bron-Kerbosch](/bron-kerbosch/).

## Bounds

- **NP-complete.** The problem is in [NP](/np/) (the map is a certificate checked in $O(k^2)$ time), and it is NP-hard because clique is the special case $H = K_k$ (Garey and Johnson, Section 3.2.1; Cook 1971 already treated the subgraph problem).
- **Upper bound.** $O(n^k k^2)$ by brute force: $n(n-1)\cdots(n-k+1)$ injective maps, each checked against all pattern pairs.
- **Conditional lower bound.** Under the exponential time hypothesis, $k$-clique has no $f(k) \cdot n^{o(k)}$ algorithm (Chen and others, 2006), so subgraph isomorphism has none either. Brute force is optimal up to the constant in the exponent for general patterns.
- **Graph isomorphism contrast.** When $|V_H| = |V_G|$ and $|E_H| = |E_G|$ the problem is graph isomorphism, which is not believed to be NP-complete; the hardness comes from the freedom of choosing where the pattern sits.

## Reductions

- **From clique** ($H = K_k$) and **from Hamiltonian cycle** ($H = C_n$): each is a special case, so subgraph isomorphism is NP-hard, and the reductions are linear.
- **Induced version:** with $H = K_k$ it is again clique, so it is NP-hard too; with $H = \overline{K_k}$ (no edges) it is [independent set](/independent-set/).
- **To SAT and constraint satisfaction:** one variable per pattern vertex with domain $V_G$, an all-different constraint, and one binary constraint per pattern edge. This is how modern solvers model it.
- **To clique in the association graph:** the [maximum common subgraph](/maximum-common-subgraph/) reduction of Barrow and Burstall turns the induced version into finding a $k$-clique in a graph with $kn$ vertices.

## Applications

- Searching chemical databases for molecules that contain a given substructure, with atom and bond labels.
- Querying graph databases with patterns (Cypher and SPARQL basic graph patterns are subgraph queries with labels).
- Counting [network motifs](/network-motif/) in biological and social networks.
- Finding instances of circuit cells in netlists, and of code patterns in program graphs.
- Computer vision with relational models of objects.

## References
