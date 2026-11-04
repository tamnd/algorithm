---
title: Comb sort sorts the array and stops
proves: [correctness, termination]
status: full
---

Each change of $A$ is an exchange of two items of $A$ (line L8), so $A$ always holds a permutation of the input. It remains to show that the loop of line L3 stops, and that $A$ is sorted when it stops.

**Lemma 1.** If $i < k$ and $A[i] > A[k]$, exchanging $A[i]$ and $A[k]$ lowers the number of inversions of $A$ by at least 1.

*Proof.* Let $x = A[i]$ and $y = A[k]$, with $x > y$. The pair $(i, k)$ is an inversion before the exchange and not after it. Pairs that do not contain $i$ or $k$ do not change. Pairs with one index outside $[i, k]$ keep the same set of two values on the same side, so their number of inversions does not change in total. For an index $m$ with $i < m < k$ and value $z = A[m]$, the pairs $(i, m)$ and $(m, k)$ have $[x > z] + [z > y]$ inversions before and $[y > z] + [z > x]$ after. If $z > x$ the counts are $1$ before and $1$ after. If $z < y$ they are $1$ and $1$. If $y \le z \le x$ they are at least $1$ before, as $x > y$ implies $x > z$ or $z > y$, and $0$ after. So no group of pairs gains inversions, and the pair $(i, k)$ loses one. $\square$

**Lemma 2.** The values of $gap$ at line L5 are non-increasing, and after at most $\lceil \log_{13/10} n \rceil + 1$ passes, $gap = 1$ at each later pass.

*Proof.* Line L4 sets $gap$ to $\max(1, \lfloor 10\, gap / 13 \rfloor)$. If $gap \ge 2$, then $\lfloor 10\, gap/13 \rfloor \le 10\, gap / 13 < gap$, so the value drops, and after $k$ passes it is at most $n (10/13)^k$, which is less than 2 once $k > \log_{13/10} n$. If $gap = 1$, line L4 keeps it at 1. $\square$

**Termination.** By Lemma 2, after finitely many passes each pass has $gap = 1$. Consider a pass with $gap = 1$. If it makes no exchange, line L5 set $done$ to true and line L9 never ran, so the loop stops at the next test of line L3. If it makes an exchange, the number of inversions drops by at least 1, by Lemma 1, and no exchange raises it. The number of inversions is a non-negative integer, so only finitely many passes make an exchange. So the loop stops.

**Correctness at the end.** The loop stops only at a test of line L3 that finds $done$ true. Line L5 sets $done$ to true only when $gap = 1$, and line L9 sets it to false at each exchange. So the last pass had $gap = 1$ and made no exchange: for each $i$ with $0 \le i \le n - 2$, line L7 found $A[i] \le A[i+1]$, and nothing changed $A$ after the test. So each pair of neighbours is in order, and since $\le$ is transitive, $A$ is in non-decreasing order. If $n \le 1$, the pass with $gap = 1$ has no step, and $A$ is sorted. $\blacksquare$
