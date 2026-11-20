---
tag: JTBTTM
kind: algorithm
slug: massey-frame-synchronization
name: Massey optimum frame synchronization
aliases:
- Massey sync rule
area: communications/synchronization
level: advanced
summary: "The maximum likelihood rule to find a sync word among random binary data on the AWGN channel. It subtracts a sum of ln cosh terms from the plain correlation at each candidate position."
solves: [frame-synchronization]
model: real-ram
complexity:
  vars: {N: the number of candidate positions in the window, L: the length of the sync word}
  time: {worst: O(N L)}
  space: {extra: O(1)}
properties: {deterministic: true, optimal: "maximum likelihood and minimum error probability for equally likely positions", needs_snr: true, soft_decision: true}
history:
  year: 1972
  people: [James L. Massey]
  note: "Massey showed in 1972 that correlation is not the optimum frame sync rule when the sync word is surrounded by random data, and gave the optimum rule with its correction term."
prereqs: [frame-synchronization, maximum-likelihood-estimation]
see_also: [preamble-correlation-detection, barker-code, cross-correlation, matched-filter, phase-shift-keying, schmidl-cox-synchronization, additive-white-gaussian-noise-channel, maximal-length-sequence]
sources:
  - paper: doi:10.1109/TCOM.1972.1091127
    title: "James L. Massey, Optimum frame synchronization, IEEE Transactions on Communications 20(2), 1972, pages 115 to 119"
    locator: "the maximum likelihood rule for a sync word in random binary data on the Gaussian channel, its high-SNR form and the rule for hard decisions"
  - paper: doi:10.1109/TCOM.1980.1094813
    title: "Robert A. Scholtz, Frame synchronization techniques, IEEE Transactions on Communications 28(8), 1980, pages 1204 to 1213"
    locator: "the survey of frame sync rules, including Massey's rule and the choice of sync words"
  - paper: doi:10.1109/TCOM.1987.1096864
    title: "G. L. Lui and H. H. Tan, Frame synchronization for Gaussian channels, IEEE Transactions on Communications 35(8), 1987, pages 818 to 829"
    locator: "the maximum likelihood frame sync rule and its approximations on Gaussian channels, and their error probabilities"
---

Massey optimum frame synchronization finds where a known sync word starts in a received stream of binary symbols when the symbols around it are random data. The obvious rule is to correlate the received values with the sync word and pick the largest correlation. James L. Massey showed in 1972 that this rule is not optimum. A position where the received values are large in magnitude, but are data, can give a large correlation by chance. The maximum likelihood rule subtracts a correction from the correlation at each candidate position $\mu$:
$$M(\mu) = \sum_{i=0}^{L-1} s_i\,y_{\mu+i} - \frac{N_0}{2\sqrt{E_s}}\sum_{i=0}^{L-1}\ln\cosh\frac{2\sqrt{E_s}\,y_{\mu+i}}{N_0}.$$
Up to a scale and a constant, the second sum is the log-likelihood that the values are random data. The rule picks the $\mu$ with the largest $M(\mu)$. It needs the signal-to-noise ratio, but it has a simple high-SNR form, $\sum_i (s_i y_{\mu+i} - |y_{\mu+i}|)$, that does not. It is a rule for [frame synchronization](/frame-synchronization/), the soft-decision counterpart of the [correlation detector](/preamble-correlation-detection/).

## In plain words

A receiver looks for a known short pattern inside a long stream of signs. The simple method slides the pattern along the stream and counts how well it matches at each place. But strong random data can match by chance. Massey's rule also asks, at each place, how well the received values look like random data. It rewards places that look like the pattern and also look unlike random data. The rule needs to know how strong the noise is. When the noise is weak, it becomes simple: a place only scores well if every sign agrees with the pattern.

## The problem

The input is a window of $N$ real received values $y_0, \ldots, y_{N-1}$, read cyclically, and a sync word $s_0, \ldots, s_{L-1} \in \{+1, -1\}$. The window holds the sync word at an unknown start $\mu \in \{0, \ldots, N-1\}$, all values equally likely. The other $N - L$ symbols are independent and equally likely to be $+1$ or $-1$. Each received value is $y_i = \sqrt{E_s}\,d_i + n_i$, where $d_i$ is the sync or data symbol and the $n_i$ are independent Gaussian with variance $N_0/2$, the real [AWGN channel](/additive-white-gaussian-noise-channel/) after a matched filter and correct symbol timing. The output is an estimate $\hat\mu$ that minimizes the probability that $\hat\mu \ne \mu$.

