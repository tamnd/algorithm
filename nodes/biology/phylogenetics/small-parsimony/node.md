---
tag: Q07R6W
kind: problem
slug: small-parsimony
name: Small parsimony problem
aliases:
- weighted small parsimony
area: biology/phylogenetics
level: core
summary: For a fixed tree with a state at each leaf, label the internal nodes so that the total cost of the changes along the edges is least.
prereqs: [phylogenetic-tree, tree-dynamic-programming]
see_also: [fitch-algorithm, sankoff-algorithm, hartigan-algorithm, maximum-parsimony, wagner-parsimony, camin-sokal-parsimony, dollo-parsimony, ancestral-sequence-reconstruction]
sources:
  - paper: doi:10.2307/2412116
    title: Walter M. Fitch, Toward defining the course of evolution, minimum change for a specific tree topology, Systematic Zoology 20(4), 1971, 406-416
    locator: the problem of the least number of changes on a given topology, and its solution for unit costs on a binary tree
  - paper: doi:10.1137/0128004
    title: David Sankoff, Minimal mutation trees of sequences, SIAM Journal on Applied Mathematics 28(1), 1975, 35-42
    locator: the labeling of the internal nodes of a given tree with sequences, for a general cost between letters
  - paper: doi:10.1007/BF01681346
    title: David Sankoff and Pascale Rousseau, Locating the vertices of a Steiner tree in an arbitrary metric space, Mathematical Programming 9, 1975, 240-246
    locator: the dynamic program over the tree for one character in a metric space
  - book: isbn:9780262101066
    title: Neil C. Jones and Pavel A. Pevzner, An Introduction to Bioinformatics Algorithms, MIT Press, 2004
    locator: Section 10.10, Small Parsimony Problem
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 2, Counting evolutionary changes
---

The small parsimony problem takes a [phylogenetic tree](/phylogenetic-tree/) whose shape is fixed and whose leaves carry observed states, for example the letters of one column of an alignment. It asks for states at the internal nodes such that the total cost of the changes along the edges is as small as possible. That least cost is the parsimony score of the tree. The problem is the inner step of [maximum parsimony](/maximum-parsimony/), which also searches over the trees. Small parsimony is easy: a [dynamic program over the tree](/tree-dynamic-programming/) solves it in time linear in the number of nodes. [Fitch's algorithm](/fitch-algorithm/) does this for unit costs on binary trees, [Hartigan's algorithm](/hartigan-algorithm/) for unit costs on trees of any degree, and the [Sankoff algorithm](/sankoff-algorithm/) for any cost table.

## In plain words

You have a family tree of species, and you know a trait of each living species at the tips, for example which letter it has at one position of a gene. You do not know the trait of the ancestors at the inner points of the tree. Each time the trait differs between a parent and its child, you count one change, or a cost that depends on the two traits.

Guess the ancestors so that the count is as small as possible. The best count tells how well the tree explains the data with few changes. The guesses at the inner points are a reconstruction of the ancestors.

Only the inner points are free, and the shape of the tree is given. This makes the problem easy. When the shape is also free, the problem is the hard one, maximum parsimony.

## Definition

**Input.** A rooted tree $T$ with leaf set $L$ and internal node set $I$, a finite set $\Sigma$ of $k$ states, a leaf labeling $x : L \to \Sigma$, and a cost $\delta : \Sigma \times \Sigma \to \mathbb{R}_{\ge 0} \cup \{\infty\}$ with $\delta(a, a) = 0$. The value $\delta(a, b)$ is the cost of a change from state $a$ in a parent to state $b$ in its child.

**Labeling.** A labeling is a map $\lambda : L \cup I \to \Sigma$ with $\lambda(\ell) = x(\ell)$ for each leaf $\ell$. Its cost is

$$\operatorname{cost}(\lambda) = \sum_{(u, v) \in E(T)} \delta(\lambda(u), \lambda(v)),$$

where each edge $(u, v)$ goes from the parent $u$ to the child $v$.

