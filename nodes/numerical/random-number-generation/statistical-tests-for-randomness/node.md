---
tag: A97QR0
kind: problem
slug: statistical-tests-for-randomness
name: Statistical tests for randomness
aliases:
- Diehard tests
- Dieharder
- TestU01
- BigCrush
- empirical tests for random number generators
- NIST SP 800-22 test suite
- PractRand
area: numerical/random-number-generation
level: advanced
summary: Batteries of statistical tests that detect non-random patterns in generator output.
prereqs: [pseudorandom-number-generator, uniform-distribution, central-limit-theorem]
see_also: [randu, mersenne-twister, xorshift, berlekamp-massey, birthday-paradox, computational-indistinguishability, kolmogorov-complexity, entropy-source]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: "Section 3.3.1, general test procedures (the chi-square and Kolmogorov-Smirnov tests); Section 3.3.2, empirical tests (equidistribution, serial, gap, poker, coupon collector, permutation, runs, maximum-of-t, collision, birthday spacings and serial correlation tests); Section 3.5, what is a random sequence"
  - paper: doi:10.1145/1268776.1268777
    title: Pierre L'Ecuyer and Richard Simard, TestU01, a C library for empirical testing of random number generators, ACM Transactions on Mathematical Software 33(4), 2007, Article 22
    locator: the design of the library, the batteries SmallCrush, Crush and BigCrush, the treatment of p-values, and the tables of results for many published generators
  - paper: "George Marsaglia, The Marsaglia Random Number CDROM including the Diehard Battery of Tests of Randomness, Florida State University, 1995"
    locator: the Diehard tests (birthday spacings, overlapping permutations, binary matrix ranks, bitstream, OPSO, OQSO, DNA, count-the-ones, parking lot, minimum distance, 3D spheres, squeeze, overlapping sums, runs and craps)
  - paper: "Andrew Rukhin, Juan Soto, James Nechvatal and others, A Statistical Test Suite for Random and Pseudorandom Number Generators for Cryptographic Applications, NIST Special Publication 800-22 Revision 1a, 2010"
    locator: the 15 tests of the suite, from the frequency (monobit) test to the random excursions variant test, and the procedure for interpreting the proportion and uniformity of p-values
  - paper: "Andrew Chi-Chih Yao, Theory and applications of trapdoor functions, 23rd Annual Symposium on Foundations of Computer Science, 1982, pages 80 to 91"
    locator: the equivalence between passing every polynomial-time statistical test and passing the next-bit test
  - paper: "Per Martin-Löf, The definition of random sequences, Information and Control 9(6), 1966, pages 602 to 619"
    locator: the definition of a random infinite sequence as one that passes every effective sequential statistical test, and the existence of a universal test
  - url: https://webhome.phy.duke.edu/~rgb/General/dieharder.php
    title: Robert G. Brown, Dirk Eddelbuettel and David Bauer, Dieharder, a random number test suite
    locator: the open source suite that reimplements the Diehard tests, part of the NIST tests and further tests, with adjustable sample sizes
---

