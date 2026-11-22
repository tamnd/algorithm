---
tag: RM91H8
kind: concept
slug: side-channel-attack
name: Side-channel attack
aliases:
- side-channel analysis
area: security-and-privacy/side-channel-attacks
level: intro
summary: "An attack that learns secrets from physical or timing effects of a computation, such as time, power, radiation or cache state."
history:
  year: 1996
  people: [Paul C. Kocher, Joshua Jaffe, Benjamin Jun]
  note: "Kocher showed timing attacks on public-key implementations in 1996, and Kocher, Jaffe and Jun showed simple and differential power analysis in 1999."
prereqs: []
see_also: [timing-attack, simple-power-analysis, differential-power-analysis, boolean-masking, constant-time-programming, test-vector-leakage-assessment, side-channel-key-rank-estimation, noninterference]
sources:
  - paper: "Paul C. Kocher, Timing attacks on implementations of Diffie-Hellman, RSA, DSS, and other systems, CRYPTO 1996, LNCS 1109, pages 104 to 113"
    locator: the observation that the running time of an implementation depends on the secret, and the first countermeasures
  - paper: "Paul Kocher, Joshua Jaffe and Benjamin Jun, Differential power analysis, CRYPTO 1999, LNCS 1666, pages 388 to 397"
    locator: simple power analysis, differential power analysis, and the general discussion of countermeasures
  - paper: "Stefan Mangard, Elisabeth Oswald and Thomas Popp, Power Analysis Attacks, Springer, 2007, ISBN 978-0-387-30857-9"
    locator: "Chapter 1 (side-channel attacks among the attacks on cryptographic devices) and Chapter 3 (leakage models)"
  - paper: doi:10.1007/978-3-642-01001-9_26
    title: "François-Xavier Standaert, Tal G. Malkin and Moti Yung, A unified framework for the analysis of side-channel key recovery attacks, EUROCRYPT 2009, LNCS 5479, pages 443 to 461"
    locator: the separation of the leakage of an implementation (an information measure) from the power of an attack (the success rate and the guessing entropy)
  - paper: doi:10.1007/3-540-48405-1_26
    title: "Suresh Chari, Charanjit S. Jutla, Josyula R. Rao and Pankaj Rohatgi, Towards sound approaches to counteract power-analysis attacks, CRYPTO 1999, LNCS 1666, pages 398 to 412"
    locator: the secret sharing countermeasure and the bound on the number of traces in a model with Gaussian noise on each share
---

A side-channel attack learns a secret from the way a computation runs, not from its inputs and outputs. The algorithm can be correct and the cipher can be strong: if the time, the power use, the electromagnetic radiation or the state of a shared cache depends on the key, then an observer of that effect sees a function of the key. Kocher (1996) showed it for the running time of public-key code, the [timing attack](/timing-attack/), and Kocher, Jaffe and Jun (1999) for the power use of smart cards, with [simple](/simple-power-analysis/) and [differential power analysis](/differential-power-analysis/). The answers are to make the observed effect independent of the secret, as in [constant-time programming](/constant-time-programming/), or to make each observed value independent of the secret by randomization, as in [Boolean masking](/boolean-masking/).

## In plain words

A program can keep a secret in its output and still give it away in how it works. A lock that clicks once for each right digit tells you the code. A chip that uses a little more power for each 1 bit it moves tells you how many 1 bits a secret value has. One such hint is weak and noisy. But the attacker can watch the chip many times with different inputs and use statistics to put the hints together. The usual trick is to guess a small part of the key, predict the hint for each run, and keep the guess whose predictions match what was seen. Defences either remove the hint, by making the work the same for every secret, or make the hint random, so that it does not match any guess.

## The idea

**The leakage function.** A device computes $y = F(k, p)$ with a secret $k$ and an input $p$. A side channel adds an observation $\ell = L(k, p) + N$, where $L$ is a deterministic leakage function and $N$ is noise. For power analysis, a standard model is

$$\ell = \varepsilon \cdot \mathrm{HW}(v(k, p)) + N, \qquad N \sim \mathcal{N}(0, \sigma^2),$$

with $v$ an intermediate value such as $S(p \oplus k)$ for an [S-box](/s-box/) $S$, and $\mathrm{HW}$ the [Hamming weight](/hamming-weight/); the [Hamming distance](/hamming-distance/) between two register states is the other common model (Mangard, Oswald and Popp, Chapter 3). For a timing channel, $L$ is the number of operations or of cache misses. These are models: a real device leaks through many effects at once, and a model is a hypothesis about which effect dominates.

