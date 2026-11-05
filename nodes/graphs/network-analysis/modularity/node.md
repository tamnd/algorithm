---
tag: RC3PCT
kind: definition
slug: modularity
name: Modularity
aliases:
- Newman-Girvan modularity
area: graphs/network-analysis
level: core
summary: 'Score of a partition: fraction of edges inside groups minus the expected fraction under a null model.'
prereqs: [graph, degree, community-detection, configuration-model]
see_also: [louvain-method, leiden-algorithm, girvan-newman-algorithm, label-propagation-algorithm, infomap, stochastic-block-model, assortativity, spectral-clustering]
sources:
  - paper: doi:10.1103/PhysRevE.69.026113
    title: M. E. J. Newman and Michelle Girvan, Finding and evaluating community structure in networks, Physical Review E 69, 026113 (2004)
    locator: the section that defines the modularity Q from the matrix e of edge fractions between communities
  - paper: doi:10.1073/pnas.0601602103
    title: M. E. J. Newman, Modularity and community structure in networks, Proceedings of the National Academy of Sciences 103(23), 8577 to 8582 (2006)
    locator: the form of Q with the modularity matrix B and the spectral method
  - paper: doi:10.1109/TKDE.2007.190689
    title: Ulrik Brandes, Daniel Delling, Marco Gaertler, Robert Görke, Martin Hoefer, Zoran Nikoloski and Dorothea Wagner, On modularity clustering, IEEE Transactions on Knowledge and Data Engineering 20(2), 172 to 188 (2008)
    locator: the NP-completeness of the decision version, the range of Q, and the properties of optimal clusterings
  - paper: doi:10.1073/pnas.0605965104
    title: Santo Fortunato and Marc Barthélemy, Resolution limit in community detection, Proceedings of the National Academy of Sciences 104(1), 36 to 41 (2007)
    locator: the whole paper (the ring of cliques and the scale of about the square root of 2m)
  - paper: doi:10.1103/PhysRevLett.100.118703
    title: E. A. Leicht and M. E. J. Newman, Community structure in directed networks, Physical Review Letters 100, 118703 (2008)
    locator: the directed form of the modularity
---

Modularity is a score of a partition of the [vertices](/vertex/) of a graph into groups: the fraction of the edges that fall inside the groups, minus the fraction that would fall inside them if the edges were placed at random with the same [degrees](/degree/). A partition with modularity near 0 is no better than chance, and a large value means dense groups with few edges between them. It is the most used objective of [community detection](/community-detection/), and the quantity that the [Louvain](/louvain-method/) and [Leiden](/leiden-algorithm/) methods raise.

## Definition

Let $G = (V, E)$ be an undirected graph with $n$ vertices and $m \ge 1$ edges, with adjacency matrix $A$ and degrees $k_i = \sum_j A_{ij}$, so that $\sum_i k_i = 2m$. Let $\mathcal{C}$ be a partition of $V$, and let $c(i)$ be the group of vertex $i$. The **modularity** of $\mathcal{C}$ is

$$Q(\mathcal{C}) = \frac{1}{2m} \sum_{i, j \in V} \left( A_{ij} - \frac{k_i k_j}{2m} \right) [c(i) = c(j)].$$

The sum is over ordered pairs, and includes $i = j$. The term $k_i k_j / 2m$ is the expected number of edges between $i$ and $j$ when the ends of all edges are paired at random, as in the [configuration model](/configuration-model/). The matrix $B_{ij} = A_{ij} - k_i k_j/2m$ is the **modularity matrix**.

**The form by groups.** For a group $C$, let $e_C$ be the number of edges with both ends in $C$ and $D_C = \sum_{i \in C} k_i$ the sum of its degrees. The ordered pairs inside $C$ count each inside edge twice, so $\sum_{i, j \in C} A_{ij} = 2e_C$ and $\sum_{i, j \in C} k_i k_j = D_C^2$. This gives

$$Q(\mathcal{C}) = \sum_{C \in \mathcal{C}} \left[ \frac{e_C}{m} - \left( \frac{D_C}{2m} \right)^2 \right].$$

**Weighted graphs.** Replace $A_{ij}$ by the weight $w_{ij} \ge 0$, $k_i$ by the weighted degree, and $m$ by the total weight. A [self-loop](/self-loop/) of weight $w$ at $i$ adds $w$ to $e_C$ for the group of $i$ and $2w$ to $k_i$. This rule is what the aggregation step of the Louvain method needs.

**Directed graphs.** Leicht and Newman use the out-degree $k_i^{\mathrm{out}}$ and the in-degree $k_j^{\mathrm{in}}$, and the number of arcs $m$:

$$Q_{\mathrm{dir}} = \frac{1}{m} \sum_{i, j} \left( A_{ij} - \frac{k_i^{\mathrm{out}} k_j^{\mathrm{in}}}{m} \right) [c(i) = c(j)].$$

**Resolution.** Many programs use $Q_\gamma = \sum_C [e_C/m - \gamma (D_C/2m)^2]$ with a resolution $\gamma > 0$. A larger $\gamma$ favours smaller groups. The plain modularity is $\gamma = 1$.

**Disconnected graphs and isolated vertices.** The formula needs only $m \ge 1$. An isolated vertex has $k_i = 0$ and adds 0 wherever it is put. Two vertices in different [connected components](/connected-components/) can be in one group, but such a group never helps: see the split rule below.

**Ties.** Modularity scores partitions, and several partitions can have the same score, for example when an automorphism of the graph maps one to the other. "The" partition of maximum modularity need not be unique.

### Basic facts

