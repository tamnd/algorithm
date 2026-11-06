---
title: APR-CL is always right and always stops
proves: [correctness, termination]
status: full
---

We use the pseudocode APR-CL$(N)$ of the page and its notation. After line L4, $N \ge 2$ is odd and coprime to $t s$, so $N$ is coprime to every $q$ of the plan and to every prime $p \mid t$. The plan has $s^2 > N$, $t = \operatorname{lcm}(q_i - 1)$ with $t/2$ odd, and every odd $q$ of the plan has $q \equiv 3 \pmod 4$. For a prime $p$ and an integer $x \ne 0$, $v_p(x)$ is the exponent of $p$ in $x$.

## 1. Rings and sums for one pair

Fix a prime $q \nmid N$ and an odd prime $p \mid q - 1$, with $m = p^k$ the exact power of $p$ in $q - 1$. Let $\zeta = \zeta_m$, $\omega = \zeta_q$, $K = \mathbb{Q}(\zeta, \omega)$ and $R = \mathbb{Z}[\zeta, \omega]$. As $\gcd(m, q) = 1$, $R = \mathbb{Z}[\zeta_{mq}]$, it is a free $\mathbb{Z}$-module, and it is a free $\mathbb{Z}[\zeta]$-module with basis $1, \omega, \ldots, \omega^{q-2}$. The automorphisms of $K$ are $\sigma_c \rho_d$ for $c$ prime to $m$ and $d$ prime to $q$, with $\sigma_c(\zeta) = \zeta^c$, $\sigma_c(\omega) = \omega$, $\rho_d(\zeta) = \zeta$ and $\rho_d(\omega) = \omega^d$. They map $R$ onto $R$.

Let $g$ be the least primitive root modulo $q$, $\chi(g^x) = \zeta^x$ and $\chi(0) = 0$. As $m$ is odd and $m \mid q - 1$, $m \mid (q-1)/2$, so $\chi(-1) = \zeta^{(q-1)/2} = 1$. Let
$$\tau = \sum_{x = 1}^{q-1} \chi(x) \omega^x, \qquad \bar\tau = \sum_{x = 1}^{q-1} \chi(x)^{-1} \omega^{-x}.$$

**Lemma 1.** (a) $\tau \bar\tau = q$. (b) $\rho_d(\tau) = \chi(d)^{-1} \tau$ and $\sigma_c(\tau) = \sum_x \chi(x)^c \omega^x$. (c) $\tau^2 = J \sigma_2(\tau)$, with $J = \sum_{x=2}^{q-1} \chi(x) \chi(1 - x)$.

*Proof.* (a) $\tau\bar\tau = \sum_{x, y \ne 0} \chi(x y^{-1}) \omega^{x - y}$. Put $x = cy$: this is $\sum_{c \ne 0} \chi(c) \sum_{y \ne 0} \omega^{(c-1)y}$. The inner sum is $q - 1$ for $c = 1$ and $-1$ otherwise, as the $q$-th roots of unity add up to 0. So $\tau\bar\tau = (q - 1) - \sum_{c \ne 0, 1} \chi(c) = q$, since $\sum_{c \ne 0} \chi(c) = 0$ for the nontrivial $\chi$.
(b) $\rho_d(\tau) = \sum_x \chi(x) \omega^{dx} = \sum_y \chi(d^{-1} y) \omega^y$ with $y = dx$. The second claim holds because $\sigma_c$ maps $\chi(x) = \zeta^{\operatorname{ind} x}$ to $\chi(x)^c$.
(c) $\tau^2 = \sum_a \omega^a \sum_{x + y = a} \chi(x) \chi(y)$. For $a = 0$ the inner sum is $\chi(-1) \sum_x \chi^2(x) = 0$, as $\chi^2$ is nontrivial ($m$ is odd and $m > 1$). For $a \ne 0$ put $x = a x'$, $y = a y'$: the inner sum is $\chi^2(a) J$. So $\tau^2 = J \sum_a \chi^2(a) \omega^a = J \sigma_2(\tau)$ by (b). $\square$

