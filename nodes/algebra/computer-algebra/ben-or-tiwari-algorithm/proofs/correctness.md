---
title: The Ben-Or and Tiwari algorithm recovers every polynomial with at most T terms from 2T values
proves: [correctness, termination]
status: full
---

Let $K = \mathbb{Q}$ and $f = \sum_{j=1}^{t} c_j x^{e_j} \in K[x_1, \ldots, x_n]$ with $c_j \ne 0$, distinct $e_j \in \mathbb{N}^n$, and $t \le T$. Let $p_1, \ldots, p_n$ be the first $n$ primes, $m_j = \prod_k p_k^{e_{jk}}$, and $a_i = f(p_1^i, \ldots, p_n^i) = \sum_j c_j m_j^i$ for $0 \le i < 2T$, the values computed at lines L1 and L2. Let $\Lambda(z) = \prod_j (z - m_j)$.

A *recurrence of length $L$* for $a_0, \ldots, a_{N-1}$ is a monic polynomial $\Gamma(z) = \sum_{k=0}^{L} \gamma_k z^k$ of degree $L$ with $\sum_{k=0}^{L} \gamma_k a_{s+k} = 0$ for $0 \le s \le N - 1 - L$. In terms of the connection polynomial $C(z) = 1 + C_1 z + \cdots + C_L z^L$ used by Berlekamp-Massey, $\Gamma(z) = z^L C(1/z)$.

We use one known theorem. **Massey's theorem** (Massey 1969; MCA Section 12.3 gives an equivalent form through Padé approximation): on input $a_0, \ldots, a_{N-1}$, the Berlekamp-Massey algorithm terminates after $N$ steps and returns a recurrence of the least possible length $L$ for this prefix.

**Lemma 1 (distinct nodes).** The $m_j$ are distinct positive integers.

*Proof.* Each $m_j$ is a product of positive primes, so it is a positive integer. If $m_j = m_k$, uniqueness of prime factorization gives $e_{j\ell} = e_{k\ell}$ for every $\ell$, so $e_j = e_k$ and $j = k$. $\square$

**Lemma 2 (the recurrence found is $\Lambda$).** The polynomial $\Gamma$ computed at line L3 equals $\Lambda$, and $t = \deg \Gamma$.

*Proof.* First, $\Lambda$ is a recurrence of length $t$ for the whole prefix: for every $s$, $\sum_k \lambda_k a_{s+k} = \sum_j c_j m_j^s \Lambda(m_j) = 0$. By Massey's theorem, line L3 returns a recurrence $\Gamma$ of least length $L$, so $L \le t$.

Now let $\Gamma$ be any recurrence of length $L \le t$ for $a_0, \ldots, a_{2T-1}$. Since $L \le t \le T$, the defining relations hold for $0 \le s \le 2T - 1 - L$, which includes $0 \le s \le t - 1$ because $2T - 1 - L \ge 2t - 1 - t = t - 1$. For these $s$,

$$0 = \sum_{k=0}^{L} \gamma_k a_{s+k} = \sum_{j=1}^{t} \bigl(c_j \Gamma(m_j)\bigr) m_j^s .$$

This is a homogeneous linear system in the $t$ unknowns $u_j = c_j \Gamma(m_j)$ whose matrix $(m_j^s)_{0 \le s < t,\ 1 \le j \le t}$ is a Vandermonde matrix with distinct nodes by Lemma 1, hence nonsingular. So $u_j = 0$, and since $c_j \ne 0$, $\Gamma(m_j) = 0$ for every $j$. The $m_j$ are distinct, so $\Lambda$ divides $\Gamma$. Then $t \le L$, so $L = t$, and two monic polynomials of the same degree, one dividing the other, are equal: $\Gamma = \Lambda$.

If $t = 0$, the argument says $L = 0$ and $\Gamma = 1$, and line L4 returns the zero polynomial, which is $f$. $\square$

**Lemma 3 (the roots).** If $t \ge 1$, line L5 terminates and returns $m_1, \ldots, m_t$.

