---
tag: 39NYBT
kind: data-structure
slug: positional-burrows-wheeler-transform
name: Positional Burrows-Wheeler transform
aliases:
- PBWT
area: biology/population-genetics
level: advanced
summary: "Durbin's sorting of haplotypes at each site by their reversed prefixes. It finds all set-maximal matches in O(NM) time for M haplotypes and N sites, which is linear in the input size."
model: word-ram
complexity:
  vars: {M: the number of haplotypes, N: the number of sites, R: the number of reported matches}
  time: {build: O(N M), long-matches: O(N M + R), set-maximal-matches: O(N M + R)}
  space: {streaming: O(M), all-arrays: O(N M)}
history:
  year: 2014
  people: [Richard Durbin]
  note: "Durbin introduced the PBWT in 2014, with the update of the sort order and of the divergence array in one pass per site, the reports of long and set-maximal matches, and a compressed storage of haplotype panels."
prereqs: [burrows-wheeler-transform, counting-sort]
see_also: [fm-index, suffix-array, radix-sort, li-stephens-model, haplotype-phasing, identity-by-descent, genotype-imputation, extended-haplotype-homozygosity]
sources:
  - paper: doi:10.1093/bioinformatics/btu014
    title: Richard Durbin, Efficient haplotype matching and storage using the positional Burrows-Wheeler transform (PBWT), Bioinformatics 30(9), 2014
    locator: pp. 1266-1272 (Algorithms 1 and 2 for the prefix and divergence arrays, Algorithm 3 for long matches, Algorithm 4 for set-maximal matches, Algorithm 5 for matches of a new sequence, and the bound on the number of set-maximal matches)
  - paper: "Michael Burrows and David J. Wheeler, A block-sorting lossless data compression algorithm, SRC Research Report 124, Digital Equipment Corporation, 1994"
    title: Burrows and Wheeler 1994
    locator: the transform that sorts the rotations of one string, which the PBWT adapts to many aligned strings
---

The positional Burrows-Wheeler transform (PBWT) is a set of arrays that describe, for a panel of $M$ binary haplotypes over $N$ sites, the order of the haplotypes sorted by their reversed prefixes at every site $k$. A second array at each site gives the start of the match of each haplotype with its neighbor in that order. Durbin (2014) showed that both arrays at site $k + 1$ come from those at site $k$ in one stable pass over column $k$. So the transform takes $O(NM)$ time, and from it all set-maximal matches between haplotypes can be listed in $O(NM)$ time, which is linear in the input size. Unlike the [Burrows-Wheeler transform](/burrows-wheeler-transform/) and the [FM-index](/fm-index/), which sort the suffixes of one string, the PBWT sorts many aligned strings by their prefixes read backward from each site.

## In plain words

Think of many copies of a chromosome, each written as a row of 0s and 1s, one column per variant. At each column, put the rows in order by what they read just before that column, then the column before that, and so on going back. Rows that share a long stretch ending at that column then sit next to each other.

When you move one column to the right, you do not sort again. You go down the current order once and put each row in one of two piles, by its value in the new column, keeping the order inside each pile. The two piles, one after the other, are the new order. Next to the order, the structure keeps for each row where its shared stretch with the row above begins. That is enough to find all long shared stretches.

## The abstract type

**Input.** Haplotypes $x_0, \ldots, x_{M-1} \in \{0, 1\}^N$. Write $x_i[s, e)$ for the sites $s, \ldots, e - 1$ of $x_i$.

**Prefix arrays.** For $k = 0, \ldots, N$, $a_k$ is the permutation of $0, \ldots, M - 1$ that sorts the haplotypes by the reversed prefix $x_i[k - 1], x_i[k - 2], \ldots, x_i[0]$ in lexicographic order, with ties broken by the index $i$. So $a_0$ is the identity.

**Divergence arrays.** For $k \ge 0$ and $1 \le r < M$, $d_k[r]$ is the smallest $s$ such that $x_{a_k[r]}[s, k) = x_{a_k[r-1]}[s, k)$; it is $k$ if the two haplotypes differ at site $k - 1$. By convention $d_k[0] = k$.

**Matches.** A match between $x_i$ and $x_j$ is an interval $[s, e)$ with $s < e$ on which they agree. It is maximal if it cannot grow: $s = 0$ or $x_i[s - 1] \ne x_j[s - 1]$, and $e = N$ or $x_i[e] \ne x_j[e]$. A maximal match of $x_i$ to $x_j$ on $[s, e)$ is set-maximal if no match of $x_i$ to any haplotype covers $[s, e)$ and is longer.

**Queries.** Report all maximal matches of length at least $L$. Report all set-maximal matches. Find the longest matches of a new haplotype $z$ to the panel.

