---
tag: 03XC0B
kind: problem
slug: maximum-parsimony
name: Maximum parsimony
aliases:
- large parsimony problem
area: biology/phylogenetics
level: core
summary: Find the tree on the given taxa, with the best labels at the internal nodes, that explains the aligned characters with the least number of changes. NP-hard.
prereqs: [small-parsimony, phylogenetic-tree, rooted-and-unrooted-trees]
see_also: [fitch-algorithm, maximum-parsimony-np-hard, parsimony-informative-site, long-branch-attraction, stepwise-addition, parsimony-ratchet, maximum-likelihood-phylogeny, phylogenetic-tree-reconstruction]
sources:
  - paper: doi:10.1111/j.1558-5646.1965.tb01722.x
    title: Joseph H. Camin and Robert R. Sokal, A method for deducing branching sequences in phylogeny, Evolution 19(3), 1965, 311-326
    locator: the first explicit search for the tree with the least number of changes
  - paper: doi:10.2307/2412116
    title: Walter M. Fitch, Toward defining the course of evolution, minimum change for a specific tree topology, Systematic Zoology 20(4), 1971, 406-416
    locator: the score of a given topology, which a search over topologies minimizes
  - paper: doi:10.1016/S0196-8858(82)80004-3
    title: L. R. Foulds and R. L. Graham, The Steiner problem in phylogeny is NP-complete, Advances in Applied Mathematics 3(1), 1982, 43-49
    locator: the NP-completeness of the decision version
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 1, Parsimony methods; Chapter 3, How many trees are there?; Chapter 4 and Chapter 5, on heuristic search and branch and bound
  - book: isbn:9780262101066
    title: Neil C. Jones and Pavel A. Pevzner, An Introduction to Bioinformatics Algorithms, MIT Press, 2004
    locator: Section 10.11, Large Parsimony Problem
---

Maximum parsimony is the problem of finding the [phylogenetic tree](/phylogenetic-tree/) that explains a set of aligned characters with the least number of changes. The input is one sequence or one row of characters per taxon. Each candidate tree gets the score of its [small parsimony problem](/small-parsimony/), which labels the internal nodes as well as possible, and the answer is a tree of least score. For a fixed tree the score takes linear time, but the number of unrooted binary trees on $n$ taxa is $(2n - 5)!!$, and the problem is [NP-hard](/maximum-parsimony-np-hard/). In practice, exact search works up to about 20 to 30 taxa with branch and bound, and larger data sets need heuristic search.

## In plain words

You have a few species and a gene of each, lined up letter by letter. Many family trees could connect the species. For each tree, guess the letters of the ancestors so that the number of letter changes along the branches is as small as possible. That number is the cost of the tree.

Maximum parsimony picks the tree with the smallest cost. The idea is that the simplest story, with the fewest changes, is the best guess.

To score one tree is fast. The hard part is that there are too many trees to try them all. With 20 species there are more than $10^{20}$ trees. So programs try good trees first, change them a little at a time, and keep the best one they find.

## Definition

**Input.** A set $X$ of $n \ge 3$ taxa, and for each taxon $t$ a row $x_t = x_t[1] \cdots x_t[m]$ of $m$ characters over a set of states $\Sigma$. The columns $x[i] = (x_t[i])_{t \in X}$ are the sites. Optionally a cost $\delta$ on $\Sigma \times \Sigma$; the default is the unit cost, 1 for each change.

**Score of a tree.** For an unrooted tree $T$ whose leaves are the taxa, the parsimony score is

$$\operatorname{PS}(T) = \sum_{i = 1}^{m} \operatorname{PS}(T, x[i]),$$

where $\operatorname{PS}(T, x[i])$ is the small parsimony score of site $i$ on $T$: the least cost of the changes over all ways to give states to the internal nodes.

**Output.** An unrooted tree $T^*$ with $\operatorname{PS}(T^*) = \min_T \operatorname{PS}(T)$. Such a tree is a most parsimonious tree. There can be several.

**Decision version.** Given the rows and an integer $C$, is there a tree $T$ with $\operatorname{PS}(T) \le C$?

