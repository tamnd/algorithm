---
title: HGCD returns the Euclid state straddling 2^m, and GCD returns gcd(a, b)
proves: [correctness]
status: full
---

Write $E(q) = \begin{pmatrix} q & 1 \\ 1 & 0 \end{pmatrix}$ for the **quotient matrix** of $q$. Then $E(q) (x, y)^T = (qx + y, x)^T$, $\det E(q) = -1$ and $E(q)^{-1} = \begin{pmatrix} 0 & 1 \\ 1 & -q \end{pmatrix}$. One **Euclid step** maps $(x, y)$ with $x \ge y > 0$ to $(y, x - qy)$ with $q = \lfloor x/y \rfloor$; equivalently $(x, y)^T = E(q) (y, x - qy)^T$. For an input $a \ge b \ge 0$ of HGCD, the **Euclid states** are the pairs $s_0 = (a, b)$, $s_1$, $s_2$, ..., obtained by Euclid steps until the second entry is 0, and $Q_i$ is the list of the first $i$ quotients. The second entries strictly decrease.

**Lemma 1 (certificate).** Let $q_1, \ldots, q_j \ge 1$ with $j \ge 1$, $R = E(q_1) \cdots E(q_j)$, and $(\alpha, \beta)^T = R^{-1} (a, b)^T$. If $\alpha > \beta > 0$, then $(\alpha, \beta) = s_j$ and the first $j$ quotients of Euclid on $(a, b)$ are $q_1, \ldots, q_j$.

*Proof.* Let $p_j = (\alpha, \beta)$ and $p_{i-1} = E(q_i) p_i$ for $i = j, \ldots, 1$, so $p_0 = R p_j = (a, b)$. We show by downward induction that $p_i = (x_i, y_i)$ satisfies $x_i > y_i > 0$ for all $i$. It holds for $i = j$. If it holds for $i$, then $p_{i-1} = (q_i x_i + y_i, x_i)$, and $q_i x_i + y_i \ge x_i + y_i > x_i > 0$, so it holds for $i - 1$. Now for each $i \ge 1$, $p_{i-1} = (q_i x_i + y_i, x_i)$ with $0 < y_i < x_i$, so $\lfloor (q_i x_i + y_i)/x_i \rfloor = q_i$ and the remainder is $y_i$: the Euclid step from $p_{i-1}$ has quotient $q_i$ and leads to $p_i$. Since $p_0 = (a, b) = s_0$, induction on $i$ gives $p_i = s_i$ with quotients $q_1, \ldots, q_i$. $\square$

**Lemma 2 (FIXUP).** Let $R = E(q_1) \cdots E(q_j)$ with all $q_i \ge 1$ and $P = (q_1, \ldots, q_j)$, $j \ge 0$, and let $a \ge b \ge 0$ and $L \le a$. Then FIXUP$(R, P, a, b, L)$ terminates and returns $(R', P', \alpha, \beta)$ with $P'$ a prefix $(q_1, \ldots, q_i)$ of $P$, $R' = E(q_1) \cdots E(q_i)$, $(a, b)^T = R' (\alpha, \beta)^T$, and either $i = 0$ and $(\alpha, \beta) = (a, b)$, or $i \ge 1$, $\alpha > \beta > 0$ and $\alpha \ge L$. In both cases $(\alpha, \beta) = s_i$ and $P' = Q_i$.

*Proof.* Line L11 sets $(\alpha, \beta)^T = R^{-1}(a, b)^T$; the implementation computes $R^{-1}$ as $\det R$ times the adjugate, which is exact because $\det R = (-1)^j$. The loop keeps the relation $(\alpha, \beta)^T = R^{-1} (a, b)^T$ with $R$ the product over $P$: removing $q$ replaces $R$ by $R E(q)^{-1}$, whose inverse is $E(q) R^{-1}$, and $E(q) (\alpha, \beta)^T = (q\alpha + \beta, \alpha)^T$, which is the update of line L12. Each iteration shortens $P$, so the loop ends. If it ends with $P$ empty, then $R = I$ and $(\alpha, \beta) = (a, b) = s_0$. Otherwise it ends because $\alpha > \beta > 0$ and $\alpha \ge L$, and Lemma 1 gives $(\alpha, \beta) = s_i$ with quotients $P'$. $\square$

