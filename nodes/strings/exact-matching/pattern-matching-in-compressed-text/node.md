---
tag: WXKJZV
kind: problem
slug: pattern-matching-in-compressed-text
name: Pattern matching in compressed text
aliases:
- compressed pattern matching
area: strings/exact-matching
level: research
summary: Search for a pattern in a compressed representation (e.g. LZ or grammar) without full decompression.
model: word-ram
complexity:
  vars: {n: the size of the compressed text, m: the length of the pattern, N: the length of the uncompressed text}
  time: {worst: O(n + m)}
prereqs: [string-matching, knuth-morris-pratt, straight-line-program, lz78]
see_also: [lzw, lz77, grammar-based-compression, run-length-encoding, compressed-indexing, fm-index, lz-index, string-matching-automaton]
sources:
  - paper: doi:10.1006/jcss.1996.0023
    title: Amihood Amir, Gary Benson and Martin Farach, Let sleeping files lie, pattern matching in Z-compressed files, Journal of Computer and System Sciences 52(2) (1996), 299-307
    locator: the algorithms for LZW-compressed text, including the O(n log m + m) bound
  - paper: doi:10.1145/2483699.2483705
    title: Paweł Gawrychowski, Optimal pattern matching in LZW compressed strings, ACM Transactions on Algorithms 9(3) (2013) (SODA 2011)
    locator: the abstract and main theorem (detecting an occurrence in O(n + m) time, deterministic) and the comparison with earlier bounds
  - paper: doi:10.1007/pl00009202
    title: Martin Farach and Mikkel Thorup, String matching in Lempel-Ziv compressed strings, Algorithmica 20(4) (1998), 388-404 (STOC 1995)
    locator: the randomized algorithm for LZ77-compressed text
  - paper: doi:10.1007/978-3-642-23719-5_36
    title: Paweł Gawrychowski, Pattern matching in Lempel-Ziv compressed strings, fast, simple, and deterministic, Algorithms (ESA 2011), Lecture Notes in Computer Science, 421-432
    locator: the deterministic algorithm for LZ77-compressed text
  - paper: doi:10.1145/2631920
    title: Artur Jeż, Faster fully compressed pattern matching by recompression, ACM Transactions on Algorithms 11(3) (2015) (ICALP 2012)
    locator: the abstract and main theorem (O((n + m) log M) time for SLP-compressed text and pattern, by local recompression; the earlier O(n^2 m) bound of Lifshits)
  - paper: doi:10.1007/3-540-60044-2_44
    title: Marek Karpinski, Wojciech Rytter and Ayumi Shinohara, Pattern-matching for strings with short descriptions, Combinatorial Pattern Matching (CPM 1995), Lecture Notes in Computer Science, 205-214
    locator: the polynomial-time algorithm for fully compressed matching
  - paper: doi:10.1016/s0304-3975(02)00426-7
    title: Takuya Kida, Tetsuya Matsumoto, Yusuke Shibata, Masayuki Takeda, Ayumi Shinohara and Setsuo Arikawa, Collage system, a unifying framework for compressed pattern matching, Theoretical Computer Science 298(1) (2003), 253-272
    locator: the collage system and its matching algorithm
  - paper: doi:10.1002/spe.663
    title: Gonzalo Navarro and Jorma Tarhio, LZgrep, a Boyer-Moore string matching tool for Ziv-Lempel compressed text, Software, Practice and Experience 35(12) (2005), 1107-1130
    locator: the Boyer-Moore approach over LZ78 and LZW and the experiments (speedups of up to 50 percent over decompressing and then searching)
  - paper: doi:10.1145/348751.348754
    title: Edleno Silva de Moura, Gonzalo Navarro, Nivio Ziviani and Ricardo Baeza-Yates, Fast and flexible word searching on compressed text, ACM Transactions on Information Systems 18(2) (2000), 113-139
    locator: the word-based byte-oriented Huffman code and the search experiments (about twice as fast as searching the uncompressed text for simple words, up to 8 times for complex patterns)
---

Pattern matching in compressed text asks for the occurrences of a pattern $P$ of length $m$ in a text $T$ of length $N$ that is given only in compressed form, of size $n$, without decompressing it first. Decompressing and then running [string matching](/string-matching/) costs $\Theta(N + m)$, and $N$ can be much larger than $n$: quadratic in $n$ for [LZ78](/lz78/) and [LZW](/lzw/), and exponential in $n$ for [LZ77](/lz77/) and for grammars. The best algorithms run in time close to $n + m$; for LZW, Gawrychowski detected an occurrence in optimal $O(n + m)$ time, and when the pattern is compressed as well, Jeż found all occurrences in $O((n + m) \log M)$ time on grammar-compressed strings.

## In plain words

