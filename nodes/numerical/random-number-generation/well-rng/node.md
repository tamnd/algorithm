---
tag: RZPYG3
kind: algorithm
slug: well-rng
name: WELL generator
aliases:
- Well Equidistributed Long-period Linear
- WELL512a
- WELL1024a
- WELL19937a
area: numerical/random-number-generation
level: advanced
summary: A Mersenne-Twister-like generator with better equidistribution and faster state recovery.
model: word-ram
complexity:
  vars: {r: "the number of state words, 16 for WELL512a", w: "the word size, 32"}
  time: {worst: Θ(1)}
  space: {extra: Θ(r)}
properties: {deterministic: true, in_place: true, recursive: false}
prereqs: [mersenne-twister, linear-feedback-shift-register, equidistribution]
see_also: [primitive-polynomial, berlekamp-massey, xorshift, xoshiro-xoroshiro, jump-ahead, statistical-tests-for-randomness, mersenne-prime, lagged-fibonacci-generator]
sources:
  - paper: doi:10.1145/1132973.1132974
    title: François Panneton, Pierre L'Ecuyer and Makoto Matsumoto, Improved long-period generators based on linear recurrences modulo 2, ACM Transactions on Mathematical Software 32(1), 2006, pages 1 to 16
    locator: the WELL design (a recurrence on r words with cheap matrices T0 to T7), the parameter tables for WELL512a, WELL1024a, WELL19937a and WELL44497a, the dimension defects, the number N1 of non-zero coefficients, and the experiments on escape from states with few ones
  - paper: doi:10.1145/272991.272995
    title: Makoto Matsumoto and Takuji Nishimura, Mersenne twister, a 623-dimensionally equidistributed uniform pseudo-random number generator, ACM Transactions on Modeling and Computer Simulation 8(1), 1998, pages 3 to 30
    locator: the twisted GFSR recurrence and tempering that WELL improves on, and the definition of k-distribution to v-bit accuracy
  - paper: doi:10.1145/1268776.1268777
    title: Pierre L'Ecuyer and Richard Simard, TestU01, a C library for empirical testing of random number generators, ACM Transactions on Mathematical Software 33(4), 2007, Article 22
    locator: the results for WELL and Mersenne Twister generators, and the linear complexity tests that all GF(2)-linear generators fail
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.2.2, linear recurrences modulo 2 and primitive polynomials
---

The WELL generators (Well Equidistributed Long-period Linear) of François Panneton, Pierre L'Ecuyer and Makoto Matsumoto (2006) are linear generators over $\mathrm{GF}(2)$ in the family of the [Mersenne Twister](/mersenne-twister/). The state is $r$ words of 32 bits. Each step combines a few of them with cheap matrices, shifts, XORs and masks, and writes two new words. The parameters are chosen so that the characteristic polynomial is [primitive](/primitive-polynomial/), which gives the maximal period $2^{32 r - p} - 1$, so that the outputs are as [equidistributed](/equidistribution/) as the state size allows, and so that the polynomial has many non-zero coefficients. The last property makes the generator escape quickly from states with almost all bits zero, where the Mersenne Twister lingers far longer. WELL512a, with a 512-bit state and period $2^{512} - 1$, is the smallest member; WELL19937a and WELL44497a match the Mersenne Twister's periods.

## In plain words

The generator keeps sixteen 32-bit numbers. To make a new number, it takes three or four of them, shifts their bits left or right, and combines them with exclusive or. Two of the stored numbers are replaced by the results, and one of them is the output.

These operations treat each bit as 0 or 1 and never carry, so the whole generator is a large linear system over bits. That lets us prove its cycle length and how evenly its outputs spread. The designers searched for operations that mix the bits more thoroughly than the Mersenne Twister does, so that a bad state, with almost all bits zero, turns into a normal one within a few dozen steps instead of a few hundred thousand.

## The problem

