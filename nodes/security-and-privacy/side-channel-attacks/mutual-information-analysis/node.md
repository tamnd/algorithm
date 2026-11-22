---
tag: DNRK95
kind: algorithm
slug: mutual-information-analysis
name: Mutual information analysis
aliases:
- MIA
area: security-and-privacy/side-channel-attacks
level: advanced
summary: "Ranks key guesses by the estimated mutual information between leakage and predicted values, which works without a linear leakage model."
model: real-ram
complexity:
  vars: {m: the number of traces, T: the number of samples in each trace, g: the number of key guesses, B: the number of bins, V: the number of model values}
  time: {worst: Θ(g T (m + V B)), average: Θ(g T (m + V B)), best: Θ(g T (m + V B))}
  space: {extra: Θ(m T + V B + g)}
history:
  year: 2008
  people: [Benedikt Gierlichs, Lejla Batina, Pim Tuyls, Bart Preneel]
  note: "Gierlichs, Batina, Tuyls and Preneel proposed mutual information as a generic distinguisher for side-channel attacks at CHES 2008."
prereqs: [correlation-power-analysis, shannon-entropy, conditional-entropy]
see_also: [differential-power-analysis, template-attack, side-channel-key-rank-estimation, histogram, kernel-density-estimation, hamming-weight, s-box]
sources:
  - paper: "Benedikt Gierlichs, Lejla Batina, Pim Tuyls and Bart Preneel, Mutual information analysis, CHES 2008, LNCS 5154, pages 426 to 442"
    locator: "the definition of the distinguisher, the histogram estimate of the conditional entropy, and the comparison with the correlation attack"
  - paper: "Stefan Mangard, Elisabeth Oswald and Thomas Popp, Power Analysis Attacks, Springer, 2007, ISBN 978-0-387-30857-9"
    locator: "Chapter 3 (the Hamming weight model) and Chapter 6, pages 119 to 165 (the correlation attack that MIA is compared with)"
  - paper: doi:10.1007/978-3-540-74735-2_31
    title: "Andrey Bogdanov and others, PRESENT, an ultra-lightweight block cipher, CHES 2007, LNCS 4727"
    locator: the description of the substitution layer (the table of the 4-bit S-box used in the examples of this page)
  - paper: doi:10.1007/978-3-642-01001-9_26
    title: "François-Xavier Standaert, Tal G. Malkin and Moti Yung, A unified framework for the analysis of side-channel key recovery attacks, EUROCRYPT 2009, LNCS 5479, pages 443 to 461"
    locator: the information theoretic metric and the definitions of the success rate and the guessing entropy
---

Mutual information analysis (MIA) finds a key from power traces with the mutual information between the measured power and a predicted value, in place of the correlation of [CPA](/correlation-power-analysis/). For each key guess it groups the traces by a model value, such as the [Hamming weight](/hamming-weight/) of an S-box output, and estimates how much knowing that value reduces the uncertainty of the power. Because mutual information sees any dependence, not only a linear one, the attack works when the power is a non-linear function of the model. Gierlichs, Batina, Tuyls and Preneel (2008) proposed it as a generic distinguisher.

## In plain words

Sort the recorded runs into boxes by a value that a key guess predicts, for example the number of ones in a value inside the chip. Then look at the power in each box. If the guess is right, each box holds runs with similar power, so knowing the box tells you a lot about the power. If the guess is wrong, every box holds a mix, and the box tells you little. Mutual information measures, in bits, how much one thing tells you about another. It does not care whether the power goes up or down with the value, or in which pattern. It only asks whether the boxes differ. The guess whose boxes differ the most wins.

## The problem

The attacker sees $m$ pairs $(p_i, \ell_i)$, with $p_i$ a known input nibble and $\ell_i$ a trace of $T$ real samples. The device holds a fixed key nibble $k$. The leakage model is

$$\ell_i[j^\ast] = f\big(\mathrm{HW}(S(p_i \oplus k))\big) + N_{ij^\ast}, \qquad \ell_i[j] = N_{ij} \ \text{for } j \ne j^\ast,$$

where $S$ is the 4-bit S-box of PRESENT, $f$ is a function that the attacker does not know, the noise values $N_{ij}$ are independent with law $N(0, \sigma^2)$, and the inputs are independent and uniform. The attacker knows that the power depends on the Hamming weight, but not how. The goal is to output $k$. The cost model is the [real RAM](/real-ram/).

## The algorithm

