---
tag: 7HXWRF
kind: definition
slug: safe-prime
name: Safe prime
aliases:
- safe prime pair
area: number-theory/primality
level: core
summary: A prime p such that (p-1)/2 is also prime. The group of units modulo p then has order 2q with q prime, which is the structure that Diffie-Hellman groups want.
prereqs: [prime-number, multiplicative-group-modulo-n, sophie-germain-prime]
see_also: [sophie-germain-prime, diffie-hellman, pohlig-hellman, primitive-root, random-prime-generation, small-subgroup-attack, pollard-p-minus-1, quadratic-residue]
sources:
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography
    locator: Chapter 4, Section 4.6.1 (Definition 4.85 and Algorithm 4.86, selecting a k-bit safe prime and a generator)
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition
    locator: Section 5.5.5 (Sophie Germain primes, Conjecture 5.24) and Section 10.3, Exercises 10.3, 10.5, 10.6 and 10.10
  - url: https://www.rfc-editor.org/rfc/rfc3526
    title: T. Kivinen and M. Kojo, RFC 3526, More Modular Exponential (MODP) Diffie-Hellman groups for Internet Key Exchange (IKE), 2003
    locator: Sections 2 and 3 (the 1536-bit and 2048-bit MODP groups)
  - url: https://www.rfc-editor.org/rfc/rfc2409
    title: D. Harkins and D. Carrel, RFC 2409, The Internet Key Exchange (IKE), 1998
    locator: Sections 6.1 and 6.2 (the first and second Oakley groups)
---

A safe prime is a [prime](/prime-number/) $p = 2q + 1$ such that $q$ is also prime; the prime $q$ is then a [Sophie Germain prime](/sophie-germain-prime/). For a safe prime, the [group of units modulo $p$](/multiplicative-group-modulo-n/) has order $2q$, so its only subgroups have orders $1$, $2$, $q$ and $2q$. That makes [discrete logarithms](/discrete-logarithm-problem/) modulo $p$ as hard as the size of $p$ allows, and it makes [generators](/primitive-root/) easy to recognize, which is why [Diffie-Hellman](/diffie-hellman/) standards use safe primes.

## Definition

A prime $p$ is a **safe prime** if $q = (p - 1)/2$ is a prime (Handbook of Applied Cryptography, Definition 4.85). Equivalently, $p = 2q + 1$ with $p$ and $q$ both prime.

**Residues modulo 12.** Each safe prime $p > 7$ satisfies $p \equiv 11 \pmod{12}$. *Proof.* Here $q = (p-1)/2 > 3$, so $q$ is odd and $q \not\equiv 0 \pmod 3$. If $q \equiv 1 \pmod 3$ then $p = 2q + 1 \equiv 0 \pmod 3$, which is impossible for a prime $p > 3$. So $q \equiv 2 \pmod 3$ and $q$ is odd, that is $q \equiv 5 \pmod 6$, and $p = 2q + 1 \equiv 11 \pmod{12}$. $\square$ The exceptions are $p = 5$ ($q = 2$) and $p = 7$ ($q = 3$).

**The group of units.** Let $p = 2q + 1$ be a safe prime with $q$ odd. The group $\mathbb{Z}_p^*$ is cyclic of order $2q$. By Lagrange's theorem each element has order $1$, $2$, $q$ or $2q$. The only element of order 2 is $-1$. The [quadratic residues](/quadratic-residue/) form the subgroup of order $q$, which has prime order. The generators are the elements of order $2q$; there are $\varphi(2q) = q - 1$ of them, almost half the group.

