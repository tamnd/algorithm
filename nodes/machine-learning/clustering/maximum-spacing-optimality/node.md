---
tag: QN9SAE
kind: theorem
slug: maximum-spacing-optimality
name: Single-linkage spacing optimality
aliases:
- maximum spacing theorem
area: machine-learning/clustering
level: advanced
summary: "Kruskal's algorithm stopped at k components, which is the single-linkage cut into k clusters, gives the largest spacing among all k-clusterings."
prereqs: [maximum-spacing-k-clustering, kruskal, exchange-argument]
see_also: [single-linkage-clustering, minimum-spanning-tree, cut-property, cycle-property, greedy-stays-ahead, dendrogram, slink, disjoint-set]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 4.7 (Clustering), the statement that deleting the k - 1 most expensive edges of a minimum spanning tree gives a k-clustering of maximum spacing, with its proof
  - paper: doi:10.2307/2346439
    title: "J. C. Gower and G. J. S. Ross, Minimum spanning trees and single linkage cluster analysis, Journal of the Royal Statistical Society Series C 18(1) (1969), 54-64"
    locator: the single linkage clusters as the parts of a minimum spanning tree after the deletion of its longest edges
  - paper: doi:10.1109/T-C.1971.223083
    title: "C. T. Zahn, Graph-theoretical methods for detecting and describing gestalt clusters, IEEE Transactions on Computers C-20(1) (1971), 68-86"
    locator: clustering by the deletion of inconsistent long edges of a minimum spanning tree
---

