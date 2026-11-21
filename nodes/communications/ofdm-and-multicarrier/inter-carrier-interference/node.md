---
tag: A85JTD
kind: concept
slug: inter-carrier-interference
name: Inter-carrier interference
aliases:
- ICI
area: communications/ofdm-and-multicarrier
level: core
summary: "Leakage between OFDM subcarriers caused by frequency offset, phase noise or Doppler, which breaks their orthogonality."
prereqs: [orthogonal-frequency-division-multiplexing, frequency-offset-estimation]
see_also: [schmidl-cox-synchronization, moose-frequency-offset-estimator, van-de-beek-estimator, common-phase-error-correction, doppler-spread, spectral-leakage, filter-bank-multicarrier, orthogonal-time-frequency-space-modulation]
sources:
  - paper: doi:10.1109/26.380034
    title: "T. Pollet, M. Van Bladel and M. Moeneclaey, BER sensitivity of OFDM systems to carrier frequency offset and Wiener phase noise, IEEE Transactions on Communications 43(2/3/4), 1995"
    locator: "pages 191 to 193 (the SNR degradation caused by a carrier frequency offset and by Wiener phase noise)"
  - paper: doi:10.1109/ICC.1995.524481
    title: "P. Robertson and S. Kaiser, Analysis of the effects of phase-noise in orthogonal frequency division multiplex (OFDM) systems, IEEE International Conference on Communications (ICC), 1995"
    locator: "pages 1652 to 1657 (phase noise splits into a common phase error and inter-carrier interference)"
  - paper: doi:10.1109/11.948268
    title: "A. Garcia Armada, Understanding the effects of phase noise in orthogonal frequency division multiplexing (OFDM), IEEE Transactions on Broadcasting 47(2), 2001"
    locator: "pages 153 to 159 (the common phase error and the inter-carrier interference from phase noise)"
  - book: isbn:9780521837163
    title: "Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005"
    locator: "Chapter 12 (multicarrier modulation, with the effects of frequency offset and timing errors on the subcarriers)"
---

Inter-carrier interference (ICI) is the part of the signal of one OFDM subcarrier that appears in the DFT outputs of the other subcarriers. In [OFDM](/orthogonal-frequency-division-multiplexing/) with a long enough [cyclic prefix](/cyclic-prefix/), the subcarriers are orthogonal over the DFT window, so each DFT output depends on one data symbol only: $Y[k] = H[k] X[k] + W[k]$. Orthogonality needs each subcarrier to make a whole number of turns in the window. Anything that changes the signal during the window breaks this: a carrier frequency offset between the transmitter and the receiver, the phase noise of the oscillators, or a channel that changes in time because of Doppler. Then each subcarrier is attenuated and rotated, and part of its power leaks to the others. This page treats the leakage between subcarriers inside one symbol. [Intersymbol interference](/intersymbol-interference/) between successive OFDM symbols, which the prefix removes, is a different effect. The same mechanism appears in spectral analysis as [spectral leakage](/spectral-leakage/). The page uses $j$ for the imaginary unit, the unitary DFT pair of the OFDM page, and $\varepsilon = \Delta f\, N / f_s$ for the frequency offset $\Delta f$ normalized to the subcarrier spacing $f_s / N$.

## In plain words

The receiver of an OFDM symbol is like a row of tuned glasses, one per subcarrier. Each glass responds only to its own tone, as long as every tone is exactly on its own pitch. If the receiver is slightly out of tune, every tone sits a little between two glasses. Then each glass rings a bit weaker, and it also picks up a little of the neighbor tones. That pickup is inter-carrier interference. It acts like extra noise that grows with the size of the mistuning, and it does not go away when you send with more power. Shaky oscillators and fast motion cause the same kind of leakage.

## The idea

**Frequency offset.** Let the receiver see the samples $e^{j 2\pi \varepsilon n / N}\, c[n] + w[n]$ inside the DFT window, where $c$ is the circular convolution of the channel and the OFDM symbol. Expanding $c$ in subcarriers and summing the geometric series gives the closed form

$$Y[k] = \sum_{m=0}^{N-1} H[m]\, X[m]\, S(m - k + \varepsilon) + W[k], \qquad S(x) = \frac{\sin(\pi x)}{N \sin(\pi x / N)}\, e^{j\pi x (N - 1)/N}.$$

The term $m = k$ is the wanted signal, scaled by $S(\varepsilon)$: its size drops to $\sin(\pi\varepsilon) / (N \sin(\pi\varepsilon/N))$, and all subcarriers rotate by the same angle $\pi\varepsilon(N-1)/N$. The terms $m \ne k$ are the ICI. For an integer $\varepsilon$, $S(m - k + \varepsilon)$ is zero except at $m = k - \varepsilon$, so the subcarriers are only shifted, with no leakage. Synchronizers for OFDM therefore estimate a fractional part, which causes ICI, and an integer part, which only renames the subcarriers.

