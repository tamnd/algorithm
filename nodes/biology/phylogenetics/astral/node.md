---
tag: AJ00YQ
kind: algorithm
slug: astral
name: ASTRAL
aliases:
- Accurate Species TRee ALgorithm
area: biology/phylogenetics
level: research
summary: Finds the species tree that shares the most quartets with a set of gene trees, by dynamic programming over a set of allowed bipartitions.
solves: [species-tree-estimation]
model: word-ram
complexity:
  vars: {n: the number of species, k: the number of gene trees, x: the number of allowed bipartitions}
  time: {worst: O(n k x^2)}
  space: {extra: O(n k + x)}
history:
  year: 2014
  people: [Siavash Mirarab, Rezwana Reaz, Md. Shamsuzzoha Bayzid, Théo Zimmermann, M. Shel Swenson, Tandy Warnow]
  note: Mirarab and coauthors introduced ASTRAL in 2014 as a statistically consistent summary method that scales to thousands of genes.
prereqs: [species-tree-estimation, maximum-quartet-consistency, bitmask-dp]
see_also: [multispecies-coalescent, quartet, incomplete-lineage-sorting, traceback, splits-of-a-tree, quartet-max-cut, supertree, tree-dynamic-programming]
sources:
  - paper: doi:10.1093/bioinformatics/btu462
    title: Siavash Mirarab, Rezwana Reaz, Md. Shamsuzzoha Bayzid, Théo Zimmermann, M. Shel Swenson and Tandy Warnow, ASTRAL, genome-scale coalescent-based species tree estimation, Bioinformatics 30(17), 2014
    locator: pp. i541-i548 (the quartet objective, the dynamic program over allowed bipartitions, and statistical consistency)
  - paper: doi:10.1093/bioinformatics/btv234
    title: Siavash Mirarab and Tandy Warnow, ASTRAL-II, coalescent-based species tree estimation with many hundreds of taxa and thousands of genes, Bioinformatics 31(12), 2015
    locator: pp. i44-i52 (the weight of a tripartition from gene tree tripartitions, O(nk|X|^2) time, and a larger allowed set)
  - paper: doi:10.1186/s12859-018-2129-y
    title: Chao Zhang, Maryam Rabiee, Erfan Sayyari and Siavash Mirarab, ASTRAL-III, polynomial time species tree reconstruction from partially resolved gene trees, BMC Bioinformatics 19(Suppl. 6), 2018
    locator: article 153 (an allowed set of size linear in nk, polytomies in gene trees, and polynomial running time)
  - paper: doi:10.1007/s00285-010-0355-7
    title: Elizabeth S. Allman, James H. Degnan and John A. Rhodes, Identifying the rooted species tree from the distribution of unrooted gene trees under the coalescent, Journal of Mathematical Biology 62(6), 2011
    locator: pp. 833-862 (the species tree quartet is the most probable unrooted quartet gene tree)
---

ASTRAL estimates a species tree from a set of unrooted gene trees. It returns the unrooted species tree that agrees with the gene trees on the largest number of [quartets](/quartet/), counted over all gene trees and all sets of four species. This is the weighted form of [maximum quartet consistency](/maximum-quartet-consistency/), which is NP-hard in general, so ASTRAL solves it exactly only among trees whose bipartitions come from an allowed set $\mathcal{X}$, by a [dynamic program over sets](/bitmask-dp/) of taxa. Under the [multispecies coalescent](/multispecies-coalescent/), the best tree converges to the true species tree as the number of genes grows, even when [incomplete lineage sorting](/incomplete-lineage-sorting/) makes most gene trees disagree with it.

## In plain words

Many genes each give their own family tree of the same species, and these trees often disagree. Look at any four species: each gene tree says which two of the four are closer. When the trees disagree because of how genes are passed down in populations, the right answer for four species is still the most common one.

ASTRAL looks for the single tree that agrees with the genes on as many of these four-species questions as possible. It builds the tree from small groups of species up to the full set. For each group it remembers the best way to split it in two. Only groups that appear in the gene trees are tried, which keeps the search fast.

## The problem

**Input.** A taxon set $X$ with $|X| = n$, and $k$ unrooted gene trees on $X$.

**Quartet score.** For an unrooted binary tree $T$ on $X$, let $Q(T)$ be the set of quartet topologies $ab|cd$ that $T$ induces, one for each four taxa. The score is

