---
tag: 9K7QSC
kind: algorithm
slug: van-de-beek-estimator
name: Van de Beek estimator
aliases:
- cyclic prefix ML synchronization
area: communications/ofdm-and-multicarrier
level: advanced
summary: "The maximum likelihood estimate of OFDM symbol timing and carrier frequency offset from the correlation of the cyclic prefix with the end of the symbol. It needs no training symbol."
solves: [frequency-offset-estimation]
model: real-ram
complexity:
  vars: {N: the number of subcarriers, P: the prefix length N_cp, T: the number of candidate starts}
  time: {worst: O(P + T)}
  space: {extra: O(T)}
properties: {deterministic: true, blind: true, timing_and_frequency: true, maximum_likelihood: true}
history:
  year: 1997
  people: [Jan-Jaap van de Beek, Magnus Sandell, Per Ola Börjesson]
  note: "Van de Beek, Sandell and Börjesson derived the joint maximum likelihood estimate of timing and frequency offset from the redundancy of the cyclic prefix, for a Gaussian model of the OFDM samples."
prereqs: [orthogonal-frequency-division-multiplexing, cyclic-prefix, maximum-likelihood-estimation, frequency-offset-estimation]
see_also: [schmidl-cox-synchronization, moose-frequency-offset-estimator, inter-carrier-interference, symbol-timing-recovery, frame-synchronization, cramer-rao-bound, autocorrelation, moving-average]
sources:
  - paper: doi:10.1109/78.599949
    title: "J.-J. van de Beek, M. Sandell and P. O. Börjesson, ML estimation of time and frequency offset in OFDM systems, IEEE Transactions on Signal Processing 45(7), 1997"
    locator: "pages 1800 to 1805 (the Gaussian model, the log-likelihood function with the correlation gamma and the energy term Phi, and the joint estimate of timing and offset)"
  - paper: doi:10.1109/26.650240
    title: "T. M. Schmidl and D. C. Cox, Robust frequency and timing synchronization for OFDM, IEEE Transactions on Communications 45(12), 1997"
    locator: "pages 1613 to 1621 (the training-symbol alternative, with a wider range of offsets)"
---

The van de Beek estimator finds where an OFDM symbol starts and the carrier frequency offset of the receiver from the [cyclic prefix](/cyclic-prefix/) alone, without a training symbol. In [OFDM](/orthogonal-frequency-division-multiplexing/), the first $N_{cp}$ samples of each symbol are a copy of its last $N_{cp}$ samples, $N$ samples later. The estimator slides a window of $N_{cp}$ samples along the input and, for each candidate start $\theta$, correlates the window with the samples $N$ positions later, $\gamma(\theta) = \sum_k r(k)\, r^*(k + N)$. It also computes the energy $\Phi(\theta)$ of the same samples. The timing estimate maximizes $|\gamma(\theta)| - \rho\, \Phi(\theta)$, with $\rho = \text{SNR}/(\text{SNR} + 1)$, and the offset estimate is $-\angle\gamma(\hat\theta) / (2\pi)$ in subcarrier spacings. Van de Beek, Sandell and Börjesson showed that this is the joint maximum likelihood estimate when the OFDM samples are modeled as Gaussian and the channel adds white noise only. It solves the problem of [frequency offset estimation](/frequency-offset-estimation/) and symbol timing for continuous OFDM streams. The page uses $j$ for the imaginary unit and $\varepsilon = \Delta f\, N / f_s$ for the offset. The code calls the prefix length `l`.

## In plain words

Every OFDM symbol starts with a copy of its own tail. So somewhere in the received signal, a short stretch of samples matches another short stretch exactly one symbol body later. The receiver does not know where, so it tries every start. At each start it multiplies the stretch by the later stretch and adds up the products. At the right start, all the products point the same way and the sum is as large as the energy of the stretch. At wrong starts, they point in random directions and partly cancel. The right start is where the sum comes closest to the energy. A frequency offset turns the later copy by a fixed angle, so the angle of the sum at that start tells the receiver its offset.

## The problem

The input is a window of complex baseband samples $r(0), \ldots, r(M - 1)$ with $M \ge 2N + N_{cp}$, the DFT size $N$, the prefix length $N_{cp}$ and the SNR per sample. The model is $r(k) = s(k)\, e^{j 2\pi\varepsilon k / N} + n(k)$, where $s$ is a stream of OFDM symbols with prefixes, $\varepsilon$ is the unknown offset with $|\varepsilon| < 1/2$, and $n(k)$ is white noise $\mathcal{CN}(0, N_0)$. Find the index $\hat\theta$ of the first sample of a prefix inside the window, and an estimate $\hat\varepsilon$ of $\varepsilon$.

## The algorithm

