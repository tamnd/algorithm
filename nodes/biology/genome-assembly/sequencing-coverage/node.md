---
tag: J45KP4
kind: concept
slug: sequencing-coverage
name: Sequencing coverage
aliases:
- read depth
- fold coverage
area: biology/genome-assembly
level: intro
summary: The mean number of reads that contain a base of the genome, c = NL/G. Under random sampling the depth at a base is close to Poisson with mean c.
prereqs: [shotgun-sequencing, poisson-distribution]
see_also: [lander-waterman-model, kmer-spectrum, paired-end-reads, genome-assembly-problem, read-error-correction, binomial-distribution, linearity-of-expectation]
sources:
  - paper: doi:10.1016/0888-7543(88)90007-9
    title: Eric S. Lander and Michael S. Waterman, Genomic mapping by fingerprinting random clones, a mathematical analysis, Genomics 2(3) (1988)
    locator: pp. 231 to 239 (the redundancy c = LN/G and Proposition 1)
  - paper: doi:10.1101/gr.074492.107
    title: Daniel R. Zerbino and Ewan Birney, Velvet, algorithms for de novo short read assembly using de Bruijn graphs, Genome Research 18(5) (2008)
    locator: pp. 821 to 829, Methods (k-mer coverage C_k = C(L - k + 1)/L)
  - book: isbn:9780990374602
    title: Phillip Compeau and Pavel Pevzner, Bioinformatics Algorithms, An Active Learning Approach, Volume I, second edition
    locator: Chapter 3 (read coverage and read-pairs)
---

Sequencing coverage is the mean number of reads that contain a given base of the genome. With $N$ reads of length $L$ from a genome of length $G$, the coverage is $c = NL/G$, written as "$c$-fold" or "$c\times$". The word also names the depth at one base: the number of reads that contain that base. When the read start positions are random, the depth at a base is close to a Poisson variable with mean $c$, so a fraction of about $e^{-c}$ of the genome has no read at all.

## In plain words

Paint a long wall by throwing small square stickers at random spots. The total area of the stickers, divided by the area of the wall, tells how many layers of stickers there are on average. That number is the coverage. Some spots get many layers, and some get none, because the throws are random. With one layer on average, about a third of the wall stays bare. With five layers, less than one spot in a hundred stays bare. With thirty layers, a bare spot is rare.

Sequencing works the same way. Each read is a sticker on the genome. More reads give fewer bare spots, but each new read helps less than the one before it. Real sequencers also put more reads on some regions than on others, so the bare spots in practice are more frequent than the random model says.

## The idea

### Mean coverage

Let the genome have length $G$ and let there be $N$ reads, each of length $L$. Each read contains $L$ bases, so the reads hold $NL$ bases in total. The coverage is

$$c = \frac{NL}{G}.$$

By [linearity of expectation](/linearity-of-expectation/), $c$ is the expected depth at a base, for any placement rule that gives each base the same chance to be in a read. For read lengths that vary, $L$ is the mean read length.

### The depth at a base

Model the genome as a circle of length $G$ so that there are no edge effects, and let each read start at a uniform random position, independent of the other reads. A base $x$ is in read $i$ if and only if the read starts at one of the $L$ positions $x - L + 1, \ldots, x$. The probability of that is $L/G$. The reads are independent, so the depth $D_x$ at $x$ is [binomial](/binomial-distribution/) with parameters $N$ and $L/G$:

$$\Pr(D_x = d) = \binom{N}{d} \left(\frac{L}{G}\right)^d \left(1 - \frac{L}{G}\right)^{N - d}.$$

When $N$ is large and $L/G$ is small, this is close to the [Poisson distribution](/poisson-distribution/) with mean $c$:

$$\Pr(D_x = d) \approx e^{-c} \frac{c^d}{d!}.$$

The case $d = 0$ gives the probability that a base has no read:

$$\Pr(D_x = 0) = \left(1 - \frac{L}{G}\right)^N \approx e^{-NL/G} = e^{-c}.$$

So the expected number of uncovered bases is about $G e^{-c}$. The uncovered bases come in runs, the gaps between the islands of overlapping reads. The [Lander-Waterman model](/lander-waterman-model/) counts the islands: about $N e^{-c}$ of them, for reads that must overlap by at least one base to be joined.

### How many reads to ask for

The expected number of gaps, $N e^{-c}$, falls exponentially in $c$, but the factor $N = cG/L$ grows with $c$. To get fewer than $\varepsilon$ expected gaps, ask for $N e^{-c} \le \varepsilon$, that is

$$c \ge \ln \frac{N}{\varepsilon} = \ln \frac{G}{L} + \ln \frac{c}{\varepsilon}.$$

