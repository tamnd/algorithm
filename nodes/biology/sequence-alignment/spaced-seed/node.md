---
tag: 0TDJNQ
kind: concept
slug: spaced-seed
name: Spaced seed
aliases:
- gapped seed
- PatternHunter seed
- spaced seed pattern
area: biology/sequence-alignment
level: advanced
summary: A seed that requires matches only at chosen positions of a window, such as 111010010100110111. It hits more true alignments than a contiguous k-mer of the same weight.
prereqs: [seed-and-extend, kmer]
see_also: [blast, kmer-index, minimizer, seed-and-extend, q-gram-filtering, alignment-free-comparison, read-mapping, markov-chain]
sources:
  - paper: doi:10.1093/bioinformatics/18.3.440
    title: Bin Ma, John Tromp and Ming Li, PatternHunter, faster and more sensitive homology search, Bioinformatics 18(3), 2002
    locator: pages 440 to 445 (spaced seeds, the seed 111010010100110111 of weight 11, its sensitivity against the contiguous seed of weight 11, and the overlap argument)
  - paper: "Uri Keich, Ming Li, Bin Ma and John Tromp, On spaced seeds for similarity search, Discrete Applied Mathematics 138(3), 2004, pages 253 to 263"
    title: Keich, Li, Ma and Tromp 2004
    locator: the dynamic program for the exact hit probability of a seed on a random region, and the proof that the best spaced seed beats the contiguous seed for long regions
  - paper: "Ming Li, Bin Ma, Derek Kisman and John Tromp, PatternHunter II, highly sensitive and fast homology search, Journal of Bioinformatics and Computational Biology 2(3), 2004, pages 417 to 439"
    title: Li, Ma, Kisman and Tromp 2004 (PatternHunter II)
    locator: sets of several spaced seeds and their joint sensitivity
  - paper: doi:10.1016/S0022-2836(05)80360-2
    title: Stephen F. Altschul, Warren Gish, Webb Miller, Eugene W. Myers and David J. Lipman, Basic local alignment search tool, Journal of Molecular Biology 215(3), 1990
    locator: pages 403 to 410 (contiguous word seeds, the baseline that spaced seeds improve on)
---

A spaced seed is a pattern of *care* and *don't-care* positions, written as a 0/1 string such as 111010010100110111, that defines when two sequences have a seed hit: they must match at each 1 and may differ at each 0. The number of 1s is the *weight* and the length is the *span*. Ma, Tromp and Li (2002) showed in PatternHunter that a well-chosen spaced seed hits more true alignments than the contiguous seed 11111111111 of the same weight, at about the same number of chance hits. It is a drop-in change to the seed step of [seed and extend](/seed-and-extend/).

## In plain words

A search tool such as BLAST starts from places where the two sequences agree on 11 letters in a row. A spaced seed also asks for 11 agreeing letters, but spread over a window of 18, with some places where it does not care.

Why does that help? Real matches have mismatches here and there. With the plain seed, if one test fails at one place, the next place you try shares almost all of its letters with it, so it tends to fail too. The tries are not independent. With a spaced seed, two nearby tries share only a few letters, so a failure in one says little about the next. You get about the same number of hits on average, but they are spread over more of the true matches, so fewer matches get no hit at all.

## The idea

**The model.** A seed is a string $Q$ over $\{1, 0\}$ that starts and ends with 1, of span $\ell$ and weight $w$. Two sequences $x$ and $y$ over an alphabet of size $\sigma$ have a *hit* at $(i, j)$ if $x[i + t] = y[j + t]$ for every $t$ with $Q[t] = 1$. The contiguous seed of weight $w$ is $1^w$, which is a $w$-[mer](/kmer/) match. For the analysis, an ungapped alignment of length $L$ is a 0/1 string $R$ with $R[t] = 1$ when column $t$ is a match; in the *Bernoulli model* the columns are independent and each is a match with probability $p$. The *sensitivity* of $Q$ is the probability that $R$ contains a hit, that is, an offset $i$ with $R[i + t] = 1$ for every care position $t$.

**The index.** A spaced seed is looked up like a $k$-mer. The *spaced word* at a position is the string of letters at the care positions, $w$ letters in all. A [hash table](/hash-table/) or an array of $\sigma^w$ lists, keyed by spaced words, finds every hit, so the cost of the lookup is the same as for a contiguous $w$-mer.

**Same mean, different spread.** Let $N$ be the number of hits in $R$. A placement at offset $i$ hits with probability $p^w$, for any seed of weight $w$, so

$$\mathbb{E}[N] = (L - \ell + 1)\, p^w.$$

In random sequences with uniform letters the same holds with $p = 1/\sigma$, so the expected number of chance hits per position pair is $\sigma^{-w}$, the same for every seed of weight $w$. The longer span even gives a few fewer placements. What differs is the variance. Two placements at a shift of $j$ share the care positions in the overlap of $Q$ with itself shifted by $j$. For $1^{11}$ the overlap at shift $j$ is $11 - j$. For the PatternHunter seed the overlaps for $j = 1, \ldots, 17$ are

