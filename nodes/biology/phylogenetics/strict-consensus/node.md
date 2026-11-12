---
tag: RNKXSB
kind: algorithm
slug: strict-consensus
name: Strict consensus tree
aliases:
- strict consensus
area: biology/phylogenetics
level: intro
summary: Keeps only the clusters or splits found in every input tree. Day's interval table computes it in O(kn) time for k trees on n taxa.
solves: [consensus-tree]
model: word-ram
complexity:
  vars: {k: the number of input trees, n: the number of taxa}
  time: {worst: "O(k n)"}
  space: {extra: "O(n)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1985
  people: [Robert R. Sokal, F. James Rohlf, William H. E. Day]
  note: The name strict consensus is usually credited to Sokal and Rohlf (1981). Day (1985) gave the first algorithm that runs in time linear in the input size.
prereqs: [consensus-tree, splits-of-a-tree]
see_also: [majority-rule-consensus, adams-consensus, day-algorithm, robinson-foulds-distance, tree-comparison, phylogenetic-bootstrap, supertree, split-system]
sources:
  - paper: doi:10.1007/BF01908061
    title: William H. E. Day, Optimal algorithms for comparing trees with labeled leaves, Journal of Classification 2, 1985, pages 7 to 28
    locator: the cluster table of a tree with leaves in depth-first order, and its use for the strict consensus in O(kn) time
  - paper: doi:10.1007/BF02459446
    title: T. Margush and F. R. McMorris, Consensus n-trees, Bulletin of Mathematical Biology 43(2), 1981, pages 239 to 244
    locator: the consensus rules in terms of clusters (n-trees), with the strict rule as the case of a threshold of all trees
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, 2004
    locator: Chapter 30, Consensus trees and distances between trees
  - book: isbn:9781107184718
    title: Tandy Warnow, Computational Phylogenetics, 2017
    locator: Chapter 6, Consensus and agreement trees
---

The strict consensus tree of a set of [phylogenetic trees](/phylogenetic-tree/) on the same taxa keeps exactly the groups that every input tree has, and it merges everything else into multifurcations. For rooted trees the groups are clusters, and for unrooted trees they are [splits](/splits-of-a-tree/). It is the most cautious answer to the [consensus tree](/consensus-tree/) problem: each group that it shows is supported by all the trees. Day (1985) showed how to compute it in $O(kn)$ time for $k$ trees on $n$ taxa, which is linear in the size of the input.

## In plain words

You have several trees for the same species, for example the many equally good trees from a parsimony search. You want one summary tree. The strict consensus keeps a group of species only if every tree puts that group together. Where the trees do not agree, it does not choose. It puts the species of that region on one node with many branches, which means that the question is open.

To find the shared groups fast, the method reads the leaves of the first tree from left to right. Then each group of that tree is a run of neighboring positions. A group of another tree is in the first tree only if its leaves form a run with no gap, and a small table tells in one step whether that run is a group of the first tree.

## The problem

The input is $k \ge 1$ rooted trees $T_1, \ldots, T_k$ on the same leaf set $X$ of $n$ taxa. Internal nodes can have any number of children, but not exactly one. The cluster of a node is the set of leaves below it. The output is the tree $S$ whose clusters are the clusters that are in all $k$ trees. This tree always exists and is unique, because the shared clusters are a subset of the clusters of $T_1$, and clusters of one tree are nested or disjoint (see the proof file).

For unrooted trees, root every tree at the same taxon $r$. A split $A \mid B$ with $r \in B$ then becomes the cluster $A$, so shared splits and shared clusters correspond one to one.

## The algorithm

```pseudo id=main
STRICT-CONSENSUS(T_1, ..., T_k)
L1  number the leaves of T_1 from 1 to n in depth-first order
L2  for each node v of T_1, set lo(v), hi(v) to its first and last leaf number
L3  for each internal node v of T_1: if v is the root or a leftmost child,
        store (lo(v), hi(v)) in row hi(v) of table X, else in row lo(v)
L4  set count(r) ← 1 for each row r that holds an entry
L5  for j ← 2 to k do
L6      in postorder of T_j, compute min, max and size of each cluster (leaf numbers of T_1)
L7      if max − min + 1 = size and X[min] or X[max] equals (min, max), add 1 to that row's count
L8  keep the internal nodes v of T_1 with count = k, and the root
L9  return T_1 with the internal edges above the other nodes contracted
```

Line L1 is the key idea. After it, every cluster of $T_1$ is an interval of leaf numbers, so a pair of numbers names it. Line L3 puts each interval in one row of a table with $n$ rows. The rule about the leftmost child makes sure that no two intervals use the same row. Line L6 reads a cluster of another tree in terms of the numbers of $T_1$. If its numbers have a gap, the cluster is not an interval and cannot be in $T_1$. If they form an interval, the cluster is in $T_1$ exactly when the table has this interval in row min or in row max. Line L9 removes the clusters that failed, which makes their children children of the node above.

## Example

There are three rooted trees on the six taxa A to F, in [Newick format](/newick-format/):

- $T_1$ = `(((A,B),C),(D,(E,F)));`
- $T_2$ = `(((A,B),D),(C,(E,F)));`
- $T_3$ = `((A,(B,C)),(D,(E,F)));`

**Lines L1 to L4.** The leaf order of $T_1$ gives A = 1, B = 2, C = 3, D = 4, E = 5, F = 6. The table is:

| node of $T_1$ | interval | leftmost child or root | row |
|---|---|---|---|
| AB | (1, 2) | yes | 2 |
| ABC | (1, 3) | yes | 3 |
| EF | (5, 6) | no | 5 |
| DEF | (4, 6) | no | 4 |
| root | (1, 6) | root | 6 |

**Lines L5 to L7.** The clusters of $T_2$ and $T_3$, in leaf numbers:

| tree | cluster | numbers | min, max, size | interval | in table | count after |
|---|---|---|---|---|---|---|
| $T_2$ | AB | 1, 2 | 1, 2, 2 | yes | row 2 | AB: 2 |
| $T_2$ | ABD | 1, 2, 4 | 1, 4, 3 | no | | |
| $T_2$ | EF | 5, 6 | 5, 6, 2 | yes | row 5 | EF: 2 |
| $T_2$ | CEF | 3, 5, 6 | 3, 6, 3 | no | | |
| $T_2$ | root | 1 to 6 | 1, 6, 6 | yes | row 6 | root: 2 |
| $T_3$ | BC | 2, 3 | 2, 3, 2 | yes | no: row 2 holds (1, 2), row 3 holds (1, 3) | |
| $T_3$ | ABC | 1, 2, 3 | 1, 3, 3 | yes | row 3 | ABC: 2 |
| $T_3$ | EF | 5, 6 | 5, 6, 2 | yes | row 5 | EF: 3 |
| $T_3$ | DEF | 4, 5, 6 | 4, 6, 3 | yes | row 4 | DEF: 2 |
| $T_3$ | root | 1 to 6 | 1, 6, 6 | yes | row 6 | root: 3 |

**Lines L8 and L9.** Only EF and the root have count 3. Contracting AB, ABC and DEF gives the strict consensus `(A,B,C,D,(E,F));`. The [majority-rule consensus](/majority-rule-consensus/) of the same trees is $T_1$, because AB, ABC and DEF are each in two of the three trees.

## Correctness

Clusters of one tree are nested or disjoint, and a depth-first order makes each of them an interval of leaf numbers. The proof file shows that the rule of line L3 gives every internal node of $T_1$ its own row: two nested intervals with the same right end belong to a node and its last descendant on the right side, and that descendant is not a leftmost child, so it uses its left end. So the test of line L7 is exact. A cluster of $T_j$ is in $T_1$ if and only if it is an interval whose pair is in row min or row max. Each tree has each cluster at most once, so a counter reaches $k$ exactly when its cluster is in all trees. The shared clusters are a subfamily of the clusters of $T_1$, and contracting the other edges of $T_1$ gives the unique tree with exactly these clusters. The full proof is in the proof file.

## Complexity

The model is the word RAM. A tree on $n$ leaves without nodes of one child has fewer than $n$ internal nodes.

| step | time | reason |
|---|---|---|
| lines L1 to L4 | $O(n)$ | one traversal of $T_1$ |
| line L6 for one tree | $O(n)$ | min, max and size come from the children |
| line L7 for one tree | $O(n)$ | two table lookups per node |
| lines L8 and L9 | $O(n)$ | one traversal of $T_1$ |

The total is $O(kn)$ time, which is the size of the input, so no algorithm can be faster by more than a constant factor. The table, the counters and the arrays for the current tree take $O(n)$ extra space. A direct method that stores every cluster as an $n$-bit set and intersects the sets takes $O(kn^2/w)$ time on words of $w$ bits.

## Properties

- **A subset of every input.** The strict consensus is a contraction of each input tree. So it never shows a group that some tree rejects.
- **Monotone in the input.** Adding a tree can only remove clusters. With many trees, the result often becomes a star with little information.
- **Order does not matter.** The cluster set does not depend on the order of the trees. The implementation takes the left-to-right order of children from $T_1$, but the tree is the same.
- **Pareto.** A cluster that is in all trees is in the output, and the output has no other cluster. So it is the most conservative of the rules that keep clusters by their frequency.
- **Equivalent for splits.** For unrooted trees, rooting at one taxon gives the same result for every choice of that taxon.

## Variants and improvements

- **[Majority-rule consensus](/majority-rule-consensus/)** keeps the clusters that are in more than half of the trees. It always contains the strict consensus.
- **Semi-strict or combinable component consensus** (Bremer 1990) keeps every cluster that is compatible with all input trees, not only the clusters that all trees have. It is useful when some trees are less resolved than others.
- **[Adams consensus](/adams-consensus/)** keeps nesting information and can show groups that no input tree has.
- **[Supertrees](/supertree/).** When the trees have different leaf sets, strict consensus is not defined. Steel (1992) gives a polynomial algorithm for the strict consensus of all trees that display a set of rooted trees on overlapping leaf sets.
- **Comparing two trees.** The same table also counts the shared clusters of two trees in $O(n)$ time, which gives the [Robinson-Foulds distance](/robinson-foulds-distance/). This is the use of [Day's algorithm](/day-algorithm/).

## When to use it

Use the strict consensus to report the groups that all your equally optimal trees agree on, for example the shortest trees of a [maximum parsimony](/maximum-parsimony/) search. Use it when a group shown must hold in every tree, as when you summarize the trees from several data sets and want only the uncontested groups. For a sample of trees from the [bootstrap](/phylogenetic-bootstrap/) or from [Bayesian inference](/bayesian-phylogenetic-inference/), the strict consensus is usually a star, and the [majority-rule consensus](/majority-rule-consensus/) is the usual choice.

## Pitfalls

- **One rogue taxon.** A single taxon that moves between distant places in the trees removes every cluster on the paths between those places. The result can be a star, although the other taxa agree.
- **Different leaf sets.** All trees must have the same taxa. Prune them to the common leaf set first, or use a [supertree](/supertree/) method.
- **Rooted against unrooted.** The cluster $\{A, B\}$ of a rooted tree is not the same thing as the split $AB \mid CDEF$ of an unrooted tree. For unrooted trees, root all trees at the same taxon before using the cluster test.
- **Wrong table rule.** If every interval is stored in its right end row, nested intervals with the same right end overwrite each other, and the test misses clusters.
- **Nodes of one child.** A node with one child repeats the cluster of its child. Remove such nodes first, or line L7 counts the cluster twice for one tree.

## Implementations

## History

Adams (1972) introduced the first consensus tree method. The strict rule, which keeps only the shared groups, is usually credited to Sokal and Rohlf (1981), and Margush and McMorris (1981) studied it with the other rules that keep clusters found in more than a given fraction of the trees. Day (1985) gave the interval table that compares a cluster with a tree in constant time, which makes the strict consensus and the Robinson-Foulds distance linear-time problems.

## References