Big files are often stored compressed, and searching them usually means unpacking first. That can be slow, and for some kinds of compression the unpacked file is enormously larger than the packed one.

Most compressors work by reuse: a piece of the file is written as "copy that earlier piece, then add this". So the search can work piece by piece. For each piece, remember a short summary: if a search arrives at the start of the piece in a given state, what state it leaves in, and how many matches it passes on the way. A new piece built from earlier pieces gets its summary by combining theirs, without ever spelling out its letters.

With good summaries, the work depends on the size of the packed file and the pattern, not on the length of the unpacked text.

## Definition

**Alphabet.** An integer alphabet, as used by the compressors; the methods below compare characters for equality, except where they index tables by character.

**Compressed representations.**

- A *straight-line program* ([SLP](/straight-line-program/)) of size $n$ is a sequence of rules $X_1, \ldots, X_n$, each either $X_i \to c$ for a character $c$ or $X_i \to X_j X_k$ with $j, k < i$. It is a context-free grammar that generates exactly one string, $T = \mathrm{exp}(X_n)$. [Grammar-based compression](/grammar-based-compression/) produces such grammars.
- [LZ78](/lz78/) writes $T$ as $n$ phrases, each an earlier phrase followed by one character; [LZW](/lzw/), the scheme of Unix compress, is a variant with an implicit character. Each phrase is a rule $X_i \to X_j\,c$, so an LZ78 or LZW parse is an SLP of size $O(n)$. Phrase $i$ has length at most $i$, so $N \le n(n+1)/2$.
- [LZ77](/lz77/) writes $T$ as $n$ phrases, each a copy of an earlier factor, possibly overlapping itself, or a single new character. With self-overlap, $a^N$ needs only 2 phrases.
- [Run-length encoding](/run-length-encoding/) writes $T$ as $n$ runs $c^k$.

**Input.** A compressed representation of $T[0 \ldots N-1]$, of size $n$, and a pattern $P[0 \ldots m-1]$, given plainly. In the *fully compressed* version, $P$ is also given as an SLP of size $m$, and $M$ denotes its length.

**Output.** Depending on the version: whether $P$ occurs in $T$ (detection), the number of occurrences, the first occurrence, or the set $\{\, i : 0 \le i \le N - m,\ T[i \ldots i+m-1] = P \,\}$ of 0-based positions in the uncompressed text. Occurrences may overlap. As on the other pages of this area, if $m = 0$ every position $0, \ldots, N$ occurs, and if $m > N$ none does. Since the set can have $\Theta(N)$ elements, reporting algorithms are measured by $n$, $m$ and the number of occurrences.

## Variants

- **Detection versus reporting.** Gawrychowski's optimal LZW algorithm detects an occurrence; reporting all of them needs at least time proportional to their number, which can exceed $n$.
- **Fully compressed matching.** Both $P$ and $T$ are SLPs. Equality of two SLP-compressed strings is the special case $M = N$; Karpinski, Rytter and Shinohara gave an early polynomial-time algorithm, and Jeż's recompression gives $O((n + m) \log M)$.
- **Searching for many patterns, or approximate patterns, in compressed text.** Navarro and Tarhio handle several patterns; word-based compression also allows approximate and regular expression search (de Moura et al.).
- **Indexing.** Build a compressed index of $T$ that answers pattern queries without the text, as in the [FM-index](/fm-index/), the [LZ-index](/lz-index/) and other [compressed indexes](/compressed-indexing/). There the text is processed once in advance, while here each search reads the compressed text again.
- **Compression designed for searching.** Choose the compressor so that search is easy: de Moura et al. compress words with a byte-oriented Huffman code, so that the compressed pattern can be searched directly with any matcher.

## Examples

Take the SLP $X_0 \to$ b, $X_1 \to$ a, and $X_i \to X_{i-1} X_{i-2}$ for $i = 2, \ldots, 6$, with 7 rules. It generates the Fibonacci words: $\mathrm{exp}(X_2)$ = ab, $\mathrm{exp}(X_3)$ = aba, $\mathrm{exp}(X_4)$ = abaab, $\mathrm{exp}(X_5)$ = abaababa, and $T = \mathrm{exp}(X_6)$ = abaababaabaab, with $N = 13$. The pattern $P$ = aba occurs at positions 0, 3, 5 and 8, overlapping at 3 and 5.

The method below keeps, for each rule $X$ and each state $q$ of the [KMP automaton](/string-matching-automaton/) of $P$, the state $D_X(q)$ reached after reading $\mathrm{exp}(X)$ from $q$, and the number $C_X(q)$ of occurrences that end inside $\mathrm{exp}(X)$. The states are 0 to 3, and from state 3 (a full match) the automaton continues as from state 1.

