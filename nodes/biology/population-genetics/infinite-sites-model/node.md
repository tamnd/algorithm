---
tag: F4PWHX
kind: model
slug: infinite-sites-model
name: Infinite sites model
aliases:
- Kimura infinite sites model
area: biology/population-genetics
level: core
summary: A mutation model with so many sites that each mutation hits a new site, so every segregating site has two alleles and a unique origin.
history:
  year: 1969
  people: [Motoo Kimura]
  note: Kimura introduced the model in 1969 to count the heterozygous nucleotide sites that a steady flux of mutations keeps in a finite population.
prereqs: [kingman-coalescent, coalescent-theory]
see_also: [infinite-alleles-model, four-gamete-condition, perfect-phylogeny, site-frequency-spectrum, watterson-estimator, nucleotide-diversity, coalescent-simulation, jukes-cantor-model]
sources:
  - paper: doi:10.1093/genetics/61.4.893
    title: Motoo Kimura, The number of heterozygous nucleotide sites maintained in a finite population due to steady flux of mutations, Genetics 61(4), 1969
    locator: pp. 893-903 (the model of a locus with so many sites that each new mutation hits a site that is not yet segregating)
  - paper: doi:10.1016/0040-5809(75)90020-9
    title: G. A. Watterson, On the number of segregating sites in genetical models without recombination, Theoretical Population Biology 7(2), 1975
    locator: pp. 256-276 (the distribution of the number of segregating sites, its mean theta a_n and its variance)
  - paper: doi:10.1093/genetics/105.2.437
    title: Fumio Tajima, Evolutionary relationship of DNA sequences in finite populations, Genetics 105(2), 1983
    locator: pp. 437-460 (the mean and the variance of the number of pairwise differences under the infinite-sites model)
  - paper: doi:10.1006/tpbi.1995.1025
    title: Yun-Xin Fu, Statistical properties of segregating sites, Theoretical Population Biology 48(2), 1995
    locator: pp. 172-197 (the expected number of sites with i derived copies, theta / i)
  - book: isbn:9780974707754
    title: John Wakeley, Coalescent Theory, An Introduction, Roberts and Company, 2009
    locator: Chapter 4 (neutral genetic variation under the infinite-sites model)
---

The infinite sites model is a model of mutation in a DNA region that has so many sites, and so few mutations per site, that every new mutation falls on a site where no earlier mutation is still present in the population. Each segregating site then has exactly two alleles, the ancestral one and the derived one, and all copies of the derived allele descend from one mutation. Kimura introduced it in 1969. Together with the [Kingman coalescent](/kingman-coalescent/) it is the standard null model of [coalescent theory](/coalescent-theory/) for DNA polymorphism, and the estimators and tests on [Watterson's estimator](/watterson-estimator/), [nucleotide diversity](/nucleotide-diversity/), the [site frequency spectrum](/site-frequency-spectrum/) and [Tajima's D](/tajimas-d/) all assume it.

## The machine

**The state.** A sample of $n$ sequences (gene copies) from one locus. The data is a binary matrix $H$ with $n$ rows and $S$ columns: one column per segregating site, with 0 for the ancestral allele and 1 for the derived allele. Sites that do not vary in the sample are not stored.

**The parameters.** $N$ is the number of diploid individuals, so the population has $2N$ gene copies. $\mu$ is the mutation rate of the whole locus per gene copy per generation. The population mutation rate is $\theta = 4N\mu$ (for a haploid population of $N$ copies, $\theta = 2N\mu$). The model does not use the number of sites $m$ or the rate per site, only their product $\mu$, because it is the limit $m \to \infty$ with $\mu$ fixed.

**The rules.** Time runs backward in units of $2N$ generations. The genealogy of the sample is a Kingman coalescent tree: while $k$ lineages remain, they merge at rate $k(k-1)/2$. Given the tree, mutations fall on each branch as a Poisson process with rate $\theta/2$ per unit of time, independently on different branches. Each mutation creates a new segregating site. A mutation on a branch above exactly $i$ of the sampled copies gives a column of $H$ with $i$ ones.

**The standing assumptions.** Neutral mutations; a constant population size; random mating; no population structure; no recombination inside the locus (one tree for all sites); the ancestral allele at each site is known. A version with recombination puts the mutations on the local trees of the [ancestral recombination graph](/ancestral-recombination-graph/) instead of on one tree.

**A small sample.** Take $n = 5$ sequences with $S = 6$ segregating sites:

| copy | s1 | s2 | s3 | s4 | s5 | s6 |
|---|---|---|---|---|---|---|
| 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| 2 | 1 | 0 | 0 | 0 | 0 | 0 |
| 3 | 0 | 1 | 0 | 1 | 0 | 0 |
| 4 | 0 | 0 | 1 | 1 | 0 | 0 |
| 5 | 0 | 0 | 1 | 1 | 1 | 0 |

The sets of copies that carry the derived allele are $\{1,2\}$, $\{3\}$, $\{4,5\}$, $\{3,4,5\}$, $\{5\}$ and $\{1\}$. Any two of these sets are either disjoint or nested, so the six mutations fit on one rooted tree, $((1,2),(3,(4,5)))$, with one mutation per branch that they label. This is what the model predicts for every data set without recombination.

## What it counts

