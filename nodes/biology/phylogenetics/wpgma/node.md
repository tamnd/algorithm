---
tag: 76VTZ9
kind: algorithm
slug: wpgma
name: WPGMA
aliases:
- weighted pair group method with arithmetic mean
area: biology/phylogenetics
level: intro
summary: Like UPGMA, but the distance from a merged cluster is the plain mean of the distances from its two parts. Exact on ultrametrics, O(n^3) time.
solves: [ultrametric-tree-reconstruction]
model: word-ram
complexity:
  vars: {n: the number of taxa}
  time: {worst: "O(n^3)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1966
  people: [Louis L. McQuitty]
  note: McQuitty described the equal-weight update in 1966. The pair-group methods of Sokal and Michener (1958) are the common origin of WPGMA and UPGMA.
prereqs: [upgma, ultrametric, linkage-criterion]
see_also: [ultrametric-tree-reconstruction, ultrametric-tree-fitting-upgma-check, lance-williams-formula, agglomerative-clustering, neighbor-joining, molecular-clock]
sources:
  - paper: doi:10.1177/001316446602600402
    title: Louis L. McQuitty, Similarity analysis by reciprocal pairs for discrete and continuous data, Educational and Psychological Measurement 26(4), 1966, pages 825 to 831
    locator: the clustering of reciprocal pairs with the equal-weight update
  - paper: "Robert R. Sokal and Charles D. Michener, A statistical method for evaluating systematic relationships, University of Kansas Science Bulletin 38, 1958"
    title: Sokal and Michener 1958
    locator: pages 1409 to 1438, the pair-group methods with arithmetic averages
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, 2004
    locator: Chapter 11, Distance matrix methods, UPGMA and its weighted version
---

WPGMA (weighted pair group method with arithmetic mean) builds a rooted [phylogenetic tree](/phylogenetic-tree/) from a distance matrix of $n$ taxa in the same way as [UPGMA](/upgma/), with one change. When it merges clusters $A$ and $B$, the distance from the new cluster to another cluster $K$ is $(D_{AK} + D_{BK}) / 2$, so the two parts get equal weight whatever their sizes. On an [ultrametric](/ultrametric/) it returns the same tree as UPGMA, the true one, in $O(n^3)$ time. McQuitty described this update in 1966; in the [Lance-Williams](/lance-williams-formula/) family it is the "weighted average" or McQuitty linkage.

## In plain words

WPGMA builds a rooted tree by joining the two closest groups again and again, and it puts each new ancestor halfway up the distance between the two groups. The difference from UPGMA is how it measures the distance from a new group to the other groups. UPGMA averages over all members, so a big group counts more. WPGMA takes the plain average of the two old distances, so a group of ten species and a single species count the same. This makes the work per step simple, but it gives more weight to species that joined late. When the distances follow a strict clock, both averages give the same numbers, so both methods rebuild the same correct tree.

## The problem

The input is $n \ge 1$ taxa and a symmetric $n \times n$ matrix $D$ with zero diagonal and entries at least 0. The output is a rooted binary tree with the taxa as leaves at height 0 and a height for each internal node; the tree gives two leaves the distance $2\, h(\mathrm{lca}(x, y))$. The exact goal is [ultrametric tree reconstruction](/ultrametric-tree-reconstruction/): if $D_{xz} \le \max(D_{xy}, D_{yz})$ for all triples, return the tree that realizes $D$.

## The algorithm

```pseudo id=main
WPGMA(D, n)
L1  C ← {{1}, ..., {n}}; each leaf has height 0
L2  while |C| > 1 do
L3      (A, B) ← a pair of clusters in C with the smallest D_AB
L4      create a node u with children A and B; h(u) ← D_AB / 2
L5      for each K ∈ C \ {A, B} do D_uK ← D_Ku ← (D_AK + D_BK) / 2
L6      C ← (C \ {A, B}) ∪ {u}
L7  return the tree
```

The only difference from UPGMA is line L5, which does not need the cluster sizes. Unrolling line L5 gives a closed form: if a leaf $x$ of cluster $X$ is at depth $t_x$ below the root of the subtree of $X$, then
$$D_{XK} = \sum_{x \in X} \sum_{k \in K} 2^{-t_x}\, 2^{-t_k}\, D_{xk}.$$
At the start each leaf has depth 0, weight 1, and $D_{\{x\}\{k\}} = D_{xk}$. When $A$ and $B$ merge, each of their leaves goes one level deeper, so its weight halves, and line L5 gives $\frac{1}{2}D_{AK} + \frac{1}{2}D_{BK}$, which is the sum above for $A \cup B$. The weights of each cluster add up to 1, so $D_{XK}$ is a weighted average of leaf distances. "Weighted" in the name refers to these unequal weights of the leaves.

## Example

The five taxa A to E have this matrix. It is a metric but not an ultrametric.

| | A | B | C | D | E |
|---|---|---|---|---|---|
| A | 0 | 9 | 5 | 3 | 7 |
| B | 9 | 0 | 7 | 7 | 8 |
| C | 5 | 7 | 0 | 2 | 8 |
| D | 3 | 7 | 2 | 0 | 9 |
| E | 7 | 8 | 8 | 9 | 0 |

**Passes 1 and 2 are the same in both methods.** C and D merge at height 1 into $u_1$, with entries $(5 + 3)/2 = 4$ to A, $7$ to B and $17/2$ to E. Then A and $u_1$ merge at height 2 into $u_2 = \{A, C, D\}$.

**Pass 3 differs.** The entries from $u_2$ are:

| entry | UPGMA, by size | WPGMA, equal weights |
|---|---|---|
| $u_2$ to B | $(1 \cdot 9 + 2 \cdot 7)/3 = 23/3$ | $(9 + 7)/2 = 8$ |
| $u_2$ to E | $(1 \cdot 7 + 2 \cdot 17/2)/3 = 8$ | $(7 + 17/2)/2 = 31/4$ |

With $D_{BE} = 8$, UPGMA merges B with $u_2$ at height 23/6, and WPGMA merges E with $u_2$ at height 31/8. Both roots end at height 4. The trees are `(E,(B,(A,(C,D))));` for UPGMA and `(B,(E,(A,(C,D))));` for WPGMA. In WPGMA the leaf A, which joined last, has weight 1/2 in the distance from $u_2$, while C and D have weight 1/4 each.

## Correctness

If $D$ is an ultrametric, WPGMA returns a tree with $2\,h(\mathrm{lca}(x, y)) = D_{xy}$ for all pairs, with edge lengths at least 0. The proof is the invariant used for UPGMA: all leaf distances between two current clusters are equal and stored, each subtree reproduces the distances inside its cluster, and twice the height of a cluster is between its diameter and its distance to any outside leaf. For the closest pair $A, B$ and another cluster $K$, the three-point condition on a triple of leaves forces $D_{AK} = D_{BK}$, so any average of the two, with any weights, is that common value. On every input the merge heights never decrease, so the output is an ultrametric tree. The full proof is in the proof file.

## Complexity

The model is the word RAM with unit-cost arithmetic. Line L3 scans $O(r^2)$ pairs of the $r$ current clusters, and line L5 takes $O(r)$ time. Over $n - 1$ passes the time is $O(n^3)$ in the worst case, with $O(n^2)$ space. The update of line L5 is reducible, since $D_{uK} \ge \min(D_{AK}, D_{BK})$, so the [nearest-neighbor chain](/nearest-neighbor-chain/) algorithm gives the same tree in $O(n^2)$ time when ties are broken the same way.

## Properties

- **Exact on ultrametrics,** with the same tree as UPGMA, [single linkage](/single-linkage-clustering/) and [complete linkage](/complete-linkage-clustering/).
- **Always ultrametric output.** Merge heights never decrease.
- **Dyadic leaf weights.** Each cluster distance is the weighted average with weights $2^{-t_x}$ shown above. Leaves that join a cluster late get large weights.
- **No sizes needed.** The update uses only the two old entries, so a program does not keep cluster sizes.
- **Not exact on tree metrics.** Like UPGMA it needs a clock; on a [tree metric](/tree-metric/) with unequal rates it can return a wrong topology.

## Variants and improvements

- **[UPGMA](/upgma/)** weights by cluster size, so every leaf pair counts the same.
- **Median linkage** (WPGMC) uses the same equal weights on cluster centers in Euclidean space; it is not monotone, so its heights can decrease.
- **[Neighbor-joining](/neighbor-joining/)** drops the clock and is exact on all tree metrics.

## When to use it

Use WPGMA when a program or a standard asks for it, or when you want each merged subgroup to count once regardless of how many taxa it has, for example when one subgroup is sampled much more densely than the others. On ultrametric data it is the same as UPGMA. On data without a clock both are poor tree estimators, and the choice between them matters less than the choice of a better method.

## Pitfalls

- **Confusing the names.** "Weighted" here means unequal weights for the leaves, which comes from equal weights for the two clusters. Check the update rule, not only the name; R's `hclust` calls this method `"mcquitty"` and calls UPGMA `"average"`.
- **Assuming the same tree as UPGMA.** On non-ultrametric data the trees can differ, as in the example.
- **Halving the height.** The new node is at $D_{AB}/2$, not at $D_{AB}$.
- **Ties.** As with UPGMA, ties in line L3 on non-ultrametric data make the output depend on the tie rule.

## Implementations

## History

Sokal and Michener (1958) introduced pair-group methods with arithmetic averages for numerical taxonomy. McQuitty (1966) clustered reciprocal pairs and averaged the two merged groups with equal weights, and the [Lance-Williams formula](/lance-williams-formula/) later put this update in a common family with the other linkages.

## References
