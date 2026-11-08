---
tag: V3VE7E
kind: algorithm
slug: splitmix64
name: SplitMix64
aliases:
- splitmix
- SplittableRandom
- SplitMix
area: numerical/random-number-generation
level: advanced
summary: A fast 64-bit generator used to seed other generators, based on a Weyl sequence and a mixer.
model: word-ram
complexity:
  vars: {w: "the word size, 64"}
  time: {worst: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, in_place: true, recursive: false}
prereqs: [pseudorandom-number-generator, murmurhash, modular-inverse]
see_also: [xoshiro-xoroshiro, xorshift, seed, pcg-random, avalanche-effect, philox, jump-ahead, birthday-paradox]
sources:
  - paper: doi:10.1145/2660193.2660195
    title: Guy L. Steele Jr., Doug Lea and Christine H. Flood, Fast splittable pseudorandom number generators, OOPSLA 2014, ACM SIGPLAN Notices 49(10), pages 453 to 472
    locator: the SplitMix design (a Weyl sequence with an odd gamma, a mixing function for the output, and a split operation that derives a new seed and gamma), and the TestU01 results
  - url: https://prng.di.unimi.it/splitmix64.c
    title: Sebastiano Vigna, splitmix64.c, reference implementation
    locator: the constants 0x9e3779b97f4a7c15, 0xbf58476d1ce4e5b9 and 0x94d049bb133111eb with the shifts 30, 27, 31, and the advice to use it to seed xoshiro and xoroshiro generators
  - url: http://zimbry.blogspot.com/2011/09/better-bit-mixing-improving-on.html
    title: David Stafford, Better bit mixing, improving on MurmurHash3's 64-bit finalizer, 2011
    locator: the table of mixing variants, of which variant 13 uses the shifts 30, 27, 31 and the two multipliers above
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.2.1.1, the multiplicative inverse modulo a power of 2 of an odd number, and Section 3.2.2 on additive sequences
---

SplitMix64 is a 64-bit generator whose state is a counter. Each call adds a fixed odd constant $\gamma$ to the state modulo $2^{64}$, a Weyl sequence, and returns a strong bijective hash of the new state. The odd increment gives the period exactly $2^{64}$, and the hash, three XOR-shifts and two multiplications, makes neighbouring states give unrelated outputs. Steele, Lea and Flood introduced it in 2014 for Java's `SplittableRandom`. It is fast, accepts any seed including 0, and is the standard way to expand one 64-bit seed into the state of a larger generator such as [xoshiro256**](/xoshiro-xoroshiro/).

## In plain words

The generator keeps a counter. Each time you ask for a number, it adds a large odd constant to the counter, letting it wrap around at $2^{64}$. Because the constant is odd, the counter visits every possible 64-bit value once before it returns to the start.

A counter alone is a poor random number: consecutive values differ by the same amount. So the generator does not return the counter. It returns a scrambled copy, made by mixing the bits of the counter with shifts, exclusive or and multiplications. The scrambling can be undone, so different counter values always give different outputs, and a change of one bit in the counter changes about half the bits of the output.

## The problem

We use the notation of the [pseudorandom number generator](/pseudorandom-number-generator/) page with the word size $w = 64$. The state space is $S = \mathbb{Z}_{2^{64}}$, all 64-bit words, including 0. The transition function is $f(x) = (x + \gamma) \bmod 2^{64}$, and the output function $g$ is a fixed bijection of 64-bit words, the *mixer*. The task is to make the outputs $g(x_0 + i \gamma)$ look independent and uniform, at a cost of a few word operations per output, for every seed $x_0$.

A second goal is *splitting*: from one generator, create a second one whose stream looks independent of the first, without communication, for parallel programs with a tree of tasks.

## The algorithm

