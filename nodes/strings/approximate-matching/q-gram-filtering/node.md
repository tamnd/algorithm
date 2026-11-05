---
tag: 7G6EZX
kind: technique
slug: q-gram-filtering
name: q-gram filtering
aliases:
- q-gram count filter
area: strings/approximate-matching
level: core
summary: Discard candidate pairs whose shared q-gram count falls below the q-gram lemma threshold before verifying them.
prereqs: [q-gram-lemma, sellers-algorithm]
see_also: [q-gram-lemma, pigeonhole-filtering, approximate-string-matching, string-similarity-join, approximate-dictionary-lookup, kmer-index, read-mapping, chang-lawler-algorithm]
sources:
  - paper: "Petteri Jokinen and Esko Ukkonen, Two algorithms for approximate string matching in static texts, Mathematical Foundations of Computer Science 1991, Lecture Notes in Computer Science 520, Springer"
    locator: the q-gram threshold and its use with a q-gram index of the text
  - paper: doi:10.1145/375360.375365
    title: Gonzalo Navarro, A guided tour to approximate string matching, ACM Computing Surveys 33(1), 2001
    locator: Section 8 (filtering algorithms, counting filters on text windows and their verification)
  - paper: "Luis Gravano, Panagiotis G. Ipeirotis, H. V. Jagadish, Nick Koudas, S. Muthukrishnan and Divesh Srivastava, Approximate string joins in a database (almost) for free, Proceedings of the 27th International Conference on Very Large Data Bases (VLDB), 2001"
    locator: the count, length and position filters on q-grams for joins under the edit distance
  - book: isbn:9780521813075
    title: Gonzalo Navarro and Mathieu Raffinot, Flexible Pattern Matching in Strings, Cambridge University Press, 2002
    locator: Chapter 6 (filtering algorithms for approximate matching)
---

q-gram filtering is a technique for approximate search that counts the substrings of length $q$ that a candidate shares with the pattern, discards each candidate whose count is below the threshold of the [q-gram lemma](/q-gram-lemma/), and checks only the rest with an exact method. The filter never discards a true match, because the lemma says that a string within $k$ edits of a pattern of length $m$ shares at least $m - q + 1 - kq$ q-grams with it. The count takes $O(1)$ time per text position, so the filter is fast, and its value depends on how many candidates it removes. It is used for [approximate string matching](/approximate-string-matching/) in texts and for [string similarity joins](/string-similarity-join/).

## In plain words

Comparing a pattern with every place in a text by the exact method is slow. A cheap test can first throw away most places.

Cut the pattern into all its short overlapping pieces of a fixed length. A place in the text that is close to the pattern must contain most of these pieces, because each small error breaks only a few pieces. So slide a window over the text and keep a running count of the pattern pieces in the window. When the count is too low, no match can end there, and the window is skipped.

The places that pass the test still need the slow check, because a window can contain the right pieces in the wrong order. The test saves time when the pieces are rare in the text, which needs pieces that are long enough and a pattern with few errors allowed.

## When it applies

- The distance is the Levenshtein [edit distance](/edit-distance/), the [Hamming distance](/hamming-distance/) or a distance where each operation breaks a bounded number of q-grams.
- The threshold $t = m - q + 1 - kq$ is positive, so $q < (m + 1)/(k + 1)$. The error level $\alpha = k/m$ must be small.
- The q-grams of the pattern are rare in the text. On a random text over $\sigma$ letters, a q-gram occurs at a position with probability $\sigma^{-q}$, so the filter works well when $\sigma^q$ is large compared with $m$.
- An exact verifier exists for the candidate regions, such as the [Sellers algorithm](/sellers-algorithm/).

## The template

The search below finds the end positions $j \in \{0, \ldots, n\}$ of the approximate occurrences of $P$ (length $m$) in $T$ (length $n$), under the Levenshtein distance with bound $k$. Indices are 0-based. $G_P(v)$ is the number of positions of the q-gram $v$ in $P$, and $W_j = T[\max(0, j - m) \ldots j)$ is the window of length $m$ that ends at $j$.

