---
tag: H5FN0Q
kind: algorithm
slug: correlation-power-analysis
name: Correlation power analysis
aliases:
- Brier-Clavier-Olivier attack
area: security-and-privacy/side-channel-attacks
level: core
summary: "Ranks key guesses by the Pearson correlation between measured power and a leakage model such as the Hamming weight of an intermediate value."
model: real-ram
complexity:
  vars: {m: the number of traces, T: the number of samples in each trace, g: the number of key guesses}
  time: {worst: Θ(g m T), average: Θ(g m T), best: Θ(g m T)}
  space: {extra: Θ(m + T + g)}
history:
  year: 2004
  people: [Eric Brier, Christophe Clavier, Francis Olivier]
  note: "Brier, Clavier and Olivier proposed the attack at CHES 2004, with a linear model of the power in the Hamming distance of a register to a reference state."
prereqs: [differential-power-analysis, hamming-weight]
see_also: [mutual-information-analysis, template-attack, side-channel-key-rank-estimation, boolean-masking, hamming-distance, linear-regression, welch-t-test, s-box]
sources:
  - paper: "Eric Brier, Christophe Clavier and Francis Olivier, Correlation power analysis with a leakage model, CHES 2004, LNCS 3156, pages 16 to 29"
    locator: "the linear leakage model in the Hamming distance, the correlation coefficient as the distinguisher, and the comparison with DPA"
  - paper: "Stefan Mangard, Elisabeth Oswald and Thomas Popp, Power Analysis Attacks, Springer, 2007, ISBN 978-0-387-30857-9"
    locator: "Chapter 3 (the Hamming weight and Hamming distance models), Chapter 4 (the statistics of power traces) and Chapter 6, pages 119 to 165 (the correlation attack and the rule of thumb for the number of traces)"
  - paper: doi:10.1007/978-3-540-74735-2_31
    title: "Andrey Bogdanov and others, PRESENT, an ultra-lightweight block cipher, CHES 2007, LNCS 4727"
    locator: the description of the substitution layer (the table of the 4-bit S-box used in the examples of this page)
  - paper: doi:10.1007/978-3-642-01001-9_26
    title: "François-Xavier Standaert, Tal G. Malkin and Moti Yung, A unified framework for the analysis of side-channel key recovery attacks, EUROCRYPT 2009, LNCS 5479, pages 443 to 461"
    locator: the definitions of the success rate and the guessing entropy
---

Correlation power analysis (CPA) finds a key from power traces by a correlation test. For each key guess, it predicts the leakage of each trace with a model, usually the [Hamming weight](/hamming-weight/) or the [Hamming distance](/hamming-distance/) of an intermediate value, and it computes the Pearson correlation between the prediction and the measured power at each time sample. The guess with the largest correlation wins. Brier, Clavier and Olivier (2004) introduced it as an improvement of [differential power analysis](/differential-power-analysis/), which uses only one bit of the value.

## In plain words

A chip uses a little more power for each wire that carries a one. Guess a small part of the key. With the guess and the known input of each run, you can compute a value inside the chip and count its ones. If the guess is right, the runs with many ones are the runs where the chip used more power, so the two lists of numbers rise and fall together. If the guess is wrong, your counts are for a different value, and the two lists agree much less. A correlation coefficient measures how well two lists rise and fall together. Compute it for every guess and keep the guess with the strongest agreement.

## The problem

The attacker sees $m$ pairs $(p_i, \ell_i)$, with $p_i$ a known input nibble and $\ell_i$ a trace of $T$ real samples. The device holds a fixed key nibble $k$. The leakage model is

$$\ell_i[j^\ast] = \varepsilon \cdot \mathrm{HW}(S(p_i \oplus k)) + N_{ij^\ast}, \qquad \ell_i[j] = N_{ij} \ \text{for } j \ne j^\ast,$$

where $S$ is the 4-bit S-box of PRESENT, $\varepsilon > 0$, the noise values $N_{ij}$ are independent with law $N(0, \sigma^2)$, and the inputs are independent and uniform. The attacker does not know $j^\ast$, $\varepsilon$ or $\sigma$. The goal is to output $k$. The cost model is the [real RAM](/real-ram/).

The attacker needs a model that is close to linear in the true leakage, but not the scale or the offset: the correlation does not change if the power is $a \cdot \mathrm{HW} + c$ for any $a > 0$ and any $c$.

## The algorithm

