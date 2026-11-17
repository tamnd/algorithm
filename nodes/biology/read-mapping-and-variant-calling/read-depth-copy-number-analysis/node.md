---
tag: K5DFVM
kind: technique
slug: read-depth-copy-number-analysis
name: Read-depth copy number analysis
aliases:
- read depth method
area: biology/read-mapping-and-variant-calling
level: advanced
summary: Count reads in windows, correct for GC content and mappability, and turn the normalized depth into copy number along the genome.
prereqs: [structural-variant-detection, sequencing-coverage, copy-number-segmentation]
see_also: [circular-binary-segmentation, hmm-copy-number-calling, discordant-read-pair-method, split-read-method, poisson-distribution, mapping-quality, duplicate-read-marking, somatic-variant-calling]
sources:
  - paper: doi:10.1101/gr.092981.109
    title: Seungtai Yoon, Zhenyu Xuan, Vladimir Makarov, Kenny Ye and Jonathan Sebat, Sensitive and accurate detection of copy number variants using read depth of coverage, Genome Research 19(9), 2009
    locator: pp. 1586 to 1592 (the counts in windows, the correction for GC content, and the event-wise testing of runs of windows)
  - paper: doi:10.1101/gr.114876.110
    title: Alexej Abyzov, Alexander E. Urban, Michael Snyder and Mark Gerstein, CNVnator, an approach to discover, genotype, and characterize typical and atypical CNVs from family and population genome sequencing, Genome Research 21(6), 2011
    locator: the sections on the bins of read depth, the correction for GC content and the segmentation by mean shift
  - paper: doi:10.1038/nrg2958
    title: Can Alkan, Bradley P. Coe and Evan E. Eichler, Genome structural variation discovery and genotyping, Nature Reviews Genetics 12(5), 2011
    locator: the section on read-depth methods and their limits
---

Read-depth copy number analysis estimates how many copies of each part of the genome a sample has from the number of reads that map there. If sequencing samples the genome evenly, a region with one copy gets half the reads of a region with two copies, and a region with three copies gets one and a half times as many. The technique counts the reads in windows along the genome, removes the known biases of the depth, turns the counts into ratios to the expected depth, and then segments the ratios into stretches of constant copy number. It finds deletions and duplications and their copy number, but not balanced events such as inversions, and it gives breakpoints only to within a window. It is the depth signal of [structural variant detection](/structural-variant-detection/).

## In plain words

Sequencing throws many short reads at random onto the genome, like rain on a road. Where the road is twice as wide, twice as much rain falls.

So cut the genome into pieces of the same length and count the reads in each. A piece with fewer reads than usual has lost a copy, and a piece with more has gained one. Some pieces always get a little more or less, for reasons that have nothing to do with copies, so correct for those first. Then look for long stretches of pieces that are all high or all low, because one odd piece is often just noise.

## When it applies

- **Even sampling.** The reads come from a random sample of the genome, as in whole-genome sequencing, so that depth is proportional to copy number after correction. With exome or other targeted data, each target has its own capture efficiency, and the depth must be compared with the same target in other samples.
- **Events that change copy number.** Deletions, duplications and amplifications. Inversions, balanced translocations and insertions of new sequence leave the depth unchanged.
- **Events of many windows.** The method needs enough reads per event to rise above the noise, so it works for events of thousands of bases or more at typical coverage, and for smaller events only at high coverage.
- **Mappable sequence.** Reads must be placed uniquely, so the method cannot see inside long repeats.

## The template

```pseudo id=main
READ-DEPTH-CNV(reads, ref, w)
L1  cut the genome into windows of w bases; drop the windows of low mappability
L2  r_i ← the number of reads with good mapping quality that start in window i
L3  for each GC bin b: m_b ← the median of r_i over the windows in bin b
L4  r̃_i ← r_i · m / m_b(i), where m is the median of all r_i and b(i) the GC bin of window i
L5  y_i ← log2(r̃_i / m), or the log ratio to a control sample
L6  segments ← SEGMENT(y), by CBS, an HMM or a test of runs of windows
L7  for each segment: copy number ← 2 · 2^(mean of y), for a diploid genome
L8  return the segments whose copy number is not 2
```

Line L4 is the correction for GC content of Yoon et al. (2009): windows with the same share of G and C bases should have the same depth, so each count is scaled by the ratio of the overall median to the median of its GC bin. Line L5 assumes that most of the genome has two copies, so the median count is the depth of two copies. Line L6 is a [copy number segmentation](/copy-number-segmentation/) problem, solved by [CBS](/circular-binary-segmentation/), by an [HMM](/hmm-copy-number-calling/) with one state for each copy number, or by the event-wise testing of Yoon et al., which tests runs of windows with a significance level corrected for the number of runs.