```pseudo id=main
QGRAM-FILTER(P, T, k, q)                     ▷ reports end positions
L1  t ← m − q + 1 − k q
L2  if t ≤ 0 then return SELLERS(P, T, k)    ▷ the filter cannot discard anything
L3  G_P ← the q-gram profile of P; G_W ← 0 for every q-gram; c ← 0
L4  for j ← 0 to n do
L5      if j ≥ q then v ← T[j − q .. j); if G_W(v) < G_P(v) then c ← c + 1; G_W(v) ← G_W(v) + 1
L6      if j − m − 1 ≥ 0 then v ← T[j − m − 1 .. j − m − 1 + q); G_W(v) ← G_W(v) − 1; if G_W(v) < G_P(v) then c ← c − 1
L7      if c ≥ t then mark j as a candidate     ▷ c = Σ_v min(G_P(v), G_W(v)) for the window W_j
L8  for each maximal run a, a + 1, ..., b of candidates do
L9      run SELLERS on T[max(0, a − m − k) .. b) and report each j in a..b with value at most k
```

Line L5 adds the q-gram that ends at $j$ to the window, and line L6 removes the q-gram that starts just before the window. The variable $c$ counts the q-grams of the window with multiplicity, but at most $G_P(v)$ copies of each $v$, which is the shared count $\sum_v \min(G_P(v), G_{W_j}(v))$. Each step takes $O(1)$ time with a table of counts indexed by q-grams, so the filter takes $O(n + m)$ time.

**Why no match is lost.** Let $T[h \ldots j)$ have distance at most $k$ to $P$. If $j - h \le m$, the window $W_j$ contains $T[h \ldots j)$, and the q-gram lemma gives $c \ge t$. If $j - h = m + a$ with $a > 0$, fix an optimal alignment with $b$ insertion columns. Then $b \ge a$, because the lengths differ by the number of insertions minus the number of deletions. In the proof of the lemma, an insertion breaks at most $q - 1$ q-grams, so at least $m - q + 1 - (k - b) q - b (q - 1) = t + b$ q-grams of $P$ map to distinct equal q-grams of $T[h \ldots j)$. At most $a$ of these images start before $j - m$, so at least $t + b - a \ge t$ lie in $W_j$. So every true end is a candidate.

**Why the verification is exact.** An occurrence that ends at $j$ has length at most $m + k$, so it starts at or after $j - m - k$. The [Sellers](/sellers-algorithm/) table over $T[\max(0, a - m - k) \ldots b)$ covers all starts of all occurrences that end in $a, \ldots, b$, so its last row at $j$ is the true least distance.

**Example.** $P = \texttt{GATAA}$, $k = 1$ and $q = 2$, so $t = 5 - 2 + 1 - 2 = 2$, and the q-grams of $P$ are $\texttt{GA}$, $\texttt{AT}$, $\texttt{TA}$ and $\texttt{AA}$. In $T = \texttt{CCTCGTCCGATACCTCGGATAACC}$ ($n = 24$), the counts $c$ for $j = 0, \ldots, 24$ are

0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 3, 2, 1, 0, 0, 0, 1, 2, 3, 4, 3, 2.

The candidates are $11, \ldots, 14$ and $20, \ldots, 24$, which are 9 of the 25 end positions. Sellers runs on $T[5 \ldots 14)$ and $T[14 \ldots 24)$ and reports the ends $\{12, 13, 21, 22, 23\}$, the same as Sellers on the whole text. For example, $T[8 \ldots 12) = \texttt{GATA}$ is one deletion from $P$.

## Classic examples

