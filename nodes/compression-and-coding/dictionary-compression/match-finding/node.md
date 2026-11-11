---
tag: 625H77
kind: concept
slug: match-finding
name: Match finding
aliases:
- match finder
- longest match search
area: compression-and-coding/dictionary-compression
level: core
summary: Locating the longest earlier occurrence of the text at the current position, the main cost of LZ encoders.
prereqs: [hash-table, string-matching]
see_also: [lz77, greedy-parsing, lazy-matching, optimal-lz-parsing, longest-previous-factor, deflate, lzma, suffix-array]
sources:
  - url: https://www.rfc-editor.org/rfc/rfc1951
    title: L. Peter Deutsch, RFC 1951, DEFLATE Compressed Data Format Specification version 1.3, May 1996
    locator: Section 4, Compression algorithm details (the chained hash table on 3-byte sequences, the search from the newest string, the chain limit, and lazy matching)
  - url: https://github.com/madler/zlib/blob/v1.2.12/deflate.c
    title: Jean-loup Gailly and Mark Adler, zlib 1.2.12, deflate.c, 2022
    locator: "the functions longest_match and fill_window, the macros UPDATE_HASH and INSERT_STRING, and configuration_table (max_chain, nice_length, good_length per level)"
  - url: https://man7.org/linux/man-pages/man1/xz.1.html
    title: Lasse Collin, xz(1) manual page, XZ Utils 5.8
    locator: "the LZMA1 and LZMA2 options mf (hc3, hc4, bt2, bt3, bt4, with the minimum nice length and memory use of each) and depth"
  - paper: doi:10.1016/j.ipl.2007.10.006
    title: Maxime Crochemore and Lucian Ilie, Computing Longest Previous Factor in linear time and applications, Information Processing Letters 106(2), 75-80, 2008
    locator: Section 3 (the LPF array from the suffix array and the LCP array) and Section 4 (the Lempel-Ziv factorization from LPF)
  - paper: "Michael Rodeh, Vaughan R. Pratt and Shimon Even, Linear algorithm for data compression via string matching, Journal of the ACM 28(1), 16-24, 1981"
    locator: the suffix tree method for the longest previous match at each position, in linear time over the whole text
---

Match finding is the search, at each position $i$ of the input, for an earlier string that is equal to a prefix of the text that starts at $i$. The result is a match, a pair (length, distance) that an [LZ77](/lz77/) style encoder writes as a [back-reference](/back-reference/). An encoder runs it at almost every position, so it takes most of the encoding time, while the decoder never does it. The usual methods are hash chains (zlib, gzip), binary trees of suffixes (LZMA, xz), and suffix structures, which give the exact longest match for every position at once.

## In plain words

You copy out a long text, and you want to save work. When the next words already occur earlier in the text, you write "go back this far and copy this many letters" in place of the words. The hard part is to find the earlier copy quickly. To read the whole text before each word would be far too slow.

So the encoder keeps an index. The simple index has a box for each group of three letters. Each box lists the places where those three letters occur, the newest place first. At each step the encoder opens the box for the next three letters and checks the places in it. It keeps the place that gives the longest copy. When a box has too many places, the encoder stops early and accepts a copy that is good, but maybe not the best.

## The idea

**The problem.** The input is a string $t = t[0 \ldots n-1]$ over an alphabet $\Sigma$ of size $\sigma$ (bytes in practice, $\sigma = 256$). A *match* at position $i$ is a pair $(\ell, d)$ with $1 \le d \le i$ and $t[i-d+k] = t[i+k]$ for $0 \le k < \ell$. The source $t[i-d \ldots i-d+\ell-1]$ may overlap the position $i$, so a run of $\ell$ equal bytes is one match of distance $1$. A format adds limits: a window $w$ with $d \le w$, a minimum length $\ell_{\min}$ (3 in DEFLATE) and a maximum length $\ell_{\max}$ (258 in DEFLATE, 273 in LZMA). The *longest match* at $i$ has the largest $\ell$ under these limits. On a tie, the smallest $d$ is best, because a short distance costs fewer output bits in every common format. The longest match at $i$ without a window is the [longest previous factor](/longest-previous-factor/) of $t$ at $i$.

