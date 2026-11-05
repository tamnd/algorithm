---
tag: A6FF0J
kind: concept
slug: bad-character-rule
name: Bad-character rule
aliases:
- occurrence heuristic
area: strings/exact-matching
level: core
summary: On a mismatch, shift the pattern to align the mismatched text character with its last occurrence in the pattern.
prereqs: [string-matching, naive-string-matching, alphabet]
see_also: [good-suffix-rule, boyer-moore, boyer-moore-horspool, quick-search, galil-rule, set-horspool]
sources:
  - paper: doi:10.1145/359842.359859
    title: R. S. Boyer and J S. Moore, A fast string searching algorithm, Communications of the ACM 20(10) (1977), 762-772
    locator: the table delta1, indexed by the character that caused the mismatch
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 2, Section 2.2 (the bad character rule and the extended bad character rule), pages 16-34
  - url: http://www-igm.univ-mlv.fr/~lecroq/string/node14.html
    title: Christian Charras and Thierry Lecroq, Exact String Matching Algorithms, 1997
    locator: Boyer-Moore algorithm (the bad-character shift bmBc and the example with x = GCAGAGAG)
  - paper: doi:10.1002/spe.4380100608
    title: R. N. Horspool, Practical fast searching in strings, Software, Practice and Experience 10(6) (1980), 501-506
    locator: the simplified algorithm that shifts by the bad-character table alone
---

The bad-character rule is a shift rule for string matching with right-to-left comparison: when the pattern character $P[j]$ does not match the text character $c$ below it, move the pattern right until the last occurrence of $c$ in the pattern lies under that text character, or past it if $c$ does not occur. It needs only a table of last occurrences, of size $\sigma$, and on large alphabets it often shifts the pattern by almost its full length. It is one of the two rules of [Boyer-Moore](/boyer-moore/) and the only rule of [Horspool](/boyer-moore-horspool/) and [Quick Search](/quick-search/).

## In plain words

Compare the word with the text from the right end of the word. Suppose a text letter does not match. Any new position of the word must put some letter of the word under that text letter, and it must be the same letter. So slide the word until its nearest copy of that letter, looking leftward from the mismatch, comes under it.

If the letter does not occur in the word at all, no position that covers it can match, and the word can jump completely past it. With a big alphabet and a long word this happens often, so the search skips most of the text without reading it.

The simple version uses only the last copy of each letter in the word; if that copy is to the right of the mismatch, it shifts by one.

## The idea

**Setting.** The text is $T[0 \ldots n-1]$ and the pattern is $P[0 \ldots m-1]$, with 0-based indices. The alphabet is an integer alphabet $\{0, \ldots, \sigma - 1\}$, so a character can index a table; a hash map gives the same rule for a general alphabet. The pattern is at shift $s$ and is compared from right to left, so the characters $P[j+1 \ldots m-1]$ matched and $P[j] \ne T[s+j] = c$.

**The last-occurrence table.** Define

$$\lambda(c) = \max\{\, k : 0 \le k < m,\ P[k] = c \,\}, \quad \lambda(c) = -1 \text{ if } c \text{ does not occur in } P.$$

It is computed in $O(m + \sigma)$ time by one left-to-right pass over $P$.

**The rule.** Shift the pattern by

$$\mathrm{bc}(j, c) = \max(1,\ j - \lambda(c)).$$

**Why it is safe.** A shift $d$ with $1 \le d < j - \lambda(c)$ puts $P[j - d]$ under $T[s + j] = c$, and $\lambda(c) < j - d < j$. Then $P[j-d] \ne c$, because the last occurrence of $c$ is at $\lambda(c)$, before $j - d$. So no occurrence starts at $s + d$, and no valid shift is skipped. If $\lambda(c) > j$, the last occurrence is to the right of the mismatch and the rule gives no information beyond a shift of 1.

**The extended rule.** Gusfield's extended bad-character rule uses the rightmost occurrence of $c$ to the left of position $j$: $R_j(c) = \max\{\, k < j : P[k] = c \,\}$, or $-1$, and shifts by $j - R_j(c) \ge 1$. It never shifts by less than the simple rule, and the same argument shows it is safe. It needs a table of size $m\sigma$, or, per character, the sorted list of its positions in $P$ and a search in it.

**Variants by the character used.** [Horspool](/boyer-moore-horspool/) always uses the text character under the last pattern position, $T[s + m - 1]$, whatever $j$ is, with the table built from $P[0 \ldots m-2]$, so its shift is always at least 1. [Quick Search](/quick-search/) uses the text character just after the window, $T[s + m]$, with the table built from all of $P$, so its shift can be $m + 1$.

**Cost.** Used alone, the rule does not bound the worst case: for $T = a^n$ and $P = b\,a^{m-1}$, every window matches $m - 1$ characters and then fails at $j = 0$ on the character a, whose last occurrence is $m - 1 > 0$, so the shift is 1 and the time is $\Theta(nm)$. On random text over a large alphabet, most windows fail at the last position on a character that does not occur in $P$, and the shift is close to $m$, which gives the sublinear average of the [Boyer-Moore](/boyer-moore/) family. Combined with the [good-suffix rule](/good-suffix-rule/), the larger of the two shifts is used.

## Examples

**The table.** For $P$ = gcagagag ($m = 8$) over {a, c, g, t}:

| $c$ | a | c | g | t |
|---|---|---|---|---|
| $\lambda(c)$ | 6 | 1 | 7 | $-1$ |

**Three mismatches.** Take $T$ = gcatcgcagagagtatacagtacg, the example text of Charras and Lecroq.

| shift $s$ | mismatch at $j$ | text character $c$ | $j - \lambda(c)$ | shift |
|---|---|---|---|---|
| 0 | 7 | a | $7 - 6 = 1$ | 1 |
| 1 | 5 | c | $5 - 1 = 4$ | 4 |
| 16 | 6 | c | $6 - 1 = 5$ | 5 |

At $s = 1$, the window is catcgcag; the suffix ag matched, then $P[5]$ = g faced c. The only c of the pattern is at position 1, so the shift is 4 and puts it under that c. The occurrence at $s = 5$ is not skipped.

**An absent character.** If $P$ = gcagagag fails at $j = 7$ against a t, then $\lambda(\text{t}) = -1$ and the shift is 8: the whole pattern passes the t.

**A useless case, and the extended rule.** If $P$ = gcagagag fails at $j = 3$ against a g, then $\lambda(\text{g}) = 7 > 3$, so the simple rule gives only 1. The rightmost g left of position 3 is at 0, so the extended rule shifts by 3.

**A non-example.** Shifting by $m - 1 - \lambda(c)$, the distance from the last occurrence to the pattern end, is wrong when the mismatch is not at the last position. In the row $s = 1$ above, it would give $8 - 1 - 1 = 6$ and skip the occurrence at $s = 5$. That formula is only right for the character aligned with the last position, as in Horspool.

## Where it is used

- [Boyer-Moore](/boyer-moore/) takes the larger of the bad-character shift and the [good-suffix](/good-suffix-rule/) shift.
- [Horspool](/boyer-moore-horspool/) uses only a bad-character table, on the last character of the window.
- [Quick Search](/quick-search/) uses only a bad-character table, on the character after the window.
- [Turbo Boyer-Moore](/turbo-boyer-moore/) and [Apostolico-Giancarlo](/apostolico-giancarlo/) keep the rule next to their worst-case improvements.
- [Set Horspool](/set-horspool/) and [Wu-Manber](/wu-manber/) apply the same idea to many patterns, with a table on characters or on blocks of characters.

## References
