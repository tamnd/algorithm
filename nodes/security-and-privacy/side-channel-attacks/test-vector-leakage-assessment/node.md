---
tag: 89GDF4
kind: technique
slug: test-vector-leakage-assessment
name: Test vector leakage assessment
aliases:
- fixed versus random t-test
area: security-and-privacy/side-channel-attacks
level: advanced
summary: "Tests a device for leakage by a Welch t-test between traces of fixed and random inputs (the non-specific variant), with 4.5 as the conventional threshold."
prereqs: [side-channel-attack, welch-t-test]
see_also: [differential-power-analysis, correlation-power-analysis, boolean-masking, threshold-implementation, isw-private-circuits, mutual-information-analysis, bonferroni-correction, false-discovery-rate]
sources:
  - url: "https://www.rambus.com/wp-content/uploads/2015/08/a-testing-methodology-for-side-channel-resistance-validation.pdf"
    title: "Gilbert Goodwill, Benjamin Jun, Josh Jaffe and Pankaj Rohatgi, A testing methodology for side-channel resistance validation, NIST Non-Invasive Attack Testing Workshop, 2011"
    locator: "Sections 2 and 3 (the fixed versus random and the specific tests, the Welch t statistic, the threshold 4.5, and the rule of two independent sets of traces)"
  - paper: doi:10.1007/978-3-662-48324-4_25
    title: "Tobias Schneider and Amir Moradi, Leakage assessment methodology, a clear roadmap for side-channel evaluations, CHES 2015, LNCS 9293, pages 495 to 513"
    locator: the higher-order univariate and multivariate t-tests on centred and standardized moments, and the one-pass formulas for the moments
  - paper: "Stefan Mangard, Elisabeth Oswald and Thomas Popp, Power Analysis Attacks, Springer, 2007, ISBN 978-0-387-30857-9"
    locator: Chapter 4 (the statistics of power traces and the signal to noise ratio)
  - paper: doi:10.1007/978-3-540-74735-2_31
    title: "Andrey Bogdanov and others, PRESENT, an ultra-lightweight block cipher, CHES 2007, LNCS 4727"
    locator: the description of the substitution layer (the table of the 4-bit S-box used in the synthetic device of this page)
---

Test vector leakage assessment (TVLA) asks whether a device leaks, without trying to find a key. In its common, non-specific form, the evaluator records one group of power traces with a fixed input and another with random inputs, in random order, and computes a [Welch t-test](/welch-t-test/) between the two groups at every time sample. If the device leaks any information about the data it processes, the mean power at some sample differs between the fixed and the random group. Goodwill, Jun, Jaffe and Rohatgi (2011) proposed the method with a threshold $|t| > 4.5$ and a repetition on a second, independent set of traces. The threshold is a convention, not a theorem. Schneider and Moradi (2015) extended the test to higher orders, which is needed to test [masked](/boolean-masking/) implementations.

## In plain words

Run the chip many times on the same input and many times on random inputs, and record its power each time. If the chip hides its data well, the two piles of recordings look the same on average at every moment. If it does not, at some moment the average of one pile is a little higher than the other. A t-test measures whether such a difference is larger than what random noise would make. A big value at some moment means the chip shows something about its data there. The test does not say whether an attacker can use the leak, or how. A small value does not prove that the chip is safe, only that this test with this many traces found nothing.

## When it applies

- **A leakage question, not an attack.** Use it to decide whether an implementation passes or fails, or to find the samples that leak during development. It needs no model of the leakage and no knowledge of the key.
- **Control of the inputs.** The evaluator must choose the input of each run, so that a fixed group and a random group can be made. The fixed input is often chosen so that some intermediate value is special, but any input works.
- **Comparable runs.** The traces must be aligned in time, and the two groups must be recorded interleaved in random order, so that a drift of the temperature or of the supply affects both the same way.
- **First order by default.** The plain test compares means. A first-order masked implementation has the same mean for every input at each sample, so the test must be repeated on combinations of samples, or on higher moments, to find a higher-order leak.

## The template

```pseudo id=main
TVLA(device, n traces for each group, threshold C, order o)
L1  for each of two independent sets s = 1, 2 do
L2      record n traces with a FIXED input and n with RANDOM inputs, interleaved at random
L3      for each sample j do t_s[j] ← WELCH-T(PREPROCESS_o(fixed group, j), PREPROCESS_o(random group, j))
L4  leaky ← the samples j with |t_1[j]| > C and |t_2[j]| > C
L5  return fail if leaky is not empty, else pass
```

The holes are the inputs FIXED and RANDOM, the preprocessing for the order $o$ and the threshold $C$. Line L3 is the Welch statistic

$$t = \frac{\bar x - \bar y}{\sqrt{s_x^2 / n_x + s_y^2 / n_y}},$$

with the sample means $\bar x, \bar y$ and the unbiased sample variances $s_x^2, s_y^2$ of the two groups at sample $j$. For $o = 1$, PREPROCESS is the identity. For a second-order test on one pair of samples $(i, j)$, it replaces each trace by the centred product $(\ell[i] - \bar\ell[i])(\ell[j] - \bar\ell[j])$, with the means of its own group; for a univariate test of order 2 on one sample, by $(\ell[j] - \bar\ell[j])^2$ (Schneider and Moradi).

Line L4 is the decision rule of Goodwill and others: a sample fails only if both sets pass the threshold there. For a normal variable, $\Pr[|Z| > 4.5] \approx 6.8 \times 10^{-6}$. If there is no leak and $n$ is large, $t$ is close to normal at each sample (a theorem, by the central limit theorem). So with $10^5$ samples in a trace, one set gives about 0.68 false alarms on average. The two-set rule makes a false alarm at the same sample about $4.6 \times 10^{-11}$ likely for each sample, if the sets are independent. These numbers are approximations for large $n$ and independent samples; they are heuristics for real traces.

