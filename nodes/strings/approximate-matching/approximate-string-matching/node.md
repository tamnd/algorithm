---
tag: NGNQGX
kind: problem
slug: approximate-string-matching
name: Approximate string matching
aliases:
- approximate pattern matching
- fuzzy string matching
area: strings/approximate-matching
level: intro
summary: Find all text positions where a pattern matches within a bounded number of errors.
prereqs: [edit-distance, string-matching]
see_also: [k-differences-problem, k-mismatch-problem, sellers-algorithm, landau-vishkin-algorithm, myers-bit-parallel-algorithm, q-gram-filtering, pigeonhole-filtering, approximate-dictionary-lookup]
sources:
  - paper: doi:10.1145/375360.375365
    title: Gonzalo Navarro, A guided tour to approximate string matching, ACM Computing Surveys 33(1), 2001
    locator: Section 3.1 (the problem), Section 5 (dynamic programming), Section 6 (automata), Section 7 (bit-parallelism) and Section 8 (filtering)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 11 (inexact matching by dynamic programming) and Chapter 12 (bounded differences and exclusion methods)
  - book: isbn:9780521813075
    title: Gonzalo Navarro and Mathieu Raffinot, Flexible Pattern Matching in Strings, Cambridge University Press, 2002
    locator: Chapter 6, Approximate matching
  - paper: doi:10.1016/0196-6774(80)90016-4
    title: Peter H. Sellers, The theory and computation of evolutionary distances, pattern recognition, Journal of Algorithms 1(4), 1980
    locator: pages 359 to 373 (the dynamic program with a first row of zeros)
  - paper: doi:10.1137/S0097539700370527
    title: Richard Cole and Ramesh Hariharan, Approximate string matching, a simpler faster algorithm, SIAM Journal on Computing 31(6), 2002
    locator: pages 1761 to 1782 (the O(n k^4 / m + n + m) bound and the conjecture of O(n k^3 / m + n + m))
  - paper: "Panagiotis Charalampopoulos, Tomasz Kociumaka and Philip Wellnitz, Faster approximate pattern matching: a unified approach, Proceedings of the 61st IEEE Symposium on Foundations of Computer Science (FOCS), 2020, arXiv:2004.08350"
    locator: Section 1 (the survey of the known bounds and the conditional lower bound of order n + k^2 n / m)
  - paper: "William I. Chang and Thomas G. Marr, Approximate string matching and local similarity, Combinatorial Pattern Matching (CPM 1994), LNCS 807"
    locator: the average-case lower bound of order n (k + log m) / m for a uniform random text, and an algorithm that reaches it for small error levels
---

Approximate string matching is the problem of finding all places in a text where a pattern occurs with at most $k$ errors. An error is an [edit operation](/edit-operations/): with substitutions only, the problem is the [k-mismatch problem](/k-mismatch-problem/), and with insertions, deletions and substitutions it is the [k-differences problem](/k-differences-problem/). The classic solution is the $O(mn)$ dynamic program of [Sellers](/sellers-algorithm/), and the best worst-case bounds are $O(kn)$ by [Landau and Vishkin](/landau-vishkin-algorithm/) and $O(n + k^4 n / m)$ by [Cole and Hariharan](/cole-hariharan-algorithm/).

## In plain words

You search a long text for a word, but the text has typing errors, or the word itself is spelt in a slightly different way. Exact search misses these places. Approximate search accepts a place in the text when a few small changes turn the text there into the word. You choose how many changes are allowed.

A change can be one wrong letter, one missing letter or one extra letter. Some versions allow only wrong letters, so the matching piece of text has the same length as the word.

The output is a list of places in the text. For each place, some piece of text that ends there is close enough to the word. Most methods read the text from left to right and keep a small amount of work for each letter of the text.

## Definition

Let $T = T[0 \ldots n-1]$ be the text and $P = P[0 \ldots m-1]$ the pattern, over an [alphabet](/alphabet/) $\Sigma$ of size $\sigma$. Indices are 0-based, and $T[i \ldots j)$ is the substring $T[i] \cdots T[j-1]$ (empty when $i = j$). Let $k \ge 0$ be an integer, and let $d$ be a distance on strings.

**Edit model (k differences).** Here $d$ is the [Levenshtein distance](/edit-distance/), with unit cost for an insertion, a deletion and a substitution. The output is the set of end positions

$$\mathrm{Occ}_k(P, T) = \{\, j \in \{0, \ldots, n\} : d(P, T[i \ldots j)) \le k \text{ for some } i \le j \,\}.$$

One reports end positions, not start positions, because a match that ends at $j$ can start at several places. If $k \ge m$, each $j$ is in the set, because the empty substring $T[j \ldots j)$ has distance $m$. The ratio $\alpha = k / m$ is the error level. Some papers report start positions instead, with the same definition read on the reversed strings.

**Hamming model (k mismatches).** Here $d$ is the [Hamming distance](/hamming-distance/) and the substring has length $m$. The output is the set of start positions $i \in \{0, \ldots, n - m\}$ with $d(P, T[i \ldots i+m)) \le k$. When $m = 0$, each $i \in \{0, \ldots, n\}$ is an occurrence.

With $k = 0$, both models give the exact [string matching](/string-matching/) problem.

## Variants

