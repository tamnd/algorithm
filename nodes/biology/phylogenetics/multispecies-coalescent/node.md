---
tag: PX7YZ9
kind: model
slug: multispecies-coalescent
name: Multispecies coalescent
aliases:
- MSC
- multispecies coalescent model
area: biology/phylogenetics
level: research
summary: The Kingman coalescent run backward in time inside each branch of a species tree. It gives the distribution of gene trees for a given species tree.
history:
  year: 1988
  people: [Pekka Pamilo, Masatoshi Nei]
  note: Pamilo and Nei computed the probability that a gene tree differs from the species tree under the coalescent in 1988; Rannala and Yang gave the full gene tree density in 2003.
prereqs: [kingman-coalescent, phylogenetic-tree]
see_also: [incomplete-lineage-sorting, species-tree-estimation, astral, coalescent-theory, ancestral-recombination-graph, duplication-loss-model, bayesian-phylogenetic-inference, quartet]
sources:
  - paper: doi:10.1093/oxfordjournals.molbev.a040517
    title: Pekka Pamilo and Masatoshi Nei, Relationships between gene trees and species trees, Molecular Biology and Evolution 5(5), 1988
    locator: pp. 568-583 (the probability that a gene tree matches the species tree, for three and four species)
  - paper: doi:10.1093/genetics/164.4.1645
    title: Bruce Rannala and Ziheng Yang, Bayes estimation of species divergence times and ancestral population sizes using DNA sequences from multiple loci, Genetics 164(4), 2003
    locator: pp. 1645-1656 (the density of a gene tree with coalescent times in a species tree, and Bayesian estimation of divergence times and population sizes)
  - paper: doi:10.1111/j.0014-3820.2005.tb00891.x
    title: James H. Degnan and Laura A. Salter, Gene tree distributions under the coalescent process, Evolution 59(1), 2005
    locator: pp. 24-37 (the probability of each gene tree topology given the species tree)
  - paper: doi:10.1016/j.tree.2009.01.009
    title: James H. Degnan and Noah A. Rosenberg, Gene tree discordance, phylogenetic inference and the multispecies coalescent, Trends in Ecology and Evolution 24(6), 2009
    locator: pp. 332-340 (a review of the model and its consequences for inference)
  - paper: doi:10.1007/s00285-010-0355-7
    title: Elizabeth S. Allman, James H. Degnan and John A. Rhodes, Identifying the rooted species tree from the distribution of unrooted gene trees under the coalescent, Journal of Mathematical Biology 62(6), 2011
    locator: pp. 833-862 (the most probable unrooted quartet gene tree matches the species tree, and identifiability)
  - paper: doi:10.1080/10635150601146041
    title: Laura Salter Kubatko and James H. Degnan, Inconsistency of phylogenetic estimates from concatenated data under coalescence, Systematic Biology 56(1), 2007
    locator: pp. 17-24 (concatenated maximum likelihood can converge to a wrong tree under the model)
---

The multispecies coalescent (MSC) is the standard model of how gene trees vary around a species tree. Each branch of the species tree is a population with its own size. Lineages of a gene, sampled from the present species, are traced backward in time; inside each branch they merge by the [Kingman coalescent](/kingman-coalescent/), and at the top of a branch the lineages that are left pass into the ancestral population, where they can merge with the lineages of the sister species. Because two lineages need not merge in the first population they share, a gene tree can differ from the species tree, which is [incomplete lineage sorting](/incomplete-lineage-sorting/). The model treats different loci as independent draws, and it is the basis of most methods of [species tree estimation](/species-tree-estimation/).

## The machine

**The parameters.** A rooted species tree $S$. Each branch $b$ has a duration $\tau_b$ and a population size $N_b$, or in mutation units a duration in expected substitutions and $\theta_b = 4 N_b u$ for a diploid population with mutation rate $u$ per site per generation. The root branch extends without limit into the past. In *coalescent units*, a branch of $t$ generations in a diploid population of size $N$ has length $t / (2N)$.

**The samples.** For each locus, a number of gene copies from each present species.

**The process, run backward in time.**

1. Place the sampled lineages of each species at the bottom of its leaf branch.
2. In a branch with $j$ lineages, each pair merges at rate $1$ in coalescent units, or $2 / \theta_b$ in mutation units, so the next merge comes after an exponential time with rate $\binom{j}{2}$ in coalescent units.
3. At the top of a non-root branch, stop. The lineages left there enter the parent branch together with those from the sister branch.
4. In the root branch, merge until one lineage is left.

