---
tag: 7HPG9Q
kind: problem
slug: haplotype-phasing
name: Haplotype phasing
aliases:
- statistical phasing
- haplotype inference
area: biology/population-genetics
level: core
summary: Infer the two haplotypes of each individual from unphased genotypes, using patterns shared across a population sample.
history:
  year: 1990
  people: [Andrew G. Clark, Laurent Excoffier, Montgomery Slatkin, Matthew Stephens, Peter Donnelly]
  note: "Clark gave a rule that resolves genotypes with haplotypes already seen in 1990. Excoffier and Slatkin estimated haplotype frequencies by EM in 1995, and Stephens, Smith and Donnelly gave the coalescent-based method PHASE in 2001. Later methods use the Li-Stephens model on large samples."
prereqs: [linkage-disequilibrium, hidden-markov-model]
see_also: [em-haplotype-frequency-estimation, li-stephens-model, haplotype-assembly, perfect-phylogeny, positional-burrows-wheeler-transform, genotype-imputation, minimum-error-correction-problem, np-hard]
sources:
  - paper: "Andrew G. Clark, Inference of haplotypes from PCR-amplified samples of diploid populations, Molecular Biology and Evolution 7(2), 1990"
    title: Clark 1990
    locator: pp. 111-122 (the rule that resolves an ambiguous genotype with a known haplotype and its complement)
  - paper: "Laurent Excoffier and Montgomery Slatkin, Maximum-likelihood estimation of molecular haplotype frequencies in a diploid population, Molecular Biology and Evolution 12(5), 1995"
    title: Excoffier and Slatkin 1995
    locator: pp. 921-927 (the EM algorithm for haplotype frequencies under Hardy-Weinberg equilibrium)
  - paper: doi:10.1086/319501
    title: Matthew Stephens, Nicholas J. Smith and Peter Donnelly, A new statistical method for haplotype reconstruction from population data, American Journal of Human Genetics 68(4), 2001
    locator: pp. 978-989 (PHASE, a Gibbs sampler with a coalescent-based conditional distribution of one haplotype given the others)
  - paper: doi:10.1038/nmeth.1785
    title: Olivier Delaneau, Jonathan Marchini and Jean-Francois Zagury, A linear complexity phasing method for thousands of genomes, Nature Methods 9(2), 2012
    locator: pp. 179-181 (SHAPEIT, a Li-Stephens HMM over a graph of haplotype segments, linear in the number of sites and individuals)
  - paper: "Giuseppe Lancia, Maria Cristina Pinotti and Romeo Rizzi, Haplotyping populations by pure parsimony, complexity of exact and approximation algorithms, INFORMS Journal on Computing 16(4), 2004"
    title: Lancia, Pinotti and Rizzi 2004
    locator: pp. 348-359 (pure parsimony haplotyping is APX-hard)
---

Haplotype phasing takes the genotypes of diploid individuals, which give at each site the two alleles of an individual but not which chromosome copy carries which, and finds the two haplotypes of each individual. A genotype with $s$ heterozygous sites is consistent with $2^{s - 1}$ pairs of haplotypes, and the data of one individual cannot choose among them. Phasing uses the fact that individuals in a population share haplotypes over long stretches, because of [linkage disequilibrium](/linkage-disequilibrium/). Under the pure parsimony objective, which asks for the fewest distinct haplotypes, the problem is NP-hard. In practice it is solved by statistical methods, and the methods in wide use are [hidden Markov models](/hidden-markov-model/) built on the [Li-Stephens model](/li-stephens-model/). Phasing from a population sample differs from [haplotype assembly](/haplotype-assembly/), which phases one individual from its sequencing reads.

## In plain words

You carry two copies of each chromosome, one from each parent. A standard genotype test tells you, at each position, which two variants you have, but not which copy each one sits on. If you have two different variants at many positions, there are many ways to split them into two copies.

To choose, look at many people at once. Chromosome copies in a population are made of long stretches shared with other people. A split that makes your two copies look like copies that other people carry is more likely to be right. Methods do this by building each person's copies as patchworks of the copies of other people, and by improving all of them in turn.

## Definition

**Input.** Genotypes $g_i \in \{0, 1, 2\}^m$ for individuals $i = 1, \ldots, n$, counting copies of one allele at each of $m$ biallelic sites.

**Phasing.** A phasing gives each individual a pair of haplotypes $h_i, h_i' \in \{0, 1\}^m$ with $h_i + h_i' = g_i$ at every site. At a homozygous site both haplotypes are fixed. At the $s_i$ heterozygous sites one haplotype carries 1 and the other 0, so there are $2^{s_i - 1}$ unordered pairs for $s_i \ge 1$.

**Objectives.**

- **Statistical.** Choose the phasing with the highest probability under a population model, or sample phasings from the posterior. The model is a distribution of haplotype pairs, for example Hardy-Weinberg pairing of haplotypes with unknown frequencies, or a copying model along the genome.
- **Pure parsimony.** Choose a phasing that uses the fewest distinct haplotypes in total.
- **Perfect phylogeny.** Choose a phasing whose $2n$ haplotypes fit a [perfect phylogeny](/perfect-phylogeny/), that is, a tree with no recurrent mutation and no recombination.

**Accuracy.** Against a known truth, the switch error rate is the fraction of pairs of successive heterozygous sites whose relative phase is wrong.

## Variants

