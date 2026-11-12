---
tag: CA9Q6A
kind: definition
slug: phylogenetic-tree
name: Phylogenetic tree
aliases:
- phylogeny
- evolutionary tree
- phylogenetic X-tree
area: biology/phylogenetics
level: intro
summary: A tree whose leaves are labeled one to one by a set of taxa and whose inner vertices, all of degree 3 or more, stand for common ancestors. It may be rooted and may carry branch lengths.
prereqs: [tree, rooted-tree]
see_also: [rooted-and-unrooted-trees, newick-format, splits-of-a-tree, quartet, rooted-triplet, tree-metric, ultrametric, phylogenetic-network]
sources:
  - book: isbn:9780198509424
    title: Charles Semple and Mike Steel, Phylogenetics, Oxford University Press, 2003
    locator: Chapter 2 (X-trees, phylogenetic X-trees, rooted phylogenetic trees and their isomorphism)
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 3, How many trees are there? (rooted and unrooted bifurcating and multifurcating trees)
  - book: isbn:9781107184718
    title: Tandy Warnow, Computational Phylogenetics, An Introduction to Designing Methods for Phylogeny Estimation, Cambridge University Press, 2017
    locator: Chapter 2, Trees
  - url: https://phylipweb.github.io/phylip/newicktree.html
    title: Joseph Felsenstein, The Newick tree format, PHYLIP documentation
    locator: the example trees, including (B:6.0,(A:5.0,C:3.0,E:4.0):5.0,D:11.0);
---

A phylogenetic tree on a set $X$ of taxa is a [tree](/tree/) whose leaves are labeled one to one by $X$ and whose other vertices have degree at least 3. The leaves stand for species, genes or sequences that we observe, and the inner vertices stand for ancestors that we infer. The tree can be [rooted or unrooted](/rooted-and-unrooted-trees/), and its edges can carry lengths, so that the path length between two leaves models their evolutionary distance. It is the object that every method of [phylogenetic tree reconstruction](/phylogenetic-tree-reconstruction/) outputs and that every method of [tree comparison](/tree-comparison/) takes as input.

## Definition

Let $X$ be a finite set with $n = |X| \ge 2$ elements, the *taxa*.

**Unrooted.** An *unrooted phylogenetic $X$-tree* is a pair $(T, \varphi)$, where $T = (V, E)$ is a tree and $\varphi : X \to V$ is a bijection from $X$ onto the set of leaves (vertices of degree 1) of $T$, and each vertex that is not a leaf has degree at least 3.

**Rooted.** A *rooted phylogenetic $X$-tree* is a tree $T$ with a distinguished vertex $\rho$, the *root*, and a bijection $\varphi$ from $X$ onto the vertices other than $\rho$ that have degree 1. The root has degree at least 2, and each other vertex that is not a leaf has degree at least 3. Each edge is directed away from $\rho$, so each non-root vertex has one parent, and an inner vertex has at least two children. The *cluster* of a vertex $v$ is the set of taxa at the leaves below $v$, as in a [rooted tree](/rooted-tree/).

**Binary.** A phylogenetic tree is *binary* (or fully resolved, or bifurcating) if each inner vertex has degree exactly 3, with the root, if any, of degree exactly 2. A vertex of higher degree is a *polytomy*. A polytomy can be *hard* (one ancestor split into three or more lines) or *soft* (the data cannot resolve the order of the splits).

**Equality.** Two phylogenetic $X$-trees $(T, \varphi)$ and $(T', \varphi')$ are the same tree if there is a graph isomorphism $\psi : T \to T'$ with $\psi \circ \varphi = \varphi'$, and $\psi(\rho) = \rho'$ in the rooted case. So the order of the children of a vertex has no meaning: $(A,(B,C))$ and $((C,B),A)$ in [Newick format](/newick-format/) are one tree.

**Branch lengths.** A *weighted* phylogenetic tree also has a map $\ell : E \to \mathbb{R}_{\ge 0}$. The *path length* between taxa $x$ and $y$ is
$$d_T(x, y) = \sum_{e \text{ on the path from } \varphi(x) \text{ to } \varphi(y)} \ell(e).$$
In a molecular tree $\ell(e)$ is usually the expected number of substitutions per site along the edge; in a dated tree it is time. The map $d_T$ is a [tree metric](/tree-metric/) when all lengths are positive. A rooted weighted tree is *ultrametric* (or clock-like) if all leaves are at the same path length from the root. Then $d_T$ is an [ultrametric](/ultrametric/).

