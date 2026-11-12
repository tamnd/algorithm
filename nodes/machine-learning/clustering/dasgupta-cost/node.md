---
tag: 1XM7WH
kind: definition
slug: dasgupta-cost
name: Dasgupta's cost
aliases:
- Dasgupta objective
- Dasgupta cost function
area: machine-learning/clustering
level: research
summary: "A cost of a hierarchy on a similarity graph: each edge ij pays w_ij times the number of leaves below the lowest common ancestor of i and j."
prereqs: [hierarchical-clustering-problem, lowest-common-ancestor]
see_also: [sparsest-cut-problem, upgma, dendrogram, divisive-clustering, np-hard, semidefinite-programming, bisecting-k-means, binary-tree]
sources:
  - paper: doi:10.1145/2897518.2897527
    title: "Sanjoy Dasgupta, A cost function for similarity-based hierarchical clustering, Proceedings of the 48th ACM Symposium on Theory of Computing (STOC 2016), 118-127"
    locator: the definition of the cost, its basic properties, the proof that it is NP-hard to minimize, and the O(α log n) bound for recursive sparsest cut
  - paper: doi:10.1137/1.9781611974782.53
    title: "Moses Charikar and Vaggos Chatziafratis, Approximate hierarchical clustering via sparsest cut and spreading metrics, Proceedings of the 28th ACM-SIAM Symposium on Discrete Algorithms (SODA 2017), 841-854"
    locator: the O(α) bound for recursive sparsest cut, which gives O(sqrt(log n)) with ARV, and the hardness of a constant factor under the small set expansion hypothesis
  - paper: "Benjamin Moseley and Joshua R. Wang, Approximation bounds for hierarchical clustering: average linkage, bisecting k-means, and local search, Advances in Neural Information Processing Systems 30 (NIPS 2017), 3094-3103"
    locator: the revenue, which is the dual of the cost, and the 1/3 approximation of the best revenue by average linkage
  - paper: "Vincent Cohen-Addad, Varun Kanade, Frederik Mallmann-Trenn and Claire Mathieu, Hierarchical clustering: objective functions and algorithms, Journal of the ACM 66(4) (2019), Article 26"
    locator: the admissible cost functions, of which Dasgupta's cost is the main example, and the version for dissimilarities
---

## Definition

Let $G = (V, E, w)$ be an undirected graph on $n$ points with similarity weights $w_{ij} \ge 0$: a large weight means that $i$ and $j$ are alike. A *hierarchy* on $V$ is a rooted tree $T$ whose leaves are the points of $V$, in which each internal node has at least two children. For a node $v$ of $T$, let $\text{leaves}(v)$ be the set of leaves below $v$, and let $i \vee j$ be the [lowest common ancestor](/lowest-common-ancestor/) of the leaves $i$ and $j$. **Dasgupta's cost** of $T$ is

$$\text{cost}_G(T) = \sum_{\{i, j\} \in E} w_{ij} \, \bigl|\text{leaves}(i \vee j)\bigr|.$$

The *Dasgupta problem* asks for a hierarchy of least cost. A pair of similar points pays the size of the smallest cluster that holds both, so a good tree keeps similar points together in small clusters and separates them only near the root.

**The cost by nodes.** If $T$ is binary, each pair $i, j$ is split at exactly one internal node $v = i \vee j$, one in each child. So

$$\text{cost}_G(T) = \sum_{v \text{ internal}} \bigl|\text{leaves}(v)\bigr| \cdot w\bigl(\text{leaves}(v_1), \text{leaves}(v_2)\bigr),$$

where $v_1$, $v_2$ are the children of $v$ and $w(A, B) = \sum_{i \in A, j \in B} w_{ij}$. At the root, the term is $n$ times the weight of the cut between the two top clusters. This form shows the link to cuts: a good top split is a cut of small weight, but a cut that splits off one point is cheap only if the point is weakly linked.

**Binary trees suffice.** A node with three or more children can be replaced by a binary tree on the same children, and this does not raise the leaf count of any lowest common ancestor. So some binary tree has the least cost. There are $(2n - 3)!! = 1 \cdot 3 \cdot 5 \cdots (2n - 3)$ binary trees on $n$ labeled leaves, so a search over all trees is exponential.

