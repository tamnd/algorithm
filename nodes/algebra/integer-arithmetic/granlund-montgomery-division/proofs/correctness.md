---
title: Granlund-Montgomery and Möller-Granlund division are exact
proves: [correctness, termination]
status: full
---

Let $\beta = 2^w$. Every line runs once, so the algorithms terminate. We prove that DIVIDE and DIVIDE-2BY1 return the quotient and the remainder.

## DIVIDE

Let $1 \le d < \beta$ and $\ell = \lceil \log_2 d \rceil$, so $2^{\ell - 1} < d \le 2^\ell$ for $d \ge 2$, and $\ell = 0$ for $d = 1$.

**Lemma 1.** $0 \le m < \beta$, and $M := \beta + m = \lfloor 2^{w+\ell}/d \rfloor + 1$.

*Proof.* $\beta(2^\ell - d)/d + \beta = 2^{w+\ell}/d$, and adding the integer $\beta$ commutes with the floor, which gives the formula for $M$. If $d = 2^\ell$, then $m = 1$. Otherwise $d \ge 2^{\ell - 1} + 1$ and $\ell \le w$, so $1 - (2^\ell - d)/d = (2d - 2^\ell)/d \ge 2/d > 2^{1-w}$; hence $\beta(2^\ell - d)/d < \beta - 2$ and $m < \beta - 1$. $\square$

**Lemma 2.** For $0 \le n < \beta$, $\lfloor n/d \rfloor = \lfloor Mn / 2^{w+\ell} \rfloor$.

*Proof.* Write $Md = 2^{w+\ell} + e$. Since $M - 1 = \lfloor 2^{w+\ell}/d \rfloor$, $(M - 1)d \le 2^{w+\ell} < Md$, so $1 \le e \le d$. Let $n = qd + r$ with $0 \le r < d$. Then

$$\frac{Mn}{2^{w+\ell}} = \frac{n}{d} + \frac{en}{d \, 2^{w+\ell}} = q + \frac{r}{d} + \frac{en}{d \, 2^{w+\ell}} .$$

The last term is nonnegative and, since $e \le d \le 2^\ell$ and $n < 2^w$, it is less than $1/d$. So the sum of the last two terms is in $[0, (r + 1)/d) \subseteq [0, 1)$, and the floor is $q$. $\square$

**Theorem 1.** DIVIDE returns $(\lfloor n/d \rfloor, n \bmod d)$, and every intermediate value fits in a word.

*Proof.* Let $t = \lfloor mn/\beta \rfloor$ (line L4). Since $m < \beta$, $t \le n$. By nested floors,

$$\left\lfloor \frac{Mn}{2^{w+\ell}} \right\rfloor = \left\lfloor \frac{\lfloor (\beta n + mn)/\beta \rfloor}{2^\ell} \right\rfloor = \left\lfloor \frac{n + t}{2^\ell} \right\rfloor .$$

If $\ell = 0$ then $d = 1$, $m = 1$, $t = 0$, $s_1 = s_2 = 0$, and line L5 gives $q = n$. If $\ell \ge 1$, then $s_1 = 1$, $s_2 = \ell - 1$, and $(n + t)/2 = t + (n - t)/2$ with $n - t \ge 0$, so $\lfloor (n + t)/2 \rfloor = t + \lfloor (n - t)/2 \rfloor$, and, by nested floors again, $\lfloor (n + t)/2^\ell \rfloor = \lfloor (t + \lfloor (n - t)/2 \rfloor)/2^{\ell - 1} \rfloor$, which is line L5. By Lemma 2 the result is $\lfloor n/d \rfloor$. The values $n - t \in [0, n]$ and $t + \lfloor (n - t)/2 \rfloor \le n$ fit in a word, and so does $n - qd \in [0, d)$ (line L6). $\blacksquare$

## DIVIDE-2BY1

Let $\beta/2 \le d < \beta$, $u = u_1 \beta + u_0$ with $0 \le u_1 < d$ and $0 \le u_0 < \beta$, so $q^* = \lfloor u/d \rfloor < \beta$. Let $B = \beta + v = \lfloor (\beta^2 - 1)/d \rfloor$ and $k = \beta^2 - Bd$.

**Lemma 3.** $0 \le v < \beta$, $1 \le k \le d$, and the value $Bu_1 + u_0$ of line L7 is less than $\beta^2$.