- **Range.** $-\tfrac12 \le Q < 1$ for every partition. For the upper bound, $Q \le \sum_C e_C/m - \sum_C (D_C/2m)^2 \le 1 - \sum_C (D_C/2m)^2$, and the last sum is positive since some group has $D_C > 0$. For the lower bound, let $E_{\mathrm{in}} = \sum_C e_C$. A group $C$ has $D_C = 2e_C + c_C$, where $c_C$ is the number of edges that leave $C$, and $c_C \le m - E_{\mathrm{in}}$. With $a_C = D_C/2m$ and $\sum_C a_C = 1$, we get $\sum_C a_C^2 \le \max_C a_C \le (2E_{\mathrm{in}} + m - E_{\mathrm{in}})/2m = \tfrac12 + E_{\mathrm{in}}/2m$. So $Q \ge E_{\mathrm{in}}/m - \tfrac12 - E_{\mathrm{in}}/2m \ge -\tfrac12$.
- **One group.** The partition with one group has $e_V = m$ and $D_V = 2m$, so $Q = 0$. Hence the maximum modularity of every graph is at least 0.
- **Merging two groups.** If groups $A$ and $B$ are joined by $e_{AB}$ edges, merging them changes $Q$ by
$$\Delta Q = \frac{e_{AB}}{m} - 2\,\frac{D_A}{2m}\,\frac{D_B}{2m},$$
because $e_{A \cup B} = e_A + e_B + e_{AB}$ and $(D_A + D_B)^2 = D_A^2 + D_B^2 + 2 D_A D_B$. This is the step of the greedy and Louvain methods.
- **The split rule.** If $e_{AB} = 0$, the merge changes $Q$ by $-2 D_A D_B/(2m)^2 \le 0$. So in a partition with maximum modularity, each group, without the isolated vertices of $G$, induces a connected subgraph: else it splits into two parts with no edge between them and positive degree sums, and the split raises $Q$.
- **Hardness.** Brandes and co-authors show that deciding whether a graph has a partition with $Q \ge K$ is NP-complete. So exact maximization is done only on small graphs.

## Examples and non-examples

**Two triangles joined by an edge.** Take the vertices 0 to 5 with the edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{3,4\}$, $\{3,5\}$, $\{4,5\}$ and the bridge $\{2,3\}$, so $m = 7$ and the degrees are $2, 2, 3, 3, 2, 2$.

| partition | $e_C$ | $D_C$ | $Q$ |
|---|---|---|---|
| $\{0,1,2\}$, $\{3,4,5\}$ | 3, 3 | 7, 7 | $\frac{6}{7} - 2 \cdot \frac{49}{196} = \frac{5}{14} \approx 0.357$ |
| $\{0,1,2,3\}$, $\{4,5\}$ | 4, 1 | 10, 4 | $\frac{5}{7} - \frac{100 + 16}{196} = \frac{6}{49} \approx 0.122$ |
| $\{0,1\}$, $\{2,3\}$, $\{4,5\}$ | 1, 1, 1 | 4, 6, 4 | $\frac{3}{7} - \frac{16 + 36 + 16}{196} = \frac{4}{49} \approx 0.082$ |
| one group | 7 | 14 | 0 |
| each vertex alone | 0 each | | $-\frac{4 \cdot 4 + 2 \cdot 9}{196} = -\frac{17}{98} \approx -0.173$ |

Of all 203 partitions of the six vertices, the two triangles have the largest modularity, $5/14$.

**The lower bound is reached.** In the [complete bipartite graph](/bipartite-graph/) $K_{3,3}$, put the two sides in two groups. No edge is inside a group, and each side has $D_C = 9 = m$, so $Q = 0 - 2 \cdot \tfrac14 = -\tfrac12$. The same holds for every bipartite graph split into its two sides. For $K_{3,3}$, no partition of the 203 has $Q > 0$, so the best partition is a single group: a graph can have no community structure in the sense of modularity.

**The resolution limit.** Take a ring of $r$ cliques $K_q$, each joined to the next by one edge. Each clique has $L = q(q-1)/2$ edges and degree sum $D = 2(L + 1)$, and $m = r(L + 1)$. The partition into single cliques and the partition into neighbouring pairs of cliques differ by
$$Q_{\mathrm{pairs}} - Q_{\mathrm{single}} = \frac{r}{2m}\left(1 - \frac{D^2}{2m}\right),$$
which is positive exactly when $r > 2(L+1) = q(q-1) + 2$. For $q = 5$ the threshold is $r = 22$: with $r = 30$, single cliques give $Q \approx 0.8758$ and pairs give $Q \approx 0.8879$. So modularity merges groups that are obviously separate when the graph is large. Fortunato and Barthélemy show that this happens for groups with fewer than about $\sqrt{2m}$ inside edges.

**Non-examples.**

- The fraction of inside edges, $\sum_C e_C/m$, is not modularity. It is 1 for the single group, so it rewards putting everything together.
- The [clustering coefficient](/clustering-coefficient/) is not a score of a partition. It measures triangles around vertices and needs no groups.
- The *conductance* of a group, the number of leaving edges divided by the smaller of $D_C$ and $2m - D_C$, scores one group, not a partition, and has no null model.

## Related definitions

- [Community detection](/community-detection/): the problem that modularity turns into an optimization problem.
- [Configuration model](/configuration-model/): the null model behind the term $k_i k_j / 2m$.
- [Assortativity](/assortativity/): the same formula with the groups given by a vertex attribute, read as a correlation.
- [Stochastic block model](/stochastic-block-model/): a model of random graphs with planted groups, whose likelihood is another objective for the same problem.
- [Louvain method](/louvain-method/), [Leiden algorithm](/leiden-algorithm/) and [Girvan-Newman algorithm](/girvan-newman-algorithm/): algorithms that use modularity.
- [Spectral clustering](/spectral-clustering/): Newman's spectral method splits the graph by the signs of the leading eigenvector of $B$.

## References