**Binary trees are enough.** If a node of $T$ has more than three neighbours, split it into two nodes joined by a new edge, and give the new node the same state as the old one at every site. The cost does not change. So some binary tree is most parsimonious, and searches only look at binary trees.

**Steiner form.** With unit costs, a labeled tree is a tree in the space $\Sigma^m$ of sequences, and its cost is the sum of the [Hamming distances](/hamming-distance/) along its edges. So the least score is the length of a shortest [Steiner tree](/steiner-tree-problem/) for the rows in $\Sigma^m$ with the Hamming metric. A row that ends up at an internal node of the Steiner tree becomes a leaf on an extra edge of length 0.

## Variants

- **Weighted parsimony.** A cost table $\delta$ in place of the unit cost, scored by the [Sankoff algorithm](/sankoff-algorithm/). Weights per site, for example a lower weight for the third position of a codon, are a special case.
- **Ordered characters.** [Wagner parsimony](/wagner-parsimony/), with cost $|i - j|$ between states $i$ and $j$.
- **Rooted, irreversible.** [Camin-Sokal parsimony](/camin-sokal-parsimony/): each character starts in state 0 at the root and only increases.
- **Single gain.** [Dollo parsimony](/dollo-parsimony/): a derived state arises once and can be lost many times.
- **Rooted or unrooted.** For a symmetric cost, the score of a rooted tree does not depend on the root, so the problem is about unrooted trees ([rooted and unrooted trees](/rooted-and-unrooted-trees/)). The Camin-Sokal and Dollo variants are asymmetric and need a root.
- **All most parsimonious trees.** Many programs report all trees of least score, and a [consensus tree](/consensus-tree/) of them.

## Examples

**Four taxa.** There are three unrooted binary trees on the taxa $A, B, C, D$, one for each split $AB \mid CD$, $AC \mid BD$ and $AD \mid BC$. A site of the form $xxyy$, with one state on $A$ and $B$ and another state on $C$ and $D$, costs 1 on the tree $AB \mid CD$ and 2 on the other two. A site such as $xxxy$, $xxyz$ or $xyzw$ costs 1, 2 or 3 on all three trees. So on four taxa, maximum parsimony picks the split that the most sites of the form $xxyy$ support. This simple rule is the base of [long-branch attraction](/long-branch-attraction/).

**Five taxa.** Take these rows of 8 DNA sites.

| taxon | sequence |
|---|---|
| $S_1$ | AAGTTCGA |
| $S_2$ | AAGCTCGA |
| $S_3$ | AGGCTTGC |
| $S_4$ | GGACTTGC |
| $S_5$ | GGACATAC |

There are 15 unrooted binary trees on five taxa. The tree $((S_1, S_2), S_3, (S_4, S_5))$ has score 8: each site needs exactly one change on it. No tree can do better, because each of the 8 sites shows two states and so needs at least one change on any tree. The scores of all 15 trees are 8 (one tree), 10 (two trees: $((S_1, S_2), S_4, (S_3, S_5))$ and $((S_1, S_2), S_5, (S_3, S_4))$), 11 (two trees) and 13 (ten trees). Sites 4, 5 and 7 (columns TCCCC, TTTTA and GGGGA) have one taxon that differs from the rest. They cost 1 on every tree, so they do not help to choose a tree ([parsimony-informative site](/parsimony-informative-site/)). The other five sites decide the answer.

**How many trees.** The number of unrooted binary trees on $n$ labeled taxa is $(2n - 5)!! = 3 \cdot 5 \cdots (2n - 5)$: each new taxon can be put on any of the $2n - 5$ edges of a tree on $n - 1$ taxa.

| $n$ | 4 | 5 | 6 | 7 | 8 | 10 | 20 | 50 |
|---|---|---|---|---|---|---|---|---|
| trees | 3 | 15 | 105 | 945 | 10 395 | 2 027 025 | $\approx 2.2 \cdot 10^{20}$ | $\approx 2.8 \cdot 10^{74}$ |

## Known algorithms

