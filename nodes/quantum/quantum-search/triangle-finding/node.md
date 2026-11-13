---
tag: 6MA4JK
kind: problem
slug: triangle-finding
name: Triangle finding
aliases:
- triangle detection
area: quantum/quantum-search
level: research
summary: "Find a triangle in an n-vertex graph, or report none, with queries to its adjacency matrix. Quantum query bounds lie between Ω(n) and Õ(n^(5/4)); classical algorithms need Θ(n^2)."
prereqs: [graph, adjacency-matrix, quantum-query-model, quantum-oracle]
see_also: [magniez-santha-szegedy-triangle, triangle-detection-hypothesis, triangle-counting, negative-triangle, boolean-matrix-multiplication, quantum-query-complexity, ambainis-element-distinctness, triangle-listing-by-degree]
sources:
  - paper: doi:10.1137/050643684
    title: "Frédéric Magniez, Miklos Santha and Mario Szegedy, Quantum algorithms for the triangle problem, SIAM Journal on Computing 37(2), 2007, pages 413-424"
    locator: with the numbering of arXiv:quant-ph/0310134 version 3, Section 1 (the problem, the lower bound Omega(n) and the limit of the adversary method for small certificates), Theorem 1 (Õ(n^(10/7))), Theorem 4 (Õ(n^(13/10))) and Theorem 5 (fixed subgraphs)
  - paper: doi:10.1137/S0097539702402780
    title: "Harry Buhrman, Christoph Dürr, Mark Heiligman, Peter Høyer, Frédéric Magniez, Miklos Santha and Ronald de Wolf, Quantum algorithms for element distinctness, SIAM Journal on Computing 34(6), 2005, pages 1324-1330"
    locator: the triangle result (O(n + sqrt(n m)) queries for a graph with m edges); a general locator
  - paper: doi:10.1145/2213977.2213985
    title: "Aleksandrs Belovs, Span programs for functions with constant-sized 1-certificates, Proceedings of the 44th ACM STOC, 2012, pages 77-84"
    locator: the abstract (O(n^(35/27)) queries by a learning graph), arXiv:1105.4024
  - paper: doi:10.1137/1.9781611973105.107
    title: "Troy Lee, Frédéric Magniez and Miklos Santha, Improved quantum query algorithms for triangle finding and associativity testing, Proceedings of the 24th ACM-SIAM SODA, 2013, pages 1486-1502"
    locator: the main result (O(n^(9/7)) queries); a general locator
  - paper: doi:10.1137/1.9781611973105.106
    title: "Stacey Jeffery, Robin Kothari and Frédéric Magniez, Nested quantum walks with quantum data structures, Proceedings of the 24th ACM-SIAM SODA, 2013, pages 1474-1485"
    locator: the abstract (nested walks reproduce O(n^(35/27)) and O(n^(9/7)) up to logarithmic factors), arXiv:1210.1199
  - paper: doi:10.1109/FOCS.2014.31
    title: "François Le Gall, Improved quantum algorithm for triangle finding via combinatorial arguments, Proceedings of the 55th IEEE FOCS, 2014, pages 216-225"
    locator: the abstract (Õ(n^(5/4)) queries, and the lower bounds Omega(n^(9/7)/sqrt(log n)) of Belovs and Rosmanis for non-adaptive learning graphs), arXiv:1407.0085
  - paper: doi:10.1137/S0097539796300933
    title: "Charles H. Bennett, Ethan Bernstein, Gilles Brassard and Umesh Vazirani, Strengths and weaknesses of quantum computing, SIAM Journal on Computing 26(5), 1997, pages 1510-1523"
    locator: the lower bound Omega(sqrt(N)) for search, used for Omega(n) here
  - paper: doi:10.1109/FOCS.2010.67
    title: "Virginia Vassilevska Williams and Ryan Williams, Subcubic equivalences between path, matrix and triangle problems, Proceedings of the 51st IEEE FOCS, 2010, pages 645-654"
    locator: the equivalences of the triangle test with Boolean matrix multiplication for combinatorial algorithms, and of negative triangle with all-pairs shortest paths; a general locator (journal version JACM 65(5), 2018)
