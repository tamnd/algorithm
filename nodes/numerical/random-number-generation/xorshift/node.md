---
tag: ZZ9CEX
kind: algorithm
slug: xorshift
name: Xorshift
aliases:
- xorshift generator
- xorshift32
- xorshift64
- xor128
- Marsaglia xorshift
area: numerical/random-number-generation
level: core
summary: Fast generator using repeated XOR-shifts on a fixed-width word.
model: word-ram
complexity:
  vars: {w: "the word size, 32 or 64", n: "the state size, a multiple of w"}
  time: {worst: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, in_place: true, recursive: false}
prereqs: [linear-feedback-shift-register, primitive-polynomial, bitwise-operations]
see_also: [xoshiro-xoroshiro, splitmix64, mersenne-twister, berlekamp-massey, jump-ahead, well-rng, statistical-tests-for-randomness, equidistribution]
sources:
  - paper: doi:10.18637/jss.v008.i14
    title: George Marsaglia, Xorshift RNGs, Journal of Statistical Software 8(14), 2003, pages 1 to 6
    locator: the theorem that the generator has period 2^n - 1 for every non-zero seed exactly when T has order 2^n - 1, the 81 triples for 32 bits and the 275 triples for 64 bits, and the code of xor32 (13, 17, 5), xor64 (13, 7, 17) and xor128
  - paper: doi:10.18637/jss.v011.i05
    title: Richard P. Brent, Note on Marsaglia's xorshift random number generators, Journal of Statistical Software 11(5), 2004, pages 1 to 5
    locator: the proof that xorshift generators are linear feedback shift register generators, and the remark on their poor mixing
  - paper: doi:10.1145/1113316.1113319
    title: François Panneton and Pierre L'Ecuyer, On the xorshift random number generators, ACM Transactions on Modeling and Computer Simulation 15(4), 2005, pages 346 to 361
    locator: the characteristic polynomial and equidistribution analysis, and the TestU01 results of xorshift generators
  - paper: doi:10.1145/2845077
    title: Sebastiano Vigna, An experimental exploration of Marsaglia's xorshift generators, scrambled, ACM Transactions on Mathematical Software 42(4), article 30, 2016
    locator: the xorshift* generators, in particular xorshift64* with the shifts 12, 25, 27 and the multiplier 2685821657736338717
  - paper: doi:10.1016/j.cam.2016.11.006
    title: Sebastiano Vigna, Further scramblings of Marsaglia's xorshift generators, Journal of Computational and Applied Mathematics 315, 2017, pages 175 to 181
    locator: the xorshift128+ generator with the shifts 23, 17, 26
---

A xorshift generator keeps a word $x$ of $w$ bits and updates it with three XOR-shifts, $x \leftarrow x \oplus (x \ll a)$, $x \leftarrow x \oplus (x \gg b)$, $x \leftarrow x \oplus (x \ll c)$. Each step is a linear map $T$ on the vector space $\mathrm{GF}(2)^w$. For well-chosen shift amounts, such as $(13, 17, 5)$ for $w = 32$, $T$ has order $2^w - 1$, and every non-zero seed runs through all $2^w - 1$ non-zero words before it repeats. George Marsaglia introduced the family in 2003. It costs six word operations per output, but its output is linear over $\mathrm{GF}(2)$ and fails tests that detect this, so modern generators add a non-linear output step.

## In plain words

The generator keeps one number written in binary. To make the next number, it slides a copy of the number some places to the left, and combines the copy with the original with exclusive or: each binary digit becomes 1 where the two digits differ. Then it does the same with a slide to the right, and once more with a slide to the left.

These three cheap steps scramble the digits. With the right slide distances, the generator goes through every possible non-zero number before it comes back to the start. Zero is the one number to avoid: sliding and combining zero gives zero again.

The scrambling is still simple in a precise sense. Each digit of the result is an exclusive or of some digits of the start. Strong tests can detect this.

## The problem

We use the notation of the [pseudorandom number generator](/pseudorandom-number-generator/) page. The state space is $S = \{0, 1\}^w \setminus \{0\}$, a non-zero word of $w$ bits, and we read a word as a vector over the field $\mathrm{GF}(2)$ with two elements, where addition is XOR. The transition function $f$ must be cheap, it must be a bijection on $S$, and its period $\rho$ must be as large as possible, $2^w - 1$. The output function $g$ is the identity, or $g(x) = x / 2^w$ for an output in $U(0, 1)$.

Let $L$ be the $w \times w$ matrix of the left shift by one place (the top bit falls off) and $R$ that of the right shift. The left shift by $a$ places is $L^a$, and $x \oplus (x \ll a)$ is $(I + L^a) x$.

