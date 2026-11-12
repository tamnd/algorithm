---
tag: Z6WYX9
kind: definition
slug: splits-of-a-tree
name: Splits of a tree
aliases:
- splits
- splits-equivalence theorem
area: biology/phylogenetics
level: core
summary: Each edge of an unrooted phylogenetic tree cuts the taxa into two parts, a split. A set of splits comes from a tree exactly when its splits are pairwise compatible, and then the tree is unique.
prereqs: [phylogenetic-tree, rooted-and-unrooted-trees]
see_also: [split-system, robinson-foulds-distance, day-algorithm, quartet, rooted-triplet, character-compatibility, four-gamete-condition, consensus-tree]
sources:
  - book: isbn:9780198509424
    title: Charles Semple and Mike Steel, Phylogenetics, Oxford University Press, 2003
    locator: Section 3.1, Theorem 3.1.4 (the splits-equivalence theorem) and the definitions of X-splits and compatibility before it
  - paper: "Peter Buneman, The recovery of trees from measures of dissimilarity, in Mathematics in the Archaeological and Historical Sciences, Edinburgh University Press, 1971, pages 387 to 395"
    title: Peter Buneman, The recovery of trees from measures of dissimilarity, 1971
    locator: the theorem that pairwise compatible splits determine a unique tree
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 30, Consensus trees and distances between trees (partitions of the taxa given by the branches)
---

A split of a [phylogenetic tree](/phylogenetic-tree/) is the partition of its taxa into two parts that we get when we delete one edge. An unrooted tree on $n$ taxa has at most $2n - 3$ splits, one for each edge. The splits-equivalence theorem says that a set of splits comes from a tree exactly when each pair of splits is compatible, and that the tree is then unique. So a tree and its set of splits carry the same information, and most methods that compare or combine trees work on splits.

## Definition

Let $X$ be a set of $n \ge 2$ taxa. An *$X$-split* is a partition $A \mid B$ of $X$ into two nonempty parts. The order of the parts has no meaning: $A \mid B$ and $B \mid A$ are one split. A split is *trivial* if one part has one element, as in $\{x\} \mid X \setminus \{x\}$.

**Splits of a tree.** Let $T$ be an unrooted phylogenetic $X$-tree and $e$ an edge of $T$. Deleting $e$ leaves two subtrees. Let $A$ be the taxa at the leaves of one subtree and $B$ those of the other. Each part is nonempty, because each subtree holds a vertex of degree at most 1 in $T$, which is a leaf. The split $\sigma_e = A \mid B$ is the split of $e$, and
$$\Sigma(T) = \{\sigma_e : e \text{ an edge of } T\}$$
is the *split set* of $T$. The edge at a leaf $x$ gives the trivial split $\{x\} \mid X \setminus \{x\}$, so $\Sigma(T)$ holds all $n$ trivial splits. The splits of the inner edges are the *nontrivial* splits; many programs list only these. Distinct edges give distinct splits (this follows from the uniqueness part of the theorem below), so $|\Sigma(T)|$ is the number of edges.

Biologists also call a split a *bipartition*, and the split of an edge is the statement "the taxa in $A$ form a group, if the root is in $B$".

**Compatibility.** Two $X$-splits $A \mid B$ and $C \mid D$ are *compatible* if at least one of the four sets
$$A \cap C, \quad A \cap D, \quad B \cap C, \quad B \cap D$$
is empty. Otherwise they are *incompatible*. A set of splits is compatible if each pair in it is compatible. Each trivial split is compatible with every split, and a split is compatible with itself.

**Clusters.** For a [rooted tree](/rooted-and-unrooted-trees/), the analog of a split is a *cluster*, the set of taxa below a vertex. Fix a taxon $r$ and, for each split, take the part that does not hold $r$. The next lemma says that compatibility then becomes a simple condition on sets.

**Lemma.** Let $A \mid B$ and $C \mid D$ be $X$-splits with $r \in B$ and $r \in D$. They are compatible if and only if $A$ and $C$ are disjoint or one of them contains the other.

*Proof.* $B \cap D$ holds $r$, so it is not empty. So the splits are compatible if and only if $A \cap C = \emptyset$, or $A \cap D = \emptyset$, or $B \cap C = \emptyset$. The first says that $A$ and $C$ are disjoint. The second says $A \subseteq X \setminus D = C$. The third says $C \subseteq A$. $\square$

A family of sets in which any two are disjoint or nested is a *hierarchy*, and a hierarchy on $X$ is the same thing as a rooted tree. This is the idea of the proof below.