We use the notation of the [pseudorandom number generator](/pseudorandom-number-generator/) page with the word size $w = 32$. A linear generator over $\mathrm{GF}(2)$ has state $S = \mathrm{GF}(2)^k$, transition $f(V) = A V$ and output $g(V) = B V$ for bit matrices $A$ and $B$. The task is to choose $A$ so that it is cheap (a few word operations per output), its characteristic polynomial $P$ is primitive (period $2^k - 1$), the outputs are equidistributed in as many dimensions as possible, and $P$ has many non-zero coefficients, which is the WELL measure of how well $A$ mixes bits.

## The algorithm

WELL512a uses 16 words $v_{n,0}, \ldots, v_{n,15}$ in a circular buffer, with $v_{n,0}$ at index $i$. With $T_0(t, v) = v \oplus (v \ll t)$, all shifts within 32 bits, and the constant mask $\texttt{0xda442d24}$:

```pseudo id=main
WELL512A-NEXT(V, i)          ▷ V: 16 words of 32 bits, not all zero; indices mod 16
L1  z0 ← V[i + 15]
L2  z1 ← T0(16, V[i]) ⊕ T0(15, V[i + 13])
L3  z2 ← V[i + 9] ⊕ (V[i + 9] ≫ 11)
L4  V[i] ← z1 ⊕ z2                                  ▷ the new v_(n+1,1)
L5  V[i + 15] ← T0(2, z0) ⊕ T0(18, z1) ⊕ (z2 ≪ 28) ⊕ (V[i] ⊕ ((V[i] ≪ 5) ∧ 0xda442d24))
L6  i ← i + 15 mod 16                                ▷ the new v_(n+1,0) is at index i
L7  return V[i]
```

The output is $v_{n+1,0}$; the reference code returns it times $2^{-32}$ as a double in $[0, 1)$. Other members use more words, a few masked bits ($p > 0$) so that $32 r - p$ is a Mersenne exponent, and, in WELL19937c and WELL44497b, a final tempering step like the Mersenne Twister's.

## Example

From the state $v_{0,j} = j + 1$ for $j = 0, \ldots, 15$, the reference C code of the authors gives the 32-bit outputs

$$2692481146, \quad 2447117626, \quad 752362814, \quad 4237304894, \quad 3767796794,$$

that is $0.62689211824908853, 0.56976397195830941, \ldots$ as doubles. This page's implementation reproduces them.

To see the escape from a nearly zero state, start from the state with a single bit set. After 10 steps, about 3% of the 512 state bits are 1; after 50 steps about 43%; after 200 steps about 48%, the level of a random state. The Mersenne Twister, from a similar state, needs far more steps to get there, according to the experiments in the WELL paper.

## Correctness

Correctness here means the period and the equidistribution, both proved in full in the proof file.

1. **Linearity.** Every operation is a XOR, a shift or a mask, so $V_{n+1} = A V_n$ over $\mathrm{GF}(2)$, and the output is linear in the state.
2. **Period $2^{512} - 1$.** The tests run [Berlekamp-Massey](/berlekamp-massey/) on 1024 output bits, find linear complexity 512, and so obtain the characteristic polynomial $P$ of $A$. They then check that $z^{2^{512} - 1} \equiv 1$ and $z^{(2^{512} - 1)/q} \not\equiv 1$ modulo $P$ for each prime $q$ dividing $2^{512} - 1 = F_0 F_1 \cdots F_8$, the product of the Fermat numbers. All 13 prime factors are proved prime in the tests, the largest, with 62 digits, by Pocklington's criterion. So $P$ is primitive and every non-zero state has period $2^{512} - 1$.
3. **Maximal equidistribution.** For each $\ell = 1, \ldots, 32$ and $k = \lfloor 512 / \ell \rfloor$, the map from the state to the top $\ell$ bits of $k$ consecutive outputs has full rank $\ell k$, which the tests verify. Over a period, every $k$-tuple of $\ell$-bit values then occurs equally often, except the all-zero tuple, which occurs once less.

## Complexity

