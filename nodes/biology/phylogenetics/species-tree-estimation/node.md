---
tag: M34RQ8
kind: problem
slug: species-tree-estimation
name: Species tree estimation
aliases:
- species tree inference from gene trees
- species tree inference
area: biology/phylogenetics
level: research
summary: Infer the tree of species from many loci whose gene trees disagree. Methods are judged by statistical consistency under the multispecies coalescent.
prereqs: [multispecies-coalescent, phylogenetic-tree-reconstruction]
see_also: [astral, incomplete-lineage-sorting, maximum-quartet-consistency, maximum-rooted-triplet-consistency, supertree, tree-reconciliation, bayesian-phylogenetic-inference, maximum-likelihood-phylogeny]
sources:
  - paper: doi:10.1093/sysbio/46.3.523
    title: Wayne P. Maddison, Gene trees in species trees, Systematic Biology 46(3), 1997
    locator: pp. 523-536 (causes of gene tree discordance, and the minimize deep coalescence criterion)
  - paper: doi:10.1080/10635150601146041
    title: Laura Salter Kubatko and James H. Degnan, Inconsistency of phylogenetic estimates from concatenated data under coalescence, Systematic Biology 56(1), 2007
    locator: pp. 17-24 (concatenated maximum likelihood can converge to a wrong species tree)
  - paper: doi:10.1016/j.tpb.2014.12.005
    title: Sebastien Roch and Mike Steel, Likelihood-based tree reconstruction on a concatenation of aligned sequence data sets can be statistically inconsistent, Theoretical Population Biology 100, 2015
    locator: pp. 56-62 (a proof that maximum likelihood on concatenated loci is inconsistent under the multispecies coalescent)
  - paper: doi:10.1186/1471-2148-10-302
    title: Liang Liu, Lili Yu and Scott V. Edwards, A maximum pseudo-likelihood approach for estimating species trees under the coalescent model, BMC Evolutionary Biology 10, 2010
    locator: article 302 (MP-EST, a pseudo-likelihood of rooted triplets of gene trees)
  - paper: doi:10.1093/bioinformatics/btu530
    title: Julia Chifman and Laura Kubatko, Quartet inference from SNP data under the coalescent model, Bioinformatics 30(23), 2014
    locator: pp. 3317-3324 (SVDquartets, quartets from site pattern frequencies)
  - paper: doi:10.1093/molbev/msp274
    title: Joseph Heled and Alexei J. Drummond, Bayesian inference of species trees from multilocus data, Molecular Biology and Evolution 27(3), 2010
    locator: pp. 570-580 (*BEAST, joint Bayesian inference of gene trees and the species tree)
  - paper: doi:10.1093/bioinformatics/btu462
    title: Siavash Mirarab, Rezwana Reaz, Md. Shamsuzzoha Bayzid, Théo Zimmermann, M. Shel Swenson and Tandy Warnow, ASTRAL, genome-scale coalescent-based species tree estimation, Bioinformatics 30(17), 2014
    locator: pp. i541-i548 (a quartet-based summary method, consistent under the multispecies coalescent)
---

Species tree estimation asks for the tree of a set of species from data at many loci, each of which has its own gene tree. Gene trees disagree with each other and with the species tree because of [incomplete lineage sorting](/incomplete-lineage-sorting/), gene duplication and loss, [horizontal gene transfer](/horizontal-gene-transfer/), and estimation error. Under the [multispecies coalescent](/multispecies-coalescent/), the central question is which methods are *statistically consistent*: they return the true species tree with probability tending to $1$ as the number of loci grows. Concatenating all loci into one alignment is not consistent (Kubatko and Degnan 2007; Roch and Steel 2015), while summary methods that combine rooted triplets or unrooted quartets of the gene trees, such as [ASTRAL](/astral/), are.

## In plain words

Each gene in a genome has its own family tree. Because genes are passed down in populations, and not one copy per species, those trees often differ from the true tree of the species and from each other.

The task is to find the species tree from many genes. One easy way is to join all the genes into one long sequence and build one tree from it. With enough disagreement between genes, this can give the wrong tree, and adding more genes does not fix it.

Better methods first build a tree for each gene and then ask, for each small group of species, which shape most genes support. For groups of three or four species, the most common shape is the true one, so these votes point to the right tree when there are enough genes.

## Definition

**Input.** A set $X$ of $n$ species and data for $k$ loci: either sequence alignments, or gene trees estimated from them. A locus may have several copies per species, or miss some species.

**Model.** Given the species tree $S$ with branch lengths in coalescent units, the gene trees are independent draws from the multispecies coalescent, and the sequences evolve along them under a [substitution model](/substitution-model/).

**Output.** The topology of $S$, and often its branch lengths in coalescent units and a root.

**Criterion.** An estimator $\hat S_k$ is statistically consistent if $\Pr(\hat S_k = S) \to 1$ as $k \to \infty$ for every species tree $S$ and every choice of branch lengths.

## Variants