$$5, 5, 5, 4, 4, 3, 3, 4, 3, 2, 3, 3, 3, 2, 3, 2, 1.$$

So its hits are much less correlated. For a fixed mean, a smaller second moment $\mathbb{E}[N^2]$ means a larger chance of at least one hit, by the second moment bound $\Pr(N \ge 1) \ge \mathbb{E}[N]^2 / \mathbb{E}[N^2]$. The contiguous seed wastes its hits in clusters on the same good stretch.

**Exact sensitivity.** The probability of at least one hit is computed exactly by a dynamic program over the columns of $R$ (Keich, Li, Ma and Tromp 2004). In the code on this page the state is the set of placements that have started and have not yet failed, stored as a bit mask of at most $\ell - 1$ bits. Each column adds a new placement, removes the ones that see a mismatch at a care position, and moves the rest one step. A placement that reaches the end of the seed is a hit, and its probability leaves the program. The time is $O(L \cdot r)$ for $r$ reachable states, with $r \le 2^{\ell - 1}$ in the worst case; for the seeds above, $r$ is small. Summing over all $2^L$ strings gives the same value for small $L$.

**Choosing a seed.** The sensitivity depends on $L$ and $p$, and no single seed is best for all of them. Seeds are chosen by computing the sensitivity of many candidates with the dynamic program, for the $L$ and $p$ of interest. A seed and its reverse have the same sensitivity in the Bernoulli model.

## Examples

**The PatternHunter seed against the contiguous seed.** Weight 11 for both; span 18 against 11. Hit probabilities in the Bernoulli model, exact by the dynamic program:

| region length $L$ | $p$ | $1^{11}$ | 111010010100110111 |
|---|---|---|---|
| 64 | 0.6 | 0.0785 | 0.1317 |
| 64 | 0.7 | 0.3002 | 0.4671 |
| 64 | 0.8 | 0.7140 | 0.8821 |
| 64 | 0.9 | 0.9824 | 0.9984 |
| 18 | 0.7 | 0.0613 | 0.0198 |
| 32 | 0.7 | 0.1416 | 0.1995 |
| 100 | 0.7 | 0.4439 | 0.6635 |

At $L = 64$ and $p = 0.7$, the expected number of hits is $54 \cdot 0.7^{11} = 1.068$ for the contiguous seed and $47 \cdot 0.7^{11} = 0.929$ for the spaced seed. The spaced seed has fewer hits on average, but finds 47% of the regions instead of 30%. For a short region of 18 columns the contiguous seed wins, because the spaced seed has only one placement there.

**A small case.** Weight 3, $L = 8$, $p = 0.7$:

| seed | 111 | 1101 | 1011 | 11001 | 10101 |
|---|---|---|---|---|---|
| hit probability | 0.776322 | 0.780027 | 0.780027 | 0.736191 | 0.692973 |

So 1101 beats 111, but 11001 and 10101 are worse than 111. Not every spaced seed helps; the pattern matters. 1101 and its reverse 1011 have the same value.

**A pair that BLAST misses.** Let $y$ be a DNA sequence of 64 bases equal to $x$ except at every eighth position. The match string is $R = (1111111\,0)^8$. The contiguous seed $1^{11}$ never hits, which is why the 11-letter words of BLASTN find nothing in the example on the [BLAST](/blast/) page. The PatternHunter seed hits $R$ at the 12 offsets $1, 4, 9, 12, 17, 20, 25, 28, 33, 36, 41, 44$, because its 0s can fall on the mismatches.

## Where it is used

- **PatternHunter** (2002) used the seed 111010010100110111 for DNA search and reported both higher sensitivity and higher speed than BLASTN with 11-letter words.
- **Several seeds.** PatternHunter II (2004) uses a set of spaced seeds; a region is found if any seed hits. With enough seeds the sensitivity comes close to that of Smith-Waterman at a fraction of the cost.
- **Discontiguous megablast** in NCBI BLAST uses spaced templates for cross-species DNA search.
- **Read mapping and protein search.** Some read mappers and protein search tools use spaced seeds in their [k-mer index](/kmer-index/), alone or with [minimizers](/minimizer/).
- **Alignment-free comparison.** Counting spaced words instead of contiguous $k$-mers gives distance estimates that depend less on the positions of mismatches. See [alignment-free comparison](/alignment-free-comparison/).
- **Lossless filters.** For approximate matching with at most $e$ mismatches, spaced seeds can be chosen so that every such match has a hit, like the [q-gram](/q-gram-filtering/) filters of string matching, but often with fewer chance hits.

The idea is a change of the seed only. The index, the extension and the statistics of the search stay the same. The sensitivity numbers come from the Bernoulli model; real alignments have gaps and runs of conserved positions, such as the third positions of codons, and seeds can be tuned for those patterns.

## References
