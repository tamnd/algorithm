---
tag: TGNZ8J
kind: data-structure
slug: lz-index
name: LZ-index
aliases:
- Lempel-Ziv index
area: data-structures/string-structures
level: research
summary: Full-text index built on a Lempel-Ziv parsing of the text.
implements: [full-text-index]
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern, z: the number of occurrences, σ: the size of the alphabet}
  time: {worst: O(m^3 log σ + (m + z) log n)}
  space: {extra: O(n log σ)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [lz78-parsing, trie, full-text-index]
see_also: [compressed-indexing, lz78-parsing, lempel-ziv-parsing, fm-index, compressed-suffix-array, r-index, sparse-suffix-tree, succinct-data-structures]
sources:
  - paper: Gonzalo Navarro, Indexing text using the Ziv-Lempel trie, Journal of Discrete Algorithms 2(1), 2004, doi:10.1016/S1570-8667(03)00066-2
    locator: pages 87 to 114, the LZTrie, the RevTrie, the Range structure, the three types of occurrences, and the space and time bounds of the LZ-index
  - paper: Juha Kärkkäinen and Esko Ukkonen, Lempel-Ziv parsing and sublinear-size index structures for string matching, Proceedings of the 3rd South American Workshop on String Processing (WSP 1996)
    locator: pages 141 to 155, the idea of indexing a text through its Lempel-Ziv phrases, with occurrences split into those inside a phrase and those that cross a phrase boundary
  - paper: Diego Arroyuelo, Gonzalo Navarro and Kunihiko Sadakane, Stronger Lempel-Ziv based compressed text indexing, Algorithmica 62(1), 2012, doi:10.1007/s00453-010-9443-8
    locator: pages 54 to 101, smaller and faster variants of the LZ-index, with fewer structures and search times that depend less on the pattern length
---

The LZ-index of Navarro (2004) is a compressed [full-text index](/full-text-index/) built on the [LZ78 parsing](/lz78-parsing/) of the text. The text is cut into phrases, each one a previous phrase extended by one symbol, and the index stores two tries of the phrases, one forward and one of the reversed phrases, and a two-dimensional structure that links each phrase with the next one. An occurrence of a pattern lies inside one phrase, crosses one phrase boundary, or covers whole phrases, and each kind is found with a different combination of the tries. The tries have one node per phrase, so the index takes space proportional to the LZ78-compressed text, which is $O(n \log \sigma)$ bits and close to $n H_k$ for compressible texts, and it can report occurrences without the text. The topic of indexes in compressed space in general is on the page of [compressed indexing](/compressed-indexing/).

## In plain words

LZ78 compression cuts the text into pieces from left to right. Each new piece is the longest earlier piece that matches here, plus one letter. So the pieces form a trie, and a repetitive text has few, long pieces.

The LZ-index searches the pieces instead of the text. A match of the pattern sits inside one piece, or straddles the end of one piece and the start of the next, or runs over whole pieces. For the first kind, it is enough to find the pieces that end with the pattern and take every piece that extends them. For the second kind, the pattern is cut in two, and we look for a piece ending with the first part followed by one starting with the second. The third kind is rare and is checked piece by piece.

## The abstract type

The LZ-index implements a static [full-text index](/full-text-index/): after preprocessing a text $T$ of length $n$, report all positions where a pattern $P$ of length $m$ occurs. It is self-contained: the phrases, and so any part of the text, can be read back from the trie, so the text itself need not be stored.

## Representation

Append an end marker $\$$ to $T$, so that the last phrase is new, and let $B_1 B_2 \cdots B_N = T\$$ be the LZ78 parsing, with $B_0$ the empty phrase. Each $B_j$ for $j \ge 1$ is $B_{q} c$ for some $q < j$ and symbol $c$, and the phrases are distinct.

- **LZTrie.** The trie of the phrases. Since every prefix of a phrase is a phrase, each node is a phrase; node $j$ stores the phrase number $j$.
- **RevTrie.** The trie of the reversed phrases $B_j^r$. Not every node is a phrase, so the nodes that are carry their phrase numbers.
- **Range.** The points $(j, j + 1)$ for $1 \le j < N$, placed by the rank of $B_j^r$ among the reversed phrases and of $B_{j+1}$ among the phrases, so that a query rectangle selects the pairs of a phrase ending with one string followed by a phrase starting with another.
- For each phrase, its starting position $start(j)$ in $T$ and its length.

**Invariant.** (Z1) $B_1 \cdots B_N = T\$$, the phrases are distinct, and each $B_j$ with $j \ge 1$ is a previous phrase plus one symbol. (Z2) Node $j$ of the LZTrie spells $B_j$, and the RevTrie node of $B_j^r$ carries $j$. (Z3) $start(j) = \lvert B_1 \cdots B_{j-1} \rvert$.

## Operations

```pseudo id=main
BUILD(T)
L1  parse T$ by LZ78: walk the LZTrie from the root while the next symbol has a child, then add a child for one more symbol as a new phrase
L2  insert every reversed phrase B_j^r into the RevTrie, marking its node with j;  build Range on the pairs (j, j + 1)

SEARCH(P)
L3  inside a phrase:  for each phrase k in the RevTrie subtree of P^r:  for each phrase j in the LZTrie subtree of k:  report start(j) + |B_k| − m
L4  across one boundary:  for i ← 1 to m − 1:  A ← the phrases ending with P[0 … i − 1] (RevTrie);  C ← the phrases starting with P[i …] (LZTrie)
L5      for each pair (j, j + 1) of Range with j in A and j + 1 in C:  report start(j + 1) − i
L6  over whole phrases:  for i ← 1 to m − 2:  walk the LZTrie along P[i …]; for each phrase k = P[i … d − 1] met with d < m:
L7      if B_{k−1} ends with P[0 … i − 1] and B_{k+1} B_{k+2} ⋯ starts with P[d …]:  report start(k) − i
```

Line L3 uses the prefix closure of LZ78: if $P$ occurs inside $B_j$, ending at offset $e$, then $B_j[0 \ldots e]$ is a phrase $B_k$ that ends with $P$, and $B_j$ is in the subtree of $B_k$. Lines L4 and L5 cut $P$ at each of the $m - 1$ places and ask Range for the consecutive pairs that match the two parts. Lines L6 and L7 fix the first whole phrase $B_k$ inside the occurrence; since the phrases are distinct, each substring $P[i \ldots d - 1]$ is at most one phrase, and the check extracts the neighboring phrases from the trie.

## Example

Take $T = $ abababab. The LZ78 parsing of abababab\$ is a | b | ab | aba | b\$, phrases 1 to 5, starting at positions 0, 1, 2, 4 and 7. The pattern aba occurs at 0, 2 and 4, once of each kind:

| step | query | result |
|---|---|---|
| L3 | phrases ending with aba | phrase 4 (aba); its LZTrie subtree is phrase 4 alone: report $4 + 3 - 3 = 4$ |
| L4, i = 1 | ending with a, starting with ba | phrases 1 and 4; no phrase starts with ba: nothing |
| L4, i = 2 | ending with ab, starting with a | phrase 3; phrases 1, 3 and 4; the pair (3, 4) matches: report $4 - 2 = 2$ |
| L6, i = 1 | phrases spelling a prefix of ba, with $d < 3$ | phrase 2 = b; phrase 1 = a ends with a, phrase 3 = ab starts with the rest a: report $1 - 1 = 0$ |

The answer is $\{0, 2, 4\}$: the occurrence at 4 lies inside aba, the one at 2 crosses the boundary between ab and aba, and the one at 0 covers the whole phrase b.

## Correctness

Each occurrence touches one, two, or at least three consecutive phrases, and the three parts of SEARCH find exactly the occurrences of each kind, each once: line L3 by the prefix closure, lines L4 and L5 by the unique cut at the phrase boundary, and lines L6 and L7 by the unique first whole phrase inside the occurrence. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

LZ78 produces $N = O(n / \log_\sigma n)$ phrases, so a trie with one node per phrase and a phrase number per node takes $O(N \log N) = O(n \log \sigma)$ bits. Navarro (2004) stores the LZTrie, the RevTrie, the map from phrase numbers to LZTrie nodes and Range in succinct form, in about $4 N \log N$ bits, which he shows is $4 n H_k(T) + o(n \log \sigma)$ bits for small $k$, where $H_k$ is the empirical entropy of order $k$.

The search time he proves is $O(m^3 \log \sigma + (m + z) \log n)$ for $z$ occurrences. The $m^3$ term comes from the third kind: $O(m^2)$ candidate substrings, each checked against the following phrases. The first two kinds take $O(m^2)$ trie steps and $O(m + z)$ range queries and reports, each with a logarithmic cost in the succinct representation.

The Python implementation uses plain tries and replaces Range by a set intersection, so it follows the logic but not the space or the time bounds.

## Variants

- **Kärkkäinen and Ukkonen (1996).** The first index built on a Lempel-Ziv parsing, which split occurrences into those inside a phrase and those crossing a boundary; it needs the text and achieves sublinear extra space.
- **Smaller LZ-indexes.** Arroyuelo, Navarro and Sadakane (2012) remove some of the four structures, reaching about $(2 + \epsilon) n H_k$ bits, and reduce the dependence of the search time on $m$.
- **Indexes on LZ77 and grammars.** Indexes based on [LZ77](/lz77/) or on grammar compression use the same split into occurrences inside and across phrases, and are much smaller on highly repetitive texts, such as collections of genomes.
- **FM-index and compressed suffix arrays.** The other main family of compressed indexes; see the [FM-index](/fm-index/) and the [compressed suffix array](/compressed-suffix-array/). They count occurrences without listing them, which the LZ-index cannot do quickly.

## When to use it

Use an LZ-index when the text must be stored compressed, the queries need to list occurrences, often of short patterns, and decompressing parts of the text quickly also matters: the LZTrie gives back phrases directly. For counting queries and long patterns, an FM-index is usually faster. For very repetitive texts, an LZ77-based or [r-index](/r-index/) uses much less space.

## Pitfalls

- **The last phrase.** Without an end marker, the last phrase of LZ78 can repeat an earlier phrase; it is then not a node of its own, and occurrences inside it are missed.
- **Counting each occurrence once.** An occurrence must be assigned to exactly one kind; in the third kind, the anchor is the first whole phrase inside the occurrence, and the occurrence must start strictly inside the phrase before it.
- **RevTrie nodes.** The RevTrie has nodes that are not phrases; the subtree query must collect only the marked nodes.
- **Short patterns.** For $m = 1$ only the first kind applies, and for $m = 2$ the third kind does not.

## Implementations

The Python class parses the text by LZ78 into a trie with parent pointers, builds the trie of reversed phrases, and runs the three parts of the search. The second kind intersects the phrases ending with the left part with those starting with the right part, instead of a two-dimensional range query, and the third kind reads neighboring phrases from the trie. check_invariant verifies (Z1) to (Z3). The tests replay the example, check a unary text with many overlapping occurrences, and compare 600 random texts with a direct scan.

## History

Ziv and Lempel introduced the LZ78 parsing in 1978. Kärkkäinen and Ukkonen (1996) used Lempel-Ziv parsing for sublinear-size indexes. Navarro (2004) designed the LZ-index, the first self-index based on LZ78, with the three kinds of occurrences and bounds in terms of the empirical entropy. Arroyuelo, Navarro and Sadakane (2012) made it smaller and faster.

## References
