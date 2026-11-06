---
tag: N6B914
kind: concept
slug: multiplicative-order
name: Multiplicative order
aliases:
- order of an element mod n
area: number-theory/modular-arithmetic
level: core
summary: The smallest k > 0 with a^k ≡ 1 (mod n), defined when gcd(a, n) = 1; it divides φ(n) and every exponent m with a^m ≡ 1.
prereqs: [multiplicative-group-modulo-n, modular-exponentiation]
see_also: [primitive-root, euler-theorem, carmichael-function, lagranges-theorem-group-theory, order-finding, pohlig-hellman, cycle-detection, pisano-period]
sources:
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1997
    locator: Section 2.4.3, Definition 2.128 (order), Fact 2.129, Example 2.130 and Table 2.3 (orders of the elements of Z_21^*); Section 4.6, Algorithm 4.79 (determining the order of a group element)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 6, Section 6.8, The order of a (mod m)
  - book: isbn:9780471625469
    title: Ivan Niven, Herbert S. Zuckerman and Hugh L. Montgomery, An Introduction to the Theory of Numbers, fifth edition
    locator: Section 2.8, Primitive roots and power residues
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 3.2.1.2, Choice of multiplier (the order of a modulo m and the period of multiplicative generators)
---

The multiplicative order of an integer $a$ modulo $n$, written $\operatorname{ord}_n(a)$, is the smallest $k \ge 1$ with $a^k \equiv 1 \pmod n$. It exists exactly when $\gcd(a, n) = 1$, and it is the order of $a$ as an element of the [multiplicative group modulo n](/multiplicative-group-modulo-n/). Its main property is that $a^m \equiv 1 \pmod n$ if and only if $\operatorname{ord}_n(a)$ divides $m$, so the order divides $\varphi(n)$ and the [Carmichael function](/carmichael-function/) $\lambda(n)$. Given the factorization of $\varphi(n)$ it can be computed with $O(\log n)$ [modular exponentiations](/modular-exponentiation/); without the factors, computing it is as hard as factoring in general.

## In plain words

Pick a number with no common factor with the clock size and multiply it by itself again and again on the clock. Sooner or later you come back to the position 1, and from there the same positions repeat in the same cycle. The number of steps in this cycle is the order of the number. Each time a power of the number lands on 1, the exponent is a whole number of cycles, so it is a multiple of the order. The order is always a factor of the count of positions that share no factor with the clock size. This tells you where to look when you want to find it.

## The idea

**Existence.** If $\gcd(a, n) = 1$, the powers $a, a^2, \ldots$ lie in the finite set $\mathbb{Z}_n^*$, so two of them are equal, $a^i \equiv a^j$ with $i < j$. Multiplying by the inverse of $a^i$ gives $a^{j - i} \equiv 1$, so a positive exponent with power 1 exists. If $\gcd(a, n) = g > 1$ and $n > 1$, then $g$ divides every $a^k$, so $a^k \equiv 1 \pmod n$ would make $g$ divide 1; no such $k$ exists.

**The divisibility property.** Let $t = \operatorname{ord}_n(a)$. Then $a^m \equiv 1 \pmod n$ if and only if $t \mid m$. Proof: write $m = qt + r$ with $0 \le r < t$. Then $a^m = (a^t)^q a^r \equiv a^r$, and $a^r \equiv 1$ with $r < t$ forces $r = 0$ by the minimality of $t$. More generally, $a^i \equiv a^j$ if and only if $i \equiv j \pmod t$, so the powers of $a$ run through exactly $t$ distinct residues, periodically.

**Consequences.**

