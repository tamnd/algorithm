---
tag: MDH318
kind: problem
slug: haplotype-assembly
name: Haplotype assembly
aliases:
- single individual haplotyping
- read-based phasing
area: biology/read-mapping-and-variant-calling
level: advanced
summary: Split the heterozygous alleles of one diploid genome into its two haplotypes, using reads that cover several variant sites.
prereqs: [variant-calling-problem, variant-call-format, paired-end-reads]
see_also: [minimum-error-correction-problem, fixed-parameter-mec, haplotype-phasing, li-stephens-model, positional-burrows-wheeler-transform, maximum-cut, haplotype-based-variant-calling, connected-components]
sources:
  - paper: doi:10.1093/bioinformatics/btn298
    title: Vikas Bansal and Vineet Bafna, HapCUT, an efficient and accurate algorithm for the haplotype assembly problem, Bioinformatics 24(16), 2008
    locator: pp. i153 to i159 (the fragment matrix, the MEC objective, and the heuristic of repeated graph cuts)
  - paper: doi:10.1089/cmb.2014.0157
    title: Murray Patterson, Tobias Marschall, Nadia Pisanti, Leo van Iersel, Leen Stougie, Gunnar W. Klau and Alexander Schönhuth, WhatsHap, weighted haplotype assembly for future-generation sequencing reads, Journal of Computational Biology 22(6), 2015
    locator: pp. 498 to 509 (an exact dynamic program for weighted MEC, exponential only in the coverage)
  - paper: doi:10.1093/bib/3.1.23
    title: Ross Lippert, Russell Schwartz, Giuseppe Lancia and Sorin Istrail, Algorithmic strategies for the single nucleotide polymorphism haplotype assembly problem, Briefings in Bioinformatics 3(1), 2002
    locator: the statement of the haplotype assembly problem and its models
  - paper: "Giuseppe Lancia, Vineet Bafna, Sorin Istrail, Ross Lippert and Russell Schwartz, SNPs problems, complexity, and algorithms, Algorithms - ESA 2001, Lecture Notes in Computer Science 2161, Springer, 2001"
    title: SNPs problems, complexity, and algorithms
    locator: the first statement of the problem with the conflict graph of fragments
---

Haplotype assembly finds the two haplotypes of one diploid person, the sequences of alleles on the copy of each chromosome from the mother and from the father, using the reads of that person alone. Variant calling gives the heterozygous sites, but not which alleles lie on the same copy. A read that covers two or more heterozygous sites shows the alleles of one copy at those sites, so reads link the sites, and enough overlapping reads give the phase of a whole region. The reads have errors, so the problem is posed as an optimization, most often as the [minimum error correction problem](/minimum-error-correction-problem/) (MEC). It differs from [haplotype phasing](/haplotype-phasing/) in the narrow sense, which infers haplotypes from the genotypes of many people with a model of the population, and does not need reads that span several sites.

## In plain words

Each person has two copies of each chromosome. A variant caller tells you that at one place the person has an A and a G, and at a place further on a C and a T. It does not tell you whether the A sits on the same copy as the C or as the T.

A read comes from one copy. If one read shows both A and C, they are on the same copy. Collect many such reads, sort them into two piles, one for each copy, and read the two copies off the piles. Some reads have mistakes, so choose the sorting that needs the fewest corrections.

## Definition

**Input.** The heterozygous sites $1, \ldots, m$ of one sample, with the two alleles of each coded as 0 and 1, and the reads of the sample mapped to the reference. Each read, or each pair of reads of one fragment, gives a row of the *fragment matrix*: 0 or 1 at the sites it covers, and a hole elsewhere. The entries can carry weights, from the base qualities.

**Output.** Two haplotypes $h_1, h_2 \in \{0, 1\}^m$, usually complements of each other since the sites are heterozygous, in *phase blocks*. Two sites are in one block if a chain of fragments links them. Between blocks the relative phase is not determined by the reads.

**Objective.** Since the data have errors, the haplotypes are those of an optimal solution of a model:

- **MEC**, the fewest changes of entries so that the fragments split into two conflict-free groups; see [minimum error correction](/minimum-error-correction-problem/);
- **minimum fragment removal** and **minimum SNP removal**, which remove rows or columns instead;
- a **likelihood** of the reads with an error rate for each entry.

MEC, with weights, is the model of most tools.

