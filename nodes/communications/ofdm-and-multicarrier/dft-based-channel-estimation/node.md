---
tag: Q4YZBD
kind: algorithm
slug: dft-based-channel-estimation
name: DFT-based channel estimation
aliases:
- transform-domain channel estimation
area: communications/ofdm-and-multicarrier
level: core
summary: "Refines a least squares OFDM channel estimate by an inverse FFT, a cut to the channel length L_t and an FFT back. This removes all but L_t / N of the noise."
solves: [channel-estimation]
model: real-ram
complexity:
  vars: {N: the number of subcarriers}
  time: {worst: O(N log N)}
  space: {extra: O(N)}
properties: {deterministic: true, exact_without_noise: true, orthogonal_projection: true, needs_channel_length: true}
history:
  year: 1995
  people: [Jan-Jaap van de Beek, Ove Edfors, Magnus Sandell, Sarah Kate Wilson, Per Ola Börjesson]
  note: "Van de Beek, Edfors, Sandell, Wilson and Börjesson studied OFDM channel estimators that use the short length of the channel in time, including the estimate through the DFT, at the 1995 IEEE Vehicular Technology Conference."
prereqs: [orthogonal-frequency-division-multiplexing, least-squares-channel-estimation, fast-fourier-transform, comb-pilot-channel-estimation]
see_also: [lmmse-channel-estimation, two-dimensional-wiener-pilot-interpolation, singular-value-decomposition, delay-spread, cyclic-prefix, channel-estimation, frequency-domain-equalization, discrete-fourier-transform]
sources:
  - paper: doi:10.1109/VETEC.1995.504981
    title: "J.-J. van de Beek, O. Edfors, M. Sandell, S. K. Wilson and P. O. Börjesson, On channel estimation in OFDM systems, IEEE 45th Vehicular Technology Conference, 1995"
    locator: "pages 815 to 819 (least squares and LMMSE estimators, and the estimator that transforms to the time domain and uses the short length of the channel)"
  - paper: doi:10.1109/26.701321
    title: "O. Edfors, M. Sandell, J.-J. van de Beek, S. K. Wilson and P. O. Börjesson, OFDM channel estimation by singular value decomposition, IEEE Transactions on Communications 46(7), 1998"
    locator: "pages 931 to 939 (low-rank channel estimators for OFDM, which keep the few strongest dimensions of the channel)"
  - paper: doi:10.1109/TBC.2002.804034
    title: "S. Coleri, M. Ergen, A. Puri and A. Bahai, Channel estimation techniques based on pilot arrangement in OFDM systems, IEEE Transactions on Broadcasting 48(3), 2002"
    locator: "pages 223 to 229 (interpolation of comb pilots in the time domain, compared with interpolation along frequency)"
---

DFT-based channel estimation improves a noisy estimate of the [OFDM](/orthogonal-frequency-division-multiplexing/) channel by using what the receiver knows about the channel in time: its impulse response is short. The response $H[k]$ on $N$ subcarriers is the DFT of at most $L_t$ taps, with $L_t$ much smaller than $N$, so the $N$ values have only $L_t$ degrees of freedom. The [least squares estimate](/least-squares-channel-estimation/) $Y[k]/X[k]$ has noise on all $N$ values. The estimator takes the inverse DFT of it, keeps the first $L_t$ taps, sets the rest to zero and takes the DFT again. The result is exact without noise and keeps only the fraction $L_t / N$ of the noise power, because the three steps are an orthogonal projection onto the responses of channels with $L_t$ taps. The cut is to the channel length $L_t$; when $L_t$ is unknown, receivers often use the [cyclic prefix](/cyclic-prefix/) length plus one as a safe upper bound. The same idea interpolates comb pilots exactly. The page uses $j$ for the imaginary unit and the unnormalized DFT pair, so the inverse DFT of $H$ gives the taps.

## In plain words

The receiver has a rough measurement of the channel on every subcarrier, spoiled by noise. It knows that the channel is made of a few echoes that all arrive within a short time. So it converts the measurement to the time domain, where the channel shows up as a few values at the start and the noise is spread over all the time slots. It keeps the slots where echoes can be, throws away the rest, and converts back. What it throws away is pure noise. If there are 8 possible echo slots out of 64, it keeps only an eighth of the noise.

## The problem

