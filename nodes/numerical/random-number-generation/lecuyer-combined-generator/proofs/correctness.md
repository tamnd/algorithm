---
title: The combined generator equals one MRG modulo the product, with period the lcm of the components
proves: [correctness]
status: full
---

We use the pseudocode of the page. There are $J \ge 1$ components with pairwise coprime moduli $m_1, \ldots, m_J$ (distinct primes in practice), a common order $k$ (pad shorter recurrences with zero coefficients), coefficients $a_{j,1}, \ldots, a_{j,k}$, and integer weights $\delta_j$. Component $j$ satisfies $x_{j,n} = (\sum_{i=1}^{k} a_{j,i} x_{j,n-i}) \bmod m_j$.

**Lemma 1 (one step).** One call of COMBINED-NEXT advances every component by one step and returns $g(z_n)$ with $z_n = (\sum_j \delta_j x_{j,n}) \bmod m_1$, where $g(z) = z/(m_1 + 1)$ for $z > 0$ and $g(0) = m_1/(m_1 + 1)$.

*Proof.* For each $j$, line L3 evaluates the recurrence of component $j$ on its stored values $x_{j,n-1}, \ldots, x_{j,n-k}$, and line L4 stores the result as $x_{j,n}$ and drops $x_{j,n-k}$, so after the loop each component has advanced once. Lines L1 and L5 accumulate $z = \sum_j \delta_j x_{j,n}$, and L6 reduces it modulo $m_1$. Line L7 applies $g$. $\square$

**Theorem 1 (equivalent MRG).** Let $m = \prod_j m_j$, $w_n = (\sum_j \delta_j x_{j,n} / m_j) \bmod 1$ and $X_n = m w_n$. Let $a_i$ be the integer in $[0, m)$ with $a_i \equiv a_{j,i} \pmod{m_j}$ for all $j$, which exists and is unique by the Chinese remainder theorem. Then $X_n$ is an integer in $[0, m)$ and $X_n = (\sum_{i=1}^{k} a_i X_{n-i}) \bmod m$ for all $n \ge k$.

*Proof.* Let $M_j = m / m_j$. Then $\sum_j \delta_j x_{j,n} / m_j = (\sum_j \delta_j M_j x_{j,n}) / m$, so $X_n = (\sum_j \delta_j M_j x_{j,n}) \bmod m$, an integer in $[0, m)$. Fix $l$. For $j \ne l$, $m_l \mid M_j$, so $X_n \equiv \delta_l M_l x_{l,n} \pmod{m_l}$. Hence, modulo $m_l$,
$$\sum_i a_i X_{n-i} \equiv \delta_l M_l \sum_i a_{l,i} x_{l,n-i} \equiv \delta_l M_l x_{l,n} \equiv X_n.$$
So $X_n - \sum_i a_i X_{n-i}$ is divisible by every $m_l$, hence by their product $m$ because they are pairwise coprime. As $0 \le X_n < m$, $X_n = (\sum_i a_i X_{n-i}) \bmod m$. $\square$

**Proposition 2 (distance between $u_n$ and $w_n$ for two components).** Let $J = 2$, $\delta = (1, -1)$ and $u'_n = z_n / m_1$. Then $u'_n - w_n \equiv x_{2,n}(m_1 - m_2)/(m_1 m_2) \pmod 1$.

*Proof.* $z_n / m_1 \equiv (x_{1,n} - x_{2,n}) / m_1 \pmod 1$ and $w_n \equiv x_{1,n}/m_1 - x_{2,n}/m_2 \pmod 1$. Subtracting, $u'_n - w_n \equiv x_{2,n} (1/m_2 - 1/m_1) = x_{2,n} (m_1 - m_2)/(m_1 m_2) \pmod 1$. Since $0 \le x_{2,n} < m_2$, the representative on the right lies in $[0, (m_1 - m_2)/m_1)$ when $m_1 > m_2$. $\square$

**Theorem 3 (period).** Suppose every component's transition is a bijection on its state space (true when $a_{j,k} \not\equiv 0 \pmod{m_j}$, as $m_j$ is prime) and component $j$ is purely periodic with period $\rho_j$ from its seed. Then the combined state sequence is purely periodic with period $\operatorname{lcm}(\rho_1, \ldots, \rho_J)$.

*Proof.* The combined state returns to its start at step $t > 0$ if and only if every component does, that is, if and only if $\rho_j \mid t$ for all $j$. The least such $t$ is the least common multiple. $\square$

**Corollary.** If each component has a primitive characteristic polynomial modulo the prime $m_j$ and a nonzero seed, then $\rho_j = m_j^k - 1$, and the period is $\operatorname{lcm}_j (m_j^k - 1)$. Each $m_j^k - 1$ is even when $m_j$ is odd, so for $J$ odd primes the period is at most $\prod_j (m_j^k - 1) / 2^{J-1}$.

*Proof.* For a primitive characteristic polynomial, the transition matrix has multiplicative order $m_j^k - 1$ and acts transitively on the nonzero vectors of $\mathbb{F}_{m_j}^k$, so every nonzero seed lies on one cycle of length $m_j^k - 1$. Then Theorem 3 applies, and the lcm of $J$ even numbers is at most their product divided by $2^{J-1}$. $\square$
