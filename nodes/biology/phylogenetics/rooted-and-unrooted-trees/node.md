---
tag: 4P5GAR
kind: definition
slug: rooted-and-unrooted-trees
name: Rooted and unrooted trees
aliases:
- rooted phylogenetic tree
- unrooted phylogenetic tree
area: biology/phylogenetics
level: intro
summary: A rooted phylogenetic tree has a root that fixes the direction of time; an unrooted one records only adjacency. There are (2n-3)!! rooted and (2n-5)!! unrooted binary trees on n taxa.
prereqs: [phylogenetic-tree]
see_also: [tree-rooting, midpoint-rooting, splits-of-a-tree, rooted-triplet, quartet, newick-format, stepwise-addition, rooted-tree]
sources:
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 3, How many trees are there? (sections Rooted bifurcating trees and Unrooted bifurcating trees)
  - paper: doi:10.2307/2412810
    title: Joseph Felsenstein, The number of evolutionary trees, Systematic Zoology 27(1), 1978, 27-33
    locator: the counts of rooted and unrooted bifurcating trees with labeled tips
  - book: isbn:9780198509424
    title: Charles Semple and Mike Steel, Phylogenetics, Oxford University Press, 2003
    locator: Chapter 2 (rooted and unrooted phylogenetic trees and the number of binary phylogenetic trees)
---

A [phylogenetic tree](/phylogenetic-tree/) is *rooted* when one vertex, the root, is marked as the common ancestor of all taxa, so that each edge points forward in time. It is *unrooted* when no such vertex is marked: the tree then says which taxa are close to which, but not which split came first. On $n$ taxa there are $(2n-3)!!$ rooted binary trees and $(2n-5)!!$ unrooted ones. Most tree reconstruction methods return an unrooted tree, and a separate step of [tree rooting](/tree-rooting/) places the root.

## Definition

Let $X$ be a set of $n$ taxa. A *rooted phylogenetic $X$-tree* has a root $\rho$ of degree at least 2, and each other inner vertex has degree at least 3. An *unrooted phylogenetic $X$-tree* has no root, and each inner vertex has degree at least 3. In both kinds the leaves are labeled one to one by $X$ (see [phylogenetic tree](/phylogenetic-tree/) for the full definition). The two kinds are linked by two operations.

**Unrooting.** Delete the mark on $\rho$. If $\rho$ has degree 2, suppress it: replace its two edges $\rho - a$ and $\rho - b$ by one edge $a - b$ whose length is the sum of the two lengths. The result is an unrooted phylogenetic $X$-tree.

**Rooting on an edge.** For an edge $e = \{u, v\}$ of an unrooted tree, subdivide $e$ by a new vertex $\rho$, mark $\rho$ as the root and direct each edge away from $\rho$. If $e$ has length $\ell$, the two new edges get lengths $t$ and $\ell - t$ for some $0 < t < \ell$; the choice of $t$ changes the branch lengths but not the topology. Rooting at an inner vertex $v$ is also possible; it gives a root of degree at least 3.

A rooted tree is described by its *clusters*, the leaf sets below its vertices, and an unrooted tree by its [splits](/splits-of-a-tree/), the bipartitions given by its edges. A rooted tree says which taxa share a more recent common ancestor ([rooted triplets](/rooted-triplet/)); an unrooted tree only says which pairs of taxa are separated from which ([quartets](/quartet/)).

### Counts of binary trees

For an odd integer $k \ge -1$ write $k!! = k (k-2) (k-4) \cdots 1$, with $(-1)!! = 1!! = 1$. Let $U(n)$ and $R(n)$ be the numbers of unrooted and rooted binary phylogenetic trees on a fixed set of $n$ taxa.

**Proposition.**
1. An unrooted binary tree with $n \ge 3$ leaves has $n - 2$ inner vertices and $2n - 3$ edges. A rooted binary tree with $n \ge 2$ leaves has $n - 1$ inner vertices, the root included, and $2n - 2$ edges.
2. $U(n) = (2n-5)!!$ for $n \ge 3$, and $R(n) = (2n-3)!!$ for $n \ge 2$.
3. $R(n) = (2n - 3)\, U(n)$ for $n \ge 3$: rooting an unrooted binary tree on each of its $2n - 3$ edges gives $2n - 3$ different rooted trees, and each rooted binary tree arises in this way from exactly one pair (unrooted tree, edge).

*Proof.* (1) Let $i$ be the number of inner vertices and $m$ the number of edges. A tree has $m = n + i - 1$. In the unrooted case the degrees sum to $n + 3i = 2m = 2n + 2i - 2$, so $i = n - 2$ and $m = 2n - 3$. In the rooted case the root has degree 2, so $n + 3(i - 1) + 2 = 2(n + i - 1)$, which gives $i = n - 1$ and $m = 2n - 2$.