## The algorithm

```pseudo id=main
MASSEY-SYNC(y[0..N-1], s[0..L-1], Es, N0)
L1  best <- -infinity; bestmu <- 0
L2  for mu <- 0 to N - 1 do
L3      for i <- 0 to L - 1 do
L4          corr <- corr + s[i] * y[(mu + i) mod N]
L5          lc <- lc + ln cosh(2 sqrt(Es) y[(mu + i) mod N] / N0)
L6      M <- corr - N0 / (2 sqrt(Es)) * lc         ▷ corr and lc start at 0 for each mu
L7      if M > best then
L8          best <- M; bestmu <- mu
L9  return bestmu
```

Line L4 is the plain correlation and line L5 adds Massey's correction. The function $\ln\cosh x$ is computed as $|x| + \ln(1 + e^{-2|x|}) - \ln 2$, which does not overflow for large $|x|$. Line L6 combines the two sums with the weight $N_0/(2\sqrt{E_s})$. Lines L7 to L9 keep the best position.

## Example

Take $s = (+1, +1, -1)$, $E_s = N_0 = 1$, so the weight in line L6 is $\frac12$, and the window $y = (0.7, 0.4, -0.6, 2.4, 1.8, 0.3, 0.9, 1.2)$. The sync word was sent at $\mu = 0$, and the large values at positions 3 and 4 are data.

| $\mu$ | correlation | $\sum\ln\cosh(2y)$ | $M(\mu)$ | $\sum(s_iy_i - \lvert y_i\rvert)$ | sign disagreements |
|---|---|---|---|---|---|
| 0 | $1.7$ | $1.650$ | $0.875$ | $0$ | 0 |
| 1 | $-2.6$ | $4.991$ | $-5.096$ | $-6.0$ | 2 |
| 2 | $0$ | $7.608$ | $-3.804$ | $-4.8$ | 2 |
| 3 | $3.9$ | $7.185$ | $0.308$ | $-0.6$ | 1 |
| 4 | $1.2$ | $4.212$ | $-0.906$ | $-1.8$ | 1 |
| 5 | $0$ | $3.019$ | $-1.509$ | $-2.4$ | 1 |
| 6 | $1.4$ | $3.615$ | $-0.407$ | $-1.4$ | 1 |
| 7 | $1.5$ | $2.772$ | $0.114$ | $-0.8$ | 1 |

Correlation picks $\mu = 3$, because the data values $2.4$ and $1.8$ are large. Massey's rule picks $\mu = 0$: the large values at $\mu = 3$ also have a large $\ln\cosh$ sum, so they look like data. The high-SNR form and the count of sign disagreements also pick $\mu = 0$.

In 2000 random trials per row, the fraction of wrong positions was (measurement):

| sync word, window, $E_s/N_0$ | Massey | correlation | high-SNR form | hard decisions |
|---|---|---|---|---|
| Barker 7, $N = 32$, 0 dB | $0.197$ | $0.358$ | $0.215$ | $0.333$ |
| Barker 13, $N = 64$, 0 dB | $0.036$ | $0.159$ | $0.039$ | $0.137$ |
| Barker 13, $N = 64$, 3 dB | $0.004$ | $0.060$ | $0.004$ | $0.025$ |

## Correctness

**Claim.** $M(\mu)$ is a positive multiple of the log-likelihood of $\mu$ plus a constant that does not depend on $\mu$. So the rule is the maximum likelihood rule, and with equally likely positions it minimizes the probability of a wrong $\hat\mu$ among all rules that see $y$. This is a theorem under the model of the problem.

**Key steps.** Given $\mu$, the values are independent. At a sync position the density of $y$ is $\phi(y)e^{2\sqrt{E_s}sy/N_0}$, and at a data position it is $\phi(y)\cosh(2\sqrt{E_s}y/N_0)$, the average over $d = \pm1$, where $\phi$ does not depend on $\mu$. The product over all $N$ positions, divided by the product of the $\cosh$ terms over all positions, leaves only the sync positions, and its logarithm is $\frac{2\sqrt{E_s}}{N_0}M(\mu)$ plus a constant. As $N_0 \to 0$, $\frac{N_0}{2a}\ln\cosh\frac{2ay}{N_0} \to |y|$, which gives the high-SNR form. The full proof is in the proofs file, and the tests compare $M$ with a direct sum of log densities.

