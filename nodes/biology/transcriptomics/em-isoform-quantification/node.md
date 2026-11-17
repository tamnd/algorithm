---
tag: QSYASY
kind: algorithm
slug: em-isoform-quantification
name: EM isoform quantification
aliases:
- RSEM algorithm
area: biology/transcriptomics
level: core
summary: 'Estimate isoform abundances by EM: share each multi-mapping read among its transcripts in proportion to the current abundances, then re-estimate the abundances from the shares.'
solves: [transcript-abundance-estimation]
model: real-ram
complexity:
  vars: {m: the number of transcripts, R: "the total size of the equivalence classes, the sum of |e| over all classes", T: the number of iterations}
  time: {worst: O(T·(R+m))}
  space: {extra: O(m)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2010
  people: [Bo Li, Victor Ruotti, Ron M. Stewart, James A. Thomson, Colin N. Dewey]
  note: Li and others gave the read-level EM with a noise isoform and showed that its likelihood is concave. RSEM (2011) added effective lengths, TPM and Bayesian credibility intervals. kallisto and Salmon run the same EM on equivalence classes.
prereqs: [transcript-abundance-estimation, expectation-maximization, maximum-likelihood-estimation]
see_also: [pseudoalignment, selective-alignment, rpkm-and-fpkm, transcripts-per-million, jensens-inequality, kullback-leibler-divergence, gibbs-sampling, gaussian-mixture-model]
sources:
  - paper: doi:10.1093/bioinformatics/btp692
    title: Bo Li, Victor Ruotti, Ron M. Stewart, James A. Thomson and Colin N. Dewey, RNA-Seq gene expression estimation with read mapping uncertainty, Bioinformatics 26(4) (2010)
    locator: pp. 493 to 500, Section 2.2 (inference with the EM algorithm; the likelihood is concave; the plateau when isoforms cannot be told apart)
  - paper: doi:10.1186/1471-2105-12-323
    title: Bo Li and Colin N. Dewey, RSEM, accurate transcript quantification from RNA-Seq data with or without a reference genome, BMC Bioinformatics 12 (2011)
    locator: Article 323, Methods (the model, effective length, TPM and credibility intervals by Gibbs sampling)
  - paper: doi:10.1111/j.2517-6161.1977.tb01600.x
    title: A. P. Dempster, N. M. Laird and D. B. Rubin, Maximum likelihood from incomplete data via the EM algorithm, Journal of the Royal Statistical Society Series B 39(1) (1977)
    locator: pp. 1 to 22
  - paper: doi:10.1093/bioinformatics/btp113
    title: Hui Jiang and Wing Hung Wong, Statistical inferences for isoform expression in RNA-Seq, Bioinformatics 25(8) (2009)
    locator: pp. 1026 to 1032
  - paper: doi:10.1038/nbt.3519
    title: Nicolas L. Bray, Harold Pimentel, Páll Melsted and Lior Pachter, Near-optimal probabilistic RNA-seq quantification, Nature Biotechnology 34(5) (2016)
    locator: pp. 525 to 527 (the EM on equivalence classes)
  - paper: doi:10.1038/nmeth.4197
    title: Rob Patro, Geet Duggal, Michael I. Love, Rafael A. Irizarry and Carl Kingsford, Salmon provides fast and bias-aware quantification of transcript expression, Nature Methods 14(4) (2017)
    locator: pp. 417 to 419, Online Methods (online inference, then offline EM or variational Bayes on rich equivalence classes)
---

EM isoform quantification estimates how much of each transcript is in an RNA sample when many reads fit more than one transcript. The isoforms of a gene share exons, so a read from a shared exon cannot be given to one of them by its sequence alone. The [expectation-maximization](/expectation-maximization/) algorithm solves this with a loop: share each read among the transcripts it fits, in proportion to their current abundances and lengths, then set each abundance to the fraction of reads it received. Each round increases the likelihood of the reads. The likelihood is concave in the abundances, so a fixed point with no zero abundance is a global maximum, but the maximum is not always unique. This is the core of RSEM, and kallisto and Salmon run the same loop on [equivalence classes](/pseudoalignment/) of reads.

## In plain words

Two songs share the same chorus. You hear the chorus 40 times on the radio, the verse that only song A has 30 times, and the verse that only song B has 30 times. How many times was each song played?

You cannot tell which song each chorus came from. So you make a guess, for example that both songs were played equally often. With that guess you split the 40 choruses between the two songs. Now each song has a total, and the totals give you a better guess. Split the choruses again with the new guess, and repeat.

The guesses settle down quickly. A short song gives fewer pieces each time it plays, so the split also takes the length of each song into account.

## The problem

There are $m$ transcripts with ids $1, \ldots, m$ and effective lengths $\ell_t > 0$. The effective length is the number of positions where a fragment can start, often $\ell_t = \mathrm{len}_t - \mu + 1$ for a mean fragment length $\mu$. Each read was mapped by [pseudoalignment](/pseudoalignment/), [selective alignment](/selective-alignment/) or a [read mapper](/read-mapping/) to the set of transcripts it is compatible with. Reads with the same set form an *equivalence class* $e$, and $c_e$ is the number of reads in it. $N = \sum_e c_e$.

The model: a read comes from transcript $t$ with probability $\alpha_t$, and then from one of the $\ell_t$ start positions of $t$ with equal probability. The probability of a read in class $e$ is $\sum_{t \in e} \alpha_t / \ell_t$, so

$$\log L(\alpha) = \sum_e c_e \log \sum_{t \in e} \frac{\alpha_t}{\ell_t}.$$

The task is to find $\alpha$ in the simplex that maximizes $\log L$. This is the [maximum likelihood estimate](/maximum-likelihood-estimation/) of the mixture weights of a mixture whose components are fixed. The transcript fractions are $\tau_t = (\alpha_t / \ell_t) / \sum_u (\alpha_u / \ell_u)$, and [transcripts per million](/transcripts-per-million/) are $10^6 \tau_t$.

## The algorithm

The pseudocode numbers transcripts from 1; the code numbers them from 0.

```pseudo id=main
EM-ABUNDANCE(classes e with counts c_e, lengths ℓ, iterations T, tolerance ε)
L1  α_t ← 1/m for each transcript t
L2  for iter ← 1 to T do
L3      n_t ← 0 for each t
L4      for each class e do
L5          s ← Σ_{u in e} α_u / ℓ_u
L6          for each t in e: n_t ← n_t + c_e · (α_t / ℓ_t) / s
L7      α'_t ← n_t / N for each t
L8      if max_t |α'_t - α_t| < ε then return α'
L9      α ← α'
L10 return α
```

Lines L5 and L6 are the E step. The share $c_e (\alpha_t / \ell_t) / s$ is the expected number of reads of class $e$ that came from $t$, given the current $\alpha$. Line L7 is the M step: with the expected counts fixed, the best weights are the counts divided by $N$. Line L1 starts with every $\alpha_t > 0$. This matters, because a zero never becomes positive again in line L6.

The loop works on classes, not on reads. Reads with the same compatible set get the same share in line L6, so one class with count $c_e$ does the work of $c_e$ reads. In practice the number of classes is much smaller than the number of reads (a measurement, not a bound), so each round is fast.

## Example

Transcript A has effective length 1000 and transcript B has effective length 500. There are 100 reads: 30 fit only A, 30 fit only B, and 40 fit both. So the classes are $\{A\}$ with 30 reads, $\{A, B\}$ with 40 and $\{B\}$ with 30.

| round | $\alpha_A$ | $\alpha_B$ | shared reads given to A | $\log L$ |
|---|---|---|---|---|
| 0 (start) | 0.5000 | 0.5000 | 13.33 | -695.3513 |
| 1 | 0.4333 | 0.5667 | 11.06 | -694.1501 |
| 2 | 0.4106 | 0.5894 | 10.33 | -694.0105 |
| 3 | 0.4033 | 0.5967 | 10.10 | -693.9961 |
| 4 | 0.4010 | 0.5990 | 10.03 | -693.9946 |
| 5 | 0.4003 | 0.5997 | 10.01 | -693.9945 |

In round 0, line L5 gives $s = 0.5/1000 + 0.5/500 = 0.0015$, and line L6 gives A the share $0.0005 / 0.0015 = 1/3$ of the 40 shared reads, so $n_A = 30 + 13.33$ and $\alpha_A = 0.4333$. B is shorter, so at equal $\alpha$ each of its positions is twice as likely, and B gets two thirds of the shared reads. The values approach $\alpha = (0.4, 0.6)$, and with $\varepsilon = 10^{-10}$ line L8 stops after 19 rounds.

The limit is the maximum. With $\alpha_B = 1 - \alpha_A$, $\log L$ is $30 \log \alpha_A + 40 \log(2 - \alpha_A) + 30 \log(1 - \alpha_A)$ plus a constant, and its derivative $30/\alpha_A - 40/(2 - \alpha_A) - 30/(1 - \alpha_A)$ is $75 - 25 - 50 = 0$ at $\alpha_A = 0.4$. In transcript fractions, $\alpha_A / \ell_A = 0.0004$ and $\alpha_B / \ell_B = 0.0012$, so the TPM values are 250000 for A and 750000 for B. A has 40% of the reads but only 25% of the molecules, because it is twice as long.

## Correctness

[The proof](proofs/correctness.md) shows three facts. **Monotonicity (a theorem):** each round satisfies $\log L(\alpha') - \log L(\alpha) \ge N \cdot \mathrm{KL}(\alpha' \| \alpha) \ge 0$, by [Jensen's inequality](/jensens-inequality/) applied to each class, with equality only at a fixed point. **Global maximum (a theorem):** $\log L$ is concave, because each class adds the log of a linear function. At a fixed point with all $\alpha_t > 0$, every partial derivative equals $N$, so the tangent plane is flat on the simplex and the fixed point is a global maximum. Li, Ruotti, Stewart, Thomson and Dewey (2010) state the concavity and conclude that EM finds the maximum likelihood values. **Limits:** a fixed point with a zero can be far from the maximum, and two transcripts of the same length in the same classes give a whole segment of maxima, so the answer then depends on the start.

## Complexity

Let $R = \sum_e |e|$ be the total size of the classes. One round reads each class twice, in lines L5 and L6, and touches each transcript in lines L3, L7 and L8, so it costs $O(R + m)$ arithmetic operations in the real RAM. $T$ rounds cost $O(T (R + m))$. The extra space is $O(m)$ for $n$ and $\alpha'$, on top of the input.

The number of rounds is the weak part. EM converges linearly, and the rate is slow when two transcripts are nearly indistinguishable, because the likelihood is then almost flat along one direction. Tools stop on a relative change of the abundances, or after a fixed cap of rounds. Building the classes costs one pass over the reads, and a hash table of compatible sets, before the loop starts.

## Properties

- **Increases the likelihood every round** (a theorem, Section 2 of the proof).
- **Stays in the simplex.** Every iterate is a probability vector, with no projection step.
- **Exact at the limit only.** The output is an approximation after finitely many rounds; the limit of the likelihood values exists, but this page does not prove that the iterates converge.
- **Deterministic.** The uniform start fixes the result, also on a ridge of equal maxima.
- **Works on summaries.** Only the classes and their counts are used, not the reads.

## Variants and improvements

- **Read-level EM with a noise transcript.** Li and others (2010) give each read its own probability for each alignment, from base qualities and positions, and add a transcript $\theta_0$ for reads from nowhere. The loop is the same, with the per-read probability in place of $1/\ell_t$.
- **RSEM.** Li and Dewey (2011) add fragment length models, effective lengths, paired-end reads, and credibility intervals: a [Gibbs sampler](/gibbs-sampling/) draws read assignments and abundance vectors from the posterior.
- **Equivalence classes.** kallisto runs the EM on classes of reads with the same compatible set. Salmon uses *rich* equivalence classes that also keep, for each transcript of the class, an average conditional probability, so position and bias weights survive the grouping.
- **Online and variational inference.** Salmon first updates the abundances while it streams the reads, then runs an offline EM or variational Bayes EM on the classes. Variational Bayes adds a prior on the abundances, and the strength of the prior changes how many small abundances end near zero.
- **Bias models.** Salmon corrects the effective lengths for sequence bias at fragment ends and for the GC content of fragments.

## When to use it

Use it whenever reads fit more than one transcript, which is the normal case for genes with several isoforms. It is the standard last step after pseudoalignment or selective alignment, and its classes come for free from those mappers. Counting only the reads unique to each transcript throws away the shared exons and biases the result toward transcripts with long unique parts. When you need uncertainty, add bootstrap samples over reads, as kallisto does, or Gibbs sampling, as RSEM and Salmon do; the point estimate alone hides a flat likelihood.

## Pitfalls

- **Starting with zeros.** If line L1 sets some $\alpha_t = 0$, line L6 never gives that transcript a read, and the result can be a poor fixed point. Start with every $\alpha_t > 0$.
- **Raw lengths in line L5.** Using the full transcript length instead of the effective length overweights long transcripts against short ones, and short transcripts near the fragment length get the largest error. Use $\ell_t = \max(\mathrm{len}_t - \mu + 1, 1)$ or the full fragment length distribution.
- **Reading $\alpha$ as expression.** $\alpha$ is a fraction of reads, not of molecules. Report $\tau$ or TPM, which divide by $\ell_t$ first.
- **Trusting one answer on a ridge.** If two transcripts are in the same classes, the split between them is not fixed by the data. Report their sum, or the uncertainty, not the split.
- **A loose stop in line L8.** An absolute tolerance on large $\alpha_t$ stops too late for small ones. Use a relative change on transcripts above a small floor.

## Implementations

## History

Dempster, Laird and Rubin (1977) gave the EM algorithm in general form. Jiang and Wong (2009) wrote the likelihood of isoform abundances under a Poisson model of reads. Li, Ruotti, Stewart, Thomson and Dewey (2010) gave the read-level EM with multi-mapping reads and a noise isoform, and noted that the likelihood is concave. Trapnell and others (2010) maximized a similar likelihood in Cufflinks. Li and Dewey (2011) released RSEM with effective lengths, TPM and credibility intervals. Bray, Pimentel, Melsted and Pachter (2016) ran the EM on equivalence classes from pseudoalignment in kallisto, and Patro, Duggal, Love, Irizarry and Kingsford (2017) added online inference and bias models in Salmon.

## References