**Divide and conquer.** A block cipher mixes the full key, so a guess of the key cannot be tested. But an early intermediate value depends on only a few key bits: $S(p \oplus k)$ depends on one 4-bit or 8-bit part. So the attacker tests the 16 or 256 guesses of each part apart, and a 128-bit key costs $16 \times 256$ tests instead of $2^{128}$. The parts that are not first in their list can be searched after, and [key rank estimation](/side-channel-key-rank-estimation/) tells how much search is left.

**Classes of attacks.** A *simple* attack reads the secret from one or a few traces, for example the sequence of squarings and multiplications of an exponentiation. A *differential* attack uses many traces and a statistic: a difference of means in [DPA](/differential-power-analysis/), a correlation in [CPA](/correlation-power-analysis/), a mutual information in [MIA](/mutual-information-analysis/). A *profiled* attack first measures a copy of the device and then uses the best statistical test, as in the [template attack](/template-attack/). A *passive* attack only observes; an *active* attack, such as a [fault attack](/differential-fault-analysis/), disturbs the computation. Cache attacks such as [Flush+Reload](/flush-and-reload/) and [Prime+Probe](/prime-and-probe/) need only software that shares the machine.

**Measuring an attack and a leak.** Standaert, Malkin and Yung (2009) separate two questions. How much does the device leak? That is an information measure, for example the mutual information between the key and a trace. How well does a given attack use the leak? That is its success rate, the probability that the right key is first, and its guessing entropy, the expected rank of the right key. A leakage test such as [TVLA](/test-vector-leakage-assessment/) asks a third, simpler question: is there any detectable dependence at all?

**Countermeasures.** Hiding makes the leak smaller or harder to find: constant-time code, balanced logic, noise and random order of operations. Masking splits each secret value into random shares, so that no single point depends on it; the [probing model](/probing-model/) states what a masked circuit guarantees, and the [ISW construction](/isw-private-circuits/) achieves it for any circuit. A first-order mask stops attacks that use one point of the trace. Chari, Jutla, Rao and Rohatgi (1999) proved, in a model with Gaussian noise on each share, that the number of traces an attack needs grows exponentially with the number of shares; on devices this is a measured trend, not a guarantee. In information flow terms, a defence tries to make the observation satisfy [noninterference](/noninterference/) with respect to the secret.

## Examples

All examples are abstract models with made-up values.

**Square and multiply.** A left-to-right exponentiation does a squaring for each bit of the exponent and a multiplication for each 1 bit. If a squaring and a multiplication have different shapes in the trace, one trace of an exponentiation that starts from 1 shows a sequence such as S M S S M S M. Each S followed by an M is a 1 bit and each S alone is a 0 bit, so the exponent is 1 0 1 1. This is [simple power analysis](/simple-power-analysis/). The defence is a fixed sequence of operations for every exponent.

**One bit of an S-box output.** With the 4-bit PRESENT S-box and the leakage $\mathrm{HW}(S(p \oplus k)) + N$, split the traces by the value of one bit of $S(p \oplus g)$ for a guess $g$. For the right guess, the two groups differ in mean power by 1 in expectation, the weight of the bit, because the S-box is a permutation and the other three bits have the same distribution in both groups. For a wrong guess the split is partly random and the difference is smaller. This is the idea of [DPA](/differential-power-analysis/), and the page gives the exact table of the differences.

**A cache line.** A table lookup $T[k \oplus p]$ loads one line of the cache. If an attacker can see which line was loaded, it learns the upper bits of $k \oplus p$, and so of $k$. In an abstract cache model, a computation that reads every line in a fixed order, or that has no secret-dependent index, gives the observer the same trace for every key.

**Masking one bit.** Store a secret bit $x$ as the pair $(x \oplus m, m)$ for a fresh uniform bit $m$. Each of the two values alone is a uniform bit whatever $x$ is, so an attack on one point learns nothing. The product of the centred leakages of both points still depends on $x$: this is a second-order attack, discussed on [Boolean masking](/boolean-masking/).

## Where it is used

- **Smart cards and secure elements.** Banking cards, SIM cards and identity documents are evaluated against power and electromagnetic analysis, with tests of the kind described on [TVLA](/test-vector-leakage-assessment/).
- **Cryptographic libraries.** Libraries for RSA, elliptic curves and AES aim at [constant-time](/constant-time-programming/) code for operations on secrets, and tools for [constant-time verification](/constant-time-verification/) check it.
- **Hardware design.** Masked hardware uses gadgets in the style of [ISW](/isw-private-circuits/) or [threshold implementations](/threshold-implementation/), which also resist glitches.
- **Processors and operating systems.** Speculative execution attacks such as [Spectre](/spectre-attack/) and [Meltdown](/meltdown-attack/) use a cache side channel to read data across a security boundary, and their defences change processors, compilers and kernels.
- **Security evaluation.** Labs report success rates, guessing entropy and [key ranks](/side-channel-key-rank-estimation/) of attacks, following the framework of Standaert, Malkin and Yung.

## References
