---
tag: X19VXC
kind: algorithm
slug: lucas-lehmer-test
name: Lucas-Lehmer test
aliases:
- Lucas-Lehmer primality test
area: number-theory/primality
level: core
summary: Deterministic test for Mersenne numbers 2^p - 1. Starting from s = 4, it squares and subtracts 2 modulo 2^p - 1, p - 2 times; the number is prime exactly when the result is 0.
solves: [primality-testing]
model: multitape-turing-machine
complexity:
  vars: {p: the exponent of the Mersenne number 2^p - 1}
  time: {worst: O(p^3), best: O(1)}
  space: {extra: O(p)}
properties: {deterministic: true, recursive: false, certifying: false}
history:
  year: 1930
  people: [Édouard Lucas, Derrick Henry Lehmer]
  note: Lucas gave the test in 1876 and 1878 with a different starting value and a proof of one direction; Lehmer gave the form with s = 4 and a full proof in 1930.
prereqs: [mersenne-prime, quadratic-reciprocity, multiplicative-order, modular-exponentiation]
see_also: [mersenne-prime, lucas-primality-test, pepin-test, proth-test, miller-rabin, fermat-prime, primality-testing, schonhage-strassen-multiplication]
sources:
  - paper: doi:10.2307/1968235
    title: D. H. Lehmer, An extended theory of Lucas' functions, Annals of Mathematics 31 (1930)
    locator: pages 419 to 448 (the test for 2^p - 1 with s_0 = 4)
  - paper: doi:10.2307/2369308
    title: Édouard Lucas, Théorie des fonctions numériques simplement périodiques, American Journal of Mathematics 1 (1878)
    locator: pages 184 to 240 and 289 to 321
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 4.2.1, the Lucas-Lehmer test for Mersenne primes, with its proof
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.5.4, Factoring into primes (the Lucas-Lehmer test and its exercises)
  - url: https://www.mersenne.org/primes/
    title: Great Internet Mersenne Prime Search, List of known Mersenne prime numbers
    locator: the table of the 52 known Mersenne primes and the dates of discovery
---

The Lucas-Lehmer test decides whether a Mersenne number $M_p = 2^p - 1$ is [prime](/prime-number/). It starts from $s_0 = 4$, computes $s_{i+1} = s_i^2 - 2 \bmod M_p$, and declares $M_p$ prime exactly when $s_{p-2} \equiv 0$. The test is deterministic and always right, and it costs $p - 2$ squarings modulo $M_p$, about as much as one round of [Miller-Rabin](/miller-rabin/) on a number of the same size. Because no test of similar speed is known for general numbers, the largest known primes are [Mersenne primes](/mersenne-prime/) found with this test.

## In plain words

Mersenne numbers are one less than a power of two, such as 7, 31 and 127. To test one, start with the number four. Square it, subtract two, and keep only the remainder after division by the Mersenne number. Repeat this a fixed number of times, two fewer than the power of two used. If the final remainder is zero, the Mersenne number is prime; otherwise it is not.

Each step is one squaring, and the division by a Mersenne number is cheap, because it only needs to cut the binary digits into blocks and add them. That is why computers can test numbers with millions of digits this way.

## The problem

The input is an integer $p \ge 2$. The output is true if $M_p = 2^p - 1$ is prime and false otherwise. The answer is always right. Only Mersenne numbers can be tested, which is the price of the speed. The test is usually run only for prime $p$, because $M_p$ is composite when $p$ is composite; but it gives the right answer for every $p \ge 2$.

**Cost model.** The integers are of arbitrary precision. The number tested, $M_p$, has $p$ binary digits, so $p = \Theta(\log M_p)$. Costs are in bit operations, as on a [multitape Turing machine](/multitape-turing-machine/), and $M(p)$ is the cost of one product of two $p$-digit integers: $O(p^2)$ for [schoolbook multiplication](/schoolbook-multiplication/), $O(p \log p)$ for [Harvey and van der Hoeven](/harvey-van-der-hoeven-multiplication/).

## The algorithm

```pseudo id=main
LUCAS-LEHMER(p)                             ▷ true exactly when 2^p − 1 is prime
L1  if p = 2 then return true               ▷ M_2 = 3
L2  M ← 2^p − 1
L3  s ← 4
L4  for i ← 1 to p − 2 do
L5      s ← (s² − 2) mod M
L6  return s = 0
```

Line L1 handles $p = 2$, where the loop would not run and $4 \bmod 3 \ne 0$. After the $i$-th pass of line L5, $s \equiv s_i \pmod M$, where $s_0 = 4$ and $s_{i+1} = s_i^2 - 2$. Line L6 checks $s_{p-2} \equiv 0 \pmod{M_p}$.

