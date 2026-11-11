---
tag: H8NZFT
kind: problem
slug: longest-previous-factor
name: Longest previous factor
aliases:
- LPF array
- longest previous factor problem
area: compression-and-coding/dictionary-compression
level: advanced
summary: For each position i of a string, find the longest prefix of the suffix at i that also starts at an earlier position. Solvable in O(n) from the suffix array.
prereqs: [suffix-array, lcp-array, monotonic-stack]
see_also: [lempel-ziv-factorization, match-finding, greedy-parsing, kasai-algorithm, sa-is, maximal-repetition, string-attractor, lz77]
sources:
  - paper: doi:10.1016/j.ipl.2007.10.006
    title: Maxime Crochemore and Lucian Ilie, Computing Longest Previous Factor in linear time and applications, Information Processing Letters 106(2), 75-80, 2008
    locator: "Section 2 (the definition of LPF and PrevOcc), Section 3 (LPF from the suffix array and the LCP array through the previous and next smaller values, in linear time) and Section 4 (the Lempel-Ziv factorization and other applications)"
  - paper: doi:10.1007/3-540-48194-X_17
    title: Toru Kasai, Gunho Lee, Hiroki Arimura, Setsuo Arikawa and Kunsoo Park, Linear-time longest-common-prefix computation in suffix arrays and its applications, CPM 2001, LNCS 2089, 181-192
    locator: the linear-time computation of the LCP array from the suffix array
  - paper: "Michael Rodeh, Vaughan R. Pratt and Shimon Even, Linear algorithm for data compression via string matching, Journal of the ACM 28(1), 16-24, 1981"
    locator: the longest earlier match at each position from a suffix tree, in linear time for a fixed alphabet
  - paper: "Roman Kolpakov and Gregory Kucherov, Finding maximal repetitions in a word in linear time, Proceedings of the 40th IEEE Symposium on Foundations of Computer Science (FOCS 1999), 596-604"
    locator: the use of the Lempel-Ziv factorization (s-factorization) to find all maximal repetitions
---

The longest previous factor problem asks, for each position $i$ of a string $t$, for the length $\mathrm{LPF}[i]$ of the longest prefix of $t[i \ldots n-1]$ that also occurs at some earlier position $j < i$, and for one such $j$. The two occurrences may overlap. Crochemore and Ilie (2008) compute the whole array in $O(n)$ time from the [suffix array](/suffix-array/) and the [LCP array](/lcp-array/). The array gives the [Lempel-Ziv factorization](/lempel-ziv-factorization/) of $t$ at once, and it is the exact answer that a [match finder](/match-finding/) for LZ77 with an unbounded window tries to approximate.

## In plain words

Read a text from left to right. At each letter, ask: how much of the text from here on did I already see, starting somewhere before? The answer is a number for each letter. It is zero when the letter is new, and it is large in a part of the text that repeats an earlier part.

A compressor wants exactly this number, because a long earlier copy means a cheap "copy from back there". To compute it for all letters at once, sort all the endings of the text in dictionary order. An ending shares the most with its neighbours in that order. So for each ending, the best earlier ending is the nearest neighbour above or below it in the sorted list that starts earlier in the text.

## Definition

**Input.** A string $t = t[0 \ldots n-1]$ over an ordered alphabet $\Sigma$ of size $\sigma$.

**Output.** The arrays $\mathrm{LPF}[0 \ldots n-1]$ and $\mathrm{PrevOcc}[0 \ldots n-1]$, where
$$\mathrm{LPF}[i] = \max\{\, \ell \ge 0 : t[j \ldots j+\ell-1] = t[i \ldots i+\ell-1] \text{ for some } j < i \,\},$$
and $\mathrm{PrevOcc}[i]$ is a position $j < i$ that reaches this maximum, or $-1$ when $\mathrm{LPF}[i] = 0$. Here $\mathrm{LPF}[i] = \max_{j < i} \mathrm{lcp}(t[j \ldots], t[i \ldots])$, where lcp is the length of the longest common prefix. $\mathrm{LPF}[0] = 0$, and $\mathrm{LPF}[i] = 0$ exactly when $t[i]$ does not occur before $i$.