**Output.** The parsimony score $\operatorname{PS}(T, x) = \min_\lambda \operatorname{cost}(\lambda)$, and a labeling $\lambda$ that reaches it. Such a labeling is a most parsimonious reconstruction. Some versions ask for all of them, or for the set of states that each node takes in at least one of them.

**Sequences.** For aligned sequences of length $m$ at the leaves, the sites are independent: the cost of a labeling by sequences is the sum of the costs of its $m$ columns, so $\operatorname{PS}$ is the sum of $m$ one-site scores. Only one site is treated below.

**Unrooted trees.** If $\delta$ is symmetric, the cost does not depend on the direction of the edges. So the score of an unrooted tree is the score of the same tree rooted at any of its nodes. A root put inside an edge $(u, v)$ adds a node $r$ with $\delta(\lambda(r), \lambda(u)) + \delta(\lambda(r), \lambda(v)) \ge \delta(\lambda(u), \lambda(v))$ when $\delta$ obeys the [triangle inequality](/triangle-inequality/), with equality for $\lambda(r) = \lambda(u)$, so this root does not change the score either.

## Variants

- **Unit costs (Fitch parsimony).** $\delta(a, b) = 1$ for $a \ne b$. The score is the least number of changes. This is the version that [Fitch's algorithm](/fitch-algorithm/) solves on binary trees.
- **Weighted (Sankoff parsimony).** A general table $\delta$, for example a higher cost for transversions than for transitions in DNA. The [Sankoff algorithm](/sankoff-algorithm/) solves it.
- **Ordered characters.** The states are $0, 1, \ldots, k - 1$ and $\delta(i, j) = |i - j|$: [Wagner parsimony](/wagner-parsimony/).
- **Irreversible characters.** The root has the ancestral state 0, and only changes $i \to j$ with $j > i$ are allowed: [Camin-Sokal parsimony](/camin-sokal-parsimony/).
- **Single gain.** The derived state arises at most once, and it can be lost many times: [Dollo parsimony](/dollo-parsimony/).
- **Known root state.** Some versions fix the state of the root. This is the same as an extra edge above the root, from a node with the fixed state.
- **All reconstructions.** Count or list all most parsimonious labelings, or give each node its set of optimal states. [Hartigan's algorithm](/hartigan-algorithm/) gives these sets for unit costs.
- **Sequences with insertions and deletions.** If the leaves carry unaligned sequences and the internal nodes may carry any sequences, with the edit distance as the cost of an edge, the problem is called tree alignment. It is NP-hard, unlike the versions above, because the columns are no longer fixed (Wang and Jiang 1994, see [NP-hardness of multiple sequence alignment](/msa-np-hardness/)).

## Examples

**Unit costs.** Take the rooted binary tree $((t_1, t_2), (t_3, (t_4, t_5)))$ with the leaf states A, C, C, G, A. Name the internal nodes $u = (t_1, t_2)$, $w = (t_4, t_5)$, $v = (t_3, w)$ and the root $r = (u, v)$. Label every internal node A. The changes are on the edges to $t_2$, to $t_3$ and to $t_4$, so the cost is 3. A check of all $4^4 = 256$ labelings of the four internal nodes shows that no labeling costs less. Exactly 4 labelings of $(r, u, v, w)$ cost 3: (A, A, A, A), and (C, C, C, $s$) for $s \in \{$A, C, G$\}$. So the score is 3, and the optimal states are $\{$A, C$\}$ at $r$, $u$ and $v$, and $\{$A, C, G$\}$ at $w$.

**Weighted costs.** On the same tree, take the leaf states A, C, T, G, A, with cost 1 for a transition (A and G, or C and T) and cost 2 for a transversion. The labeling with A at every internal node costs $2 + 2 + 1 = 5$, for the edges to $t_2$, $t_3$ and $t_4$. The [Sankoff algorithm](/sankoff-algorithm/) shows that 5 is the least, and that this labeling is the only optimal one.

**Unrooted.** The same tree without its root is the unrooted tree with the splits $t_1 t_2 \mid t_3 t_4 t_5$ and $t_1 t_2 t_3 \mid t_4 t_5$. Its score for the first site is 3 for every choice of the root, as the definition says.

## Known algorithms

| algorithm | costs | tree | time per site |
|---|---|---|---|
| [Fitch](/fitch-algorithm/) (1971) | unit | rooted binary | $O(nk)$, or $O(n)$ with bit sets |
| [Hartigan](/hartigan-algorithm/) (1973) | unit | rooted, any degree | $O(nk)$ |
| [Sankoff](/sankoff-algorithm/) (1975) | any table $\delta$ | rooted, any degree | $O(nk^2)$ |
| interval pass of [Wagner parsimony](/wagner-parsimony/) (Farris 1970) | $\lvert i - j \rvert$ | rooted binary | $O(n)$ |
| clade count of [Camin-Sokal parsimony](/camin-sokal-parsimony/) | irreversible, two states | rooted | $O(n)$ |

Here $n$ is the number of nodes and $k$ the number of states. All of them are dynamic programs over the tree. The first pass goes from the leaves to the root and finds the score. The second pass goes from the root to the leaves and picks states. For $m$ sites, multiply by $m$.

## Bounds

- **Linear time.** For a fixed number of states, the problem takes $\Theta(n)$ time per site. Each leaf must be read, and Fitch's algorithm does $O(1)$ work per node when the sets fit in a machine word. For $m$ sites this is $\Theta(mn)$.
- **Score bounds.** If the leaves of a site show $r$ distinct states, every tree has a score of at least $r - 1$ under unit costs, since each state other than the root state must arise on some edge. A star tree with the most frequent state at the center reaches $n_L - f$, where $n_L$ is the number of leaves and $f$ the count of the most frequent state, and no tree has a higher score. See [parsimony-informative site](/parsimony-informative-site/) for when the score depends on the tree.
- **Number of reconstructions.** A site can have many most parsimonious labelings. Counting them is a dynamic program of the same shape: for each node $v$ and state $a$, store the number of optimal labelings of the subtree of $v$ with $v$ in state $a$, and multiply over the children the sums over the states that reach the minimum.

## Reductions

- **To a Steiner problem.** If $\delta$ is a metric, small parsimony on sequences is the [Steiner tree problem](/steiner-tree-problem/) in the space of sequences with the summed per-site distance, with the shape of the tree fixed. Sankoff and Rousseau (1975) showed that this fixed-shape version is solved one coordinate at a time by the dynamic program.
- **Unit and ordered costs to the weighted case.** Fitch parsimony is Sankoff parsimony with the unit table, and Wagner parsimony is Sankoff parsimony with $\delta(i, j) = |i - j|$. Camin-Sokal parsimony is Sankoff parsimony with $\delta(i, j) = \infty$ for $j < i$ and a fixed root state.
- **To large parsimony.** Maximum parsimony is the minimum of the small parsimony score over all trees on the taxa. This outer minimum makes it NP-hard ([NP-hardness of maximum parsimony](/maximum-parsimony-np-hard/)), while the inner problem stays linear.
- **Probabilistic analogue.** The [Felsenstein pruning algorithm](/felsenstein-pruning/) has the same two-pass shape, with sums of probabilities in place of minimums of costs. Fitch's and Sankoff's passes are its min-plus form.

## Applications

- **Scoring trees in a parsimony search.** Each tree that a heuristic such as [stepwise addition](/stepwise-addition/) or [nearest-neighbor interchange](/nearest-neighbor-interchange/) visits is scored by small parsimony over all sites.
- **Ancestral states.** The optimal labels are a reconstruction of the ancestral sequences ([ancestral sequence reconstruction](/ancestral-sequence-reconstruction/)), used to place changes on the branches of a tree.
- **Character mapping.** Biologists map a trait, such as the gain of a body part, onto a known tree and count how often it changed.
- **Starting values.** The number of changes on each branch of the best labeling gives rough branch lengths for later fits by [maximum likelihood](/maximum-likelihood-phylogeny/).

## References
