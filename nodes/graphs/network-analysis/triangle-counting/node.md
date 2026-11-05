---
tag: YST4ZA
kind: problem
slug: triangle-counting
name: Triangle counting
aliases:
- Triangle counting and listing
- triangle enumeration
area: graphs/network-analysis
level: core
summary: Count the triangles in a graph, globally or per node.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(m^(3/2))}
prereqs: [graph, adjacency-list, degree, adjacency-matrix]
see_also: [triangle-listing-by-degree, compact-forward-algorithm, clustering-coefficient, triadic-closure, triangle-detection-hypothesis, boolean-matrix-multiplication, arboricity, network-motif-enumeration]
sources:
  - paper: doi:10.1137/0214017
    title: Norishige Chiba and Takao Nishizeki, Arboricity and subgraph listing algorithms, SIAM Journal on Computing 14(1), 210 to 223 (1985)
    locator: the lemma that the sum over the edges of the smaller end degree is at most 2a(G)m, and the triangle listing algorithm in O(a(G)m) time
  - paper: doi:10.1137/0207033
    title: Alon Itai and Michael Rodeh, Finding a minimum circuit in a graph, SIAM Journal on Computing 7(4), 413 to 423 (1978)
    locator: the triangle finding methods, by matrix multiplication and in O(m^(3/2)) time
  - paper: doi:10.1007/BF02523189
    title: Noga Alon, Raphael Yuster and Uri Zwick, Finding and counting given length cycles, Algorithmica 17(3), 209 to 223 (1997)
    locator: the triangle counting algorithm in O(m^(2ω/(ω+1))) time, which splits the vertices by degree
  - paper: doi:10.1016/j.tcs.2008.07.017
    title: Matthieu Latapy, Main-memory triangle computations for very large (sparse (power-law)) graphs, Theoretical Computer Science 407(1-3), 458 to 473 (2008)
    locator: the survey of the listing algorithms (node iterator, edge iterator, forward, compact-forward) and their costs
  - paper: doi:10.1145/3186893
    title: Virginia Vassilevska Williams and R. Ryan Williams, Subcubic equivalences between path, matrix, and triangle problems, Journal of the ACM 65(5), article 27 (2018)
    locator: the equivalence of Boolean matrix multiplication and triangle detection for combinatorial algorithms with a truly subcubic running time
---

Triangle counting asks for the number of triangles of an undirected graph, that is, of sets of three vertices that are pairwise adjacent, either in total or for each vertex. The listing version asks for the triangles themselves. Both are solved in $O(m^{3/2})$ time on a graph with $m$ edges by [listing by degree order](/triangle-listing-by-degree/), which is optimal for listing because a graph can have $\Theta(m^{3/2})$ triangles. Triangle counts are the core of the [clustering coefficient](/clustering-coefficient/) and of transitivity in network analysis.

## In plain words

A triangle is three people who all know each other. The problem asks how many such groups a network has, or how many each person belongs to.

Testing every group of three people works, but the number of groups grows with the cube of the number of people, which is far too many for a large network. A better method looks only at pairs of friends and checks which friends they share. The best methods visit each friendship once and keep the lists they compare short, by handling the people with many friends in a careful order.

Counting triangles tells you how cliquish a network is. Social networks have many more triangles than random networks of the same size.

## Definition

**Input.** A simple undirected graph $G = (V, E)$ without weights, with $n = |V|$ and $m = |E|$, given by [adjacency lists](/adjacency-list/) or an [adjacency matrix](/adjacency-matrix/). There are no self-loops and no repeated edges. The graph need not be connected.

**Output.** A *triangle* is a set $\{a, b, c\} \subseteq V$ of three distinct vertices with $\{a, b\}, \{b, c\}, \{a, c\} \in E$. The *global count* is

$$T(G) = \bigl|\{\{a, b, c\} : \{a, b, c\} \text{ is a triangle}\}\bigr|,$$

and the *local count* of $v$ is the number $t(v)$ of triangles that contain $v$. Since each triangle has three vertices, $\sum_v t(v) = 3T(G)$.

**The matrix form.** With $A$ the adjacency matrix,

$$t(v) = \tfrac12 (A^3)_{vv}, \qquad T(G) = \tfrac16 \operatorname{tr}(A^3).$$

