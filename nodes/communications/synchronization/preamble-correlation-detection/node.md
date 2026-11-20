---
tag: 31P2YC
kind: algorithm
slug: preamble-correlation-detection
name: Preamble correlation detection
aliases:
- sync word correlation
- correlation frame synchronizer
area: communications/synchronization
level: core
summary: "Slides a known preamble over the received symbols, normalizes the correlation by the energy of both, and declares a frame start where it passes a threshold set for a false alarm rate."
solves: [frame-synchronization]
model: real-ram
complexity:
  vars: {N: the number of received symbols, L: the length of the preamble}
  time: {worst: O(N L), with_fft: O(N log L)}
  space: {extra: O(1)}
properties: {deterministic: true, online: true, carrier_phase_invariant: true, gain_invariant: true, constant_false_alarm_rate: "on white circular Gaussian noise"}
history:
  year: 1953
  people: [R. H. Barker]
  note: "Barker's 1953 paper on group synchronizing of binary systems is an early published treatment of finding a sync group by correlation, and it introduced the Barker sequences with low sidelobes."
prereqs: [frame-synchronization, cross-correlation]
see_also: [massey-frame-synchronization, barker-code, schmidl-cox-synchronization, cfar-detection, zadoff-chu-sequence, maximal-length-sequence, matched-filter, symbol-timing-recovery]
sources:
  - book: "R. H. Barker, Group synchronizing of binary digital systems, in Communication Theory, W. Jackson (editor), Butterworths, London, 1953, pages 273 to 287"
    title: "R. H. Barker, Group synchronizing of binary digital systems, in Communication Theory, Butterworths, 1953"
    locator: "the detection of a synchronizing group by agreement with a known pattern and the binary sequences with small off-peak agreement"
  - paper: doi:10.1109/TCOM.1980.1094813
    title: "Robert A. Scholtz, Frame synchronization techniques, IEEE Transactions on Communications 28(8), 1980, pages 1204 to 1213"
    locator: "the correlation detector with a threshold, its false alarm and miss probabilities, and the choice of sync words"
  - paper: doi:10.1109/TCOM.1972.1091127
    title: "James L. Massey, Optimum frame synchronization, IEEE Transactions on Communications 20(2), 1972, pages 115 to 119"
    locator: "the comparison of correlation with the optimum rule for a sync word in random data"
  - paper: doi:10.1109/26.650240
    title: "Timothy M. Schmidl and Donald C. Cox, Robust frequency and timing synchronization for OFDM, IEEE Transactions on Communications 45(12), 1997, pages 1613 to 1621"
    locator: "a timing metric normalized by the received energy, used to detect a preamble in bursts"
---