```pseudo id=main
VAN-DE-BEEK(r, N, N_cp, SNR)
L1  for θ ← 0, 1, .., M - N - N_cp do                ▷ γ(0), Φ(0) are direct sums over k = 0, .., N_cp-1
L2      γ(θ) ← γ(θ-1) + r[θ-1+N_cp] conj(r[θ-1+N_cp+N]) - r[θ-1] conj(r[θ-1+N])
L3      Φ(θ) ← Φ(θ-1) + ½(|r[θ-1+N_cp]|² + |r[θ-1+N_cp+N]|² - |r[θ-1]|² - |r[θ-1+N]|²)
L4  Λ(θ) ← |γ(θ)| - ρ Φ(θ) for every θ, with ρ = SNR / (SNR + 1)
L5  θ̂ ← argmax_θ Λ(θ)
L6  ε̂ ← -angle(γ(θ̂)) / (2π)                              ▷ wrapped to [-1/2, 1/2)
L7  return θ̂, ε̂
```

Lines L1 to L3 slide the window of $N_{cp}$ pairs: each step adds the newest pair and drops the oldest, so each candidate costs $O(1)$. On the prefix, the pair $r(k)$, $r(k + N)$ holds the same sent sample, and the offset turns the second one by $e^{j 2\pi\varepsilon}$, so $r(k)\, r^*(k + N) = e^{-j 2\pi\varepsilon} |s(k)|^2$ apart from noise. Line L4 compares the size of the correlation with the energy. Without noise, $|\gamma| \le \Phi$ everywhere, with equality at a prefix start. With noise, the factor $\rho$ comes from the likelihood: it weights the energy less when the noise makes the pairs less alike. Line L5 picks the start, and line L6 reads the offset from the angle at that start.

## Example

Take $N = 8$, $N_{cp} = 2$, a stream of three symbols whose time samples are independent $\mathcal{CN}(0, 1)$ (seed 3), $\varepsilon = 0.1$, no noise, and a window of 20 samples that starts 3 samples into the stream. The prefix of the second symbol starts at sample 10 of the stream, which is $\theta = 7$ in the window. There are 11 candidates.

| $\theta$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $\lvert\gamma(\theta)\rvert$ | 1.382 | 1.197 | 1.678 | 0.684 | 0.725 | 0.363 | 2.182 | 4.650 | 3.309 | 2.064 | 1.364 |
| $\Phi(\theta)$ | 2.779 | 2.631 | 1.751 | 0.931 | 1.104 | 0.741 | 2.512 | 4.650 | 3.796 | 2.372 | 1.956 |
| $\Lambda(\theta)$, $\rho = 1$ | -1.397 | -1.434 | -0.073 | -0.248 | -0.380 | -0.378 | -0.330 | 0 | -0.487 | -0.308 | -0.592 |
| $-\angle\gamma / 2\pi$ | 0.407 | -0.390 | -0.397 | -0.162 | -0.168 | 0.391 | 0.123 | 0.1 | 0.065 | -0.051 | -0.096 |

Every $\Lambda$ is negative except at $\theta = 7$, where $|\gamma| = \Phi = 4.650$ and $\gamma = 3.762 - 2.733j$, with the angle $-2\pi \cdot 0.1$. Line L5 returns $\hat\theta = 7$ and line L6 returns $\hat\varepsilon = 0.1$. With the SNR set to 10 dB, so $\rho = 0.909$, the result is the same. At wrong starts the angle is random, which is why line L6 must use the angle at $\hat\theta$ only.

At 10 dB per sample with $N = 64$, $N_{cp} = 16$ and $\varepsilon = 0.2$, the tests measure 150 windows at random positions; about 95 percent of the timing estimates are within 2 samples of the prefix start, and at least 90 percent must be.

## Correctness

**Claim.** (a) Under the Gaussian model, the log-likelihood of $(\theta, \varepsilon)$ is a constant plus a positive multiple of $\operatorname{Re}(e^{j 2\pi\varepsilon} \gamma(\theta)) - \rho\, \Phi(\theta)$, so lines L4 to L6 give the joint maximum likelihood estimate. (b) Without noise, $\Lambda(\theta) \le 0$ for every $\theta$, with equality at a prefix start, where the angle of $\gamma$ is $-2\pi\varepsilon$; so the algorithm is exact for $|\varepsilon| < 1/2$ unless a wrong start ties. Both are theorems in the model above.

**Key invariant.** On a prefix, $r(k + N) = e^{j 2\pi\varepsilon} r(k)$ without noise. The Gaussian model makes every other pair of samples uncorrelated, so the likelihood depends on $(\theta, \varepsilon)$ only through the $N_{cp}$ prefix pairs, and these enter through $\gamma$ and $\Phi$ alone.

Part (b) is the triangle inequality with $|a||b| \le \frac12 (|a|^2 + |b|^2)$. At a high SNR, the variance of $\hat\varepsilon$ at the true start is close to $\frac{1}{4\pi^2 N_{cp}\, \text{SNR}} (1 + \frac{1}{2\,\text{SNR}})$, a closed form for a linearized phase error. The full proof is below.