---

Triangle finding asks for three vertices of a graph that are pairwise adjacent, or for the answer "none", when the graph can be read only through queries to its adjacency matrix. This quantum page is about query complexity in the [quantum query model](/quantum-query-model/): a classical algorithm needs $\Theta(n^2)$ queries on $n$ vertices, [Grover search](/grover-search/) over all triples needs $O(n^{3/2})$, and the best known quantum algorithm needs $\tilde O(n^{5/4})$, while the best lower bound is $\Omega(n)$. This page is the problem; the first walk-based algorithm, with $\tilde O(n^{13/10})$ queries, is [Magniez-Santha-Szegedy triangle finding](/magniez-santha-szegedy-triangle/). For the time of classical algorithms see the [triangle detection hypothesis](/triangle-detection-hypothesis/) and [triangle counting](/triangle-counting/).

## In plain words

A group of people is given, and you want three who all know each other. You can only ask one question at a time: "do these two know each other?". A classical method must ask about almost every pair, because a single unasked pair could close the only triangle. A quantum method can ask about many pairs at once in superposition. It still needs at least as many questions as there are people, and the best methods need a little more. Since 2003 a series of quantum methods has lowered the number of questions, but no one knows the true cost. It lies between the number of people and that number to the power one and a quarter.

## Definition

**Input.** A simple undirected graph $G$ on the vertex set $[n] = \{1, \ldots, n\}$, given by the bit oracle $O_G|u, v\rangle|b\rangle = |u, v\rangle|b \oplus [uv \in E]\rangle$, which reads one entry of the [adjacency matrix](/adjacency-matrix/). The phase form of the oracle is equivalent, with one query, by [phase kickback](/phase-kickback/).

**Output.** A triangle, three vertices $u, v, w$ with $uv, vw, uw \in E$, if there is one, and "none" otherwise. The decision version only asks whether a triangle exists.

**Cost.** The number of oracle calls, with bounded error (success probability at least $2/3$). See [quantum query complexity](/quantum-query-complexity/). The bounds below are stated for $n \to \infty$.

A query bound is not a time bound. The query algorithms keep large data, such as the edges inside a set of vertices, in quantum registers, and a fast step needs [quantum random access memory](/quantum-random-access-memory/) or a quantum data structure.

## Variants

- **Sparse graphs.** The bounds can be stated in terms of $n$ and the number $m$ of edges.
- **Adjacency lists.** Queries can read the $i$-th neighbor of a vertex instead of one matrix entry; the bounds then differ.
- **Edge weights.** In the weighted form, a triangle must have weight below a threshold, as in [negative triangle](/negative-triangle/). It is harder in the query model; see the bounds.
- **Counting and listing.** Classical algorithms that count or list all triangles are on [triangle counting](/triangle-counting/) and [triangle listing by degree](/triangle-listing-by-degree/).
- **Fixed subgraphs.** Find a copy of a fixed graph $H$ on $k$ vertices, for example a $k$-clique. The same methods apply with other exponents.

## Examples

- **The complete graph $K_4$.** Every three of the four vertices form a triangle, so there are 4 triangles.
- **The cycle $C_5$.** No three vertices are pairwise adjacent, and the answer is "none".
- **A hidden edge.** Take the complete bipartite graph $K_{3,3}$ with parts $\{1, 2, 3\}$ and $\{4, 5, 6\}$; it has no triangle. Add the edge $12$: then $1, 2, 4$ is a triangle, and so are $1, 2, 5$ and $1, 2, 6$. An algorithm must find out whether one of the 6 pairs inside a part is an edge. For large $n$ this is a search over about $n^2/4$ pairs, which gives the lower bounds below.

## Known algorithms

