---
tag: M7PPXT
kind: algorithm
slug: clique-subspace-clustering
name: CLIQUE subspace clustering
aliases:
- grid-based subspace clustering
- Clustering In QUEst
area: machine-learning/clustering
level: advanced
summary: "Cuts each attribute into xi intervals, finds the dense units of all subspaces bottom-up by an Apriori-style join and prune, and reports connected dense units as clusters with DNF descriptions."
solves: [subspace-clustering-problem]
model: real-ram
complexity:
  vars: {N: the number of points, k: the largest dimension of a dense unit, c: a constant that depends on the data and on xi}
  time: {worst: "O(c^k + N k)"}
  space: {extra: "O(c^k)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1998
  people: [Rakesh Agrawal, Johannes Gehrke, Dimitrios Gunopulos, Prabhakar Raghavan]
  note: Agrawal, Gehrke, Gunopulos and Raghavan presented CLIQUE at SIGMOD 1998, bringing the level-wise search of the Apriori algorithm for frequent itemsets to dense regions of subspaces. A journal version appeared in Data Mining and Knowledge Discovery in 2005.
prereqs: [subspace-clustering-problem, connected-components]
see_also: [dbscan, density-based-clustering-problem, grid-file, greedy-set-cover, biclustering-problem, feature-selection, principal-component-analysis, k-means]
sources:
  - paper: doi:10.1145/276304.276314
    title: "Rakesh Agrawal, Johannes Gehrke, Dimitrios Gunopulos and Prabhakar Raghavan, Automatic subspace clustering of high dimensional data for data mining applications, Proceedings of ACM SIGMOD 1998, pages 94 to 105"
    locator: "Section 2 (units, dense units with threshold tau, clusters as connected dense units, regions and minimal DNF descriptions), Section 3.1 (bottom-up search, the monotonicity lemma, candidate generation by join and prune, MDL pruning of subspaces, the O(c^k + m k) time and k passes), Section 3.2 (connected components by depth-first search) and Section 3.3 (greedy growth of maximal regions and removal of redundant regions)"
  - paper: "Rakesh Agrawal, Johannes Gehrke, Dimitrios Gunopulos and Prabhakar Raghavan, Automatic subspace clustering of high dimensional data, Data Mining and Knowledge Discovery 11(1), 2005, pages 5 to 33"
    locator: the journal version, with the same algorithm and more experiments
  - paper: "Rakesh Agrawal and Ramakrishnan Srikant, Fast algorithms for mining association rules, Proceedings of the 20th International Conference on Very Large Data Bases (VLDB 1994), pages 487 to 499"
    locator: "the Apriori candidate generation (join on the first k - 2 items, then prune by the (k - 1)-subsets) that CLIQUE reuses"
  - paper: doi:10.1145/1497577.1497578
    title: "Hans-Peter Kriegel, Peer Kröger and Arthur Zimek, Clustering high-dimensional data: a survey on subspace clustering, pattern-based clustering, and correlation clustering, ACM Transactions on Knowledge Discovery from Data 3(1), 2009, article 1"
    locator: "CLIQUE as the first bottom-up, grid-based axis-parallel subspace clustering algorithm, and its successors ENCLUS, MAFIA and SUBCLU"
---

CLIQUE finds clusters in subspaces of high-dimensional data, the [subspace clustering problem](/subspace-clustering-problem/) in its axis-parallel form. It cuts each attribute into $\xi$ equal intervals, which makes a grid of *units* in every subspace, and calls a unit *dense* if it holds more than a fraction $\tau$ of the $N$ points. Density is *downward closed*: if a unit is dense in a set $S$ of attributes, its projection onto any subset of $S$ is dense too. So CLIQUE finds the dense units bottom-up, one dimension per pass over the data, generating the $k$-dimensional candidates from the $(k-1)$-dimensional dense units with the join and prune step of the Apriori algorithm for frequent itemsets. A cluster is a maximal set of connected dense units in one subspace, and CLIQUE describes each cluster by a short DNF expression, a union of axis-parallel boxes. For a given $\xi$ and $\tau$ it finds every dense unit in every subspace, without looking at all $2^d - 1$ subspaces.

## In plain words

Draw a grid on your data: cut every column of numbers into a few equal ranges. A cell of the grid is "busy" if more than a set share of the points falls in it.

Start with single columns and mark the busy ranges. Then look at pairs of columns, but only at cells whose two ranges were each busy alone, because a cell cannot be busy if one of its sides is not. Count those cells. Then go to triples, built only from busy pairs, and so on, until nothing is busy any more.

In each set of columns, busy cells that touch form a group. Each group is then written as a short rule such as "age from 20 to 40 and income from 30 to 50", so people can read why the points belong together.

## The algorithm

The input is $N$ points in $d$ attributes, each attribute with a known range (or the range of the data), the number of intervals $\xi$ and the density threshold $\tau \in [0, 1)$. A *$k$-dimensional unit* is a choice of $k$ distinct attributes $a_1 < \cdots < a_k$ and one interval for each; a point is in the unit if its value in each $a_j$ lies in the chosen interval. The unit is *dense* if it holds more than $\tau N$ points.

```pseudo id=main
CLIQUE(D, ξ, τ)
L1  map each point to its grid cell: one of ξ intervals per attribute
L2  U_1 ← the 1-dimensional units with more than τN points      ▷ one pass over D
L3  for k ← 2, 3, ... while U_{k-1} ≠ ∅
L4      C_k ← join each pair of units of U_{k-1} that agree on their first k-2 (attribute, interval) pairs and whose last attributes a < a' differ
L5      remove from C_k each unit with a (k-1)-dimensional projection that is not in U_{k-1}
L6      U_k ← the units of C_k with more than τN points        ▷ one pass over D
L7  for each subspace S that has dense units
L8      clusters of S ← the connected components of its dense units, two units being adjacent if they share a common face
L9      for each cluster, grow maximal regions greedily from uncovered units until the cluster is covered
L10     remove regions whose units are all covered by the other regions, smallest first, and output the rest as a DNF
```

**Units as itemsets.** Write a unit as the sorted tuple of its (attribute, interval) pairs. Line L4 is the Apriori join: two dense units with the same first $k - 2$ pairs and different last attributes give one candidate with $k$ pairs. Line L5 is the Apriori prune.

**Adjacency.** Two units of the same subspace share a common face if they agree in all attributes but one, and in that one their intervals are next to each other. A cluster is a connected component of this graph; line L8 finds it by depth-first search, as for [connected components](/connected-components/).

**Regions and DNF.** A *region* is an axis-parallel box of units, one range of intervals per attribute of $S$. It is *maximal* in a cluster if it lies in the cluster and cannot be extended by one interval in any direction. Line L9 picks an uncovered unit, extends it along the first attribute as far as possible (up, then down), then along the second with the whole slab, and so on. A cover by regions $R_1, \ldots, R_r$ gives the description $R_1 \lor \cdots \lor R_r$, where each $R_i$ is a conjunction $\bigwedge_{a \in S} (\ell_a \le x_a < h_a)$.

## Example

Twenty points in $d = 3$ attributes, all in $[0, 8]$, with $\xi = 4$ intervals $[0, 2), [2, 4), [4, 6), [6, 8]$ per attribute and $\tau = 1/5$, so a unit is dense if it holds more than $4$ points:

- $a_1, \ldots, a_{10}$: $x_1 \in [0, 4)$ (five in each of the first two intervals), $x_2 \in [0, 2)$, and $x_3$ spread over all of $[0, 8]$;
- $b_1, \ldots, b_6$: $x_2 \in [4, 6)$, $x_3 \in [6, 8]$, and $x_1$ spread over $[0, 8]$ (0.5, 2.5, 4.5, 5.5, 6.5, 7.5);
- four noise points (5, 2.5, 1), (7, 7.5, 2.5), (5.5, 6.5, 4.5), (6.5, 3, 0.5).

**Pass 1 (line L2).** The dense 1-dimensional units are $x_1 \in [0, 2)$ (6 points), $x_1 \in [2, 4)$ (6), $x_2 \in [0, 2)$ (10), $x_2 \in [4, 6)$ (6), $x_3 \in [0, 2)$ (5: three of the $a_i$ and two noise points) and $x_3 \in [6, 8]$ (8).

**Pass 2 (lines L4 to L6).** The join gives $2 \cdot 2 \cdot 3 = 12$ candidates, one per pair of these units on different attributes, and none is pruned. Counting keeps three:

| unit | points |
|---|---|
| $x_1 \in [0, 2) \land x_2 \in [0, 2)$ | 5 |
| $x_1 \in [2, 4) \land x_2 \in [0, 2)$ | 5 |
| $x_2 \in [4, 6) \land x_3 \in [6, 8]$ | 6 |

**Pass 3.** The join needs two dense 2-dimensional units with the same first pair. The two units that start with an $x_1$ pair have different $x_1$ intervals, and the third unit is the only one that starts with $x_2$, so $C_3 = \emptyset$ and the loop stops. A brute force over all $2^3 - 1 = 7$ subspaces and all their units finds the same 9 dense units.

**Clusters and descriptions (lines L7 to L10).** There are 7 clusters:

| subspace | cluster | DNF |
|---|---|---|
| $\{x_1, x_2\}$ | $a_1, \ldots, a_{10}$ | $(0 \le x_1 < 4) \land (0 \le x_2 < 2)$ |
| $\{x_2, x_3\}$ | $b_1, \ldots, b_6$ | $(4 \le x_2 < 6) \land (6 \le x_3 \le 8)$ |
| $\{x_1\}$ | 12 points | $0 \le x_1 < 4$ |
| $\{x_2\}$ | two clusters | $0 \le x_2 < 2$; $4 \le x_2 < 6$ |
| $\{x_3\}$ | two clusters | $0 \le x_3 < 2$; $6 \le x_3 \le 8$ |

The two adjacent units of $\{x_1, x_2\}$ form one cluster and one region. The two planted clusters appear in their own two-dimensional subspaces, and in the full space there is nothing dense. The one-dimensional clusters are the projections that downward closure promises, plus the noise-driven $x_3 \in [0, 2)$.

**A redundant region.** Take a cluster of four units in a 2-dimensional subspace, a staircase with interval pairs $(0, 0), (0, 1), (1, 1), (1, 2)$. Line L9 grows $\{0\} \times [0, 1]$ from $(0, 0)$, then $[0, 1] \times \{1\}$ from $(1, 1)$, then $\{1\} \times [1, 2]$ from $(1, 2)$. All three are maximal, but the middle one is covered by the other two, so line L10 removes it, and the description has two terms.

## Correctness

The full proof is in the correctness proof. In short:

1. *Downward closure.* If a unit $u$ in $S$ is dense and $T \subset S$ is not empty, the projection of $u$ onto $T$ contains every point of $u$, so it is dense.
2. *The candidates are complete.* Let $c$ be a $k$-dimensional unit whose $(k-1)$-dimensional projections are all dense. Drop its last pair to get $u$ and its second-to-last pair to get $v$. Both are dense, they share the first $k - 2$ pairs, and the last attribute of $u$ is smaller than that of $v$, so line L4 joins them into $c$, and line L5 keeps $c$. Conversely, every unit that survives line L5 has all its projections dense.
3. *Induction.* By 1 and 2, $C_k$ contains every dense $k$-dimensional unit, so $U_k$ is exactly the set of dense $k$-dimensional units. If $U_{k-1} = \emptyset$, there is no dense unit of dimension $k$ or more, so the loop stops with all dense units found, after at most $d$ passes.
4. *Clusters and covers.* Line L8 returns the connected components. Each region of line L9 lies in the cluster and is maximal; each unit is covered when its turn comes; line L10 removes only regions whose units stay covered. So the DNF describes exactly the points of the cluster.

The tests check point 3 against a brute force over all $2^d - 1$ subspaces on random data, the downward closure, the equality of $C_k$ with "all projections dense", the components against union-find, and that each cover is exact, made of maximal regions and free of redundant ones.

## Complexity

Agrawal and others give the time of the dense-unit search as $O(c^k + N k)$, where $k$ is the largest dimension of a dense unit and $c$ is a constant. The reason: a dense $k$-dimensional unit has $2^k - 1$ dense projections, all of which are generated and counted, so the number of candidates grows like $c^k$; and the search makes $k$ passes over the $N$ points, each with a cost per point that does not depend on $N$ when the candidates sit in a hash tree. Factors that depend on $d$ and $\xi$ are hidden in $c$.

- **In the implementation.** Pass $k$ costs $O(N \cdot s_k \cdot k)$ for $s_k$ candidate subspaces, with a hash set per subspace, and the join costs $O(|U_{k-1}|^2 k)$.
- **Clusters.** The depth-first search touches each dense unit and its $2k$ possible neighbors, $O(k)$ hash lookups each.
- **Covers.** Growing one region checks each unit of each slab once per extension, which is polynomial in the number of dense units of the cluster. A cover with the fewest regions is NP-hard in general, which is why lines L9 and L10 are greedy.
- **Space.** The dense units and the candidates of one level, plus the grid cells of the points, $O(N d)$.

## Properties

- **Complete for the grid.** It finds every dense unit of every subspace, for the given $\xi$ and $\tau$.
- **Insensitive to the order of the points.** The counts do not depend on the order.
- **No number of clusters.** Clusters come out of the density threshold, not from a given $k$.
- **Overlapping output.** A point can be in clusters of several subspaces.
- **Interpretable.** Each cluster comes with a DNF description over intervals of named attributes.
- **Scales linearly in $N$.** The number of passes is the largest dimension of a dense unit, not $d$.

## Variants and improvements

- **MDL pruning.** CLIQUE can keep only the subspaces with high *coverage* (the fraction of points in their dense units), choosing the cut by the minimum description length principle. This speeds up the search but can lose clusters.
- **ENCLUS** (Cheng, Fu and Zhang 1999) ranks subspaces by the entropy of the grid instead of a fixed density.
- **MAFIA** (Goil, Nagesh and Choudhary 1999) uses adaptive intervals from the histogram of each attribute and a parallel implementation.
- **SUBCLU** (Kailing, Kriegel and Kröger 2004) keeps the bottom-up idea but replaces grid density with [DBSCAN](/dbscan/) density, which is also downward closed.
- **Density with a threshold that grows with dimension.** Later methods note that a fixed $\tau$ favors low-dimensional subspaces, and scale the threshold with $k$.

## When to use it

Use CLIQUE when the data has tens of attributes, clusters are expected to be axis-parallel and dense in a few of them, you want readable descriptions of each cluster, and you do not know the number of clusters. Avoid it when clusters are tilted (correlated attributes), when the right grid size is unclear and the result changes a lot with $\xi$, or when the dense units reach high dimension, where the $c^k$ term dominates.

## Pitfalls

- **Grid boundaries.** A cluster that straddles an interval boundary is split between units, and each part may fall below $\tau$. Try more than one $\xi$ or shifted grids.
- **A fixed threshold across dimensions.** With $\xi$ intervals, a uniform random point falls in a given $k$-dimensional unit with probability $\xi^{-k}$. The same $\tau$ is easy to reach in one dimension and very hard in ten, so CLIQUE reports many low-dimensional and few high-dimensional clusters.
- **Redundant output.** By downward closure every projection of a cluster is reported too. Keep only clusters in maximal subspaces if that is what you need.
- **Strict inequality.** "Dense" means more than $\tau N$ points. Off-by-one errors here change the units at the boundary.
- **The top value.** The largest value of an attribute must go into the last interval, not into an interval $\xi$ that does not exist.

## Implementations

## History

Agrawal, Gehrke, Gunopulos and Raghavan introduced CLIQUE at SIGMOD 1998, in the IBM Quest data mining project, and with it the problem of finding clusters in all subspaces. They took the level-wise candidate generation of the Apriori algorithm of Agrawal and Srikant (1994) for frequent itemsets and applied it to grid units, using the downward closure of density in place of the Apriori property of support. ENCLUS and MAFIA (1999) followed with other grids, PROCLUS (1999) started the top-down projected clustering line, and SUBCLU (2004) moved the bottom-up search to density-based clusters. The journal version of CLIQUE appeared in 2005.

## References
