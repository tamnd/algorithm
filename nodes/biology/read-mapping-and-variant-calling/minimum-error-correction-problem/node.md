---
tag: FWK7XY
kind: problem
slug: minimum-error-correction-problem
name: Minimum error correction problem
aliases:
- MEC problem
area: biology/read-mapping-and-variant-calling
level: advanced
summary: Flip the fewest alleles in a fragment matrix so that the rows split into two conflict-free haplotypes. NP-hard even for gapless rows, it is fixed-parameter tractable in the coverage.
prereqs: [haplotype-assembly, np-hard, hamming-distance]
see_also: [fixed-parameter-mec, fixed-parameter-tractable, odd-cycle-transversal, maximum-cut, bipartiteness-testing, clustering-problem, local-search, haplotype-phasing]
sources:
  - paper: doi:10.1093/bib/3.1.23
    title: Ross Lippert, Russell Schwartz, Giuseppe Lancia and Sorin Istrail, Algorithmic strategies for the single nucleotide polymorphism haplotype assembly problem, Briefings in Bioinformatics 3(1), 2002
    locator: the sections on the fragment conflict models (fragment removal, SNP removal and error correction) and their complexity
  - paper: doi:10.1007/s00453-007-0029-z
    title: Rudi Cilibrasi, Leo van Iersel, Steven Kelk and John Tromp, The complexity of the single individual SNP haplotyping problem, Algorithmica 49(1), 2007
    locator: pp. 13 to 36 (MEC is NP-hard also when no fragment has a hole, and some polynomial cases)
  - paper: "Giuseppe Lancia, Vineet Bafna, Sorin Istrail, Ross Lippert and Russell Schwartz, SNPs problems, complexity, and algorithms, Algorithms - ESA 2001, Lecture Notes in Computer Science 2161, Springer, 2001"
    title: SNPs problems, complexity, and algorithms
    locator: the sections on the conflict graph of fragments, minimum fragment removal and minimum SNP removal, and the gapless case
  - paper: doi:10.1089/cmb.2014.0157
    title: Murray Patterson, Tobias Marschall, Nadia Pisanti, Leo van Iersel, Leen Stougie, Gunnar W. Klau and Alexander Schönhuth, WhatsHap, weighted haplotype assembly for future-generation sequencing reads, Journal of Computational Biology 22(6), 2015
    locator: pp. 498 to 509 (weighted MEC and its dynamic program, exponential only in the coverage)
---

The minimum error correction problem (MEC) is the usual combinatorial form of [haplotype assembly](/haplotype-assembly/). Each read of a diploid genome shows, at the heterozygous sites that it covers, which allele it carries, and the reads of one copy of the chromosome should agree with each other. Because of sequencing errors, they do not always agree. MEC asks for the smallest number of entries to change so that the reads split into two groups, each without disagreement inside; the two groups then spell the two haplotypes. Lippert et al. (2002) defined it. It is [NP-hard](/np-hard/), and Cilibrasi et al. (2007) proved that it stays NP-hard when every fragment is gapless. It is [fixed-parameter tractable](/fixed-parameter-tractable/) in the coverage: the [dynamic program of WhatsHap](/fixed-parameter-mec/) solves it in $O(2^c m)$ time.

## In plain words

Think of a table with one row for each read and one column for each place where the two copies of a chromosome can differ. Each cell holds 0, 1 or nothing, if the read does not reach that column.

If the reads had no errors, you could sort the rows into two groups so that, in each column, all rows of a group show the same value. With errors, that may be impossible. So change as few cells as you can until it works. The two groups then tell you the two copies.

## Definition

**Input.** A fragment matrix $F$ with $n$ rows, the fragments, and $m$ columns, the sites. Each entry $F_i(j)$ is 0, 1 or a hole $-$. A fragment is *gapless* if its non-hole entries are consecutive.

**Conflicts.** Two fragments *conflict* if they have different values at some column where neither has a hole. The *conflict graph* has the fragments as vertices and an edge for each conflict. The matrix is *feasible* if its rows can be split into two sets without a conflict inside either set, which is the same as a bipartite conflict graph: a set of binary rows with no conflict between any two has, at each column, one value shared by all its non-hole entries.

**MEC.** Find the fewest entries of $F$ to change from 0 to 1 or from 1 to 0 so that the matrix becomes feasible. An equivalent form is a 2-clustering in [Hamming distance](/hamming-distance/) with holes ignored:

$$\mathrm{MEC}(F) = \min_{h_1, h_2 \in \{0, 1\}^m} \sum_{i = 1}^{n} \min(d(F_i, h_1), d(F_i, h_2)),$$

where $d(F_i, h)$ counts the non-hole entries of $F_i$ that differ from $h$. Each fragment goes to the haplotype it is closer to, and the entries that differ from it are the ones changed.

