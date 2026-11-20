---
tag: 6HGD52
kind: algorithm
slug: luise-reggiannini-estimator
name: Luise and Reggiannini frequency estimator
aliases:
- L and R frequency estimator
area: communications/synchronization
level: advanced
summary: "Estimates the carrier frequency from the angle of a sum of L sample autocorrelations. With L near N/2 it stays close to the CRB down to low SNR; its range |nu| < 1/(L+1) shrinks as L grows."
solves: [frequency-offset-estimation]
model: real-ram
complexity:
  vars: {N: the number of samples, L: the number of autocorrelation lags}
  time: {worst: O(N L)}
  space: {extra: O(1)}
properties: {deterministic: true, feedforward: true, data_aided: true, range: "|nu| < 1/(L+1) cycles per symbol"}
history:
  year: 1995
  people: [Marco Luise, Ruggero Reggiannini]
  note: "Marco Luise and Ruggero Reggiannini of the University of Pisa published the estimator in 1995 for burst-mode all-digital modems, with a TDMA satellite link and a GSM-like mobile radio link as test cases."
prereqs: [frequency-offset-estimation, autocorrelation, cramer-rao-bound]
see_also: [kay-frequency-estimator, rife-boorstyn-frequency-estimator, modified-cramer-rao-bound, data-aided-synchronization, moose-frequency-offset-estimator, schmidl-cox-synchronization, carrier-recovery, pilot-symbol-assisted-modulation]
sources:
  - paper: doi:10.1109/26.380149
    title: "M. Luise and R. Reggiannini, Carrier frequency recovery in all-digital modems for burst-mode transmissions, IEEE Transactions on Communications 43(2/3/4), 1995, pages 1169 to 1178"
    locator: "the open-loop data-aided estimator from the angle of the sum of autocorrelations, its range and variance, and its use as a frequency error detector in a closed loop"
  - book: isbn:9780306457258
    title: "Umberto Mengali and Aldo N. D'Andrea, Synchronization Techniques for Digital Receivers, Plenum Press, 1997"
    locator: "Chapter 3 (carrier frequency recovery with linear modulations, data-aided feedforward estimators based on autocorrelations)"
---

The Luise and Reggiannini (L and R) estimator finds a carrier frequency offset from $N$ samples whose data are known or have been removed. It computes the sample autocorrelations $R(m)$ at the lags $m = 1, \ldots, L$, adds them, and divides the angle of the sum by $\pi(L+1)$. The sum of the noise-free terms $e^{j2\pi\nu m}$ has the exact angle $\pi\nu(L+1)$ for $|\nu| < \frac{1}{L+1}$, so the parameter $L$ trades the range against the noise: with $L$ near $N/2$, the variance stays close to the [Cramer-Rao bound](/cramer-rao-bound/) down to low SNR, which in synchronization with known data is the [modified Cramer-Rao bound](/modified-cramer-rao-bound/). It belongs to the estimators for [frequency offset estimation](/frequency-offset-estimation/). The [Kay estimator](/kay-frequency-estimator/) uses only lag 1, so it has the full range but a higher threshold, and the [Rife and Boorstyn estimator](/rife-boorstyn-frequency-estimator/) is the ML periodogram peak with the full range and the lowest threshold, at the cost of an FFT and a search. In OFDM, the [Moose](/moose-frequency-offset-estimator/) and [Schmidl and Cox](/schmidl-cox-synchronization/) estimators use the same idea at one long lag between repeated symbols.

## In plain words

A tone turns by a fixed angle per sample. Comparing each sample with the sample one step earlier shows that angle, but noisily. Comparing with the sample two steps earlier shows twice the angle, three steps earlier three times, and so on. The receiver averages all these comparisons up to some number of steps and reads one angle from the total. Using many steps averages more noise away, but if the tone turns too fast, the comparisons over many steps go more than half a turn round and the answer is wrong. So the number of steps sets both the accuracy and the largest offset that can be measured.

## The problem

