---
tag: Z4GVFF
kind: problem
slug: edit-distance
name: Edit distance
aliases:
- Levenshtein distance
- string edit distance
area: strings/approximate-matching
level: intro
summary: Minimum number of insertions, deletions and substitutions that turn one string into another.
prereqs: [edit-operations]
see_also: [wagner-fischer-algorithm, approximate-string-matching, damerau-levenshtein-distance, weighted-edit-distance, longest-common-subsequence, edit-distance-hardness, landau-vishkin-algorithm, myers-bit-parallel-algorithm]
sources:
  - paper: "Vladimir I. Levenshtein, Binary codes capable of correcting deletions, insertions, and reversals, Soviet Physics Doklady 10(8), 1966, 707-710"
    locator: the distance between binary words as the least number of insertions, deletions and substitutions (Russian original in Doklady Akademii Nauk SSSR 163(4), 1965)
  - paper: doi:10.1145/321796.321811
    title: Robert A. Wagner and Michael J. Fischer, The string-to-string correction problem, Journal of the ACM 21(1), 1974
    locator: pages 168 to 173 (the problem with general costs and the O(mn) dynamic program)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 11 (edit distance, its dynamic program, edit graphs and weighted edit distance) and Chapter 12 (linear space and bounded differences)
  - paper: doi:10.1016/0022-0000(80)90002-1
    title: William J. Masek and Michael S. Paterson, A faster algorithm computing string edit distances, Journal of Computer and System Sciences 20(1), 1980
    locator: pages 18 to 31 (the O(n^2 / log n) algorithm for a finite alphabet)
  - paper: doi:10.1145/321921.321923
    title: C. K. Wong and Ashok K. Chandra, Bounds for the string editing problem, Journal of the ACM 23(1), 1976
    locator: pages 13 to 16 (the lower bound of order mn in a model with equal and unequal tests)
  - paper: doi:10.1137/15M1053128
    title: Arturs Backurs and Piotr Indyk, Edit distance cannot be computed in strongly subquadratic time (unless SETH is false), SIAM Journal on Computing 47(3), 2018
    locator: pages 1087 to 1097 (the main theorem; conference version in STOC 2015)
  - paper: doi:10.1016/S0019-9958(85)80046-2
    title: Esko Ukkonen, Algorithms for approximate string matching, Information and Control 64, 1985
    locator: pages 100 to 118 (the O(d min(m, n)) algorithm on the diagonals of the table)
---

The edit distance problem asks for the least number of insertions, deletions and substitutions of single characters that turn one string into another. This number is the Levenshtein distance, and the three steps are the [edit operations](/edit-operations/). The [Wagner-Fischer algorithm](/wagner-fischer-algorithm/) solves the problem in $O(mn)$ time for strings of lengths $m$ and $n$. Under the Strong Exponential Time Hypothesis, no algorithm solves it in time $O(n^{2-\varepsilon})$ for a constant $\varepsilon > 0$.

## In plain words

You have two words, and you want to change the first word into the second one. In one step you can add a letter, remove a letter, or change a letter into another letter. The edit distance is the smallest number of steps that does the job.

Two equal words have distance zero. A word and the same word with one typing error have distance one. A short word and a long word are always far apart, because each step adds or removes at most one letter.

The answer is found by a table. Each cell holds the distance between a start of the first word and a start of the second word. Each cell needs only three of its neighbours, so the table fills in one pass.

## Definition

Let $\Sigma$ be an [alphabet](/alphabet/), and let $x = x[0 \ldots m-1]$ and $y = y[0 \ldots n-1]$ be strings over $\Sigma$. Indices are 0-based. The Levenshtein distance $d(x, y)$ is the least number of unit-cost edit operations (insertion of one character, deletion of one character, substitution of one character by a different one) that turn $x$ into $y$.

The problem: given $x$ and $y$, output $d(x, y)$. Some applications also ask for an optimal edit script or an optimal alignment.

For the prefixes $x[0 \ldots i-1]$ and $y[0 \ldots j-1]$, let $D[i][j]$ be their distance. Then $D[i][0] = i$, $D[0][j] = j$, and for $i, j \ge 1$

$$D[i][j] = \min\bigl(D[i-1][j] + 1,\; D[i][j-1] + 1,\; D[i-1][j-1] + [x[i-1] \ne y[j-1]]\bigr),$$

where $[\cdot]$ is 1 when the condition holds and 0 when it does not. The answer is $D[m][n]$. The [Wagner-Fischer algorithm](/wagner-fischer-algorithm/) page proves this recurrence.

**Properties.** The Levenshtein distance is a metric on $\Sigma^*$, so it makes $\Sigma^*$ a [metric space](/metric-space/). It is zero only for equal strings. It is symmetric, because each operation has an inverse operation of the same cost. It satisfies the [triangle inequality](/triangle-inequality/), because a script from $x$ to $y$ followed by a script from $y$ to $z$ is a script from $x$ to $z$. Each operation changes the length by at most 1, so $d(x, y) \ge |m - n|$. Substitution of the first $\min(m, n)$ positions, then insertion or deletion of the rest, gives $d(x, y) \le \max(m, n)$.

## Variants

