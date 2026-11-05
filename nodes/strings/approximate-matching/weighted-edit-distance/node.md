---
tag: 8JTT8X
kind: definition
slug: weighted-edit-distance
name: Weighted edit distance
aliases:
- cost-weighted edit distance
area: strings/approximate-matching
level: core
summary: Edit distance where each edit operation carries its own cost.
prereqs: [edit-distance, edit-operations]
see_also: [edit-distance, wagner-fischer-algorithm, damerau-levenshtein-distance, longest-common-subsequence, hamming-distance, needleman-wunsch, substitution-matrix, affine-gap-penalty]
sources:
  - paper: doi:10.1145/321796.321811
    title: Robert A. Wagner and Michael J. Fischer, The string-to-string correction problem, Journal of the ACM 21(1), 1974
    locator: pages 168 to 173 (edit operations with a cost function, traces, and the dynamic program for the least cost)
  - paper: "Peter H. Sellers, On the theory and computation of evolutionary distances, SIAM Journal on Applied Mathematics 26(4), 1974, 787-793"
    locator: the distance between sequences with weighted operations and its metric property
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 11 (weighted edit distance, alphabet-weighted edit distance and string similarity)
  - paper: doi:10.1145/375360.375365
    title: Gonzalo Navarro, A guided tour to approximate string matching, ACM Computing Surveys 33(1), 2001
    locator: Section 3.1 (the general weighted distance and its special cases)
---

A weighted edit distance between two strings is the least total cost of a sequence of [edit operations](/edit-operations/) that turns one string into the other, where each insertion, deletion and substitution has a cost that can depend on the characters involved. It generalizes the Levenshtein [edit distance](/edit-distance/), where every operation costs 1. The [Wagner-Fischer algorithm](/wagner-fischer-algorithm/) computes it in $O(mn)$ time with the same table, with the costs in place of the ones. The choice of costs gives the [Hamming distance](/hamming-distance/), the distance based on the [longest common subsequence](/longest-common-subsequence/), and the scores of biological sequence alignment.

## Definition

Let $\Sigma$ be an [alphabet](/alphabet/) and $\varepsilon$ the empty string. A **cost function** is a map $\delta : (\Sigma \cup \{\varepsilon\}) \times (\Sigma \cup \{\varepsilon\}) \to \mathbb{R}_{\ge 0} \cup \{\infty\}$ with $\delta(a, a) = 0$ for each $a \in \Sigma$. The operation $a \to b$ with $a, b \in \Sigma$ is a substitution with cost $\delta(a, b)$, the operation $a \to \varepsilon$ is a deletion with cost $\delta(a, \varepsilon)$, and $\varepsilon \to b$ is an insertion with cost $\delta(\varepsilon, b)$. Indices are 0-based.

**Script distance.** For strings $x$ and $y$, $d_\delta(x, y)$ is the least sum of costs of a finite sequence of operations that turns $x$ into $y$. An operation may act on a character that an earlier operation wrote.

**Alignment cost.** An alignment of $x = x[0 \ldots m-1]$ and $y = y[0 \ldots n-1]$ pairs each character of $x$ with at most one character of $y$, so that the pairs do not cross. Its cost is the sum of $\delta(a, b)$ over the pairs, plus $\delta(a, \varepsilon)$ over the unpaired characters $a$ of $x$, plus $\delta(\varepsilon, b)$ over the unpaired characters $b$ of $y$. $A_\delta(x, y)$ is the least cost of an alignment. With $D[i][j] = A_\delta(x[0 \ldots i), y[0 \ldots j))$, $D[0][0] = 0$ and

$$D[i][j] = \min\bigl(D[i-1][j] + \delta(x[i-1], \varepsilon),\; D[i][j-1] + \delta(\varepsilon, y[j-1]),\; D[i-1][j-1] + \delta(x[i-1], y[j-1])\bigr),$$

where a term with a negative index is left out. This table has $(m+1)(n+1)$ cells, so it takes $O(mn)$ time when $\delta$ takes $O(1)$ time.

**The two values.** An alignment is a script in which each character is edited at most once, so $d_\delta(x, y) \le A_\delta(x, y)$ for each cost function. When $\delta$ satisfies the [triangle inequality](/triangle-inequality/) $\delta(a, c) \le \delta(a, b) + \delta(b, c)$ for all $a, b, c \in \Sigma \cup \{\varepsilon\}$, the two values are equal: two operations on the same character can be replaced by one operation of no larger cost, so some cheapest script edits each character at most once. Wagner and Fischer prove this for traces, and the proof on the [Wagner-Fischer algorithm](/wagner-fischer-algorithm/) page for unit costs uses the same steps.

