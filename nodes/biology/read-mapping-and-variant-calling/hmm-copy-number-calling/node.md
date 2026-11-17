---
tag: HP6C4B
kind: algorithm
slug: hmm-copy-number-calling
name: HMM copy number calling
aliases:
- hidden Markov model CNV calling
area: biology/read-mapping-and-variant-calling
level: advanced
summary: Model the copy number of each window as the hidden state of a Markov chain along the genome, emit the read depth from it, and decode the states with Viterbi.
solves: [copy-number-segmentation]
model: real-ram
complexity:
  vars: {n: the number of windows, K: the number of copy number states}
  time: {worst: Θ(K^2 n), average: Θ(K^2 n), best: Θ(K^2 n)}
  space: {extra: Θ(K n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2004
  people: [Jane Fridlyand, Antoine M. Snijders, Dan Pinkel, Donna G. Albertson, Ajay N. Jain]
  note: Fridlyand et al. segmented array CGH data with a hidden Markov model whose states are copy number levels. PennCNV (Wang et al. 2007) used an HMM with copy number states for SNP arrays, and the same model was later applied to read depth.
prereqs: [hidden-markov-model, viterbi-algorithm, copy-number-segmentation]
see_also: [forward-backward-algorithm, baum-welch-algorithm, circular-binary-segmentation, read-depth-copy-number-analysis, poisson-distribution, log-sum-exp-trick, hidden-semi-markov-model, structural-variant-detection]
sources:
  - paper: doi:10.1016/j.jmva.2004.02.008
    title: Jane Fridlyand, Antoine M. Snijders, Dan Pinkel, Donna G. Albertson and Ajay N. Jain, Hidden Markov models approach to the analysis of array CGH data, Journal of Multivariate Analysis 90(1), 2004
    locator: pp. 132 to 153 (an HMM along each chromosome with states for copy number levels, fitted by EM and decoded by Viterbi)
  - paper: doi:10.1101/gr.6861907
    title: Kai Wang, Mingyao Li, Dexter Hadley and others, PennCNV, an integrated hidden Markov model designed for high-resolution copy number variation detection in whole-genome SNP genotyping data, Genome Research 17(11), 2007
    locator: the sections on the hidden states of copy number, the emissions of the log R ratio and the B allele frequency, and the transitions
  - paper: doi:10.1109/5.18626
    title: Lawrence R. Rabiner, A tutorial on hidden Markov models and selected applications in speech recognition, Proceedings of the IEEE 77(2), 1989
    locator: the sections on the forward procedure and the Viterbi algorithm
---

HMM copy number calling turns the read depth along a chromosome into an integer copy number for each window. It treats the copy number as the hidden state of a [hidden Markov model](/hidden-markov-model/): the state stays the same from one window to the next with high probability, and each state emits read counts around its own mean. The [Viterbi algorithm](/viterbi-algorithm/) finds the most probable sequence of states, which gives the segments and their copy numbers at once. The cost is $\Theta(K^2 n)$ for $K$ states and $n$ windows. Fridlyand et al. (2004) used this approach for array CGH, PennCNV (2007) for SNP arrays, and tools such as XHMM use it for read depth from exome sequencing.

## In plain words

Cut the genome into windows of the same size and count the reads that land in each one. A normal window has two copies of its DNA and gets some usual number of reads. A window with one copy gets about half as many, and one with three copies about one and a half times as many.

The counts are noisy, so one low window is not enough. But copy number changes seldom, so the true answer is a few long stretches. The model scores every possible list of copy numbers: it rewards lists that fit the counts and punishes each change. A fast table search finds the list with the best score without trying them all.

## The problem

The input is a list of read counts $x_0, \ldots, x_{n-1}$, one for each window of the same size, after correction for GC content and mappability. The hidden copy numbers are $c_0, \ldots, c_{n-1}$ in $\{0, \ldots, K - 1\}$. The model of the code is:

- **Emission.** $x_t \mid c_t = c$ is Poisson with mean $\lambda \max(c, \varepsilon)/2$, where $\lambda$ is the mean count of a window with two copies and $\varepsilon > 0$ allows a few misplaced reads in a deleted region.
- **Transition.** $P(c_t = c_{t-1}) = 1 - p$, and each other state has probability $p/(K - 1)$.
- **Start.** Each state has probability $1/K$.

The task is to find $c^* = \arg\max_c P(x, c)$, the most probable path, and, if needed, the posterior $P(c_t = c \mid x)$ of each window. Without a given $\lambda$, the code takes the median count, which assumes that most of the chromosome has two copies.

## The algorithm

All values are logarithms, so that a long chromosome does not underflow. $E[t][c]$ is $\ln P(x_t \mid c)$ and $T[b][c]$ is $\ln P(c \mid b)$.

```pseudo id=main
HMM-CNV(x, K, λ, p)
L1  E[t][c] ← x_t ln μ_c - μ_c - ln(x_t!), with μ_c = λ max(c, ε)/2, for each t and c
L2  V[0][c] ← ln(1/K) + E[0][c] for each c
L3  for t ← 1 to n - 1 do
L4      for c ← 0 to K - 1 do
L5          V[t][c] ← max_b (V[t - 1][b] + T[b][c]) + E[t][c]
L6          ptr[t][c] ← the b that reaches the max, the smallest on ties
L7  c*[n - 1] ← the c with the largest V[n - 1][c], the smallest on ties
L8  for t ← n - 1 down to 1 do c*[t - 1] ← ptr[t][c*[t]]
L9  return c* and its runs of equal states as segments
```

$V[t][c]$ is the log probability of the best path that ends in state $c$ at window $t$, joint with the first $t + 1$ counts. The [forward algorithm](/forward-algorithm/) is the same table with the max of line L5 replaced by a sum, done with the [log-sum-exp trick](/log-sum-exp-trick/). With the [backward pass](/forward-backward-algorithm/), it gives the posterior of each state at each window.

## Example

Ten windows, with $\lambda = 20$, $K = 4$ states (0 to 3 copies) and $p = 0.1$:

$$x = (19, 22, 10, 8, 11, 20, 21, 32, 29, 31).$$

The state means are 0.5, 10, 20 and 30. Three rows of the emission table, $\ln P(x_t \mid c)$:

| window | count | $c = 0$ | $c = 1$ | $c = 2$ | $c = 3$ |
|---|---|---|---|---|---|
| 0 | 19 | -53.01 | -5.59 | **-2.42** | -4.72 |
| 2 | 10 | -22.54 | **-2.08** | -5.15 | -11.09 |
| 7 | 32 | -104.24 | -17.88 | -5.69 | **-2.72** |

A change of state costs $\ln(0.1/3) = -3.40$ and staying costs $\ln 0.9 = -0.105$. The Viterbi path is

$$c^* = (2, 2, 1, 1, 1, 2, 2, 3, 3, 3),$$

with $\ln P(x, c^*) = -36.53$: a loss of one copy in windows 2 to 4 and a gain in windows 7 to 9. The forward algorithm gives $\ln P(x) = -35.48$, so this one path has about 35% of the probability of the data.

The posteriors show where the path is unsure. At window 5, $P(c = 2 \mid x) = 0.574$. At window 6, $P(c = 2 \mid x) = 0.485$ and $P(c = 3 \mid x) = 0.512$, so the state with the largest posterior there is 3, while the best path has 2. Each window can be decoded on its own, but the path of those choices need not be the best path.

With $p = 0.05$, a change costs more, and the path becomes $(2, 2, 1, 1, 1, 3, 3, 3, 3, 3)$: one jump from 1 to 3 at window 5 costs less than two jumps, even though counts of 20 and 21 fit 2 copies better. Its log probability is $-37.62$, against $-38.29$ for the path with the 2-copy stretch. The value of $p$ sets the shortest segment that the method can call.

## Correctness

By induction on $t$, $V[t][c]$ is the largest $\ln P(x_0, \ldots, x_t, c_0, \ldots, c_t)$ over the paths with $c_t = c$: the joint probability of a path is the product of its start, transitions and emissions, so the best path into $c$ at $t$ is the best path into some $b$ at $t - 1$ plus one step, which is line L5. Line L6 stores the $b$, and lines L7 and L8 follow the pointers back from the best last state, which gives a path with the largest joint probability. The forward table is the same induction with sums. The proofs are in proofs/correctness.md, and the tests check both against a search over all $K^n$ paths for small cases. The decoding is exact for the model; the model itself is an approximation of real read depth.

## Complexity

- **Time.** Line L1 is $\Theta(K n)$. Each window does $K$ maximizations over $K$ states, so the Viterbi pass is $\Theta(K^2 n)$, and so are the forward and backward passes.
- **A faster step.** With the transition matrix of this page, the best predecessor of $c$ is $c$ itself or the best other state, so one step can be done in $\Theta(K)$ with the two largest values of $V$, for $\Theta(K n)$ in total. The code keeps the general loop.
- **Space.** The back pointers take $\Theta(K n)$. The forward and backward tables take $\Theta(K n)$ for posteriors.
- **Training.** If $\lambda$, $p$ or the emissions are learned with [Baum-Welch](/baum-welch-algorithm/), each iteration costs one forward and one backward pass, $\Theta(K^2 n)$, and the number of iterations depends on the data.

## Properties

- **Exact for its model.** Viterbi returns a most probable path, and forward returns $P(x)$, both theorems up to rounding.
- **Integer states.** The output is a copy number, not only a segment mean, which is what [CBS](/circular-binary-segmentation/) gives.
- **One smoothing parameter.** The transition probability $p$ acts as a penalty for each change point.
- **Geometric segment lengths.** A Markov chain gives segment lengths with a geometric distribution, which is a poor fit for real copy number changes; a [hidden semi-Markov model](/hidden-semi-markov-model/) allows other length distributions.

## Variants and improvements

- **B allele frequency.** At heterozygous SNPs, the fraction of reads with each allele shows 1:1 for two copies, 1:2 for three and 0:1 for a copy-neutral loss of heterozygosity. PennCNV emits both the intensity and this fraction from each state.
- **Overdispersion.** Read counts vary more than a Poisson law allows; a negative binomial emission is a better fit.
- **Tumor purity and ploidy.** In a tumor sample, the expected depth of copy number $c$ is a mix of the tumor and the normal cells, so the means of the states depend on the purity, which is estimated with the states.
- **Distance-dependent transitions.** If the windows or probes are not evenly spaced, the probability of a change can grow with the distance.
- **Exome data.** XHMM and similar tools use an HMM over the depth of exome targets, after removing systematic noise with principal components.

## When to use it

Use an HMM when you want integer copy numbers directly, when you can state the expected depth of each state, or when you want to combine depth with allele fractions. It is a good fit for germline copy number variants, which have a few known states. For tumors with many subclonal levels, or when the noise is hard to model, [CBS](/circular-binary-segmentation/) followed by a separate calling step is a common choice.

## Pitfalls

- **The diploid level.** Setting $\lambda$ to the median count is wrong when most of the chromosome is not diploid, as in many tumors.
- **Uncorrected depth.** GC content and mappability bias make waves that the HMM calls as gains and losses.
- **Overconfident emissions.** A Poisson model with real, overdispersed counts makes each window look more certain than it is, and the path changes state too often.
- **The value of $p$.** It decides the smallest segment that can be called, as the example shows. It needs tuning or training.
- **Viterbi versus posteriors.** The best path can have windows whose most probable state is another one; report the posterior when the confidence of a call matters.

## Implementations

## History

Fridlyand, Snijders, Pinkel, Albertson and Jain (2004) segmented array CGH data with a hidden Markov model whose states are levels of copy number, fitted by expectation maximization and decoded by Viterbi. Wang et al. (2007) built PennCNV, which combines the log R ratio and the B allele frequency of SNP arrays in one HMM. With whole-genome and exome sequencing, the same model was applied to read depth in windows or exome targets, in tools such as XHMM.

## References
