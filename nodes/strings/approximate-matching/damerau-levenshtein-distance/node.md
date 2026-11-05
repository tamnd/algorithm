---
tag: SQBSDW
kind: definition
slug: damerau-levenshtein-distance
name: Damerau-Levenshtein distance
aliases:
- optimal string alignment distance
area: strings/approximate-matching
level: core
summary: Edit distance that also allows transposition of two adjacent characters.
prereqs: [edit-distance, edit-operations]
see_also: [edit-distance, wagner-fischer-algorithm, weighted-edit-distance, jaro-winkler-distance, approximate-dictionary-lookup, metric-space, triangle-inequality, sorting-by-transpositions]
sources:
  - paper: doi:10.1145/363958.363994
    title: Fred J. Damerau, A technique for computer detection and correction of spelling errors, Communications of the ACM 7(3), 1964
    locator: pages 171 to 176 (the four kinds of single errors, among them the transposition of two adjacent letters)
  - paper: doi:10.1145/321879.321880
    title: Roy Lowrance and Robert A. Wagner, An extension of the string-to-string correction problem, Journal of the ACM 22(2), 1975
    locator: pages 177 to 183 (edit distance with adjacent transpositions, the condition 2 W_T >= W_I + W_D, and the O(mn) algorithm)
  - paper: doi:10.1145/375360.375365
    title: Gonzalo Navarro, A guided tour to approximate string matching, ACM Computing Surveys 33(1), 2001
    locator: Section 3.1 (the distances with transpositions)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 11 (edit distance and its variants)
---

The Damerau-Levenshtein distance between two strings is the least number of insertions, deletions, substitutions and transpositions of two adjacent characters that turn one string into the other. It extends the Levenshtein [edit distance](/edit-distance/) with the swap of neighbours, the typing error that Damerau counted among the four most common ones. Two different functions carry the name: the true distance, computed by the algorithm of Lowrance and Wagner, and the simpler optimal string alignment distance, which forbids a second edit on a transposed pair. Both take $O(mn)$ time, but only the first is a metric.

## Definition

Let $x = x[0 \ldots m-1]$ and $y = y[0 \ldots n-1]$ be strings over an [alphabet](/alphabet/) $\Sigma$. Indices are 0-based. The four unit-cost [edit operations](/edit-operations/) are insertion, deletion and substitution of one character, and the transposition $ab \to ba$ of two adjacent characters.

**Damerau-Levenshtein distance.** $d_{\mathrm{DL}}(x, y)$ is the least number of the four operations that turn $x$ into $y$. An operation may act on characters that an earlier operation inserted or moved.

**Optimal string alignment distance.** $d_{\mathrm{OSA}}(x, y)$ is the least cost of an edit of $x$ into $y$ in which no substring is edited more than once. It is the value $D[m][n]$ of this table: $D[i][0] = i$, $D[0][j] = j$, and for $i, j \ge 1$

$$D[i][j] = \min\begin{cases} D[i-1][j] + 1, \\ D[i][j-1] + 1, \\ D[i-1][j-1] + [x[i-1] \ne y[j-1]], \\ D[i-2][j-2] + 1 & \text{if } i, j \ge 2,\ x[i-1] = y[j-2],\ x[i-2] = y[j-1]. \end{cases}$$

**The recurrence for $d_{\mathrm{DL}}$.** Lowrance and Wagner prove that, when twice the cost of a transposition is at least the cost of an insertion plus the cost of a deletion, an optimal edit exists in which each transposed pair has only deletions between its two characters in $x$ and only insertions between them in $y$. Unit costs satisfy this condition, because $2 \cdot 1 \ge 1 + 1$. So, with $D[i][j] = d_{\mathrm{DL}}(x[0 \ldots i), y[0 \ldots j))$, the fourth case of the table above becomes

$$D[i'-1][j'-1] + (i - i' - 1) + 1 + (j - j' - 1),$$

