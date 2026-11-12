---
tag: QR49M0
kind: model
slug: lander-waterman-model
name: Lander-Waterman model
aliases:
- Lander-Waterman statistics
area: biology/genome-assembly
level: advanced
summary: Random reads of length L start at uniform positions on a genome, and two reads join if they overlap by at least T bases. It gives about N e^(-c(1-T/L)) islands at coverage c.
history:
  year: 1988
  people: [Eric S. Lander, Michael S. Waterman]
  note: Lander and Waterman built the model for physical mapping by fingerprinting random clones, and stated that it applies to shotgun sequencing too.
prereqs: [sequencing-coverage, geometric-distribution, linearity-of-expectation, walds-equation]
see_also: [sequencing-coverage, shotgun-sequencing, poisson-distribution, coupon-collector-problem, balls-into-bins, jensens-inequality, contig, genome-assembly-problem]
sources:
  - paper: doi:10.1016/0888-7543(88)90007-9
    title: Eric S. Lander and Michael S. Waterman, Genomic mapping by fingerprinting random clones, a mathematical analysis, Genomics 2(3) (1988)
    locator: pp. 231 to 239 (the model and notation, p. 232; Proposition 1 and the maximum number of islands, pp. 232 to 233; the proofs, Section 5, pp. 237 to 238; Proposition 2 on variable lengths)
  - paper: doi:10.1186/1471-2105-14-S5-S18
    title: Guy Bresler, Ma'ayan Bresler and David Tse, Optimal assembly for high throughput shotgun sequencing, BMC Bioinformatics 14(Suppl 5) (2013)
    locator: Article S18 (the Lander-Waterman coverage condition as a lower bound on the number of reads)
  - paper: doi:10.1016/0888-7543(95)80219-c
    title: Jared C. Roach, Cecilie Boysen, Kai Wang and Leroy Hood, Pairwise end sequencing, a unified approach to genomic mapping and sequencing, Genomics 26(2) (1995)
    locator: pp. 345 to 353
---

The Lander-Waterman model is the standard probability model of a shotgun experiment. Reads (or clones) of length $L$ start at independent uniform positions on a genome of length $G$, and two overlapping reads are joined only if their overlap is at least $T$ bases. With $N$ reads, coverage $c = NL/G$ and $\sigma = 1 - T/L$, the expected number of islands of joined reads is $N e^{-c\sigma}$, and the expected fraction of the genome in no read is $e^{-c}$. Lander and Waterman derived these results in 1988 for the physical mapping of genomes, and they are still the first estimate for planning a [shotgun sequencing](/shotgun-sequencing/) project.

## The machine

The model has five parameters, in the notation of the paper:

| symbol | meaning |
|---|---|
| $G$ | the length of the genome, in bases |
| $L$ | the length of a clone or read |
| $N$ | the number of clones or reads |
| $T$ | the least overlap, in bases, that the method detects |
| $\alpha = N/G$ | the probability that a read starts at a given base |

From these come the coverage and the overlap fraction:

$$c = \frac{LN}{G}, \qquad \theta = \frac{T}{L}, \qquad \sigma = 1 - \theta.$$

**The random placement.** Each base of the genome is the start of a read with probability $\alpha$, independently of the other bases. So the gap between two consecutive read starts is [geometric](/geometric-distribution/) with parameter $\alpha$, and for large $G$ the starts form a Poisson process of rate $\alpha$. The model ignores the ends of the genome, which is fine when $G$ is much larger than $L$.

**The overlap rule.** Reads that start at $x < y$ overlap by $L - (y - x)$ bases when $y - x < L$. The experiment *detects* the overlap, and so joins the two reads, only if the overlap is at least $T$:

$$L - (y - x) \ge T \iff y - x \le L\sigma.$$