(2) Fix a taxon $x$ and let $n \ge 4$. From an unrooted binary tree $T$ on $X$, delete the leaf $x$. Its neighbour now has degree 2; suppress it, which creates one edge $e$. The result is a binary tree $T'$ on $X \setminus \{x\}$ with a marked edge $e$. Conversely, from $T'$ and any edge $e$ of $T'$, subdivide $e$ by a new vertex and hang $x$ from it. The two maps are inverse to each other, so the trees on $X$ are in bijection with the pairs $(T', e)$. By (1), $T'$ has $2(n-1) - 3 = 2n - 5$ edges, so $U(n) = (2n - 5)\, U(n - 1)$. With $U(3) = 1$ (the star), $U(n) = 3 \cdot 5 \cdots (2n-5) = (2n-5)!!$. For the rooted count, add a new taxon $\rho'$ joined to the root. This maps rooted binary trees on $X$ one to one onto unrooted binary trees on $X \cup \{\rho'\}$; the inverse deletes $\rho'$ and marks its neighbour as the root, which then has degree 2. So $R(n) = U(n + 1) = (2n-3)!!$ for $n \ge 2$.

(3) Rooting $T$ on the edge $e$ and then unrooting gives back $T$, and the root of degree 2 sits on $e$. So the map from pairs $(T, e)$ to rooted trees is one to one. It is onto, because unrooting a rooted binary tree suppresses its root of degree 2 and so creates an edge on which rooting gives the tree back. Hence $R(n) = (2n-3)\, U(n)$, which agrees with (2). $\square$

The closed form $(2n-5)!! = \dfrac{(2n-4)!}{(n-2)!\, 2^{n-2}}$ follows by writing $(2n-4)! = (2n-5)!! \cdot (2n-4)(2n-6) \cdots 2$ and $(2n-4)(2n-6)\cdots 2 = 2^{n-2} (n-2)!$. With $m = n - 2$ and Stirling's formula for $(2m)!$ and $m!$, this gives $U(n) \sim \sqrt{2}\,(2m/e)^{m}$, so $U(n)$ grows faster than any exponential function of $n$.

## Examples and non-examples

**Four taxa.** On $\{a, b, c, d\}$ there are $U(4) = 3$ unrooted binary trees, one for each way to pair the taxa: $ab \mid cd$, $ac \mid bd$ and $ad \mid bc$. Each has 5 edges. Rooting $ab \mid cd$ on its inner edge gives the balanced tree $((a,b),(c,d))$; rooting it on the edge of $a$ gives the caterpillar $(a,(b,(c,d)))$, and the other three leaf edges give three more caterpillars. So the three unrooted trees give $3 \times 5 = 15 = R(4)$ rooted trees: 3 balanced ones and 12 caterpillars.

**Growth.** The table gives $U(n)$ and $R(n)$.

| $n$ | $U(n) = (2n-5)!!$ | $R(n) = (2n-3)!!$ |
|---|---|---|
| 3 | 1 | 3 |
| 4 | 3 | 15 |
| 5 | 15 | 105 |
| 6 | 105 | 945 |
| 7 | 945 | 10395 |
| 8 | 10395 | 135135 |
| 9 | 135135 | 2027025 |
| 10 | 2027025 | 34459425 |
| 20 | about $2.216 \times 10^{20}$ | about $8.201 \times 10^{21}$ |
| 50 | about $2.838 \times 10^{74}$ | about $2.753 \times 10^{76}$ |

So exhaustive search over all trees stops being possible at about a dozen taxa, and methods such as [maximum parsimony](/maximum-parsimony/) and [maximum likelihood](/maximum-likelihood-phylogeny/) search the tree space with heuristics such as [stepwise addition](/stepwise-addition/) and [nearest neighbor interchange](/nearest-neighbor-interchange/).

**The same Newick string, two readings.** By a common convention, `(A,B,(C,D));` with three children at the outer level is an unrooted tree, and `((A,B),(C,D));` with two is rooted. But many programs read both as unrooted, and then the two strings are the same tree $AB \mid CD$. A file does not always say which reading is meant.

**Non-example: a root of degree 1.** Some programs write a stem edge above the root, as in `((A,B),C):0.5;`. A rooted phylogenetic tree has no such edge: the root has degree at least 2. The length 0.5 belongs to no edge of the tree.

**Non-example: an unrooted tree read as rooted.** Drawing an unrooted tree from a chosen vertex makes it look rooted, but the drawing adds no information. Reading $ab \mid cd$ as "$a$ and $b$ are sister taxa" is wrong unless the root is known to lie outside the pair $\{a, b\}$. For four taxa, the rooting on the edge of $a$ makes $b$, $c$ and $d$ a clade, and $a$ and $b$ are not sisters.

## Related definitions

- [Tree rooting](/tree-rooting/) is the problem of placing the root on an unrooted tree, and [midpoint rooting](/midpoint-rooting/) is one method for it.
- [Splits](/splits-of-a-tree/) describe unrooted trees and clusters describe rooted ones. Rooting at a leaf $r$ turns the splits into clusters: the side of each split that does not hold $r$.
- [Quartets](/quartet/) are the four-taxon pieces of unrooted trees, and [rooted triplets](/rooted-triplet/) the three-taxon pieces of rooted trees.
- In graph theory a [rooted tree](/rooted-tree/) is any tree with a chosen vertex, and a free tree is a tree with none ([free tree properties](/free-tree-properties/)). The phylogenetic versions add the leaf labels and the degree conditions, which is why the counts above differ from [Cayley's formula](/cayley-formula/) for labeled trees, where all vertices carry labels.

## References
