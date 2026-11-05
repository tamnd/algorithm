---
title: SOUNDEX computes the code that the four Soundex rules define
proves: [correctness]
status: full
---

Let $s = s[0 \ldots L-1]$ be the name after line L1: upper-case ASCII letters only, with $L \ge 1$. Indices are 0-based. Let $\mathrm{code}$ be the digit map of the page, with $\mathrm{code}(a) = 0$ for A, E, I, O, U, Y, H and W.

**The rules.** For $1 \le i < L$, let $p(i)$ be the largest index $j < i$ with $s[j] \notin \{\mathrm{H}, \mathrm{W}\}$, or $p(i) = 0$ if there is no such $j \ge 1$. Position $i \ge 1$ is *kept* when $\mathrm{code}(s[i]) \ne 0$ and $\mathrm{code}(s[i]) \ne \mathrm{code}(s[p(i)])$. The digit string $\Delta$ is the sequence of $\mathrm{code}(s[i])$ over the kept positions $i$, in increasing order of $i$. The Soundex code is $s[0]$ followed by the first three digits of $\Delta$, with zeros added at the end when $\Delta$ has fewer than three digits. This is the definition of the page: the first letter stays (rule 1), letters get digits (rule 2), a letter with the same digit as the last letter before it, with only H and W between them, is dropped (rule 3), and vowels, H and W after the first letter are dropped and the result has length 4 (rule 4).

**Invariant.** At the test of line L3 for the letter $s[i]$, with $1 \le i \le L$ ($i = L$ means the loop ends):

1. $last = \mathrm{code}(s[q])$, where $q$ is the largest index $j < i$ with $j = 0$ or $s[j] \notin \{\mathrm{H}, \mathrm{W}\}$;
2. $out$ is $s[0]$ followed by the codes of the kept positions in $1 \ldots i-1$, and it has at most 3 digits.

*Initialization.* Line L2 sets $out = s[0]$ and $last = \mathrm{code}(s[0])$. For $i = 1$, $q = 0$, and no position in $1 \ldots 0$ exists. Both parts hold.

*Maintenance.* Take the step for $s[i]$, with $i < L$. For $i \ge 1$, the index $q$ of part 1 equals $p(i)$ by the two definitions. If $s[i]$ is H or W, line L5 skips the letter. H and W have code 0, so position $i$ is not kept, and $q$ for $i + 1$ is the same as for $i$, because $s[i]$ is H or W. Both parts hold. Otherwise line L4 sets $c = \mathrm{code}(s[i])$, and by part 1, $last = \mathrm{code}(s[p(i)])$. So the test of line L6 is true exactly when position $i$ is kept, and then line L6 appends its digit. Line L7 sets $last = \mathrm{code}(s[i])$, and $q$ for $i + 1$ is $i$, because $s[i]$ is not H or W. Both parts hold.

*Early stop.* Line L8 stops the loop when $out$ has 3 digits. These are the first three digits of $\Delta$ by part 2, and the code uses no later digit, so the rest of the scan does not change the result.

*End.* If the loop ends without line L8, part 2 for $i = L$ says that $out$ is $s[0]$ followed by all of $\Delta$, with at most 3 digits. Line L9 adds zeros to length 4. In both cases the result is $s[0]$ followed by the first three digits of $\Delta$, padded with zeros. This is the Soundex code. $\blacksquare$

The loop runs at most $L$ times with $O(1)$ work each, so the time is $O(L)$, and line L1 takes time linear in the length of the input.
