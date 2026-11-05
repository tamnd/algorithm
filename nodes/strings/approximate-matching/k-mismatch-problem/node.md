---
tag: R3KH3Y
kind: problem
slug: k-mismatch-problem
name: k-mismatch problem
aliases:
- pattern matching with mismatches
- string matching with k mismatches
area: strings/approximate-matching
level: core
summary: Find all alignments of a pattern in a text with at most k mismatched characters.
prereqs: [hamming-distance, string-matching]
see_also: [hamming-string-matching, k-differences-problem, landau-vishkin-algorithm, amir-lewenstein-porat-algorithm, fischer-paterson-algorithm, bitap-algorithm, longest-common-extension-query, approximate-string-matching]
sources:
  - paper: doi:10.1016/0304-3975(86)90178-7
    title: Gad M. Landau and Uzi Vishkin, Efficient string matching with k mismatches, Theoretical Computer Science 43, 1986
    locator: pages 239 to 249 (the O(kn) algorithm by jumps over longest common extensions)
  - paper: doi:10.1137/0216067
    title: Karl Abrahamson, Generalized string matching, SIAM Journal on Computing 16(6), 1987
    locator: pages 1039 to 1051 (the mismatch count at every alignment in O(n (m log m)^(1/2)) time)
  - paper: doi:10.1016/S0196-6774(03)00097-X
    title: Amihood Amir, Moshe Lewenstein and Ely Porat, Faster algorithms for string matching with k mismatches, Journal of Algorithms 50(2), 2004
    locator: pages 257 to 275 (the O(n (k log k)^(1/2)) algorithm and the O((n + n k^3 / m) log k) algorithm)
  - paper: "Panagiotis Charalampopoulos, Tomasz Kociumaka and Philip Wellnitz, Faster approximate pattern matching: a unified approach, Proceedings of the 61st IEEE Symposium on Foundations of Computer Science (FOCS), 2020, arXiv:2004.08350"
    locator: Section 1, Hamming distance (the history of the problem from Abrahamson and Kosaraju to Gawrychowski and Uznanski)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 9 (the k-mismatch problem with longest common extensions)
---

The k-mismatch problem asks for all positions where a pattern of length $m$ matches a text window of the same length with at most $k$ wrong characters. It is [approximate string matching](/approximate-string-matching/) under the [Hamming distance](/hamming-distance/): only substitutions are allowed, so a match has exactly the length of the pattern. [Landau and Vishkin](/landau-vishkin-algorithm/) solve it in $O(nk)$ time by jumps over [longest common extensions](/longest-common-extension-query/), and convolution-based methods reach $O(n \sqrt{k \log k})$ and, for long patterns, $\tilde O(n + k n / \sqrt{m})$.

## In plain words

Slide the pattern along the text, one position at a time. At each position, put the pattern on top of the text and count the places where the letters differ. If the count is at most the allowed number, report the position.

The direct method compares every letter at every position, which is slow for a long pattern. A faster method jumps: from the current place it finds at once how far the pattern and the text agree, then it steps over the next difference and jumps again. It stops after one difference too many, so each position costs only about as many jumps as the allowed number of differences.

Other methods count, for each letter of the alphabet, the matching places at all positions at once with a fast multiplication of long numbers.

## Definition

Let $T = T[0 \ldots n-1]$ be the text and $P = P[0 \ldots m-1]$ the pattern over an alphabet $\Sigma$, and let $k \ge 0$. Indices are 0-based. For a start $i$ with $0 \le i \le n - m$, the mismatch count is

$$\mathrm{Ham}_i = \bigl|\{\, t \in \{0, \ldots, m-1\} : P[t] \ne T[i + t] \,\}\bigr|.$$

The output is the set $\{\, i \in \{0, \ldots, n-m\} : \mathrm{Ham}_i \le k \,\}$ of start positions, in increasing order. The edit model is substitution only, with unit cost. If $m > n$, the output is empty. If $m = 0$, every $i \in \{0, \ldots, n\}$ is an occurrence. If $k \ge m$, every $i \in \{0, \ldots, n - m\}$ is an occurrence. With $k = 0$ the problem is exact [string matching](/string-matching/).

Many algorithms also report $\mathrm{Ham}_i$ for each occurrence. Computing $\mathrm{Ham}_i$ for every $i$, without a threshold, is [Hamming string matching](/hamming-string-matching/).

## Variants

- **Report the distances.** Output $\mathrm{Ham}_i$ for each occurrence, or $\min(\mathrm{Ham}_i, k + 1)$ for each $i$.
- **Don't care symbols.** A wildcard in $P$ or $T$ matches every character. Convolution methods handle it with one more product.
- **Weighted mismatches.** Each pair of characters has a cost, and the sum must be at most $k$.
- **Streaming.** The text arrives one character at a time, and the algorithm has space much smaller than $m$. Algorithms with space polynomial in $k$ and $\log n$ exist.
- **Indexed text.** Preprocess $T$ so that each later pattern is answered fast. Known indexes have size or query time that grows with $\log^k n$.
- **Edit errors.** With insertions and deletions as well, the problem is the [k-differences problem](/k-differences-problem/).