## Representation

At each site, the structure holds $a_k$ and $d_k$, two integer arrays of length $M$. A program that streams over the sites keeps only the current pair, in $O(M)$ space. To store a panel, Durbin keeps the column $y_k[r] = x_{a_k[r]}[k]$ in sort order instead of $a_k$. Because similar haplotypes are adjacent, $y_k$ has long runs of equal values and compresses well with run-length coding, and $a_{k+1}$ can be computed from $a_k$ and $y_k$.

## Operations

**Building the arrays.** Durbin's Algorithm 2 computes $(a_{k+1}, d_{k+1})$ from $(a_k, d_k)$ and column $k$:

```pseudo id=main
PBWT-BUILD(x_0, ..., x_{M-1})
L1  a ← (0, 1, ..., M-1); d ← (0, ..., 0)
L2  for k = 0 to N-1 do
L3      zeros, ones ← empty; p ← k+1; q ← k+1
L4      for r = 0 to M-1 do                         ▷ in the order a
L5          p ← max(p, d[r]); q ← max(q, d[r])
L6          if x_{a[r]}[k] = 0 then append (a[r], p) to zeros; p ← 0
L7          else append (a[r], q) to ones; q ← 0
L8      a ← indices of zeros then of ones; d ← their divergences
L9  return the arrays a_0..a_N and d_0..d_N
```

Line L6 puts a haplotype with 0 at site $k$ in the zero pile. Its divergence in the new order is the largest $d$ seen since the previous row with 0 at site $k$, because its new neighbor above is that row, and the match between them is the intersection of the matches of the rows in between. The value $k + 1$ for the first row of each pile records that it has no match ending at site $k + 1$ with the row above it. Line L7 does the same for the ones.

**Long matches.** At site $k$, cut the order $a_k$ into blocks at the rows $r$ with $d_k[r] > k - L$. Two rows in the same block share at least $L$ sites before $k$, and two rows in different blocks do not. Within a block, a pair whose values at site $k$ differ (or any pair when $k = N$) is a maximal match of length at least $L$ ending at $k$. Durbin's Algorithm 3 lists these pairs by splitting each block by the value at site $k$, in time $O(M)$ per site plus the size of the output.

**Set-maximal matches.** At site $k$, the longest match of $x_{a_k[r]}$ ending at $k$ is with the row above or the row below, with start $\min(d_k[r], d_k[r + 1])$. Algorithm 4 scans up from $r$ while the divergences stay at most this start, and down in the same way. If any row in this range has the same value at site $k$, the match goes on past $k$ and none is reported. Otherwise each row in the range gives a set-maximal match ending at $k$. Sentinels $d_k[0] = d_k[M] = k + 1$ stop the scans at the ends.

**Matching a new haplotype.** Durbin's Algorithm 5 keeps, for a new sequence $z$, the interval of rows of $a_k$ that share the longest suffix with $z[0, k)$, and updates it at each site with rank counts on $y_k$, in the way that backward search updates an interval in the [FM-index](/fm-index/). It reports the set-maximal matches of $z$ in time $O(N)$ beyond the precomputed counts.

## Example

Five haplotypes over five sites:

| | site 0 | site 1 | site 2 | site 3 | site 4 |
|---|---|---|---|---|---|
| $x_0$ | 0 | 1 | 0 | 1 | 0 |
| $x_1$ | 1 | 1 | 0 | 0 | 1 |
| $x_2$ | 0 | 1 | 1 | 1 | 0 |
| $x_3$ | 1 | 0 | 0 | 0 | 1 |
| $x_4$ | 0 | 1 | 0 | 1 | 1 |

The arrays are

| $k$ | $a_k$ | $d_k$ |
|---|---|---|
| 0 | 0 1 2 3 4 | 0 0 0 0 0 |
| 1 | 0 2 4 1 3 | 1 0 0 1 0 |
| 2 | 3 0 2 4 1 | 2 2 0 0 1 |
| 3 | 3 0 4 1 2 | 3 2 0 1 3 |
| 4 | 3 1 0 4 2 | 4 2 4 0 3 |
| 5 | 0 2 3 1 4 | 5 3 5 2 4 |

At $k = 1$, column 0 is $(0, 1, 0, 1, 0)$ in the order $a_0$, so the zero pile is $0, 2, 4$ and the one pile is $1, 3$. At $k = 5$, the reversed prefixes are $01010$ for $x_0$, $01110$ for $x_2$, $10001$ for $x_3$, $10011$ for $x_1$ and $11010$ for $x_4$, which is the order $a_5$. The entry $d_5 = 2$ for $x_1$ says that $x_1$ and $x_3$ agree on sites 2 to 4.

