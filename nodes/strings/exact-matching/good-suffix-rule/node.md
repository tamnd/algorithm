---
tag: FFWGQW
kind: concept
slug: good-suffix-rule
name: Good-suffix rule
aliases:
- match heuristic
- strong good-suffix rule
area: strings/exact-matching
level: core
summary: After a partial match of a suffix, shift to the next occurrence of that suffix or its border.
prereqs: [border, string-period, bad-character-rule]
see_also: [boyer-moore, boyer-moore-comparison-bound, galil-rule, turbo-boyer-moore, apostolico-giancarlo, z-algorithm]
sources:
  - paper: doi:10.1145/359842.359859
    title: R. S. Boyer and J S. Moore, A fast string searching algorithm, Communications of the ACM 20(10) (1977), 762-772
    locator: the table delta2 and the rightmost plausible reoccurrence of the matched suffix
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 2, Section 2.2 (the strong good suffix rule, the values L'(i) and l'(i), and their computation from the values N_j), pages 16-34
  - url: http://www-igm.univ-mlv.fr/~lecroq/string/node14.html
    title: Christian Charras and Thierry Lecroq, Exact String Matching Algorithms, 1997
    locator: Boyer-Moore algorithm (the functions suffixes and preBmGs, and the table bmGs for x = GCAGAGAG)
  - paper: doi:10.1137/0206024
    title: D. E. Knuth, J. H. Morris and V. R. Pratt, Fast pattern matching in strings, SIAM Journal on Computing 6(2) (1977), 323-350
    locator: the section on the Boyer-Moore algorithm (a linear-time computation of the shift table and the linear bound when the pattern does not occur)
---

The good-suffix rule is a shift rule for string matching with right-to-left comparison: when the pattern has matched a suffix $u$ of itself against the text and then fails, move it to the nearest position where the text $u$ again lies under an equal part of the pattern, preceded by a different pattern character, or where a suffix of $u$ lies under a prefix of the pattern. Its table depends only on the pattern, has $m$ entries, and is computed in $O(m)$ time. With the [bad-character rule](/bad-character-rule/), it forms [Boyer-Moore](/boyer-moore/), and it is what makes the worst-case bounds of the Boyer-Moore family linear.

## In plain words

You compare the word with the text from the right. Some letters at the end of the word matched, then a letter failed. You now know a piece of the text: it equals that matched end of the word.

So slide the word until a part of it that has the same letters sits under that piece of text. There is no point choosing a copy that has, just before it, the same letter that just failed: the same mismatch would happen again. If no full copy exists, slide until the start of the word fits the end of the known piece.

All these slides depend only on the word, so they are computed once, before the search, for each place where a mismatch can happen.

## The idea

**Setting.** The pattern is $P[0 \ldots m-1]$ and the text is $T[0 \ldots n-1]$, with 0-based indices, over a general alphabet: the rule itself uses only equality tests. At shift $s$, the comparison went from right to left, $u = P[j+1 \ldots m-1]$ matched $T[s+j+1 \ldots s+m-1]$, and $P[j] \ne T[s+j]$, with $0 \le j \le m - 1$.

**The strong rule.** The good-suffix shift $\mathrm{gs}[j]$ is the smallest $d \ge 1$ such that

1. $P[i - d] = P[i]$ for every $i$ with $j < i < m$ and $i - d \ge 0$, and
2. $j - d < 0$, or $P[j - d] \ne P[j]$.

Condition 1 says that, after the shift, the pattern agrees with the known text $u$ wherever they overlap: either $u$ reoccurs in $P$ ending at position $m - 1 - d$, or the shift is so large that only a suffix of $u$ remains under the pattern, and that suffix is a prefix of $P$, a [border](/border/) of the pattern. Condition 2 excludes reoccurrences preceded by the character that just failed. The value $d = m$ always satisfies both, so $\mathrm{gs}[j] \le m$.

**After a full match.** Nothing failed, and the next shift that agrees with the matched text is the smallest [period](/string-period/) of $P$, $\mathrm{per}(P) = m - \pi[m-1]$, where $\pi$ is the [prefix function](/prefix-function/). Many implementations store this value as $\mathrm{gs}[0]$, which is equal to it.

**Why it is safe.** Every occurrence at shift $s + d$ with $d \ge 1$ must agree with the text $u$ and with $T[s + j] \ne P[j]$. Condition 1 is necessary for the first, and condition 2 for the second, since if $j - d \ge 0$ the occurrence puts $P[j-d]$ under $T[s+j]$, and $P[j-d] = P[j]$ would make it differ from the text. So every $d < \mathrm{gs}[j]$ is impossible.

