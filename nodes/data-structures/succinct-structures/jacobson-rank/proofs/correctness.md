---
title: Jacobson's rank structure returns rank and select correctly
proves: [correctness]
status: full
---

We use the pseudocode and the notation of the page: $b$ is the block length, $s$ the number of blocks in a superblock, $L = sb$, $K = \lfloor n/b \rfloor$, and $B[p] = 0$ for $p \ge n$ by convention. Write $R(i) = \text{rank}_1(i) = |\{p < i : B[p] = 1\}|$. With the convention, $R(i)$ is defined for each $i \ge 0$ and equals $R(n) = m$ for $i \ge n$.

**Lemma 1 (the table).** After line L2, $T[x][r] = |\{t < r : \text{bit } t \text{ of } x \text{ is } 1\}|$ for $0 \le x < 2^b$ and $0 \le r \le b$.

*Proof.* Line L2 sets each entry to this value by its definition. $\square$

**Lemma 2 (BUILD).** After BUILD, for $0 \le k \le K$: bit $t$ of $X[k]$ is $B[kb + t]$ for $0 \le t < b$; $RS[q] = R(qL)$ for $0 \le q \le \lfloor K/s \rfloor$; and $RB[k] = R(kb) - RS[\lfloor k/s \rfloor]$.

*Proof.* We show the invariant $c = R(kb)$ at the top of each step $k$ of the loop of line L4, and that after step $k$ the entries $X[k]$, $RB[k]$ and, if $s \mid k$, $RS[k/s]$ hold their stated values.

*Initialization.* Line L3 sets $c = 0 = R(0)$ before step $k = 0$.

*Maintenance.* Assume $c = R(kb)$ at the top of step $k$. If $s \mid k$, line L5 sets $RS[k/s] = c = R(kb) = R((k/s) L)$. Otherwise $q = \lfloor k/s \rfloor$ satisfies $qs < k$, so $RS[q]$ was set at step $qs$, which came earlier. In both cases $RS[\lfloor k/s \rfloor]$ exists when line L6 runs, and line L6 sets $RB[k] = R(kb) - RS[\lfloor k/s \rfloor]$. Line L7 sets bit $t$ of $X[k]$ to $B[kb + t]$. By Lemma 1 with $r = b$, line L8 adds the number of 1s among $B[kb], \ldots, B[kb + b - 1]$, which is $R(kb + b) - R(kb)$. So $c = R((k+1) b)$ at the top of step $k + 1$.

*Termination.* The loop runs for $k = 0, \ldots, K$, so each entry is set. The superblock indices $k/s$ for $s \mid k \le K$ are exactly $0, \ldots, \lfloor K/s \rfloor$. $\square$

**Lemma 3 (RANK1).** For $0 \le i \le n$, RANK1$(i)$ returns $R(i)$.

*Proof.* Let $k = \lfloor i/b \rfloor$, $r = i \bmod b$ and $q = \lfloor k/s \rfloor$. Since $i \le n$, $k \le \lfloor n/b \rfloor = K$, so all three reads of line L10 are defined. We have $qL = qsb \le kb \le i = kb + r$. By Lemma 2, $RS[q] + RB[k] = R(kb)$. The positions $p$ with $kb \le p < i$ are $kb + t$ for $0 \le t < r$, and by Lemma 2 their bits are bits $0$ to $r - 1$ of $X[k]$. By Lemma 1, $T[X[k]][r]$ is their number of 1s, which is $R(i) - R(kb)$. The sum is $R(i)$. $\square$

**Lemma 4 (SELECT1).** For $1 \le j \le m$, SELECT1$(j)$ returns $p^* = \min\{p : R(p + 1) \ge j\}$, which is the position of the $j$-th 1.

*Proof.* First, $p^*$ is the position of the $j$-th 1. The function $R$ does not decrease, $R(0) = 0 < j$ and $R(n) = m \ge j$, so $p^*$ exists and $0 \le p^* \le n - 1$. By minimality, $R(p^*) < j \le R(p^* + 1)$. Since $R(p^* + 1) - R(p^*) \le 1$, this gives $R(p^*) = j - 1$ and $B[p^*] = 1$, which is the definition of $\text{select}_1(j)$.

For the search we use the invariant **(I)**: $lo \le p^* \le hi$. Line L11 makes it true, since $0 \le p^* \le n - 1$. In an iteration, $lo \le mid < hi$. If $R(mid + 1) \ge j$, then $p^* \le mid$ by the definition of $p^*$, and $hi \leftarrow mid$ keeps (I). Otherwise $R(mid + 1) < j$, and since $R$ does not decrease, $R(p + 1) < j$ for each $p \le mid$, so $p^* \ge mid + 1$ and $lo \leftarrow mid + 1$ keeps (I). Lemma 3 gives the value $R(mid + 1)$, since $mid + 1 \le n$. Each iteration makes $hi - lo$ smaller by at least $\lceil (hi - lo)/2 \rceil \ge 1$, so the loop stops after at most $\lceil \lg n \rceil$ iterations, with $lo = hi$. By (I), $lo = p^*$. $\blacksquare$
