---
tag: BBT7PH
kind: concept
slug: lempel-ziv-parsing
name: Lempel-Ziv parsing
aliases:
- LZ parsing
- Lempel-Ziv parse
area: compression-and-coding/dictionary-compression
level: intro
summary: The family of left-to-right parses that cut a string into phrases, each a copy of earlier text, with or without one new symbol, as in LZ77, LZ78 and LZ factorization.
prereqs: [adaptive-dictionary-compression, back-reference]
see_also: [lempel-ziv-factorization, lz78-parsing, lempel-ziv-factor, lz77, lz78, lz-end, lempel-ziv-complexity, grammar-based-compression]
sources:
  - paper: doi:10.1109/TIT.1976.1055501
    title: Abraham Lempel and Jacob Ziv, On the complexity of finite sequences, IEEE Transactions on Information Theory 22(1), 1976
    locator: pages 75 to 81 (the production history of a sequence and its complexity)
  - paper: doi:10.1109/TIT.1977.1055714
    title: Jacob Ziv and Abraham Lempel, A universal algorithm for sequential data compression, IEEE Transactions on Information Theory 23(3), 1977
    locator: pages 337 to 343 (the sliding-window parse with one new symbol per phrase)
  - paper: doi:10.1109/TIT.1978.1055934
    title: Jacob Ziv and Abraham Lempel, Compression of individual sequences via variable-rate coding, IEEE Transactions on Information Theory 24(5), 1978
    locator: pages 530 to 536 (the incremental parsing)
  - paper: doi:10.1007/978-3-642-38905-4_19
    title: Juha Kärkkäinen, Dominik Kempa and Simon J. Puglisi, Linear time Lempel-Ziv factorization, simple, fast, small, CPM 2013, LNCS 7922
    locator: Section 2, Preliminaries (the definition of the LZ factorization, with the example zzzzzipzip)
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, Cambridge University Press, 2016
    locator: the chapter on compressed text indexes (Lempel-Ziv parsings as a measure of repetition)
---

A Lempel-Ziv parsing cuts a string, from left to right, into phrases that are each a copy of something earlier, with or without one new symbol at the end. The members of the family differ in what "earlier" means: any earlier text ([LZ factorization](/lempel-ziv-factorization/)), earlier text with one new symbol ([LZ77](/lz77/)), or an earlier phrase with one new symbol ([LZ78 parsing](/lz78-parsing/)). The number of phrases is a measure of how repetitive the string is, and it is the size of the output of the matching compressor up to the cost of each phrase.

## In plain words

Read a text from the start. At each point, look for the longest piece that starts here and that you have seen before. Cut the text after that piece, and go on from the cut. The pieces are the phrases.

There are a few rules for what counts as "seen before". In one rule, the piece may come from anywhere earlier in the text. In another rule, the piece must be one of the earlier phrases, and the phrase also takes one more letter. The first rule finds long repeats at once. The second rule learns them a little at a time, but it needs much less work.

A text with many repeats has few phrases. A text with no repeats has about one phrase per letter.

## The idea

Let $T = T[1..n]$ be a string over an alphabet $\Sigma$ of size $\sigma$. Each parsing below is greedy: at position $i$ it takes the longest prefix of $T[i..n]$ that the rule allows. Write $\mathrm{lpf}(i)$ for the length of the longest prefix of $T[i..n]$ that also starts at some $j < i$; the occurrence at $j$ may overlap position $i$.

| Parse | A phrase at position $i$ | Number of phrases |
|---|---|---|
| [LZ factorization](/lempel-ziv-factorization/) (LZ77 without the extra symbol, sometimes called LZ76) | $T[i..i+\mathrm{lpf}(i)-1]$, or the single new symbol $T[i]$ when $\mathrm{lpf}(i) = 0$ | $z$ |
| LZ factorization without self-reference | the longest prefix of $T[i..n]$ that occurs inside $T[1..i-1]$, or one new symbol | $z_{\mathrm{no}} \ge z$ |
| [LZ77](/lz77/) triple parse | $T[i..i+\ell]$ with $\ell$ the longest copy (limited to a window and to $n - i$), plus one literal symbol | $z_{77} \le z$ |
| [LZ78 parsing](/lz78-parsing/) | the longest earlier *phrase* that is a prefix of $T[i..n]$, plus one symbol | $z_{78}$ |
| [LZ-End](/lz-end/) | a copy whose source ends at the end of an earlier phrase, plus one symbol | $z_{\mathrm{end}}$ |

The phrase of the LZ factorization is the [Lempel-Ziv factor](/lempel-ziv-factor/). Some authors use "LZ77" for the factorization and some for the triple parse; the two differ by the extra symbol, and on a page about counts it is worth saying which one is meant.

**How the counts relate.** Each relation follows from the rules.