The degree conditions make the tree a minimal picture of its branching pattern. A vertex of degree 2 that is not the root carries no information about branching: suppress it, and join its two edges into one edge whose length is the sum.

## Examples and non-examples

**A binary unrooted tree.** The Newick string `(((A,B),C),(D,(E,F)));` read as an unrooted tree has $n = 6$ leaves, $n - 2 = 4$ inner vertices, each of degree 3, and $2n - 3 = 9$ edges. Removing an inner edge separates the leaves into $\{A, B\} \mid \{C, D, E, F\}$, $\{A, B, C\} \mid \{D, E, F\}$ or $\{A, B, C, D\} \mid \{E, F\}$. These [splits](/splits-of-a-tree/) determine the tree.

**A tree with a polytomy and branch lengths.** Felsenstein's example `(B:6.0,(A:5.0,C:3.0,E:4.0):5.0,D:11.0);` has an inner vertex $u$ of degree 4, with $A$, $C$, $E$ and one more edge of length 5 to the vertex $w$ that holds $B$ and $D$. So it is not binary. The path lengths follow by addition: $d_T(A, B) = 5 + 5 + 6 = 16$, $d_T(A, C) = 5 + 3 = 8$ and $d_T(B, D) = 6 + 11 = 17$.

**A rooted ultrametric tree.** In `((A:2,B:2):1,(C:1,D:1):2);` the root has two children, and each leaf is at path length 3 from the root ($2 + 1$ and $1 + 2$). So the tree is ultrametric, and $d_T(x, y) = 2h$, where $h$ is the height of the [lowest common ancestor](/lowest-common-ancestor/) of $x$ and $y$ above the leaves: $d_T(A, B) = 4$ and $d_T(A, C) = 6$.

**Non-example: a vertex of degree 2.** Take the tree with the edges $A - u$, $u - v$, $v - B$ and $v - C$. The vertex $u$ has degree 2 and is not a root, so this is not a phylogenetic tree. Suppress $u$: the edges $A - v$, $v - B$ and $v - C$ give the only unrooted phylogenetic tree on three taxa, the star.

**Non-example: a repeated label.** A gene tree in which two leaves carry the name of one species (two copies of a gene) is not a phylogenetic tree on the species, because $\varphi$ is not one to one. It is a phylogenetic tree on the set of gene copies, and [tree reconciliation](/tree-reconciliation/) relates it to the species tree.

**Non-example: a cycle.** A graph with a cycle that models hybridization or [horizontal gene transfer](/horizontal-gene-transfer/) is a [phylogenetic network](/phylogenetic-network/), not a tree.

**Non-example: labels on inner vertices.** Semple and Steel's more general *$X$-trees* allow a taxon to label an inner vertex (a sampled ancestor) or several taxa to share a vertex. A phylogenetic tree allows neither.

## Related definitions

- [Rooted and unrooted trees](/rooted-and-unrooted-trees/) compares the two kinds, gives the counts $(2n-3)!!$ and $(2n-5)!!$ of binary trees, and shows how to root and unroot.
- [Newick format](/newick-format/) is the usual text form of a phylogenetic tree.
- [Splits of a tree](/splits-of-a-tree/), [quartets](/quartet/) and [rooted triplets](/rooted-triplet/) are three ways to break a tree into small parts that, taken together, determine it.
- [Tree metric](/tree-metric/) and [ultrametric](/ultrametric/) describe the distances $d_T$ of weighted trees, and the [four-point condition](/four-point-condition/) characterizes them.
- A [phylogenetic network](/phylogenetic-network/) allows reticulate events; a [consensus tree](/consensus-tree/) and a [supertree](/supertree/) combine many trees into one.
- In [graph theory](/tree/), a tree has no labels and no degree condition. A phylogenetic tree is a leaf-labeled tree with a degree condition, and its inner vertices are not named, so two phylogenetic trees are equal by a label-preserving [isomorphism](/tree-isomorphism/).

## References
