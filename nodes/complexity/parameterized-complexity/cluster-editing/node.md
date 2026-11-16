---
tag: NF40MG
kind: problem
slug: cluster-editing
name: Cluster editing
aliases:
- correlation clustering editing
area: complexity/parameterized-complexity
level: advanced
summary: "Add or delete at most k edges so that the graph becomes a disjoint union of cliques. FPT in k: O(1.62^k + n + m) time and a kernel with 2k vertices; no 2^o(k) algorithm under ETH."
prereqs: [bounded-search-tree, kernel]
see_also: [correlation-clustering, bounded-search-tree, kernel, polynomial-kernel, edge-clique-cover, subexponential-parameterized-algorithm, parameterized-vertex-cover, fixed-parameter-tractable]
sources:
  - paper: doi:10.1016/j.dam.2004.01.007
    title: "Ron Shamir, Roded Sharan and Dekel Tsur, Cluster graph modification problems, Discrete Applied Mathematics 144(1-2), 173-182 (2004)"
    locator: NP-completeness of cluster editing and cluster deletion
  - paper: doi:10.1016/j.jda.2012.04.005
    title: "Sebastian Böcker, A golden ratio parameterized algorithm for cluster editing, Journal of Discrete Algorithms 16, 79-89 (2012)"
    locator: O(1.62^k + m + n) time
  - paper: doi:10.1016/j.jcss.2011.04.001
    title: "Jianer Chen and Jie Meng, A 2k kernel for the cluster editing problem, Journal of Computer and System Sciences 78(1), 211-220 (2012)"
    locator: kernel with at most 2k vertices
  - paper: doi:10.1016/j.dam.2012.05.019
    title: "Christian Komusiewicz and Johannes Uhlmann, Cluster editing with locally bounded modifications, Discrete Applied Mathematics 160(15), 2259-2270 (2012)"
    locator: no 2^o(k) n^O(1) algorithm unless ETH fails
  - paper: doi:10.1016/j.jcss.2014.04.015
    title: "Fedor V. Fomin, Stefan Kratsch, Marcin Pilipczuk, Michal Pilipczuk and Yngve Villanger, Tight bounds for parameterized complexity of cluster editing with a small number of clusters, Journal of Computer and System Sciences 80(7), 1430-1447 (2014)"
    locator: 2^(O(sqrt(pk))) + n^O(1) for at most p clusters, and matching lower bounds under ETH
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 2, Kernelization (cluster editing); Chapter 3, Bounded search trees
---

Cluster editing asks whether at most $k$ edge additions and deletions turn a graph into a *cluster graph*, a disjoint union of cliques. The parameter is $k$. It is the unweighted form of [correlation clustering](/correlation-clustering/) on a complete graph with $+$ and $-$ labels. Shamir, Sharan and Tsur proved it NP-complete in 2004. It is [fixed-parameter tractable](/fixed-parameter-tractable/): a simple search tree gives $O^\ast(3^k)$, where $O^\ast$ hides polynomial factors, Böcker gave $O(1.62^k + n + m)$, and Chen and Meng gave a [kernel](/kernel/) with $2k$ vertices. Under the exponential time hypothesis (ETH) there is no $2^{o(k)} n^{O(1)}$ algorithm, but with at most $p$ clusters the problem is subexponential.

## In plain words

You have a network of people, and a link means that two people are similar. You want to split them into groups so that everyone in a group is linked to everyone else in the group, and no links go between groups. The data has errors, so you may add or remove at most $k$ links.

A graph is a union of groups exactly when no three people $u, v, w$ have $u$ linked to $v$, $v$ linked to $w$, but $u$ not linked to $w$. Each such triple must be fixed by one of three edits, so a search tries the three edits and has at most $3^k$ leaves. Better rules lower the number of branches, and simple data reduction shrinks any input to at most $2k$ people.

## Definition

- Instance: an undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges, given by adjacency lists, and an integer $k \ge 0$.
- Parameter: $k$.
- Question: is there a set $F$ of at most $k$ vertex pairs such that the graph $(V, E \mathbin{\triangle} F)$ is a cluster graph?

Here $E \mathbin{\triangle} F$ is the symmetric difference: pairs of $F$ that are edges are deleted, and the others are added.

**Lemma.** A graph is a cluster graph if and only if it has no induced path on three vertices, $P_3$.

