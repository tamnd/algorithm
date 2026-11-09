---
title: Solovay-Strassen never rejects a prime, and the Euler liars of a composite form a proper subgroup
proves: [correctness]
status: full
---

Let $n \ge 5$ be odd. Write $\left(\frac{a}{n}\right)$ for the [Jacobi symbol](/jacobi-symbol/), $\mathbb{Z}_n^*$ for the group of units modulo $n$, of order $\varphi(n)$, and $e = (n-1)/2$. A round with base $a$ (lines L4 to L6) passes exactly when

$$\left(\frac{a}{n}\right) \ne 0 \quad \text{and} \quad a^{e} \equiv \left(\frac{a}{n}\right) \pmod n. \tag{$\ast$}$$

For composite $n$, a base with $(\ast)$ is an **Euler liar**; let $E(n)$ be the set of Euler liars in $\{1, \dots, n - 1\}$.

**Lemma 1 (JACOBI is correct).** For odd $n \ge 1$ and any integer $a$, lines L8 to L14 return $\left(\frac{a}{n}\right)$.

*Proof.* Let $a_0, n_0$ be the input. We show that $t \cdot \left(\frac{a}{n}\right) = \left(\frac{a_0}{n_0}\right)$ holds at the start of each pass of line L9, with $n$ odd and $0 \le a < n$. Line L8 makes it true, since the symbol depends only on $a \bmod n$. In line L10, $\left(\frac{2}{n}\right) = -1$ exactly when $n \equiv 3, 5 \pmod 8$, and the symbol is multiplicative in the top argument, so halving $a$ and flipping $t$ in these cases keeps the equation. After line L10, $a$ is odd. Line L11 swaps the two, and line L12 applies [quadratic reciprocity](/quadratic-reciprocity/) for the Jacobi symbol: for odd positive $a, n$, $\left(\frac{a}{n}\right) = \left(\frac{n}{a}\right)$ unless $a \equiv n \equiv 3 \pmod 4$, when the sign flips. (If $\gcd(a, n) > 1$, both symbols are 0 and the equation holds for any sign.) Line L13 reduces the top argument again. The pair $(a, n)$ follows the Euclidean algorithm, so $a$ reaches 0 after $O(\log n_0)$ passes. Then $n = \gcd(a_0, n_0)$ up to the factors of 2 that line L10 removed, which are coprime to the odd $n_0$; so $n = \gcd(a_0, n_0)$. If $n = 1$, then $\left(\frac{0}{1}\right) = 1$ and line L14 returns $t = \left(\frac{a_0}{n_0}\right)$. If $n > 1$, then $\gcd(a_0, n_0) > 1$, the symbol is 0, and line L14 returns 0. $\square$

**Lemma 2 (primes pass).** If $n$ is an odd prime, every $a$ with $1 \le a \le n - 1$ satisfies $(\ast)$.

*Proof.* For a prime the Jacobi symbol is the [Legendre symbol](/legendre-symbol/), which is $\pm 1$ for $a \not\equiv 0$. [Euler's criterion](/euler-criterion/) says $a^{(n-1)/2} \equiv \left(\frac{a}{n}\right) \pmod n$. $\square$

So a COMPOSITE answer is always right.

**Lemma 3 (the Euler liars form a subgroup).** For odd composite $n$, $E(n)$ is a subgroup of $\mathbb{Z}_n^*$.

*Proof.* A liar has $\left(\frac{a}{n}\right) \ne 0$, so $\gcd(a, n) = 1$ and $a \in \mathbb{Z}_n^*$. $1 \in E(n)$. If $a, b \in E(n)$, then $(ab)^e = a^e b^e \equiv \left(\frac{a}{n}\right)\left(\frac{b}{n}\right) = \left(\frac{ab}{n}\right)$, by multiplicativity, so $ab \in E(n)$. A nonempty subset of a finite group that is closed under products is a subgroup. $\square$

**Lemma 4 (the subgroup is proper).** For odd composite $n$, there is $g \in \mathbb{Z}_n^* \setminus E(n)$.

*Proof.* Two cases.

*Case 1: $p^2 \mid n$ for a prime $p$.* Let $g = 1 + n/p$. Then $p \mid n/p$, so $(n/p)^2$ is divisible by $n$, and the binomial theorem gives $g^t \equiv 1 + t\,n/p \pmod n$. So $g^t \equiv 1$ if and only if $p \mid t$; $g$ is a unit of order $p$. If $g$ were a liar, then $g^{e} \equiv \pm 1$, so $g^{n-1} \equiv 1$, so $p \mid n - 1$. But $p \mid n$, so $p \nmid n - 1$. Hence $g \notin E(n)$.

*Case 2: $n$ is squarefree.* Then $n = p m$ with $p$ prime, $m > 1$ and $\gcd(p, m) = 1$. Let $c$ be a quadratic non-residue modulo $p$. By the [Chinese remainder theorem](/chinese-remainder-theorem/) there is $g$ with $g \equiv c \pmod p$ and $g \equiv 1 \pmod m$. It is a unit, and

$$\left(\frac{g}{n}\right) = \left(\frac{g}{p}\right)\left(\frac{g}{m}\right) = \left(\frac{c}{p}\right)\left(\frac{1}{m}\right) = -1.$$

But $g^{e} \equiv 1 \pmod m$. If $g$ were a liar, then $g^e \equiv -1 \pmod n$, so $1 \equiv -1 \pmod m$, so $m \mid 2$, which is false for odd $m > 1$. Hence $g \notin E(n)$. $\square$

**Theorem.** If $n$ is prime, SOLOVAY-STRASSEN$(n, k)$ returns PRIME or PROBABLY PRIME. If $n$ is an odd composite, $|E(n)| \le \varphi(n)/2$, a base uniform on $\{2, \dots, n - 2\}$ is a liar with probability at most $1/2$, and $k$ rounds return PROBABLY PRIME with probability at most $2^{-k}$.

*Proof.* The first claim is Lemma 2, with line L1 for $n < 5$ and even $n$. By Lemmas 3 and 4 and [Lagrange's theorem](/lagranges-theorem-group-theory/), $|E(n)|$ is a proper divisor of $\varphi(n)$, so $|E(n)| \le \varphi(n)/2$. The bases 1 and $n - 1$ are always liars, since $\left(\frac{-1}{n}\right) = (-1)^{e}$; line L3 does not draw them. So the probability is $(|E(n)| - 2)/(n - 3) \le (\varphi(n)/2 - 2)/(n - 3) < 1/2$, using $\varphi(n) \le n - 1$. The $k$ bases are independent, and the answer is PROBABLY PRIME only if all of them are liars. $\blacksquare$

**Tightness.** The bound $\varphi(n)/2$ is reached, for example by the Carmichael numbers $1729 = 7 \cdot 13 \cdot 19$ (648 of 1296 units) and $2465 = 5 \cdot 17 \cdot 29$ (896 of 1792). The tests check this, and that no odd composite below 1500 reaches it.

**Relation to Miller-Rabin.** Every strong liar is an Euler liar, and the two sets are equal when $n \equiv 3 \pmod 4$; the proof is Lemma 4 on the [Miller-Rabin page](/miller-rabin-primality-test/). So the strong test is never weaker, and its bound is $\varphi(n)/4$ instead of $\varphi(n)/2$.