## Examples

Let $T = \texttt{abxabcbc}$, $P = \texttt{abc}$ and $k = 1$.

| start $i$ | window | mismatches | occurrence |
|---|---|---|---|
| 0 | abx | 1 | yes |
| 1 | bxa | 3 | no |
| 2 | xab | 3 | no |
| 3 | abc | 0 | yes |
| 4 | bcb | 3 | no |
| 5 | cbc | 1 | yes |

The output is $\{0, 3, 5\}$. With $k = 0$ it is $\{3\}$. Under the edit distance with $k = 1$, the same pair has the six end positions $\{2, 3, 5, 6, 7, 8\}$, so the two models give different answers.

A DNA example: $T = \texttt{ACGAAACGTTACCTA}$, $P = \texttt{ACGTA}$ and $k = 1$. The mismatch counts for $i = 0, \ldots, 10$ are $1, 4, 5, 4, 4, 1, 3, 5, 5, 5, 1$, so the occurrences are $0$, $5$ and $10$.

## Known algorithms

| algorithm | time | case | idea |
|---|---|---|---|
| naive | $O(nm)$ | worst | compare each window |
| [Bitap](/bitap-algorithm/) (shift-add) | $O(n \lceil m \log k / w \rceil)$ | worst | a counter for each pattern position in machine words |
| [Landau-Vishkin](/landau-vishkin-algorithm/), Galil-Giancarlo | $O(nk)$ after $O(n + m)$ preprocessing | worst | at most $k + 1$ longest common extensions per window |
| [Convolution](/fischer-paterson-algorithm/) per symbol | $O(\sigma n \log m)$ | worst | one fast Fourier transform per symbol |
| Abrahamson, Kosaraju | $O(n \sqrt{m \log m})$ | worst | convolution for frequent symbols, counting for rare ones |
| [Amir-Lewenstein-Porat](/amir-lewenstein-porat-algorithm/) | $O(n \sqrt{k \log k})$ | worst | frequent symbols mark few candidates, kangaroo checks |
| Amir-Lewenstein-Porat | $O((n + n k^3 / m) \log k)$ | worst | periodicity of the pattern |
| Clifford, Fontaine, Porat, Sach, Starikovskaya | $O(n k^2 \log k / m + n \operatorname{polylog} m)$ | worst | structure of the occurrences |
| Gawrychowski-Uznanski | $\tilde O(n + k n / \sqrt{m})$ | worst | a trade-off between the two lines above |

Here $\sigma = |\Sigma|$, $w$ is the word size, and $\tilde O$ hides factors polylogarithmic in $n$. Several bounds assume that the text is cut into windows of length $2m$ that overlap by $m - 1$, which gives a factor $n / m$ on the cost of one window.

## Bounds

- **Upper bounds.** $O(n \sqrt{k \log k})$ for each $k$ and $\tilde O(n + k n / \sqrt{m})$ for long patterns are the best deterministic bounds above. Chan, Golan, Kociumaka, Kopelowitz and Porat removed most of the logarithmic factors of the second bound with a Monte Carlo algorithm.
- **Conditional lower bound.** Gawrychowski and Uznanski show that a combinatorial algorithm much faster than $\tilde O(n + k n / \sqrt{m})$ would give a faster combinatorial algorithm for Boolean matrix multiplication.
- **Trivial bounds.** For $k = 0$ the problem is exact matching, and $\Omega(n)$ time is needed in the worst case, since an occurrence can be anywhere and the output can have $n - m + 1$ positions.

## Reductions

- **To longest common extensions.** $\mathrm{Ham}_i \le k$ if and only if at most $k + 1$ extension queries, each followed by a skip of one mismatch, reach the end of the pattern. With a [suffix tree](/suffix-tree/) and [lowest common ancestor](/lowest-common-ancestor/) queries, or a suffix array with [range minimum queries](/range-minimum-query/), each query costs $O(1)$.
- **To convolution.** The number of positions where both $P$ and $T[i \ldots i+m)$ hold the symbol $c$ is the correlation of the 0-1 vectors of $c$ in $P$ and in $T$. Summing over all symbols gives $m - \mathrm{Ham}_i$. A [fast Fourier transform](/fast-fourier-transform/) computes each correlation in $O(n \log m)$ time.
- **To exact matching.** If $P$ is cut into $k + 1$ pieces, each occurrence holds one piece exactly, by the [pigeonhole principle](/pigeonhole-principle/). This gives a filter.

## Applications

- **DNA.** Short reads with sequencing errors, which are mostly substitutions, are matched to a genome with a few mismatches.
- **Signal and image search.** Symbol sequences with noise but no shifts.
- **A tool for other problems.** The k-mismatch problem appears inside algorithms for the [k-differences problem](/k-differences-problem/), for periodicity with errors, and for approximate matching in compressed text.

## References
