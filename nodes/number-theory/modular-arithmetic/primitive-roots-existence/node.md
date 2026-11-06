---
tag: 31P105
kind: theorem
slug: primitive-roots-existence
name: Existence of primitive roots
aliases:
- Gauss's theorem on primitive roots
area: number-theory/modular-arithmetic
level: advanced
summary: Primitive roots mod n exist exactly when n is 1, 2, 4, p^k, or 2p^k for odd prime p.
prereqs: [primitive-root, multiplicative-order]
see_also: [multiplicative-group-modulo-n, cyclic-group, euler-totient, carmichael-function, lagranges-theorem-group-theory, hensel-lifting, discrete-logarithm-problem, euler-criterion]
sources:
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1997
    locator: Section 2.4.3, Definition 2.131 and Fact 2.132 (Z_n^* is cyclic exactly when n is 2, 4, p^k or 2p^k), and Algorithm 4.80
  - book: isbn:9780387973296
    title: Kenneth Ireland and Michael Rosen, A Classical Introduction to Modern Number Theory, second edition, Springer GTM 84
    locator: Chapter 4, Section 4.1 (the group of units modulo a prime is cyclic; the structure of the units modulo 2^k and p^k; the classification of n with primitive roots)
  - book: isbn:9780471625469
    title: Ivan Niven, Herbert S. Zuckerman and Hugh L. Montgomery, An Introduction to the Theory of Numbers, fifth edition
    locator: Section 2.8, Primitive roots and power residues
  - book: isbn:9780387962542
    title: Carl Friedrich Gauss, Disquisitiones Arithmeticae, English translation by Arthur A. Clarke, Springer, 1986
    locator: Section III, Residues of powers (the existence of primitive roots for a prime, and their extension to prime powers and twice prime powers)
---

A [primitive root](/primitive-root/) modulo $n$ is an integer $g$ whose [multiplicative order](/multiplicative-order/) modulo $n$ is $\varphi(n)$, so that its powers run through all residues coprime to $n$. Such a $g$ exists exactly when $n$ is $1$, $2$, $4$, $p^k$ or $2p^k$ for an odd prime $p$ and $k \ge 1$. In group terms, the [multiplicative group](/multiplicative-group-modulo-n/) $\mathbb{Z}_n^*$ is cyclic exactly for these $n$. The case of a prime rests on the fact that a polynomial of degree $d$ has at most $d$ roots modulo $p$. The prime powers follow by lifting from $p$ to $p^2$ and then to every $p^k$. For every other $n$, every element has order at most $\varphi(n)/2$. Gauss gave the first complete proof in 1801.

## Statement

**Theorem.** Let $n \ge 1$. There is an integer $g$ with $\gcd(g, n) = 1$ and $\operatorname{ord}_n(g) = \varphi(n)$ if and only if

$$n \in \{1, 2, 4\} \quad \text{or} \quad n = p^k \quad \text{or} \quad n = 2p^k, \qquad p \text{ an odd prime}, \ k \ge 1.$$

In that case $\mathbb{Z}_n^*$ is cyclic and there are exactly $\varphi(\varphi(n))$ primitive roots modulo $n$ in $\{1, \ldots, n\}$. For all other $n$, $x^{\varphi(n)/2} \equiv 1 \pmod n$ for every $x$ coprime to $n$.

**Examples.** Modulo 7 the orders of $1, \ldots, 6$ are $1, 3, 6, 3, 6, 2$, so 3 and 5 are the primitive roots, $\varphi(\varphi(7)) = \varphi(6) = 2$ of them.

Modulo $29^2 = 841$: 14 is a primitive root modulo 29, but $14^{28} \equiv 1 \pmod{841}$, so it has order 28 modulo 841 and is not a primitive root there. Then $14 + 29 = 43$ has order $812 = \varphi(841)$, as the proof below predicts. Among the 12 primitive roots modulo 29 in $\{1, \ldots, 28\}$, 14 is the only one that fails to lift.

Modulo $125$: 2 has order 4 modulo 5 and order 20 modulo 25, so it is a primitive root modulo 25, and then also modulo 125, where its order is $100 = \varphi(125)$. Modulo $250 = 2 \cdot 125$, the odd number $2 + 125 = 127$ has order 100 and is a primitive root. Modulo $18 = 2 \cdot 3^2$, the primitive roots are 5 and 11, of order 6.

