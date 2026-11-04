---
title: The skyline sweep outputs the shortest list of key points of the skyline
proves: [correctness, termination]
status: full
---

**Setting.** The input is $n \ge 0$ buildings $(L_i, R_i, H_i)$ with $L_i < R_i$ and $H_i > 0$. Building $i$ is *active* at $x$ when $L_i \le x < R_i$. Let $f(x) = \max\{H_i : i \text{ active at } x\}$, and $f(x) = 0$ when no building is active. Let $X = [x_1 < x_2 < \cdots < x_k]$ be the distinct values of all $L_i$ and $R_i$, as built in line L1. We write $x_{k+1} = +\infty$.

**Lemma 1 ($f$ is a step function on the events).** For $1 \le t \le k$, $f$ is constant on $[x_t, x_{t+1})$. Also $f(x) = 0$ for $x < x_1$ and for $x \ge x_k$.

*Proof.* Take $x, y \in [x_t, x_{t+1})$ with $x < y$. If building $i$ is active at $x$ but not at $y$, then $R_i \le y$ and $R_i > x$, so $R_i \in (x, y] \subseteq (x_t, x_{t+1})$, which contains no value of $X$. If $i$ is active at $y$ but not at $x$, then $L_i \in (x, y]$, the same contradiction. So the same buildings are active at $x$ and at $y$, and $f(x) = f(y)$. For $x < x_1$, each $L_i \ge x_1 > x$, so no building is active. For $x \ge x_k$, each $R_i \le x_k \le x$, so no building is active. $\square$

**Lemma 2 (heap invariant).** Line L2 sorts $B$ by $L$. For $1 \le t \le k$, after line L8 in the iteration for $x = x_t$:

> **(a)** The entries inserted so far are exactly the buildings with $L_i \le x_t$, and $i - 1$ is their number.
> **(b)** Each building that is active at $x_t$ has its entry in $Q$.
> **(c)** If $Q$ is not empty, its top entry belongs to a building that is active at $x_t$.

*Proof.* *Part (a)*, by induction on $t$. Before the first iteration no entry was inserted and $i = 1$. Assume that before the iteration for $x_t$ the inserted entries are those with $L_i \le x_{t-1}$ (none when $t = 1$). Since $B$ is sorted by $L$ and each $L$ is a value of $X$, the next buildings in $B$ have $L \ge x_t$, and those with $L = x_t$ come first. The loop of line L5 inserts exactly them and stops at the first building with $L > x_t$ or at $i = n + 1$. No $L_i$ lies strictly between $x_{t-1}$ and $x_t$, so the inserted entries are now those with $L_i \le x_t$.

*Part (b).* Let building $j$ be active at $x_t$. By (a) its entry was inserted. An entry is removed only by line L8 in some iteration $s \le t$, and only when its $R \le x_s \le x_t$. But $R_j > x_t$, so the entry of $j$ was never removed.

*Part (c).* The loop of line L7 stops only when $Q$ is empty or the top entry has $R > x_t$. The top entry was inserted, so by (a) its $L \le x_t$. With $R > x_t$ its building is active at $x_t$. $\square$

**Lemma 3 (the height).** After line L9 in the iteration for $x_t$, $h = f(x_t)$.

*Proof.* If $Q$ is empty, then by Lemma 2(b) no building is active at $x_t$, so $f(x_t) = 0 = h$. Otherwise let $(H, R)$ be the top entry, so $H$ is the largest height in $Q$. By Lemma 2(c), $H$ is the height of an active building, so $H \le f(x_t)$. By Lemma 2(b), each active building has its entry in $Q$, so each active height is at most $H$, and $f(x_t) \le H$. So $h = H = f(x_t)$. $\square$

**Theorem.** SKYLINE-SWEEP terminates and returns the list $P = [(x_t, f(x_t)) : 1 \le t \le k,\ f(x_t) \ne f(x_{t-1})]$, where $f(x_0) = 0$ by convention. This list is the unique shortest list of key points: its $x$ values increase, consecutive heights differ, $f(x) = h_j$ on $[x_j, x_{j+1})$ for consecutive points $(x_j, h_j)$, $(x_{j+1}, h_{j+1})$ of $P$, and $f(x) = 0$ before the first point and from the last point on.

*Proof.* *Termination.* The loop of line L4 runs $k \le 2n$ times. Each run of line L6 increases $i$ by 1 and $i \le n + 1$, so line L6 runs at most $n$ times in total. Each run of line L8 removes one of the at most $n$ inserted entries, so line L8 runs at most $n$ times in total. So the algorithm stops.

*The output.* We show by induction on $t$ that after the iteration for $x_t$, $prev = f(x_t)$ and $out$ is the part of $P$ with $x \le x_t$. Before the first iteration $prev = 0 = f(x_0)$ and $out$ is empty. In the iteration for $x_t$, Lemma 3 gives $h = f(x_t)$, and by the hypothesis $prev = f(x_{t-1})$. Lines L10 and L11 append $(x_t, f(x_t))$ exactly when $f(x_t) \ne f(x_{t-1})$, and then set $prev = f(x_t)$. If $f(x_t) = f(x_{t-1})$, then $prev$ already equals $f(x_t)$. At the end, $out = P$.

*$P$ describes $f$.* By Lemma 1, $f$ is constant on each $[x_t, x_{t+1})$, and between two consecutive points of $P$ the value $f$ does not change at the events in between, because those events are not in $P$. So $f = h_j$ on $[x_j, x_{j+1})$. Before the first point of $P$, $f$ is 0 on $(-\infty, x_1)$ by Lemma 1 and does not change at the events before the first point. After the last point $(x_j, h_j)$ of $P$, $f$ does not change, and $f(x_k) = 0$ by Lemma 1, so $h_j = 0$ and $f = 0$ from $x_j$ on. Consecutive heights in $P$ differ because each point of $P$ has a height different from the value of $f$ just before it, which is the height of the previous point.

*$P$ is the shortest list.* Let $P'$ be any list of key points that describes $f$ in this way. At each $x_t$ with $f(x_t) \ne f(x_{t-1})$, $f$ changes value at $x_t$: it is $f(x_{t-1})$ on $[x_{t-1}, x_t)$ and $f(x_t)$ at $x_t$. A list that describes $f$ by values on half-open pieces must start a new piece at each point where $f$ changes, so $P'$ has a point at $x_t$. So $P'$ contains a point at each $x$ of $P$, and $|P'| \ge |P|$. If also consecutive heights of $P'$ differ, $P'$ has no point where $f$ does not change, so $P' = P$. $\blacksquare$

**Cost of the heap operations.** The termination argument also gives the cost: at most $n$ INSERT and at most $n$ EXTRACT-MAX calls in total, each on a heap of at most $n$ entries, so $O(n \log n)$ time for the heap, plus $O(n \log n)$ for the sorts of lines L1 and L2.
