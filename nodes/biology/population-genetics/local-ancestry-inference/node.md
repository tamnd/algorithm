---
tag: PMNM84
kind: problem
slug: local-ancestry-inference
name: Local ancestry inference
aliases:
- admixture mapping of segments
area: biology/population-genetics
level: advanced
summary: Label each segment of an admixed genome with the source population it descends from, usually with an HMM along the chromosome.
history:
  year: 2003
  people: [Daniel Falush, Matthew Stephens, Jonathan K. Pritchard]
  note: "Falush, Stephens and Pritchard let the population of origin change along each chromosome as a Markov chain in 2003. HAPMIX (2009) and RFMix (2013) made the inference fast and accurate with dense SNP data and reference haplotypes."
prereqs: [hidden-markov-model, population-structure-inference, li-stephens-model]
see_also: [forward-backward-algorithm, viterbi-algorithm, pritchard-stephens-donnelly-model, haplotype-phasing, conditional-random-field, random-forest, patterson-f-statistics, genome-wide-association-study]
sources:
  - paper: doi:10.1093/genetics/164.4.1567
    title: Daniel Falush, Matthew Stephens and Jonathan K. Pritchard, Inference of population structure using multilocus genotype data, linked loci and correlated allele frequencies, Genetics 164(4), 2003
    locator: pp. 1567-1587 (the linkage model, with the origin of each copy as a Markov chain along the chromosome)
  - paper: doi:10.1371/journal.pgen.1000519
    title: Alkes L. Price, Arti Tandon, Nick Patterson and coauthors, Sensitive detection of chromosomal segments of distinct ancestry in admixed populations, PLoS Genetics 5(6), 2009
    locator: e1000519 (HAPMIX, a hidden Markov model that copies from reference haplotypes of two source populations)
  - paper: doi:10.1016/j.ajhg.2013.06.020
    title: Brian K. Maples, Simon Gravel, Eimear E. Kenny and Carlos D. Bustamante, RFMix, a discriminative modeling approach for rapid and robust local-ancestry inference, American Journal of Human Genetics 93(2), 2013
    locator: pp. 278-288 (random forests in windows, smoothed by a conditional random field)
---

Local ancestry inference takes the genome of an admixed individual and labels each position of each chromosome copy with the source population that the copy descends from at that position. After an admixture event, recombination in each generation cuts the chromosomes of the mixed population into ever shorter segments, each from one source. So the label is constant over a stretch and changes at the points of past recombination. The standard method is a [hidden Markov model](/hidden-markov-model/) along the genome, whose hidden state is the ancestry, whose transitions model the recombination since the admixture, and whose emissions come from the allele frequencies or the haplotypes of reference panels of the sources. The labels are then read off with the [forward-backward algorithm](/forward-backward-algorithm/) or the [Viterbi algorithm](/viterbi-algorithm/).

## In plain words

When two populations mix, the children carry whole chromosomes from parents of each side. Over the following generations, chromosomes are cut and joined each time they are passed on. After some generations, each chromosome is a patchwork of pieces from the two sides, and the pieces get shorter with time.

The task is to find these pieces. You walk along the chromosome. At each position you ask which source population the variants here look like, using samples of the sources. You also prefer to stay with the same source for a while, because a change needs a cut, and cuts are rare over short distances. A method that weighs these two things gives, for each position, the chance that it comes from each source.

## Definition

**Input.**

- An admixed haplotype $h \in \{0, 1\}^m$ at $m$ biallelic sites with genetic positions $x_1 < \cdots < x_m$ in Morgans, or an unphased genotype vector in $\{0, 1, 2\}^m$.
- Information about $K$ source populations: their allele frequencies $f_{kj}$, or reference haplotypes from each source.
- Admixture fractions $\alpha_1, \ldots, \alpha_K$ and the number of generations $T$ since the admixture, given or estimated.

**Model.** The ancestry $z_j \in \{1, \ldots, K\}$ at site $j$ follows a Markov chain. At the first site, $z_1 = k$ with probability $\alpha_k$. Between sites $j$ and $j + 1$, at genetic distance $d_j = x_{j+1} - x_j$, the ancestry is drawn again from $\alpha$ with probability $1 - e^{-T d_j}$, which may give the same source, and is kept otherwise. Given $z_j = k$, the allele $h_j$ is 1 with probability $f_{kj}$, or is drawn from a copying model of the haplotypes of source $k$, as in the [Li-Stephens model](/li-stephens-model/).

**Output.** For each site $j$, the posterior $P(z_j = k \mid h)$ for each $k$, or the most likely sequence $z_1, \ldots, z_m$. For a diploid genotype, the output is the number of copies of each ancestry at each site, 0, 1 or 2.

## Variants

