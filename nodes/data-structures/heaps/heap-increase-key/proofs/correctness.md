---
title: HEAP-INCREASE-KEY leaves a max-heap with the key replaced
proves: [correctness, termination]
status: full
---

Write $p(j) = \lfloor j/2 \rfloor$. An *edge* is a pair $(p(j), j)$ with $2 \le j \le n$, and it *holds* when $A[p(j)] \ge A[j]$. Let $C(i)$ be the set of children of $i$ that exist.

**Invariant.** Before each test of line L3:

> **(U)** each edge $(p(j), j)$ with $j \ne i$ holds, and if $i \ge 2$, then $A[p(i)] \ge A[c]$ for each $c \in C(i)$.

*Initialization.* Let $a$ be the key at $i$ before line L2, so $k \ge a$ by line L1. Before line L2 each edge held. Line L2 changes only the cell $i$. The edges $(i, c)$ held with $a$, so $A[c] \le a \le k$, and they still hold. The edges not touching $i$ are unchanged. The edge $(p(i), i)$ is the one that (U) excludes. If $i \ge 2$, the old edges give $A[p(i)] \ge a \ge A[c]$ for each $c \in C(i)$. So (U) holds.

*Maintenance.* Let the test be true, so $i \ge 2$ and, with $q = p(i)$, $x = A[q] < A[i] = y$. Line L4 swaps them, so $A[q] = y$ and $A[i] = x$. We check the edges with an end at $q$ or $i$, except the edge into $q$, which (U) for the new $i = q$ excludes.

- The edge $(q, i)$: $y \ge x$.
- The edges $(i, c)$ for $c \in C(i)$: the second part of (U) gave $x = A[q] \ge A[c]$, and $A[c]$ did not change.
- The edge $(q, t)$ for the other child $t$ of $q$: it held before, so $A[t] \le x < y$.

So after line L5 each edge except the one into the new $i$ holds. For the second part of (U) at the new $i = q \ge 2$: the edge $(p(q), q)$ held before the swap, because it is not the edge into the old $i$, so $A[p(q)] \ge x$; and the children of $q$ now hold $x$ and $A[t] \le x$. So (U) holds.

*Termination.* Each iteration halves $i$, so the loop stops after at most $\lfloor \lg i \rfloor$ iterations. When it stops, either $i = 1$, and the root has no edge into it, or $A[p(i)] \ge A[i]$, so the excluded edge holds too. With (U), each edge holds.

**Theorem.** If $A[1 \ldots n]$ is a max-heap, $1 \le i \le n$ and $k \ge A[i]$, then after HEAP-INCREASE-KEY$(A, i, k)$ the array is a max-heap, and its multiset of keys is the old one with one copy of the old $A[i]$ replaced by $k$. If $k < A[i]$, it reports an error and changes nothing.

*Proof.* Line L1 handles $k < A[i]$. Else, by the invariant and termination, each edge holds at the end. Line L2 replaced one key by $k$, and the loop only swaps. $\blacksquare$
