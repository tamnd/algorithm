---
tag: WP9YPG
kind: problem
slug: consensus-tree
name: Consensus tree
area: biology/phylogenetics
level: advanced
summary: Given several trees on the same taxa, return one tree that summarizes the groups they share. Strict, majority-rule and Adams rules give different answers.
prereqs: [phylogenetic-tree, splits-of-a-tree]
see_also: [strict-consensus, majority-rule-consensus, adams-consensus, supertree, robinson-foulds-distance, maximum-agreement-subtree, phylogenetic-bootstrap, consensus-clustering]
sources:
  - paper: doi:10.2307/2412432
    title: Edward N. Adams III, Consensus techniques and the comparison of taxonomic trees, Systematic Zoology 21(4), 1972, pages 390 to 397
    locator: the first consensus tree method, now called the Adams consensus
  - paper: doi:10.1007/BF02459446
    title: T. Margush and F. R. McMorris, Consensus n-trees, Bulletin of Mathematical Biology 43(2), 1981, pages 239 to 244
    locator: the majority rule for clusters and the proof that the clusters in more than half of the trees form a tree
  - paper: doi:10.1007/BF01894194
    title: J. P. Barthelemy and F. R. McMorris, The median procedure for n-trees, Journal of Classification 3(2), 1986, pages 329 to 334
    locator: the majority-rule tree as a median for the symmetric difference distance
  - paper: doi:10.1007/BF01908061
    title: William H. E. Day, Optimal algorithms for comparing trees with labeled leaves, Journal of Classification 2, 1985, pages 7 to 28
    locator: the O(kn) strict consensus by an interval table
  - paper: doi:10.1007/978-3-540-39763-2_17
    title: Nina Amenta, Frederick Clarke and Katherine St. John, A linear-time majority tree algorithm, WABI 2003, LNCS 2812, pages 216 to 227
    locator: a randomized algorithm for the majority-rule tree in O(kn) expected time
  - paper: doi:10.1145/2925985
    title: Jesper Jansson, Chuanqi Shen and Wing-Kin Sung, Improved algorithms for constructing consensus trees, Journal of the ACM 63(3), 2016, article 28
    locator: deterministic O(nk) algorithms for the majority-rule and loose consensus trees, and O(n^2 k) for the greedy consensus tree
  - paper: "David Bryant, A classification of consensus methods for phylogenetics, in Bioconsensus, DIMACS Series in Discrete Mathematics and Theoretical Computer Science 61, 2003, pages 163 to 184"
    title: David Bryant, A classification of consensus methods for phylogenetics
    locator: the definitions of the cluster based, Adams and median consensus methods and the relations between them
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, 2004
    locator: Chapter 30, Consensus trees and distances between trees
  - book: isbn:9781107184718
    title: Tandy Warnow, Computational Phylogenetics, 2017
    locator: Chapter 6, Consensus and agreement trees
---

The consensus tree problem takes a set of [phylogenetic trees](/phylogenetic-tree/) on the same taxa and asks for one tree that summarizes them. The trees can be the equally good trees of one search, the trees of a [bootstrap](/phylogenetic-bootstrap/) or of a [Bayesian](/bayesian-phylogenetic-inference/) sample, or trees from different genes. There is no single correct answer: each consensus rule states which groups to keep, and the rules differ in how much disagreement they accept. The three classic rules are the [strict consensus](/strict-consensus/), the [majority-rule consensus](/majority-rule-consensus/) and the [Adams consensus](/adams-consensus/).

## In plain words

Suppose that you have a hundred trees for the same twenty species, and they agree on many groups but not on all. A reader wants one picture. A consensus tree is that picture. It shows a group of species when enough of the trees support that group. Where the trees disagree, it puts the species on one node with many branches, which means that the order of splitting there is open.

How much support is enough is a choice. The strict rule needs all trees, so it shows few groups, but each one is certain. The majority rule needs more than half of the trees, so it shows more groups, and it usually writes the percentage of trees on each group. Other rules keep information that is not a group, for example that a species always falls inside some larger group.

