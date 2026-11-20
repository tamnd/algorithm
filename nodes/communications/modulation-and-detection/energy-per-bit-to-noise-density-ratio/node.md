---
tag: K0VXVH
kind: definition
slug: energy-per-bit-to-noise-density-ratio
name: Energy per bit to noise density ratio
aliases:
- "Eb/N0"
area: communications/modulation-and-detection
level: intro
summary: The received energy of one information bit divided by the noise power spectral density, the SNR measure that compares schemes of different rates.
prereqs: [additive-white-gaussian-noise-channel, digital-modulation]
see_also: [spectral-efficiency, shannon-hartley-theorem, channel-capacity, bit-error-rate, symbol-error-rate, digital-modulation, adaptive-modulation, channel-coding-theorem]
sources:
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008
    locator: Section 4.6, A Comparison of Digital Signaling Methods (bandwidth and dimensionality, the plane of spectral efficiency against SNR per bit, and the Shannon limit)
  - paper: doi:10.1109/JRPROC.1949.232969
    title: Claude E. Shannon, Communication in the presence of noise, Proceedings of the IRE 37(1), 10-21, 1949
    locator: the capacity W log2(1 + P/N) of a band-limited channel with white Gaussian noise
  - book: isbn:9780792375487
    title: John R. Barry, Edward A. Lee and David G. Messerschmitt, Digital Communication, third edition, Kluwer Academic Publishers, 2004
    locator: Chapter 6, Advanced Modulation (the comparison of modulation schemes by spectral efficiency and SNR per bit)
---

$E_b/N_0$ is the received energy per information bit divided by the one-sided power spectral density of the noise. It is the measure of signal strength that lets one compare schemes with different numbers of bits per symbol and different code rates, because it charges each scheme for the energy it spends per bit of information. It is one of three closely related quantities: [spectral efficiency](/spectral-efficiency/) counts bits per second per hertz, the [Shannon-Hartley theorem](/shannon-hartley-theorem/) gives the capacity for a given SNR, and $E_b/N_0$ is the energy side of the same trade, with the Shannon limit of $-1.59$ dB as its floor.

## Definition

Let a link deliver information bits at the rate $R_b$ (bit/s) with received signal power $P$ (W), in white Gaussian noise of one-sided power spectral density $N_0$ (W/Hz). The **energy per bit** is $E_b = P / R_b$, and

$$\frac{E_b}{N_0} = \frac{P}{N_0 R_b},$$

a ratio without units, usually given in decibels: $10 \log_{10}(E_b/N_0)$ dB.

**From symbols to bits.** For a constellation of $M$ points and a channel code of rate $R$, each symbol carries $R \log_2 M$ information bits, so with $E_s = \mathbb{E}|x|^2$ the energy per symbol,

$$E_b = \frac{E_s}{R \log_2 M}, \qquad \frac{E_b}{N_0}\Big|_{\mathrm{dB}} = \frac{E_s}{N_0}\Big|_{\mathrm{dB}} - 10\log_{10}(R \log_2 M).$$

Area pages use "SNR" for $E_s/N_0$ unless they say otherwise. For uncoded BPSK the two ratios are equal; for uncoded QPSK, $E_s/N_0$ is 3.01 dB larger.

**From $E_b/N_0$ to the SNR in a bandwidth.** If $B$ is the noise bandwidth, the noise power is $N_0 B$, so

$$\mathrm{SNR} = \frac{P}{N_0 B} = \frac{E_b}{N_0} \cdot \frac{R_b}{B} = \eta\, \frac{E_b}{N_0},$$

where $\eta = R_b/B$ is the spectral efficiency. For a real channel $y = x + z$ with $z \sim \mathcal{N}(0, \sigma^2)$, as used in the [AWGN channel](/additive-white-gaussian-noise-channel/) page, $\sigma^2 = N_0/2$ per real dimension, so $P/\sigma^2 = 2E_s/N_0$ for one real symbol of energy $E_s$.

**The Shannon limit.** *Theorem.* On the AWGN channel with bandwidth $B$, reliable transmission at the spectral efficiency $\eta$ is possible only if

