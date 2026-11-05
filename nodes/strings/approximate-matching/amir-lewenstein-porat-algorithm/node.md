---
tag: EGHY1F
kind: algorithm
slug: amir-lewenstein-porat-algorithm
name: Amir-Lewenstein-Porat algorithm
aliases:
- Amir-Lewenstein-Porat k-mismatch
area: strings/approximate-matching
level: research
summary: Solves k-mismatch matching in O(n (k log k)^(1/2)) time by treating frequent and rare pattern symbols differently.
solves: [k-mismatch-problem]
model: word-ram
complexity:
  vars: {m: the pattern length, n: the text length, k: the mismatch bound}
  time: {worst: "O(n + n (k log m)^(1/2))"}
  space: {extra: O(n + m)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2000
  people: [Amihood Amir, Moshe Lewenstein, Ely Porat]
  note: Amir, Lewenstein and Porat presented the algorithm at SODA 2000, with the journal version in the Journal of Algorithms in 2004. It was faster than both the O(nk) method and Abrahamson's O(n (m log m)^(1/2)) method.
prereqs: [k-mismatch-problem, longest-common-extension-query, fast-fourier-transform]
see_also: [fischer-paterson-algorithm, hamming-string-matching, landau-vishkin-algorithm, number-theoretic-transform, convolution, suffix-tree, bitap-algorithm, pigeonhole-filtering]
sources:
  - paper: doi:10.1016/S0196-6774(03)00097-X
    title: Amihood Amir, Moshe Lewenstein and Ely Porat, Faster algorithms for string matching with k mismatches, Journal of Algorithms 50(2), 2004
    locator: pages 257 to 275 (the O(n (k log k)^(1/2)) algorithm with frequent and rare symbols, marks and verification, and the O((n + n k^3 / m) log k) algorithm for periodic and aperiodic patterns)
  - paper: doi:10.1137/0216067
    title: Karl Abrahamson, Generalized string matching, SIAM Journal on Computing 16(6), 1987
    locator: pages 1039 to 1051 (the split of the symbols into frequent ones, handled by convolution, and rare ones, handled by counting)
  - paper: doi:10.1016/0304-3975(86)90178-7
    title: Gad M. Landau and Uzi Vishkin, Efficient string matching with k mismatches, Theoretical Computer Science 43, 1986
    locator: pages 239 to 249 (the check of one alignment with at most k + 1 constant-time longest common extensions)
  - paper: "Raphaël Clifford, Allyx Fontaine, Ely Porat, Benjamin Sach and Tatiana Starikovskaya, The k-mismatch problem revisited, Proceedings of the 27th ACM-SIAM Symposium on Discrete Algorithms (SODA), 2016, arXiv:1508.00731"
    locator: Section 1 (the history of the k-mismatch bounds and the O(n k^2 log k / m + n polylog m) algorithm)
  - paper: "Panagiotis Charalampopoulos, Tomasz Kociumaka and Philip Wellnitz, Faster approximate pattern matching: a unified approach, Proceedings of the 61st IEEE Symposium on Foundations of Computer Science (FOCS), 2020, arXiv:2004.08350"
    locator: Section 1, Hamming distance (the later bounds, up to the O~(n + k n / m^(1/2)) algorithm of Gawrychowski and Uznanski)
---

The Amir-Lewenstein-Porat algorithm solves the [k-mismatch problem](/k-mismatch-problem/): it finds every alignment of a pattern of length $m$ in a text of length $n$ with at most $k$ mismatched symbols. It sorts the symbols of the pattern into frequent and rare ones. If many symbols are frequent, a few marked positions of the pattern rule out most alignments, and the rest are checked with [longest common extensions](/longest-common-extension-query/). If few symbols are frequent, one [convolution](/convolution/) per frequent symbol and direct counting for the rare ones give every distance. The time is $O(n \sqrt{k \log m})$, and with a second algorithm of the same paper, $O(n \sqrt{k \log k})$.

## In plain words

Slide the pattern along the text, count the differing letters at each position, and report the positions with at most the allowed number.

Two older methods each win in one setting. One checks a position by jumps: it stops after one difference too many, so it is fast when few differences are allowed. The other counts, for each letter, the agreements at all positions at once with a fast multiplication, so it is fast when the pattern uses few letters.

This algorithm looks at how often each letter occurs in the pattern. If many letters occur often, it marks a few copies of them. A position that agrees with too few marks cannot be good, so only a small number of positions remain for the jump check. If only a few letters occur often, it multiplies for those letters and counts the rare ones by hand.

## The problem

The input is a pattern $P = P[0 \ldots m-1]$, a text $T = T[0 \ldots n-1]$ over an alphabet $\Sigma$, and an integer $k \ge 0$. Indices are 0-based. The edit model is the [Hamming distance](/hamming-distance/): substitutions only, with unit cost, so the pattern is compared with windows of exactly $m$ symbols. For a start $i$ with $0 \le i \le n - m$, let

$$ h_i = \bigl| \{\, q \in \{0, \ldots, m-1\} : P[q] \ne T[i + q] \,\} \bigr|. $$

The output is the sorted list of start positions $i$ with $h_i \le k$. If $m > n$ it is empty, and if $k \ge m$ it holds every $i$ in $0, \ldots, n - m$.

For the algorithm, let $\lambda = \lceil \log_2 m \rceil$, and let

$$ f = \max\bigl(1, \lceil \sqrt{k \lambda}\, \rceil\bigr), \qquad g = \lceil 2k / f \rceil. $$

A symbol is **frequent** if it occurs at least $f$ times in $P$, and **rare** otherwise. Let $F$ be the set of frequent symbols.

## The algorithm

```pseudo id=main
ALP-K-MISMATCH(P, T, k)
L1  if k ≥ m then return 0, 1, …, n − m
L2  compute f, g and the set F of frequent symbols
L3  if |F| ≥ g then                              ▷ case A: many frequent symbols
L4      marks ← f positions of each of g symbols of F   ▷ g·f ≥ 2k marks
L5      for each j and each mark q with P[q] = T[j] and 0 ≤ j − q ≤ n − m: count[j − q] += 1
L6      return the i with count[i] ≥ g·f − k for which KANGAROO(i) succeeds
L7  match[0 … n − m] ← 0                          ▷ case B: fewer than g frequent symbols
L8  for each c in F: add the correlation of the positions of c in P and in T to match
L9  for each j with T[j] rare and each q with P[q] = T[j] and 0 ≤ j − q ≤ n − m: match[j − q] += 1
L10 return the i with m − match[i] ≤ k
```

**KANGAROO(i)** checks one alignment. Start with $q = 0$ and $e = 0$. While $q < m$: add to $q$ the length of the longest common prefix of $P[q \ldots]$ and $T[i + q \ldots]$; if now $q < m$, the symbols at $q$ differ, so add 1 to $e$, fail if $e > k$, and add 1 to $q$. Succeed when $q = m$. Each longest common extension takes $O(1)$ time with a [suffix tree](/suffix-tree/) of $P$ and $T$ and [lowest common ancestor](/lowest-common-ancestor/) queries, and the check makes at most $k + 1$ of them.

**Line L8** computes, for every $i$, the number of $q$ with $P[q] = T[i + q] = c$. This is a correlation of two 0-1 vectors. Cut $T$ into blocks of length $2m - 1$ that start at multiples of $m$, and correlate $P$ with each block by a [fast Fourier transform](/fast-fourier-transform/), or exactly with a [number-theoretic transform](/number-theoretic-transform/), in $O(m \log m)$ time. There are about $n / m$ blocks, so one symbol costs $O(n \log m)$.

## Example

**Case A.** Let $P = \texttt{ACGTA}$, $T = \texttt{ACGAAACGTTACCTA}$ and $k = 1$. Then $m = 5$, $\lambda = 3$, $f = \lceil \sqrt 3 \rceil = 2$ and $g = 1$. The only frequent symbol is A, with 2 occurrences, so $|F| = 1 \ge g$. The marks are the positions 0 and 4 of $P$, and an alignment needs $count[i] \ge 2 - 1 = 1$.

| $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $count[i]$ | 2 | 1 | 0 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 2 |
| candidate | yes | yes | | yes | yes | yes | yes | | | | yes |
| $h_i$ | 1 | 4 | 5 | 4 | 4 | 1 | 3 | 5 | 5 | 5 | 1 |
| KANGAROO | yes | no | | no | no | yes | no | | | | yes |

Seven of the eleven alignments are candidates. At $i = 1$, $P = \texttt{ACGTA}$ meets $\texttt{CGAAA}$: the first extension has length 0, so $e = 1$, and the second also has length 0, so $e = 2 > k$ and the check fails after two queries. The output is $0, 5, 10$.

**Case B.** Let $P = \texttt{AACAGTA}$, $T = \texttt{CAACAGTAAGCAGTAACATTA}$ and $k = 3$. Then $m = 7$, $\lambda = 3$, $f = 3$ and $g = 2$. Only A is frequent (4 occurrences), so $|F| = 1 < g$. One correlation gives the agreements on A, and counting gives those on C, G and T:

| $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| agreements on A | 1 | 4 | 2 | 1 | 2 | 2 | 1 | 2 | 3 | 1 | 1 | 3 | 1 | 1 | 4 |
| agreements on C, G, T | 0 | 3 | 0 | 0 | 0 | 1 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 1 | 2 |
| $h_i$ | 6 | 0 | 5 | 6 | 5 | 4 | 6 | 5 | 1 | 6 | 6 | 4 | 6 | 5 | 1 |

The output is $1, 8, 14$.

## Correctness

In case B the algorithm computes every $h_i$ exactly: each pair $(q, i)$ with $P[q] = T[i + q]$ is counted once, by line L8 if the symbol is frequent and by line L9 if it is rare, so $match[i] = m - h_i$. In case A, line L6 is a filter followed by an exact check. The marks are $g f \ge 2k$ positions of $P$. If $h_i \le k$, at most $k$ marks are mismatched at $i$, so $count[i] \ge g f - k$, and the filter keeps $i$. KANGAROO counts the mismatches from left to right, one per extension, so it succeeds exactly when $h_i \le k$. The [full proof](proofs/correctness.md) gives the details.

## Complexity

Assume $1 \le k < m \le n$; the other cases end at line L1 or give an empty output.

- **Case A.** For each text position $j$, line L5 visits the $f$ marks of the symbol $T[j]$ if it is marked, and nothing otherwise, so it makes at most $n f$ increments. A candidate has $count[i] \ge g f - k \ge k$, so there are at most $n f / k$ candidates, and each check costs $O(k + 1)$. The total is $O(n f)$.
- **Case B.** There are $|F| \le g - 1 < 2k / f$ convolutions, $O(n \log m)$ each, and each text symbol meets fewer than $f$ positions of a rare symbol in line L9. The total is $O(n k \lambda / f + n f)$.

With $f = \lceil \sqrt{k \lambda} \rceil$, both totals are $O(n + n \sqrt{k \log m})$ in the worst case on the word RAM. For $k = 0$, $g = 0$, every alignment is a candidate, and the checks take $O(n)$. The longest common extension structure takes $O(n + m)$ time for an integer alphabet of size polynomial in $n$, and the extra space is $O(n + m)$.

**From $\log m$ to $\log k$.** The same paper gives a second algorithm, for periodic and aperiodic patterns, that runs in $O((n + n k^3 / m) \log k)$ time. If $k^3 \le m$, it takes $O(n \log k)$ time. If $k^3 > m$, then $\log m < 3 \log k$. Choosing by this test gives $O(n \sqrt{k \log k})$ for $k \ge 2$.

## Properties

- **Exact and deterministic.** It reports exactly the alignments with $h_i \le k$, with no randomness, when the convolutions are exact.
- **A threshold, not all distances.** Case A gives $h_i$ only for the alignments that it checks. Computing every $h_i$ is [Hamming string matching](/hamming-string-matching/), where Abrahamson's $O(n \sqrt{m \log m})$ is the classic bound.
- **Offline.** It needs the whole pattern first to count the symbols. Case A reads the text in one pass, but the checks need the longest common extension structure of the text.
- **Independent of the alphabet size.** Only the frequent symbols get convolutions, so a large alphabet costs no more.

## Variants and improvements

- **Abrahamson's method.** With threshold $\sqrt{m / \log m}$ instead of a threshold based on $k$, the frequent and rare split alone gives every $h_i$ in $O(n \sqrt{m \log m})$ time. This page uses the same split, and adds the marks for case A.
- **Long patterns.** For $k$ much smaller than $m$, later algorithms use the structure of the pattern: Clifford, Fontaine, Porat, Sach and Starikovskaya reach $O(n k^2 \log k / m + n\, \mathrm{polylog}\, m)$, and Gawrychowski and Uznanski $\tilde O(n + k n / \sqrt{m})$.
- **Approximate counts.** Karloff's method estimates every $h_i$ within a factor $1 + \varepsilon$ with random projections to a few symbols.
- **Wildcards.** Don't care symbols fit the convolution part with one more product, but they break the longest common extension check.

## When to use it

Use it for exact k-mismatch matching when $k$ is moderate: large enough that the $O(nk)$ [Landau-Vishkin](/landau-vishkin-algorithm/) method is slow, and small compared with $m$, so that $\sqrt{k \log m}$ is far below $\sqrt{m \log m}$. For small $k$ and short patterns, the [bitap algorithm](/bitap-algorithm/) or the $O(nk)$ method is simpler. For all distances, use [convolutions](/fischer-paterson-algorithm/) or Abrahamson's method.

## Pitfalls

- **Marks of the same symbol.** All $f$ marks of one symbol must be distinct positions of $P$, and the $g$ symbols distinct, or the bound on the increments of line L5 fails.
- **Too many marks.** Using every occurrence of the frequent symbols as a mark keeps the filter correct but breaks the bound of $n f$ increments, since one symbol can fill the whole pattern.
- **Exact convolutions.** Floating-point FFT counts must be rounded to the nearest integer. A number-theoretic transform modulo a prime above $m$ avoids rounding.
- **Edges.** For $k \ge m$ every alignment matches, and $\lambda = 0$ when $m = 1$, so $f$ needs the floor of 1.

## Implementations

## History

Abrahamson (1987) and Kosaraju solved Hamming string matching in $O(n \sqrt{m \log m})$ time with the split of the symbols into frequent and rare ones, and Landau and Vishkin (1986) solved the k-mismatch problem in $O(nk)$ time with longest common extensions. Amir, Lewenstein and Porat combined the two ideas and presented the $O(n \sqrt{k \log k})$ algorithm at SODA 2000, with the journal version in 2004. The bound for long patterns was later improved by Clifford, Fontaine, Porat, Sach and Starikovskaya (2016) and by Gawrychowski and Uznanski (2018).

## References