The result is a rooted gene tree with node times. Different loci give independent gene trees given $S$. Sequences then evolve along each gene tree by a [substitution model](/substitution-model/).

## What it counts

- **The density of a gene tree with its coalescent times** (Rannala and Yang 2003). For a branch $b$, let $m_b$ lineages enter at the bottom and $n_b$ leave at the top, with $n_b = 1$ for the root branch. Let $t_{b,j}$ be the time during which branch $b$ has exactly $j$ lineages, for $n_b \le j \le m_b$, up to the top of the branch. Then the density of a gene tree with labeled coalescences and times is

$$f(G, t \mid S) = \prod_b \left(\frac{2}{\theta_b}\right)^{m_b - n_b} \exp\Big(-\sum_{j = n_b}^{m_b} \frac{j (j - 1)}{\theta_b} \, t_{b,j}\Big).$$

Each coalescence of a given pair contributes the rate $2 / \theta_b$, and each interval contributes the probability that no other pair merges.

- **The probability of a gene tree topology.** Integrating the density over times and summing over the ways to place the coalescences in branches gives the probability of each rooted gene tree topology (Degnan and Salter 2005). The number of terms grows fast with the number of taxa.
- **The probability of no coalescence in a branch.** Two lineages in a branch of length $T$ coalescent units fail to merge there with probability $e^{-T}$. With $k$ lineages, the distribution of the number left at the top is given by the Tavaré formula for the lineage-count process of the Kingman coalescent.
- **Sequence divergence between species.** For one lineage from each of two species that split at time $\tau$ (in mutation units), the coalescent time is $\tau$ plus an exponential with mean $\theta / 2$, where $\theta$ is for the ancestral population. So the expected divergence of the two sequences is $2\tau + \theta$, which overestimates the species divergence $2\tau$ by $\theta$.

## Relation to other models

- **Kingman coalescent.** A species tree with one branch is the Kingman coalescent for one population. The MSC glues copies of it together, one per branch, with the lineages at the top of each branch as the input to the next.
- **Coalescent with recombination.** The MSC assumes no recombination inside a locus and free recombination between loci. The [ancestral recombination graph](/ancestral-recombination-graph/) models linked sites with recombination.
- **Duplication and loss.** The [duplication-loss model](/duplication-loss-model/) explains gene tree discordance by gene copies instead of by deep coalescence. Combined models first grow a locus tree by duplication and loss, then run the coalescent inside it.
- **Networks and migration.** The network MSC lets lineages follow one of two parents at a hybridization node, and isolation-with-migration models let lineages move between populations that exist at the same time.
- **Birth-death trees.** Priors on the species tree itself come from the [Yule model](/yule-model/) or the [birth-death process](/birth-death-process/). Together with the MSC they give the hierarchical models of Bayesian species tree inference.

## Known results in the model

- **Three taxa.** The gene tree that matches the rooted species tree is the most probable one, with the closed form on the [incomplete lineage sorting](/incomplete-lineage-sorting/) page (Pamilo and Nei 1988). So the most frequent rooted triplet over loci gives the species tree on each set of three taxa.
- **Anomalous gene trees.** For four or more taxa, the most probable rooted gene tree topology can differ from the species tree when inner branches are short. This is the anomaly zone, which does not exist for rooted triplets or for unrooted quartets.
- **Unrooted quartets.** For each set of four taxa, the unrooted quartet gene tree that matches the species tree is strictly the most probable (Allman, Degnan and Rhodes 2011). So the unrooted species tree topology is identifiable from the distribution of unrooted gene trees, and with five or more taxa so are the rooted topology and the inner branch lengths in coalescent units. Quartet methods such as [ASTRAL](/astral/) rest on this fact.
- **Branch lengths from frequencies.** If the [quartet](/quartet/) that matches the species tree has frequency $p$, the length of the inner branch in coalescent units is $T = -\ln\big(\tfrac{3}{2}(1 - p)\big)$.
- **Concatenation is not consistent.** Joining all loci into one alignment and fitting one tree by maximum likelihood can converge to a wrong tree as the number of loci grows, for some species trees with short inner branches (Kubatko and Degnan 2007).
- **Bayesian estimation.** With sequence data from many loci, the joint posterior of species divergence times, population sizes and the species tree can be sampled by MCMC, using the Rannala-Yang density as the prior on gene trees.

## References
