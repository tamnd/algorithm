---
tag: MXPHKN
kind: algorithm
slug: myers-bit-parallel-algorithm
name: Myers bit-parallel algorithm
aliases:
- Myers bit-vector algorithm
area: strings/approximate-matching
level: advanced
summary: Encodes DP columns as bit vectors, giving O(nm/w) time for edit distance and approximate matching.
solves: [k-differences-problem, edit-distance, approximate-string-matching]
model: word-ram
complexity:
  vars: {m: the pattern length, n: the text length, k: the error bound, w: the word length, σ: the alphabet size}
  time: {worst: "O(m + ⌈m / w⌉ (σ + n))", average: "O(m + ⌈m / w⌉ (σ + n))"}
  space: {extra: "O(σ ⌈m / w⌉)"}
properties: {deterministic: true, exact: true, online: true, recursive: false}
history:
  year: 1998
  people: [Gene Myers, Heikki Hyyrö]
  note: Myers presented the algorithm at CPM 1998 and in the Journal of the ACM in 1999. Hyyrö restated it in 2001 in the form with vertical and horizontal difference vectors used on this page.
prereqs: [sellers-algorithm, bit-parallelism, edit-distance]
see_also: [wu-manber-approximate-matching, bitap-algorithm, ukkonen-cutoff-algorithm, k-differences-problem, wagner-fischer-algorithm, landau-vishkin-algorithm, levenshtein-automaton, word-ram]
sources:
  - paper: "Gene Myers, A fast bit-vector algorithm for approximate string matching based on dynamic programming, Journal of the ACM 46(3), 1999"
    locator: the whole paper (the encoding of a column by its vertical differences, the cell logic, the addition that resolves the dependency along the column, and the blocks for long patterns)
  - paper: "Heikki Hyyrö, Explaining and extending the bit-parallel approximate string matching algorithm of Myers, Technical Report A-2001-10, Department of Computer and Information Sciences, University of Tampere, 2001"
    locator: the derivation of the vectors Pv, Mv, Ph, Mh and D0 and the step formulas that this page uses
  - paper: doi:10.1145/375360.375365
    title: Gonzalo Navarro, A guided tour to approximate string matching, ACM Computing Surveys 33(1), 2001
    locator: Section 7.3, Parallelizing the dynamic programming matrix (the paragraph Myers 1998, with the difference recurrences and the bounds O(⌈m/w⌉ n) worst case and O(⌈k/w⌉ n) average case)
  - book: isbn:9780521813075
    title: Gonzalo Navarro and Mathieu Raffinot, Flexible Pattern Matching in Strings, Cambridge University Press, 2002
    locator: Chapter 6, Approximate matching (the bit-parallel simulation of the dynamic programming matrix)
---

Myers' bit-parallel algorithm solves the [k-differences problem](/k-differences-problem/) and computes the [edit distance](/edit-distance/) by storing, for one column of the [Sellers table](/sellers-algorithm/), the differences between vertically adjacent cells in two bit vectors. Each difference is $-1$, $0$ or $+1$, so two bits per cell are enough, and about fifteen word operations update the whole column for one text character. On a [word RAM](/word-ram/) with $w$-bit words the time is $O(\lceil m / w \rceil n)$ for a pattern of length $m$ and a text of length $n$, which is $O(n)$ when the pattern fits in one word. Gene Myers published it in 1998, and this page uses the form that Heikki Hyyrö gave in 2001.

## In plain words

The classic table for approximate matching has one column for each text letter and one number for each pattern letter. Two neighbouring numbers in a column differ by at most one. So instead of the numbers, the program can store only the steps between them: up, down or flat.

The program keeps two rows of bits. One row marks where the column steps up, the other where it steps down. For each text letter, a few bit operations on whole machine words turn the steps of one column into the steps of the next. One addition handles the hard part, where a change at one row moves down to the rows below.

The number at the bottom of the column says how many errors the best match ending at this text letter needs. The program keeps it in a counter and reports the text position when it is small enough.

## The problem

The edit model is the Levenshtein distance: insertion, deletion and substitution of one character, each at cost 1, and no transpositions. Indices are 0-based. The input is a pattern $P$ of length $m$, a text $T$ of length $n$ and an integer $k \ge 0$. The output is the sorted list of end positions $j \in \{0, \ldots, n\}$ such that some substring $T[h..j)$ with $0 \le h \le j$ has $\operatorname{ed}(P, T[h..j)) \le k$. Each end position is reported once, even when several substrings end there. For $m = 0$ every $j$ is reported. The same vectors with another first row give $\operatorname{ed}(A, B)$ for two strings.

Let $C[i][j]$ be the Sellers table: $C[0][j] = 0$, $C[i][0] = i$, and $C[i][j] = \min(C[i-1][j-1] + [P[i-1] \ne T[j-1]],\ C[i][j-1] + 1,\ C[i-1][j] + 1)$. Then $C[m][j] = \min_h \operatorname{ed}(P, T[h..j))$. The algorithm keeps column $j$ as two $m$-bit vectors: bit $i - 1$ of $Pv$ is set when $C[i][j] - C[i-1][j] = 1$, and bit $i - 1$ of $Mv$ is set when it is $-1$.

