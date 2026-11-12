---
tag: M5AQEX
kind: problem
slug: kmer-counting
name: k-mer counting
area: biology/genome-assembly
level: core
summary: Count how many times each distinct k-mer occurs in a set of reads. Hash tables, sorting and disk partitions solve it; the hard part is memory, as errors add many rare k-mers.
prereqs: [kmer, hash-table]
see_also: [kmer-spectrum, bloom-filter, count-min-sketch, compare-and-swap, radix-sort, minimizer, frequent-items-problem, external-merge-sort]
sources:
  - paper: doi:10.1093/bioinformatics/btr011
    title: Guillaume Marçais and Carl Kingsford, A fast, lock-free approach for efficient parallel counting of occurrences of k-mers, Bioinformatics 27(6) (2011)
    locator: pp. 764 to 770 (Jellyfish, the lock-free hash table with compare-and-swap, quadratic reprobing and quotienting)
  - paper: doi:10.1186/1471-2105-12-333
    title: Páll Melsted and Jonathan K. Pritchard, Efficient counting of k-mers in DNA sequences using a Bloom filter, BMC Bioinformatics 12 (2011)
    locator: Article 333 (BFCounter, the Bloom filter in front of the hash table, and the comparison with Jellyfish)
  - paper: doi:10.1186/1471-2105-14-160
    title: Sebastian Deorowicz, Agnieszka Debudaj-Grabysz and Szymon Grabowski, Disk-based k-mer counting on a PC, BMC Bioinformatics 14 (2013)
    locator: Article 160 (KMC, disk bins and radix sorting)
  - paper: doi:10.1093/bioinformatics/btv022
    title: Sebastian Deorowicz, Marek Kokot, Szymon Grabowski and Agnieszka Debudaj-Grabysz, KMC 2, fast and resource-frugal k-mer counting, Bioinformatics 31(10) (2015)
    locator: pp. 1569 to 1576 (signatures and super k-mers)
---

k-mer counting is the problem of finding, for a set of DNA reads and an integer $k$, every distinct [k-mer](/kmer/) of the reads and the number of times it occurs. It is the first step of most short-read tools: the counts give the [k-mer spectrum](/kmer-spectrum/), separate true k-mers from error k-mers for [read error correction](/read-error-correction/), and give the nodes of a de Bruijn assembler. A [hash table](/hash-table/) solves it in expected linear time. The difficulty is memory: a run of tens of gigabases has billions of distinct k-mers, and most of them are errors that occur once.

## In plain words

You have a huge pile of short DNA strings. Slide a window of fixed width along every string, and write down each piece the window shows. At the end you want a list: every distinct piece, and how many times you saw it.

A notebook with one line per piece does this. Each time you see a piece, find its line and add one. The problem is size. A human sequencing run gives billions of pieces, and a few errors in each string create many pieces that are seen only once. Most of the notebook fills with these useless lines. So the methods differ in how they find lines fast, how they share the work between processors, how they move work to disk, and how they avoid writing down pieces that occur only once.

## Definition

**Input.** A multiset of reads $R = \{r_1, \ldots, r_N\}$ over $\Sigma = \{A, C, G, T\}$ and an integer $k$. Let

$$M = \sum_{i=1}^{N} \max(|r_i| - k + 1, 0)$$

be the number of k-mer occurrences. Usually k-mers that contain a base other than A, C, G and T are skipped.

**Output.** For every k-mer $x$ that occurs in some read, the count

$$\text{count}(x) = \big|\{(i, j) : r_i[j \ldots j + k - 1] = x\}\big|.$$

Let $D$ be the number of distinct k-mers with a nonzero count. The output has size $D$, and $D \le \min(M, 4^k)$.

**Canonical counting.** Reads come from both strands, so most tools count the canonical k-mer $\min(x, \overline{x})$ in place of $x$, where $\overline{x}$ is the reverse complement. Then $\text{count}(x)$ and $\text{count}(\overline{x})$ are added together.

## Variants

- **With a threshold.** Report only the k-mers with count at least $t$, usually $t = 2$, to drop most error k-mers.
- **Histogram only.** Report the number of distinct k-mers with each count, the [k-mer spectrum](/kmer-spectrum/), and not the k-mers.
- **Approximate counts.** Allow overestimates with small probability, as with a [count-min sketch](/count-min-sketch/), in exchange for fixed memory.
- **Frequent k-mers.** Report only the k-mers above a frequency threshold; this is the [frequent items problem](/frequent-items-problem/) on the stream of k-mers.
- **Distinct k-mers.** Estimate only $D$, the [distinct elements problem](/distinct-elements-problem/), for example to size a hash table before counting.
- **Weighted counts.** Add a weight that depends on the quality values of the bases instead of 1, as Quake does for error correction.
- **Long k.** For $k > 32$ a k-mer no longer fits in one 64-bit word, and keys take several words.

## Examples

**Three reads.** Let $R = \{\texttt{ACGTTGCA}, \texttt{TGCAACGT}, \texttt{GTTGCATT}\}$ and $k = 3$. Each read gives 6 k-mers, so $M = 18$.

| k-mer | count | canonical | canonical count |
|---|---|---|---|
| AAC | 1 | AAC | 3 (AAC, GTT) |
| ACG | 2 | ACG | 4 (ACG, CGT) |
| ATT | 1 | AAT | 1 (ATT) |
| CAA | 1 | CAA | 3 (CAA, TTG) |
| CAT | 1 | ATG | 1 (CAT) |
| CGT | 2 | | |
| GCA | 3 | GCA | 6 (GCA, TGC) |
| GTT | 2 | | |
| TGC | 3 | | |
| TTG | 2 | | |

