---
title: BROWN-GCD returns gcd(f, g) and stops after finitely many primes
proves: [correctness]
status: full
---

Let $f, g \in \mathbb{Z}[x]$ be nonzero and not constant after line L1, so that $f$ and $g$ are primitive with positive leading coefficients. (If one input is zero or a constant, the implementation answers directly, and the answer is the gcd by definition.) Let $G = \gcd(f, g)$ in $\mathbb{Z}[x]$, primitive with $\mathrm{lc}(G) > 0$, and $b = \gcd(\mathrm{lc} f, \mathrm{lc} g)$. For $a \in \mathbb{Z}[x]$, $\|a\|_1$ and $\|a\|_\infty$ are the sum and the largest absolute value of the coefficients. The primes come from a list of distinct primes, and only primes $p \nmid b$ reach line L4.

**Lemma 1 (contents).** $\gcd(f_0, g_0) = \gcd(\mathrm{cont} f_0, \mathrm{cont} g_0) \cdot \gcd(\mathrm{pp} f_0, \mathrm{pp} g_0)$ for the original inputs $f_0, g_0$.

*Proof.* This is a consequence of [Gauss's lemma](/gauss-lemma/): the product of primitive polynomials is primitive, so contents and primitive parts of common divisors split independently. $\square$

So it is enough to show that line L10 returns $c \cdot G$ with $c = \gcd(\mathrm{cont} f_0, \mathrm{cont} g_0)$.

**Lemma 2 (images).** Let $p \nmid b$ and let $v_p$ be the monic gcd of $f \bmod p$ and $g \bmod p$. Then $\deg v_p \ge \deg G$, and if equality holds, $b\, v_p \equiv (b/\mathrm{lc}\, G)\, G \pmod p$.

*Proof.* $\mathrm{lc}(G)$ divides $\mathrm{lc}(f)$ and $\mathrm{lc}(g)$, so it divides $b$, and $p \nmid \mathrm{lc}(G)$. Hence $G \bmod p$ has degree $\deg G$. It divides $f \bmod p$ and $g \bmod p$, so it divides $v_p$ in $(\mathbb{Z}/p\mathbb{Z})[x]$, and $\deg v_p \ge \deg G$. If the degrees are equal, $v_p = G \cdot \mathrm{lc}(G)^{-1} \bmod p$, since both are monic and one divides the other. Multiplying by $b$ gives the claim, and $b/\mathrm{lc}(G)$ is an integer. $\square$

Call $p$ lucky if $\deg v_p = \deg G$. Let $H^\circ = (b/\mathrm{lc}\, G)\, G$, $U^\circ = \mathrm{lc}(G)\, f/G$ and $W^\circ = \mathrm{lc}(G)\, g/G$. These are in $\mathbb{Z}[x]$, and $b f = H^\circ U^\circ$, $b g = H^\circ W^\circ$.

**Invariant.** After line L8, $d$ is the smallest degree $\deg v_p$ seen so far, $m$ is the product of the primes $p$ seen so far with $\deg v_p = d$ since the last restart, and $H, U, W$ have coefficients in the symmetric range modulo $m$ with

$$H \equiv b\, v_p,\quad U \equiv f / v_p,\quad W \equiv g / v_p \pmod p \quad \text{for each such } p, \qquad b f \equiv H U,\quad b g \equiv H W \pmod m,$$

and the coefficient of $x^d$ in $H$ is $\equiv b \not\equiv 0 \pmod p$ for every $p \mid m$, so $\deg H = d$.

*Proof.* Line L5 discards primes of larger degree, line L6 restarts with one prime when the degree drops or at the first prime, and line L7 combines a new image of the same degree, so the first part follows by induction, using that the Chinese remainder theorem gives the unique residue modulo $m p$ with the given residues modulo $m$ and $p$. For each $p \mid m$, $b f \equiv b\, v_p \cdot (f/v_p) \equiv H U \pmod p$, and the same holds for $g$; the primes are distinct, so the congruences hold modulo $m$. Finally $v_p$ is monic of degree $d$, so the coefficient of $x^d$ in $H$ is $\equiv b \pmod p$, and higher coefficients are $0$. $\square$

**Lemma 3 (the test is sound).** If the test at line L9 passes, then $\mathrm{pp}(H) = G$.

*Proof.* Every coefficient of $H U$ has absolute value at most $\|H\|_1 \|U\|_1 < m/2$, and every coefficient of $b f$ has absolute value less than $m/2$. Two integers in $(-m/2, m/2)$ that are congruent modulo $m$ are equal, so $b f = H U$ in $\mathbb{Z}[x]$, and in the same way $b g = H W$. So $H$ divides $b f$ and $b g$, and so does $\mathrm{pp}(H)$. As $\mathrm{pp}(H)$ is primitive, Gauss's lemma gives $\mathrm{pp}(H) \mid f$ and $\mathrm{pp}(H) \mid g$, so $\mathrm{pp}(H)$ divides $G$. By Lemma 2, every image has degree at least $\deg G$, so $\deg \mathrm{pp}(H) = d \ge \deg G$. A divisor of $G$ of degree at least $\deg G$ is $\pm G$, and both have positive leading coefficients, so $\mathrm{pp}(H) = G$. $\square$

With Lemma 1, the returned value $c \cdot \mathrm{pp}(H)$ is $\gcd(f_0, g_0)$.

**Lemma 4 (unlucky primes are finite).** If $p \nmid b$ is unlucky, then $p$ divides the resultant $r = \mathrm{res}(f/G, g/G)$, which is a nonzero integer.

*Proof.* $f/G$ and $g/G$ are coprime in $\mathbb{Q}[x]$, so $r \ne 0$. Since $p \nmid b$, $p$ does not divide both leading coefficients, say $p \nmid \mathrm{lc}(f)$, hence $p \nmid \mathrm{lc}(f/G)$. Then $r \bmod p$ equals, up to a power of $\mathrm{lc}(f/G)$ and a sign, the resultant of the reductions, and it is zero if the reductions have a common factor of positive degree. If $p$ is unlucky, $v_p$ has degree greater than $\deg G$, so $v_p / (G \bmod p)$ is a common factor of $(f/G) \bmod p$ and $(g/G) \bmod p$ of positive degree, and $p \mid r$. $\square$

**Termination.** Only finitely many primes are unlucky by Lemma 4, and each is either discarded at line L5 or causes a restart at line L6 that a later lucky prime undoes, since a lucky prime has the smallest possible degree $\deg G$. After the last unlucky prime in the list, every prime $p \nmid b$ is lucky, $d = \deg G$, and by Lemma 2 and the invariant, $H \equiv H^\circ$, $U \equiv U^\circ$, $W \equiv W^\circ \pmod m$. Once $m > 2 \max(\|H^\circ\|_1 \|U^\circ\|_1, \|H^\circ\|_1 \|W^\circ\|_1, \|H^\circ\|_\infty, \|U^\circ\|_\infty, \|W^\circ\|_\infty, \|b f\|_\infty, \|b g\|_\infty)$, the symmetric residues at line L8 are $H^\circ, U^\circ, W^\circ$ themselves, and the test at line L9 passes. The list must contain enough primes; the implementation raises an error otherwise. $\blacksquare$
