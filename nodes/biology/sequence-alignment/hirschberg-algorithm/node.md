---
tag: WVTXEZ
kind: algorithm
slug: hirschberg-algorithm
name: Hirschberg's alignment algorithm
aliases:
- Hirschberg linear-space global alignment
area: biology/sequence-alignment
level: advanced
summary: Finds an optimal global alignment in O(mn) time and O(min(m, n)) space, by a forward and a backward score pass that split the problem at its middle row.
solves: [global-alignment]
model: word-ram
complexity:
  vars: {m: the length of the longer sequence, n: the length of the shorter sequence}
  time: {worst: Θ(m n), average: Θ(m n), best: Θ(m n)}
  space: {extra: "O(n + log m)"}
properties: {deterministic: true, exact: true, online: false, recursive: true}
history:
  year: 1975
  people: [Daniel S. Hirschberg]
  note: Hirschberg (1975) found a longest common subsequence in linear space by divide and conquer. Myers and Miller (1988) brought the method to alignment with affine gaps, and it became the standard way to align long sequences in little memory.
prereqs: [needleman-wunsch, divide-and-conquer-paradigm, rolling-array-space-reduction]
see_also: [hirschberg-lcs, needleman-wunsch, smith-waterman, gotoh-algorithm, alignment-graph, banded-alignment, global-alignment, semi-global-dp]
sources:
  - paper: doi:10.1145/360825.360861
    title: Daniel S. Hirschberg, A linear space algorithm for computing maximal common subsequences, Communications of the ACM 18(6), 1975, 341-343
    locator: the last row of the table in linear space, and the divide and conquer on the middle row of the first string
  - paper: "Eugene W. Myers and Webb Miller, Optimal alignments in linear space, Computer Applications in the Biosciences 4(1), 1988, 11-17"
    locator: the linear-space alignment with affine gap costs
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 2, Section 2.6, Linear space alignments
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design, Addison-Wesley, 2006
    locator: Section 6.7, Sequence alignment in linear space via divide and conquer
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 12, the section on computing alignments in only linear space
---

Hirschberg's algorithm finds an optimal [global alignment](/global-alignment/) of two sequences in $\Theta(mn)$ time and only $O(\min(m, n))$ working space, where the [Needleman-Wunsch](/needleman-wunsch/) traceback needs the whole $\Theta(mn)$ table. It computes the scores of the top half of one sequence against every prefix of the other, and the scores of the bottom half against every suffix, each with one row of memory. The best sum of the two shows where an optimal alignment crosses the middle row, and the algorithm solves the two halves on each side of that point in the same way. The work is about twice that of one table fill. This page uses a substitution score $s(a, b)$ and a linear gap penalty $d$ per gap symbol; the LCS form of the same method is on the page [Hirschberg's LCS algorithm](/hirschberg-lcs/).

## In plain words

The global method fills a grid of scores and then walks back through it to find the alignment. For two long sequences, the grid does not fit in memory. But the scores alone need only two rows at a time; it is the walk back that needs the whole grid.

Hirschberg's idea: cut the first sequence in the middle. Score the top half against every start of the second sequence, going forward. Score the bottom half against every end of the second sequence, going backward. Both passes keep only two rows. For each place where you could cut the second sequence, add the two scores. The best place tells you how the best alignment splits into a top part and a bottom part. Now you have two smaller problems of the same kind, and you solve each one the same way, until the pieces are tiny.

## The problem

**Input.** Sequences $x = x_1 \cdots x_m$ and $y = y_1 \cdots y_n$ over an alphabet $\Sigma$ (DNA, RNA or amino acids), a substitution score $s : \Sigma \times \Sigma \to \mathbb{Z}$, and a gap penalty $d \ge 0$ per gap symbol. If $y$ is longer than $x$, exchange the two and use $s(b, a)$ in place of $s(a, b)$, so that $n \le m$.