The cost is $\Theta(n T)$ arithmetic operations for each set with $T$ samples; a second-order test on all pairs costs $\Theta(n T^2)$.

## Classic examples

The examples use a synthetic device: the 4-bit PRESENT [S-box](/s-box/), key $\texttt{B}$, and traces of 4 samples with Gaussian noise $\sigma = 1$. Sample 0 leaks; the others are noise. The fixed input is $p = 1$, so the fixed value is $S(1 \oplus \texttt{B}) = \texttt{F}$, with Hamming weight 4. The code of this page draws these traces from the stated model with a seeded `random.Random`; it never reads a device, a file or a clock, and its tests reproduce the numbers below.

**An unprotected device.** Sample 0 is $\mathrm{HW}(S(p \oplus k)) + N$. The fixed group has mean 4 and variance 1; the random group has mean 2 and variance $1 + 1 = 2$. So $t \approx 2 / \sqrt{3/n} = 2\sqrt{n/3}$: this is the expected value for large $n$. With $n = 50$ the two sets gave $t = 7.54$ and $7.25$ at sample 0 and $|t| < 1.2$ elsewhere, so the device fails at sample 0 only. Over 20 runs with $n = 200$, the mean of $t$ was 16.2, against $2\sqrt{200/3} = 16.3$. The same leak is what [DPA](/differential-power-analysis/) and [CPA](/correlation-power-analysis/) use to find the key.

**A first-order masked device.** Sample 0 is $\mathrm{HW}(S(p \oplus k) \oplus m) + N$ and sample 1 is $\mathrm{HW}(m) + N$ for a fresh uniform mask $m$, as in [Boolean masking](/boolean-masking/). Each sample has mean 2 for every input, so the first-order test passes: with $n = 1000$, $|t| \le 1.8$ at all samples. The centred product of samples 0 and 1 has expectation $\varepsilon^2(1 - \mathrm{HW}(x)/2)$ for the value $x = S(p \oplus k)$, which is $-1$ for the fixed $x = \texttt{F}$ and 0 on average over random $x$. The second-order test on the same traces gave $t = -9.0$ and $-11.8$, so the device fails at order 2, as a first-order masked device must.

**A threshold implementation in hardware.** For hardware, the test is run on the masked design, for example a [threshold implementation](/threshold-implementation/), to check that glitches do not combine shares. A first-order pass with many traces, together with a second-order failure, is the expected result for a design with three shares and first-order security.

**A specific test.** Instead of fixed against random, split the random traces by one bit of an intermediate value, such as a bit of $S(p \oplus k)$ with the known key. This specific test finds a leak of that bit, and it is close to [DPA](/differential-power-analysis/) with the right key. It needs a model of the intermediate values; the non-specific test does not.

## Variations

- **Fixed versus fixed.** Two different fixed inputs give two groups with smaller variance than a random group, so the test can be more sensitive to a leak that the two inputs separate. It misses leaks that both inputs share.
- **Higher-order and multivariate tests.** Schneider and Moradi (2015) define tests on centred moments of order $o$ for one sample, and on centred products of $o$ samples, with one-pass formulas that update the moments as traces arrive.
- **Other statistics.** A $\chi^2$ test on histograms of the samples, or an estimate of the [mutual information](/mutual-information-analysis/), can detect differences in distribution that the mean misses, at a cost in traces.
- **Corrections for many samples.** With very many samples, a [Bonferroni correction](/bonferroni-correction/) or a control of the [false discovery rate](/false-discovery-rate/) gives a threshold with a stated error probability, instead of the fixed 4.5.

## Pitfalls

- **A pass is not a proof.** The test finds only differences that its statistic and its $n$ can see. A device can pass with $n$ traces and fail with $10n$, and a first-order pass says nothing about second-order leaks.
- **A fail is not an attack.** A leak at one sample of the input loading, or of a value that is public, is a fail, but it may not help an attacker. The evaluator must find out what leaks before claiming an attack.
- **Groups recorded apart.** If the fixed group is recorded first and the random group second, a slow drift of the device appears as a difference of means at every sample. Interleave the two groups in random order.
- **Small groups.** With 30 traces in each group the Welch statistic has heavier tails than the normal law: the synthetic test of this page measured $|t| > 2$ for 110 of 2000 samples of pure noise (5.5 percent), against 4.55 percent for the normal law. The threshold 4.5 assumes large groups.
- **The wrong means in second order.** The centring of the second-order preprocessing must use the mean of each group, or of all traces, the same way in both groups. Centring with a constant that is not the mean adds a first-order term to the product.
- **Many samples.** Without the second set, a trace with millions of samples has false alarms by chance. Use the two-set rule or a correction for multiple tests.

## Exercises

1. In the unprotected example, compute the expected $t$ at sample 0 for $n = 200$, and the $n$ at which it reaches 4.5.
2. Show that for a uniform 4-bit mask $m$, $\mathrm{E}[\mathrm{HW}(x \oplus m)] = 2$ for every $x$, so the first-order test of a masked device has the same mean in both groups.
3. Show that $\mathrm{E}[(\mathrm{HW}(x \oplus m) - 2)(\mathrm{HW}(m) - 2)] = 1 - \mathrm{HW}(x)/2$. Which fixed values $x$ make the second-order test blind?
4. A trace has $10^6$ samples, and one set is tested at $C = 4.5$. How many false alarms do you expect with no leak? What threshold gives an expected 0.01 false alarms for one set?

## References