$$\mathrm{score}(T) = \sum_{i=1}^{k} |Q(T) \cap Q(G_i)|.$$

**Output.** An unrooted binary tree $T$ with every bipartition in a given set $\mathcal{X}$ that maximizes the score. ASTRAL builds $\mathcal{X}$ from the bipartitions of the gene trees, and later versions add more. With $\mathcal{X}$ the set of all bipartitions, this is the unconstrained problem.

**Tripartition weights.** Root $T$ anywhere. An internal node $v$ other than the root splits $X$ into three parts: the clusters $A_1, A_2$ of its two children and the rest $X \setminus (A_1 \cup A_2)$. Define $w(A_1 | A_2 | A_3)$ as the number of pairs (gene tree $G_i$, quartet) such that two taxa of the quartet lie in two different parts, the other two lie in the third part, and $G_i$ puts the first two together. A quartet of $T$ has exactly two such nodes in $T$, the two ends of its inner path. So $\mathrm{score}(T)$ is half the sum of $w$ over the internal nodes.

## The algorithm

```pseudo id=main
ASTRAL(G_1..G_k, X, 𝒳)
L1  for each cluster A, from either side of a bipartition in 𝒳, in order of size do
L2      if |A| = 1 then V(A) ← 0
L3      else V(A) ← max over A = A1 ⊔ A2 with A1, A2 clusters of V(A1) + V(A2) + w(A1 | A2 | X − A)
L4          record the split that gives the maximum
L5  build the tree by following the recorded splits down from X
L6  return the tree and V(X) / 2
```

The weight $w$ in line L3 comes from the gene trees without listing quartets. Each internal node of a gene tree also has a tripartition $(P_1, P_2, P_3)$. Let $I_{ip} = |A_i \cap P_p|$. Then

$$w(A_1 | A_2 | A_3) = \sum_{\text{gene nodes}} \ \sum_{s=1}^{3} \sum_{r=1}^{3} \binom{I_{sr}}{2} \big( I_{ip} I_{jq} + I_{iq} I_{jp} \big),$$

where $\{i, j\} = \{1, 2, 3\} \setminus \{s\}$ and $\{p, q\} = \{1, 2, 3\} \setminus \{r\}$. The term counts quartets with the pair $c, d$ in species part $s$ and gene part $r$, and with $a$, $b$ in the other two parts on both sides. Equal gene tripartitions in different gene trees are counted once, with a multiplicity.

## Example

Five species $A, B, C, D, E$ and three gene trees: $G_1 = ((A, B), C, (D, E))$, $G_2 = ((A, C), B, (D, E))$ and $G_3 = ((A, B), D, (C, E))$. Each gene tree induces $5$ quartets, so the score is at most $15$.

The best tree is $((A, B), C, (D, E))$, with score $11$: it agrees with $G_1$ on all $5$ quartets, and with $G_2$ and $G_3$ on $3$ each. Rooted on the edge of $A$, its internal nodes and weights are:

| node | tripartition | $w$ from $G_1$, $G_2$, $G_3$ | $w$ |
|---|---|---|---|
| $\{B, C, D, E\}$ | $B \mid CDE \mid A$ | $3 + 1 + 3$ | $7$ |
| $\{C, D, E\}$ | $C \mid DE \mid AB$ | $4 + 2 + 2$ | $8$ |
| $\{D, E\}$ | $D \mid E \mid ABC$ | $3 + 3 + 1$ | $7$ |

The sum is $22$ and $V(X) / 2 = 11$. The next best trees are $G_2$ and $G_3$ themselves, with score $9$ each. Here $\mathcal{X}$ from the gene trees has $18$ clusters, and the best tree is among the trees it allows.

## Correctness

Two facts make the dynamic program exact on its search space. First, every quartet of $T$ is counted at exactly the two ends of its inner path, so the score is half the sum of the tripartition weights. Second, the tripartition of a node depends only on its own cluster and its children's clusters, so the best rooted tree on a cluster $A$ is made of best rooted trees on the two parts, and line L3 finds its value by induction on $|A|$. The root of the rooted tree has an empty third part and weight $0$, so $V(X)$ is the sum over the internal nodes of the unrooted tree. Because the set of clusters is closed under complement, rooted trees with allowed clusters are exactly the rootings of unrooted trees with allowed bipartitions. The proof file has the details and the consistency theorem.

