---
tag: 6NYYG1
kind: algorithm
slug: circular-binary-segmentation
name: Circular binary segmentation
aliases:
- CBS segmentation
area: biology/read-mapping-and-variant-calling
level: core
summary: Split a sequence where a permutation test finds an arc of changed mean, the largest arc t-statistic on a circle, then repeat on each part (Olshen and Venkatraman).
solves: [copy-number-segmentation]
model: real-ram
complexity:
  vars: {n: the number of points, N: the number of permutations per test}
  time: {worst: O(N n^3), per_test: O(N n^2)}
  space: {extra: O(n)}
properties: {deterministic: false, exact: false, online: false, recursive: true}
history:
  year: 2004
  people: [Adam B. Olshen, E. S. Venkatraman, Robert Lucito, Michael Wigler]
  note: Olshen et al. proposed CBS for array CGH data in 2004, and Venkatraman and Olshen (2007) made it fast with an early stop of the permutations and a tail approximation, in the DNAcopy package.
prereqs: [copy-number-segmentation, binary-segmentation, permutation-test]
see_also: [change-point-detection, hmm-copy-number-calling, read-depth-copy-number-analysis, student-t-test, segmented-least-squares, pelt-algorithm, cusum, false-discovery-rate]
sources:
  - paper: doi:10.1093/biostatistics/kxh008
    title: Adam B. Olshen, E. S. Venkatraman, Robert Lucito and Michael Wigler, Circular binary segmentation for the analysis of array-based DNA copy number data, Biostatistics 5(4), 2004
    locator: the sections on the method (the maximal t-statistic over arcs, the permutation reference distribution and the recursive splitting)
  - paper: doi:10.1093/bioinformatics/btl646
    title: E. S. Venkatraman and Adam B. Olshen, A faster circular binary segmentation algorithm for the analysis of array CGH data, Bioinformatics 23(6), 2007
    locator: the sections on the early stopping of the permutations and on the approximation of the tail probability
  - paper: doi:10.1016/j.jmva.2004.02.008
    title: Jane Fridlyand, Antoine M. Snijders, Dan Pinkel, Donna G. Albertson and Ajay N. Jain, Hidden Markov models approach to the analysis of array CGH data, Journal of Multivariate Analysis 90(1), 2004
    locator: pp. 132 to 153, an HMM segmentation of the same data, for comparison
---

Circular binary segmentation (CBS) splits a noisy sequence of numbers along a chromosome, such as log ratios of read depth, into segments of constant mean. It bends each segment into a circle and looks for the arc whose mean differs most from the rest, measured by a t-statistic. If a [permutation test](/permutation-test/) says the difference is real, it cuts the segment at the two ends of the arc and repeats on each part. The circle lets one test find a short change in the middle of a segment, which a split into two parts finds badly. Olshen, Venkatraman, Lucito and Wigler proposed it in 2004 for array CGH, and it is the default [copy number segmentation](/copy-number-segmentation/) method of the DNAcopy package.

## In plain words

You have a long row of numbers that jump up or down at a few places, with noise on top. You want to find the jumps.

Join the two ends of the row so that it makes a ring. Try every stretch of the ring, and for each one, compare the average inside with the average outside, scaled by how much noise there is. Take the stretch with the biggest difference.

To see if that difference is real, shuffle the numbers many times and do the same search on each shuffle. If almost no shuffle gives a difference as big, cut the row at the two ends of the stretch. Then do the same on each piece, until no piece gives a real difference.

## The problem

Given $x_1, \ldots, x_n$ with $x_t = \mu_t + \varepsilon_t$, where $\mu$ is piecewise constant with a few change points and $\varepsilon$ is noise, find the change points. CBS answers this with a sequence of tests, not by fitting a model with a known number of segments. See [copy number segmentation](/copy-number-segmentation/) for the problem and its exact solution by dynamic programming.

For a segment $y$ of length $n$, an arc $a$ is a set of positions that are consecutive on the circle, with $k$ positions, $1 \le k \le n - 1$. With $s$ the sample standard deviation of $y$, the arc statistic and the test statistic are