- **Exhaustive search.** Build every tree by [stepwise addition](/stepwise-addition/) of the taxa in all positions, and score each one with [Fitch's algorithm](/fitch-algorithm/). This takes $O((2n - 5)!! \cdot m n)$ time and is practical up to about 10 or 11 taxa.
- **Branch and bound.** Hendy and Penny (1982) add the taxa one at a time and cut a partial tree when its score already reaches the best complete score found so far. Adding a taxon never lowers the score, so the cut is safe. This is a [depth-first branch and bound](/depth-first-branch-and-bound/). It stays exact and often solves 20 to 30 taxa, but its worst case is still exponential.
- **Heuristic search.** Build a start tree by stepwise addition with a random order of the taxa, then improve it by [local search](/local-search/) with [nearest-neighbor interchange](/nearest-neighbor-interchange/), [subtree prune and regraft](/subtree-prune-and-regraft/) or [tree bisection and reconnection](/tree-bisection-and-reconnection/). The [parsimony ratchet](/parsimony-ratchet/) reweights the sites at random to escape local optima. There is no guarantee of optimality.
- **Approximation.** A [minimum spanning tree](/minimum-spanning-tree/) of the rows under the Hamming distance, with each row turned into a leaf by an edge of length 0, is a tree of cost at most twice the optimum, by the [Steiner ratio](/steiner-ratio/) of a metric space.
- **Perfect data.** If the sites are binary and pairwise compatible, a [perfect phylogeny](/perfect-phylogeny/) exists, has one change for each site that is not constant, and is most parsimonious. It is found in $O(nm)$ time.

## Bounds

- **NP-hard.** The decision version is NP-complete, already for binary characters (Foulds and Graham 1982). See [the NP-hardness of maximum parsimony](/maximum-parsimony-np-hard/), which also gives a reduction from [vertex cover](/vertex-cover/).
- **Lower bound per site.** A site with $r$ distinct states needs at least $r - 1$ changes on any tree, so $\operatorname{PS}(T) \ge \sum_i (r_i - 1)$ for every $T$. Branch and bound uses this bound, and the five-taxon example reaches it.
- **Upper bound per site.** A site costs at most $n - f_i$ on any tree, where $f_i$ is the count of its most frequent state: give that state to every internal node.
- **Binary characters.** For two-state sites, the lower bound $\sum_i (r_i - 1)$ is reached if and only if the sites are pairwise compatible, which the [four-gamete condition](/four-gamete-condition/) tests.
- **Search space.** $(2n - 5)!!$ unrooted binary trees, and $(2n - 3)!!$ rooted ones, which is 34 459 425 for $n = 10$.

## Reductions

- **From vertex cover.** For a graph with $m$ edges and vertex cover number $\tau$, a set of $m + 1$ binary rows, the zero row and one row per edge, has least parsimony score $m + \tau$. This makes maximum parsimony NP-hard. The details are in [the NP-hardness page](/maximum-parsimony-np-hard/).
- **To and from the Steiner tree problem.** With unit costs, maximum parsimony is the Steiner tree problem in the Hamming space $\Sigma^m$, as in the definition. This is the view of Foulds and Graham.
- **Small parsimony inside.** The score of one tree is a [small parsimony](/small-parsimony/) problem per site, solved by [Fitch's](/fitch-algorithm/), [Hartigan's](/hartigan-algorithm/) or the [Sankoff](/sankoff-algorithm/) algorithm.
- **Relation to likelihood.** For a model in which every site has its own branch lengths, the [maximum likelihood](/maximum-likelihood-phylogeny/) tree is the most parsimonious tree (Tuffley and Steel 1997). Under a common model with shared branch lengths the two methods can disagree, and parsimony can be inconsistent ([long-branch attraction](/long-branch-attraction/)).

## Applications

- **Morphological data.** In cladistics, the characters are traits of the body, coded as states. Parsimony is still a standard method for such data, where good models of change are hard to give.
- **Molecular data.** For DNA and protein alignments, parsimony is fast and needs no model. It is often used for a quick tree or a start tree for [maximum likelihood](/maximum-likelihood-phylogeny/).
- **Ancestral states.** The labels of a most parsimonious tree give a reconstruction of the ancestors ([ancestral sequence reconstruction](/ancestral-sequence-reconstruction/)).
- **Support of branches.** The [phylogenetic bootstrap](/phylogenetic-bootstrap/) repeats the search on resampled sites to measure how well the data support each branch.

## References