**ICI power.** For independent data with $E|X[m]|^2 = E_s$ and $|H[m]| = 1$, the ICI power on a subcarrier is $E_s \sum_{m \ne k} |S(m - k + \varepsilon)|^2 = E_s (1 - |S(\varepsilon)|^2)$, because the values $|S(x + \varepsilon)|^2$ over a full set of $N$ shifts sum to 1 (Parseval for the window). For small $\varepsilon$, $1 - |S(\varepsilon)|^2 \approx (\pi\varepsilon)^2 / 3$, nearly independent of $N$. The ICI does not depend on the noise, so it sets a floor on the signal to interference ratio.

**SNR loss.** Pollet, Van Bladel and Moeneclaey treat the ICI as Gaussian noise and give, for small offsets, the SNR degradation $D \approx \frac{10}{3 \ln 10} (\pi\varepsilon)^2\, E_s / N_0$ dB, with $E_s / N_0$ the SNR per subcarrier. It is an approximation: it grows with the SNR, because at a high SNR the ICI is the main disturbance. The same paper gives the degradation for Wiener phase noise, which grows with the ratio of the oscillator linewidth to the subcarrier spacing.

**Phase noise.** A phase $\varphi[n]$ that changes inside the window gives $Y[k] = I_0 H[k] X[k] + \sum_{q \ne 0} I_q H[k - q] X[k - q] + W[k]$ with $I_q = \frac1N \sum_n e^{j\varphi[n]} e^{-j 2\pi q n / N}$. The factor $I_0$ is common to all subcarriers: its angle is the common phase error, which pilots can remove, as in [common phase error correction](/common-phase-error-correction/). The sum over $q \ne 0$ is ICI and has the power $1 - |I_0|^2$ for unit-energy data. A frequency offset is the special case $\varphi[n] = 2\pi\varepsilon n / N$.

**Doppler.** If the channel taps change during the window, the channel is no longer a circular convolution with fixed taps, and energy spreads over neighbor subcarriers, roughly over the range $\pm f_D N / f_s$ subcarriers for a maximum Doppler shift $f_D$ (see [Doppler spread](/doppler-spread/)). Unlike a frequency offset, the spread of Doppler shifts cannot be removed by one correction. The remedies are a larger subcarrier spacing, ICI-aware equalizers, pulse-shaped waveforms such as [filter bank multicarrier](/filter-bank-multicarrier/), or the delay-Doppler signaling of [OTFS](/orthogonal-time-frequency-space-modulation/).

## Examples

**Leakage for N = 64.** These values follow from the closed form above (exact for the model, computed to the digits shown):

| $\varepsilon$ | $\lvert S(\varepsilon)\rvert^2$ | ICI power $1 - \lvert S\rvert^2$ | $(\pi\varepsilon)^2/3$ | $E_s$ to ICI ratio |
|---|---|---|---|---|
| 0.02 | 0.998685 | 0.001315 | 0.001316 | 28.81 dB |
| 0.05 | 0.991804 | 0.008196 | 0.008225 | 20.86 dB |
| 0.1 | 0.967539 | 0.032461 | 0.032899 | 14.89 dB |
| 0.2 | 0.875168 | 0.124832 | 0.131595 | 9.04 dB |
| 0.5 | 0.405366 | 0.594634 | 0.822467 | 2.26 dB |

For $\varepsilon = 0.1$, the two nearest subcarriers contribute $0.01195$ and $0.00800$ of the power, more than half of the total ICI. The small-offset form is good up to about $\varepsilon = 0.1$ and poor at $0.5$. The last column is $10 \log_{10}(1 / (1 - |S|^2))$; the ratio of the scaled signal $|S|^2 E_s$ to the ICI is lower, $28.81$, $20.83$, $14.74$, $8.46$ and $-1.66$ dB.

**SNR loss at 10 dB.** Treat the ICI as noise, so the SINR is $|S(\varepsilon)|^2 E_s / (N_0 + (1 - |S(\varepsilon)|^2) E_s)$. At $E_s / N_0 = 10$ dB the loss $10 \log_{10}(\text{SNR}/\text{SINR})$ is $0.378$ dB for $\varepsilon = 0.05$ and $1.364$ dB for $\varepsilon = 0.1$. Pollet's approximation gives $0.357$ dB and $1.429$ dB. So a residual offset of a few percent of the spacing is the usual target for an OFDM synchronizer.

**What the offset is in hertz.** For IEEE 802.11a numbers, $f_s = 20$ MHz and $N = 64$, the spacing is $312.5$ kHz. A crystal error of 20 parts per million at 5.2 GHz is an offset of 104 kHz, $\varepsilon = 0.33$, far too large for data. The receiver must estimate it, for example with [Schmidl-Cox synchronization](/schmidl-cox-synchronization/) or the [Moose estimator](/moose-frequency-offset-estimator/), and remove it before the DFT.

## Where it is used

The ICI model tells a designer how precise the frequency synchronization of an OFDM receiver must be, how good its oscillators must be, and how large the subcarrier spacing must be for a given Doppler spread. It is why LTE and 5G NR use wider subcarrier spacing for high speeds and high carrier frequencies. The common phase part of the leakage is removed by pilots, and the remaining ICI is treated as noise in link budgets. Receivers for fast-moving users estimate the ICI terms and cancel them, and newer waveforms such as OTFS and AFDM were designed for channels where ICI in OFDM would be severe.

## References
