---
tag: W29D9B
kind: concept
slug: incomplete-lineage-sorting
name: Incomplete lineage sorting
aliases:
- deep coalescence
area: biology/phylogenetics
level: advanced
summary: Gene lineages that do not coalesce in the ancestral population of two species can give a gene tree that differs from the species tree.
prereqs: [kingman-coalescent, rooted-triplet]
see_also: [multispecies-coalescent, species-tree-estimation, astral, coalescent-theory, quartet, horizontal-gene-transfer, tree-reconciliation, phylogenetic-network]
sources:
  - paper: doi:10.1093/oxfordjournals.molbev.a040517
    title: Pekka Pamilo and Masatoshi Nei, Relationships between gene trees and species trees, Molecular Biology and Evolution 5(5), 1988
    locator: pp. 568-583 (the probability 1 - (2/3) exp(-T) that the gene tree of three species matches the species tree)
  - paper: doi:10.1093/sysbio/46.3.523
    title: Wayne P. Maddison, Gene trees in species trees, Systematic Biology 46(3), 1997
    locator: pp. 523-536 (lineage sorting as a cause of discordance, and deep coalescence)
  - paper: doi:10.1371/journal.pgen.0020068
    title: James H. Degnan and Noah A. Rosenberg, Discordance of species trees with their most likely gene trees, PLoS Genetics 2(5), 2006
    locator: e68 (the anomaly zone, and the bound a(x) for four taxa)
  - paper: doi:10.1007/s00285-010-0355-7
    title: Elizabeth S. Allman, James H. Degnan and John A. Rhodes, Identifying the rooted species tree from the distribution of unrooted gene trees under the coalescent, Journal of Mathematical Biology 62(6), 2011
    locator: pp. 833-862 (unrooted quartet gene trees have no anomaly)
  - paper: doi:10.1038/nature10842
    title: Aylwyn Scally et al., Insights into hominid evolution from the gorilla genome sequence, Nature 483, 2012
    locator: pp. 169-175 (about 30% of the genome with a gene tree that differs from the species tree of human, chimpanzee and gorilla)
---

Incomplete lineage sorting (ILS) happens when the gene copies of two species do not find their common ancestor in the population that was ancestral to just these two species. The lineages then pass into an older population, where they can coalesce with a lineage of a third species first, and the gene tree differs from the species tree. It is the main source of gene tree discordance under the [multispecies coalescent](/multispecies-coalescent/), and it is most common when the branches of the species tree are short compared with the population size. With three species the gene tree that matches the species tree is always the most probable, but with four or more species there can be *anomalous* gene trees that are more probable than the matching one.

## In plain words

A species carries many versions of each gene at the same time. When a species splits in two, both new species start with this mix of versions.

Follow one gene back in time from two related species. The two copies can only meet in a common ancestor before the split, in the old shared population. If that population lived for only a short time, or was large, the copies may not meet there. They go back into an even older population, together with the copy from a third species, and then any two of the three can meet first.

So the family tree of one gene can put a species with a more distant relative. Different genes give different trees, and the true tree of the species is hidden behind them.

## The idea

**Three species.** Take the species tree $((A,B),C)$ and one gene copy from each species. Let $T$ be the length of the branch from the split of $A$ and $B$ back to the split of $AB$ and $C$, in coalescent units ($T = t / 2N_e$ for a branch of $t$ generations in a diploid population of effective size $N_e$). The copies from $A$ and $B$ enter the ancestral branch at the split of $A$ and $B$. By the [Kingman coalescent](/kingman-coalescent/), they coalesce in it with probability $1 - e^{-T}$, and then the gene tree is $((A,B),C)$. With probability $e^{-T}$ they do not, and three lineages enter the population ancestral to all three species. There, the first pair to coalesce is uniform among the three pairs. So

$$P\big(((A,B),C)\big) = 1 - \tfrac{2}{3} e^{-T}, \qquad P\big(((A,C),B)\big) = P\big(((B,C),A)\big) = \tfrac{1}{3} e^{-T}.$$

These are the formulas of Pamilo and Nei (1988). The matching [rooted triplet](/rooted-triplet/) has probability larger than $1/3$ for every $T > 0$, and the two others are equally likely.

**What makes it common.** The probability of discordance depends only on $T$, the branch length in units of $2N_e$ generations. A branch of one million years gives much discordance in a species with a large population and a long generation time, and little in a small one. Rapid radiations, with many splits close in time, have many short branches and much discordance.

**Deep coalescence without a wrong topology.** Even when the gene tree matches, the two copies coalesce before the split of their species, never after it. So gene divergence times are older than species divergence times, and a clock on gene trees overestimates the ages of splits.

