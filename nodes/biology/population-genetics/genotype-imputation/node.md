---
tag: Q7FXWH
kind: problem
slug: genotype-imputation
name: Genotype imputation
aliases:
- imputation of untyped variants
- haplotype reference imputation
area: biology/population-genetics
level: core
summary: "Predict genotypes at variants not assayed in a sample from a reference panel of haplotypes, usually with the Li-Stephens HMM."
prereqs: [li-stephens-model, hidden-markov-model, forward-backward-algorithm]
see_also: [haplotype-phasing, linkage-disequilibrium, positional-burrows-wheeler-transform, genome-wide-association-study, genotype-likelihood, expectation-maximization, identity-by-descent, viterbi-algorithm]
sources:
  - paper: doi:10.1038/ng2088
    title: Jonathan Marchini, Bryan Howie, Simon Myers, Gil McVean and Peter Donnelly, A new multipoint method for genome-wide association studies by imputation of genotypes, Nature Genetics 39(7), 2007
    locator: pp. 906-913 (IMPUTE, an HMM over reference haplotypes for unphased study genotypes, and association tests on the imputed genotypes)
  - paper: doi:10.1002/gepi.20533
    title: Yun Li, Cristen J. Willer, Jun Ding, Paul Scheet and Gonçalo R. Abecasis, MaCH, using sequence and genotype data to estimate haplotypes and unobserved genotypes, Genetic Epidemiology 34(8), 2010
    locator: pp. 816-834 (the MaCH HMM, the estimation of its error and crossover parameters, and the estimated r-squared of imputed genotypes)
  - paper: doi:10.1371/journal.pgen.1000529
    title: Bryan N. Howie, Peter Donnelly and Jonathan Marchini, A flexible and accurate genotype imputation method for the next generation of genome-wide association studies, PLoS Genetics 5(6), 2009
    locator: article e1000529 (IMPUTE2, with alternating phasing and imputation steps and a subset of reference haplotypes per study haplotype)
  - paper: doi:10.1093/genetics/165.4.2213
    title: Na Li and Matthew Stephens, Modeling linkage disequilibrium and identifying recombination hotspots using single-nucleotide polymorphism data, Genetics 165(4), 2003
    locator: pp. 2213-2233 (the copying model of a haplotype as a mosaic of other haplotypes)
---

Genotype imputation fills in the genotypes of a sample at variants that were not measured, using a reference panel of densely genotyped or sequenced haplotypes. A genotyping array measures a few hundred thousand SNPs. Because nearby variants are in [linkage disequilibrium](/linkage-disequilibrium/), the measured alleles of a person identify, locally, which reference haplotypes their chromosomes resemble, and the alleles of those haplotypes predict the missing variants. The standard model is the [Li-Stephens](/li-stephens-model/) hidden Markov model, and the posterior probabilities from the [forward-backward algorithm](/forward-backward-algorithm/) give a probability for each missing genotype, not only a best guess.

## In plain words

People who live today carry long stretches of chromosome that they inherited from shared distant ancestors. A reference panel holds many such stretches, read in full. A study measures only some positions in each person. Over a short region, the measured positions usually match one or a few reference stretches well. The positions that were not measured are then likely to carry the same letters as those stretches. Because the match changes along the chromosome, the method lets each person switch from one reference stretch to another at any point, with a small chance per step. It then computes, for every missing position, how likely each possible letter is. These guesses let studies that used different arrays be combined.

## Definition

**Input.**

- A reference panel of $K$ phased haplotypes at $M$ sites, $H \in \{0, 1\}^{K \times M}$.
- A target sample, genotyped at a subset $T$ of the sites: unphased genotypes $g_m \in \{0, 1, 2\}$ for $m \in T$, or genotype likelihoods from sequencing.
- A genetic map, which gives the genetic distance $d_m$ between sites $m$ and $m + 1$.

**Model (Li-Stephens).** Each target haplotype is a mosaic of the reference haplotypes. A hidden state $z_m \in \{1, \dots, K\}$ says which reference haplotype it copies at site $m$. Between sites, with probability $\rho_m$, a switch happens and the new state is uniform over the $K$ haplotypes; otherwise the state stays. At each site the copied allele is emitted, and with a small probability $\varepsilon$ it is changed, to model mutation and error. For a diploid target, the two haplotypes are two independent such chains, and only their sum is observed at the typed sites.

**Output.** For every untyped site $m \notin T$, the posterior probabilities $P(g_m = 0), P(g_m = 1), P(g_m = 2)$ given the observed genotypes, or the dosage $\mathrm E[g_m] \in [0, 2]$.

## Variants

- **Pre-phased imputation.** First phase the target genotypes into two haplotypes, by [haplotype phasing](/haplotype-phasing/), then impute each haplotype with the haploid model. This is much faster, since the state space has $K$ states, not $K^2$.
- **Imputation from sequencing reads.** For low-coverage sequencing, the emissions are [genotype likelihoods](/genotype-likelihood/) from the reads, and every site is uncertain.
- **Reference-free imputation.** Without a panel, the study samples themselves serve as each other's references, and the model parameters are estimated from the data.
- **Imputation of structural variants and HLA alleles.** Any variant that is phased in the panel and in linkage disequilibrium with SNPs can be imputed the same way.

