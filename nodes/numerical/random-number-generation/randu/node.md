---
tag: 352H47
kind: algorithm
slug: randu
name: RANDU
aliases:
- IBM RANDU
area: numerical/random-number-generation
level: intro
summary: A famously poor 1960s LCG with multiplier 65539 whose triples fall on few planes.
model: word-ram
complexity:
  vars: {w: "the word size, 32"}
  time: {worst: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, in_place: true, recursive: false}
prereqs: [linear-congruential-generator, multiplicative-order]
see_also: [park-miller-minimal-standard, spectral-test, marsaglia-hyperplane-theorem, hull-dobell-theorem, generator-period, statistical-tests-for-randomness]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.2.1.2 (Theorem B, the maximum period 2^(e-2) of the multiplicative method modulo 2^e) and Section 3.3.4 (the spectral test, with RANDU as the example of a bad multiplier)
  - paper: doi:10.1073/pnas.61.1.25
    title: George Marsaglia, Random numbers fall mainly in the planes, Proceedings of the National Academy of Sciences 61(1), 1968, pages 25 to 28
    locator: the theorem that t-tuples of a multiplicative congruential generator lie on a small number of parallel hyperplanes
  - paper: doi:10.1145/1268776.1268777
    title: Pierre L'Ecuyer and Richard Simard, TestU01, a C library for empirical testing of random number generators, ACM Transactions on Mathematical Software 33(4), article 22, 2007
    locator: Section 7 (the results of the batteries on old generators, among them RANDU)
---

RANDU is the multiplicative [linear congruential generator](/linear-congruential-generator/) $x_{i+1} = 65539\, x_i \bmod 2^{31}$, distributed by IBM in the 1960s. Because $65539 = 2^{16} + 3$, its square is $6 \cdot 65539 - 9$ modulo $2^{31}$, so every three consecutive outputs satisfy $9 u_i - 6 u_{i+1} + u_{i+2} \in \mathbb{Z}$, and all points $(u_i, u_{i+1}, u_{i+2})$ lie on only 15 planes. Its period is $2^{29}$ for an odd seed. It is the standard example of a bad generator.

## In plain words

RANDU keeps one odd number below about two billion. To get the next number, it multiplies by 65539 and keeps the remainder after division by $2^{31}$. The multiplier was chosen because a computer can multiply by it fast, with one shift and two additions.

That choice is the problem. Take any three numbers in a row from RANDU and combine them: nine times the first, minus six times the second, plus the third. The result is always a whole number. So if you plot the triples as points in a cube, they do not fill the cube. They lie on 15 flat sheets with empty space between them. A simulation in three dimensions sees this at once.

## The problem

We use the notation of the [pseudorandom number generator](/pseudorandom-number-generator/) page. The modulus is $m = 2^{31}$, the multiplier is $a = 65539 = 2^{16} + 3$ and the increment is $c = 0$. The state space is the set of odd integers in $[1, 2^{31})$, the transition function is $f(x) = a x \bmod m$ and the output function is $g(x) = x / 2^{31}$, which imitates a draw from $U(0, 1)$. The word size is $w = 32$; the reference code used the signed 32-bit integer overflow of the IBM System/360 and then cleared the sign.

## The algorithm

```pseudo id=main
RANDU-NEXT(x)                                ▷ x odd, 0 < x < 2^31
L1  x ← (x · 2^16 + 2x + x) mod 2^31          ▷ = 65539 · x mod 2^31, a shift and two additions
L2  return x, u ← x / 2^31                    ▷ the new state and the output
```

Line L1 computes $a x = (2^{16} + 2 + 1) x$ with a left shift by 16 and two additions, and the reduction modulo $2^{31}$ keeps the low 31 bits. Line L2 scales the state to the unit interval.

## Example

From the seed $x_0 = 123456789$, the first states and the index $j = 9 u_{i-2} - 6 u_{i-1} + u_i$ of the plane of the triple that ends at $x_i$ are:

| $i$ | $x_i$ | $u_i$ | $9 x_{i-2} - 6 x_{i-1} + x_i$ | plane $j$ |
|---|---|---|---|---|
| 0 | 123456789 | 0.057489 | | |
| 1 | 1663592255 | 0.774671 | | |
| 2 | 280507837 | 0.130622 | $-4 \cdot 2^{31}$ | $-4$ |
| 3 | 1743102263 | 0.811695 | $7 \cdot 2^{31}$ | 7 |
| 4 | 1491592101 | 0.694577 | $-3 \cdot 2^{31}$ | $-3$ |
| 5 | 1851566831 | 0.862203 | $4 \cdot 2^{31}$ | 4 |
| 6 | 1980039373 | 0.922028 | $2 \cdot 2^{31}$ | 2 |
| 7 | 1658585703 | 0.772339 | $3 \cdot 2^{31}$ | 3 |
| 8 | 721094453 | 0.335786 | $4 \cdot 2^{31}$ | 4 |

