---
tag: 2AQSRW
kind: algorithm
slug: wu-manber
name: Wu-Manber algorithm
aliases:
- Wu-Manber multiple pattern matching
- mgrep algorithm
area: strings/multiple-pattern-matching
level: advanced
summary: Practical multi-pattern matcher that shifts by blocks of characters using a shift table, fast when patterns are long.
solves: [multiple-string-matching]
model: word-ram
complexity:
  vars: {n: the length of the text, m: the total length of the patterns, ℓ: the shortest nonempty pattern length, B: the block size, z: the number of occurrences, L: the largest pattern length}
  time: {build: O(B·m), worst: O(n·(B + m)), expected: O(B·n/ℓ + z·L)}
  space: {extra: O(m)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1994
  people: [Sun Wu, Udi Manber]
  note: Technical report TR 94-17 of the University of Arizona, May 1994. An earlier version was part of agrep, and the algorithm was the multi-pattern engine of the glimpse search tool.
prereqs: [boyer-moore-horspool, block-shift-table, hash-table]
see_also: [set-horspool, commentz-walter, aho-corasick, karp-rabin-multiple-patterns, multiple-string-matching, bad-character-rule, dictionary-matching, boyer-moore]
sources:
  - url: https://www.cs.arizona.edu/sites/default/files/TR94-17.pdf
    title: Sun Wu and Udi Manber, A fast algorithm for multi-pattern searching, Technical Report TR 94-17, Department of Computer Science, University of Arizona, May 1994
    locator: Section 2.2 (the SHIFT, HASH and PREFIX tables), Section 2.3 with Figure 1 (the scanning loop), Section 3.1 (the rough analysis with B in the order of log_c 2M)
  - book: isbn:9780521813075
    title: Gonzalo Navarro and Mathieu Raffinot, Flexible Pattern Matching in Strings, Cambridge University Press, 2002
    locator: Chapter 3, Multiple string matching (Wu-Manber among the suffix-based algorithms, and the experimental comparison by alphabet size and number of patterns)
  - paper: doi:10.1002/spe.4380100608
    title: R. Nigel Horspool, Practical fast searching in strings, Software, Practice and Experience 10(6) (1980), 501-506
    locator: the single-character shift that Wu-Manber generalizes to blocks
---

The Wu-Manber algorithm searches for a large set of patterns at once by moving a window over the text and shifting it by a distance read from a table indexed by the last $B$ characters of the window, a block. It cuts every pattern to the length $\ell$ of the shortest one, so that all patterns end at the same place in the window, and the [block shift table](/block-shift-table/) gives the distance from the end of the window to the nearest place where the block occurs in some cut pattern. Only when the shift is 0 does it look further: a hash table lists the patterns whose cut ends with this block, a prefix check removes most of them, and the rest are compared in full. With blocks of 2 or 3 characters, shifts stay long for thousands of patterns, which makes it one of the fastest practical methods for large sets of not too short patterns, although its worst case is $O(nm)$.

## In plain words

[Horspool's](/boyer-moore-horspool/) method looks at the last letter under a frame and jumps forward unless that letter appears near the end of the pattern. With thousands of patterns, every letter appears near the end of some pattern, so the jumps vanish.

Wu-Manber looks at the last two or three letters instead. Pairs and triples of letters are much more varied than single letters, so most of them appear in no pattern, or only far from the end, and the frame can still jump. All patterns are cut to the length of the shortest, so the jump can be computed from one table.

When the last letters do appear at the very end of some cut pattern, the method checks only the patterns that end with these letters, and compares their first letters before it compares them in full.

## The problem

Given a text $T = T[0 \ldots n-1]$ and patterns $P_0, \ldots, P_{k-1}$, output every pair $(s, j)$ with $T[s \ldots s + |P_j| - 1] = P_j$. Indices are 0-based. Occurrences may overlap. A pattern listed twice is reported once for each index, and the empty pattern occurs at every $s$ from $0$ to $n$. The alphabet is general, with characters used as keys of hash tables; in the original, characters are bytes and blocks are packed into integers. Let $\ell$ be the length of the shortest nonempty pattern, $B \le \ell$ the block size, $L$ the longest length and $m$ the total length.

## The algorithm

Cut each nonempty pattern to its first $\ell$ characters, $\hat P_j = P_j[0 \ldots \ell - 1]$. The three tables are:

- $\mathrm{SHIFT}[X]$ for a block $X$ of $B$ characters: the smallest $\ell - q$ over all $j$ and all $q \in \{B, \ldots, \ell\}$ with $\hat P_j[q - B \ldots q - 1] = X$, and $\ell - B + 1$ if $X$ occurs in no cut pattern. This is the [block shift table](/block-shift-table/).
- $\mathrm{HASH}[X]$: the indices $j$ whose cut pattern ends with $X$, that is $\hat P_j[\ell - B \ldots \ell - 1] = X$.
- $\mathrm{PREFIX}[j]$: the first $B$ characters of $P_j$.

```pseudo id=main
WU-MANBER(T[0 .. n-1], P_0, ..., P_{k-1}, B)
L1  output (s, j) for every s in 0 .. n and every j with P_j = ε
L2  if no pattern is nonempty then return
L3  ℓ ← the shortest length of a nonempty pattern; B ← min(B, ℓ)
L4  SHIFT[X] ← ℓ − B + 1 for every block X
L5  for each nonempty P_j and q ← B to ℓ do X ← P_j[q − B .. q − 1]; SHIFT[X] ← min(SHIFT[X], ℓ − q)
L6  for each nonempty P_j do append j to HASH[P_j[ℓ − B .. ℓ − 1]]; PREFIX[j] ← P_j[0 .. B − 1]
L7  pos ← ℓ − 1
L8  while pos ≤ n − 1 do
L9      X ← T[pos − B + 1 .. pos]
L10     if SHIFT[X] > 0 then pos ← pos + SHIFT[X]
L11     else
L12         s ← pos − ℓ + 1
L13         for each j in HASH[X] do
L14             if T[s .. s + B − 1] = PREFIX[j] and s + |P_j| ≤ n and T[s .. s + |P_j| − 1] = P_j then output (s, j)
L15         pos ← pos + 1
```

The window is $T[s \ldots \mathrm{pos}]$ with $s = \mathrm{pos} - \ell + 1$, and a pattern is found at the start $s$ of the window, where its cut part fills the window. In the original program, a block is packed into an integer by shifts of 5 bits per character, the tables have $2^{15}$ entries, and $B$ is 2 for small sets and 3 for large ones; several blocks may then share an entry of SHIFT, which keeps the smallest of their shifts and stays safe. The prefix check of line L14 used the first $B' = 2$ characters, and the analysis takes $B' = B$, as here.

## Example

Take the patterns search, pattern, tern, text and barn, the text fastsearchforpatternsinlongtext ($n = 31$), and $B = 2$. The shortest length is $\ell = 4$, so the cut patterns are sear, patt, tern, text and barn, and the default shift is $\ell - B + 1 = 3$. Line L5 gives the shifts below; every other block has shift 3.

| shift | blocks |
|---|---|
| 0 | ar, rn, tt, xt |
| 1 | at, ea, er, ex |
| 2 | ba, pa, se, te |

The hash table has $\mathrm{HASH}[\mathrm{ar}] = \{0\}$, $\mathrm{HASH}[\mathrm{tt}] = \{1\}$, $\mathrm{HASH}[\mathrm{rn}] = \{2, 4\}$ and $\mathrm{HASH}[\mathrm{xt}] = \{3\}$.

| pos | window | block | SHIFT | candidates at shift 0 | next pos |
|---|---|---|---|---|---|
| 3 | fast | st | 3 | | 6 |
| 6 | tsea | ea | 1 | | 7 |
| 7 | sear | ar | 0 | search: equal, output (4, 0) | 8 |
| 8 | earc | rc | 3 | | 11 |
| 11 | chfo | fo | 3 | | 14 |
| 14 | orpa | pa | 2 | | 16 |
| 16 | patt | tt | 0 | pattern: equal, output (13, 1) | 17 |
| 17 | atte | te | 2 | | 19 |
| 19 | tern | rn | 0 | tern: equal, output (16, 2); barn: prefix ba ≠ te | 20 |
| 20 | erns | ns | 3 | | 23 |
| 23 | sinl | nl | 3 | | 26 |
| 26 | long | ng | 3 | | 29 |
| 29 | gtex | ex | 1 | | 30 |
| 30 | text | xt | 0 | text: equal, output (27, 3) | 31, stop |

The output is (4, 0), (13, 1), (16, 2) and (27, 3): search, pattern, tern and text. The occurrences of pattern and tern overlap. The search uses 14 windows for 31 characters; at four of them the shift is 0, and the prefix table rejects barn without a full comparison. The patterns search and pattern are longer than $\ell$ and are compared in full at line L14, past the right end of the window.

## Correctness

Three facts give the result. First, a pattern that occurs at the start $s$ of the window has its cut part equal to the window, so the block $X$ is its last cut block, $\mathrm{SHIFT}[X] = 0$, and $j \in \mathrm{HASH}[X]$; line L14 then confirms it. Second, line L14 outputs only pairs it has compared in full. Third, a positive shift skips no start: if $P_j$ occurred at $s + \delta$ with $0 \le \delta < \mathrm{SHIFT}[X]$, then either $\delta \le \ell - B$, the block $X$ lies inside the cut part of that occurrence and ends at its index $q = \ell - \delta$, which gives $\mathrm{SHIFT}[X] \le \delta$; or $\delta \ge \ell - B + 1$, which is not below any shift. A shift of 1 after a zero shift is always safe. The full proof is in the proof file below.

## Complexity

- **Preprocessing.** Line L5 forms at most $\ell - B + 1$ blocks per pattern, each of $B$ characters, so the tables take $O(Bm)$ time with hashing, or $O(m)$ with a rolling block code, and $O(m)$ entries.
- **Worst case.** A window with shift 0 may compare every pattern in $\mathrm{HASH}[X]$ in full, so it costs $O(B + m)$, and there are at most $n$ windows: $O(n(B + m))$. This is reached by the text $a^n$ with the patterns $a^\ell$ and $a^i b$ for $\ell \le i < L$: every block is $a^B$ with shift 0, every pattern passes the prefix check, and each $a^i b$ is compared for $i + 1$ characters, so each window costs $\Theta(m)$.
- **Expected case.** Wu and Manber estimate the time for a random text and $k$ random patterns of one length $\ell$, with $M = k \ell$ and the block size $B = \lceil \log_\sigma 2M \rceil$. Each SHIFT value, including 0, is taken by at most $k$ of the at least $2M$ blocks, so a random block has each shift with probability at most $1/(2\ell)$, and the mean shift is at least about $\ell/2$. Each window costs $O(B)$, so the scan costs $O(Bn/\ell)$, plus the cost of true matches.

**Measured shifts.** On a random text of $10^5$ characters and $k$ random patterns of length 8, the mean shift (text length divided by the number of windows) was:

| alphabet, $k$ | $B = 1$ | $B = 2$ | $B = 3$ | $B = 4$ | $B = 5$ |
|---|---|---|---|---|---|
| 26 letters, 10 | 2.70 | 6.62 | 5.99 | 5.00 | 4.00 |
| 26 letters, 100 | 1.00 | 4.23 | 5.89 | 5.00 | 4.00 |
| 26 letters, 1000 | 1.00 | 1.06 | 5.01 | 4.97 | 4.00 |
| 4 letters, 10 | 1.25 | 1.32 | 3.73 | 4.46 | 3.91 |
| 4 letters, 100 | 1.00 | 1.00 | 1.04 | 2.14 | 3.20 |
| 4 letters, 1000 | 1.00 | 1.00 | 1.00 | 1.00 | 1.20 |

The best $B$ grows with the number of patterns and falls with the alphabet size, as $\log_\sigma 2M$ predicts: for 1000 patterns of length 8 it is $\log_{26} 16000 \approx 3.0$ for letters and $\log_4 16000 \approx 7.0$ for DNA, which is close to $\ell$ and leaves almost no room for shifts. A larger $B$ also lowers the largest shift $\ell - B + 1$, so the table shows a peak.

## Properties

- **Deterministic and exact.** The tables give candidates, but every output is compared in full.
- **Shift-based.** Like [Horspool](/boyer-moore-horspool/), the shift depends only on the last block of the window, not on how much matched. With $B = 1$, SHIFT is the shift table of [Set Horspool](/set-horspool/), extended by the value 0 for final characters.
- **Not online.** The decision at a window needs the block at its right end, and a full comparison reads up to $L - \ell$ characters past it.
- **Bounded by the shortest pattern.** No shift exceeds $\ell - B + 1$; one short pattern slows the search for all.
- **Small tables.** The tables are indexed by blocks, not by trie nodes, so the memory depends on the table size chosen and on $m$, not on the alphabet of the patterns.

## Variants and improvements

- **Compressed SHIFT table.** Map blocks to a fixed number of entries by a hash function, and keep the minimum shift per entry. This trades a few shorter shifts for a table that fits in cache; the original uses $2^{15}$ entries.
- **Larger blocks for small alphabets.** For DNA and other small alphabets, $B$ of 4 to 8 is needed for large sets, as the table above shows; some implementations read blocks of 2 bits per base.
- **Shortest patterns apart.** Search the few shortest patterns with another method, such as [Aho-Corasick](/aho-corasick/), and the rest with a larger $\ell$.
- **Factor-based methods.** Set backward oracle matching and related algorithms read the window backward in an automaton of reversed factors and can shift past the read part; Navarro and Raffinot find them faster for very large sets of long patterns.
- **Hash-only matching.** [Karp-Rabin with many patterns](/karp-rabin-multiple-patterns/) looks up a hash of the whole window at every position, with no shifts; it is simpler and better for short patterns of one length.

## When to use it

Use Wu-Manber for hundreds to tens of thousands of patterns whose shortest length is at least about 4 to 8, over text such as natural language or bytes. It was the multi-pattern engine of agrep and glimpse. For small alphabets with many patterns, short patterns, or a worst-case guarantee, use [Aho-Corasick](/aho-corasick/). For a few patterns over a large alphabet, [Set Horspool](/set-horspool/) is simpler and as fast.

## Pitfalls

- **Mixing the two alignments.** The patterns are cut to their first $\ell$ characters, so a candidate starts at the start of the window. An implementation that cuts to the last $\ell$ characters must instead test each candidate as ending at the end of the window, at $s = \mathrm{pos} - |P_j| + 1$; mixing the two misses occurrences.
- **Verifying only the window.** A pattern longer than $\ell$ must be compared in full, past the right end of the window, and the comparison must check that it fits in the text.
- **A block size above $\ell$.** If $B > \ell$, no block fits in a cut pattern; set $B = \min(B, \ell)$, as line L3 does.
- **Shift after a zero.** After the candidates are checked, the shift is 1, since the table gives 0 for this block. A longer shift needs information about the matched part, as in [Commentz-Walter](/commentz-walter/).
- **Worst-case inputs.** Periodic text and patterns that end in a common block make every window a zero-shift window, and the time becomes $\Theta(nm)$ in the worst case; do not use Wu-Manber where inputs may be adversarial.

## Implementations

## History

Sun Wu and Udi Manber described the algorithm in a technical report of the University of Arizona in May 1994. An earlier version was part of agrep, and the algorithm was the engine of glimpse. Their report compares it with [Aho-Corasick](/aho-corasick/), the basis of UNIX fgrep, and with [Commentz-Walter](/commentz-walter/), which GNU fgrep 2.0 and Hume's gre used, and finds it faster for large sets. Navarro and Raffinot (2002) place it among the suffix-based methods and find it among the fastest for large sets of patterns over moderate alphabets.

## References
