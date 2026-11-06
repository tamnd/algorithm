---
title: The Solovay-Strassen test never rejects a prime, and on an odd composite each round passes with probability below 1/2
proves: [correctness, termination, error]
status: full
---

We use the pseudocode SOLOVAY-STRASSEN$(n, k)$ of the page. For an odd integer $n \ge 3$, $\mathbb{Z}_n^*$ is the group of residues coprime to $n$ under multiplication modulo $n$, and $\varphi(n)$ is its order. $\left(\frac{a}{n}\right)$ is the Jacobi symbol. We use these standard facts about it, for odd $n, m \ge 1$: it depends only on $a \bmod n$; it is multiplicative in $a$, that is $\left(\frac{ab}{n}\right) = \left(\frac{a}{n}\right)\left(\frac{b}{n}\right)$; it is multiplicative in the modulus, $\left(\frac{a}{nm}\right) = \left(\frac{a}{n}\right)\left(\frac{a}{m}\right)$; it is $0$ exactly when $\gcd(a, n) > 1$; for a prime $n$ it equals the Legendre symbol; and $\left(\frac{-1}{n}\right) = (-1)^{(n-1)/2}$. For an odd composite $n$, an *Euler liar* is a unit $a \in \mathbb{Z}_n^*$ with $a^{(n-1)/2} \equiv \left(\frac{a}{n}\right) \pmod n$, and $E(n)$ is the set of Euler liars.

**Termination.** The loop of lines L3 to L7 runs at most $k$ times. Each pass computes one Jacobi symbol, whose loop ends because the modulus decreases strictly at each swap, and one exponentiation, which ends. So the call ends.

**Lemma 1 (a prime is accepted).** If $n$ is prime, SOLOVAY-STRASSEN$(n, k)$ returns true for every choice of the random bases.

*Proof.* If $n \in \{2, 3\}$, line L1 returns true. Otherwise $n \ge 5$ is an odd prime, so lines L1 and L2 do not return. Each base of line L4 satisfies $2 \le a \le n - 2$, so $n \nmid a$, and $j = \left(\frac{a}{n}\right)$ is the Legendre symbol, which is $1$ or $-1$. So line L6 does not return. Euler's criterion gives $a^{(n-1)/2} \equiv \left(\frac{a}{n}\right) \pmod n$, so $a^{(n-1)/2} \bmod n = j \bmod n$ and line L7 does not return. Line L8 returns true. $\square$

**Lemma 2 (the answer false is right).** If SOLOVAY-STRASSEN$(n, k)$ returns false, then $n$ is not prime.

*Proof.* Line L1 returns false only for $n \in \{0, 1\}$, which are not prime. Line L2 returns false for an even $n \ge 4$, which has the factor 2 and is larger than 2. Lines L6 and L7 run only for odd $n \ge 5$, and by Lemma 1 neither returns when $n$ is prime. $\square$

**Lemma 3 (the liars form a subgroup).** Let $n \ge 5$ be odd and composite. Then $E(n)$ is a subgroup of $\mathbb{Z}_n^*$, and $1, n - 1 \in E(n)$. A base $a$ with $2 \le a \le n - 2$ passes a round (lines L6 and L7 do not return) if and only if $a \in E(n)$.

*Proof.* $1^{(n-1)/2} = 1 = \left(\frac{1}{n}\right)$, so $1 \in E(n)$. Also $(n-1)^{(n-1)/2} \equiv (-1)^{(n-1)/2} = \left(\frac{-1}{n}\right) = \left(\frac{n-1}{n}\right)$, so $n - 1 \in E(n)$. If $a, b \in E(n)$, then $(ab)^{(n-1)/2} = a^{(n-1)/2} b^{(n-1)/2} \equiv \left(\frac{a}{n}\right)\left(\frac{b}{n}\right) = \left(\frac{ab}{n}\right)$, so $ab \in E(n)$. A nonempty subset of a finite group that is closed under the product is a subgroup. For the last claim: if $\gcd(a, n) > 1$ then $j = 0$ and line L6 returns; if $\gcd(a, n) = 1$ then $j = \pm 1$, and line L7 does not return exactly when $a^{(n-1)/2} \equiv j \pmod n$, that is when $a \in E(n)$. $\square$

