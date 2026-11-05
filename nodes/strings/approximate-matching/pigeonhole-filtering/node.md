---
tag: X6KSHQ
kind: technique
slug: pigeonhole-filtering
name: Pigeonhole filtering
aliases:
- pigeonhole partition filtering
area: strings/approximate-matching
level: core
summary: Split the pattern into k+1 pieces; any approximate match must contain one exact piece.
prereqs: [approximate-string-matching, pigeonhole-principle, aho-corasick]
see_also: [q-gram-filtering, q-gram-lemma, wu-manber-approximate-matching, k-mismatch-problem, string-similarity-join, seed-and-extend, read-mapping, sellers-algorithm]
sources:
  - paper: doi:10.1145/135239.135244
    title: Sun Wu and Udi Manber, Fast text searching allowing errors, Communications of the ACM 35(10), 1992
    locator: pages 83 to 91 (the partition of the pattern into k + 1 blocks, one of which must appear exactly, used in agrep for long patterns)
  - paper: doi:10.1145/375360.375365
    title: Gonzalo Navarro, A guided tour to approximate string matching, ACM Computing Surveys 33(1), 2001
    locator: Section 8 (filtering algorithms, the partition into exact search and into less errors, and hierarchical verification)
  - book: isbn:9780521813075
    title: Gonzalo Navarro and Mathieu Raffinot, Flexible Pattern Matching in Strings, Cambridge University Press, 2002
    locator: Chapter 6 (filtering for approximate matching, partitioning into exact search)
---

Pigeonhole filtering is a technique for approximate search that splits the pattern into $k + 1$ disjoint pieces, searches the text for the pieces exactly, and verifies only the text regions around the piece occurrences. It works because $k$ edits can touch at most $k$ of the $k + 1$ pieces, so one piece survives unchanged in every occurrence with at most $k$ errors, by the [pigeonhole principle](/pigeonhole-principle/). The exact search for several pieces at once is fast with a multi-pattern matcher such as [Aho-Corasick](/aho-corasick/). The method pays off when the pieces are long enough to be rare in the text, which needs a small error level $k/m$.

## In plain words

Suppose a pattern may appear in a text with a few errors, at most a given number. Cut the pattern into one more piece than the number of errors allowed. Each error falls into at most one piece, so at least one piece has no error at all, and it must appear in the text exactly as it is.

Exact search is much faster than search with errors. So first look for the pieces exactly. Each place where a piece appears tells you where the full pattern would have to be. Check only those places with the slow method that allows errors, and skip the rest of the text.

The test never misses a match. It saves time when the pieces are long and rare. With many errors allowed, the pieces become short and appear everywhere, and the test passes almost all of the text.

## When it applies

- The distance is the Levenshtein [edit distance](/edit-distance/) or the [Hamming distance](/hamming-distance/), or any distance where one operation changes at most one piece. Under the [Damerau-Levenshtein distance](/damerau-levenshtein-distance/), a transposition across a piece boundary touches two pieces, so the pattern needs $2k + 1$ pieces, or pieces separated by one unused character.
- The pattern has at least $k + 1$ characters, so each piece is nonempty. The pieces have length about $m/(k+1)$.
- On a random text over $\sigma$ letters, a piece of length $\ell$ matches at a position with probability $\sigma^{-\ell}$. The filter discards most of the text when $(k + 1)\, \sigma^{-m/(k+1)}$ times the verification cost per hit is small, which needs about $m/(k+1) > \log_\sigma m$.
- An exact verifier exists for the candidate regions, such as the [Sellers algorithm](/sellers-algorithm/).

## The template

The search finds the end positions $j \in \{0, \ldots, n\}$ of the approximate occurrences of $P$ (length $m$) in $T$ (length $n$) under the Levenshtein distance with bound $k$. Indices are 0-based. Piece $r$ is $P[s_r \ldots s_r + \ell_r)$, for $r = 0, \ldots, k$.

```pseudo id=main
PIGEONHOLE-FILTER(P, T, k)                     ▷ reports end positions
L1  if m ≤ k then return 0, 1, ..., n           ▷ every substring of length 0 is a match
L2  split P into k + 1 consecutive pieces P[s_r .. s_r + ℓ_r) of lengths ⌊m/(k+1)⌋ or ⌈m/(k+1)⌉
L3  find all exact occurrences of all pieces in T, for example with Aho-Corasick
L4  for each occurrence of piece r at T[p .. p + ℓ_r) do
L5      add the interval of ends [p − s_r + m − k, p − s_r + m + k] ∩ [0, n]
L6  merge the intervals that overlap or touch
L7  for each merged interval [a, b] do
L8      run SELLERS on T[max(0, a − m − k) .. b) and report each j in a..b with value at most k
```

