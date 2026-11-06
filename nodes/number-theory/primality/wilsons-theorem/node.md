---
tag: 09S8VR
kind: theorem
slug: wilsons-theorem
name: Wilson's theorem
aliases:
- Wilson's primality criterion
- Wilson-Lagrange theorem
area: number-theory/primality
level: core
summary: An integer n > 1 is prime if and only if (n-1)! = -1 (mod n). As a primality test it is exact but slow, since no method computes (n-1)! mod n much faster than about n^(1/2) operations.
prereqs: [wilson-theorem, prime-number, primality-testing]
see_also: [wilson-theorem, trial-division, fermat-little-theorem, modular-inverse, prime-counting-function, quadratic-residue, aks-primality-test, factorial-modulo-prime]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 1.3.3 (Theorem 1.3.6, Wilson primes and Wilson quotients), Section 1.2.5 (the formula for pi(n)), Exercise 1.57 (Clement's theorem), Section 5.5 (polynomial evaluation method) and Exercise 9.73
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition
    locator: Section 2.8.1 (Theorem 2.22, Wilson's theorem, proved with Euler's criterion)
---

Wilson's theorem says that an integer $n > 1$ is [prime](/prime-number/) if and only if $(n - 1)! \equiv -1 \pmod n$. It is an exact criterion for primality that uses no factoring and no randomness. As a [primality test](/primality-testing/) it is useless for large $n$: computing $(n - 1)! \bmod n$ takes about $n$ multiplications directly and about $n^{1/2}$ with the best known methods, no better than [trial division](/trial-division/). This page treats the theorem as a primality criterion; the page on [Wilson's theorem in modular arithmetic](/wilson-theorem/) treats its algebra.

## Statement

**Theorem** (Wilson and Lagrange; Crandall and Pomerance, Theorem 1.3.6). Let $n > 1$ be an integer. Then
$$n \text{ is prime} \iff (n - 1)! \equiv -1 \pmod n.$$
Moreover, if $n$ is composite, then $(n - 1)! \equiv 0 \pmod n$, except for $n = 4$, where $3! \equiv 2 \pmod 4$.

**As a test.** The criterion gives a deterministic decision procedure:

1. Set $f \leftarrow 1$.
2. For $j = 2, 3, \ldots, n - 1$: set $f \leftarrow f \cdot j \bmod n$.
3. Return "prime" if $f = n - 1$, else "composite".

**Cost model.** Let $\ell = \lfloor \lg n \rfloor + 1$ be the bit length of $n$, and count bit operations on integers of arbitrary precision. The loop does $n - 2$ multiplications modulo $n$, each $O(\ell^2)$ with schoolbook arithmetic, so it costs $O(n (\log n)^2)$ bit operations, which is $2^{\ell} \ell^2$ up to a constant: exponential in the input length. With fast polynomial evaluation (below) the cost drops to $n^{1/2 + o(1)}$, still exponential in $\ell$.

## In plain words

Multiply all the numbers from 1 up to one less than $n$, and look at the remainder after division by $n$. If $n$ is prime, the remainder is always $n - 1$. If $n$ is not prime, the remainder is $0$, except for $n = 4$, where it is $2$. So this one product tells exactly whether a number is prime. The trouble is the size of the work: the product has about $n$ factors, and for a number with a hundred digits that is far more steps than any computer can do. Faster tests exist, and this one is mainly a tool for proofs.

## Proof

*Primes satisfy the congruence.* For $p = 2$, $1! = 1 \equiv -1 \pmod 2$. Let $p$ be an odd prime. Each $a \in \{1, \ldots, p - 1\}$ has a [modular inverse](/modular-inverse/) $a^{-1}$ in the same set. Moreover $a^{-1} = a$ only if $a^2 \equiv 1$, that is $p \mid (a - 1)(a + 1)$, so $a = 1$ or $a = p - 1$, since $p$ is prime. So the numbers $2, \ldots, p - 2$ split into pairs $\{a, a^{-1}\}$ with $a \ne a^{-1}$, and the product of each pair is $1$. Hence
$$(p - 1)! \equiv 1 \cdot (p - 1) \cdot \prod_{\text{pairs}} a \, a^{-1} \equiv -1 \pmod p.$$

*Composites do not.* Let $n$ be composite and let $d$ be a divisor with $1 < d < n$. Then $d$ is one of the factors $1, \ldots, n - 1$, so $d \mid (n - 1)!$. If $(n - 1)! \equiv -1 \pmod n$, then also $(n - 1)! \equiv -1 \pmod d$, so $d \mid 1$, which is false.

*The residue for composites.* Write $n = ab$ with $1 < a \le b < n$. If $a < b$, then $a$ and $b$ are distinct factors of $(n - 1)!$, so $n \mid (n - 1)!$. If $a = b$, then $n = a^2$; for $a > 2$, $a < 2a < a^2$, so $a$ and $2a$ are distinct factors, and $n \mid a \cdot 2a$ divides $(n - 1)!$. The only remaining case is $a = b = 2$, that is $n = 4$, where $3! = 6 \equiv 2$. $\blacksquare$