**Lemma 4 (the subgroup is proper).** Let $n \ge 5$ be odd and composite. Then $E(n) \ne \mathbb{Z}_n^*$, and so $|E(n)| \le \varphi(n)/2$.

*Proof.* We give a unit that is not a liar.

*Case 1: $p^2 \mid n$ for some prime $p$.* Let $a = 1 + n/p$. Since $p \mid n/p$, $n \mid (n/p)^2$, and by the binomial theorem $a^p = 1 + p \cdot (n/p) + \sum_{i \ge 2} \binom{p}{i} (n/p)^i \equiv 1 \pmod n$. So $a$ is a unit. Also $1 < a < n$, so $a \not\equiv 1$, and the order of $a$ is the prime $p$. Suppose $a \in E(n)$. Then $a^{(n-1)/2} \equiv \pm 1$, so $a^{n-1} \equiv 1$ and $p \mid n - 1$. With $p \mid n$ this gives $p \mid 1$, which is false.

*Case 2: $n$ is squarefree.* Then $n = pm$ with $p$ prime, $m > 1$ odd, and $\gcd(p, m) = 1$. As $p$ is odd, there is a quadratic non-residue $s$ modulo $p$. By the Chinese remainder theorem there is $a$ with $a \equiv s \pmod p$ and $a \equiv 1 \pmod m$; it is a unit modulo $n$. Then $\left(\frac{a}{n}\right) = \left(\frac{a}{p}\right)\left(\frac{a}{m}\right) = \left(\frac{s}{p}\right)\left(\frac{1}{m}\right) = -1$. Suppose $a \in E(n)$. Then $a^{(n-1)/2} \equiv -1 \pmod n$, so $a^{(n-1)/2} \equiv -1 \pmod m$. But $a \equiv 1 \pmod m$ gives $a^{(n-1)/2} \equiv 1 \pmod m$. So $m \mid 2$, which is false for odd $m > 1$.

In both cases $E(n)$ is a proper subgroup by Lemma 3. By Lagrange's theorem $|E(n)|$ divides $\varphi(n)$, and a proper divisor of $\varphi(n)$ is at most $\varphi(n)/2$. $\square$

**Theorem (error).** Let $n \ge 5$ be odd and composite, and let the bases of line L4 be independent and uniform on $[2, n-2]$. Then SOLOVAY-STRASSEN$(n, k)$ returns true with probability $q^k$, where $q = (|E(n)| - 2)/(n - 3) < 1/2$. So the error probability is less than $2^{-k}$, and it is zero for every prime $n$.

*Proof.* By Lemma 3, the call returns true exactly when all $k$ bases lie in $E(n) \cap [2, n-2] = E(n) \setminus \{1, n - 1\}$, which has $|E(n)| - 2$ elements (here $1 \ne n - 1$ as $n \ge 5$). The interval $[2, n-2]$ has $n - 3$ elements, so one round passes with probability $q$, and by independence all $k$ rounds pass with probability $q^k$. A composite $n$ has a divisor $d$ with $1 < d < n$, which is not a unit, so $\varphi(n) \le n - 2$. With Lemma 4, $|E(n)| - 2 \le (n-2)/2 - 2 = (n - 6)/2 < (n - 3)/2$, so $q < 1/2$ and $q^k < 2^{-k}$. For a prime $n$, Lemma 1 shows that the answer is always true, which is right; by Lemma 2 the answer false is always right. $\square$

Together, termination, Lemma 1, Lemma 2 and the theorem show that SOLOVAY-STRASSEN is a Monte Carlo algorithm for primality with one-sided error less than $2^{-k}$ on every input. $\blacksquare$