## Complexity

In the [real RAM](/real-ram/) with $\ln\cosh$ as one operation, the direct rule does $L$ multiply-adds and $L$ evaluations of $\ln\cosh$ for each of the $N$ positions, so $O(NL)$ time and $O(1)$ extra space. Since the correction at one position is a sum of a function of single values, $\ln\cosh$ can be computed once per sample and summed with a sliding window in $O(N)$. The correlations can be computed for all positions with the FFT in $O(N\log N)$. The high-SNR form replaces $\ln\cosh$ with an absolute value, and the hard rule needs only sign comparisons.

## Properties

- **Optimal for its model.** No rule has a smaller error probability on the AWGN channel with random binary data and a uniform start.
- **Needs $E_s$ and $N_0$.** The weight and the argument of $\ln\cosh$ depend on both. A wrong estimate gives a rule between correlation and the high-SNR form.
- **High-SNR form.** $\sum_i(s_iy_{\mu+i} - |y_{\mu+i}|) \le 0$, with equality only when every sign agrees with $s$. It needs no SNR and in the table it is close to the optimum.
- **Low-SNR form.** For small $\sqrt{E_s}|y|/N_0$, $M(\mu) \approx \sum_i s_iy_{\mu+i} - \frac{\sqrt{E_s}}{N_0}\sum_i y_{\mu+i}^2$, a correlation minus an energy term.
- **Hard decisions.** With only the signs of $y$, a binary symmetric channel, the optimum rule counts the sign disagreements with $s$ and picks the fewest.

## Variants and improvements

- **Periodic sync words.** When the sync word repeats every frame, the metrics of several frames can be added before the decision, which lowers the error probability.
- **Sequential detection.** Instead of a window with exactly one sync word, a receiver can test each position as it arrives against a threshold, as in [preamble correlation detection](/preamble-correlation-detection/), at the cost of false alarms.
- **Other channels and modulations.** Lui and Tan derived the maximum likelihood rule and its approximations for Gaussian channels in more general settings. For M-ary signals the $\ln\cosh$ term becomes the log of the average likelihood over the data alphabet.
- **Unknown carrier phase.** With noncoherent reception the correlation becomes a magnitude, and the correction changes with it.
- **Choice of the sync word.** Words with low off-peak autocorrelation, such as [Barker codes](/barker-code/), reduce the chance that a shifted copy of the word partly overlapping itself wins.

## When to use it

Use Massey's rule when the receiver must find a short sync word in soft-decision data at a low SNR and has an estimate of $E_s/N_0$. Use the high-SNR form when the SNR is moderate or unknown, since it keeps almost all of the gain and needs only absolute values. Use plain correlation only when the sync word is long compared with the bias from the data, or when the data around the word are not random, as with a known preamble before the payload.

## Pitfalls

- **Treating correlation as optimum.** The example shows correlation choosing a data position. The gap grows at low SNR and for short sync words.
- **Wrong noise level.** The rule is only optimum with the correct $N_0$ and $E_s$. Large errors in the estimate move it toward one of its limits.
- **Overflow in $\ln\cosh$.** $\cosh x$ overflows in double precision for $|x|$ above about $710$. Use the stable form.
- **Model mismatch.** The derivation needs exactly one sync word in the window and random binary data. Several sync words, coded data with structure, or a window at the edge of a burst break this.
- **Timing first.** The rule works on symbol-spaced matched filter outputs, so symbol timing must be recovered before it is applied.

## Implementations

## History

Before 1972, receivers found sync words by correlation, and the choice of good sync words, from the Barker codes of 1953 onward, was studied in that setting. James L. Massey published "Optimum frame synchronization" in the IEEE Transactions on Communications in 1972. He derived the maximum likelihood rule for a sync word in random binary data on the Gaussian channel, with its high-SNR form and a rule for hard decisions, and showed that correlation lacks a correction term. Robert A. Scholtz surveyed frame synchronization techniques in 1980, and G. L. Lui and H. H. Tan extended the analysis of the optimum rules for Gaussian channels in 1987.

## References
