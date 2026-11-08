---
tag: QTA94K
kind: concept
slug: true-random-number-generator
name: True random number generator
aliases:
- TRNG
- hardware random number generator
- physical random number generator
- HRNG
area: numerical/random-number-generation
level: intro
summary: A generator that extracts randomness from physical processes rather than from a deterministic recurrence.
prereqs: [pseudorandom-number-generator, min-entropy]
see_also: [entropy-source, seed, randomness-extractor, von-neumann-debiasing, unbiased-bits-from-biased-coin, cryptographically-secure-prng, ctr-drbg]
sources:
  - paper: doi:10.6028/NIST.SP.800-90B
    title: Meltem Sönmez Turan, Elaine Barker, John Kelsey, Kerry A. McKay, Mary L. Baish and Mike Boyle, NIST Special Publication 800-90B, Recommendation for the Entropy Sources Used for Random Bit Generation, 2018
    locator: Section 2 (the model of an entropy source with a noise source, a conditioning component and health tests), Section 4.4 (the repetition count test and the adaptive proportion test) and Section 6 (min-entropy estimation)
  - paper: doi:10.6028/NIST.SP.800-90Ar1
    title: Elaine Barker and John Kelsey, NIST Special Publication 800-90A Revision 1, Recommendation for Random Number Generation Using Deterministic Random Bit Generators, 2015
    locator: Section 8.6 (seeds for a DRBG come from an approved entropy source)
  - paper: "John von Neumann, Various techniques used in connection with random digits, in Monte Carlo Method, National Bureau of Standards Applied Mathematics Series 12, 1951, pages 36 to 38"
    locator: the method of taking pairs of biased bits and keeping 01 and 10, and the remark that arithmetic methods only give pseudorandom digits
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.1, Introduction (tables of random digits made by physical devices and their drawbacks)
---

A true random number generator (TRNG) produces random bits by measuring a physical process, such as electrical noise or the timing jitter of an oscillator, instead of by a deterministic rule. Its output cannot be reproduced from a [seed](/seed/), and its quality is measured by [min-entropy](/min-entropy/), not by a period. Raw physical bits are biased and correlated, so a TRNG always has a conditioning step and health tests, and in practice it seeds a [cryptographically secure PRNG](/cryptographically-secure-prng/) instead of being used directly.

## In plain words

A program that follows fixed rules can only make numbers that look random. A true random number generator gets its randomness from the physical world: the tiny, unpredictable changes of a voltage, the moment a radioactive atom decays, or how long an electronic clock wavers.

Such measurements are not fair coins. A noise signal can give more ones than zeros, and one sample can depend on the one before it. So the device first estimates how much real unpredictability each sample holds, then compresses many raw samples into fewer good bits, and it checks all the time that the physical part has not failed.

Real devices are slow compared with a formula. So computers use a small amount of true randomness to start a fast, secure formula.

## The idea

A TRNG has three parts, in the model of NIST SP 800-90B:

1. A **noise source**: a physical process sampled to give raw symbols $x_1, x_2, \ldots$. Common sources are thermal noise in a resistor or diode, the jitter of free-running ring oscillators, metastable latches, photon detectors and radioactive decay.
2. A **conditioning component**: a function that maps a block of raw symbols to fewer output bits that are closer to uniform. Examples are the [von Neumann method](/von-neumann-debiasing/), a cryptographic hash, and a block-cipher CBC-MAC.
3. **Health tests** that run during operation and stop the output when the noise source fails.

The amount of randomness is measured by min-entropy. For a source symbol $X$,

$$H_\infty(X) = -\log_2 \max_x \Pr[X = x].$$

It is the right measure because an attacker who guesses the most likely value succeeds with probability $2^{-H_\infty(X)}$. Shannon entropy can be large while one value is very likely, so it overstates security. A [randomness extractor](/randomness-extractor/) can turn a block of total min-entropy $k$ into about $k$ bits that are close to uniform, but no deterministic function can do this for every source: one extra uniform seed, or an assumption on the source, is necessary.

What is proved and what is not:

- The von Neumann method is exactly unbiased under a stated model: the raw bits are independent and each is 1 with the same unknown probability $p$, with $0 < p < 1$. Then $\Pr[01] = \Pr[10] = p(1-p)$. If the bits are correlated, the output can be biased. See [unbiased bits from a biased coin](/unbiased-bits-from-biased-coin/).
- The min-entropy of a physical source is not proved. It is estimated, either from a stochastic model of the physics or by the statistical estimators of SP 800-90B Section 6, and the estimate is only as good as the model.
- Health tests detect gross failures, such as a stuck output. They do not prove that the output is random.

A TRNG differs from a [pseudorandom number generator](/pseudorandom-number-generator/) in four ways: it has no period, it cannot be repeated, its rate is limited by the physics (often kilobits to a few megabits per second), and its output distribution is not known exactly.

## Examples

**Von Neumann conditioning.** Take the raw bits 1 1 0 1 1 0 0 0 1 0 and cut them into pairs: 11, 01, 10, 00, 10. Drop 00 and 11, and output the first bit of each other pair. The output is 0, 1, 1. For independent bits with $p = 0.7$, a pair gives an output with probability $2p(1 - p) = 0.42$, so the rate is $0.21$ output bits for each raw bit, while the min-entropy of a raw bit is $-\log_2 0.7 \approx 0.515$. The method is exact but wastes more than half of the available entropy.

**Repetition count test.** SP 800-90B Section 4.4.1 stops the source when one value repeats $C$ times in a row, with

$$C = 1 + \left\lceil \frac{-\log_2 \alpha}{H} \right\rceil,$$

where $H$ is the claimed min-entropy per sample and $\alpha$ is the accepted false-alarm rate, with $\alpha = 2^{-20}$ advised. A source that claims $H = 1$ bit per sample stops after 21 equal samples, and one that claims $H = 0.5$ after 41. A working source with that entropy gives such a run with probability at most $\alpha$.

**Adaptive proportion test.** SP 800-90B Section 4.4.2 counts how often the first sample of a window appears in that window, with a window of 512 samples for binary sources and 1024 for others, and stops the source when the count passes a cutoff computed from the binomial distribution.

**Processor instructions.** Some processors have an on-chip noise source whose conditioned output seeds an on-chip [CTR_DRBG](/ctr-drbg/). An instruction such as RDSEED on x86 returns conditioned entropy, and RDRAND returns the output of the DRBG.

**Operating systems.** Linux `/dev/random` and `getrandom`, and the system generators of other operating systems, collect timing noise from interrupts and hardware sources, and use it to seed a cryptographic generator. Programs should read these interfaces instead of sampling hardware themselves.

## Where it is used

- Seeding a [cryptographically secure PRNG](/cryptographically-secure-prng/) such as [HMAC_DRBG](/hmac-drbg/), [Hash_DRBG](/hash-drbg/) or [CTR_DRBG](/ctr-drbg/). SP 800-90A requires that the seed of a DRBG come from an approved entropy source.
- Key generation, nonces and the masks of side-channel countermeasures, through such a seeded generator.
- Lotteries and gaming machines, where a regulator may require a physical source.
- Seeding simulation generators when the runs need not be reproducible. For reproducible simulation, a fixed [seed](/seed/) of a [pseudorandom number generator](/pseudorandom-number-generator/) is better.

## References
