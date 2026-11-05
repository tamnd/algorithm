---
tag: QVG192
kind: problem
slug: k-differences-problem
name: k-differences problem
aliases:
- k-errors problem
- pattern matching with edits
area: strings/approximate-matching
level: core
summary: Find all substrings of a text within edit distance k of a pattern.
prereqs: [approximate-string-matching, edit-distance]
see_also: [sellers-algorithm, ukkonen-cutoff-algorithm, landau-vishkin-algorithm, galil-park-algorithm, cole-hariharan-algorithm, chang-lawler-algorithm, myers-bit-parallel-algorithm, k-mismatch-problem]
sources:
  - paper: doi:10.1016/0196-6774(89)90010-2
    title: Gad M. Landau and Uzi Vishkin, Fast parallel and serial approximate string matching, Journal of Algorithms 10(2), 1989
    locator: pages 157 to 169 (the O(kn) algorithm on the diagonals with a suffix tree and lowest common ancestor queries)
  - paper: doi:10.1145/375360.375365
    title: Gonzalo Navarro, A guided tour to approximate string matching, ACM Computing Surveys 33(1), 2001
    locator: Section 3.1 (the problem), Section 5.2 (improving the worst case) and Section 5.3 (improving the average case)
  - paper: doi:10.1137/S0097539700370527
    title: Richard Cole and Ramesh Hariharan, Approximate string matching, a simpler faster algorithm, SIAM Journal on Computing 31(6), 2002
    locator: Section 1 (the history from Landau and Vishkin to Sahinalp and Vishkin, the O(n k^4 / m + n + m) bound and the conjectured O(n k^3 / m + n + m))
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 12 (the k-differences problem, the O(km) and O(kn) methods with longest common extensions, and exclusion methods)
  - paper: "Panagiotis Charalampopoulos, Tomasz Kociumaka and Philip Wellnitz, Faster approximate pattern matching: a unified approach, Proceedings of the 61st IEEE Symposium on Foundations of Computer Science (FOCS), 2020, arXiv:2004.08350"
    locator: Section 1 (the state of the art for pattern matching with edits and the conditional lower bound of order n + k^2 n / m)
---

