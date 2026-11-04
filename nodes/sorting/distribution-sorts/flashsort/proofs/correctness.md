---
title: Flashsort sorts its input
proves: [correctness, termination]
status: full
---

Assume $n \ge 2$ and $lo < hi$; otherwise lines L1 and L2 return an array that is already sorted. The class map $K$ is non-decreasing, with $K(lo) = 0$ and $K(hi) = m - 1$, and $0 \le K(x) \le m - 1$ for $lo \le x \le hi$. Let $C[k]$ be the count of line L4, $end[k] = C[0] + \cdots + C[k]$ the value of $top[k]$ after line L5, and $start[k] = end[k] - C[k]$. The blocks $[start[k], end[k])$ are disjoint, in the order of $k$, and cover $[0, n)$.

Call position $p$ *placed* if $p \in [top[k], end[k])$ for the class $k$ whose block contains $p$. Placed positions hold keys of the class of their block, as we show.

**Invariant (P).** At each test of line L7:

> **(P1)** each placed position $p$ in block $k$ holds a key of class $k$;
> **(P2)** for each $k$, the number of keys of class $k$ at positions that are not placed is $top[k] - start[k]$;
> **(P3)** every position $p < i$ is placed;
> **(P4)** $A$ is a permutation of the input.

At the start no position is placed, $top[k] = end[k]$, and there are $C[k] = end[k] - start[k]$ keys of class $k$, so (P1) to (P4) hold with $i = 0$.

**Line L8.** Let $i < n$, let $b$ be the block that contains $i$, and let $k = K(A[i])$. If $i$ is placed, then $k = b$ by (P1), and $i \ge top[b]$, so line L8 moves on, and (P3) holds for $i + 1$. If $i$ is not placed, then $start[b] \le i < top[b]$. By (P3), all positions of $[start[b], i)$ are placed, and since the placed positions of block $b$ are $[top[b], end[b])$, this means $i = start[b]$. Now $k \ge b$: if $k < b$, then the block of $k$ lies before $i$ and is fully placed by (P3), so $top[k] = start[k]$, and by (P2) there is no key of class $k$ at a position that is not placed, but $A[i]$ is one. If $k = b$, then $i < top[k]$. If $k > b$, then $i < end[b] \le start[k] \le top[k]$. So in both cases line L8 does not skip, and line L9 starts a cycle with $x = A[i]$.

**The cycle of line L10.** During the cycle, position $i$ is treated as empty: its content is the leader, which is also in hand. We claim that before each step, the key in hand $x$ is a key of some class $k$ that is not yet placed, and $top[k] - 1$ is a position that is not placed, at or after $i$. By (P2) applied with $x$ counted at its old position, $top[k] - start[k] \ge 1$, so $top[k] - 1 \ge start[k]$ is in block $k$ and not placed. If $k$'s block lies before $i$, it is fully placed by (P3), which contradicts the existence of $x$, so $top[k] - 1 \ge i$. The step decreases $top[k]$, so the position $top[k]$ is now placed and holds $x$, a key of class $k$: (P1) holds. The key that was there was at a position that was not placed; it is now in hand, and (P2) holds for its class, because it is counted as not placed until it is put down. If the position was $i$, the key that was there is the stale copy of the leader, which is already accounted for, and the cycle ends with $A[i]$ placed. Each step places one more position, and there are finitely many, so the cycle ends. The cycle can end only at position $i$, so when it ends, $i$ is placed and holds a key of its block; the leader was put down in the cycle at its own place; and each key of the input is again at exactly one position, so (P4) holds. Then (P3) holds for $i + 1$ at the next test.

**Termination of the loop.** Each turn of line L7 either increases $i$ or runs a cycle that places at least one position and then the next turn increases $i$ at line L8. So the loop ends with $i = n$.

**After the loop.** By (P3) every position is placed, and by (P1) block $k$ holds keys of class $k$. Since $K$ is non-decreasing, a key of a lower class is not larger than a key of a higher class. So the array is a permutation of the input in which every inversion is between two keys of the same block.

**Line L11.** Insertion sort sorts any array, so the result is sorted. $\blacksquare$