**Lemma 3 (HGCD).** For $a \ge b \ge 0$ and a threshold $T \ge 2$, HGCD$(a, b)$ terminates and returns $(M, Q, \alpha, \beta)$ with $Q = Q_j$, $M = E(q_1) \cdots E(q_j)$, $(\alpha, \beta) = s_j$, and $\alpha \ge 2^m > \beta$, where $m = \lceil n/2 \rceil$ and $n$ is the bit length of $a$; or $j = 0$ and $b < 2^m$.

*Proof.* By strong induction on $n$. Let $\lambda = 2^m$.

*Lines L1 to L3.* If $b < \lambda$, line L2 returns $s_0$ with $j = 0$, as claimed. If $n \le T$, line L3 does Euclid steps while the second entry is at least $\lambda$, and records each quotient; this is the claim directly, since the second entries decrease, and each step is legal because the second entry is positive.

Otherwise $n > T \ge 2$, so $m \ge 1$, and $b \ge \lambda$. We use the **invariant**: the current pair is $s_i$ for $i = |Q|$, $Q = Q_i$, $M = E(q_1) \cdots E(q_i)$, and the first entry of the current pair is at least $\lambda$.

*Line L4.* The arguments $\lfloor a/\lambda \rfloor \ge \lfloor b/\lambda \rfloor \ge 0$ have $n - m < n$ bits, so by the induction hypothesis the call terminates and returns quotients $P$, all at least 1, and $R$ their product. (Its $\alpha$ and $\beta$ are not used.)

*Line L5.* By Lemma 2 with $L = \lambda \le a$, the result is $s_i$ with $Q = Q_i$ and $M$ their product, and its first entry is at least $\lambda$: either it is $a \ge \lambda$ ($i = 0$), or it was checked. So the invariant holds.

*Line L6.* If $b \ge \lambda$, one Euclid step is legal ($b > 0$), gives $s_{i+1}$ and appends its quotient; the new first entry is the old $b \ge \lambda$. The invariant holds.

*Lines L7 and L8.* Let $\ell$ be the bit length of the current $a$. The call is made only if $b \ge \lambda$ and $2(\ell - m) < n$. Since $\ell \le n \le 2m$, $k = 2m - \ell \ge 0$, and the arguments $\lfloor a/2^k \rfloor \ge \lfloor b/2^k \rfloor \ge 0$ have $\ell - k = 2(\ell - m) < n$ bits, so the induction hypothesis applies again. Lemma 2 for the current pair $s_i$, with $L = \lambda \le a$, gives the Euclid state $s_{i+i'}$ of the current pair after $i'$ more quotients, which are the next quotients of the original input. Multiplying $M$ by $S$ and appending $P$ keeps the invariant.

*Line L9.* Each Euclid step is legal because $b \ge \lambda > 0$, and it keeps the invariant because the new first entry is the old $b \ge \lambda$. The loop ends because the second entries strictly decrease.

*Line L10.* Now $b < \lambda$ and $a \ge \lambda$ by the invariant. The current pair is $s_j$ with $j = |Q|$, and the second entries of the Euclid states decrease, so $s_j$ is the unique state with first entry at least $\lambda$ and second entry below $\lambda$. $\square$

**Theorem.** GCD$(a, b)$ returns $\gcd(a, b)$ for all integers $a$ and $b$.

*Proof.* Line L14 replaces $a, b$ by their absolute values in decreasing order, which does not change the gcd. Each pass of line L15 replaces $(a, b)$ by a Euclid state of it (Lemma 3), and then, if $b \ne 0$, by one more Euclid step. Euclid steps keep the gcd by the GCD recursion theorem: $\gcd(x, y) = \gcd(y, x - qy)$. The pass strictly decreases $b$: HGCD does not increase it, and the final step replaces $b$ by $a \bmod b < b$. So line L15 ends, and the order $a \ge b$ is kept. Line L16 is Euclid's algorithm, which ends with $(\gcd, 0)$, and $\gcd(x, 0) = x$ for $x \ge 0$. With $a = b = 0$, no loop runs and the result is $0 = \gcd(0, 0)$. $\blacksquare$
