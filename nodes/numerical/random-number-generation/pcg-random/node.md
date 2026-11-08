---
tag: 0VZS5V
kind: algorithm
slug: pcg-random
name: PCG random number generator
aliases:
- permuted congruential generator
- PCG
- pcg32
- pcg64
- PCG XSH RR
area: numerical/random-number-generation
level: advanced
summary: An LCG whose output is passed through a permutation function to improve statistical quality.
model: word-ram
complexity:
  vars: {w: "the output size, 32 for pcg32", n: "the state size, 64 for pcg32"}
  time: {worst: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, in_place: true, recursive: false}
prereqs: [linear-congruential-generator, hull-dobell-theorem, bitwise-operations]
see_also: [xoshiro-xoroshiro, splitmix64, jump-ahead, lemire-bounded-integers, uniform-random-integer-generation, statistical-tests-for-randomness, randu, philox]
sources:
  - url: https://www.pcg-random.org/pdf/hmc-cs-2014-0905.pdf
    title: Melissa E. O'Neill, PCG, a family of simple fast space-efficient statistically good algorithms for random number generation, Harvey Mudd College technical report HMC-CS-2014-0905, 2014
    locator: the sections on the permutation functions (XSH RR, XSH RS, RXS M XS, XSL RR), on the members pcg32 and pcg64 with their uniformity over a period, on extended generators, and on the TestU01 results of reduced-size members
  - url: https://www.pcg-random.org/download.html
    title: Melissa E. O'Neill, PCG random number generators, C minimal implementation pcg-c-basic
    locator: pcg_basic.c (pcg32_srandom_r, pcg32_random_r, pcg32_boundedrand_r) and the output of pcg32-demo for the seed 42 and stream 54
  - paper: "Forrest B. Brown, Random number generation with arbitrary strides, Transactions of the American Nuclear Society 71, 1994, pages 202 to 203"
    locator: the jump ahead of an LCG by k steps in O(log k) operations, used by pcg32_advance
  - paper: "T. E. Hull and A. R. Dobell, Random number generators, SIAM Review 4(3), 1962, pages 230 to 254"
    locator: the conditions for full period of a mixed congruential generator modulo a power of 2
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.2.1.2, Theorem A (full period of a linear congruential sequence), and Section 3.2.1.1 on the short periods of the low bits modulo a power of 2
---

PCG, the permuted congruential generator of Melissa O'Neill (2014), runs a [linear congruential generator](/linear-congruential-generator/) modulo $2^{64}$ or $2^{128}$ and passes each state through a small permutation before output. The member pcg32 keeps a 64-bit state, computes 32-bit outputs with "XSH RR": an XOR-shift of the high bits, then a rotation by an amount taken from the top five bits. The LCG gives the full period $2^{64}$, cheap jump-ahead and $2^{63}$ selectable streams; the output step hides the weak low bits and the lattice structure. Each 32-bit value appears exactly $2^{32}$ times per period. NumPy's default generator is a PCG.

## In plain words

A linear congruential generator multiplies a number by a constant, adds another constant and keeps the remainder after division by a power of two. It is fast and easy to analyse, but its lower binary digits repeat with very short cycles, and its numbers fall on a few planes when plotted.

PCG keeps such a generator inside, with a 64-bit number, but never shows that number directly. It throws away the weak low digits, mixes the rest with a shift and an exclusive or, and then rotates the result by an amount that depends on the top digits. So the rotation changes from one call to the next in a way that is hard to predict, and the simple patterns disappear from the output.

## The problem

We use the notation of the [pseudorandom number generator](/pseudorandom-number-generator/) page. The state space is $S = \mathbb{Z}_{2^{64}}$, and the transition is the LCG $f(x) = (a x + c) \bmod 2^{64}$ with the modulus $m = 2^{64}$, the multiplier $a = 6364136223846793005$ and an odd increment $c$. The LCG alone is cheap and has a full period, but bit $k$ of the state has period at most $2^{k+1}$, and $t$-tuples of outputs lie on a lattice. The task is an output function $g$ from 64 to 32 bits that

- costs a few word operations;
- keeps the output exactly uniform over a period;
- removes the weaknesses of the LCG well enough to pass the statistical batteries.

## The algorithm

