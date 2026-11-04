---
title: Expected and amortized cost of the chained hash table
proves: [time.expected, time.worst]
status: full
---

Count the cost of an operation on key $k$ as 1 for the hash and the bucket index, plus 1 for each pair that the scan of bucket $b_m(k)$ examines. The cost of a call of RESIZE$(T, m')$ is $m' + n$: one for each new list and one for each pair moved.

**Claim 1 (worst case).** Some sets of keys make an operation cost $\Theta(n)$.

*Proof.* The scan of a bucket examines at most all $n$ pairs, so each operation costs $O(n)$ without the resize, and a resize from line L6 costs $2m + n = O(n)$ since $m < n$. For the lower bound, fix $h$ and $m$, and start with $m$ buckets where $m \ge n$, so that $n$ inserts cause no resize. If the key universe has at least $(n - 1) m + 1$ keys, then by the pigeonhole principle some $n$ keys have the same bucket $b_m$. Insert these $n$ keys. Their bucket holds all $n$ pairs, and a search for the key that is last in that list examines $n$ pairs. $\square$

**Claim 2 (expected cost without the resize).** Let $h$ be drawn from a family $\mathcal{H}$ such that, for each two distinct keys $x \ne y$, $\Pr_{h \in \mathcal{H}}[b_m(x) = b_m(y)] \le 1/m$. Let the table hold a set $S$ of $n$ keys that does not depend on the choice of $h$. Then the expected cost of a search, an insert (before line L6) or a delete of a key $k$ is at most $2 + \alpha$, where $\alpha = n/m$.

*Proof.* For $y \in S$ with $y \ne k$, let $X_y = 1$ if $b_m(y) = b_m(k)$, and $X_y = 0$ else. Then $E[X_y] = \Pr[b_m(y) = b_m(k)] \le 1/m$. The scan examines only pairs of bucket $b_m(k)$, which are $k$ itself (if $k \in S$) and the keys $y$ with $X_y = 1$. So the cost is at most $1 + 1 + \sum_{y \in S, y \ne k} X_y$. By linearity of expectation, the expected cost is at most $2 + \sum_{y \ne k} E[X_y] \le 2 + n/m = 2 + \alpha$. $\square$

By (H4), $\alpha \le 1$ after each operation, and during an insert $n \le m + 1$ before line L6, so $\alpha \le 2$. Hence each operation costs $O(1)$ in expectation, without the resize.

**Claim 3 (the resizes are amortized).** Start with an empty table of $m_0 \ge 1$ buckets, and apply $s$ operations. Then the total cost of all calls of RESIZE is less than $8s$.

*Proof.* A resize happens only at line L6, when $n = m + 1$, and it doubles $m$. If there is no resize, the total is 0. Else let $r + 1$ be the number of resizes. The sizes before them are $m_0, 2 m_0, \ldots, 2^{r} m_0$. The resize at size $m' = 2^j m_0$ makes $2m'$ lists and moves $n = m' + 1$ pairs, so it costs $3m' + 1 \le 4m'$. Before the last resize the table holds $2^r m_0 + 1$ keys, and each key needs its own insert, so $s \ge 2^r m_0 + 1 > 2^r m_0$. The total cost is at most $\sum_{j=0}^{r} 4 \cdot 2^j m_0 < 4 \cdot 2^{r+1} m_0 = 8 \cdot 2^r m_0 < 8 s$. $\square$

So the total cost of $s$ operations is the sum of their costs without the resize, which has expectation at most $(2 + 2) s = 4s$ by Claim 2 (each operation sees a set that does not depend on $h$ when the sequence is fixed in advance), plus less than $8s$ for the resizes. The expected total is $O(s)$, and each operation costs $O(1)$ expected amortized time. $\blacksquare$

The condition that the keys do not depend on $h$ is necessary. An adversary who sees $h$, or the order of the keys in an iteration, can pick keys with the same bucket, and then Claim 1 applies.
