---
tag: DAQVWC
kind: problem
slug: ultrametric-tree-reconstruction
name: Ultrametric tree reconstruction
aliases:
- ultrametric fitting
- ultrametric tree fitting
area: biology/phylogenetics
level: core
summary: Given a distance matrix, find a rooted tree with all leaves at the same distance from the root that fits it exactly or best. Exact in O(n^2) time; L1 and L2 fits are NP-hard.
prereqs: [ultrametric, phylogenetic-tree-reconstruction]
see_also: [upgma, wpgma, ultrametric-tree-fitting-upgma-check, single-linkage-clustering, molecular-clock, additive-tree-reconstruction, dendrogram, hierarchical-clustering-problem]
sources:
  - paper: "Robert R. Sokal and Charles D. Michener, A statistical method for evaluating systematic relationships, University of Kansas Science Bulletin 38, 1958, pages 1409 to 1438"
    title: Sokal and Michener 1958
    locator: UPGMA, the average-linkage method that returns the tree of an ultrametric
  - paper: "Martin Farach, Sampath Kannan and Tandy Warnow, A robust model for finding optimal evolutionary trees, Algorithmica 13(1-2), 1995, pages 155 to 179"
    title: Farach, Kannan and Warnow 1995
    locator: the L-infinity fit of an ultrametric to a matrix in O(n^2) time
  - paper: "Victor Chepoi and Bernard Fichet, l-infinity approximation via subdominants, Journal of Mathematical Psychology 44(4), 2000, pages 600 to 616"
    title: Chepoi and Fichet 2000
    locator: the optimal L-infinity ultrametric as the subdominant shifted by half the largest gap
  - paper: doi:10.1007/BF02458863
    title: William H. E. Day, Computational complexity of inferring phylogenies from dissimilarity matrices, Bulletin of Mathematical Biology 49(4), 1987, pages 461 to 467
    locator: NP-hardness of the L1 and L2 fits by ultrametrics and by tree metrics
  - paper: "Mirko Křivánek and Jaroslav Morávek, NP-hard problems in hierarchical-tree clustering, Acta Informatica 23(3), 1986, pages 311 to 323"
    title: Křivánek and Morávek 1986
    locator: NP-hardness of fitting a hierarchical tree to a dissimilarity
  - paper: "Stephen C. Johnson, Hierarchical clustering schemes, Psychometrika 32(3), 1967, pages 241 to 254"
    title: Johnson 1967
    locator: the one-to-one correspondence between ultrametrics and hierarchical clusterings with levels
  - paper: "J. C. Gower and G. J. S. Ross, Minimum spanning trees and single linkage cluster analysis, Journal of the Royal Statistical Society, Series C (Applied Statistics) 18(1), 1969, pages 54 to 64"
    title: Gower and Ross 1969
    locator: single linkage from a minimum spanning tree
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, 1997
    locator: Chapter 17, ultrametric trees and the test of a matrix for the ultrametric property
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, 2004
    locator: Chapter 11, Distance matrix methods, UPGMA and the molecular clock
---

Ultrametric tree reconstruction is the problem of finding, from a matrix of distances between $n$ taxa, a rooted tree in which every leaf is at the same distance from the root and the path lengths between leaves fit the matrix. A matrix fits such a tree exactly if and only if it is an [ultrametric](/ultrametric/), and then the tree is unique and [UPGMA](/upgma/) or single linkage finds it. For data that are not ultrametric, the best fit in the maximum norm takes $O(n^2)$ time, and the best fits in the $L_1$ and $L_2$ norms are NP-hard. The model is a tree under a strict [molecular clock](/molecular-clock/).

## In plain words

Suppose all species change at the same constant rate. Then the distance between two species is twice the time since their last shared ancestor, and the tree can be drawn with the root at the top and all species on one line at the bottom. In such data, among any three species, the two largest of the three distances are equal. When the data pass this test, joining the closest pair again and again builds the one correct tree. Real data break the test because rates differ and measurements have errors. Then you want the clock tree that is closest to the data, which is easy for one way to measure closeness and hard for the usual ones.

## Definition

