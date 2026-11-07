---
title: Restoring division computes the quotient and the remainder
proves: [correctness, termination]
status: full
---

Let $U \ge 0$ have the binary digits $u_{m-1} \ldots u_0$, so $U = \sum_{i<m} u_i 2^i$, and let $V \ge 1$. For $0 \le i \le m$ let $P_i = \lfloor U / 2^i \rfloor = \sum_{j \ge i} u_j 2^{j - i}$. Then $P_m = 0$, $P_0 = U$, and

$$P_i = 2P_{i+1} + u_i \qquad (0 \le i < m).$$

Let $Q_i = \sum_{j \ge i} q_j 2^{j-i}$ be the number formed by the quotient digits found so far, after the step for $i$, and let $R_i$ be the value of $R$ after that step. Put $Q_m = 0$ and $R_m = 0$, the values set by line L1.

**Lemma (invariant).** For $i = m, m - 1, \ldots, 0$: $P_i = Q_i V + R_i$ and $0 \le R_i < V$.

*Proof.* By downward induction on $i$. For $i = m$: $0 = 0 \cdot V + 0$ and $0 \le 0 < V$, since $V \ge 1$.

Assume the claim for $i + 1$, and consider the step for $i$. Line L3 forms $R' = 2R_{i+1} + u_i$. From $0 \le R_{i+1} \le V - 1$ and $u_i \in \{0, 1\}$,

$$0 \le R' \le 2V - 1 .$$

Also $P_i = 2P_{i+1} + u_i = 2Q_{i+1}V + 2R_{i+1} + u_i = 2Q_{i+1}V + R'$. Line L4 forms $R' - V$, which lies in $[-V, V - 1]$.

- If $R' - V \ge 0$, lines L5 and L7 set $q_i = 1$ and $R_i = R' - V$, so $0 \le R_i \le V - 1$, and $Q_i = 2Q_{i+1} + 1$. Then $Q_iV + R_i = 2Q_{i+1}V + V + R' - V = P_i$.
- If $R' - V < 0$, line L6 adds $V$ back, so $R_i = R'$ with $0 \le R' < V$, and $q_i = 0$, $Q_i = 2Q_{i+1}$. Then $Q_iV + R_i = 2Q_{i+1}V + R' = P_i$.

In both cases the claim holds for $i$. $\square$

**Theorem.** RESTORING-DIV terminates after $m$ steps and returns $Q = \lfloor U / V \rfloor$ and $R = U - QV$, with $0 \le R < V$.

*Proof.* The loop of line L2 runs over the $m$ values $i = m - 1, \ldots, 0$, and each step does a bounded amount of work, so it terminates. By the lemma for $i = 0$, $U = P_0 = Q_0V + R_0$ with $0 \le R_0 < V$. By the uniqueness of [division with remainder](/division-with-remainder/), $Q_0 = \lfloor U/V \rfloor$ and $R_0 = U \bmod V$, and these are the returned values, since the digits $q_{m-1}, \ldots, q_0$ are the binary digits of $Q_0$.

**The sign test in finite registers.** The implementation holds $R$ in $n + 1$ limbs of $w$ binary digits, where $V < 2^{nw}$. By the bounds above, $0 \le R' \le 2V - 1 < 2^{nw + 1} \le 2^{(n+1)w}$, so line L3 never overflows. The subtraction of line L4 is done modulo $2^{(n+1)w}$, and its borrow out is 1 exactly when $R' < V$, which is the test of line L5. In that case the addition of line L6, also modulo $2^{(n+1)w}$, gives $(R' - V) + V \equiv R'$, and since $0 \le R' < 2^{(n+1)w}$ the stored value is $R'$. So the register computation agrees with the integer one. $\blacksquare$
