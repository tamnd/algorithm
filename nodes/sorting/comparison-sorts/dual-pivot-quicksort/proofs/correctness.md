---
title: Yaroslavskiy's partition splits the range into three parts, and dual-pivot quicksort sorts
proves: [correctness, termination]
status: full
---

Fix a call PARTITION$(A, lo, hi)$ with $lo < hi$. Every change of $A$ is an exchange of two positions in $[lo, hi]$, so the multiset of $A[lo \ldots hi]$ never changes, and no position outside the range changes. After line L8, $p = A[lo] \le q = A[hi]$, and these two positions are not touched by the loop, because all exchanges of lines L12, L15 and L17 use positions $k$, $l$ and $g$, which stay in $[lo+1, hi-1]$, as the invariant shows.

**Invariant.** At each test of line L10:

> **(P)** $lo + 1 \le l \le k$, $l \le g + 1$, $k \le g + 2$ and $g + 1 \le hi$, and
> (a) each item of $A[lo+1 \ldots l-1]$ is less than $p$;
> (b) each item of $A[l \ldots \min(k-1, g)]$ is at least $p$ and at most $q$;
> (c) each item of $A[g+1 \ldots hi-1]$ is at least $q$.

*Initialization.* $l = k = lo + 1$ and $g = hi - 1$, so all three zones are empty, and $lo + 1 \le hi$ because $lo < hi$.

While $k \le g$, the zone (b) is $A[l \ldots k-1]$, and $A[k \ldots g]$ is the unseen zone.

*Maintenance.* Assume (P) and $k \le g$, and let $v = A[k]$.

Case 1, $v < p$ (lines L11, L12). If $l < k$, then $A[l]$ is a middle item by (b), and the exchange puts $v$ at $l$ and the middle item at $k$. If $l = k$, the exchange does nothing. Then $l$ and $k$ grow by 1 (line L18). Zone (a) gains $v < p$, and zone (b) moves one place right with the same items. (P) holds.

Case 2, $p \le v < q$ (the tests of L11 and L13 both fail). Only $k$ grows, and zone (b) gains $v$, with $p \le v \le q$. (P) holds.

Case 3, $v \ge q$ (line L13). The loop of line L14 moves $g$ left while $A[g] > q$ and $k < g$. Each position it passes holds an item greater than $q$, so it can join zone (c). It stops at some $g' \ge k$ with $A[g'] \le q$ or $g' = k$. Line L15 exchanges $A[k]$ and $A[g']$ and sets $g \leftarrow g' - 1$. Now $A[g'+1]$, which is the old $A[k] = v \ge q$ if $g' > k$ or $v$ itself if $g' = k$, is at least $q$, so zone (c) is $A[g' \ldots hi-1]$ after the decrement, and (c) holds. The new $A[k]$ is the old $A[g']$. If $g' = k$ it is $v$ again, line L16 does not move it because $v \ge q \ge p$, and line L18 makes $k = g + 2$. Then $\min(k-1, g) = g$, so zone (b) is the same as before the step, and $v$ is in zone (c). (P) holds, and the loop ends. If $g' > k$, the new $A[k]$ is at most $q$. Line L16 tests it: if it is less than $p$, line L17 moves it into zone (a) as in Case 1; otherwise it is between $p$ and $q$ and joins zone (b) when line L18 increments $k$. In this subcase $g \ge k$ after line L15, so after line L18 $k \le g + 1$, and (P) holds.

*Termination.* In each iteration, $g - k$ drops by at least 1, because $k$ grows by 1 and $g$ never grows. So the loop ends, with $k = g + 1$ or $k = g + 2$.

**The result of PARTITION.** At the end, $k \ge g + 1$, so zone (b) is $A[l \ldots g]$, and the zones (a), (b), (c) cover $A[lo+1 \ldots hi-1]$. Line L19 sets $l \leftarrow l - 1$ and $g \leftarrow g + 1$. Now $A[l]$ is the last item of zone (a), or $A[lo]$ itself if zone (a) is empty, and $A[g]$ is the first item of zone (c), or $A[hi]$ itself if zone (c) is empty. Line L20 exchanges $A[lo]$ with $A[l]$: the item less than $p$ goes to $lo$, inside the left part, and $p$ goes to $l$. Likewise $q$ goes to $g$, and the item at least $q$ goes to $hi$. So:

> $A[l] = p$, $A[g] = q$, $lo \le l < g \le hi$, each item of $A[lo \ldots l-1]$ is less than $p$, each item of $A[l+1 \ldots g-1]$ is between $p$ and $q$, and each item of $A[g+1 \ldots hi]$ is at least $q$.

Here $l < g$ because $l \le g + 1$ before line L19, so $l - 1 < g + 1$.

**DUAL-PIVOT-QUICKSORT sorts.** By induction on $m = hi - lo + 1$. For $m \le 1$, line L1 returns, and the range is sorted. For $m \ge 2$, line L2 only exchanges items inside the range, and PARTITION returns $(l, g)$ as above. The ranges $[lo, l-1]$, $[l+1, g-1]$ and $[g+1, hi]$ do not contain $l$ or $g$, so each has fewer than $m$ items, and by induction the three calls sort them. Each call changes only its own range, so the order relations above still hold: every item left of $l$ is less than $p$, every item between $l$ and $g$ is in $[p, q]$, and every item right of $g$ is at least $q$. Together with the sorted parts this makes $A[lo \ldots hi]$ non-decreasing.

**Termination.** Each call either returns at line L1 or makes three calls on strictly shorter ranges, and PARTITION ends. So the recursion is finite, whatever the random choices of line L2. $\blacksquare$