The input is $z_k = A e^{j(2\pi\nu k + \phi)} + w_k$, $k = 0, \ldots, N - 1$, where $\nu$ is the frequency offset in cycles per symbol, $A$ and $\phi$ are unknown, and $w_k \sim \mathcal{CN}(0, N_0)$ is white, $\mathrm{SNR} = A^2/N_0$. In a burst modem, $z_k = r_k \overline{c_k}$ for the received samples $r_k$ and the known preamble symbols $c_k$ of unit modulus. Choose $1 \le L \le N - 1$ and output $\hat\nu$.

## The algorithm

```pseudo id=main
L-AND-R(z[0..N-1], L)
L1  N <- length of z
L2  S <- 0
L3  for m <- 1 to L do
L4      S <- S + (1 / (N - m)) * sum over k = m..N-1 of z[k] * conj(z[k - m])     ▷ R(m)
L5  return arg(S) / (pi * (L + 1))
```

Line L4 is the unbiased sample autocorrelation at lag $m$. Line L5 divides by $\pi(L+1)$, not by $2\pi$, because the angle of the sum of the lags $1$ to $L$ is the mean lag $\frac{L+1}{2}$ times $2\pi\nu$. The result is in cycles per symbol; multiply by $2\pi$ for radians per symbol, or divide by the symbol period for hertz.

## Example

$N = 8$, $\nu = 0.05$, $\phi = 0.3$, $\mathrm{SNR} = 10$ dB (noise seed 10), $L = 4$, so the range is $|\nu| < 0.2$. Line L4 gives:

| $m$ | $R(m)$ | noise-free $e^{j2\pi\nu m}$ |
|---|---|---|
| 1 | $0.8789 + 0.2741j$ | $0.9511 + 0.3090j$ |
| 2 | $0.7186 + 0.5334j$ | $0.8090 + 0.5878j$ |
| 3 | $0.4279 + 0.7508j$ | $0.5878 + 0.8090j$ |
| 4 | $0.1800 + 0.8422j$ | $0.3090 + 0.9511j$ |

$S = 2.2054 + 2.4006j$, with $\arg S = 0.8278$. Line L5 gives $\hat\nu = 0.8278/(5\pi) = 0.05270$, an error of $0.0027$. The bound for $N = 8$ at 10 dB is a standard deviation of $0.0055$ cycles.

With $N = 32$, 300 random offsets per point, $\nu$ uniform in $[-0.02, 0.02]$ (seed 3), the mean square error over the CRB $\frac{6}{(2\pi)^2\,\mathrm{SNR}\,N(N^2-1)}$ was (measurements):

| $L$ | range | $-3$ dB | 0 dB | 3 dB | 5 dB | 10 dB |
|---|---|---|---|---|---|---|
| 4 | $0.2$ | $12.2$ | $5.94$ | $3.76$ | $3.06$ | $2.30$ |
| 8 | $0.111$ | $3.35$ | $2.07$ | $1.64$ | $1.50$ | $1.36$ |
| 16 | $0.0588$ | $1.36$ | $1.20$ | $1.14$ | $1.12$ | $1.09$ |
| 24 | $0.04$ | $1.38$ | $1.24$ | $1.18$ | $1.17$ | $1.15$ |

$L = N/2 = 16$ is within about 20 percent of the bound down to 0 dB and within 36 percent at $-3$ dB, and a larger $L$ does not help. A small $L$ widens the range but costs accuracy at every SNR.

## Correctness

**Claim.** Each $R(m)$ is an unbiased estimate of $A^2 e^{j2\pi\nu m}$. Without noise, $\hat\nu = \nu$ exactly for $|\nu| < \frac{1}{L+1}$ (theorem). Outside the range the estimate aliases: for $\frac{1}{L+1} < \nu < \frac1L$ it returns $\nu - \frac{2}{L+1}$ (theorem). That the variance is close to the CRB for $L \approx N/2$ is a closed form under assumptions in the original paper and a measurement here.

**Key steps.** $\sum_{m=1}^{L} e^{j2\pi\nu m} = e^{j\pi\nu(L+1)}\frac{\sin(\pi\nu L)}{\sin(\pi\nu)}$. For $|\nu| < \frac{1}{L+1}$ the real factor is positive and $|\pi\nu(L+1)| < \pi$, so the angle of the sum is exactly $\pi\nu(L+1)$. Beyond the range, the angle wraps or the real factor turns negative, which the proof works out.

