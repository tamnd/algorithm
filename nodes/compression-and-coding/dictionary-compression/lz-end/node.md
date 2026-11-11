---
tag: 71G02H
kind: algorithm
slug: lz-end
name: LZ-End
aliases:
- LZ-End parsing
area: compression-and-coding/dictionary-compression
level: research
summary: An LZ77 variant in which each copy must end where an earlier phrase ends. Any phrase can then be decoded in time linear in its length.
solves: [lossless-compression]
model: word-ram
complexity:
  vars: {n: the length of the text, z: the number of phrases, σ: the alphabet size}
  time: {worst: O(z·n·log n)}
  space: {extra: O(σ·n)}
properties: {deterministic: true, recursive: false, online: false, comparison: false}
history:
  year: 2010
  people: [Sebastian Kreft, Gonzalo Navarro]
  note: Kreft and Navarro gave LZ-End at the Data Compression Conference in 2010, as a parse of repetitive texts with fast random access.
prereqs: [lz77, fm-index]
see_also: [lempel-ziv-factorization, longest-previous-factor, lz-index, string-attractor, r-index, fenwick-tree, sparse-table, burrows-wheeler-transform]
sources:
  - paper: doi:10.1109/DCC.2010.29
    title: Sebastian Kreft and Gonzalo Navarro, LZ77-like compression with fast random access, Data Compression Conference (DCC 2010), 239-248
    locator: the definition of the LZ-End parse, its extraction algorithm, and its construction by backward search on the reversed text
  - paper: doi:10.1016/j.tcs.2012.02.006
    title: Sebastian Kreft and Gonzalo Navarro, On compressing and indexing repetitive sequences, Theoretical Computer Science 483, 115-133, 2013
    locator: the journal version, with LZ-End, its extraction and the self-index built on it
  - paper: doi:10.4230/LIPIcs.ESA.2017.53
    title: Dominik Kempa and Dmitry Kosolobov, LZ-End parsing in linear time, 25th European Symposium on Algorithms (ESA 2017), LIPIcs 87, 53:1-53:14
    locator: the abstract (a deterministic construction in linear time and space for an integer alphabet of polynomial size)
  - paper: doi:10.1109/DCC.2017.73
    title: Dominik Kempa and Dmitry Kosolobov, LZ-End parsing in compressed space, Data Compression Conference (DCC 2017), 350-359
    locator: "the abstract (O(n log l) expected time and O(z + l) space, where l is the length of the longest phrase)"
  - paper: doi:10.1137/1.9781611977073.111
    title: Dominik Kempa and Barna Saha, An upper bound and linear-space queries on the LZ-End parsing, SODA 2022, 2847-2866
    locator: the main bound, that the number of LZ-End phrases is O(z log^2 n) where z is the number of LZ77 phrases
  - paper: doi:10.4230/LIPIcs.CPM.2023.3
    title: Hideo Bannai, Mitsuru Funakoshi, Kazuhiro Kurita, Yuto Nakashima, Kazuhisa Seto and Takeaki Uno, Optimal LZ-End parsing is hard, 34th Symposium on Combinatorial Pattern Matching (CPM 2023), LIPIcs 259, paper 3
    locator: the abstract (the optimal LZ-End parse is NP-complete to compute, and the greedy parse can have close to twice as many phrases)
  - url: https://arxiv.org/abs/2106.01173
    title: Takumi Ideue, Takuya Mieno, Mitsuru Funakoshi, Yuto Nakashima, Shunsuke Inenaga and Masayuki Takeda, On the approximation ratio of LZ-End to LZ77, arXiv 2106.01173, 2021
    locator: the abstract (the ratio approaches 2 on the period-doubling sequence over a binary alphabet)
---

LZ-End is a variant of [LZ77](/lz77/) in which each phrase is a copy of earlier text followed by one explicit symbol, with one extra rule: the copy must end exactly where an earlier phrase ends. Kreft and Navarro (2010) gave it for very repetitive texts, such as versions of a document or genomes of one species. The rule costs some phrases compared with LZ77, but it makes random access cheap: a phrase, or any text that ends at a phrase end, is decoded with one step per symbol, with no long chains of copies of copies. Greedy parsing as below takes $O(z \cdot n \log n)$ time in this version, and Kempa and Kosolobov (2017) showed how to compute it in $O(n)$ time.