**The anomaly zone.** With four or more species, the most probable gene tree can differ from the species tree. Degnan and Rosenberg (2006) found the exact condition for the four-taxon caterpillar species tree $(((A,B),C),D)$. Let $y$ be the length of the branch above the split of $A$ and $B$, and $x$ the length of the branch above the split of $AB$ and $C$. The symmetric gene tree $((A,B),(C,D))$ is more probable than the matching tree exactly when $y < a(x)$, with

$$a(x) = \log\left[\frac{2}{3} + \frac{3 e^{2x} - 2}{18\,(e^{3x} - e^{2x})}\right].$$

The reason: when the two short branches see few coalescences, most of the history happens in the root population. There, each balanced labeled tree has two rankings and each caterpillar has one, so $((A,B),(C,D))$ is twice as likely as $(((A,B),C),D)$, as in the [Yule](/yule-model/) law. They also showed that for four taxa only the caterpillar has an anomaly zone, and that for five or more taxa every species tree shape has one.

**Triplets and quartets have no anomaly.** For rooted triplets, the three-taxon formula shows that the matching tree is always the most probable. Allman, Degnan and Rhodes (2011) proved the same for unrooted [quartets](/quartet/): for a quartet with internal branch length $t$ in the species tree, the matching unrooted gene quartet has probability $1 - \frac{2}{3} e^{-t}$, and each other one has $\frac{1}{3} e^{-t}$. So the most frequent gene triplet or quartet points to the species tree, while the most frequent whole gene tree may not. This is why [species tree estimation](/species-tree-estimation/) methods such as [ASTRAL](/astral/) work with quartets or triplets.

**Telling ILS from other causes.** [Horizontal gene transfer](/horizontal-gene-transfer/), gene duplication and loss, and errors in the gene trees also give discordant gene trees. Under ILS alone, the two minority triplet topologies have the same frequency. An excess of one of them points to gene flow between the species. Duplication and loss are handled by [reconciliation](/tree-reconciliation/), and some methods model several causes at once, or use a [phylogenetic network](/phylogenetic-network/) for gene flow.

## Examples

**Three species, by branch length.**

| $T$ (units of $2N_e$ generations) | $P$(matching) | $P$(each other tree) | $P$(discordant) |
|---|---|---|---|
| 0.1 | 0.397 | 0.302 | 0.603 |
| 0.5 | 0.596 | 0.202 | 0.404 |
| 1 | 0.755 | 0.123 | 0.245 |
| 2 | 0.910 | 0.045 | 0.090 |

At $T = 0.1$ the matching tree is only a little more frequent than each other tree. A study that counts gene trees then needs many genes to find the species tree.

**Generations.** A diploid ancestral population with $N_e = 100{,}000$ and a branch of $100{,}000$ generations gives $T = 100{,}000 / 200{,}000 = 0.5$. About $40\%$ of independent genes then have a gene tree that differs from the species tree.

**Human, chimpanzee and gorilla.** Scally et al. (2012) found that in about $30\%$ of the genome, gorilla is closer to human or to chimpanzee than these two are to each other. Under the three-taxon formula, $\frac{2}{3} e^{-T} = 0.3$ gives $T \approx 0.80$ units for the branch ancestral to human and chimpanzee.

**An anomalous gene tree.** In the caterpillar $(((A,B),C),D)$ with $y = x = 0.05$, the symmetric gene tree $((A,B),(C,D))$ has probability $0.121$, and the matching gene tree has probability $0.079$. With $y = x = 0.1$ the values are $0.128$ and $0.104$. With equal lengths $y = x$, the caterpillar is in the anomaly zone when the lengths are below about $0.157$. For $x = 0.1$ the bound is $a(0.1) \approx 0.327$, and for $x = 0.2$ it is $a(0.2) \approx 0.080$. For $x$ above about $0.266$, $a(x) < 0$ and no value of $y$ gives an anomaly.

## Where it is used

- **Species tree estimation.** Summary methods ([ASTRAL](/astral/), MP-EST) and site-based methods (SVDquartets) use the triplet and quartet results above to be consistent under ILS.
- **Phylogenomics of rapid radiations.** In birds, mammals, plants and other groups with short internal branches, ILS explains why gene trees from thousands of loci disagree.
- **Population sizes of ancestors.** The fraction of discordant gene trees estimates $T$, so with a dated split it estimates the size of an ancestral population.
- **Tests for gene flow.** The equal frequencies of the minority topologies under ILS are the null hypothesis of tests for introgression.
- **Traits.** A trait that follows a discordant gene tree can look like convergent evolution on the species tree.

## References