**Output.** An optimal global alignment of $x$ and $y$ and its score, as for [Needleman-Wunsch](/needleman-wunsch/), using $O(n)$ words of working memory beside the input and the output, plus $O(\log m)$ for the pending subproblems. The costs are in the [word RAM](/word-ram/) model: a score fits in one word, and one step of the recurrence takes constant time.

## The algorithm

Write $x(i_0, i_1]$ for $x_{i_0 + 1} \cdots x_{i_1}$. LAST-ROW computes the last row of the Needleman-Wunsch table of $x(i_0, i_1]$ against $y(j_0, j_1]$ with one row of $w + 1$ cells, $w = j_1 - j_0$. In the backward mode it reads both pieces from the right, so its entry $r[k]$ is the best score of $x(i_0, i_1]$ against the last $k$ letters of $y(j_0, j_1]$.

```pseudo id=main
LAST-ROW(x(i0, i1], y(j0, j1], backward)
L1  for k ← 0 to w do r[k] ← −k · d                       ▷ w = j1 − j0
L2  for t ← 1 to i1 − i0 do                               ▷ a ← x_{i0+t}, or x_{i1−t+1} if backward
L3      diag ← r[0], r[0] ← −t · d
L4      for k ← 1 to w do                                 ▷ b ← y_{j0+k}, or y_{j1−k+1} if backward
L5          new ← max(diag + s(a, b), r[k] − d, r[k − 1] − d), diag ← r[k], r[k] ← new
L6  return r

HIRSCHBERG(i0, i1, j0, j1)                                ▷ align x(i0, i1] with y(j0, j1]
L7  if i0 = i1 or j0 = j1 then return the columns of the rest against gaps
L8  if i1 − i0 = 1 then return x_{i1} under the letter b of y(j0, j1] with the largest s(x_{i1}, b), and gaps against the other letters, if s(x_{i1}, b) > −2d; otherwise (x_{i1}, −) and gaps against all of y(j0, j1]
L9  mid ← ⌊(i0 + i1) / 2⌋
L10 f ← LAST-ROW(x(i0, mid], y(j0, j1], forward)
L11 b ← LAST-ROW(x(mid, i1], y(j0, j1], backward)
L12 k ← the smallest k in 0 .. w with the largest f[k] + b[w − k]
L13 return HIRSCHBERG(i0, mid, j0, j0 + k) followed by HIRSCHBERG(mid, i1, j0 + k, j1)
```

The first call is HIRSCHBERG$(0, m, 0, n)$, and the score of the alignment is the sum of its column scores.

LAST-ROW is Needleman-Wunsch with one row. Before line L5 overwrites $r[k]$, $r[k]$ still holds the cell above and $r[k - 1]$ already holds the cell to the left; the variable $diag$ keeps the old $r[k - 1]$, the cell above and to the left.

Line L7 handles an empty piece: the only alignment is all gaps. Line L8 handles one letter $a$ of $x$ against $w \ge 1$ letters of $y$. The alignment either pairs $a$ with one letter $b$, with the score $s(a, b) - (w - 1)d$, or leaves $a$ against a gap, with the score $-(w + 1)d$. So pairing is better exactly when $s(a, b) > -2d$.

Lines L9 to L12 find the split. Every alignment of the two pieces is a path in the [alignment graph](/alignment-graph/) that crosses row $mid$ at some column $j_0 + k$. The best path through that point scores $f[k] + b[w - k]$: the best alignment of the top half with the first $k$ letters, plus the best alignment of the bottom half with the other $w - k$ letters. Line L12 takes the best $k$, and line L13 solves the two parts. The implementation keeps the pending parts on an explicit stack instead of the call stack.

## Example

Toy DNA scheme: $s(a, a) = +2$, $s(a, b) = -1$ for $a \ne b$, $d = 2$. Align $x = $ AGTACGCA ($m = 8$) and $y = $ TATGC ($n = 5$).

**The first split.** $mid = 4$, so the top half is AGTA and the bottom half is CGCA. Line L10 scores AGTA against the prefixes of TATGC, line L11 scores CGCA against the suffixes.

