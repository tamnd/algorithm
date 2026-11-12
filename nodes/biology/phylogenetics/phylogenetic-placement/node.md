---
tag: YT5XE3
kind: problem
slug: phylogenetic-placement
name: Phylogenetic placement
aliases:
- query placement
area: biology/phylogenetics
level: research
summary: Given a fixed reference tree with branch lengths and a new aligned sequence, find the edge, the point on it and the pendant length that maximize the likelihood of the tree with the query added.
prereqs: [phylogenetic-likelihood, felsenstein-pruning]
see_also: [stepwise-addition, maximum-likelihood-phylogeny, subtree-prune-and-regraft, bayesian-phylogenetic-inference, jukes-cantor-model, phylogenetic-tree-reconstruction, fitch-algorithm, phylogenetic-diversity]
sources:
  - paper: doi:10.1186/1471-2105-11-538
    title: Frederick A. Matsen, Robin B. Kodner and E. Virginia Armbrust, pplacer, linear time maximum-likelihood and Bayesian phylogenetic placement of sequences onto a fixed reference tree, BMC Bioinformatics 11, 2010, 538
    locator: the precomputed partial likelihoods on both sides of every edge, the likelihood weight ratio, and the posterior probability of a placement
  - paper: doi:10.1093/sysbio/syr010
    title: Simon A. Berger, Denis Krompass and Alexandros Stamatakis, Performance, accuracy, and web server for evolutionary placement of short sequence reads under maximum likelihood, Systematic Biology 60(3), 2011, 291-302
    locator: the evolutionary placement algorithm in RAxML, with a fast prescoring of all edges and a full optimization on the best ones
  - paper: doi:10.1007/BF01734359
    title: Joseph Felsenstein, Evolutionary trees from DNA sequences, a maximum likelihood approach, Journal of Molecular Evolution 17(6), 1981, 368-376
    locator: the pruning algorithm, and the pulley principle that lets the root be put at any point of a tree under a reversible model
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 16, Likelihood methods, the computation of the likelihood and the pulley principle
---

Phylogenetic placement adds a new sequence, the query, to a reference tree that is already known, without changing the tree. The reference is an unrooted binary [phylogenetic tree](/phylogenetic-tree/) on $n$ taxa with fixed branch lengths and an alignment of their sequences. A placement cuts one of the $2n - 3$ edges at a point and hangs the query from that point by a new pendant edge. The problem asks for the placement of highest [likelihood](/phylogenetic-likelihood/). It is one step of [stepwise addition](/stepwise-addition/) with the tree held fixed, and it is the core of pplacer (Matsen, Kodner and Armbrust 2010) and of the evolutionary placement algorithm EPA (Berger, Krompass and Stamatakis 2011). With the partial likelihoods on both sides of every edge computed once, each candidate placement costs $O(m)$ for $m$ sites, so one query takes time linear in the size of the tree.

## In plain words

You have a trusted tree of known species, and a new sequence, perhaps a short read from a soil sample. You want to know where it belongs on the tree, but you do not want to rebuild the tree.

So you try each branch of the tree in turn. For each branch, you imagine the new sequence joined at a point on it, and you ask how probable the data are with it there. The branch with the highest probability is the answer. The scores of all branches also tell you how sure to be: if two branches score almost the same, the read could belong to either one.

The trick that makes this fast is to do the hard work once for the tree, and then reuse it for every branch and every new sequence.

## Definition

**Input.** An unrooted binary reference tree $T$ on taxa $1, \ldots, n$ with branch lengths $t_e > 0$; aligned sequences of length $m$ for the taxa; a query sequence $q$ of length $m$, aligned to them; and a time-reversible substitution model with stationary distribution $\pi$, such as the [Jukes-Cantor model](/jukes-cantor-model/). The sites are independent.

**Placement.** A placement is a triple $(e, a, p)$ where $e = \{u, v\}$ is an edge, $0 \le a \le t_e$ is the distance of the attachment point from $u$, and $p \ge 0$ is the pendant length. The tree $T_{e,a,p}$ on $n + 1$ taxa replaces $e$ by a new vertex $x$ joined to $u$ by length $a$, to $v$ by length $t_e - a$, and to a new leaf $q$ by length $p$.

