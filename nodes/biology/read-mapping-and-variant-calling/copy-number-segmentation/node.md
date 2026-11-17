---
tag: 62DJV1
kind: problem
slug: copy-number-segmentation
name: Copy number segmentation
aliases:
- CNV segmentation
area: biology/read-mapping-and-variant-calling
level: core
summary: Split a noisy sequence of log ratios along a chromosome into segments of constant copy number, each with its own mean.
prereqs: [change-point-detection, segmented-least-squares]
see_also: [circular-binary-segmentation, hmm-copy-number-calling, read-depth-copy-number-analysis, binary-segmentation, pelt-algorithm, cusum, structural-variant-detection, somatic-variant-calling]
sources:
  - paper: doi:10.1093/biostatistics/kxh008
    title: Adam B. Olshen, E. S. Venkatraman, Robert Lucito and Michael Wigler, Circular binary segmentation for the analysis of array-based DNA copy number data, Biostatistics 5(4), 2004
    locator: the statement of the segmentation problem for array CGH and the method of circular binary segmentation
  - paper: doi:10.1016/j.jmva.2004.02.008
    title: Jane Fridlyand, Antoine M. Snijders, Dan Pinkel, Donna G. Albertson and Ajay N. Jain, Hidden Markov models approach to the analysis of array CGH data, Journal of Multivariate Analysis 90(1), 2004
    locator: pp. 132 to 153 (segmentation of copy number by a hidden Markov model with one state for each level)
  - paper: doi:10.1186/1471-2105-6-27
    title: Franck Picard, Stephane Robin, Marc Lavielle, Christian Vaisse and Jean-Jacques Daudin, A statistical approach for array CGH data analysis, BMC Bioinformatics 6, 2005
    locator: the sections on the least squares segmentation by dynamic programming and the choice of the number of segments
  - paper: doi:10.1080/01621459.2012.737745
    title: Rebecca Killick, Paul Fearnhead and Idris A. Eckley, Optimal detection of changepoints with a linear computational cost, Journal of the American Statistical Association 107(500), 2012
    locator: the sections on the penalized cost and the pruning rule of PELT
---

Copy number segmentation takes a sequence of measurements of DNA copy number along a chromosome, such as log ratios of read depth or of array intensities, and splits it into stretches where the true copy number is constant. Each stretch, a *segment*, gets its own mean, and the places between segments are the *change points*, the approximate breakpoints of gains and losses. The data are noisy and the changes are few, so the problem is to find a few change points that explain the data well without fitting the noise. It is the [change point problem](/change-point-detection/) for a change in the mean, applied to genomes. With the least squares cost, the best fit with $k$ segments is found exactly by dynamic programming in $O(n^2 k)$ time; heuristics such as [CBS](/circular-binary-segmentation/) and [HMMs](/hmm-copy-number-calling/) are faster or give more.

## In plain words

You walk along a chromosome and, at each step, measure how many copies of the DNA are there. The measure is noisy: it goes up and down a little even where nothing changes.

The true copy number is a staircase. It stays flat for long stretches and jumps at a few places. The task is to draw that staircase through the noisy points. Drawing a step at every point fits perfectly but means nothing, and drawing one flat line misses the real jumps. A good answer has few steps and stays close to the points.

## Definition

**Input.** Values $x_1, \ldots, x_n$ in the order of their positions on one chromosome, usually $\log_2$ of the ratio of the observed and the expected depth of each window, after the corrections of [read-depth analysis](/read-depth-copy-number-analysis/).

**Model.** $x_t = \mu_t + \varepsilon_t$, where $\mu$ is piecewise constant and $\varepsilon$ is noise with mean 0. A segmentation with $k$ segments is a list of change points $0 = \tau_0 < \tau_1 < \cdots < \tau_k = n$, and segment $j$ holds the points $\tau_{j-1} + 1, \ldots, \tau_j$.

**The least squares form.** For a fixed $k$, find the change points that minimize

$$F_k = \sum_{j=1}^{k} \sum_{t = \tau_{j-1} + 1}^{\tau_j} (x_t - \bar x_j)^2,$$

where $\bar x_j$ is the mean of segment $j$. This is the maximum likelihood fit for normal noise with one variance.

**The penalized form.** With $k$ unknown, minimize $F_k + \beta k$ over all $k$, with a penalty $\beta > 0$ for each segment. The penalty sets the balance between fit and number of segments, and choosing it is part of the problem.

## Variants

