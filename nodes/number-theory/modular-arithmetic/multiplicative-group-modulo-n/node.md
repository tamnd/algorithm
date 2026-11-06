---
tag: 2M0K3Y
kind: concept
slug: multiplicative-group-modulo-n
name: Multiplicative group modulo n
aliases:
- unit group of Z_n
- (Z/nZ)^*
area: number-theory/modular-arithmetic
level: core
summary: The residues modulo n that are coprime to n, which form a finite abelian group of order φ(n) under multiplication mod n.
prereqs: [congruence, coprime-integers, modular-inverse]
see_also: [euler-totient, carmichael-function, multiplicative-order, primitive-root, lagranges-theorem-group-theory, chinese-remainder-theorem, additive-group-modulo-n, unit-group]
sources:
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1997
    locator: Section 2.4.3, The integers modulo n (Definitions 2.124 and 2.125, Fact 2.126 Euler's theorem, Fact 2.129, Definition 2.131 generator, Fact 2.132 on when Z_n^* is cyclic)
  - book: isbn:9780387973296
    title: Kenneth Ireland and Michael Rosen, A Classical Introduction to Modern Number Theory, second edition, Springer GTM 84
    locator: Chapter 4, The Structure of U(Z/nZ), Section 4.1, Primitive Roots and the Group Structure of U(Z/nZ)
  - book: isbn:9780471625469
    title: Ivan Niven, Herbert S. Zuckerman and Hugh L. Montgomery, An Introduction to the Theory of Numbers, fifth edition
    locator: Section 2.8, Primitive roots and power residues
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.3, Modular arithmetic (finite groups, the groups Z_n^*, subgroups and Lagrange's theorem)
---

The multiplicative group modulo $n$, written $\mathbb{Z}_n^*$ or $(\mathbb{Z}/n\mathbb{Z})^\times$, is the set of residues $a \in \{0, \ldots, n - 1\}$ with $\gcd(a, n) = 1$, with multiplication modulo $n$ as the operation. It is a finite abelian group whose size is [Euler's totient](/euler-totient/) $\varphi(n)$, and its elements are exactly the residues that have a [modular inverse](/modular-inverse/). Its structure explains [Euler's theorem](/euler-theorem/), the [multiplicative order](/multiplicative-order/) of an element, and why [primitive roots](/primitive-root/) exist only for some $n$. Most of public-key cryptography and probabilistic primality testing happens inside this group.

## In plain words

Take a clock of a given size and keep only the positions that share no factor with the size. Multiply two of these positions and land on the clock: you get another kept position. Each kept position also has a partner that brings it back to the position 1 when you multiply them. So the kept positions form a closed system, a group. Many facts about remainders follow from this. If you multiply any kept position by itself over and over, you return to 1 after a number of steps that divides the number of kept positions. For some clock sizes, one position produces all others by repeated multiplication; for other sizes, no such position exists.

## The idea

**The set and the operation.** For $n \ge 2$, let $\mathbb{Z}_n^* = \{ a : 0 \le a < n,\ \gcd(a, n) = 1 \}$, and let $a \cdot b = ab \bmod n$. For $n = 1$ the ring $\mathbb{Z}_1$ has one element, $0 = 1$, and $\mathbb{Z}_1^* = \{0\}$ is the trivial group.

**It is a group.**

- *Closure.* If $\gcd(a, n) = \gcd(b, n) = 1$, then $\gcd(ab, n) = 1$, since a prime that divides $n$ and $ab$ divides $a$ or $b$ by [Euclid's lemma](/euclids-lemma/). Reduction modulo $n$ does not change the gcd with $n$.
- *Identity and associativity.* The residue 1 is the identity, and associativity comes from that of integer multiplication.
- *Inverses.* By [Bézout's identity](/bezouts-identity/) there are $x, y$ with $ax + ny = 1$, so $ax \equiv 1 \pmod n$, and $x \bmod n$ is coprime to $n$. Conversely, if $ax \equiv 1$ then $\gcd(a, n)$ divides $1$. So $\mathbb{Z}_n^*$ is exactly the set of invertible residues, the [unit group](/unit-group/) of the ring $\mathbb{Z}_n$.
- *Commutativity.* $ab = ba$.

**Its order.** $|\mathbb{Z}_n^*| = \varphi(n) = n \prod_{p \mid n} (1 - 1/p)$. For a prime $p$, $\mathbb{Z}_p^* = \{1, \ldots, p - 1\}$ has $p - 1$ elements, and every nonzero residue is invertible, so $\mathbb{Z}_p$ is a field.

**Lagrange's theorem and its consequences.** By [Lagrange's theorem](/lagranges-theorem-group-theory/), the order of every element divides $\varphi(n)$. This gives [Euler's theorem](/euler-theorem/) $a^{\varphi(n)} \equiv 1 \pmod n$ for $\gcd(a, n) = 1$, and [Fermat's little theorem](/fermat-little-theorem/) for prime $n$. It also gives a counting tool: a proper subgroup has at most half of the elements. The analysis of the Fermat and Solovay-Strassen primality tests uses it: the "liars" form a subgroup, so if one witness exists, at least half of all elements are witnesses.

**Structure.** By the [Chinese remainder theorem](/chinese-remainder-theorem/), if $n = p_1^{e_1} \cdots p_r^{e_r}$, then

$$\mathbb{Z}_n^* \cong \mathbb{Z}_{p_1^{e_1}}^* \times \cdots \times \mathbb{Z}_{p_r^{e_r}}^*.$$

Each factor is known (Ireland and Rosen, Chapter 4):

- for an odd prime $p$ and $e \ge 1$, $\mathbb{Z}_{p^e}^*$ is cyclic of order $p^{e-1}(p - 1)$;
- $\mathbb{Z}_2^*$ is trivial and $\mathbb{Z}_4^*$ is cyclic of order 2;
- for $e \ge 3$, $\mathbb{Z}_{2^e}^* \cong C_2 \times C_{2^{e-2}}$, generated by $-1$ and $5$, and it is not cyclic.

So $\mathbb{Z}_n^*$ is cyclic exactly for $n = 1, 2, 4, p^e, 2p^e$ with $p$ an odd prime; this is the theorem on [the existence of primitive roots](/primitive-roots-existence/). A generator of a cyclic $\mathbb{Z}_n^*$ is a [primitive root](/primitive-root/). The largest order of an element, the exponent of the group, is the [Carmichael function](/carmichael-function/) $\lambda(n)$, which divides $\varphi(n)$ and equals it exactly when the group is cyclic.

**Squares.** The map $x \mapsto x^2$ is a group homomorphism. Its image is the subgroup of [quadratic residues](/quadratic-residue/). For an odd prime $p$ its kernel is $\{\pm 1\}$, so exactly half of $\mathbb{Z}_p^*$ are squares.

**Computing in it.** A residue is stored as an integer in $[0, n)$. The product is a [modular multiplication](/modular-multiplication/), the inverse takes one extended Euclidean algorithm, $O(\log n)$ word operations, and membership is one gcd. Powers use [modular exponentiation](/modular-exponentiation/). Computing $\varphi(n)$ or the structure of the group needs the factorization of $n$, and no fast method is known without it.

## Examples

**A prime modulus.** $\mathbb{Z}_7^* = \{1, 2, 3, 4, 5, 6\}$. The powers of 3 are $3, 2, 6, 4, 5, 1$, so 3 generates the group and it is cyclic of order 6. The orders of $1, \ldots, 6$ are $1, 3, 6, 3, 6, 2$, all divisors of 6.

**A prime power.** $\mathbb{Z}_9^* = \{1, 2, 4, 5, 7, 8\}$, of order $\varphi(9) = 6$. The powers of 2 are $2, 4, 8, 7, 5, 1$, so it is cyclic.

**A non-cyclic group.** $\mathbb{Z}_{12}^* = \{1, 5, 7, 11\}$. Every element squares to 1: $5^2 = 25 \equiv 1$, $7^2 = 49 \equiv 1$, $11^2 = 121 \equiv 1$. So no element has order 4, and the group is $C_2 \times C_2$, the Klein four-group. The same holds for $\mathbb{Z}_8^* = \{1, 3, 5, 7\}$.

**A product.** $\mathbb{Z}_{15}^* = \{1, 2, 4, 7, 8, 11, 13, 14\}$ has order $\varphi(15) = 8$. The orders are $1, 4, 2, 4, 4, 2, 4, 2$. The largest order is $4 = \lambda(15)$, so the group is not cyclic; by the Chinese remainder theorem it is $\mathbb{Z}_3^* \times \mathbb{Z}_5^* \cong C_2 \times C_4$. The inverse of 7 is 13, since $7 \cdot 13 = 91 = 6 \cdot 15 + 1$.

**A power of two.** $\mathbb{Z}_{16}^* = \{1, 3, 5, \ldots, 15\}$ has 8 elements, and the largest order is 4, reached by $3, 5, 11, 13$. It is $\{\pm 1\} \times \langle 5 \rangle \cong C_2 \times C_4$.

**Small moduli.** $\mathbb{Z}_2^* = \{1\}$, and $\mathbb{Z}_1^* = \{0\}$, where $0 = 1$.

## Where it is used

- **RSA.** The [RSA cryptosystem](/rsa-cryptosystem/) works in $\mathbb{Z}_N^*$ for $N = pq$. Decryption works because $ed \equiv 1 \pmod{\varphi(N)}$, or modulo $\lambda(N)$, and the security rests on the difficulty of finding the group order without the factors.
- **Discrete logarithm cryptography.** [Diffie-Hellman](/diffie-hellman/) and [ElGamal](/elgamal-encryption/) work in a cyclic subgroup of $\mathbb{Z}_p^*$. The [Pohlig-Hellman](/pohlig-hellman/) algorithm uses the factorization of the group order, which is why $p - 1$ must have a large prime factor.
- **Primality testing.** The [Fermat test](/fermat-primality-test/), [Solovay-Strassen](/solovay-strassen/) and [Miller-Rabin](/miller-rabin/) check identities that hold in $\mathbb{Z}_p^*$ for prime $p$, and count how often they fail in $\mathbb{Z}_n^*$ for composite $n$.
- **Order finding.** [Shor's algorithm](/shor-algorithm/) factors $n$ by finding the order of a random element of $\mathbb{Z}_n^*$.
- **Number-theoretic transform.** The [NTT](/number-theoretic-transform/) needs roots of unity of order $2^k$, which exist in $\mathbb{Z}_p^*$ when $2^k \mid p - 1$, because the group is cyclic.
- **Pseudorandom generators.** A multiplicative [linear congruential generator](/linear-congruential-generator/) $x \mapsto ax \bmod m$ has period equal to the order of $a$ in $\mathbb{Z}_m^*$.

## References