## The algorithm

```pseudo id=main
MYERS(P, T, k)                       ▷ m = |P| ≥ 1; all vectors have m bits
L1  for each symbol c: Peq[c] ← the vector with bit i set exactly when P[i] = c
L2  Pv ← 1^m, Mv ← 0, score ← m      ▷ column 0: C[i][0] = i
L3  if score ≤ k then report 0
L4  for j ← 1 to n do
L5      Eq ← Peq[T[j − 1]], Xv ← Eq | Mv
L6      Xh ← (((Eq & Pv) + Pv) ⊕ Pv) | Eq      ▷ the carry out of bit m − 1 is dropped
L7      Ph ← Mv | ¬(Xh | Pv), Mh ← Pv & Xh
L8      if bit m − 1 of Ph is set then score ← score + 1 else if bit m − 1 of Mh is set then score ← score − 1
L9      Ph ← Ph << 1, Mh ← Mh << 1           ▷ bit 0 becomes 0, because C[0][j] = 0
L10     Pv ← Mh | ¬(Xv | Ph), Mv ← Ph & Xv
L11     if score ≤ k then report j
```

Besides $Pv$ and $Mv$ for column $j - 1$, the step uses three derived vectors for column $j$. Bit $i - 1$ of $Ph$ (of $Mh$) is set when $C[i][j] - C[i][j-1]$ is $+1$ (is $-1$). The vector $D = Xh \mid Mv$ marks the rows $i$ with $C[i][j] = C[i-1][j-1]$. A row has $D$ set when its letters match, when its column steps down, or when the row above steps down horizontally. The last case depends on the row above in the same column, and line L6 resolves this chain for all rows at once with one addition, whose carries run down a block of set bits of $Pv$. Lines L7 and L10 then read the new horizontal and vertical steps from $D$ and the old steps. The counter $score$ follows $C[m][j]$ through the horizontal step of the last row.

For the edit distance $\operatorname{ed}(A, B)$ with $P = A$ and $T = B$, the first row is $C[0][j] = j$. The only change is in line L9: the shift of $Ph$ fills bit 0 with 1, because row 0 steps up in each column. Then $score = \operatorname{ed}(A, B)$ after the last column.

## Example

Take $P = \texttt{GATAA}$, $T = \texttt{CAGATAAGAGAA}$ and $k = 1$. In the tables, a vector is written with bit 0 (row 1) on the left and bit 4 (row 5) on the right, so the carries of an addition run to the right. The match masks are $Peq[\texttt{G}] = 10000$, $Peq[\texttt{A}] = 01011$, $Peq[\texttt{T}] = 00100$, and 00000 for $\texttt{C}$.

| $j$ | $T[j-1]$ | $Pv$ | $Mv$ | $score = C[5][j]$ |
|---|---|---|---|---|
| 0 | | 11111 | 00000 | 5 |
| 1 | C | 11111 | 00000 | 5 |
| 2 | A | 10111 | 00000 | 4 |
| 3 | G | 01111 | 00000 | 4 |
| 4 | A | 10111 | 01000 | 3 |
| 5 | T | 10011 | 00100 | 2 |
| 6 | A | 10001 | 00010 | 1 |
| 7 | A | 10100 | 00011 | 0 |
| 8 | G | 01100 | 00001 | 1 |
| 9 | A | 10110 | 01000 | 2 |
| 10 | G | 01011 | 00000 | 3 |
| 11 | A | 10101 | 01000 | 2 |
| 12 | A | 10000 | 00000 | 1 |

The scores at most 1 give the end positions 6, 7, 8 and 12. For example, $j = 7$ ends the exact occurrence $T[2..7) = \texttt{GATAA}$, and $j = 12$ ends $T[7..12) = \texttt{GAGAA}$ with one substitution. With $k = 0$ the only end position is 7.

Column 7 has $Pv = 10100$ and $Mv = 00011$, so its values are $C[\cdot][7] = 0, 1, 1, 2, 1, 0$ for rows 0 to 5. The step to column 8 reads $T[7] = \texttt{G}$:

| vector | value | how |
|---|---|---|
| $Eq$ | 10000 | $Peq[\texttt{G}]$ |
| $Xv$ | 10011 | $Eq \mid Mv$ |
| $Eq \,\&\, Pv$ | 10000 | row 1 |
| $(Eq \,\&\, Pv) + Pv$ | 01100 | row 1 gives 1 + 1, the carry moves to row 2 |
| $Xh$ | 11000 | $\oplus\, Pv$, then $\mid Eq$ |
| $Ph$ | 00011 | $Mv \mid \lnot(Xh \mid Pv)$ |
| $Mh$ | 10000 | $Pv \,\&\, Xh$ |
| new $Pv$ | 01100 | after the shifts, $Mh = 01000$ and $Ph = 00001$ |
| new $Mv$ | 00001 | $Ph \,\&\, Xv$ |