**The group ring.** Let $G = (\mathbb{Z}/m)^*$ and $Y$ the representatives $1 \le y < m$, $p \nmid y$. The ring $\mathbb{Z}[G]$ acts on $K^*$ by $x^{\sum a_c \sigma_c} = \prod \sigma_c(x)^{a_c}$; this action is multiplicative in the exponent and commutes with every $\rho_d$. Let
$$\theta = \sum_{y \in Y} y \, \sigma_y^{-1}, \qquad \alpha_c = \sum_{y \in Y} \lfloor c y / m \rfloor \sigma_y^{-1} \quad (c \ge 0).$$

**Lemma 2.** For $c$ prime to $m$, $(c - \sigma_c) \theta = m \alpha_c$. Hence $(2 - \sigma_2) \alpha_N = (N - \sigma_N) \alpha_2$.

*Proof.* $c y = m \lfloor cy/m \rfloor + (cy \bmod m)$, so $c\theta = m\alpha_c + \sum_y (cy \bmod m) \sigma_y^{-1}$. Put $y' = cy \bmod m$, which runs over $Y$; then $\sigma_y^{-1} = \sigma_{c} \sigma_{y'}^{-1}$, so the last sum is $\sigma_c \theta$. For the second claim, $m (2 - \sigma_2) \alpha_N = (2 - \sigma_2)(N - \sigma_N)\theta = m (N - \sigma_N) \alpha_2$, and $\mathbb{Z}[G]$ has no torsion. $\square$

Let $u = \tau^{\alpha_2} = \prod_{y \in Y, \, y > m/2} \sigma_{y^{-1}}(\tau)$, an element of $R$, and $w = \sum_{y \in Y, \, y > m/2} y^{-1} \bmod m$.

**Lemma 3.** (a) $S = J^{\alpha_N}$, and $S \sigma_N(u) = u^N$ in $R$. (b) $\rho_d(u) = \chi(d)^{-w} u$.

*Proof.* (a) The code computes $\prod_y \sigma_{y^{-1}}(J)^{\lfloor Ny/m \rfloor} = J^{\alpha_N}$, by the identity $\lfloor Ny/m \rfloor = \lfloor N/m \rfloor y + \lfloor (N \bmod m) y/m \rfloor$ of the page. By Lemma 1(c), $J = \tau^{2 - \sigma_2}$ in $K^*$, so by Lemma 2, $J^{\alpha_N} = \tau^{(N - \sigma_N)\alpha_2} = u^N / \sigma_N(u)$. Both $S \sigma_N(u)$ and $u^N$ lie in $R$ and are equal in $K$.
(b) By Lemma 1(b), $\rho_d(\sigma_{c}(\tau)) = \sigma_c(\chi(d)^{-1}\tau) = \chi(d)^{-c} \sigma_c(\tau)$. Multiply over $c = y^{-1}$ with $y > m/2$. $\square$

**Lemma 4.** $w \bmod p$ does not depend on $k$, and the code checks $p \nmid w$ for every pair of the plan. So $p \nmid w$ for every pair used, including those of line L16.

*Proof.* Modulo $p$, $y^{-1} \bmod m$ is the inverse of $y \bmod p$. The $y$ in $Y$ with $y > m/2$ are the numbers from $(m+1)/2$ to $m - 1$ that are prime to $p$. Their count is $(m - 1)/2 = p (p^{k-1} - 1)/2 + (p - 1)/2$. Take the last $(p-1)/2$ of them, with residues $(p + 1)/2, \ldots, p - 1$; the others form a run of whole blocks of $p$ consecutive numbers, and each block adds $\sum_{c=1}^{p-1} c^{-1} \equiv 0 \pmod p$. So $w \equiv \sum_{c = (p+1)/2}^{p-1} c^{-1} \pmod p$ for every $k$. The function check_units raises an error if $p \mid w$ for a pair of the plan; the extra pairs of line L16 use a prime $p \mid t$, which already occurs in the plan. $\square$

## 2. The semigroup of one prime factor