| $k$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $f[k]$: AGTA against the first $k$ letters | $-8$ | $-4$ | 0 | $-2$ | $-1$ | $-3$ |
| $b[5 - k]$: CGCA against the last $5 - k$ letters | $-3$ | $-1$ | 1 | 0 | $-4$ | $-8$ |
| $f[k] + b[5 - k]$ | $-11$ | $-5$ | **1** | $-2$ | $-5$ | $-11$ |

The best sum is 1 at $k = 2$, so the optimal score is 1, and an optimal alignment aligns AGTA with TA and CGCA with TGC.

**The recursion.** Each line is one call of HIRSCHBERG; the sums are $f[k] + b[w - k]$ for $k = 0, 1, \ldots$

| call | split of $x$ | sums | $k$ | result |
|---|---|---|---|---|
| AGTACGCA, TATGC | AGTA, CGCA | $-11, -5, 1, -2, -5, -11$ | 2 | TA and TGC |
| AGTA, TA | AG, TA | $0, -3, -6$ | 0 | AG against nothing, TA against TA |
| AG, empty | | | | line L7: (A, $-$), (G, $-$) |
| TA, TA | T, A | $-2, 4, -2$ | 1 | line L8 twice: (T, T), (A, A) |
| CGCA, TGC | CG, CA | $-8, -5, 1, -5$ | 2 | CG against TG, CA against C |
| CG, TG | C, G | $-2, 1, -5$ | 1 | line L8 twice: (C, T), (G, G) |
| CA, C | C, A | $-3, 0$ | 1 | line L8: (C, C); line L7: (A, $-$) |

The columns, in order, give

```
A G T A C G C A
- - T A T G C -
```

with the score $-2 - 2 + 2 + 2 - 1 + 2 + 2 - 2 = 1$. LAST-ROW and line L8 compute 75 cells in total: $40 = 8 \cdot 5$ at the top, then $8$, $4$, $12$, $4$ and $2$ at the inner splits, and 5 in the one-letter calls. Needleman-Wunsch computes $8 \cdot 5 = 40$ cells. Here the ratio is $75 / 40 \approx 1.9$.

## Correctness

The split is right because every alignment of the two pieces crosses the middle row of the alignment graph at some column $j_0 + k$, and cutting it there gives an alignment of the top half with $y(j_0, j_0 + k]$ and one of the bottom half with $y(j_0 + k, j_1]$. So the best score is $\max_k$ of the sum of the two best part scores. LAST-ROW gives these part scores: $f[k]$ directly, and $b[w - k]$ because reversing both strings maps alignments to alignments with the same score. Concatenating optimal alignments of the two parts at the best $k$ gives an optimal alignment of the whole. The base cases of lines L7 and L8 list all the alignments. Induction on $i_1 - i_0$ finishes the proof, which is below.

## Complexity

Count the cells that LAST-ROW and line L8 compute; every other step of a call takes time linear in $w$, and there are $O(m)$ calls. A call on $m'$ rows and $n'$ columns computes $m' n'$ cells in lines L10 and L11 together, then calls itself on $\lfloor m'/2 \rfloor$ rows with $k$ columns and on $\lceil m'/2 \rceil$ rows with $n' - k$ columns. A proof below shows that the total is at most $n \cdot R(m)$, where

$$R(1) = 1, \qquad R(m) = m + R(\lceil m/2 \rceil), \qquad R(m) \le 2m + \lceil \lg m \rceil - 1.$$

- **Time.** At least the $mn$ cells of the top level and at most $n(2m + \lceil \lg m \rceil - 1)$ cells, so $\Theta(mn)$ in the best, the average and the worst case. For $m$ a power of 2, the count is exactly $n(2m - 1)$, whatever the splits: $5 \cdot 15 = 75$ in the example. So the work is about twice that of a Needleman-Wunsch fill.
- **Space.** The rows $f$, $b$ and $r$ have at most $n + 1$ cells each, and they are freed before the next call, so $O(n)$ words. The stack of pending parts has $O(\log m)$ entries, because $i_1 - i_0$ halves at each level. The output has at most $m + n$ columns. With $n \le m$, the working space is $O(\min(m, n) + \log \max(m, n))$.
- **The cost of the swap.** If the rows ran over the longer sequence, the space would be $O(\max(m, n))$. The time bound needs no swap.

