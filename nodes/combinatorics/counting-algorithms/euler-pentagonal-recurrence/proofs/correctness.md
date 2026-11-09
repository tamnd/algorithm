---
title: The pentagonal recurrence returns p(0), ..., p(n) with Θ(n^(3/2)) additions
proves: [correctness, termination, time.worst, time.best]
status: full
---

We use the pseudocode PENTAGONAL-PARTITIONS of the page. $p(m)$ is the number of partitions of $m$, with $p(0) = 1$ and $p(m) = 0$ for $m < 0$, and $g_j = j(3j - 1)/2$ for every integer $j$.

**Lemma 1 (the recurrence).** For every $m \ge 1$,

$$p(m) = \sum_{j \ge 1} (-1)^{j+1} \bigl( p(m - g_j) + p(m - g_{-j}) \bigr),$$

where only finitely many terms are nonzero.

*Proof.* The generating function of the partition numbers is $\sum_{m \ge 0} p(m) x^m = \prod_{k \ge 1} (1 - x^k)^{-1}$, because a partition is fixed by the number of parts equal to $k$ for each $k$. By the pentagonal number theorem, $\prod_{k \ge 1} (1 - x^k) = \sum_{j \in \mathbb{Z}} (-1)^j x^{g_j}$. The product of the two series is $1$, so for $m \ge 1$ the coefficient of $x^m$ in the product is $0$:

$$\sum_{j \in \mathbb{Z}} (-1)^j\, p(m - g_j) = 0.$$

The term $j = 0$ is $p(m)$, since $g_0 = 0$. Move the other terms to the right side and pair $j$ with $-j$, which have the same sign $(-1)^j = (-1)^{-j}$. This gives $p(m) = -\sum_{j \ge 1} (-1)^j (p(m - g_j) + p(m - g_{-j}))$, which is the claim. For $j \ge 1$, $g_j \ge j$, so the terms with $j > m$ are $0$. $\square$

**Lemma 2 (order of the shifts).** For $j \ge 1$, $g_j < g_{-j} < g_{j+1}$.

*Proof.* $g_{-j} - g_j = j > 0$ and $g_{j+1} - g_{-j} = (3j + 1) - j = 2j + 1 > 0$. $\square$

**Lemma 3 (the inner loop).** Fix $m \ge 1$ and assume $P[i] = p(i)$ for $0 \le i < m$ when line L3 runs. Let $J$ be the largest $j \ge 0$ with $g_j \le m$. Then the loop of line L4 runs for $j = 1, \ldots, J$ and stops, and at that point

$$s = \sum_{j=1}^{J} (-1)^{j+1} \Bigl( p(m - g_j) + [g_{-j} \le m]\, p(m - g_{-j}) \Bigr) = p(m).$$

*Proof.* The sequence $g_1, g_2, \ldots$ is strictly increasing by Lemma 2, so the test of line L4 holds exactly for $j = 1, \ldots, J$, and line L8 makes the loop reach $j = J + 1$ and stop. This also proves termination, since $J \le m$. For each $j \le J$, line L5 sets $c = (-1)^{j+1}$. Since $1 \le g_j \le m$, the index $m - g_j$ lies in $[0, m - 1]$, so line L6 reads $p(m - g_j)$ by the assumption. Line L7 reads $P[m - g_{-j}] = p(m - g_{-j})$ when $g_{-j} \le m$, again with an index in $[0, m-1]$, and adds nothing otherwise. So after the loop, $s$ is the first sum. The terms of Lemma 1 that it leaves out have $g_j > m$ (all $j > J$) or $g_{-j} > m$, and these terms are $p$ of a negative number, which is $0$. So $s = p(m)$ by Lemma 1. $\square$

**Theorem (correctness).** PENTAGONAL-PARTITIONS$(n)$ returns $P$ with $P[m] = p(m)$ for $0 \le m \le n$.

*Proof.* We show by induction on $m$ the invariant of line L2: before the iteration with value $m$, $P[i] = p(i)$ for $0 \le i < m$. For $m = 1$, line L1 has set $P[0] = 1 = p(0)$. If the invariant holds before iteration $m$, Lemma 3 shows that line L9 stores $p(m)$ in $P[m]$, and no other entry changes, so it holds before iteration $m + 1$. After the last iteration, $m = n$, every entry is correct. For $n = 0$ the loop does not run and $P = [1]$. $\blacksquare$

**Modular form.** If every value is reduced modulo $M$ at line L9, the same induction shows $P[m] = p(m) \bmod M$, because reduction modulo $M$ is a ring homomorphism from the integers, so it commutes with the additions, subtractions and multiplications by $\pm 1$ of lines L6 and L7.

**Theorem (operation count).** The number of additions in lines L6 and L7 is the same for every input of size $n$, and it is $\Theta(n^{3/2})$.

*Proof.* For a fixed $m$, the loop runs $J(m)$ times, where $J(m)$ is the largest $j$ with $g_j \le m$. For $j \ge 1$, $j^2 \le g_j$, because $2j^2 \le 3j^2 - j$. So $g_{J(m)} \le m$ gives $J(m) \le \sqrt m$. Also $g_j \le \frac{3}{2} j^2$, so every $j \le \sqrt{2m/3}$ passes the test of line L4, and $J(m) \ge \lfloor \sqrt{2m/3} \rfloor$. Each iteration does one or two additions. So the total count $A(n)$ satisfies

$$\sum_{m=1}^{n} \Bigl\lfloor \sqrt{2m/3} \Bigr\rfloor \le A(n) \le \sum_{m=1}^{n} 2\sqrt m.$$

Since $\sqrt t$ is increasing, the right side is at most $2 \int_0^{n+1} \sqrt t\, dt = \frac{4}{3} (n + 1)^{3/2}$, and the left side is at least $\sum_{m=1}^{n} (\sqrt{2m/3} - 1) \ge \sqrt{2/3} \int_0^{n} \sqrt t\, dt - n = \frac{2}{3}\sqrt{2/3}\, n^{3/2} - n$. Both bounds are $\Theta(n^{3/2})$. The other lines cost $O(1)$ for each iteration of the loop that contains them, which adds $O(n^{3/2})$. $\blacksquare$
