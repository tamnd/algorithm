---
tag: 9J75HR
kind: algorithm
slug: felsenstein-pruning
name: Felsenstein's pruning algorithm
aliases:
- tree-pruning algorithm
- Felsenstein's algorithm
- pruning algorithm
area: biology/phylogenetics
level: core
summary: Computes the likelihood of a tree for one site in O(n k^2) time. A postorder pass gives each node the probability of the leaves below it for each of its k states.
model: real-ram
complexity:
  vars: {n: the number of nodes of the tree, k: the number of states, m: the number of distinct site patterns}
  time: {worst: Θ(m n k^2), average: Θ(m n k^2), best: Θ(m n k^2)}
  space: {extra: Θ(n k)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1981
  people: [Joseph Felsenstein]
  note: Felsenstein gave the pruning computation of the likelihood of a tree from DNA sequences in 1981, after using the same idea for discrete characters in 1973.
prereqs: [phylogenetic-likelihood, postorder-traversal, tree-dynamic-programming]
see_also: [sankoff-algorithm, substitution-model, maximum-likelihood-phylogeny, ancestral-sequence-reconstruction, forward-backward-algorithm, variable-elimination, belief-propagation, log-sum-exp-trick]
sources:
  - paper: doi:10.1007/BF01734359
    title: Joseph Felsenstein, Evolutionary trees from DNA sequences, a maximum likelihood approach, Journal of Molecular Evolution 17 (1981)
    locator: pp. 368 to 376 (the pruning computation of the likelihood, the pulley principle, and the tree search)
  - book: isbn:9780199602612
    title: Ziheng Yang, Molecular Evolution, A Statistical Approach, Oxford University Press, 2014
    locator: Chapter 4, Section 4.2.2 (the pruning algorithm) and Section 4.2.3 (time reversibility and the root of the tree)
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 16, Likelihood methods (computing the likelihood of a tree)
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 8, Probabilistic approaches to phylogeny (Felsenstein's algorithm for the likelihood)
---

Felsenstein's pruning algorithm computes the [phylogenetic likelihood](/phylogenetic-likelihood/) of a tree. The definition of the likelihood of one site sums over all states of the $(n - 1)/2$ internal nodes of a rooted binary tree with $n$ nodes, which is $k^{(n-1)/2}$ terms for $k$ states. The pruning algorithm visits the nodes in [postorder](/postorder-traversal/) and gives each node $v$ a vector $L_v$ of $k$ *partial likelihoods*: $L_v(a)$ is the probability of the leaf states below $v$, given state $a$ at $v$. A node's vector is a product over its children of one matrix-vector product per child, so one site costs $\Theta(n k^2)$ time. It is [dynamic programming on a tree](/tree-dynamic-programming/), and it has the same shape as the [Sankoff algorithm](/sankoff-algorithm/) with (min, +) replaced by (+, ×). Every likelihood and Bayesian phylogenetics program runs it at its core.

## In plain words

You know the letters at the tips of a tree and want the chance of seeing them, but you do not know the letters at the inner points. Listing every possible choice of inner letters is hopeless: each new inner point multiplies the number of choices by four, so even a tree of fifty tips has far too many.

So work from the tips upward. For each inner point, keep a small table with one entry per letter. The entry says: if this point had this letter, how likely is everything we see below it? A tip's table is simple: 1 for its own letter, 0 for the others. A parent builds its table from its children's tables and the change chances on the branches to them. At the top, mix the top table with how common each letter is, and you have the answer. Each point is handled once.

## The problem

**Input.** A rooted tree $T$ with $n$ nodes, a state $x_\ell \in \{1, \ldots, k\}$ at each leaf $\ell$ (or a mark that it is unknown), for each non-root node $w$ a $k \times k$ matrix $P_w$, where $P_w(a, b)$ is the probability of state $b$ at $w$ given state $a$ at its parent, and a root distribution $\pi$. For a substitution model, $P_w = e^{Q t_w}$ with $t_w$ the length of the branch above $w$.

**Output.** The site likelihood

$$L = \sum_{\text{internal states}} \pi_{a_\rho} \prod_{\text{edges } (u, w)} P_w(a_u, a_w),$$

where the sum is over all assignments of states to the internal nodes, the leaves keep their observed states, and $\rho$ is the root. For an alignment, the log-likelihood is the sum of $\ln L$ over the sites. If $Q$ is reversible and $\pi$ is its stationary distribution, the root can be any node, and the result is the likelihood of the unrooted tree.

## The algorithm

For a node $v$ and a state $a$, let $L_v(a)$ be the sum, over the states of the internal nodes strictly below $v$, of the product of $P_w(a_u, a_w)$ over the edges below $v$, with $a_v = a$. Once $v$ has a state, the subtrees of its children have no common variable, so the sum of the products splits:

$$L_v(a) = \prod_{w \text{ child of } v} \; \sum_{b=1}^{k} P_w(a, b)\, L_w(b).$$

```pseudo id=main
PRUNE(T, P, π, x)
L1  for each node v of T in postorder do
L2      if v is a leaf with a known state then L_v(a) ← 1 if a = x_v, else 0, for each state a
L3      else if v is a leaf with an unknown state then L_v(a) ← 1 for each state a
L4      else for each state a do
L5          L_v(a) ← product over the children w of v of (sum over b of P_w(a, b) · L_w(b))
L6  return sum over a of π_a · L_root(a)
```

Line L5 reads only the vectors of the children, which the postorder has already filled. The sum inside line L5 is the *message* $M_w(a) = (P_w L_w)(a)$ from $w$ to its parent: the probability of the leaves below $w$ given state $a$ at the parent. Line L6 averages the root vector over the root distribution.

## Example

Take the tree $((1{:}0.1, 2{:}0.2)u{:}0.1, (3{:}0.1, 4{:}0.3)w{:}0.2)r$ under [JC69](/jukes-cantor-model/), where the number after each node is the length of the branch above it, and the site A, C, A, A at the leaves 1 to 4. The states are in the order A, C, G, T. The JC69 entries for the three branch lengths are

| $t$ | $P(a, a)$ | $P(a, b)$, $b \ne a$ |
|---|---|---|
| 0.1 | 0.906380 | 0.031207 |
| 0.2 | 0.824446 | 0.058518 |
| 0.3 | 0.752740 | 0.082420 |

The leaf vectors are unit vectors: $L_1 = L_3 = L_4 = (1, 0, 0, 0)$ and $L_2 = (0, 1, 0, 0)$. So the message from a leaf with state $c$ is the column $c$ of its matrix. Line L5 gives:

| node | message from first child | message from second child | $L_v$ |
|---|---|---|---|
| $u$ | (0.906380, 0.031207, 0.031207, 0.031207) | (0.058518, 0.824446, 0.058518, 0.058518) | (0.0530395, 0.0257282, 0.00182615, 0.00182615) |
| $w$ | (0.906380, 0.031207, 0.031207, 0.031207) | (0.752740, 0.082420, 0.082420, 0.082420) | (0.682269, 0.00257205, 0.00257205, 0.00257205) |
| $r$ | (0.0489908, 0.0250887, 0.00417025, 0.00417025) | (0.562945, 0.0423465, 0.0423465, 0.0423465) | (0.0275791, 0.00106242, 0.000176595, 0.000176595) |

For example, $L_u(\text{A}) = 0.906380 \times 0.058518 = 0.0530395$: leaf 1 keeps A and leaf 2 changes to C. The message from $u$ to $r$ in state A is $0.906380 \times 0.0530395 + 0.031207 \times (0.0257282 + 2 \times 0.00182615) = 0.0489908$. At the root, line L6 gives

$$L = \tfrac14 (0.0275791 + 0.00106242 + 0.000176595 + 0.000176595) = 0.00724868.$$

The brute-force sum over the $4^3 = 64$ states of $u$, $w$ and $r$ gives the same number. Since JC69 is reversible, rooting the tree at $u$ with a branch of length $0.3$ from $u$ to $w$ also gives $0.00724868$.

## Correctness

Fix a node $v$ and a state $a$, and let $S_v(a)$ be the sum, over all assignments of the internal nodes strictly below $v$ with $v$ in state $a$, of the product of the matrix entries on the edges of the subtree of $v$. By induction in postorder, line L5 stores $S_v(a)$. At a leaf the subtree has no edges, and the indicator of line L2 is the empty product for the observed state and 0 for the others (line L3 sums over the unknown state). At an internal node, an assignment below $v$ is an independent choice of a state $b_w$ for each child $w$ and of an assignment below $w$. So the sum of products is a product over the children of the separate sums, each of which is $\sum_b P_w(a, b) S_w(b)$ by distributivity. At the root, every assignment of the internal nodes is a root state $a$ and an assignment below the root, so the sum in the definition of $L$ is $\sum_a \pi_a S_{\text{root}}(a)$. The proof uses only the distributive law, so it holds for any matrices, stochastic or not. The full proof is below.

## Complexity

- **Time.** Line L5 does, for each child $w$ of $v$, $k$ dot products of length $k$. Each non-root node is the child of exactly one node, so one site costs $\Theta((n - 1) k^2) = \Theta(n k^2)$ in every case, against $k^{(n-1)/2}$ terms for the direct sum on a binary tree. An alignment with $m$ distinct site patterns costs $\Theta(m n k^2)$, plus the time to find the patterns. For DNA $k = 4$, for amino acids $k = 20$, and for codons $k = 61$, where the $k^2$ factor dominates.
- **Matrices.** The matrices $P_w = e^{Q t_w}$ are shared by all sites. Computing them costs $O(k^3)$ per branch from an eigen decomposition of $Q$, done one time per $Q$, which is small next to the site work when $m$ is large.
- **Space.** One site needs $\Theta(n k)$ numbers. Programs keep all $\Theta(m n k)$ partial likelihoods, so that a change of one branch length needs only the vectors on the path to the root.
- **Special models.** For [F81](/felsenstein-81-model/) and JC69, $P_w v = e^{-\mu t} v + (1 - e^{-\mu t}) (\pi \cdot v) \mathbf 1$, so each message costs $O(k)$ and a site costs $O(n k)$.

## Properties

- **Exact.** In exact arithmetic it returns the sum of the definition. The implementation tests run it on fractions and compare with the brute-force sum.
- **Deterministic and not recursive.** One postorder pass with an explicit stack; no choices.
- **Any degree.** A node may have any number of children, including one.
- **Any matrices.** The proof does not use that the rows of $P_w$ sum to 1, so the same code sums any product of edge weights over the labelings of a tree. With $P_w(a, b) = e^{-\delta(a, b)}$ it sums $e^{-\text{cost}}$ over all labelings, a smooth version of the [Sankoff](/sankoff-algorithm/) score.
- **Root.** For a reversible model with $\pi$ stationary, the result is the same for every root node and every root position on an edge, by the pulley principle on the [likelihood](/phylogenetic-likelihood/) page.
- **Partial likelihoods.** $L_v(a)$ is the probability of the leaves below $v$ given state $a$ at $v$, so $\pi_a L_{\text{root}}(a) / L$ is the posterior probability of state $a$ at the root. A second, downward pass gives the posterior at every node ([ancestral sequence reconstruction](/ancestral-sequence-reconstruction/)).

## Variants and improvements

- **Scaling against underflow.** On a tree with hundreds of taxa, $L$ is far below the smallest double (about $10^{-308}$). Programs divide each $L_v$ by its largest entry and add the logarithm of that factor to a running sum, or work in log space with the [log-sum-exp trick](/log-sum-exp-trick/). The test of the implementation uses a caterpillar tree with 500 leaves whose exact log-likelihood is below $-745$: the plain product gives 0.0, and the scaled version matches the exact value.
- **Site patterns.** Sites with the same pattern give the same $L$. Compressing the alignment into patterns with weights cuts the work, by large factors for alignments of close taxa.
- **Rate classes.** With [rate heterogeneity](/rate-heterogeneity/), run the pass once per rate class with the scaled matrices and average the root results, at $K$ times the cost.
- **Upward and downward vectors.** A second pass from the root down gives, for each edge, the vector of the rest of the tree. Then the likelihood as a function of the length of one edge is $\sum_{a, b} \mathrm{Out}(a) P(a, b; t) L(b)$, and its first and second derivatives in $t$ are cheap. [Newton-Raphson](/newton-raphson-method/) steps on one branch at a time use this in [maximum likelihood](/maximum-likelihood-phylogeny/) programs.
- **Local updates.** After a tree rearrangement such as [NNI](/nearest-neighbor-interchange/) or [SPR](/subtree-prune-and-regraft/), only the vectors on the changed paths need new values.
- **Graphical models.** The algorithm is the sum-product algorithm, or [variable elimination](/variable-elimination/) in postorder, on a tree-shaped Bayesian network; [belief propagation](/belief-propagation/) on a tree gives all the marginals with the downward pass. On a path it is the forward algorithm of a [hidden Markov model](/hidden-markov-model/).

## When to use it

Use it whenever the likelihood of a fixed tree under a Markov model of characters is needed: to score trees in [maximum likelihood phylogeny](/maximum-likelihood-phylogeny/), inside the Markov chain of [Bayesian phylogenetic inference](/bayesian-phylogenetic-inference/), to place new sequences on a tree in [phylogenetic placement](/phylogenetic-placement/), and to fit the parameters of a [substitution model](/substitution-model/). For the most parsimonious labeling instead of a probability, use the [Sankoff algorithm](/sankoff-algorithm/) or [Fitch's algorithm](/fitch-algorithm/).

## Pitfalls

- **Underflow.** Without scaling, a large tree gives a likelihood of exactly 0 and a log-likelihood of $-\infty$. Scale, or work in logs.
- **Direction of the matrix.** Line L5 must use $P_w(a, b)$ with $a$ the parent state and $b$ the child state. For a reversible model with uniform $\pi$ the matrix is symmetric and the mistake is invisible; with unequal frequencies it gives wrong values.
- **Missing data.** An unknown leaf state is a vector of ones, not of zeros. A vector of zeros makes the likelihood 0.
- **The root distribution.** Line L6 must use $\pi$ as the root distribution for the pulley principle to hold. With another root distribution, or a non-reversible $Q$, the result depends on the root.
- **Negative probabilities.** Small negative entries of $e^{Qt}$ from rounding in the eigen decomposition, at tiny $t$, can make $L$ negative. Clip them, or use the symmetric form of a reversible $Q$.

## Implementations

## History

Felsenstein described the computation of the likelihood of a tree, summing over the states of the internal nodes from the tips up, for discrete characters in 1973, and he gave it for DNA sequences under a substitution model in his 1981 paper in the Journal of Molecular Evolution, where he called it pruning. The same idea appeared earlier in human genetics as the peeling method of Elston and Stewart (1971) for the likelihood of a pedigree, and it was later recognized as a case of the sum-product algorithm on graphical models. Today the pruning algorithm runs inside PhyML, RAxML, IQ-TREE, MrBayes, BEAST and the BEAGLE library, which ports it to graphics processors.

## References