The coverage needed grows as the logarithm of the number of reads. This is the same effect as in the [coupon collector problem](/coupon-collector-problem/): the last uncovered places are the hardest to hit.

### Other kinds of coverage

- **Physical coverage.** For [paired-end reads](/paired-end-reads/), each pair spans an insert of length $I$ that includes the unread middle. With $P$ pairs, the physical coverage is $PI/G$. It is the mean number of pairs whose insert spans a point of the genome. Pairs that span a gap or a repeat are what [scaffolding](/scaffolding/) uses.
- **k-mer coverage.** A read of length $L$ holds $L - k + 1$ [k-mers](/kmer/). A k-mer of the genome is in a read only if the read starts in one of $L - k + 1$ positions, so the mean count of a genome k-mer is

$$c_k = c \cdot \frac{L - k + 1}{L}.$$

Velvet uses this relation to convert between read coverage and k-mer coverage. The peak of the [k-mer spectrum](/kmer-spectrum/) sits near $c_k$, a bit lower when the reads have errors.

- **Coverage of a target.** In targeted sequencing, coverage is the mean depth over the target bases only, and the fraction of target bases with depth at least some threshold is often given too.

### Where the model fails

The Poisson model assumes uniform and independent start positions. Real data has bias: the depth depends on the GC content of the region, on how well the region amplifies, and on whether reads from it map to a unique place. The depth then varies more than a Poisson variable with the same mean, and more bases are uncovered than $G e^{-c}$. Long [genome repeats](/genome-repeat/) also take more reads than their share, because all copies send reads to the same assembled sequence.

## Examples

**A small genome.** Let $G = 1000$, $N = 40$ and $L = 50$. Then $c = 40 \cdot 50 / 1000 = 2$. The Poisson approximation predicts $1000 e^{-2} \approx 135.3$ uncovered bases. On a circle the exact expectation is $1000 \cdot (1 - 0.05)^{40} \approx 128.5$. The approximation is a bit high, because $N = 40$ is small.

**Depth histogram.** In a simulation with a circular genome of $G = 200{,}000$ bases, $L = 100$ and $c = 5$, the fraction of bases with depth 0 was 0.0064, against the Poisson value $e^{-5} \approx 0.0067$. The fraction with depth 5 was 0.1758, against $e^{-5} 5^5 / 5! \approx 0.1755$.

**Uncovered fraction by coverage.**

| $c$ | uncovered fraction $e^{-c}$ |
|---|---|
| 1 | 0.368 |
| 2 | 0.135 |
| 3 | 0.050 |
| 5 | 0.0067 |
| 10 | 0.000045 |

**A human genome at $30\times$.** Let $G = 3.1 \times 10^9$ and $L = 150$. For $c = 30$ the run needs $N = cG/L = 6.2 \times 10^8$ reads. The ideal model predicts $G e^{-30} \approx 3 \times 10^{-4}$ uncovered bases, so in the model the whole genome is covered with probability above 0.999. Under the Poisson model, a base has depth at least 10 with probability above 0.9999 and depth at least 20 with probability about 0.978. In real data the gaps that remain come from bias and from regions that are hard to sequence, not from bad luck.

**Coverage for a target number of gaps.** Solve $N = (G/L) \ln(N/\varepsilon)$ for $\varepsilon = 0.01$ expected gaps:

| genome | $G$ | $L$ | reads $N$ | coverage $c$ |
|---|---|---|---|---|
| bacterium | $5 \times 10^6$ | 100 | about $9.2 \times 10^5$ | about 18.3 |
| human | $3.1 \times 10^9$ | 150 | about $5.1 \times 10^8$ | about 24.7 |

The human genome is 620 times longer, but it needs only about 35% more coverage in this model.

**Paired reads.** A bacterial genome of $G = 5 \times 10^6$ is sequenced with $500{,}000$ pairs of 150-base reads, with insert length 500. The sequence coverage is $2 \cdot 150 \cdot 500{,}000 / (5 \times 10^6) = 30$. The physical coverage is $500 \cdot 500{,}000 / (5 \times 10^6) = 50$.

## Where it is used

- Planning a sequencing run: the coverage target sets the number of reads to buy.
- Assembly: assemblers use the depth of a [contig](/contig/) to tell unique regions from collapsed [repeats](/genome-repeat/), which have a multiple of the usual depth.
- Error correction: [read error correction](/read-error-correction/) and the [k-mer spectrum](/kmer-spectrum/) depend on coverage high enough that true k-mers occur many times and error k-mers occur once or twice.
- Genome size estimates: the total number of k-mers divided by the k-mer coverage gives $G$; see [k-mer spectrum](/kmer-spectrum/).
- Variant calling: the depth at a site decides how sure a call can be, and a depth much higher than usual can mark a copy number gain.

## References