The estimate of the mutual information uses a [histogram](/histogram/): each sample is cut into $B$ bins of equal width from its smallest to its largest value. The entropies are the plug-in [Shannon entropies](/shannon-entropy/) of the counts, in bits.

```pseudo id=main
MIA(traces (p_1, l_1) .. (p_m, l_m), S-box S, model M, bins B)
L1  best ← none, top ← -∞
L2  for each sample j: bin_i[j] ← the bin of l_i[j] among B equal bins of column j
L3  for each key guess g = 0 .. |S| - 1 do
L4      for i = 1 .. m do h_i ← M(S(p_i ⊕ g))       ▷ the model value, HW here
L5      for each sample j = 1 .. T do
L6          count the pairs (h_i, bin_i[j]) in a table
L7          I_j ← H(bin) + H(h) - H(h, bin)        ▷ plug-in entropies of the counts
L8      score(g) ← max over j of I_j
L9      if score(g) > top then
L10         best ← g, top ← score(g)
L11 return best and the list of scores
```

Line L7 is the identity $I(X; Y) = H(X) + H(Y) - H(X, Y)$, applied to the empirical joint distribution of the table of line L6. The first term is the same for every guess at a given sample, so the ranking at one sample depends only on the [conditional entropy](/conditional-entropy/) $H(\text{bin} \mid h)$: the right guess is the one whose groups have the most concentrated power.

## Example

**Hamming weight leakage.** Take $k = \texttt{B}$, $f(w) = w$, no noise, one sample in each trace, each of the 16 inputs once, and $B = 5$ bins. The trace values $0, \ldots, 4$ then fall in 5 different bins, and the scores are exact mutual informations:

| guess | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | A | B | C | D | E | F |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| score (bits) | 0.906 | 1.281 | 0.686 | 0.686 | 1.250 | 1.281 | 0.906 | 0.686 | 0.561 | 0.936 | 0.906 | **2.031** | 0.561 | 0.811 | 0.906 | 1.186 |

The right guess scores $H(\mathrm{HW}) = 2.031$ bits, the entropy of the weights $0, 1, 2, 3, 4$ with counts $1, 4, 6, 4, 1$: the groups are pure. The closest rivals are the guesses 1 and 5, at $1.281$ bits.

**Non-linear leakage.** Now let $f(w) = (w - 2)^2$, so the power is 0 for weight 2, 1 for weights 1 and 3, and 4 for weights 0 and 4. The covariance of $w$ and $(w-2)^2$ is the third central moment of a symmetric binomial law, which is 0, so the right guess of CPA has correlation 0. With $B = 4$ bins, MIA gives the right guess $1.406$ bits and the best wrong guess, $k \oplus \texttt{F}$, $1.0$ bit. A measurement in the model, with $\sigma = 1$, 8 bins, 200 seeded runs for each cell and a random key in each run:

| traces m | 25 | 50 | 100 | 200 | 400 |
|---|---|---|---|---|---|
| MIA, f(w) = w | 0.385 | 0.72 | 0.985 | 1.0 | 1.0 |
| CPA, f(w) = w | 0.915 | 0.995 | 1.0 | 1.0 | 1.0 |
| MIA, f(w) = (w - 2)² | 0.42 | 0.645 | 0.86 | 0.97 | 0.99 |
| CPA, f(w) = (w - 2)² | 0.15 | 0.105 | 0.035 | 0.005 | 0.0 |

When the linear model is right, CPA needs fewer traces. When it is wrong, CPA converges to a wrong key, because some wrong guesses keep a correlation of up to $0.306$ with $(w - 2)^2$, while MIA still converges to the right one.

## Correctness

The loop of line L3 keeps the [loop invariant](/loop-invariant/) that top is the largest score so far and best is the first guess with it, so line L11 returns the first argmax. Line L7 is the plug-in mutual information of the table, by the identity above. The key fact is a theorem about the population, from the data processing inequality: given the right model value $\mathrm{HW}(S(p \oplus k))$, the binned power depends only on the noise, so a wrong model value cannot carry more information about it. For every binning $b$ and every $g$,

$$I\big(b(\ell[j^\ast]);\ \mathrm{HW}(S(p \oplus g))\big) \le I\big(b(\ell[j^\ast]);\ \mathrm{HW}(S(p \oplus k))\big).$$

With fixed bin edges and a strict inequality, the plug-in estimates converge, and the right key wins with a probability that tends to 1. The [proof](proofs/correctness.md) gives these steps, and also the proof that an injective model makes all guesses equal.

## Complexity

