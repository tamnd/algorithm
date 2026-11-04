---
title: RANK counts the smaller keys, and PUT and DELETE keep the arrays sorted
proves: [correctness]
status: full
---

**Invariant (I).** $keys[0] < \cdots < keys[n-1]$, and the table holds exactly the pairs $(keys[i], vals[i])$ for $0 \le i < n$.

For a key $k$, let $r(k) = \lvert \{ i < n : keys[i] < k \} \rvert$. Under (I), the keys less than $k$ are exactly $keys[0..r(k) - 1]$, and if $k$ is in the table, it is $keys[r(k)]$.

**Lemma (RANK).** Under (I), RANK$(T, k)$ returns $r(k)$ after at most $\lfloor \lg n \rfloor + 1$ passes of the loop.

*Proof.* We use the loop invariant

> (R) $0 \le lo \le hi + 1 \le n$, every key in $keys[0..lo-1]$ is less than $k$, and every key in $keys[hi+1..n-1]$ is greater than $k$.

Line L1 sets $lo = 0$ and $hi = n - 1$; both ranges are empty and (R) holds. In a pass, $lo \le hi$, and line L3 gives $lo \le mid \le hi$. If $k < keys[mid]$, then since the keys increase, every key in $keys[mid..n-1]$ is greater than $k$, and line L4 sets $hi = mid - 1 \ge lo - 1$; (R) holds. If $k > keys[mid]$, every key in $keys[0..mid]$ is less than $k$, and line L5 sets $lo = mid + 1 \le hi + 1$; (R) holds. Otherwise $keys[mid] = k$, and line L6 returns $mid$; since the keys increase strictly, exactly the $mid$ keys before it are less than $k$, so $mid = r(k)$.

If the loop ends, $lo > hi$, and with (R), $lo = hi + 1$. Then the two ranges of (R) cover all $n$ indices, so exactly $lo$ keys are less than $k$, and line L7 returns $lo = r(k)$.

*Passes.* Let $s = hi - lo + 1$ be the size of the range. Line L3 splits it into $mid - lo = \lfloor (s - 1)/2 \rfloor$ cells to the left of $mid$ and $s - 1 - \lfloor (s - 1)/2 \rfloor = \lceil (s - 1)/2 \rceil$ to the right. Either way the new size is at most $\lfloor s / 2 \rfloor$. Starting from $s = n$, after $t$ passes $s \le \lfloor n / 2^t \rfloor$, which is 0 for $t = \lfloor \lg n \rfloor + 1$. So there are at most $\lfloor \lg n \rfloor + 1$ passes. $\square$

**GET$(T, k)$.** By the lemma, line L8 finds $i = r(k)$. If $k$ is in the table, it is $keys[i]$, and line L8 returns its value $vals[i]$ by (I). If it is not, then either $i = n$ or $keys[i] \ne k$, and line L8 returns NIL. Nothing is written.

**PUT$(T, k, v)$.** Let $i = r(k)$ from line L9. If $i < n$ and $keys[i] = k$, line L10 replaces the value of $k$ and changes no key, so (I) holds for the table with $(k, v)$ in place of the old pair of $k$. Otherwise $k$ is not in the table, and $keys[0..i-1] < k < keys[i..n-1]$. The loop of line L11 runs $j = n, n - 1, \ldots, i + 1$. At step $j$ it copies cell $j - 1$ to cell $j$. Cell $j$ is either the free cell $n$ (for $j = n$) or a cell already copied at step $j + 1$; cell $j - 1$ is not yet written. So after the loop, $keys[j] $ holds the old $keys[j - 1]$ for $i < j \le n$, and cells $0..i - 1$ are unchanged; the same holds for $vals$. Line L12 writes $(k, v)$ at index $i$ and sets the count to $n + 1$. The new key sequence is $keys[0..i-1], k, $ old $keys[i..n-1]$, which is strictly increasing, and the pairs are the old pairs and $(k, v)$. So (I) holds.

**DELETE$(T, k)$.** Let $i = r(k)$. If $k$ is not in the table, line L13 returns and nothing changes. Otherwise $keys[i] = k$. The loop of line L14 runs $j = i, \ldots, n - 2$ and copies cell $j + 1$ to cell $j$. Cell $j + 1$ has not yet been written by the loop, so after it, cell $j$ holds the old cell $j + 1$ for $i \le j \le n - 2$. Line L15 sets the count to $n - 1$. The new key sequence is the old one without $keys[i]$, which is still strictly increasing, and the pairs are the old pairs without the pair of $k$. So (I) holds.

**Order operations.** Under (I), $keys[0]$ is the least key, $keys[n-1]$ the greatest, and $keys[i]$ has exactly $i$ smaller keys, so it is select$(i)$. For ceiling, $keys[r(k)]$ is the least key $\ge k$, since all earlier keys are less than $k$. For floor, if $keys[r(k)] = k$ it is the answer; otherwise every key $\ge k$ is greater than $k$, and the largest key less than $k$ is $keys[r(k) - 1]$. The keys in $[lo, hi]$ are those with index from $r(lo)$ to $r(hi) - 1$, plus $keys[r(hi)]$ if it equals $hi$; their count is $r(hi) - r(lo)$, plus 1 in that case. $\blacksquare$
