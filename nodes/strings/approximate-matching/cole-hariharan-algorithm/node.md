---
tag: 5Z7RCS
kind: algorithm
slug: cole-hariharan-algorithm
name: Cole-Hariharan algorithm
aliases:
- Cole-Hariharan k-differences
area: strings/approximate-matching
level: research
summary: Finds all k-differences matches in O(n + m + n k^4 / m) time, which is linear when the pattern is at least k^4 long.
solves: [k-differences-problem, approximate-string-matching]
model: word-ram
complexity:
  vars: {m: the pattern length, n: the text length, k: the error bound}
  time: {worst: O(n + m + n k^4 / m), best: O(n + m)}
  space: {extra: O(n + m)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1998
  people: [Richard Cole, Ramesh Hariharan]
  note: Cole and Hariharan presented the algorithm at SODA 1998, with the journal version in the SIAM Journal on Computing in 2002.
prereqs: [k-differences-problem, landau-vishkin-algorithm, string-period, aho-corasick]
see_also: [galil-park-algorithm, chang-lawler-algorithm, pigeonhole-filtering, amir-lewenstein-porat-algorithm, longest-common-extension-query, suffix-tree, periodicity-detection, edit-distance-hardness]
sources:
  - paper: doi:10.1137/S0097539700370527
    title: Richard Cole and Ramesh Hariharan, Approximate string matching, a simpler faster algorithm, SIAM Journal on Computing 31(6), 2002, 1761-1782
    locator: the sparsification with 2k aperiodic breaks of length k^2, the verification of a text window by Landau-Vishkin on a band of diagonals, and the O(k^4) procedure for mostly periodic patterns and texts
  - paper: "Richard Cole and Ramesh Hariharan, Approximate string matching: a simpler faster algorithm, Proceedings of the 9th ACM-SIAM Symposium on Discrete Algorithms (SODA), 1998, 463-472"
    locator: the conference version, with the bounds O(n + m + n k^3 / m) for patterns that are not mostly periodic and O(n + m + n k^4 / m) for the others
  - paper: "Gad M. Landau and Uzi Vishkin, Fast parallel and serial approximate string matching, Journal of Algorithms 10(2), 1989, pages 157 to 169"
    locator: the O(kn) diagonal method with constant-time longest common extensions, which the algorithm runs on few diagonals
  - paper: doi:10.1145/375360.375365
    title: Gonzalo Navarro, A guided tour to approximate string matching, ACM Computing Surveys 33(1), 2001
    locator: the part on worst-case improvements of the dynamic programming algorithms, which lists the Cole-Hariharan bound
---

The Cole-Hariharan algorithm solves the [k-differences problem](/k-differences-problem/) in $O(n + m + n k^4 / m)$ time, which is linear in the text length when the pattern is at least $k^4$ long. It picks $2k$ disjoint aperiodic pieces of length $k^2$ in the pattern, the breaks. At least $k$ breaks survive any match without an error, so an exact search for the breaks leaves few places where a match can start, and the [Landau-Vishkin algorithm](/landau-vishkin-algorithm/) checks only those places. Patterns without $2k$ such breaks are almost periodic, and a separate procedure uses that structure.

## In plain words

Take a long pattern and allow only a few errors. Most of the pattern must then appear in the text exactly. Cut a number of short pieces from the pattern, twice as many as the allowed errors. Each error can spoil at most one piece, so in any match at least half of the pieces appear exactly, and they appear about where they sit in the pattern.

So find all exact copies of the pieces in the text first. Each copy votes for the few starting places it fits. A starting place needs votes from at least half the pieces, and only those places get the slow, exact check.

The pieces are chosen so that copies of one piece cannot crowd together, which keeps the votes and checks few. When the pattern is too repetitive to give such pieces, it is nearly periodic, and a different method handles it.

## The problem

The input is a pattern $P = P[0 \ldots m-1]$, a text $T = T[0 \ldots n-1]$ and an integer $k \ge 0$. Indices are 0-based. The edit model is Levenshtein: insertions, deletions and substitutions of single symbols, each of cost 1, with no transpositions, and $\mathrm{ed}$ is the distance. Following the paper, the output is the sorted list of **start positions** $s \in \{0, \ldots, n\}$ such that $\mathrm{ed}(P, T[s \ldots j)) \le k$ for some $j \ge s$. The start positions of $P$ in $T$ are the end positions of the reversed pattern in the reversed text, at $n - s$, so the same method reports end positions.

**Periods and breaks.** The period of a nonempty string $x$ is the least $p \ge 1$ with $x[i] = x[i + p]$ for all $i$ with $i + p < |x|$. The string is **aperiodic** if its period is more than $|x|/2$; see [string period](/string-period/). Two occurrences of an aperiodic string $x$ in a text are more than $|x|/2$ apart, since two occurrences at distance $\delta \le |x|/2$ would give $x$ the period $\delta$. A **break** is one of $2k$ disjoint aperiodic substrings $P[o_b \ldots o_b + k^2)$ of the pattern, for $b = 0, \ldots, 2k-1$, at offsets $o_0 < o_1 < \cdots$. The pattern is **mostly periodic** if it has no $2k$ such substrings.

**Windows.** For $k \ge 1$, window $w$ is the set of start positions $\{wk, \ldots, wk + k - 1\} \cap \{0, \ldots, n\}$, for $0 \le w \le \lfloor n/k \rfloor$.

## The algorithm

```pseudo id=main
COLE-HARIHARAN(P, T, k)
L1  B ← up to 2k disjoint aperiodic substrings of P of length k², by a greedy scan (none if k = 0)
L2  if |B| < 2k then
L3      return the starts found by the mostly periodic procedure (in the code: Landau-Vishkin on all diagonals)
L4  find all exact occurrences of the breaks in T with the Aho-Corasick automaton
L5  for each break b at offset o and each occurrence q of it: mark with b each window that meets [q − o − k, q − o + k]
L6  C ← the windows marked by at least k distinct breaks
L7  for each window w in C: find its starts by Landau-Vishkin on the diagonals of w widened by k on each side
L8  return the sorted starts
```

**Line L1, the greedy scan.** Start at $c = 0$. Compute the period $p$ of $P[c \ldots c + k^2)$ with the failure function of the [Knuth-Morris-Pratt algorithm](/knuth-morris-pratt/). If $2p > k^2$, this substring is a break, and the scan continues at $c + k^2$. Otherwise extend to the first $i \ge c + k^2$ with $P[i] \ne P[i - p]$; the substring of length $k^2$ that ends at $i$ is aperiodic, since a string with period $p$ that loses this period at its last symbol has only aperiodic suffixes of length at least $2p$. It becomes a break, and the scan continues at $i + 1$. Each step takes the aperiodic substring that ends first, so the scan finds $2k$ breaks whenever the pattern has $2k$ disjoint aperiodic substrings of length $k^2$, in $O(m)$ time.

**Lines L5 and L6, the votes.** In a match that starts at $s$, a break that receives no error is copied exactly into the text at some position $q$, shifted from $s + o$ by the difference of the insertions and deletions before it. That difference lies between $-k$ and $k$, so $s \in [q - o - k, q - o + k]$, and the window of $s$ gets a mark from this break. Each error spoils at most one break, so at least $k$ of the $2k$ breaks are clean, and the window of $s$ is marked by at least $k$ distinct breaks.

**Line L7, the check.** The starts in a window are ends $j = n - s$ in the reversed strings, on the diagonals $d = j - m$ of the [Landau-Vishkin](/landau-vishkin-algorithm/) table. A diagonal $d$ at error level $e$ depends only on the diagonals $d - 1$, $d$ and $d + 1$ at level $e - 1$. So the values at level $k$ on the $k$ diagonals of the window come out right even when the computation sees only those diagonals and $k$ more on each side. The window then costs $O((k + 1) \cdot 3k)$ longest common extension queries.

**The mostly periodic case.** If the pattern has fewer than $2k$ breaks, the stretches between its at most $2k - 1$ aperiodic substrings of length $k^2$ have periods of at most $k^2/2$. Cole and Hariharan cut the text into pieces of length $2m - 2k$ that overlap by $m + k - 1$ symbols, so every match lies in a piece, and treat each piece as follows.

- **Trimming.** An aperiodic substring of length $k^2$ of the text, set against a stretch with period at most $k^2/2$, costs at least one error. So all matches lie in a part of the piece with at most $10k - 2$ disjoint aperiodic substrings of length $k^2$, which is found in $O(m)$ time.
- **Locked intervals.** The breaks of the pattern and of the text are grouped and widened by periodic runs of length about $k^3$ into intervals. Two periodic strings of length at least $k^3 + k^2$ whose canonical periods (least rotations of the period) differ, with periods of at most $k^2/2$, are more than $k$ apart. So in a match far from the ends of the breaks, all periodic stretches that meet the intervals share one canonical period $u$, the intervals lock to the copies of $u$, and the distance of the match is the sum of the distances of the intervals to powers of $u$. Matches near breaks begin in $O(k^2)$ windows of length $O(k^3)$. This gives $O(k^6)$ time per piece.
- **The $O(k^4)$ refinement.** A further analysis of patterns and texts that are almost a power of a single string $u$ brings the time per piece down to $O(k^4)$, after $O(m)$ preprocessing.

The implementation below runs the sparse case as written and uses the Landau-Vishkin algorithm on all diagonals for the mostly periodic case, which gives the same output in $O(k(n + m))$ time.

## Example

Let $k = 2$, so breaks have length $k^2 = 4$ and windows hold 2 starts. Let $P = \texttt{CCGTAATGCCTTTCCC}$ ($m = 16$) and

$$ T = \texttt{TAACAGAGTTTTCCGTACTGCCTTCCCTCGAATGCGTGT} \quad (n = 39). $$

The scan of line L1 finds the 4 breaks $\texttt{CCGT}$, $\texttt{AATG}$, $\texttt{CCTT}$ and $\texttt{TCCC}$ at offsets 0, 4, 8 and 12, each of period 4. Line L4 finds one occurrence of each. Line L5 marks the windows that meet the range of starts of each occurrence.

| break | offset $o$ | occurrence $q$ | starts $[q - o - 2, q - o + 2]$ | windows marked |
|---|---|---|---|---|
| CCGT | 0 | 12 | $[10, 14]$ | 5, 6, 7 |
| AATG | 4 | 30 | $[24, 28]$ | 12, 13, 14 |
| CCTT | 8 | 20 | $[10, 14]$ | 5, 6, 7 |
| TCCC | 12 | 23 | $[9, 13]$ | 4, 5, 6 |

Windows 5 and 6 get 3 marks, window 7 gets 2, and windows 4, 12, 13 and 14 get 1. Line L6 keeps windows 5, 6 and 7, the starts 10 to 15, and line L7 checks only these 6 of the 40 starts. The check finds the single start 12: $T[12 \ldots 27) = \texttt{CCGTACTGCCTTCCC}$ is $P$ with one substitution ($\texttt{A} \to \texttt{C}$ at offset 5) and one deletion (a $\texttt{T}$ of the run at offsets 10 to 12), so its distance is 2. The starts 11 and 13 have distance 3, and the occurrence of $\texttt{AATG}$ at 30 is a stray copy that no other break supports.

## Correctness

Line L7 reports only true starts, because the banded computation gives the true Landau-Vishkin values on the diagonals of the window. For the converse, fix a match that starts at $s$ and an alignment of cost at most $k$. A break is spoiled only by an error at one of its own symbols or by an inserted text symbol between two of its symbols, and different breaks own different errors, so at least $k$ breaks are clean. Each clean break occurs in $T$ at $q$ with $s \in [q - o - k, q - o + k]$, so the window of $s$ gets at least $k$ marks, and line L7 finds $s$. The mostly periodic branch and $k = 0$ run the Landau-Vishkin algorithm on all diagonals, which is exact. The [full proof](proofs/correctness.md) gives the details.

## Complexity

- **Sparse case.** The scan of line L1 takes $O(m)$ time. The breaks have total length $2k^3 \le m$, so the Aho-Corasick search takes $O(n + m)$ time. A break is aperiodic of length $k^2$, so it occurs at most $2n/k^2 + 1$ times, and all $2k$ breaks occur at most $4n/k + 2k$ times. Each occurrence marks at most 3 windows, since its range of $2k + 1$ starts meets at most 3 windows of $k$ starts. So there are at most $12 n/k + 6k$ marks and at most $12 n/k^2 + 6$ candidate windows, each checked with $O(k^2)$ extension queries. With a [suffix tree](/suffix-tree/) and [lowest common ancestor](/lowest-common-ancestor/) queries, each [longest common extension](/longest-common-extension-query/) takes $O(1)$ time, and the sparse case takes $O(n + m)$ time. The paper states the bound $O(n + m + n k^3 / m)$ for it, which is the same since $m \ge 2k^3$ here.
- **Mostly periodic case.** Each of the $O(n/m)$ pieces of the text costs $O(m)$ time for the preprocessing and $O(k^4)$ for the matches, which totals $O(n + n k^4 / m)$. The paper assumes $m \ge 5k^3$ and runs the Landau-Vishkin algorithm for shorter patterns, in $O(nk) = O(n k^4 / m)$ time. Together, the worst case is $O(n + m + n k^4 / m)$.
- **This implementation.** The suffix array with prefix doubling takes $O((n + m) \log^2 (n + m))$ time, and the fallback branch takes $O(k(n + m))$ queries. The space is $O(n + m)$ in all cases.

## Properties

- **Linear for long patterns.** When $m \ge k^4$, the time is $O(n + m)$ in the worst case, for any text. The $O(nk)$ bound of Landau-Vishkin and Galil-Park is linear only for constant $k$.
- **A filter with exact checks.** The votes never miss a match, and the banded check removes the false candidates, so the output is exact.
- **Structure, not chance.** The bounds hold for every input. The only property used is that aperiodic strings cannot occur close together, and the strings that lack this property are periodic, which the second procedure exploits.
- **Offline.** The extension queries need an index of the text and the pattern, so the text must be known in advance, or searched piece by piece.

## Variants and improvements

- **Simpler periodic cases.** The paper notes that the bounds $O(n + m + n k^6/m)$ and $O(n + m + n k^5/m)$ for mostly periodic inputs are much easier to reach than $O(n + m + n k^4/m)$. Its first procedure for these inputs is the $O(k^6)$ one above.
- **Weighted edits.** When every operation costs at least 1, the same method works with a weighted Landau-Vishkin step, as the paper remarks.
- **Later bounds.** Cole and Hariharan conjectured that $O(n + m + n k^3 / m)$ is possible for all patterns. Charalampopoulos, Kociumaka and Wellnitz later lowered the power of $k$ below 4, to about $k^{3.5}$ up to logarithmic factors.
- **Hamming distance.** For substitutions only, the [k-mismatch problem](/k-mismatch-problem/) has the stronger bounds of [Amir, Lewenstein and Porat](/amir-lewenstein-porat-algorithm/),.

## When to use it

It is a worst-case result for long patterns with few errors, $k$ well below $m^{1/4}$, where it beats the $O(nk)$ methods on every input. In practice, filters such as [pigeonhole filtering](/pigeonhole-filtering/) or the [Chang-Lawler algorithm](/chang-lawler-algorithm/), followed by [Myers' bit-parallel algorithm](/myers-bit-parallel-algorithm/), are simpler and fast on typical data. The sparse case alone is a clean tool when the pattern is known to be far from periodic.

## Pitfalls

- **Starts and ends.** The paper reports left ends of matches. Reuse an end-position matcher by reversing both strings, and map an end $j$ back to $n - j$.
- **The band must be wider than the window.** The check needs $k$ extra diagonals on each side of the window. Without them, the values on the window diagonals can be too small, and matches near the window edges are lost.
- **Count breaks, not occurrences.** A window needs marks from $k$ distinct breaks. Two occurrences of one break, or two breaks with equal strings at different offsets, must be counted by break.
- **The case $k = 0$.** Windows of $k$ starts and breaks of length $k^2$ are empty, so handle exact matching separately.
- **Short patterns.** A pattern shorter than $2k^3$ cannot have $2k$ breaks, and the paper sends patterns shorter than $5k^3$ to the Landau-Vishkin algorithm.

## Implementations

## History

Cole and Hariharan presented the algorithm at SODA 1998 and published the journal version in the SIAM Journal on Computing in 2002. Landau and Vishkin had solved the k-differences problem in $O(nk)$ time in 1989, and Sahinalp and Vishkin had shown with locally consistent parsing that time $O(n + m + n \, \mathrm{poly}(k)/m)$ is possible, with a larger power of $k$. Cole and Hariharan replaced the parsing by the simple vote of aperiodic breaks, and their analysis of mostly periodic patterns identified the inputs that are hard for this approach.

## References
