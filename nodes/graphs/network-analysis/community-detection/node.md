---
tag: C9RFRX
kind: problem
slug: community-detection
name: Community detection
aliases:
- graph clustering
- network clustering
- modularity maximization
area: graphs/network-analysis
level: core
summary: Split the vertices of a network into groups that have many edges inside and few edges between them.
prereqs: [graph, connected-components]
see_also: [modularity, louvain-method, leiden-algorithm, girvan-newman-algorithm, label-propagation-algorithm, stochastic-block-model, clique-percolation-method, spectral-clustering]
sources:
  - paper: doi:10.1016/j.physrep.2009.11.002
    title: Santo Fortunato, Community detection in graphs, Physics Reports 486(3-5), 75 to 174 (2010)
    locator: Sections 3 (the definitions of a community and of a partition), 6 (modularity optimization and its limits) and 15 (testing algorithms)
  - paper: doi:10.1103/PhysRevE.69.026113
    title: M. E. J. Newman and Michelle Girvan, Finding and evaluating community structure in networks, Physical Review E 69, 026113 (2004)
    locator: the definition of modularity Q and the divisive algorithm by edge betweenness
  - paper: doi:10.1109/TKDE.2007.190689
    title: Ulrik Brandes, Daniel Delling, Marco Gaertler, Robert Görke, Martin Hoefer, Zoran Nikoloski and Dorothea Wagner, On modularity clustering, IEEE Transactions on Knowledge and Data Engineering 20(2), 172 to 188 (2008)
    locator: the NP-completeness proof for the decision version of modularity maximization, and the properties of optimal clusterings
  - paper: doi:10.1073/pnas.0605965104
    title: Santo Fortunato and Marc Barthélemy, Resolution limit in community detection, Proceedings of the National Academy of Sciences 104(1), 36 to 41 (2007)
    locator: the whole paper (the merge of small cliques in the modularity optimum)
  - url: "https://jmlr.org/papers/v18/16-480.html"
    locator: Emmanuel Abbe, Community detection and stochastic block models, recent developments, Journal of Machine Learning Research 18(177), 1 to 86 (2018) (the threshold for weak recovery in the symmetric two-block model)
---

Community detection is the problem of splitting the [vertices](/vertex/) of a network into groups, called communities, so that many edges join vertices of the same group and few edges join different groups. Unlike most graph problems, it has no single exact definition: each method fixes its own objective, such as the [modularity](/modularity/) $Q$, a cut ratio, or the likelihood of a [stochastic block model](/stochastic-block-model/), and the best partitions under different objectives can differ. Maximizing modularity is NP-hard, so practical methods such as the [Louvain method](/louvain-method/) are heuristics.

## In plain words

In a school, students form groups of friends. Most friendships are inside a group, and only a few cross between groups. If you only have the list of who is friends with whom, can you find the groups?

That is community detection. You look for a way to split the people so that the splits cut few friendships, while each group stays well knit. The hard part is to say what a good split is. Putting everyone in one group cuts nothing but finds nothing. Putting each person alone finds nothing either. So each method uses a score that rewards groups that are denser than chance, and searches for a split with a high score. Different scores can give different answers on the same network.

## Definition

**Input.** A graph $G = (V, E)$ with $n$ vertices and $m$ edges. The basic case is undirected and without weights. Variants allow weights $w(e) > 0$, read as the strength of a tie, and directed edges.

**Output.** A partition $\mathcal{C} = \{C_1, \ldots, C_k\}$ of $V$ into non-empty disjoint sets whose union is $V$. The number $k$ is usually not given and is part of the answer.

**The objective.** The problem is fixed only when an objective is chosen. The most used one is the **modularity** of Newman and Girvan:

$$Q(\mathcal{C}) = \sum_{i=1}^{k} \left[ \frac{e_i}{m} - \left( \frac{D_i}{2m} \right)^2 \right],$$

where $e_i$ is the number of edges with both ends in $C_i$ and $D_i = \sum_{v \in C_i} d(v)$ is the sum of the degrees in $C_i$. The first term is the fraction of edges inside the groups, and the second is the fraction expected if the edges were placed at random with the same degrees. The *modularity maximization* problem asks for a partition with the largest $Q$. See [modularity](/modularity/) for its properties.

Other objectives are the normalized cut or the conductance of each group, which favour groups with a small boundary; the likelihood of a [stochastic block model](/stochastic-block-model/), which treats the communities as hidden labels of a random graph; and the description length of a random walk, used by [Infomap](/infomap/).

**Disconnected graphs.** No good partition puts two [connected components](/connected-components/) in one group: for modularity, splitting a group along a component boundary always raises $Q$, because it removes no inside edge and lowers the second term. So the components are found first, in $O(n + m)$ time, and each is split on its own. Isolated vertices form groups of their own and add 0 to $Q$.

**Ties.** Several partitions can have the same optimal value, for example in a graph with symmetries. Heuristics also depend on the order in which they visit the vertices, so two runs can return different partitions of almost equal quality. A report should fix the order or the random seed.

## Variants