## Examples

Take two reference haplotypes over three sites, $H_1 = (0, 1, 0)$ and $H_2 = (1, 0, 1)$, a haploid target typed at sites 1 and 3, $\varepsilon = 0.01$, and a switch probability that gives $P(\text{stay}) = 0.95$ and $P(\text{move to the other}) = 0.05$ between neighbouring sites. The prior on the first state is uniform.

- **Target $(0, ?, 0)$.** The forward values at site 2 are $\alpha_2 = (0.4705, 0.0295)$ and the backward values $\beta_2 = (0.941, 0.059)$. The posterior of copying $H_1$ at site 2 is $0.4705 \cdot 0.941 / (0.4705 \cdot 0.941 + 0.0295 \cdot 0.059) = 885481/888962 = 0.9961$. So the imputed allele is 1, the allele of $H_1$, with probability $0.9961 \cdot 0.99 + 0.0039 \cdot 0.01 = 0.986$.
- **Target $(0, ?, 1)$.** Now site 1 favours $H_1$ and site 3 favours $H_2$, so a switch is needed, before or after site 2. $\beta_2 = (0.059, 0.941)$, the two products are both $0.0277595$, and the posterior is exactly $1/2$ for each haplotype. The imputed allele has probability $1/2$, and the dosage carries this uncertainty into the association test.
- **Diploid target.** If the two haplotypes of a person have the posteriors $0.986$ and $0.5$ for allele 1 at site 2, the dosage is $0.986 + 0.5 = 1.486$.

## Known algorithms

- **Forward-backward on the Li-Stephens HMM.** With $K$ states, the transition is "stay with probability $1 - \rho$, else jump to a uniform state". So $\alpha_{m+1}(k) = e_{m+1}(k) [(1 - \rho_m) \alpha_m(k) + (\rho_m / K) \sum_j \alpha_m(j)]$, and the sum is computed once per site. This makes the cost $O(M K)$ per haploid target, not the $O(M K^2)$ of a general HMM.
- **Diploid targets.** The pair of states $(z^{(1)}_m, z^{(2)}_m)$ has $K^2$ values. A general HMM would cost $O(M K^4)$, but the transition factorizes over the two chains, and the same trick gives $O(M K^2)$. IMPUTE (Marchini and coworkers 2007) and MaCH (Li and coworkers 2010) work in this space.
- **Pre-phasing with a subset of the panel.** IMPUTE2 (Howie and coworkers 2009) alternates phasing and imputation and uses, for each study haplotype, only the reference haplotypes closest to it. Minimac and later Beagle versions impute pre-phased haplotypes at $O(M K)$ each.
- **Selecting references with the PBWT.** The [positional Burrows-Wheeler transform](/positional-burrows-wheeler-transform/) finds, at each site, the reference haplotypes with the longest match to the target, so that the HMM runs on a few states.
- **Parameter estimation.** The switch and error rates can be fitted by [expectation maximization](/expectation-maximization/) or by Markov chain sampling on the study data, as in MaCH.

## Bounds

- **Time.** Any method that reads the panel spends $\Omega(M K)$ per target in the worst case. Forward-backward with the uniform jump meets this bound for haploid targets. Methods that index the panel once, such as the PBWT, spend less per target after the index is built.
- **Accuracy.** No method can predict a variant that is not in linkage disequilibrium with the typed sites, since then the typed alleles carry no information about it. Accuracy is lowest for rare variants, which are carried by few reference haplotypes and are tagged poorly by common SNPs, and for panels of a different ancestry.
- **Measures.** The squared correlation $r^2$ between the dosage and the true genotype measures accuracy. When the truth is unknown, programs report an estimate from the posteriors alone, such as the ratio of the variance of the dosages to the binomial variance $2p(1 - p)$, or the information measure of IMPUTE. A test on imputed dosages with accuracy $r^2$ has about the power of a test on $r^2 N$ genotyped people.

## Reductions

- **To phasing.** Imputation and phasing use the same HMM. Phasing infers the hidden pair of haplotypes, and imputation reads off their alleles at the untyped sites.
- **To an HMM posterior.** Under the model, imputation is exactly the computation of posterior marginals in an HMM, solved by the forward-backward algorithm.
- **From missing data.** Sporadic missing genotypes at typed sites are a special case, with the same model.

## Applications

- **Meta-analysis.** Studies that used different arrays are imputed to one reference panel, so that every study has the same variants.
- **Denser association scans.** Imputation brings array data close to the variant density of the panel, which helps to locate the causal variant of a [genome-wide association study](/genome-wide-association-study/) signal.
- **Low-coverage sequencing.** Imputation from genotype likelihoods turns cheap, shallow sequencing into accurate genotypes at common variants.
- **Imputation servers.** Large panels are kept on servers, and users upload their genotypes for imputation, because the panels cannot be shared freely.

## References
