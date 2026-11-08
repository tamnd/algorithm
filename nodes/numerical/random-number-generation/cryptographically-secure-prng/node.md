---
tag: RNE8SQ
kind: definition
slug: cryptographically-secure-prng
name: Cryptographically secure pseudorandom generator
aliases:
- CSPRNG
- CSPRG
- cryptographically secure pseudorandom number generator
area: numerical/random-number-generation
level: advanced
summary: A seeded generator whose output no efficient algorithm can tell from uniform bits, and whose leaked state reveals no earlier outputs.
prereqs: [pseudorandom-generator, computational-indistinguishability, entropy-source]
see_also: [yao-next-bit-unpredictability, one-way-function, blum-blum-shub, hmac-drbg, ctr-drbg, dual-ec-drbg, mersenne-twister, chacha20]
sources:
  - book: isbn:9780521791724
    title: Oded Goldreich, Foundations of Cryptography, Volume 1, Basic Tools, Cambridge University Press, 2001
    locator: Chapter 3, Pseudorandom generators (definition by computational indistinguishability, the next-bit test, and constructions from one-way permutations)
  - paper: "Andrew C. Yao, Theory and applications of trapdoor functions, 23rd IEEE Symposium on Foundations of Computer Science, 1982, pages 80 to 91"
    locator: the equivalence of passing the next-bit test and passing all polynomial-time statistical tests
  - paper: "Manuel Blum and Silvio Micali, How to generate cryptographically strong sequences of pseudo-random bits, SIAM Journal on Computing 13(4), 1984, pages 850 to 864"
    locator: the definition of cryptographically strong generators and the construction from the discrete logarithm
  - paper: "Johan Håstad, Russell Impagliazzo, Leonid A. Levin and Michael Luby, A pseudorandom generator from any one-way function, SIAM Journal on Computing 28(4), 1999, pages 1364 to 1396"
    locator: the main theorem that pseudorandom generators exist if and only if one-way functions exist
  - paper: "Boaz Barak and Shai Halevi, A model and architecture for pseudo-random generation with applications to /dev/random, ACM Conference on Computer and Communications Security, 2005"
    locator: the security model with state compromise, forward security and recovery through refreshing
  - paper: doi:10.6028/NIST.SP.800-90Ar1
    title: Elaine Barker and John Kelsey, NIST Special Publication 800-90A Revision 1, Recommendation for Random Number Generation Using Deterministic Random Bit Generators, June 2015
    locator: the definitions of security strength, backtracking resistance, prediction resistance and reseeding
---

A cryptographically secure pseudorandom generator (CSPRNG) expands a short secret seed into a long stream of bits that no efficient algorithm can tell apart from independent fair coin flips. The formal definition is the [pseudorandom generator](/pseudorandom-generator/) of complexity theory: computational indistinguishability against every probabilistic polynomial-time test. Practical generators add requirements about state: leaking the current state must not reveal past outputs, and fresh entropy must restore security after a leak. Statistical quality is not enough; the Mersenne Twister passes most statistical tests and is fully predictable from 624 outputs.

## Definition

Let $n$ be the security parameter and $\ell(n) > n$ a polynomial. A function $\varepsilon(n)$ is *negligible* if $\varepsilon(n) < 1/p(n)$ for every polynomial $p$ and all large enough $n$. Let $U_k$ denote a uniform string in $\{0,1\}^k$.

**Pseudorandom generator (asymptotic).** A deterministic polynomial-time function $G : \{0,1\}^n \to \{0,1\}^{\ell(n)}$ is a cryptographically secure pseudorandom generator if for every probabilistic polynomial-time algorithm $D$ (the *distinguisher*), the advantage
$$\operatorname{Adv}_D(n) = \big| \Pr[D(G(U_n)) = 1] - \Pr[D(U_{\ell(n)}) = 1] \big|$$
is negligible.

**Next-bit unpredictability.** $G$ passes the *next-bit test* if for every probabilistic polynomial-time predictor $A$ and every $i < \ell(n)$, given the first $i$ output bits of $G(U_n)$, $A$ guesses bit $i + 1$ with probability at most $\tfrac12 + \varepsilon(n)$, $\varepsilon$ negligible. Yao's theorem says the two definitions are equivalent ([Yao's next-bit theorem](/yao-next-bit-unpredictability/)): a distinguisher with advantage $\delta$ yields a predictor with advantage at least $\delta / \ell$, and a predictor yields a distinguisher directly.

**Concrete security.** In practice $G$ is fixed and the statement is quantitative: $G$ is $(t, \varepsilon)$-secure if no distinguisher running in time $t$ has advantage more than $\varepsilon$. A generator has *security strength* $k$ bits if attacks need about $2^k$ work, as in NIST SP 800-90A.

