---
title: The Amir-Lewenstein-Porat algorithm reports exactly the k-mismatch occurrences
proves: [correctness]
status: full
---

Indices are 0-based, $|P| = m$, $|T| = n$, $k \ge 0$, and $h_i$ is the number of $q \in \{0, \ldots, m-1\}$ with $P[q] \ne T[i + q]$, for $0 \le i \le n - m$. The claim is that ALP-K-MISMATCH returns the set $\{\, i : 0 \le i \le n - m,\ h_i \le k \,\}$ in increasing order. If $m > n$ there is no start position, and the algorithm returns nothing. Assume $m \le n$ from now on.

**Line L1.** If $k \ge m$, then $h_i \le m \le k$ for every $i$, so every start position is an occurrence, which is what line L1 returns. Assume $k < m$ from now on. Then $m \ge 1$.

**The parameters.** Since $f \ge 1$ and $g = \lceil 2k / f \rceil$, we have $g f \ge 2k$. Each symbol of $F$ occurs at least $f$ times in $P$, so in case A line L4 can choose $f$ distinct positions of each of $g$ distinct symbols of $F$. Let $M$ be this set of marks. Then $|M| = g f$, and $P[q]$ is one of the chosen symbols for each $q \in M$.

## Lemma 1: the counts of case A

After line L5, $count[i]$ is the number of marks $q \in M$ with $P[q] = T[i + q]$, for $0 \le i \le n - m$.

*Proof.* Line L5 adds 1 to $count[i]$ once for each pair $(j, q)$ with $q \in M$, $P[q] = T[j]$ and $j - q = i$. For a fixed $i$, the map $q \mapsto (i + q, q)$ is a bijection from the marks $q$ with $P[q] = T[i + q]$ onto these pairs, since $j = i + q$ is determined by $q$, and $0 \le i + q \le n - 1$ holds because $0 \le i \le n - m$ and $0 \le q \le m - 1$. $\square$

## Lemma 2: the filter keeps every occurrence

If $h_i \le k$, then $count[i] \ge g f - k$.

*Proof.* The marks with $P[q] \ne T[i + q]$ are some of the $h_i$ mismatched positions, so there are at most $h_i \le k$ of them. By Lemma 1, $count[i] \ge |M| - k = g f - k$. $\square$

## Lemma 3: the kangaroo check

KANGAROO($i$) succeeds if and only if $h_i \le k$.

*Proof.* Let $h = h_i$, let $q_1 < q_2 < \cdots < q_h$ be the mismatched positions of alignment $i$, and let $q_0 = -1$ and $q_{h+1} = m$. We claim that for $e = 0, 1, \ldots$, if the loop has not stopped, its iteration number $e + 1$ starts with $q = q_e + 1$ and the counter equal to $e$. This holds for $e = 0$. In this iteration, $P[q'] = T[i + q']$ for $q_e < q' < q_{e+1}$, and $P[q_{e+1}] \ne T[i + q_{e+1}]$ when $q_{e+1} < m$. So the longest common prefix of $P[q \ldots m-1]$ and $T[i + q \ldots n-1]$ has length $q_{e+1} - q$, and $q$ becomes $q_{e+1}$. If $e = h$, then $q = m$, and the check succeeds. Otherwise the counter becomes $e + 1$; the check fails if $e + 1 > k$, and else $q$ becomes $q_{e+1} + 1$, which proves the claim for $e + 1$. So the check fails in iteration $e + 1$ for the least $e < h$ with $e + 1 > k$, which exists if and only if $h > k$; and when $h \le k$, it reaches iteration $h + 1$ and succeeds. $\square$

Each step makes one extension query, and the check fails at the latest at the $(k+1)$st mismatch, so it makes at most $k + 1$ queries. A query at $q < m$ reads the suffix of $T$ from $i + q \le n - 1$, so it is defined.

## Case A is correct

Line L6 returns the $i$ with $count[i] \ge g f - k$ for which KANGAROO($i$) succeeds, in increasing order. By Lemma 3, every returned $i$ has $h_i \le k$. Conversely, if $h_i \le k$, Lemma 2 shows that $i$ passes the filter, and Lemma 3 shows that the check succeeds, so $i$ is returned.

## Case B is correct

We show that after lines L8 and L9, $match[i] = m - h_i$, the number of $q$ with $P[q] = T[i + q]$. Split these $q$ by the symbol $c = P[q] = T[i + q]$.

- If $c \in F$, line L8 adds the correlation for $c$, which counts at $i$ exactly the $q$ with $P[q] = c$ and $T[i + q] = c$. Each block of $T$ of length $2m - 1$ starting at $b$ holds the windows of the starts $i = b, \ldots, b + m - 1$, and the blocks start at $0, m, 2m, \ldots$, so each start $i \le n - m$ is computed in exactly one block. The transform computes the correlation exactly: with a number-theoretic transform modulo a prime $p > m$ each value is at most $m < p$, and with a floating-point transform each value is rounded to the nearest integer.
- If $c$ is rare, line L9 adds 1 at $i$ for the pair $(j, q) = (i + q, q)$, since $T[j] = c$ is rare and $P[q] = T[j]$, and for no other pair with this $q$, by the bijection of Lemma 1.

A pair $(i, q)$ with $P[q] \ne T[i + q]$ is counted by neither line: the correlation for $c$ needs $P[q] = T[i + q] = c$, and line L9 needs $P[q] = T[j]$. So $match[i] = m - h_i$, and line L10 returns exactly the $i$ with $h_i \le k$, in increasing order.

## Conclusion

Lines L3 to L10 run exactly one of the two cases, and each returns the set of occurrences. With line L1, ALP-K-MISMATCH is correct for all $k \ge 0$ and all strings, including the empty pattern, which line L1 handles because $k \ge 0 = m$. $\blacksquare$