## Properties

- **Exact.** It returns an optimal global alignment for every integer $s$ and $d \ge 0$.
- **Deterministic.** Line L12 takes the smallest best $k$. Different tie rules can give different optimal alignments, and they need not agree with the traceback of Needleman-Wunsch.
- **Recursive.** The divide and conquer has depth $\lceil \lg m \rceil$.
- **The score comes early.** The best sum of the first split, line L12 at the top level, is already the optimal score.

## Variants and improvements

- **Affine gaps.** Myers and Miller (1988) extended the method to the gap penalty $d + (L - 1)e$ of the [Gotoh algorithm](/gotoh-algorithm/). The split must also record whether the optimal path crosses the middle row inside a vertical gap, so that the gap is not charged two openings.
- **Local and semi-global forms.** A score-only pass of [Smith-Waterman](/smith-waterman/) finds the end of the best local alignment, a reversed pass finds its start, and Hirschberg's algorithm aligns the part between them. The [semi-global DP](/semi-global-dp/) works the same way.
- **LCS.** With match 1 and no penalties, the method is the original [Hirschberg's LCS algorithm](/hirschberg-lcs/).
- **Checkpoints.** Instead of halving, keep every $\sqrt{m}$-th row of the table in a first pass, then fill each block again for the traceback. This uses $O(n\sqrt{m})$ space and about twice the work, without recursion; with more levels it trades space for time.
- **Bands.** In a [banded alignment](/banded-alignment/), the same split works inside the band.
- **Parallel.** The forward and backward passes of a call are independent, and so are the two calls of line L13.

## When to use it

Use Hirschberg's algorithm when you need the alignment itself and the $(m + 1)(n + 1)$ table of Needleman-Wunsch does not fit in memory: two sequences of $10^5$ letters need $10^{10}$ cells, but Hirschberg's algorithm needs a few rows of $10^5$ cells. If you need only the score, two rows of Needleman-Wunsch are enough, and that is twice as fast. If the table fits in memory, Needleman-Wunsch is simpler and about twice as fast.

## Pitfalls

- **A wrong one-letter rule.** In line L8, the letter of $x$ pairs with a letter of $y$ only if the score is above $-2d$, because the pair replaces two gap columns. A threshold of $-d$ can choose the gap version when the pair is better. With $s(a, b) = -3$, $d = 2$ and one letter on each side, the pair scores $-3$ and the two gap columns score $-4$, but the test $s(a, b) > -d$ fails and rejects the pair.
- **The wrong backward entry.** Line L12 must add $f[k]$ to $b[w - k]$, not to $b[k]$, because $b[k]$ is the score against the last $k$ letters. With $b[k]$, the example would add the scores of overlapping parts of $y$, and the result would not be an alignment of the whole.
- **A backward pass that reverses only one string.** Line L11 must read both pieces from the right. Reversing only $y$ computes a different table, which is not the score of any suffix pair.
- **Rows over the longer sequence.** If the rows of lines L1 to L5 run over the longer sequence, the memory is $O(\max(m, n))$. Exchange the two sequences first, and transpose $s$ if it is not symmetric.

## Implementations

## History

Daniel Hirschberg published the method in 1975 in the Communications of the ACM, for the longest common subsequence: "A linear space algorithm for computing maximal common subsequences". The paper showed that the last row of the LCS table can be computed in linear space, and that a divide and conquer on the middle row recovers the subsequence itself in linear space and quadratic time. Myers and Miller (1988), in "Optimal alignments in linear space", brought the method to sequence alignment with affine gap costs, and it became part of the standard toolbox of sequence analysis. The textbook by Durbin et al. (1998) presents it as the linear-space form of Needleman-Wunsch, and Kleinberg and Tardos present it as an example of divide and conquer combined with dynamic programming.

## References
