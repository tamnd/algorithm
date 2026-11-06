---
tag: 3S79TJ
kind: theorem
slug: lagranges-theorem-group-theory
name: Lagrange's theorem for groups
aliases:
- Lagrange's theorem
area: number-theory/modular-arithmetic
level: core
summary: The order of any subgroup of a finite group divides the order of the group, which bounds element orders and subgroup sizes.
prereqs: [finite-group, subgroup, equivalence-relation]
see_also: [cyclic-group, euler-theorem, fermat-little-theorem, multiplicative-order, multiplicative-group-modulo-n, miller-rabin, solovay-strassen, order-finding]
sources:
  - book: isbn:9780471433347
    title: David S. Dummit and Richard M. Foote, Abstract Algebra, third edition
    locator: Section 3.2, More on cosets and Lagrange's theorem (the theorem, its corollaries on element orders and groups of prime order, and A_4 as a counterexample to the converse)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.3, Modular arithmetic (subgroups, Lagrange's theorem and the corollary that a proper subgroup has at most half the elements), and Section 31.8, Primality testing (the use of this corollary to bound the error of the tests)
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition
    locator: Section 6.3, Cosets and quotient groups
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 2.5.1, Fact 2.171 (Lagrange's theorem and the corollary that the order of an element divides the group order)
  - url: https://en.wikipedia.org/wiki/Lagrange%27s_theorem_(group_theory)
    title: Lagrange's theorem (group theory), Wikipedia
    locator: sections Existence of subgroups of given order (with the counterexample A_4 to the converse) and History
---

Lagrange's theorem says that in a [finite group](/finite-group/) $G$, the number of elements of each [subgroup](/subgroup/) $H$ divides the number of elements of $G$. The proof splits $G$ into cosets of $H$, which all have the same size. Its main corollary is that the order of every element divides $|G|$, so $g^{|G|} = 1$. Applied to the [multiplicative group modulo n](/multiplicative-group-modulo-n/), this gives [Euler's theorem](/euler-theorem/) and [Fermat's little theorem](/fermat-little-theorem/). In algorithms it bounds the error of the [Miller-Rabin](/miller-rabin/) and [Solovay-Strassen](/solovay-strassen/) primality tests, because a proper subgroup holds at most half of the group, and it restricts the search for the [multiplicative order](/multiplicative-order/) of an element to the divisors of the group order.

## Statement

**Theorem (Lagrange).** Let $G$ be a finite group and $H$ a subgroup of $G$. Then $|H|$ divides $|G|$. More precisely, the left cosets $gH = \{gh : h \in H\}$ partition $G$, each has $|H|$ elements, and if $[G : H]$ denotes their number (the **index** of $H$ in $G$), then

$$|G| = [G : H] \cdot |H|.$$

**Corollary 1 (orders of elements).** For each $g \in G$, the order of $g$ divides $|G|$, and $g^{|G|} = 1$.

**Corollary 2 (prime order).** A group of prime order $p$ is [cyclic](/cyclic-group/), and every element other than the identity generates it.

**Corollary 3 (proper subgroups).** If $H$ is a proper subgroup of $G$, then $|H| \le |G|/2$.

## In plain words

Take a finite group and a smaller group inside it. Shift the smaller group by each element of the big one. Each shifted copy has the same size as the smaller group, and two shifted copies are either the same or share nothing.

So the copies split the big group into equal blocks, and the size of the big group is the number of blocks times the block size. Hence the size of the smaller group divides the size of the big one.

For any element, its powers form such a smaller group. So the number of steps it takes to come back to the identity divides the size of the group. A smaller group that misses at least one element has at most half of all the elements.

## Proof

Write the group multiplicatively with identity $1$.

1. **Each coset has $|H|$ elements.** For fixed $g$, the map $h \mapsto gh$ from $H$ to $gH$ is surjective by definition, and injective because $gh = gh'$ implies $h = h'$ after multiplication by $g^{-1}$ on the left.
2. **Cosets are equal or disjoint.** Define $a \sim b$ if $a^{-1} b \in H$. This is an [equivalence relation](/equivalence-relation/): $a^{-1} a = 1 \in H$; if $a^{-1} b \in H$ then its inverse $b^{-1} a \in H$; and if $a^{-1} b, b^{-1} c \in H$ then their product $a^{-1} c \in H$. The class of $a$ is $\{b : a^{-1} b \in H\} = \{ah : h \in H\} = aH$. Equivalence classes are equal or disjoint.
3. **Cosets cover $G$.** Each $g$ lies in its own coset $gH$, since $g = g \cdot 1$.
4. So $G$ is the disjoint union of $[G : H]$ cosets, each with $|H|$ elements, and $|G| = [G : H] \cdot |H|$. $\square$

**Corollary 1.** Let $g$ have order $t$. The powers $1, g, \ldots, g^{t-1}$ are distinct and form the subgroup $\langle g \rangle$ with $t$ elements. By the theorem, $t \mid |G|$, so $g^{|G|} = (g^t)^{|G|/t} = 1$.

**Corollary 2.** Let $|G| = p$ prime and $g \ne 1$. The order of $g$ divides $p$ and is not $1$, so it is $p$, and $\langle g \rangle = G$.

**Corollary 3.** If $H \ne G$, then $[G : H] \ge 2$, so $|H| = |G| / [G : H] \le |G|/2$. $\blacksquare$

## Consequences

- **[Euler's theorem](/euler-theorem/).** The units modulo $n$ form a group of order $\varphi(n)$, so $a^{\varphi(n)} \equiv 1 \pmod n$ for $\gcd(a, n) = 1$. For a prime $p$ this is [Fermat's little theorem](/fermat-little-theorem/), $a^{p-1} \equiv 1 \pmod p$.
- **Error bounds of primality tests.** For an odd composite $n$, the bases $a$ with $a^{n-1} \equiv 1 \pmod n$ form a subgroup of $\mathbb{Z}_n^*$. If one coprime base fails the test, the subgroup is proper, so at most half of the coprime bases pass. Modulo $91 = 7 \cdot 13$, exactly $36$ of the $72$ units pass, and modulo $341$, $100$ of $300$ pass. The same argument, with a subgroup that is always proper, bounds the error of [Solovay-Strassen](/solovay-strassen/) by $1/2$ per round, and it is the first step in the analysis of [Miller-Rabin](/miller-rabin/) (CLRS, Section 31.8).
- **Order computation.** The [multiplicative order](/multiplicative-order/) of $a$ modulo $n$ divides $\varphi(n)$. If the factorization of $\varphi(n)$ is known, the order is found by starting from $\varphi(n)$ and removing each prime factor while the power stays $1$. In [order finding](/order-finding/) and in [Pohlig-Hellman](/pohlig-hellman/), the divisibility splits the problem along the prime factors of the group order.
- **Generators.** In a cyclic group of order $n$, an element $h$ generates the group if and only if $h^{n/p} \ne 1$ for each prime $p \mid n$, because its order divides $n$ and is a proper divisor only if it divides some $n/p$. This is the standard test for a [primitive root](/primitive-root/).
- **Counting.** If $H$ and $K$ are subgroups with coprime orders, then $H \cap K = \{1\}$, because $|H \cap K|$ divides both $|H|$ and $|K|$.

## Tightness

**The converse is false.** A divisor of $|G|$ need not be the order of a subgroup. The smallest counterexample is the alternating group $A_4$, the even permutations of four symbols: it has $12$ elements and subgroups of orders $1, 2, 3, 4$ and $12$, but none of order $6$. This can be checked by a search over all $6$-element subsets of $A_4$.

**Where the converse holds.** For [cyclic groups](/cyclic-group/) the converse holds in a strong form: there is exactly one subgroup of each order $d \mid n$. For every finite group, Cauchy's theorem gives an element of each prime order $p$ dividing $|G|$, and the Sylow theorems give a subgroup of order $p^k$ for the largest power $p^k$ that divides $|G|$ (Wikipedia, section Existence of subgroups of given order).

**The bound of Corollary 3 is attained.** A subgroup of index $2$ has exactly half of the elements. For example, the squares in $\mathbb{Z}_p^*$ for an odd prime $p$ form a subgroup of index $2$, the [quadratic residues](/quadratic-residue/).

**Element orders need not reach $|G|$.** The theorem gives only divisibility. In $\mathbb{Z}_8^*$, of order $4$, every element has order at most $2$; the least common exponent is the [Carmichael function](/carmichael-function/) $\lambda(n)$, not $\varphi(n)$.

## History

Lagrange did not prove the theorem in its general form. In 1771, in his *Réflexions sur la résolution algébrique des équations*, he showed that the number of distinct polynomials obtained by permuting the $n$ variables of a polynomial in all $n!$ ways divides $n!$, which is a special case for subgroups of the symmetric group. Gauss proved the case of the multiplicative group modulo a prime in the *Disquisitiones Arithmeticae* of 1801, Cauchy proved the theorem for the [symmetric group](/symmetric-group/) $S_n$ in 1844, and Camille Jordan proved it for every permutation group in 1861 (Wikipedia, section History). The coset proof given here is the standard one in textbooks, for example Dummit and Foote (Section 3.2).

## References
