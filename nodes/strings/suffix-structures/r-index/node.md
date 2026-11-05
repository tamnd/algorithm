---
tag: D8XXKM
kind: data-structure
slug: r-index
name: r-index
aliases:
- run-length BWT index
- run-length compressed suffix array index
area: strings/suffix-structures
level: research
summary: A full-text index whose size is proportional to the number of runs in the BWT.
implements: [full-text-index]
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern, r: the number of runs in the BWT, z: the number of occurrences}
  time: {count: O(m log log n), locate: O((m + z) log log n)}
  space: {extra: O(r)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [fm-index, burrows-wheeler-transform]
see_also: [fm-index, suffix-array, burrows-wheeler-transform, matching-statistics, top-k-document-retrieval, compressed-suffix-array, lz77, full-text-index]
sources:
  - paper: doi:10.1137/1.9781611975031.96
    title: Travis Gagie, Gonzalo Navarro and Nicola Prezza, Optimal-time text indexing in BWT-runs bounded space, SODA 2018
    locator: the toehold lemma during backward search, the sampling of the suffix array at run boundaries, and the computation of phi from O(r) samples
  - paper: doi:10.1145/3375890
    title: Travis Gagie, Gonzalo Navarro and Nicola Prezza, Fully functional suffix trees and optimal text searching in BWT-runs bounded space, Journal of the ACM 67(1), 2020
    locator: the journal version, with the r-index locate bound and the extension to suffix tree functionality in O(r) space
  - paper: doi:10.1007/11496656_5
    title: Veli Mäkinen and Gonzalo Navarro, Succinct suffix arrays based on run-length encoding, CPM 2005
    locator: counting by backward search on the run-length encoded BWT in space proportional to the number of runs
  - paper: doi:10.1007/s00453-017-0327-z
    title: Alberto Policriti and Nicola Prezza, LZ77 computation based on the run-length encoded BWT, Algorithmica 80, 2018
    locator: the sampling of suffix array values at the ends of BWT runs, on which the toehold lemma builds
  - paper: doi:10.1109/focs46700.2020.00097
    title: Dominik Kempa and Tomasz Kociumaka, Resolution of the Burrows-Wheeler transform conjecture, FOCS 2020
    locator: the bound r = O(z log^2 n) relating the number of BWT runs to the number of LZ77 phrases
---

The r-index is a [full-text index](/full-text-index/) for a text $S$ of length $n$ that uses $O(r)$ words of space, where $r$ is the number of runs (maximal blocks of equal symbols) in the [Burrows-Wheeler transform](/burrows-wheeler-transform/) of $S$. It counts the occurrences of a pattern of length $m$ by backward search on the run-length encoded BWT, and it lists all $z$ occurrences using only suffix array samples at the run boundaries: the *toehold lemma* gives one occurrence during the search, and a function $\phi$ computed from $O(r)$ samples gives the others one by one. Gagie, Navarro and Prezza introduced it in 2018. For collections of many similar genomes or versions of a document, $r$ is far smaller than $n$, and the r-index is often the only full-text index that fits in memory.

## In plain words

A collection of a thousand copies of a genome, with small differences, holds little new information beyond the first copy. Most indexes still grow with the full length. The Burrows-Wheeler transform of such a collection has long blocks of the same letter, and the number of blocks grows only with the differences.

The r-index keeps a few numbers for each block and nothing else. To count a pattern, it narrows a range of sorted endings one letter at a time, from the last letter of the pattern, and the block numbers suffice for this. To find where the matches are, it keeps the position of one match while it narrows the range. From one known match position, a small table at the block borders gives the position of the next match in sorted order, and so on for all of them.

## The abstract type

The [full-text index](/full-text-index/) over a fixed text $S$:

- `count(P)`: the number of positions where $P$ occurs in $S$.
- `locate(P)`: the list of these positions, in any order.
- `contains(P)`: whether $P$ occurs.

Some versions also support `extract` (a substring of $S$) and suffix tree operations in $O(r)$ space; this page treats count and locate.

## Representation

Let $t = S\$$, where the [sentinel](/sentinel-character/) $\$$ is smaller than every symbol and occurs once; positions are 0-based, $|t| = n + 1$. Let $SA$ be the [suffix array](/suffix-array/) of $t$ and $BWT[i] = t[SA[i] - 1]$, cyclically ($t[-1] = \$$). The symbols are mapped to ranks $1, \ldots, \sigma$ and $\$$ to 0. Write the BWT as $r$ runs; run $k$ has a head symbol $c_k$, a start $s_k$ and an end $e_k$. The r-index stores, and keeps after construction, only:

- **Run-length BWT.** The heads and starts of the $r$ runs, and for each symbol $c$, the starts and ends of its runs and the number of $c$ before each of them. With these, $BWT[i]$ and $rank_c(i)$, the number of $c$ in $BWT[0 \ldots i-1]$, need one predecessor search. The array $C[c]$ counts the symbols smaller than $c$.
- **Samples at run ends.** $SA[e_k]$ for each run $k$, for the toehold lemma.
- **Samples for $\phi$.** Define $\phi(j) = SA[ISA[j] - 1]$, the text position in the row just above the row of $j$. For each run start $s_k$ with $SA[s_k] \ge 1$, store the pair $(SA[s_k] - 1,\ \phi(SA[s_k] - 1))$, sorted by the first value.

In total $O(r)$ integers. The code builds the suffix array naively to fill these tables and then uses only them; real constructions work in compressed space from the BWT.

## Operations

Backward search keeps the range $[sp, ep)$ of rows whose suffixes start with the part of $P$ read so far, and the toehold $s = SA[ep - 1]$.

```pseudo id=main
SEARCH(P)                                       ▷ returns sp, ep and s = SA[ep − 1]
L1  sp ← 0; ep ← n + 1; s ← SA[n]                 ▷ the sample at the end of the last run
L2  for k ← m − 1 down to 0 do
L3      c ← P[k]
L4      if BWT[ep − 1] = c then q ← s            ▷ the last c in the range is row ep − 1
L5      else q ← SA at the end of the last run of c that starts before ep; if that run ends before sp, return empty
L6      sp ← C[c] + rank_c(sp); ep ← C[c] + rank_c(ep)
L7      if sp ≥ ep then return empty
L8      s ← q − 1                                 ▷ toehold lemma: s = SA[ep − 1] again
LOCATE(P)
L9  (sp, ep, s) ← SEARCH(P); report s; repeat ep − sp − 1 times: s ← φ(s); report s
PHI(x)
L10 find the smallest sampled key y ≥ x, with value φ(y); return φ(y) − (y − x)
```

`count(P)` is $ep - sp$ after SEARCH. The empty pattern occurs at the $n + 1$ positions $0, \ldots, n$, and SEARCH returns the full range for it.

**Toehold lemma.** Let $q$ be the last row in $[sp, ep)$ with $BWT[q] = c$. Then $LF(q) = C[c] + rank_c(q) = ep' - 1$, the last row of the new range, so $SA[ep' - 1] = SA[q] - 1$. If $q = ep - 1$, $SA[q]$ is the current toehold. Otherwise $BWT[q + 1] \ne c$, so $q$ is the end of a run of $c$, and $SA[q]$ is a stored sample.

