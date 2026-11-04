---
title: Counting sort sorts the items and keeps equal keys in input order
proves: [correctness, stability]
status: full
---

Write $\kappa(j) = \mathrm{key}(A[j])$ for $0 \le j < n$, and assume that $0 \le \kappa(j) < k$ for each $j$. For a key value $v$ let $N_v = |\{j : \kappa(j) = v\}|$ and let $S_v = \sum_{u < v} N_u$, the number of items with a key less than $v$. Block $v$ is the index range $[S_v, S_v + N_v)$ of $B$. The blocks for $v = 0, \ldots, k-1$ are disjoint, they follow each other in order of $v$, and together they cover $[0, n)$, because $S_{v+1} = S_v + N_v$ and $S_k = n$.

**Step 1 (pass 1).** At the test of line L2 with index $i$, $C[v] = |\{j < i : \kappa(j) = v\}|$ for each $v$. This holds for $i = 0$ by line L1. Line L3 adds 1 to exactly the entry $v = \kappa(i)$, so it holds for $i + 1$. When the loop stops, $i = n$ and $C[v] = N_v$.

**Step 2 (pass 2).** At the test of line L5 with index $v$, we claim that $s = S_v$, that $C[u] = S_u$ for $u < v$, and that $C[u] = N_u$ for $u \ge v$. For $v = 0$ this holds by line L4 and Step 1, since $S_0 = 0$. Line L6 saves $t = N_v$, sets $C[v] = s = S_v$, and sets $s = S_v + N_v = S_{v+1}$. So the claim holds for $v + 1$. At the end, $C[v] = S_v$ for each $v$.

**Step 3 (pass 3).** Let $P_v(i) = (j_1 < j_2 < \cdots < j_m)$ be the indices $j < i$ with $\kappa(j) = v$, in increasing order. The invariant at the test of line L8 with index $i$ is:

> **(P)** For each $v$, $C[v] = S_v + |P_v(i)|$, and $B[S_v + r - 1] = A[j_r]$ for $r = 1, \ldots, |P_v(i)|$.

For $i = 0$ each $P_v(0)$ is empty and $C[v] = S_v$ by Step 2, so (P) holds. Assume (P) at index $i$, and let $v = \kappa(i)$. Then $P_v(i+1)$ is $P_v(i)$ followed by $i$. Line L9 writes $A[i]$ at index $C[v] = S_v + |P_v(i)|$. This index is in block $v$, because $|P_v(i)| < N_v$: the item $i$ itself has key $v$ and is not in $P_v(i)$. So the write does not touch the slots of another block, and it does not touch the earlier slots of block $v$. Line L10 adds 1 to $C[v]$. The lists and counters of all other keys do not change. So (P) holds at index $i + 1$.

**Step 4 (the result).** When the loop stops, $i = n$, and (P) says that block $v$ holds the $N_v$ items with key $v$, in increasing order of their input index, for each $v$. The blocks cover $B$ and are in order of $v$. So each slot of $B$ is written exactly once, $B$ holds each item of $A$ exactly once, the keys in $B$ are non-decreasing, and items with equal keys appear in their input order. $\blacksquare$

**Termination.** Each of the three loops has a fixed range of $n$ or $k$ steps, and each step does a fixed number of operations.
