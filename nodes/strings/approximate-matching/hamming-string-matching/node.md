---
tag: 3ZCPFE
kind: problem
slug: hamming-string-matching
name: Hamming string matching
aliases:
- string matching with mismatches
- all Hamming distances
area: strings/approximate-matching
level: advanced
summary: Compute the Hamming distance between the pattern and every alignment in the text.
prereqs: [hamming-distance, string-matching, k-mismatch-problem]
see_also: [k-mismatch-problem, fischer-paterson-algorithm, amir-lewenstein-porat-algorithm, landau-vishkin-algorithm, bitap-algorithm, fast-fourier-transform, approximate-string-matching]
sources:
  - paper: "Michael J. Fischer and Michael S. Paterson, String-matching and other products, in Complexity of Computation, SIAM-AMS Proceedings 7, 1974"
    locator: the reduction of string matching with don't cares to convolutions computed by fast multiplication
  - paper: doi:10.1137/0216067
    title: Karl Abrahamson, Generalized string matching, SIAM Journal on Computing 16(6), 1987
    locator: pages 1039 to 1051 (the mismatch count at every alignment in O(n (m log m)^(1/2)) time, with the split into frequent and rare symbols)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 4 (the match-count problem and its solution with the fast Fourier transform)
  - paper: "Raphaël Clifford, Allyx Fontaine, Ely Porat, Benjamin Sach and Tatiana Starikovskaya, The k-mismatch problem revisited, Proceedings of the 27th ACM-SIAM Symposium on Discrete Algorithms (SODA), 2016, arXiv:1508.00731"
    locator: Section 1 (the history from the O(n (m log m)^(1/2)) algorithms of Abrahamson and Kosaraju to the k-mismatch algorithms, and the time bounds of Karloff's approximations)
---

Hamming string matching is the problem of computing, for every position of a text, the number of characters that differ between the pattern and the text window of the same length that starts there. The answer is an array of [Hamming distances](/hamming-distance/), one per alignment. It contains the answer to exact [string matching](/string-matching/) (the zeros) and to the [k-mismatch problem](/k-mismatch-problem/) (the entries at most $k$). The direct method takes $O(nm)$ time, convolutions with the [fast Fourier transform](/fast-fourier-transform/) take $O(\sigma\, n \log m)$ time for an alphabet of size $\sigma$, and Abrahamson's method takes $O(n \sqrt{m \log m})$ time for any alphabet.

## In plain words

Put the pattern under the text at the first position and count the letters that differ. Then move the pattern one step to the right and count again, and so on until the pattern reaches the end of the text. The answer is the list of all these counts.

The direct method counts each position from scratch, so a long pattern makes it slow. A faster method treats one letter of the alphabet at a time. It marks where that letter is in the pattern and where it is in the text, and one fast multiplication of two long lists then gives, for every position at once, how many places agree on that letter. Adding these numbers for all letters gives the agreements, and the differences are the rest.

## Definition

Let $P = P[0 \ldots m-1]$ and $T = T[0 \ldots n-1]$ be strings over an alphabet $\Sigma$ of size $\sigma$, with $m \le n$. Indices are 0-based. The edit model is the Hamming distance: only substitutions count, so each alignment compares $P$ with a window of exactly $m$ characters. The problem asks for the array $h[0 \ldots n-m]$ with

$$h[i] = |\{\, q \in \{0, \ldots, m-1\} : P[q] \ne T[i + q] \,\}|.$$

Results are indexed by the start position $i$ of the window. When $m = 0$, $h[i] = 0$ for every $i$ in $0, \ldots, n$. When $m > n$, the array is empty.

Write $\chi_c(S)$ for the 0 or 1 vector that marks the positions of the character $c$ in $S$. Then the number of agreements at $i$ is a sum of correlations,

$$m - h[i] = \sum_{c \in \Sigma} \sum_{q=0}^{m-1} \chi_c(P)[q] \cdot \chi_c(T)[i + q],$$

and each inner sum, taken for all $i$ at once, is one convolution of $\chi_c(T)$ with the reverse of $\chi_c(P)$.

## Variants

- **k mismatches.** Report only the positions with $h[i] \le k$, and the value there. This is the [k-mismatch problem](/k-mismatch-problem/), which has faster algorithms when $k$ is small.
- **Approximate counts.** Output values $\tilde h[i]$ with $h[i] \le \tilde h[i] \le (1 + \varepsilon) h[i]$. Karloff gave a randomized method and a deterministic method for this in 1993.
- **Don't cares.** A wildcard symbol in $P$ or $T$ matches every character. Fischer and Paterson solved exact matching with don't cares by convolutions, and the counts with don't cares follow the same way.
- **Other distances on numbers.** For texts of numbers, the sum of $|P[q] - T[i+q]|$ or of $(P[q] - T[i+q])^2$ at every alignment. The squared version needs one convolution and prefix sums.
- **Streaming.** The text arrives one character at a time, and $h[i]$ must be output when $T[i + m - 1]$ arrives, with little space.
- **Edit distance.** Allowing insertions and deletions gives [approximate string matching](/approximate-string-matching/), where an alignment no longer has a fixed length.

## Examples

$P = \texttt{abc}$ and $T = \texttt{abxabcbc}$, so $n - m = 5$:

| $i$ | window | $h[i]$ |
|---|---|---|
| 0 | abx | 1 |
| 1 | bxa | 3 |
| 2 | xab | 3 |
| 3 | abc | 0 |
| 4 | bcb | 3 |
| 5 | cbc | 1 |

The agreements per character are $(1, 0, 0, 1, 0, 0)$ for $\texttt{a}$, $(1, 0, 0, 1, 0, 1)$ for $\texttt{b}$ and $(0, 0, 0, 1, 0, 1)$ for $\texttt{c}$. Their sum is $(2, 0, 0, 3, 0, 2)$, and $3$ minus the sum is $h = (1, 3, 3, 0, 3, 1)$. The exact occurrence is at 3, and with $k = 1$ the k-mismatch answer is $\{0, 3, 5\}$.

$P = \texttt{ACGTA}$ and $T = \texttt{ACGAAACGTTACCTA}$ give $h = (1, 4, 5, 4, 4, 1, 3, 5, 5, 5, 1)$.

## Known algorithms

| algorithm | time | notes |
|---|---|---|
| direct count | $\Theta(nm)$ | any alphabet, no extra space |
| [bitap](/bitap-algorithm/) with counters | $O(n \lceil m \log m / w \rceil)$ | fields of $\lceil \log_2(m+1) \rceil$ bits on a word RAM with $w$-bit words |
| one convolution per symbol ([Fischer-Paterson](/fischer-paterson-algorithm/) method) | $O(\sigma\, n \log m)$ | fast Fourier transform on blocks of length $2m$ |
| Abrahamson (1987); Kosaraju (1987) | $O(n \sqrt{m \log m})$ | frequent symbols by convolution, rare symbols by direct pairs |
| Karloff (1993) | $O(n \varepsilon^{-2} \log^2 m)$ randomized, $O(n \varepsilon^{-2} \log^3 m)$ deterministic | $(1 + \varepsilon)$-approximate counts |

**Abrahamson's split.** Call a symbol frequent if it occurs more than $f$ times in $P$. There are at most $m/f$ frequent symbols, and each costs one convolution, $O(n \log m)$ time. For a rare symbol, each text position $j$ with $T[j] = c$ and each of the at most $f$ positions $q$ of $c$ in $P$ add one agreement to $h$ at $i = j - q$, so the rare symbols cost $O(nf)$ time in total. The choice $f = \sqrt{m \log m}$ balances the two parts at $O(n \sqrt{m \log m})$.

## Bounds

- **Output size.** The output has $n - m + 1$ numbers, so every algorithm needs $\Omega(n)$ time for $m \le n/2$, and $\Omega(n + m)$ time to read the input.
- **Small alphabets.** For a constant $\sigma$, the convolution method takes $O(n \log m)$ time.
- **Large alphabets.** For $\sigma$ near $m$, the best bound of the classic methods is Abrahamson's $O(n \sqrt{m \log m})$, which is far above the $O(n)$ of exact matching.
- **Small distances.** If only the values at most $k$ are needed, the k-mismatch algorithms take $O(nk)$ by [Landau and Vishkin](/landau-vishkin-algorithm/) and $O(n \sqrt{k \log k})$ by [Amir, Lewenstein and Porat](/amir-lewenstein-porat-algorithm/).

## Reductions

- **From exact matching.** $P$ occurs at $i$ exactly when $h[i] = 0$.
- **To the k-mismatch problem.** The k-mismatch answer is $\{ i : h[i] \le k \}$, so any algorithm for all distances solves the k-mismatch problem in the same time.
- **To convolution.** By the identity in the definition, the problem is $\sigma$ correlations of 0 or 1 vectors. A correlation of a vector of length $n$ with one of length $m$ splits into about $n/m$ correlations of length $2m$, each of $O(m \log m)$ time by the fast Fourier transform.
- **From Boolean correlation.** Write two 0 or 1 vectors $x$ and $y$ as strings over $\{\texttt{a}, \texttt{b}\}$. Then $m - h[i] = 2 \sum_q x[q]\, y[i+q] + m - \sum_q x[q] - \sum_q y[i+q]$, so the correlation of $x$ and $y$ follows from $h$ and prefix sums in $O(n)$ extra time.

## Applications

- **Motif search in DNA.** Find the places in a genome where a short sequence occurs with a few substitutions, such as binding sites or primers.
- **Error-tolerant search in signals.** Compare a template with every window of a sampled signal over a finite set of levels.
- **Filters for approximate matching.** A fast estimate of $h$ selects the windows for an exact check in the [k-mismatch problem](/k-mismatch-problem/).
- **Image matching.** Two-dimensional versions count the mismatched pixels of a template at every position of an image.

## References