## The algorithm

The shift amounts $(a, b, c)$ are constants with $1 \le a, b, c < w$.

```pseudo id=main
XORSHIFT-NEXT(x)                         ▷ x is a non-zero w-bit word, shifts (a, b, c)
L1  x ← x ⊕ ((x ≪ a) mod 2^w)
L2  x ← x ⊕ (x ≫ b)
L3  x ← x ⊕ ((x ≪ c) mod 2^w)
L4  return x                             ▷ the new state is also the output
```

The step computes $f(x) = T x$ with $T = (I + L^c)(I + R^b)(I + L^a)$. Marsaglia's published triples are $(13, 17, 5)$ for $w = 32$ and $(13, 7, 17)$ for $w = 64$.

The same idea works on a state of several words. Marsaglia's xor128 keeps four 32-bit words $(x, y, z, v)$ and computes $t = x \oplus (x \ll 11)$, then shifts the words, $(x, y, z) \leftarrow (y, z, v)$, and sets $v \leftarrow v \oplus (v \gg 19) \oplus t \oplus (t \gg 8)$, which is the output. Its period is $2^{128} - 1$.

## Example

From $x = 1$ with $w = 32$ and $(a, b, c) = (13, 17, 5)$, in hexadecimal:

| step | $x$ before | after L1 | after L2 | after L3 = output | decimal |
|---|---|---|---|---|---|
| 1 | `00000001` | `00002001` | `00002001` | `00042021` | 270369 |
| 2 | `00042021` | `84000021` | `84004221` | `04080601` | 67634689 |
| 3 | `04080601` | `04c82601` | `04c82465` | `9dcca8c5` | 2647435461 |

In step 1 the right shift by 17 does nothing, because the word has no bits above position 16. After three steps the bits have spread over the whole word, but the sparse start is still visible in the first outputs, a sign of slow diffusion. Marsaglia's xor32 listing starts from $x = 2463534242$ and outputs $723471715, 2497366906, 2064144800, \ldots$; this page's tests check these values and the first outputs of xor64 and xor128.

## Correctness

Correctness means: for a good triple, every non-zero seed has the full period $2^w - 1$. The argument has three parts, proved below.

1. **The step is a bijection.** Each factor $I + L^a$ is invertible, because $L^a$ is nilpotent ($L^w = 0$), so $(I + L^a)^{-1} = I + L^a + L^{2a} + \cdots$. So $T$ is invertible, $T 0 = 0$, and $T$ maps the non-zero words onto themselves. Every orbit is a pure cycle.
2. **Full period and the order of $T$.** All non-zero seeds have period $2^w - 1$ if and only if the matrix $T$ has order $2^w - 1$ in the group of invertible matrices over $\mathrm{GF}(2)$ (Marsaglia 2003).
3. **The order and the characteristic polynomial.** $T$ has order $2^w - 1$ if and only if its characteristic polynomial $P(z)$ is a [primitive polynomial](/primitive-polynomial/) of degree $w$. Then the generator is a [linear feedback shift register](/linear-feedback-shift-register/) in disguise: each output bit satisfies the linear recurrence with characteristic polynomial $P$.

Primitivity has a finite test: $z^{2^w - 1} \equiv 1 \pmod{P}$ and $z^{(2^w - 1)/q} \not\equiv 1$ for each prime $q$ dividing $2^w - 1$. For $w = 32$, $2^{32} - 1 = 3 \cdot 5 \cdot 17 \cdot 257 \cdot 65537$. The tests of this page find $P$ by the [Berlekamp-Massey algorithm](/berlekamp-massey/) on $2w$ output bits and run this test in exact arithmetic for $(13, 17, 5)$, $(13, 7, 17)$ and xor128. A search over all triples with $a < c$ gives exactly 81 good triples for $w = 32$ and 275 for $w = 64$, the counts that Marsaglia reported.

## Complexity

Each output costs three shifts and three XORs, plus two masks in a language without fixed-width integers: $\Theta(1)$ word operations, about six. The state is one word for xorshift32 and xorshift64, and $n / w$ words for a generator of $n$ bits such as xor128. Jumping ahead by $J$ steps costs $O(w^2 \log J)$ bit operations with the polynomial $z^J \bmod P(z)$, as on the [jump-ahead](/jump-ahead/) page.

## Properties