- $S$, the number of segregating sites in the sample. Given the tree, $S$ is Poisson with mean $\theta L/2$, where $L$ is the total branch length.
- The [site frequency spectrum](/site-frequency-spectrum/) $\xi_1, \ldots, \xi_{n-1}$, where $\xi_i$ is the number of sites with $i$ derived copies. In the example, $\xi = (3, 2, 1, 0)$.
- The number of pairwise differences $d_{jk}$ between two copies $j$ and $k$, and their mean over the $\binom{n}{2}$ pairs, which is [nucleotide diversity](/nucleotide-diversity/) per locus. In the example the mean is $30/10 = 3$.
- The number of distinct haplotypes (rows of $H$). Without recombination it follows the [Ewens sampling formula](/ewens-sampling-formula/), because the model then is an [infinite alleles model](/infinite-alleles-model/) at the level of whole haplotypes.
- The joint pattern of the columns: which pairs of sites show all four gametes 00, 01, 10 and 11.

## Relation to other models

- **[Infinite alleles model](/infinite-alleles-model/).** It records only whether two copies carry the same allele. The infinite sites model records which sites differ, so it keeps more information: the sizes of the differences and the nesting of the mutations. Without recombination, the haplotypes of the infinite sites model follow the infinite alleles model with the same $\theta$.
- **Finite sites models.** A [substitution model](/substitution-model/) such as [Jukes-Cantor](/jukes-cantor-model/) lets a site mutate many times, with back mutations and more than two alleles. The infinite sites model is the limit of a finite sites model with $m$ sites and rate $\mu/m$ per site as $m \to \infty$.
- **[Perfect phylogeny](/perfect-phylogeny/) and the [four-gamete condition](/four-gamete-condition/).** Without recombination, every pair of columns of $H$ fails to show all four gametes, so $H$ has a perfect phylogeny. A pair that shows all four gametes proves, under this model, that recombination (or gene conversion) happened between the two sites. Under a finite sites model, the same pattern can also come from a repeat mutation.
- **[Coalescent simulation](/coalescent-simulation/).** Hudson's algorithm samples data from this model: a Kingman tree, then Poisson mutations on its branches.

## Known results in the model

Write $a_n = \sum_{i=1}^{n-1} 1/i$ and $b_n = \sum_{i=1}^{n-1} 1/i^2$. Each result holds for $n \ge 2$, under the assumptions above.

**Segregating sites (Watterson 1975).** $E[S] = \theta a_n$ and $\operatorname{Var}[S] = \theta a_n + \theta^2 b_n$. The proof is on the [Kingman coalescent](/kingman-coalescent/) page: given the tree, $S$ is Poisson with mean $\theta L / 2$, and $E[L] = 2 a_n$, $\operatorname{Var}[L] = 4 b_n$. For $n = 10$ and $\theta = 5$: $a_{10} = 2.828968$, $b_{10} = 1.539768$, so $E[S] = 14.1448$ and $\operatorname{Var}[S] = 52.6390$. [Watterson's estimator](/watterson-estimator/) $S / a_n$ is unbiased for $\theta$.

**Two sequences.** For $n = 2$, $P(S = k) = \frac{1}{1 + \theta} \left(\frac{\theta}{1 + \theta}\right)^k$ for $k = 0, 1, 2, \ldots$, a geometric law.

*Proof.* With two lineages, the coalescence happens at rate 1 and mutations happen at rate $\theta/2$ on each of the two branches, so at total rate $\theta$. Going back in time, the next event is a mutation with probability $\theta / (1 + \theta)$ and the coalescence with probability $1 / (1 + \theta)$, by the race of independent exponential clocks. The process has no memory, so $S = k$ means $k$ mutation events followed by the coalescence. $\square$

For $\theta = 1$ this gives $P(S = k) = 1/2^{k+1}$: $1/2, 1/4, 1/8, \ldots$, with mean $1 = \theta a_2$.

**Mean pairwise difference (Tajima 1983).** For two copies, $E[d_{jk}] = \theta$, because their total branch length has mean $2 \cdot 1 = 2$ (two branches of mean length $E[T_2] = 1$) and the mutations fall at rate $\theta/2$. So the mean over all pairs is also unbiased for $\theta$. The variance is on the [nucleotide diversity](/nucleotide-diversity/) page.

**The frequency spectrum (Fu 1995).** $E[\xi_i] = \theta / i$ for $i = 1, \ldots, n-1$. The proof is on the [site frequency spectrum](/site-frequency-spectrum/) page. Rare variants are the most common class. For $n = 4$, the expected number of singletons is $\theta$, more than the $5\theta/6$ of the two other classes together. The expected fraction of singletons among all sites is $1 / a_n$, which is $0.353$ for $n = 10$.

**Compatibility.** Without recombination, every pair of sites is compatible (no four gametes). The sets of copies that carry each derived allele are then pairwise disjoint or nested, and they are the clusters of one rooted tree, with one mutation on each branch that a column labels. Branches that carry no mutation do not show in $H$, so the tree is only partly resolved. Gusfield's algorithm builds it in $O(n S)$ time; see [perfect phylogeny](/perfect-phylogeny/).

**When the approximation fails.** The model is a limit. With $m$ real sites and $S$ mutations placed uniformly, the probability that no two mutations share a site is $\prod_{j=0}^{S-1} (1 - j/m) \approx e^{-S(S-1)/(2m)}$, the birthday problem. For $S = 50$ and $m = 1000$ this is $0.288$, so a repeat hit is likely; for $S = 50$ and $m = 10000$ it is $0.885$. Mutation rates also vary between sites (CpG sites mutate faster in mammals), which makes repeat hits more likely than this uniform estimate. Data from fast-evolving viruses, from distant species, or from hypermutable sites often break the model; there, a finite sites model is the right one.

## References