Moduli without primitive roots: modulo 8, every odd $x$ has $x^2 \equiv 1$, so the largest order is $2 < 4 = \varphi(8)$. Modulo 15 the largest order is $4 < 8$, modulo 12 it is $2 < 4$, and modulo 21 it is $6 < 12$.

The moduli up to 50 with a primitive root are 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 14, 17, 18, 19, 22, 23, 25, 26, 27, 29, 31, 34, 37, 38, 41, 43, 46, 47, 49 and 50.

## In plain words

Pick a modulus and look at the numbers that share no factor with it. Sometimes a single number, raised to successive powers, visits all of them before coming back to one. That number is a primitive root. The theorem lists exactly when such a number exists: when the modulus is a prime, a power of an odd prime, twice such a power, or one of the small numbers one, two and four. For any other modulus, every number comes back to one by halfway through the count, so no single number can visit all the others.

## Proof

We write $\operatorname{ord}_n(a)$ for the order of $a$ modulo $n$, and use two standard facts. If $a^t \equiv 1 \pmod n$, then $\operatorname{ord}_n(a) \mid t$. The order of $a^j$ is $\operatorname{ord}_n(a) / \gcd(j, \operatorname{ord}_n(a))$.

**Step 1: Lagrange's bound.** A nonzero polynomial $f$ of degree $d$ with coefficients in $\mathbb{Z}_p$ has at most $d$ roots in $\mathbb{Z}_p$. Induct on $d$; $d = 0$ is clear. If $f(r) = 0$, divide to get $f(x) = (x - r) h(x)$ with $\deg h = d - 1$. If $f(s) = 0$ and $s \ne r$, then $(s - r) h(s) = 0$, and since $p$ is prime and $s - r \not\equiv 0$, $h(s) = 0$. So the roots of $f$ are $r$ and the at most $d - 1$ roots of $h$.

**Step 2: Gauss's identity.** For $m \ge 1$, $\sum_{d \mid m} \varphi(d) = m$. Group $k \in \{1, \ldots, m\}$ by $\gcd(k, m)$. The $k$ with $\gcd(k, m) = m/d$ are $k = (m/d) j$ with $1 \le j \le d$ and $\gcd(j, d) = 1$, and there are $\varphi(d)$ of them. Summing over the divisors $d$ of $m$ counts each $k$ once.

**Step 3: odd and even primes.** Let $p$ be prime. For $d \mid p - 1$, let $\psi(d)$ be the number of elements of order $d$ in $\mathbb{Z}_p^*$. Every element has an order dividing $p - 1$ by Fermat's little theorem, so $\sum_{d \mid p-1} \psi(d) = p - 1$. Suppose $\psi(d) \ge 1$ and let $a$ have order $d$. Then $1, a, \ldots, a^{d-1}$ are $d$ distinct roots of $x^d - 1$, and by Step 1 there are no others. Every element of order $d$ is a root of $x^d - 1$, so it is some $a^j$, and $a^j$ has order $d$ exactly when $\gcd(j, d) = 1$. So $\psi(d) = \varphi(d)$. In all cases $\psi(d) \le \varphi(d)$, and

$$p - 1 = \sum_{d \mid p-1} \psi(d) \le \sum_{d \mid p-1} \varphi(d) = p - 1$$

by Step 2. So equality holds for every $d$, and in particular $\psi(p - 1) = \varphi(p - 1) \ge 1$: a primitive root modulo $p$ exists.

**Step 4: from $p$ to $p^2$, for odd $p$.** Let $g$ be a primitive root modulo $p$, and let $e = \operatorname{ord}_{p^2}(g)$. Since $g^e \equiv 1 \pmod{p^2}$ implies $g^e \equiv 1 \pmod p$, $p - 1 \mid e$, and $e \mid \varphi(p^2) = p(p - 1)$. So $e = p - 1$ or $e = p(p - 1)$. In the second case $g$ is a primitive root modulo $p^2$. In the first, $g^{p-1} \equiv 1 \pmod{p^2}$. Then $g + p$ is also a primitive root modulo $p$, and by the binomial theorem

$$(g + p)^{p-1} \equiv g^{p-1} + (p - 1) g^{p-2} p \equiv 1 - p\, g^{p-2} \pmod{p^2},$$

which is not $1 \pmod{p^2}$ because $p \nmid g$. So $g + p$ has order $p(p - 1)$ modulo $p^2$. Either way a primitive root modulo $p^2$ exists, and every primitive root $g$ modulo $p^2$ satisfies $g^{p-1} = 1 + p u$ with $p \nmid u$.