**Generator test** (HAC Algorithm 4.86). For $2 \le g \le p - 2$, $g$ generates $\mathbb{Z}_p^*$ if and only if $g^q \not\equiv 1 \pmod p$. *Proof.* $g \ne \pm 1$, so the order of $g$ is $q$ or $2q$, and it is $q$ exactly when $g^q \equiv 1$. $\square$ By [Euler's criterion](/euler-criterion/), $g^q \equiv \left(\frac{g}{p}\right)$, so the generators in this range are exactly the quadratic non-residues.

**Primality test for $2q + 1$** (Shoup, Exercise 10.3). Let $q$ be prime and $n = 2q + 1$. Then $n$ is prime if and only if $2^{n-1} \equiv 1 \pmod n$. *Proof.* If $n$ is prime, this is [Fermat's little theorem](/fermat-little-theorem/). Conversely, suppose $2^{2q} \equiv 1 \pmod n$. For $q = 2$, $n = 5$ is prime. Let $q$ be odd and let $r$ be a prime factor of $n$, and $d$ the order of 2 modulo $r$. Then $d \mid 2q$, so $d \in \{1, 2, q, 2q\}$. $d = 1$ is impossible, and $d = 2$ means $r \mid 3$, so $r = 3$. If $d \in \{q, 2q\}$, then $q \mid r - 1$, and $r - 1$ is even, so $2q \mid r - 1$ and $r \ge 2q + 1 = n$, so $r = n$ and $n$ is prime. In the remaining case every prime factor of $n$ is 3, so $n = 3^j$ with $j \ge 2$ (as $n \ge 7$). Then $9 \mid n$, and $2^{n-1} \equiv 1 \pmod 9$ needs $6 \mid n - 1 = 2q$ because 2 has order 6 modulo 9. So $3 \mid q$, $q = 3$ and $n = 7$, which is not a power of 3. $\square$ So once $q$ is known to be prime, one Fermat test base 2 proves or disproves the primality of $2q + 1$.

## Examples and non-examples

**Examples.**

- The safe primes below 1000 are $5, 7, 11, 23, 47, 59, 83, 107, 167, 179, 227, 263, 347, 359, 383, 467, 479, 503, 563, 587, 719, 839, 863, 887, 983$. There are 25 of them, against 168 primes.
- Counts of safe primes up to $x$:

| $x$ | $10^3$ | $10^4$ | $10^5$ | $10^6$ | $10^7$ |
|---|---|---|---|---|---|
| safe primes up to $x$ | 25 | 115 | 670 | 4324 | 30657 |
| all primes up to $x$ | 168 | 1229 | 9592 | 78498 | 664579 |

- $p = 23$, $q = 11$. The generators of $\mathbb{Z}_{23}^*$ are $5, 7, 10, 11, 14, 15, 17, 19, 20, 21$, which is $q - 1 = 10$ elements, and each of them satisfies $g^{11} \equiv -1 \pmod{23}$.
- The Internet Key Exchange groups use safe primes of the form $p = 2^L - 2^{L - 64} - 1 + 2^{64} \left( \lfloor 2^{L - 130} \pi \rfloor + c \right)$, where $c$ is a small offset that makes $p$ a safe prime: $c = 149686$ for $L = 768$ and $c = 129093$ for $L = 1024$ (RFC 2409), $c = 741804$ for $L = 1536$ and $c = 124476$ for $L = 2048$ (RFC 3526). The top 64 and bottom 64 bits are all ones, and the binary digits of $\pi$ fix the middle bits, so only the offset $c$ was free. Each of these $p$ is $\equiv 7 \pmod 8$, so $2$ is a quadratic residue, and the RFC generator $g = 2$ generates the subgroup of prime order $q$.

**Non-examples.**

- $13$, $17$, $29$ and $31$ are primes but not safe primes: $(p-1)/2$ is $6$, $8$, $14$ and $15$.
- $3 = 2 \cdot 1 + 1$ is not a safe prime, since $1$ is not prime. $2$ is not a safe prime.
- $15 = 2 \cdot 7 + 1$ has $q = 7$ prime but is composite. The test above sees this at once: $2^{14} \equiv 4 \pmod{15}$.
- A prime $p$ for which $p - 1$ has only small prime factors is the opposite of a safe prime. For such $p$, [Pohlig-Hellman](/pohlig-hellman/) computes discrete logarithms modulo $p$ fast, because it works in each prime-order part of $\mathbb{Z}_p^*$ separately.

## Related definitions

- **[Sophie Germain prime](/sophie-germain-prime/).** The prime $q$ with $2q + 1$ prime. Safe primes are the numbers $2q + 1$ for Sophie Germain primes $q$, so the safe primes up to $x$ match the Sophie Germain primes up to $(x - 1)/2$. Whether there are infinitely many is open; Shoup's Conjecture 5.24 gives the expected density.
- **Generating safe primes.** Pick a random $q$, test $q$ and $2q + 1$ for small factors together, then run [Miller-Rabin](/miller-rabin/) on $q$ and the base-2 test above on $2q + 1$ (Shoup, Exercises 10.5, 10.6 and 10.10; HAC Algorithm 4.86). Under Conjecture 5.24, the expected number of candidates grows like $(\ln p)^2$, against $\ln p$ for a plain [random prime](/random-prime-generation/) of the same size.
- **Strong prime.** A prime $p$ such that $p - 1$ and $p + 1$ have large prime factors, with further conditions (HAC Definition 4.52). A safe prime meets the condition on $p - 1$ in the strongest way. Large prime factors of $p - 1$ defeat [Pollard's $p - 1$ method](/pollard-p-minus-1/) when $p$ is a secret factor of an RSA modulus.
- **[Small subgroup attack](/small-subgroup-attack/).** An attack that pushes a protocol into a small subgroup of $\mathbb{Z}_p^*$. For a safe prime the only small subgroups are $\{1\}$ and $\{1, -1\}$, so a check against $\pm 1$ stops it.
- **[Primitive root](/primitive-root/).** A generator of $\mathbb{Z}_p^*$. For a safe prime, the factorization $p - 1 = 2q$ is known, so one exponentiation recognizes a generator.

## References