An **ultrametric tree** on a set $X$ of taxa is a rooted tree $T$ with leaf set $X$ and a height $h(v) \ge 0$ for each vertex, with $h = 0$ on the leaves and $h(u) > h(v)$ when $u$ is the parent of $v$. The edge from $u$ to $v$ has length $h(u) - h(v)$, so every leaf is at distance $h(\text{root})$ from the root, and the path length between leaves is
$$u_T(x, y) = 2\, h(\operatorname{lca}(x, y)).$$
A matrix $U$ is an **ultrametric** if $U(x, z) \le \max(U(x, y), U(y, z))$ for all $x, y, z$ (the three-point condition); equivalently, in each triple the two largest distances are equal.

**Exact version.** Given a symmetric matrix $D$ with zero diagonal and positive entries off it, find an ultrametric tree with $u_T = D$, or report that none exists. One exists if and only if $D$ is an ultrametric, and the tree with no vertex of out-degree 1 is unique.

**Fitting version.** For a norm, find an ultrametric tree that minimizes $\lVert D - u_T \rVert$. The usual norms are $L_\infty$ (the largest error), $L_1$ (the sum of absolute errors) and $L_2$ (the sum of squared errors).

## Variants

- **Subdominant.** Find the largest ultrametric $u^*$ with $u^* \le D$ in every entry. It exists, it is unique, and $u^*(x, y)$ is the smallest possible largest entry on a path from $x$ to $y$ in the complete graph weighted by $D$; this is the cophenetic matrix of [single linkage clustering](/single-linkage-clustering/).
- **Least squares.** The $L_2$ fit, for a fixed topology a [quadratic program](/quadratic-programming/) with order constraints on the heights; over all topologies NP-hard.
- **Not necessarily binary.** Ties in the data give a vertex with more than two children; a binary tree then has internal edges of length 0.
- **Dated trees.** With fossil dates or tip dates the heights are times, and the problem becomes a constrained fit of a time tree.
- **Clock-free.** Without the clock the problem is [additive tree reconstruction](/additive-tree-reconstruction/).

## Examples

**An ultrametric.** The matrix on A to E with $D_{AB} = 2$, $D_{DE} = 4$, $D_{CD} = D_{CE} = 6$ and all distances between $\{A, B\}$ and $\{C, D, E\}$ equal to 10 passes the three-point test on all ten triples. Its tree is `((A:1,B:1):4,(C:3,(D:2,E:2):1):2);`, with heights 1, 2, 3 and 5 for the four internal vertices. [UPGMA](/upgma/), [WPGMA](/wpgma/), single linkage and complete linkage all return this tree; the page of [UPGMA](/upgma/) runs it step by step.

**Not an ultrametric.** The matrix

| | A | B | C | D |
|---|---|---|---|---|
| A | 0 | 6 | 3 | 6 |
| B | 6 | 0 | 7 | 10 |
| C | 3 | 7 | 0 | 5 |
| D | 6 | 10 | 5 | 0 |

fails the test on all four triples: their sorted distances are $(3, 6, 7)$ for ABC, $(6, 6, 10)$ for ABD, $(3, 5, 6)$ for ACD and $(5, 7, 10)$ for BCD. Three fits:

| fit | AB | AC | AD | BC | BD | CD | largest error | sum of squared errors |
|---|---|---|---|---|---|---|---|---|
| subdominant $u^*$ | 6 | 3 | 5 | 6 | 6 | 5 | 4 | 18 |
| $u^* + 2$ (best $L_\infty$) | 8 | 5 | 7 | 8 | 8 | 7 | 2 | 18 |
| UPGMA | 23/3 | 3 | 11/2 | 23/3 | 23/3 | 11/2 | 7/3 | 55/6 |

The largest gap $D - u^*$ is 4, at BD, so the shift is $4/2 = 2$ and the largest error is 2, which no ultrametric beats. UPGMA has a larger maximum error but a much smaller sum of squares, so the best tree depends on the norm.

## Known algorithms