**The weak rule.** Dropping condition 2 gives the weak good-suffix rule, which is easier to explain but shifts less. The linear worst-case bounds of Knuth and of Cole for [Boyer-Moore](/boyer-moore/) are proved for the strong rule; see the [comparison bound](/boyer-moore-comparison-bound/).

**Computing the table in $O(m)$ time.** Let $\mathrm{suff}[i]$ be the length of the longest common suffix of $P[0 \ldots i]$ and $P$; it is the [Z array](/z-algorithm/) of the reversed pattern, read backwards, and is computed in $O(m)$ time. Then:

1. Set $\mathrm{gs}[j] = m$ for every $j$.
2. **Borders.** For $i = m - 1$ down to 0, if $\mathrm{suff}[i] = i + 1$, the prefix $P[0 \ldots i]$ is a border of $P$; for every $j < m - 1 - i$ not yet set, set $\mathrm{gs}[j] = m - 1 - i$. A single pointer $j$ moves left to right across all $i$, so this step is $O(m)$.
3. **Reoccurrences.** For $i = 0$ to $m - 2$, set $\mathrm{gs}[m - 1 - \mathrm{suff}[i]] = m - 1 - i$. The suffix of length $\mathrm{suff}[i]$ ends at $i$ and the character before it differs from the one before the suffix of $P$, which is condition 2. Larger $i$ means a smaller shift and overwrites.

This is the procedure of Charras and Lecroq; Gusfield computes the same values as $L'(i)$ and $l'(i)$ from the values $N_j$.

## Examples

**The table of gcagagag.** The example pattern of Charras and Lecroq ($m = 8$, period 7).

| $j$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $P[j]$ | g | c | a | g | a | g | a | g |
| $\mathrm{suff}[j]$ | 1 | 0 | 0 | 2 | 0 | 4 | 0 | 8 |
| strong $\mathrm{gs}[j]$ | 7 | 7 | 7 | 2 | 7 | 4 | 7 | 1 |
| weak shift | 7 | 7 | 7 | 2 | 2 | 2 | 2 | 1 |

**Strong against weak.** Suppose the suffix ag matched and $P[5]$ = g failed ($j = 5$). The suffix ag also occurs at positions 4 to 5, preceded by $P[3]$ = g, and at positions 2 to 3, preceded by $P[1]$ = c. The weak rule shifts by 2, to the copy at 4 to 5, but that copy puts the g of $P[3]$ under the same text character that just refused a g, so it must fail. The strong rule skips it and shifts by 4, to the copy at 2 to 3.

**A border.** At $j = 4$, the matched suffix is gag. It does not reoccur in $P$ with a different character before it, so only the border g can be used: the shift is $8 - 1 = 7$, putting $P[0]$ = g under the last matched text character.

**Nothing matched.** At $j = 7$, $u$ is empty and condition 1 is empty. Condition 2 asks for the nearest $P[7 - d] \ne$ g, which is $P[6]$ = a, so $\mathrm{gs}[7] = 1$. For $P = a^4$, it gives $\mathrm{gs}[3] = 4$: if the last character failed, the text character is not a, and no a may be put under it.

**A non-example.** Shifting to the nearest reoccurrence of $u$ that lies entirely inside $P$ but ignoring borders gives too large shifts. For $P$ = abab and $j = 0$ (bab matched), bab does not reoccur in $P$, yet the shift 2 is possible, because the border ab of the pattern can lie under the end of the text bab; the table gives $\mathrm{gs}[0] = 2$, not 4.

## Where it is used

- [Boyer-Moore](/boyer-moore/) shifts by the larger of the bad-character and the good-suffix values.
- [Turbo Boyer-Moore](/turbo-boyer-moore/) adds a turbo shift on top of it, and [Apostolico-Giancarlo](/apostolico-giancarlo/) adds a table of skips that avoids comparing text characters twice; both give $2n$ bounds.
- The [Galil rule](/galil-rule/) uses the period, which is the good-suffix shift after a full match, to stop rescanning the overlap of two occurrences.
- The [comparison bound](/boyer-moore-comparison-bound/) of Cole, $3n$ comparisons when the pattern does not occur, is a theorem about this rule.
- [Multiple pattern matching](/multiple-string-matching/) algorithms in the style of Commentz-Walter extend the rule to a trie of reversed patterns.

## References