- **Population phasing.** Only the genotypes of unrelated individuals are known. This is the main form of the problem.
- **With a reference panel.** Phased haplotypes of other individuals are given, and the genotypes of a new sample are phased against them, often together with [genotype imputation](/genotype-imputation/).
- **Pedigree phasing.** With the genotypes of parents and children, Mendelian rules fix the phase at most sites of a child of a trio.
- **Read-based phasing.** Sequencing reads that cover several heterozygous sites of one individual give their phase directly. This is [haplotype assembly](/haplotype-assembly/), often posed as the [minimum error correction problem](/minimum-error-correction-problem/), and it needs no population data. Methods can combine reads with population information.
- **Short regions.** For a few sites, the frequencies of all haplotypes can be estimated, as in [EM haplotype frequency estimation](/em-haplotype-frequency-estimation/), and each individual is given its most probable pair.

## Examples

Take three individuals at two sites, with genotypes $g_1 = (1, 1)$, $g_2 = (2, 1)$ and $g_3 = (1, 2)$.

- $g_2$ has one heterozygous site, so its phase is fixed: $\{11, 10\}$. In the same way $g_3$ is $\{11, 01\}$.
- $g_1$ has two heterozygous sites, so it is $\{00, 11\}$ or $\{01, 10\}$.
- **Pure parsimony.** With $\{00, 11\}$, the haplotypes used are $00, 11, 10, 01$, four in all. With $\{01, 10\}$, they are $01, 10, 11$, three in all. Pure parsimony picks $\{01, 10\}$.
- **Clark's rule.** Start from the haplotypes of the resolved individuals: $11$, $10$ and $01$. The genotype $g_1$ minus the known haplotype $10$ is $01$, which is also known, so the rule resolves $g_1$ as $\{10, 01\}$, the same answer.

A genotype such as $(1, 1, 2, 1)$ has three heterozygous sites and $2^2 = 4$ possible phasings.

## Known algorithms

- **Clark's rule (1990).** Resolve each ambiguous genotype with a known haplotype and its complement, add the complement to the known set, and repeat. The result depends on the order, and some genotypes may stay unresolved.
- **EM under Hardy-Weinberg equilibrium.** Excoffier and Slatkin (1995) estimate haplotype frequencies by [expectation maximization](/expectation-maximization/), treating the phase as missing data. The cost grows with the number of possible haplotypes, so it suits short regions. See [EM haplotype frequency estimation](/em-haplotype-frequency-estimation/).
- **PHASE.** Stephens, Smith and Donnelly (2001) use a Gibbs sampler that phases one individual at a time, given the current haplotypes of all others, with a conditional distribution from coalescent theory. Later versions add recombination.
- **Li-Stephens HMMs.** Methods such as SHAPEIT, Beagle and Eagle phase each individual with an HMM whose states are pairs of haplotypes to copy from the rest of the sample or from a reference panel, and repeat over individuals. SHAPEIT (Delaneau, Marchini and Zagury 2012) has a cost linear in the number of sites and in the number of individuals per iteration. Large panels use matching with the [positional Burrows-Wheeler transform](/positional-burrows-wheeler-transform/) or similar to keep few states.
- **Pure parsimony.** Exact solutions come from integer linear programming formulations, which work for small inputs.
- **Perfect phylogeny haplotyping.** Gusfield (2002) gave a polynomial-time algorithm, and later work made it linear in the input size.

## Bounds

- **Pure parsimony is hard.** Finding a phasing with the fewest distinct haplotypes is NP-hard, and it is APX-hard, so it has no polynomial-time approximation scheme unless P = NP (Lancia, Pinotti and Rizzi 2004). See [NP-hard](/np-hard/).
- **Perfect phylogeny is easy.** Deciding whether genotypes have a phasing that fits a perfect phylogeny, and finding one, takes polynomial time.
- **Statistical methods.** Their cost per iteration is $O(nmK)$ or similar for $K$ copying states, but they give no guarantee of reaching the most probable phasing, and their accuracy is measured on data with known phase.
- **Information limit.** Two heterozygous sites with no linkage disequilibrium between them, or an individual whose haplotypes are rare in the sample, cannot be phased reliably by any population method.

## Reductions

- **Phasing to HMM decoding.** In the Li-Stephens form, the phase of one individual given the haplotypes of the others is the decoding of an HMM whose state is an ordered pair of copied haplotypes, with emissions that check the sum against the genotype.
- **Pure parsimony to integer programming.** Gusfield's formulation has one variable per candidate haplotype pair of each individual and one per distinct haplotype.
- **Perfect phylogeny haplotyping to graph realization.** Gusfield reduced it to the problem of realizing a graph from a set of paths, which has a near-linear algorithm.
- **Frequency estimation.** Phasing a short region reduces to estimating haplotype frequencies and then choosing the most probable pair for each individual.

## Applications

- **Imputation.** Phased haplotypes of a sample are matched to a reference panel to fill in sites that were not typed; see [genotype imputation](/genotype-imputation/).
- **Local ancestry and shared segments.** [Local ancestry inference](/local-ancestry-inference/) and the search for segments [identical by descent](/identity-by-descent/) work on haplotypes.
- **Selection scans.** Statistics of haplotype length, such as [extended haplotype homozygosity](/extended-haplotype-homozygosity/), need phased data.
- **Clinical genetics.** Whether two damaging variants in one gene are on the same copy or on different copies decides whether a recessive disease is expected.
- **Molecular studies.** Allele-specific expression and effects of variants in cis need the phase of the variants.

## References
