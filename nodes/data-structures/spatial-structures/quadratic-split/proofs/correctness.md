---
title: The quadratic split returns two groups of at least m entries, with seeds of largest waste
proves: [correctness, termination]
status: full
---

Let $n \ge 2$ and $1 \le m \le n/2$. Write $r$ for the number of entries that are not yet assigned.

**Seeds.** Lines L1 and L2 compute the waste of every pair $i < j$ and keep a pair whose waste is the largest; $G_1$ and $G_2$ each start with one of the two, and $r = n - 2$.

**Partition.** Each step of the loop moves exactly one entry from the remaining set to one group (line L7), or moves all remaining entries to one group and stops (line L4). An entry is never moved twice. So at the end, $G_1$ and $G_2$ are disjoint and their union is the input.

**Termination.** Each pass of the loop either stops at line L4 or lowers $r$ by 1, and the loop ends when $r = 0$. So there are at most $n - 2$ passes.

**Minimum fill.** We show that at the end $|G_1| \ge m$ and $|G_2| \ge m$. Let $s_k = |G_k| + r$ for $k = 1, 2$.

*Claim: at the start of each pass of line L3 in which line L4 does not fire, $s_1 > m$ and $s_2 > m$; and at the start of every pass, $s_1 \ge m$ and $s_2 \ge m$.* At the start, $s_1 = s_2 = 1 + (n - 2) = n - 1 \ge 2m - 1 \ge m$, since $n \ge 2m$ and $m \ge 1$. Suppose a pass starts with $s_1, s_2 \ge m$. If line L4 fires, the loop stops. Otherwise $s_1 \ne m$ and $s_2 \ne m$, so $s_1 > m$ and $s_2 > m$. The pass moves one entry to one group: the sum $s_k$ of that group does not change, and the sum of the other group drops by 1, so both are still at least $m$ at the start of the next pass. This proves the claim.

Now look at how the loop ends. If line L4 fires for group $k$, then $|G_k| + r = m$ and the $r$ entries go to $G_k$, so $|G_k| = m$; the other group $j$ has $s_j \ge m$ by the claim, and since $r$ entries leave the remaining set and none join $G_j$, its final size is $s_j - r$. We need $s_j - r \ge m$. The two groups and the remaining entries add up to $n$, so $s_j - r = |G_j| = n - |G_k| - r = n - m \ge m$, using $n \ge 2m$. If instead the loop ends with $r = 0$, then $|G_k| = s_k \ge m$ for both groups by the claim.

So the output is a partition of the input into two groups of at least $m$ entries, whose first entries are a pair of largest waste. $\blacksquare$
