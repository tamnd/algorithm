---
tag: XXBA1W
kind: algorithm
slug: xoshiro-xoroshiro
name: Xoshiro and xoroshiro generators
aliases:
- xoshiro256**
- xoroshiro128+
- xoshiro256++
- xoshiro256+
- xoroshiro128**
- scrambled linear generators
area: numerical/random-number-generation
level: advanced
summary: Families of fast xor-shift-rotate generators with improved statistical quality.
model: word-ram
complexity:
  vars: {w: "the word size, 64", n: "the state size, 128 or 256"}
  time: {worst: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, in_place: true, recursive: false}
prereqs: [xorshift, linear-feedback-shift-register, primitive-polynomial]
see_also: [splitmix64, pcg-random, jump-ahead, mersenne-twister, equidistribution, statistical-tests-for-randomness, berlekamp-massey, well-rng]
sources:
  - paper: doi:10.1145/3460772
    title: David Blackman and Sebastiano Vigna, Scrambled linear pseudorandom number generators, ACM Transactions on Mathematical Software 47(4), article 36, 2021
    locator: the xoroshiro and xoshiro linear engines and their parameters, the scramblers +, ++ and **, the analysis of the linear and non-linear bits, the jump functions and the results of BigCrush and PractRand
  - url: https://prng.di.unimi.it/
    title: Sebastiano Vigna, xoshiro and xoroshiro generators and the PRNG shootout, reference C code
    locator: xoshiro256starstar.c, xoshiro256plusplus.c, xoroshiro128plus.c and xoroshiro128starstar.c, with the constants JUMP, LONG_JUMP and the characteristic polynomials in comments
  - paper: doi:10.1016/j.cam.2018.10.019
    title: Daniel Lemire and Melissa E. O'Neill, Xorshift1024*, xorshift1024+, xorshift128+ and xoroshiro128+ fail statistical tests for linearity, Journal of Computational and Applied Mathematics 350, 2019, pages 139 to 142
    locator: the failures of the linear complexity and matrix rank tests of BigCrush on the bit-reversed output of xoroshiro128+
  - paper: doi:10.1287/ijoc.1070.0251
    title: Hiroshi Haramoto, Makoto Matsumoto, Takuji Nishimura, François Panneton and Pierre L'Ecuyer, Efficient jump ahead for F2-linear random number generators, INFORMS Journal on Computing 20(3), 2008, pages 385 to 390
    locator: the jump ahead by the polynomial x^J modulo the characteristic polynomial, evaluated with Horner's rule on the state
---

The xoshiro and xoroshiro generators of David Blackman and Sebastiano Vigna (2018) are *scrambled linear* generators. A linear engine, a few XORs, shifts and rotations of 64-bit words, updates a state of 128 or 256 bits with period $2^n - 1$. A small non-linear scrambler, such as $\mathrm{rotl}(5 s_1, 7) \cdot 9$ in xoshiro256**, then turns one or two state words into the output. Their speed is close to that of [xorshift](/xorshift/), they pass the common statistical batteries in the authors' tests, they can jump ahead by $2^{128}$ steps to make independent streams, and xoshiro256** and xoshiro256++ are the default generators of several languages. The `+` variants keep linear low bits, which fail linearity tests.

## In plain words

A xorshift generator scrambles one number by sliding copies of it and combining them with exclusive or. Xoshiro and xoroshiro do the same with a few numbers at once, and they also rotate numbers: a rotation is a slide in which the digits that fall off one end come back at the other end. Rotations mix the digits faster than slides.

All of this mixing is still "linear", a structure that strong tests can find. So the generators do not output the state directly. They take one state number, multiply it, rotate it and multiply again before they return it. This last step costs little and hides the linear structure from the tests.

## The problem

We use the notation of the [pseudorandom number generator](/pseudorandom-number-generator/) page with the word size $w = 64$. The state space is $S = \{0, 1\}^n \setminus \{0\}$, $n = 128$ (two words) or $n = 256$ (four words). The transition function $f$ is linear over $\mathrm{GF}(2)$, a matrix $T$, and should have the full period $2^n - 1$, which holds exactly when the characteristic polynomial of $T$ is primitive, as on the [xorshift](/xorshift/) page. The output function $g$ is a cheap non-linear function of one or two words of the state. The goals are:

- a few word operations per output;
- the full period and good [equidistribution](/equidistribution/) of the outputs;
- no detectable failure in BigCrush or PractRand;
- jumps of $2^{n/2}$ steps for non-overlapping parallel streams.

## The algorithm

xoshiro256** keeps four words $s_0, s_1, s_2, s_3$, not all zero. Its engine uses the shift 17 and the rotation 45. Its scrambler is `**`, a multiplication by 5, a rotation by 7 and a multiplication by 9. All arithmetic is modulo $2^{64}$, and $\mathrm{rotl}(x, k)$ rotates a word left by $k$ places.

