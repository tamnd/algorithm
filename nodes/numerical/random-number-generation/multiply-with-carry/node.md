---
tag: D46KH3
kind: algorithm
slug: multiply-with-carry
name: Multiply-with-carry generator
aliases:
- MWC
- multiply-with-carry
- complementary multiply-with-carry
- CMWC
area: numerical/random-number-generation
level: advanced
summary: A generator that carries high bits of a multiplication into the next state, with a long period.
model: word-ram
complexity:
  vars: {r: "the lag, 1 for the basic generator", b: "the base, usually 2^32"}
  time: {worst: Θ(1)}
  space: {extra: Θ(r)}
properties: {deterministic: true, in_place: true, recursive: false}
prereqs: [linear-congruential-generator, multiplicative-order, safe-prime]
see_also: [lagged-fibonacci-generator, ranlux, multiple-recursive-generator, jump-ahead, quadratic-residue, xorshift, spectral-test, statistical-tests-for-randomness]
sources:
  - paper: "George Marsaglia, Random number generators, Journal of Modern Applied Statistical Methods 2(1), 2003, pages 2 to 13"
    title: George Marsaglia, Random number generators, Journal of Modern Applied Statistical Methods 2(1), 2003
    locator: the multiply-with-carry and complementary multiply-with-carry generators, the choice of a with a b^r - 1 a safe prime, and the code of CMWC4096
  - paper: doi:10.1090/S0025-5718-97-00827-2
    title: Raymond Couture and Pierre L'Ecuyer, Distribution properties of multiply-with-carry random number generators, Mathematics of Computation 66(218), 1997, pages 591 to 607
    locator: the equivalence of a lag-r MWC with a multiplicative LCG modulo a b^r - 1 whose multiplier is the inverse of b, the period as the order of b, and the lattice structure of the outputs
  - paper: doi:10.1214/aoap/1177005878
    title: George Marsaglia and Arif Zaman, A new class of random number generators, Annals of Applied Probability 1(3), 1991, pages 462 to 480
    locator: the add-with-carry and subtract-with-borrow generators, the carry idea that multiply-with-carry extends
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.2.1.2, the period of the multiplicative congruential method x_(n+1) = a x_n mod m as the order of a modulo m
---

A multiply-with-carry (MWC) generator in base $b$ keeps a value $x$ and a carry $c$. Each step computes $t = a x + c$, keeps the low digit $t \bmod b$ as the new value and output, and carries the high digit $\lfloor t / b \rfloor$ into the next step. With $b = 2^{32}$ this is one 64-bit multiply-add and a split into halves. George Marsaglia proposed it in the 1990s. The carry turns a weak recurrence into one with a clean theory: the generator is exactly a multiplicative [linear congruential generator](/linear-congruential-generator/) modulo the large number $m = a b - 1$ with multiplier $a$, so its period is the [multiplicative order](/multiplicative-order/) of $b$ modulo $m$. Choosing $m$ as a [safe prime](/safe-prime/) gives a period of $(m - 1)/2$.

## In plain words

Multiply the current number by a fixed constant and add a small leftover from the previous step. The result has two halves. The lower half is the next random number. The upper half is the leftover for the next time, like the carry digit when you multiply by hand.

Without the carry, the low half alone would be a poor generator. With it, the pair of number and leftover behaves exactly like a simple, well-understood generator working with a much larger number. That gives a long cycle whose length can be computed in advance, and it costs one multiplication and one addition per number.

## The problem

We use the notation of the [pseudorandom number generator](/pseudorandom-number-generator/) page with the base $b = 2^w$. The task is a generator with a period far longer than $b$, a few word operations per output, and a provable period. The state space is $S = \{(x, c) : 0 \le x < b, 0 \le c < a\}$, the transition $f$ is the step below, and the output function is $g(x, c) = x$.

## The algorithm

Choose $a$ with $m = a b - 1$ prime, ideally a safe prime, and seed $(x, c)$ with $0 < a x + c < m$, which rules out the two fixed states $(0, 0)$ and $(b - 1, a - 1)$.