**Reduction modulo $M_p$.** Since $2^p \equiv 1 \pmod{M_p}$, a number $x = x_1 2^p + x_0$ with $0 \le x_0 < 2^p$ satisfies $x \equiv x_1 + x_0$. So reducing the square in line L5 needs a shift, a mask and an addition, repeated until the value is at most $M_p$, with $M_p$ itself mapped to 0. The subtraction of 2 is done before the reduction, as $s^2 + M - 2$, to keep the value non-negative.

**Where the numbers come from.** Let $\omega = 2 + \sqrt 3$ and $\bar\omega = 2 - \sqrt 3$, so $\omega \bar\omega = 1$. Then $s_i = \omega^{2^i} + \bar\omega^{2^i}$, because $s_0 = 4$ and $(\omega^{2^i} + \bar\omega^{2^i})^2 - 2 = \omega^{2^{i+1}} + \bar\omega^{2^{i+1}}$. The test checks whether $\omega^{2^{p-1}} \equiv -1$ modulo $M_p$ in the ring of numbers $a + b\sqrt 3$. This is a Fermat-like condition in a quadratic extension: it holds when $M_p$ is prime, and its truth forces $\omega$ to have order $2^p$, which is too large for any prime factor of a composite $M_p$.

## Example

**$p = 7$, $M_7 = 127$.** The loop runs $p - 2 = 5$ times.

| $i$ | $s_{i-1}^2 - 2$ | $s_i \bmod 127$ |
|---|---|---|
| 0 | | $4$ |
| 1 | $14$ | $14$ |
| 2 | $194$ | $67$ |
| 3 | $4487$ | $42$ |
| 4 | $1762$ | $111$ |
| 5 | $12319$ | $0$ |

So $s_5 \equiv 0$ and $127$ is prime. The reduction of $4487$ by blocks: $4487 = 35 \cdot 128 + 7$, so $4487 \equiv 35 + 7 = 42 \pmod{127}$.

**$p = 11$, $M_{11} = 2047 = 23 \cdot 89$.** The values are $4, 14, 194, 788, 701, 119, 1877, 240, 282, 1736$, and $s_9 = 1736 \ne 0$. So 2047 is composite. The test does not give the factors.

## Correctness

**Theorem (Lucas, Lehmer).** For each integer $p \ge 2$, LUCAS-LEHMER$(p)$ returns true if and only if $2^p - 1$ is prime.

*If $s_{p-2} \equiv 0$, then $M_p$ is prime.* Suppose $p \ge 3$ and $M_p$ is composite, and let $q$ be its smallest prime factor, so $q^2 \le M_p$ and $q$ is odd. In the ring $\mathbb{Z}_q[\sqrt 3] = \mathbb{Z}_q[x]/(x^2 - 3)$, which has $q^2$ elements, $s_{p-2} \equiv 0$ means $\omega^{2^{p-2}} = -\bar\omega^{2^{p-2}}$, and multiplying by $\omega^{2^{p-2}}$ gives $\omega^{2^{p-1}} = -1$. So $\omega$ is a unit of order exactly $2^p$. The units of the ring number at most $q^2 - 1 < M_p < 2^p$, a contradiction.

