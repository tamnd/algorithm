---
tag: HSYVA5
kind: algorithm
slug: miller-rabin-primality-test
name: Miller-Rabin primality test
aliases:
- strong probable prime test
- Rabin-Miller test
area: randomized/monte-carlo-and-las-vegas
level: core
summary: Tests n with random bases by looking for a nontrivial square root of 1 in a^d, a^(2d), ..., a^(n-1) mod n; a random base catches a composite with probability at least 3/4.
solves: [primality-testing]
model: word-ram
complexity:
  vars: {n: the integer to test, k: the number of rounds}
  time: {worst: O(k log^3 n)}
  space: {extra: O(log n)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 1980
  people: [Gary L. Miller, Michael O. Rabin]
  note: Miller gave a deterministic test that is correct under the extended Riemann hypothesis in 1976; Rabin turned it into an unconditional randomized test with error at most 1/4 per base in 1980.
prereqs: [modular-exponentiation, fermat-primality-test, one-sided-error, multiplicative-group-modulo-n]
see_also: [solovay-strassen-primality-test, fermat-primality-test, aks-primality-test, deterministic-miller-rabin-bases, strong-pseudoprime, carmichael-number, nontrivial-square-root-of-one, error-amplification]
sources:
  - paper: doi:10.1016/0022-314X(80)90084-0
    title: Michael O. Rabin, Probabilistic algorithm for testing primality, Journal of Number Theory 12(1), 1980
    locator: pages 128 to 138 (the randomized test and the bound of at most (n-1)/4 strong liars)
  - paper: doi:10.1016/0304-3975(80)90007-9
    title: Louis Monier, Evaluation and comparison of two efficient probabilistic primality testing algorithms, Theoretical Computer Science 12(1), 1980
    locator: pages 97 to 108 (the exact number of strong liars and of Euler liars, and the bound phi(n)/4 for n other than 9)
  - paper: "Gary L. Miller, Riemann's hypothesis and tests for primality, Journal of Computer and System Sciences 13(3), 1976"
    title: Gary L. Miller, Riemann's hypothesis and tests for primality
    locator: pages 300 to 317 (the deterministic test under the extended Riemann hypothesis)
  - paper: doi:10.1090/S0025-5718-1990-1023756-8
    title: Eric Bach, Explicit bounds for primality testing and related problems, Mathematics of Computation 55(191), 1990
    locator: pages 355 to 380 (under the extended Riemann hypothesis, a composite n has a witness below 2 (ln n)^2)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 3.5, Algorithm 3.5.2 (strong probable prime test) and Theorem 3.5.4 (Monier and Rabin, at most phi(n)/4 strong liars for n > 9)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 14, Number theoretic algorithms (primality testing)
---

The Miller-Rabin test decides whether an odd integer $n$ is prime by checking random bases $a$. It writes $n - 1 = 2^s d$ with $d$ odd and looks at the sequence $a^d, a^{2d}, \dots, a^{2^s d} \bmod n$. For a prime, this sequence is all ones, or it reaches $n - 1$ before it reaches 1, because the only square roots of 1 modulo a prime are $\pm 1$. A composite $n$ fails this for at least $3/4$ of the bases (Rabin 1980, Monier 1980). So the test is a [Monte Carlo algorithm](/monte-carlo-algorithm/) with [one-sided error](/one-sided-error/): COMPOSITE is always right, and PROBABLY PRIME is wrong with probability at most $4^{-k}$ after $k$ rounds. Unlike the [Fermat test](/fermat-primality-test/), it has no bad inputs such as the [Carmichael numbers](/carmichael-number/).

## In plain words

Fermat's little theorem says that for a prime $n$, raising any base to the power $n - 1$ gives 1. Some composite numbers also give 1 for almost every base, so that check alone can be fooled forever.

Miller-Rabin also watches how the value reaches 1. It starts from a large odd power of the base and squares again and again. For a prime, the step just before the first 1 must be $n - 1$, which plays the role of minus one. If the value jumps to 1 from anything else, or never reaches 1, the number is surely composite. A composite number can fool this check for at most a quarter of the bases, so a few random bases make a mistake very unlikely.

## The problem

Given an integer $n \ge 1$, decide whether $n$ is prime. See [primality testing](/primality-testing/). The input size is $\log_2 n$ bits, so an efficient test runs in time polynomial in $\log n$.

Notation on this page: $n - 1 = 2^s d$ with $d$ odd; $\varphi$ is [Euler's totient](/euler-totient/); $\mathbb{Z}_n^*$ is the [group of units modulo n](/multiplicative-group-modulo-n/); $\Pr$ is over the bases. A base $a$ is a **strong liar** for an odd composite $n$ if $a^d \equiv 1$ or $a^{2^j d} \equiv -1 \pmod n$ for some $0 \le j < s$, and a **witness** otherwise. Randomness model: each base is uniform on $\{2, \dots, n - 2\}$, drawn by rejection from uniform random bits.

## The algorithm

```pseudo id=main
MILLER-RABIN(n, k)
L1  if n ∈ {2, 3} then return PRIME;  if n < 2 or n even then return COMPOSITE
L2  write n − 1 = 2^s · d with d odd
L3  for i ← 1 to k do
L4      a ← uniform integer in {2, ..., n − 2}
L5      x ← a^d mod n                          ▷ modular exponentiation
L6      if x = 1 or x = n − 1 then continue with the next round
L7      repeat s − 1 times
L8          x ← x² mod n
L9          if x = n − 1 then continue with the next round
L10     return COMPOSITE                        ▷ a is a witness; always correct
L11 return PROBABLY PRIME                       ▷ wrong with probability at most 4^-k
```

Line L10 is reached in two ways. Either some $x \ne \pm 1$ squares to 1, which is a [nontrivial square root of 1](/nontrivial-square-root-of-one/) and cannot exist modulo a prime, or $a^{n-1} \not\equiv 1$, which breaks Fermat's little theorem. The loop of line L7 stops before $x_s = a^{n-1}$, since only the value $n - 1$ at an earlier step can save the base.

## Example

**A Carmichael number.** $n = 561 = 3 \cdot 11 \cdot 17$ has $n - 1 = 560 = 2^4 \cdot 35$, so $s = 4$ and $d = 35$. With $a = 2$:

| step | line | value mod 561 |
| --- | --- | --- |
| $x_0 = 2^{35}$ | L5 | 263 |
| $x_1 = x_0^2$ | L8 | 166 |
| $x_2 = x_1^2$ | L8 | 67 |
| $x_3 = x_2^2$ | L8 | 1 |

No value is 560, so line L10 returns COMPOSITE. In fact $67^2 \equiv 1$ with $67 \ne \pm 1$, a nontrivial square root of 1, and $\gcd(67 - 1, 561) = 33$ is a factor. The Fermat test with base 2 passes, since $2^{560} \equiv 1$; the Fermat test passes for every base coprime to 561. Only 10 of the 320 units are strong liars for 561, so a random base from $\{2, \dots, 559\}$ fools the test with probability $8/558 \approx 0.014$.

**A liar and a witness.** $n = 221 = 13 \cdot 17$ has $n - 1 = 2^2 \cdot 55$. Base 174 gives $x_0 = 47$, then $x_1 = 220 = n - 1$, so 174 is a strong liar and the round passes. Base 137 gives $188, 205$, and line L10 returns COMPOSITE.

**A prime.** $n = 97$ has $n - 1 = 2^5 \cdot 3$. Base 5 gives $28, 8, 64, 22, 96$, and $96 = n - 1$ ends the round with a pass, as Lemma 1 of the proof says it must.

## Correctness

If $n$ is prime, then $a^{n-1} \equiv 1$ and the only square roots of 1 are $\pm 1$, so walking back from $a^{2^s d} = 1$ to the first 1 in the sequence finds $n - 1$ just before it, or the sequence starts at 1. So a prime is never called composite. If $n$ is an odd composite, the strong liars all lie in a proper subgroup of $\mathbb{Z}_n^*$: the subgroup $\{x : x^{n-1} \equiv 1\}$ when $n$ is a prime power, and the subgroup $\{x : x^{m} \equiv \pm 1\}$ for a well chosen $m = 2^{j_0} d$ when $n$ has two coprime factors, which the [Chinese remainder theorem](/chinese-remainder-theorem/) shows to be proper. By [Lagrange's theorem](/lagranges-theorem-group-theory/) there are at most $\varphi(n)/2$ strong liars, which gives error at most $1/2$ per round. The sharper bound $\varphi(n)/4$ for $n \ne 9$ is due to Rabin (1980) and Monier (1980); the [full proof](proofs/correctness.md) proves the bound $1/2$ in full, states the bound $1/4$ with Monier's exact count, and proves that every strong liar is an Euler liar.

## Complexity

- **Time.** Line L5 is a [modular exponentiation](/modular-exponentiation/) with $O(\log n)$ multiplications modulo $n$, and lines L7 to L9 do at most $s - 1 < \log_2 n$ more. One round is $O(\log n)$ multiplications of $O(\log n)$-bit numbers, so $O(\log^3 n)$ bit operations with schoolbook multiplication and $\tilde{O}(\log^2 n)$ with fast multiplication. $k$ rounds cost $k$ times as much.
- **Rounds for a target error.** Error $\delta$ needs $k = \lceil \log_4(1/\delta) \rceil$ rounds by the worst-case bound: 4 for $10^{-2}$, 10 for $10^{-6}$, 15 for $10^{-9}$ and 32 for $2^{-64}$. See [error amplification](/error-amplification/).
- **Space.** $O(\log n)$ bits.
- **Random bits.** About $\log_2 n$ bits per round.

## Properties

- **One-sided error.** COMPOSITE is always right and comes with a witness $a$, which anyone can check. So PRIMES is in [co-RP](/co-rp/). Since 2002 it is also in P by the [AKS test](/aks-primality-test/).
- **No bad inputs.** The bound $1/4$ holds for every odd composite, including Carmichael numbers. The Fermat test has no such bound.
- **Exact liar counts.** Monier's formula gives the number of strong liars. Below 2000, the bound $\varphi(n)/4$ is reached only at $n = 15, 91, 703$ and $1891$. Below 10000, the Carmichael numbers have few strong liars: 10 of 320 for 561, 162 of 1296 for 1729, 1782 of 7128 for 8911 (exactly a quarter).
- **Stronger than Solovay-Strassen.** Every strong liar is an Euler liar, see the proof. So one Miller-Rabin round with a base $a$ catches every composite that one [Solovay-Strassen](/solovay-strassen-primality-test/) round with $a$ catches, and it does not need the [Jacobi symbol](/jacobi-symbol/). For $n \equiv 3 \pmod 4$ the two tests accept the same bases.
- **Random inputs are easier.** For a random odd $n$ of many bits, the chance that one round passes a composite is far below $1/4$. The bound $1/4$ is a worst case over $n$.

## Variants and improvements

- **Fixed bases.** For $n$ below a known bound, a fixed set of bases has no common strong pseudoprime, which gives a deterministic test. The smallest [strong pseudoprime](/strong-pseudoprime/) to base 2 is 2047, and the smallest to both bases 2 and 3 is $1373653 = 829 \cdot 1657$. Tables of bases that are enough for all 32-bit and 64-bit integers are on [deterministic Miller-Rabin bases](/deterministic-miller-rabin-bases/).
- **Miller's deterministic test.** Miller (1976) showed that, if the extended Riemann hypothesis holds, every odd composite $n$ has a witness $a = O((\ln n)^2)$. Bach (1990) made the constant explicit: a witness below $2(\ln n)^2$ exists. Testing all these bases gives a deterministic polynomial-time test whose correctness depends on the hypothesis.
- **Baillie-PSW.** One Miller-Rabin round with base 2 followed by a strong Lucas test has no known counterexample. See [Baillie-PSW](/baillie-psw/).
- **Factoring from a witness.** When line L8 finds $x \ne \pm 1$ with $x^2 \equiv 1$, $\gcd(x - 1, n)$ is a proper factor of $n$. For a Carmichael number, $a^{n-1} \equiv 1$ for every unit $a$, so every witness that is a unit is of this kind.
- **Certifying primality.** PROBABLY PRIME is not a proof. Elliptic curve primality proving or AKS give a certificate or a deterministic answer.

## When to use it

- The default primality test in practice, for example to generate the primes of an [RSA](/rsa-cryptosystem/) key. With a few rounds and a trial division by small primes first, it is fast and its error is far below the rate of hardware faults.
- For $n < 2^{64}$, use a fixed set of bases instead of random ones, which makes the answer exact.
- For an adversarial $n$, use random bases, not fixed ones. A number can be built to pass any fixed set of bases.
- When a proof of primality is needed, use a certifying method after Miller-Rabin has filtered out the composites.

## Pitfalls

- **Bases outside $\{2, \dots, n - 2\}$.** The bases 1 and $n - 1$ are liars for every $n$. A fixed base $a$ with $n \mid a$, such as the base 7 for $n = 7$, gives $x = 0$ and a wrong COMPOSITE for a prime. Code with fixed bases must handle the primes among the bases first.
- **Even $n$ and small $n$.** The decomposition $n - 1 = 2^s d$ with $s \ge 1$ needs $n$ odd, and the range of line L4 is empty for $n = 3$. Line L1 handles these cases.
- **Stopping the loop at $x_s$.** Checking $x_s = n - 1$ would accept bases with $a^{n-1} \equiv -1$, which no prime has.
- **Overflow in $x^2$.** For 64-bit $n$, the product $x \cdot x$ needs 128 bits. Use a 128-bit product or Montgomery multiplication.
- **Fixed bases against an adversary.** A composite can be built to pass the first $t$ prime bases, for any $t$. Random bases avoid this.
- **Reading $4^{-k}$ as the chance that $n$ is composite.** The bound is the chance that a composite $n$ passes, not the chance that a number that passed is composite. The second depends on how $n$ was chosen.

## Implementations

## History

Gary Miller (1976) gave a deterministic test based on the strong condition and proved it correct under the extended Riemann hypothesis. Michael Rabin (1980) removed the hypothesis by choosing the bases at random and proved that at most $(n-1)/4$ bases are liars. Louis Monier (1980) found the exact number of strong liars and compared the test with the Solovay-Strassen test. Bach (1990) gave the explicit bound $2(\ln n)^2$ on the least witness under the extended Riemann hypothesis. In 2002 Agrawal, Kayal and Saxena gave a deterministic polynomial-time test, but Miller-Rabin remains the test in use because it is much faster.

## References