The maximum spacing theorem says that [Kruskal's algorithm](/kruskal/), stopped when $k$ components are left, solves the [maximum-spacing k-clustering](/maximum-spacing-k-clustering/) problem: no partition of the points into $k$ clusters has a larger least distance between clusters. The components are the cut of the [single-linkage](/single-linkage-clustering/) tree into $k$ clusters, and also the parts of a [minimum spanning tree](/minimum-spanning-tree/) after the deletion of its $k - 1$ longest edges. The proof is an [exchange argument](/exchange-argument/) in the form of Kleinberg and Tardos: a different clustering must cut a path of short edges.

## Statement

Let $U$ be a set of $n$ points with distances $d(p, q) = d(q, p) \ge 0$, and let $2 \le k \le n$. A *$k$-clustering* is a partition $\mathcal{C}$ of $U$ into $k$ nonempty sets, and its *spacing* is

$$\text{spacing}(\mathcal{C}) = \min\{d(p, q) : p, q \text{ in different sets of } \mathcal{C}\}.$$

Run Kruskal's algorithm on the complete graph on $U$: take the pairs in an order of nondecreasing distance, with ties in any order, and add a pair as an edge when its ends are in different components. Stop when exactly $k$ components are left. Call them $\mathcal{C}^* = \{C_1^*, \ldots, C_k^*\}$, and let $d^* = \text{spacing}(\mathcal{C}^*)$.

**Theorem.** For each $k$-clustering $\mathcal{C}$, $\text{spacing}(\mathcal{C}) \le d^*$. So $\mathcal{C}^*$ is a $k$-clustering of maximum spacing. Also $d^*$ is the distance of the next edge that Kruskal's algorithm would add, which is the $(k - 1)$-th largest edge weight of the minimum spanning tree.

## In plain words

Kruskal's algorithm joins the closest pairs first. When it stops at $k$ groups, every pair that it joined is at most as far apart as the closest pair of different groups. Now take any other way to make $k$ groups. It must split some group of Kruskal's into two. That group is held together by a path of short joins, and somewhere the path crosses from one of the new groups to another. That crossing pair is close, so the other way has a gap no larger than Kruskal's.

## Proof

**Step 1: the edges inside the components are short.** At the stop, each pair that the algorithm has looked at has both ends in one component: either it was added, which joined its ends, or it was skipped because its ends were already joined, and components only grow. Each pair $p, q$ in different components of $\mathcal{C}^*$ has therefore not been looked at yet, so it comes after all the added edges in the order. Since the order does not decrease, each added edge $e$ has

$$d(e) \le d(p, q) \quad \text{for each pair } p, q \text{ in different components}.$$

Taking the least such pair gives $d(e) \le d^*$ for each added edge $e$.

**Step 2: a different clustering splits a component.** Let $\mathcal{C} \ne \mathcal{C}^*$ be a $k$-clustering. Suppose that each $C_r^*$ lies inside one set of $\mathcal{C}$. Then each set of $\mathcal{C}$ is a union of sets of $\mathcal{C}^*$, and it is nonempty, so it holds at least one of them. There are $k$ sets on each side, so each set of $\mathcal{C}$ is exactly one set of $\mathcal{C}^*$, and $\mathcal{C} = \mathcal{C}^*$, which is false. So some component $C_r^*$ has two points $p$, $q$ in different sets of $\mathcal{C}$, say $p \in A$ and $q \notin A$ for a set $A$ of $\mathcal{C}$.

**Step 3: the path crosses.** The component $C_r^*$ is connected by added edges, so it has a path $p = x_0, x_1, \ldots, x_s = q$ in which each $\{x_{t-1}, x_t\}$ is an added edge. Let $t$ be the first index with $x_t \notin A$. It exists because $x_s = q \notin A$, and $t \ge 1$ because $x_0 = p \in A$. Then $x_{t-1} \in A$ and $x_t \notin A$, so $x_{t-1}$ and $x_t$ are in different sets of $\mathcal{C}$, and by Step 1

$$\text{spacing}(\mathcal{C}) \le d(x_{t-1}, x_t) \le d^*.$$

For $\mathcal{C} = \mathcal{C}^*$ the bound holds with equality. So no $k$-clustering has spacing larger than $d^*$.

**Step 4: the value.** The algorithm stops after it adds $n - k$ edges. If it went on, it would skip pairs inside components and add the first pair in the order whose ends are in different components. By Step 1, all such pairs come after the added edges, and the first of them has the least distance among them, which is $d^*$. So $d^*$ is the weight of the $(n - k + 1)$-th edge that Kruskal's algorithm adds. With the tree weights $w_1 \le \cdots \le w_{n-1}$ in the order of addition, $d^* = w_{n-k+1}$, the $(k - 1)$-th largest. $\square$

## Consequences

- **Single linkage is optimal at every level.** The cut of the single linkage [dendrogram](/dendrogram/) into $k$ clusters is $\mathcal{C}^*$ for each $k$, so one tree holds an optimal clustering for every $k$ at once.
- **Deletion of the longest tree edges.** Each minimum spanning tree is the output of Kruskal's algorithm for some order of the ties. So deleting the $k - 1$ longest edges of any minimum spanning tree, built by [Prim's algorithm](/prim/), [SLINK](/slink/) or another method, gives a clustering of maximum spacing.
- **The best spacing does not increase with $k$.** It is $w_{n-k+1}$, and $w$ does not decrease.
- **A fast exact algorithm.** The problem takes $\Theta(n^2)$ time for a general distance and $O(n \log n)$ time in the Euclidean plane, while most other clustering objectives are NP-hard.
- **Only the order matters.** An increasing change of all distances does not change $\mathcal{C}^*$.

## Tightness

- **The bound is attained.** $\mathcal{C}^*$ has spacing exactly $d^*$.
- **Uniqueness with distinct distances.** If all distances are different, the edges added before the stop are different pairs from the pair at $d^*$, so they are strictly shorter. Then Step 3 gives $\text{spacing}(\mathcal{C}) < d^*$ for each $\mathcal{C} \ne \mathcal{C}^*$, and the optimum is unique.
- **Ties allow several optima.** For the points $0, 1, 2$ on a line and $k = 2$, the clusterings $\{0\}, \{1, 2\}$ and $\{0, 1\}, \{2\}$ both have spacing 1.
- **Other cuts can be worse.** For $a, \ldots, f$ at $0, 2, 3, 7, 13, 21$ and $k = 3$, the optimum is $\{a, b, c, d\}, \{e\}, \{f\}$ with spacing 6, while the cut of [complete linkage](/complete-linkage-clustering/) has spacing 4.
- **Only for the spacing.** The theorem says nothing about the sizes or the diameters of the clusters. A long chain of close points stays in one cluster, and the largest diameter can be far from the least possible.

## History

Gower and Ross (1969) showed that single linkage clusters are the parts of a minimum spanning tree after the deletion of its longest edges. Zahn (1971) used the deletion of long tree edges for clustering in the plane. Kleinberg and Tardos (2006) gave the exchange proof of the maximum spacing theorem, in the form used here, as an application of Kruskal's algorithm.

## References