pcg32 uses the output function XSH RR (xorshift high, random rotation). The increment $c$ is odd; it selects one of $2^{63}$ streams.

```pseudo id=main
PCG32-NEXT(state, c)                        ▷ 64-bit state, c odd
L1  old ← state
L2  state ← (a · old + c) mod 2^64          ▷ a = 6364136223846793005
L3  x ← ((old ≫ 18) ⊕ old) ≫ 27 mod 2^32   ▷ bits 27 to 58 after a xorshift
L4  r ← old ≫ 59                            ▷ the top 5 bits, 0 ≤ r < 32
L5  return (state, rotr32(x, r))
```

The output is a function of the old state, so the multiplication of line L2 can run in parallel with lines L3 and L4.

**Seeding.** The reference code `pcg32_srandom_r(initstate, initseq)` sets $c = 2 \cdot \mathit{initseq} + 1$ (modulo $2^{64}$), starts from state 0, steps once, adds $\mathit{initstate}$, and steps again.

**Jump-ahead.** The $k$-fold composition of $x \mapsto a x + c$ is $x \mapsto A_k x + C_k$, with $A_k = a^k$ and $C_k = c (a^{k-1} + \cdots + 1)$. Brown's method computes $(A_k, C_k)$ by squaring and multiplying affine maps for the set bits of $k$, in $O(\log k)$ multiplications, as on the [jump-ahead](/jump-ahead/) page. A negative $k$ is the same as $k \bmod 2^{64}$, so the generator can also step backwards.

**Bounded integers.** `pcg32_boundedrand_r(bound)` rejects outputs below $t = 2^{32} \bmod \mathit{bound}$ and returns $r \bmod \mathit{bound}$, which is exactly uniform, as on the [uniform random integer](/uniform-random-integer-generation/) page.

## Example

The reference program `pcg32-demo` seeds with $\mathit{initstate} = 42$ and $\mathit{initseq} = 54$. Then $c = 109$ and the state after seeding is `185706b82c2e03f8`. In hexadecimal:

| call | old state | $x$ after L3 | $r$ after L4 | output |
|---|---|---|---|---|
| 1 | `185706b82c2e03f8` | `0ae015bd` | 3 | `a15c02b7` |
| 2 | `2b47fed88766bb05` | `68fe812f` | 5 | `7b47f409` |
| 3 | `8b33296d19bf5b4e` | `6661743a` | 17 | `ba1d3330` |

In call 1, the top five bits of `185706b8...` are `00011`, so the rotation is by 3: `0ae015bd` rotated right by 3 is `a15c02b7`. The next outputs are `83d2f293`, `bfa4784b` and `cbed606e`, as printed by the demo; after them, six calls of the bounded generator with bound 6 give 5, 3, 0, 2, 0, 1.

## Correctness

Correctness means: from every state, the period is exactly $2^{64}$, and over one period every 32-bit output value appears exactly $2^{32}$ times. The proofs are below.

1. **Full period.** By the [Hull-Dobell theorem](/hull-dobell-theorem/), an LCG modulo $2^{64}$ has period $2^{64}$ if and only if $c$ is odd and $a \equiv 1 \pmod 4$. The seeding makes $c$ odd, and $a \equiv 5 \pmod 8$.
2. **Uniform output.** Fix the top five bits of the state, which fix the rotation $r$. Bits 0 to 26 of the state do not affect the output. Bits 27 to 58 are mapped to $x$ by a triangular map: bit $k$ of $x$ is $x_{k+27} \oplus x_{k+45}$ for $k \le 18$ and $x_{k+27}$ for $k \ge 19$, so it can be solved from the top down, and it is a bijection for each value of the top five bits. Rotation by a fixed $r$ is a bijection. So each output value comes from exactly $2^{5} \cdot 2^{27} = 2^{32}$ states, and a full period visits every state once.

## Complexity

Each output costs one 64-bit multiplication and addition, three shifts, one XOR and one 32-bit rotation: $\Theta(1)$ word operations, about eight. The state is two words, the state and the increment, or one if the increment is a constant. A jump of $k$ steps costs $O(\log k)$ multiplications. pcg64 needs a 128-bit multiplication per output, which costs several 64-bit operations on most processors.

## Properties