Fix a prime $r \mid N$ and let $A = R / rR$. As $R$ is a free $\mathbb{Z}$-module, $A$ is a finite ring that is not 0. As $r \nmid q$, $q$ is a unit of $A$, so by Lemma 1(a) $\tau$ and all $\sigma_c(\tau)$ are units of $A$, and so is $u$.

**Lemma 5.** The powers $\zeta^i$, $0 \le i < m$, are distinct in $A$.

*Proof.* $\prod_{j=1}^{m-1} (1 - \zeta^j) = m$, the value at $x = 1$ of $(x^m - 1)/(x - 1) = \prod_{j=1}^{m-1}(x - \zeta^j)$. If $\zeta^i = \zeta^{i'}$ in $A$ with $i \ne i'$, then $1 - \zeta^{i'-i} = 0$ in $A$, so $m = 0$ in $A$. But $r \nmid m$, so $m$ is a unit of $A$, and $A \ne 0$. $\square$

**Lemma 6 (Frobenius).** In $A$, $u^r = \chi(r)^{-wr} \sigma_r(u)$.

*Proof.* For $x = \sum c_{ij} \zeta^i \omega^j \in R$, the multinomial theorem and Fermat's little theorem give $x^r \equiv \sum c_{ij} \zeta^{ri} \omega^{rj} = \sigma_r \rho_r(x) \pmod{rR}$. With Lemma 3(b), $u^r = \sigma_r(\chi(r)^{-w} u) = \chi(r)^{-wr} \sigma_r(u)$. $\square$

Let $\Gamma$ be the set of integers $a \ge 1$ with $p \nmid a$ for which $u^a = \varepsilon \sigma_a(u)$ in $A$ for some $\varepsilon = \zeta^i$. As $\sigma_a(u)$ is a unit, $\varepsilon$ is unique by Lemma 5; call it $\varepsilon(a)$, and let $\lambda(a) = \varepsilon(a)^{a'}$, where $a a' \equiv 1 \pmod m$.

**Lemma 7.** (a) $1 \in \Gamma$, and if $a, b \in \Gamma$ then $ab \in \Gamma$ and $\lambda(ab) = \lambda(a)\lambda(b)$. (b) $r \in \Gamma$ with $\lambda(r) = \chi(r)^{-w}$. (c) If the check of line L11 passes for the pair, with $S \equiv \zeta^h \pmod N$, then $N \in \Gamma$ with $\lambda(N) = \zeta^{h N'}$, $N N' \equiv 1 \pmod m$. (d) There is an $e \ge 0$ such that for $a, b \in \Gamma$ with $a \equiv b \pmod{p^E}$ and $E \ge \max(e, k)$, $\lambda(a) = \lambda(b)$.

*Proof.* (a) $u^{ab} = (\varepsilon(a) \sigma_a(u))^b = \varepsilon(a)^b \sigma_a(u^b) = \varepsilon(a)^b \varepsilon(b)^a \sigma_{ab}(u)$, since $\sigma_a$ is a ring map of $A$ with $\sigma_a(\zeta^i) = \zeta^{ai}$. So $\varepsilon(ab) = \varepsilon(a)^b \varepsilon(b)^a$, and raising to $(ab)'$ gives $\lambda(ab) = \varepsilon(a)^{a'} \varepsilon(b)^{b'}$.
(b) Lemma 6 gives $\varepsilon(r) = \chi(r)^{-wr}$.
(c) $S \equiv \zeta^h$ modulo $N \mathbb{Z}[\zeta]$, so modulo $rR$, and Lemma 3(a) gives $u^N = \zeta^h \sigma_N(u)$ in $A$.
(d) $A$ is finite, so $u$ has a finite order $p^e c$ with $p \nmid c$. Let $v = u^c$, of order $p^e$. For $a \in \Gamma$, $v^a = \varepsilon(a)^c \sigma_a(v)$. If $a \equiv b \pmod{p^E}$, then $v^a = v^b$, and $\sigma_a = \sigma_b$ as $m \mid p^E$. So $\varepsilon(a)^c = \varepsilon(b)^c$, hence $\varepsilon(a) = \varepsilon(b)$ by Lemma 5, as $c$ is invertible modulo $m$. Also $a' \equiv b' \pmod m$. $\square$

**Fact F.** Let $p$ be odd, $f \ge 1$, and $a$ an integer with $v_p(a - 1) = f$. For $E \ge f$, the order of $a$ modulo $p^E$ is $p^{E - f}$, and the powers of $a$ modulo $p^E$ are exactly the residues $\equiv 1 \pmod{p^f}$.

*Proof.* If $a = 1 + p^f x$ with $p \nmid x$, then $a^p = 1 + p^{f+1} x + \binom p2 p^{2f} x^2 + \ldots \equiv 1 + p^{f+1} x \pmod{p^{f+2}}$, as $p$ is odd. By induction $v_p(a^{p^i} - 1) = f + i$, so the order is $p^{E-f}$. The residues $\equiv 1 \pmod{p^f}$ form a group of $p^{E-f}$ elements that contains the powers of $a$. $\square$

## 3. The conditions $L_p$ for odd $p$

For odd $p \mid t$, $L_p$ is: $v_p(r^{p-1} - 1) \ge v_p(N^{p-1} - 1)$ for every prime $r \mid N$. Write $f = v_p(N^{p-1} - 1) \ge 1$.

**Lemma 8 (proving $L_p$).** $L_p$ holds if $N^{p-1} \not\equiv 1 \pmod{p^2}$, or if for some prime $q \nmid N$ with $p \mid q - 1$ the check gives $S \equiv \zeta^h$ with $p \nmid h$.

*Proof.* In the first case $f = 1$, and $v_p(r^{p-1} - 1) \ge 1$ by Fermat. In the second case fix $r \mid N$, suppose $g = v_p(r^{p-1} - 1) < f$, and work in $A$ for this pair. Take $E \ge \max(e, k, f)$. By Fact F for $b = r^{p-1}$, $N^{p-1} \equiv b^j \pmod{p^E}$ for some $j \ge 0$, and as $b^j \equiv 1 \pmod{p^f}$ and $b$ has order $p^{f-g}$ modulo $p^f$, $p \mid j$. By Lemma 7, $N^{p-1}$ and $b^j$ lie in $\Gamma$, and $\lambda(N)^{p-1} = \lambda(r)^{(p-1)j} = \chi(r)^{-w(p-1)j}$. The left side is $\zeta^{hN'(p-1)}$, of order exactly $m$, as $p \nmid h N' (p-1)$. The right side is a $p$-th power in the group of order $m$, so its order divides $m/p$. This is a contradiction, so $g \ge f$. $\square$

**Lemma 9.** Suppose $L_p$ holds and every pair $(p, q)$ with $q$ in the plan passes line L11. Then there are integers $l(r)$, one for each prime $r \mid N$, such that $\chi_{p,q}(r) = \chi_{p,q}(N)^{l(r)}$ for every odd $q$ of the plan with $p \mid q - 1$, where $\chi_{p,q}$ is the character $\chi$ of that pair.

*Proof.* There are finitely many primes $r \mid N$ and pairs $(p, q)$; take $E$ at least $f + k$ and at least the $e$ of Lemma 7(d) for each of them. By $L_p$ and Fact F for $a = N^{p-1}$, each $r$ has an $l(r)$ with $r^{p-1} \equiv N^{(p-1) l(r)} \pmod{p^E}$, unique modulo $p^{E - f}$.

Fix a pair and $r$, and work in $A$. Both sides lie in $\Gamma$, so by Lemma 7, $\chi(r)^{-w(p-1)} = \lambda(N)^{(p-1) l(r)}$. As $p - 1$ and $w$ are invertible modulo $m$, $\chi(r)^{-w} = \lambda(N)^{l(r)}$ and $\chi(r) = \psi^{l(r)}$ with $\psi = \lambda(N)^{-w^{-1}} = \zeta^{-hN' w^{-1}}$, where $w^{-1}$ is the inverse modulo $m$. This $\psi$ depends only on the pair and $h$, not on $r$.

Now write $N = \prod r_i^{e_i}$. Then $N^{p-1} = \prod r_i^{(p-1)e_i} \equiv N^{(p-1) \sum e_i l(r_i)} \pmod{p^E}$, and as $N^{p-1}$ has order $p^{E-f}$ modulo $p^E$, $\sum e_i l(r_i) \equiv 1 \pmod{p^{E-f}}$, so also modulo $m$. Hence $\chi(N) = \prod \chi(r_i)^{e_i} = \psi^{\sum e_i l(r_i)} = \psi$, and $\chi(r) = \chi(N)^{l(r)}$. $\square$

## 4. The case $p = 2$

Here $L_2$ is: $v_2(r - 1) \ge v_2(N - 1)$ for every prime $r \mid N$. Let $\sigma = v_2(N - 1) \ge 1$. For an odd $q$ of the plan, the character of order $2 = 2^{v_2(q-1)}$ is the Legendre symbol $(\cdot/q)$, and $E_q = (-q)^{(N-1)/2} \bmod N$.

**Lemma 10.** (a) If some $E_q = N - 1$, then $L_2$ holds, and $L_2$ holds if $N \equiv 3 \pmod 4$. (b) If $N$ is not a square, $(z/N) = -1$ and $z^{(N-1)/2} \equiv -1 \pmod N$, then $L_2$ holds.

*Proof.* If $x^{(N-1)/2} \equiv -1 \pmod r$, the order $o$ of $x$ modulo $r$ divides $N - 1 = 2^\sigma n'$ but not $(N - 1)/2$, so $v_2(o) = \sigma$; as $o \mid r - 1$, $v_2(r - 1) \ge \sigma$. Apply this to $x = -q$ for (a) and to $x = z$ for (b). If $N \equiv 3 \pmod 4$, $\sigma = 1$, and $r - 1$ is even. $\square$

**Lemma 11.** Suppose $L_2$ holds and every odd $q$ of the plan has $E_q = \pm 1$. Let $l(r) = 1$ if $v_2(r - 1) = \sigma$ and $l(r) = 0$ otherwise. Then $(r/q) = (N/q)^{l(r)}$ for every prime $r \mid N$ and every odd $q$ of the plan.

*Proof.* Let $o$ be the order of $-q$ modulo $r$ and $\rho = v_2(r - 1) \ge \sigma$. By [Euler's criterion](/euler-criterion/), $(-q/r) = -1$ exactly when $o \nmid (r-1)/2$, that is when $v_2(o) = \rho$. If $E_q = -1$, $v_2(o) = \sigma$ as in Lemma 10, so $(-q/r) = (-1)^{l(r)}$. If $E_q = 1$, $o \mid (N-1)/2$, so $v_2(o) \le \sigma - 1 < \rho$ and $(-q/r) = 1$. In both cases $(-q/r) = E_q^{l(r)}$. By [quadratic reciprocity](/quadratic-reciprocity/), $(-q/r) = (-1)^{(r-1)/2} (q/r) = (-1)^{(r-1)/2 \, (1 + (q-1)/2)} (r/q) = (r/q)$, as $(q - 1)/2$ is odd. So $(r/q) = E_q^{l(r)}$.

Write $N = \prod r_i^{e_i}$. By $L_2$, $r_i \equiv 1 + 2^\sigma l(r_i) \pmod{2^{\sigma+1}}$, and as $2\sigma \ge \sigma + 1$, $N \equiv 1 + 2^\sigma \sum e_i l(r_i) \pmod{2^{\sigma+1}}$. Also $N \equiv 1 + 2^\sigma \pmod{2^{\sigma+1}}$, so $\sum e_i l(r_i)$ is odd, and $(N/q) = \prod (r_i/q)^{e_i} = E_q^{\sum e_i l(r_i)} = E_q$. Hence $(r/q) = (N/q)^{l(r)}$. $\square$

## 5. The final search

**Lemma 12.** Suppose $N$ reaches line L17. Then every prime $r \mid N$ has $r \equiv N^l \pmod s$ for some $0 \le l < t$.

*Proof.* Lines L11 and L14 passed for every pair of the plan. After line L16, done[$p$] is true for every prime $p \mid t$, each set by line L5, L6, L12, L15 or the extra check, so by Lemmas 8 and 10 every $L_p$ holds (for the extra check of an odd $p$ with a prime $q$ not in the plan, Lemma 8 applies with that $q$, as $q \nmid N$ is checked; Lemma 4 gives $p \nmid w$). Lemmas 9 and 11 give numbers $l_p(r)$ for every $p \mid t$. By the Chinese remainder theorem choose $0 \le l < t$ with $l \equiv l_p(r) \pmod{p^{v_p(t)}}$ for every $p \mid t$.

Fix an odd $q$ of the plan and $p^k \| q - 1$. As $p^k \mid p^{v_p(t)}$ and $\chi_{p,q}$ has order $p^k$, $\chi_{p,q}(r) = \chi_{p,q}(N)^l$ for every $p \mid q - 1$, so $\operatorname{ind}_g r \equiv l \operatorname{ind}_g N \pmod{p^k}$ for every such $p$, hence modulo $q - 1$, and $r \equiv N^l \pmod q$. Also $r \equiv N^l \equiv 1 \pmod 2$. As $s$ is the product of these distinct primes, $r \equiv N^l \pmod s$. $\square$

**Theorem 1 (prime answers are right).** If APR-CL$(N)$ returns prime, $N$ is prime.

*Proof.* Line L3 returns prime only for a prime of the plan or a prime factor of $t$. If the extra check of line L16 met a prime $q \mid N$, it continued only when $N = q$, which is prime. Otherwise the answer comes from line L20 and Lemma 12 applies. Suppose $N$ is composite there, and let $r$ be its least prime factor, so $r \le \sqrt N < s$. By Lemma 12, $r \equiv N^l \pmod s$ with $0 \le l < t$. As $1 < r < s$, $r = N^l \bmod s$, and $l \ne 0$ since $r \ne 1$. Lines L17 and L18 compute $N^i \bmod s$ for every $1 \le i < t$, so at $i = l$ or before, line L19 finds a number $r'$ with $1 < r' < N$ and $r' \mid N$, and returns composite. This contradicts the answer prime. $\square$

**Theorem 2 (composite answers are right).** If APR-CL$(N)$ returns composite, $N$ is composite.

*Proof.* We show that a prime $N$ never reaches a "composite". Line L1: $N \ge 2$. Line L4: a prime that is not in line L3 is coprime to $ts$. Line L11: in $A = R/NR$, Lemma 6 and Lemma 3(a) give $S \sigma_N(u) = u^N = \chi(N)^{-wN} \sigma_N(u)$, so $S \equiv \chi(N)^{-wN}$ modulo $NR$, hence modulo $N\mathbb{Z}[\zeta]$, as $R$ is free over $\mathbb{Z}[\zeta]$ with a basis that contains 1. Line L14: Euler's criterion gives $E = (-q/N) = \pm 1$. Line L16 for $p = 2$: a prime is not a square, the Jacobi symbol is the Legendre symbol, $(z/N) = 0$ is impossible for $z < N$, and $z^{(N-1)/2} \equiv (z/N) = -1$. Line L16 for odd $p$: a prime $q \mid N$ means $N = q$, which returns "proved", not composite, and the check of line L11 passes as above. Line L19: a prime has no factor $r$ with $1 < r < N$. $\square$

**Theorem 3 (termination).** APR-CL$(N)$ stops.

*Proof.* The plan comes from a finite table, and lines L7 to L15 run over finitely many pairs. Each power is a loop of $O(\log N)$ steps, and the search for $h$ at line L11 tries $m$ values. In the extra check for $p = 2$, a non-square $N = \prod p_i^{e_i}$ has some $e_i$ odd; by the Chinese remainder theorem there is a $z < N$ that is a non-residue modulo $p_i$ and $\equiv 1$ modulo the other prime powers, and $(z/N) = -1$. So the loop over $z$ stops at the latest at the least such $z$. The extra check for odd $p$ stops after 60 primes $q$ that it tests. The search of lines L17 to L19 has $t - 1$ steps. So every run stops, with prime, composite, or no answer from the cap of line L16. $\square$

$\blacksquare$