**The brute force.** Compare $t[i \ldots]$ with each earlier start $j$, from $j = i-1$ down to $\max(0, i-w)$. This costs $O(w \cdot \ell_{\max})$ symbol comparisons per position, so $O(n w \ell_{\max})$ in total. It is the oracle in the tests.

**Hash chains.** A match of length at least $\ell_{\min}$ starts with the same $\ell_{\min}$ symbols as the text at $i$. So the encoder puts each position $j$ in a list keyed by a hash of $t[j \ldots j+\ell_{\min}-1]$. The lists are two arrays: `head[h]` is the newest position with hash $h$, and `prev[j]` is the position before $j$ with the same hash. To insert $j$ costs $O(1)$; the chains link positions, so no list memory is allocated. The search walks the chain from the newest position, so the first candidate of a given length has the smallest distance.

```pseudo id=main
INSERT(j)                                  ▷ put position j at the head of its chain
L1  h ← HASH(t[j .. j + ℓmin − 1])
L2  prev[j] ← head[h]
L3  head[h] ← j

FIND(i)                                    ▷ the longest match at i among the inserted positions
L4  j ← head[HASH(t[i .. i + ℓmin − 1])]; best ← (0, 0)
L5  while j ≠ NIL and i − j ≤ w do
L6      if the chain limit is used up then break
L7      ℓ ← the length of the common prefix of t[j ..] and t[i ..], at most ℓmax
L8      if ℓ > best.ℓ then best ← (ℓ, i − j)
L9      j ← prev[j]
    return best if best.ℓ ≥ ℓmin, else no match
```

A hash collision only puts a wrong candidate on the chain, and line L7 then measures its true length, so a collision costs time but gives no wrong match. Without a chain limit, every position $j$ with the same first $\ell_{\min}$ symbols as $i$ and $i - j \le w$ is on the chain, so FIND returns a longest match. With a limit it is a heuristic. A long chain with short matches is the slow case: on a text where one 3-byte string occurs at every fourth position, the chain at position $i$ holds about $i/4$ positions inside the window, and each gives a match of length 3.

zlib adds three cut-offs to this loop. `max_chain` bounds the number of candidates. `nice_length` ends the search as soon as a match of that length is found. And when the previous match is already at least `good_length` long, the chain limit is divided by four, because a lazy encoder then needs a better match only rarely (see [lazy matching](/lazy-matching/)). The levels of zlib 1.2.12 set `max_chain` from 4 (level 1) to 4096 (level 9) and `nice_length` from 8 to 258. zlib also uses position 0 as the end marker of a chain, so it never takes a source that starts at position 0.

**Binary trees.** The LZMA match finder `bt4` keeps the positions with the same hash in a [binary search tree](/binary-search-tree/), ordered by the suffixes $t[j \ldots]$ cut at $\ell_{\max}$. The longest common prefix of $t[i \ldots]$ with a set of suffixes is reached at the lexicographic predecessor or successor of $t[i \ldots]$ in the set, and both lie on the search path for $t[i \ldots]$. So a search that measures the common prefix at each node of the path finds the longest match, and it visits only one path, not a whole chain. The encoder inserts $i$ at the root during the same walk: it splits the old tree into the nodes smaller and larger than $t[i \ldots]$ and hangs them as the two subtrees of $i$. Newer positions are therefore nearer the root, and the walk stops at the first node outside the window. The tree is not balanced, so a cap on the depth (the `depth` option of xz) bounds the worst case; with the cap, the search is a heuristic again. The xz manual lists hash chain finders `hc3` and `hc4` and binary tree finders `bt2`, `bt3` and `bt4`; the digits give the lengths of the hashed prefixes, and `bt4` uses 2-, 3- and 4-byte hashes. Hash chains are usually faster, and binary trees usually find longer matches.