- **Integer states.** Ask not only for segments but for an integer copy number of each, as the [HMM approach](/hmm-copy-number-calling/) does.
- **Several samples.** Find change points shared by many samples, or by the tumor and its normal sample.
- **Allele fractions.** Segment the depth and the fraction of reads with each allele at heterozygous sites together, which shows a copy-neutral loss of heterozygosity.
- **Other noise models.** A Poisson or negative binomial cost on the raw counts in place of least squares on log ratios.
- **Tumors.** In a tumor, the levels depend on the purity and the ploidy of the sample, and the segment means do not lie at the levels of a diploid genome.

## Examples

Twelve values, from the [CBS](/circular-binary-segmentation/) page:

$$x = (0.1, -0.2, 0.0, 0.2, -0.1, 1.1, 0.9, 1.0, 1.2, 0.0, -0.1, 0.1).$$

The exact least squares optimum for each $k$, with change points given as the index of the first point of each new segment, counted from 0:

| $k$ | $F_k$ | change points |
|---|---|---|
| 1 | 3.110 | none |
| 2 | 2.060 | 5 |
| 3 | 0.170 | 5, 9 |
| 4 | 0.140 | 5, 8, 9 |
| 5 | 0.117 | 1, 2, 5, 9 |

The drop from $k = 2$ to $k = 3$ is large and the later drops are small, so three segments, with means 0.0, 1.05 and 0.0, explain the data. Among $k \le 5$, the penalized cost $F_k + \beta k$ chooses $k = 3$ for every $\beta$ from about 0.03 to 1.47. Note that the best fit with two segments is poor: a single change point cannot describe a gain in the middle of the chromosome, which is why [binary segmentation](/binary-segmentation/) with one split per test does badly here and CBS tests arcs.

## Known algorithms

| method | page | result | time |
|---|---|---|---|
| dynamic programming over the last change point | [segmented least squares](/segmented-least-squares/) | exact optimum $F_k$ for each $k$ up to a given one | $O(n^2 k)$ |
| PELT | [PELT](/pelt-algorithm/) | exact optimum of the penalized form | $O(n^2)$ worst case, $O(n)$ expected when the number of change points grows in proportion to $n$ |
| binary segmentation | [binary segmentation](/binary-segmentation/) | heuristic, one change point per split | $O(n \log n)$ typical |
| circular binary segmentation | [CBS](/circular-binary-segmentation/) | heuristic, splits tested by permutations | $O(N n^2)$ per test with $N$ permutations |
| hidden Markov model | [HMM copy number calling](/hmm-copy-number-calling/) | exact most probable path of states under the model | $\Theta(K^2 n)$ for $K$ states |

The dynamic program uses prefix sums of $x$ and $x^2$, which give the cost of any segment in $O(1)$, and the recurrence $F_k(j) = \min_i (F_{k-1}(i) + \mathrm{cost}(i, j))$ over the end of the previous segment. Picard et al. (2005) used it for array CGH, with a rule to choose $k$.

## Bounds

- **Exact in polynomial time.** Both the fixed-$k$ and the penalized forms have exact polynomial algorithms, so the problem is not hard in the sense of complexity; the hard part is the statistics, the choice of $k$ or $\beta$ and a noise model that fits.
- **Detection.** A change of size $\delta$ over a segment of $m$ points in noise of standard deviation $\sigma$ gives a test statistic of about $\delta \sqrt{m} / \sigma$, so a short or small change is lost in the noise. Read depth with more reads per window lowers $\sigma$ but makes the windows longer.
- **Resolution.** A change point is placed only to within a window, and the true breakpoint lies somewhere between two measurements.
- **Correlated noise.** Waves in the depth from GC content make the noise correlated along the genome, which breaks the independence that both the tests and the penalties assume.

## Reductions

- **From structural variants.** The depth signal of [structural variant detection](/structural-variant-detection/) reduces to this problem.
- **To shortest paths.** The fixed-$k$ problem is a shortest path with $k$ edges in the directed acyclic graph on $0, \ldots, n$ with an edge of weight $\mathrm{cost}(i, j)$ for each $i < j$.
- **To decoding an HMM.** With a fixed set of levels and a penalty for each change, the penalized form becomes Viterbi decoding of an HMM with one state for each level.

## Applications

- **Cancer genomics.** Gains and losses of chromosome arms and of focal regions, and the genes in them.
- **Germline copy number variants.** Deletions and duplications in the genomes of patients with developmental disorders.
- **Arrays and sequencing.** The same methods run on array CGH, SNP arrays, and read depth from exome and whole-genome sequencing.
- **Single cells.** The copy number profiles of single tumor cells, from very low depth.

## References
