---
tag: 78KW1X
kind: algorithm
slug: walktrap-algorithm
name: Walktrap algorithm
aliases:
- Walktrap
area: graphs/network-analysis
level: advanced
summary: Agglomerative clustering where nodes close in short random-walk distance merge.
solves: [community-detection]
model: real-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, t: the walk length}
  time: {worst: O(m n^2 + t n (n + m))}
  space: {extra: O(n^2)}
properties: {directed: false, weighted: true, deterministic: true, recursive: false}
history:
  year: 2005
  people: [Pascal Pons, Matthieu Latapy]
  note: Pons and Latapy presented Walktrap at ISCIS 2005 and in the Journal of Graph Algorithms and Applications in 2006, combining a random-walk distance between vertices with Ward's agglomerative clustering.
prereqs: [community-detection, modularity, markov-chain, ward-method]
see_also: [community-detection, modularity, ward-method, agglomerative-clustering, louvain-method, girvan-newman-algorithm, spectral-clustering, dendrogram]
sources:
  - paper: doi:10.7155/jgaa.00124
    title: Pascal Pons and Matthieu Latapy, Computing communities in large networks using random walks, Journal of Graph Algorithms and Applications 10(2), 191 to 218 (2006)
    locator: Section 2 (the distance r between vertices and communities), Section 3 (the merging by the increase of sigma, Theorem 3 and the update formulas of Theorem 4, and the choice of the partition by modularity), and Section 4 (the complexity analysis)
  - paper: doi:10.1080/01621459.1963.10500845
    title: Joe H. Ward Jr., Hierarchical grouping to optimize an objective function, Journal of the American Statistical Association 58(301), 236 to 244 (1963)
    locator: the agglomerative method that merges at each step the two groups whose union increases the within-group sum of squares the least
  - paper: doi:10.1103/PhysRevE.69.026113
    title: M. E. J. Newman and M. Girvan, Finding and evaluating community structure in networks, Physical Review E 69(2), 026113 (2004)
    locator: the definition of modularity Q, used to choose a level of a dendrogram
  - paper: doi:10.1016/j.physrep.2009.11.002
    title: Santo Fortunato, Community detection in graphs, Physics Reports 486(3 to 5), 75 to 174 (2010)
    locator: Section 8.2, dynamic algorithms based on random walks, including Walktrap
---