**Suffix structures.** A [suffix tree](/suffix-tree/) or a [suffix array](/suffix-array/) with its [LCP array](/lcp-array/) answers the question for all positions at once. Rodeh, Pratt and Even (1981) found the longest previous match at each position with a suffix tree in linear time for a constant alphabet. Crochemore and Ilie (2008) compute the [longest previous factor](/longest-previous-factor/) array from the suffix array and the LCP array in $O(n)$ time, with one stack pass. These methods are exact, but they need the whole text and $\Theta(n)$ words of memory, and a window or a cap on $d$ needs more work. Compressors that run on a stream with a fixed memory budget use hash chains or binary trees.

**More than one match.** An [optimal parser](/optimal-lz-parsing/) needs, for each length $\ell$, the smallest distance of a match of length at least $\ell$. A walk on a chain or on a tree gives these for free: each time the length grows, the encoder records the pair. LZMA's binary tree finder returns this list of pairs, sorted by length.

## Examples

**A chain limit that misses the longest match.** Let $t$ = `abcde_abcxy_abcde`, with positions 0 to 16, $\ell_{\min} = 3$, and a large window.

| Position $i$ | Text at $i$ | Chain for `abc` before the search | Candidates checked | Match found |
|---|---|---|---|---|
| 0 | `abcde_...` | empty | none | none |
| 6 | `abcxy_...` | 0 | 0 gives 3 (`abc`, then `d` against `x`) | (3, 6) |
| 12 | `abcde` | 6, 0 | 6 gives 3, then 0 gives 5 | (5, 12) |

With `max_chain` = 1 the search at position 12 stops after position 6 and returns (3, 6). With `max_chain` = 2 or no limit it returns (5, 12), which is the longest match. The binary tree finder also returns (5, 12). The tests check these values.

**A long run.** For $t$ = `a` repeated 600 times, the longest match at each position $i \ge 1$ is $(\min(\ell_{\max}, n-i), 1)$: the source starts one byte back and overlaps the text it copies. The hash chain finder of the implementation checks only one candidate per position, because the first candidate already gives the cap. zlib differs at position 1, because it never takes position 0 as a source.

**Exactness.** The tests compare both finders with the brute force at every position of random and repetitive strings with fixed seeds. Hash chains with no chain limit return the same pair as the brute force (the longest length and, on a tie, the smallest distance). The binary trees return the longest length, with a valid distance. With `max_chain` = 2, the hash chains return a shorter match than the brute force at some positions of the random strings.

## Where it is used

- **DEFLATE** ([deflate](/deflate/), in zlib, gzip and PNG): hash chains on 3-byte strings with a 32 KiB window. RFC 1951 describes this method in Section 4 but does not require it; any encoder that writes valid back-references is correct.
- **LZMA and xz** ([lzma](/lzma/)): the binary tree finder `bt4` at the default presets from 4 up and hash chains `hc3` or `hc4` at the fast presets, with windows of many megabytes.
- **Zstandard** ([zstandard](/zstandard/)): its strategies go from a single hash table to hash chains (`greedy`, `lazy`, `lazy2`) and binary trees (`btlazy2`, `btopt`, `btultra`).
- **LZ4 and Snappy** ([lz4](/lz4/), [snappy](/snappy/)): the fast modes keep one position per hash bucket and no chain, so they test one candidate per position. This is the fastest finder and the one that misses the most.
- **Parsers.** [Greedy parsing](/greedy-parsing/) takes the match at each step, [lazy matching](/lazy-matching/) also looks one position ahead, and [optimal LZ parsing](/optimal-lz-parsing/) needs the list of matches by length at each position.
- **Text indexing.** The [LZ factorization](/lempel-ziv-factorization/) used by compressed indexes and by string algorithms is computed with the exact suffix array method, not with a heuristic finder.

## References
