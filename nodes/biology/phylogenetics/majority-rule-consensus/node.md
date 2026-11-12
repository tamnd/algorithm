---
tag: X4MGF9
kind: algorithm
slug: majority-rule-consensus
name: Majority-rule consensus
aliases:
- majority consensus tree
area: biology/phylogenetics
level: intro
summary: Keeps the clusters or splits found in more than half of the input trees. They always fit in one tree, and that tree is a Robinson-Foulds median.
solves: [consensus-tree]
model: word-ram
complexity:
  vars: {k: the number of input trees, n: the number of taxa, w: the word size in bits}
  time: {expected: "O(k n^2 / w + n^2)"}
  space: {extra: "O(k n^2 / w)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1981
  people: [T. Margush, F. R. McMorris]
  note: Margush and McMorris defined the majority rule for n-trees in 1981. Barthelemy and McMorris showed in 1986 that it gives a median tree.
prereqs: [consensus-tree, splits-of-a-tree, robinson-foulds-distance]
see_also: [strict-consensus, adams-consensus, phylogenetic-bootstrap, bayesian-phylogenetic-inference, hash-table, bitmask, day-algorithm, tree-comparison]
sources:
  - paper: doi:10.1007/BF02459446
    title: T. Margush and F. R. McMorris, Consensus n-trees, Bulletin of Mathematical Biology 43(2), 1981, pages 239 to 244
    locator: the definition of the majority rule and the proof that the majority clusters are compatible
  - paper: doi:10.1007/BF01894194
    title: J. P. Barthelemy and F. R. McMorris, The median procedure for n-trees, Journal of Classification 3(2), 1986, pages 329 to 334
    locator: the majority-rule tree as a median for the symmetric difference metric
  - paper: doi:10.1007/978-3-540-39763-2_17
    title: Nina Amenta, Frederick Clarke and Katherine St. John, A linear-time majority tree algorithm, WABI 2003, LNCS 2812, pages 216 to 227
    locator: a randomized O(kn) expected time algorithm
  - paper: doi:10.1145/2925985
    title: Jesper Jansson, Chuanqi Shen and Wing-Kin Sung, Improved algorithms for constructing consensus trees, Journal of the ACM 63(3), 2016, article 28
    locator: a deterministic O(kn) time algorithm for the majority-rule tree, and the greedy consensus tree
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, 2004
    locator: Chapter 30, Consensus trees and distances between trees, majority-rule consensus trees
  - book: isbn:9781107184718
    title: Tandy Warnow, Computational Phylogenetics, 2017
    locator: Chapter 6, Consensus and agreement trees
---

The majority-rule consensus of a set of [phylogenetic trees](/phylogenetic-tree/) on the same taxa keeps each cluster, or each [split](/splits-of-a-tree/) for unrooted trees, that is in more than half of the trees. Any two such clusters share a tree, so they are compatible, and together they always form one tree. It is the usual answer to the [consensus tree](/consensus-tree/) problem for a sample of trees: the frequency of each kept cluster is its [bootstrap](/phylogenetic-bootstrap/) support or its posterior probability. Barthélemy and McMorris (1986) showed that it is a median tree for the [Robinson-Foulds distance](/robinson-foulds-distance/).

## In plain words

You have many trees for the same species, for example a thousand trees from a bootstrap analysis. For each group of species, count how many trees have that group. Keep the groups that more than half of the trees have, and write the percentage on each one.

Why do the kept groups always fit in one tree? Take two kept groups. Each one is in more than half of the trees, so at least one tree has both. Groups of one tree never cross each other, so the two groups do not cross. That holds for every pair, so all the kept groups fit in one tree.

The tree is also the best middle tree. If you count, for each input tree, the groups in which it differs from a candidate tree, the majority tree has the smallest total.

## The problem

The input is $k \ge 1$ rooted trees $T_1, \ldots, T_k$ on the same leaf set $X$ of $n$ taxa, without nodes of one child. For a set $c \subseteq X$ of 2 to $n - 1$ taxa, $n_c$ is the number of trees that have $c$ as a cluster. The output is the tree $T_M$ whose nontrivial clusters are the sets $c$ with $n_c > k/2$, and the count $n_c$ of each. For unrooted trees, root every tree at the same taxon $r$, so that the split $A \mid B$ with $r \in B$ becomes the cluster $A$.

## The algorithm

```pseudo id=main
MAJORITY-RULE(T_1, ..., T_k)
L1  count ← an empty hash table, keyed by bit sets of taxa
L2  for each tree T_i do
L3      for each internal node v of T_i, in postorder, add 1 to count[cluster(v)]
L4  M ← the clusters c ≠ X with count[c] > k/2
L5  sort M by decreasing size; set owner(x) ← X for each taxon x
L6  for each c ∈ M in that order do
L7      make a node for c below the node owner(x), for any x ∈ c
L8      set owner(x) ← c for each x ∈ c
L9  hang each taxon x below owner(x); return the tree and the counts
```

Line L3 computes the bit set of a node as the union of the bit sets of its children, so each cluster costs one pass over its children. Line L4 is the majority rule. The strict inequality matters: with an even $k$, two conflicting clusters can each be in exactly half of the trees. Lines L5 to L9 build the tree from its clusters. Processing the clusters from large to small means that when $c$ comes, the last kept cluster that holds a taxon of $c$ is the parent of $c$.

## Example

There are three rooted trees on the six taxa A to F:

- $T_1$ = `(((A,B),C),(D,(E,F)));`
- $T_2$ = `(((A,B),D),(C,(E,F)));`
- $T_3$ = `((A,(B,C)),(D,(E,F)));`

**Lines L1 to L4.** The table after all three trees:

| cluster | AB | ABC | BC | ABD | CEF | DEF | EF |
|---|---|---|---|---|---|---|---|
| count | 2 | 2 | 1 | 1 | 1 | 2 | 3 |
| kept ($> 3/2$) | yes | yes | no | no | no | yes | yes |

**Lines L5 to L9.** The kept clusters by decreasing size are ABC, DEF, AB and EF.

| step | cluster | parent from owner | owner after the step |
|---|---|---|---|
| 1 | ABC | root | A, B, C → ABC |
| 2 | DEF | root | D, E, F → DEF |
| 3 | AB | ABC | A, B → AB |
| 4 | EF | DEF | E, F → EF |

The result is `(((A,B)67,C)67,(D,(E,F)100)67);`, with the support of each cluster in percent. It equals $T_1$.

**The median property.** Count the Robinson-Foulds distance as the number of nontrivial clusters in one tree and not in the other. The sums of the distances to the three input trees are:

| candidate | to $T_1$ | to $T_2$ | to $T_3$ | sum |
|---|---|---|---|---|
| $T_M = T_1$ | 0 | 4 | 2 | 6 |
| $T_2$ | 4 | 0 | 6 | 10 |
| $T_3$ | 2 | 6 | 0 | 8 |
| strict consensus `(A,B,C,D,(E,F));` | 3 | 3 | 3 | 9 |

The test file checks, over all 236 rooted trees on five taxa, that no tree has a smaller sum than the majority tree.

## Correctness

The proof file has three steps. First, if $n_a > k/2$ and $n_b > k/2$, then the sets of trees that contain $a$ and $b$ have more than $k$ members together, so some tree contains both, and $a$ and $b$ are compatible. Second, the construction of lines L5 to L9 gives the unique tree with exactly these clusters: when $c$ comes, every earlier cluster that meets $c$ contains $c$, so the owner of each taxon of $c$ is the smallest kept cluster above $c$. Third, the median property: for any tree $T$,
$$\sum_i d(T, T_i) = \sum_i |\mathcal{C}(T_i)| + \sum_{c \in \mathcal{C}(T)} (k - 2 n_c).$$
A cluster lowers this sum exactly when $n_c > k/2$. The majority tree has all such clusters and no others, so it has the smallest sum. If $k$ is odd, no term is zero, and the majority tree is the only median.

## Complexity

The model is the word RAM with $w$-bit words, and the bit set of a cluster takes $\lceil n / w \rceil$ words.

| step | time | reason |
|---|---|---|
| lines L2 and L3 | $O(kn^2 / w)$ expected | fewer than $kn$ clusters, each an $n$-bit union and a hash probe |
| line L4 | $O(kn^2 / w)$ | one pass over the table |
| line L5 | $O(n \log n)$ | at most $n - 2$ clusters are kept |
| lines L6 to L9 | $O(n^2)$ | each kept cluster updates the owners of its taxa |

The total is $O(kn^2 / w + n^2)$ expected time and $O(kn^2 / w)$ words for the table. For the usual sizes, a few thousand trees on a few hundred taxa, this is fast. Amenta, Clarke and St. John (2003) give a randomized algorithm in $O(kn)$ expected time, and Jansson, Shen and Sung (2016) a deterministic one in $O(kn)$ time. Both are optimal, because the input has size $\Theta(kn)$.

## Properties

- **Always a tree.** The majority clusters are compatible for every profile. The bound $1/2$ is the smallest threshold for which this holds: for the two trees `((A,B),C);` and `((A,C),B);`, AB and AC each have frequency $1/2$ and conflict.
- **A median.** It minimizes the total Robinson-Foulds distance to the input trees, and it is the unique minimizer when $k$ is odd.
- **Refines the strict consensus.** Every cluster that is in all trees is kept.
- **Need not be an input tree.** The majority tree can have clusters that never occur together in one input tree.
- **Same for rooted and unrooted.** For unrooted trees, rooting at any one taxon gives the same set of splits.
- **Independent of order.** The output depends only on the multiset of trees.

## Variants and improvements

- **Threshold consensus.** Keep the clusters with $n_c > \ell k$ for some $\ell \ge 1/2$. The value $\ell = 1$, with $n_c = k$, gives the [strict consensus](/strict-consensus/).
- **Greedy or extended majority consensus.** After the majority clusters, add the other clusters in order of decreasing count, each one if it is compatible with all clusters already chosen. Many programs, for example the consense program of PHYLIP, offer this option. The result depends on how ties are broken, and Jansson, Shen and Sung (2016) compute it in $O(kn^2)$ time.
- **Weighted trees.** Give each tree a weight, such as a posterior probability, and use the total weight in place of the count.
- **[Adams consensus](/adams-consensus/).** It uses nestings in place of counts and can keep structure that no single cluster frequency shows.

## When to use it

Use the majority-rule tree to summarize a sample of trees: the [bootstrap](/phylogenetic-bootstrap/) replicates of a data set or the posterior sample of a [Bayesian analysis](/bayesian-phylogenetic-inference/). The count on each edge is the support value that readers expect. Use the [strict consensus](/strict-consensus/) when a group must be in every tree, for example among equally optimal trees.

## Pitfalls

- **Ties with even $k$.** A cluster in exactly half of the trees is not kept. Use $2 \cdot \mathrm{count} > k$, not $\ge$, or two conflicting clusters can both pass.
- **Splits on different sides.** For unrooted trees, a split $A \mid B$ must have one canonical form, for example the side without a fixed taxon. Otherwise $A$ and $X \setminus A$ count as two different keys.
- **Support is not probability of truth.** A bootstrap frequency of 70 percent does not mean that the group is true with probability 0.7.
- **Reading a point estimate.** The majority-rule tree is a summary. It need not be the most frequent tree, and it may not be the best tree for the data under the model.
- **Unresolved inputs.** A tree with a multifurcation does not have the clusters that a resolution would have. Many polytomies lower the counts, so check how the trees were made.

## Implementations

## History

Margush and McMorris (1981) defined the majority rule for n-trees, which are rooted trees described by their clusters, and proved that the clusters in more than half of the trees are compatible. Barthélemy and McMorris (1986) showed that the majority-rule tree is a median for the symmetric difference metric, which is the Robinson-Foulds distance. Felsenstein (1985) used the majority-rule tree to report bootstrap support, and this became the standard practice. Amenta, Clarke and St. John (2003) and Jansson, Shen and Sung (2016) gave linear-time algorithms.

## References