```pseudo id=main
XOSHIRO256SS-NEXT(s)                         ▷ s = (s0, s1, s2, s3), not all zero
L1  r ← rotl(5 · s1 mod 2^64, 7) · 9 mod 2^64   ▷ the ** scrambler
L2  t ← (s1 ≪ 17) mod 2^64
L3  s2 ← s2 ⊕ s0;  s3 ← s3 ⊕ s1
L4  s1 ← s1 ⊕ s2;  s0 ← s0 ⊕ s3
L5  s2 ← s2 ⊕ t
L6  s3 ← rotl(s3, 45)
L7  return r
```

Lines L2 to L6 are the linear engine xoshiro256 (xor, shift, rotate). The other members of the family change one part:

| generator | state | engine step | output |
|---|---|---|---|
| xoshiro256** | 4 words | lines L2 to L6 | $\mathrm{rotl}(5 s_1, 7) \cdot 9$ |
| xoshiro256++ | 4 words | lines L2 to L6 | $\mathrm{rotl}(s_0 + s_3, 23) + s_0$ |
| xoshiro256+ | 4 words | lines L2 to L6 | $s_0 + s_3$ |
| xoroshiro128** | 2 words | $s_1 \mathrel{\oplus}= s_0$; $s_0 \leftarrow \mathrm{rotl}(s_0, 24) \oplus s_1 \oplus (s_1 \ll 16)$; $s_1 \leftarrow \mathrm{rotl}(s_1, 37)$ | $\mathrm{rotl}(5 s_0, 7) \cdot 9$ |
| xoroshiro128+ | 2 words | as above | $s_0 + s_1$ |

The output is computed from the old state, before the engine step.

**Jumping.** Let $P$ be the characteristic polynomial of the engine $T$ and let $J(z) = z^{2^{128}} \bmod P(z) = \sum_i j_i z^i$. By the Cayley-Hamilton theorem, $T^{2^{128}} = J(T)$, so the jumped state $\sum_i j_i T^i s$ costs 256 engine steps and XORs. The reference code stores $J$ as the constant JUMP; LONG_JUMP is $z^{2^{192}} \bmod P$. This is the method of Haramoto and others on the [jump-ahead](/jump-ahead/) page.

**Seeding.** Fill the state with four outputs of [SplitMix64](/splitmix64/) from the user's seed. These four words are distinct, so they are not all zero.

## Example

From the state $(1, 2, 3, 4)$, xoshiro256** gives, in hexadecimal for the state:

| call | $s_0$ | $s_1$ | $s_2$ | $s_3$ | output |
|---|---|---|---|---|---|
| 1 | `1` | `2` | `3` | `4` | 11520 |
| 2 | `7` | `0` | `40002` | `c00000000000` | 0 |
| 3 | `c00000000007` | `40005` | `40005` | `18000000` | 1509978240 |
| 4 | `c00018040002` | `c00000000007` | `c008000e0002` | `8000a00000000300` | 1215971899390074240 |

The first output is $\mathrm{rotl}(10, 7) \cdot 9 = 1280 \cdot 9 = 11520$. The second is 0, because $s_1 = 0$ after one step. A start state with few 1 bits gives poor outputs for a while; the bits spread over the words in a few dozen steps. This is why seeding goes through SplitMix64. The reference code gives the same six first outputs, and a JUMP from the state after six calls gives the state (`1a06ce59a8dda48d`, `b32b2b669a1680ce`, `ca7ca09057bfb30f`, `7d9aec7be8db7696`); the tests of this page check both.

## Correctness

Correctness means: every non-zero state has period exactly $2^{256} - 1$, the jump function advances the state by exactly $2^{128}$ steps, and the outputs of xoshiro256** are 4-dimensionally equidistributed. The proofs are below; they rest on exact computations that the tests repeat.

1. **Period.** The engine is a linear map $T$ on $\mathrm{GF}(2)^{256}$. The [Berlekamp-Massey algorithm](/berlekamp-massey/) on 512 bits of the state sequence gives a recurrence of degree 256, and its polynomial equals the characteristic polynomial printed in the reference code. That polynomial is primitive: $z^{2^{256} - 1} \equiv 1 \pmod P$, and $z^{(2^{256} - 1)/q} \not\equiv 1$ for each prime factor $q$ of $2^{256} - 1$, the product of the Fermat numbers $F_0, \ldots, F_7$, whose eleven prime factors are known. By the theorem of the [xorshift](/xorshift/) proof, the period is $2^{256} - 1$ for every non-zero state.
2. **Jump.** JUMP equals $z^{2^{128}} \bmod P$, computed by 128 squarings, and $J(T) = T^{2^{128}}$ because $P(T) = 0$.
3. **Equidistribution.** The linear map from the state to four consecutive values of $s_1$ has rank 256 over $\mathrm{GF}(2)$, so it is a bijection. The scrambler $x \mapsto \mathrm{rotl}(5x, 7) \cdot 9$ is a bijection of words, because 5 and 9 are odd and a rotation is a permutation. So over one period, every 4-tuple of 64-bit outputs appears exactly once, except $(0, 0, 0, 0)$, which never appears.