Preamble correlation detection finds the start of a frame or burst by searching the received symbols for a known preamble or sync word. At each start $n$ it correlates the received block $y_n, \ldots, y_{n+L-1}$ with the preamble $s_0, \ldots, s_{L-1}$, $c(n) = \sum_i \bar s_i\,y_{n+i}$. It then normalizes the squared magnitude by the energies of the preamble and of the received block, $\rho(n) = |c(n)|^2/(E_sE(n))$, which is between 0 and 1. It declares a frame when $\rho(n)$ passes a threshold $\lambda$, and then moves to the largest $\rho$ near that point. The magnitude removes the carrier phase, and the normalization removes the unknown gain and noise level, so on Gaussian noise the false alarm rate depends only on $\lambda$ and $L$. The phase and gain of $c(n)$ give a first estimate of the channel. It is the usual rule for burst receivers, and the threshold version of [cross-correlation](/cross-correlation/) with a [matched filter](/matched-filter/) for the preamble. For a sync word in random data with a known noise level, [Massey's rule](/massey-frame-synchronization/) is the optimum.

## In plain words

The sender puts a known pattern in front of each message. The receiver slides a copy of the pattern along what it receives and, at each place, measures how well the received part looks like the pattern, on a scale from 0 to 1. The scale does not depend on how loud the signal is or on its phase. When the measure is higher than a set level, the receiver says that a message starts there. It then checks a few nearby places and takes the best one. A higher set level gives fewer false starts on noise but can miss weak messages.

## The problem

The input is a stream of complex symbols $y_0, y_1, \ldots$ at one sample per symbol, after the matched filter and symbol timing, a known preamble $s_0, \ldots, s_{L-1}$ with energy $E_s = \sum_i |s_i|^2$, and a threshold $\lambda \in (0, 1)$. Where a preamble starts at $n_0$, $y_{n_0+i} = h\,s_i + v_{n_0+i}$ for an unknown complex gain $h$ that includes the carrier phase, and $v$ is noise. Before and after the preamble the stream is noise or data. The output is the start $\hat n_0$, or nothing if no preamble is present, together with the gain estimate $c(\hat n_0)/E_s$. The aims are a small probability of false alarm on noise or data and a small probability of a miss or a wrong start.

## The algorithm

```pseudo id=main
DETECT(y[0..N-1], s[0..L-1], lambda)
L1  E <- sum of |y[i]|^2 for i <- 0 to L - 1
L2  for n <- 0 to N - L do
L3      if n > 0 then E <- E + |y[n+L-1]|^2 - |y[n-1]|^2     ▷ running energy
L4      c[n] <- sum of conj(s[i]) * y[n+i] for i <- 0 to L - 1
L5      rho[n] <- |c[n]|^2 / (Es * E)
L6  for n <- 0 to N - L do
L7      if rho[n] >= lambda then
L8          b <- the k in [n, n + L - 1] with the largest rho[k]
L9          return (b, rho[b], c[b] / Es)
L10 return none
```

Lines L1 to L5 compute $\rho(n)$ for all starts, with a running sum for the energy. Line L7 compares with the threshold. For a target false alarm probability $P_{fa}$ per start on noise, the threshold is $\lambda = 1 - P_{fa}^{1/(L-1)}$. Line L8 refines the start to the peak in the next $L$ starts, because $\rho$ can first pass $\lambda$ on a sidelobe or on a partial overlap. Line L9 returns the start, the peak value and the complex gain estimate.

## Example

Take the [Barker code](/barker-code/) of length 13, $s = (1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1)$, with $E_s = 13$. The stream is two noise samples, the preamble times the gain $h = 0.5e^{j0.7}$, and one more noise sample: $y = (0.3 - 0.2j, -0.1 + 0.4j, h s_0, \ldots, h s_{12}, 0.2 + 0.1j)$, so there are four starts.

| $n$ | $c(n)$ | $\lvert c(n)\rvert^2$ | $E(n)$ | $\rho(n)$ |
|---|---|---|---|---|
| 0 | $0.5824 + 0.5221j$ | $0.6118$ | $3.05$ | $0.0154$ |
| 1 | $-0.1 + 0.4j$ | $0.17$ | $3.17$ | $0.0041$ |
| 2 | $4.9715 + 4.1874j$ | $42.25$ | $3.25$ | $1.0$ |
| 3 | $0.2 + 0.1j$ | $0.05$ | $3.05$ | $0.0013$ |

With $P_{fa} = 10^{-6}$ the threshold is $\lambda = 0.6838$. The scan stops at $n = 2$, and the detector returns $(2, 1.0, 0.3824 + 0.3221j)$, which is $h$. At $n = 1$ the preamble overlaps itself shifted by one, and the Barker sidelobe at that shift is 0, so only the noise sample remains in $c(1)$. On noise alone, $\lambda = 0.25$ gave 151 false alarms in 5000 windows against the predicted 158, with a noise variance that changed from window to window (measurement). At $E_s/N_0 = 10$ dB with a random carrier phase, all of 100 preambles were found at the correct start, with a mean peak $\rho$ of $0.914$ (measurement).

## Correctness

**Claim.** $0 \le \rho(n) \le 1$, and $\rho(n) = 1$ exactly when the block is $h\,s$ for some $h \ne 0$, in which case $c(n)/E_s = h$. Scaling $y$ by any nonzero complex number changes no $\rho(n)$. If the samples of a block are independent circular Gaussian with any variance, $\rho(n)$ has the Beta$(1, L - 1)$ distribution, so $P(\rho(n) \ge \lambda) = (1 - \lambda)^{L-1}$. Without noise, a preamble whose neighbours within $L - 1$ starts have $\rho < 1$ is found at its correct start, with the correct gain, if no earlier start passes $\lambda$. These are theorems.

**Key steps.** The bound and the equality case are the Cauchy-Schwarz inequality. The invariance holds because $h$ multiplies $c(n)$ by $h$ and $E(n)$ by $|h|^2$. For the distribution, $\rho$ is the squared cosine of the angle between a fixed vector and an isotropic random vector in $\mathbb{C}^L$, which is Beta$(1, L - 1)$. The full proof is in the proofs file. The tests check the running energy against direct sums, the invariance and the false alarm rate.

## Complexity

In the [real RAM](/real-ram/), line L3 costs $O(1)$ per start, line L4 costs $L$ complex multiply-adds, and line L5 costs $O(1)$. So $N$ symbols cost $O(NL)$ operations, and the refinement adds $O(L)$. With $\pm1$ preambles the multiplications become additions and subtractions. With the FFT and overlap-save blocks the correlations cost $O(N\log L)$. A streaming detector keeps only the last $L$ symbols, so the extra space beyond the input buffer is $O(1)$ for the energy and the correlation.

## Properties

- **Constant false alarm rate on noise.** The threshold sets $P_{fa}$ without knowledge of the noise level. A union bound gives at most $KP_{fa}$ for any false alarm in $K$ starts.
- **Phase and gain free.** The detection needs no carrier recovery, and the result gives a gain and phase estimate for it.
- **Data can cause false alarms.** On random data symbols the Beta law does not hold, because data can match part of the preamble. The rate depends on the data alphabet and the preamble.
- **Sidelobes matter.** Near the true start, $\rho$ follows the aperiodic autocorrelation of the preamble. Sequences with low sidelobes, such as Barker codes, give a sharp peak.
- **Not optimum for an embedded sync word.** For a sync word in random binary data and a known SNR, Massey's rule has a lower error probability.

## Variants and improvements

- **Unnormalized correlation.** $|c(n)|^2$ against a threshold that scales with an estimate of the noise level, as in [CFAR detection](/cfar-detection/). This is cheaper but needs the noise estimate.
- **Differential correlation.** Correlating $y_{n+i}\bar y_{n+i-1}$ with $s_i\bar s_{i-1}$ tolerates a frequency offset that would make $c(n)$ cancel over the preamble.
- **Autocorrelation of a repeated preamble.** [Schmidl and Cox](/schmidl-cox-synchronization/) send a preamble with two equal halves and correlate the received signal with itself, which works for any frequency offset but has a flat peak.
- **Other preambles.** [Zadoff-Chu sequences](/zadoff-chu-sequence/) have constant amplitude and zero periodic autocorrelation sidelobes, and [m-sequences](/maximal-length-sequence/) have two-valued periodic autocorrelation. Both give longer preambles than the Barker codes allow.
- **Fractional timing.** Running the detector at several samples per symbol and interpolating the peak also gives the symbol timing.

## When to use it

Use preamble correlation detection in burst receivers, packet radios and any link where frames start with a known preamble and the carrier phase, gain and noise level are unknown. Choose $L$ and $\lambda$ from the needed false alarm and miss rates. When the preamble is short and embedded in random data at a low SNR, use Massey's rule. When the frequency offset is large compared with $1/L$ symbols, use a differential or autocorrelation detector.

## Pitfalls

- **Frequency offset.** For a preamble of constant amplitude, a phase that rotates by $\Delta\phi$ per symbol multiplies $|c(n)|$ at the true start by $|\sin(L\Delta\phi/2)/(L\sin(\Delta\phi/2))|$. When $L\Delta\phi$ approaches $2\pi$, the peak vanishes.
- **Stopping at the first crossing.** The first start with $\rho \ge \lambda$ can be a partial overlap. Refine to the peak, as line L8 does.
- **Zero energy.** A block of exact zeros gives $0/0$. The implementation returns $\rho = 0$ there.
- **Drift of the running sum.** In floating point, the running energy can drift over long streams. Recompute it from time to time, or use exact arithmetic on integer samples.
- **Threshold from the wrong model.** The formula for $\lambda$ is for white Gaussian noise. On data or on interference, measure the false alarm rate.

## Implementations

## History

R. H. Barker described in 1953 how a receiver can find a synchronizing group in a binary stream by comparing it with the known pattern, and gave the binary sequences, now called Barker codes, whose off-peak agreement is at most one. Correlation with a sync word then became the usual method for frame synchronization in telemetry and data links. James L. Massey showed in 1972 that correlation is not the optimum rule for a sync word in random data, and Robert A. Scholtz surveyed the correlation detector, its error probabilities and the design of sync words in 1980. Burst and packet receivers use the energy-normalized form, which Schmidl and Cox also used for their timing metric in 1997.

## References