*Proof.* In a cluster graph, two neighbors of a vertex lie in its clique, so they are adjacent. Conversely, with no induced $P_3$, adjacency is transitive, so each component is a clique. $\square$

## Variants

- **Cluster deletion.** Only deletions are allowed. It is also NP-complete (Shamir, Sharan and Tsur). The answers can differ, as the example below shows.
- **Cluster completion.** Only additions are allowed. Then the components of $G$ must become cliques, so the answer is the number of missing edges inside components, computed in polynomial time.
- **At most $p$ clusters.** Fomin, Kratsch, Pilipczuk, Pilipczuk and Villanger solved this version in $2^{O(\sqrt{pk})} + n^{O(1)}$ time and showed that the bound is tight under ETH.
- **Weighted cluster editing.** Each pair has a cost for editing, and the budget bounds the total cost. This is correlation clustering in the decision form.
- **Cluster vertex deletion.** Delete at most $k$ vertices to get a cluster graph. It is a hitting set problem for induced $P_3$, with a $3^k$ search tree by the same argument.

## Examples

A scratch script took the graph on $1, \ldots, 6$ with the 8 edges $12$, $13$, $23$, $34$, $45$, $46$, $56$, $24$: two triangles $123$ and $456$ joined by the edges $34$ and $24$.

- It has 6 induced $P_3$s. Over all $B_6 = 203$ partitions of the vertices, the least editing cost is 2, reached only by the clusters $\{1, 2, 3\}$, $\{4, 5, 6\}$: delete $34$ and $24$. The least cluster deletion cost is also 2, with the same clusters.
- The search tree that branches on the first induced $P_3$ answers NO for $k = 0$ after 1 leaf, NO for $k = 1$ after 3 failed leaves, and YES for $k = 2$.

The graph $K_4$ minus the edge $14$ has 2 induced $P_3$s, $1, 2, 4$ and $1, 3, 4$. Cluster editing needs 1 edit: add $14$. Cluster deletion needs 2 deletions, for example the edges $12$ and $13$, with clusters $\{1\}$ and $\{2, 3, 4\}$.

## Known algorithms

- **Search tree on induced $P_3$.** Find $u, v, w$ with $uv, vw \in E$ and $uw \notin E$. Branch into deleting $uv$, deleting $vw$, or adding $uw$, and mark the edited pair as fixed. This gives $O^\ast(3^k)$. See [bounded search tree](/bounded-search-tree/).
- **Böcker (2012).** $O(1.62^k + n + m)$ time, with a branching that uses edge weights after merging vertices. The base $1.62$ is the golden ratio rounded up.
- **Chen and Meng (2012).** A kernel with at most $2k$ vertices, computed in polynomial time.
- **At most $p$ clusters.** $2^{O(\sqrt{pk})} + n^{O(1)}$ time (Fomin, Kratsch, Pilipczuk, Pilipczuk and Villanger).

## Bounds

- **Classical complexity.** NP-complete under polynomial-time many-one reductions (Shamir, Sharan and Tsur 2004).
- **Lower bound in time.** No $2^{o(k)} n^{O(1)}$ algorithm exists unless ETH fails (Komusiewicz and Uhlmann; Fomin et al.). With at most $p$ clusters, the $2^{O(\sqrt{pk})}$ bound is tight under ETH.
- **Kernels.** A kernel with $2k$ vertices exists, so the kernel is linear in vertices and has $O(k^2)$ edges. See [polynomial kernel](/polynomial-kernel/).

## Reductions

- **To hitting set with sets of size 3.** Each induced $P_3$ gives the set of its three vertex pairs, and a solution must contain a pair from each set. After an edit new $P_3$s may appear, so this is not a plain reduction, but it is the reason for the $3^k$ search tree.
- **To correlation clustering.** Label each edge $+$ and each non-edge $-$. A clustering that disagrees with $d$ labels is a cluster editing set of size $d$. So cluster editing is correlation clustering on complete graphs with unit weights.

## Applications

Cluster editing models clustering of data with a similarity graph: genes or proteins with similar expression, documents with similar content, or records that refer to the same entity. The edits are the errors that the clustering must accept. Exact algorithms based on the kernel and on search trees are practical when the number of edits is small compared with the size of the data.

## References