The same computations give period $2^{128} - 1$ for xoroshiro128, JUMP equal to $z^{2^{64}} \bmod P$, and 2-dimensional equidistribution for xoroshiro128**.

## Complexity

xoshiro256** costs about 11 word operations per output: two multiplications, two rotations, one shift and six XORs, with a dependency chain short enough for several instructions per cycle on a modern processor. xoroshiro128+ costs about 8. The state is 2 or 4 words. A jump costs $n$ engine steps and $n$ conditional XORs of the state, $O(n^2 / w)$ word operations.

## Properties

- **Period** $2^{256} - 1$ for xoshiro256 and $2^{128} - 1$ for xoroshiro128, proved by the primitivity of the characteristic polynomials. The zero state is a fixed point.
- **Equidistribution.** Proved for the `**` versions: 4-dimensional for xoshiro256**, 2-dimensional for xoroshiro128**, in the sense above.
- **Linear low bits of `+`.** Addition has no carry into bit 0, so the lowest bit of $s_0 + s_3$ is the XOR of the lowest bits, an LFSR bit with linear complexity at most $n$. The next few bits are only slightly non-linear. Lemire and O'Neill (2019) show that xoroshiro128+ fails the linear complexity and matrix rank tests of BigCrush when its bits are reversed. This is proved for bit 0 and empirical for the other bits.
- **Statistical quality.** Blackman and Vigna report that xoshiro256**, xoshiro256++ and xoroshiro128** pass BigCrush and long PractRand runs, and that the `+` versions fail only tests aimed at the low bits. These are empirical results.
- **Streams.** JUMP gives $2^{128}$ non-overlapping blocks of length $2^{128}$ from one seed for xoshiro256, and LONG_JUMP $2^{64}$ blocks of length $2^{192}$.
- **Not secure.** The engine is linear and the `**` scrambler is invertible. Four outputs of xoshiro256** give four values of $s_1$, which determine the state by the rank argument above.

## Variants and improvements

- **xoshiro512 and xoroshiro1024.** Larger states with periods $2^{512} - 1$ and $2^{1024} - 1$, for massively parallel use, with the same scramblers.
- **32-bit versions.** xoshiro128** and xoshiro128++ use four 32-bit words for 32-bit platforms.
- **Floating-point output.** For a double in $[0, 1)$, take the top 53 bits: $(x \gg 11) \cdot 2^{-53}$. With xoshiro256+, this uses only high bits, so the linear low bits do not matter; this is the use the authors intended for the `+` versions.
- **Older parameters.** The first xoroshiro128+ (2016) used the constants $(55, 14, 36)$. The reference code changed to $(24, 16, 37)$ in 2018. The two give different streams.
- **Other families.** [PCG](/pcg-random/) uses an LCG engine with a permutation as output; the [Mersenne Twister](/mersenne-twister/) and [WELL](/well-rng/) use larger linear engines with tempering; counter-based generators such as [Philox](/philox/) skip the engine altogether.

## When to use it

Use xoshiro256** or xoshiro256++ as a general-purpose generator for simulation, randomized algorithms and games when speed matters and no adversary is involved. Use xoroshiro128** or xoroshiro128++ when memory is very tight, and xoshiro256+ only for floating-point output from the high bits. Use JUMP to give each thread its own block of the period. For cryptography, use a [cryptographically secure generator](/cryptographically-secure-prng/); for very large parallel runs with simple seeding, a counter-based generator such as [Philox](/philox/) may be easier.

## Pitfalls

- **The zero state.** An all-zero state stays zero and outputs zeros. Seeding with SplitMix64 avoids it.
- **Low-entropy seeds.** Setting the state to a small integer such as $(1, 0, 0, 0)$ gives poor outputs for dozens of calls, as the example shows. Never fill the state directly from a small user seed.
- **Using the low bits of the `+` versions.** `rand() % 2` or `x & 1` with xoroshiro128+ or xoshiro256+ returns an LFSR bit. Use the high bits, or a `**` or `++` version.
- **Mixed-up versions.** xoroshiro128+ with the 2016 constants and with the 2018 constants are different generators, and xoshiro256** and xoshiro256++ have different outputs on the same state. Record the exact name and constants for reproducibility.
- **Assuming independence of streams with nearby seeds.** Two generators seeded from SplitMix64 with seeds $s$ and $s + 1$ start at unrelated points of one long cycle, which is usually fine; but two states that differ by a jump of only a few steps produce overlapping streams. Use JUMP for guaranteed non-overlapping streams.

## Implementations

## History

Marsaglia's [xorshift](/xorshift/) (2003) and Vigna's scrambled xorshift* and xorshift+ (2016, 2017) were the predecessors. Blackman and Vigna introduced xoroshiro128+ in 2016, revised its constants and added the xoshiro family with the `**` scrambler in 2018, and later added the `++` scrambler. Their paper appeared in ACM Transactions on Mathematical Software in 2021. Lemire and O'Neill (2019) showed the linearity failures of the `+` versions. xoshiro256** and xoshiro256++ were then adopted as default generators in several languages and libraries.

## References
