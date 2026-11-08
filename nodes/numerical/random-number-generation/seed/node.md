---
tag: 8Q8SEB
kind: definition
slug: seed
name: Seed
aliases:
- random seed
- seed value
- seeding
area: numerical/random-number-generation
level: intro
summary: The initial value that fully determines a pseudorandom generator's output sequence.
prereqs: [pseudorandom-number-generator, generator-period]
see_also: [entropy-source, true-random-number-generator, splitmix64, jump-ahead, min-entropy, birthday-paradox, cryptographically-secure-prng]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.2.1 (the starting value X_0 of a congruential sequence) and Section 3.6, Summary (advice on the choice of the seed)
  - paper: "Pierre L'Ecuyer, Uniform random number generation, Annals of Operations Research 53, 1994, pages 77 to 120"
    locator: Section 2 (the initial state chosen from a distribution on the state space)
  - paper: doi:10.1145/272991.272995
    title: Makoto Matsumoto and Takuji Nishimura, Mersenne Twister, a 623-dimensionally equidistributed uniform pseudo-random number generator, ACM Transactions on Modeling and Computer Simulation 8(1), 1998, pages 3 to 30
    locator: the initialization of the state array from a 32-bit seed and the forbidden all-zero state
  - paper: "Ian Goldberg and David Wagner, Randomness and the Netscape browser, Dr. Dobb's Journal, January 1996"
    locator: the recovery of SSL session keys from a seed made of the time of day and process ids
  - url: https://nvd.nist.gov/vuln/detail/CVE-2008-0166
    title: National Vulnerability Database, CVE-2008-0166 (the Debian OpenSSL random number generator)
    locator: the description (the process id was the only varying input to the seed, so the keys were guessable)
---

A seed is the value from which a [pseudorandom number generator](/pseudorandom-number-generator/) computes its start state. The generator is deterministic, so the seed fixes the full output sequence: the same seed gives the same numbers, and the number of different sequences is at most the number of different seeds. A seed must avoid the states that the generator forbids, and for security it must be unpredictable, which a [true random number generator](/true-random-number-generator/) or an [entropy source](/entropy-source/) provides.

## Definition

Let a generator have the state space $S$, the transition function $f$ and the output function $g$, with $s_{i+1} = f(s_i)$ and $u_i = g(s_i)$. A *seed space* is a finite set $\Sigma$, and a *seeding function* is a map $h : \Sigma \to S$. A *seed* is an element $\sigma \in \Sigma$. The start state is $s_0 = h(\sigma)$, and the output sequence is

$$u_i = g(f^i(h(\sigma))), \qquad i = 0, 1, 2, \ldots$$

Three facts follow at once from this definition.

1. **Reproducibility.** The map $\sigma \mapsto (u_0, u_1, \ldots)$ is a function. Two runs with the same seed give the same sequence.
2. **Counting bound.** For each $n$, the first $n$ outputs take at most $|h(\Sigma)| \le \min(|\Sigma|, |S|)$ values. A 32-bit seed gives at most $2^{32}$ different sequences, whatever the size of $S$.
3. **Entropy bound.** If the seed is a random variable $\sigma$, then each output block $(u_0, \ldots, u_{n-1})$ is a function of $\sigma$, so its [min-entropy](/min-entropy/) is at most the min-entropy of $\sigma$. An attacker who can guess the seed with probability $p$ can guess the full sequence with probability at least $p$.

A *valid* seed is one with $h(\sigma)$ in the set of allowed start states. For a generator that is linear over GF(2), such as [xorshift](/xorshift/), the zero state is a fixed point of $f$, so a valid seed must give a non-zero state. For a multiplicative congruential generator with modulus $m$, the state 0 is a fixed point, so the seed must be in $\{1, \ldots, m - 1\}$.

## Examples and non-examples

**Examples.**

- [MT19937](/mersenne-twister/) with the reference function `init_genrand` maps a 32-bit seed to its 624-word state by a recurrence. The default seed 5489 gives the first output 3499211612. Python's `random.seed(n)` uses a different seeding function (`init_by_array` on the 32-bit pieces of $n$), so the same algorithm seeded with 42 gives 1608637542 in C++ (`std::mt19937(42)`) and 2746317213 in Python (`getrandbits(32)` after `seed(42)`). The seed alone does not fix the sequence: the seeding function is part of the definition.
- The authors of [xoshiro256**](/xoshiro-xoroshiro/) advise to fill its 256-bit state from a 64-bit seed with [SplitMix64](/splitmix64/). SplitMix64 is a bijection on 64-bit words, so four calls never give the forbidden all-zero state from one seed: its first output for the seed 0 is 16294208416658607535, not 0.
- [PCG32](/pcg-random/) takes two seeds: a 64-bit start value and a stream selector. The demo program seeds with $(42, 54)$ and its first output is `0xa15c02b7`.
- For [Philox](/philox/) and [Threefry](/threefry/), the key plays the role of the seed, and the counter selects the position in the sequence.
- A cryptographic generator such as [HMAC_DRBG](/hmac-drbg/) takes its seed from an [entropy source](/entropy-source/), and NIST SP 800-90A requires a seed with at least as much entropy as the security strength.

**Non-examples.**

- The counter of a counter-based generator is not a seed. Two different counters under the same key give two positions of one sequence, not two sequences.
- The current state in the middle of a run is not a seed in the sense above when $h$ is not onto. For MT19937 only $2^{32}$ of the $2^{19937} - 1$ non-zero states are images of `init_genrand`, so most states are not start states of any seed.
- A stream of bits from a physical source is not a seed of anything until it is passed through a seeding function.

**Pitfalls.**

- **Seeds from the clock.** A seed made from the time in seconds has few possible values, and parallel jobs that start in the same second get the same sequence. In 1995 the Netscape browser seeded its SSL generator from the time of day and process ids, and Goldberg and Wagner recovered session keys by search over the seeds. In the Debian OpenSSL bug (CVE-2008-0166, 2006 to 2008) the process id was the only input that varied, so only a few tens of thousands of keys of each type could appear.
- **Short seeds and many streams.** With $n$ jobs that draw independent uniform $k$-bit seeds, the probability that two jobs share a seed is about $1 - e^{-n(n-1)/2^{k+1}}$ (the [birthday paradox](/birthday-paradox/)). For $k = 32$ it passes $1/2$ at $n = 77{,}163$ jobs, and for $n = 10^5$ it is about 0.69. For $k = 64$ and $n = 10^5$ it is about $2.7 \times 10^{-10}$.
- **Nearby seeds.** With a weak seeding function, the seeds 1 and 2 give start states that differ in few bits, and a linear generator then gives sequences that stay similar for many steps. A good seeding function mixes the seed, for example with SplitMix64.
- **The forbidden state.** A seed of 0 for xorshift, or a seed that is a multiple of $m$ for the [Park-Miller generator](/park-miller-minimal-standard/), gives the constant sequence 0.

## Related definitions

- [Pseudorandom number generator](/pseudorandom-number-generator/): the state machine that the seed starts.
- [Period](/generator-period/): the length of the cycle that the seeded sequence enters.
- [Jump-ahead](/jump-ahead/): a way to get many non-overlapping streams from one seed, by moving the state far along one sequence.
- [Entropy source](/entropy-source/) and [true random number generator](/true-random-number-generator/): where an unpredictable seed comes from.
- [Min-entropy](/min-entropy/): the measure of how hard a seed is to guess.

## References
