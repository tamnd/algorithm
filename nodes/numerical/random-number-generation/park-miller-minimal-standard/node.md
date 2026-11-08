---
tag: HR4MZ7
kind: algorithm
slug: park-miller-minimal-standard
name: Park-Miller minimal standard generator
aliases:
- Lehmer generator
- minimal standard generator
- MINSTD
- minstd_rand0
area: numerical/random-number-generation
level: intro
summary: A multiplicative LCG with modulus 2^31 - 1 and multiplier 16807, a standard baseline.
model: word-ram
complexity:
  vars: {w: "the word size, 32 (signed)"}
  time: {worst: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, in_place: true, recursive: false}
prereqs: [linear-congruential-generator, primitive-root, multiplicative-order]
see_also: [randu, spectral-test, hull-dobell-theorem, generator-period, seed, lecuyer-combined-generator]
sources:
  - paper: doi:10.1145/63039.63042
    title: Stephen K. Park and Keith W. Miller, Random number generators, good ones are hard to find, Communications of the ACM 31(10), 1988, pages 1192 to 1201
    locator: the minimal standard (a = 16807, m = 2^31 - 1), the integer version with Schrage's method, and the check value 1043618065 for x_10000 from x_0 = 1
  - paper: "Linus Schrage, A more portable Fortran random number generator, ACM Transactions on Mathematical Software 5(2), 1979, pages 132 to 138"
    locator: the decomposition m = aq + r that computes ax mod m without overflow when r < q
  - paper: "Stephen K. Park, Keith W. Miller and Paul K. Stockmeyer, Technical correspondence, Communications of the ACM 36(7), 1993, pages 105 to 110"
    locator: the remark of Park and Miller that the multiplier 48271 is preferable to 16807
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.2.1 (Lehmer's multiplicative method of 1949), Section 3.2.1.1 (choice of modulus and the computation of ax mod m), Section 3.2.1.2 (Theorem B on the period of the multiplicative method with prime modulus) and Section 3.3.4 (the spectral test)
  - paper: "P. A. W. Lewis, A. S. Goodman and J. M. Miller, A pseudo-random number generator for the System/360, IBM Systems Journal 8(2), 1969, pages 136 to 146"
    locator: the first proposal of the multiplier 16807 with the modulus 2^31 - 1
  - paper: doi:10.1145/1268776.1268777
    title: Pierre L'Ecuyer and Richard Simard, TestU01, a C library for empirical testing of random number generators, ACM Transactions on Mathematical Software 33(4), article 22, 2007
    locator: Section 7 (the results of SmallCrush, Crush and BigCrush on widely used generators, among them the LCG with m = 2^31 - 1 and a = 16807)
---

The Park-Miller minimal standard generator is the multiplicative [linear congruential generator](/linear-congruential-generator/) $x_{i+1} = 16807\, x_i \bmod (2^{31} - 1)$. The modulus is a prime and $16807 = 7^5$ is a [primitive root](/primitive-root/) of it, so every non-zero seed gives the full period $2^{31} - 2$. Schrage's method computes the product modulo $m$ with signed 32-bit integers only. It was proposed as a portable baseline in 1988, and it is now too small and too regular for serious simulation.

## In plain words

The generator keeps one whole number between 1 and about two billion. To get the next number, it multiplies the current number by 16807 and keeps the remainder after division by $2^{31} - 1$, a prime. Dividing the result by that prime gives a fraction between 0 and 1.

Because the modulus is prime and the multiplier is chosen well, the generator visits every number from 1 to the modulus minus one before it repeats. The number 0 is the one value to avoid: zero times anything is zero, so a generator started at zero stays there.

The product of two 31-bit numbers does not fit in 32 bits. A trick by Schrage splits the multiplication so that every step fits.

## The problem

We use the notation of the [pseudorandom number generator](/pseudorandom-number-generator/) page. The state space is $S = \{1, 2, \ldots, m - 1\}$ with $m = 2^{31} - 1 = 2147483647$. The transition function is $f(x) = a x \bmod m$ with the multiplier $a = 16807$ and the increment $c = 0$. The output function is $g(x) = x / m$, a number in the open interval $(0, 1)$ that imitates a draw from $U(0, 1)$.

The task is to compute $f(x)$ on a machine whose integers are signed 32-bit words, where $a x$ can be as large as about $2^{45.0}$ and does not fit.

## The algorithm

Let $q = \lfloor m / a \rfloor$ and $r = m \bmod a$, so $m = a q + r$. For $a = 16807$, $q = 127773$ and $r = 2836$.

```pseudo id=main
PARK-MILLER-NEXT(x)                         ▷ 1 ≤ x ≤ m − 1, m = 2^31 − 1, a = 16807
L1  q ← ⌊m / a⌋, r ← m mod a                ▷ q = 127773, r = 2836, constants
L2  t ← a · (x mod q) − r · ⌊x / q⌋         ▷ −m < t < m
L3  if t < 0 then t ← t + m
L4  return t                                ▷ the new state; the output is u = t / m
```

Line L2 replaces the high part $a q \lfloor x/q \rfloor$ of the product by $-r \lfloor x / q \rfloor$, which is congruent to it modulo $m$ because $a q = m - r$. Both products in line L2 are less than $m$, so they fit in 31 bits. Line L3 moves a negative result into range. The seed $\sigma$ is mapped to $x_0 = \sigma \bmod m$, and the value 0 is rejected.

## Example

From the seed $x_0 = 1$ the first seven states are below, with the two parts of line L2.

| $i$ | $x_{i-1}$ | $x \bmod q$ | $\lfloor x / q \rfloor$ | $t$ | $x_i$ | $u_i = x_i / m$ |
|---|---|---|---|---|---|---|
| 1 | 1 | 1 | 0 | 16807 | 16807 | 0.000008 |
| 2 | 16807 | 16807 | 0 | 282475249 | 282475249 | 0.131538 |
| 3 | 282475249 | 96919 | 2210 | 1622650073 | 1622650073 | 0.755605 |
| 4 | 1622650073 | 60746 | 12699 | 984943658 | 984943658 | 0.458650 |
| 5 | 984943658 | 69374 | 7708 | 1144108930 | 1144108930 | 0.532767 |
| 6 | 1144108930 | 29488 | 8954 | 470211272 | 470211272 | 0.218959 |
| 7 | 470211272 | 6632 | 3680 | 101027544 | 101027544 | 0.047045 |

None of these steps needs line L3. The largest state needs it: for $x = m - 1 = 2147483646$, $x \bmod q = 2835$ and $\lfloor x / q \rfloor = 16807$, so $t = 16807 \cdot 2835 - 2836 \cdot 16807 = -16807$ and the result is $m - 16807 = 2147466840$, which is $-a \equiv a(m-1) \pmod m$.

Park and Miller give a check value for an implementation: from $x_0 = 1$, the state $x_{10000}$ is $1043618065$. With the multiplier 48271 it is $399268537$.

## Correctness

Two claims make the generator correct. First, line L2 and line L3 return exactly $a x \bmod m$, and each intermediate value lies in $(-m, m)$; this needs only $r \le q$, which holds since $2836 \le 127773$. Second, for every seed in $\{1, \ldots, m - 1\}$ the period is $m - 1$, because $m$ is prime and $a$ is a primitive root modulo $m$. The [multiplicative order](/multiplicative-order/) of 16807 modulo $m$ is $m - 1$ because

$$m - 1 = 2 \cdot 3^2 \cdot 7 \cdot 11 \cdot 31 \cdot 151 \cdot 331$$

and $16807^{(m-1)/p} \not\equiv 1 \pmod m$ for each of the primes $p = 2, 3, 7, 11, 31, 151, 331$. The full proofs are below.

## Complexity

Each output costs two divisions by the constant $q$ (or one division and one multiplication), two multiplications, one subtraction, one comparison and at most one addition: $\Theta(1)$ word operations on 32-bit signed words. The state is one word. The output $u = x / m$ costs one floating-point division or a multiplication by $1/m$. On a machine with 64-bit integers, the product $a x < 2^{46}$ fits, and $a x \bmod m$ can also be computed with shifts because $m$ is a Mersenne number: if $p = a x$, then $p \bmod m$ equals $(p \bmod 2^{31}) + \lfloor p / 2^{31} \rfloor$ reduced by one subtraction of $m$.

## Properties

- **Full period.** Every non-zero seed lies on the one cycle of length $2^{31} - 2$, so all seeds give shifts of the same sequence.
- **Never 0 or 1.** The output lies in $\{1/m, \ldots, (m-1)/m\}$, so $\log(u)$ and $1/u$ are always defined.
- **Lattice structure.** The points $(u_i, u_{i+1}, \ldots, u_{i+t-1})$ lie on a lattice, like those of every LCG. The [spectral test](/spectral-test/) measures the gaps between its hyperplanes.
- **Statistical quality.** With a period of about $2^{31}$, a simulation that uses more than a small fraction of the period sees the lattice. The generator fails several tests of the SmallCrush and Crush batteries of TestU01 in the results of L'Ecuyer and Simard (2007). This is an empirical result.
- **Not secure.** One output reveals the state, and the state gives all later outputs.

## Variants and improvements

- **Multiplier 48271.** Park, Miller and Stockmeyer (1993) advise $a = 48271$, also a primitive root, with better spectral test values. C++ calls it `minstd_rand`, and the 16807 version `minstd_rand0`.
- **Carta's method.** Compute the 46-bit product as two halves and fold the high half back, using $2^{31} \equiv 1 \pmod m$. This avoids division.
- **Combined generators.** [L'Ecuyer's combined generator](/lecuyer-combined-generator/) of 1988 adds two multiplicative generators with different prime moduli to get a period near $2^{61}$.
- **Larger moduli.** Multiplicative generators modulo primes near $2^{61}$ or $2^{63}$, and the [multiple recursive generators](/multiple-recursive-generator/) such as [MRG32k3a](/mrg32k3a/), keep the same theory with a much longer period.

## When to use it

Use it as a reference implementation, for teaching, or to reproduce results of old programs that used it. Do not use it for new simulations: its period is about $2.1 \times 10^9$, which a modern computer exhausts in seconds, and its lattice structure shows in a few dimensions. Use [xoshiro256**](/xoshiro-xoroshiro/), [PCG](/pcg-random/), [MRG32k3a](/mrg32k3a/) or the [Mersenne Twister](/mersenne-twister/) instead. Use a [cryptographically secure generator](/cryptographically-secure-prng/) for anything an adversary can see.

## Pitfalls

- **The seed 0.** Line L2 maps 0 to 0, and the sequence stays at 0. The same holds for each multiple of $m$. Reject such a seed before the first call.
- **Overflow without Schrage.** Writing `x = (a * x) % m` in 32-bit arithmetic overflows for most $x$, and the result is wrong without warning. Use line L2, or 64-bit arithmetic.
- **A wrong multiplier with Schrage.** Line L2 is exact only when $m \bmod a \le \lfloor m / a \rfloor$. A large multiplier such as $a = 630360016$ breaks this condition, and line L2 then overflows.
- **Using the low bits.** The low bits of a prime-modulus generator are better than those of a power-of-two modulus, but the output is still only 31 bits wide. Building a 64-bit value from two outputs does not double the quality or the period.
- **Different conventions.** Some libraries return $x_0$ first, others $x_1$. Compare against the check value $x_{10000} = 1043618065$ with the same convention.

## Implementations

## History

D. H. Lehmer proposed the multiplicative congruential method in 1949. Lewis, Goodman and Miller proposed the multiplier 16807 with the modulus $2^{31} - 1$ for the IBM System/360 in 1969. Schrage published his portable way to compute the product in 1979. Park and Miller (1988) called the generator the "minimal standard" and asked implementers to check it against $x_{10000} = 1043618065$. In 1993, Park, Miller and Stockmeyer said that they now preferred the multiplier 48271.

## References
