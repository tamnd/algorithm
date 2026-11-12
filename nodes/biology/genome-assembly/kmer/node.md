---
tag: GSETTQ
kind: definition
slug: kmer
name: k-mer
aliases:
- kmer
- n-gram
- q-gram
area: biology/genome-assembly
level: intro
summary: A substring of length k of a read or a genome. A DNA string of length n holds n - k + 1 k-mers, out of 4^k possible ones.
prereqs: [alphabet]
see_also: [kmer-counting, kmer-spectrum, kmer-index, minimizer, de-bruijn-graph, q-gram-lemma, subword-complexity, spaced-seed]
sources:
  - book: isbn:9780990374602
    title: Phillip Compeau and Pavel Pevzner, Bioinformatics Algorithms, An Active Learning Approach, Volume I, second edition
    locator: Chapter 3 (the k-mer composition of a string and the de Bruijn graph of k-mers)
  - book: isbn:9781107078536
    title: Veli Mäkinen, Djamal Belazzougui, Fabio Cunial and Alexandru I. Tomescu, Genome-Scale Algorithm Design, Cambridge University Press (2015)
    locator: Chapter 13, Fragment assembly
  - paper: doi:10.1073/pnas.171285098
    title: Pavel A. Pevzner, Haixu Tang and Michael S. Waterman, An Eulerian path approach to DNA fragment assembly, PNAS 98(17) (2001)
    locator: pp. 9748 to 9753 (the l-tuple spectrum of a set of reads)
  - paper: doi:10.1186/1471-2105-12-333
    title: Páll Melsted and Jonathan K. Pritchard, Efficient counting of k-mers in DNA sequences using a Bloom filter, BMC Bioinformatics 12 (2011)
    locator: Article 333, Methods (a k-mer and its reverse complement are counted as the lexicographically smaller of the two)
---

A k-mer is a substring of length $k$ of a DNA string, such as a read or a genome. A string of length $n$ holds $n - k + 1$ k-mers, one at each start position, and there are $4^k$ possible k-mers over $\{A, C, G, T\}$. Because DNA has two strands, tools often count a k-mer and its reverse complement as one *canonical* k-mer. The k-mer is the unit of [k-mer counting](/kmer-counting/), of the [k-mer spectrum](/kmer-spectrum/), of the [de Bruijn graph](/de-bruijn-graph/) and of the seeds in a [k-mer index](/kmer-index/).

## Definition

Let $\Sigma = \{A, C, G, T\}$ and let $s = s[0 \ldots n-1]$ be a string over $\Sigma$. For an integer $k$ with $1 \le k \le n$, the **k-mer of $s$ at position $i$**, for $0 \le i \le n - k$, is

$$s[i \ldots i + k - 1].$$

A **k-mer** is any string in $\Sigma^k$. There are $|\Sigma^k| = 4^k$ of them. The **k-mer composition** of $s$ is the multiset of its $n - k + 1$ k-mers, one for each position. The number of *distinct* k-mers of $s$ is at most $\min(n - k + 1, 4^k)$. In a set of reads, the k-mers of each read are taken separately: a string that crosses the end of one read and the start of the next is not a k-mer of the data.

**Reverse complement.** The complement swaps $A \leftrightarrow T$ and $C \leftrightarrow G$. The reverse complement of $x = x[0 \ldots k-1]$ is

$$\overline{x}[j] = \text{comp}(x[k - 1 - j]), \qquad 0 \le j \le k - 1.$$

The map $x \mapsto \overline{x}$ is an involution: $\overline{\overline{x}} = x$. A read from the second strand of the genome shows $\overline{x}$ where a read from the first strand shows $x$.

**Canonical k-mer.** Fix a total order on $\Sigma^k$, usually the [lexicographic order](/lexicographic-order/) with $A < C < G < T$. The canonical form of $x$ is

$$\text{can}(x) = \min(x, \overline{x}).$$

So $\text{can}(x) = \text{can}(\overline{x})$, and counts of canonical k-mers do not depend on the strand that a read came from.

**Reverse-complement palindromes and odd $k$.** A k-mer is a *palindrome* in this sense when $x = \overline{x}$.

- If $k$ is odd, no k-mer is a palindrome. Proof: let $m = (k-1)/2$ be the middle position. If $x = \overline{x}$, then $x[m] = \text{comp}(x[k - 1 - m]) = \text{comp}(x[m])$. No base is its own complement, so this is impossible.
- If $k$ is even, there are exactly $4^{k/2}$ palindromes. Proof: $x = \overline{x}$ holds if and only if $x[k-1-j] = \text{comp}(x[j])$ for $0 \le j < k/2$. So the first half is free and fixes the second half.

**The number of canonical k-mers.** The involution splits $\Sigma^k$ into orbits $\{x, \overline{x}\}$ of size 2, and fixed points (the palindromes) of size 1. Each orbit gives one canonical k-mer. So the number of canonical k-mers is $4^k / 2$ for odd $k$ and $(4^k + 4^{k/2})/2$ for even $k$. Odd $k$ is common in assemblers for this reason: with no palindromes, each canonical k-mer stands for exactly two distinct strings, one for each strand, and no k-mer is the same on both strands.