**The $\phi$ lemma.** If row $i \ge 1$ is not a run start, then $BWT[i - 1] = BWT[i]$, so $LF(i - 1) = LF(i) - 1$, and with $j = SA[i]$ this says $\phi(j - 1) = \phi(j) - 1$. So $\phi$ grows by one along runs of text positions that do not cross a value $SA[s_k]$, and $\phi(x) = \phi(y) - (y - x)$ for the smallest sampled key $y \ge x$.

## Example

Take $S = \texttt{banana}$, $t = \texttt{banana\$}$, with $\$ < \texttt{a} < \texttt{b} < \texttt{n}$.

| row $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $SA[i]$ | 6 | 5 | 3 | 1 | 0 | 4 | 2 |
| suffix | `$` | `a$` | `ana$` | `anana$` | `banana$` | `na$` | `nana$` |
| $BWT[i]$ | a | n | n | b | $ | a | a |

The BWT $\texttt{annb\$aa}$ has $r = 5$ runs: $\texttt{a}$ at 0, $\texttt{nn}$ at 1 to 2, $\texttt{b}$ at 3, $\$$ at 4, $\texttt{aa}$ at 5 to 6. The samples at the run ends are $SA[0] = 6$, $SA[2] = 3$, $SA[3] = 1$, $SA[4] = 0$, $SA[6] = 2$. The $\phi$ samples, from the run starts 0, 1, 3, 5 (the start 4 has $SA = 0$), are $\phi(5) = 6$, $\phi(4) = 0$, $\phi(0) = 1$ and $\phi(3) = 5$. Here $C[\texttt{a}] = 1$ and $C[\texttt{n}] = 5$.

Search for $P = \texttt{ana}$, reading $\texttt{a}$, $\texttt{n}$, $\texttt{a}$:

| step | $c$ | case | $q$ | new $[sp, ep)$ | new $s$ |
|---|---|---|---|---|---|
| start | | | | $[0, 7)$ | $SA[6] = 2$ |
| 1 | a | L4, $BWT[6] = \texttt{a}$ | 2 | $[1, 4)$ | 1 |
| 2 | n | L5, $BWT[3] = \texttt{b}$; last $\texttt{n}$ run ends at row 2, sample 3 | 3 | $[5, 7)$ | 2 |
| 3 | a | L4, $BWT[6] = \texttt{a}$ | 2 | $[2, 4)$ | 1 |

So `count(ana)` is 2, and the toehold is $SA[3] = 1$. Then $\phi(1)$: the smallest key at least 1 is 3, with $\phi(3) = 5$, so $\phi(1) = 5 - 2 = 3 = SA[2]$. `locate(ana)` returns 1 and 3. The code checks this example.

## Correctness