- **Weighted errors.** Each operation has a cost, and a match needs total cost at most $k$. See [weighted edit distance](/weighted-edit-distance/).
- **Transpositions.** The swap of two adjacent characters costs 1, as in the [Damerau-Levenshtein distance](/damerau-levenshtein-distance/). This models typing errors.
- **The best match.** Find the least $k$ for which a match exists, or the substrings of least distance.
- **Many patterns.** Search for a set of patterns at once.
- **Indexed search.** The text is fixed and is preprocessed into an index, for example a [suffix tree](/suffix-tree/) or a [q-gram](/q-gram-filtering/) index, and many patterns are searched later. For a set of words, this is [approximate dictionary lookup](/approximate-dictionary-lookup/).
- **Other distances.** Sound-based codes such as [Soundex](/soundex/) give [phonetic matching](/phonetic-string-matching/), and the [block edit distance](/block-edit-distance/) allows moves of substrings.

## Examples

Let $T = \texttt{surgery}$, $P = \texttt{survey}$ and $k = 2$.

| end $j$ | best substring $T[i \ldots j)$ | distance to $P$ | match |
|---|---|---|---|
| 3 | $\texttt{sur}$ | 3 | no |
| 4 | $\texttt{surg}$ | 3 | no |
| 5 | $\texttt{surge}$ | 2 | yes |
| 6 | $\texttt{surger}$ | 2 | yes |
| 7 | $\texttt{surgery}$ | 2 | yes |

So $\mathrm{Occ}_2 = \{5, 6, 7\}$. The ends 0 to 2 have distances 6, 5 and 4. In the Hamming model with $k = 2$, only the start 0 matches: $\texttt{surger}$ and $\texttt{survey}$ differ at positions 3 and 5. With $k = 1$, no end matches in either model.

A second example: $T = \texttt{abxabcbc}$, $P = \texttt{abc}$, $k = 1$. The edit model gives the ends $\{2, 3, 5, 6, 7, 8\}$, and the Hamming model gives the starts $\{0, 3, 5\}$.

## Known algorithms

Edit model, with $n$ the text length, $m$ the pattern length and $w$ the word size of the [word RAM](/word-ram/):

| algorithm | time | case |
|---|---|---|
| [Sellers](/sellers-algorithm/) | $O(mn)$ | worst |
| [Ukkonen's cut-off](/ukkonen-cutoff-algorithm/) | $O(kn)$ | expected, random text |
| [Landau-Vishkin](/landau-vishkin-algorithm/), [Galil-Park](/galil-park-algorithm/) | $O(kn)$ after preprocessing | worst |
| [Wu-Manber](/wu-manber-approximate-matching/) | $O(k \lceil m / w \rceil\, n)$ | worst |
| [Myers bit-parallel](/myers-bit-parallel-algorithm/) | $O(\lceil m / w \rceil\, n)$ | worst |
| [Chang-Lawler](/chang-lawler-algorithm/) | $O(n)$, and sublinear for small $k$ | expected, for $\alpha$ below a threshold |
| [Cole-Hariharan](/cole-hariharan-algorithm/) | $O(n k^4 / m + n + m)$ | worst |
| [Levenshtein automaton](/levenshtein-automaton/) | $O(n)$ after a preprocessing that grows fast with $k$ | worst |

Filters discard most of the text with a fast test and verify the rest: [pigeonhole filtering](/pigeonhole-filtering/) cuts the pattern into $k+1$ pieces, and [q-gram filtering](/q-gram-filtering/) counts shared q-grams by the [q-gram lemma](/q-gram-lemma/).

Hamming model: the naive $O(mn)$ method, $O(kn)$ by Landau and Vishkin, $O(\sigma\, n \log m)$ by [convolution](/fischer-paterson-algorithm/), $O(n \sqrt{m \log m})$ by Abrahamson, and $O(n \sqrt{k \log k})$ by [Amir, Lewenstein and Porat](/amir-lewenstein-porat-algorithm/). See [Hamming string matching](/hamming-string-matching/).

## Bounds

- **Worst case, edit model.** The best known bound is $O(n + k^4 n / m)$ for $m \ge 5 k^3$ and $O(kn)$ in general, from the work of Cole and Hariharan and of Landau and Vishkin. Cole and Hariharan conjecture that $O(n + k^3 n / m)$ is possible. The conditional lower bound of Backurs and Indyk for [edit distance](/edit-distance-hardness/) rules out an algorithm significantly faster than $O(n + k^2 n / m)$ under the Strong Exponential Time Hypothesis, and the gap between $k^2$ and $k^4$ is open.
- **Average case.** For a uniform random text, Chang and Marr show that each algorithm needs $\Omega(n (k + \log_\sigma m) / m)$ expected time. They also give an algorithm with this expected time, when $\alpha$ is below a constant that depends on $\sigma$, so the bound is tight in that range.

## Reductions

- **To edit distance with a free start.** Set the first row of the edit distance table to zero. Then the last row gives, for each end $j$, the least distance from $P$ to a substring that ends at $j$. This is the method of Sellers.
- **Hamming model to convolution.** For each symbol $c$, the number of positions where $P$ and $T[i \ldots i+m)$ both hold $c$ is a correlation of two 0-1 vectors. A [fast Fourier transform](/fast-fourier-transform/) computes it for each $i$ at once.
- **From exact matching.** The case $k = 0$ is [string matching](/string-matching/), so each lower bound for exact matching also holds here.

## Applications

- **Text search with errors.** Tools such as agrep search files for a pattern with a few errors, with the bit-parallel methods.
- **Biology.** Short DNA reads are found in a genome with a few substitutions and indels, in [read mapping](/read-mapping/).
- **Spelling and data cleaning.** Search for names and words with typing errors, and link records that differ in a few characters.
- **Signal and music retrieval.** Melodies and other symbol sequences are searched with errors.

## References
