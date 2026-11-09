---
title: Miller-Rabin never rejects a prime, and a composite passes a random base with probability at most 1/2 (1/4 by Rabin and Monier)
proves: [correctness]
status: full
---

Let $n \ge 5$ be odd, and let line L2 write $n - 1 = 2^s d$ with $d$ odd, so $s \ge 1$. For a base $a$ with $1 \le a \le n - 1$, lines L5 to L10 compute $x_0 = a^d \bmod n$ and $x_{i} = x_{i-1}^2 \bmod n = a^{2^i d} \bmod n$ for $i = 1, \dots, s - 1$, and they accept $a$ exactly when

$$x_0 = 1 \quad \text{or} \quad x_j = n - 1 \text{ for some } 0 \le j \le s - 1. \tag{$\ast$}$$

A base that satisfies $(\ast)$ for a composite $n$ is a **strong liar**; let $S(n)$ be the set of strong liars. Write $\mathbb{Z}_n^*$ for the group of units modulo $n$, of order $\varphi(n)$.

**Lemma 1 (primes pass).** If $n$ is prime, every base $a$ with $1 \le a \le n - 1$ satisfies $(\ast)$.

*Proof.* By Fermat's little theorem $x_s = a^{n-1} \equiv 1 \pmod n$. Modulo a prime, $x^2 \equiv 1$ means $n \mid (x - 1)(x + 1)$, so $x \equiv \pm 1$. If $x_0 = 1$ we are done. Otherwise let $i \ge 1$ be the least index with $x_i = 1$; it exists because $x_s = 1$. Then $x_{i-1}^2 = 1$ and $x_{i-1} \ne 1$, so $x_{i-1} = n - 1$ with $i - 1 \le s - 1$. $\square$

So line L10 never returns COMPOSITE for a prime, and line L1 handles $n < 5$ and even $n$ correctly. A COMPOSITE answer is always right.

**Lemma 2 (strong liars are units).** Every $a \in S(n)$ is in $\mathbb{Z}_n^*$.

*Proof.* $(\ast)$ gives $a^{m} \equiv \pm 1$ for some $m \ge 1$, so $a \cdot a^{m-1} \equiv \pm 1$ and $a$ has an inverse. $\square$

**Lemma 3 (the strong liars lie in a proper subgroup).** For odd composite $n$ there is a subgroup $H \subsetneq \mathbb{Z}_n^*$ with $S(n) \subseteq H$.

*Proof.* Two cases.

*Case 1: $n = p^e$ with $p$ prime and $e \ge 2$.* Let $H = \{x \in \mathbb{Z}_n^* : x^{n-1} \equiv 1\}$. It is a subgroup, since it is closed under products and contains 1, and $\mathbb{Z}_n^*$ is finite. It contains $S(n)$, because $(\ast)$ gives $a^{n-1} = (a^{2^j d})^{2^{s-j}} \equiv 1$ in both cases of $(\ast)$. Let $g = 1 + p^{e-1}$. By the binomial theorem, $g^t \equiv 1 + t p^{e-1} \pmod{p^e}$, because $p^{2(e-1)}$ is divisible by $p^e$ when $e \ge 2$. So $g^t \equiv 1$ if and only if $p \mid t$. Since $p \mid n$, $p \nmid n - 1$, so $g^{n-1} \not\equiv 1$ and $g \notin H$.

*Case 2: $n$ is not a prime power.* Then $n = n_1 n_2$ with $\gcd(n_1, n_2) = 1$ and $n_1, n_2 \ge 3$. The base $n - 1 \equiv -1$ satisfies $(-1)^{2^0 d} = -1$ since $d$ is odd. So the set of $j \in \{0, \dots, s - 1\}$ such that some $v \in \mathbb{Z}_n^*$ has $v^{2^j d} \equiv -1$ is not empty; let $j_0$ be its largest element, $v$ a unit with $v^{2^{j_0} d} \equiv -1$, and $m = 2^{j_0} d$. Let

$$H = \{x \in \mathbb{Z}_n^* : x^{m} \equiv \pm 1 \pmod n\}.$$

$H$ is a subgroup, since $(xy)^m = x^m y^m \equiv \pm 1$. It contains $S(n)$: if $a^d \equiv 1$ then $a^m \equiv 1$; if $a^{2^j d} \equiv -1$ with $j \le s - 1$, then $j \le j_0$ by the choice of $j_0$, and $a^m = (a^{2^j d})^{2^{j_0 - j}} \equiv \pm 1$. By the [Chinese remainder theorem](/chinese-remainder-theorem/) there is $w$ with $w \equiv v \pmod{n_1}$ and $w \equiv 1 \pmod{n_2}$; it is a unit. Then $w^m \equiv -1 \pmod{n_1}$ and $w^m \equiv 1 \pmod{n_2}$. If $w^m \equiv 1 \pmod n$, then $-1 \equiv 1 \pmod{n_1}$, so $n_1 \mid 2$, which is false. If $w^m \equiv -1 \pmod n$, then $1 \equiv -1 \pmod{n_2}$, also false. So $w \notin H$. $\square$

