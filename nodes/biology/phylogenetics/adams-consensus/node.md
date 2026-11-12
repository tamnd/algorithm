---
tag: V4J1S8
kind: algorithm
slug: adams-consensus
name: Adams consensus
aliases:
- Adams consensus tree
area: biology/phylogenetics
level: research
summary: Consensus of rooted trees that splits each block by the common refinement of the trees' partitions at its lowest common ancestor. Keeps every common nesting.
solves: [consensus-tree]
model: word-ram
complexity:
  vars: {k: the number of input trees, n: the number of taxa}
  time: {worst: "O(k n^2)"}
  space: {extra: "O(k n)"}
properties: {deterministic: true, exact: true, online: false, recursive: true}
history:
  year: 1972
  people: [Edward N. Adams III]
  note: Adams introduced the method in 1972 as the first consensus tree technique. Jansson, Li and Sung (2015) reduced the time to O(kn log n).
prereqs: [consensus-tree, lowest-common-ancestor, rooted-triplet]
see_also: [strict-consensus, majority-rule-consensus, supertree, maximum-agreement-subtree, tree-comparison, phylogenetic-tree, rooted-and-unrooted-trees]
sources:
  - paper: doi:10.2307/2412432
    title: Edward N. Adams III, Consensus techniques and the comparison of taxonomic trees, Systematic Zoology 21(4), 1972, pages 390 to 397
    locator: the consensus construction by the common refinement of the partitions at the root, applied again to each block
  - paper: "Edward N. Adams III, N-trees as nestings: complexity, similarity, and consensus, Journal of Classification 3, 1986, pages 299 to 317"
    title: Edward N. Adams III, N-trees as nestings, complexity, similarity, and consensus
    locator: the description of trees by nestings and the nesting property of the Adams tree
  - paper: "Jesper Jansson, Zhaoxian Li and Wing-Kin Sung, On finding the Adams consensus tree, STACS 2015, LIPIcs 30, 2015"
    title: Jesper Jansson, Zhaoxian Li and Wing-Kin Sung, On finding the Adams consensus tree
    locator: an O(kn log n) time algorithm, against O(kn^2) for the direct method
  - paper: "David Bryant, A classification of consensus methods for phylogenetics, in Bioconsensus, DIMACS Series in Discrete Mathematics and Theoretical Computer Science 61, 2003, pages 163 to 184"
    title: David Bryant, A classification of consensus methods for phylogenetics
    locator: the definition of the Adams consensus by partitions at the lowest common ancestor, and its nesting property
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, 2004
    locator: Chapter 30, Consensus trees and distances between trees
  - book: isbn:9781107184718
    title: Tandy Warnow, Computational Phylogenetics, 2017
    locator: Chapter 6, Consensus and agreement trees
---

The Adams consensus is a [consensus tree](/consensus-tree/) method for rooted [phylogenetic trees](/phylogenetic-tree/) on the same taxa. It does not count groups. It works from the top down: each tree splits the current set of taxa at the [lowest common ancestor](/lowest-common-ancestor/) of that set, and the Adams tree takes the common refinement of these splits. The result keeps every *nesting* that all input trees share, for example every [rooted triplet](/rooted-triplet/) that they all show. It can show a group that no input tree has. Adams (1972) introduced it as the first consensus tree method.

## In plain words

Strict consensus asks, for each group, whether all trees have it. Adams consensus asks a different question: for each set of species, how do all the trees agree to divide it? At the top, each tree cuts the full set into the groups below its root. Two species stay together in the Adams tree only if every tree keeps them on the same side. Then the method looks at each piece. In each tree it finds the lowest node that holds the whole piece, and it cuts the piece by the branches of that node. It repeats this until each piece is one species.

The effect is that a species that jumps around in the trees does not destroy the structure of the others. It goes down to the deepest place where all trees agree to put it.

## The problem