```pseudo id=main
CPA(traces (p_1, l_1) .. (p_m, l_m), S-box S)    ▷ each l_i has T samples
L1  best ← none, top ← -∞
L2  for each key guess g = 0 .. |S| - 1 do
L3      for i = 1 .. m do h_i ← HW(S(p_i ⊕ g))      ▷ the hypothesis of trace i
L4      for each sample j = 1 .. T do
L5          r_j ← corr((h_1 .. h_m), (l_1[j] .. l_m[j]))    ▷ 0 if one list is constant
L6      score(g) ← max over j of |r_j|
L7      if score(g) > top then
L8          best ← g, top ← score(g)
L9  return best and the list of scores
```

Line L5 is the sample Pearson correlation

$$r_j = \frac{\sum_i (h_i - \bar h)(\ell_i[j] - \bar\ell[j])}{\sqrt{\sum_i (h_i - \bar h)^2 \, \sum_i (\ell_i[j] - \bar\ell[j])^2}} .$$

The code computes the two means first and then the three sums of centred products. Line L6 takes the absolute value, so the attack works for a device whose power rises with the Hamming weight and for one whose power falls with it. Line L7 uses a strict test, so the first guess with the top score wins.

## Example

Take $k = \texttt{B}$ (hex), $\varepsilon = 1$, no noise, one sample in each trace, and each of the 16 inputs once. The trace values are $\mathrm{HW}(S(p \oplus \texttt{B}))$ for $p = 0, \ldots, \texttt{F}$:

$$1, 4, 3, 2, 1, 1, 3, 1, 3, 2, 2, 2, 3, 2, 0, 2 .$$

The signed correlation of each guess with these values is:

| guess | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | A | B | C | D | E | F |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| r | 0.125 | 0.5 | 0.375 | -0.5 | -0.625 | 0.5 | 0.125 | -0.5 | 0.25 | -0.375 | -0.25 | **1.0** | 0.25 | -0.75 | -0.25 | 0.125 |

The right guess has $r = 1$, because the hypothesis is exactly the trace. The closest rival is the guess D, which is $k \oplus 6$, with $|r| = 0.75$. For DPA on the same traces the margin was $0.25$ on a scale where the right key scores $1$; here it is also $0.25$, but every one of the 16 traces adds to the signal, not only the 8 on one side of a bit.

## Correctness

The loop of line L2 keeps the [loop invariant](/loop-invariant/) that top is the largest score of the guesses seen so far, and best is the first guess with that score, so line L9 returns the first argmax of the scores. In the model, the population correlation of the hypothesis of guess $g$ with the leaking sample is

$$\rho_g = c(g \oplus k) \cdot \rho, \qquad \rho = \frac{1}{\sqrt{1 + \sigma^2/\varepsilon^2}},$$

where $c(\delta)$ is the correlation of $\mathrm{HW}(S(X))$ and $\mathrm{HW}(S(X \oplus \delta))$ for a uniform $X$. Here $c(0) = 1$, and $|c(\delta)| \le 0.75$ for $\delta \ne 0$ on the PRESENT S-box. By the law of large numbers each $r_j$ converges to its population value, so the right key wins with a probability that tends to 1. This is a theorem in the stated model. The [proof](proofs/correctness.md) gives the details and the table of $c$.

## Complexity

For each of the $g$ guesses, line L3 costs $\Theta(m)$ and lines L4 and L5 cost $\Theta(mT)$, so the time is $\Theta(g m T)$ in every case. The extra space is $\Theta(m)$ for the hypothesis, $\Theta(T)$ for the correlations and $\Theta(g)$ for the scores. For a 4-bit S-box, $g = 16$; for a byte of AES, $g = 256$.

The number of traces depends on $\rho$, the correlation of the right guess. A heuristic from Mangard, Oswald and Popp (Chapter 6) uses the Fisher $z$ transform to find the $m$ at which $\rho$ is distinguished from 0 at the error level $\alpha$:

$$m \approx 3 + 8 \, \frac{z_{1-\alpha}^2}{\ln^2 \frac{1+\rho}{1-\rho}} .$$

With $z_{1-\alpha} = 3.719$ ($\alpha = 10^{-4}$) this gives 38.6 traces for $\rho = 0.707$, 94.7 for $\rho = 0.5$ and 2750.8 for $\rho = 0.1$. For small $\rho$, $\ln\frac{1+\rho}{1-\rho} \approx 2\rho$, and the rule becomes $m \approx 28/\rho^2$: half the correlation costs four times the traces. The heuristic compares the right key with no correlation; it does not see the wrong keys with $|c| = 0.75$. A measurement in the model, with 200 seeded runs for each cell, $\varepsilon = 1$, one sample in each trace and a random key in each run:

