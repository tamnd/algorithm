---
tag: VXYDJ6
kind: concept
slug: kmer-spectrum
name: k-mer spectrum
aliases:
- k-mer frequency histogram
area: biology/genome-assembly
level: core
summary: The histogram of k-mer counts in a set of reads. Errors make a peak at 1, the genome makes a peak near the k-mer coverage, and the two give genome size and error rate.
prereqs: [kmer-counting, sequencing-coverage]
see_also: [kmer-counting, read-error-correction, sequencing-coverage, genome-repeat, poisson-distribution, alignment-free-comparison, n50, de-bruijn-assembly]
sources:
  - paper: doi:10.1101/gr.074492.107
    title: Daniel R. Zerbino and Ewan Birney, Velvet, algorithms for de novo short read assembly using de Bruijn graphs, Genome Research 18(5) (2008)
    locator: pp. 821 to 829, Methods (k-mer coverage C_k = C(L - k + 1)/L)
  - paper: doi:10.1186/gb-2010-11-11-r116
    title: David R. Kelley, Michael C. Schatz and Steven L. Salzberg, Quake, quality-aware detection and correction of sequencing errors, Genome Biology 11(11) (2010)
    locator: Article R116 (the k-mer count histogram and the cutoff between trusted and untrusted k-mers)
  - paper: doi:10.1093/bioinformatics/btx153
    title: Gregory W. Vurture et al., GenomeScope, fast reference-free genome profiling from short reads, Bioinformatics 33(14) (2017)
    locator: pp. 2202 to 2204 (a mixture model of the spectrum for genome size, heterozygosity and error rate)
  - paper: doi:10.1073/pnas.171285098
    title: Pavel A. Pevzner, Haixu Tang and Michael S. Waterman, An Eulerian path approach to DNA fragment assembly, PNAS 98(17) (2001)
    locator: pp. 9748 to 9753 (solid and weak l-tuples)
  - paper: doi:10.1186/1471-2105-12-333
    title: Páll Melsted and Jonathan K. Pritchard, Efficient counting of k-mers in DNA sequences using a Bloom filter, BMC Bioinformatics 12 (2011)
    locator: Article 333 (most k-mers that occur once are errors)
---

The k-mer spectrum of a set of reads is the histogram of [k-mer](/kmer/) counts: for each $j$, the number of distinct k-mers that occur exactly $j$ times. In shotgun data it has two main parts. Sequencing errors make many k-mers that occur once or twice, a peak at the left edge. The k-mers of the genome occur about $c_k$ times each, where $c_k$ is the k-mer coverage, and make a second peak there. The spectrum is cheap to compute and needs no reference, so it is the first look at a new data set: it gives the genome size, the coverage, the error rate, and the cutoff for [read error correction](/read-error-correction/).

## In plain words

Cut many copies of a long text into short words of fixed length and count each distinct word. Then make a second count: how many distinct words were seen once, how many twice, and so on. That second count is the spectrum.

Words from the real text show up about as many times as there are copies, say twenty. Typing mistakes create new words that are seen only once or twice. So the chart has a tall spike at the left, from the mistakes, and a hump in the middle, from the real text. The hump tells how many copies there were. Dividing the number of good words by the copy count gives the length of the text. Words that the text itself repeats show up as smaller humps at twice and three times the copy count.

## The idea

### Definition

Count the k-mers of the reads, usually as canonical k-mers, with [k-mer counting](/kmer-counting/). For $j \ge 1$, let

$$h(j) = \big|\{x : \text{count}(x) = j\}\big|.$$

The spectrum is the sequence $h(1), h(2), \ldots$. It has two simple sums: $\sum_j h(j) = D$, the number of distinct k-mers, and $\sum_j j\, h(j) = M$, the number of k-mer occurrences in the reads.

### The k-mer coverage

Let the genome have length $G$, and let $N$ reads of length $L$ start at random positions, so the read coverage is $c = NL/G$ (see [sequencing coverage](/sequencing-coverage/)). A k-mer at a given place in the genome is fully inside a read only if the read starts at one of $L - k + 1$ positions. So the expected number of reads that contain it is

$$c_k = \frac{N (L - k + 1)}{G} = c \cdot \frac{L - k + 1}{L}.$$

This is the k-mer coverage, the relation used by Velvet. If each base is wrong with probability $e$, independently, a read holds an error-free copy of the k-mer with probability $(1 - e)^k$. The count of a unique genome k-mer is then close to a [Poisson](/poisson-distribution/) variable with mean

$$\lambda = c_k (1 - e)^k.$$

### The parts of the spectrum