There are 10 distinct k-mers and 6 distinct canonical k-mers. The canonical counts form the histogram: two k-mers occur once, two occur three times, one four times and one six times. Sorting the 18 canonical k-mers and counting runs of equal values gives the same result.

**Rolling codes.** With $A, C, G, T \mapsto 0, 1, 2, 3$, the 3-mers of ACGTTGCA have forward codes 6, 27, 47, 62, 57, 36 and reverse-complement codes 27, 6, 1, 16, 36, 57. The canonical code is the smaller of the two at each position: 6, 6, 1, 16, 36, 36, for ACG, ACG, AAC, CAA, GCA, GCA. Each code comes from the last one in $O(1)$ operations; see [k-mer](/kmer/).

**Error k-mers dominate.** In a simulation of a random genome of 100,000 bases, read at coverage 30 with reads of 100 bases and a 1% substitution rate, the 30,000 reads hold $M = 2{,}400{,}000$ canonical 21-mers. There are $D = 542{,}887$ distinct ones, while the genome has only 99,980 distinct 21-mers. Of the 442,914 distinct error k-mers, 429,787 occur only once. A table that skips the k-mers seen only once holds 113,096 entries instead of 542,887.

## Known algorithms

### Hash table

Scan the reads, compute each canonical k-mer code, and increment its entry in a [hash table](/hash-table/). The expected time is $O(M)$ for $k \le 32$, and the space is $O(D)$ entries. This is the [frequency counter](/frequency-counter/) pattern applied to k-mers.

Jellyfish (Marçais and Kingsford) makes this parallel without locks. Many threads update one table in shared memory with [open addressing](/open-addressing/). A thread claims an empty slot or increments a count with a [compare-and-swap](/compare-and-swap/) instruction, and retries if another thread changed the slot first. Collisions follow a quadratic reprobe sequence, the $i$-th probe at offset $i(i+1)/2$ as in [quadratic probing](/quadratic-probing/). To save space, an entry stores only part of the key: the slot position already encodes the rest, a technique called quotienting.

### Sort and count

Write all $M$ k-mer codes into an array, sort it, and count runs of equal codes. With [radix sort](/radix-sort/) on $2k$-bit keys this takes $O(M)$ time for fixed $k$, but $O(M)$ space, which is more than the hash table when k-mers repeat many times.

### Disk partitions

KMC (Deorowicz, Debudaj-Grabysz and Grabowski) splits the k-mers into many bins on disk, then loads one bin at a time, sorts it with radix sort and counts it. Memory then depends on the largest bin, not on $D$. KMC 2 cuts the disk traffic with *super k-mers*: consecutive k-mers of a read that share the same signature, a variant of the [minimizer](/minimizer/), are written once as one longer string and all go to the same bin. The same divide-and-sort idea is behind [external merge sort](/external-merge-sort/).

### Skip the singletons with a Bloom filter

BFCounter (Melsted and Pritchard) puts a [Bloom filter](/bloom-filter/) in front of the hash table. The first time a k-mer appears, it goes only into the Bloom filter. When a k-mer appears and the filter already reports it, it goes into the hash table. Most error k-mers occur once, so they never reach the table. A [false positive](/false-positive-rate/) of the filter lets a few singletons in, and a second pass over the reads computes exact counts for the k-mers in the table and drops those with count 1. On human reads at about $40\times$ coverage with $k = 25$, the paper reports 42 GB of memory for BFCounter against 71 GB for Jellyfish, at about three times the running time.

### Approximate counting

A [count-min sketch](/count-min-sketch/) keeps $d$ rows of counters indexed by independent hash functions and reports the minimum over the rows. It never underestimates, uses fixed memory, and overestimates by a bounded amount with high probability. Tools that only need to ask "is this k-mer frequent?" accept these errors.

## Bounds

- **Time.** Any method must read the input, so it needs $\Omega(\sum |r_i|)$ time. Hashing and radix sorting reach $O(M)$ for $k \le 32$ on a [word RAM](/word-ram/); for longer $k$ each key costs $O(k / w)$ word operations on $w$-bit words.
- **Space.** An exact answer has $D$ entries. Storing a set of $D$ k-mers from a universe of $4^k$ needs at least $\log_2 \binom{4^k}{D}$ binary digits in the worst case, about $D (2k - \log_2 D + 1.44)$ when $D$ is much smaller than $4^k$. Quotienting gets close to this by storing only the part of each key that the table position does not give.
- **Errors set $D$.** For a genome of size $G$ at error rate $e$ per base, each error creates up to $k$ new k-mers. So $D$ is at most about $G$ plus $k$ times the number of errors in the reads. The second term grows with the amount of data, and at moderate coverage the error k-mers outnumber the true ones, as in the simulation above.

## Reductions

- **To frequency counting.** k-mer counting is counting the frequency of each item in a stream of $M$ items, the k-mers, from a universe of size $4^k$. Every method for that problem applies.
- **To sorting.** Counting is sorting followed by a scan for runs; see the [sorting problem](/sorting-problem/).
- **From k-mer counting to the spectrum.** The [k-mer spectrum](/kmer-spectrum/) is the frequency count of the counts, a second counting pass over $D$ numbers.

## Applications

- The [k-mer spectrum](/kmer-spectrum/), to estimate genome size, coverage, heterozygosity and the error rate.
- [Read error correction](/read-error-correction/): k-mers with high counts are trusted, the rest are suspect.
- [De Bruijn assembly](/de-bruijn-assembly/): the solid k-mers are the edges of the [de Bruijn graph](/de-bruijn-graph/).
- [Alignment-free comparison](/alignment-free-comparison/) of genomes and samples through their k-mer profiles.
- Building a [k-mer index](/kmer-index/) for seeding in [read mapping](/read-mapping/).

## References