## Definition

**Input.** A profile $P = (T_1, \ldots, T_k)$ of $k \ge 1$ trees on the same leaf set $X$, $|X| = n$. The trees are either all rooted or all unrooted, and internal nodes can have more than two children.

**Clusters and splits.** For a rooted tree, the cluster of a node is the set of leaves below it, and $\mathcal{C}(T)$ is the set of clusters of $T$. For an unrooted tree, each edge gives a [split](/splits-of-a-tree/) $A \mid B$, and $\Sigma(T)$ is the set of splits. A tree is fixed by its clusters or by its splits. For a cluster or split $c$, its frequency is $f(c) = |\{i : c \in \mathcal{C}(T_i)\}| / k$.

**Output.** A tree $T$ on $X$, chosen by a consensus rule, which is a function from profiles to trees. The main rules are:

- **Threshold rules.** For $\ell \in [1/2, 1]$, the tree $M_\ell$ has the clusters $c$ with $f(c) > \ell$, or with $f(c) = 1$ when $\ell = 1$. The strict consensus is $M_1$, and the majority-rule consensus is $M_{1/2}$. For $\ell \ge 1/2$ these clusters are always pairwise compatible, so $M_\ell$ exists. For $\ell < 1/2$ two such clusters can conflict, and no tree has them all.
- **Median rule.** A median tree minimizes $\sum_i d(T, T_i)$ for a tree distance $d$. With the [Robinson-Foulds distance](/robinson-foulds-distance/), the majority-rule tree is a median (Barthélemy and McMorris 1986).
- **Adams rule.** The [Adams consensus](/adams-consensus/) keeps the nestings of the trees, which are statements of the form "the set $A$ falls inside a smaller group than the set $B$ does". It is defined for rooted trees only.

A rule is *Pareto* on clusters if every cluster that is in all $T_i$ is in the output. The strict, majority and Adams rules are all Pareto. The strict consensus is contained in every output of a threshold rule.

## Variants

- **Rooted or unrooted.** Root every unrooted tree at the same taxon to move between splits and clusters. The threshold rules give the same result either way. The Adams rule needs real roots.
- **Greedy or extended majority.** Sort all clusters by frequency, and add each one that is compatible with those already chosen. The result refines the majority-rule tree, but it depends on how ties are broken.
- **Semi-strict or combinable component consensus.** Keep each cluster of some input tree that is compatible with every input tree. It suits profiles where some trees are less resolved.
- **Weighted trees.** Each tree has a weight, for example a posterior probability. The frequency becomes the total weight of the trees that contain the cluster.
- **Agreement subtrees.** Remove taxa, not groups: the [maximum agreement subtree](/maximum-agreement-subtree/) is the largest set of taxa on which all trees agree.
- **Different leaf sets.** When the trees have different taxa, the problem becomes the [supertree](/supertree/) problem.

## Examples

Take the three rooted trees on the six taxa A to F:

- $T_1$ = `(((A,B),C),(D,(E,F)));` with the nontrivial clusters AB, ABC, DEF and EF
- $T_2$ = `(((A,B),D),(C,(E,F)));` with AB, ABD, CEF and EF
- $T_3$ = `((A,(B,C)),(D,(E,F)));` with BC, ABC, DEF and EF

The frequencies are 3/3 for EF, 2/3 for AB, ABC and DEF, and 1/3 for ABD, CEF and BC.

| rule | result | nontrivial clusters |
|---|---|---|
| strict ($M_1$) | `(A,B,C,D,(E,F));` | EF |
| $M_\ell$ for $1/2 \le \ell < 2/3$ | `(((A,B),C),(D,(E,F)));` | AB, ABC, DEF, EF |
| Adams | `((A,B),C,D,(E,F));` | AB, EF |