- **The error peak.** A substitution creates up to $k$ k-mers that are usually not in the genome. The same error k-mer is rarely created twice, so these k-mers have count 1, sometimes 2. The error part of $h$ falls fast from $j = 1$.
- **The valley.** Between the error peak and the main peak, $h$ has a minimum. k-mers with counts above the valley are called *solid* or *trusted*, and those below *weak* or *untrusted*. Pevzner, Tang and Waterman use the terms solid and weak, with a count threshold. Quake fits the histogram to choose the cutoff automatically.
- **The main peak.** The unique k-mers of the genome form a hump near $\lambda$. Real data has more spread than Poisson, because coverage is not uniform.
- **Repeat peaks.** A k-mer in a [repeat](/genome-repeat/) with $m$ copies occurs about $m\lambda$ times, so small peaks appear at $2\lambda$, $3\lambda$ and higher.
- **The heterozygous peak.** In a diploid genome, a k-mer that covers a site where the two chromosome copies differ is on only one copy. Such k-mers form a peak at $\lambda / 2$. The ratio of the two peaks tells how often the copies differ.

### What the spectrum estimates

- **Genome size.** Each unique genome k-mer contributes about $\lambda$ occurrences, so

$$\hat G = \frac{\sum_{j \ge v} j\, h(j)}{\lambda},$$

where $v$ is the valley. Counting only above the valley removes the error k-mers. Repeats are counted correctly: a k-mer with $m$ copies contributes $m\lambda$ occurrences and $m$ positions.

- **Coverage.** From $\lambda$ and the read length, $c = \lambda L / ((L - k + 1)(1 - e)^k)$.
- **Error rate.** A fraction $(1 - e)^k$ of the k-mer occurrences is error-free. With $M_s = \sum_{j \ge v} j\, h(j)$, this gives $\hat e = 1 - (M_s / M)^{1/k}$.
- **Heterozygosity and repeat content**, from the sizes of the half peak and of the repeat peaks.

GenomeScope fits all of these at once: it fits a mixture model of the spectrum of a diploid genome, with one peak for each copy number, and reads the genome size, heterozygosity, repeat content and error rate from the fitted parameters.

### Choosing $k$

$k$ must be long enough that most k-mers are unique in the genome: a few units above $\log_4 G$. Longer $k$ lowers $c_k$ and makes each k-mer more likely to hold an error, so the main peak moves left toward the error peak. At low coverage the two peaks merge and the estimates fail.

## Examples

**A simulated spectrum.** A random genome of $G = 100{,}000$ bases is read at $c = 30$ with $N = 30{,}000$ reads of $L = 100$ bases. Each base is substituted with probability $e = 0.01$, and each read comes from a random strand. The canonical 21-mers have this spectrum:

| $j$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 14 | 16 | 18 | 20 | 22 | 24 | 26 | 28 | 30 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $h(j)$ | 429,791 | 12,914 | 231 | 3 | 10 | 29 | 94 | 4,397 | 7,554 | 9,002 | 8,776 | 7,232 | 4,925 | 2,802 | 1,404 | 645 |

- The error peak at $j = 1$ is about 48 times higher than the main peak. Then the counts fall to a valley at $j = 4$ and rise to a main peak with mode 18.
- The model predicts $c_k = 30 \cdot 80/100 = 24$ and $\lambda = 24 \cdot 0.99^{21} \approx 19.43$. The k-mers with count at least 4 have mean count 19.45 and variance 19.60, as for a Poisson variable with mean 19.43.
- Cutting at the valley separates the two classes almost perfectly. Of the 99,980 distinct 21-mers of the genome, 29 fall below the valley, and no error k-mer is at or above it.

**Genome size from the same spectrum.** There are $M = 2{,}400{,}000$ k-mer occurrences, and $M_s = 1{,}943{,}688$ of them above the valley.

| estimate | value | error |
|---|---|---|
| $M$ / mode | $2{,}400{,}000 / 18 = 133{,}333$ | $+33\%$ |
| $M_s$ / mode | $1{,}943{,}688 / 18 = 107{,}983$ | $+8\%$ |
| $M_s$ / $\lambda$ | $1{,}943{,}688 / 19.43 = 100{,}035$ | $0.04\%$ |

Using all k-mers counts the errors as genome. Dividing by the mode in place of the mean adds a smaller bias, because the peak is broad.

**Error rate from the same spectrum.** $M_s / M = 0.8099$, and $1 - 0.8099^{1/21} \approx 0.0100$, the error rate of the simulation.

## Where it is used

- Genome profiling before assembly: the size, heterozygosity and repeat content of a new genome, to plan the sequencing and the assembly.
- [Read error correction](/read-error-correction/): the valley sets the threshold between trusted and untrusted k-mers.
- [De Bruijn assembly](/de-bruijn-assembly/): assemblers drop the k-mers below a coverage cutoff before they build the graph, and use $c_k$ to guess the copy number of a contig.
- Quality control: contamination shows up as an extra peak at a different coverage, and low coverage as a main peak that merges with the error peak.
- Assembly evaluation: comparing the k-mers of an assembly with the spectrum of the reads shows k-mers that the assembly lost or duplicated.
- Genome size, with the [N50](/n50/) family of measures: NG50 needs an estimate of $G$, and the spectrum is a common source.

## References