*Proof.* $(A^3)_{vv} = \sum_{x, y} A_{vx} A_{xy} A_{yv}$ counts the closed walks $v, x, y, v$ of length 3. There are no self-loops, so $x \ne v$, $y \ne x$ and $v \ne y$; so $\{v, x, y\}$ is a triangle that contains $v$. Conversely each triangle $\{v, x, y\}$ gives exactly two such walks from $v$: through $x$ first or through $y$ first. So $(A^3)_{vv} = 2t(v)$, and summing over $v$ gives $\operatorname{tr}(A^3) = 2 \cdot 3T(G)$. $\square$

**Directed graphs and weights.** For a directed graph, the usual practice is to count the triangles of the underlying undirected graph, and then to classify each one by the directions of its arcs: a cyclic triangle has $a \to b \to c \to a$, and a transitive one has $a \to b \to c$ with $a \to c$. Weights play no role in whether a triangle exists. Weighted versions of the clustering coefficient use weights on the triangles found, and the minimum-weight triangle is the separate [negative triangle](/negative-triangle/) problem.

## Variants

- **Detection.** Decide whether $T(G) > 0$, and output one triangle if there is one. This decision version has the tightest known connections to matrix multiplication.
- **Counting.** Compute $T(G)$, or all the $t(v)$. The $t(v)$ give the local [clustering coefficient](/clustering-coefficient/) $C(v) = t(v)/\binom{d(v)}{2}$.
- **Listing.** Output every triangle once. The output size $T(G)$ is a lower bound on the time.
- **Per-edge counts.** For each edge $\{u, v\}$, count $|N(u) \cap N(v)|$. This is the support used by the $k$-truss and by the [neighbourhood overlap](/weak-ties/) of an edge.
- **Approximate counting.** Estimate $T(G)$ within a factor $1 \pm \varepsilon$, by sampling wedges or edges, or in one pass over a stream of edges ([streaming triangle counting](/streaming-triangle-counting-problem/)).
- **Distributed and parallel.** Count on a graph split across machines ([distributed triangle enumeration](/distributed-triangle-enumeration/)).

## Examples

Take the vertices 0 to 5 and the 10 edges $\{0,1\}$, $\{0,2\}$, $\{0,3\}$, $\{0,4\}$, $\{0,5\}$, $\{1,2\}$, $\{1,5\}$, $\{2,3\}$, $\{2,4\}$, $\{3,4\}$. The degrees are $5, 3, 4, 3, 3, 2$. The six triangles are

$$\{0,1,2\}, \{0,1,5\}, \{0,2,3\}, \{0,2,4\}, \{0,3,4\}, \{2,3,4\}.$$

| $v$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $t(v)$ | 5 | 2 | 4 | 3 | 3 | 1 |
| $\binom{d(v)}{2}$ | 10 | 3 | 6 | 3 | 3 | 1 |

The local counts sum to $18 = 3 \cdot 6$, and $\operatorname{tr}(A^3) = 36 = 6 \cdot 6$. There are $\sum_v \binom{d(v)}{2} = 26$ paths of length 2, so the transitivity is $18/26 = 9/13 \approx 0.692$.

**Standard graphs.**

- The [complete graph](/complete-graph/) $K_k$ has $\binom{k}{3}$ triangles and $\binom{k}{2}$ edges. With $m = \binom{k}{2}$, $T = \Theta(m^{3/2})$, so the bound $O(m^{3/2})$ is reached.
- A [tree](/tree/), a [bipartite graph](/bipartite-graph/) and a cycle of length at least 4 have $T = 0$.
- The wheel with a hub and a cycle of $k \ge 4$ rim vertices has $T = k$, all through the hub, and $t(\text{hub}) = k$.
- In $G(n, p)$, the expected count is $\binom{n}{3} p^3$.

## Known algorithms