$$Z(a) = \frac{|\bar y_a - \bar y_{\bar a}|}{s\sqrt{1/k + 1/(n - k)}}, \qquad T = \max_a Z(a).$$

An arc that starts at the first position, or ends at the last, is one change point, as in [binary segmentation](/binary-segmentation/). Any other arc is two change points.

## The algorithm

```pseudo id=main
CBS(x, α, N)
L1  stack ← [(0, n)]; cuts ← empty
L2  while stack is not empty do
L3      (lo, hi) ← POP(stack)
L4      y ← x[lo..hi)
L5      (T, i, j) ← MAX-ARC(y)
L6      count ← the number of N random permutations π of y with MAX-ARC(π(y)).T ≥ T
L7      p ← (count + 1) / (N + 1)
L8      if p ≤ α then
L9          add lo + i and lo + j to cuts, the ones strictly inside (lo, hi)
L10         push the two or three parts of y onto the stack
L11 return the sorted cuts
```

Segments are half-open, and a segment with fewer than 2 points or a constant one is not tested. MAX-ARC scans every interval with prefix sums. By symmetry, the complement of an interval has the same $Z$, and every arc is an interval or the complement of one, so the scan over intervals covers every arc on the circle.

```pseudo id=max-arc
MAX-ARC(y)
L12 S[0] ← 0; S[t + 1] ← S[t] + y[t] for t = 0, ..., n - 1
L13 s ← the sample standard deviation of y
L14 for each i < j with 1 ≤ j - i ≤ n - 1 do
L15     d ← (S[j] - S[i]) / k - (S[n] - S[j] + S[i]) / (n - k), with k = j - i
L16     Z(i, j) ← |d| / (s sqrt(1/k + 1/(n - k)))
L17 return the largest Z(i, j) and the first (i, j) that reaches it
```

The test at line L6 needs no model of the noise. A permutation does not change $s$, so all the statistics in one test use the same scale, and the p-value of line L7 is valid for exchangeable data, such as independent values with one distribution. The code uses a fixed order of the segments (the left part first) and one random generator, so a seed gives the same result each time.

## Example

Twelve values: five near 0, four near 1 and three near 0.

$$x = (0.1, -0.2, 0.0, 0.2, -0.1, \mathbf{1.1, 0.9, 1.0, 1.2}, 0.0, -0.1, 0.1)$$

The standard deviation is $s = 0.5317$. MAX-ARC finds the arc $[5, 9)$, the four high values, with mean 1.05 against 0.0 outside:

$$Z = \frac{1.05}{0.5317 \sqrt{1/4 + 1/8}} = 3.2247.$$

The best single split, at position 5, gives only $Z = 1.93$, because the values after the high stretch drop back and pull the right mean down. This is why CBS uses arcs.

For the exact p-value, put the twelve values on the circle in a random order. The four high values form one arc in 12 of the $\binom{12}{4} = 495$ ways to choose their four positions, and those placements give $T \ge 3.2247$. A search over all other placements found that their largest $Z$ is 2.918. So the exact p-value is $12/495 = 0.0242$. One run of the code with $N = 999$ permutations gave $p = 0.037$.

At $\alpha = 0.05$, CBS cuts at 5 and 9. The three parts give $T = 1.41$, $1.55$ and $1.22$, and none of them passes the test, so the result is the segments $[0, 5)$, $[5, 9)$ and $[9, 12)$ with means 0.0, 1.05 and 0.0. A search over all ways to cut 12 points into 3 segments gives the same cuts as the least squares optimum. At $\alpha = 0.01$, CBS returns no cut, because the exact p-value of the strongest arc is 0.0242.

## Correctness

MAX-ARC is exact. Line L12 makes the sum of every interval one subtraction, lines L15 and L16 are the definition of $Z$, and because $Z(a) = Z(\bar a)$ and every arc on the circle is an interval or the complement of one, the scan of line L14 covers all arcs. The test is valid: if the values are exchangeable under the null hypothesis, then the observed $T$ and the $N$ shuffled values are exchangeable, and the rank argument gives $P(p \le \alpha) \le \alpha$ for the p-value of line L7. This holds for any $N$ and does not need normal noise.