The constants are $\gamma = \texttt{0x9e3779b97f4a7c15}$, the odd integer nearest to $2^{64} / \varphi$ with $\varphi$ the golden ratio, and the multipliers $M_1 = \texttt{0xbf58476d1ce4e5b9}$ and $M_2 = \texttt{0x94d049bb133111eb}$. All arithmetic is modulo $2^{64}$.

```pseudo id=main
SPLITMIX64-NEXT(x)                           ▷ x is the 64-bit state, any value
L1  x ← (x + γ) mod 2^64                     ▷ Weyl step, γ odd
L2  z ← x
L3  z ← (z ⊕ (z ≫ 30)) · M1 mod 2^64
L4  z ← (z ⊕ (z ≫ 27)) · M2 mod 2^64
L5  return (x, z ⊕ (z ≫ 31))                 ▷ the new state and the output
```

Lines L3 to L5 are the mixer $g$, variant 13 of David Stafford's improvements of the 64-bit finalizer of [MurmurHash3](/murmurhash/). To fill the state of a larger generator, call SPLITMIX64-NEXT once per word, starting from the user's seed.

**Splitting.** In Java's `SplittableRandom`, a generator also has its own odd $\gamma$. To split, the parent draws two values from its own stream: one becomes the child's start state, and the other, mixed by a second function and forced odd, becomes the child's $\gamma$. A $\gamma$ with too few changes between adjacent bits is replaced, because such a constant makes the Weyl sequence too regular.

## Example

From the seed $x_0 = 0$, in hexadecimal:

| $i$ | $x_i$ after L1 | $z$ after L3 | $z$ after L4 | output | output in decimal |
|---|---|---|---|---|---|
| 1 | `9e3779b97f4a7c15` | `6f68261b57e7a770` | `e220a838bf5c9dde` | `e220a8397b1dcdaf` | 16294208416658607535 |
| 2 | `3c6ef372fe94f82a` | `2a94fcbfccb43499` | `6e789e6a7d485920` | `6e789e6aa1b965f4` | 7960286522194355700 |
| 3 | `daa66d2c7ddf743f` | `f1c3dd6322d82c9e` | `06c45d188d81ff7e` | `06c45d188009454f` | 487617019471545679 |

The states advance by the same step, and the carry out of the top bit is lost: $x_2 = 2\gamma - 2^{64}$. The outputs show no such pattern. The reference code from the seed 1234567 gives $6457827717110365317, 3203168211198807973, 9817491932198370423, \ldots$; this page's tests check these values.

## Correctness

Correctness here means: the generator has period exactly $2^{64}$ from every seed, and over one period its outputs are all $2^{64}$ words, each once. Both follow from two facts, proved below.

1. **The Weyl step has full period.** $x_i = x_0 + i \gamma \bmod 2^{64}$, and $x_i = x_j$ if and only if $2^{64}$ divides $(i - j)\gamma$. Since $\gamma$ is odd, this holds if and only if $2^{64}$ divides $i - j$.
2. **The mixer is a bijection.** Each of its five steps is invertible: $z \mapsto z \oplus (z \gg s)$ with $s \ge 1$ is inverted by repeating $y \leftarrow z \oplus (y \gg s)$, and multiplication by an odd $M$ is inverted by multiplication by $M^{-1} \bmod 2^{64}$, which exists because $M$ is odd ([modular inverse](/modular-inverse/)).

So the outputs of one period are the images of all $2^{64}$ words under a bijection.

## Complexity

Each output costs one addition, two multiplications, three shifts and three XORs: $\Theta(1)$ word operations, about nine, with a dependency chain of two multiplications. The state is one word, plus $\gamma$ if it is not a constant. Jumping ahead by $J$ outputs costs one multiplication: $x_{i + J} = x_i + J \gamma \bmod 2^{64}$, so random access into the stream is free, as in a counter-based generator such as [Philox](/philox/).

## Properties

