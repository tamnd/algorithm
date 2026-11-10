---
title: Marzullo's sweep returns the largest depth and a region where every point has that depth
proves: [correctness]
status: full
---

Let the input be closed intervals $I_i = [l_i, h_i]$, $i = 1, \dots, k$, with $l_i \le h_i$. The *depth* of a point $x$ is $D(x) = |\{ i : l_i \le x \le h_i \}|$, and $c^* = \max_x D(x)$ (0 when $k = 0$). We use the pseudocode of the page. Number the sorted entries $0, 1, \dots, 2k-1$, and let $x_j$ be the position of entry $j$. For each $j$ let $\mathrm{cnt}_j$ be the value of count after entry $j$.

**Lemma 1 (the counter).** $\mathrm{cnt}_j$ is the number of intervals whose START has index at most $j$ and whose END has index greater than $j$.

*Proof.* Each START adds 1 (line L5) and each END subtracts 1 (line L8). An interval's START comes before its END in the sorted order: if $l_i < h_i$ by position, and if $l_i = h_i$ by the rule of line L2. So after entry $j$ the counter is the number of started intervals less the number of ended ones, which is the number of intervals that have started and not ended. $\square$

**Lemma 2 (the counter never exceeds the depth).** If entry $j$ is a START, then $\mathrm{cnt}_j \le D(x_j)$, and if $j$ is the last START at position $x_j$, then $\mathrm{cnt}_j = D(x_j)$.

*Proof.* Let $I_i$ be counted by Lemma 1. Its START has index at most $j$, so $l_i \le x_j$. Its END has index greater than $j$, so $h_i \ge x_j$. So $x_j \in I_i$, and $\mathrm{cnt}_j \le D(x_j)$. Now let $j$ be the last START at position $p = x_j$, and let $p \in I_i$. Then $l_i \le p$, so the START of $I_i$ is at a smaller position or is a START at $p$; in both cases its index is at most $j$. Also $h_i \ge p$, and all END entries at position $p$ come after all START entries at $p$, so the END of $I_i$ has index greater than $j$. So $I_i$ is counted, and $\mathrm{cnt}_j = D(p)$. $\square$

**Lemma 3 (a left end has the largest depth).** If $k \ge 1$, some left end $l_i$ has $D(l_i) = c^*$.

*Proof.* Let $D(x) = c^*$ and let $S$ be the set of intervals that hold $x$; $S$ is not empty since $c^* \ge 1$. Let $p = \max_{i \in S} l_i$. For each $i \in S$, $l_i \le p \le x \le h_i$, so $p \in I_i$. Hence $D(p) \ge |S| = c^*$, and $D(p) = c^*$. $\square$

**Theorem 1.** MARZULLO returns $best = c^*$. If $k \ge 1$, every point of the returned $[a, b]$ has depth exactly $c^*$, and $a$ is the smallest point of depth $c^*$.

*Proof.* The value $best$ is the largest $\mathrm{cnt}_j$ over START entries $j$, because line L6 compares at each START and END entries only lower the counter. By Lemma 2 each such value is at most $c^*$. By Lemma 3 some $p = l_i$ has depth $c^*$, and by Lemma 2 the last START at $p$ gives a counter of $c^*$. So $best = c^*$.

Let $j$ be the entry at which line L7 last fires, so $\mathrm{cnt}_j = c^*$, $a = x_j$ and $b = x_{j+1}$. Entry $j + 1$ exists, since an interval counted at $j$ ends at a later index. Each of the $c^*$ intervals counted at $j$ has $l_i \le x_j = a$ and its END at index at least $j + 1$, so $h_i \ge x_{j+1} = b$. So every point of $[a, b]$ lies in these $c^*$ intervals and has depth at least $c^*$, and so exactly $c^*$.

Line L7 fires for the last time at the first START $j$ with $\mathrm{cnt}_j = c^*$. Suppose some $y < a$ has $D(y) = c^*$. By the proof of Lemma 3 there is a left end $p \le y$ with $D(p) = c^*$, and by Lemma 2 the last START at $p$ has counter $c^*$. Its position $p$ is less than $a$, so its index is less than $j$, which contradicts the choice of $j$. $\square$

**Corollary (fault tolerance).** Suppose the true value $t$ lies in every correct interval and at most $f$ intervals are wrong. Then $D(t) \ge k - f$, so $c^* \ge k - f$ and the call with $f$ does not fail. The region $[a, b]$ need not hold $t$. But every point of depth at least $k - f$ lies in at least $k - 2f$ correct intervals, so when $k > 2f$ each point of $[a, b]$ is within the width of some correct interval of $t$.

*Proof.* The first claim follows from the definition of depth. For the second, a point $x$ of depth at least $k - f$ lies in at least $k - f$ intervals, of which at most $f$ are wrong, so at least $k - 2f$ are correct. A correct interval that holds $x$ also holds $t$, so $|x - t|$ is at most its width. $\square$

**The NTP variant finds the truth when the falsetickers are few.** Let $m$ candidates give the intervals $[\theta_i - \lambda_i, \theta_i + \lambda_i]$, let at most $f$ of them miss the true offset $t$, and let $2f < m$. In the upward scan, the counter after all low and high entries at positions at most $t$ (lows first at a tie) is at least the number of intervals that hold $t$, by the argument of Lemma 2, and so at least $m - f$. So the scan stops at a position $l \le t$. By symmetry, the downward scan stops at $u \ge t$. So if the mid test of step 3 passes for this $f$, or for a smaller $f$ at which the same argument holds, the returned region holds $t$. The mid test can still reject this $f$; then the loop tries a larger one. The test of this page checks, on 500 seeded random inputs with $k < m/2$ far falsetickers, that the returned $f$ is $k$ and that $l \le t \le u$. $\square$

**Running time.** Line L2 sorts $2k$ entries in $O(k \log k)$ time. Each of the $2k$ entries costs $O(1)$ in lines L4 to L8. The table uses $O(k)$ space. $\square$
