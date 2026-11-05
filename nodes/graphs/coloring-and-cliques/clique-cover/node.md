---
tag: AZ9JHN
kind: problem
slug: clique-cover
name: Clique cover problem
aliases:
- minimum clique partition
area: graphs/coloring-and-cliques
level: core
summary: Partition the vertices into the fewest cliques; equivalent to coloring the complement graph.
prereqs: [clique, graph-coloring, complement-graph]
see_also: [graph-coloring, complement-graph, independent-set, perfect-graph, chordal-graph, edge-clique-cover, maximum-matching, bjorklund-chromatic-number]
sources:
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, Plenum (1972), 85 to 103
    locator: the list of 21 problems (Clique cover, reduced from Chromatic number)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A1.1, problem GT15, Partition into cliques
  - paper: doi:10.1137/0201013
    title: Fănică Gavril, Algorithms for minimum coloring, maximum clique, minimum covering by cliques, and maximum independent set of a chordal graph, SIAM Journal on Computing 1(2), 180 to 187 (1972)
    locator: the algorithm for minimum covering by cliques of a chordal graph
  - paper: doi:10.1016/0012-365X(72)90006-4
    title: László Lovász, Normal hypergraphs and the perfect graph conjecture, Discrete Mathematics 2(3), 253 to 267 (1972)
    locator: the main theorem (the complement of a perfect graph is perfect)
  - paper: doi:10.1016/S0304-0208(08)72943-8
    title: Martin Grötschel, László Lovász and Alexander Schrijver, Polynomial algorithms for perfect graphs, in Topics on Perfect Graphs, Annals of Discrete Mathematics 21, 325 to 356 (1984)
    locator: the polynomial algorithms for minimum coloring and minimum clique cover of a perfect graph
  - paper: doi:10.1137/070683933
    title: Andreas Björklund, Thore Husfeldt and Mikko Koivisto, Set partitioning via inclusion-exclusion, SIAM Journal on Computing 39(2), 546 to 563 (2009)
    locator: the O*(2^n) algorithm for the chromatic number, applied to the complement
---

The clique cover problem asks for a partition of the vertices of an undirected graph $G$ into as few [cliques](/clique/) as possible. The least number is the clique cover number $\theta(G)$. A set is a clique of $G$ exactly when it is an independent set of the [complement](/complement-graph/) $\overline G$, so a clique cover of $G$ is a proper [coloring](/graph-coloring/) of $\overline G$, and $\theta(G) = \chi(\overline G)$. The problem is NP-hard in general, and polynomial on triangle-free graphs, chordal graphs and perfect graphs.

## In plain words

Split a group of people into teams so that everybody in a team knows everybody else in that team. Use as few teams as you can.

Two people who do not know each other must be in different teams. So this is the coloring problem, turned inside out: draw a line between each pair of strangers, and color so that strangers get different colors. Each color is a team.

People who are all strangers to each other must all be in different teams. So the size of the largest group of strangers is a lower limit on the number of teams.

## Definition

Let $G = (V, E)$ be a finite simple undirected graph with $n$ vertices. A *clique cover* (or clique partition) of size $k$ is a partition $V = K_1 \cup \cdots \cup K_k$ in which each $K_i$ is a clique.

**Optimization version.** Input: $G$. Output: a clique cover of size $\theta(G)$, where

$$\theta(G) = \min \{ k : V \text{ has a partition into } k \text{ cliques} \}.$$

**Decision version.** Input: $G$ and $k$. Question: does $V$ have a partition into at most $k$ cliques?

Covering $V$ by cliques that may overlap gives the same minimum, because removing shared vertices from all but one clique leaves cliques. The name *clique cover* is also used for covering the edges by cliques, a different problem; see [edge clique cover](/edge-clique-cover/).

**Duality with independent sets.** An [independent set](/independent-set/) meets each clique in at most one vertex, so

$$\theta(G) \ge \alpha(G),$$

where $\alpha(G)$ is the independence number. This is the inequality $\chi(\overline G) \ge \omega(\overline G)$ seen in the complement.

## Variants

- **Fixed $k$.** $\theta(G) \le 1$ when $G$ is complete. $\theta(G) \le 2$ exactly when $\overline G$ is bipartite, decided in $O(n^2)$ time by the [bipartite test](/bipartite-graph-test/) on $\overline G$. $\theta(G) \le 3$ is NP-complete, as 3-coloring of $\overline G$.
- **Triangle-free graphs.** The only cliques are single vertices and edges, so a cover is a matching plus single vertices, and $\theta(G) = n - \nu(G)$, where $\nu$ is the size of a [maximum matching](/maximum-matching/).
- **Perfect graphs.** The complement of a [perfect graph](/perfect-graph/) is perfect (Lovász 1972), so $\theta(G) = \alpha(G)$, and a minimum cover is found in polynomial time (Grötschel, Lovász and Schrijver 1984).
- **Chordal graphs.** [Chordal graphs](/chordal-graph/) are perfect, and Gavril (1972) gives a direct linear-time algorithm.
- **Edge clique cover.** Cover the edges, not the vertices. See [edge clique cover](/edge-clique-cover/).