Each value in the fourth column is an exact multiple of $2^{31}$. Over the first $10^5$ outputs from this seed, the plane index takes each of the 15 values $-5, -4, \ldots, 9$, and no other value. From the seed 1 the states are $65539, 393225, 1769499, 7077969, \ldots$: they are the powers $3^i$ plus multiples of $2^{16}$ until they wrap, so a small seed also gives small first outputs.

## Correctness

The generator is correct when it computes $f(x) = 65539 x \bmod 2^{31}$; line L1 does this because $65539 x = 2^{16} x + 2x + x$. The interesting claims are about its structure. Three statements are proved below:

1. **The plane identity.** $a^2 \equiv 6a - 9 \pmod{2^{31}}$, so $x_{i+2} \equiv 6 x_{i+1} - 9 x_i$ and $9 u_i - 6 u_{i+1} + u_{i+2}$ is an integer.
2. **Fifteen planes.** That integer lies in $\{-5, \ldots, 9\}$, so the points $(u_i, u_{i+1}, u_{i+2})$ lie on 15 parallel planes $9x - 6y + z = j$.
3. **The period.** For an odd seed, the period is exactly $2^{29}$, the largest possible for a multiplicative generator modulo $2^{31}$.

The proofs are in the proof file below. The planes are $1/\sqrt{118} \approx 0.092$ apart, since the normal vector $(9, -6, 1)$ has length $\sqrt{118}$; in the language of the [spectral test](/spectral-test/), $\nu_3 \le \sqrt{118}$, while a good 31-bit generator has $\nu_3$ near $2^{31/3} \approx 1290$.

## Complexity

Each output costs one shift, two additions and one mask, so $\Theta(1)$ word operations. The state is one word. This speed was the reason for the multiplier: on the machines of the 1960s, a multiplication was much slower than a shift.

## Properties

- **Period $2^{29}$.** Only odd states occur, and each odd seed lies on a cycle of length $2^{29}$. The odd numbers below $2^{31}$ split into 2 cycles.
- **Weak low bits.** The lowest bit is always 1. In general, for $k \ge 3$, $x_i \bmod 2^k$ has period at most $2^{k-2}$, so the low bits repeat fast. This is true of every generator modulo a power of 2.
- **Fifteen planes in three dimensions.** Proved above. This fails any test of triples, for example a test of the distribution of points in small cubes.
- **Empirical results.** RANDU fails tests of the SmallCrush battery of TestU01 (L'Ecuyer and Simard 2007). This is an empirical statement, and it is not needed: the plane identity is a proof that RANDU is bad in three dimensions.

## Variants and improvements

- **A better multiplier modulo $2^{31}$.** A multiplier $a \equiv 5 \pmod 8$ chosen by the [spectral test](/spectral-test/) gives the same period with far better planes.
- **A prime modulus.** The [Park-Miller minimal standard](/park-miller-minimal-standard/) uses $m = 2^{31} - 1$ and $a = 16807$, with period $2^{31} - 2$ and no weak low bits.
- **An increment.** A mixed LCG with odd $c$ and $a \equiv 1 \pmod 4$ has period $2^{31}$ by the [Hull-Dobell theorem](/hull-dobell-theorem/), but a multiplier close to a power of 2 still gives few planes.

## When to use it

Never use RANDU in new work. Use it only to reproduce results of old programs, to teach the lattice structure of congruential generators, or as a known-bad input when you test a [battery of statistical tests](/statistical-tests-for-randomness/). Results of simulations from the 1960s and 1970s that used RANDU in three or more dimensions are suspect.

## Pitfalls

- **Choosing a multiplier for speed.** A multiplier of the form $2^k + \epsilon$ with small $\epsilon$ makes $a^2 - 2\epsilon a + \epsilon^2 = 2^{2k}$, which vanishes modulo $2^{31}$ when $2k \ge 31$. Any such multiplier puts triples on few planes. Choose the multiplier by the spectral test instead.
- **An even seed.** Line L1 keeps the power of 2 in $x$. An even seed gives a shorter period, and the seed 0 gives the constant 0. Accept only odd seeds.
- **Judging by one dimension.** RANDU passes simple tests of the distribution of single values. Its defect shows only in tests of triples, so test a generator in several dimensions.

## Implementations

## History

IBM distributed RANDU in the 1960s, in the Scientific Subroutine Package of the System/360, and it was copied to many other systems. Marsaglia (1968) proved that the $t$-tuples of every multiplicative congruential generator lie on a limited number of hyperplanes, and RANDU became the main example of the effect. Knuth's Section 3.3.4 uses it as the example of a bad multiplier.

## References