Backward search is correct by the LF-mapping property of the BWT: the rows whose suffixes start with $cX$ are $C[c] + rank_c(sp)$ to $C[c] + rank_c(ep) - 1$ when $[sp, ep)$ are the rows of $X$. The run-length tables compute $rank_c$ exactly: the runs of $c$ before row $i$ contribute their full lengths, and the run that contains $i - 1$, if it is a run of $c$, contributes the part before $i$. The toehold lemma keeps $s = SA[ep - 1]$ by induction on the steps, and the $\phi$ lemma gives $SA[i - 1]$ from $SA[i]$ for each row above $ep - 1$ in the range. The proof file gives the details.

## Complexity

**Space.** The run tables take $2r$ words plus $3r$ words split among the symbols, the run-end samples $r$ words, and the $\phi$ samples at most $2r$ words, plus $\sigma + 1$ for $C$. So $O(r)$ words, against the $n$ words of a plain suffix array and the $O(n)$ bits of an [FM-index](/fm-index/) with full sampling.

**Time.** Each backward step does a constant number of predecessor searches over $O(r)$ sorted values. With binary search, as in the code, each costs $O(\log r)$. With predecessor structures in $O(r)$ space, Gagie, Navarro and Prezza get $O(m \log\log_w(\sigma + n/r))$ time for counting and $O(\log\log_w(n/r))$ more per reported occurrence, and $O(m + z)$ time with $O(r \log\log_w(\sigma + n/r))$ space; $w$ is the word size.

| operation | time (code) | time (paper, $O(r)$ space) |
|---|---|---|
| count | $O(m \log r)$ | $O(m \log\log_w(\sigma + n/r))$ |
| locate | $O((m + z) \log r)$ | count time plus $O(z \log\log_w(n/r))$ |
| space | $O(r)$ words | $O(r)$ words |

**Size of $r$.** For a text with $d$ copies of a base string of length $\ell$ and few edits each, $r$ grows with $\ell$ plus the number of edits, not with $d\ell$. Kempa and Kociumaka proved $r = O(z_{77} \log^2 n)$, where $z_{77}$ is the number of LZ77 phrases, so $r$ is within polylogarithmic factors of the best dictionary compression. For random text $r$ is close to $n$, and the r-index has no advantage.

## Variants

- **Run-length FM-index.** Mäkinen and Navarro (2005) counted in $O(r)$ space but needed $\Theta(n/s)$ samples to locate with a step of $s$; the r-index removes this term.
- **Fully functional suffix trees.** The JACM version supports suffix tree navigation in $O(r)$ space.
- **Matching statistics and MEMs.** With thresholds between runs, the [matching statistics](/matching-statistics/) of a pattern are computed with the r-index (MONI, by Rossi, Oliva, Langmead, Gagie and Boucher), which finds maximal exact matches against pangenomes.
- **Document retrieval.** Listing the documents of a collection that contain a pattern, and [top-k retrieval](/top-k-document-retrieval/), in space close to $O(r)$.
- **Prefix-free parsing construction.** Boucher and others build the BWT and the samples of very large repetitive collections with prefix-free parsing, in space related to the compressed size.
- **Subsampled r-index.** Keeping only some of the samples trades time for space.

## When to use it

Use the r-index for large, highly repetitive collections: pangenomes, many versions of a document, or source code repositories, where counting and locating must work in memory proportional to the compressed size. For a single genome or ordinary text, $r$ is a large fraction of $n$, and an [FM-index](/fm-index/) with regular sampling is simpler and faster.

## Pitfalls

- **Wrong toehold case.** When $BWT[ep - 1] \ne c$, the needed sample is at the end of the last run of $c$ that starts before $ep$, not at the start of the next run.
- **Off-by-one in $\phi$.** The $\phi$ samples are keyed by $SA[s_k] - 1$, the text position just before a run-start value, and the lookup takes the smallest key at least $x$. Keying by $SA[s_k]$ or taking the predecessor gives wrong positions only on some inputs.
- **The cyclic sentinel.** The BWT is taken cyclically, so $BWT[ISA[0]] = \$$. The run of $\$$ is a run like any other, and the row of $\$$ (row 0) counts as a run start.
- **Expecting a small index on any text.** On text without long repeats, $r$ is near $n$ and the r-index is larger than a plain FM-index.
- **Symbols missing from the text.** A pattern symbol that does not occur has no runs; return an empty result before any rank query.

## Implementations

## History

Burrows and Wheeler (1994) noted that their transform creates long runs on repetitive data. Mäkinen and Navarro (2005) built a counting index on the run-length encoded BWT, with space proportional to $r$, but locating needed samples spread over the whole text. Policriti and Prezza (2018) used samples at the run ends to compute the LZ77 parse from the run-length BWT. Gagie, Navarro and Prezza (SODA 2018; Journal of the ACM, 2020) completed the index with the toehold lemma and the $\phi$ samples, giving locate in $O(r)$ space. Kempa and Kociumaka (2020) bounded $r$ by the LZ77 size up to $\log^2 n$, which settled how compressible the measure $r$ is.

## References