| rule | expansion | $D_X(0), \ldots, D_X(3)$ | $C_X(0), \ldots, C_X(3)$ |
|---|---|---|---|
| $X_0$ | b | 0, 2, 0, 2 | 0, 0, 0, 0 |
| $X_1$ | a | 1, 1, 3, 1 | 0, 0, 1, 0 |
| $X_2$ | ab | 2, 2, 2, 2 | 0, 0, 1, 0 |
| $X_3$ | aba | 3, 3, 3, 3 | 1, 1, 2, 1 |
| $X_4$ | abaab | 2, 2, 2, 2 | 1, 1, 2, 1 |
| $X_5$ | abaababa | 3, 3, 3, 3 | 3, 3, 4, 3 |
| $X_6$ | abaababaabaab | 2, 2, 2, 2 | 4, 4, 5, 4 |

For instance $C_{X_6}(0) = C_{X_5}(0) + C_{X_4}(D_{X_5}(0)) = 3 + C_{X_4}(3) = 3 + 1 = 4$, the number of occurrences, found without writing out $T$.

## Known algorithms

| compression | method | time |
|---|---|---|
| any | decompress, then [KMP](/knuth-morris-pratt/) | $O(N + m)$ |
| SLP, LZ78, LZW | KMP automaton summaries per rule | $O(nm)$ |
| LZW | Amir, Benson and Farach | $O(n \log m + m)$ |
| LZW | Gawrychowski (detection) | $O(n + m)$ |
| LZ77 | Farach and Thorup (randomized); Gawrychowski (deterministic) | depends on $n$, $m$ and $\log(N/n)$ |
| SLP, both compressed | Lifshits | $O(n^2 m)$ |
| SLP, both compressed | Jeż, recompression | $O((n + m) \log M)$ |
| LZ78, LZW, in practice | Navarro and Tarhio, Boyer-Moore skipping | up to 50 percent faster than decompressing |

**Automaton summaries.** For a rule $X \to c$, $D_X(q) = \delta(q, c)$, the KMP automaton's transition, and $C_X(q)$ is 1 if that transition completes a match and 0 otherwise. For a rule $X \to Y Z$, reading $\mathrm{exp}(X)$ means reading $\mathrm{exp}(Y)$ and then $\mathrm{exp}(Z)$, so $D_X(q) = D_Z(D_Y(q))$ and $C_X(q) = C_Y(q) + C_Z(D_Y(q))$. Filling the tables in rule order takes $O(m)$ per rule, $O(nm)$ in all, and $C_{X_n}(0)$ is the number of occurrences. Reporting positions walks down from $X_n$ into the rules that contain occurrences, and the first occurrence is found the same way.

**Faster methods.** The $O(nm)$ tables store a whole function of the state for each rule. The faster algorithms avoid this: for each phrase they keep only its longest prefix that is a suffix of $P$, its longest suffix that is a prefix of $P$, and whether $P$ occurs inside it, and they combine the pieces across phrase boundaries with data structures built on $P$ alone, such as a [suffix tree](/suffix-tree/) of $P$. Kida et al. describe a common framework, the collage system, that covers dictionary-based schemes such as the LZ family and run-length encoding.

**Recompression.** Jeż's algorithm rewrites both SLPs in the same way, replacing pairs and blocks of letters by new letters, until the pattern is very short, without decompressing either string; occurrences are then found locally.

## Bounds

**Upper bounds.** $O(n + m)$ for detection in LZW-compressed text (Gawrychowski), $O((n + m) \log M)$ for fully compressed SLPs (Jeż), and $O(nm)$ for any SLP by the simple method.

**Lower bound.** In general an algorithm must read the whole compressed text and the pattern, so $\Omega(n + m)$, which Gawrychowski reaches for LZW.

**Size gap.** For SLPs, $N$ can be $2^{n-1}$, as for $X_1 \to$ a and $X_i \to X_{i-1} X_{i-1}$, so decompressing first is exponential in the input size. For LZ78 and LZW the gap is at most quadratic.

## Reductions

- **From LZ78 and LZW to SLPs.** Each phrase $X_j\,c$ becomes a rule $X_i \to X_j C$ with $C \to c$, so methods for SLPs apply with $O(n)$ rules.
- **To string matching, with a cost of $N$.** Decompress and use any [exact matcher](/string-matching/); this is optimal only when $n$ is close to $N$.
- **Equality of compressed strings.** Testing $\mathrm{exp}(A) = \mathrm{exp}(B)$ for two SLPs is fully compressed matching with $M = N$, so fully compressed matching is at least as hard as equality.

## Applications

- Searching compressed files and logs with grep-like tools, as LZgrep does directly on files compressed with Unix compress.
- Full-text search in compressed document collections, where de Moura et al. found search on compressed text faster than on the uncompressed text, because there is less of it to read.
- Algorithms on highly repetitive data, such as versioned documents and collections of genomes, which compress to grammars far smaller than the text.

## References
