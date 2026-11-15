---
title: The posting list operations keep the order and NEXT-GEQ finds the first id at least x
proves: [correctness]
status: full
---

We write $P$ for a posting list with $n = |P|$ entries and $P[i]$ for its $i$-th document id, with $0 \le i < n$. The invariant of the structure is

> **(I)** $P[0] < P[1] < \cdots < P[n-1]$, and $P.\mathit{tf}$ has $n$ entries, each at least 1.

**Lemma 1 (APPEND).** If (I) holds before APPEND$(P, d, f)$ with $f \ge 1$, then the call either reports an error and changes nothing, or it adds $(d, f)$ at the end, and (I) holds after it.

*Proof.* If $n > 0$ and $d \le P[n-1]$, line L1 reports an error before any change. Otherwise $n = 0$, or $P[n-1] < d$. Line L2 adds $d$ at index $n$ and $f$ at the end of $P.\mathit{tf}$. The ids $P[0 \ldots n-1]$ do not change, so they are still strictly increasing, and $P[n-1] < P[n] = d$. Both arrays now have $n + 1$ entries. $\square$

ACCESS reads index $i$ of the two arrays and changes nothing, so it keeps (I).

**Lemma 2 (binary search).** Let $a \le c$ be indices such that $P[a-1] < x$ when $a > 0$, and $P[c] \ge x$ when $c < n$. The loop of lines L8 to L10 ends with $a = c = p$, where $p$ is the least index with $p \ge a$ and $P[p] \ge x$, or $p = n$ if there is none. It makes at most $\lceil \log_2(s+1) \rceil$ comparisons, where $s = c - a$ is the start size.

*Proof.* Under (I), the indices $q \ge a$ with $P[q] < x$ form a prefix of the range, so $p$ is in $[a, c]$ as long as the two conditions hold. Line L9 picks $q$ with $a \le q < c$. If $P[q] < x$, the new $a = q + 1$ has $P[a-1] < x$. Else $P[q] \ge x$, and the new $c = q$ has $P[c] \ge x$. So both conditions hold after each step, and $p$ stays in $[a, c]$. When $a = c$, the range has one index, so $a = p$. Let $s = c - a$ and $q = a + \lfloor s/2 \rfloor$. The new size is $\lfloor s/2 \rfloor$ in the second case, and $s - \lfloor s/2 \rfloor - 1 = \lceil s/2 \rceil - 1 \le \lfloor s/2 \rfloor$ in the first case. So each step makes one comparison and at least halves the size, rounding down. From $s \ge 1$, the size reaches 0 after at most $\lfloor \log_2 s \rfloor + 1 = \lceil \log_2(s+1) \rceil$ steps. $\square$

**Theorem (NEXT-GEQ).** Assume (I) and $lo \ge 0$. NEXT-GEQ$(P, x, lo)$ returns the least index $p \ge lo$ with $P[p] \ge x$, or $n$ if there is none. Let $g = p - lo$ when $lo < n$. The call makes one comparison when $g = 0$, and at most $2 \lfloor \log_2 g \rfloor + 2$ comparisons when $g \ge 1$. It makes no comparison when $lo \ge n$.

*Proof.* If $lo \ge n$, there is no index $p$ with $lo \le p < n$, and line L4 returns $lo$ with no comparison. (The answer "none" is then $lo$ itself, which the caller reads as the end of the list.) If $lo < n$ and $P[lo] \ge x$, line L4 returns $lo$, which is the least such index, after one comparison. So $g = 0$ costs one comparison.

Else $P[lo] < x$. Line L5 sets $b = 1$, so the statement

> **(G)** $b$ is a power of 2 and $P[lo + b - 1] < x$

holds. A step of the loop of line L6 runs only when $P[lo + 2b - 1] < x$, and then doubles $b$, so (G) holds after it. Each step at least doubles $b$ and $lo + 2b - 1 < n$ is needed for a step, so the loop stops. When it stops, either $lo + 2b - 1 \ge n$ or $P[lo + 2b - 1] \ge x$. Line L7 sets $a = lo + b$ and $c = \min(lo + 2b - 1, n)$. By (G), $P[a - 1] < x$. By the stop condition, $c = n$ or $P[c] \ge x$. And $a \le c$, because $lo + b \le lo + 2b - 1$ and $lo + b - 1 < n$ by (G). So Lemma 2 applies, and line L11 returns the least $p \ge a$ with $P[p] \ge x$, or $n$. Each index from $lo$ to $a - 1$ holds an id of at most $P[a-1] < x$ by (I), so this $p$ is also the least $p \ge lo$ with $P[p] \ge x$.

For the count, let $b = 2^t$ at the end of the loop, so the loop made $t$ steps that each made one comparison with result "$<$". The test of line L6 that ends the loop makes one more comparison, unless $lo + 2b - 1 \ge n$. By (G), $P[lo + 2^t - 1] < x$, so $p \ge lo + 2^t$ and $g \ge 2^t$, that is $t \le \lfloor \log_2 g \rfloor$. The binary search starts with size $c - a \le (lo + 2b - 1) - (lo + b) = 2^t - 1$, so by Lemma 2 it makes at most $\lceil \log_2 2^t \rceil = t$ comparisons. The total is at most $1 + t + 1 + t = 2t + 2 \le 2 \lfloor \log_2 g \rfloor + 2$, where the first 1 is line L4. $\blacksquare$

**Consequence.** A sequence of calls NEXT-GEQ$(P, x_j, p_{j-1})$, where each call starts at the answer $p_{j-1}$ of the call before it, with $r$ calls and $\sum_j g_j \le n$, makes at most $\sum_j (2 \log_2(g_j + 1) + 2) \le 2r \log_2(1 + n/r) + 2r$ comparisons. The first step uses $\lfloor \log_2 g \rfloor \le \log_2(g + 1)$ for $g \ge 1$ and $1 \le 2$ for $g = 0$. The second step uses that $\log_2(1 + y)$ is concave, so by Jensen's inequality the sum of $\log_2(1 + g_j)$ is at most $r \log_2(1 + \frac{1}{r} \sum_j g_j)$.