**Problem.** Find a placement that maximizes $L(T_{e,a,p})$, the likelihood of the $n + 1$ sequences. Also report, for each edge $e$, the best likelihood $L_e = \max_{a, p} L(T_{e,a,p})$ and the likelihood weight ratio
$$w_e = \frac{L_e}{\sum_f L_f},$$
which sums to 1 over the $2n - 3$ edges.

The full search for a tree on $n + 1$ taxa is a heuristic over $(2(n+1)-5)!!$ trees, and finding the best one is [NP-hard](/ml-tree-np-hard/). Placement holds the reference fixed, so there are only $2n - 3$ edges to try, and the problem is easy apart from the numerical optimization of $a$ and $p$ on each edge.

**Theorem (the edge formula).** Let $D_v$ be the vector of partial likelihoods at $v$ of the subtree on the $v$ side of $e$, with entries $D_v(y) = P(\text{leaf states on the } v \text{ side} \mid v \text{ in state } y)$, and $D_u$ the same for the $u$ side. Then, for one site,
$$L(T_{e,a,p}) = \sum_{y} \pi_y \,\bigl[P(t_e - a) D_v\bigr]_y \,\bigl[P(a) D_u\bigr]_y \,\bigl[P(p)\, \mathbf e_{q}\bigr]_y,$$
where $P(t)$ is the transition matrix and $\mathbf e_q$ is the indicator vector of the query state.

*Proof.* The model is reversible, so the likelihood of $T_{e,a,p}$ does not change when the tree is rooted at any vertex, by Felsenstein's pulley principle. Root it at $x$ with state $y$ drawn from $\pi$. Given the state of $x$, the three subtrees below $x$ evolve independently. The $v$ side is reached through an edge of length $t_e - a$, so its probability given $x = y$ is $\sum_z P_{yz}(t_e - a) D_v(z) = [P(t_e - a) D_v]_y$. The same holds for the $u$ side with length $a$, and for the leaf $q$ with length $p$. Multiply and sum over $y$. $\blacksquare$

The vectors $D_u$ and $D_v$ do not depend on $a$, $p$ or the query. For all $2(2n-3)$ directed edges they can be computed in one $O(nm)$ pass for DNA, each from the two directed edges behind it. This is the precomputation of pplacer and EPA.

```pseudo id=main
PLACE(T, lengths, D, q, fractions, pendants)
L1  for each directed edge (u, v), compute the partial vectors of the v side at every site
L2  for each edge {u, v} of length t do
L3      for each f in fractions and each p in pendants do
L4          ℓ ← log of the edge formula with a = f t, summed over the m sites
L5          if ℓ is the best so far on this edge then keep (ℓ, f t, p)
L6      best[{u, v}] ← the kept triple
L7  return best
```

With $g$ grid points per edge, the cost is $O(nm)$ for line L1 and $O(nmg)$ for the loops, for $n$ taxa, $m$ sites and DNA, in the worst case. The code tests the edge formula against a brute-force sum over all internal states of $T_{e,a,p}$, and against a fresh pruning pass on the $(n+1)$-taxon tree for every edge and grid point, for $n = 5$, 7 and 9.

## Variants

- **Optimized position and pendant.** Replace the grid by a numerical optimization of $a$ and $p$ on each edge, for example by Newton steps on the log likelihood. The function need not be concave, so the result is a local optimum.
- **Bayesian placement.** Put priors on $a$ and $p$ and integrate them out, which gives a posterior probability for each edge. pplacer offers both this and the likelihood weight ratio.
- **Many queries.** The precomputation of line L1 is shared by all queries, so $k$ queries cost $O(nm + knmg)$. The queries are placed one at a time and do not affect each other.
- **Parsimony placement.** Use the parsimony length instead of the likelihood. With the Fitch sets of both sides of every edge, the extra length of a placement is the number of sites where the query state is not in the root set of that edge, as on the [stepwise addition](/stepwise-addition/) page.
- **Distance placement.** Place by a distance criterion on the leaf-to-query distances, without a full likelihood.
- **Prescoring.** EPA scores all edges by a fast approximation and fully optimizes only the best ones.

