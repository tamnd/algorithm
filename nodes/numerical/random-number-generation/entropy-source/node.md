---
tag: ZBMJCZ
kind: concept
slug: entropy-source
name: Entropy source
aliases:
- entropy pool
- noise source
area: numerical/random-number-generation
level: intro
summary: A physical or system process, with its digitization, health tests and conditioning, that supplies unpredictable bits to seed or reseed a generator.
prereqs: [min-entropy]
see_also: [true-random-number-generator, randomness-extractor, von-neumann-debiasing, seed, cryptographically-secure-prng, hmac-drbg, ctr-drbg, shannon-entropy]
sources:
  - paper: doi:10.6028/NIST.SP.800-90B
    title: Meltem Sonmez Turan, Elaine Barker, John Kelsey, Kerry McKay, Mary Baish and Mike Boyle, NIST Special Publication 800-90B, Recommendation for the Entropy Sources Used for Random Bit Generation, January 2018
    locator: Section 2 (the entropy source model, with noise source, digitization, conditioning and health tests), Section 4.4 (the repetition count test and the adaptive proportion test) and Section 6 (the min-entropy estimators)
  - paper: doi:10.6028/NIST.SP.800-90Ar1
    title: Elaine Barker and John Kelsey, NIST Special Publication 800-90A Revision 1, Recommendation for Random Number Generation Using Deterministic Random Bit Generators, June 2015
    locator: Section 8.6 (seeds, entropy input and the required min-entropy)
  - paper: "Nadia Heninger, Zakir Durumeric, Eric Wustrow and J. Alex Halderman, Mining your Ps and Qs: detection of widespread weak keys in network devices, Proceedings of the 21st USENIX Security Symposium, 2012"
    locator: the analysis of weak RSA and DSA keys caused by low entropy at boot time in embedded devices
  - paper: "Zvi Gutterman, Benny Pinkas and Tzachy Reinman, Analysis of the Linux random number generator, IEEE Symposium on Security and Privacy, 2006"
    locator: the description of the entropy pools and the sources of entropy of the Linux kernel generator
---

An entropy source is a process that produces bits that an attacker cannot predict, together with the steps that turn its raw signal into usable bits. It is the only input of a [cryptographically secure generator](/cryptographically-secure-prng/) that is truly random: the generator stretches a short [seed](/seed/) from the entropy source into a long output. The amount of unpredictability is measured in bits of [min-entropy](/min-entropy/), not in output bits.

## In plain words

A program cannot make true randomness by computing. So it collects it from the outside world: tiny timing differences in hardware, electrical noise, the moment when keys are pressed or packets arrive. These raw signals are messy. Some values come up more often than others, and nearby samples can depend on each other.

An entropy source does three jobs. It measures the noise and turns it into numbers. It checks all the time that the noise has not failed, for example stuck at one value. It mixes many raw samples into a few good bits. Those bits then seed a fast generator. The question that matters is not how many bits come out, but how hard the best guess at them is.

## The idea

**Min-entropy, not output length.** Let a raw sample $X$ take value $x$ with probability $p_x$. Its min-entropy is $H_\infty(X) = -\log_2 \max_x p_x$. An attacker who guesses the most likely value wins with probability $2^{-H_\infty}$, so min-entropy measures guessing work directly. The [Shannon entropy](/shannon-entropy/) $-\sum_x p_x \log_2 p_x$ can be much larger and is the wrong measure for security. For an 8-bit sample that is 0 with probability $1/2$ and uniform on the other 255 values, the Shannon entropy is about 4.997 bits, but the min-entropy is exactly 1 bit: the attacker guesses 0 and is right half the time.

**The model of NIST SP 800-90B.** The standard splits an entropy source into parts.

1. A *noise source*, the non-deterministic physical or system process, with a *digitization* step that turns it into raw samples.
2. *Health tests* that run all the time on the raw samples and stop output when the noise source fails.
3. An optional *conditioning component*, a deterministic function such as a hash, HMAC or CBC-MAC that compresses many raw samples into fewer bits with more min-entropy per bit.