$$\frac{E_b}{N_0} \ge \frac{2^\eta - 1}{\eta},$$

and the right side decreases to $\ln 2$ as $\eta \to 0$. So no scheme of any bandwidth can work below $E_b/N_0 = \ln 2 = 0.6931$, which is $-1.5917$ dB.

*Proof.* By the capacity formula, reliable transmission needs $\eta \le \log_2(1 + \mathrm{SNR}) = \log_2(1 + \eta E_b/N_0)$; solve for $E_b/N_0$. The function $f(\eta) = (e^{\eta \ln 2} - 1)/\eta$ is the slope of the chord of the convex function $e^{s\ln 2}$ from $0$ to $\eta$, so it increases with $\eta$, and its limit at $0$ is the derivative $\ln 2$. $\square$

## Examples and non-examples

**The bound at several spectral efficiencies.**

| $\eta$ (bit/s/Hz) | $(2^\eta - 1)/\eta$ | in dB |
|---|---|---|
| $\to 0$ | 0.6931 | $-1.59$ |
| 0.5 | 0.8284 | $-0.82$ |
| 1 | 1 | 0 |
| 2 | 1.5 | 1.76 |
| 4 | 3.75 | 5.74 |
| 6 | 10.5 | 10.21 |
| 8 | 31.875 | 15.03 |

As $\eta$ grows, the cost of each extra bit/s/Hz approaches $10\log_{10} 2 = 3.01$ dB; from $\eta = 6$ to $\eta = 8$ it is 2.4 dB per bit/s/Hz.

**The gap of an uncoded scheme.** Uncoded QPSK reaches the [bit error rate](/bit-error-rate/) $10^{-5}$ at $E_b/N_0 = 9.59$ dB with $\eta = 2$ (ideal pulses). The bound at $\eta = 2$ is 1.76 dB, so the gap is 7.83 dB, and the gap to the absolute limit of $-1.59$ dB is 11.18 dB. Channel codes close most of this gap.

**Coded schemes.** BPSK with a code of rate 1/2 has $E_s/N_0 = E_b/N_0 - 3.01$ dB: each symbol carries half a bit. 16-QAM with a code of rate 3/4 carries 3 bits per symbol, so $E_s/N_0 = E_b/N_0 + 4.77$ dB.

**A link budget.** Thermal noise at the reference temperature $T_0 = 290$ K has $N_0 = k T_0 = 4.004 \times 10^{-21}$ W/Hz, that is $-173.98$ dBm/Hz, where $k$ is Boltzmann's constant. A received power of $-100$ dBm at $R_b = 1$ Mbit/s (60 dB above 1 bit/s) gives $E_b/N_0 = -100 - 60 + 173.98 = 13.98$ dB, before the noise figure of the receiver is subtracted.

**Non-example: $E_s/N_0$.** The ratio per symbol is not per bit. 16-QAM and QPSK at the same $E_s/N_0$ are not a fair comparison, because 16-QAM carries twice as many bits with the same energy per symbol.

**Non-example: SNR in a bandwidth.** $P/(N_0 B)$ depends on the bandwidth that the receiver counts as noise, so two receivers can report different SNRs for the same signal. $E_b/N_0$ depends only on the power, the noise density and the bit rate.

## Related definitions

- **Spectral efficiency.** $\eta = R_b / B$, the other axis of the bandwidth and power trade; see [spectral efficiency](/spectral-efficiency/).
- **Capacity.** $C = B \log_2(1 + P/(N_0 B))$ by the [Shannon-Hartley theorem](/shannon-hartley-theorem/); see also [channel capacity](/channel-capacity/) and the [channel coding theorem](/channel-coding-theorem/).
- **Energy per symbol.** $E_s = E_b R \log_2 M$; the [symbol error rate](/symbol-error-rate/) is most naturally written in $E_s/N_0$, and the [bit error rate](/bit-error-rate/) in $E_b/N_0$.
- **Carrier to noise density.** $C/N_0 = P/N_0$ in dB-Hz; $E_b/N_0 = C/N_0 - 10\log_{10} R_b$.

## References
