---
title: The Fermat test never rejects a prime, and its error on a composite is q^k with q given by the number of liars
proves: [correctness, termination, error]
status: full
---

We use the pseudocode FERMAT-PRIMALITY-TEST$(n, k)$ of the page. For an integer $n \ge 2$, $(\mathbb{Z}/n\mathbb{Z})^*$ is the group of residues coprime to $n$ under multiplication modulo $n$, and $\varphi(n)$ is its order. A *liar* for an odd composite $n$ is an $a \in [1, n-1]$ with $a^{n-1} \equiv 1 \pmod n$, and $L(n)$ is the set of liars. A *Carmichael number* is a composite $n$ with $a^{n-1} \equiv 1 \pmod n$ for every $a$ coprime to $n$.

**Termination.** The loop of lines L3 to L5 runs at most $k$ times, and each pass does one exponentiation, which ends. So the call ends.

**Lemma 1 (a prime is accepted).** If $n$ is prime, FERMAT-PRIMALITY-TEST$(n, k)$ returns true for every choice of the random bases.

*Proof.* If $n \in \{2, 3\}$, line L1 returns true. Otherwise $n \ge 5$ is an odd prime, so line L2 does not return. Each base of line L4 satisfies $2 \le a \le n - 2$, so $n \nmid a$, and Fermat's little theorem gives $a^{n-1} \equiv 1 \pmod n$. So line L5 never returns, and line L6 returns true. $\square$

**Lemma 2 (the answer false is right).** If FERMAT-PRIMALITY-TEST$(n, k)$ returns false, then $n$ is not prime.

*Proof.* Line L1 returns false only for $n \in \{0, 1\}$, which are not prime. Line L2 returns false for an even $n \ge 4$, which has the factor 2 and is larger than 2. Line L5 returns false only when $a^{n-1} \not\equiv 1 \pmod n$, and by Lemma 1 this is impossible for a prime $n$. $\square$

**Lemma 3 (liars are units and form a subgroup).** Let $n \ge 5$ be odd and composite. Each liar is coprime to $n$. The set $L(n)$ is a subgroup of $(\mathbb{Z}/n\mathbb{Z})^*$, and it contains $1$ and $n - 1$.

*Proof.* If $a^{n-1} \equiv 1 \pmod n$, then $a \cdot a^{n-2} \equiv 1$, so $a$ has an inverse modulo $n$ and $\gcd(a, n) = 1$. The residue $1$ is a liar. If $a, b \in L(n)$, then $(ab)^{n-1} = a^{n-1} b^{n-1} \equiv 1$, so $L(n)$ is closed under products. A nonempty finite subset of a finite group that is closed under products is a subgroup, because each element $x$ has finite order $m$ and $x^{-1} = x^{m-1}$ is a product of copies of $x$. Finally $(n-1)^{n-1} \equiv (-1)^{n-1} = 1$, since $n - 1$ is even. $\square$

**Lemma 4 (at most half are liars).** Let $n \ge 5$ be odd, composite and not a Carmichael number. Then $|L(n)| \le \varphi(n)/2$, and the number of liars in $[2, n-2]$, divided by $n - 3$, is less than $1/2$.

*Proof.* Since $n$ is not a Carmichael number, some $b$ coprime to $n$ has $b^{n-1} \not\equiv 1$, so $L(n)$ is a proper subgroup of $(\mathbb{Z}/n\mathbb{Z})^*$ by Lemma 3. By Lagrange's theorem its order divides $\varphi(n)$ and is smaller, so $|L(n)| \le \varphi(n)/2$. The liars in $[2, n-2]$ are $L(n)$ without $1$ and $n - 1$, which are distinct since $n \ge 5$, so there are $|L(n)| - 2 \le \varphi(n)/2 - 2$ of them. As $\varphi(n) \le n - 1$,

$$\frac{\varphi(n)/2 - 2}{n - 3} \le \frac{(n-1)/2 - 2}{n - 3} = \frac{n - 5}{2(n - 3)} < \frac{1}{2}. \qquad \square$$

**Lemma 5 (the number of liars).** Let $n = \prod_{i=1}^{r} p_i^{e_i}$ be odd and at least 3, with distinct primes $p_i$. Then $|L(n)| = \prod_{i=1}^{r} \gcd(n - 1, p_i - 1)$, where for a prime $n$ the set $L(n)$ means all $a \in [1, n-1]$ with $a^{n-1} \equiv 1$.

*Proof.* By the [Chinese remainder theorem](/chinese-remainder-theorem/), $a \bmod n$ corresponds to the tuple $(a \bmod p_i^{e_i})_i$, and $a^{n-1} \equiv 1 \pmod n$ holds if and only if $a^{n-1} \equiv 1 \pmod{p_i^{e_i}}$ for each $i$. So $|L(n)|$ is the product of the numbers $N_i$ of solutions of $x^{n-1} \equiv 1$ modulo $p_i^{e_i}$. Each solution is a unit, as in Lemma 3. For an odd prime $p$, the group $(\mathbb{Z}/p^e\mathbb{Z})^*$ is cyclic of order $m = p^{e-1}(p - 1)$ (see [existence of primitive roots](/primitive-roots-existence/)). In a cyclic group with generator $g$ and order $m$, the element $g^j$ with $0 \le j < m$ satisfies $(g^j)^t = 1$ if and only if $m \mid jt$, that is $\frac{m}{d} \mid j$ with $d = \gcd(t, m)$, and exactly $d$ values of $j$ in $[0, m)$ have this property. So $N_i = \gcd(n - 1, p_i^{e_i - 1}(p_i - 1))$. Since $p_i \mid n$, $p_i \nmid n - 1$, so the factor $p_i^{e_i - 1}$ does not change the gcd, and $N_i = \gcd(n - 1, p_i - 1)$. $\square$

For a Carmichael number every unit is a liar, so $|L(n)| = \varphi(n)$; this is consistent with Lemma 5 and Korselt's criterion that $p_i - 1 \mid n - 1$ for each $i$ and $n$ is squarefree.

**Theorem (error).** Let $n \ge 5$ be odd and composite, and let $q = (|L(n)| - 2)/(n - 3)$. Then FERMAT-PRIMALITY-TEST$(n, k)$ returns true with probability exactly $q^k$. If $n$ is not a Carmichael number, then $q < 1/2$, and the probability is less than $2^{-k}$. If $n$ is a Carmichael number, then $q = (\varphi(n) - 2)/(n - 3)$.

*Proof.* Lines L1 and L2 do not return for odd $n \ge 5$. The call returns true if and only if each of the $k$ bases drawn by line L4 is a liar. The $k$ draws are independent and uniform on the $n - 3$ integers of $[2, n-2]$, and $|L(n)| - 2$ of them are liars, by Lemma 3. So the probability is $q^k$. Lemma 4 gives $q < 1/2$ when $n$ is not a Carmichael number. For a Carmichael number, $|L(n)| = \varphi(n)$ by the definition and Lemma 3. $\blacksquare$

**Remark.** The bound depends only on $n$ and $k$; no assumption on the distribution of inputs is used. It cannot be made uniform: for a Carmichael number $n = p_1 p_2 p_3$ with $p_1 < p_2 < p_3$, $q \ge (\varphi(n) - 2)/n$, and $\varphi(n)/n = \prod (1 - 1/p_i) \ge (1 - 1/p_1)^3$ tends to 1 as $p_1$ grows.