- **Search in a text.** For [approximate string matching](/approximate-string-matching/), the template above is the counting filter. With a [k-mer index](/kmer-index/) of a static text, Jokinen and Ukkonen look up the q-grams of the pattern and count them per text region, so most of the text is never read.
- **Similarity joins.** In a [string similarity join](/string-similarity-join/) under the edit distance, two strings $x$ and $y$ can be within $k$ only if they share at least $\max(|x|, |y|) - q + 1 - kq$ q-grams. Gravano and others run this count filter, a length filter and a position filter inside a relational database before the exact check.
- **Spelling correction.** In an [approximate dictionary lookup](/approximate-dictionary-lookup/), an inverted index from q-grams to words returns the words that share enough q-grams with the query, and only these words get an edit distance computation.
- **Biological sequence search.** Tools such as QUASAR and SWIFT count shared q-grams in regions of a genome or a database to find the places where a query can align with few errors, a step that [read mapping](/read-mapping/) also needs.

## Variations

- **Length filter.** $d(x, y) \ge ||x| - |y||$, so pairs whose lengths differ by more than $k$ can be dropped without any q-gram count.
- **Position filter.** By the q-gram lemma, the kept q-grams appear at positions that differ by at most $k$. Counting only the shared q-grams whose positions differ by at most $k$ gives a stronger filter with the same threshold.
- **Disjoint q-grams.** Instead of all q-grams of the pattern, use $\lfloor m / q \rfloor$ disjoint ones. Each edit breaks at most one of them, so at least $\lfloor m / q \rfloor - k$ survive. With $k + 1$ pieces this is the [pigeonhole filter](/pigeonhole-filtering/).
- **Choice of $q$.** A larger $q$ makes q-grams rarer in the text but lowers the threshold. A common choice on random text is $q \approx \log_\sigma m$.
- **Gapped q-grams.** A q-gram with fixed gaps, such as positions 0, 1 and 3, can be more selective at the same threshold. The threshold must then be computed for the shape of the gaps.
- **Hamming distance.** With only substitutions, use windows of length exactly $m$ and count the q-grams at equal offsets. The threshold is the same.
- **q-gram distance.** The value $D_q(x, y) / (2q)$, from the [q-gram lemma](/q-gram-lemma/) page, is a lower bound of $d(x, y)$ that a filter can test instead of the count.

## Pitfalls

- **Sets instead of multisets.** Counting distinct shared q-grams loses true matches. For $P = \texttt{aaaaa}$, $q = 2$ and $k = 1$, the threshold is 2, and the text $\texttt{aaaaa}$ matches exactly, but it shares only one distinct 2-gram with $P$.
- **A threshold of zero or less.** When $q \ge (m + 1)/(k + 1)$, every window passes, and the filter only adds cost. Choose a smaller $q$ or another method.
- **Transpositions.** Under the [Damerau-Levenshtein distance](/damerau-levenshtein-distance/), one transposition breaks up to $q + 1$ q-grams, so the threshold must be $m - q + 1 - k(q + 1)$.
- **Verification region.** An occurrence ending at a candidate $j$ can start as early as $j - m - k$. A verifier that starts at $j - m$ misses occurrences with insertions.
- **Repetitive texts.** On a text full of the pattern's q-grams, almost every window passes, and the total time is the time of the verifier plus the filter.

## Exercises

1. For $m = 20$ and $k = 3$, find the largest $q$ with a positive threshold, and the threshold for that $q$.
2. Prove that $d(x, y) \le k$ implies $||x| - |y|| \le k$, and use it to bound the length of an approximate occurrence.
3. Show that with $\lfloor m / q \rfloor$ disjoint q-grams of the pattern, at least $\lfloor m / q \rfloor - k$ of them occur in any string within distance $k$.
4. Give a pattern, a text window and $k$ such that the window passes the count filter but contains no occurrence.
5. Change the template for the Hamming distance, where each occurrence has length exactly $m$, and prove that it reports the same starts as a direct count.

## References