**The size of the windows.** If a window of two copies gets $\lambda$ reads on average, the count has a standard deviation of about $\sqrt{\lambda}$ under [Poisson](/poisson-distribution/) sampling, and the loss of one copy lowers it by $\lambda / 2$. At 30x coverage with reads of 100 bases, a window of 1000 bases gets about 300 reads. Its standard deviation is 17.3, and the loss of one copy is a drop of 150, or 8.7 standard deviations. A window of 100 bases gets 30 reads, and the drop is only 2.7 standard deviations. So larger windows give cleaner counts but coarser breakpoints, and real data have more noise than the Poisson law.

## Classic examples

**A worked example of GC correction.** Eight windows of 1000 bases, with a depth of about 300 reads for two copies. Windows with 60% GC get about 10% more reads in this library, and windows 4 and 5 have lost one copy:

| window | GC | count | corrected | $\log_2$ ratio | copy number |
|---|---|---|---|---|---|
| 0 | 0.4 | 298 | 300.0 | 0.000 | 2.00 |
| 1 | 0.4 | 305 | 307.0 | 0.033 | 2.05 |
| 2 | 0.6 | 331 | 303.7 | 0.018 | 2.02 |
| 3 | 0.6 | 327 | 300.0 | 0.000 | 2.00 |
| 4 | 0.4 | 151 | 152.0 | -0.981 | 1.01 |
| 5 | 0.6 | 166 | 152.3 | -0.978 | 1.02 |
| 6 | 0.4 | 302 | 304.0 | 0.019 | 2.03 |
| 7 | 0.4 | 296 | 298.0 | -0.010 | 1.99 |

The overall median is 300, the median of the windows with 40% GC is 298 and that of the windows with 60% GC is 327. Before the correction, windows 2 and 3 have log ratios of 0.142 and 0.124, and window 5 has $-0.854$, so the GC-rich windows look like part of a gain and the deletion looks uneven. After the correction, the two windows of the deletion agree, and segmentation finds one segment of copy number 1.

**Tools.**

- Yoon et al. (2009) introduced the GC correction of line L4 and the event-wise testing of runs of windows, and showed that read depth finds copy number variants with good sensitivity from whole-genome sequencing.
- CNVnator (Abyzov et al., 2011) corrects for GC content in a similar way and segments the depth with a mean-shift method, not an HMM.
- Exome tools such as XHMM compare the depth of each target with other samples, remove the systematic noise, and segment with an HMM.
- Cancer pipelines compute the log ratio of a tumor to its matched normal sample in each window, which cancels most biases, and segment it with CBS.

## Variations

- **A control sample.** The ratio of the sample to a control sequenced in the same way removes GC and mappability biases at once, but adds the noise of the control.
- **Allele fractions.** At heterozygous sites, the share of reads with each allele separates a copy-neutral loss of heterozygosity from no event, and two copies of one allele from one of each.
- **Purity and ploidy.** In a tumor, the log ratio of $c$ copies is $\log_2((\rho c + 2(1 - \rho)) / (\rho P + 2(1 - \rho)))$ for purity $\rho$ and average tumor ploidy $P$, so the levels are compressed toward zero and must be fitted jointly with $\rho$ and $P$.
- **Read pairs and split reads.** Combining the depth with [read pairs](/discordant-read-pair-method/) and [split reads](/split-read-method/) gives the exact breakpoints of the deletions and duplications that the depth finds.
- **Single cells.** Very low depth per cell and large windows give a profile of copy number for each cell.

## Pitfalls

- **GC and mappability waves.** Uncorrected, they make long waves in the depth that segmentation calls as gains and losses.
- **PCR duplicates.** Copies of one fragment add to the count without new information; [mark duplicates](/duplicate-read-marking/) before counting.
- **Reads in repeats.** Reads with low [mapping quality](/mapping-quality/) placed at random among the copies of a repeat blur the depth there; either filter them and lose the region or keep them and accept the noise.
- **The wrong baseline.** The median of the counts is the depth of two copies only when most of the genome has two copies. In a tumor with many changes, or on the sex chromosomes, the baseline must be chosen in another way.
- **Breakpoints.** The edges of a segment are known only to within a window. Do not report them as exact.
- **Overdispersion.** Real counts vary more than a Poisson law allows, so tests that assume it call too many small events.

## Exercises

1. At 30x coverage with reads of 150 bases, how long must a window be for the loss of one copy to lower its mean count by 5 Poisson standard deviations?
2. In the worked example, change the count of window 5 to 180 and recompute its corrected count and copy number. Does it still look like a deletion?
3. For a tumor with purity 0.5 and ploidy 2, compute the log ratio of 1, 3 and 4 copies with the formula in the variations, and compare them with the values for a pure sample.
4. Explain why a balanced inversion cannot be found from the depth, and name the signal that finds it.

## References
