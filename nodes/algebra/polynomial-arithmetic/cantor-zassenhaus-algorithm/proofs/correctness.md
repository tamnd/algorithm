---
title: CANTOR-ZASSENHAUS returns the complete factorization and stops with probability one
proves: [correctness]
status: full
---

Let $p$ be a prime, $\mathbb{F}_p = \mathbb{Z}/p\mathbb{Z}$, and $f \in \mathbb{F}_p[x]$ nonzero with $c = \mathrm{lc}(f)$. We use two facts from the pages on the stages. DISTINCT-DEGREE$(s)$, for monic square-free $s$, returns the pairs $(g, d)$ with $g \ne 1$ the product of the irreducible factors of $s$ of degree $d$. EQUAL-DEGREE$(g, d)$, for such $g$, returns the irreducible factors of $g$ and stops with probability $1$.

**Lemma 1 (derivative).** Let $u = \prod_q q^{e_q}$ be monic with distinct monic irreducible $q$. Then $\gcd(u, u') = \prod_{p \nmid e_q} q^{e_q - 1} \prod_{p \mid e_q} q^{e_q}$.

*Proof.* Fix one $q$ and write $u = q^{e} t$ with $q \nmid t$. Then $u' = q^{e - 1}(e\, q' t + q t')$. If $p \mid e$, the first term is zero and $q^e \mid u'$. If $p \nmid e$, then $q \nmid e\, q' t$: $q \nmid t$, and $q' \ne 0$ has degree less than $\deg q$, since an irreducible $q$ with $q' = 0$ would be a $p$-th power $\left(\sum_j a_{jp} x^j\right)^p$. So $q^{e-1}$ is the exact power of $q$ that divides $u'$. Taking the minimum with $e_q$ for every $q$ gives the claim. $\square$

**Lemma 2 ($p$-th roots).** If every exponent of $v = \sum_i a_i x^i$ is a multiple of $p$, then $v = \left(\sum_j a_{jp} x^j\right)^p$.

*Proof.* In characteristic $p$, $(y + z)^p = y^p + z^p$, and $a^p = a$ for $a \in \mathbb{F}_p$ by Fermat's little theorem. So $\left(\sum_j a_{jp} x^j\right)^p = \sum_j a_{jp}^p x^{jp} = \sum_j a_{jp} x^{jp} = v$. $\square$

**Invariant of the work list.** We prove by induction on the pushes: for every pair $(u, k)$ on the work list, $k = p^j$ for some $j \ge 0$, and $u = \prod q^{e_q / k}$, the product over the irreducible $q \mid f$ with $p^j \mid e_q$, where $e_q$ is the multiplicity of $q$ in $f$.

*Base.* At line L1, $(f/c, 1)$ has this form with $j = 0$.

*Step.* Let $(u, k)$ with $k = p^j$ be popped at line L3, and write $\epsilon_q = e_q / k$ for the multiplicities in $u$. By Lemma 1, line L3 gives $v = \prod_{p \nmid \epsilon_q} q^{\epsilon_q - 1} \prod_{p \mid \epsilon_q} q^{\epsilon_q}$ and $w = u / v = \prod_{p \nmid \epsilon_q} q$. Claim: before the test at line L4,

$$w = \prod_{p \nmid \epsilon_q,\ \epsilon_q \ge i} q, \qquad v = \prod_{p \nmid \epsilon_q,\ \epsilon_q \ge i} q^{\epsilon_q - i} \prod_{p \mid \epsilon_q} q^{\epsilon_q}.$$

This holds for $i = 1$. At line L5, every $q \mid w$ has $p \nmid \epsilon_q$, and $q \mid v$ exactly when $\epsilon_q > i$, so $y = \prod_{p \nmid \epsilon_q,\ \epsilon_q > i} q$ and $s = \prod_{p \nmid \epsilon_q,\ \epsilon_q = i} q$. Line L9 then makes $w = y$ and divides each exponent $\epsilon_q - i \ge 1$ in $v$ by one factor $q$, which is the claim for $i + 1$.

The loop ends when $w = 1$, that is, when no $q$ with $p \nmid \epsilon_q$ has $\epsilon_q \ge i$. Then $v = \prod_{p \mid \epsilon_q} q^{\epsilon_q}$. All exponents of $v$ as a polynomial are multiples of $p$, since $v$ is the $p$-th power of $\prod_{p \mid \epsilon_q} q^{\epsilon_q / p}$, and by Lemma 2 and unique factorization, the $p$-th root at line L10 is $\prod_{p \mid \epsilon_q} q^{\epsilon_q / p} = \prod_{p^{j+1} \mid e_q} q^{e_q / (p k)}$. So the pushed pair $(\cdot, p k)$ has the claimed form with $j + 1$. $\square$

**Output.** In the step above, each $q$ with $p^j \mid e_q$ and $p \nmid e_q / p^j$ is in $s$ exactly once, at $i = \epsilon_q = e_q / k$. Then $s$ is monic and square-free, so by the facts on DISTINCT-DEGREE and EQUAL-DEGREE, lines L7 and L8 append $(q, i k) = (q, e_q)$, and only such pairs. Every irreducible $q \mid f$ has a unique $j$ with $p^j \mid e_q$ and $p \nmid e_q / p^j$, and the pair with $k = p^j$ is on the work list by the invariant, since $p^{j'} \mid e_q$ for all $j' \le j$. So the result lists every $(q, e_q)$ exactly once, and line L11 returns $c$ and this list. Then $f = c \prod_q q^{e_q}$.

**Termination.** For a pushed pair with $k = p^{j}$, $\deg u \le n / p^{j}$, so $j \le \log_p n$ for $u \ne 1$, and a pair is pushed only if $v \ne 1$. So at most $\log_p n + 1$ pairs are popped. In the inner loop at line L4, $i$ grows by one per step, and $w = 1$ as soon as $i$ exceeds every $\epsilon_q$, so it stops after at most $\deg u$ steps. Each call of EQUAL-DEGREE stops with probability $1$. So the algorithm stops with probability $1$. $\blacksquare$