## In plain words

An LZ77 file says "copy 5 symbols from 300 symbols back, then write `d`". To read one symbol in the middle of the file, you follow the copy back. The source of that copy can be a copy too, and so on, and in a bad case you must decode most of the file.

LZ-End adds one rule: a copy can only end at a place where an earlier phrase ended. The last symbol of each phrase is written in the file. So to read a phrase from right to left, you take its last symbol directly, then the copy before it ends at the end of an earlier phrase, so you start there with its last symbol, and so on. Each step gives one new symbol. The price is that the copies are a little shorter, so there are a few more phrases than in LZ77.

## The problem

The input is a string $t = t[0 \ldots n-1]$. The output is the *LZ-End parse* $t = Z_0 Z_1 \cdots Z_{z-1}$. Let $E_q$ be the position of the last symbol of $Z_q$. If $Z_0 \cdots Z_{p-1} = t[0 \ldots i-1]$, then $Z_p = t[i \ldots i+\ell]$, where $\ell$ is the largest number with $\ell \le n - 1 - i$ such that $t[i \ldots i+\ell-1]$ is a suffix of $t[0 \ldots E_q]$ for some $q < p$. The empty string counts as a suffix, so $\ell = 0$ is always possible. The phrase is stored as $(q, \ell, t[i+\ell])$: the source phrase, the copy length and the explicit symbol, with $q = -1$ when $\ell = 0$. The bound $\ell \le n-1-i$ keeps one explicit symbol in the last phrase; Kreft and Navarro add a unique end symbol instead.

The copy lies inside $t[0 \ldots i-1]$, so it never overlaps the phrase it is part of. This is a difference from LZ77, where a copy can overlap.

## The algorithm

The copy $t[i \ldots j]$ must be a suffix of a prefix $t[0 \ldots E]$. Read backwards, the copy is a prefix of $t[E] t[E-1] \cdots t[0]$, which is a suffix of the reversed text $t^R$. So the parser keeps an [FM-index](/fm-index/) of $t^R$ and the interval $[sp, ep)$ of the suffixes of $t^R$ that start with the reversed copy. A new symbol $t[j]$ at the end of the copy goes at the front of the reversed copy, which is one step of backward search. Two more structures answer questions about the interval:

- a [Fenwick tree](/fenwick-tree/) over the ranks of $t^R$, with a mark at the rank of each reversed prefix $t[0 \ldots E_q]$ of an existing phrase end: "is a phrase end in the interval, and which one?";
- a [sparse table](/sparse-table/) for range minima of the prefix end $E$ over the ranks: "does the copy still occur inside $t[0 \ldots i-1]$?".

```pseudo id=main
LZ-END(t)
L1  build the FM-index of the reversed text, the range minima of the prefix ends, an empty mark set; i ← 0
L2  while i < n do
L3      (sp, ep) ← all ranks; ℓ ← 0; q ← −1; j ← i
L4      while j < n − 1 do
L5          (sp, ep) ← backward step of (sp, ep) with t[j]       ▷ now the interval of t[i .. j] reversed
L6          if the interval is empty or each prefix end in it is ≥ i then break
L7          r ← the first marked rank ≥ sp
L8          if r < ep then ℓ ← j − i + 1; q ← the phrase of r      ▷ t[i .. j] ends at a phrase end
            j ← j + 1
L9      output (q, ℓ, t[i + ℓ])
L10     mark the rank of the prefix t[0 .. i + ℓ]; i ← i + ℓ + 1
L11 return the phrases
```

The loop of line L4 cannot stop at the first length with no mark in the interval. A copy can end at a phrase end while a shorter prefix of it does not, so the set of good lengths is not closed under shorter lengths. The loop goes on while the copy occurs at all in $t[0 \ldots i-1]$, which is a property that does hold for each shorter prefix (line L6), and it keeps the last length with a mark.