## Complexity

The direct form costs $O(NL)$ time, which is $O(N^2)$ for $L = N/2$, and $O(1)$ extra space. All autocorrelations can be computed with a zero-padded FFT in $O(N\log N)$. Only one angle is computed, at the end; the Kay estimator needs $N - 1$ angles.

## Properties

- **Range set by $L$.** $|\nu| < \frac{1}{L+1}$ cycles per symbol. For $L = N/2$ and $N = 32$ this is $0.0588$, so the estimator is a fine estimator after a coarse one, or for small offsets.
- **Close to the bound down to low SNR.** For $L \approx N/2$ the measured error is within about 20 percent of the CRB down to 0 dB. The angle is taken once, after averaging, so there are no wraps of single differences, which is what limits the Kay estimator.
- **Data-aided.** The data must be removed. For M-PSK without known data, apply it to $z_k^M$; the range is then divided by $M$, and the noise grows.
- **Simple.** One sum of products and one angle; no search, no FFT required, no unwrapping.
- **Biased near the range edge.** As $|\nu|$ approaches $\frac{1}{L+1}$, the noise pushes the angle over $\pm\pi$ more often, and the estimate aliases.

## Variants and improvements

- **Fitz estimator.** Takes the angle of each $R(m)$ separately, unwraps them across $m$ and fits a line. It has a similar range and accuracy.
- **Mengali and Morelli estimator.** Uses the phase differences $\arg(R(m)\overline{R(m-1)})$ with optimal weights, which gives a range of $|\nu| < \frac12$ independent of $L$ and an accuracy close to the bound.
- **Closed-loop form.** Luise and Reggiannini also used $\operatorname{Im}$ of the estimate as a frequency error detector in a recursive loop for continuous transmission.
- **Coarse plus fine.** Use a small $L$, or the Kay estimator, for a coarse estimate, derotate, then use $L = N/2$ for the fine estimate.
- **OFDM forms.** With a repeated training symbol, the same angle-of-correlation idea at one long lag gives the [Moose](/moose-frequency-offset-estimator/) and [Schmidl and Cox](/schmidl-cox-synchronization/) estimators.

## When to use it

Use it in burst modems with a known preamble, when the residual offset is small compared with the symbol rate and the SNR is low, for example a few dB, so that the Kay estimator is below its threshold. Choose $L$ as large as the largest expected offset allows, up to about $N/2$. For large offsets, use a coarse stage first, or the Rife and Boorstyn estimator.

## Pitfalls

- **Offset larger than the range.** An offset above $\frac{1}{L+1}$ gives a wrong estimate with no warning. In the tests, $\nu = 0.135$ with $L = 7$ returned $-0.115$.
- **Leaving the data in.** Unknown symbols randomize the products $z_k\overline{z_{k-m}}$. Divide out the preamble, or use a power for PSK.
- **Dividing by $2\pi$.** The angle of the sum is $\pi\nu(L+1)$; dividing it by $2\pi$ instead of $\pi(L+1)$ gives a wrong scale.
- **Using biased autocorrelations.** Dividing every $R(m)$ by $N$ instead of $N - m$ gives the long lags less weight. The angle of the noise-free sum is then no longer exactly $\pi\nu(L+1)$, and the estimate has a bias even without noise.
- **Taking $L$ larger than $N/2$.** It narrows the range and, in the measurement, did not improve the variance.

## Implementations

## History

Marco Luise and Ruggero Reggiannini, at the University of Pisa, published the estimator in the IEEE Transactions on Communications in 1995. They designed it for all-digital burst modems and tested it on a TDMA satellite link and on a mobile radio link with GSM-like signals. They also showed how to use it as a frequency error detector inside a loop. It followed the fast single-tone estimators of Kay (1989) and Fitz, and was followed by the estimator of Mengali and Morelli (1997), which removed the dependence of the range on $L$. Mengali and D'Andrea's book of 1997 presents it among the data-aided frequency estimators.

## References