*Proof.* $\Lambda$ is monic with integer coefficients and the distinct integer roots $m_j$, so its discriminant $\Delta = \prod_{j < k} (m_j - m_k)^2$ is a nonzero integer. The implementation tries primes $q$ in increasing order. For a prime $q \nmid \Delta$, the $m_j$ are distinct modulo $q$, so $\Lambda \bmod q = \prod_j (z - m_j)$ has exactly the $t$ roots $m_j \bmod q$, and $\Lambda'(m_j) = \prod_{k \ne j} (m_j - m_k)$ is a unit modulo $q$. Only finitely many primes divide $\Delta$, so such a $q$ is reached and the loop over $q$ terminates. For an earlier prime $q$ the test fails when the number of roots is not $t$ or a root is a root of $\Lambda'$; if it passes, the lifted values are still checked by exact evaluation at the end, so a wrong answer is never returned.

Fix a prime $q$ that passes the test and a root $r_0$ of $\Lambda$ modulo $q$ with $\Lambda'(r_0) \not\equiv 0$. Since $\Lambda \equiv \prod_j (z - m_j)$ and $q$ is prime, $r_0 \equiv m_j \pmod q$ for some $j$. Newton's step $r' = r - \Lambda(r) \Lambda'(r)^{-1} \bmod Q^2$, applied to $r \equiv m_j \pmod Q$, gives $r' \equiv m_j \pmod{Q^2}$: write $r = m_j + Q h$; by Taylor expansion $\Lambda(r) \equiv Q h \Lambda'(r) \pmod{Q^2}$, so $r' \equiv r - Q h \equiv m_j \pmod{Q^2}$. This is Hensel's lemma, and $\Lambda'(r)$ is invertible modulo $Q^2$ because it is a unit modulo $q$. The modulus is squared until it exceeds $2B$, where $B = 1 + \max_k |\lambda_k|$ is Cauchy's bound, so $|m_j| < B$. Then the symmetric representative of $r$ in $(-Q/2, Q/2]$ is $m_j$ itself. Distinct roots modulo $q$ give distinct $m_j$, so all $t$ values are found, they satisfy $\Lambda(m_j) = 0$ exactly, and the procedure returns them. $\square$

**Lemma 4 (the exponents).** Line L6 computes $e_j$ from $m_j$.

*Proof.* Dividing $m_j$ by $p_k$ as long as the division is exact counts the exponent of $p_k$ in $m_j$, which is $e_{jk}$ by Lemma 1's factorization $m_j = \prod_k p_k^{e_{jk}}$. After all $k$, the quotient is 1, so no error is raised. $\square$

**Lemma 5 (the coefficients).** Line L7 returns $c_1, \ldots, c_t$.

*Proof.* Fix $j$ and let $\Lambda_j(z) = \Lambda(z)/(z - m_j) = \sum_{i=0}^{t-1} q_{ji} z^i$. Synthetic division computes it: comparing coefficients in $\Lambda(z) = (z - m_j)\Lambda_j(z)$ gives $q_{j,t-1} = \lambda_t = 1$ and $q_{j,i-1} = \lambda_i + m_j q_{ji}$, which is the loop in the implementation. Then

$$\sum_{i=0}^{t-1} q_{ji} a_i = \sum_{k=1}^{t} c_k \sum_{i=0}^{t-1} q_{ji} m_k^i = \sum_{k=1}^{t} c_k \Lambda_j(m_k) = c_j \Lambda_j(m_j),$$

because $\Lambda_j(m_k) = 0$ for $k \ne j$. Finally $\Lambda_j(m_j) = \Lambda'(m_j) = \prod_{k \ne j}(m_j - m_k) \ne 0$ by Lemma 1, so the division in the implementation gives $c_j$. The system of line L7 has a nonsingular Vandermonde matrix, so this is its unique solution. $\square$

**Theorem.** If $f \in \mathbb{Q}[x_1, \ldots, x_n]$ has at most $T$ terms, BEN-OR-TIWARI$(f, n, T)$ terminates after exactly $2T$ evaluations and returns $f$.

*Proof.* Lines L1 and L2 make $2T$ evaluations and stop. Line L3 terminates by Massey's theorem and, by Lemma 2, returns $\Lambda$ and the true number of terms $t$. If $t = 0$ then $f = 0$ is returned at line L4. Otherwise Lemmas 3, 4 and 5 show that lines L5, L6 and L7 terminate and produce the roots $m_j$, the exponent vectors $e_j$ and the coefficients $c_j$, all nonzero. Line L8 returns $\sum_j c_j x^{e_j} = f$. $\blacksquare$