*If $M_p$ is prime, then $s_{p-2} \equiv 0$.* Let $q = M_p$ with $p \ge 3$. Then $p$ is prime, $q \equiv 7 \pmod 8$ and $q \equiv 1 \pmod 3$. So 2 is a [quadratic residue](/quadratic-residue/) modulo $q$, and by [quadratic reciprocity](/quadratic-reciprocity/) 3 is not. Hence $\mathbb{Z}_q[\sqrt 3]$ is a field in which $(a + b\sqrt 3)^q = a - b\sqrt 3$. With $\tau = 1 + \sqrt 3$, $\tau^2 = 2\omega$ and $\tau^{q+1} = \tau \bar\tau = -2$, so $\omega^{(q+1)/2} = \tau^{q+1} / 2^{(q+1)/2} = -2 / (2 \cdot 2^{(q-1)/2}) = -1$, because $2^{(q-1)/2} \equiv 1$ by [Euler's criterion](/euler-criterion/). Since $(q+1)/2 = 2^{p-1}$, this is $\omega^{2^{p-1}} = -1$, and so $s_{p-2} = \omega^{2^{p-2}} + \bar\omega^{2^{p-2}} = \bar\omega^{2^{p-2}}(\omega^{2^{p-1}} + 1) = 0$.

The full proof is in the proofs.

## Complexity

**Time.** The loop runs $p - 2$ times. Each pass squares a number below $M_p$, of $p$ binary digits, and reduces a number of at most $2p$ digits with two or three shift-and-add steps of $O(p)$ bit operations. So the test costs $O(p \, M(p))$ bit operations: $O(p^3)$ with schoolbook multiplication, $O(p^2 \log p)$ with the Harvey and van der Hoeven bound. In terms of $N = M_p$, this is $O((\log N)^3)$ with schoolbook arithmetic, the cost of a single Miller-Rabin round on a general number of the same size. The best case is $p = 2$, in $O(1)$.

**Space.** The value $s$ and the square need $O(p)$ binary digits.

**In practice.** For $p$ in the tens of millions, the squarings use [fast Fourier transform](/fast-fourier-transform/) multiplication, and the reduction modulo $2^p - 1$ is folded into the transform as a cyclic convolution (the irrational base discrete weighted transform of Crandall and Fagin), so no separate reduction is needed. A Lucas-Lehmer test of $M_{136279841}$ needs about $1.4 \cdot 10^8$ squarings of numbers with $41$ million decimal digits.

## Properties

- **Deterministic and exact.** No randomness and no error, unlike [Miller-Rabin](/miller-rabin/).
- **Special purpose.** It applies only to numbers $2^p - 1$. The [Lucas primality test](/lucas-primality-test/) and [Pépin's test](/pepin-test/) are tests of the same kind for other special forms.
- **Not certifying in the usual sense.** The final residue 0 is not a short certificate: to check it, one has to repeat the $p - 2$ squarings. A nonzero result proves $M_p$ composite but gives no factor.
- **An $N + 1$ test.** $M_p + 1 = 2^p$ is completely factored, and the test is the special case of the Lucas $N + 1$ test, in which a Lucas sequence plays the part that powers play in the $N - 1$ tests.

## Variants and improvements

- **Other starting values.** $s_0 = 10$ works as well, and so does $s_0 = 2 \cdot 3^{-1} \bmod M_p$; each gives the same answers for every odd prime $p$. Lucas stated his criteria in other forms.
- **Lucas-Lehmer-Riesel test.** For $N = h \cdot 2^n - 1$ with $h < 2^n$, a starting value that depends on $h$ gives a test of the same speed.
- **Trial factoring first.** Each prime factor of $M_p$ has the form $2kp + 1$ with $q \equiv \pm 1 \pmod 8$ (see [Mersenne prime](/mersenne-prime/)). Searches such as GIMPS first look for small factors of this form, and then run the much more costly full test only on the survivors.
- **Probable prime test with a proof.** GIMPS now runs a Fermat test with base 3 for first-time tests, which can be checked with a short proof, and confirms a new Mersenne prime with the Lucas-Lehmer test.
- **Error checks.** Long runs on consumer hardware use checksums on the squarings and compare the final 64 binary digits of $s_{p-2}$ (the residue) between independent runs.

## When to use it

Use the Lucas-Lehmer test to decide primality of a Mersenne number $2^p - 1$, and nothing else; there it beats every general test. Before running it, check that $p$ is prime, and search for small factors $2kp + 1$, which removes most candidates cheaply. For a general number use [Miller-Rabin](/miller-rabin/), or a proving method such as [ECPP](/ecpp/). For Fermat numbers use [Pépin's test](/pepin-test/), and for $k \cdot 2^n + 1$ the [Proth test](/proth-test/).

## Pitfalls

- **The case $p = 2$.** The loop runs zero times and $4 \bmod 3 = 1$, so $M_2 = 3$ needs its own line.
- **Negative values.** After the reduction, $s$ can be 0 or 1, and $s^2 - 2$ is then negative. Add $M_p$ first, or use a reduction that handles negative numbers.
- **The value $M_p$ itself.** The shift-and-add reduction can end at $M_p$, which is 0 modulo $M_p$. Map it to 0, or the final check fails for a prime.
- **Wrong loop count.** The loop runs $p - 2$ times, not $p - 1$ or $p$. With $p - 1$ passes a prime gives $s_{p-1} \equiv -2$, not 0.
- **Hardware errors.** A run of weeks on a home computer can suffer a bit flip. Large searches double-check each result.

## Implementations

## History

Édouard Lucas studied the sequences now named after him in 1876 to 1878, and used them to prove in 1876 that $M_{127}$ is prime, by hand. That record stood until 1951. Derrick Henry Lehmer gave the test its present form, with $s_0 = 4$ and a proof in both directions, in his 1930 paper. In 1952 Raphael Robinson ran the test on the SWAC computer and found $M_{521}$, $M_{607}$, $M_{1279}$, $M_{2203}$ and $M_{2281}$. Since 1996 the Great Internet Mersenne Prime Search has found each new Mersenne prime, the latest being $M_{136279841}$ in October 2024.

## References
