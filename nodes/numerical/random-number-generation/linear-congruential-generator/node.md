---
tag: GFMHDY
kind: algorithm
slug: linear-congruential-generator
name: Linear congruential generator
aliases:
- LCG
- mixed congruential generator
- Lehmer generator
area: numerical/random-number-generation
level: intro
summary: Generates s_(i+1) = (a s_i + c) mod m and outputs s_i / m, the classic simple pseudorandom number generator.
model: word-ram
complexity:
  vars: {n: the number of outputs, m: the modulus, w: the word size}
  time: {worst: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, cryptographic: false}
history:
  year: 1949
  people: [D. H. Lehmer]
  note: Lehmer proposed the multiplicative congruential method at a symposium at Harvard in 1949.
prereqs: [congruence, generator-period]
see_also: [hull-dobell-theorem, marsaglia-hyperplane-theorem, spectral-test, park-miller-minimal-standard, randu, multiple-recursive-generator, jump-ahead, pcg-random]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.2.1 (the linear congruential method), Section 3.2.1.1 (choice of modulus), Section 3.2.1.2 (choice of multiplier, Theorem A on full period and the case c = 0), Section 3.2.1.3 (potency) and Section 3.3.4 (the spectral test)
  - paper: doi:10.1145/63039.63042
    title: Stephen K. Park and Keith W. Miller, Random number generators, good ones are hard to find, Communications of the ACM 31(10), 1988
    locator: the minimal standard generator with m = 2^31 - 1 and a = 16807, Schrage's method, and the check value 1043618065 after 10000 steps from seed 1
  - paper: "Pierre L'Ecuyer, Tables of linear congruential generators of different sizes and good lattice structure, Mathematics of Computation 68(225), 1999, pages 249 to 260"
    locator: the tables of multipliers selected by the spectral test for prime moduli and for powers of two
  - paper: "T. E. Hull and A. R. Dobell, Random number generators, SIAM Review 4(3), 1962, pages 230 to 254"
    locator: the theorem on the conditions for full period of the mixed congruential method
  - paper: "Alan M. Frieze, Johan Hastad, Ravi Kannan, Jeffrey C. Lagarias and Adi Shamir, Reconstructing truncated integer variables satisfying linear congruences, SIAM Journal on Computing 17(2), 1988"
    locator: the lattice reduction attack that recovers the state of a linear congruential generator from truncated outputs
---