The input is $k \ge 1$ rooted trees $T_1, \ldots, T_k$ on the same leaf set $X$ of $n$ taxa, without nodes of one child. For a set $B$ of two or more taxa, $\mathrm{lca}_i(B)$ is the lowest node of $T_i$ whose cluster contains $B$. The children of that node divide $B$ into a partition $\pi_i(B)$. The common refinement $\pi(B)$ has as blocks the nonempty intersections of one block of each $\pi_i(B)$, so two taxa are in the same block exactly when every tree puts them below the same child.

The Adams tree $AD$ has a root for $X$, and the node for a block $B$ with $|B| \ge 2$ has one child for each block of $\pi(B)$.

The guarantee is about nestings. For $A \subsetneq B$, the set $A$ *nests in* $B$ in a tree when some cluster contains $A$ and not $B$, which means that $A$ is grouped more tightly than $B$. If $A$ nests in $B$ in all input trees, then $A$ nests in $B$ in the Adams tree.

## The algorithm

```pseudo id=main
ADAMS-CONSENSUS(T_1, ..., T_k)
L1  push the block X on a stack
L2  while the stack is not empty do pop a block B
L3      if |B| = 1 then make B a leaf; continue
L4      for each tree T_i: v_i ← lca_i(B)
L5          π_i ← the partition of B by the children of v_i
L6      π ← π_1 ∧ ... ∧ π_k              ▷ group the taxa of B by their k child labels
L7      make a node for B with one child for each block of π
L8      push each block of π
L9  return the node for X
```

Line L4 finds the lowest node that holds the whole block, and line L5 labels each taxon of the block with the child of that node above it. Line L6 puts two taxa in the same block when their labels agree in every tree. By the first step of the proof, each $\pi_i$ has at least two blocks, so each node gets two children or more and every block is strictly smaller than its parent. Lines L7 and L8 build the tree from the top down. The stack replaces the recursion of the usual description.

## Example

There are two rooted trees on the six taxa A to F:

- $T_1$ = `((((A,B),C),D),(E,F));`
- $T_2$ = `((A,(B,(C,D))),(E,F));`

| block $B$ | node $v_1$ in $T_1$ | $\pi_1$ | node $v_2$ in $T_2$ | $\pi_2$ | $\pi = \pi_1 \wedge \pi_2$ |
|---|---|---|---|---|---|
| ABCDEF | root | ABCD, EF | root | ABCD, EF | ABCD, EF |
| ABCD | ABCD | ABC, D | ABCD | A, BCD | A, BC, D |
| BC | ABC | B, C | BCD | B, C | B, C |
| EF | EF | E, F | EF | E, F | E, F |

The Adams tree is `((A,(B,C),D),(E,F));`. The cluster BC is in neither input tree. It is in the Adams tree because B and C nest in ABCD in both trees: $T_1$ has the cluster ABC and $T_2$ has the cluster BCD, and each contains B and C but not all of ABCD. The [strict consensus](/strict-consensus/) of the same trees is `((A,B,C,D),(E,F));`, and with two trees the [majority-rule consensus](/majority-rule-consensus/) is the same.

A second example shows a taxon that moves. Let $T_1$ = `((((F,A),B),C),(D,E));` and $T_2$ = `(((A,B),C),(D,(F,E)));`. Taxon F is next to A in one tree and next to E in the other. The strict consensus is the star `(A,B,C,D,E,F);`, but the Adams tree is `(((A,B),C),(D,E),F);`. It keeps the structure of the other five taxa and places F at the root.

## Correctness

The proof file proves three facts. First, the output is a tree: if all of $B$ were below one child of $v_i$, that child would be a lower common ancestor, so each $\pi_i$ has two blocks or more, and so does $\pi$. Second, the Adams tree keeps every common nesting. Suppose that $A$ nests in $B$ in every tree, and let $D$ be the smallest Adams block that contains $B$. In each tree, the cluster that holds $A$ and not $B$ lies strictly below $\mathrm{lca}_i(D)$, so $A$ is below one child of that node. So $A$ lies in one block of $\pi(D)$. That block cannot contain $B$, because $D$ is the smallest such block, so it is a cluster of the Adams tree that holds $A$ and not $B$. Third, by the same argument, a cluster that is in every input tree is a cluster of the Adams tree. So the Adams tree refines the strict consensus.

