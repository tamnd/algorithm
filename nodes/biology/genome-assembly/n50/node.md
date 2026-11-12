---
tag: H0RY1P
kind: definition
slug: n50
name: N50
aliases:
- NG50
- contig N50
area: biology/genome-assembly
level: intro
summary: The largest length L such that contigs of length at least L hold half the bases of the assembly. NG50 uses half the genome size instead.
prereqs: [genome-assembly-problem]
see_also: [contig, scaffold, assembly-quality-assessment, genome-assembly-problem, genome-repeat, kmer-spectrum]
sources:
  - paper: doi:10.1016/j.ygeno.2010.03.001
    title: Jason R. Miller, Sergey Koren and Granger Sutton, Assembly algorithms for next-generation sequencing data, Genomics 95(6) (2010)
    locator: pp. 315 to 327 (N50 as the usual measure of contig size)
  - paper: doi:10.1101/gr.126599.111
    title: Dent Earl et al., Assemblathon 1, a competitive assessment of de novo short read assembly methods, Genome Research 21(12) (2011)
    locator: pp. 2224 to 2241 (the definition of NG50, with G for genome)
  - paper: doi:10.1093/bioinformatics/btt086
    title: Alexey Gurevich, Vladislav Saveliev, Nikolay Vyahhi and Glenn Tesler, QUAST, quality assessment tool for genome assemblies, Bioinformatics 29(8) (2013)
    locator: pp. 1072 to 1075 (N50, NG50, NA50 and NGA50)
---

N50 is the standard number for how long the pieces of a genome assembly are. Sort the [contigs](/contig/) from longest to shortest and add up their lengths; N50 is the length of the contig at which the sum first reaches half of the total length. So half of the assembled bases lie in contigs of length N50 or more. NG50 is the same with half of the genome size in place of half of the assembly size. Neither number says whether the contigs are correct, and both go up when an assembler joins pieces that do not belong together.

## Definition

Let an assembly have contigs of lengths $\ell_1 \ge \ell_2 \ge \cdots \ge \ell_m$, sorted in decreasing order, with total length $T = \sum_{i=1}^{m} \ell_i$.

**N50.** Let $j$ be the smallest index with

$$\ell_1 + \ell_2 + \cdots + \ell_j \ge \frac{T}{2}.$$

Then $\text{N50} = \ell_j$, and **L50** $= j$ is the number of contigs needed to reach half of the assembly.

**Equivalent form.** N50 is the largest length $\ell$ such that the contigs of length at least $\ell$ hold at least half of the bases:

$$\text{N50} = \max \Big\{ \ell : \sum_{i \,:\, \ell_i \ge \ell} \ell_i \ge \frac{T}{2} \Big\}.$$

Proof of the equivalence: the contigs of length at least $\ell_j$ include $\ell_1, \ldots, \ell_j$, so they hold at least $T/2$ bases. For any $\ell > \ell_j$, the contigs of length at least $\ell$ are among $\ell_1, \ldots, \ell_{j-1}$, which hold less than $T/2$ by the choice of $j$.

**Length-weighted median.** Pick a base of the assembly uniformly at random and look at the length of the contig that holds it. N50 is a median of this length. It is not the median contig length: a few long contigs can hold half of the bases while most contigs are short.

**Nx.** For $0 < x < 100$, Nx replaces $T/2$ with $xT/100$. N50 is the case $x = 50$, and N90 is often given too.

**NG50.** Let $G$ be the genome size, known or estimated, for example from the [k-mer spectrum](/kmer-spectrum/). NG50 uses $G/2$ in place of $T/2$: the smallest $j$ with $\ell_1 + \cdots + \ell_j \ge G/2$ gives $\text{NG50} = \ell_j$. The Assemblathon 1 study defined it (G for genome) so that assemblies of the same genome with different total lengths can be compared. If $T < G/2$, NG50 is not defined.

**Contig N50 and scaffold N50.** The same formula applied to the [scaffolds](/scaffold/), which may contain gaps, gives the scaffold N50. Contig N50 is computed after the scaffolds are split at their gaps.

## Examples and non-examples

**A small assembly.** Let the contig lengths be 100, 40, 30, 30, 20, 20, 10, 10, 10, 10, so $T = 280$, and let the genome size be $G = 300$.

| $j$ | $\ell_j$ | running sum |
|---|---|---|
| 1 | 100 | 100 |
| 2 | 40 | 140 |
| 3 | 30 | 170 |
| 4 | 30 | 200 |

- N50: half of the assembly is 140. The running sum reaches 140 at $j = 2$, so $\text{N50} = 40$ and $\text{L50} = 2$.
- NG50: half of the genome is 150. The running sum reaches 150 at $j = 3$, so $\text{NG50} = 30$.
- N90: 90% of 280 is 252, reached at $j = 8$, so $\text{N90} = 10$.

**Pitfall 1: misjoins raise N50.** Suppose the assembler joins the contigs of length 40 and 30 into one contig of length 70, although they are not neighbors in the genome. The lengths become 100, 70, 30, 20, 20, 10, 10, 10, 10. The total is still 280, and now N50 = 70 and NG50 = 70. The assembly got worse and both numbers grew. A contig that crosses a [repeat](/genome-repeat/) by a wrong guess has the same effect. QUAST answers this with NGA50: it aligns the contigs to a reference, breaks them at each misassembly, and computes NG50 of the aligned blocks.

**Pitfall 2: dropping short contigs raises N50.** Remove all contigs shorter than 30. The lengths become 100, 40, 30, 30, with $T = 200$. Half is 100, reached at $j = 1$, so N50 = 100. The assembly lost 80 bases and its N50 grew from 40 to 100. NG50 does not change: it is still 30, because $G$ did not change. This is the main reason to prefer NG50 when $G$ is known.

**Pitfall 3: NG50 may not exist.** Contigs of lengths 80 and 70 from a genome of size $G = 400$ hold 150 bases, less than $G/2 = 200$. NG50 is not defined.

**Non-examples.**

- The mean contig length (28 in the small assembly) is not N50. Neither is the median contig length (20).
- N50 is not a measure of correctness. Two assemblies with the same N50 can have different numbers of errors.
- N50 of the reads, sometimes given for long-read data, uses the same formula on read lengths. It describes the input, not an assembly.

## Related definitions

- **[Contig](/contig/)** and **[scaffold](/scaffold/)**: the objects whose lengths go into N50.
- **L50 and LG50**: the number of contigs needed to reach half of the assembly or half of the genome.
- **NA50 and NGA50**: N50 and NG50 of the aligned blocks, after contigs are broken at misassemblies.
- **[Assembly quality assessment](/assembly-quality-assessment/)**: the full set of measures, including misassemblies, mismatch rates and gene completeness, of which N50 is one.

## References
