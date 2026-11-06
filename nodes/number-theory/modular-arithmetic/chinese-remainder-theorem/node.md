---
tag: M4X9A6
kind: theorem
slug: chinese-remainder-theorem
name: Chinese remainder theorem
aliases:
- Sunzi's theorem
- CRT
area: number-theory/modular-arithmetic
level: core
summary: Pairwise coprime moduli give a unique solution mod their product to a system of congruences.
prereqs: [congruence, coprime-integers, bezouts-identity]
see_also: [chinese-remainder-problem, garner-algorithm, residue-number-system, euler-totient, multiplicative-group-modulo-n, modular-inverse, rsa-cryptosystem, multimodular-determinant]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.5, The Chinese remainder theorem (the theorem, the construction with the coefficients m_i, and the corollaries for the units modulo n)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.3.2, Modular arithmetic (Theorem C, the Chinese remainder theorem, and its use for multiple-precision arithmetic)
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition
    locator: Section 2.4, Chinese remainder theorem
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 2.4.3, Fact 2.120 (the theorem), Algorithm 2.121 (Gauss's algorithm) and Example 2.122
  - url: https://en.wikipedia.org/wiki/Chinese_remainder_theorem
    title: Chinese remainder theorem, Wikipedia
    locator: section History (Sunzi Suanjing, Aryabhata, Qin Jiushao's Mathematical Treatise in Nine Sections of 1247, Gauss's Disquisitiones Arithmeticae of 1801)
---

The Chinese remainder theorem says that if the moduli $n_1, \ldots, n_k$ are pairwise [coprime](/coprime-integers/), then for any remainders $a_1, \ldots, a_k$ the system of [congruences](/congruence/) $x \equiv a_i \pmod{n_i}$ has exactly one solution modulo $N = n_1 n_2 \cdots n_k$. In algebraic terms, the ring $\mathbb{Z}/N\mathbb{Z}$ is isomorphic to the product of the rings $\mathbb{Z}/n_i\mathbb{Z}$. This lets a computation modulo a large $N$ be split into independent computations modulo small factors, which is the base of the [residue number system](/residue-number-system/), of fast RSA decryption, and of [multimodular methods](/modular-methods/). It also proves that [Euler's totient](/euler-totient/) is multiplicative. Solving the system is the [Chinese remainder problem](/chinese-remainder-problem/); [Garner's algorithm](/garner-algorithm/) is one efficient method.

## Statement

**Theorem (Chinese remainder theorem).** Let $n_1, \ldots, n_k \ge 1$ be pairwise coprime, that is, $\gcd(n_i, n_j) = 1$ for $i \ne j$, and let $N = n_1 \cdots n_k$. Then for all integers $a_1, \ldots, a_k$ there is an integer $x$ with

$$x \equiv a_i \pmod{n_i} \quad \text{for } i = 1, \ldots, k,$$

and any two such integers are congruent modulo $N$.

**Ring form.** Under the same hypothesis, the map

$$\psi : \mathbb{Z}/N\mathbb{Z} \to \mathbb{Z}/n_1\mathbb{Z} \times \cdots \times \mathbb{Z}/n_k\mathbb{Z}, \qquad x \bmod N \mapsto (x \bmod n_1, \ldots, x \bmod n_k)$$

is a bijection that respects addition and multiplication componentwise, so it is a ring isomorphism.

**Explicit solution.** Let $N_i = N / n_i$ and let $M_i$ be the inverse of $N_i$ modulo $n_i$. Then

$$x = \sum_{i=1}^{k} a_i N_i M_i \bmod N$$

is the solution.

**General moduli.** For arbitrary moduli $n_1, \ldots, n_k \ge 1$, the system $x \equiv a_i \pmod{n_i}$ has a solution if and only if $a_i \equiv a_j \pmod{\gcd(n_i, n_j)}$ for all $i, j$. The solution is then unique modulo $\operatorname{lcm}(n_1, \ldots, n_k)$.

## In plain words

Suppose you know the remainders of an unknown number on division by a few divisors that share no common factors. Then you know the number exactly, up to a multiple of the product of the divisors. And every choice of remainders is possible.

For example, the remainders on division by three, five and seven pin down a number between zero and one hundred and four. Each of the one hundred and five numbers in this range gives a different list of three remainders.

So you can store a big number as a short list of small remainders. You add and multiply the lists entry by entry, and convert back at the end.

## Proof

**Uniqueness.** Let $x$ and $y$ both solve the system. Then $n_i \mid x - y$ for each $i$. So $x - y$ is a common multiple of the $n_i$, and thus a multiple of their [least common multiple](/least-common-multiple/). For pairwise coprime moduli, $\operatorname{lcm}(n_1, \ldots, n_k) = N$. This follows by induction from $\operatorname{lcm}(a, b) = ab$ for coprime $a, b$, and from $\gcd(n_1 \cdots n_{j}, n_{j+1}) = 1$: a prime that divides $n_{j+1}$ and the product divides some $n_i$ with $i \le j$ by [Euclid's lemma](/euclids-lemma/), which contradicts $\gcd(n_i, n_{j+1}) = 1$. Hence $N \mid x - y$.

**Existence.** For each $i$, $N_i = \prod_{j \ne i} n_j$ is coprime to $n_i$, by the argument just given. By [Bezout's identity](/bezouts-identity/) there are integers $M_i, t_i$ with $N_i M_i + n_i t_i = 1$, so $N_i M_i \equiv 1 \pmod{n_i}$. For $j \ne i$, $n_j \mid N_i$, so $N_i M_i \equiv 0 \pmod{n_j}$. Let $x = \sum_i a_i N_i M_i$. Modulo $n_j$ every term except the $j$-th vanishes, and the $j$-th is $a_j \cdot 1$. So $x \equiv a_j \pmod{n_j}$ for each $j$.

**Ring form.** The map $\psi$ is well defined, because $x \equiv y \pmod N$ implies $x \equiv y \pmod{n_i}$ for each $i$. It respects $+$ and $\times$, because reduction modulo $n_i$ does. Uniqueness says that $\psi$ is injective, and existence says that it is surjective. (Alternatively, an injective map between two finite sets with $N$ elements each is surjective.)

**General moduli.** If a solution $x$ exists, then for all $i, j$ with $g = \gcd(n_i, n_j)$, $a_i \equiv x \equiv a_j \pmod g$. For the converse, take two congruences $x \equiv a_1 \pmod{n_1}$ and $x \equiv a_2 \pmod{n_2}$ with $g = \gcd(n_1, n_2) \mid a_2 - a_1$. Write $x = a_1 + n_1 t$. The second congruence becomes $n_1 t \equiv a_2 - a_1 \pmod{n_2}$, a [linear congruence](/linear-congruence/) that has a solution $t$ because $g \mid a_2 - a_1$. So the pair has a solution, and by the uniqueness argument it is unique modulo $L = \operatorname{lcm}(n_1, n_2)$. The pair is equivalent to the single congruence $x \equiv x_0 \pmod L$. Replace the pair by it and repeat. The pairwise condition carries over: for each other index $j$, $x_0 \equiv a_1 \pmod{\gcd(n_1, n_j)}$ and $x_0 \equiv a_2 \pmod{\gcd(n_2, n_j)}$, and since $a_1 \equiv a_j$ and $a_2 \equiv a_j$ modulo these gcds, $x_0 - a_j$ is divisible by both gcds and so by their least common multiple, which is $\gcd(L, n_j)$ (compare the exponent of each prime). After $k - 1$ steps one congruence modulo $\operatorname{lcm}(n_1, \ldots, n_k)$ remains. $\blacksquare$

## Consequences

- **The Sunzi problem.** For $x \equiv 2 \pmod 3$, $x \equiv 3 \pmod 5$ and $x \equiv 2 \pmod 7$: $N = 105$, $N_i = 35, 21, 15$, and the inverses are $M_i = 2, 1, 1$, since $35 \cdot 2 = 70 \equiv 1 \pmod 3$, $21 \equiv 1 \pmod 5$ and $15 \equiv 1 \pmod 7$. So $x = 2 \cdot 70 + 3 \cdot 21 + 2 \cdot 15 = 233 \equiv 23 \pmod{105}$.
- **Totient is multiplicative.** Under $\psi$, $x$ is a unit modulo $N$ if and only if each component is a unit modulo $n_i$. So the units correspond, $(\mathbb{Z}/N\mathbb{Z})^* \cong \prod_i (\mathbb{Z}/n_i\mathbb{Z})^*$ as groups, and $\varphi(N) = \prod_i \varphi(n_i)$. This gives the product formula for [Euler's totient](/euler-totient/) and the structure of the [multiplicative group modulo n](/multiplicative-group-modulo-n/).
- **Counting roots.** The number of solutions of a polynomial congruence $f(x) \equiv 0 \pmod N$ is the product of the numbers of solutions modulo each $n_i$. For example $x^2 \equiv 1$ has two solutions modulo each odd prime, so it has $2^3 = 8$ solutions modulo $105 = 3 \cdot 5 \cdot 7$: $1, 29, 34, 41, 64, 71, 76, 104$. Modulo $15$ it has the four solutions $1, 4, 11, 14$. Square roots of $1$ other than $\pm 1$ reveal a factor, $\gcd(4 - 1, 15) = 3$, which is the idea behind the [Miller-Rabin test](/miller-rabin/).
- **Faster RSA decryption.** With $n = pq$, decrypt modulo $p$ and $q$ with the exponents $d \bmod (p-1)$ and $d \bmod (q-1)$, and combine by CRT. Each half uses numbers of half the length, so it costs about an eighth of the full exponentiation with schoolbook multiplication, and the two halves together cost about a quarter. For $n = 3233 = 61 \cdot 53$, $d = 2753$ and $c = 2790$: $d \bmod 60 = 53$, $d \bmod 52 = 49$, $2790^{53} \equiv 4 \pmod{61}$, $2790^{49} \equiv 12 \pmod{53}$, and the unique $x$ modulo $3233$ with these remainders is $65$, the message. See [RSA](/rsa-cryptosystem/).
- **Residue arithmetic.** In a [residue number system](/residue-number-system/), integers below $N$ are stored by their residues, and addition, subtraction and multiplication act on each residue independently, with no carries. [Multimodular algorithms](/modular-methods/) such as the [multimodular determinant](/multimodular-determinant/) compute a result modulo many small primes and reconstruct it.
- **Polynomials.** The same proof works in any ring with a Euclidean algorithm. For polynomials over a field it gives [Lagrange interpolation](/lagrange-interpolation/): a polynomial modulo $\prod (x - x_i)$ is fixed by its values $f(x_i)$ at distinct points.

## Tightness

**Existence fails without coprimality.** The system $x \equiv 0 \pmod 2$ and $x \equiv 1 \pmod 4$ has no solution, since $x \equiv 1 \pmod 4$ forces $x$ odd. Here $\gcd(2, 4) = 2$ and $0 \not\equiv 1 \pmod 2$. Likewise $x \equiv 1 \pmod 4$ and $x \equiv 2 \pmod 6$ has no solution, since $1 \not\equiv 2 \pmod 2$.

**Uniqueness is only modulo the lcm.** The system $x \equiv 1 \pmod 4$ and $x \equiv 3 \pmod 6$ satisfies the condition, since $1 \equiv 3 \pmod 2$, and its solutions are $x \equiv 9 \pmod{12}$, not a single class modulo $24$. The system $x \equiv 0 \pmod 4$ and $x \equiv 0 \pmod 6$ has the two solutions $0$ and $12$ modulo $24$.

**The ring form fails without coprimality.** $\mathbb{Z}/4\mathbb{Z}$ is not isomorphic to $\mathbb{Z}/2\mathbb{Z} \times \mathbb{Z}/2\mathbb{Z}$, even though both have four elements: in $\mathbb{Z}/4\mathbb{Z}$ the element $1$ needs four additions to reach $0$, while every element of the product reaches $0$ after two. Under $\psi$, the residues $1$ and $3$ modulo $4$ both map to $(1, 1)$.

## History

The oldest known instance is a problem in the *Sunzi Suanjing*, a Chinese text dated between the third and fifth centuries: find a number that leaves remainder $2$ on division by $3$, remainder $3$ on division by $5$, and remainder $2$ on division by $7$. The answer given is $23$. An algorithm for such problems was described by Aryabhata in India in the sixth century. Qin Jiushao gave a complete method, the *dayan* rule, in his *Mathematical Treatise in Nine Sections* of 1247, and Gauss stated and proved the theorem in modern form in the *Disquisitiones Arithmeticae* of 1801 (Wikipedia, section History). Knuth (Section 4.3.2) uses the theorem as the base of modular multiple-precision arithmetic, and CLRS (Section 31.5) gives the construction with the coefficients $N_i M_i$.

## References
