---
title: Garner's algorithm returns the unique solution in [0, M)
proves: [correctness]
status: full
---

**Notation.** Let $m_1, \ldots, m_t \ge 1$, let $P_0 = 1$ and $P_i = m_1 m_2 \cdots m_i$, and let $M = P_t$. The residues are $v_1, \ldots, v_t$.

**Claim.** The setup (lines L1 to L4) succeeds if and only if the moduli are pairwise coprime, and then $C_i \equiv P_{i-1}^{-1} \pmod{m_i}$ for $2 \le i \le t$. With these constants, lines L5 to L10 compute digits $0 \le u_i < m_i$, and lines L11 to L13 return
$$x = u_1 + u_2 P_1 + u_3 P_2 + \cdots + u_t P_{t-1},$$
which is the unique integer with $0 \le x < M$ and $x \equiv v_i \pmod{m_i}$ for all $i$.

**Setup.** For each $i \ge 2$, line L2 computes $p \equiv P_{i-1} \pmod{m_i}$, as a product of the factors $m_j \bmod m_i$ reduced after each step. Line L3 computes $g = \gcd(p, m_i) = \gcd(P_{i-1}, m_i)$ and, when $g = 1$, $C_i$ with $C_i P_{i-1} \equiv 1 \pmod{m_i}$. A prime divides $\gcd(P_{i-1}, m_i)$ exactly when it divides $m_i$ and some $m_j$ with $j < i$. So all the checks of line L4 pass if and only if every pair $m_j, m_i$ with $j < i$ is coprime.

**Partial values.** Let $x_i = u_1 + u_2 P_1 + \cdots + u_i P_{i-1}$. We prove by induction on $i$ that $0 \le x_i < P_i$ and $x_i \equiv v_j \pmod{m_j}$ for all $j \le i$.

- *Base.* Line L5 sets $u_1 = v_1 \bmod m_1$, so $x_1 = u_1 \in [0, m_1)$ and $x_1 \equiv v_1 \pmod{m_1}$.
- *The Horner loop.* Fix $i \ge 2$. Define $y_{i-1} = u_{i-1}$ and $y_j = u_j + m_j y_{j+1}$ for $j = i - 2, \ldots, 1$. Expanding, $y_j = \sum_{l=j}^{i-1} u_l \, m_j m_{j+1} \cdots m_{l-1}$, so $y_1 = x_{i-1}$. Line L7 sets $s \equiv y_{i-1}$, and each pass of line L9, for $j$ from $i - 2$ down to $1$, turns $s \equiv y_{j+1}$ into $s \equiv m_j y_{j+1} + u_j = y_j \pmod{m_i}$. After the loop, $s \equiv x_{i-1} \pmod{m_i}$.
- *Step.* Line L10 sets $u_i = (v_i - s) C_i \bmod m_i$, so $0 \le u_i < m_i$. Then
$$x_i = x_{i-1} + u_i P_{i-1} \equiv s + (v_i - s) C_i P_{i-1} \equiv s + (v_i - s) = v_i \pmod{m_i}.$$
For $j < i$, $m_j \mid P_{i-1}$, so $x_i \equiv x_{i-1} \equiv v_j \pmod{m_j}$ by the induction hypothesis. For the range, $0 \le x_i \le (P_{i-1} - 1) + (m_i - 1) P_{i-1} = P_i - 1$.

**Evaluation.** Lines L11 and L12 compute $u_t$, then $u_t m_{t-1} + u_{t-1}$, and so on down to index $1$. This is the Horner form of $x_t$, so line L13 returns $x = x_t$. By the induction, $0 \le x < M$ and $x \equiv v_i \pmod{m_i}$ for all $i$.

**Uniqueness.** If $x$ and $x'$ both satisfy all congruences, then every $m_i$ divides $x - x'$. The moduli are pairwise coprime, so their product $M$ divides $x - x'$. Two different integers in $[0, M)$ differ by less than $M$, so $x = x'$.

**Empty system.** For $t = 0$, $M = 1$ and the only value in $[0, 1)$ is $0$, which the implementation returns. $\blacksquare$