- **Weighted edit distance.** Each operation has its own cost, for example a cost that depends on the two characters. See [weighted edit distance](/weighted-edit-distance/).
- **Transpositions.** The [Damerau-Levenshtein distance](/damerau-levenshtein-distance/) also allows a swap of two adjacent characters at cost 1.
- **Indel distance.** With only insertions and deletions, the distance is $m + n - 2\,\mathrm{LCS}(x, y)$, where $\mathrm{LCS}$ is the length of a [longest common subsequence](/longest-common-subsequence/).
- **Hamming distance.** With only substitutions, the strings must have the same length, and the distance is the number of positions where they differ. See [Hamming distance](/hamming-distance/).
- **Bounded distance.** Given $k$, decide whether $d(x, y) \le k$. This is faster than the full problem when $k$ is small.
- **Search in a text.** Find the substrings of a text at distance at most $k$ from a pattern. This is [approximate string matching](/approximate-string-matching/), also called the [k-differences problem](/k-differences-problem/).
- **Block moves.** The [block edit distance](/block-edit-distance/) also allows the move of a whole substring as one operation.
- **Trees.** The [tree edit distance](/tree-edit-distance/) applies the same operations to the nodes of ordered trees.

## Examples

| $x$ | $y$ | $d(x, y)$ | one optimal script |
|---|---|---|---|
| $\texttt{kitten}$ | $\texttt{sitting}$ | 3 | $k \to s$, $e \to i$, insert $g$ |
| $\texttt{sunday}$ | $\texttt{saturday}$ | 3 | insert $a$, insert $t$, $n \to r$ |
| $\texttt{intention}$ | $\texttt{execution}$ | 5 | delete $i$, $n \to e$, $t \to x$, insert $u$, $n \to c$ |
| $\texttt{GATTACA}$ | $\texttt{GCATGCU}$ | 4 | insert $C$, delete $T$, $A \to G$, $A \to U$ |
| $\texttt{abc}$ | $\texttt{abc}$ | 0 | the empty script |
| $\varepsilon$ | $\texttt{abc}$ | 3 | insert $a$, $b$, $c$ |

The pair $\texttt{ab}$ and $\texttt{ba}$ is a non-example for the bound $d \le 1$ for one typing error: the Levenshtein distance is 2, while the Damerau-Levenshtein distance is 1.

## Known algorithms

| algorithm | time | space | notes |
|---|---|---|---|
| [Wagner-Fischer](/wagner-fischer-algorithm/) | $O(mn)$ | $O(\min(m, n))$ for the distance | the full table gives a script by [traceback](/traceback/) |
| Hirschberg's divide and conquer | $O(mn)$ | $O(m + n)$ with a script | the method of [Hirschberg's LCS](/hirschberg-lcs/) |
| Masek and Paterson | $O(n^2 / \log n)$ | $O(n)$ for the distance | finite alphabet, $m = n$, the [Four Russians method](/four-russians-method/) |
| Ukkonen (1985) | $O(d \min(m, n))$ | $O(d)$ for the distance | only the diagonals near the main diagonal |
| diagonal extension with LCE | $O(m + n + d^2)$ | $O(m + n)$ | a [longest common extension](/longest-common-extension-query/) query per step, as in [Landau-Vishkin](/landau-vishkin-algorithm/) |
| [Myers bit-parallel](/myers-bit-parallel-algorithm/) | $O(\lceil m / w \rceil\, n)$ | $O(\sigma \lceil m / w \rceil)$ | word size $w$ in the [word RAM](/word-ram/) |

Here $d = d(x, y)$, $\sigma = |\Sigma|$, and $w$ is the number of positions that one machine word holds. The diagonal methods use the fact that a path of cost $d$ in the table stays within $d$ diagonals of the main diagonal.

## Bounds

- **Upper bound.** $O(mn)$ time by dynamic programming. For a finite alphabet, Masek and Paterson reach $O(n^2 / \log n)$ when $m = n$, and this is the best known bound in the worst case.
- **Lower bound in a comparison model.** Wong and Chandra show that an algorithm that only tests characters for equality needs $\Omega(mn)$ tests in the worst case, when the alphabet is not bounded.
- **Conditional lower bound.** Backurs and Indyk show that an algorithm with time $O(n^{2-\varepsilon})$ for a constant $\varepsilon > 0$ would refute the Strong Exponential Time Hypothesis. See [edit distance hardness](/edit-distance-hardness/).
- **Output-sensitive bound.** The diagonal methods take $O(m + n + d^2)$ time, so they are linear when $d = O(\sqrt{n})$.

## Reductions

- **To shortest paths.** The table is a grid graph with an edge of cost 1 for each insertion and deletion and an edge of cost 0 or 1 on each diagonal. The distance is the length of a shortest path from the corner $(0, 0)$ to the corner $(m, n)$. This graph is acyclic, so a [dynamic program on a DAG](/dp-on-dag/) solves it.
- **From the longest common subsequence.** With cost 1 for an insertion and for a deletion and cost 2 for a substitution, the weighted distance equals $m + n - 2\,\mathrm{LCS}(x, y)$. So an edit distance algorithm with weights also computes the [longest common subsequence](/longest-common-subsequence/) length.
- **From orthogonal vectors.** Backurs and Indyk reduce the orthogonal vectors problem to edit distance. This is the base of the conditional lower bound.

## Applications

- **Spelling correction.** A misspelt word is compared to the words of a dictionary, and the closest words are suggestions. See [approximate dictionary lookup](/approximate-dictionary-lookup/).
- **Biology.** The comparison of DNA and protein sequences uses a weighted form, the [global alignment](/global-alignment/) of Needleman and Wunsch.
- **Record linkage and search.** Names and addresses with small errors are matched by a small edit distance, and search engines use it to correct queries.
- **Coding theory.** Levenshtein defined the distance to study codes that correct insertions and deletions of bits.

## References