- **Period** $2^{64}$ from every state, and $2^{63}$ streams selected by the odd increment (proved). Every state is allowed, including 0.
- **Exact uniformity** over a period: each 32-bit output appears $2^{32}$ times (proved). The output is not $k$-dimensionally equidistributed for $k \ge 3$ in general, since 64 bits of state cannot give all $2^{96}$ triples of outputs.
- **Statistical quality.** O'Neill reports that pcg32 and pcg64 pass BigCrush, and that reduced-size members fail it only at sizes predicted by the state size. These are empirical results.
- **Low bits are hidden.** Bit $k$ of an LCG state modulo $2^{64}$ has period at most $2^{k+1}$ (proved, Knuth 3.2.1.1). XSH RR uses only bits 27 to 63.
- **Related streams.** For two increments $c$ and $c'$, the map $y = u x$ with $u = c' c^{-1} \bmod 2^{64}$ turns the LCG with increment $c$ into the one with $c'$: $a (u x) + c' = u (a x + c)$. So the internal states of two streams are scaled copies of each other (proved). The output permutation hides this only partly, and correlations between streams with related increments have been reported.
- **Not secure.** O'Neill argues that PCG is harder to predict than a plain LCG, but no reduction to a hard problem exists. Bouillaguet, Martinez and Sauvage (2020) recovered the full state of PCG64 from a small number of outputs, and the 64-bit state of pcg32 is easier still. Treat PCG as insecure.

## Variants and improvements

- **pcg64 (XSL RR 128/64).** A 128-bit LCG; the output XORs the high and low 64-bit halves and rotates by the top 6 bits. NumPy's `default_rng` used PCG64 from version 1.17.
- **PCG64 DXSM.** A later output function ("double xorshift multiply") with a cheaper 64-bit multiplier for the LCG, added to NumPy as PCG64DXSM to address correlations between many parallel PCG64 streams.
- **Other permutations.** RXS M XS (random xorshift, multiply, xorshift) gives an output as wide as the state, a permutation of the state; XSH RS uses a random shift instead of a rotation.
- **Extended generators.** O'Neill's extension adds a table of extra state words that is updated rarely, for periods such as $2^{64 \cdot 2^k}$ and $k$-dimensional equidistribution.
- **MCG variant.** A multiplicative generator ($c = 0$) modulo $2^{64}$ is faster but has period $2^{62}$ and only odd states.

## When to use it

Use pcg32 when you need a small, fast, statistically good 32-bit generator with streams and cheap jump-ahead, for simulation, games and randomized algorithms. Use pcg64 or PCG64DXSM for 64-bit outputs. For the same jobs, [xoshiro256**](/xoshiro-xoroshiro/) is a comparable choice; for parallel work with millions of independent streams, a counter-based generator such as [Philox](/philox/) is simpler to seed. Use a [cryptographically secure generator](/cryptographically-secure-prng/) for anything security related.

## Pitfalls

- **Even increments.** With an even $c$, the period drops to at most $2^{62}$, and the state may get stuck in a short cycle. The seeding code forces $c$ odd; a hand-written seeding must too.
- **Assuming streams are independent.** Different increments give related state sequences, as shown above. Seeding many generators with consecutive stream numbers and the same start state is a known source of correlation. Prefer different start states as well, or jump within one stream.
- **Using the LCG state as output.** The state itself has all the LCG weaknesses. Only the permuted output is good.
- **Reducing modulo a bound.** `pcg32() % n` is biased when $n$ does not divide $2^{32}$. Use the bounded function or [Lemire's method](/lemire-bounded-integers/).
- **Version mismatch.** pcg32 in pcg-c-basic, pcg-cpp and other ports use the same multiplier but may seed differently. NumPy's PCG64 and PCG64DXSM give different streams. Record the exact variant for reproducibility.

## Implementations

## History

Linear congruential generators go back to Lehmer (1949), and the idea of improving them by dropping low bits or tempering the output is old. Melissa O'Neill introduced the PCG family in a 2014 technical report, with permutation functions chosen by testing reduced-size members against TestU01 to see how much state each output function needs. PCG became widely used through NumPy, which adopted PCG64 as its default bit generator in 2019, and later added PCG64DXSM. Criticism of the correlations between PCG streams, by Sebastiano Vigna among others, was part of the discussion that led NumPy to add PCG64DXSM.

## References
