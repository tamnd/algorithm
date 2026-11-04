---
title: BUILD-BY-INSERTION makes the array a max-heap
proves: [correctness, termination]
status: full
---

Write $p(j) = \lfloor j/2 \rfloor$. For $m \le n$, an *edge of the prefix* $A[1 \ldots m]$ is a pair $(p(j), j)$ with $2 \le j \le m$, and it *holds* when $A[p(j)] \ge A[j]$. The prefix is a max-heap when each of its edges holds. Let $C_m(i)$ be the set of children of $i$ that are at most $m$.

**Outer invariant.** Before the test of line L1 with the value $j$, the prefix $A[1 \ldots j - 1]$ is a max-heap, and $A$ is a permutation of the input.

*Initialization.* For $j = 2$, the prefix $A[1 \ldots 1]$ has no edges.

*Maintenance.* Fix $j$ and consider lines L2 to L5 with $m = j$. Before each test of line L3, we claim:

> **(I)** each edge $(p(t), t)$ of $A[1 \ldots j]$ with $t \ne i$ holds, and if $i \ge 2$, then $A[p(i)] \ge A[c]$ for each $c \in C_j(i)$.

When line L2 sets $i = j$, the cell $j$ has no children in $A[1 \ldots j]$, because $2j > j$. The edges of $A[1 \ldots j]$ other than $(p(j), j)$ are the edges of $A[1 \ldots j - 1]$, which hold by the outer invariant. The second part holds because $C_j(j)$ is empty. So (I) holds.

Let the test of line L3 be true, so $i \ge 2$ and, with $q = p(i)$, $x = A[q] < A[i] = y$. Line L4 swaps them. We check the edges with an end at $q$ or $i$, except the edge into $q$.

- The edge $(q, i)$ now holds, since $y > x$.
- For $c \in C_j(i)$, the edge $(i, c)$: by the second part of (I), $x \ge A[c]$, and $A[c]$ did not change.
- For the other child $t$ of $q$, if $t \le j$: the edge $(q, t)$ held before, so $A[t] \le x < y$.

Line L5 sets $i = q$. So each edge except the one into the new $i$ holds. If the new $i \ge 2$, the edge $(p(q), q)$ held before the swap, since it was not the edge into the old $i$; so $A[p(q)] \ge x \ge A[t]$, and the children of $q$ now hold $x$ and $A[t]$. So (I) holds again.

Each iteration halves $i$, so the inner loop stops after at most $\lfloor \lg j \rfloor$ iterations. When it stops, either $i = 1$, which has no edge into it, or $A[p(i)] \ge A[i]$. With (I), each edge of $A[1 \ldots j]$ holds, so $A[1 \ldots j]$ is a max-heap. The loop only swaps cells, so $A$ is still a permutation of the input. This is the outer invariant for $j + 1$.

*Termination.* The outer loop runs for $j = 2, \ldots, n$, and each inner loop stops, as shown. When the outer loop ends, $j = n + 1$, and the outer invariant says that $A[1 \ldots n]$ is a max-heap.

**Theorem.** For each array $A[1 \ldots n]$ with $n \ge 0$, BUILD-BY-INSERTION$(A, n)$ stops, and after it $A$ is a max-heap that is a permutation of the input. Moreover, after the iteration with the value $j$, the prefix $A[1 \ldots j]$ is a max-heap, and the iteration does not read or write a cell beyond $j$.

*Proof.* The first two claims are the invariant at the end and termination. The last claim holds because the inner loop reads and writes only the cells $i$ and $p(i)$ with $i \le j$. So the method is online: it can run while the keys arrive. $\blacksquare$