## Examples

| graph | $n$ | $\alpha$ | $\theta$ | a minimum cover |
|---|---|---|---|---|
| $K_n$ | $n$ | 1 | 1 | $V$ |
| $\overline{K_n}$, no edges | $n$ | $n$ | $n$ | single vertices |
| $C_5$ | 5 | 2 | 3 | $\{0,1\}, \{2,3\}, \{4\}$ |
| Petersen graph | 10 | 4 | 5 | a perfect matching |
| triangle strip $S$ below | 6 | 2 | 2 | $\{0,1,2\}, \{3,4,5\}$ |
| $S$ plus vertex 6 and edges $56$, $06$ | 7 | 3 | 3 | $\{0,6\}, \{1,2\}, \{3,4,5\}$ |

Here $S$ has vertices $0, \ldots, 5$ and edges $01, 02, 12, 13, 23, 24, 34, 35, 45$.

- $C_5$ shows that $\theta$ can exceed $\alpha$. It is triangle-free with $\nu = 2$, so $\theta = 5 - 2 = 3$.
- The Petersen graph is triangle-free and has a perfect matching, so $\theta = 10 - 5 = 5$, while $\alpha = 4$.
- $S$ is chordal, so $\theta(S) = \alpha(S) = 2$; $\{0, 5\}$ is an independent set of size 2.
- In $S$ plus vertex 6, the set $\{1, 4, 6\}$ is independent, so 3 cliques are needed, and the cover in the table uses 3.

## Known algorithms

- **Through coloring.** Build $\overline G$ in $O(n^2)$ time and color it with any exact or heuristic [coloring algorithm](/graph-coloring/). [Björklund's algorithm](/bjorklund-chromatic-number/) gives $\theta(G)$ in $O^*(2^n)$ time. Heuristics such as [DSATUR](/dsatur/) on $\overline G$ give a cover with no guarantee.
- **Triangle-free graphs.** A maximum matching, by Edmonds' blossom algorithm or [Hopcroft-Karp](/hopcroft-karp/) on bipartite graphs, gives an optimal cover: its edges plus the unmatched vertices.
- **Chordal graphs (Gavril 1972).** Take a [perfect elimination ordering](/perfect-elimination-ordering/) $v_1, \ldots, v_n$. Scan it, and each time the current vertex $v$ is still uncovered, form the clique of $v$ and its uncovered later neighbors, and mark them covered. The chosen vertices $v$ are pairwise non-adjacent, so the number of cliques equals the size of an independent set, and the cover is optimal. It runs in $O(n + m)$ time.
- **Perfect graphs.** The ellipsoid method on the Lovász theta function gives $\alpha(G)$ and a minimum cover in polynomial time.

## Bounds

- **NP-hardness.** The decision version is NP-complete (Karp 1972; Garey and Johnson, problem GT15). It stays NP-complete for $k = 3$, since $G \mapsto \overline G$ maps 3-coloring to it.
- **Exact.** $O^*(2^n)$ time through the complement and Björklund, Husfeldt and Koivisto (2009).
- **Approximation.** Approximating $\chi$ within $n^{1 - \varepsilon}$ is NP-hard, and complementing preserves $n$, so the same holds for $\theta$.
- **Lower bound.** $\theta(G) \ge \alpha(G)$ and $\theta(G) \ge n / \omega(G)$. For perfect graphs the first holds with equality.

## Reductions

- **To and from coloring.** $\theta(G) \le k$ exactly when $\chi(\overline G) \le k$. The map $G \mapsto \overline G$ takes $O(n^2)$ time and is its own inverse, so the two problems are equivalent under polynomial reductions.
- **To set partition.** A clique cover is a partition of $V$ into members of the family of cliques; the inclusion-exclusion method for set partitioning counts such partitions.
- **To matching.** On triangle-free graphs, $\theta(G) = n - \nu(G)$ reduces the problem to maximum matching.

## Applications

- **Grouping compatible items.** When an edge means "may share a resource", the cliques are groups that can share it, and $\theta$ is the least number of groups.
- **Registers and channels.** Compatibility graphs in circuit synthesis are partitioned into cliques to share hardware units.
- **Clustering.** Partitioning a similarity graph into cliques is the exact form of a clustering in which each cluster is fully connected.
- **Lower bounds for coloring.** $\theta(G) \ge \alpha(G)$ and $\chi(G) \ge n / \alpha(G)$ connect covers of $G$ with colorings of $G$ in proofs about perfect graphs.

## References