| task | method | time |
|---|---|---|
| exact tree from an ultrametric | [UPGMA](/upgma/), [WPGMA](/wpgma/), [single linkage](/single-linkage-clustering/), [complete linkage](/complete-linkage-clustering/) | $O(n^2)$ to $O(n^3)$ |
| subdominant $u^*$ | a [minimum spanning tree](/minimum-spanning-tree/) by [Prim's algorithm](/prim/), then the largest edge on each tree path | $O(n^2)$ |
| test whether $D$ is an ultrametric | compute $u^*$ and compare it with $D$ | $O(n^2)$ |
| best $L_\infty$ fit | $u^* + \varepsilon$ with $\varepsilon = \frac{1}{2}\max(D - u^*)$ (Farach, Kannan and Warnow 1995; Chepoi and Fichet 2000) | $O(n^2)$ |
| $L_2$ fit, heuristic | UPGMA, or local search over topologies with a fit for each | varies |

**Why the linkage methods are exact.** If $D$ is an ultrametric and $a, b$ is a closest pair of clusters, then every taxon outside $a \cup b$ has the same distance to all taxa of $a \cup b$, by the three-point condition. So the average, weighted average, minimum and maximum of these distances are all equal, the reduced matrix is again the ultrametric of the tree with $a \cup b$ as a leaf, and induction on $n$ finishes the proof.

**Why the test works.** $u^* \le D$ always, and $u^* = D$ when $D$ is an ultrametric because $D$ is then one of the ultrametrics below $D$ and $u^*$ is the largest. The cophenetic matrix of a spanning tree takes $O(n^2)$ time by one traversal from each vertex.

**Why the shift is optimal.** $D - u^*$ lies in $[0, 2\varepsilon]$, so $D - (u^* + \varepsilon)$ lies in $[-\varepsilon, \varepsilon]$. If an ultrametric $U$ has $|D - U| \le \delta$ in every entry, then $U - \delta$ satisfies the three-point condition and is at most $D$, so $U - \delta \le u^*$ and $D \le U + \delta \le u^* + 2\delta$, which gives $\delta \ge \varepsilon$.

## Bounds

- **Exact and $L_\infty$ versions:** $O(n^2)$ time, which is linear in the input. Recognition needs $\Omega(n^2)$ reads, because raising any single unread entry of an ultrametric above the other two distances of a triple breaks the condition.
- **$L_1$ and $L_2$ versions:** NP-hard (Křivánek and Morávek 1986; Day 1987).
- **Number of candidate topologies:** $(2n-3)!!$ rooted binary trees, for example 34,459,425 for $n = 10$.

## Reductions

- **Ultrametrics and dendrograms.** Ultrametrics on $X$ correspond one to one to [dendrograms](/dendrogram/), which are nested clusterings with merge levels (Johnson 1967). The exact problem and the [hierarchical clustering problem](/hierarchical-clustering-problem/) with ultrametric input are the same.
- **Tree metrics to ultrametrics.** For a taxon $r$ and $M = \max_x D_{rx}$, $D$ is a [tree metric](/tree-metric/) if and only if $2M - D_{rx} - D_{ry} + D_{xy}$ is an ultrametric on the other taxa (the Farris transform). So an algorithm for ultrametric trees also builds unrooted trees; the page of [additive tree reconstruction](/additive-tree-reconstruction/) has a worked example. Agarwala et al. (1999) use this reduction with the $L_\infty$ fit to get a factor 3 approximation for tree metrics.
- **Subdominant to minimum spanning trees.** $u^*$ is read off a minimum spanning tree of the complete graph weighted by $D$ (Gower and Ross 1969).

## Applications

- **Molecular clock trees.** When rates are close to constant, an ultrametric tree gives relative divergence times; calibrated with dates, it gives absolute times.
- **Hierarchical clustering.** Every agglomerative clustering produces an ultrametric, the cophenetic matrix of its dendrogram; see [agglomerative clustering](/agglomerative-clustering/).
- **Guide trees.** Multiple aligners build a quick UPGMA tree to fix the order of [progressive alignment](/progressive-alignment/).
- **Pitfall.** On data without a clock, ultrametric methods can join taxa that are not sisters; the [UPGMA ultrametric check](/ultrametric-tree-fitting-upgma-check/) shows how to detect this, and [neighbor-joining](/neighbor-joining/) does not need the clock.

## References