Shoup (Theorem 2.22) proves the prime case in the group $\mathbb{Z}_p^*$, as a by-product of [Euler's criterion](/euler-criterion/): the product of all elements of $\mathbb{Z}_p^*$ is $-1$.

## Consequences

- **An exact but exponential test.** The criterion decides primality with no error, but in time exponential in the bit length. Trial division up to $\sqrt n$ is faster and also finds a factor. Polynomial time tests use other ideas: the randomized [Miller-Rabin test](/miller-rabin/) and the deterministic [AKS test](/aks-primality-test/).
- **Fast factorials would give fast factoring.** If $F(k, n) = k! \bmod n$ were easy to compute, then $n > 1$ would be prime exactly when $\gcd(F(\lfloor \sqrt n \rfloor, n), n) = 1$, and a binary search for the least $k$ with $\gcd(F(k, n), n) > 1$ would find the least prime factor of $n$ (Crandall and Pomerance, Section 5.5).
- **Computing the factorial faster.** Let $m = \lceil \sqrt{n - 1} \rceil$ and $g(t) = (t + 1)(t + 2) \cdots (t + m)$. The product of $g(0), g(m), \ldots, g((m - 1) m)$ is $(m^2)!$, and the few extra factors up to $n - 1$ can be divided out or handled separately. Fast multipoint evaluation computes the $m$ values of $g$ modulo $n$ with $O(m (\log m)^2)$ ring operations, so $(n - 1)! \bmod n$ costs $n^{1/2 + o(1)}$ bit operations (Crandall and Pomerance, Section 5.5 and Exercise 9.73). The Pollard-Strassen factoring method uses the same idea with blocks of size $n^{1/4}$.
- **A formula for $\pi(n)$.** For $j \ge 2$, $\lfloor ((j-1)! + 1)/j \rfloor - \lfloor (j-1)!/j \rfloor$ is $1$ if $j$ is prime and $0$ otherwise, so the [prime-counting function](/prime-counting-function/) is
$$\pi(n) = \sum_{j=2}^{n} \left( \left\lfloor \frac{(j-1)! + 1}{j} \right\rfloor - \left\lfloor \frac{(j-1)!}{j} \right\rfloor \right).$$
Crandall and Pomerance (Section 1.2.5) give it as an example of a formula with no evident value for computation.
- **Twin primes** (Clement's theorem; Crandall and Pomerance, Exercise 1.57). For an integer $p > 1$, the pair $p, p + 2$ consists of two primes if and only if $4 (p - 1)! \equiv -4 - p \pmod{p (p + 2)}$.
- **Square roots of $-1$.** For a prime $p$, pairing $j$ with $p - j$ gives $(p - 1)! \equiv (-1)^{(p-1)/2} \left( \left(\tfrac{p-1}{2}\right)! \right)^2$. So for $p \equiv 1 \pmod 4$, $x = \left(\frac{p-1}{2}\right)!$ satisfies $x^2 \equiv -1 \pmod p$, and $-1$ is a [quadratic residue](/quadratic-residue/). For $p = 13$, $6! = 720 \equiv 5$ and $5^2 = 25 \equiv -1 \pmod{13}$.
- **A variant.** Dividing by $n - 1 \equiv -1$ gives: $n > 1$ is prime if and only if $(n - 2)! \equiv 1 \pmod n$.

## Tightness

- **The exception $n = 4$.** The residue $0$ for composites fails only at $n = 4$, where $3! \equiv 2$. Since $2 \ne 3 \equiv -1$, the criterion itself has no exception.
- **The congruence modulo $p^2$.** The congruence $(p - 1)! \equiv -1$ holds modulo $p$ for each prime, but modulo $p^2$ it holds only for the rare *Wilson primes*. With the Wilson quotient $w_p = ((p - 1)! + 1)/p$, a Wilson prime is a prime with $w_p \equiv 0 \pmod p$. A heuristic gives probability about $1/p$ for each prime, and the only Wilson primes below $5 \cdot 10^8$ are $5$, $13$ and $563$ (Crandall and Pomerance, Section 1.3.3). For example $4! = 24 \equiv -1 \pmod{25}$ and $12! \equiv -1 \pmod{169}$.
- **No shortcut is known.** No algorithm computes $(n - 1)! \bmod n$ in time polynomial in $\log n$; such an algorithm would also factor integers fast, by the consequence above. So the exponential cost is not a weakness of the proof but of all known methods.

**Worked check.** For $n = 7$: $6! = 720 = 102 \cdot 7 + 6$, so $6! \equiv -1$. For $n = 9$: $8! = 40320 = 4480 \cdot 9$, so $8! \equiv 0$. For $n = 4$: $3! = 6 \equiv 2$. The criterion and the residues $0$ and $2$ agree with trial division for every $n \le 3000$.

## History

The theorem carries the name of Wilson, and Crandall and Pomerance call it the Wilson-Lagrange theorem, crediting the converse to Lagrange (Theorem 1.3.6 and the text after it). They also note that factorials modulo $p^2$ have been computed by polynomial evaluation for primes as large as $p = 2^{40} + 5$, in searches for Wilson primes by Crandall, Dilcher and Pomerance (1997), which shows that machines can confirm 12-digit primes with the converse of Wilson's theorem.

## References