- Since $a^{\varphi(n)} \equiv 1$ by [Euler's theorem](/euler-theorem/), $t \mid \varphi(n)$. The same holds for $\lambda(n)$, the largest order modulo $n$, which is a multiple of every order. For a prime $p$, $t \mid p - 1$.
- **Powers.** $\operatorname{ord}_n(a^j) = t / \gcd(t, j)$.
- **Products.** If $\operatorname{ord}_n(a) = s$ and $\operatorname{ord}_n(b) = t$ with $\gcd(s, t) = 1$, then $\operatorname{ord}_n(ab) = st$.
- **Several moduli.** For coprime $m$ and $n$, $\operatorname{ord}_{mn}(a) = \operatorname{lcm}(\operatorname{ord}_m(a), \operatorname{ord}_n(a))$, by the [Chinese remainder theorem](/chinese-remainder-theorem/).
- **Primitive roots.** $a$ is a [primitive root](/primitive-root/) modulo $n$ exactly when $\operatorname{ord}_n(a) = \varphi(n)$.

**Computing it from a factorization.** Suppose $N$ is a known multiple of $t$, for example $N = \varphi(n)$, and its prime factorization is known. Start with $t \leftarrow N$. For each prime $q$ dividing $N$, as long as $q \mid t$ and $a^{t/q} \equiv 1 \pmod n$, set $t \leftarrow t/q$. At the end, $t = \operatorname{ord}_n(a)$. The reason: for each prime $q$, the loop removes factors $q$ until the next removal would give an exponent that the order no longer divides, so the power of $q$ left in $t$ is exactly the power of $q$ in the order. The number of modular exponentiations is at most the number of prime factors of $N$ with multiplicity plus the number of distinct primes, which is $O(\log N)$. With word-sized $n$ this is $O(\log^2 n)$ word operations; for $k$-digit $n$ and classical arithmetic it is $O(k^4)$ bit operations.

**Without the factorization.** If $\varphi(n)$ is unknown, computing the order is the [order-finding](/order-finding/) problem. For $n = pq$, knowing the orders of random elements gives the factors of $n$, so no fast classical method is expected. Generic methods, such as [baby-step giant-step](/baby-step-giant-step/), take $O(t^{1/2})$ multiplications. [Shor's algorithm](/shor-algorithm/) solves it in polynomial time on a quantum computer.

## Examples

**Prime modulus.** Modulo 7: $\operatorname{ord}_7(2) = 3$, since $2, 4, 1$; and $\operatorname{ord}_7(3) = 6$, since $3, 2, 6, 4, 5, 1$. So 3 is a primitive root modulo 7, and 2 is not. Both orders divide $6$.

**Computing with the factorization.** Find $\operatorname{ord}_{101}(10)$, with $N = 100 = 2^2 \cdot 5^2$. For $q = 2$: $10^{50} \equiv -1 \pmod{101}$, since $10^2 = 100 \equiv -1$, so $t$ stays 100. For $q = 5$: $10^{20} = (10^2)^{10} \equiv 1$, so $t = 20$; then $10^4 \equiv 1$, so $t = 4$; and $5 \nmid 4$. The order is 4.

**Decimal periods.** For a prime $p \ne 2, 5$, the decimal expansion of $1/p$ has period $\operatorname{ord}_p(10)$. So $1/7 = 0.\overline{142857}$ has period $\operatorname{ord}_7(10) = 6$, $1/13$ has period 6, $1/17$ has period 16, and $1/101 = 0.\overline{0099}$ has period 4.

**Powers of two.** For $k \ge 3$, $\operatorname{ord}_{2^k}(3) = \operatorname{ord}_{2^k}(5) = 2^{k-2}$, while $\varphi(2^k) = 2^{k-1}$. So no element has order $\varphi(2^k)$, and there is no primitive root modulo 8, 16, 32, and so on.

**Mersenne and Fermat numbers.** If $q$ is a prime factor of $2^p - 1$ with $p$ prime, then $\operatorname{ord}_q(2) = p$, so $p \mid q - 1$, and since $q$ is odd, $q \equiv 1 \pmod{2p}$. For $2^{11} - 1 = 2047 = 23 \cdot 89$, both factors are $\equiv 1 \pmod{22}$. In the same way, a prime factor $q$ of $2^{32} + 1$ has $\operatorname{ord}_q(2) = 64$, so $q \equiv 1 \pmod{64}$; Euler found the factor $641 = 10 \cdot 64 + 1$.

**Card shuffles.** A perfect out-shuffle of $2m$ cards sends the card at position $i$ (counting from 0) to position $2i \bmod (2m - 1)$, with the last card fixed. The deck returns to its order after $\operatorname{ord}_{2m - 1}(2)$ shuffles: for 52 cards, $\operatorname{ord}_{51}(2) = 8$.

## Where it is used

- **[Primitive roots](/primitive-root/).** A primitive root is an element of order $\varphi(n)$, and the test for it is the algorithm above with all removals failing.
- **Discrete logarithms.** [Pohlig-Hellman](/pohlig-hellman/) reduces a discrete logarithm modulo the order of the base to logarithms modulo its prime-power factors. Groups for [Diffie-Hellman](/diffie-hellman/) use a base whose order is a large prime.
- **Factoring and order finding.** If $a^r \equiv 1 \pmod n$ with $r$ even and $a^{r/2} \not\equiv \pm 1$, then $\gcd(a^{r/2} - 1, n)$ is a proper factor of $n$. This is the classical part of [Shor's algorithm](/shor-algorithm/).
- **Primality proofs.** The [Lucas primality test](/lucas-primality-test/) and [Pocklington's test](/pocklington-primality-test/) prove $n$ prime by finding an element of large order, using the factorization of $n - 1$.
- **Pseudorandom generators.** The period of a multiplicative [linear congruential generator](/linear-congruential-generator/) $x_{i+1} = a x_i \bmod m$ is $\operatorname{ord}_m(a)$ when $\gcd(x_0, m) = 1$; good multipliers have the largest order $\lambda(m)$ (Knuth, Section 3.2.1.2).
- **Periodic sequences.** Cycle lengths of linear recurrences modulo $n$, such as the [Pisano period](/pisano-period/), are orders of elements in related groups.

## References