### The splits-equivalence theorem

**Theorem** (Buneman 1971; Semple and Steel, Theorem 3.1.4). Let $\Sigma$ be a set of $X$-splits that holds all $n$ trivial splits. There is an unrooted phylogenetic $X$-tree $T$ with $\Sigma(T) = \Sigma$ if and only if $\Sigma$ is compatible. If $T$ exists, it is unique up to isomorphism.

*Proof that the splits of a tree are compatible.* Let $e \ne f$ be edges of $T$. The edge $f$ lies in one of the two subtrees of $T - e$. Let $A$ be the taxa of the other subtree, so $\sigma_e = A \mid B$. In the same way, let $D$ be the taxa of the subtree of $T - f$ that does not hold $e$, so $\sigma_f = C \mid D$. The subtree of $T - e$ with the taxa $A$ does not hold $f$, so it is connected in $T - f$, and it is joined through $e$ to the side of $f$ that holds $e$. So $A \subseteq C$, and $A \cap D = \emptyset$.

*Proof that a compatible set comes from a tree.* Fix a taxon $r$. For each split in $\Sigma$, let its *cluster* be its part that does not hold $r$, and let $\mathcal{H}$ be the set of these clusters. By the lemma, any two members of $\mathcal{H}$ are disjoint or nested. $\mathcal{H}$ holds $\{x\}$ for each $x \ne r$ and $X \setminus \{r\}$ (from the trivial splits), and every member is a subset of $X \setminus \{r\}$.

For $C \in \mathcal{H}$ other than $X \setminus \{r\}$, let the *parent* of $C$ be the smallest member of $\mathcal{H}$ that strictly contains $C$. It is well defined: the members that strictly contain $C$ all meet $C$, so any two of them meet and are nested, so they form a chain, and the chain holds $X \setminus \{r\}$. Build the graph $T$ with one vertex for each member of $\mathcal{H}$, an edge from each $C$ to its parent, and one more vertex $r$ with an edge to $X \setminus \{r\}$. Each vertex other than $r$ and $X \setminus \{r\}$ has one parent, and parents are strictly larger, so $T$ is a tree.

The *children* of $C$ are the members whose parent is $C$. They are pairwise disjoint, since two nested children would contradict the choice of the smallest parent. They cover $C$: for $x \in C$, the members that hold $x$ form a chain from $\{x\}$ up to $X \setminus \{r\}$, and the member just below $C$ in this chain is a child of $C$ that holds $x$. If $|C| \ge 2$, the children are proper subsets of $C$ that cover it, so there are at least two, and with the edge to the parent (or to $r$) the vertex $C$ has degree at least 3. If $|C| = 1$, $C$ has no children, since a split has no empty part. So the leaves of $T$ are the vertices $\{x\}$ for $x \ne r$ and the vertex $r$, and labeling them by $x$ and $r$ makes $T$ an unrooted phylogenetic $X$-tree.

Since the children of each $C$ partition $C$, induction from the leaves up shows that the leaves below $C$ are exactly the taxa in $C$. So deleting the edge from $C$ to its parent gives the split $C \mid X \setminus C$, and deleting the edge at $r$ gives $\{r\} \mid X \setminus \{r\}$. These are the splits of $\Sigma$, one per edge, so $\Sigma(T) = \Sigma$.

*Proof of uniqueness.* Let $T'$ be any phylogenetic $X$-tree with $\Sigma(T') = \Sigma$. Direct each edge of $T'$ away from the leaf $r$. For a vertex $v \ne r$, the edge into $v$ gives a split whose part without $r$ is the set $c(v)$ of taxa below $v$, so $c(v) \in \mathcal{H}$. The map $v \mapsto c(v)$ is one to one: if neither of $v, w$ is below the other, their clusters are disjoint, and if $w$ is below $v$, then $v$ has a second child, because it has degree at least 3, and that child has taxa outside $c(w)$. It is onto $\mathcal{H}$, since each split of $\Sigma$ is the split of an edge of $T'$. A vertex $w$ is a child of $v$ in $T'$ exactly when $c(v)$ is the smallest cluster that strictly contains $c(w)$, because the clusters that contain $c(w)$ are those of the vertices on the path from $w$ to $r$. So the map is an isomorphism from $T'$ to $T$ that keeps the labels. $\square$