**Metric.** $d_\delta$ satisfies the triangle inequality on $\Sigma^*$ for every $\delta$, because a script from $x$ to $y$ followed by a script from $y$ to $z$ is a script from $x$ to $z$. If $\delta$ is also symmetric and $\delta(a, b) > 0$ for $a \ne b$, then $d_\delta$ is a metric on $\Sigma^*$, and $\Sigma^*$ is a [metric space](/metric-space/).

## Examples and non-examples

- **Levenshtein distance.** $\delta(a, b) = 1$ for $a \ne b$, and $\delta(a, \varepsilon) = \delta(\varepsilon, a) = 1$. This is the [edit distance](/edit-distance/), with $d(\texttt{kitten}, \texttt{sitting}) = 3$.
- **Indel distance.** Insertions and deletions cost 1, and substitutions of different characters cost 2 (or $\infty$, which gives the same value). Then $d_\delta(x, y) = |x| + |y| - 2\,\mathrm{LCS}(x, y)$, where $\mathrm{LCS}$ is the length of a [longest common subsequence](/longest-common-subsequence/). For $\texttt{kitten}$ and $\texttt{sitting}$, $\mathrm{LCS} = 4$ ($\texttt{ittn}$), so the distance is $6 + 7 - 8 = 5$.
- **Hamming distance.** Substitutions cost 1, and insertions and deletions cost $\infty$. Then $d_\delta(x, y)$ is the [Hamming distance](/hamming-distance/) when $|x| = |y|$, and $\infty$ otherwise.
- **Character-dependent costs.** A spelling corrector can give a substitution of two neighbouring keys on the keyboard a lower cost than other substitutions. Alignment of proteins uses a [substitution matrix](/substitution-matrix/) such as BLOSUM, with scores instead of costs (see below).
- **Asymmetric costs.** With insertion cost 1, deletion cost 2 and substitution cost 1, $d_\delta(\texttt{ab}, \texttt{a}) = 2$ but $d_\delta(\texttt{a}, \texttt{ab}) = 1$. The distance is not symmetric, so it is not a metric.
- **Non-example: script and alignment differ.** Let $\Sigma = \{\texttt{a}, \texttt{b}, \texttt{c}\}$, $\delta(\texttt{a}, \texttt{b}) = \delta(\texttt{b}, \texttt{a}) = 5$, all other substitutions cost 1, and insertions and deletions cost 10. This $\delta$ breaks the triangle inequality, because $5 > 1 + 1$. The table gives $A_\delta(\texttt{a}, \texttt{b}) = 5$, but the script $\texttt{a} \to \texttt{c} \to \texttt{b}$ costs 2, so $d_\delta(\texttt{a}, \texttt{b}) = 2$. The table computes $A_\delta$, not $d_\delta$, for such costs.
- **Non-example: a pseudometric.** If $\delta(\texttt{a}, \texttt{A}) = \delta(\texttt{A}, \texttt{a}) = 0$, distinct strings such as $\texttt{abc}$ and $\texttt{Abc}$ have distance 0. Then $d_\delta$ is a pseudometric, not a metric.

## Related definitions

- **Unit-cost distances.** The [edit distance](/edit-distance/) and the [Damerau-Levenshtein distance](/damerau-levenshtein-distance/), which adds a transposition with its own cost $W_T$.
- **Similarity scores.** Biology often maximizes a score instead of minimizing a cost: matches get positive scores, and mismatches and gaps get negative scores. The [Needleman-Wunsch](/needleman-wunsch/) algorithm computes the best global alignment with the same table, with max in place of min.
- **Gap costs.** An [affine gap penalty](/affine-gap-penalty/) charges a run of $L$ insertions $g_{\mathrm{open}} + L\, g_{\mathrm{ext}}$, so one long gap costs less than many short gaps. This cost is not a sum of costs of single operations, and the [Gotoh algorithm](/gotoh-algorithm/) handles it with three tables.
- **Approximate matching with weights.** The [Sellers algorithm](/sellers-algorithm/) for [approximate string matching](/approximate-string-matching/) works with any cost function: the first row of the table is set to 0 so an occurrence can start at any text position.

## References