**Hardness.** Dasgupta (2016) proved that the Dasgupta problem is [NP-hard](/np-hard/). Recursive [sparsest cut](/sparsest-cut-problem/), which splits each cluster by an $\alpha$-approximate sparsest cut, has cost at most $O(\alpha)$ times the least cost, by the analysis of Charikar and Chatziafratis (2017). With the Leighton-Rao algorithm this gives $O(\log n)$, and with the ARV algorithm, which uses [semidefinite programming](/semidefinite-programming/), $O(\sqrt{\log n})$. Under the small set expansion hypothesis, no polynomial-time algorithm has a constant factor.

## Examples and non-examples

**A path.** Take the points $1, 2, 3, 4$ with the edges $12$, $23$, $34$, each of weight 1.

| tree | cost of $12$ | cost of $23$ | cost of $34$ | total |
|---|---|---|---|---|
| $((1, 2), (3, 4))$ | 2 | 4 | 2 | 8 |
| $(((1, 2), 3), 4)$ | 2 | 3 | 4 | 9 |
| $((1, (2, 3)), 4)$ | 3 | 2 | 4 | 9 |
| $((1, 4), (2, 3))$ | 4 | 2 | 4 | 10 |

The balanced tree is best. Each edge pays at least 2, and since the graph is connected, some edge crosses the root split and pays 4, so no tree costs less than 8.

**The clique.** For the complete graph on $n$ points with unit weights, every binary tree has the same cost, $(n^3 - n)/3$. By the cost by nodes, a root split into $a$ and $b = n - a$ points gives $n a b + f(a) + f(b)$, and with $f(m) = (m^3 - m)/3$ this is $\bigl((a + b)^3 - (a + b)\bigr)/3 = f(n)$. So the cost does not prefer any tree when all points are equally similar, as it should.

**Two cliques.** For two disjoint cliques of $a$ and $b$ points with unit weights, a tree that splits the two cliques at the root costs $f(a) + f(b)$. No tree costs less: a tree restricted to the leaves of one clique gives a tree on that clique, and the restriction can only lower the leaf counts, so each clique pays at least $f(a)$ or $f(b)$.

**Non-example: the heights.** The cost depends only on the shape of the tree. Two [dendrograms](/dendrogram/) with the same tree and different heights have the same cost, so the cost does not score the ultrametric of a dendrogram.

**Non-example: a distance in place of a similarity.** If $w_{ij}$ is a distance, the least cost puts far points together low in the tree, which is the wrong goal. For dissimilarities, the right objective is to *maximize* the same sum, as in Cohen-Addad and others (2019).

## Related definitions

- **Revenue.** Moseley and Wang (2017) defined the revenue $\text{rev}_G(T) = \sum_{\{i, j\} \in E} w_{ij} \bigl(n - |\text{leaves}(i \vee j)|\bigr) = n W - \text{cost}_G(T)$, where $W$ is the total weight. A tree has the least cost exactly when it has the largest revenue, but the approximation factors differ. Average linkage ([UPGMA](/upgma/) on the similarities) has revenue at least $1/3$ of the best revenue, and so does a random binary tree in expectation.
- **Admissible costs.** Cohen-Addad, Kanade, Mallmann-Trenn and Mathieu (2019) call a cost of the form $\sum w_{ij} g(|\text{leaves}(i \vee j)|)$ admissible if, on data with a planted hierarchy, the planted tree has the least cost. Dasgupta's cost, with $g(m) = m$, is the main example.
- **[Sparsest cut](/sparsest-cut-problem/).** The ratio $w(A, B)/(|A| \cdot |B|)$ of a split. The cost by nodes shows why a split of low ratio is a good top split.
- **[Divisive clustering](/divisive-clustering/).** Recursive sparsest cut is a divisive method. [Bisecting k-means](/bisecting-k-means/) is another, and Moseley and Wang also studied it for the revenue.
- **Cophenetic distance.** For a dendrogram, $u(i, j)$ is the height of $i \vee j$. Dasgupta's cost uses the size of $i \vee j$ in place of its height.

## References