That is a statement about each test. CBS as a whole is a heuristic for the segmentation problem: it does not minimize any stated objective, its tests are chosen from the data, and $\alpha$ is a threshold per test, not an error rate for the whole result. The full proofs of the two lemmas are in proofs/correctness.md.

## Complexity

- **One test.** MAX-ARC visits $n(n + 1)/2 - 1$ intervals at $O(1)$ each, so it is $\Theta(n^2)$. A test with $N$ permutations is $\Theta(N n^2)$.
- **The recursion.** Segments at one depth of the recursion do not overlap, so the tests at one depth cost $O(N n^2)$ in total. The depth is at most the number of splits, so the worst case is $O(N n^3)$. With a few change points that split the data into balanced parts, the cost is close to that of the first test.
- **The fast version.** Venkatraman and Olshen (2007) stop the permutations early when the p-value is clearly large, and replace most permutations by an approximation of the tail probability, which made CBS practical for arrays with many probes.
- **Space.** $O(n)$ for the prefix sums, the copy of a segment and the stack.

## Properties

- **Not exact.** CBS is a heuristic for segmentation; only MAX-ARC and the validity of each test are theorems.
- **Randomized.** The p-values come from random permutations, so two runs with different seeds can differ at a borderline split.
- **Nonparametric test.** The permutation test needs exchangeable noise, not normal noise. Correlated noise along the genome breaks this, and then the test splits too often.
- **Top down.** Each split is final; a wrong early cut is not undone.
- **No number of segments needed.** The number of segments comes from $\alpha$, not from the user.

## Variants and improvements

- **Pruning of splits.** DNAcopy can undo splits whose parts differ by less than a set number of standard deviations (undo.splits), which removes small segments caused by noise.
- **Minimum width.** An arc must have at least a set number of points, so that one outlier does not make a segment.
- **Smoothing of outliers.** Single extreme points are pulled toward their neighbors before segmentation.
- **Weights.** Points with more reads or better probes can count more.
- **Other segmenters.** [Binary segmentation](/binary-segmentation/) with one change point per test, [PELT](/pelt-algorithm/) for an exact penalized fit in about linear time, and the [HMM approach](/hmm-copy-number-calling/), which gives each segment a copy number state.

## When to use it

Use CBS to segment log ratios of copy number along a chromosome, from arrays or from [read depth](/read-depth-copy-number-analysis/) in windows, when you do not know the number of segments and want a method with few settings. It is the standard in many cancer pipelines and is robust to the shape of the noise. If you need integer copy numbers, call them after CBS or use an HMM. If you need the least squares optimum for a given number of segments or a penalty, use the [exact dynamic program](/copy-number-segmentation/) or PELT.

## Pitfalls

- **Too few points.** For a stretch of $k$ high points among $n$, the exact p-value is at least about $n / \binom{n}{k}$, the share of placements where the high points form an arc. In the example this is $12/495$, so the change is lost at $\alpha = 0.01$.
- **Uncorrected depth.** GC content and mappability make waves in read depth. CBS cuts them into many segments that are not real.
- **Correlated noise.** Neighboring windows that share reads are not exchangeable, so the p-values are too small.
- **$\alpha$ is per test.** With many tests along a genome, some false cuts are expected at any $\alpha$.
- **Too few permutations.** With $N$ permutations the smallest p-value is $1/(N + 1)$, so $\alpha$ below that can never pass.

## Implementations

## History

Olshen, Venkatraman, Lucito and Wigler (2004) proposed CBS for array comparative genomic hybridization (array CGH), as a change to binary segmentation that tests for arcs. In the same year Fridlyand et al. (2004) segmented the same kind of data with a hidden Markov model. Venkatraman and Olshen (2007) made CBS fast for arrays with many probes, and the DNAcopy package of Bioconductor made it a standard step in copy number analysis. It was later used for read depth from sequencing.

## References