**Haplotype assembly is not population phasing.** Population phasing takes the genotypes of many unrelated people, without read information, and uses the fact that people share long stretches of haplotype, as in the [Li-Stephens model](/li-stephens-model/) and methods based on the [positional Burrows-Wheeler transform](/positional-burrows-wheeler-transform/). Haplotype assembly takes the reads of one person and needs no population. The two can be combined.

## Variants

- **Long reads.** Reads of many thousands of bases cover many sites each, which gives long blocks but high error rates.
- **Paired and linked reads.** Pairs with long inserts and barcoded linked reads join sites that are far apart, at the cost of holes inside the fragments.
- **Trios and pedigrees.** With the reads or genotypes of the parents, most sites can be phased by Mendel's rules, and reads phase the rest.
- **Polyploid genomes.** Plants and some other genomes have more than two copies, and the reads must be split into $k$ groups.
- **Genotyping during phasing.** The same model can correct the genotypes of the sites, by allowing a column to be homozygous.

## Examples

**Two sites.** A sample is heterozygous A/G at site 1 and C/T at site 2. Five reads cover both: three show A and C, one shows G and T, and one shows G and C. Code A and C as 0, G and T as 1. The fragments are 00, 00, 00, 11 and 10. The phase A-C and G-T explains four reads and needs one change, in the last read, while the phase A-T and G-C needs four. The MEC solution is $h_1 = 00$, $h_2 = 11$, so the haplotypes are AC and GT.

**Four sites with a triangle of conflicts.** The example on the [MEC](/minimum-error-correction-problem/) page has six gapless fragments over four sites, three of which conflict with each other pairwise. One change gives the haplotypes 0011 and 1100, and this is the optimum.

**Blocks.** If no fragment covers both site 10 and site 11, sites 1 to 10 and sites 11 to 20 are two blocks. Each block has a phase, but the reads give no information on whether $h_1$ of the first block goes with $h_1$ or $h_2$ of the second. A tool reports the two blocks separately.

## Known algorithms

| method | approach | result |
|---|---|---|
| HapCUT (Bansal and Bafna, 2008) | starts from a phase and repeatedly finds a cut in a graph of the sites, weighted by the fragments that disagree with the current phase, and flips the sites on one side when that lowers the MEC cost | heuristic, fast, no bound on the coverage |
| WhatsHap (Patterson et al., 2015) | the [dynamic program over columns](/fixed-parameter-mec/) | exact weighted MEC in $O(2^c m)$ for coverage $c$, after read selection |
| greedy and [local search](/local-search/) methods | add reads or flip sites one at a time | heuristic |
| probabilistic methods | an HMM or a likelihood over the phase with error rates | exact or heuristic, by model |

## Bounds

- **NP-hard.** MEC is NP-hard, even for gapless fragments, so no exact polynomial algorithm is expected; see [MEC](/minimum-error-correction-problem/).
- **Fixed-parameter tractable.** The exact dynamic program is exponential only in the coverage, so tools select reads to keep the coverage at about 15 to 20.
- **Blocks are limited by the data.** Two adjacent heterozygous sites can be phased only if some fragment covers both or a chain of fragments joins them. If the distance between sites is larger than the fragments, no method that uses only reads can phase them.
- **Accuracy.** Results are measured by the *switch error rate*, the share of adjacent pairs of sites whose relative phase is wrong, and by the length of the blocks, which depend on the read length, the error rate and the density of heterozygous sites.

## Reductions

- **To MEC.** The reads give the fragment matrix, and the haplotypes are those of an optimal MEC solution.
- **To blocks.** The [connected components](/connected-components/) of the graph of sites linked by fragments are the blocks, and each block is solved alone.
- **To graph cuts.** With sites as vertices and edges weighted by the support for the same and the opposite phase, a phase is a 2-coloring, and a good phase is a [maximum cut](/maximum-cut/) of a suitable graph, which is the idea of HapCUT.

## Applications

- **Compound heterozygosity.** In clinical genetics, two damaging variants in one gene cause disease only if they lie on different copies.
- **Allele-specific expression and methylation.** Reads of RNA or of methylation assays are assigned to a copy by the phased variants.
- **Phased assembly.** The two copies of a diploid genome are assembled separately using the phase.
- **Reference panels.** Phased genomes from long reads give haplotypes for panels used in population phasing and [imputation](/genotype-imputation/).

## References