where $i' < i$ is the largest 1-based index with $x[i'-1] = y[j-1]$, and $j' < j$ is the largest with $y[j'-1] = x[i-1]$. The case applies when both exist. An array of the last row of each character and one variable for the last column give $i'$ and $j'$ in $O(1)$ time, so the table takes $O(mn)$ time and $O(mn + \sigma)$ space, where $\sigma = |\Sigma|$.

**Order of the three distances.** Each OSA edit is a DL edit, and each Levenshtein edit is an OSA edit, so

$$d_{\mathrm{DL}}(x, y) \le d_{\mathrm{OSA}}(x, y) \le d_{\mathrm{Lev}}(x, y) \le 2\, d_{\mathrm{DL}}(x, y).$$

The last inequality holds because one transposition is two substitutions.

**Metric or not.** $d_{\mathrm{DL}}$ is a metric on $\Sigma^*$: each operation has an inverse operation of the same cost, so it is symmetric, and a script from $x$ to $y$ followed by one from $y$ to $z$ is a script from $x$ to $z$, so it satisfies the [triangle inequality](/triangle-inequality/). $d_{\mathrm{OSA}}$ is symmetric and is zero only on equal strings, but it fails the triangle inequality (see below).

## Examples and non-examples

| $x$ | $y$ | Levenshtein | OSA | Damerau-Levenshtein |
|---|---|---|---|---|
| teh | the | 2 | 1 | 1 |
| ab | ba | 2 | 1 | 1 |
| abcdef | abdcef | 2 | 1 | 1 |
| ca | abc | 3 | 3 | 2 |
| acb | bac | 2 | 2 | 2 |
| kitten | sitting | 3 | 3 | 3 |

- **A typing error.** $\texttt{teh} \to \texttt{the}$ is one transposition, so both distances with transpositions give 1, while the Levenshtein distance is 2.
- **The two definitions differ.** For $\texttt{ca}$ and $\texttt{abc}$, the edit $\texttt{ca} \to \texttt{ac} \to \texttt{abc}$ transposes, then inserts $\texttt{b}$ between the two moved characters. It costs 2, so $d_{\mathrm{DL}} = 2$. The OSA distance forbids the second edit on the moved pair, and it gives 3.
- **Non-example of a metric.** $d_{\mathrm{OSA}}(\texttt{ca}, \texttt{ac}) = 1$ and $d_{\mathrm{OSA}}(\texttt{ac}, \texttt{abc}) = 1$, but $d_{\mathrm{OSA}}(\texttt{ca}, \texttt{abc}) = 3 > 1 + 1$. So OSA is not a metric, and a [BK-tree](/bk-tree/) or another [metric index](/metric-space-indexing/) can miss answers if it uses OSA.
- **Transposition of non-neighbours.** $\texttt{acb}$ and $\texttt{bac}$ is not one transposition: no adjacent swap turns one into the other. All three distances are 2.

## Related definitions

- **Levenshtein distance.** The same without transpositions. See [edit distance](/edit-distance/) and the [Wagner-Fischer algorithm](/wagner-fischer-algorithm/).
- **Weighted version.** Lowrance and Wagner allow separate costs $W_I$, $W_D$, $W_C$ and $W_T$ for insertion, deletion, change and transposition, and their algorithm needs $2 W_T \ge W_I + W_D$. See [weighted edit distance](/weighted-edit-distance/).
- **Jaro-Winkler distance.** Another measure for short strings with typing errors, which counts transposed matching characters. See [Jaro-Winkler distance](/jaro-winkler-distance/).
- **Transpositions in other settings.** The distance that allows only adjacent transpositions is the number of inversions between two permutations. Moves of longer blocks lead to [sorting by transpositions](/sorting-by-transpositions/) and to the [block edit distance](/block-edit-distance/).
- **Approximate search.** With transpositions, [approximate string matching](/approximate-string-matching/) and [approximate dictionary lookup](/approximate-dictionary-lookup/) find more typing errors with the same bound $k$.

## References
