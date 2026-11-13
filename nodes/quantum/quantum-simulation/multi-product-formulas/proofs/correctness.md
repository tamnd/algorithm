---
title: The multi-product formula with Lagrange weights in k^(-2) has error O(t^(2m+1)), and its LCU circuit applies M/s
proves: [correctness]
status: full
---

We use the pseudocode of the page. $H = \sum_{l=1}^L A_l$ with $A_l = c_lP_l$, $S_2(\tau) = e^{-iA_1\tau/2}\cdots e^{-iA_L\tau/2}e^{-iA_L\tau/2}\cdots e^{-iA_1\tau/2}$, and $k_1, \ldots, k_m$ are distinct positive integers. The norm is the spectral norm.

**Lemma 1 (the weights).** With $x_q = k_q^{-2}$ and $C_q = \prod_{p \ne q}k_q^2/(k_q^2 - k_p^2)$ (line L1), $\sum_q C_qx_q^J = 1$ for $J = 0$ and $= 0$ for $1 \le J \le m - 1$.

*Proof.* The Lagrange basis polynomial $\ell_q(x) = \prod_{p \ne q}(x - x_p)/(x_q - x_p)$ has $\ell_q(0) = \prod_{p \ne q}(-k_p^{-2})/(k_q^{-2} - k_p^{-2})$. Multiplying the numerator and the denominator of each factor by $k_p^2k_q^2$ gives $-k_q^2/(k_p^2 - k_q^2) = k_q^2/(k_q^2 - k_p^2)$, so $C_q = \ell_q(0)$. The nodes $x_q$ are distinct, and Lagrange interpolation is exact for polynomials of degree at most $m - 1$, so $x^J = \sum_q x_q^J\ell_q(x)$ for $J \le m - 1$. At $x = 0$ this gives the claim. $\square$

**Lemma 2 (the odd logarithm).** There is $\rho > 0$ such that for $|\tau| < \rho$, $S_2(\tau) = e^{Z(\tau)}$ with $Z(\tau) = \sum_{j \ge 0}\tau^{2j+1}E_{2j+1}$, a series that converges absolutely, and $E_1 = -iH$.

*Proof.* $S_2$ is an entire function of $\tau$ with $S_2(0) = I$, so for small $|\tau|$, $\|S_2(\tau) - I\| < 1$, and $Z(\tau) = \log S_2(\tau) = \sum_{n \ge 1}(-1)^{n+1}(S_2(\tau) - I)^n/n$ is analytic in $\tau$, with $e^{Z(\tau)} = S_2(\tau)$ and $Z(0) = 0$. The factors of $S_2(-\tau)$ are the inverses of the factors of $S_2(\tau)$ in the reverse order, and the order of $S_2$ is a palindrome, so $S_2(-\tau) = S_2(\tau)^{-1}$. For small $\tau$, both $Z(-\tau)$ and $-Z(\tau)$ are small logarithms of $S_2(\tau)^{-1}$, and the logarithm close to 0 is unique, so $Z(-\tau) = -Z(\tau)$. So $Z$ is odd, and its power series has only odd powers. The derivative at 0 is $S_2'(0) = \sum_l(-iA_l/2) \cdot 2 = -iH$, so $E_1 = -iH$. $\square$

**Lemma 3 (the expansion in $1/k^2$).** There is $\rho' > 0$ such that for $|t| < \rho'$ and every integer $k \ge 1$,
$$S_2(t/k)^k = \sum_{J \ge 0}k^{-2J}G_J(t),$$
where the $G_J$ do not depend on $k$, $G_0(t) = e^{-iHt}$, and $\|G_J(t)\| \le a\,(|t|/\rho')^{2J+1}$ for $J \ge 1$ and a constant $a$.

*Proof.* For $|t/k| < \rho$, $S_2(t/k)^k = e^{kZ(t/k)}$ and
$$kZ(t/k) = \sum_{j \ge 0}k^{-2j}t^{2j+1}E_{2j+1} = X(t, k^{-2}), \qquad X(t, y) = \sum_{j \ge 0}y^jt^{2j+1}E_{2j+1}.$$
The term $j$ of $X$ has norm $|t|\,(|y|\,|t|^2)^j\|E_{2j+1}\|$. For $|y| \le 2$ and $|t| \le \rho/2$, $|y|\,|t|^2 \le \rho^2/2$, so $X$ converges absolutely by Lemma 2 with $\tau = \rho/\sqrt 2$. Set $\rho' = \rho/2$. Then $F(t, y) = e^{X(t, y)}$ is analytic in both variables on $|t| \le \rho'$, $|y| \le 2$, and $S_2(t/k)^k = F(t, k^{-2})$ with $k^{-2} \le 1$. Write $F(t, y) = \sum_J y^JG_J(t)$. At $y = 0$, $X = -iHt$, so $G_0 = e^{-iHt}$. Every monomial $y^bt^c$ of $X$ has $c = 2b + 1$. A monomial of $e^X = \sum_n X^n/n!$ with $n \ge 1$ factors has $c = 2b + n \ge 2b + 1$, so the coefficient $G_J$ of $y^J$, $J \ge 1$, is a power series in $t$ that starts at $t^{2J+1}$ or later. Let $a$ bound $\|F\|$ on $|t| \le \rho'$, $|y| \le 2$. The Cauchy estimate in $y$ on the circle $|y| = 2$ gives $\|G_J(t)\| \le a\,2^{-J}$ for $|t| \le \rho'$. The function $G_J(t)/t^{2J+1}$ is analytic on $|t| \le \rho'$, so by the maximum principle its norm is at most $a\,2^{-J}/\rho'^{2J+1}$, and $\|G_J(t)\| \le a\,2^{-J}(|t|/\rho')^{2J+1} \le a(|t|/\rho')^{2J+1}$. $\square$

**Theorem 1 (order).** For $|t| < \rho'$, $\|M(t) - e^{-iHt}\| \le s\,a\sum_{J \ge m}(|t|/\rho')^{2J+1} = O(t^{2m+1})$, with $s = \sum_q|C_q|$.

