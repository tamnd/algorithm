---
tag: JK11E7
kind: concept
slug: ultrametric-tree-fitting-upgma-check
name: UPGMA ultrametric check
area: biology/phylogenetics
level: intro
summary: Test whether a distance matrix is ultrametric, the condition under which UPGMA returns the exact tree, by comparing the matrix with the distances of the UPGMA tree.
prereqs: [upgma, ultrametric]
see_also: [ultrametric-tree-reconstruction, wpgma, neighbor-joining, molecular-clock, single-linkage-clustering, minimum-spanning-tree, dendrogram, tree-metric]
sources:
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, 2004
    locator: Chapter 11, Distance matrix methods, UPGMA, the molecular clock and the failure of UPGMA without a clock
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, 1997
    locator: Chapter 17, ultrametric trees and the test of a matrix for the ultrametric property
  - paper: "Robert R. Sokal and F. James Rohlf, The comparison of dendrograms by objective methods, Taxon 11(2), 1962, pages 33 to 40"
    title: Sokal and Rohlf 1962
    locator: the cophenetic correlation between a matrix and the distances of its dendrogram
  - paper: "J. C. Gower and G. J. S. Ross, Minimum spanning trees and single linkage cluster analysis, Journal of the Royal Statistical Society, Series C (Applied Statistics) 18(1), 1969, pages 54 to 64"
    title: Gower and Ross 1969
    locator: single linkage from a minimum spanning tree, the basis of the O(n^2) test
---

The UPGMA ultrametric check is the test of whether a distance matrix is an [ultrametric](/ultrametric/), done by comparing the matrix with the leaf-to-leaf distances of the tree that [UPGMA](/upgma/) builds from it. The two agree in every entry if and only if the matrix is an ultrametric, which is exactly the case in which UPGMA returns the true tree. When they do not agree, the size of the difference shows how far the data are from a [molecular clock](/molecular-clock/).

## In plain words

UPGMA always gives an answer, even when its answer is wrong. It is only safe when the data come from a tree in which all species changed at the same rate. To check this, take the tree UPGMA built and read off from it the distance between each pair of species. If every one of these is the same as the input distance, the data fit a same-rate tree and the result is correct. If some are different, the data do not fit, and the larger the differences, the less you should trust the tree. A method that does not need equal rates, such as neighbor-joining, is then a better choice.

## The idea

**The cophenetic matrix.** UPGMA returns a rooted tree with a height $h(v)$ at each internal vertex. Its cophenetic matrix is
$$C(x, y) = 2\, h(\operatorname{lca}(x, y)),$$
the path length between the leaves $x$ and $y$ in the tree.

**The check.** Compute $C$ and compare it with $D$ entry by entry. Then $C = D$ if and only if $D$ is an ultrametric.

- If $D$ is an ultrametric, UPGMA is exact on it (see [ultrametric tree reconstruction](/ultrametric-tree-reconstruction/)), so $C = D$.
- Conversely, UPGMA heights never decrease from one merge to the next: when clusters $a$ and $b$ merge at the smallest entry $d_{ab}$, each new entry is a weighted average of entries $d_{ak}$ and $d_{bk}$, which are at least $d_{ab}$. So $h$ grows from the leaves to the root, and $C$ satisfies the three-point condition $C(x, z) \le \max(C(x, y), C(y, z))$, because two of the three lowest common ancestors of $x, y, z$ are the same vertex and the third is at or below it. If $C = D$, then $D$ is an ultrametric.

**Cost.** UPGMA takes $O(n^3)$ time in its simple form and the comparison takes $O(n^2)$. The direct test of the three-point condition on all triples takes $O(n^3)$. The fastest test is $O(n^2)$: build a [minimum spanning tree](/minimum-spanning-tree/) with [Prim's algorithm](/prim/), compute the largest edge on each tree path, which is the cophenetic matrix of [single linkage](/single-linkage-clustering/), and compare it with $D$. On an ultrametric all linkage methods give the same tree, so the single-linkage form decides the same question.

**Measures of the difference.** When $C \ne D$, the usual measures are
- the largest error $\max_{x<y} |D(x, y) - C(x, y)|$,
- the sum of squared errors $\sum_{x<y} (D(x, y) - C(x, y))^2$,
- the cophenetic correlation, the Pearson correlation between the entries of $D$ and of $C$ (Sokal and Rohlf 1962), which is 1 for a perfect fit.

These measure fit, not correctness of the topology: a matrix with a small error can still give a wrong tree when two merge distances are close.

**Exact arithmetic.** With measured data, equality almost never holds, so the check is used with a tolerance or as a measure. For a test of the exact property, use integer or rational entries, as UPGMA averages produce fractions.

## Examples

**A pass.** The matrix on A to E with $D_{AB} = 2$, $D_{DE} = 4$, $D_{CD} = D_{CE} = 6$ and distance 10 between $\{A, B\}$ and $\{C, D, E\}$ gives the UPGMA merges AB at height 1, DE at height 2, C with DE at height 3 and the two parts at height 5. The cophenetic matrix is $2 \times$ these heights: $C_{AB} = 2$, $C_{DE} = 4$, $C_{CD} = C_{CE} = 6$ and 10 across. It equals $D$ in all ten entries, so $D$ is an ultrametric and the tree `((A:1,B:1):4,(C:3,(D:2,E:2):1):2);` is exact.

**A fail.** For the matrix with $D_{AB} = 6$, $D_{AC} = 3$, $D_{AD} = 6$, $D_{BC} = 7$, $D_{BD} = 10$, $D_{CD} = 5$, UPGMA merges A and C at height $3/2$, then D at height $11/4$, then B at height $23/6$.

| pair | AB | AC | AD | BC | BD | CD |
|---|---|---|---|---|---|---|
| $D$ | 6 | 3 | 6 | 7 | 10 | 5 |
| $C$ | 23/3 | 3 | 11/2 | 23/3 | 23/3 | 11/2 |
| $D - C$ | $-5/3$ | 0 | $1/2$ | $-2/3$ | $7/3$ | $-1/2$ |

The largest error is $7/3$, the sum of squared errors is $55/6$, and the cophenetic correlation is $\sqrt{106/161} \approx 0.811$. All four triples fail the three-point condition, which agrees with the check.

**A tree metric without a clock.** The matrix of `((A:2,B:7):1,E:5,(C:3,D:6):2);` is a [tree metric](/tree-metric/) but not an ultrametric: 9 of its 10 triples fail the three-point condition. UPGMA merges A and C first at distance 8 (tied with A and E), then E, then D, then B. A's sister in the true tree is B, so the UPGMA tree is wrong. The check shows it: $C_{AB} = 51/4$ against $D_{AB} = 9$, a largest error of $15/4$, a sum of squared errors of $139/4$ and a cophenetic correlation of $\sqrt{117/256} \approx 0.676$. [Neighbor-joining](/neighbor-joining/) returns the true tree from the same matrix.

## Where it is used

- **Before trusting UPGMA.** The check tells whether the clock assumption behind [UPGMA](/upgma/) and [WPGMA](/wpgma/) holds for the data.
- **Testing a clock.** A large error suggests rates differ between lineages; the formal tests of the clock compare likelihoods of trees with and without the clock, see [molecular clock](/molecular-clock/).
- **Clustering.** In [hierarchical clustering](/hierarchical-clustering-problem/), the cophenetic correlation measures how well a [dendrogram](/dendrogram/) represents the input dissimilarities.
- **Choosing a method.** When the check fails, use a method for unrooted trees such as [neighbor-joining](/neighbor-joining/) and root the result afterwards, for example by [midpoint rooting](/midpoint-rooting/).

## References