## Complexity

The direct sums for $\theta = 0$ cost $O(N_{cp})$, and each of the $T = M - N - N_{cp} + 1$ candidates costs $O(1)$ in lines L2 to L4, so the time is $O(N_{cp} + T)$ in the [real RAM](/real-ram/). The implementation stores $\gamma$ and $\Phi$ for all candidates, $O(T)$ extra space. A streaming receiver keeps only the running sums, a delay line of $N + N_{cp}$ samples and the best value so far, so it needs $O(N)$ space.

## Properties

- **Blind.** It uses only the structure of the prefix, so it costs no training symbols and works on every symbol of a stream.
- **Range.** The offset is found modulo 1, so $|\varepsilon| < 1/2$. An offset of $0.6$ is read as $-0.4$, as the tests check. The integer part needs another method.
- **Variance.** Close to $\frac{1}{4\pi^2 N_{cp}\,\text{SNR}} (1 + \frac{1}{2\,\text{SNR}})$ at a high SNR: $1.66 \times 10^{-4}$ for $N_{cp} = 16$ at 10 dB. It uses $N_{cp}$ pairs instead of $N$, so the variance is $N / N_{cp}$ times that of the [Moose estimator](/moose-frequency-offset-estimator/), which correlates two repeated symbols.
- **Timing spread.** The metric changes slowly near the peak, so with noise the timing estimate spreads over a few samples. Short prefixes make this worse.
- **Model.** The derivation assumes Gaussian samples and a channel with white noise only. OFDM samples are close to Gaussian for large $N$, so the estimator works well for real signals, but in a dispersive channel the first $L - 1$ prefix samples contain interference from the previous symbol and it is no longer the maximum likelihood estimate.

## Variants and improvements

- **Average over symbols.** In a continuous stream, the timing and the offset do not change from symbol to symbol, so adding $\Lambda$ and $\gamma$ over several symbols, at the same position in each, cuts the variance roughly by the number of symbols.
- **Without the SNR.** Setting $\rho = 1$ in line L4 gives $|\gamma| - \Phi$, which needs no SNR. It is still exact without noise, but it is no longer the maximum likelihood estimate at a finite SNR.
- **Correlation only.** Some receivers use the maximum of $|\gamma(\theta)|$ alone. Without the energy term, a strong sample in a wrong window can win, so the estimate is worse.
- **Dispersive channels.** Correlating only the last $N_{cp} - L + 1$ samples of the prefix, which are free of interference from the previous symbol, removes the bias at the cost of fewer pairs.
- **With pilots.** Systems such as DVB-T add continual pilots for a finer frequency estimate and an integer offset search after the DFT; the prefix estimate serves for the first coarse step.

## When to use it

Use it for a continuous OFDM stream without a preamble, as in digital broadcasting, or to track timing and offset on every symbol after acquisition. Use [Schmidl-Cox synchronization](/schmidl-cox-synchronization/) for bursts with a preamble, where a large offset must be found quickly and the training symbol gives a wider range. Use the [Moose estimator](/moose-frequency-offset-estimator/) when two repeated symbols are available and the timing is known, to get a smaller variance.

## Pitfalls

- **The wrong sign in line L6.** The product $r(k)\, r^*(k + N)$ has the angle $-2\pi\varepsilon$, so line L6 must negate the angle. With the product $r^*(k)\, r(k + N)$ in line L2, the sign in line L6 must change too.
- **Reading the angle at another start.** Line L6 must take the angle of $\gamma$ at $\hat\theta$ from line L5. At other starts the angle is random, as the example shows.
- **Correlating over the wrong lag.** Line L2 must pair samples exactly $N$ apart, the DFT size, not $N + N_{cp}$, the symbol length.
- **A window that is too short.** Line L1 must see a whole prefix and its copy, so the window needs at least $2N + N_{cp}$ samples to contain a full prefix pair for any position of the stream.
- **Dropping the energy term.** Line L4 must subtract $\rho\, \Phi(\theta)$. The maximum of $|\gamma|$ alone favors windows with large samples, not windows on the prefix.
- **Constant-modulus test signals.** If the time samples all have the same modulus, other starts can also give $\Lambda = 0$ without noise, and line L5 may pick one of them. Test with Gaussian samples or with OFDM symbols made by an inverse DFT.

## Implementations

## History

Jan-Jaap van de Beek, Magnus Sandell and Per Ola Börjesson, at Luleå University of Technology, published the joint maximum likelihood estimator in IEEE Transactions on Signal Processing in 1997. The same year, Schmidl and Cox published their method with a training symbol. The prefix estimator became the standard blind synchronizer for continuous OFDM systems, and its correlation of the prefix with the symbol end is used in broadcasting receivers and in many later estimators that add pilots or average over symbols.

## References