**The Lempel-Ziv factorization.** Cut $t$ from the left: at position $i$, the next factor has length $\max(1, \mathrm{LPF}[i])$. It is a copy of the earlier occurrence, or a new symbol. This is the greedy LZ77 parse with an unbounded window and no explicit symbol after a copy, and by the argument on the [greedy parsing](/greedy-parsing/) page it has the fewest factors among all parses into earlier factors and single symbols. The page [Lempel-Ziv factorization](/lempel-ziv-factorization/) covers the factorization itself; this page is about the array.

**The key lemma.** Let $SA$ be the suffix array, $i = SA[r]$, and let $\mathrm{lcp}(s, r)$ be the lcp of the suffixes of rank $s$ and $r$. For ranks $s < s' < r$ we have $\mathrm{lcp}(s, r) \le \mathrm{lcp}(s', r)$, because $\mathrm{lcp}(s, r) = \min(\mathrm{LCP}[s+1], \ldots, \mathrm{LCP}[r])$ and the range for $s'$ is a part of the range for $s$. The same holds above $r$. So among the suffixes that start before $i$, the best one is the nearest rank below $r$ with $SA$ value less than $i$ (the *previous smaller value*) or the nearest rank above $r$ with $SA$ value less than $i$ (the *next smaller value*):
$$\mathrm{LPF}[i] = \max\big(\mathrm{lcp}(\mathrm{PSV}(r), r),\ \mathrm{lcp}(r, \mathrm{NSV}(r))\big),$$
with the lcp taken as 0 when a neighbour does not exist.

## Variants

- **The window.** Only $j \ge i - w$ counts. This is what an LZ77 encoder with a window $w$ needs. The two-neighbour lemma no longer applies, because the nearest suffix in the window can be far away in suffix array order.
- **No overlap.** Require $j + \ell \le i$, so that the earlier occurrence ends before $i$. This fits formats whose decoders cannot copy from the text being written.
- **The factorization only.** Some algorithms compute the factors without the full array, for example with an FM index or by working on blocks of the text, to save memory.
- **Bounded length.** Cap $\ell$ at $\ell_{\max}$, as real formats do. This is $\min(\mathrm{LPF}[i], \ell_{\max})$, but the minimum distance for the capped length may differ.

## Examples

Let $t$ = `abbaabbbaaabab` ($n = 14$). Its suffix array and LCP array are:

| Rank $r$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $SA[r]$ | 8 | 9 | 3 | 12 | 10 | 0 | 4 | 13 | 7 | 2 | 11 | 6 | 1 | 5 |
| $\mathrm{LCP}[r]$ | 0 | 2 | 3 | 1 | 2 | 2 | 3 | 0 | 1 | 3 | 2 | 1 | 4 | 2 |

The result is:

| $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $t[i]$ | a | b | b | a | a | b | b | b | a | a | a | b | a | b |
| $\mathrm{LPF}[i]$ | 0 | 0 | 1 | 1 | 3 | 2 | 4 | 3 | 2 | 3 | 2 | 2 | 2 | 1 |
| $\mathrm{PrevOcc}[i]$ | $-1$ | $-1$ | 1 | 0 | 0 | 1 | 1 | 2 | 3 | 3 | 0 | 2 | 10 | 7 |

For $i = 6$ (the suffix `bbaaabab`, rank 11), the previous smaller value is rank 9 (start 2), with lcp $\min(\mathrm{LCP}[10], \mathrm{LCP}[11]) = 1$, and the next smaller value is rank 12 (start 1), with lcp $\mathrm{LCP}[12] = 4$. So $\mathrm{LPF}[6] = 4$ and $\mathrm{PrevOcc}[6] = 1$: `bbaa` occurs at 1 and at 6.

The Lempel-Ziv factorization reads the array from position 0: `a` | `b` | `b` | `a` | `abb` | `baa` | `ab` | `ab`, 8 factors. The factor `abb` at 4 copies position 0, `baa` at 7 copies position 2, and the last `ab` at 12 copies position 10. The tests check every value in the two tables.

## Known algorithms

**Brute force.** Compare $t[i \ldots]$ with each earlier suffix. This takes $O(n^3)$ symbol comparisons in the worst case, or $O(n^2)$ with the [Z-algorithm](/z-algorithm/) run on each suffix. The tests use the cubic version as the oracle.

**Suffix tree.** Store at each node of the [suffix tree](/suffix-tree/) the smallest start of a leaf below it. Then $\mathrm{LPF}[i]$ is the depth of the deepest ancestor of leaf $i$ whose smallest start is less than $i$. Rodeh, Pratt and Even (1981) used a suffix tree to find the longest earlier match at each position in linear time for a fixed alphabet.