- **From gene trees (summary methods).** The input is $k$ estimated gene tree topologies. ASTRAL, MP-EST and NJst are examples.
- **From sequences, jointly.** The gene trees are not fixed but integrated out, as in Bayesian co-estimation.
- **From sites.** Each site is an independent draw of a gene tree and a site pattern, for unlinked SNPs. SVDquartets works this way.
- **With multiple individuals per species**, which improves the estimates of short branches near the tips.
- **With gene families.** Loci with paralogs need a model of duplication and loss as well, or a method that scores gene trees with several copies, as in [tree reconciliation](/tree-reconciliation/).
- **With networks.** If hybridization is part of the history, the output is a network instead of a tree.

## Examples

**Three species.** With species tree $((A, B), C)$ and an inner branch of $T = 0.5$ coalescent units, the rooted gene tree $((A, B), C)$ has probability $1 - \tfrac{2}{3} e^{-0.5} \approx 0.596$, and each of the other two has probability $\tfrac{1}{3} e^{-0.5} \approx 0.202$. With $100$ loci, the expected counts are about $60$, $20$ and $20$, and a majority vote over gene trees picks the species tree with high probability.

**A short branch needs many loci.** The gap between the matching and the other frequencies is $1 - e^{-T}$, which is about $T$ for a short branch. For $T = 0.1$ the frequencies are about $0.397$ and $0.302$, so a few hundred loci are needed before the majority is reliable.

**Why concatenation can fail.** For four or more species with short inner branches, the most common rooted gene tree can differ from the species tree. A concatenated analysis fits one tree to all sites, so it follows the sites of the discordant loci when they are the majority, and more loci only make it more certain of the wrong tree.

## Known algorithms

| method | input | idea | consistent under the MSC |
|---|---|---|---|
| concatenation | alignments | one [maximum likelihood tree](/maximum-likelihood-phylogeny/) on the joined alignment | no |
| minimize deep coalescence (Maddison 1997) | gene trees | species tree with the fewest extra lineages in branches | not in general |
| majority rooted triplets | rooted gene trees | the most frequent triplet for each three species, then assemble | yes |
| MP-EST (Liu, Yu and Edwards 2010) | rooted gene trees | maximize a pseudo-likelihood of the triplet counts | yes |
| NJst and STAR | gene trees | average distances between taxa over gene trees, then [neighbor joining](/neighbor-joining/) | yes |
| ASTRAL (Mirarab et al. 2014) | unrooted gene trees | maximize quartet support over a constrained set of bipartitions | yes |
| SVDquartets (Chifman and Kubatko 2014) | site patterns | rank of a flattening matrix per quartet, then assemble | yes |
| *BEAST, StarBEAST (Heled and Drummond 2010) | alignments | MCMC over gene trees and the species tree together | yes, under the model |

Assembling quartets or triplets into one tree is itself a [supertree](/supertree/) problem. Maximizing the number of agreeing quartets is [maximum quartet consistency](/maximum-quartet-consistency/) with weights, and maximizing agreeing triplets is [maximum rooted triplet consistency](/maximum-rooted-triplet-consistency/).

## Bounds

- **Concatenation is inconsistent.** There are species trees on which maximum likelihood on concatenated data converges to a wrong topology as $k \to \infty$ (Kubatko and Degnan 2007; Roch and Steel 2015).
- **Majority gene tree is inconsistent** for four or more species, because of anomalous gene trees.
- **Quartet and triplet summaries are consistent**, because for each three species the matching rooted triplet, and for each four species the matching unrooted quartet, is the strict most probable gene tree.
- **The quartet objective is NP-hard** in general, so consistent quartet methods either search a constrained space exactly, as ASTRAL does, or use heuristics.
- **Loci needed.** For a species tree with shortest inner branch $f$ in coalescent units, the number of loci needed for a fixed error probability grows as $f$ shrinks, about as $1/f^2$ for small $f$ on three species.

## Reductions

- **To weighted maximum quartet consistency.** Weight each quartet topology by the number of gene trees that induce it. The best species tree for this weight is the ASTRAL objective.
- **To rooted triplet consistency.** With rooted gene trees, weighting each rooted triplet by its gene tree count gives a triplet version.
- **To distance methods.** Average internode distances of the gene trees form a matrix whose neighbor joining tree is consistent, which reduces the problem to [phylogenetic tree reconstruction](/phylogenetic-tree-reconstruction/) from distances.

## Applications

- **Phylogenomics.** Trees of birds, mammals, plants and insects from thousands of genes, where rapid radiations give short branches and much discordance.
- **Species delimitation.** Deciding whether populations are separate species uses the same model with population sizes and divergence times.
- **Dating and diversification.** A species tree is the input of [divergence time estimation](/divergence-time-estimation/) and of studies of speciation rates.
- **Comparative methods.** Trait analyses such as [independent contrasts](/phylogenetic-independent-contrasts/) need the species tree, not a gene tree, as the shared history of the species.

## References