## Complexity

The model is the word RAM. The Adams tree has at most $n - 1$ internal nodes, so lines L4 to L8 run for at most $n - 1$ blocks of size 2 or more.

| step | time per block | reason |
|---|---|---|
| line L4 | $O(kn)$ | one postorder pass per tree that counts the taxa of $B$ below each node |
| line L5 | $O(kn)$ | one traversal of the subtrees below $v_i$ per tree |
| line L6 | $O(k \lvert B \rvert)$ expected | group taxa by their label vectors in a [hash table](/hash-table/) |
| lines L7 and L8 | $O(\lvert B \rvert)$ | |

The total is $O(kn^2)$ time in the worst case, reached when the Adams tree is binary, because each of its $n - 1$ blocks costs $\Theta(kn)$ in this method. The extra space is $O(kn)$ for the label vectors of one block and the stack. With an $O(1)$ [lowest common ancestor](/lowest-common-ancestor/) query structure on each tree, line L4 is faster, but line L5 still touches each taxon of $B$ once per tree. Jansson, Li and Sung (2015) organize the work so that the total is $O(kn \log n)$.

## Properties

- **Keeps common nestings.** Proved above. In particular, every [rooted triplet](/rooted-triplet/) that all input trees show is shown by the Adams tree.
- **Refines the strict consensus.** Every cluster that all trees have is in the Adams tree. The test file checks this on random profiles.
- **Can show new clusters.** The cluster BC of the example is in no input tree. An Adams cluster means "these taxa are always grouped more tightly than the rest of their block", not "these taxa form a clade in some tree".
- **Rooted only.** The method needs the root of each tree. Rooting unrooted trees in different ways gives different results.
- **Unique result.** The tree does not depend on the order of the input trees or of the children. The implementation sorts children by their smallest label to give a canonical tuple.

## Variants and improvements

- **Faster construction.** Jansson, Li and Sung (2015) give an $O(kn \log n)$ time algorithm, against $O(kn^2)$ for the direct method.
- **[Strict](/strict-consensus/) and [majority-rule](/majority-rule-consensus/) consensus** keep clusters by their frequency. They have a direct reading as clades, which the Adams tree does not have.
- **[Maximum agreement subtree](/maximum-agreement-subtree/).** It handles rogue taxa by deleting them, where the Adams tree moves them down to a common node.
- **[Supertrees](/supertree/).** For trees on different leaf sets, the [BUILD](/rooted-triplet/) algorithm of Aho, Sagiv, Szymanski and Ullman uses a similar top-down split of the taxa.

## When to use it

Use the Adams consensus when a few taxa move between distant positions in the trees and you want to see the structure of the other taxa, as in the second example. It is a good diagnostic: comparing it with the strict consensus shows which taxa cause the conflict. Do not use it to report clades or support values. For that, use the [strict](/strict-consensus/) or [majority-rule](/majority-rule-consensus/) consensus.

## Pitfalls

- **Reading Adams clusters as clades.** A cluster of the Adams tree need not be a clade of any input tree. Say so when you publish an Adams tree.
- **Unrooted input.** The method is defined for rooted trees. Root all trees in the same way first, for example with the same outgroup.
- **Wrong node for a block.** Line L4 must use the lowest common ancestor of the current block, computed again in each tree for each block. In the example, the block BC has its lowest common ancestor at ABC in $T_1$, not at the node ABCD where the block was made.
- **Missing the common refinement.** Taking the partition of one tree and checking the others only for consistency is wrong. Two taxa stay together only when every tree keeps them together.
- **Nodes of one child.** Remove them first. Otherwise the lowest node that holds a block can have one child, and the block does not get smaller.

## Implementations

## History

Adams (1972) proposed the method in a paper on comparing taxonomic trees, before the strict and majority rules got their names. Adams (1986) described rooted trees by their nestings and showed that the Adams tree keeps the nestings that all input trees share. Bryant (2003) placed it in a classification of consensus methods. Jansson, Li and Sung (2015) gave the $O(kn \log n)$ algorithm.

## References
