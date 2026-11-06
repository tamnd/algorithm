---
tag: 8SP71V
kind: algorithm
slug: pollard-p-minus-1
name: Pollard's p-1 algorithm
aliases:
- Pollard p-1
area: number-theory/factorization
level: core
summary: Computes g = gcd(a^M - 1, N) with M = lcm(1, 2, ..., B). It finds a prime factor p of N when p - 1 has no prime power factor above B, with O(B) multiplications modulo N.
solves: [integer-factorization]
model: word-ram
complexity:
  vars: {N: the integer to factor, n: the number of binary digits of N, B: the smoothness bound}
  time: {worst: O(B log log B)}
  space: {extra: O(B)}
  multiplications_mod_N: {worst: O(B)}
  bit_operations: {worst: O(B n^2 + B log log B)}
properties: {deterministic: true, recursive: false}
prereqs: [fermat-little-theorem, modular-exponentiation, greatest-common-divisor, smooth-number]
see_also: [williams-p-plus-1, elliptic-curve-factorization, pollard-rho, trial-division, multiplicative-order, dickman-function, rsa-cryptosystem, integer-factorization]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 5.4, Pollard p - 1 method, pages 236 to 238 (Algorithm 5.4.1, the failures for n = 2047, and the second stage)
  - paper: "J. M. Pollard, Theorems on factorization and primality testing, Proceedings of the Cambridge Philosophical Society 76, 1974"
    locator: pages 521 to 528 (the p - 1 method)
  - paper: "Peter L. Montgomery, Speeding the Pollard and elliptic curve methods of factorization, Mathematics of Computation 48(177), 1987"
    locator: pages 243 to 264 (the second stage of the p - 1 method)
---

Pollard's $p - 1$ algorithm finds a [prime](/prime-number/) factor $p$ of an integer $N$ when $p - 1$ is a product of small prime powers. It raises a base $a$ to a large exponent $M$ that is a multiple of every such $p - 1$, and then takes $\gcd(a^M - 1, N)$. By [Fermat's little theorem](/fermat-little-theorem/), $a^M \equiv 1 \pmod p$, so $p$ divides the gcd. The cost depends on the bound $B$ on the prime powers of $p - 1$, not on the size of $p$, so it can find a large factor quickly when $p - 1$ is [smooth](/smooth-number/), and it fails when $p - 1$ has a large prime factor.

## In plain words

Take a prime $p$ that divides your number. Fermat's little theorem says that a power of $a$ whose exponent is a multiple of $p - 1$ leaves the remainder $1$ when divided by $p$.

You do not know $p$, so you do not know $p - 1$. But if $p - 1$ is made only of small primes, then a big exponent built from all small primes is a multiple of it. Raise $a$ to that big exponent, working modulo your number so the values stay small. Subtract one. The result is a multiple of $p$, so its common divisor with your number shows $p$.

If $p - 1$ has a big prime factor, the method cannot find $p$. A different curve or group, as in the elliptic curve method, gives a new chance.

## The problem

**Input.** An integer $N \ge 3$, a bound $B \ge 1$, and a base $a$ with $2 \le a < N$. In practice $N$ is odd and composite, with its small factors removed by [trial division](/trial-division/).

**Output.** The divisor $g = \gcd(a^M - 1, N)$ of $N$, where $M = M(B)$ is the least common multiple of $1, 2, \dots, B$. The method succeeds when $1 < g < N$. Repeated on $g$ and $N/g$, it gives a full [integer factorization](/integer-factorization/), but only when enough of the primes $p$ have a smooth $p - 1$.

**Cost model.** On the [word RAM](/word-ram/) with $N < 2^w$, a multiplication modulo $N$ costs $O(1)$. For an arbitrary-precision $N$ with $n$ binary digits, one multiplication modulo $N$ costs $O(n^2)$ bit operations with schoolbook arithmetic, or $O(M(n))$ with fast multiplication. The primes up to $B$ come from a [sieve of Eratosthenes](/sieve-of-eratosthenes/) in $O(B \log \log B)$ word operations.

## The algorithm

A prime power $q^e$ divides $M(B)$ exactly when $q^e \le B$, so $M(B) = \prod_{q \le B} q^{e_q}$, where $q^{e_q}$ is the largest power of $q$ that is at most $B$.

