---
tag: TFYKXG
kind: theorem
slug: kleinberg-impossibility-theorem
name: Kleinberg's impossibility theorem
aliases:
- impossibility theorem for clustering
- Kleinberg's clustering axioms
area: machine-learning/clustering
level: advanced
summary: For n >= 2 points, no clustering function is scale invariant, rich and consistent at once. Single linkage with a suitable stopping rule has any two of the three properties.
prereqs: [clustering-problem, set-partitions]
see_also: [single-linkage-clustering, kruskal, minimum-spanning-tree, maximum-spacing-k-clustering, k-means-problem, ultrametric, cluster-validity]
sources:
  - paper: "Jon Kleinberg, An impossibility theorem for clustering, Advances in Neural Information Processing Systems 15 (NIPS 2002), MIT Press, 2003"
    locator: Theorem 2.1 (the impossibility), Theorem 2.2 (single linkage with the k-cluster, distance-r and scale-alpha stopping conditions), Theorems 3.1 and 3.2 (the range of a scale-invariant consistent function is an antichain, and each antichain is such a range), Section 4 (centroid-based functions are not consistent), Section 5 (relaxations)
  - paper: "Margareta Ackerman and Shai Ben-David, Measures of clustering quality, a working set of axioms for clustering, Advances in Neural Information Processing Systems 21 (NIPS 2008)"
    locator: the versions of scale invariance, richness and consistency for measures of clustering quality, which can hold together
  - paper: "Reza Bosagh Zadeh and Shai Ben-David, A uniqueness theorem for clustering, Proceedings of the 25th Conference on Uncertainty in Artificial Intelligence (UAI 2009)"
    locator: the axioms with a fixed number k of clusters, and the characterization of single linkage among such functions
---

Kleinberg's impossibility theorem says that there is no clustering function with three natural properties at once. Scale invariance: multiplying all distances by the same factor does not change the clusters. Richness: every partition of the points is the output for some distances. Consistency: making distances inside clusters smaller and distances between clusters larger does not change the clusters. Jon Kleinberg proved it in 2002 for every set of $n \ge 2$ points. Each two of the three properties are possible together: [single linkage](/single-linkage-clustering/) with three different stopping rules gives each pair. The theorem shows that every [clustering](/clustering-problem/) method gives up something, which is one reason why there are many methods and many [validity](/cluster-validity/) criteria.

## Statement

**Setting.** $S$ is a set of $n \ge 2$ points. A **distance function** on $S$ is a function $d: S \times S \to \mathbb{R}$ with $d(i, j) \ge 0$, $d(i, j) = 0$ if and only if $i = j$, and $d(i, j) = d(j, i)$. The triangle inequality is not needed, so $d$ need not be a [metric](/metric-space/). A **clustering function** $f$ maps each distance function $d$ on $S$ to a [partition](/set-partitions/) $f(d)$ of $S$. The number of clusters is not an input: $f$ chooses it.

For a partition $\Gamma$ and distance functions $d$ and $d'$, $d'$ is a **$\Gamma$-transformation** of $d$ if $d'(i, j) \le d(i, j)$ whenever $i$ and $j$ are in the same cluster of $\Gamma$, and $d'(i, j) \ge d(i, j)$ whenever they are in different clusters. A partition $\Gamma$ **refines** a partition $\Gamma'$ if each cluster of $\Gamma$ lies inside a cluster of $\Gamma'$.

**The three properties.**

1. **Scale invariance.** $f(\alpha \cdot d) = f(d)$ for every distance function $d$ and every $\alpha > 0$.
2. **Richness.** $\mathrm{Range}(f)$ is the set of all partitions of $S$.
3. **Consistency.** If $f(d) = \Gamma$ and $d'$ is a $\Gamma$-transformation of $d$, then $f(d') = \Gamma$.

**Theorem (Kleinberg 2002, Theorem 2.1).** For each $n \ge 2$, there is no clustering function on $n$ points that satisfies scale invariance, richness and consistency.

**Theorem (antichains, Theorem 3.1).** If $f$ is scale invariant and consistent, then no two distinct partitions in $\mathrm{Range}(f)$ are such that one refines the other. That is, $\mathrm{Range}(f)$ is an antichain in the refinement order.

## In plain words

Imagine any rule that takes the distances between some points and puts the points into groups. We ask three things of the rule. If we measure all distances in a different unit, the groups stay the same. Any grouping at all can come out, for the right distances. If we move points of the same group closer together and points of different groups farther apart, the groups stay the same.

Each wish sounds harmless, and any two of them can hold together. The theorem says that all three cannot. The reason is that the first and third wishes stop the rule from producing two groupings where one is a finer version of the other. But the second wish needs the grouping where every point is alone and also the grouping with one big group, and the first is a finer version of the second.

## Proof

The proof first shows the antichain theorem and then derives the impossibility from it.