Walktrap is a [community detection](/community-detection/) algorithm for undirected graphs, by Pons and Latapy (2005). Its idea is that a short random walk tends to stay trapped inside the community where it starts, so two vertices in the same community see the rest of the graph in the same way: the distributions of a $t$-step walk from them are close. Walktrap turns this into a distance between vertices and between groups of vertices, merges groups bottom-up with [Ward's method](/ward-method/), always joining the two adjacent groups whose union keeps the groups tightest, and finally cuts the resulting tree at the level with the highest [modularity](/modularity/).

## In plain words

Drop a walker on a vertex and let it take a few random steps along the edges. If the graph has groups that are densely connected inside and loosely connected to each other, the walker will usually still be in its starting group after a few steps. So where a walker from vertex A tends to end up says a lot about which group A belongs to.

Walktrap compares vertices by this: two vertices whose walkers end up in the same places are close. It starts with every vertex alone, and repeatedly joins the two neighbouring groups that are closest in this sense. This builds a family tree of groups, from single vertices up to whole connected pieces of the graph. The final answer is the level of the tree whose grouping scores best on modularity, the standard measure of how much denser the groups are inside than chance.

## The problem

**Input.** An undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges, with positive edge weights (weight 1 when unweighted), and a walk length $t \ge 1$.

**Output.** A partition of $V$ into communities, together with the dendrogram of merges from which it was chosen.

**The distance.** Add a loop of weight 1 at every vertex, let $A$ be the resulting weighted adjacency matrix, $d(i) = \sum_j A_{ij}$, $D$ the diagonal matrix of the $d(i)$, and $P = D^{-1} A$ the transition matrix of the random walk. Write $P^t_{i\cdot}$ for row $i$ of $P^t$, the distribution of the walk after $t$ steps from $i$. For a set $C$ of vertices, $P^t_{C\cdot} = \frac{1}{|C|} \sum_{i \in C} P^t_{i\cdot}$. The distance between two sets is

$$r_{C_1 C_2} = \bigl\| D^{-1/2} \bigl(P^t_{C_1\cdot} - P^t_{C_2\cdot}\bigr) \bigr\| = \Bigl( \sum_{k} \frac{(P^t_{C_1 k} - P^t_{C_2 k})^2}{d(k)} \Bigr)^{1/2},$$

and $r_{ij}$ is the case of single vertices. Dividing by $d(k)$ removes the bias toward high-degree vertices, which every walk visits often.

**The objective.** For a partition $\mathcal{P}$, $\sigma(\mathcal{P}) = \frac{1}{n} \sum_{C \in \mathcal{P}} \sum_{i \in C} r_{iC}^2$, the mean squared distance of vertices to their community. Merging $C_1$ and $C_2$ increases $\sigma$ by

$$\Delta\sigma(C_1, C_2) = \frac{1}{n}\, \frac{|C_1|\,|C_2|}{|C_1| + |C_2|}\, r_{C_1 C_2}^2.$$

## The algorithm

```pseudo id=main
WALKTRAP(G, t)
L1  add a loop of weight 1 at every vertex; d(i) ← weighted degree; P ← D⁻¹A
L2  for each vertex i: v_i ← D^(−1/2) P^t_{i·}; C_i ← {i}
L3  for each edge {i, j} with i ≠ j: Δσ(C_i, C_j) ← (1/n) · (1/2) · ‖v_i − v_j‖²
L4  partitions ← [the partition into single vertices]
L5  while two current communities are adjacent do
L6      C₁, C₂ ← the adjacent pair with the smallest Δσ (ties: the smallest pair of ids)
L7      C₃ ← C₁ ∪ C₂ with the new id; v_{C₃} ← (|C₁| v_{C₁} + |C₂| v_{C₂}) / (|C₁| + |C₂|)
L8      for each community C adjacent to C₃: Δσ(C, C₃) ← (1/n) · |C||C₃| / (|C| + |C₃|) · ‖v_C − v_{C₃}‖²
L9      append the current partition to partitions
L10 return the partition in partitions with the largest modularity (ties: the earliest)
```

Lines L1 and L2 compute, for each vertex, the scaled distribution of a $t$-step walk. Line L3 fills the table of merge costs for adjacent vertices; only adjacent communities are ever merged, which keeps every community connected and the table of size $O(m)$. Line L6 picks the cheapest merge. Line L7 forms the new community, whose vector is the size-weighted mean of the two old ones, so it equals $D^{-1/2} P^t_{C_3\cdot}$ without another walk. Line L8 removes the costs that involved $C_1$ or $C_2$ and computes the costs between $C_3$ and its neighbours. After at most $n - 1$ merges, each connected component is one community, and line L10 chooses the level of the dendrogram by modularity $Q = \sum_C \bigl( e_C / m_w - (\mathrm{vol}(C) / 2 m_w)^2 \bigr)$, computed on the input graph without the added loops, where $e_C$ is the weight of the edges inside $C$, $\mathrm{vol}(C)$ the sum of the weighted degrees in $C$, and $m_w$ the total edge weight. New communities get the ids $n, n + 1, \dots$ in the order they are created.

## Example

Take two triangles $\{0, 1, 2\}$ and $\{3, 4, 5\}$ joined by the edge 2-3, without weights, and $t = 2$. With the loops, vertices 0 and 1 have the same closed neighbourhood $\{0, 1, 2\}$, so their walks have the same distribution and $r_{01} = 0$; the same holds for 4 and 5.

| step | merged | new id | $\Delta\sigma$ | partition | $Q$ |
|---|---|---|---|---|---|
| start | | | | singletons | $-0.173$ |
| 1 | 0, 1 | 6 | 0 | $\{0,1\}, 2, 3, 4, 5$ | $-0.071$ |
| 2 | 4, 5 | 7 | 0 | $\{0,1\}, 2, 3, \{4,5\}$ | $0.031$ |
| 3 | 2, 6 | 8 | $217/279936 \approx 0.00078$ | $\{0,1,2\}, 3, \{4,5\}$ | $0.194$ |
| 4 | 3, 7 | 9 | $217/279936$ | $\{0,1,2\}, \{3,4,5\}$ | $0.357$ |
| 5 | 8, 9 | 10 | $1931/69984 \approx 0.0276$ | everything | $0$ |

Steps 1 and 2 tie at 0, and steps 3 and 4 tie by symmetry; the rule on ids decides the order, and the dendrogram is the same either way. The last merge costs about 36 times as much as the two before it, which signals two real communities. The best level is the two triangles, with $Q = 5/14 \approx 0.357$.

## Correctness

Write $v_i = D^{-1/2} P^t_{i\cdot}$. Then $r_{iC}$ is the Euclidean distance between $v_i$ and the mean $v_C$ of the vectors in $C$, and $n\,\sigma$ is the within-group sum of squares of the points $v_i$. Ward's identity says that merging two groups with sizes $s_1$, $s_2$ and means $\mu_1$, $\mu_2$ increases the within-group sum of squares by $\frac{s_1 s_2}{s_1 + s_2} \|\mu_1 - \mu_2\|^2$, which gives the formula for $\Delta\sigma$. The loop keeps two invariants: each community's stored vector is the mean of its members' vectors (line L7), and the table holds the correct $\Delta\sigma$ for exactly the adjacent pairs of current communities (lines L3 and L8). So line L6 makes the greedy choice that increases $\sigma$ the least. Each round removes one community, so the loop ends after at most $n - 1$ rounds, with one community per connected component. The full proof is in the proof file below. The greedy choice is not guaranteed to minimize $\sigma$ over all partitions with the same number of parts: like every agglomerative method, Walktrap is a heuristic for its objective.

## Complexity

The walks of line L2 take $t$ rounds of sparse matrix-vector products for each of the $n$ start vertices, $O(t n (n + m))$ time with dense vectors. Each vector has $n$ entries, so storing them takes $O(n^2)$ space, the dominant cost in memory. A merge computes one distance, $O(n)$ time, for each neighbour of the new community; summed over all merges, Pons and Latapy bound the number of such computations by $O(m H)$, where $H$ is the height of the dendrogram, so the merges take $O(m n H)$ time, which is $O(m n^2)$ in the worst case. Keeping the costs in a heap, as in the paper, makes each choice at line L6 cost $O(\log m)$; scanning the table costs $O(m)$ per merge, $O(n m)$ in all, within the same bound. Pons and Latapy report that on sparse real-world graphs, where the dendrogram has height $O(\log n)$, the time is $O(n^2 \log n)$.

## Properties

- **Undirected, weighted.** Weights enter through $A$. Directed graphs are not handled: the random-walk distance needs a symmetric $A$ for its interpretation and for $D^{-1/2}$ scaling.
- **Deterministic.** No random choices; with a fixed tie rule the dendrogram is unique.
- **Hierarchical.** It returns the whole dendrogram, not only the chosen partition; any level can be used.
- **Connected communities.** Only adjacent communities are merged, so every community induces a connected subgraph, and different components are never merged.
- **Twins merge at no cost.** Two vertices with the same closed neighbourhood, like 0 and 1 in the example, have identical walk distributions and $\Delta\sigma = 0$, so they merge first: Walktrap respects [structural equivalence](/structural-equivalence/).

## Variants and improvements

- **Choice of $t$.** With $t$ too small the walks see only the immediate neighbourhood; with $t$ too large they approach the stationary distribution, proportional to the degree, and all vertices look alike. Pons and Latapy recommend small values, and the igraph implementation uses $t = 4$ by default.
- **Memory limits.** The paper keeps only some of the community vectors in memory and recomputes the others when needed, trading time for space on large graphs.
- **Other merge rules.** Using the distance $r$ alone, without the size factor of Ward's rule, or average linkage, gives other agglomerative methods with the same distance.
- **Relatives.** The [Louvain method](/louvain-method/) also merges greedily but optimizes modularity directly and is much faster on large graphs; Markov clustering and Infomap also use random walks; diffusion distances and [spectral clustering](/spectral-clustering/) use the same walk matrices globally.

## When to use it

Use Walktrap for graphs with up to tens of thousands of vertices when a full dendrogram is wanted and the result should not depend on a random seed. It is a good choice for medium-sized social and biological networks, where benchmark comparisons usually find it more accurate than the greedy modularity method of Clauset, Newman and Moore. For graphs with millions of vertices, the $O(n^2)$ memory rules it out; use the Louvain or [Leiden](/leiden-algorithm/) method.

## Pitfalls

- **Forgetting the loops.** Without the loops, a bipartite part of the graph makes the walk periodic, and two adjacent vertices then have walk distributions on opposite sides after an even $t$, so they look far apart.
- **Too large a $t$.** All rows of $P^t$ converge to the stationary distribution, all distances shrink toward 0, and the merges are decided by rounding noise.
- **Memory.** $n$ dense vectors of length $n$: about 80 GB of doubles for $10^5$ vertices. Store the vectors sparsely, or use the memory-limited version.
- **Modularity's resolution limit.** The final cut is by modularity, which cannot resolve communities smaller than about $\sqrt{2 m}$ edges in a large graph; inspect the dendrogram for smaller structure.
- **Disconnected graphs.** The dendrogram is a forest, one tree per component; the chosen partition never merges components, which is correct, but code that expects a single root must handle it.

## Implementations

## History

Pascal Pons and Matthieu Latapy presented Walktrap at the International Symposium on Computer and Information Sciences (ISCIS) in 2005, and the journal version appeared in the Journal of Graph Algorithms and Applications in 2006. It combined the random-walk view of communities with Ward's 1963 method for hierarchical clustering and with the modularity of Newman and Girvan (2004) for choosing the level, and it was one of the methods compared in the benchmarks of community detection of the late 2000s.

## References
