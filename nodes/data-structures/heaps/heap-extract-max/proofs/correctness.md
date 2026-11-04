---
title: HEAP-EXTRACT-MAX returns a largest key and leaves a max-heap
proves: [correctness, termination]
status: full
---

Write $s$ for $A.\mathit{heap\text{-}size}$ and $p(j) = \lfloor j/2 \rfloor$. An *edge* is a pair $(p(j), j)$ with $2 \le j \le s$, and it *holds* when $A[p(j)] \ge A[j]$. Let $C(i)$ be the set of children of $i$ that exist, a subset of $\{2i, 2i + 1\}$ of indices at most $s$.

**Lemma (MAX-HEAPIFY).** Let $1 \le i \le s$ and assume

> **(D)** each edge $(p(j), j)$ with $p(j) \ne i$ holds, and if $i \ge 2$, then $A[p(i)] \ge A[c]$ for each $c \in C(i)$.

Then MAX-HEAPIFY$(A, i)$ stops after at most $\lfloor \lg(s/i) \rfloor$ swaps, only permutes the keys of $A[1 \ldots s]$, and afterwards each edge holds.

*Proof.* We show that (D) is an invariant of the loop of line L7 for the current $i$. It holds at the start. Lines L8 to L10 set $m$ to an index of a largest key among $A[i]$ and $A[c]$ for $c \in C(i)$: line L9 tests the left child against $A[i]$, line L10 tests the right child against the larger of the two, and each test is made only for a child that exists.

If $m = i$, then $A[i] \ge A[c]$ for each $c \in C(i)$, so the edges out of $i$ hold, and with (D) every edge holds. Line L11 returns.

Else let $x = A[i]$ and $y = A[m]$, so $y > x$, and $y \ge A[t]$ for the other child $t$ of $i$ if it exists. Line L12 swaps them. Then the edge $(i, m)$ holds because $y \ge x$, the edge $(i, t)$ holds because $y \ge A[t]$, and the edge $(p(i), i)$, if $i \ge 2$, holds because (D) gave $A[p(i)] \ge A[m] = y$. Other edges with an end at $i$ or $m$ are the edges out of $m$, which (D) for the new value $i = m$ excludes. For the second part of (D) at $m$: its parent now holds $y$, and each child $c$ of $m$ had $A[c] \le y$ before the swap, because the edges out of $m$ were not excluded. So (D) holds for the new $i$.

Each swap moves $i$ one level down. The subtree of the first $i$ has height $\lfloor \lg(s/i) \rfloor$, so there are at most that many swaps, and then the next iteration finds $m = i$, at the latest at a leaf. The only changes are swaps. $\square$

**Theorem.** Let $A[1 \ldots n]$ be a max-heap with $n \ge 1$. Then HEAP-EXTRACT-MAX returns a largest key of $A$, and afterwards $A[1 \ldots n - 1]$ is a max-heap whose multiset of keys is the old one with one copy of the returned key removed. With $n = 0$ it reports an error. It stops.

*Proof.* Line L1 handles $n = 0$. Let $n \ge 1$. Each $j$ has the root $1$ as an ancestor, and the edges on the path from $1$ to $j$ hold, so $A[1] \ge A[j]$ by a chain of inequalities. So $\mu = A[1]$, saved at line L2, is a largest key. Lines L3 and L4 write the old $A[n]$ into the root and set $s = n - 1$, so the keys of $A[1 \ldots s]$ are the old keys with one copy of $\mu$ removed (if $n = 1$, the array is empty and the claim holds). Each edge $(p(j), j)$ with $p(j) \ne 1$ and $j \le s$ joins two cells other than the root, whose keys did not change, so it holds; and the root has no parent. So (D) holds with $i = 1$, and by the lemma, after line L5 each edge holds and the keys were only permuted. Line L6 returns $\mu$. $\blacksquare$
