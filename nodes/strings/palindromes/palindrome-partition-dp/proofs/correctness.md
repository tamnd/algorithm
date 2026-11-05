---
title: Correctness of palindrome partition dynamic programming
proves: [correctness]
status: full
---

We prove that PALINDROME-PARTITION-DP returns $\mathrm{PL}(s)$, the least number of nonempty palindromes whose concatenation is $s = s[0..n-1]$, together with a partition of $s$ into that many palindromes. Indices are 0-based and $s[j..i]$ includes both ends. We write $\mathrm{PL}_i$ for $\mathrm{PL}(s[0..i-1])$, so $\mathrm{PL}_0 = 0$.

**Lemma 1 (the table).** After the run of the outer loop for $i$, for each $0 \le j \le i$, the entry $\mathrm{pal}[j][i]$ is true if and only if $s[j..i]$ is a palindrome.

*Proof.* By induction on $i$. The entry $\mathrm{pal}[j][i]$ is set only in the run for $i$, by line L6, and only if the test of line L5 holds. If $i - j \le 1$, then $s[j..i]$ is a palindrome if and only if $s[j] = s[i]$, which is the test. If $i - j \ge 2$, then $s[j..i]$ is a palindrome if and only if $s[j] = s[i]$ and $s[j+1..i-1]$ is a palindrome, because the mirror pairs of $s[j..i]$ are $(j, i)$ and the mirror pairs of $s[j+1..i-1]$. The entry $\mathrm{pal}[j+1][i-1]$ is in column $i - 1$, with $j + 1 \le i - 1$, so it is correct by the induction hypothesis, and no later run changes it. $\square$

**Lemma 2 (the recurrence).** For $0 \le i \le n - 1$,
$$ \mathrm{PL}_{i+1} = \min\{\mathrm{PL}_j + 1 : 0 \le j \le i,\ s[j..i] \text{ is a palindrome}\}. $$

*Proof.* The set is not empty, because $s[i..i]$ is a palindrome. Let $s[0..i] = p_1 \cdots p_k$ be a partition into $k = \mathrm{PL}_{i+1}$ palindromes, and let $p_k = s[j..i]$. Then $p_1 \cdots p_{k-1}$ is a partition of $s[0..j-1]$ into palindromes, so $k - 1 \ge \mathrm{PL}_j$, and the right side is at most $k$. Conversely, for each $j$ in the set, a partition of $s[0..j-1]$ into $\mathrm{PL}_j$ palindromes followed by the piece $s[j..i]$ is a partition of $s[0..i]$ into $\mathrm{PL}_j + 1$ palindromes, so $\mathrm{PL}_{i+1} \le \mathrm{PL}_j + 1$. $\square$

**Lemma 3 (the values).** After the run of the outer loop for $i$, $\mathrm{best}[i+1] = \mathrm{PL}_{i+1}$, and $s[0..\mathrm{start}[i+1]-1]$ followed by $s[\mathrm{start}[i+1]..i]$ is a split whose last piece is a palindrome and with $\mathrm{best}[\mathrm{start}[i+1]] + 1 = \mathrm{best}[i+1]$.

*Proof.* By induction on $i$, with $\mathrm{best}[0] = 0 = \mathrm{PL}_0$ from line L1. In the run for $i$, line L3 sets $\mathrm{best}[i+1]$ to $\infty$, and the inner loop goes over $j = 0, \ldots, i$. By Lemma 1, the test of line L5 holds exactly for the $j$ with $s[j..i]$ a palindrome, and by the induction hypothesis $\mathrm{best}[j] = \mathrm{PL}_j$ for these $j \le i$. Line L7 keeps the running minimum of $\mathrm{best}[j] + 1$ over them and the $j$ where it was reached. At the end of the run, by Lemma 2, $\mathrm{best}[i+1] = \mathrm{PL}_{i+1}$, and $\mathrm{start}[i+1]$ is a $j$ with $s[j..i]$ a palindrome and $\mathrm{PL}_j + 1 = \mathrm{PL}_{i+1}$. Later runs do not change $\mathrm{best}[i+1]$ or $\mathrm{start}[i+1]$. $\square$

**Lemma 4 (the rebuild).** Lines L8 and L9 put $\mathrm{best}[n]$ pieces into $\mathit{pieces}$, each a palindrome, and their concatenation is $s$.

*Proof.* We show the invariant: at each test of line L9, $\mathit{pieces}$ is a list of $\mathrm{best}[n] - \mathrm{best}[i]$ palindromes whose concatenation is $s[i..n-1]$. At the start $i = n$ and the list is empty. If $i > 0$, let $j = \mathrm{start}[i]$. By Lemma 3, $s[j..i-1]$ is a palindrome and $\mathrm{best}[j] = \mathrm{best}[i] - 1$, so after line L9 the list holds $\mathrm{best}[n] - \mathrm{best}[j]$ palindromes whose concatenation is $s[j..n-1]$, and the new value of $i$ is $j$. Since $j \le i - 1$, the loop stops after at most $n$ steps, with $i = 0$ and $\mathrm{best}[0] = 0$. $\square$

**Theorem.** PALINDROME-PARTITION-DP returns $\mathrm{PL}(s)$ and a partition of $s$ into $\mathrm{PL}(s)$ palindromes.

*Proof.* For $n = 0$ the outer loop does not run and the result is $0$ with the empty partition, which is correct. For $n \ge 1$, Lemma 3 with $i = n - 1$ gives $\mathrm{best}[n] = \mathrm{PL}_n = \mathrm{PL}(s)$, and Lemma 4 shows that the returned pieces form a partition of $s$ into $\mathrm{best}[n]$ palindromes. Both loops are bounded, so the algorithm stops. $\blacksquare$