**The objects.** An *island* is a maximal chain of reads joined by detected overlaps. An island with two or more reads is a *contig*, and the space between two islands is an *ocean*. The model calls these islands *apparent*, because two islands may still overlap by less than $T$ bases; *actual* islands are the connected stretches of covered bases, the case $T = 0$, $\sigma = 1$.

## What it counts

The model counts the shape of the read layout, not the work of any algorithm:

- the expected number of islands and contigs;
- the expected number of reads in an island;
- the expected length of an island, in bases;
- the probability that an ocean is long, or that an apparent ocean is real;
- the expected fraction of bases that no read covers.

All results are expectations under the random placement. They do not include errors, [repeats](/genome-repeat/) or the uneven coverage of real data, so they are lower bounds on what a real project needs.

## Relation to other models

- **[Sequencing coverage](/sequencing-coverage/).** The depth at one base is binomial and close to [Poisson](/poisson-distribution/) with mean $c$. The uncovered fraction $e^{-c}$ is the Poisson probability of depth 0. The Lander-Waterman model adds the overlap threshold and counts islands, which the depth at single bases does not show.
- **Covering problems.** Covering every base resembles the [coupon collector problem](/coupon-collector-problem/) and [balls into bins](/balls-into-bins/): the last uncovered bases are the hardest to hit, so the coverage for no gap grows as $\ln(G/L)$.
- **Earlier library statistics.** Lander and Waterman relate their result to the formula of Clarke and Carbon (1976) for the chance that a clone library contains a given gene, which is the case of covering one point.
- **Variable lengths.** Proposition 2 of the paper lets $L$ and $\theta$ vary from read to read. By [Jensen's inequality](/jensens-inequality/), the expected number of islands is at least $N e^{-c E(\sigma)}$.
- **Pairs and information limits.** Roach and colleagues analyzed pairwise end sequencing, in which each clone gives two linked reads. Bresler, Bresler and Tse use the Lander-Waterman coverage condition as one of two lower bounds on the reads needed to reconstruct a genome; the other comes from repeats (see [genome assembly problem](/genome-assembly-problem/)).

## Known results in the model

These are the parts of Proposition 1 of the paper, each with a short derivation. Write $p = e^{-c\sigma}$.

**1. Expected number of islands: $N e^{-c\sigma}$.** Each island has exactly one rightmost read, so the number of islands equals the number of reads that are rightmost. A read starting at $x$ is rightmost if and only if no read starts in the $L\sigma$ bases after $x$. That has probability $(1 - \alpha)^{L\sigma} \approx e^{-\alpha L\sigma} = e^{-c\sigma}$. By [linearity of expectation](/linearity-of-expectation/) over the $N$ reads, the expected number of islands is $N e^{-c\sigma}$.

**2. Islands by size.** Walk an island from its leftmost read. Each next start is within $L\sigma$, and so continues the island, with probability $1 - p$, independently. So the number $J$ of reads in an island is geometric: $\Pr(J = j) = p (1 - p)^{j - 1}$. The expected number of islands with $j$ reads is $N e^{-2c\sigma} (1 - e^{-c\sigma})^{j-1}$, and the expected number of contigs ($j \ge 2$) is $N e^{-c\sigma} - N e^{-2c\sigma}$.

**3. Expected reads per island: $e^{c\sigma}$.** This is $E[J] = 1/p$. It also equals $N$ divided by the number of islands.

**4. Expected island length: $L\left[\dfrac{e^{c\sigma} - 1}{c} + 1 - \sigma\right]$.** An island is $L$ bases long plus the $J - 1$ gaps between consecutive starts inside it. In the continuous limit the gaps between starts are exponential with mean $L/c$, and a gap inside an island is one that is at most $L\sigma$. For an exponential gap $g$ with rate $\lambda = c/L$ and $a = L\sigma$,

$$E[g \mid g \le a] = \frac{1}{\lambda} - \frac{a e^{-\lambda a}}{1 - e^{-\lambda a}} = \frac{L}{c} - \frac{L\sigma\, p}{1 - p}.$$

$J - 1$ is the number of short gaps before the first long one, so by [Wald's equation](/walds-equation/) the expected sum of the short gaps is $E[J - 1] \cdot E[g \mid g \le a]$, with $E[J - 1] = (1 - p)/p = e^{c\sigma} - 1$. Then

$$E[\text{length}] = L + (e^{c\sigma} - 1)\frac{L}{c} - L\sigma\, \frac{(e^{c\sigma} - 1)\, p}{1 - p} = L\left[\frac{e^{c\sigma} - 1}{c} + 1 - \sigma\right],$$

because $(e^{c\sigma} - 1)p/(1 - p) = 1$.

**5. Actual islands and uncovered bases.** Set $\sigma = 1$: there are about $N e^{-c}$ actual islands, so as many true gaps. A base is uncovered when no read starts in the $L$ bases that end at it, with probability $(1 - \alpha)^L \approx e^{-c}$; this does not depend on $T$.

**6. Ocean lengths: $\Pr(\text{ocean} \ge kL) = e^{-c(k + \theta)}$.** An island ends when the gap $g$ to the next start is more than $L\sigma$. The ocean after it has length $g - L$. By the memoryless property,

$$\Pr(g - L \ge kL \mid g > L\sigma) = \frac{e^{-c(1 + k)}}{e^{-c\sigma}} = e^{-c(k + \theta)}.$$

For $k = 0$ this is $e^{-c\theta}$, the probability that an apparent ocean is a real gap rather than an overlap too short to detect.

**7. The most islands.** The expected number of islands, $(G/L)\, c\, e^{-c\sigma}$, grows with $c$ and then falls. Its derivative is zero at $c = 1/\sigma$, where it equals $(G/L) e^{-1} / \sigma$. Early in a project, each new read tends to start a new island; past $c = 1/\sigma$, new reads mostly join islands.

| $\theta$ | $c$ at the maximum | islands per $G/L$ at the maximum |
|---|---|---|
| 0 | 1 | 0.368 |
| 0.25 | 4/3 | 0.491 |
| 0.5 | 2 | 0.736 |
| 0.75 | 4 | 1.472 |

### Check by simulation

A simulation placed $N = cG/L$ reads uniformly on a circular genome with $G = 10^6$ and $L = 1000$, and averaged over 200 runs. Each pair of columns gives the simulated mean and the formula.

| $c$ | $\theta$ | islands | $N e^{-c\sigma}$ | reads per island | $e^{c\sigma}$ | island length | formula 4 | uncovered | $e^{-c}$ |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 367.45 | 367.88 | 2.721 | 2.718 | 1717.3 | 1718.3 | 0.36897 | 0.36788 |
| 2 | 0 | 270.92 | 270.67 | 7.382 | 7.389 | 3190.0 | 3194.5 | 0.13577 | 0.13534 |
| 3 | 0 | 149.31 | 149.36 | 20.092 | 20.086 | 6365.5 | 6361.8 | 0.04954 | 0.04979 |
| 5 | 0 | 33.98 | 33.69 | 147.1 | 148.4 | 29223 | 29483 | 0.00684 | 0.00674 |
| 5 | 0.25 | 118.56 | 117.59 | 42.18 | 42.52 | 8484 | 8554 | | |
| 8 | 0.5 | 146.90 | 146.53 | 54.46 | 54.60 | 7182 | 7200 | | |

Every simulated mean is within 1% of the formula for the island counts, the reads per island and the island lengths, and within 1.5% for the uncovered fraction. On a circle the exact expected number of islands is $N(1 - L\sigma/G)^{N-1}$, for example 368.06 at $c = 1$; the formula $N e^{-c\sigma}$ is its limit for large $G$. At $c = 8$, $\theta = 0$ only about 2.7 islands are expected, and the simulated mean, 2.52, is too noisy for a tight check.

## References