**Suffix array and LCP array (Crochemore and Ilie).** Build $SA$ (in $O(n)$ time for an integer alphabet with [SA-IS](/sa-is/)), then the LCP array with [Kasai's algorithm](/kasai-algorithm/). Then one pass over the ranks with a [monotonic stack](/monotonic-stack/) finds, for each rank, its previous and next smaller values and the two lcp values. The stack holds ranks with increasing $SA$ values, each with its lcp to the rank below it. A sentinel rank $n$ with $SA[n] = -1$ empties the stack at the end.

```pseudo id=main
LPF(t)
L1  build SA and LCP of t; SA[n] ← −1; LCP[n] ← 0            ▷ sentinel rank n
L2  S ← empty stack of pairs (rank, lcp with the rank below it)
L3  for r ← 0 to n do
L4      h ← LCP[r]                                         ▷ lcp of rank r with the top of S
L5      while S is not empty and SA[top(S)] > SA[r] do
L6          (q, left) ← pop(S)                             ▷ r is the next smaller value of q
L7          LPF[SA[q]] ← max(left, h); PrevOcc[SA[q]] ← the start on the side of the maximum
L8          h ← min(left, h)                               ▷ lcp of rank r with the new top
L9      if r < n then push (r, h) on S, with h ← 0 if S is empty
L10 return LPF and PrevOcc
```

*Why it is correct.* Invariant: before step $r$, the stack holds, from the bottom, the ranks $q < r$ that have no smaller $SA$ value at a rank in $(q, r)$, in increasing order of $SA$, and the value stored with $q$ is its lcp with the rank below it in the stack, which is its previous smaller value. At line L4, $h$ is the lcp of rank $r$ with the top, because the top is rank $r - 1$. When $q$ is popped, $SA[r] < SA[q]$ and no rank between has a smaller value, so $r$ is the next smaller value of $q$, and $h = \mathrm{lcp}(q, r)$; the key lemma gives line L7. Line L8 keeps $h$ equal to the lcp of $r$ with the next top, by $\mathrm{lcp}(q', r) = \min(\mathrm{lcp}(q', q), \mathrm{lcp}(q, r))$ for $q' < q < r$. The sentinel has the smallest value, so every rank is popped once.

*Cost.* Each rank is pushed and popped once, so the pass takes $O(n)$ time and $O(n)$ words of space on top of $SA$ and LCP. The implementation builds $SA$ by prefix doubling in $O(n \log^2 n)$ time, so its total is $O(n \log^2 n)$; with SA-IS the total is $O(n)$.

## Bounds

- $\Omega(n)$ time, to read the input.
- In the comparison model, $\Omega(n \log n)$ comparisons: $\mathrm{LPF}$ is all zeros exactly when all symbols of $t$ are distinct, so the problem solves [element distinctness](/element-distinctness/), which needs $\Omega(n \log n)$ in the algebraic decision tree model ([element distinctness lower bound](/element-distinctness-lower-bound/)). A comparison-based suffix sort meets this bound.
- $O(n)$ time for an integer alphabet $\{0, \ldots, n^{O(1)}\}$, by SA-IS and the stack pass.

## Reductions

- **LPF to the LZ factorization.** Given LPF and PrevOcc, the factorization takes $O(z)$ steps, where $z$ is the number of factors: each step reads one entry and jumps.
- **Previous and next smaller values.** The core of the method is the all nearest smaller values problem on the $SA$ array, solved with a stack, and range minima on the LCP array; see [range minimum query](/range-minimum-query/) and [LCP and RMQ](/lcp-rmq-reduction/) for the general tool.
- **Element distinctness.** It reduces to LPF, as in the bounds above.

## Applications

- **Compression.** The LZ factorization gives an exact LZ77 parse with an unbounded window, and LPF gives the longest match for a [match finder](/match-finding/) or an [optimal LZ parser](/optimal-lz-parsing/) in offline use.
- **Repetitions.** Kolpakov and Kucherov find all [maximal repetitions](/maximal-repetition/) (runs) of a string in linear time with the help of its Lempel-Ziv factorization.
- **Repetitive text indexes.** The number of LZ factors $z$ is a measure of repetitiveness, related to the size of the smallest [string attractor](/string-attractor/), and indexes such as the [LZ-index](/lz-index/) are built on the factorization.

## References