Bit 4 of $Ph$ is set, so the score grows from 0 to 1. Row 2 of $Xh$ is set only by the carry: $C[2][8] = 1 = C[1][7]$ because row 1 steps down from $C[1][7] = 1$ to $C[1][8] = 0$ when $\texttt{G}$ matches $P[0]$. The new vectors give $C[\cdot][8] = 0, 0, 1, 2, 2, 1$.

## Correctness

The proof is an induction over the columns. First, all vertical and horizontal differences of the Sellers table lie in $\{-1, 0, 1\}$, which follows from the recurrence one cell at a time. Then the value $C[i][j] - C[i-1][j-1]$ is 0 or 1, and it is 0 exactly when the letters match, or row $i$ of column $j - 1$ steps down, or row $i - 1$ steps down from column $j - 1$ to column $j$. This gives the cell logic of lines L7 and L10. The last condition makes a chain along the column, and a lemma on binary addition shows that the carries of line L6 follow exactly this chain. The full proof is below.

## Complexity

For $m \le w$, each text character costs a constant number of word operations: one table lookup, one addition, two shifts and about ten Boolean operations. The search takes $O(n)$ time after $O(m + \sigma)$ preprocessing for the table $Peq$, and the extra space is $O(\sigma)$ words, or $O(m)$ words with a hash table over the symbols of $P$. For $m > w$, each vector takes $\lceil m / w \rceil$ words. The addition passes its carry from word to word, and the shifts pass one bit from word to word, so a column costs $O(\lceil m / w \rceil)$ and the search costs $O(\lceil m / w \rceil n)$ in the worst case and on average. With Ukkonen's cut-off on blocks of $w$ rows, Myers' version for long patterns updates only the blocks up to the last active row, which gives $O(\lceil k / w \rceil n)$ on average for random text. The edit distance of two strings of lengths $m$ and $n$ costs $O(\lceil m / w \rceil n)$ the same way.

## Properties

- **Exact.** It reports exactly the end positions of the Sellers algorithm, not candidates.
- **Online.** It reads the text once, from left to right, with no lookahead.
- **Independent of $k$.** The work per column does not depend on $k$, unlike [Wu-Manber](/wu-manber-approximate-matching/), which needs $k + 1$ vectors.
- **Two bits per cell.** One word holds the state of $w$ rows of a column.
- **Unit costs only.** The encoding needs differences in $\{-1, 0, 1\}$, which holds for unit costs but not for general [weighted edit distances](/weighted-edit-distance/).

## Variants and improvements

- **Long patterns.** Split each vector into $\lceil m / w \rceil$ words, pass the carry of the addition and the bits of the shifts across words, and keep the score of each block for the cut-off.
- **The cut-off.** Myers combines the blocks with [Ukkonen's cut-off](/ukkonen-cutoff-algorithm/): only the blocks above the last row with value at most $k$ are updated.
- **Edit distance.** Fill bit 0 of the shifted $Ph$ with 1, as in the algorithm section. The same code then computes the [Levenshtein distance](/edit-distance/) of two strings.
- **Transpositions.** Hyyrö extended the vectors to the optimal string alignment form of the [Damerau-Levenshtein distance](/damerau-levenshtein-distance/), with one more vector that remembers the matches of the previous column.
- **Diagonal parallelism.** Baeza-Yates and Navarro pack the [automaton](/levenshtein-automaton/) by diagonals instead of by columns. Its update is a little simpler, but it needs more bits, so long patterns need more words.

## When to use it

Use it for approximate search with unit costs when the pattern is up to a few hundred characters long and $k$ is not tiny. For a small ratio $k / m$ on random text, a filter such as [pigeonhole filtering](/pigeonhole-filtering/), with this algorithm on the candidate areas, is faster. When $k$ is much smaller than $m / w$, the $O(k n)$ worst-case bound of [Landau-Vishkin](/landau-vishkin-algorithm/) is smaller.

## Pitfalls

- **The carry out.** The addition in line L6 can overflow bit $m - 1$. Mask the sum to $m$ bits, or the carry corrupts bits above the pattern.
- **Negation.** In a language with unbounded integers, such as Python, $\lnot x$ is negative. Mask it to $m$ bits each time.
- **Search or distance.** The search shifts a 0 into $Ph$, the distance computation shifts a 1. Swapping them gives wrong results with no error.
- **The order of the score update.** Read bit $m - 1$ of $Ph$ and $Mh$ before the shifts of line L9, which drop that bit.
- **Mv in the addition.** Hyyrö's form adds $Eq \,\&\, Pv$, not $(Eq \mid Mv) \,\&\, Pv$, and adds $Mv$ only after the addition. Both work, because $Pv$ and $Mv$ never share a bit, but mixing the two forms in one program breaks it.
- **Empty pattern.** With $m = 0$ there are no bits. Treat this case on its own: every position $0$ to $n$ is an end position.

## Implementations

## History

Gene Myers presented the algorithm at the conference on Combinatorial Pattern Matching (CPM) in 1998, and the journal version appeared in the Journal of the ACM in 1999. Navarro's survey of 2001 notes that it uses the bits of a word better than the earlier parallel forms of the dynamic programming matrix. In 2001 Heikki Hyyrö gave a new derivation of the algorithm with vertical and horizontal difference vectors, which most later descriptions and programs follow.

## References