**Step 5: from $p^2$ to $p^k$, for odd $p$.** Claim: if $j \ge 1$ and $x = 1 + p^j u$ with $p \nmid u$, then $x^p = 1 + p^{j+1} u'$ with $p \nmid u'$. Expand:

$$x^p = 1 + p \cdot p^j u + \binom{p}{2} p^{2j} u^2 + \sum_{i=3}^{p} \binom{p}{i} p^{ij} u^i.$$

Since $p$ is odd, $p \mid \binom{p}{2}$, so the third term is divisible by $p^{2j+1}$, and $2j + 1 \ge j + 2$. Each term with $i \ge 3$ is divisible by $p^{3j}$, and $3j \ge j + 2$. So $x^p \equiv 1 + p^{j+1} u \pmod{p^{j+2}}$, which proves the claim with $u' \equiv u \pmod p$.

Now let $g$ be a primitive root modulo $p^2$, so $g^{p-1} = 1 + p u$ with $p \nmid u$ by Step 4. Applying the claim $k - 2$ times gives $g^{p^{k-2}(p-1)} = 1 + p^{k-1} u_k$ with $p \nmid u_k$, so

$$g^{p^{k-2}(p-1)} \not\equiv 1 \pmod{p^k}.$$

Let $e = \operatorname{ord}_{p^k}(g)$. As in Step 4, $p - 1 \mid e$ and $e \mid p^{k-1}(p - 1)$, so $e = p^s (p - 1)$ for some $s \le k - 1$. If $s \le k - 2$, then $e$ divides $p^{k-2}(p - 1)$, contradicting the display. So $e = p^{k-1}(p - 1) = \varphi(p^k)$, and $g$ is a primitive root modulo $p^k$ for every $k \ge 2$.

**Step 6: $2p^k$.** Let $g$ be a primitive root modulo $p^k$. If $g$ is even, replace it by $g + p^k$, which is odd and still a primitive root modulo $p^k$. For odd $g$, $g^t \equiv 1 \pmod 2$ always holds, so by the Chinese remainder theorem $g^t \equiv 1 \pmod{2p^k}$ if and only if $g^t \equiv 1 \pmod{p^k}$. So $\operatorname{ord}_{2p^k}(g) = \varphi(p^k) = \varphi(2p^k)$.

**Step 7: $1$, $2$ and $4$.** $\mathbb{Z}_1^*$ and $\mathbb{Z}_2^*$ have one element, and 3 has order $2 = \varphi(4)$ modulo 4.

**Step 8: no primitive root modulo $2^k$ for $k \ge 3$.** Claim: every odd $x$ satisfies $x^{2^{k-2}} \equiv 1 \pmod{2^k}$. For $k = 3$: $x = 2y + 1$ gives $x^2 = 4y(y + 1) + 1 \equiv 1 \pmod 8$, since $y(y + 1)$ is even. If $x^{2^{k-2}} = 1 + 2^k v$, then $x^{2^{k-1}} = 1 + 2^{k+1} v + 2^{2k} v^2 \equiv 1 \pmod{2^{k+1}}$. So every order divides $2^{k-2} = \varphi(2^k)/2$.

**Step 9: no primitive root modulo $ab$ for coprime $a, b \ge 3$.** For $m \ge 3$, $\varphi(m)$ is even: if an odd prime $q$ divides $m$, then $q - 1 \mid \varphi(m)$; otherwise $m = 2^e$ with $e \ge 2$ and $\varphi(m) = 2^{e-1}$. Let $x$ be coprime to $ab$ and $h = \varphi(a)\varphi(b)/2 = \varphi(ab)/2$. Then $x^h = (x^{\varphi(a)})^{\varphi(b)/2} \equiv 1 \pmod a$ and likewise modulo $b$, so $x^h \equiv 1 \pmod{ab}$, and the order of $x$ is at most $\varphi(ab)/2$.

**Step 10: every other $n$ is covered.** Write $n = 2^e m$ with $m$ odd. If $m = 1$, then $n = 2^e$, and $e \ge 3$ is Step 8. If $m$ has two distinct prime factors $q$, write $m = q^f m'$ with $\gcd(q, m') = 1$, $q^f \ge 3$ and $m' \ge 3$; then $n = q^f \cdot (2^e m')$ is Step 9. If $m = p^k$, the only cases outside the list are $e \ge 2$, and $n = 2^e \cdot p^k$ with $2^e \ge 4$ and $p^k \ge 3$ is Step 9.