| algorithm | queries | notes |
|---|---|---|
| classical, read the whole matrix | $n(n-1)/2$ | optimal for classical queries |
| Grover search over triples | $O(n^{3/2})$ | [Grover search](/grover-search/) on $\binom{n}{3}$ items |
| Buhrman et al. (2001, SICOMP 2005) | $O(n + \sqrt{nm})$ | better than $n^{3/2}$ only for sparse graphs |
| Magniez, Santha and Szegedy, combinatorial | $\tilde O(n^{10/7})$ | Grover search only, $O(\log n)$ qubits in the quantum parts |
| [Magniez, Santha and Szegedy](/magniez-santha-szegedy-triangle/) (2003, SODA 2005) | $\tilde O(n^{13/10})$ | nested quantum walk |
| Belovs (STOC 2012) | $O(n^{35/27})$ | learning graph, about $n^{1.296}$ |
| Lee, Magniez and Santha (SODA 2013) | $O(n^{9/7})$ | learning graph, about $n^{1.286}$ |
| Jeffery, Kothari and Magniez (SODA 2013) | $\tilde O(n^{9/7})$ | nested walks with quantum data structures |
| Le Gall (FOCS 2014) | $\tilde O(n^{5/4})$ | quantum walks with combinatorial arguments |

All quantum entries are bounded-error query counts. The walk algorithms use the framework of [quantum walk search](/quantum-walk-search/) on sets of vertices, like the element distinctness walk of [Ambainis](/ambainis-element-distinctness/).

## Bounds

| bound | source | model and error |
|---|---|---|
| $\Theta(n^2)$ | the hidden edge example | classical queries, deterministic or randomized |
| $\Omega(n)$ | search over the $\Theta(n^2)$ pairs of the hidden edge example, by [Grover optimality](/grover-optimality/) | quantum queries, bounded error |
| $\tilde O(n^{5/4})$ | Le Gall (2014) | quantum queries, bounded error |
| $\Omega(n^{9/7}/\sqrt{\log n})$ | Belovs and Rosmanis, as cited by Le Gall | quantum queries for the edge-weighted form; for the unweighted form, only for non-adaptive learning graphs |

For the classical bound, an algorithm that has not read some pair inside a part of the hidden edge example cannot tell whether that pair is an edge, and a randomized algorithm must read a constant fraction of the $n^2/4$ pairs. For the quantum bound, a triangle exists exactly when one of these pairs is an edge, so the problem contains search over $\Theta(n^2)$ items, which needs $\Omega(\sqrt{n^2}) = \Omega(n)$ queries.

The gap between $\Omega(n)$ and $\tilde O(n^{5/4})$ is open. A triangle has a certificate of only 3 edges, and Magniez, Santha and Szegedy note that the positive-weight adversary methods cannot prove more than $O(\sqrt{n^2 \cdot 3}) = O(n)$ for such a problem. The general adversary bound is tight for every problem, so a better lower bound would need it, or the [polynomial method](/polynomial-method/).

## Reductions

- **Search to triangle finding.** The hidden edge example embeds search over $\Theta(n^2)$ items, which gives $\Omega(n)$.
- **Triangle finding to element distinctness.** A walk on sets of vertices, as for element distinctness, finds a set that holds an edge of a triangle. A direct use gives no better bound than $O(n^{3/2})$; the gain needs a cheaper check, such as graph collision.
- **Boolean matrix multiplication.** $G$ has a triangle exactly when some entry of $A^2$ and the same entry of $A$ are both nonzero, so a fast [Boolean matrix multiplication](/boolean-matrix-multiplication/) gives a classical algorithm in time $O(n^\omega)$. For combinatorial algorithms, a truly subcubic test for a triangle and a truly subcubic Boolean matrix multiplication are equivalent (Vassilevska Williams and Williams, 2010).
- **Negative triangle and shortest paths.** The weighted form, [negative triangle](/negative-triangle/), is equivalent to all-pairs shortest paths for subcubic time; see [APSP and negative triangle](/apsp-negative-triangle-equivalence/).

## Applications

- A test problem for quantum query methods. Triangle finding led to nested quantum walks, to learning graphs for problems with small certificates, and to quantum data structures for walks.
- Fixed subgraph finding and monotone graph properties with small certificates use the same methods.
- Associativity testing of a binary operation, studied in the paper of Lee, Magniez and Santha with the same tools.

## References
