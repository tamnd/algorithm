---
title: Non-restoring division computes the quotient and the remainder
proves: [correctness, termination]
status: full
---

Let $U \ge 0$ have the binary digits $u_{m-1} \ldots u_0$ and let $V \ge 1$. Put $P_i = \lfloor U / 2^i \rfloor$, so $P_m = 0$, $P_0 = U$ and $P_i = 2P_{i+1} + u_i$. Let $R_m = 0$ be the value set by line L1, and $R_i$ the value of $R$ after the step for $i$. Define the *restored value*

$$T_i = \begin{cases} R_i & \text{if } R_i \ge 0, \\ R_i + V & \text{if } R_i < 0. \end{cases}$$

Let $Q_i = \sum_{j \ge i} q_j 2^{j - i}$ be the number formed by the quotient digits after the step for $i$, with $Q_m = 0$.

**Lemma.** For $i = m, \ldots, 0$: $-V \le R_i < V$, $0 \le T_i < V$, and $P_i = Q_iV + T_i$. Moreover, for $i < m$, $R_i = 2T_{i+1} + u_i - V$.

*Proof.* By downward induction. For $i = m$: $R_m = T_m = 0$ and $P_m = 0 = 0 \cdot V + 0$.

Assume the claims for $i + 1$. First, $R_i = 2T_{i+1} + u_i - V$:

- if $R_{i+1} \ge 0$, line L3 gives $R_i = 2R_{i+1} + u_i - V = 2T_{i+1} + u_i - V$;
- if $R_{i+1} < 0$, then $R_{i+1} = T_{i+1} - V$, and line L4 gives $R_i = 2(T_{i+1} - V) + u_i + V = 2T_{i+1} + u_i - V$.

Let $S = 2T_{i+1} + u_i$. Since $0 \le T_{i+1} \le V - 1$ and $u_i \in \{0, 1\}$, $0 \le S \le 2V - 1$, so $R_i = S - V \in [-V, V - 1]$. Also $P_i = 2P_{i+1} + u_i = 2Q_{i+1}V + S$.

- If $R_i \ge 0$: $q_i = 1$, $Q_i = 2Q_{i+1} + 1$ and $T_i = R_i = S - V \in [0, V)$, so $Q_iV + T_i = 2Q_{i+1}V + S = P_i$.
- If $R_i < 0$: $q_i = 0$, $Q_i = 2Q_{i+1}$ and $T_i = R_i + V = S \in [0, V)$, so $Q_iV + T_i = 2Q_{i+1}V + S = P_i$.

So the claims hold for $i$. $\square$

**Theorem.** NON-RESTORING-DIV terminates after $m$ steps and one optional correction, and returns $Q = \lfloor U/V \rfloor$ and $R = U \bmod V$.

*Proof.* The loop runs over $m$ values of $i$ with a bounded amount of work each, and line L6 runs at most once, so the algorithm terminates. Line L6 replaces $R_0$ by $T_0$. By the lemma for $i = 0$, $U = Q_0V + T_0$ with $0 \le T_0 < V$, so by the uniqueness of division with remainder $Q_0 = \lfloor U/V \rfloor$ and $T_0 = U \bmod V$. The returned digits $q_{m-1}, \ldots, q_0$ are the binary digits of $Q_0$. $\square$

**The form with digits $\pm 1$.** Let $d_i = 1$ if $R_{i+1} \ge 0$ and $d_i = -1$ otherwise, the operation chosen in step $i$. Then $R_i = 2R_{i+1} + u_i - d_iV$ in both lines L3 and L4. Multiplying by $2^i$ and summing over $i = m - 1, \ldots, 0$, the terms $2^{i+1}R_{i+1}$ and $2^iR_i$ telescope, and with $R_m = 0$,

$$R_0 = \sum_{i<m} u_i 2^i - V \sum_{i<m} d_i 2^i = U - DV, \qquad D = \sum_{i<m} d_i 2^i .$$

Since $R_0 \in [-V, V)$, $Q = D$ and $R = R_0$ if $R_0 \ge 0$, and $Q = D - 1$ and $R = R_0 + V$ if $R_0 < 0$. This is the textbook correction.

**Register widths.** The implementation holds $R$ in two's complement in $n + 1$ limbs of $w \ge 2$ binary digits, with $V < 2^{nw}$. The intermediate value $2R + u_i$ lies in $[-2V, 2V)$, and $2V \le 2^{nw + 1} \le 2^{(n+1)w - 1}$ because $w \ge 2$, so every intermediate value lies in the range $[-2^{(n+1)w - 1}, 2^{(n+1)w - 1})$ of the register. Arithmetic modulo $2^{(n+1)w}$ therefore represents each value exactly, and the top binary digit is its sign. $\blacksquare$