**Two-bit encoding.** Code $A, C, G, T$ as $0, 1, 2, 3$. A k-mer becomes an integer in $[0, 4^k)$ of $2k$ binary digits, so a k-mer with $k \le 32$ fits in one 64-bit word. With this code the complement of $b$ is $3 - b$, and the numeric order of the codes is the lexicographic order of the k-mers. The next k-mer in a string, after base $b$, is computed in $O(1)$ word operations:

$$f' = (4f + b) \bmod 4^k, \qquad r' = \lfloor r/4 \rfloor + (3 - b)\, 4^{k-1},$$

where $f$ is the code of the current k-mer and $r$ the code of its reverse complement. So all $n - k + 1$ canonical k-mers of a string take $O(n)$ time on a [word RAM](/word-ram/) for $k \le 32$.

## Examples and non-examples

**The k-mers of a read.** Let $s = \texttt{GATTACAGATT}$, so $n = 11$.

- For $k = 3$ there are $11 - 3 + 1 = 9$ k-mers: GAT, ATT, TTA, TAC, ACA, CAG, AGA, GAT, ATT. Only 7 are distinct: GAT and ATT occur twice.
- Their canonical forms are ATC, AAT, TAA, GTA, ACA, CAG, AGA, ATC, AAT. For example, $\overline{\texttt{GAT}} = \texttt{ATC} < \texttt{GAT}$, so $\text{can}(\texttt{GAT}) = \texttt{ATC}$.
- For $k = 4$ there are 8 k-mers, and 7 are distinct: GATT occurs twice.

**Palindromes.** ACGT and GAATTC (the EcoRI restriction site) equal their own reverse complements. Both have even length, as the proof above requires. The 3-mer ACG is not a palindrome: $\overline{\texttt{ACG}} = \texttt{CGT}$, and $\text{can}(\texttt{ACG}) = \text{can}(\texttt{CGT}) = \texttt{ACG}$.

**Counts for small $k$.** The counts below come from listing all of $\Sigma^k$.

| $k$ | $4^k$ | palindromes | canonical k-mers |
|---|---|---|---|
| 1 | 4 | 0 | 2 |
| 2 | 16 | 4 | 10 |
| 3 | 64 | 0 | 32 |
| 4 | 256 | 16 | 136 |
| 5 | 1024 | 0 | 512 |
| 6 | 4096 | 64 | 2080 |

**Rolling codes.** In $\texttt{ACGTTGCA}$ with $k = 3$, the first k-mer ACG has code $0 \cdot 16 + 1 \cdot 4 + 2 = 6$ and its reverse complement CGT has code 27. The canonical code is $\min(6, 27) = 6$. The next base is T ($b = 3$), so $f' = (4 \cdot 6 + 3) \bmod 64 = 27$ (CGT) and $r' = \lfloor 27/4 \rfloor + 0 \cdot 16 = 6$ (ACG).

**How long must $k$ be?** In a random genome of length $G$, a fixed k-mer occurs about $G / 4^k$ times by chance. For the human genome, $G \approx 3.1 \times 10^9$ and $\log_4 G \approx 15.8$. At $k = 15$ the chance count is about 2.9, so a 15-mer often occurs by chance. At $k = 21$ it is about $7 \times 10^{-4}$. So assemblers and indexes use $k$ a few units above $\log_4 G$. Real genomes are not random: [genome repeats](/genome-repeat/) make many long k-mers occur more than once at any $k$ shorter than the repeat.

**Non-examples.**

- A pattern with fixed gaps, such as the bases at positions 0, 1, 3 and 4 of a window, is a [spaced seed](/spaced-seed/), not a k-mer.
- A string that contains the unknown base N is not a k-mer over $\Sigma$. Counters skip the k-mers that contain N.
- A *subsequence* of length $k$ (with gaps of any size) is not a k-mer. A k-mer is always contiguous.

## Related definitions

- **q-gram and n-gram.** The same object under other names: string algorithms say $q$-gram, as in the [q-gram lemma](/q-gram-lemma/), and text processing says $n$-gram. This page uses the biology name and adds the strand rules of DNA.
- **Subword complexity.** The number of distinct factors of length $k$ of a word, as a function of $k$, is its [subword complexity](/subword-complexity/).
- **[de Bruijn graph](/de-bruijn-graph/).** The graph with the $(k-1)$-mers as vertices and one edge for each k-mer. A [de Bruijn sequence](/de-bruijn-sequence/) holds each k-mer exactly once.
- **[k-mer index](/kmer-index/).** The lookup structure that maps each k-mer to its positions. It is used to find seeds in [read mapping](/read-mapping/).
- **[Minimizer](/minimizer/).** The smallest k-mer in a window of consecutive k-mers, used to sample k-mers sparsely.
- **[k-mer counting](/kmer-counting/)** is the problem of counting each distinct k-mer of a set of reads, and the **[k-mer spectrum](/kmer-spectrum/)** is the histogram of these counts.

## References