- **Period.** Exactly $2^w - 1$ for a good triple and every non-zero seed (proved). The single state 0 is a fixed point.
- **One-dimensional equidistribution.** Over a period, each non-zero $w$-bit value appears exactly once and 0 never appears, since the output is the state. For xor128 the last four outputs are the state, so over a period every 4-tuple of 32-bit words appears once, except the all-zero tuple ([equidistribution](/equidistribution/) in 4 dimensions).
- **Linear over $\mathrm{GF}(2)$.** $f(x \oplus y) = f(x) \oplus f(y)$. Each output bit has linear complexity at most $w$, so the Berlekamp-Massey algorithm recovers the recurrence from $2w$ bits. Matrices made of output bits have rank at most $w$. This is proved, and it is why xorshift fails the linear complexity and binary matrix rank tests of [statistical test batteries](/statistical-tests-for-randomness/).
- **Slow diffusion.** A state with few 1 bits gives outputs with few 1 bits for several steps, and a seed of 0 is fatal. Brent (2004) and Panneton and L'Ecuyer (2005) point out the poor mixing. In the TestU01 results of Panneton and L'Ecuyer, xorshift generators fail many tests of Crush and BigCrush. This is an empirical result.
- **Not secure.** The state is the output. Even with a hidden state, $w$ output bits give linear equations that reveal it.

## Variants and improvements

- **Other arrangements.** Marsaglia notes that a good triple gives several generators, by applying the three factors in another order or by exchanging left and right shifts. Each arrangement must still be checked to have a primitive characteristic polynomial, or taken from his list.
- **Multi-word state.** xor128 and longer variants get a period $2^n - 1$ with $n = 64, 96, 128, \ldots$ while each output still costs a few operations. Marsaglia's xorwow adds a Weyl sequence to xor160 and is the default generator of NVIDIA's cuRAND library.
- **xorshift\*.** Vigna (2016) multiplies the output by an odd constant. xorshift64* uses the shifts 12, 25, 27 (right, left, right) and the multiplier 2685821657736338717. The multiplication breaks linearity in the high bits, but not in the lowest bit, which equals the lowest state bit because the constant is odd.
- **xorshift+.** Vigna (2017) adds two consecutive words; xorshift128+ with the shifts 23, 17, 26 was the generator of `Math.random()` in several JavaScript engines. Its lowest bit is still linear.
- **[xoshiro and xoroshiro](/xoshiro-xoroshiro/).** The successors by Blackman and Vigna replace some shifts by rotations, which mix better, and scramble the output.
- **Seeding.** [SplitMix64](/splitmix64/) is the usual way to turn one 64-bit seed into a non-zero, well-mixed state.

## When to use it

Use plain xorshift where speed and tiny code matter more than quality: a hash table probe sequence, randomized tie-breaking, a quick fuzzer, a graphics effect. For simulation, prefer a scrambled successor such as [xoshiro256**](/xoshiro-xoroshiro/) or [PCG](/pcg-random/), which cost little more and pass the statistical batteries. Never use xorshift where an adversary can see outputs; use a [cryptographically secure generator](/cryptographically-secure-prng/).

## Pitfalls

- **The zero state.** A zero seed stays zero forever. Reject it, or seed through [SplitMix64](/splitmix64/), which maps seeds to well-mixed non-zero states with high probability.
- **Arbitrary shift amounts.** Most triples do not give the full period. On 8-bit words, only 24 of the 343 triples do; on 32-bit words, only 81 of the 14415 triples with $a < c$ do. Use a published triple, or check primitivity as above.
- **Missing masks.** In a language with unbounded integers, such as Python, or when a 32-bit generator runs in 64-bit variables, the left shift keeps bits above position $w$. The right shift then pulls them back, and the generator computes a different, usually worse, map. Mask after every left shift.
- **Signed right shift.** In languages such as Java, `>>` on a signed word copies the sign bit. Use the logical shift `>>>`.
- **Low-quality low bits in the scrambled variants.** The lowest bit of xorshift64* and xorshift128+ is an LFSR bit. Take the high bits when you need few bits, for example $x \gg 63$ for a coin flip.
- **Sparse seeds.** A seed with few 1 bits gives poor outputs for the first few steps. Discard a few outputs or seed with a mixing function.

## Implementations

## History

Shift register generators date back to Tausworthe (1965), who took bits from a linear feedback shift register. George Marsaglia presented xorshift generators in 2003 as a way to run such a register one word at a time with three instructions, gave the full list of good triples for 32 and 64 bits, and reported that they passed his Diehard tests. Brent (2004) showed that they are linear feedback shift register generators, and Panneton and L'Ecuyer (2005) analysed their equidistribution and showed failures in TestU01. Sebastiano Vigna added non-linear output steps in xorshift* (2016) and xorshift+ (2017), and with David Blackman designed the [xoshiro and xoroshiro](/xoshiro-xoroshiro/) families (2018 onwards).

## References