The input is one received OFDM symbol after the DFT, $Y[0], \ldots, Y[N-1]$, the known values $X[k] \ne 0$ sent on all subcarriers (a training symbol), and the channel length $L_t \le N$. The model is $Y[k] = H[k] X[k] + W[k]$ with $H[k] = \sum_{l < L_t} h_l e^{-j 2\pi k l / N}$ and white noise $W[k] \sim \mathcal{CN}(0, N_0)$. Output an estimate of $H[k]$ for all $k$.

## The algorithm

```pseudo id=main
DFT-ESTIMATE(Y, X, L_t)
L1  Ĥ_LS[k] ← Y[k] / X[k]  for k = 0, .., N-1
L2  g ← IDFT(Ĥ_LS)                                 ▷ N noisy taps
L3  g[l] ← 0  for l = L_t, .., N-1                 ▷ keep the first L_t taps
L4  return DFT(g)
```

Line L1 is the least squares estimate on each subcarrier. Line L2 moves it to the time domain, where the channel occupies the first $L_t$ taps and white noise spreads evenly over all $N$. Line L3 discards the taps where no channel can be. Line L4 returns to the subcarriers. Both transforms are FFTs.

## Example

Take $N = 8$, $L_t = 2$, the channel $h = (1, 0.5)$, random 4-QAM training values (seed 6) and $N_0 = 0.1$.

| $k$ | $H[k]$ | $\hat H_{LS}[k]$ (line L1) | squared error | $\hat H[k]$ (line L4) | squared error |
|---|---|---|---|---|---|
| 0 | $1.500$ | $1.369 - 0.321j$ | 0.120 | $1.407 - 0.122j$ | 0.024 |
| 1 | $1.354 - 0.354j$ | $1.153 - 0.092j$ | 0.109 | $1.314 - 0.423j$ | 0.006 |
| 2 | $1.000 - 0.500j$ | $0.904 - 0.491j$ | 0.009 | $1.036 - 0.571j$ | 0.006 |
| 3 | $0.646 - 0.354j$ | $0.855 - 1.001j$ | 0.463 | $0.735 - 0.479j$ | 0.023 |
| 4 | $0.500$ | $0.729 - 0.019j$ | 0.053 | $0.587 - 0.200j$ | 0.048 |
| 5 | $0.646 + 0.354j$ | $0.402 + 0.108j$ | 0.120 | $0.679 + 0.101j$ | 0.065 |
| 6 | $1.000 + 0.500j$ | $1.254 + 0.263j$ | 0.121 | $0.957 + 0.249j$ | 0.065 |
| 7 | $1.354 + 0.354j$ | $1.306 + 0.264j$ | 0.010 | $1.259 + 0.157j$ | 0.048 |

Line L2 gives the taps $0.997 - 0.161j$, $0.410 + 0.039j$, $-0.102 - 0.090j$, $0.009 - 0.062j$, $0.068 + 0.019j$, $-0.061 - 0.202j$, $0.087 + 0.062j$, $-0.037 + 0.073j$. The first two are close to $h = (1, 0.5)$; the other six are noise only, and line L3 sets them to zero. The mean squared error drops from $0.126$ for least squares to $0.036$, close to the predicted $N_0 = 0.1$ and $L_t N_0 / N = 0.025$ for one noisy symbol.

## Correctness

**Claim.** (a) Lines L2 to L4 form the orthogonal projection $P = F T F^H$ onto the responses of channels with at most $L_t$ taps, where $F$ is the unitary DFT and $T$ keeps the first $L_t$ places. (b) Without noise, the output is $H$ exactly. (c) With noise, the mean squared error is $L_t / N$ times that of least squares; for $|X[k]| = 1$ it is $L_t N_0 / N$ instead of $N_0$. (d) For $|X[k]| = 1$, the kept taps are the maximum likelihood estimate of the taps in white Gaussian noise. All are theorems in the model above.

**Key invariant.** The true response $H$ lies in the range of $P$, so $P$ leaves it unchanged, and the output error is $P$ applied to the least squares error. Every diagonal entry of $P$ is $L_t / N$, so $P$ keeps that fraction of the power of any noise with independent entries.

The full proof is below. It also covers the comb version, which is exact for $L_t \le N / D$ and has the mean squared error $L_t N_0 / P$ for $P = N / D$ pilots.

## Complexity