Statistical tests for randomness try to tell the output of a [pseudorandom number generator](/pseudorandom-number-generator/) apart from a truly random sequence. Each test computes a statistic from a long stretch of output, for example the counts of values in bins or the rank of a bit matrix, whose distribution would be known exactly if the output were independent and uniform; a value far out in the tail of that distribution is evidence against the generator. Since no finite set of tests can certify randomness, the practice is to run large batteries of tests chosen to catch the defects that real generators have: Knuth's tests (1969), Marsaglia's Diehard (1995), NIST SP 800-22 (2001), and TestU01 (L'Ecuyer and Simard, 2007), whose BigCrush battery is the usual standard today, along with PractRand for very long streams.

## In plain words

Suppose someone hands you a long list of numbers between 0 and 1 and claims they are random. You cannot prove they are, but you can look for evidence that they are not. Are about a tenth of them below 0.1? When you group them in threes, do they fill the cube evenly? Do long runs of increasing numbers appear about as often as chance predicts?

Each such question is a test. For truly random numbers, we know how surprising each possible answer would be. If the list gives an answer that random numbers would give only once in a billion tries, the list is not random. Generators are checked with hundreds of such tests, each aimed at a kind of flaw that real generators have shown.

## Definition

Let $u_0, u_1, \ldots, u_{n-1}$ be outputs of a generator, as numbers in $[0, 1)$ or as bits. The null hypothesis $H_0$ is that they are independent and uniformly distributed, $U(0, 1)$ or fair bits. A **statistical test** is a function $T$ of the outputs whose distribution $F$ under $H_0$ is known exactly or approximately. Given the observed value $t$, the **p-value** is $p = P_{H_0}(T \ge t) = 1 - F(t)$ for a right-tailed test (two-sided tests use both tails). Under $H_0$ and for continuous $F$, $p$ is uniform on $[0, 1]$.

A generator **fails** a test when $p$ is extremely small or extremely close to 1, so small that the result would be essentially impossible under $H_0$. TestU01, for example, reports p-values outside $[0.001, 0.999]$ and regards those outside $[10^{-10}, 1 - 10^{-10}]$ as clear failures. A suspicious but not extreme p-value is followed up by repeating the test with a larger $n$: a real defect drives $p$ toward 0 as $n$ grows, while a fluke does not repeat.

A **battery** is a fixed list of tests with fixed parameters and sample sizes. The problem is: given a generator, decide whether its output can be distinguished from $H_0$ by any test in the battery with a feasible amount of output.

## Variants

- **Empirical and theoretical tests.** Empirical tests, the subject of this page, look at actual output. Theoretical tests, such as the [spectral test](/spectral-test/) for LCGs or the equidistribution analysis of $\mathrm{GF}(2)$-linear generators, analyze the whole period from the generator's parameters.
- **Two-level tests.** Run a test $N$ times on disjoint stretches and compare the $N$ p-values with the uniform distribution by a Kolmogorov-Smirnov or Anderson-Darling test. This detects small but systematic deviations and also errors in the approximation of $F$.
- **Tests on bits and on real numbers.** Bit-oriented suites (NIST, PractRand, parts of TestU01) read the output as a bit stream; others use the numbers $u_i$, often only their top bits. Many generators pass with their high bits and fail with their low bits, so TestU01 also tests bit-reversed output.
- **Cryptographic tests.** NIST SP 800-22 and the health tests of SP 800-90B check generators meant for cryptography or [entropy sources](/entropy-source/). Passing them is necessary, never sufficient, for security: a counter run through a public hash passes every battery and is completely predictable.
- **Martin-Löf randomness.** For infinite sequences, Martin-Löf (1966) defined a sequence to be random if it passes every effective statistical test; this coincides with incompressibility in the sense of [Kolmogorov complexity](/kolmogorov-complexity/) and is not decidable.

## Examples

**Equidistribution in three dimensions.** Take 100000 non-overlapping triples from [RANDU](/randu/) (seed 1) and count them in the $10^3$ cubes of side $0.1$. The chi-square statistic $\sum (O - E)^2/E$ with $E = 100$ is about 1593 on 999 degrees of freedom, where the 0.001 critical value is about 1143: a clear failure, with $p$ far below $10^{-10}$. Python's Mersenne Twister gives about 1064, an unremarkable value. With $20^3$ cubes, RANDU leaves 2090 of the 8000 cells empty, because its triples lie on 15 planes. Yet the one-dimensional frequency test on the same 100000 RANDU values, with 10 bins, gives 11.6 on 9 degrees of freedom, a perfectly good value: each test sees only one kind of defect.

**Linear complexity and matrix rank.** The output bits of a $\mathrm{GF}(2)$-linear generator with a $k$-bit state, such as [xorshift](/xorshift/) or the [Mersenne Twister](/mersenne-twister/), satisfy a linear recurrence of order at most $k$. The linear complexity test computes, by [Berlekamp-Massey](/berlekamp-massey/), the shortest recurrence of a long bit sequence, which for random bits is about half the length; with more than $2k$ bits the generator's complexity stops at $k$. Likewise, binary matrices filled with output bits have too small a rank once they hold more bits than the state. TestU01 reports that MT19937 fails only the two linear complexity tests of BigCrush, while smaller generators of this kind also fail the matrix rank tests.

**Birthday spacings.** Throw $n$ points into $d$ cells, sort the cell numbers, and count the repeated values among the spacings between consecutive sorted values; under $H_0$ the count is approximately Poisson with mean $n^3/(4d)$. LCGs fail this test with sample sizes far smaller than their period, because their lattice structure makes the spacings too regular.

## Known algorithms

- **Goodness-of-fit tests.** Pearson's chi-square test on bin counts; the Kolmogorov-Smirnov and Anderson-Darling tests on the empirical distribution function. Knuth Section 3.3.1 gives both with their exact or asymptotic distributions.
- **Knuth's empirical tests.** Equidistribution, serial (pairs and tuples), gap, poker, coupon collector, permutation, runs up, maximum-of-$t$, collision, birthday spacings and serial correlation.
- **Diehard.** Marsaglia's battery of about fifteen tests, distributed on a CD-ROM in 1995, with fixed sample sizes that are now too small for modern generators. Dieharder, by Robert G. Brown, reimplements them with adjustable sizes.
- **NIST SP 800-22.** 15 bit-oriented tests: frequency (monobit), frequency within a block, runs, longest run of ones, binary matrix rank, discrete Fourier transform, non-overlapping and overlapping template matching, Maurer's universal statistical test, linear complexity, serial, approximate entropy, cumulative sums, random excursions and random excursions variant.
- **TestU01.** A C library with dozens of test families and the batteries SmallCrush (a few seconds), Crush (about an hour) and BigCrush (several hours), which apply about 100 tests and compute 160 statistics on roughly $2^{38}$ random numbers; also Rabbit and Alphabit for bit streams.
- **PractRand.** Tests a stream in doubling lengths from megabytes to terabytes or more and reports the length at which a test first fails, which ranks generators that pass BigCrush.

## Bounds

- **Multiple testing.** If a battery computes 160 p-values that are independent and uniform under $H_0$, the probability that at least one is below 0.001 is $1 - 0.999^{160} \approx 0.148$. A single moderately small p-value in a battery is therefore expected even for a perfect generator; only extreme p-values, or ones that get more extreme as $n$ grows, indicate a defect.
- **Sample size against bias.** In the monobit test, if each bit is 1 with probability $\frac12 + \varepsilon$, the normalized statistic $(\#\text{ones} - n/2)/\sqrt{n/4}$ has mean $2 \varepsilon \sqrt{n}$ and variance close to 1. Detecting the bias at about 4 standard deviations needs $n \approx (2 / \varepsilon)^2$ bits, for example $4 \times 10^8$ bits for $\varepsilon = 10^{-4}$. Defects of size $\varepsilon$ are in general invisible with fewer than about $1/\varepsilon^2$ samples.
- **Every generator fails some test.** A generator with a $k$-bit state produces at most $2^k$ distinct sequences of length $L$. The test that rejects exactly those sequences has type I error at most $2^{k - L}$ and rejects the generator with probability 1. For $L > k$ it is a valid test, though usually infeasible to compute. Structured generators fail efficient tests of this kind: $\mathrm{GF}(2)$-linear generators fail linear complexity tests with about $2k$ bits, and a generator that is a fixed function of a counter fails the test that inverts it, if inversion is easy.
- **Batteries are finite.** Consequently, passing a battery shows only that the generator has none of the defects the battery looks for, at the sample sizes used.

## Reductions

- **To prediction (Yao, 1982).** A bit generator passes every polynomial-time statistical test, in the sense that no efficient test distinguishes its output from uniform bits with non-negligible advantage, if and only if no efficient algorithm predicts the next bit from the previous ones with probability non-negligibly above $\frac12$. This is the definition of a cryptographic [pseudorandom generator](/pseudorandom-generator/) and of [computational indistinguishability](/computational-indistinguishability/); by the theorem of Håstad, Impagliazzo, Levin and Luby, such generators exist if one-way functions exist.
- **To compression.** A sequence that some test rejects strongly can be described more briefly than one of maximal Kolmogorov complexity, and conversely. By the Levin-Schnorr theorem, a sequence is Martin-Löf random exactly when all its prefixes are incompressible in the sense of prefix-free Kolmogorov complexity, up to a constant.
- **From specific tests to probability problems.** The distribution of each statistic comes from a classical problem: the [birthday paradox](/birthday-paradox/) for collisions and birthday spacings, coupon collecting, the ranks of random matrices over $\mathrm{GF}(2)$, and runs in random permutations.

## Applications

- **Choosing generators.** Libraries choose their default generators partly by TestU01 and PractRand results; generators that fail, such as LCGs with small moduli, RANDU, and plain xorshift, which fails linear complexity and matrix rank tests, are replaced.
- **Finding implementation errors.** A wrong constant, a missing mask or a bad seeding routine usually shows up as a failure in SmallCrush within seconds.
- **Monitoring hardware generators.** True random number generators and entropy sources run simple statistical health tests continuously, as required by NIST SP 800-90B, to detect a failing noise source.
- **Checking simulations.** When a simulation result is suspect, rerunning it with a generator of a different family is itself a test aimed at the defect that matters for that application, as in the Ising model simulations in which Ferrenberg, Landau and Wong (1992) found wrong results with shift-register and subtract-with-borrow generators that had passed the standard tests.

## References