**Counting.** If $g$ is a primitive root modulo $n$, then $g^j$ has order $\varphi(n)/\gcd(j, \varphi(n))$, so the primitive roots are the $g^j$ with $\gcd(j, \varphi(n)) = 1$, and there are $\varphi(\varphi(n))$ of them. $\blacksquare$

## Consequences

- **Finite fields.** Steps 1 to 3 use only that $\mathbb{Z}_p$ is a field, so the same proof shows that the multiplicative group of every finite field $\mathbb{F}_q$ is cyclic, and more generally that every finite subgroup of the multiplicative group of a field is cyclic.
- **The structure of $\mathbb{Z}_n^*$.** For $k \ge 2$, $\mathbb{Z}_{2^k}^*$ is the direct product of $\{\pm 1\}$ and the cyclic group of order $2^{k-2}$ generated by 5. With the Chinese remainder theorem, this gives $\mathbb{Z}_n^*$ for every $n$ as a product of cyclic groups. The exponent of $\mathbb{Z}_n^*$ is the [Carmichael function](/carmichael-function/) $\lambda(n)$, and $\lambda(n) = \varphi(n)$ exactly for the $n$ of the theorem.
- **Indices and power residues.** With a primitive root $g$, every $a$ coprime to $n$ has an index $i$ with $g^i \equiv a$, which turns multiplication into addition modulo $\varphi(n)$; finding $i$ is the [discrete logarithm problem](/discrete-logarithm-problem/). Then $x^k \equiv a \pmod n$ is solvable exactly when $a^{\varphi(n)/d} \equiv 1$, with $d = \gcd(k, \varphi(n))$, and has $d$ solutions in that case. For $k = 2$ and $n = p$ this is [Euler's criterion](/euler-criterion/).
- **Square roots of 1.** A cyclic group of even order has exactly one element of order 2. So for $n \ge 3$ in the list, $x^2 \equiv 1 \pmod n$ has only the solutions $\pm 1$; modulo 15, by contrast, 4 and 11 are further solutions.
- **Wilson's theorem.** In $\mathbb{Z}_p^* = \{g^0, \ldots, g^{p-2}\}$ the product of all elements is $g^{(p-1)(p-2)/2} = (g^{(p-1)/2})^{p-2} = (-1)^{p-2} = -1$ for odd $p$, which is [Wilson's theorem](/wilson-theorem/).
- **Cryptography and transforms.** Diffie-Hellman key exchange, ElGamal and DSA work in cyclic subgroups of $\mathbb{Z}_p^*$, and number-theoretic transforms modulo primes such as $998244353 = 119 \cdot 2^{23} + 1$ use a primitive root to obtain roots of unity of every order dividing $p - 1$.

## Tightness

The list of moduli is exact: the theorem is an equivalence, and Steps 8 to 10 show that every other modulus loses at least a factor 2 in the largest order.

The hypothesis that $p$ is odd is needed in Steps 4 and 5. For $p = 2$, 3 is a primitive root modulo 4 but has order 2 modulo 8, and the binomial term $\binom{2}{2} 2^{2j}$ in Step 5 is not divisible by $2^{j+2}$ when $j = 1$. The detour through $g + p$ in Step 4 is also needed: 14 is a primitive root modulo 29 but not modulo $29^2$.

The proof for primes is not constructive. To test whether $g$ is a primitive root one needs the prime factors of $p - 1$, and then one checks $g^{(p-1)/q} \not\equiv 1$ for each of them (HAC, Algorithm 4.80). Random choices succeed with probability $\varphi(p - 1)/(p - 1)$, which is $\Omega(1/\log\log p)$. No deterministic polynomial-time algorithm to find a primitive root is known; under the generalized Riemann hypothesis the least primitive root is $O((\log p)^6)$ (Shoup, 1992), but the factorization of $p - 1$ is still needed to recognize it.

## History

Lambert (1769) and Euler (1773) stated that every prime has a primitive root, and Euler named them, but his proof was incomplete. Gauss gave the first complete proofs in Section III of the Disquisitiones Arithmeticae (1801): one by counting the elements of each order, essentially Step 3 above, and one by building an element of order $q^e$ for each prime power $q^e$ dividing $p - 1$. In the same section he extended the result to the powers of odd primes and to their doubles, and showed that powers of 2 above 4 have no primitive roots. The group-theoretic statement that $\mathbb{Z}_n^*$ is cyclic exactly for these $n$ is the modern form of his result.

## References