```pseudo id=main
MWC-NEXT(x, c)                ▷ 0 ≤ x < b, 0 ≤ c < a, a and b fixed
L1  t ← a · x + c             ▷ t ≤ a b − 1, fits in 2w bits
L2  x ← t mod b               ▷ the low digit: the new value and the output
L3  c ← ⌊t / b⌋               ▷ the high digit: the new carry, again below a
L4  return (x, c)
```

With $b = 2^{32}$ and the state packed in one 64-bit word $s = c \cdot 2^{32} + x$, the step is the single line $s \leftarrow a \cdot (s \bmod 2^{32}) + \lfloor s / 2^{32} \rfloor$, and the output is the low 32 bits of $s$.

**Lag $r$.** The lag-$r$ generator keeps $x_{n-r}, \ldots, x_{n-1}$ and one carry, and computes $t = a x_{n-r} + c_{n-1}$, $x_n = t \bmod b$, $c_n = \lfloor t / b \rfloor$. It corresponds to the modulus $m = a b^r - 1$, so with a small $a$ and a large $r$ the period is huge while each step still costs one multiply-add.

## Example

Take the toy base $b = 8$ and $a = 3$, so $m = 3 \cdot 8 - 1 = 23$, a prime. Start from $(x, c) = (1, 0)$, which corresponds to $z = a x + c = 3$.

| $n$ | $t = 3x + c$ | $x$ (output) | $c$ | $z = 3x + c$ | $3^n \cdot 3 \bmod 23$ |
|---|---|---|---|---|---|
| 0 | | 1 | 0 | 3 | 3 |
| 1 | 3 | 3 | 0 | 9 | 9 |
| 2 | 9 | 1 | 1 | 4 | 4 |
| 3 | 4 | 4 | 0 | 12 | 12 |
| 4 | 12 | 4 | 1 | 13 | 13 |
| 5 | 13 | 5 | 1 | 16 | 16 |

The column $z$ is the LCG $z \leftarrow 3 z \bmod 23$, as the theorem below says. The order of 8 modulo 23 is 11, since $8 = 10^2 \bmod 23$ is a [quadratic residue](/quadratic-residue/) and $(23 - 1)/2 = 11$ is prime, so the generator has period 11, while its outputs are 3-bit numbers.

At full size, with $b = 2^{32}$, $a = 4294957665$ and the seed $x = 123456789$, $c = 362436$, the first outputs are $693968569, 3776248345, 1429218845, 44760066, 4136716891$, which the tests compare with a C implementation. Here $m = a \cdot 2^{32} - 1$ is a safe prime, so the period is $(m - 1)/2 = a \cdot 2^{31} - 1 \approx 2^{63}$.

## Correctness

Correctness here means that the step is well defined and has a known period. The full proof is in the proof file; the key facts are:

1. **The carry stays below $a$.** $t \le a(b - 1) + a - 1 = a b - 1$, so $\lfloor t / b \rfloor \le a - 1$.
2. **The step is an LCG in disguise.** Put $z = a x + c$, a bijection between states and $\{0, \ldots, m\}$. From $t = b c' + x'$ we get $b z' = a b x' + b c' = m x' + z$, so $z' \equiv b^{-1} z \equiv a z \pmod m$, because $a b \equiv 1$. Away from the two fixed states, $z' = a z \bmod m$ exactly, and the output is $x = \lfloor z / a \rfloor$.
3. **Period.** So the period from $z_0$ coprime to $m$ is the order of $a$, which equals the order of $b$, modulo $m$. For $b = 2^{32}$, $b$ is a square, so the order divides $(m - 1)/2$ when $m$ is prime; for a safe prime $m$ it equals $(m - 1)/2$.

The tests check the equivalence and the period on every state of every generator with $b \in \{8, 16, 32\}$, and check the safe-prime condition for the 64-bit multipliers with an exact Miller-Rabin test.

## Complexity

One step costs one multiplication, one addition and two word extractions: $\Theta(1)$ word operations, and a single 64-bit multiply-add for $b = 2^{32}$. The lag-$r$ version keeps $r$ words in a circular buffer, so its state is $\Theta(r)$ words while the step is still $\Theta(1)$. Jumping $k$ steps ahead costs $O(\log k)$ multiplications modulo $m$: $z_{n+k} = a^k z_n \bmod m$, by [binary exponentiation](/binary-exponentiation/).

## Properties