*Proof.* Since $d \le \beta - 1$, $(\beta^2 - 1)/d \ge (\beta^2 - 1)/(\beta - 1) = \beta + 1$, so $B \ge \beta + 1$; and $(\beta^2 - 1)/d \le (\beta^2 - 1)/(\beta/2) < 2\beta$, so $B < 2\beta$. Hence $0 \le v < \beta$. From $Bd \le \beta^2 - 1 < (B + 1)d$, $1 \le k \le d$. Finally $Bu_1 + u_0 \le B(d - 1) + \beta - 1 \le \beta^2 - 1 - B + \beta - 1 < \beta^2$, using $Bd \le \beta^2 - 1$ and $B \ge \beta + 1$. $\square$

So line L7 computes $q_1 \beta + q_0 = Bu_1 + u_0$ with $0 \le q_1, q_0 < \beta$. Let $\tilde q = q_1 + 1$ as an integer and $\tilde r = u - \tilde q d$.

**Lemma 4.** $\beta \tilde r = k u_1 + (\beta - d) u_0 + d(q_0 - \beta)$.

*Proof.* Multiply $q_1\beta + q_0 = Bu_1 + u_0$ by $d$ and use $Bd = \beta^2 - k$: $d q_1 \beta = (\beta^2 - k)u_1 + d u_0 - d q_0$. Then $\beta \tilde r = \beta^2 u_1 + \beta u_0 - \beta d q_1 - \beta d = k u_1 + (\beta - d) u_0 + d q_0 - \beta d$. $\square$

**Lemma 5.** Let $M' = \max(\beta - d, q_0)$. Then $q_0 - \beta < \tilde r < M'$ and $\tilde r \ge -d$.

*Proof.* Upper bound: $k u_1 \le d(d - 1)$ and $(\beta - d)u_0 \le (\beta - d)(\beta - 1)$, so by Lemma 4, $\beta \tilde r \le d^2 - d + (\beta - d)(\beta - 1) + dq_0 - \beta d = (\beta - d)^2 - \beta + d q_0 \le (\beta - d)M' + dM' - \beta = \beta M' - \beta$, so $\tilde r \le M' - 1$. Lower bound: the first two terms of Lemma 4 are nonnegative, so $\beta \tilde r \ge d(q_0 - \beta)$. Since $q_0 - \beta < 0$ and $0 < d < \beta$, $d(q_0 - \beta) > \beta(q_0 - \beta)$, so $\tilde r > q_0 - \beta$; and $d(q_0 - \beta) \ge -d\beta$, so $\tilde r \ge -d$. $\square$

**Theorem 2.** DIVIDE-2BY1 returns $(q^*, u - q^* d)$.

*Proof.* Line L8 computes $r = \tilde r \bmod \beta$, because $u \equiv u_0$ and the reduction of $q_1$ mod $\beta$ does not change $\tilde q d \bmod \beta$. Since $M' < \beta$ and $M' - \beta = \max(-d, q_0 - \beta)$, Lemma 5 places $\tilde r$ in $[M' - \beta, M')$, an interval of length $\beta$. All arithmetic below is on true integers; the quotient is finally in $[0, \beta)$, so its value mod $\beta$ is the integer itself.

*Case A: $\tilde r < 0$.* Then $r = \tilde r + \beta > q_0$ by Lemma 5, so line L9 runs and gives the pair $(\tilde q - 1, \tilde r + d)$, where $\tilde r + d \in [0, d)$ by Lemma 5, and $(\tilde r + \beta) + d$ reduced mod $\beta$ is $\tilde r + d$. Line L10 does not run. Since $u = (\tilde q - 1)d + (\tilde r + d)$ with remainder in $[0, d)$, the result is $(q^*, u \bmod d)$.

*Case B: $\tilde r \ge 0$ and $\tilde r \le q_0$.* Then $r = \tilde r$, line L9 does not run, and $\tilde r < M' \le \max(\beta - d, \beta - 1) < 2d$, since $\beta \le 2d$. So at most one subtraction of $d$, line L10, brings it to $[0, d)$.

*Case C: $\tilde r \ge 0$ and $\tilde r > q_0$.* Then $q_0 < \tilde r < M'$ forces $M' = \beta - d$, so $\tilde r < \beta - d \le d$. Line L9 runs and gives $(\tilde q - 1, \tilde r + d)$ with $d \le \tilde r + d < \beta$, so there is no wrap, and line L10 runs and restores $(\tilde q, \tilde r)$, with $\tilde r \in [0, d)$.

In every case the returned pair $(q, r)$ satisfies $u = qd + r$ and $0 \le r < d$, so $q = q^*$. $\blacksquare$
