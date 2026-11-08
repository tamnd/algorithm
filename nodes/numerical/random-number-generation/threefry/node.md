---
tag: SS4JEM
kind: algorithm
slug: threefry
name: Threefry
aliases:
- Threefish-based counter RNG
- Threefry2x64
- Threefry2x32
- Threefry4x64
- Random123 Threefry
area: numerical/random-number-generation
level: advanced
summary: A counter-based generator built from Threefish-style rounds, from the Random123 family.
model: word-ram
complexity:
  vars: {R: "the number of rounds, 20 by default", n: "the number of words per block, 2 or 4"}
  time: {worst: Θ(R n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, in_place: true, recursive: false}
prereqs: [pseudorandom-number-generator, block-cipher, skein]
see_also: [philox, splitmix64, avalanche-effect, chacha20, salsa20, speck, cryptographically-secure-prng, statistical-tests-for-randomness]
sources:
  - paper: doi:10.1145/2063384.2063405
    title: John K. Salmon, Mark A. Moraes, Ron O. Dror and David E. Shaw, Parallel random numbers, as easy as 1, 2, 3, Proceedings of the International Conference for High Performance Computing, Networking, Storage and Analysis (SC11), 2011, Article 16
    locator: "Section 3 on counter-based generators, Section 4 on Threefry (Threefish rounds without the tweak, new rotation constants for the 2-word and 32-bit variants), and the tables of TestU01 results by number of rounds"
  - paper: "Niels Ferguson, Stefan Lucks, Bruce Schneier, Doug Whiting, Mihir Bellare, Tadayoshi Kohno, Jon Callas and Jesse Walker, The Skein Hash Function Family, version 1.3, 2010"
    locator: "Section 3.3, the Threefish block cipher: the MIX function, the word permutation, the rotation constants for Threefish-256, the key schedule with the constant C240, and the 72 rounds"
  - url: https://github.com/DEShawResearch/random123
    title: D. E. Shaw Research, Random123, a library of counter-based random number generators
    locator: "the header threefry.h (the rotation tables R_64x2, R_64x4, R_32x2, R_32x4 and SKEIN_KS_PARITY) and the file examples/kat_vectors used by the tests"
---

Threefry is a counter-based random number generator from the Random123 library of John Salmon, Mark Moraes, Ron Dror and David Shaw (2011). Like [Philox](/philox/), it computes the $i$-th output block directly as $\Theta_K(i)$, a keyed function of the counter $i$, so streams need no state, any block can be computed independently, and parallel tasks need only distinct keys or counter ranges. The function is a weakened version of the Threefish block cipher of the [Skein](/skein/) hash function: rounds of addition, rotation and XOR on 64-bit or 32-bit words, with a key injected every four rounds, but without Threefish's tweak and with 20 rounds instead of 72. It uses no multiplications, so it is fast on any processor. Threefry2x32 with 20 rounds is the default generator of the JAX machine-learning library.

## In plain words

Number the random blocks you need 0, 1, 2 and so on. Threefry turns each number, together with a secret-looking key, into a block of bits that looks random. It does this by repeating a simple step twenty times: add one word into another, rotate the bits of the second word by a fixed amount, and combine the two with exclusive or. Every fourth step it adds the key in again.

Each step can be run backward, so different numbers always give different blocks. There is nothing to remember between blocks, so you can jump to block one billion at once, and many processors can each work on their own blocks without talking to each other.

## The problem

As in the [Philox](/philox/) page: the state is a counter $i \in \{0, \ldots, 2^{nw} - 1\}$, the transition is $f(i) = i + 1$, and the output is $g(i) = \Theta_K(i)$, a block of $n$ words of $w$ bits. Design $\Theta_K$ so that the outputs for consecutive counters pass the strongest statistical tests for every key, at the lowest cost in word operations, using only additions, rotations and XORs (the ARX operations), which are fast and constant-time on all hardware.

## The algorithm

Threefry2x64 works on two 64-bit words, with additions modulo $2^{64}$. The rotation amounts are $\mathrm{ROT} = (16, 42, 12, 31, 16, 32, 24, 21)$, used cyclically, and $C_{240} = \texttt{0x1BD11BDAA9FC1A22}$ is the key schedule constant of Threefish.

```pseudo id=main
THREEFRY2X64(X, K, R)      ▷ X = (x0, x1): counter; K = (k0, k1): key; R = 20 by default
L1  ks ← (k0, k1, k0 ⊕ k1 ⊕ C240)
L2  x0 ← x0 + ks[0]; x1 ← x1 + ks[1]
L3  for r ← 0 to R − 1
L4      x0 ← x0 + x1; x1 ← ROTL(x1, ROT[r mod 8]) ⊕ x0
L5      if r mod 4 = 3
L6          s ← (r + 1)/4; x0 ← x0 + ks[s mod 3]; x1 ← x1 + ks[(s + 1) mod 3] + s
L7  return (x0, x1)
```

Threefry4x64 and Threefry4x32 use four words and five key words. Each round applies the MIX step of line L4 to two pairs, $(x_0, x_1)$ and $(x_2, x_3)$ in even rounds and $(x_0, x_3)$ and $(x_2, x_1)$ in odd rounds, with a pair of rotation amounts per round. Every four rounds, word $i$ receives key word $(s + i) \bmod 5$, and the last word also receives $s$. Threefry4x64 has the rotation constants of Threefish-256; the 2-word and 32-bit variants have rotation constants chosen by the Random123 authors.

## Example

Take the counter $(\texttt{243f6a8885a308d3}, \texttt{13198a2e03707344})$ and the key $(\texttt{a4093822299f31d0}, \texttt{082efa98ec4e6c89})$, digits of $\pi$ from Random123's known-answer tests. The extended key word is $k_0 \oplus k_1 \oplus C_{240} = \texttt{b7f6d9606c2d477b}$. The state evolves as follows (the rows for 4 and 8 rounds include the key injection after them):

| rounds | $x_0$ | $x_1$ |
|---|---|---|
| injection only | c848a2aaaf423aa3 | 1b4884c6efbedfcd |
| 1 | e39127719f011a70 | 6757c8cf40cc0138 |
| 4 | d2ccd6c7cfdba4d9 | 43ec0030ce169cd4 |
| 13 | c3aac71561042993 | 3fe7ae8801aff316 |
| 20 | 263c7d30bb0f0af1 | 56be8361d3311526 |

The rows for 13 and 20 rounds are the published outputs of Threefry2x64-13 and Threefry2x64-20. With key 0, the counters 0 and 1 give $(\texttt{c2b6e3a8c2c69865}, \texttt{6f81ed42f350084d})$ and $(\texttt{baf51c00fb3a5957}, \texttt{ed553e57f10b3b42})$. The implementation reproduces all 36 Threefry known-answer vectors of Random123, for the four block sizes and 13, 20, 32 and 72 rounds.

## Correctness

The proof file proves the structural property; randomness is empirical.

1. **MIX is invertible.** From $(y_0, y_1) = (x_0 + x_1, \mathrm{rotl}(x_1) \oplus y_0)$, one gets $x_1 = \mathrm{rotr}(y_1 \oplus y_0)$ and $x_0 = y_0 - x_1$.
2. **Key injection is invertible.** It adds constants that depend only on the key and the round, not on the counter.
3. **Counter mode never repeats.** $\Theta_K$ is a composition of bijections, hence a permutation of the counter space: distinct counters give distinct blocks, and the period is $2^{128}$ blocks for Threefry2x64.
4. **Random access.** Block $i$ depends only on $i$ and $K$.

## Complexity

Each round costs one addition, one rotation and one XOR per word pair, and each injection $n + 1$ additions, so a block costs $\Theta(R n)$ word operations: for Threefry2x64-20, about 60 operations for 128 bits plus 15 for the five injections. There are no multiplications or table lookups, which makes Threefry fast on CPUs and constant-time. The working space is the block and the $n + 1$ key words, and jumping to any position costs one block.

## Properties

- **Proved:** for every key and every number of rounds, distinct counters give distinct blocks, so a stream has period $2^{nw}$ blocks with no repeat.
- **Empirical:** the authors report that 13 rounds of Threefry2x64 and Threefry4x64 pass all of TestU01's SmallCrush, Crush and BigCrush, and recommend 20 rounds for a safety margin. The tests here measure the avalanche of Threefry2x64: flipping one counter bit flips on average 64.0 of the 128 output bits with 20 rounds, but about 19 with 3 rounds and 56 with 6.
- **Many streams.** The key gives $2^{128}$ distinct permutations for Threefry2x64, so keys can be derived from task identifiers.
- **Not a cipher.** Threefry is Threefish without the tweak, with far fewer rounds, and in some variants with new rotation constants. Threefry4x64 with 72 rounds follows the round and key structure of Threefish-256 with a zero tweak, but the reduced versions have no security analysis, and none of them is offered as a cryptographic generator.

## Variants and improvements

- **Block sizes.** Threefry2x32, Threefry4x32, Threefry2x64 and Threefry4x64, with 13, 20 or 72 rounds; Random123 uses 20 by default.
- **[Philox](/philox/).** The Random123 family based on multiplications; faster on GPUs, which have fast multiply-high instructions.
- **JAX's splittable keys.** JAX derives new keys by applying Threefry2x32 to the old key and a counter, which turns the counter-based generator into a splittable one, in the spirit of [SplitMix](/splitmix64/).
- **Cryptographic ARX generators.** [ChaCha20](/chacha20/) and [Salsa20](/salsa20/) in counter mode are ARX constructions with a security analysis, at a few times the cost.

## When to use it

Use Threefry for parallel, reproducible random numbers on CPUs or on hardware without fast wide multiplications, and wherever a pure function from (key, counter) to random bits is the natural interface, as in functional programming and in JAX. Give each task its own key or counter range. For sequential use on one core, a small stateful generator such as [xoshiro256**](/xoshiro-xoroshiro/) is faster; for secrets, use a [cryptographically secure generator](/cryptographically-secure-prng/).

## Pitfalls

- **Reusing a (key, counter) pair.** Two tasks with the same key and overlapping counters get the same numbers. Allocate counters or keys systematically.
- **Too few rounds.** The avalanche is far from complete after 3 rounds and still visibly incomplete after 6; the authors' statistical failures with few rounds confirm it. Keep 20, or at least 13 for the 64-bit variants after testing.
- **Wrong rotation table.** The 2-word and 32-bit variants have their own rotation constants; using the Threefish-256 table for them gives a different, untested generator.
- **Word order.** The order of counter words, key words and output words varies between libraries; follow the reference to reproduce published streams.
- **Cryptographic use.** Not designed or analyzed for security; do not use it for keys, nonces or tokens.

## Implementations

## History

Threefish is the tweakable block cipher at the core of the Skein hash function, which Ferguson, Lucks, Schneier, Whiting, Bellare, Kohno, Callas and Walker submitted to the NIST SHA-3 competition in 2008; Skein reached the final round. In 2011, Salmon, Moraes, Dror and Shaw observed that a strong cipher in counter mode is an excellent random number generator but more than is needed for simulation, and built Threefry by keeping Threefish's ARX structure while removing the tweak and most of the rounds, keeping just enough to pass BigCrush with a margin. Threefry joined Philox and ARS in the Random123 library and became the default generator of JAX, whose design of explicit, splittable keys relies on its counter-based interface.

## References