**Weighted MEC.** Each entry has a weight, such as its Phred quality, and the cost is the sum of the weights of the changed entries.

**All-heterozygous MEC.** If every column is known to be heterozygous, $h_2$ must be the complement of $h_1$.

## Variants

- **Minimum fragment removal (MFR).** Remove the fewest fragments so that the rest is feasible. This is [odd cycle transversal](/odd-cycle-transversal/) on the conflict graph.
- **Minimum SNP removal (MSR).** Remove the fewest columns so that the matrix is feasible.
- **Weighted and all-heterozygous forms**, as above.
- **Polyploid MEC.** Split the rows into $k$ groups for a genome with $k$ copies.
- **Probabilistic forms.** Maximize the likelihood of the reads with an error rate for each entry, which gives MEC when all error rates are equal and small.

## Examples

**A matrix that is not feasible.** Six gapless fragments over four sites:

| fragment | site 1 | site 2 | site 3 | site 4 |
|---|---|---|---|---|
| $f_1$ | 0 | 0 | 1 | - |
| $f_2$ | 0 | 0 | - | - |
| $f_3$ | - | 0 | 1 | 1 |
| $f_4$ | 1 | 1 | 0 | - |
| $f_5$ | - | 1 | 0 | 0 |
| $f_6$ | 1 | 0 | 0 | 0 |

The fragments $f_1$, $f_4$ and $f_6$ conflict with each other pairwise, which is a triangle in the conflict graph, so no split into two conflict-free sets exists. Changing the 0 of $f_6$ at site 2 to 1 makes $f_6$ agree with $f_4$ and $f_5$. Then $\{f_1, f_2, f_3\}$ spells $h_1 = 0011$ and $\{f_4, f_5, f_6\}$ spells $h_2 = 1100$, and the cost is 1. A search over all pairs of haplotypes confirms that 1 is the optimum, and that the only optimal pair is $\{0011, 1100\}$. MFR also has cost 1 here: remove $f_6$.

**The weighted example of WhatsHap.** The four fragments of Patterson et al. (2015), worked out on the page of the [fixed-parameter dynamic program](/fixed-parameter-mec/), have weighted MEC cost 1, both in the free and in the all-heterozygous form.

## Known algorithms

| method | page | result | time |
|---|---|---|---|
| dynamic program over columns (WhatsHap) | [fixed-parameter MEC](/fixed-parameter-mec/) | exact for weighted MEC | $O(2^c m)$ for coverage $c$ |
| search over haplotypes | none | exact | $O(4^m n m)$, or $O(2^m n m)$ for the all-heterozygous form |
| HapCUT | [haplotype assembly](/haplotype-assembly/) | heuristic: repeated cuts of a graph of the sites, in the spirit of [max cut](/maximum-cut/) | fast in practice, no bound on the quality |
| [local search](/local-search/) and greedy methods | none | heuristic | fast |

The search over haplotypes is exponential in the number of sites, and the dynamic program is exponential only in the coverage, which is small for most data after read selection.

## Bounds

- **NP-hard.** MEC is NP-hard in general (Lippert et al., 2002), and Cilibrasi et al. (2007) showed that it is NP-hard also when all fragments are gapless. MFR and MSR, by contrast, are polynomial for gapless fragments (Lancia et al., 2001).
- **Fixed-parameter tractable in the coverage.** The time $O(2^c m)$ of the dynamic program is polynomial for each fixed coverage $c$. With the symmetry of the two sides, the bound is $O(2^{c-1} m)$.
- **Fixed number of sites.** For a fixed $m$, the search over haplotype pairs is polynomial in $n$.
- **Feasibility.** Whether the cost is 0 is easy to decide: it is the question whether the conflict graph is bipartite, which [bipartiteness testing](/bipartiteness-testing/) answers in linear time in the size of the graph.

## Reductions

- **From haplotype assembly.** The reads and the heterozygous sites of one sample give the fragment matrix; see [haplotype assembly](/haplotype-assembly/).
- **To clustering.** MEC is a 2-median clustering of the rows in Hamming distance with holes; see [clustering](/clustering-problem/).
- **MFR to odd cycle transversal.** The removed fragments are a set of vertices whose removal makes the conflict graph bipartite.
- **To weighted graph cuts.** With one vertex per site and edges weighted by how many reads say the two sites have the same or opposite phase, a good phase is a cut, which is the idea of HapCUT.

## Applications

- **Phasing one genome from reads.** Long reads, linked reads and pairs with long inserts cover several heterozygous sites, and MEC turns them into phase blocks.
- **Clinical genetics.** Whether two variants in one gene are on the same copy or on different copies.
- **Allele-specific analysis.** Expression and methylation of each copy, once the reads are split by haplotype.
- **Assembly.** The separation of the two copies of a diploid genome in a phased assembly.

## References