- **Overlapping communities.** The output is a cover: a vertex may be in several groups. The [clique percolation method](/clique-percolation-method/) gives such covers.
- **Hierarchical communities.** The output is a tree of nested partitions, a dendrogram, as in the [Girvan-Newman algorithm](/girvan-newman-algorithm/) and [Walktrap](/walktrap-algorithm/).
- **A given number of groups.** Fix $k$. With $k = 2$ and equal sizes this is graph bisection, which is NP-hard.
- **Local communities.** Given one seed vertex, find a good group that contains it, in time that depends on the size of the group and not on $n$. Methods based on [personalized PageRank](/personalized-pagerank/) do this.
- **Recovery in a planted model.** The graph is drawn from a stochastic block model with hidden groups, and the goal is to recover them exactly, or better than chance. This variant has sharp thresholds.
- **Directed, weighted and signed graphs.** The objectives above have forms for each of these; for signed graphs, see [structural balance](/structural-balance-theorem/).

## Examples

**A worked example.** Take the undirected graph with the vertices 0 to 6 and the 9 edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$. The degrees are $2, 3, 3, 3, 3, 2, 2$, and $2m = 18$.

| partition | $e_i$ | $D_i$ | $Q$ |
|---|---|---|---|
| $\{0,1,2,3\}$, $\{4,5,6\}$ | 5, 3 | 11, 7 | $\frac{8}{9} - \frac{121 + 49}{324} = \frac{59}{162} \approx 0.364$ |
| $\{0,1,2\}$, $\{3,4,5,6\}$ | 3, 4 | 8, 10 | $\frac{7}{9} - \frac{64 + 100}{324} = \frac{22}{81} \approx 0.272$ |
| all in one group | 9 | 18 | $1 - 1 = 0$ |
| each vertex alone | 0 each | | $-\frac{4 \cdot 4 + 4 \cdot 3 \cdot 9 + \ldots}{324} = -\frac{4}{27} \approx -0.148$ |

The first partition, which cuts only the edge $\{3, 4\}$, has the largest modularity of all 877 partitions of the 7 vertices.

**Two cliques and the resolution limit.** Take a ring of $r$ cliques $K_q$, each joined to the next by one edge. For large $r$, the partition that merges pairs of neighbouring cliques has a larger modularity than the partition into single cliques, although each clique is the obvious community. Fortunato and Barthélemy show that modularity cannot resolve groups with fewer than about $\sqrt{2m}$ internal edges, whatever the structure.

**Detectability.** In the symmetric stochastic block model with two equal groups, where each pair inside a group is an edge with probability $a/n$ and each pair across with probability $b/n$, a partition that agrees with the hidden one better than chance can be found from the graph if and only if $(a - b)^2 > 2(a + b)$. Below this threshold no algorithm does better than a random guess. For $a = 5$, $b = 1$ the test is $16 > 12$, so recovery better than chance is possible; for $a = 4$, $b = 2$ it is $4 < 12$, and it is not.

## Known algorithms

| algorithm | idea | time, typical or worst |
|---|---|---|
| [Girvan-Newman algorithm](/girvan-newman-algorithm/) | remove the edge of highest edge betweenness, again and again | $O(m^2 n)$ worst case |
| [Louvain method](/louvain-method/) | greedy local moves that raise modularity, then merge the groups and repeat | close to linear in $m$ in practice |
| [Leiden algorithm](/leiden-algorithm/) | Louvain with a refinement step that keeps the groups connected | close to linear in $m$ in practice |
| [Label propagation](/label-propagation-algorithm/) | each vertex takes the label that most of its neighbours have | $O(m)$ per round |
| [Infomap](/infomap/) | minimize the description length of a random walk | close to linear in $m$ in practice |
| [Walktrap](/walktrap-algorithm/) | merge groups by distances between short random walks | $O(m n^2)$ worst case |
| [Markov clustering](/markov-clustering/) | alternate matrix powers and entrywise powers of a random walk matrix | depends on the pruning |
| [Clique percolation](/clique-percolation-method/) | union of adjacent $k$-cliques, overlapping groups | exponential in the worst case |
| [Spectral clustering](/spectral-clustering/) | the leading eigenvectors of a Laplacian or modularity matrix, then $k$-means | an eigenvector computation |

## Bounds

- **Modularity maximization is NP-hard.** Brandes and co-authors prove that the decision version, "is there a partition with $Q \ge K$", is NP-complete, by a reduction from 3-partition. So no polynomial algorithm is known for the exact optimum.
- **Exact methods.** Integer linear programs solve the problem exactly for graphs of a few hundred vertices.
- **Statistical limits.** For the two-group symmetric block model above, weak recovery is possible exactly when $(a - b)^2 > 2(a + b)$: the impossibility below the threshold is by Mossel, Neeman and Sly, and the algorithms above it are by Massoulié and by Mossel, Neeman and Sly; see the survey of Abbe.

## Reductions

- **From graph bisection.** With $k = 2$ fixed and equal sizes required, the cut version is the minimum bisection problem, which is NP-hard.
- **To clustering of points.** Spectral methods map each vertex to a point in $\mathbb{R}^k$ by eigenvectors and then cluster the points, for example with $k$-means.
- **To connected components.** Removing all edges between groups leaves the groups as unions of components; the Girvan-Newman algorithm uses this view, with [betweenness centrality computation](/betweenness-centrality-computation/) as its inner step.

## Applications

- Social networks: find circles of friends, organizations and interest groups.
- Biology: find functional modules in protein interaction networks and in gene co-expression networks.
- The web and citation networks: group pages or papers by topic.
- Graph algorithms: partition a large graph so that each machine of a cluster holds one part and few edges cross between machines.

## References