**Decoding and random access.** Full decoding is the same as for LZ77: copy $\ell$ symbols that end at $E_q$, then append the symbol. To get $t[a \ldots e]$ where $e$ is a phrase end $E_p$, without the rest of the text:

1. write the explicit symbol of $Z_p$ at position $e$;
2. the next $k = \min(\ell_p, \text{the rest})$ symbols to the left are the last $k$ symbols of $t[0 \ldots E_{q_p}]$, so solve this as a new task that again ends at a phrase end;
3. if more symbols are needed, they end at $E_{p-1}$, so continue with $Z_{p-1}$.

Each step writes one symbol, so $t[a \ldots e]$ takes $e - a + 1$ steps, plus the time to find the phrase that ends at a position (a rank on a bit vector of phrase ends). For any substring $t[a \ldots b]$, extend $b$ to the end of its phrase. The cost is then $O(b - a + h)$, where $h$ is the length of the longest phrase. The implementation keeps the tasks on an explicit stack, so a long chain of sources does not need deep recursion.

## Example

Let $t$ = `alabaralalabarda` ($n = 16$).

| phrase $p$ | start $i$ | phrase ends so far | longest copy that ends at a phrase end | $(q, \ell, \text{symbol})$ | $Z_p$ |
|---|---|---|---|---|---|
| 0 | 0 | none | empty | $(-1, 0, a)$ | `a` |
| 1 | 1 | 0 | empty (`l` is not a suffix of `a`) | $(-1, 0, l)$ | `l` |
| 2 | 2 | 0, 1 | `a`, a suffix of $t[0 \ldots 0]$ | $(0, 1, b)$ | `ab` |
| 3 | 4 | 0, 1, 3 | `a`, a suffix of $t[0 \ldots 0]$ | $(0, 1, r)$ | `ar` |
| 4 | 6 | 0, 1, 3, 5 | `al`, a suffix of $t[0 \ldots 1]$ | $(1, 2, a)$ | `ala` |
| 5 | 9 | 0, 1, 3, 5, 8 | `labar`, a suffix of $t[0 \ldots 5]$ = `alabar` | $(3, 5, d)$ | `labard` |
| 6 | 15 | ... | empty (the last symbol must be explicit) | $(-1, 0, a)$ | `a` |

At $i = 9$ the lengths 1, 2, 3 and 5 are good (`l` ends at 1, `la` ends at 8, `lab` ends at 3, `labar` ends at 5), but the length 4 is not: `laba` occurs at 2 but ends at 5, where `alabar` ends with `abar`. This is why line L4 must go past a bad length. The LZ77 parse with a copy and a symbol is `a|l|ab|ar|alal|abard|a`, also 7 phrases.

On other inputs the gap is larger. A run `a`...`a` of length $2^k - 1$ gives phrases of lengths $1, 2, 4, \ldots, 2^{k-1}$, so $k$ phrases, while LZ77 needs 2, because its copy can overlap itself. On `abcabcabcabc`, LZ-End gives `a|b|c|abca|bcab|c` (6 phrases) and LZ77 gives 4. On the first 4000 symbols of the Fibonacci word, LZ-End gives 22 phrases and LZ77 17; on the first 4000 symbols of the period-doubling word, 23 and 13. The tests check all these numbers.

## Correctness

Line L5 keeps the invariant that $[sp, ep)$ is the set of ranks of the suffixes of $t^R$ that start with $t[j] t[j-1] \cdots t[i]$, that is, of the prefixes $t[0 \ldots E]$ that end with $t[i \ldots j]$. A rank in the interval is marked exactly when its $E$ is the end of an earlier phrase, so line L8 records exactly the good lengths. Line L6 stops only when no prefix that ends before $i$ ends with $t[i \ldots j]$; then no longer copy can be good either. So $\ell$ is the largest good length, which is the definition. The proofs of the parse, of the extraction and of $z_{77} \le z_{\text{end}}$ are in the proof file below.

## Complexity