```pseudo id=main
POLLARD-P-MINUS-1(N, B, a)                ▷ N ≥ 3, B ≥ 1, 2 ≤ a < N; returns gcd(a^M − 1, N), M = lcm(1, …, B)
L1  c ← a
L2  for each prime q ≤ B, in increasing order do
L3      e ← the largest integer with q^e ≤ B
L4      c ← c^(q^e) mod N
L5  g ← gcd(c − 1, N)
L6  return g
```

Line L4 is a [modular exponentiation](/modular-exponentiation/) by repeated squaring. After the loop, $c = a^{M(B)} \bmod N$. Line L5 takes one gcd at the end; a program can also take it after every few primes, to stop early and to lower the chance that $g = N$.

## Example

Let $N = 1403$, $B = 5$ and $a = 2$. Then $M(5) = 2^2 \cdot 3 \cdot 5 = 60$.

| $q$ | $q^e \le 5$ | $c$ after line L4 | $\gcd(c - 1, N)$ |
|---|---|---|---|
| 2 | 4 | $2^4 = 16$ | 1 |
| 3 | 3 | $16^3 \bmod 1403 = 1290$ | 1 |
| 5 | 5 | $1290^5 \bmod 1403 = 1343$ | 61 |

The method returns $g = 61$, and $N = 23 \cdot 61$. The reason is in the two values of $p - 1$: $61 - 1 = 60 = 2^2 \cdot 3 \cdot 5$ divides $M(5)$, while $23 - 1 = 2 \cdot 11$ does not, because $11 > 5$. So $2^{60} \equiv 1 \pmod{61}$, while $2^{60} \equiv 9 \pmod{23}$.

## Correctness

The output $g$ is a gcd with $N$, so it always divides $N$. If a prime $p \mid N$ with $p \nmid a$ has every prime power factor of $p - 1$ at most $B$, then $p - 1$ divides $M(B)$, so $a^{M(B)} \equiv 1 \pmod p$ by Fermat's little theorem, and $p \mid g$. If some prime power $r^k \parallel N$ has $a^{M(B)} \not\equiv 1 \pmod{r^k}$, then $r^k \nmid g$ and $g < N$. Both together give $1 < g < N$. The loop ends after $\pi(B)$ passes. The full proof is below.

## Complexity

**Multiplications.** Line L4 with the exponent $q^e \le B$ takes at most $2 \lg(q^e) \le 2 \lg B$ multiplications modulo $N$. The total is at most $2 \lg M(B) = 2\psi(B)/\ln 2$, where $\psi(B) = \ln M(B)$ is Chebyshev's function. By the [prime number theorem](/prime-number-theorem/), $\psi(B) \sim B$, so stage 1 costs $O(B)$ multiplications modulo $N$, about $1.44 B$ squarings.

- **Word RAM** ($N < 2^w$). The time is $O(B \log \log B)$ for the sieve plus $O(B)$ for the powers, so $O(B \log \log B)$, with $O(B)$ words for the sieve. A segmented sieve lowers the space to $O(B^{1/2})$.
- **Arbitrary precision.** The cost is $O(B n^2)$ bit operations for the powers with schoolbook multiplication, plus the gcd in $O(n^2)$, plus the sieve.

**When it succeeds.** The method finds $p$ once $B$ reaches the largest prime power factor of $p - 1$. This bound has nothing to do with the size of $p$ itself, so the method is fast for some large primes and slow for some small ones. In the worst case, $p = 2q + 1$ with $q$ prime, the method needs $B \ge (p - 1)/2$ and so costs $\Theta(p)$ multiplications, more than [trial division](/trial-division/). If $p - 1$ behaves like a random integer of its size, the chance that it is $B$-smooth with $B = p^{1/u}$ is about $\rho(u) \approx u^{-u}$, where $\rho$ is the [Dickman function](/dickman-function/). This is a heuristic: $p - 1$ is always even and is not a random number, and no unconditional bound on the success rate is known.

## Properties