Line L2 finds the range of each column and the bin of each value in $\Theta(mT)$ time. For each of the $g$ guesses and each of the $T$ samples, line L6 fills a table of $V \times B$ counts from $m$ pairs, and line L7 reads the table, which costs $\Theta(m + VB)$. So the time is $\Theta(g T (m + VB))$ in every case. The extra space is $\Theta(mT)$ for the bin indices, $\Theta(VB)$ for one table and $\Theta(g)$ for the scores. With the Hamming weight model of a 4-bit value, $V = 5$.

## Properties

- **Generic.** The score sees any dependence between the model and the power, linear or not, in either direction. It needs no assumption on $f$ beyond the fact that it is not constant on the model values.
- **Needs a non-injective model.** If the model is a bijection of the S-box output, every guess gives the same partition of the inputs up to a relabelling, and all scores are equal (a theorem, proved on the proof page). The Hamming weight works because it merges values.
- **Estimator bias.** The plug-in estimate of mutual information is biased upward when there are few traces in each cell of the table. A common heuristic is the Miller and Madow correction of about $(V-1)(B-1)/(2m \ln 2)$ bits. The bias is of the same order for every guess, but it adds variance to the ranking.
- **Slower than CPA when CPA is right.** In the measurement above, MIA needs two to four times as many traces as CPA for a success rate of 0.95 under linear leakage.
- **First order.** Against [Boolean masking](/boolean-masking/), the distribution of the power at one sample is the same for every key, so the mutual information with any first-order model is 0.

## Variants and improvements

- **Kernel density estimates.** Replace the histogram by a [kernel density estimate](/kernel-density-estimation/) of the power in each group. This gives a smoother estimate with a bandwidth in place of a bin count.
- **Rank by conditional entropy.** At one sample $H(\text{bin})$ is the same for every guess, so it is enough to rank the guesses by $H(\text{bin} \mid h)$, which saves one entropy per guess.
- **A choice of the bin count.** The bin count trades bias for resolution. Rules such as one bin for each few traces of each group, or a count that grows like $m^{1/3}$, are heuristics.
- **Other generic distinguishers.** Any distance between the conditional distributions of the power in the groups can replace the mutual information, for example a distance between cumulative distribution functions.
- **Profiled use.** With a copy of the device, the conditional distributions can be learned in advance. This is the [template attack](/template-attack/).

## When to use it

Use MIA when the shape of the leakage is unknown or not monotone in the model, for example when the power of a bus depends on transitions in a way that the Hamming weight does not fit. When a linear model is known to fit, use [CPA](/correlation-power-analysis/), which needs fewer traces. When a profiling device is available, a [template attack](/template-attack/) does better than both.

## Pitfalls

- **An injective model.** If line L4 is $h_i \leftarrow S(p_i \oplus g)$, the 16 model values are a relabelling of the 16 inputs for every guess, so every guess has the same table up to the order of the rows, and every score is the same, $2.031$ bits in the example. Line L4 must merge values, as the Hamming weight does.
- **Too many bins.** If line L2 uses so many bins that each trace has its own bin, then $H(h, \text{bin}) = H(\text{bin})$ and line L7 gives $H(h)$, the entropy of the model values of the guess, which depends only on the inputs and not on the power. Use a bin count that is much smaller than the number of traces in each group, such as the 8 bins of the measurement.
- **A constant column.** If all traces have the same value at a sample, line L2 has no range to cut. The code puts all values in bin 0, and the score at that sample is then 0 for every guess.
- **Comparing against CPA at its best.** A table of MIA against CPA under linear leakage only shows that CPA wins there. The reason to use MIA is a leakage that CPA does not fit; test it on one.

## Implementations

The code of this page is an abstract model on synthetic data. Its traces come from the leakage model of "The problem", drawn with a seeded `random.Random` by the function `simulate_traces`; the code never reads a device, a file or a clock. The tests check the example tables, the equal scores of an injective model, the result with too many bins, the agreement with a direct sum of $p \log (p / pq)$ on 500 random inputs, and the success rate under linear and quadratic leakage.

## History

Gierlichs, Batina, Tuyls and Preneel presented mutual information analysis at CHES 2008 as a distinguisher that needs fewer assumptions than the difference of means of [DPA](/differential-power-analysis/) and the correlation of [CPA](/correlation-power-analysis/). The idea of measuring side-channel leakage in bits, by information theory, also underlies the framework of Standaert, Malkin and Yung (2009), which compares attacks by their success rate and their guessing entropy.

## References
