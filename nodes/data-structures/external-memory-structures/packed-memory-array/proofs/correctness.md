---
title: The packed memory array keeps the keys sorted, always has room, and every operation ends
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The array has capacity $c$, a power of two, and segments of $S$ cells with $S$ dividing $c$, so the windows at each height $i \le H$ are well defined: the aligned runs of $S 2^i$ cells, and the window at height $H$ is the whole array. The thresholds satisfy $\tau_i \le \tau_0 = 1$ for all $i$. Let the *key sequence* be the keys of `slots` read from left to right, skipping gaps.

**Invariant (I).** The key sequence is strictly increasing, and it is the set stored.

**Lemma 1 (search).** If (I) holds, the binary search of line L1 returns the position of the largest key at most $k$, or $-1$ if there is none.

*Proof.* The search keeps $lo \le hi$ and the property: every key at a position before $lo$ is at most $k$, and every key at a position at or after $hi$ is larger than $k$. This holds at the start with $lo = 0$, $hi = c$. In a pass, let $mid$ be the midpoint and $j$ the first position at or after $mid$, before $hi$, that holds a key. If there is none, the cells from $mid$ to $hi$ are gaps, so setting $hi \leftarrow mid$ keeps the property. If the key $x$ at $j$ is at most $k$, then by (I) all keys before $j$ are smaller than $x$, so setting $lo \leftarrow j + 1$ keeps it. If $x > k$, all keys after $j$ are larger, and the cells from $mid$ to $j$ are gaps, so setting $hi \leftarrow mid$ keeps it. Each pass makes $hi - lo$ smaller, since $mid < hi$ and $j + 1 > mid \ge lo$, so the loop ends with $lo = hi$. Then the keys before $lo$ are exactly the keys at most $k$, and the last of them, found by the scan to the left over gaps, is the largest such key. $\square$

**Lemma 2 (insert).** If (I) holds and $k$ is absent, INSERT adds $k$, and (I) holds after it.

*Proof.* Let $p$ be the position from Lemma 1 (use segment 0 if $p = -1$). In line L5, the window $W$ holds position $p$ (or position 0). All keys before $W$ are at positions before $p$ or at $p$, so they are at most the predecessor of $k$, which is less than $k$; all keys after $W$ are after $p$, so they are larger than $k$ by Lemma 1. REBALANCE (line L12) collects the keys of $W$ in order, adds $k$ at its place, and writes them back in order. The test of line L4 gives $\mathrm{keys}(W) + 1 \le \tau_i |W| \le |W|$, so there are enough cells, and the spread positions $\lfloor t |W| / m \rfloor$ for $t = 0, \ldots, m - 1$ are distinct and increasing because $|W| \ge m$. So the new key sequence is the old keys before $W$, then the keys of $W$ with $k$, then the old keys after $W$: strictly increasing, with $k$ added. If no window passes the test, RESIZE (line L13) collects all keys in order with $k$ added, and picks a capacity $c' \ge 2\sqrt{2}\, m > m$, so the spread fits, and it is in order. $\square$

**Lemma 3 (delete).** If (I) holds, DELETE removes $k$ if it is present and changes nothing otherwise, and (I) holds after it.

*Proof.* By Lemma 1, line L7 finds $k$ if it is present. Making its cell a gap removes $k$ from the key sequence and keeps it increasing. A later REBALANCE of a window rewrites its keys in the same order in the same window, which keeps (I), as does a RESIZE, by the argument of Lemma 2 with no key added. $\square$

**Range and membership.** By (I), `range(a, b)` starts at the first key at least $a$, found from Lemma 1, and reads the keys in increasing order, stopping at the first key larger than $b$; so it returns exactly the keys in $[a, b]$. `contains(k)` is true exactly when the predecessor of $k$ is $k$.

**Termination.** The loops of lines L2 and L8 run over at most $H + 1$ heights. REBALANCE and RESIZE are single passes over a finite list; the capacity loop in RESIZE doubles $c'$ until it passes a finite bound. The binary search ends by Lemma 1. So every operation ends.

**The structure stays valid.** After a RESIZE, $c'$ is a power of two and $S$ is recomputed as a power of two at most $c'$, so $S$ divides $c'$. Every window holds at most its size in keys, because a write only puts keys at distinct cells.

The empty array satisfies (I), and by Lemmas 2 and 3, every update keeps it; inserting a present key changes nothing. So (I) holds after every sequence of operations, and the answers of all queries are right. $\blacksquare$