**Theorem (the bound 1/2).** Let $n \ge 5$ be odd and composite. Then $|S(n)| \le \varphi(n)/2$, and a base drawn uniformly from $\{2, \dots, n - 2\}$ (line L4) is a strong liar with probability at most $1/2$. So MILLER-RABIN$(n, k)$ returns PROBABLY PRIME with probability at most $2^{-k}$.

*Proof.* By Lemma 3 and [Lagrange's theorem](/lagranges-theorem-group-theory/), $|H|$ divides $\varphi(n)$ and $|H| < \varphi(n)$, so $|S(n)| \le |H| \le \varphi(n)/2$. The bases $1$ and $n - 1$ are always strong liars and line L4 never draws them, so the probability is $(|S(n)| - 2)/(n - 3) \le (\varphi(n)/2 - 2)/(n - 3) < 1/2$, using $\varphi(n) \le n - 1$. The $k$ rounds draw independent bases, and the answer is PROBABLY PRIME only if all $k$ are liars. $\blacksquare$

**Theorem (the bound 1/4, Rabin 1980 and Monier 1980).** For odd composite $n \ne 9$, $|S(n)| \le \varphi(n)/4$; for $n = 9$, $|S(9)| = 2 = (n - 1)/4$. So a uniform base from $\{2, \dots, n - 2\}$ is a liar with probability at most $1/4$, since $(|S| - 2)/(n - 3) \le 1/4$ is equivalent to $4|S| \le n + 5$. This is the bound in use; we cite it and do not prove it here. Monier gave the exact count: if $n = \prod_{i=1}^{k} p_i^{e_i}$ and $\nu = \min_i v_2(p_i - 1)$, then

$$|S(n)| = \left(1 + \frac{2^{k\nu} - 1}{2^k - 1}\right) \prod_{i=1}^{k} \gcd\big(\mathrm{odd}(n - 1), \mathrm{odd}(p_i - 1)\big),$$

where $\mathrm{odd}(x)$ is the largest odd divisor of $x$. The tests check this formula and the bound $\varphi(n)/4$ against a brute-force count for every odd composite below 2000; the ratio $\varphi(n)/4$ is reached at $n = 15, 91, 703, 1891$ in that range.

**Lemma 4 (strong liars are Euler liars).** For odd composite $n$, every strong liar $a$ satisfies $a^{(n-1)/2} \equiv \left(\frac{a}{n}\right) \pmod n$, where $\left(\frac{a}{n}\right)$ is the [Jacobi symbol](/jacobi-symbol/). If $n \equiv 3 \pmod 4$, the two sets of liars are equal.

*Proof.* $a$ is a unit by Lemma 2, so $\left(\frac{a}{n}\right) = \pm 1$.

*Case $a^d \equiv 1$.* Then $a^{(n-1)/2} = (a^d)^{2^{s-1}} \equiv 1$, and $\left(\frac{a}{n}\right) = \left(\frac{a}{n}\right)^d = \left(\frac{a^d}{n}\right) = \left(\frac{1}{n}\right) = 1$, since $d$ is odd and the symbol is multiplicative in the top argument.

*Case $a^{2^j d} \equiv -1$ with $0 \le j \le s - 1$.* Then $a^{(n-1)/2} = (a^{2^j d})^{2^{s-1-j}}$ is $-1$ if $j = s - 1$ and $1$ if $j < s - 1$. Fix a prime $p \mid n$. Modulo $p$, $a^{2^j d} \equiv -1$ and $a^{2^{j+1} d} \equiv 1$, so the order of $a$ modulo $p$ is $2^{j+1} t$ with $t$ odd. It divides $p - 1$, so $v_2(p - 1) \ge j + 1$. By [Euler's criterion](/euler-criterion/), $\left(\frac{a}{p}\right) = -1$ if and only if the order does not divide $(p-1)/2$, that is, if and only if $v_2(p - 1) = j + 1$. Let $T$ be the number of prime factors of $n$, counted with multiplicity, with $v_2(p - 1) = j + 1$. Then $\left(\frac{a}{n}\right) = (-1)^T$. Each prime factor is $\equiv 1 + 2^{j+1}$ or $\equiv 1 \pmod{2^{j+2}}$, by whether it is counted in $T$. As $(1 + 2^{j+1})^T \equiv 1 + T\,2^{j+1} \pmod{2^{j+2}}$, we get $n - 1 \equiv T\,2^{j+1} \pmod{2^{j+2}}$. So $T$ is odd if and only if $v_2(n - 1) = j + 1$, that is, $j = s - 1$. Both sides are $-1$ exactly when $j = s - 1$.

If $n \equiv 3 \pmod 4$, then $s = 1$ and $(\ast)$ says $a^{(n-1)/2} \equiv \pm 1$. An Euler liar has $a^{(n-1)/2} \equiv \left(\frac{a}{n}\right) = \pm 1$, so it is a strong liar. $\square$

Lemma 4 shows that one round of Miller-Rabin is never weaker than one round of the [Solovay-Strassen test](/solovay-strassen-primality-test/) with the same base. The inclusion can be strict: for $n = 45$ there are 2 strong liars and 4 Euler liars, the extra ones being 19 and 26; for the Carmichael number 561 there are 10 and 80.