- **Phased or unphased.** With phased haplotypes, the model has $K$ states per copy. With unphased genotypes, the state is the unordered pair of ancestries, with $K(K + 1)/2$ states, or phasing is done first.
- **Frequencies or haplotypes.** A model with only source frequencies treats sites as independent given the ancestry, which fails in regions of strong [linkage disequilibrium](/linkage-disequilibrium/). Copying from reference haplotypes models the linkage disequilibrium of each source.
- **With or without references.** With reference panels the problem is supervised. Without them, the sources and the labels are estimated together, as in the linkage model of Falush and coauthors.
- **Number of sources and pulses.** Two sources and one pulse are the simplest case. Several sources, several pulses or continuous gene flow change the distribution of segment lengths.
- **Archaic segments.** Segments from an archaic group such as Neandertals in modern genomes are found by similar models with a reference genome of the archaic group, or with no reference by the density of private variants.

## Examples

Take one haplotype at three sites, $K = 2$, $\alpha = (0.5, 0.5)$, and frequencies of allele 1 of $0.9$ in source 1 and $0.1$ in source 2 at every site. The ancestry is drawn again with probability $0.1$ between adjacent sites, so the chain stays with probability $0.9 + 0.1 \cdot 0.5 = 0.95$ and moves with probability $0.05$. The haplotype is $h = (1, 1, 0)$.

- The forward values are $(0.45, 0.05)$ at site 1, $\big((0.45 \cdot 0.95 + 0.05 \cdot 0.05) \cdot 0.9,\ (0.45 \cdot 0.05 + 0.05 \cdot 0.95) \cdot 0.1\big) = (0.387, 0.007)$ at site 2, and $(0.0368, 0.0234)$ at site 3, so $P(h) = 0.0602$.
- The posterior probability of source 1 is $0.927$ at site 1, $0.900$ at site 2 and $0.611$ at site 3.

At site 3 the allele 0 is typical of source 2, but a change of ancestry costs a factor of $0.05$, so the posterior still favors source 1. A run of several sites with allele 0 would move the label to source 2. This is how the model trades the fit at each site against the rarity of changes.

## Known algorithms

- **HMM with source frequencies.** The linkage model of Falush and coauthors and several later programs use the model of the definition with frequencies as emissions, with posteriors from the forward-backward algorithm.
- **HAPMIX.** Price and coauthors (2009) copy from reference haplotypes of two sources with a Li-Stephens model inside each source, and let the copied source change at the rate of the admixture. It handles linkage disequilibrium within each source.
- **RFMix.** Maples and coauthors (2013) classify windows of SNPs with a [random forest](/random-forest/) trained on the references, and smooth the window labels with a [conditional random field](/conditional-random-field/). It can update the references with confidently labeled admixed haplotypes, and it corrects phase errors.
- **Window methods.** Programs such as LAMP assign an ancestry to each window of SNPs and take a majority vote over overlapping windows, without a full HMM.
- **Painting by donors.** Copying from all reference haplotypes of all sources, and summing the posterior by source, gives the local ancestry and also finer structure within sources.

## Bounds

- **Time.** The forward-backward algorithm over $K$ ancestry states costs $O(mK^2)$ per haplotype, or $O(mK)$ with the stay-or-jump form of the transitions. A Li-Stephens emission with $R$ reference haplotypes costs $O(mR)$.
- **Segment lengths.** In the model of the definition, a segment of ancestry $k$ ends at rate $T(1 - \alpha_k)$ per Morgan, so its mean length is $1 / (T(1 - \alpha_k))$ Morgans. For an admixture 10 generations ago with $\alpha_k = 0.5$, the mean is 20 centimorgans. Old admixture gives short segments, and segments shorter than the spacing of informative sites cannot be found.
- **Close sources.** When the sources differ little, with small [fixation index](/fixation-index/), each site carries little information, and the error rate rises. The accuracy is measured on simulated admixed genomes, not proved.

## Reductions

- **To HMM decoding.** With the model fixed, the problem is posterior decoding or Viterbi decoding of an HMM, solved exactly in linear time in $m$.
- **To global ancestry.** The average of the local ancestry over the genome estimates the ancestry fraction $q_i$ of [population structure inference](/population-structure-inference/). Global methods are the limit with no linkage.
- **To the Li-Stephens model.** Copying from references of all sources is a Li-Stephens model whose states are grouped by source; the posterior of a group is the local ancestry.

## Applications

- **Admixture mapping.** In an admixed population, a disease variant that is more common in one source makes cases carry more of that ancestry near the variant. Testing local ancestry against the trait finds such regions with fewer tests than a [genome-wide association study](/genome-wide-association-study/).
- **Dating admixture.** The length distribution of segments, or the decay of ancestry correlation with distance, estimates the number of generations since the admixture.
- **Selection.** Regions with much more or much less ancestry from one source than the genome average suggest selection after the admixture.
- **Association studies.** Local ancestry as a covariate, or an ancestry-specific test, controls for confounding and finds effects that differ between sources.
- **History.** Labels of the genomes of African Americans, Latin Americans and other admixed groups show the sources, the fractions and the timing of the mixing.

## References