- **Deterministic.** For fixed $N$, $B$ and $a$, the output is fixed. Only the choice of $a$ and $B$ is free.
- **Depends on one number per prime.** For each prime $p \mid N$, success is decided by the multiplicative order of $a$ modulo $p$, a divisor of $p - 1$. A new base $a$ can change the order, but not $p - 1$, so a prime $p$ with a large prime factor in $p - 1$ stays out of reach whatever $a$ is.
- **Finds any prime of a given shape.** It finds $p$ with a smooth $p - 1$ regardless of the size of $p$ or of $N$.
- **Two kinds of failure.** If no prime factor has a smooth enough $p - 1$, then $g = 1$. If all prime factors do, then $g = N$.

## Variants and improvements

- **Second stage.** After stage 1, look for primes $p$ with $p - 1 = Q u$, where $u$ divides $M(B)$ and $Q$ is one prime in $(B, B']$. Starting from $b = a^{M(B)}$, step from $b^{Q_i}$ to $b^{Q_{i+1}}$ by multiplying with a precomputed $b^{Q_{i+1} - Q_i}$; the gaps between primes are small, so each $Q_i$ costs about one multiplication. With the same time as stage 1, $B'$ can be about $B \ln B$ (Crandall and Pomerance). Montgomery's fast stage 2 uses polynomial arithmetic and allows a much larger $B'$.
- **Early and staggered gcds.** If $g = N$, take the gcd after each prime $q$, or after each single factor $q$ of the exponent, or try another base. For $N = 2047 = 23 \cdot 89$ with $a = 2$, the order of $2$ is $11$ modulo both primes, so $B = 10$ gives $g = 1$ and $B = 12$ gives $g = N$; the base $a = 12$ with $B = 8$ gives $g = 89$.
- **[Williams' p + 1 method](/williams-p-plus-1/).** It replaces the group $(\mathbb{Z}/p\mathbb{Z})^*$ of order $p - 1$ by a group of order $p + 1$, using Lucas sequences, and finds $p$ when $p + 1$ is smooth.
- **[The elliptic curve method](/elliptic-curve-factorization/).** It replaces the group by the points of a random elliptic curve modulo $p$, whose order varies with the curve near $p + 1$. If one curve fails, another one can work. This removes the main weakness of the $p - 1$ method.

## When to use it

Run a short stage 1 and stage 2 of the $p - 1$ method early in a factoring program, after trial division and before the [elliptic curve method](/elliptic-curve-factorization/). It is cheaper per step than one ECM curve and catches the primes with a smooth $p - 1$. For a general number with no special structure, ECM has the better chance per unit of time. In [RSA](/rsa-cryptosystem/) key generation, the method is the reason for the old advice to choose primes $p$ where $p - 1$ has a large prime factor; with random primes of today's sizes, the chance of a smooth $p - 1$ is negligible anyway.

## Pitfalls

- **The base shares a factor with $N$.** If $\gcd(a, N) > 1$, then $c$ is never $1$ modulo that prime. Check $\gcd(a, N)$ first; a result above $1$ is already a factor.
- **Small prime powers.** With exponent $q$ instead of $q^e$ in line L4, the method misses $p$ with $4 \mid p - 1$ or $9 \mid p - 1$ and $B$ small. For $N = 1403$ above, the exponent $2 \cdot 3 \cdot 5 = 30$ gives $g = 1$, because $4 \mid 60$.
- **Raising the bound after $g = N$.** A larger $B$ cannot help then. Take gcds more often or change the base.
- **A prime $N$.** For prime $N$, Fermat's little theorem gives $g = N$ once $N - 1$ is $B$-smooth, and $g = 1$ otherwise. Test primality before you call the method, so you do not read $g = N$ as a failure to retry.
- **Many bases at once.** All bases fail together on a prime with a non-smooth $p - 1$. More bases do not help; more groups (Williams, ECM) do.

## Implementations

## History

John Pollard published the method in 1974, in a paper that also gave a deterministic factoring algorithm in about $N^{1/4}$ operations ([the Pollard-Strassen algorithm](/pollard-strassen/)). Hugh Williams used the same idea with a group of order $p + 1$ in 1982. Hendrik Lenstra's [elliptic curve method](/elliptic-curve-factorization/) of 1987 took the decisive step of using many groups whose orders vary, and Peter Montgomery made the second stage of both methods much faster in the same year.

## References
