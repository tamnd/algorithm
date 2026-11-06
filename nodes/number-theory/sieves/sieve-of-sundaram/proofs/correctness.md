---
title: The sieve of Sundaram returns exactly the primes up to n
proves: [correctness]
status: full
---

For $n < 2$ there is no prime $p \le n$, and line L1 returns the empty list. Let $n \ge 2$ and $k = \lfloor (n-1)/2 \rfloor$. The map $x \mapsto 2x + 1$ is a bijection from $\{1, \ldots, k\}$ onto the odd numbers $m$ with $3 \le m \le n$: indeed $2x + 1 \le n$ exactly when $x \le (n-1)/2$, that is, when $x \le k$.

**Lemma 1.** For $x \ge 1$, the odd number $2x + 1$ is composite if and only if $x = i + j + 2ij$ for some integers $1 \le i \le j$.

*Proof.* The identity $2(i + j + 2ij) + 1 = (2i+1)(2j+1)$ holds for all integers. If $x = i + j + 2ij$ with $1 \le i \le j$, then $2x + 1$ is the product of two integers that are at least 3, so it is composite. Conversely, if the odd number $m = 2x + 1$ is composite, write $m = ab$ with $1 < a \le b$. Both factors are odd, because $m$ is odd, so $a = 2i + 1$ and $b = 2j + 1$ with $1 \le i \le j$. Then $2x + 1 = (2i+1)(2j+1) = 2(i + j + 2ij) + 1$, so $x = i + j + 2ij$. $\square$

**Lemma 2.** After the loop of line L5 ends, for every $x$ with $1 \le x \le k$, $M[x]$ is true if and only if $x = i + j + 2ij$ for some $1 \le i \le j$.

*Proof.* Line L3 sets every $M[x]$ to false, and line L8 is the only line that writes to $M$; it writes true, at the index $i + j + 2ij$ for the current $i$ and $j$. The inner loop starts at $j = i$ (line L6) and runs while the index is at most $k$, so each written index is of the stated form with $1 \le i \le j$ and lies in $1 \ldots k$.

Conversely, take $1 \le i \le j$ with $x = i + j + 2ij \le k$. The function $f_i(j) = i + j + 2ij$ grows strictly with $j$, so $f_i(i) = 2i + 2i^2 \le f_i(j) \le k$, and the test of line L5 holds for this $i$. The outer loop takes the values $i = 1, 2, \ldots$ in order and stops at the first $i$ that fails line L5; since $f_i(i)$ grows with $i$, every $i$ with $f_i(i) \le k$ is reached. For this $i$, the inner loop takes $j = i, i + 1, \ldots$ and stops at the first $j$ with $f_i(j) > k$; since $f_i$ grows, it reaches our $j$, and line L8 sets $M[x]$ to true. $\square$

*Termination.* For each $i$ the inner loop runs at most $k$ times, since $f_i(j) \ge j$. The outer loop runs at most $k$ times, since $f_i(i) \ge i$.

*Conclusion.* By Lemmas 1 and 2, for $1 \le x \le k$ the flag $M[x]$ is false exactly when $2x + 1$ is an odd prime. By the bijection above, line L11 returns 2 followed by every odd prime $m \le n$, in increasing order. Since every prime other than 2 is odd and $2 \le n$, this is the list of all primes up to $n$. $\blacksquare$