- **Index.** The FM-index of $t^R$ needs a suffix array; the implementation uses prefix doubling, $O(n \log^2 n)$ time, and occurrence tables of $O(\sigma n)$ words, so a backward step takes $O(1)$ time. A wavelet tree makes the space $O(n)$ words and the step $O(\log \sigma)$.
- **Parsing.** Each step of the loop of line L4 takes $O(\log n)$ time for the Fenwick tree and $O(1)$ for the other parts. The loop for a phrase at $i$ runs at most $1 + m_i$ times, where $m_i$ is the length of the longest prefix of $t[i \ldots]$ that occurs in $t[0 \ldots i-1]$. As $m_i < n$, the total is $O(z \cdot n \log n)$. On a run, $m_i = i$ and the phrases double, so the total is only $O(n \log n)$.
- **Extraction.** $O(\ell + h)$ for $\ell$ symbols, as above.

Kempa and Kosolobov (2017) build the LZ-End parse in $O(n)$ time and space for an integer alphabet of polynomial size, and in a second paper in $O(n \log \lambda)$ expected time and $O(z + \lambda)$ space, where $\lambda$ is the length of the longest phrase.

## Properties

- **Never fewer phrases than LZ77.** Let $z_{77}$ be the number of phrases of the greedy LZ77 parse with an unbounded window, a copy and one symbol per phrase. Then $z_{77} \le z_{\text{end}}$: each LZ-End copy also occurs earlier, so the LZ-End parse is one of the parses that greedy LZ77 beats (proof in the proof file).
- **Not much more.** Kempa and Saha (2022) proved $z_{\text{end}} = O(z_{77} \log^2 n)$. In the other direction, the ratio can come close to 2: Kreft and Navarro gave such strings over large alphabets, and Ideue et al. (2021) over a binary alphabet.
- **Greedy is not optimal.** Unlike LZ77, the set of allowed copies depends on the earlier phrases, so the greedy parse can have more phrases than the best parse that follows the same rule. Bannai et al. (2023) showed that the best such parse is NP-hard to compute.
- **Offline.** The parser above needs the whole text for the index. Each phrase itself depends only on the text up to its end.

## Variants and improvements

- **Linear time.** Kempa and Kosolobov (2017) replace the backward search with other tools to get $O(n)$ time.
- **Compressed space.** The construction of Kempa and Kosolobov with $O(z + \lambda)$ space makes one left-to-right pass that is correct with high probability, and one right-to-left pass that checks the result.
- **Self-indexes.** Kreft and Navarro built a self-index on the LZ-End parse, which answers pattern searches and also extracts text; see the [LZ-index](/lz-index/) and the [r-index](/r-index/) for other indexes for repetitive texts.
- **A bounded window.** A real coder can cap the distance to the source phrase, at the cost of more phrases.

## When to use it

Use LZ-End for a large, very repetitive collection where you must read short parts many times without decoding all of it, such as versioned documents or many genomes of one species. For plain compression of a whole file, LZ77 or a format based on it gives fewer phrases and is simpler. For pattern search on repetitive texts, compare with the r-index.

## Pitfalls

- **Stopping at the first bad length.** The good copy lengths have gaps (the length 4 at $i = 9$ above). A parser that stops at the first length with no phrase end gives a valid parse, but not the LZ-End parse, and it can have more phrases.
- **Overlap.** An LZ77 coder copies symbol by symbol, so its copy may overlap the phrase. An LZ-End copy ends at an earlier phrase end, so it never overlaps. Code shared with LZ77 must not use the overlap rule.
- **The last phrase.** Decide how the end of the text is handled: a unique end symbol, or the rule $\ell \le n - 1 - i$ used here. The two give different last phrases.
- **Recursion in extraction.** The chain of sources can be long. Use an explicit stack, as the implementation does.

## Implementations

## History

Sebastian Kreft and Gonzalo Navarro gave LZ-End at the Data Compression Conference in 2010, with the extraction algorithm and a construction by backward search on the reversed text. The journal version (2013) adds a self-index. Kempa and Kosolobov gave a linear-time construction and a construction in compressed space in 2017. Kempa and Saha proved in 2022 that LZ-End is within an $O(\log^2 n)$ factor of LZ77, and Bannai et al. showed in 2023 that the best parse under the LZ-End rule is NP-hard.

## References