The proof is also an algorithm: with each cluster stored as a bit mask, sorting the clusters by size and finding each parent builds $T$ in $O(n \cdot |\Sigma|)$ time. The page [split system](/split-system/) gives this procedure and its implementation.

### Consequences

- **Size.** An unrooted phylogenetic tree on $n \ge 3$ taxa has at most $2n - 3$ splits, of which at most $n - 3$ are nontrivial, with equality if and only if the tree is binary. The tree has $n$ leaves, $i$ inner vertices and $n + i - 1$ edges, and the degrees sum to $2(n + i - 1) \ge n + 3i$, so $i \le n - 2$, with equality exactly when each inner vertex has degree 3.
- **Maximal sets.** By the theorem, every compatible set of $X$-splits has at most $2n - 3$ members, so the split set of a binary tree is a maximal compatible set: no split outside it is compatible with all of its splits.
- **Refinement.** For trees $T$ and $T'$ on $X$, $\Sigma(T') \subseteq \Sigma(T)$ if and only if $T'$ is obtained from $T$ by contracting edges. Then $T$ *refines* $T'$. A polytomy is a vertex at which some splits are missing.
- **Comparison.** Two trees are equal if and only if their split sets are equal, and the [Robinson-Foulds distance](/robinson-foulds-distance/) counts the splits in which they differ.

## Examples and non-examples

**Six taxa.** Read `(((A,B),C),(D,(E,F)));` as an unrooted binary tree. It has the 6 trivial splits and the 3 nontrivial splits
$$AB \mid CDEF, \qquad ABC \mid DEF, \qquad ABCD \mid EF,$$
so $|\Sigma(T)| = 9 = 2 \cdot 6 - 3$. The three nontrivial splits are pairwise compatible; for example $AB \cap EF = \emptyset$ for the first and third. With $r = A$, the clusters are the singletons $B, \ldots, F$, the top cluster $BCDEF$, and $CDEF$, $DEF$ and $EF$. The parents are: $B$ and $CDEF$ below $BCDEF$, $C$ and $DEF$ below $CDEF$, $D$ and $EF$ below $DEF$, and $E$ and $F$ below $EF$. With $A$ joined to $BCDEF$, this is the tree we started from.

**Non-example: an incompatible pair.** On $\{a, b, c, d\}$, the splits $ab \mid cd$ and $ac \mid bd$ have $ab \cap ac = \{a\}$, $ab \cap bd = \{b\}$, $cd \cap ac = \{c\}$ and $cd \cap bd = \{d\}$. All four are nonempty, so no tree has both splits. On four taxa, the three nontrivial splits $ab \mid cd$, $ac \mid bd$ and $ad \mid bc$ are pairwise incompatible, which is why a tree on four taxa has at most one inner edge.

**A star.** The tree with one inner vertex joined to all $n$ leaves has only the $n$ trivial splits. It is refined by every tree on $X$.

**A split that is not a cluster.** On the rooted tree $((a,b),(c,d))$, both $\{a, b\}$ and $\{c, d\}$ are clusters, but after unrooting they give the one split $ab \mid cd$. The two clusters of the root's children merge into one split, because unrooting suppresses the root and joins its two edges into one. In the other direction, the split $ab \mid cd$ gives the cluster $\{a, b\}$ only if the root is on the side of $c$ and $d$.

## Related definitions

- A [split system](/split-system/) is any set of splits, compatible or not. Weakly compatible and circular split systems, which are drawn as [split networks](/split-network-construction/), come from [split decomposition](/split-decomposition/) and [NeighborNet](/neighbor-net/).
- A binary character, such as the presence or absence of a gene, is a split of the taxa that have it. The [four-gamete condition](/four-gamete-condition/) is the compatibility test for two such characters, and [character compatibility](/character-compatibility/) and [perfect phylogeny](/perfect-phylogeny/) rest on the splits-equivalence theorem.
- A [quartet](/quartet/) $ab \mid cd$ is the restriction of a split to four taxa, and a [rooted triplet](/rooted-triplet/) is the analog for clusters of a rooted tree.
- The [Robinson-Foulds distance](/robinson-foulds-distance/) and [Day's algorithm](/day-algorithm/) compare split sets, and a [consensus tree](/consensus-tree/) keeps the splits that most input trees share.
- When the edges carry lengths, the tree metric is $d_T = \sum_{e} \ell(e)\, \delta_{\sigma_e}$, where $\delta_{A \mid B}(x, y) = 1$ if $x$ and $y$ are on different sides and 0 otherwise; see [tree metric](/tree-metric/).

## References
