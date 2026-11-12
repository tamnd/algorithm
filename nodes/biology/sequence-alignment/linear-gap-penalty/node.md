---
tag: JWM3NG
kind: concept
slug: linear-gap-penalty
name: Linear gap penalty
aliases:
- constant per-gap cost
- linear gap cost
area: biology/sequence-alignment
level: intro
summary: The gap model g(L) = dL, where each space costs the same amount d; the score splits over columns, so one DP table of O(mn) cells suffices.
prereqs: [gap-penalty]
see_also: [affine-gap-penalty, needleman-wunsch, smith-waterman, edit-distance, longest-common-subsequence, hirschberg-algorithm, scoring-matrix]
sources:
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 2, Section 2.2 (linear gap score) and Section 2.3 (global and local alignment with a linear gap score)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 11, Section 11.8 (gap weight models)
  - paper: doi:10.1145/321796.321811
    title: Robert A. Wagner and Michael J. Fischer, The string-to-string correction problem, Journal of the ACM 21(1), 1974, 168-173
    locator: the edit distance recurrence with a fixed cost per inserted or deleted character
---

A linear gap penalty charges a gap of length $L$ the cost $g(L) = dL$ for a fixed $d > 0$. Each space in an alignment costs $d$, and a gap of three spaces costs the same as three separate gaps of one space. Because of this, the alignment score is a sum over columns, and [Needleman-Wunsch](/needleman-wunsch/) and [Smith-Waterman](/smith-waterman/) compute the best score with one table in $O(mn)$ time. It is the simplest [gap penalty](/gap-penalty/), and the [affine gap penalty](/affine-gap-penalty/) is its usual replacement in biology.

## In plain words

When two sequences are lined up, a dash marks a letter that has no partner. The linear rule charges a fixed price for each dash. It does not matter where the dash is or whether other dashes stand next to it.

This makes the score easy to compute. Each column of the alignment gets its own score, and the total is the sum of the columns. A program fills one table, one cell at a time, and each cell looks only at three neighbours.

The price for this simplicity is biological. One insertion of ten letters is a single event, but the linear rule charges it like ten separate events. So the rule has no reason to keep dashes together, and the best alignment often scatters them in many short gaps.

## The idea

**Definition.** For $d > 0$, the linear gap penalty is $g(L) = dL$. With a [scoring matrix](/scoring-matrix/) $s$, the score of an alignment $A$ of $x = x_1 \cdots x_m$ and $y = y_1 \cdots y_n$ is

$$S(A) = \sum_{\text{pair columns } (a, b)} s(a, b) \; - \; d \cdot (\text{number of spaces in } A).$$

It is the [affine gap penalty](/affine-gap-penalty/) $g(L) = d + (L-1)e$ with $e = d$.

**The score is column additive.** Give each column a score: $s(a, b)$ for a pair column and $-d$ for a column with a space. Then $S(A)$ is the sum of the column scores, and the score of a column does not depend on its neighbours. No other gap model has this property, because any other $g$ makes the cost of a space depend on whether the column before it also has a space in the same row.

**One table.** Let $H(i, j)$ be the best score of an alignment of $x_1 \cdots x_i$ with $y_1 \cdots y_j$. The last column is a pair, a space in $y$, or a space in $x$, so

$$H(i, j) = \max\bigl\{ H(i-1, j-1) + s(x_i, y_j),\ H(i-1, j) - d,\ H(i, j-1) - d \bigr\},$$

with $H(0, 0) = 0$, $H(i, 0) = -id$ and $H(0, j) = -jd$. This is the [Needleman-Wunsch](/needleman-wunsch/) recurrence. It fills $(m+1)(n+1)$ cells in constant time each, so it runs in $O(mn)$ time. The score alone needs only two rows, $O(n)$ space, and the [Hirschberg algorithm](/hirschberg-algorithm/) also recovers the alignment in linear space. For a general gap function $g$ the same idea needs $O(mn(m+n))$ time; see [gap penalty](/gap-penalty/).

**Only one parameter is free in global alignment.** Every global alignment of $x$ and $y$ with $c$ pair columns and $r$ spaces has $2c + r = m + n$, because each pair column uses one letter from each sequence and each space column uses one letter. Replace $s(a, b)$ by $s(a, b) + 2k$ and $d$ by $d - k$ for a constant $k$. Then the score of every alignment changes by $2kc + kr = k(m + n)$, the same amount for all alignments, so the optimal alignments do not change. Multiplying $s$ and $d$ by a positive constant also keeps the optimal alignments. The matrix and the gap penalty are therefore not independent: only their relative values matter. [Local alignment](/local-alignment/) does not have this invariance, because its alignments cover substrings of different lengths.

## Examples

**Edit distance is a linear gap score.** Take match score $+2$, mismatch score $-1$ and $d = 2$. Shift with $k = -1$: match $0$, mismatch $-3$, $d = 3$. Divide by 3: match $0$, mismatch $-1$, $d = 1$. The last score is minus the Levenshtein [edit distance](/edit-distance/). So for every pair of sequences, the best score under the first scheme is $(m + n) - 3\,\mathrm{ED}(x, y)$. For $x = \texttt{ACGTTA}$ and $y = \texttt{ACTA}$, $\mathrm{ED} = 2$, and the best score is $10 - 6 = 4$, the value found on the [gap penalty](/gap-penalty/) page.

**Three classic measures.** One table, three choices of scores:

| match | mismatch | $d$ | best score | for $\texttt{kitten}$ and $\texttt{sitting}$ |
|---|---|---|---|---|
| $1$ | $0$ | $0$ | length of a [longest common subsequence](/longest-common-subsequence/) | $4$ ($\texttt{ittn}$) |
| $0$ | not allowed | $1$ | minus the insertion and deletion distance | $-5 = -(6 + 7 - 2 \cdot 4)$ |
| $0$ | $-1$ | $1$ | minus the Levenshtein distance | $-3$ |

**Scattered gaps.** Align $x = \texttt{CATGCAG}$ with $y = \texttt{CTCACG}$, match $+2$, mismatch $-1$. With the linear penalty $d = 2$, the only optimal alignment is

```
CATGCA-G
C-T-CACG
```

with five matches and three gaps of length 1: $10 - 6 = 4$. With the affine penalty $d = 4$, $e = 1$, this alignment scores $10 - 12 = -2$. The affine optimum is

```
CATGCAG
C-TCACG
```

with one gap and three mismatches: $2 + 2 - 1 - 1 - 1 + 2 - 4 = -1$. The linear penalty prefers three short gaps to three mismatches; the affine penalty makes each extra gap opening expensive.

## Where it is used

- Edit distance, the [longest common subsequence](/longest-common-subsequence/) and the [Wagner-Fischer algorithm](/wagner-fischer-algorithm/) are all linear gap models with unit or zero costs.
- Textbook presentations of [Needleman-Wunsch](/needleman-wunsch/), [Smith-Waterman](/smith-waterman/) and the [Hirschberg algorithm](/hirschberg-algorithm/) use the linear penalty first, because the recurrence has one table.
- Fast exact methods for edit distance, such as the [Landau-Vishkin algorithm](/landau-vishkin-algorithm/) and the [Myers bit-parallel algorithm](/myers-bit-parallel-algorithm/), depend on unit costs and so on a linear gap penalty.
- Protein and DNA search tools seldom use it. They use the [affine gap penalty](/affine-gap-penalty/), and the [Gotoh algorithm](/gotoh-algorithm/) keeps the $O(mn)$ time.

## References