- $z_{77} \le z$ when the window is unbounded. After the same number of phrases, the triple parse is never behind the factorization: if it stands at a position $g$ inside a factor, the rest of that factor is a copy of earlier text, so the next triple reaches at least the end of the factor.
- $z \le z_{\mathrm{no}}$, since a copy that must lie inside $T[1..i-1]$ is also a copy that may overlap.
- $z \le 2 z_{78}$. Each LZ78 phrase is an earlier phrase (a copy of earlier text) followed by one symbol, so it is the union of at most two pieces that the factorization may use, and the greedy factorization uses no more phrases than any such parse. The [Lempel-Ziv factorization](/lempel-ziv-factorization/) page proves this.
- $z_{78} = O(n / \log_\sigma n)$, since the phrases are distinct; the [LZ78 parsing](/lz78-parsing/) page proves the bound. So $z = O(n / \log_\sigma n)$ as well.
- On a run of $n$ equal symbols, $z = 2$ while $z_{78}$ is about $\sqrt{2n}$, so $z$ can be much smaller.

**Why the count matters.** A Lempel-Ziv parse with $k$ phrases is the output of a compressor with $k$ tokens. For a stationary ergodic source, the LZ77 and LZ78 coders reach the entropy rate (the [Ziv-Lempel entropy theorem](/ziv-lempel-entropy-theorem/)). For a single string in the worst case, $z$ is a lower bound on the size of the smallest context-free grammar that generates only that string ([grammar-based compression](/grammar-based-compression/), [smallest grammar problem](/smallest-grammar-problem/)), and the size of the smallest [string attractor](/string-attractor/) is at most $z$. The count of the 1976 parse of Lempel and Ziv is used as a complexity measure of a sequence; see [Lempel-Ziv complexity](/lempel-ziv-complexity/).

**How the parses are computed.** The LZ factorization needs, at each phrase start, the longest previous factor. The [suffix array](/suffix-array/) and [LCP array](/lcp-array/) give it in $O(n)$ time in total; see [Lempel-Ziv factorization](/lempel-ziv-factorization/). The LZ78 parse needs only a [trie](/trie/) of the phrases, in $O(n)$ time for a fixed alphabet. Compressors with a bounded window use [match finding](/match-finding/) with hash chains or binary trees.

The [Lyndon factorization](/lyndon-factorization/) is also a left-to-right cut of a string into factors, but its factors are Lyndon words in non-increasing order, not copies of earlier text; it measures order, not repetition.

## Examples

The counts on three short strings (the window and length fields are large enough not to matter):

| $T$ | LZ factorization | No self-reference | LZ77 triples | LZ78 parse |
|---|---|---|---|---|
| $abababab$ | $a \mid b \mid ababab$, $z = 3$ | $a \mid b \mid ab \mid abab$, 4 | $a \mid b \mid ababab$, 3 | $a \mid b \mid ab \mid aba \mid b$, 5 |
| $aaaaaaaa$ | $a \mid aaaaaaa$, $z = 2$ | $a \mid a \mid aa \mid aaaa$, 4 | $a \mid aaaaaaa$, 2 | $a \mid aa \mid aaa \mid aa$, 4 |
| $abracadabra$ | $a \mid b \mid r \mid a \mid c \mid a \mid d \mid abra$, $z = 8$ | the same, 8 | $a \mid b \mid r \mid ac \mid ad \mid abra$, 6 | $a \mid b \mid r \mid ac \mid ad \mid ab \mid ra$, 7 |

In $abababab$ the third factor $ababab$ starts at position 3 and copies from position 1, so source and target overlap; without self-reference the same text needs two more phrases. In $abracadabra$ the factorization has more phrases than the triple parse, because the triple parse can put a new symbol into a phrase with a copy, while the factorization spends a whole phrase on each single symbol $a$ that it copies.

The example of Kärkkäinen, Kempa and Puglisi: $zzzzzipzip$ has the factorization $z \mid zzzz \mid i \mid p \mid zip$, so $z = 5$.

## Where it is used

- **Compression.** Each Lempel-Ziv parse is the token stream of a compressor: [LZ77](/lz77/), [LZSS](/lzss/) and DEFLATE use the window-limited copy parse, [LZ78](/lz78/) and [LZW](/lzw/) use the phrase parse.
- **Compressed data structures.** The [LZ-index](/lz-index/) is built on the LZ78 parse, and other [compressed indexes](/compressed-indexing/) store the LZ factorization of a highly repetitive collection in $O(z)$ space. [Pattern matching in compressed text](/pattern-matching-in-compressed-text/) works on the phrases directly.
- **String algorithms.** The LZ factorization is a step in algorithms for runs, squares and other repetitions, and $z$ is a reference point for measures of repetition such as the smallest grammar and the smallest string attractor.
- **Complexity measures.** The phrase count is used to estimate the complexity of signals and of DNA sequences ([Lempel-Ziv complexity](/lempel-ziv-complexity/)).

## References
