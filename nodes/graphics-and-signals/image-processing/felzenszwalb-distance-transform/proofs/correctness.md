---
title: DT1 computes the lower envelope of the parabolas in linear time, and two passes give the exact squared Euclidean distance transform
proves: [correctness, linear-time, separability]
status: full
---

**Notation.** Let $f : \{0, \dots, n-1\} \to \mathbb{Z} \cup \{\infty\}$ and let $Q = \{q : f(q) < \infty\}$. For $q \in Q$ the parabola $P_q(p) = (p - q)^2 + f(q)$ is defined for every real $p$. The claim is $\mathrm{DT1}(f)(p) = D(p) = \min_{q \in Q} P_q(p)$ for $p = 0, \dots, n-1$, with $D = \infty$ everywhere when $Q = \emptyset$. For $r < q$ in $Q$ let

$$s(q, r) = \frac{(f(q) + q^2) - (f(r) + r^2)}{2q - 2r},$$

the value that line L4 computes.

**Lemma 1 (two parabolas).** For $r < q$ in $Q$ and real $p$: $P_q(p) \le P_r(p)$ if and only if $p \ge s(q, r)$, with equality exactly at $p = s(q, r)$.

*Proof.* $P_q(p) - P_r(p) = (f(q) + q^2) - (f(r) + r^2) - 2p(q - r)$. This is a linear function of $p$ with slope $-2(q - r) < 0$, and it is 0 at $p = s(q, r)$. $\square$

Equivalently, $P_q(p) - p^2 = -2qp + (q^2 + f(q))$ is a line $L_q$ in $p$, and the lines come in order of decreasing slope. The lower envelope of the parabolas is the lower envelope of these lines plus $p^2$.

**Lemma 2 (the envelope invariant).** Let $Q_t$ be the set of the first $t$ elements of $Q$ processed by the loop of line L2. After they are processed, with the current $k \ge 0$:

1. $v[0] < v[1] < \dots < v[k]$ are elements of $Q_t$;
2. $-\infty = z[0] < z[1] < \dots < z[k] < z[k+1] = +\infty$;
3. for each $j \le k$ and each real $p \in [z[j], z[j+1]]$, $P_{v[j]}(p) = \min_{q \in Q_t} P_q(p)$.

*Proof.* By induction on $t$. For $t = 1$, with $q$ the first element, line L4 does nothing because $k = -1$, and line L5 sets $k = 0$, $v[0] = q$, $z[0] = -\infty$, $z[1] = +\infty$. The three claims hold.

Let the claims hold for $Q_t$ with the index $k$, and let $q$ be the next element of $Q$, larger than all of $Q_t$. Write $E(p) = \min_{r \in Q_t} P_r(p)$. By Lemma 1, $P_q(p) \le E(p)$ holds if and only if $p \ge s(q, r)$ for every $r \in Q_t$, so the set where $P_q$ is at most $E$ is the interval $[\tau, \infty)$ with $\tau = \max_{r \in Q_t} s(q, r)$, and the new envelope is $E$ on $(-\infty, \tau]$ and $P_q$ on $[\tau, \infty)$.

Line L4 removes the top of the list while $s(q, v[k]) \le z[k]$. It never removes $v[0]$, because $z[0] = -\infty$. Let $c$ be the index where it stops and $\sigma = s(q, v[c])$, so that $\sigma > z[c]$. We show $\sigma \le z[c+1]$, where $z[c+1]$ is the value before line L5 changes it. If nothing was removed, $z[c+1] = +\infty$. Otherwise $b = v[c+1]$ was removed, so $s(q, b) \le z[c+1] = \zeta$. With $a = v[c]$, claim 3 at the common end $\zeta$ of the intervals of $a$ and $b$ gives $P_a(\zeta) = P_b(\zeta) = E(\zeta)$. Lemma 1 for $q$ and $b$ at $\zeta \ge s(q, b)$ gives $P_q(\zeta) \le P_b(\zeta) = P_a(\zeta)$, and then Lemma 1 for $q$ and $a$ gives $\zeta \ge s(q, a) = \sigma$.

