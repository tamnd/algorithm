---
tag: 8R2G6X
kind: concept
slug: galil-rule
name: Galil rule
aliases:
- Galil's rule
area: strings/exact-matching
level: advanced
summary: Skips over the already-matched periodic region of the pattern to make Boyer-Moore linear in the worst case.
prereqs: [boyer-moore, string-period, good-suffix-rule]
see_also: [boyer-moore-comparison-bound, turbo-boyer-moore, apostolico-giancarlo, fine-and-wilf-theorem, knuth-morris-pratt]
sources:
  - paper: doi:10.1145/359146.359148
    title: Z. Galil, On improving the worst case running time of the Boyer-Moore string matching algorithm, Communications of the ACM 22(9) (1979), 505-508
    locator: the modification that remembers the prefix known after an occurrence, and the linear bound on the number of comparisons for finding all occurrences
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 3, Section 3.2 (Cole's linear worst-case bound for Boyer-Moore, and the Galil rule that extends it to the case where the pattern occurs), pages 35-69
  - url: http://www-igm.univ-mlv.fr/~lecroq/string/node14.html
    title: Christian Charras and Thierry Lecroq, Exact String Matching Algorithms, 1997
    locator: Boyer-Moore algorithm (worst case O(mn) when searching for all occurrences, the shift by the period after a full match)
---

The Galil rule is a change to [Boyer-Moore](/boyer-moore/) for the case where the pattern occurs: after an occurrence, the pattern shifts by its [period](/string-period/) $p$, and the next window already agrees with the text on its first $m - p$ characters, so the right-to-left comparison stops there instead of rescanning them. With this rule, Boyer-Moore finds all occurrences with $O(n + m)$ comparisons, while the plain algorithm needs $\Theta(nm)$ on inputs such as $T = a^n$, $P = a^m$. Zvi Galil proposed it in 1979.

## In plain words

Boyer-Moore compares the word with the text from right to left. When the whole word matches, it slides by the smallest amount that keeps the word consistent with what it just saw, which is the period of the word.

After such a slide, the left part of the word sits on text that was just matched, and the word repeats itself with that period, so this left part certainly matches again. Plain Boyer-Moore forgets this and compares it again. The Galil rule remembers it: compare only the new part on the right, and if it matches, the whole word matches.

On a text that is one long repetition of the word, this changes the cost from the length of the word per position to one comparison per position.

## The idea

**Setting.** The text is $T[0 \ldots n-1]$ and the pattern $P[0 \ldots m-1]$, with 0-based indices and equality tests only. Let $p$ be the smallest period of $P$: $P[i] = P[i + p]$ for $0 \le i < m - p$. In [Boyer-Moore](/boyer-moore/), a full match at shift $s$ is followed by the shift $p$, which is $\mathrm{gs}[0]$ in the [good-suffix](/good-suffix-rule/) table.

**What is known.** After the occurrence at $s$, $T[s \ldots s+m-1] = P$. The next window starts at $s' = s + p$. For $0 \le k < m - p$,

$$T[s' + k] = T[s + p + k] = P[p + k] = P[k],$$

by the occurrence and then by the period. So the first $m - p$ characters of the next window are known to match.

**The rule.** Keep a bound $b$, initially 0. Compare the window at $s$ from $j = m - 1$ down, but stop at $j = b$ instead of $j = 0$: if $P[j] = T[s + j]$ for all $b \le j < m$, report an occurrence. After an occurrence, shift by $p$ and set $b = m - p$; after any mismatch, shift as usual and set $b = 0$.

```
j ← m − 1
while j ≥ b and P[j] = T[s + j] do j ← j − 1
if j < b then output s; s ← s + p; b ← m − p
else s ← s + max(gs[j], j − λ(T[s + j])); b ← 0
```

**Why it gives linear time.** In a run of occurrences at $s, s + p, s + 2p, \ldots$, each window after the first costs at most $p$ comparisons and moves the pattern by $p$, so each text character is compared $O(1)$ times inside the run. Outside such runs, the analysis of Knuth and of Cole for the search without occurrences applies; Galil's paper and Gusfield's Section 3.2 combine the two cases into an $O(n + m)$ bound for finding all occurrences. See the [comparison bound](/boyer-moore-comparison-bound/).

**Correctness of the stop.** The rule only skips comparisons whose result is known to be equal, by the identity above, so it reports exactly the same windows as Boyer-Moore. A mismatch inside the new part leads to the usual shift, computed from $j \ge b$, as in the plain algorithm.

## Examples

**A run of occurrences.** $T = a^{10}$, $P = a^4$, period $p = 1$. Plain Boyer-Moore compares all 4 characters at each of the 7 shifts: 28 comparisons. With the Galil rule, the first window costs 4 comparisons, and each of the next 6 costs 1 (only $P[3]$, since $b = 3$): 10 comparisons. For $n = 1000$ and $m = 10$, the counts are 9910 and 1000.

**A period larger than 1.** $T = (ab)^8$, $P$ = abab, $p = 2$. The 7 occurrences cost 28 comparisons without the rule and 16 with it: 4 for the first window, then 2 for each next one.

**The run ends.** $P$ = abab occurs at $s$, the pattern moves by 2 and $b = 2$. If the text then continues with ac, the comparison of $P[3]$ = b with c fails at $j = 3 \ge b$, the usual shift applies, and $b$ returns to 0 for the next window.

**A non-example.** Setting $b = m - d$ after a shift $d$ that follows a mismatch is wrong: then the window at $s$ did not match entirely, so the overlap is not known. The rule applies only after a full match.

## Where it is used

- [Boyer-Moore](/boyer-moore/) with the Galil rule is the textbook linear-time version of the algorithm, as in Gusfield's Chapter 3.
- The [comparison bound](/boyer-moore-comparison-bound/) for all occurrences combines Cole's bound with this rule.
- [Turbo Boyer-Moore](/turbo-boyer-moore/) and [Apostolico-Giancarlo](/apostolico-giancarlo/) generalize the idea: they remember what was matched in the previous window even after a mismatch.
- The same use of the period after a match appears in [KMP](/knuth-morris-pratt/) (state $\pi[m-1]$ after a match) and in the [two-way algorithm](/two-way-string-matching/), which keeps a memory of the matched prefix for periodic patterns.

## References