Each step costs about 20 word operations (shifts, XORs, one AND, index arithmetic): $\Theta(1)$. The state is $r$ words, 16 for WELL512a and 624 for WELL19937a, so $\Theta(r)$ space. Jumping ahead by $J$ steps is possible, as for any $\mathrm{GF}(2)$-linear generator, by computing $z^J \bmod P$ and evaluating that polynomial at $A$ on the state, at a cost of $O(k^2)$ word operations with $k = 32 r$ ([jump ahead](/jump-ahead/)).

## Properties

- **Proved for WELL512a (by the tests' exact computations):** period $2^{512} - 1$ from every non-zero state, and maximal equidistribution, all dimension defects 0.
- **Many non-zero coefficients.** WELL512a's characteristic polynomial has $N_1 = 225$ non-zero coefficients out of 513. The WELL paper gives about half of the coefficients for WELL19937a, against 135 out of 19938 for MT19937; it links a small $N_1$ to slow diffusion of bit differences.
- **Faster escape from zeroland:** measured, as in the example.
- **Empirical:** TestU01 reports that WELL generators pass the big batteries except the linear complexity tests, which every $\mathrm{GF}(2)$-linear generator fails once the tested bit sequence is longer than about twice the state size; small members such as WELL512a also fail matrix rank tests on matrices larger than the state ([statistical tests for randomness](/statistical-tests-for-randomness/)).
- **Not secure.** The output is linear in the state, so $512$ output bits of WELL512a determine the state by solving a linear system.

## Variants and improvements

- **WELL1024a, WELL19937a, WELL44497a.** Larger states with the same structure; WELL19937a and WELL44497a use masked bits so that the degree is a Mersenne exponent.
- **Tempered versions.** WELL19937c and WELL44497b add Matsumoto-Kurita tempering to reach maximal equidistribution where the untempered versions have small defects.
- **Mersenne Twister and SFMT.** The [Mersenne Twister](/mersenne-twister/) is faster per word but has worse equidistribution (a total defect of 6750 for MT19937 by the WELL paper's count) and slow escape from zeroland. SFMT uses SIMD instructions for speed.
- **xorshift and xoshiro.** Much smaller $\mathrm{GF}(2)$-linear generators, with nonlinear scramblers in [xoshiro](/xoshiro-xoroshiro/) that hide the linearity of the low bits.

## When to use it

Use WELL when you want a $\mathrm{GF}(2)$-linear generator with proven period and equidistribution and better mixing than the Mersenne Twister, for example in simulations that may start from poorly mixed seeds, or where maximal equidistribution in many dimensions matters. WELL512a is a good choice when a small state is needed; WELL19937c or WELL44497b replace MT19937. When speed matters more and a smaller period is enough, [xoshiro256**](/xoshiro-xoroshiro/) is faster. For security, use a [cryptographically secure generator](/cryptographically-secure-prng/).

## Pitfalls

- **The all-zero state.** It is a fixed point. Seed with at least one non-zero bit; better, fill the state from a hash or another generator, so that the start is not close to zero.
- **Unmasked shifts.** In languages with integers wider than 32 bits, the left shifts must be masked to 32 bits; otherwise the state grows and the generator is not WELL.
- **Index arithmetic.** The buffer index moves backward by one each step ($i \leftarrow i + 15 \bmod 16$), and the two new words go to the positions of $v_{n,0}$ and $v_{n,15}$. Mixing up the positions gives a different, untested generator.
- **Linearity tests.** Like all $\mathrm{GF}(2)$-linear generators, WELL fails tests that look for linear relations among bits; do not use it where such structure could bias the application, such as in some randomized algorithms over $\mathrm{GF}(2)$.
- **Licence of the reference code.** The authors' C code was released for non-commercial use; check the terms or write an independent implementation from the paper.

## Implementations

## History

Matsumoto and Nishimura's Mersenne Twister (1998) made huge-period $\mathrm{GF}(2)$-linear generators standard, but it was soon noticed that it recovers slowly from states with many zero bits and is not maximally equidistributed. Panneton, L'Ecuyer and Matsumoto addressed both points in 2006 with the WELL family, found by a computer search over cheap matrices, with the dimension defects and the number of non-zero coefficients of the characteristic polynomial as search criteria. WELL generators are available in several libraries, for example the R package rngWELL.

## References