- **Period $2^{64}$ and exact uniformity.** Proved above. Every seed works, including 0, which matters when the seeds come from users.
- **No repeated output within a period.** This is also a defect: among $n$ truly random 64-bit words, the expected number of equal pairs is about $n^2 / 2^{65}$ by the [birthday paradox](/birthday-paradox/). At $n = 2^{36}$ outputs, the expected count is 64 for random words and 0 for SplitMix64, so a collision test detects the difference after a few times $2^{32}$ outputs.
- **Statistical quality.** Steele, Lea and Flood report that SplitMix passes the BigCrush battery of TestU01. This is an empirical result about single streams from the default $\gamma$.
- **Bad $\gamma$ values.** For a $\gamma$ such as 1, or with long runs of equal bits, consecutive states differ in few bits, and the mixer does not fully hide it. This is why the splitting code rejects such values.
- **Not secure.** The mixer is invertible and public, so one output reveals the state $x_i$, and with two consecutive outputs also $\gamma$. All later outputs follow.

## Variants and improvements

- **SplittableRandom.** The Java class (since Java 8) uses the same mixer for 64-bit outputs, a different mixer for 32-bit outputs, and splitting as described above.
- **Other mixers.** The original MurmurHash3 finalizer uses the shift 33 three times with other multipliers. Stafford's table lists further variants, and later designs with more rounds aim at better avalanche behaviour for counters with small or regular steps.
- **Seeding other generators.** Vigna's reference code for [xoshiro and xoroshiro](/xoshiro-xoroshiro/) recommends filling the state with SplitMix64 outputs. Since the outputs of one period are all distinct, four consecutive outputs are never all zero, so the xoshiro256 state is never the forbidden zero state.
- **Counter-based generators.** [Philox](/philox/) and [Threefry](/threefry/) push the same idea further: the state is a counter and the output is a keyed function of it with many rounds, strong enough to pass the test batteries for any key and any counter.

## When to use it

Use SplitMix64 to turn a user's seed into the state of a larger generator, as a fast general-purpose generator when a period of $2^{64}$ is enough, or as a cheap hash of a 64-bit integer. Its jump-ahead by one multiplication makes it handy for reproducible random access. For long simulations, prefer a generator with a longer period and many streams such as [xoshiro256**](/xoshiro-xoroshiro/) or [PCG](/pcg-random/). Never use it where an adversary can see outputs; use a [cryptographically secure generator](/cryptographically-secure-prng/).

## Pitfalls

- **Unsigned arithmetic.** The right shifts must be logical. In Java, use `>>>`; in Python, mask the products to 64 bits.
- **Even $\gamma$.** With an even $\gamma = 2^k \gamma'$, the period drops to $2^{64 - k}$. Force $\gamma$ odd.
- **Overlapping streams from nearby seeds.** Two generators with seeds $s$ and $s + \gamma$ give the same stream shifted by one. With seeds chosen as small consecutive integers and the same $\gamma$, the streams are shifts of each other by $(s' - s)\gamma^{-1} \bmod 2^{64}$ steps, which is usually huge, but they are still parts of one sequence.
- **Exhausting the period.** A period of $2^{64}$ can be exhausted only in years, but the absence of collisions shows after about $2^{32}$ to $2^{36}$ outputs, as above. Do not draw that many values from one stream where it matters.
- **Using the mixer as a secure hash.** The mixer is public and invertible, so it hides nothing from an attacker. A hash table keyed by adversarial input needs a keyed hash, and secrets need a [cryptographically secure generator](/cryptographically-secure-prng/).

## Implementations

## History

Weyl sequences, $i \gamma \bmod 1$ with an irrational $\gamma$, go back to Hermann Weyl's equidistribution theorem of 1916. Guy Steele, Doug Lea and Christine Flood designed SplitMix for Java 8's `SplittableRandom` (2014), aiming at fast, splittable generators for fork-join parallelism. Sebastiano Vigna published the 64-bit version as splitmix64.c and recommended it for seeding his [xoshiro and xoroshiro](/xoshiro-xoroshiro/) generators, which made it the usual seeding routine of many libraries.

## References
