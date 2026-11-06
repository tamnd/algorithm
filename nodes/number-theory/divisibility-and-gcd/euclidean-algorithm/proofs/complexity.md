---
title: The Euclidean algorithm uses O(n^2) bit operations on n-bit inputs
proves: [bit_operations.worst]
status: full
---

**Claim.** Let $a \ge b \ge 1$ be integers of at most $n$ binary digits. With schoolbook long division, EUCLID$(a, b)$ uses $O(n^2)$ bit operations.

**Setup.** Write the remainder sequence as $r_0 = a$, $r_1 = b$, and $r_{i+1} = r_{i-1} \bmod r_i$, with quotients $q_i = \lfloor r_{i-1} / r_i \rfloor$ for $i = 1, \ldots, k$, where $r_{k+1} = 0$ and $r_k = \gcd(a, b) \ge 1$. Iteration $i$ divides $r_{i-1}$ by $r_i$. Schoolbook long division of $r_{i-1}$ by $r_i$ produces the quotient one binary digit at a time, with one subtraction of at most $\lg r_i + 1$ digits for each digit of the quotient. The quotient has at most $\lg q_i + 1$ digits, so iteration $i$ costs at most $c (1 + \lg q_i)(1 + \lg r_i)$ bit operations for a constant $c$. (The case $q_i = 0$ happens only when $r_{i-1} < r_i$, which does not occur here because $a \ge b$ and each later remainder is smaller than its divisor.)

**Step 1: the quotients multiply to at most $a$.** For each $i$, $r_{i-1} = q_i r_i + r_{i+1} \ge q_i r_i$. Chaining these inequalities gives $a = r_0 \ge q_1 r_1 \ge q_1 q_2 r_2 \ge \cdots \ge q_1 q_2 \cdots q_k r_k \ge q_1 q_2 \cdots q_k$, since $r_k \ge 1$. So $\sum_{i=1}^{k} \lg q_i \le \lg a \le n$.

**Step 2: the number of iterations.** By Theorem 2 of the correctness proof, $k \le 1 + \log_\varphi b \le 1 + 1.45 n$.

**Step 3: the sum.** Each $r_i \le b < 2^n$, so $1 + \lg r_i \le n + 1$. Then

$$\sum_{i=1}^{k} c(1 + \lg q_i)(1 + \lg r_i) \le c(n + 1)\Big(k + \sum_{i=1}^{k} \lg q_i\Big) \le c(n + 1)(1 + 1.45n + n) = O(n^2).$$

The moves of lines L4 and L5 copy at most $n + 1$ digits each, and there are $k = O(n)$ of them, so they add $O(n^2)$. The absolute values of line L1 cost $O(n)$. $\blacksquare$

**Remark.** The same sum shows why the bound is not $O(n^3)$, which the product "$O(n)$ iterations times $O(n^2)$ for each division" would suggest: a division is expensive only when its quotient is large, and large quotients make the remainders shrink fast.