*Proof.* By Lemma 3 and Lemma 1,
$$M(t) = \sum_q C_q\sum_{J \ge 0}x_q^JG_J(t) = \sum_{J \ge 0}\Big(\sum_q C_qx_q^J\Big)G_J(t) = e^{-iHt} + \sum_{J \ge m}\Big(\sum_q C_qx_q^J\Big)G_J(t).$$
Exchanging the sums is allowed because the double series converges absolutely. Since $0 < x_q \le 1$, $|\sum_q C_qx_q^J| \le s$. The bound on $G_J$ gives the claim. $\blacksquare$

**Corollary (step doubling).** Replace every $k_q$ by $2k_q$. The weights $C_q$ are homogeneous of degree 0 in the $k$'s, so they do not change, and $x_q$ becomes $x_q/4$. The error is $\sum_{J \ge m}4^{-J}(\sum_q C_qx_q^J)G_J(t)$. If the leading term $J = m$ is not zero, the error falls by a factor that tends to $2^{2m}$ as the $k_q$ grow, because the terms with $J > m$ fall faster. For one call at a short time, halving $t$ multiplies the leading term by $2^{-(2m+1)}$ by Lemma 3.

**Theorem 2 (the circuit).** With $U_q = \mathrm{sign}(C_q)S_2(t/k_q)^{k_q}$ (line L3), $B|0\rangle = s^{-1/2}\sum_q\sqrt{|C_q|}\,|q\rangle$ with a real $B$ (line L4) and $W = (B^\dagger \otimes I)\,\mathrm{SELECT}\,(B \otimes I)$ (line L5),
$$(\langle 0| \otimes I)\,W\,(|0\rangle \otimes I) = \frac{M(t)}{s}.$$
So the outcome 0 in line L6 has probability $\|M\psi\|^2/s^2$ and leaves $M|\psi\rangle/\|M|\psi\rangle\|$.

*Proof.* $(B \otimes I)|0\rangle|\psi\rangle = \sum_q b_q|q\rangle|\psi\rangle$ with $b_q = \sqrt{|C_q|/s}$. SELECT maps this to $\sum_q b_q|q\rangle U_q|\psi\rangle$. The amplitude of $|0\rangle$ after $B^\dagger$ is $\sum_q\langle 0|B^\dagger|q\rangle b_qU_q|\psi\rangle = \sum_q b_q^2U_q|\psi\rangle$, since $\langle 0|B^\dagger|q\rangle = \overline{\langle q|B|0\rangle} = b_q$. Finally $b_q^2U_q = (|C_q|/s)\,\mathrm{sign}(C_q)S_2(t/k_q)^{k_q} = (C_q/s)S_2(t/k_q)^{k_q}$, and the sum over $q$ is $M(t)/s$. The measurement rule gives the probability and the state. $\blacksquare$

**Remark (one round of amplification).** If $s \le 2$, add the weights $c = (2 - s)/2$ on $+I$ and on $-I$. They cancel in the sum, and the block of the new $W$ is $M/2$. The computation of Lemma 3 on the page of truncated Taylor series simulation shows that $-WRW^\dagger RW$ then has the block $\tfrac{3}{2}M - \tfrac{1}{2}MM^\dagger M$, which is within $O(\|M - V\|)$ of any unitary $V$ close to $M$.