**Why no match is lost.** Let $T[h \ldots j)$ have distance at most $k$ to $P$, and fix an alignment with at most $k$ edit columns. A substitution or a deletion lies inside one piece, and an insertion lies inside one piece or between two pieces. So at most $k$ pieces contain an edit column, and some piece $r$ is aligned with match columns only. These columns are consecutive, so piece $r$ occurs in $T$ at some $p$. Let $a$ and $b$ be the numbers of insertion and deletion columns after the columns of piece $r$. The part of $P$ after the piece has $m - s_r - \ell_r$ characters, so $j = p + \ell_r + (m - s_r - \ell_r) + a - b = p - s_r + m + (a - b)$. Since $|a - b| \le k$, the end $j$ lies in the interval of line L5.

**Why the verification is exact.** An occurrence that ends at $j$ has length at most $m + k$, so it starts at or after $j - m - k$. The [Sellers](/sellers-algorithm/) table of line L8 covers all these starts for all $j$ in $[a, b]$.

**Cost.** Line L3 takes $O(m + n + \mathrm{occ})$ time with Aho-Corasick, where $\mathrm{occ}$ is the number of piece occurrences. Each merged interval of length $L$ costs $O((L + m + k) m)$ in line L8, so the total verification is $O(\mathrm{occ} \cdot (m + k) \cdot m)$ in the worst case. On random text with long pieces, $\mathrm{occ}$ is small and the search costs $O(n)$ on average.

**Example.** $P = \texttt{GATAA}$ and $k = 1$ give the pieces $\texttt{GAT}$ ($s_0 = 0$) and $\texttt{AA}$ ($s_1 = 3$). In $T = \texttt{CCTCGTCCGATACCTCGGATAACC}$ ($n = 24$), $\texttt{GAT}$ occurs at 8 and 17, and $\texttt{AA}$ occurs at 20. The intervals are $[12, 14]$, $[21, 23]$ and $[21, 23]$, which merge to $[12, 14]$ and $[21, 23]$. Sellers on these regions reports the ends $\{12, 13, 21, 22, 23\}$, the same as Sellers on the whole text, after it checks 6 of the 25 end positions.

## Classic examples

- **agrep.** Wu and Manber split long patterns into $k + 1$ blocks, search for the blocks with a multi-pattern exact matcher, and run the [Wu-Manber](/wu-manber-approximate-matching/) bit-parallel search only around the hits.
- **k mismatches.** For the [k-mismatch problem](/k-mismatch-problem/), each piece sits at a fixed offset in an occurrence, so an occurrence of piece $r$ at $p$ gives the single candidate start $p - s_r$, which is checked by a direct count.
- **Seeds in read mapping.** In [read mapping](/read-mapping/), a read of length $m$ with at most $k$ errors contains an exact seed of length $\lfloor m/(k+1) \rfloor$. Tools look up the seeds in an index of the genome and extend the hits, as in [seed-and-extend](/seed-and-extend/).
- **Similarity joins.** In a [string similarity join](/string-similarity-join/) under the edit distance, each string is split into $k + 1$ segments, and a pair is a candidate only if one segment of one string appears in the other near the same position.

## Variations

- **More pieces.** With $j \ge k + 1$ pieces, at least $j - k$ of them survive. A filter can require several survivors at consistent positions, which is the step from pigeonhole filtering to [q-gram filtering](/q-gram-filtering/).
- **Fewer errors per piece.** With $j$ pieces, the edit columns split among the pieces, so some piece has at most $\lfloor k/j \rfloor$ errors. Searching the $j$ pieces with $\lfloor k/j \rfloor$ errors each allows longer pieces than exact search and works for larger error levels.
- **Hierarchical verification.** Split the pattern in two halves with $\lfloor k/2 \rfloor$ errors each, recursively. A hit of a small piece is first checked against the larger piece that contains it, and only then against the whole pattern. This discards most false hits early.
- **Indexes.** For a static text, look up the pieces in a [suffix array](/suffix-array/) or an FM-index instead of scanning the text.
- **Hamming distance.** The pieces have fixed offsets, so verification is a direct count of mismatches in one window.

## Pitfalls

- **Too many errors.** When $k + 1 > m$, some piece is empty and matches everywhere. When $m/(k+1)$ is small, the pieces occur almost everywhere and the verification dominates.
- **The wrong window.** A piece hit at $p$ fixes the start of the occurrence only up to $\pm k$ under the edit distance. Verifying only the window that starts at $p - s_r$ misses occurrences with insertions or deletions before the piece.
- **Overlapping regions.** Many hits close together give overlapping regions. Merge them before verification, or the same text is verified many times and the same end is reported more than once.
- **Transpositions.** A swap of the last character of one piece with the first character of the next one breaks two pieces, so $k + 1$ pieces are not enough under the Damerau-Levenshtein distance.
- **Repetitive text.** A periodic text can contain a piece at almost every position, so the worst case is no better than the verifier on the whole text.

## Exercises

1. Prove that with $j$ pieces and at most $k$ errors, at least $j - k$ pieces occur exactly in the occurrence.
2. Prove that with $j$ pieces, some piece has at most $\lfloor k/j \rfloor$ errors in an optimal alignment.
3. For $m = 30$, $k = 4$ and a random DNA text, estimate the expected number of piece hits per text position.
4. Show by an example that a single transposition can break two pieces, and give a split that avoids it.
5. Adapt the template to report start positions under the Hamming distance, and give its worst-case time.

## References