**Conforming and forcing.** Fix a partition $\Gamma$ and numbers $0 < a < b$. A distance function $d$ is **$(a, b)$-conforming** to $\Gamma$ if $d(i, j) \le a$ for all $i \ne j$ in the same cluster of $\Gamma$ and $d(i, j) \ge b$ for all $i, j$ in different clusters. The pair $(a, b)$ is **$\Gamma$-forcing** for $f$ if $f(d) = \Gamma$ for every $d$ that is $(a, b)$-conforming to $\Gamma$.

**Lemma 1.** If $f$ is consistent and $\Gamma \in \mathrm{Range}(f)$, then some pair $0 < a < b$ is $\Gamma$-forcing.

*Proof.* Take $d$ with $f(d) = \Gamma$. Let $a_d$ be the smallest value $d(i, j)$ over pairs $i \ne j$ in the same cluster, and $b_d$ the largest value over pairs in different clusters. If there are no pairs of one kind, use 1 for the missing value. Choose $0 < a < b$ with $a \le a_d$ and $b \ge b_d$. Let $d'$ be $(a, b)$-conforming to $\Gamma$. For $i \ne j$ in the same cluster, $d'(i, j) \le a \le a_d \le d(i, j)$. For $i, j$ in different clusters, $d'(i, j) \ge b \ge b_d \ge d(i, j)$. So $d'$ is a $\Gamma$-transformation of $d$, and consistency gives $f(d') = \Gamma$. $\square$

**Proof of the antichain theorem.** Let $f$ be scale invariant and consistent. Assume, for a contradiction, that $\Gamma_0$ and $\Gamma_1$ are distinct partitions in $\mathrm{Range}(f)$ and that $\Gamma_0$ refines $\Gamma_1$. By Lemma 1, there are pairs $(a_0, b_0)$ that is $\Gamma_0$-forcing and $(a_1, b_1)$ that is $\Gamma_1$-forcing, with $a_0 < b_0$ and $a_1 < b_1$.

Let $a_2 = a_1$, and choose $\varepsilon$ with $0 < \varepsilon < a_0 a_2 / b_0$. Define $d$ on $S$ by

$$d(i, j) = \begin{cases} \varepsilon & \text{if } i \ne j \text{ are in the same cluster of } \Gamma_0, \\ a_2 & \text{if } i, j \text{ are in the same cluster of } \Gamma_1 \text{ but in different clusters of } \Gamma_0, \\ b_1 & \text{if } i, j \text{ are in different clusters of } \Gamma_1. \end{cases}$$

Because $\Gamma_0$ refines $\Gamma_1$, each pair falls into exactly one case, and $d$ is a distance function, because all three values are positive.

*Step 1: $f(d) = \Gamma_1$.* Inside a cluster of $\Gamma_1$, the values are $\varepsilon$ or $a_2$. Here $\varepsilon < a_0 a_2/b_0 < a_2 = a_1$, because $a_0 < b_0$. Between clusters of $\Gamma_1$, the value is $b_1$. So $d$ is $(a_1, b_1)$-conforming to $\Gamma_1$, and $f(d) = \Gamma_1$.

*Step 2: $f(\alpha d) = \Gamma_0$ for $\alpha = b_0 / a_2$.* Inside a cluster of $\Gamma_0$, $\alpha d(i, j) = b_0 \varepsilon / a_2 < a_0$ by the choice of $\varepsilon$. Between clusters of $\Gamma_0$, the value of $\alpha d$ is either $\alpha a_2 = b_0$ or $\alpha b_1 = b_0 b_1 / a_2 > b_0$, since $b_1 > a_1 = a_2$. So $\alpha d$ is $(a_0, b_0)$-conforming to $\Gamma_0$, and $f(\alpha d) = \Gamma_0$.

*Step 3.* Scale invariance gives $f(\alpha d) = f(d)$, so $\Gamma_0 = \Gamma_1$, against the assumption. So $\mathrm{Range}(f)$ is an antichain. $\square$

**Proof of the impossibility theorem.** Let $f$ be scale invariant, rich and consistent, with $n \ge 2$. By richness, the partition $\Gamma_0$ into $n$ singletons and the partition $\Gamma_1 = \{S\}$ are both in $\mathrm{Range}(f)$. They are distinct because $n \ge 2$, and $\Gamma_0$ refines $\Gamma_1$. This contradicts the antichain theorem. $\square$

The proof uses only two partitions from richness. So the theorem stays true with a much weaker richness. Every partition is refined by the all-singletons partition, so a scale-invariant and consistent function that outputs the all-singletons partition for some input outputs no other partition for any input.

## Consequences

- **Every method gives up one property.** A method that fixes the number $k$ of clusters gives up richness. A method that cuts at a fixed distance gives up scale invariance. A method that cuts at a fixed fraction of the largest distance gives up consistency. The Tightness section shows each case for single linkage.
- **Centroid methods are not consistent.** Kleinberg also shows (Section 4) that for every $k \ge 2$ and $n$ large enough relative to $k$, the clustering functions that minimize a centroid cost, a class that includes the [k-means problem](/k-means-problem/) and the k-median problem, are not consistent. Moving points closer inside a cluster can make the optimal $k$ centers move and split a cluster differently.
- **The ranges that are possible.** The antichain theorem has a converse (Theorem 3.2): every antichain of partitions is the range of some scale-invariant and consistent function. So for these two properties, the antichain condition is exactly the limit on richness.
- **Relaxations.** In Section 5, Kleinberg replaces consistency by refinement-consistency, in which the output after a $\Gamma$-transformation may be a refinement of $\Gamma$. The impossibility still holds with full richness. If richness may miss only the all-singletons partition, scale invariance and refinement-consistency become possible together, for example with single linkage that stops at a distance of $\alpha$ times the smallest distance, for a fixed $\alpha \ge 1$.
- **Axioms for other objects.** Ackerman and Ben-David apply versions of the three properties to measures of clustering quality, not to clustering functions, and the versions can hold together. Zadeh and Ben-David fix $k$ and replace richness by $k$-richness, and then characterize single linkage among functions with these properties.
## Tightness

The three properties cannot hold together, but each two can (Theorem 2.2). All three examples are single linkage: sort the pairs $\{i, j\}$ by $d(i, j)$, break ties in a fixed order of the pairs, and add the edges one at a time to a graph on $S$, as in [Kruskal's algorithm](/kruskal/). The clusters are the connected components when a stopping condition holds.

**1. Stop at $k$ clusters (any $k \ge 1$, $n \ge k$): scale invariant and consistent, not rich.** Scaling does not change the order of the edges, so the output does not change. For consistency, let $\Gamma$ be the output for $d$ and $F$ the set of edges that were added; $F$ spans each cluster with a tree. Every edge between two clusters comes after all edges of $F$ in the order: an earlier one would have joined two components that end up in different clusters. Under a $\Gamma$-transformation $d'$, the edges of $F$ do not get longer and the edges between clusters do not get shorter, so this still holds, also with ties. Before the first edge between clusters, the algorithm sees all edges of $F$, and the components are then exactly the clusters of $\Gamma$, which are $k$ in number, so it stops with $\Gamma$. The output always has $k$ clusters, so it is not rich.

**2. Stop at distance $r$ (any $r > 0$): rich and consistent, not scale invariant.** Add exactly the edges with $d(i, j) \le r$. For richness, given $\Gamma$, set $d = r/2$ inside clusters and $d = 2r$ between clusters; the output is $\Gamma$. For consistency, each cluster of the output is connected by edges of length at most $r$, and these do not get longer; each edge between clusters has length more than $r$, and it does not get shorter. Scaling changes which edges are at most $r$.

**3. Stop at a fraction $\alpha$ of the largest distance (any $0 < \alpha < 1$, $n \ge 3$): scale invariant and rich, not consistent.** Add the edges with $d(i, j) \le \alpha \rho$, where $\rho$ is the largest distance. Scaling $d$ scales $\rho$ in the same way. For richness with two or more clusters, set $d = \alpha/2$ inside and $d = 1$ between. For the single cluster, give one pair the distance 1 and all others $\alpha$: with $n \ge 3$, the complete graph minus one edge is connected. With $n = 2$ the only edge is the longest one, which is never added, so the one-cluster partition never occurs.

**Concrete checks for $n = 3$.** On the 216 distance functions with values in $\{1, \ldots, 6\}$, with the scale factors $1/3$, $1/2$, $2$, $3$ and $7/3$:

- With $k = 2$, every output has two clusters, so the range misses $\{\{0, 1, 2\}\}$ and $\{\{0\}, \{1\}, \{2\}\}$. The three partitions with two clusters form an antichain, as the theorem requires.
- With $r = 3$, the distances $d(0, 1) = d(0, 2) = d(1, 2) = 2$ give one cluster, and the same distances times 2 give three singletons. So scale invariance fails.
- With $\alpha = 1/2$, the distances $d(0, 1) = 2$, $d(0, 2) = 3$, $d(1, 2) = 4$ give $\rho = 4$, threshold 2, and the clusters $\{0, 1\}, \{2\}$. Increase the distance $d(1, 2)$ between the clusters to 6. This is a $\Gamma$-transformation, but now $\rho = 6$, the threshold is 3, the edge $\{0, 2\}$ is added, and the output is one cluster. So consistency fails.

On all of these inputs, each of the three functions keeps its other two properties.

## History

Kleinberg presented the theorem at NIPS 2002, with the explicit analogy to Arrow's impossibility theorem in social choice: a few natural axioms that no single procedure can meet. Earlier axiomatic work on clustering had studied hierarchical methods; Jardine and Sibson (1971) showed that single linkage is the only hierarchical method that meets their axioms on maps to [ultrametrics](/ultrametric/). Kleinberg's setting is different because $f$ returns one partition and chooses the number of clusters itself. Later work changed the object of the axioms: Ackerman and Ben-David (2008) put them on quality measures, and Zadeh and Ben-David (2009) fixed $k$. Both found consistent sets of axioms that way.

## References