The output of the source goes to a deterministic random bit generator such as [HMAC_DRBG](/hmac-drbg/), [Hash_DRBG](/hash-drbg/) or [CTR_DRBG](/ctr-drbg/). SP 800-90A asks that the entropy input at instantiation has at least as many bits of min-entropy as the security strength, for example 128 bits for a 128-bit strength.

**Health tests.** SP 800-90B, Section 4.4, requires two approved tests (or equivalents). Both assume a claimed min-entropy $H$ per sample and a false alarm probability $\alpha$, with $\alpha$ between $2^{-20}$ and $2^{-40}$.

- The *repetition count test* fails when one value repeats $C$ times in a row, with cutoff $C = 1 + \lceil (-\log_2 \alpha) / H \rceil$. With $\alpha = 2^{-20}$ the cutoff is 21 for $H = 1$, 41 for $H = 0.5$ and 6 for $H = 4$. It catches a source that gets stuck.
- The *adaptive proportion test* counts how often the first value of a window reappears in the window (1024 samples for binary data, 512 otherwise) and fails above a cutoff from the binomial distribution. It catches a large loss of entropy that is not a plain repeat.

These tests detect gross failure only. Passing them does not prove that the claimed $H$ is right.

**Estimation is the hard part.** The min-entropy of a physical process is not observable. SP 800-90B, Section 6, gives a set of estimators (most common value, collision, Markov, compression, prediction estimators and others) and takes the minimum of their results. They give an estimate from data, not a proof. A sound claim also needs a model of the physics of the noise, which the standard asks the designer to justify.

**Conditioning.** A deterministic function cannot add entropy, but it can concentrate it. With a [randomness extractor](/randomness-extractor/), $n$ raw bits with $k$ bits of min-entropy become about $k$ bits that are close to uniform. The simplest example is [von Neumann debiasing](/von-neumann-debiasing/): read bits in pairs, output 0 for the pair 01 and 1 for 10, and drop 00 and 11. For independent bits with $\Pr[1] = p$, the two kept pairs have the same probability $p(1-p)$, so the output is exactly uniform. With $p = 0.7$, a pair gives an output bit with probability $2p(1-p) = 0.42$. The independence hypothesis is necessary: for correlated bits the output is biased.

**Seed once, then reseed.** A cryptographic generator that has a good seed can produce a very long output safely, so the entropy source runs at a low rate. Reseeding later limits the damage after a compromise of the state. A generator with no entropy at all is deterministic, whatever its algorithm.

## Examples

- **Operating system pools.** The Linux kernel collects timings of interrupts, disk and input events, and CPU instructions such as RDSEED when they exist, mixes them into a pool, and serves `getrandom(2)` and `/dev/urandom` from a ChaCha20-based generator. Windows and the BSD systems have the same structure. Gutterman, Pinkas and Reinman analysed an older version of the Linux design.
- **Hardware generators.** Many processors and security chips have a noise source such as the jitter of free-running ring oscillators or a metastable latch. Intel's RDSEED instruction returns conditioned entropy, and RDRAND returns the output of a CTR_DRBG that the hardware source reseeds.
- **Low entropy at boot.** Heninger, Durumeric, Wustrow and Halderman (2012) scanned the public keys of internet hosts and found many RSA moduli that share a prime factor. They traced most of them to embedded devices that generated keys at first boot, before the kernel pool had any entropy.
- **The Debian OpenSSL bug.** From 2006 to 2008, a change to the Debian package of OpenSSL removed almost all entropy input. The only varying input left was the process identifier, at most 32768 values, so every key that the package generated came from a tiny known set (CVE-2008-0166).
- **A per-sample budget.** If a noise source is assessed at $H = 0.5$ bits of min-entropy per sample, a 128-bit seed needs at least 256 raw samples before conditioning, and in practice a margin above that.

## Where it is used

Each cryptographic use of randomness starts at an entropy source: keys, nonces, salts, the seeds of [Hash_DRBG](/hash-drbg/), [HMAC_DRBG](/hmac-drbg/) and [CTR_DRBG](/ctr-drbg/), and the per-signature value of DSA and ECDSA. A [true random number generator](/true-random-number-generator/) is an entropy source that delivers its conditioned output directly. Simulations usually take only a seed from an entropy source, or a fixed seed for reproducibility, and then use a fast statistical generator such as the [Mersenne Twister](/mersenne-twister/).

## References