**Statistical consistency.** Under the multispecies coalescent, on each four taxa the quartet of the species tree is the most probable unrooted gene quartet (Allman, Degnan and Rhodes 2011). As $k$ grows, $\mathrm{score}(T)/k$ converges to the expected number of quartets that agree, which the species tree maximizes strictly. With $\mathcal{X}$ from the gene trees, every bipartition of the species tree appears in some gene tree with probability tending to $1$. So ASTRAL returns the species tree with probability tending to $1$.

## Complexity

Each cluster $A$ tries at most $|\mathcal{X}|$ splits. For one split, one postorder pass over each gene tree gives the counts $I_{ip}$ at every gene node, so $w$ takes $O(nk)$ time. The implementation uses bitmasks and population counts instead, which is $O(1)$ per count when $n$ fits in a word. So line L3 takes $O(nk |\mathcal{X}|^2)$ time in total, which is the bound of ASTRAL-II (2015). ASTRAL-I (2014) had an extra factor $n$. ASTRAL-III (2018) keeps $|\mathcal{X}| = O(nk)$ and shares work between similar gene trees, for $O((nk)^{1.726} D)$ time, where $D = O(nk)$ is the sum of the degrees of the distinct gene tree nodes. With $\mathcal{X}$ equal to all bipartitions, the number of pairs of a cluster and a subcluster is $3^n$, which gives an exact exponential-time algorithm.

## Properties

- **Missing taxa.** A gene tree on a subset of $X$ contributes only the quartets of the taxa it has, and the weight formula still applies with the parts restricted to those taxa.
- **No branch lengths needed.** Only gene tree topologies enter. Branch lengths of the species tree in coalescent units follow afterward from the quartet frequencies around each branch.
- **Unrooted input and output.** The gene trees and the species tree are unrooted. Rooting needs an outgroup or another method.
- **Ties.** Several trees can have the same score. The traceback returns one of them.

## Variants and improvements

- **ASTRAL-II.** A faster weight computation and a larger $\mathcal{X}$ built by adding bipartitions from similarity matrices and greedy consensus, for better accuracy on hard data.
- **ASTRAL-III.** Handles polytomies in gene trees, so low-support branches can be collapsed before the run, and bounds $|\mathcal{X}|$ to keep the time polynomial in $n$ and $k$.
- **Local branch support.** Posterior probabilities of each species tree branch from the quartet frequencies around it, under the multispecies coalescent.
- **Multi-copy gene families.** Variants score quartets of genes from different species in trees with paralogs, for gene families with duplications.
- **Weighted quartets.** Quartets weighted by gene tree branch support or length reduce the effect of gene tree errors.
- **Other summaries.** The same dynamic program over clusters works for other objectives that are sums over tripartitions, such as rooted triplet scores.

## When to use it

- Many genes, a few hundred species or more, and discordance from incomplete lineage sorting. ASTRAL is often the first species tree method in phylogenomics.
- When estimated gene trees are already available, for example from a maximum likelihood run per gene.
- When a consistent method is needed but full Bayesian co-estimation of gene trees and the species tree is too slow.

## Pitfalls

- **Gene tree error.** ASTRAL treats estimated gene trees as true. Short genes with poorly resolved trees add noise, and collapsing branches with very low support before the run helps.
- **Other causes of discordance.** Consistency holds under the multispecies coalescent. Hidden paralogs, transfers and hybridization violate the model.
- **Search space.** If a bipartition of the true tree is in no gene tree and is not added to $\mathcal{X}$, ASTRAL cannot find it. This matters with few genes or many species.
- **Rooting.** The output is unrooted. Reading it as rooted at an arbitrary place gives wrong clades.
- **Branch lengths.** The branch lengths that ASTRAL reports are in coalescent units, from quartet frequencies, and they are biased short when gene trees have errors.

## Implementations

## History

Mirarab and coauthors introduced ASTRAL in 2014, building on the result of Allman, Degnan and Rhodes (2011) that unrooted quartet gene trees identify the species tree under the multispecies coalescent. ASTRAL-II (Mirarab and Warnow 2015) made the weight computation faster and the search space larger, and ASTRAL-III (Zhang, Rabiee, Sayyari and Mirarab 2018) added polytomies and a polynomial running time. The method became a standard tool of phylogenomic studies with thousands of genes.

## References