With $L = 3$, the long matches are $x_0$ and $x_4$ on $[0, 4)$, found at $k = 4$, where they are adjacent with $d_4 = 0$ and differ at site 4, and $x_1$ and $x_3$ on $[2, 5)$, found at $k = 5$. The set-maximal matches of $x_0$ are to $x_4$ on $[0, 4)$ and to $x_2$ on $[3, 5)$; its shorter match to $x_2$ on $[0, 2)$ is covered by the match to $x_4$ and is not set-maximal for $x_0$.

## Correctness

The main claim is that line L8 gives the true $a_{k+1}$ and $d_{k+1}$. For the order: two haplotypes with different values at site $k$ compare by that value, since it is the first symbol of the reversed prefix of length $k + 1$, so all zeros come before all ones. Two haplotypes with the same value compare by their reversed prefixes of length $k$, which is their order in $a_k$, and the pass keeps that order within each pile. Ties remain broken by index because the pass is stable. For the divergence: if rows $r' < r$ of $a_k$ are adjacent in the new zero pile, the match between them ending at $k$ starts at $\max(d_k[r' + 1], \ldots, d_k[r])$, because the common suffix of two rows of a sorted list is the minimum of the common suffixes of the adjacent pairs between them. Adding site $k$, where both have 0, keeps the start. This is the value of $p$ at line L6. The claims for the match reports follow from the same fact: the haplotypes that share at least $\ell$ sites before $k$ with a given row form a contiguous range of the order around it. The full proof is below.

## Complexity

- **Building.** Each site costs $O(M)$, so all arrays take $O(NM)$ time. Space is $O(M)$ when streaming and $O(NM)$ to keep all arrays.
- **Long matches.** $O(NM)$ time plus the number of reported pairs.
- **Set-maximal matches.** $O(NM)$ time plus the output. Durbin shows that the number of set-maximal matches is at most a fixed multiple of $NM$, provided there are no large groups of haplotypes identical over all $N$ sites, so the total is $O(NM)$.
- **Storage.** With run-length coding of the columns $y_k$, panels of real haplotypes take far less than $NM$ bits, since adjacent rows tend to agree.
- **New haplotype.** $O(N)$ time per query with Algorithm 5, given count arrays over the stored columns.

## Variants

- **Bidirectional and dynamic PBWT.** Later work supports insertion and deletion of haplotypes, and runs the transform in both directions along the genome.
- **Multi-allelic sites and missing data.** A site with $c$ alleles splits the order into $c$ piles in the same stable pass. Missing values need a rule for where to place the row.
- **Uses in methods.** Phasing and imputation programs use the PBWT to pick a small set of haplotypes that match a target well over a region, and then run a [Li-Stephens](/li-stephens-model/) hidden Markov model on that set. Searches for segments shared [identical by descent](/identity-by-descent/) list long matches across large panels.
- **Relation to other transforms.** The update is one pass of a stable [counting sort](/counting-sort/) by one symbol, the step of LSD [radix sort](/radix-sort/) that sorts from the last character. Running it over all sites sorts the reversed prefixes, while the [suffix array](/suffix-array/) and the BWT sort the suffixes of one text.

## When to use it

Use it when you have many aligned haplotypes over the same sites and need long exact matches between them, or between a new haplotype and the panel, for phasing, imputation, the search for shared segments, or compressed storage. For matches between unaligned sequences, use a suffix array or an FM-index. For approximate matches with errors, the PBWT gives exact matches only, which methods then join or extend.

## Pitfalls

- **Exact matches only.** One genotype error splits a long match in two. Methods that need tolerance to errors combine matches or use the PBWT only to choose candidates.
- **Divergence convention.** $d_k[r]$ is a start position, not a length; the length of the match is $k - d_k[r]$. Mixing the two conventions is a common bug.
- **The first row and the sentinels.** The value $k + 1$ for the first row of each pile, and the sentinels in Algorithm 4, keep matches from running across the pile boundary or off the ends of the order.
- **Identical haplotypes.** Many identical haplotypes make the number of set-maximal matches large, as in Durbin's caveat, and the output can then exceed $O(NM)$.
- **Sites must be aligned.** All haplotypes must have the same sites in the same order. Indels and different variant sets break the model.

## Implementations

## History

Burrows and Wheeler (1994) sorted the rotations of a string for compression, and the FM-index of Ferragina and Manzini made the result searchable. Durbin (2014) adapted the idea to a panel of aligned haplotypes: instead of sorting the suffixes of one text, sort all haplotypes by their reversed prefixes at each site. The paper gave the algorithms for the prefix and divergence arrays, the reports of long and set-maximal matches, the matching of a new sequence, and a compressed storage of large haplotype panels. The PBWT then became a part of several phasing, imputation and shared-segment programs.

## References