So $\sigma \in [z[c], z[c+1]]$, and by claim 3, $P_a(\sigma) = E(\sigma)$. Since $P_q(\sigma) = P_a(\sigma)$ by Lemma 1, $\sigma$ is in $[\tau, \infty)$, so $\tau \le \sigma$. For $p < \sigma$, Lemma 1 gives $P_q(p) > P_a(p) \ge E(p)$, so $p < \tau$; hence $\tau \ge \sigma$, and $\tau = \sigma$.

Line L5 sets $k = c + 1$, $v[k] = q$, $z[k] = \sigma$ and $z[k+1] = +\infty$. Claim 1 holds because $q$ is larger than all of $Q_t$. Claim 2 holds because $\sigma > z[c]$. For claim 3: on $[\sigma, \infty)$ the new envelope is $P_q$; for $j < k$ the interval $[z[j], z[j+1]]$ lies in $(-\infty, \sigma]$, since $z[c+1]$ is now $\sigma \le$ the old $z[c+1]$, and there the new envelope is $E$, which is $P_{v[j]}$ by the old claim 3. $\square$

**Theorem 3 (DT1 is correct).** DT1 returns $D(p)$ for $p = 0, \dots, n-1$.

*Proof.* If $Q$ is empty, line L6 returns $\infty$ everywhere, which is $D$. Otherwise Lemma 2 holds for $Q_t = Q$ at line L7. The loop of line L8 visits $p = 0, 1, \dots, n-1$ in order, and line L9 advances $k$ while $z[k+1] < p$; it stops because $z[k+1] = +\infty$ for the last index. After line L9, $z[k+1] \ge p$. Also $z[k] \le p$: either $k = 0$ and $z[0] = -\infty$, or $k$ was advanced past $k - 1$ for this $p$ or an earlier $p' \le p$, which needed $z[k] < p' \le p$. So $p \in [z[k], z[k+1]]$, and line L10 sets $P_{v[k]}(p) = D(p)$ by claim 3. $\square$

**Theorem 4 (linear time).** DT1 runs in $O(n)$ time, with each $s$ a fraction of integers whose size is bounded by the input.

*Proof.* Each $q \in Q$ is added once at line L5 and removed at most once at line L4, so the total number of tests at line L4 is at most $|Q|$ plus one failing test per $q$: $O(n)$. In the loop of line L8, $k$ only increases and is at most $|Q| - 1$, so lines L9 and L10 run $O(n)$ times in total. $\square$

**Theorem 5 (two passes).** Let $F : \{0, \dots, W-1\} \times \{0, \dots, H-1\} \to \mathbb{Z} \cup \{\infty\}$. Line L12 computes $G(x, y) = \min_{y'} \bigl((y - y')^2 + F(x, y')\bigr)$ for every column, and line L13 computes $\min_{x'} \bigl((x - x')^2 + G(x', y)\bigr)$ for every row. The result is

$$D(x, y) = \min_{x', y'} \bigl((x - x')^2 + (y - y')^2 + F(x', y')\bigr).$$

*Proof.* By Theorem 3 applied to each column and each row. Then $\min_{x'} \bigl((x - x')^2 + \min_{y'} ((y - y')^2 + F(x', y'))\bigr) = \min_{x', y'} \bigl((x - x')^2 + (y - y')^2 + F(x', y')\bigr)$, because $(x - x')^2$ does not depend on $y'$, and a minimum of sums with a term fixed inside is the sum with the minimum. The same argument with the roles swapped shows that the order of the passes does not matter. With $F = 0$ on the feature pixels and $\infty$ elsewhere (line L14), $D(x, y)$ is the smallest squared Euclidean distance from $(x, y)$ to a feature pixel. The total time is $W \cdot O(H) + H \cdot O(W) = O(WH)$. $\blacksquare$