| traces m | 10 | 20 | 40 | 80 | 160 | 320 |
|---|---|---|---|---|---|---|
| success rate, σ = 1 (ρ = 0.707) | 0.595 | 0.825 | 0.955 | 1.0 | 1.0 | 1.0 |
| success rate, σ = 2 (ρ = 0.447) | 0.21 | 0.405 | 0.635 | 0.87 | 0.99 | 1.0 |

At $\sigma = 1$, [DPA](/differential-power-analysis/) on bit 1 needed about 400 traces for a success rate above 0.9 in the same model; CPA needs about 40.

## Properties

- **Invariant to scale and offset.** The score does not change under $\ell \mapsto a\ell + c$ with $a \ne 0$, so the attacker needs no calibration of the device.
- **Uses all bits.** In the Hamming weight model each bit of the value adds to the covariance, so the signal is larger than for a single-bit DPA.
- **Linear.** It detects only a linear dependence between the model and the power. If the true leakage is a non-linear function of the model, the correlation can be small even when the leak is large. [Mutual information analysis](/mutual-information-analysis/) has no such limit.
- **First order.** Against [Boolean masking](/boolean-masking/), the mean power at each sample is independent of the key, so every $\rho_g$ is 0. A second-order CPA on a combination of two samples is then necessary.
- **Divide and conquer.** Each key part is found on its own. The full list of scores can be given to [key rank estimation](/side-channel-key-rank-estimation/).

## Variants and improvements

- **The Hamming distance model.** Brier, Clavier and Olivier model the power as $a \cdot \mathrm{HD}(D, R) + b$, the number of bits that flip when a register goes from a reference state $R$ to the data $D$. This fits a bus or a register in CMOS hardware better than the Hamming weight.
- **Precomputed classes.** Sum the traces and their squares for each of the 16 input values once. Then each guess needs only the 16 class sums, and the time becomes $\Theta(mT + 16 g T)$.
- **Incremental CPA.** Keep the five running sums $\sum h$, $\sum h^2$, $\sum \ell$, $\sum \ell^2$ and $\sum h\ell$ so that new traces can be added one at a time.
- **Linear regression.** Fit the power as a [linear regression](/linear-regression/) on the bits of the value, so that each bit gets its own weight. This is a step toward a [template attack](/template-attack/).
- **Second order.** Against a first-order masked implementation, correlate the model with the centred product of two samples.

## When to use it

Use CPA as the default non-profiled attack when the leakage is close to the Hamming weight or the Hamming distance of a known intermediate value. Use [MIA](/mutual-information-analysis/) when the shape of the leakage is not known, and a [template attack](/template-attack/) when a copy of the device is available for profiling. To find out only whether a device leaks, with no key recovery, a [leakage test](/test-vector-leakage-assessment/) is cheaper.

## Pitfalls

- **A linear target.** If line L3 is $h_i \leftarrow \mathrm{HW}(p_i \oplus g)$, the hypothesis of $g \oplus \texttt{F}$ is $4 - h_i$, the exact negative, so with line L6 the guesses $k$ and $k \oplus \texttt{F}$ both score 1 and cannot be told apart. More generally a key addition alone gives a poor separation. Target the output of the S-box, as in line L3 above, where the non-linear map separates the guesses.
- **The signed score with the wrong sign.** If line L6 is score(g) ← max over j of $r_j$ and the device leaks $-\mathrm{HW}$ (for example a bus that is precharged to ones), the right key scores $-1$ and loses. Use the absolute value of line L6 unless the sign of the leakage is known.
- **The one-pass formula.** Computing line L5 as $\sum h\ell - m \bar h \bar\ell$ loses precision when the samples carry a large constant offset, because two large numbers that are almost equal are subtracted. Centre the values first, as the code does.
- **A constant column.** If all traces have the same value at a sample, or a guess gives the same hypothesis for every trace, the denominator of line L5 is 0. Define $r_j = 0$ in that case.

## Implementations

The code of this page is an abstract model on synthetic data. Its traces come from the leakage model of "The problem", drawn with a seeded `random.Random` by the function `simulate_traces`; the code never reads a device, a file or a clock. The tests check the example table, the exact correlations for every key, the agreement with `statistics.correlation` on 500 random inputs, the value of $\rho$ at 2000 traces, the success rate, and the rule of thumb.

## History

Brier, Clavier and Olivier presented CPA at CHES 2004. They replaced the difference of means of [Kocher, Jaffe and Jun](/differential-power-analysis/) (1999) by a correlation with a Hamming distance model. The book of Mangard, Oswald and Popp (2007) describes the correlation attack in its chapter on DPA, together with the rule of thumb for the number of traces. Gierlichs, Batina, Tuyls and Preneel (2008) proposed [mutual information](/mutual-information-analysis/) as a generic replacement for the correlation.

## References