A linear congruential generator (LCG) is a [pseudorandom number generator](/pseudorandom-number-generator/) whose state is one integer $s$ modulo $m$, updated by $s \leftarrow (a s + c) \bmod m$. It costs one multiplication and one addition per output, and its [period](/generator-period/) is known exactly from number theory: it is $m$ under the conditions of the [Hull-Dobell theorem](/hull-dobell-theorem/). Its weakness is also known exactly: consecutive outputs lie on a small number of parallel hyperplanes ([Marsaglia's theorem](/marsaglia-hyperplane-theorem/)), and its low-order bits have short periods when $m$ is a power of two.

## In plain words

Keep one whole number as the state. To get the next number, multiply the state by a fixed number, add another fixed number, and keep only the remainder after division by a third fixed number. The remainder becomes the new state and is also the output. Divide it by the third number to get a fraction between 0 and 1.

Because the state can take only a limited number of values, the numbers repeat in a cycle. With well-chosen constants the cycle passes through every possible value once. The outputs then look random to many simple checks, but they are not: they follow a rigid pattern that shows up when you plot pairs or triples of outputs.

## The problem

A generator is a tuple $(S, f, g, s_0)$ in the notation of the random-number-generation pages: a finite state space $S$, a transition $f$ with $s_{i+1} = f(s_i)$, an output function $g$ with $u_i = g(s_i)$, and a seed $s_0$. The goal is a sequence $u_1, u_2, \ldots$ in $[0, 1)$ that looks like independent draws from the uniform distribution $U(0, 1)$, at low cost per output. The LCG takes

$$S = \{0, 1, \ldots, m - 1\}, \qquad f(s) = (a s + c) \bmod m, \qquad g(s) = s / m,$$

with modulus $m \ge 2$, multiplier $0 < a < m$ and increment $0 \le c < m$. The case $c = 0$ is the *multiplicative* (Lehmer) generator, and the case $c \ne 0$ is the *mixed* generator. The cost model counts word operations per output on a [word RAM](/word-ram/) with word size $w$.

## The algorithm

```pseudo id=main
LCG-SEED(x)                               ▷ the parameters m, a, c are fixed
L1  s ← x mod m
L2  if c = 0 and s = 0 then error          ▷ 0 is a fixed point of s ↦ a s mod m

LCG-NEXT()
L3  s ← (a · s + c) mod m
L4  return s

LCG-UNIFORM()
L5  return LCG-NEXT() / m                 ▷ a value in [0, 1)

SCHRAGE(a, x)                             ▷ a · x mod m, needs q = ⌊m/a⌋, r = m mod a, r < q
L6  t ← a · (x mod q) − r · ⌊x / q⌋
L7  if t < 0 then t ← t + m
L8  return t
```

When $m = 2^w$, line L3 is a multiplication and an addition in unsigned $w$-bit arithmetic, which drops the carry out of the word for free. When $m$ is a prime such as $2^{31} - 1$, the product $a s$ needs about $2w$ bits; SCHRAGE computes $a s \bmod m$ for $c = 0$ with every intermediate value in $(-m, m)$, so it runs in signed $w$-bit arithmetic. For $m = 2^{64}$ and binary64 output, line L5 must use the top 53 bits: the quotient $s / 2^{64}$ of a large $s$ rounds up to 1.0.

## Example

Take $m = 16$, $a = 5$, $c = 3$ and seed 7.

| $i$ | $s_i$ | $5 s_i + 3$ | $s_{i+1}$ | $u_{i+1} = s_{i+1}/16$ |
|---|---|---|---|---|
| 0 | 7 | 38 | 6 | 0.375 |
| 1 | 6 | 33 | 1 | 0.0625 |
| 2 | 1 | 8 | 8 | 0.5 |
| 3 | 8 | 43 | 11 | 0.6875 |
| 4 | 11 | 58 | 10 | 0.625 |

From seed 0 the same generator gives $3, 2, 13, 4, 7, 6, 1, 8, 11, 10, 5, 12, 15, 14, 9, 0$ and then repeats, so its period is 16: every state appears once. The Hull-Dobell conditions hold: $\gcd(3, 16) = 1$, 2 divides $a - 1 = 4$, and 4 divides $a - 1$. The low bit of these states alternates $1, 0, 1, 0, \ldots$, a first sign of the weak low bits.

**Reference values.** The minimal standard of Park and Miller, $m = 2^{31} - 1$, $a = 16807$, $c = 0$, from seed 1 reaches $s_{10000} = 1043618065$; the C++ standard requires the same value of `minstd_rand0`, and the value 399268537 for `minstd_rand`, which uses $a = 48271$. The generator of Numerical Recipes, $m = 2^{32}$, $a = 1664525$, $c = 1013904223$, from seed 0 gives $1013904223, 1196435762, 3519870697, 2868466484, \ldots$

## Correctness

The procedures compute the recurrence exactly, and by induction the state after $i$ calls is $s_i$. Unrolling the recurrence gives the closed form $s_n \equiv a^n s_0 + c\,(1 + a + \cdots + a^{n-1}) \pmod m$, which is the base of [jump-ahead](/jump-ahead/). Schrage's method is exact when $r < q$: writing $x = qk + j$ gives $a x = (m - r) k + a j \equiv a j - r k$, and both $a j$ and $r k$ lie in $[0, m)$. The full proofs, with the masking step for $m = 2^w$ and the bound that keeps LCG-UNIFORM below 1, are below.

**Period.** These results are proved; the hypotheses are exact.

- *Mixed generator* (Knuth, Section 3.2.1.2, Theorem A; Hull and Dobell 1962). The period is $m$ for every seed if and only if (i) $\gcd(c, m) = 1$, (ii) every prime that divides $m$ divides $a - 1$, and (iii) 4 divides $a - 1$ if 4 divides $m$. See the [Hull-Dobell theorem](/hull-dobell-theorem/).
- *Multiplicative generator, $m$ prime.* The period from each seed in $1, \ldots, m-1$ equals the [multiplicative order](/multiplicative-order/) of $a$ modulo $m$, and it is $m - 1$ exactly when $a$ is a [primitive root](/primitive-root/) modulo $m$. The value 16807 is a primitive root modulo $2^{31} - 1$.
- *Multiplicative generator, $m = 2^w$ with $w \ge 3$.* The period is at most $2^{w-2}$. For $w \ge 4$ it equals $2^{w-2}$ exactly when $a \equiv 3$ or $5 \pmod 8$ and the seed is odd (Knuth, Section 3.2.1.2). For $w = 3$ the bound is 2, and $a = 7$ also reaches it. For example $m = 2^{10}$, $a = 5$ gives period 256 from seed 1 and 128 from seed 2.

## Complexity

- **Time.** LCG-NEXT does one multiplication, one addition and one reduction: $\Theta(1)$ word operations per output when $m \le 2^w$. For $m = 2^w$ the reduction is free. For a prime $m$ it is a division, Schrage's two divisions, or a shift-and-add trick for a Mersenne prime $m = 2^k - 1$, using $(x \bmod 2^k) + \lfloor x / 2^k \rfloor \equiv x \pmod{2^k - 1}$.
- **Space.** One word of state.
- **Jump-ahead.** The state $n$ steps ahead costs $O(\log n)$ multiplications modulo $m$ by the closed form and repeated squaring. See [jump-ahead](/jump-ahead/).

## Properties

- **Lattice structure (proved).** For each $d$, the points $(u_i, \ldots, u_{i+d-1})$ over a full period lie on a shifted lattice, and they lie on at most $(d!\, m)^{1/d}$ parallel hyperplanes. This is [Marsaglia's theorem](/marsaglia-hyperplane-theorem/). The [spectral test](/spectral-test/) measures the largest distance between such hyperplanes, and good multipliers are chosen to make it small for $d$ from 2 to 8 (L'Ecuyer 1999).
- **Weak low bits (proved).** If $m = 2^w$ and the period is full, bit $j$ of the state (bit 0 is the lowest) has period $2^{j+1}$, because the low $j+1$ bits are themselves an LCG modulo $2^{j+1}$. The lowest bit alternates.
- **Empirical quality.** LCGs with $m \le 2^{64}$ fail tests of the TestU01 batteries Crush and BigCrush (L'Ecuyer and Simard 2007). This is an empirical finding about named parameter sets, not a theorem.
- **Not cryptographic.** Each output of the plain generator is the full state, so the next output follows at once. Even when only the top bits are output, the state can be recovered from a few outputs by [lattice reduction](/lll-algorithm/) (Frieze, Hastad, Kannan, Lagarias and Shamir 1988). Never use an LCG for keys or tokens.

## Variants and improvements

- **Park-Miller minimal standard.** $m = 2^{31} - 1$, $a = 16807$ (later 48271), $c = 0$. See [the Park-Miller generator](/park-miller-minimal-standard/).
- **Power-of-two LCG with a better output.** [PCG](/pcg-random/) keeps a 64-bit or 128-bit LCG state and applies a permutation to the output, which hides the weak low bits.
- **Combined and higher-order generators.** A [multiple recursive generator](/multiple-recursive-generator/) uses $s_i = (a_1 s_{i-1} + \cdots + a_k s_{i-k}) \bmod m$, and [L'Ecuyer's combined generators](/lecuyer-combined-generator/) add several of them to get a long period and a better lattice.
- **Multiply-with-carry.** [Multiply-with-carry](/multiply-with-carry/) generators are equivalent to multiplicative LCGs with a large modulus of the form $a b^r - 1$, but they run on words of base $b$.

## When to use it

Use an LCG when the state must be one word, when you need exact and cheap jump-ahead, or in teaching and in tests where you need a known sequence. For simulation, prefer a generator with a good lattice and a long period, or an LCG with a strong output permutation. For anything an adversary can see, use a [cryptographically secure generator](/cryptographically-secure-prng/).

## Pitfalls

- **Bad multipliers.** [RANDU](/randu/), $m = 2^{31}$, $a = 65539$, $c = 0$, satisfies $s_{i+2} \equiv 6 s_{i+1} - 9 s_i \pmod{2^{31}}$ because $a^2 = 6a - 9 \pmod{2^{31}}$, so its triples lie on only 15 planes in the unit cube.
- **Low bits as a small random number.** `x % n` with $n = 2^k$ takes the $k$ lowest bits, which have period $2^k$. Use the high bits, for example $\lfloor n x / m \rfloor$, and handle [modulo bias](/modulo-bias/).
- **Seed 0 with $c = 0$.** The state stays 0 forever. An even seed with $m = 2^w$ and $c = 0$ shortens the period.
- **Overflow.** In C, `a * s` overflows a 32-bit `int` for $m = 2^{31} - 1$; use Schrage's method or a 64-bit product. Signed overflow is undefined behaviour in C, so use unsigned types for $m = 2^w$.
- **Rounding to 1.0.** For $m = 2^{64}$, `(double) s / 2^64` can return 1.0. Use the top 53 bits times $2^{-53}$.
- **Too short a period.** $m = 2^{32}$ is exhausted in seconds on current hardware; and the lattice becomes visible well before the period ends.

## Implementations

## History

D. H. Lehmer proposed the multiplicative congruential method in a talk at a symposium at Harvard in 1949, published in 1951. Knuth (Section 3.2.1) credits the mixed method with $c \ne 0$ to W. E. Thomson (1958) and A. Rotenberg (1960). Hull and Dobell (1962) proved the conditions for full period of the mixed method. Marsaglia (1968) showed the hyperplane structure, and Park and Miller (1988) proposed the minimal standard with a portable implementation by Schrage's method.

## References
