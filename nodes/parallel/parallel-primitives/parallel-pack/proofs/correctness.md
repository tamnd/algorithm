---
title: The pack writes the kept items to distinct positions in their order, in linear work and logarithmic span
proves: [correctness]
status: full
---

**Statement.** Let $A[0 \ldots n-1]$ be an array with $n \ge 1$ and let keep be a predicate that takes $O(1)$ time. Let $i_0 < i_1 < \cdots < i_{k-1}$ be the indices with keep$(A[i])$ true. Then PARALLEL-PACK returns $B[0 \ldots k-1]$ with $B[r] = A[i_r]$ for every $r$. Every write on line L5 goes to a different cell, so the algorithm needs no concurrent writes. With the [Blelloch scan](/blelloch-scan/) on line L2 and $K = \lceil \lg n \rceil$, $m = 2^K$, it does exactly $W = 2n + 2(m - 1) < 6n$ operations in $2 + 2K$ parallel rounds, so the work is $\Theta(n)$ and the span is $\Theta(\log n)$.

## 1. The positions

Line L1 sets $F[i] = 1$ if keep$(A[i])$ is true and $F[i] = 0$ otherwise. Line L2 is an exclusive $+$-scan, so by the correctness of the Blelloch scan,
$$
X[i] = \sum_{j < i} F[j] \quad \text{for } 0 \le i < n, \qquad k = \sum_{j < n} F[j].
$$
So $X[i]$ is the number of kept indices before $i$, and $k$ is the number of kept indices.

**Lemma.** For every $r$ with $0 \le r < k$, $X[i_r] = r$.

*Proof.* The kept indices before $i_r$ are exactly $i_0, \ldots, i_{r-1}$, because the list $i_0 < i_1 < \cdots$ contains every kept index in increasing order. So their number is $r$. $\square$

## 2. The scatter

On line L5, processor $i$ writes only if $F[i] = 1$, that is, if $i = i_r$ for some $r$, and then it writes $A[i_r]$ to $B[X[i_r]] = B[r]$ by the lemma. Different kept indices $i_r$ and $i_{r'}$ with $r \ne r'$ write the different cells $B[r]$ and $B[r']$, so no cell has two writers, and the step is exclusive write. Every $r$ in $0, \ldots, k-1$ is written by $i_r$, so every cell of $B$ is written once, and no write leaves the array, since $0 \le r < k$. So after line L5, $B[r] = A[i_r]$ for every $r$, which is the claim. In particular, the order of the kept items is kept: $r < r'$ if and only if $i_r < i_{r'}$.

The reads are also exclusive: processor $i$ reads only $F[i]$, $X[i]$ and $A[i]$. The scan on line L2 runs on the EREW PRAM. So the whole algorithm runs on the EREW PRAM.

## 3. Cost

Count one operation for each evaluation of the predicate on line L1, for each $+$ in the scan, and for each iteration of the loop on lines L4 and L5.

- Line L1 does $n$ operations in one round.
- The Blelloch scan pads the flags to length $m = 2^K$. The up-sweep does $m/2 + m/4 + \cdots + 1 = m - 1$ additions in $K$ rounds, and the down-sweep does $m - 1$ additions in $K$ rounds, so line L2 does $2(m - 1)$ operations in $2K$ rounds.
- Lines L4 and L5 do $n$ operations in one round.

So $W = 2n + 2(m - 1)$ and the number of rounds is $2 + 2K$. Since $m < 2n$, $W < 2n + 4n = 6n$, and $W \ge 2n$, so $W = \Theta(n)$. The number of rounds is $2 + 2 \lceil \lg n \rceil = \Theta(\log n)$. Each round is a set of independent operations, so in the work-span model the span is $\Theta(\log n)$ when each parallel loop is a PRAM step; with the loops of lines L1 and L4 implemented as balanced fork-join trees, each loop adds $\Theta(\log n)$, and the span stays $\Theta(\log n)$. The extra space is the arrays $F$ and $X$, which is $\Theta(n)$. $\blacksquare$
