---
title: Mo's algorithm with updates makes O(qB + n^2/B + m n^2/B^2) moves
proves: [complexity]
status: full
---

Let $n \ge 1$ be the length of the array, $q$ the number of queries, $m$ the number of updates, $B \ge 1$ the block size and $k = \lceil n / B \rceil$. The queries are sorted by the key $(\lfloor l / B \rfloor, \lfloor r / B \rfloor, t)$, with $0 \le l \le r \le n$ and $0 \le t \le m$. A *group* is a maximal run of queries in the sorted order with the same first two key parts $(a, b)$. Since $a \le b \le \lfloor n / B \rfloor \le k$, there are at most $(k + 1)^2$ groups. Each step of a pointer costs one APPLY, ADD or REMOVE, which is $O(1)$.

**Lemma 1 (time).** The pointer $T$ moves at most $2m (k + 1)^2$ steps.

*Proof.* Within one group the values of $t$ are non-decreasing, so $T$ moves at most $m$ steps forward inside it in total. On entering a group, $T$ moves from the last $t$ of the previous group to the first $t$ of this one, at most $m$ steps. Summing over the groups gives the bound. $\square$

**Lemma 2 (left end).** The pointer $L$ moves $O(q B + n)$ steps.

*Proof.* Between consecutive queries with the same left block, $L$ moves less than $B$. Between consecutive queries whose left blocks are $a < a'$, $L$ moves at most $(a' - a + 1) B$. The left blocks are non-decreasing along the order, so these sum to at most $n + k B + B \le 3n + B$ in total, and the first query costs at most $n$. $\square$

**Lemma 3 (right end).** The pointer $R$ moves $O(q B + n k)$ steps.

*Proof.* Between consecutive queries in the same group, $R$ moves less than $B$. Fix a left block $a$. Among its queries the right block is non-decreasing, so the moves between groups with left block $a$ sum to at most $n + kB = O(n)$, and moving into the first group of $a$ costs at most $n$. Over the at most $k + 1$ left blocks this is $O(n k)$. $\square$

**Theorem.** The total number of steps is $O(q B + n^2 / B + m n^2 / B^2 + n)$. For $q, m \le c n$ and $B = \lceil n^{2/3} \rceil$ it is $O(n^{5/3})$.

*Proof.* Add the three lemmas and use $k \le n / B + 1$. With $B = n^{2/3}$: $q B \le c n^{5/3}$, $n^2 / B = n^{4/3}$ and $m n^2 / B^2 \le c n^{5/3}$. $\square$

The sort takes $O(q \log q)$ comparisons, so the running time is $O(q B + n^2 / B + m n^2 / B^2 + n + q \log q)$.