The k-differences problem asks for all places where a pattern occurs in a text with at most $k$ differences, where a difference is an insertion, a deletion or a substitution of one character. It is [approximate string matching](/approximate-string-matching/) under the Levenshtein [edit distance](/edit-distance/), studied as a function of the error bound $k$ as well as of the lengths. [Sellers' algorithm](/sellers-algorithm/) solves it in $O(mn)$ time, [Landau and Vishkin](/landau-vishkin-algorithm/) in $O(kn)$, and [Cole and Hariharan](/cole-hariharan-algorithm/) in $O(n + k^4 n / m)$ when the pattern is long enough. The name contrasts it with the [k-mismatch problem](/k-mismatch-problem/), which allows only substitutions.

## In plain words

You look for a word in a long text, and you accept a place if the text there can become the word with a few small repairs. A repair adds a letter, removes a letter or changes a letter. You fix the number of allowed repairs in advance.

When few repairs are allowed, most of the word must appear exactly. Fast methods use this. They do not look at every pair of a word letter and a text letter. They follow long runs of letters that agree, and they spend real work only where a repair is needed.

The answer is a list of text positions where a good match ends. Several close matches often end at neighbouring positions, because one extra or one missing letter at the end of a match still fits within the allowed repairs.

## Definition

Let $T = T[0 \ldots n-1]$ be the text, $P = P[0 \ldots m-1]$ the pattern and $k \ge 0$ an integer. Indices are 0-based, and $T[h \ldots j)$ is the substring $T[h] \cdots T[j-1]$. The edit model is the Levenshtein distance $d$: unit-cost insertion, deletion and substitution, with no transpositions. A $k$-difference occurrence is a pair $(h, j)$ with $h \le j$ and $d(P, T[h \ldots j)) \le k$.

The standard output is the set of end positions

$$\{\, j \in \{0, \ldots, n\} : \exists h \le j,\ d(P, T[h \ldots j)) \le k \,\}.$$

The algorithms on this site use this output. Some papers report start positions $h$ instead. The two outputs are equivalent by reversal of $P$ and $T$. The problem is interesting when $k < m$. If $k \ge m$, each position is an end, because the empty substring costs $m$.

### The diagonal structure

Let $C[i][j] = \min_{h \le j} d(P[0 \ldots i), T[h \ldots j))$ be the table of [Sellers' algorithm](/sellers-algorithm/), with $C[0][j] = 0$ and $C[i][0] = i$. Cell $(i, j)$ lies on diagonal $j - i$. Two facts make the fast algorithms possible.

- **Diagonals are monotone.** $C[i][j] - C[i-1][j-1] \in \{0, 1\}$ for $i, j \ge 1$. So each diagonal is a non-decreasing staircase with steps of 1, and it has at most $k + 1$ cells where its value first reaches $0, 1, \ldots, k$.
- **Runs of matches are free.** If $P[i] = T[j]$, then $C[i+1][j+1] \le C[i][j]$, so by the first fact $C[i+1][j+1] = C[i][j]$. Hence the cell where a diagonal leaves the value $e$ is found by a [longest common extension](/longest-common-extension-query/) of a suffix of $P$ and a suffix of $T$.

A match ends at $j$ if and only if the diagonal $j - m$ reaches row $m$ with a value at most $k$. The [Landau-Vishkin algorithm](/landau-vishkin-algorithm/) computes, for each diagonal and each $e \le k$, the last row where the diagonal has value $e$, with $O(1)$ work for each pair.

## Variants

- **Start positions or both ends.** Report the starts $h$, or the pairs $(h, j)$. The set of pairs can be much larger than the set of ends.
- **Best distance at each end.** Report $\min(C[m][j], k + 1)$ for each $j$. Most algorithms give this at no extra cost.
- **Weighted differences.** Each operation has a cost, and the total cost is at most $k$. See [weighted edit distance](/weighted-edit-distance/).
- **Transpositions.** A swap of adjacent characters counts as one difference, as in the [Damerau-Levenshtein distance](/damerau-levenshtein-distance/).
- **The decision version.** Decide whether some occurrence exists. This is no easier in the worst case.
- **Indexed text.** Preprocess $T$ once, then answer queries for many patterns. Known indexes use space or time that grows fast with $k$.

## Examples

Let $T = \texttt{CAGATAAGAGAA}$ ($n = 12$), $P = \texttt{GATAA}$ ($m = 5$) and $k = 1$.

| occurrence $(h, j)$ | substring | distance |
|---|---|---|
| $(2, 7)$ | $\texttt{GATAA}$ | 0 |
| $(1, 7)$ | $\texttt{AGATAA}$ | 1 |
| $(2, 6)$ | $\texttt{GATA}$ | 1 |
| $(2, 8)$ | $\texttt{GATAAG}$ | 1 |
| $(3, 7)$ | $\texttt{ATAA}$ | 1 |
| $(7, 12)$ | $\texttt{GAGAA}$ | 1 |

These are all six occurrences. The set of ends is $\{6, 7, 8, 12\}$ and the set of starts is $\{1, 2, 3, 7\}$. The last row of the Sellers table, $C[5][j]$ for $j = 0, \ldots, 12$, is $5, 5, 4, 4, 3, 2, 1, 0, 1, 2, 3, 2, 1$. One exact occurrence gives three ends, 6, 7 and 8, because one deletion or one insertion at the end of the match costs 1.

## Known algorithms

| algorithm | time | case | idea |
|---|---|---|---|
| [Sellers](/sellers-algorithm/) (1980) | $O(mn)$ | worst | the table with a zero first row |
| [Ukkonen cut-off](/ukkonen-cutoff-algorithm/) (1985) | $O(kn)$ | expected | compute each column only down to its last active cell |
| [Landau-Vishkin](/landau-vishkin-algorithm/) (1989) | $O(kn)$ | worst | $k + 1$ steps on each diagonal, with $O(1)$ longest common extensions |
| [Galil-Park](/galil-park-algorithm/) (1990) | $O(kn)$ | worst | the same diagonals with a table built from the pattern only |
| [Wu-Manber](/wu-manber-approximate-matching/) (1992) | $O(k \lceil m / w \rceil\, n)$ | worst | $k + 1$ bit vectors of an automaton |
| [Chang-Lawler](/chang-lawler-algorithm/) (1994) | $O(n)$, and $O((k n / m) \log_\sigma m)$ | expected, for small $k / m$ | skip text that cannot hold a match, verify the rest |
| [Myers](/myers-bit-parallel-algorithm/) (1999) | $O(\lceil m / w \rceil\, n)$ | worst | column differences as bit vectors |
| [Cole-Hariharan](/cole-hariharan-algorithm/) (2002) | $O(n + n k^4 / m + m)$ | worst | few candidate diagonals, found from exact matches of pattern pieces |

Here $w$ is the word size in the [word RAM](/word-ram/). Sahinalp and Vishkin gave the first algorithm that runs in $O(n + m)$ time when $k \le m^{\varepsilon}$ for a small constant $\varepsilon > 0$. Cole and Hariharan simplified and improved it. Filters such as [pigeonhole filtering](/pigeonhole-filtering/) and [q-gram filtering](/q-gram-filtering/) are fast on average for small $k / m$, and they use one of the exact algorithms above to verify candidates.

## Bounds

- **Upper bounds.** $O(kn)$ in the worst case for each $k$, and $O(n + k^4 n / m)$ for $m \ge 5 k^3$. Cole and Hariharan conjecture that $O(n + k^3 n / m)$ is possible.
- **Conditional lower bound.** The [hardness of edit distance](/edit-distance-hardness/) under the Strong Exponential Time Hypothesis implies that no algorithm runs significantly faster than $O(n + k^2 n / m)$. The gap between $k^2$ and $k^4$ is open.
- **Average case.** On a uniform random text, the expected time of each algorithm is $\Omega(n (k + \log_\sigma m) / m)$ (Chang and Marr, 1994). See [approximate string matching](/approximate-string-matching/).

## Reductions

- **From exact matching.** With $k = 0$, the problem is [string matching](/string-matching/).
- **To the Sellers table.** The problem is the question "$C[m][j] \le k$?" for each $j$, so each algorithm that computes the last row of the table, or the cells with values at most $k$, solves it.
- **From edit distance.** Backurs and Indyk prove their lower bound for this pattern version first, then derive the one for [edit distance](/edit-distance/) of two strings.
- **Pigeonhole.** If $P$ is cut into $k + 1$ pieces, each $k$-difference occurrence contains one piece exactly. So the problem reduces to exact [multiple pattern matching](/aho-corasick/) plus verification.

## Applications

- **Search with typing errors.** Tools such as agrep search text files with a few errors.
- **Biology.** Search for a short DNA or protein sequence with a few mutations, insertions and deletions, as in [read mapping](/read-mapping/).
- **Filters inside larger systems.** Many indexes and similarity joins need a fast verifier for a small $k$, and they use the Landau-Vishkin or Myers algorithms.

## References