**Stateful generators.** A deployed CSPRNG keeps a state $s$, and has three operations: $\mathrm{seed}$ (set $s$ from entropy input), $\mathrm{next}$ (output bits and update $s$ by a transition $f$), and $\mathrm{reseed}$ (mix fresh entropy into $s$). Beyond pseudorandom output, it should provide:

- **Backtracking resistance (forward security).** An adversary who learns the state at time $t$ cannot distinguish the outputs produced before $t$ from uniform. This forces the update $f$ to be one-way in effect.
- **Prediction resistance (recovery).** After a compromise of the state, once the generator has been reseeded with enough [min-entropy](/min-entropy/) from an [entropy source](/entropy-source/), later outputs are again indistinguishable from uniform.

Barak and Halevi (2005) gave a model with these properties; SP 800-90A defines them for its deterministic random bit generators.

## Examples and non-examples

**Provable generators, under assumptions.**

- [Blum-Blum-Shub](/blum-blum-shub/) is a CSPRNG if factoring Blum integers is hard. It is slow: one modular squaring per few output bits.
- The [Blum-Micali generator](/blum-micali/) is a CSPRNG if discrete logarithms modulo $p$ are hard.
- In general, a CSPRNG exists if and only if a [one-way function](/one-way-function/) exists (Håstad, Impagliazzo, Levin and Luby). Whether either exists is open; their existence would imply $\mathrm{P} \ne \mathrm{NP}$.

**Practical generators, under assumptions on primitives.** [HMAC_DRBG](/hmac-drbg/), [Hash_DRBG](/hash-drbg/) and [CTR_DRBG](/ctr-drbg/) from SP 800-90A are secure if HMAC, the hash function or the block cipher behave as pseudorandom functions; stream ciphers such as [ChaCha20](/chacha20/) in counter mode serve the same role (the Linux kernel generator uses ChaCha20). These reductions are to assumptions about the primitives, not to number-theoretic problems.

**Non-examples.**

- **Linear congruential generators.** For $m = 2^w$ with odd $a$ and $c$, $s_{i+1} \equiv s_i + 1 \pmod 2$, so the low bit alternates and a predictor guesses it with probability 1. Even with only the high bits output, the state is recovered from a few outputs by lattice reduction (Frieze, Håstad, Kannan, Lagarias and Shamir 1988). See [linear congruential generator](/linear-congruential-generator/).
- **Mersenne Twister.** The output function is invertible and the transition is linear over $\mathbb{F}_2$, so 624 consecutive 32-bit outputs give the full state and every later output. See [Mersenne Twister](/mersenne-twister/).
- **Other fast statistical generators.** [Xorshift](/xorshift/), [xoshiro](/xoshiro-xoroshiro/), [PCG](/pcg-random/) and [SplitMix64](/splitmix64/) are designed to pass statistical tests at high speed. None is claimed to be cryptographically secure by its designers, and practical state recovery attacks exist for several.
- **Dual_EC_DRBG.** Its outputs are slightly biased, and whoever knows the discrete logarithm relating its two curve points can predict all output after seeing about 32 bytes. NIST recommended against it in 2013 and removed it in the 2015 revision of SP 800-90A. See [Dual_EC_DRBG](/dual-ec-drbg/).
- **A good algorithm with a bad seed.** A CSPRNG seeded with 15 bits of entropy has at most $2^{15}$ possible output streams; trying them all is a distinguisher. The Debian OpenSSL weakness of 2008 was of this kind.

**Why the seed must be long.** For any $G : \{0,1\}^n \to \{0,1\}^{\ell}$, the distinguisher "output 1 if the input equals $G(x)$ for some seed $x$" runs in time about $2^n$ evaluations of $G$ and has advantage at least $1 - 2^{n - \ell}$, since at most $2^n$ of the $2^\ell$ strings are outputs. So security strength never exceeds the seed length, and 128 to 256 bits of seed entropy are standard.

## Related definitions

- **[Pseudorandom generator](/pseudorandom-generator/)** and **[computational indistinguishability](/computational-indistinguishability/)** are the complexity-theoretic definitions behind the first requirement.
- **[Pseudorandom function](/pseudorandom-function/).** Most practical CSPRNGs are built from a keyed PRF or block cipher by running it in counter mode and rekeying after each request, which gives backtracking resistance.
- **[True random number generator](/true-random-number-generator/)** and **[entropy source](/entropy-source/).** These provide the seed. A CSPRNG adds no entropy; its output has at most as much min-entropy as its seed.
- **[Statistical tests for randomness](/statistical-tests-for-randomness/).** Passing TestU01 or PractRand is necessary for a CSPRNG and very far from sufficient: the tests are fixed and public, while the definition quantifies over all efficient tests, including those that know the algorithm.
- **[Pseudorandom number generator](/pseudorandom-number-generator/)** in the simulation sense asks only for statistical quality and speed.

## References