## Examples

**Seven edges, one query.** The reference tree is $((A,B),C,(D,E))$ with internal vertices $x$ (joined to A and B), $y$ (joined to C) and $z$ (joined to D and E), and every branch of length 0.1. The model is JC69. The sequences are A = AAAAAAAAAA, B = AAAAAAAAAC, C = AAAACCCCCC, D = GGGGTTTTTT and E = GGGTTTTTTT, and the query is GGGGTTTTTC. Each placement first takes the midpoint of the edge and pendant length 0.05.

| edge | log likelihood | likelihood weight ratio |
|---|---|---|
| D to $z$ | -75.149 | 0.747 |
| E to $z$ | -76.453 | 0.203 |
| $y$ to $z$ | -77.846 | 0.050 |
| $x$ to $y$ | -93.706 | less than $10^{-7}$ |
| C to $y$ | -93.858 | less than $10^{-7}$ |
| B to $x$ | -106.281 | less than $10^{-11}$ |
| A to $x$ | -107.034 | less than $10^{-11}$ |

The query differs from D only at the last site, so D's edge wins. With the grid $f \in \{0.25, 0.5, 0.75\}$ and $p \in \{0.01, 0.05, 0.2\}$, D's edge improves to $-75.131$ at distance 0.025 from D with $p = 0.05$, and its weight falls to 0.477. The edge from $y$ to $z$ rises to $-75.570$ at distance 0.025 from $z$ with $p = 0.01$, weight 0.308, and E's edge has 0.215. The best single edge stays the same, but the weights show that the query sits near $z$ and that the data cannot tell well which of the three edges around $z$ holds it.

**A query equal to a reference sequence.** If the query is a copy of D, the best placement is on D's edge, and the test checks this.

## Known algorithms

- **Brute force.** For each edge and each candidate $(a, p)$, build $T_{e,a,p}$ and run [Felsenstein pruning](/felsenstein-pruning/) on $n + 1$ taxa. This costs $O(nm)$ per candidate and $O(n^2 m g)$ per query.
- **Precomputed partials.** PLACE above: one pass over all directed edges, then $O(m)$ per candidate by the edge formula. This is the method of pplacer and EPA, $O(nm + nmg)$ per query.
- **Prescoring heuristics.** EPA and its successors score every edge by a cheap pass and then optimize the branch lengths only on a few top edges, which makes the cost per query smaller in practice.

## Bounds

Brute force gives $O(n^2 m g)$ per query, and the precomputed partials give $O(nm + nmg)$. Any exact method must in the worst case read all $nm$ characters of the reference alignment, because each one can change which edge is best, so $\Omega(nm)$ time is needed for the first query. The precomputation is $\Theta(nm)$ space for DNA, which holds two vectors per edge per site.

## Reductions

- **Stepwise addition.** One step of [stepwise addition](/stepwise-addition/) is a placement of the next taxon on the current tree. Placement keeps the tree fixed for every query, so placing queries one after another is not the same as building a tree.
- **SPR regraft.** Pruning one leaf and placing it back is an [SPR](/subtree-prune-and-regraft/) move of that leaf. Placement scores all regraft points of the leaf.
- **Tree building.** Placing all taxa does not solve [tree reconstruction](/phylogenetic-tree-reconstruction/): the full problem must also choose the reference tree.

## Applications

- **Metagenomics.** Place short reads from an environmental sample, such as 16S rRNA reads, on a reference tree of known organisms, to see which groups are present. Measures such as [phylogenetic diversity](/phylogenetic-diversity/) can then be computed on the placements.
- **Updating large trees.** Add new sequences to a large tree, such as a tree of virus genomes in an outbreak, without a new full search.
- **Classification.** Assign a sequence to the taxon of the clade that holds its best placement, with the weight ratios as a measure of confidence.

## References
