---
tag: Q8SHE1
kind: algorithm
slug: hdbscan
name: HDBSCAN
aliases:
- hierarchical DBSCAN
- HDBSCAN*
- hierarchical density-based spatial clustering of applications with noise
area: machine-learning/clustering
level: advanced
summary: "Build the DBSCAN* hierarchy for all radii from one minimum spanning tree of mutual reachability distances, then keep the most stable clusters."
solves: [density-based-clustering-problem]
model: real-ram
complexity:
  vars: {n: the number of points, d: the number of features}
  time: {worst: "O(n^2 (d + log n))", best: "Θ(n^2 d)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, online: false, exact: true, recursive: false}
history:
  year: 2013
  people: [Ricardo J. G. B. Campello, Davoud Moulavi, Jörg Sander]
  note: Campello, Moulavi and Sander presented HDBSCAN* at PAKDD 2013. A journal version with Arthur Zimek followed in ACM TKDD in 2015.
prereqs: [dbscan, minimum-spanning-tree, single-linkage-clustering]
see_also: [optics, prim, dendrogram, ultrametric, euclidean-minimum-spanning-tree, k-nearest-neighbor-search, density-peak-clustering, mean-shift]
sources:
  - paper: doi:10.1007/978-3-642-37456-2_14
    title: "Ricardo J. G. B. Campello, Davoud Moulavi and Jörg Sander, Density-based clustering based on hierarchical density estimates, Advances in Knowledge Discovery and Data Mining (PAKDD 2013), Lecture Notes in Computer Science 7819, Springer, 2013"
    locator: the definitions of DBSCAN*, the core distance, the mutual reachability graph and its minimum spanning tree, the condensed hierarchy, cluster stability and the optimal selection of flat clusters
  - paper: doi:10.1145/2733381
    title: "Ricardo J. G. B. Campello, Davoud Moulavi, Arthur Zimek and Jörg Sander, Hierarchical density estimates for data clustering, visualization, and outlier detection, ACM Transactions on Knowledge Discovery from Data 10(1), 2015"
    locator: the full treatment of HDBSCAN*, the stability as excess of mass, the selection as an optimization over the cluster tree, and the GLOSH outlier scores
  - paper: doi:10.21105/joss.00205
    title: "Leland McInnes, John Healy and Steve Astels, hdbscan: hierarchical density based clustering, Journal of Open Source Software 2(11), 2017"
    locator: the widely used Python implementation
---

HDBSCAN (written HDBSCAN\* by its authors) is a [density-based clustering](/density-based-clustering-problem/) algorithm that runs [DBSCAN](/dbscan/) for every radius at once. It replaces the distance by the *mutual reachability distance*, which is at least the distance to the $m_{\mathrm{pts}}$-th nearest point of each end, builds one [minimum spanning tree](/minimum-spanning-tree/) of these distances, and reads off a hierarchy of clusters, as [single linkage](/single-linkage-clustering/) does. It then drops the clusters smaller than $m_{\mathrm{clSize}}$ and selects the flat set of clusters with the largest total *stability* by a dynamic program on the tree. The user gives no radius and no number of clusters. With brute force distances it takes $O(n^2 (d + \log n))$ time in the [real RAM](/real-ram/) model.

## In plain words

DBSCAN needs a circle size, and the right size changes from one region of the data to another. HDBSCAN tries every circle size.

Start with a huge circle: everything is one group. Shrink the circle slowly. Sparse points drop out first and become noise. Now and then a group breaks into two real groups. Groups that are too small to count are just points dropping out.

Record this as a tree of groups. A group that lives a long time while the circle shrinks, and keeps many points while it lives, is stable. At the end, pick groups from the tree so that no picked group lies inside another, and the total stability is as large as possible.

## The problem

The data model is clustering of points: the input is a set $D$ of $n$ points in $\mathbb{R}^d$ with the [Euclidean distance](/euclidean-distance/), or in any [metric space](/metric-space/), and two integers: $m_{\mathrm{pts}} \ge 1$, the density parameter of DBSCAN, and $m_{\mathrm{clSize}} \ge 1$, the smallest size of a cluster. Often $m_{\mathrm{clSize}} = m_{\mathrm{pts}}$. Campello et al. (2013) define:

- The **core distance** $\mathrm{core}(x)$ is the distance from $x$ to its $m_{\mathrm{pts}}$-th nearest point, $x$ itself counted.
- The **mutual reachability distance** is $d_m(x, y) = \max(\mathrm{core}(x), \mathrm{core}(y), \mathrm{dist}(x, y))$ for $x \ne y$.
- **DBSCAN\*** at radius $\varepsilon$ is DBSCAN without border points: the core points ($\mathrm{core}(x) \le \varepsilon$) joined when within $\varepsilon$ form the clusters, and every other point is noise. In the words of $d_m$, the clusters are the components of the graph on the points with $\mathrm{core}(x) \le \varepsilon$ and the edges with $d_m \le \varepsilon$.
- As $\varepsilon$ falls, the DBSCAN\* clusters are nested. With $\lambda = 1/\varepsilon$, a cluster $C$ is born at $\lambda_{\min}(C)$, and each point $x$ leaves it at $\lambda_{\max}(x, C)$, as noise or when $C$ splits or vanishes. The **stability** of $C$ is
$$S(C) = \sum_{x \in C} \big(\lambda_{\max}(x, C) - \lambda_{\min}(C)\big).$$
It is the excess of mass of $C$: the area of the part of the density level sets that belongs to $C$ and not to its parent.
- The **output** is a set of clusters of the condensed tree, no one inside another, with the largest total stability. The other points are noise.

## The algorithm

```pseudo id=main
HDBSCAN(D, m_pts, m_clSize)
L1  core(x) ← distance to the m_pts-th nearest point of x, x itself counted
L2  T ← a minimum spanning tree of the complete graph with weights d_m
L3  (tree, λ_min, λ_max) ← CONDENSE(T, core, m_clSize)
L4  S(C) ← Σ over x in C of (λ_max(x, C) − λ_min(C)), for each cluster C
L5  chosen ← SELECT(tree, S)
L6  label each point by the chosen cluster that holds it, NOISE if none
    return the labels

CONDENSE(T, core, m_clSize)
L7  active ← {root}, root holds D, λ_min(root) ← 0
L8  for each value w in {weights of T} ∪ {core distances}, from high to low do
L9      G_w ← points with core(x) < w, and edges of T with weight < w
L10     for each active cluster C do
L11         split C into components of G_w; big ← those with ≥ m_clSize points
L12         if one big component holds all of C then continue
L13         if exactly one is big then the other points leave C at λ = 1/w; C ← that component
L14         else every point leaves C at λ = 1/w; C is no longer active
L15             if two or more are big then each is a new active child of C, λ_min ← 1/w

SELECT(tree, S)
L16 for each cluster C, children before parents do
L17     if C is a leaf then best(C) ← S(C); sel(C) ← {C}
L18     else if S(C) ≥ Σ best(children) then best(C) ← S(C); sel(C) ← {C}
L19     else best(C) ← Σ best(children); sel(C) ← union of sel(children)
L20 return sel(root)                ▷ the root itself is not a candidate by default
```

Line L2 can use the dense form of [Prim's algorithm](/prim/), which needs no list of edges and computes each $d_m$ when it needs it. Lines L8 and L9 sweep the radius from large to small. At a value $w$, the graph $G_w$ holds what DBSCAN\* sees at every radius just below $w$. Line L13 is the key rule of the condensed tree: a component with fewer than $m_{\mathrm{clSize}}$ points that breaks off is not a new cluster. Its points are noise for the parent from then on. Only a split into two or more big parts makes children.

**Ties.** All tree edges of one weight are removed at the same level, so the result does not depend on which minimum spanning tree line L2 returns. When the stability of a cluster equals the sum for its children, line L18 keeps the cluster. The root, which holds all the data, is excluded unless the user allows a single cluster. If it were a candidate, its stability would often win and the output would be one cluster. The implementation by McInnes et al. has the option `allow_single_cluster` for this case.

## Example

Take the points 0, 1, 2, 3, 10, 11, 12, 13 and 30 on the line, with $m_{\mathrm{pts}} = 2$ and $m_{\mathrm{clSize}} = 3$.

The core distance is the distance to the nearest other point: 1 for each of the first eight points and 17 for the point 30. The mutual reachability distance between neighbors in each group is 1. Between 3 and 10 it is $\max(1, 1, 7) = 7$, and between 13 and 30 it is $\max(1, 17, 17) = 17$. The minimum spanning tree is the path through the points in order, with the weights 1, 1, 1, 7, 1, 1, 1, 17.

| level $w$ | $\lambda = 1/w$ | what happens |
|---|---|---|
| 17 | 1/17 | the point 30 drops out (its core distance is not below 17): it leaves the root as noise |
| 7 | 1/7 | the edge of weight 7 goes: the root splits into {0, 1, 2, 3} and {10, 11, 12, 13}, both of size at least 3, so they are two children born at 1/7 |
| 1 | 1 | no point has a core distance below 1: both children vanish |

The stabilities are $S(\mathrm{root}) = 8 \cdot \tfrac17 + \tfrac1{17} \approx 1.20$ and $S = 4 \cdot (1 - \tfrac17) = \tfrac{24}{7} \approx 3.43$ for each child. The two children win, so the labels are 0 for the first four points, 1 for the next four, and NOISE for 30. With $m_{\mathrm{clSize}} = 5$ the split at 1/7 makes no big component, so the root vanishes there and has no children. The root is not a candidate, so every point is noise.

## Correctness

The claim is that the output is the flat clustering that Campello et al. define: among the sets of clusters of the condensed DBSCAN\* hierarchy with no cluster inside another, one with the largest total stability. First, the DBSCAN\* clusters at radius $\varepsilon$ are the components of the graph with the vertices $\mathrm{core}(x) \le \varepsilon$ and the edges $d_m \le \varepsilon$. Second, by the cycle property, the edges of a minimum spanning tree below a threshold have the same components as all edges below it, so the tree holds the whole hierarchy, and the hierarchy changes only at the tree weights and the core distances. Third, the sweep applies the condensing rule at each of these values. Last, the best set in the subtree of a cluster either is the cluster alone or is a union of best sets of the children, which gives the recursion of lines L16 to L19. The full proof is below.

## Complexity

The model is the [real RAM](/real-ram/). Here $n$ is the number of points and $d$ the number of features.

- **Core distances.** Line L1 computes all $n^2$ distances and sorts each row, $O(n^2 (d + \log n))$ time. A selection algorithm or a [k-nearest neighbor](/k-nearest-neighbor-search/) index can replace the sort.
- **Spanning tree.** The dense form of Prim's algorithm takes $\Theta(n^2 d)$ time and $O(n)$ extra space, because the complete graph has $\Theta(n^2)$ edges and no edge list is stored. In low dimension the tree can be built faster with a [k-d tree](/kd-tree/) or a [ball tree](/ball-tree/) and a dual tree form of [Borůvka's algorithm](/boruvka/), as in the implementation by McInnes et al. The mutual reachability tree is not a [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/), so the Delaunay method does not apply directly.
- **Condensing.** The sweep has at most $2n - 1$ levels, each with a [union-find](/disjoint-set/) pass over $n - 1$ tree edges, so $O(n^2 \alpha(n))$ time as written. Sorting the tree edges once and walking the single linkage [dendrogram](/dendrogram/) from the top does the same in $O(n \log n)$ time.
- **Space.** The pseudocode keeps one exit value for each point and each cluster that holds it, $O(n^2)$ in the worst case of a deep tree. Storing for each cluster only its children and the points that leave it as noise, with the sizes, gives $O(n)$ space, since $S(C)$ can be summed from these records.
- **Selection.** Lines L16 to L20 are linear in the number of clusters, which is less than $2n / m_{\mathrm{clSize}}$.

## Properties

- **Exact for its definition.** The output is the optimum of the stability objective over the condensed tree, not an approximation. The objective itself is a modelling choice.
- **Order independence.** Unlike DBSCAN, there are no border points, so the result does not depend on the input order or on the choice of minimum spanning tree.
- **All radii at once.** Each horizontal cut of the hierarchy at $\varepsilon$ is DBSCAN\* at $(\varepsilon, m_{\mathrm{pts}})$, so clusters of different densities can come from different cuts.
- **Link to single linkage.** With $m_{\mathrm{pts}} = 2$, the core distance is the distance to the nearest other point, which is at most $\mathrm{dist}(x, y)$ for each $y \ne x$. So $d_m$ equals the distance, and the hierarchy is the single linkage hierarchy. Larger core distances are what make HDBSCAN robust to thin chains of noise points between clusters.
- **Link to OPTICS.** The reachability plot of [OPTICS](/optics/) with an infinite radius is the order of Prim's algorithm on a closely related graph, so both methods encode the same family of DBSCAN clusterings.
- **Hierarchy as ultrametric.** The merge levels of the tree define an [ultrametric](/ultrametric/) on the points.

## Variants and improvements

- **GLOSH.** Campello et al. (2015) define an outlier score for each point from the $\lambda$ at which it leaves its cluster, compared with the largest $\lambda$ in the cluster.
- **Semi-supervised selection.** The 2015 paper also selects clusters with constraints that say two points must or must not be in one cluster.
- **Leaf selection.** Taking the leaves of the condensed tree instead of the most stable clusters gives many small, homogeneous clusters.
- **Epsilon threshold.** Malzer and Baum (2020) merge selected clusters whose split happened below a given radius, so that HDBSCAN behaves like DBSCAN\* in dense parts.
- **Accelerated HDBSCAN.** McInnes and Healy (2017) build the tree with dual tree Borůvka on space partitioning trees, which is close to $O(n \log n)$ in practice in low dimension.

## When to use it

Use HDBSCAN when the clusters may have different densities, when there is noise, and when you know neither the number of clusters nor a radius. The parameter $m_{\mathrm{clSize}}$ is easier to choose than $\varepsilon$, because it is a count in the units of the problem. Avoid it when the dimension is high and the distances are not meaningful, or when every point must be in a cluster.

## Pitfalls

- **Does $m_{\mathrm{pts}}$ count the point itself?** The papers count it, as DBSCAN does. Some implementations do not. The two differ by one.
- **Duplicate points.** If $m_{\mathrm{pts}}$ or more points coincide, a core distance is 0 and $\lambda = 1/0$ is infinite. Remove duplicates or give them weights.
- **The single cluster case.** Without `allow_single_cluster`, data with one real cluster is split into its two largest parts or made all noise. The example above shows the second case.
- **Large $m_{\mathrm{pts}}$.** A large $m_{\mathrm{pts}}$ smooths the density and makes more points noise. It is a smoothing parameter, not a cluster size.
- **Cluster labels from different runs.** The numbering of the clusters is arbitrary. Compare runs with the [adjusted Rand index](/adjusted-rand-index/).

## Implementations

## History

Ricardo Campello, Davoud Moulavi and Jörg Sander presented HDBSCAN\* at the PAKDD conference in 2013. They built on DBSCAN (Ester et al. 1996), OPTICS (Ankerst et al. 1999), and the statistical view of clusters as the high density components of the level sets of a density (Hartigan 1975), with stability taken from the excess of mass of Müller and Sawitzki (1991). The journal version with Arthur Zimek in 2015 added outlier scores and semi-supervised selection. The Python library of McInnes, Healy and Astels, published in 2017, made the method widely used.

## References