- **Period, proved:** the order of $b$ modulo $m = a b^r - 1$; for lag 1 with base $2^{32}$ and a safe prime $m$, exactly $(m - 1)/2 \approx a \cdot 2^{31}$.
- **Output uniformity.** If $b$ were a [primitive root](/primitive-root/) modulo a prime $m$, one period would run $z$ through all of $1, \ldots, m - 1$, and each output value would occur $a$ times, except 0 and $b - 1$, which occur $a - 1$ times. With $b = 2^{32}$ the cycle covers only the squares modulo $m$, half of them, so the counts are close to, but not exactly, equal.
- **Lattice structure.** By the equivalence, the [spectral test](/spectral-test/) of the LCG with multiplier $b^{-1} \bmod m$ describes the outputs, and Couture and L'Ecuyer (1997) studied it; a bad $a$ gives bad lattices like any LCG.
- **Empirical quality:** Marsaglia reports that his MWC and CMWC generators pass the Diehard tests. That is a measurement, not a proof; this page's tests only run a chi-square test on 20000 outputs. A lag-1 MWC with $b = 2^{32}$ has a period of only about $2^{63}$.
- **Not secure.** One full state, or a few outputs, determine all later values.

## Variants and improvements

- **Lag-$r$ MWC.** As above, with $m = a b^r - 1$. Marsaglia proposed lags up to 4096 with small multipliers, giving periods of tens of thousands of bits.
- **Complementary MWC (CMWC).** The new value is $(b - 1) - (t \bmod b)$ instead of $t \bmod b$, with modulus $m = a b^r + 1$. Marsaglia's CMWC4096 uses $b = 2^{32} - 1$, $r = 4096$ and $a = 18782$, with a period of more than $2^{131000}$ by his statement.
- **KISS.** Marsaglia's KISS generators combine an MWC (in the 1999 version, two 16-bit MWC generators with multipliers 36969 and 18000) with an LCG and a [xorshift](/xorshift/) generator.
- **Add-with-carry and subtract-with-borrow.** Marsaglia and Zaman's earlier generators use $a = 1$ and lagged additions; [RANLUX](/ranlux/) is built on subtract-with-borrow.
- **Generalizations.** Goresky and Klapper extended the theory of MWC to more general sequences with carry, and gave conditions for the maximal period.

## When to use it

Use an MWC generator when you want a tiny, fast generator with a provable period and only a multiply-add instruction, for example on small processors, in a GPU kernel or as a component of a combined generator such as KISS. A lag-1 MWC with 64-bit state gives a period of about $2^{63}$, enough for many uses but short for large simulations; for longer periods use a lag-$r$ MWC or CMWC, or a modern generator such as [xoshiro256**](/xoshiro-xoroshiro/) or [PCG](/pcg-random/). Never use it where outputs must be unpredictable; use a [cryptographically secure generator](/cryptographically-secure-prng/).

## Pitfalls

- **Bad seeds.** The states $(0, 0)$ and $(b - 1, a - 1)$ are fixed points, so the generator outputs one value forever. Seed with $0 < a x + c < m$, and keep $c < a$.
- **Overflow.** $a x + c$ needs $2w$ bits. With $b = 2^{32}$, use 64-bit unsigned arithmetic; in Python, mask the packed state to 64 bits.
- **Unchecked multipliers.** An arbitrary $a$ can give a composite $m$ or a small order of $b$, and a short period. Check that $m$ is prime and compute the order of $b$, or use a safe prime.
- **Period shorter than it looks.** With $b = 2^{32}$ the period is at most $(m - 1)/2$, not $m - 1$, because $b$ is a square modulo $m$.
- **Returning the whole word.** In the packed 64-bit form only the low half is the output. The high half is the carry, which is below $a$ and is not uniform on the 32-bit range; returning all 64 bits gives a biased value.

## Implementations

## History

Marsaglia and Zaman introduced add-with-carry and subtract-with-borrow generators in 1991. Marsaglia then proposed multiply-with-carry in the 1990s, posting it on newsgroups and including it in the KISS generators, and described the family with its complementary form in 2003. Couture and L'Ecuyer (1997) proved the equivalence with an LCG modulo $a b^r - 1$ and analysed the lattice structure, and Goresky and Klapper extended the theory to general with-carry sequences.

## References