| algorithm | time | notes |
|---|---|---|
| test every triple | $\Theta(n^3)$ | the definition |
| node iterator: test each pair of neighbours of each vertex | $O(\sum_v d(v)^2)$ | slow on a vertex of huge degree |
| [listing by degree order](/triangle-listing-by-degree/) | $O(m^{3/2})$, and $O(a(G)\, m)$ | orient each edge toward the higher degree |
| [compact-forward](/compact-forward-algorithm/) | $O(m^{3/2})$ | merges sorted lists, no extra lists |
| Chiba and Nishizeki | $O(a(G)\, m)$ | $a(G)$ is the [arboricity](/arboricity/); linear on planar graphs |
| [matrix multiplication](/matrix-multiplication-exponent/) | $O(n^\omega)$ | counts via $\operatorname{tr}(A^3)$ |
| Alon, Yuster and Zwick | $O(m^{2\omega/(\omega+1)})$ | degree split plus matrix product for the high-degree part |

Here $\omega < 2.372$ is the exponent of matrix multiplication. With $\omega = 3$, the bound of Alon, Yuster and Zwick is $O(m^{3/2})$. The degree-ordered methods also count: add one to a counter of each vertex of each triangle found.

## Bounds

- **Listing.** A graph with $m$ edges has at most $\frac{\sqrt 2}{3} m^{3/2}$ triangles. Proof: let $\lambda_1 \ge \cdots \ge \lambda_n$ be the eigenvalues of the symmetric matrix $A$. Then $\sum_i \lambda_i^2 = \operatorname{tr}(A^2) = 2m$, so $|\lambda_i| \le \sqrt{2m}$, and $6T = \operatorname{tr}(A^3) = \sum_i \lambda_i^3 \le \sqrt{2m} \sum_i \lambda_i^2 = (2m)^{3/2}$. The clique reaches this order, so $\Theta(m^{3/2})$ is the worst-case cost of listing, and the degree-ordered methods are optimal in the worst case. In terms of the [arboricity](/arboricity/): an edge $\{u, v\}$ lies in at most $\min(d(u), d(v))$ triangles, each triangle has three edges, and Chiba and Nishizeki proved $\sum_{\{u,v\} \in E} \min(d(u), d(v)) \le 2a(G)\, m$; so $T(G) \le \tfrac23 a(G)\, m$.
- **Detection and counting.** No algorithm faster than $O(\min(n^\omega, m^{2\omega/(\omega+1)}))$ is known. The [triangle detection hypothesis](/triangle-detection-hypothesis/) conjectures that detection on graphs with $m$ edges needs $m^{4/3 - o(1)}$ time, which matches this bound if $\omega = 2$. No unconditional superlinear lower bound is known in the word RAM.
- **Combinatorial algorithms.** For algorithms that avoid fast matrix multiplication, no method with $O(n^{3 - \delta})$ time for a fixed $\delta > 0$ is known, and Vassilevska Williams and Williams showed that one would give such a method for [Boolean matrix multiplication](/boolean-matrix-multiplication/).

## Reductions

- **To matrix multiplication.** $T(G) = \operatorname{tr}(A^3)/6$, so counting reduces to two products of $n \times n$ integer matrices. Detection reduces to one Boolean product $A^2$ followed by a check of $A^2 \wedge A$.
- **From Boolean matrix multiplication.** Vassilevska Williams and Williams proved that triangle detection and Boolean matrix multiplication are equivalent under subcubic reductions for combinatorial algorithms: a truly subcubic algorithm for one gives one for the other.
- **The weighted version.** Finding a triangle of negative total weight is equivalent to [all-pairs shortest paths](/all-pairs-shortest-paths/) under subcubic reductions ([the equivalence](/apsp-negative-triangle-equivalence/)).
- **To clustering.** The [clustering coefficient](/clustering-coefficient/) and the transitivity are computed from the $t(v)$ and the degrees in $O(n)$ more time.

## Applications

- [Clustering coefficient](/clustering-coefficient/) and transitivity, the measures of [triadic closure](/triadic-closure/) in social networks.
- [Network motif](/network-motif/) analysis: the triangle is the motif of size 3 that is most often over-represented.
- Community detection: dense groups have many triangles, and the $k$-truss and several clustering methods use triangle counts per edge.
- Spam and anomaly detection: the local triangle count of a vertex, compared with its degree, separates real accounts and pages from generated ones.
- Database joins: listing triangles is the join of three binary relations $R(a, b) \bowtie S(b, c) \bowtie T(a, c)$, the standard example for worst-case optimal join algorithms.

## References
