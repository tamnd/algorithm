---
tag: JXHPPT
kind: algorithm
slug: philox
name: Philox
aliases:
- Philox counter-based RNG
- Philox4x32-10
- Philox4x64
- Random123 Philox
area: numerical/random-number-generation
level: advanced
summary: A counter-based generator where output is a keyed round function of a counter, enabling parallel streams.
model: word-ram
complexity:
  vars: {R: "the number of rounds, 10 by default", n: "the number of words per block, 2 or 4"}
  time: {worst: Θ(R n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, in_place: true, recursive: false}
prereqs: [pseudorandom-number-generator, feistel-network, block-cipher]
see_also: [threefry, splitmix64, pcg-random, avalanche-effect, chacha20, cryptographically-secure-prng, jump-ahead, statistical-tests-for-randomness]
sources:
  - paper: doi:10.1145/2063384.2063405
    title: John K. Salmon, Mark A. Moraes, Ron O. Dror and David E. Shaw, Parallel random numbers, as easy as 1, 2, 3, Proceedings of the International Conference for High Performance Computing, Networking, Storage and Analysis (SC11), 2011, Article 16
    locator: "Section 3 on counter-based generators, Section 5 on the Philox round function, its multipliers and key schedule, and the tables of TestU01 results by number of rounds"
  - url: https://github.com/DEShawResearch/random123
    title: D. E. Shaw Research, Random123, a library of counter-based random number generators
    locator: "the header philox.h (the constants PHILOX_M4x32_0, PHILOX_M4x32_1, PHILOX_W32_0, PHILOX_W32_1 and the 64-bit ones) and the file examples/kat_vectors used by the tests"
  - paper: doi:10.1145/1268776.1268777
    title: Pierre L'Ecuyer and Richard Simard, TestU01, a C library for empirical testing of random number generators, ACM Transactions on Mathematical Software 33(4), 2007, Article 22
    locator: the SmallCrush, Crush and BigCrush batteries used to choose the number of rounds
---

Philox is a counter-based random number generator, introduced by John Salmon, Mark Moraes, Ron Dror and David Shaw in 2011 as part of the Random123 library. The $i$-th output block is simply $\Phi_K(i)$: a fixed function of a key $K$ and a counter $i$, built from $R$ rounds of a cheap invertible mixing step. There is no evolving state. So any block can be computed directly, any number of threads can draw from disjoint counter ranges or distinct keys without coordination, and a simulation can be replayed from any point. Philox4x32-10, which maps a 128-bit counter and a 64-bit key to 128 output bits in 10 rounds of two $32 \times 32 \to 64$-bit multiplications, is the default parallel generator in several GPU and machine-learning libraries.

## In plain words

Most generators keep a hidden state and update it each time you ask for a number, so number one thousand is only reachable by producing the 999 before it. Philox works the other way. You give it a position, 0, 1, 2 and so on, and a key, and it scrambles the position into a random-looking block of bits.

The scrambling is ten repetitions of the same step: multiply two of the words by fixed odd constants, then cross the high and low halves of the products with the other words and the key. Every step can be undone, so different positions never give the same block. Because each position is handled on its own, a thousand processors can each take their own positions or their own key and never step on each other.

## The problem

We use the notation of the [pseudorandom number generator](/pseudorandom-number-generator/) page. A counter-based generator has state $S = \{0, \ldots, 2^{nw} - 1\}$, the counter, with the trivial transition $f(i) = i + 1 \bmod 2^{nw}$, and puts all the work into the output function $g = \Phi_K$, which maps the counter to a block of $n$ words of $w$ bits. The task is to design $\Phi_K$ so that $\Phi_K(0), \Phi_K(1), \ldots$ pass the strongest statistical tests, for every key, while costing as few word operations per output as possible. A block cipher such as AES would do, but costs more; Philox weakens the cipher until it is just strong enough statistically.

## The algorithm

Philox4x32 has multipliers $M_0 = \texttt{0xD2511F53}$, $M_1 = \texttt{0xCD9E8D57}$ and key increments $W_0 = \texttt{0x9E3779B9}$, $W_1 = \texttt{0xBB67AE85}$ (the golden ratio and $\sqrt{3} - 1$ as 32-bit fractions). All arithmetic is modulo $2^{32}$, except the products, which are kept to 64 bits and split into a high word and a low word.

```pseudo id=main
PHILOX4X32(X, K, R)        ▷ X = (x0, x1, x2, x3): counter; K = (k0, k1): key; R = 10 by default
L1  repeat R times
L2      (h0, l0) ← high and low words of M0 · x0
L3      (h1, l1) ← high and low words of M1 · x2
L4      X ← (h1 ⊕ x1 ⊕ k0, l1, h0 ⊕ x3 ⊕ k1, l0)
L5      K ← (k0 + W0 mod 2^32, k1 + W1 mod 2^32)
L6  return X
```

To produce a stream, call PHILOX4X32 on the counter values $0, 1, 2, \ldots$ (as 128-bit integers split into four words, low word first) and use the four output words in order. Philox2x32 has one multiplier, $\texttt{0xD256D193}$, and the round $(x_0, x_1) \leftarrow (\mathrm{hi}(M x_0) \oplus x_1 \oplus k, \mathrm{lo}(M x_0))$; Philox2x64 and Philox4x64 use 64-bit words with $128$-bit products and 64-bit constants.

## Example

With counter $(\texttt{243f6a88}, \texttt{85a308d3}, \texttt{13198a2e}, \texttt{03707344})$ and key $(\texttt{a4093822}, \texttt{299f31d0})$, the digits of $\pi$ used in Random123's known-answer tests, the first round computes $M_0 x_0 = \texttt{1dc781e3}\,\texttt{b37e0218}$, so $h_0 = \texttt{1dc781e3}$ and $l_0 = \texttt{b37e0218}$, and the state after each round is:

| round | $x_0$ | $x_1$ | $x_2$ | $x_3$ |
|---|---|---|---|---|
| 0 | 243f6a88 | 85a308d3 | 13198a2e | 03707344 |
| 1 | 2efd7704 | ad2d4ba2 | 3728c377 | b37e0218 |
| 2 | c320345a | 20f4f871 | 70e22dde | dddb124c |
| 7 | 4dfccaba | 190a87f0 | c47362ba | b6b5242a |
| 10 | d16cfe09 | 94fdcceb | 5001e420 | 24126ea1 |

The rows for 7 and 10 rounds are the published outputs of Philox4x32-7 and Philox4x32-10. With key 0, the counters 0 and 1 give $(\texttt{6627e8d5}, \texttt{e169c58d}, \texttt{bc57ac4c}, \texttt{9b00dbd8})$ and $(\texttt{f8e4cca4}, \texttt{5cb200db}, \texttt{b1a574eb}, \texttt{097eff67})$: adjacent counters give unrelated blocks. The implementation reproduces all 24 Philox known-answer vectors of Random123.

## Correctness

The proof file proves the structural property; the statistical quality is empirical.

1. **Each round is invertible.** The multipliers are odd, hence invertible modulo $2^w$, so $x_0$ and $x_2$ are recovered from the low words $l_0$ and $l_1$; then $x_1$ and $x_3$ are recovered by XORing out the high words and the key.
2. **Counter mode never repeats.** For a fixed key, $\Phi_K$ is a composition of bijections, hence a permutation of the $2^{128}$ counter values: distinct counters give distinct blocks, and the stream has period $2^{128}$ blocks.
3. **Random access.** Block $i$ depends only on $i$ and $K$, so skipping ahead by any amount costs nothing.

## Complexity

Each block of $n$ words costs $R$ rounds of $n/2$ full multiplications and $n$ XORs plus the key update: $\Theta(R n)$ word operations, $\Theta(R)$ per output word. For Philox4x32-10, that is 20 multiplications for 128 bits, which on GPUs, with fast multiply-high instructions, makes it among the fastest generators available. The working space is the $n$ words of the block and the $n/2$ key words. Jumping to any position costs one block evaluation.

## Properties

- **Proved:** for every key and every number of rounds, distinct counters give distinct outputs; the period is $2^{128}$ blocks for Philox4x32 and $2^{256}$ for Philox4x64.
- **Empirical:** the authors report that Philox4x32 with 7 or more rounds passes TestU01's SmallCrush, Crush and BigCrush for many keys and counter patterns, and chose 10 rounds as the default for a safety margin; fewer rounds fail. The tests here measure the avalanche: flipping one counter bit flips on average 64.0 of the 128 output bits with 10 rounds, but only about 27 with 2 rounds.
- **Splittable by key.** Each key gives a different permutation, so distinct keys (for example, thread numbers) give independent-looking streams, $2^{64}$ of them for Philox4x32.
- **Not cryptographic.** Philox has no security analysis comparable to a real block cipher, and the authors make no security claim. Do not use it for keys, tokens or anything an attacker may try to predict.

## Variants and improvements

- **Philox2x32, Philox2x64, Philox4x64.** Other block sizes; NumPy's `Philox` bit generator uses Philox4x64-10.
- **[Threefry](/threefry/).** The other Random123 family, based on the add, rotate and XOR rounds of the Threefish cipher; faster on CPUs without fast multiply-high instructions.
- **ARS.** A third Random123 family using the AES round instruction with a simplified key schedule.
- **Cryptographic counter mode.** AES in counter mode or [ChaCha20](/chacha20/) give security as well, at a few times the cost.
- **Stateful splittable generators.** [SplitMix64](/splitmix64/) and the stream parameter of [PCG](/pcg-random/) also give many streams, but each stream has to be advanced in order.

## When to use it

Use Philox for parallel and reproducible simulation: on GPUs, in multi-threaded or distributed Monte Carlo, and in machine-learning frameworks where each operation needs its own random numbers determined by a seed and an operation index. Give each thread or task its own key, or its own counter range, and the results do not depend on the scheduling. For a single sequential stream on a CPU, a small stateful generator such as [xoshiro256**](/xoshiro-xoroshiro/) is faster. For security, use a [cryptographically secure generator](/cryptographically-secure-prng/).

## Pitfalls

- **Overlapping counter ranges.** Two tasks with the same key and overlapping counter ranges produce identical numbers. Partition the counter space, for example by putting the task number in the high counter words, or give each task a distinct key.
- **Reducing the rounds.** Fewer rounds are faster, but the margin is thin: the avalanche test here already fails badly at 2 rounds, and the authors report statistical failures below 7. Keep 10 unless you have tested the reduced version.
- **Word order and endianness.** Implementations differ in how they split a 128-bit counter into words and in the order the output words are used. Match the reference order when reproducing results across libraries.
- **Treating the key as a secret.** Philox was designed to pass statistical tests, not to resist cryptanalysis, and nothing is known that makes recovering the key or predicting later blocks from earlier ones hard. Do not rely on a secret key for confidentiality.
- **Unmasked arithmetic.** In languages with unbounded integers, the key additions must be reduced modulo $2^{32}$, and the products split exactly at bit 32.

## Implementations

## History

Salmon, Moraes, Dror and Shaw, of D. E. Shaw Research, presented counter-based generators at the SC11 conference in 2011 ("Parallel random numbers, as easy as 1, 2, 3"), motivated by molecular dynamics on massively parallel machines. Starting from the observation that encrypting a counter with a block cipher gives an excellent generator, they reduced the cost by keeping only as many rounds of simple bijections as needed to pass TestU01's BigCrush, which gave the Philox, Threefry and ARS families of the Random123 library. Philox4x32-10 was then adopted in NVIDIA's cuRAND and in machine-learning frameworks such as TensorFlow and PyTorch for GPU random numbers, and Philox4x64 in NumPy; a `philox_engine` was added to the C++26 standard library.

## References