Here the majority-rule tree equals $T_1$. The Adams rule first splits all six taxa by the root of each tree, into ABC and DEF, into ABD and CEF, and into ABC and DEF. The common refinement of these three partitions is AB, C, D and EF, so these are the four children of the root. Inside AB and EF nothing more happens. The Adams tree here lies between the other two. The [Adams consensus](/adams-consensus/) page has a profile where the Adams tree shows a cluster that no input tree has.

The sum of the Robinson-Foulds distances, counted as the number of clusters in one tree and not in the other, is $0 + 4 + 2 = 6$ for $T_1$ and $3 + 3 + 3 = 9$ for the strict consensus. No tree has a smaller sum than 6, because the majority-rule tree is a median.

## Known algorithms

| rule | algorithm | time |
|---|---|---|
| strict | [Day's interval table](/strict-consensus/) | $O(kn)$ |
| majority-rule | count bit-set clusters in a [hash table](/hash-table/) | $O(kn^2 / w)$ expected |
| majority-rule | Amenta, Clarke and St. John (2003) | $O(kn)$ expected |
| majority-rule | Jansson, Shen and Sung (2016) | $O(kn)$ deterministic |
| semi-strict (loose) | Jansson, Shen and Sung (2016) | $O(kn)$ |
| greedy | Jansson, Shen and Sung (2016) | $O(kn^2)$ |
| Adams | Adams (1972), partition refinement | $O(kn^2)$ |
| Adams | Jansson, Li and Sung (2015) | $O(kn \log n)$ |

Here $w$ is the word size. The input has size $\Theta(kn)$, so the strict and majority-rule trees are computable in linear time.

## Bounds

- **Lower bound.** Any rule that depends on all trees must read the input, so $\Omega(kn)$ time is needed. The linear-time algorithms above are optimal up to constant factors.
- **Size of the output.** A rooted tree on $n$ leaves without nodes of one child has at most $n - 1$ internal nodes, so every consensus tree has at most $n - 2$ nontrivial clusters.
- **Threshold 1/2 is tight.** For $\ell < 1/2$ the clusters with frequency above $\ell$ can conflict. With the two trees `((A,B),C);` and `((A,C),B);`, the clusters AB and AC each have frequency 1/2, and no tree has both.

## Reductions

- **Majority rule as a median.** For the Robinson-Foulds distance, $\sum_i d(T, T_i) = \sum_i |\mathcal{C}(T_i)| + \sum_{c \in \mathcal{C}(T)} (k - 2 k f(c))$. Each cluster with $f(c) > 1/2$ lowers the sum, and each cluster with $f(c) < 1/2$ raises it. So the majority-rule tree minimizes the sum, as the [majority-rule consensus](/majority-rule-consensus/) page proves.
- **Comparison of two trees.** The strict consensus of two trees has $|\mathcal{C}(T_1) \cap \mathcal{C}(T_2)|$ nontrivial clusters, which gives the [Robinson-Foulds distance](/robinson-foulds-distance/) in the same time.
- **Special case of supertrees.** A profile on one leaf set is a [supertree](/supertree/) input in which all trees have all taxa. A supertree method that returns the strict consensus on such input is said to generalize it.

## Applications

- **Equally optimal trees.** A [maximum parsimony](/maximum-parsimony/) search often finds many trees of the same length. The strict consensus reports the groups that they all share.
- **Support values.** The majority-rule tree of [bootstrap](/phylogenetic-bootstrap/) trees, with the frequency of each cluster written on its edge, is the usual way to report bootstrap support. The same summary of a posterior sample of trees from [Bayesian inference](/bayesian-phylogenetic-inference/) gives posterior clade probabilities.
- **Gene trees.** Consensus trees of trees from different genes show the groups that most genes support. Methods for [species tree estimation](/species-tree-estimation/) such as [ASTRAL](/astral/) are more suitable when gene trees differ because of [incomplete lineage sorting](/incomplete-lineage-sorting/).
- **Clustering.** The same ideas apply to hierarchical clusterings of data, as in [consensus clustering](/consensus-clustering/).

## References