Lines L2 and L4 are FFTs of size $N$, $O(N \log N)$ time, and lines L1 and L3 are $O(N)$. The extra space is $O(N)$ in the [real RAM](/real-ram/). The comb version uses an inverse FFT of size $P$ and an FFT of size $N$.

## Properties

- **Noise gain.** The factor $L_t / N$ is $1/8$ for $L_t = 8$ and $N = 64$, a gain of 9 dB over least squares, as the tests check within 10 percent.
- **Needs the length.** A cut shorter than the channel removes channel taps and leaves a bias; a cut longer than needed keeps more noise. With an unknown delay profile, the prefix length is the safe choice.
- **Delays between samples.** A path at a delay that is not a whole number of samples leaks into all taps, as the [spectral leakage](/spectral-leakage/) of a sinusoid between DFT bins does. The cut then leaves an error floor that more SNR cannot remove. For a single path at delay 2.5 samples and $N = 64$, the tests measure a floor that falls slowly with the cut, from about $0.128$ for $L_t = 4$ to $0.053$ for $L_t = 8$ and $0.040$ for $L_t = 16$.
- **No statistics.** Unlike [LMMSE estimation](/lmmse-channel-estimation/), it needs only $L_t$, not the delay profile or the SNR.
- **Comb pilots.** With pilots every $D$ subcarriers, the same steps interpolate exactly when $L_t \le N / D$, which is the sampling limit of the comb, where linear interpolation along frequency still has a bias.

## Variants and improvements

- **Comb pilots.** Take the inverse DFT of size $P = N / D$ of the pilot estimates, multiply tap $l$ by $e^{j 2\pi k_0 l / N}$ to undo the comb offset $k_0$, pad to $N$ and take the DFT. The implementation offers this as a second function.
- **Keep the taps near both ends.** Leakage from delays between samples goes partly to the taps near $N$, which stand for small negative delays. Keeping a few of those taps as well lowers the floor.
- **Most significant taps.** Keep only the taps whose power is above a threshold, which removes more noise in sparse channels.
- **Low rank.** Edfors and coauthors derived low-rank versions of the LMMSE estimator from the singular value decomposition of the channel correlation; the DFT-based estimate is a simpler relative that needs no statistics.
- **Null subcarriers.** When the band edges carry no pilots, filling the empty places with zeros before line L2 is no longer an orthogonal projection of the estimate, and the estimate develops errors near the edges; least squares over the used subcarriers fixes this at a higher cost.

## When to use it

Use it after least squares estimation when the channel is short compared with the symbol, the delay spread is roughly known, and the receiver already has FFT hardware. It gives most of the gain of LMMSE estimation without channel statistics. Prefer LMMSE or [two-dimensional Wiener interpolation](/two-dimensional-wiener-pilot-interpolation/) when the delay profile is known and the paths fall between samples, and plain [comb pilot interpolation](/comb-pilot-channel-estimation/) when the cost of two FFTs per symbol is too high.

## Pitfalls

- **Cutting to the wrong length.** Line L3 must keep $L_t$ taps, the length of the channel. Keeping $N$ taps changes nothing, and keeping fewer than the channel has removes signal.
- **Keeping the wrong end.** Line L3 must keep the taps $0, \ldots, L_t - 1$ after line L2. With a DFT convention that puts delay $l$ at index $N - l$, the channel sits at the other end, and line L3 then keeps only noise.
- **Mixing normalizations.** Line L2 and line L4 must be inverse to each other. A unitary inverse with an unnormalized forward transform scales the result by $\sqrt N$.
- **Forgetting the comb offset.** With pilots starting at $k_0 \ne 0$, the comb version must multiply tap $l$ by $e^{j 2\pi k_0 l / N}$ before the DFT of size $N$. Without it, the estimate is the channel shifted by $k_0$ subcarriers.
- **A cut longer than the pilots allow.** In the comb version, $L_t$ must be at most $P = N / D$. A longer cut has no data to fill it, and the channel aliases.

## Implementations

## History

The use of the time domain for OFDM channel estimation goes back to the group of van de Beek, Edfors, Sandell, Wilson and Börjesson at Luleå. Their 1995 paper at the Vehicular Technology Conference compared least squares, LMMSE and estimators that use the short length of the channel, and their 1998 paper derived low-rank estimators from the singular value decomposition. Later studies, such as the comparison of pilot arrangements by Coleri, Ergen, Puri and Bahai in 2002, included interpolation in the time domain among the methods for comb pilots.

## References
