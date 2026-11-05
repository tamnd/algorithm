---
tag: H8KKQS
kind: definition
slug: jaro-winkler-distance
name: Jaro-Winkler distance
aliases:
- Jaro-Winkler similarity
area: strings/approximate-matching
level: core
summary: Similarity measure for short strings that rewards a shared prefix, built on the Jaro measure.
prereqs: [edit-distance]
see_also: [edit-distance, damerau-levenshtein-distance, soundex, metaphone, phonetic-string-matching, approximate-dictionary-lookup, string-similarity-join, triangle-inequality]
sources:
  - paper: "Matthew A. Jaro, Advances in record-linkage methodology as applied to matching the 1985 Census of Tampa, Florida, Journal of the American Statistical Association 84(406), 1989"
    locator: the string comparator with common characters in a window and half the number of transpositions
  - paper: "William E. Winkler, String comparator metrics and enhanced decision rules in the Fellegi-Sunter model of record linkage, Proceedings of the Section on Survey Research Methods, American Statistical Association, 1990"
    locator: the increase of the Jaro value for agreement in the first four characters
  - paper: "William W. Cohen, Pradeep Ravikumar and Stephen E. Fienberg, A comparison of string distance metrics for name-matching tasks, IJCAI-03 Workshop on Information Integration on the Web, 2003"
    locator: the definitions of the Jaro and Jaro-Winkler measures and their comparison with edit distances on name data
---

The Jaro-Winkler similarity of two short strings is a number from 0 to 1 that counts the characters the strings share near the same positions, charges for shared characters in a different order, and then adds a bonus for a common prefix of up to four characters. Jaro defined the base measure for the matching of names in census records, and Winkler added the prefix bonus. The Jaro-Winkler distance is one minus the similarity. It is not a metric, and it is meant for short strings such as names, where errors near the start are rare.

## Definition

Let $s = s[0 \ldots |s|-1]$ and $t = t[0 \ldots |t|-1]$ be strings. Indices are 0-based.

**Matching characters.** The match window is $w = \max\bigl(\lfloor \max(|s|, |t|) / 2 \rfloor - 1,\ 0\bigr)$. Scan $s$ from left to right. For each $i$, pair $s[i]$ with the leftmost unpaired $t[j]$ such that $t[j] = s[i]$ and $|i - j| \le w$, if one exists. Let $m$ be the number of pairs.

**Transpositions.** Let $s'$ be the paired characters of $s$ in their order in $s$, and $t'$ the paired characters of $t$ in their order in $t$. Both have length $m$. Let $h$ be the number of positions $q$ with $s'[q] \ne t'[q]$, and $t_{\mathrm{tr}} = h / 2$.

**Jaro similarity.**

$$\mathrm{sim}_J(s, t) = \begin{cases} 0 & \text{if } m = 0, \\ \dfrac{1}{3}\left(\dfrac{m}{|s|} + \dfrac{m}{|t|} + \dfrac{m - t_{\mathrm{tr}}}{m}\right) & \text{if } m > 0. \end{cases}$$

Two empty strings are usually given similarity 1.

**Jaro-Winkler similarity.** Let $\ell$ be the length of the longest common prefix of $s$ and $t$, but at most 4, and let $p$ be a scaling factor with $0 \le p \le 1/4$. The usual value is $p = 0.1$. Then

$$\mathrm{sim}_{JW}(s, t) = \mathrm{sim}_J(s, t) + \ell\, p\, \bigl(1 - \mathrm{sim}_J(s, t)\bigr).$$

The bound $\ell p \le 1$ keeps the value in $[0, 1]$. The **Jaro-Winkler distance** is $d_{JW}(s, t) = 1 - \mathrm{sim}_{JW}(s, t)$, and it is 0 when $s = t$.

**Cost.** The scan tests at most $2w + 1$ positions of $t$ for each character of $s$, so it takes $O(|s|\,(w + 1))$ time, which is $O(|s|\,|t|)$ in the worst case.

## Examples and non-examples

$\texttt{MARTHA}$ and $\texttt{MARHTA}$: $w = 6/2 - 1 = 2$. All six characters pair, so $m = 6$. Then $s' = \texttt{MARTHA}$ and $t' = \texttt{MARHTA}$ differ at two positions, so $h = 2$ and $t_{\mathrm{tr}} = 1$. So $\mathrm{sim}_J = (1 + 1 + 5/6)/3 = 17/18 \approx 0.944$. The common prefix is $\texttt{MAR}$, so $\ell = 3$ and $\mathrm{sim}_{JW} = 17/18 + 0.3 \cdot 1/18 \approx 0.961$.

| $s$ | $t$ | $w$ | $m$ | $t_{\mathrm{tr}}$ | $\mathrm{sim}_J$ | $\ell$ | $\mathrm{sim}_{JW}$ ($p = 0.1$) |
|---|---|---|---|---|---|---|---|
| MARTHA | MARHTA | 2 | 6 | 1 | 0.944 | 3 | 0.961 |
| DWAYNE | DUANE | 2 | 4 | 0 | 0.822 | 1 | 0.840 |
| DIXON | DICKSONX | 3 | 4 | 0 | 0.767 | 2 | 0.813 |
| JONES | JOHNSON | 2 | 4 | 0 | 0.790 | 2 | 0.832 |
| CRATE | TRACE | 1 | 3 | 0 | 0.733 | 0 | 0.733 |

- **Characters far apart do not pair.** In $\texttt{CRATE}$ and $\texttt{TRACE}$ the window is 1, so the C and the T, which swap places three positions apart, are not counted. Only R, A and E pair.
- **Non-example: a short swap.** For $\texttt{AB}$ and $\texttt{BA}$ the window is 0, so no character pairs, and the similarity is 0. The [Damerau-Levenshtein distance](/damerau-levenshtein-distance/) of the two strings is 1.
- **Non-example of a metric.** $d_{JW}(\texttt{a}, \texttt{aa}) = 0.15$ and $d_{JW}(\texttt{aa}, \texttt{ba}) = 1/3$, but $d_{JW}(\texttt{a}, \texttt{ba}) = 1$, which is more than their sum $0.48\overline{3}$. So $d_{JW}$ breaks the [triangle inequality](/triangle-inequality/), and a [metric space index](/metric-space-indexing/) cannot use it.

## Related definitions

- **Edit distances.** The [edit distance](/edit-distance/) counts operations and grows with the length of the strings. The Jaro-Winkler similarity is normalized to $[0, 1]$, so values for short and long strings are on the same scale.
- **Phonetic codes.** [Soundex](/soundex/) and [Metaphone](/metaphone/) match names by sound. Record linkage systems often use a phonetic code to choose candidate pairs and a string comparator such as Jaro-Winkler to score them.
- **Winkler's threshold.** Some programs add the prefix bonus only when $\mathrm{sim}_J$ is above a threshold, often 0.7. Programs also differ in the window, in whether $t_{\mathrm{tr}}$ is rounded down, and in the value for empty strings, so their values can differ.
- **Similarity search.** A [string similarity join](/string-similarity-join/) or an [approximate dictionary lookup](/approximate-dictionary-lookup/) can use the Jaro-Winkler similarity as its measure, but the filters that rely on the triangle inequality or on counts of [q-grams](/q-gram-lemma/) do not apply to it directly.

## References
