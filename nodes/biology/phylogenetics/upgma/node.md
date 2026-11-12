---
tag: B7HW1Z
kind: algorithm
slug: upgma
name: UPGMA
aliases:
- Average-linkage clustering
- group average clustering
- unweighted pair group method with arithmetic mean
area: biology/phylogenetics
level: intro
summary: Merges the two clusters at the smallest average distance and puts the new node at half that distance. Returns the exact tree of an ultrametric matrix, in O(n^3) time.
solves: [ultrametric-tree-reconstruction]
model: word-ram
complexity:
  vars: {n: the number of taxa}
  time: {worst: "O(n^3)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1958
  people: [Robert R. Sokal, Charles D. Michener]
  note: Sokal and Michener introduced pair-group methods with arithmetic averages for numerical taxonomy in 1958.
prereqs: [ultrametric-tree-reconstruction, ultrametric, agglomerative-clustering, linkage-criterion]
see_also: [wpgma, ultrametric-tree-fitting-upgma-check, neighbor-joining, molecular-clock, dendrogram, lance-williams-formula, nearest-neighbor-chain, progressive-alignment]
sources:
  - paper: "Robert R. Sokal and Charles D. Michener, A statistical method for evaluating systematic relationships, University of Kansas Science Bulletin 38, 1958"
    title: Sokal and Michener 1958
    locator: pages 1409 to 1438, the pair-group methods with arithmetic averages
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, 2004
    locator: Chapter 11, Distance matrix methods, the section on UPGMA and the molecular clock
  - book: isbn:9780521629713
    title: Richard Durbin, Sean Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, 1998
    locator: Chapter 7, the UPGMA algorithm and the molecular clock
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, 1997
    locator: Chapter 17, ultrametric trees and ultrametric distances
---

UPGMA (unweighted pair group method with arithmetic mean) builds a rooted [phylogenetic tree](/phylogenetic-tree/) from a distance matrix of $n$ taxa. It is [agglomerative clustering](/agglomerative-clustering/) with the average [linkage criterion](/linkage-criterion/): it merges the two clusters whose average distance $\delta$ is smallest and puts their common ancestor at height $\delta/2$. When the matrix is an [ultrametric](/ultrametric/), as it is under a strict [molecular clock](/molecular-clock/), UPGMA returns the true rooted tree with its heights. The method goes back to Sokal and Michener (1958) and runs in $O(n^3)$ time.

## In plain words

UPGMA assumes that all species evolve at the same speed. Then the distance between two species is twice the time back to their common ancestor, and the two closest species must be relatives on the tree. The method starts with each species in its own group. It finds the two groups that are closest, joins them under a new ancestor, and places that ancestor halfway up the distance between them. The distance from the new group to any other group is the average of all distances between their members. It repeats until one group is left. The result is a rooted tree in which all species are at the same depth. When the equal-speed assumption fails, the closest pair may not be relatives, and the tree can be wrong.

## The problem

The input is $n \ge 1$ taxa and a symmetric $n \times n$ matrix $D$ with $D_{ii} = 0$ and $D_{ij} \ge 0$. The method reads only distances, not the $m$ sites of an alignment. The output is a rooted binary tree with the taxa as leaves at height 0 and a height $h(v) \ge 0$ for each internal node; an edge from $v$ to its child $c$ has length $h(v) - h(c)$. The distance that the tree gives to two leaves is $2\, h(\mathrm{lca}(x, y))$, twice the height of their lowest common ancestor.

The exact goal is [ultrametric tree reconstruction](/ultrametric-tree-reconstruction/): if $D$ satisfies the three-point condition $D_{xz} \le \max(D_{xy}, D_{yz})$, return the tree that realizes $D$. On other inputs UPGMA returns an ultrametric tree that approximates $D$, with no optimality guarantee.

## The algorithm

```pseudo id=main
UPGMA(D, n)
L1  C ← {{1}, ..., {n}}; each leaf has height 0 and size 1
L2  while |C| > 1 do
L3      (A, B) ← a pair of clusters in C with the smallest D_AB
L4      create a node u with children A and B; h(u) ← D_AB / 2
L5      the edges (u, A) and (u, B) get lengths h(u) − h(A) and h(u) − h(B)
L6      for each K ∈ C \ {A, B} do D_uK ← D_Ku ← (|A| D_AK + |B| D_BK) / (|A| + |B|)
L7      C ← (C \ {A, B}) ∪ {u}; |u| ← |A| + |B|
L8  return the tree
```

Line L6 is the [Lance-Williams](/lance-williams-formula/) update for the average: since $D_{AK}$ is the mean over $|A| \cdot |K|$ leaf pairs and $D_{BK}$ over $|B| \cdot |K|$ pairs, the size-weighted mean is the mean over all leaf pairs between $A \cup B$ and $K$. So the stored entry is always the plain average of the original distances, and the method never needs to look at them again. "Unweighted" in the name means that every leaf pair counts the same; the method that gives the two merged clusters equal weight instead is [WPGMA](/wpgma/).

## Example

**An ultrametric input.** The matrix comes from the rooted tree in which A and B meet at height 1, D and E at height 2, C joins D and E at height 3, and the root is at height 5.

| | A | B | C | D | E |
|---|---|---|---|---|---|
| A | 0 | 2 | 10 | 10 | 10 |
| B | 2 | 0 | 10 | 10 | 10 |
| C | 10 | 10 | 0 | 6 | 6 |
| D | 10 | 10 | 6 | 0 | 4 |
| E | 10 | 10 | 6 | 4 | 0 |

| pass | merge | $D_{AB}$ | height | new entries |
|---|---|---|---|---|
| 1 | A, B into $u_1$ | 2 | 1 | $u_1$: C 10, D 10, E 10 |
| 2 | D, E into $u_2$ | 4 | 2 | $u_2$: $u_1$ 10, C 6 |
| 3 | C, $u_2$ into $u_3$ | 6 | 3 | $u_3$: $u_1$ $(1 \cdot 10 + 2 \cdot 10)/3 = 10$ |
| 4 | $u_1$, $u_3$ into the root | 10 | 5 | none |

The output `((A:1,B:1):4,(C:3,(D:2,E:2):1):2);` gives every pair its input distance. In each pass the two entries that line L6 averages are equal, as the proof shows they must be on an ultrametric.

**An input without a clock.** The four taxa below have the tree metric of the unrooted tree `((A:1,B:5):1,(C:1,D:4));`, so the true pairs of neighbors are A with B and C with D. The rates differ: B and D are on long edges.

| | A | B | C | D |
|---|---|---|---|---|
| A | 0 | 6 | 3 | 6 |
| B | 6 | 0 | 7 | 10 |
| C | 3 | 7 | 0 | 5 |
| D | 6 | 10 | 5 | 0 |

UPGMA merges A and C at height 3/2, because $D_{AC} = 3$ is the smallest entry. The new entries are $(6 + 7)/2 = 13/2$ to B and $(6 + 5)/2 = 11/2$ to D, so it next merges $\{A, C\}$ with D at height 11/4. The last entry is $(2 \cdot 13/2 + 1 \cdot 10)/3 = 23/3$, which puts the root at 23/6. The output `(((A,C),D),B);` has the wrong topology. [Neighbor-joining](/neighbor-joining/) recovers the true tree from the same matrix.

## Correctness

If $D$ is an ultrametric, UPGMA returns a tree whose cophenetic distance $2\,h(\mathrm{lca}(x, y))$ equals $D_{xy}$ for every pair, and all its edge lengths are at least 0. The proof keeps three facts for the current clusters: all leaf distances between two clusters are equal to the stored entry; each subtree reproduces the distances inside its cluster; and the diameter of a cluster is at most twice its height, which is at most the distance to any leaf outside. When $A$ and $B$ are the closest pair and $K$ is another cluster, the three-point condition on a triple of leaves from $A$, $B$ and $K$ forces $D_{AK} = D_{BK}$, so the average in line L6 is that common value and the facts survive the merge. On any input, the heights of the merges never decrease, so the output is always an ultrametric tree. The full proof is in the proof file.

## Complexity

The model is the word RAM with unit-cost arithmetic on the entries.

- **Line L3.** Scanning all pairs of the current $r$ clusters takes $O(r^2)$ time.
- **Lines L4 to L7.** $O(r)$ time.

There are $n - 1$ passes, so the time is $O(n^3)$ in the worst case, with $O(n^2)$ space for the matrix. Average linkage is *reducible*: a merged cluster is never closer to a third cluster than the nearer of its two parts. So the [nearest-neighbor chain](/nearest-neighbor-chain/) algorithm builds the same tree in $O(n^2)$ time and $O(n^2)$ space; ties must be broken the same way for the trees to be identical. Keeping a [priority queue](/priority-queue/) of the rows gives $O(n^2 \log n)$ time.

## Properties

- **Exact on ultrametrics.** Proved above. The tree is unique once edges of length 0 are contracted, because the clusters are the classes of the relations $D_{xy} \le t$ for the values $t$ in the matrix.
- **Always ultrametric output.** Merge heights never decrease, so the output is a valid rooted tree with all leaves at the same depth, even when the input has no clock.
- **Same tree as other linkages on ultrametrics.** On an ultrametric, the averaged entries are equal, so [single linkage](/single-linkage-clustering/), [complete linkage](/complete-linkage-clustering/), WPGMA and UPGMA give the same tree.
- **Not exact on tree metrics.** A [tree metric](/tree-metric/) that is not an ultrametric can lead it to a wrong topology, as in the second example. It needs the clock, not only additivity.
- **Rooted output.** Unlike most distance methods, UPGMA places a root, at the last merge.

## Variants and improvements

- **[WPGMA](/wpgma/)** averages the two merged clusters with equal weights. It gives the same tree on ultrametrics.
- **Other linkages.** Single and complete linkage use the minimum and the maximum in line L6; [Ward's method](/ward-method/) uses squared Euclidean distances. They are general clustering methods, not tree estimators.
- **Testing the clock.** The page [UPGMA ultrametric check](/ultrametric-tree-fitting-upgma-check/) tests whether a matrix is an ultrametric and how well the UPGMA tree fits it.
- **Optimal fits.** When the data are not ultrametric, a best ultrametric under a chosen norm is a separate problem; see [ultrametric tree reconstruction](/ultrametric-tree-reconstruction/).

## When to use it

Use UPGMA when the data really are ultrametric or close to it: for example, distances that are times since divergence, or sequences that follow a clock well. It is also a quick guide-tree method for [progressive alignment](/progressive-alignment/), as in MUSCLE and MAFFT, where speed matters more than the exact topology. For sequences that evolve at different rates, use [neighbor-joining](/neighbor-joining/) or a likelihood method instead.

## Pitfalls

- **Using it without a clock.** UPGMA is wrong on tree metrics with unequal rates, as the second example shows. Check the three-point condition first, or use neighbor-joining.
- **Weighted versus unweighted.** Averaging $D_{AK}$ and $D_{BK}$ with equal weights is WPGMA. Programs and papers mix the two names, so check which update a program uses.
- **Halving the height.** The new node is at height $D_{AB}/2$, not $D_{AB}$, because the distance runs from one leaf up to the ancestor and down to the other.
- **Ties.** On non-ultrametric data, ties in line L3 can change the topology, so the output depends on the tie rule and on the order of the taxa.
- **Reading the root as real.** The root comes from the clock assumption. If the clock fails, the root position is not evidence about the order of events.

## Implementations

## History

Sokal and Michener (1958) introduced pair-group methods with arithmetic averages for numerical taxonomy, the classification of organisms from many measured characters. The method became one of the standard clustering methods of numerical taxonomy, and later the standard distance method for trees under a molecular clock. Felsenstein (2004, Chapter 11) describes its use and its failure without a clock.

## References
