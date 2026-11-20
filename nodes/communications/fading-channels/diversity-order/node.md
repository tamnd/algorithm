---
tag: C0WHEB
kind: definition
slug: diversity-order
name: Diversity order
aliases:
- diversity gain
area: communications/fading-channels
level: core
summary: "The high-SNR slope of the error or outage probability on a log-log plot, d = -lim log Pe / log gamma_bar. It counts the independent fades a scheme uses; it is not the function d(r) of the DMT."
prereqs: [rayleigh-fading-channel, outage-probability, bit-error-rate]
see_also: [maximal-ratio-combining, equal-gain-combining, selection-combining, diversity-multiplexing-tradeoff, rank-and-determinant-criteria, outage-probability, alamouti-code, nakagami-m-fading-channel]
sources:
  - book: isbn:9780521845274
    title: "David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005"
    locator: "Section 5.4.2 (receive diversity) and Section 5.4.4 (time and frequency diversity)"
  - book: isbn:9780521837163
    title: "Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005"
    locator: "Chapter 7 (diversity), with Sections 7.2.2, 7.2.4 and 7.2.5 on selection, maximal ratio and equal gain combining"
  - book: isbn:9780471649533
    title: "Marvin K. Simon and Mohamed-Slim Alouini, Digital Communication over Fading Channels, 2nd edition, Wiley, 2005"
    locator: "Chapter 9 (diversity combining)"
---

The diversity order of a transmission scheme over a fading channel is the exponent $d$ with which its error probability falls at high average SNR, $P_e \approx (G_c\bar\gamma)^{-d}$; on a plot of $\log P_e$ against $\bar\gamma$ in dB it is the slope, in decades per 10 dB. It is a property of a scheme and a channel model, not an algorithm: [maximal ratio combining](/maximal-ratio-combining/), [equal gain combining](/equal-gain-combining/) and [selection combining](/selection-combining/) of $L$ independent Rayleigh branches all have diversity order $L$, and they differ only in the constant $G_c$. The alias "diversity gain" is common, but in the [diversity-multiplexing tradeoff](/diversity-multiplexing-tradeoff/) the diversity gain $d(r)$ is a function of the multiplexing gain $r$; the diversity order here is the single number for a scheme of fixed rate.

## Definition

Let $P_e(\bar\gamma)$ be the error probability of a scheme, such as the [bit error rate](/bit-error-rate/) or the word error rate, or the [outage probability](/outage-probability/), as a function of the average SNR per branch $\bar\gamma = E|h|^2 E_s/N_0$, at a fixed rate and with a fixed fading model. The **diversity order** is

$$d = -\lim_{\bar\gamma \to \infty} \frac{\log P_e(\bar\gamma)}{\log \bar\gamma},$$

when the limit exists. If $P_e(\bar\gamma) = (G_c\bar\gamma)^{-d}(1 + o(1))$, then $d$ is the diversity order and $G_c$ is the **coding gain**, the shift of the curve along the $\bar\gamma$ axis. When $P_e$ falls faster than every power of $\bar\gamma$, as in a channel without fading, the limit is $+\infty$.

A scheme has **full diversity** when $d$ equals the number of independent fading coefficients that carry the symbol: $L$ for $L$ receive branches, $n m$ for a MIMO channel with $n$ transmit and $m$ receive antennas and i.i.d. Rayleigh fading, and $L$ for a codeword spread over $L$ independent fades in time or frequency.

The fading model, what the receiver knows (usually CSIR and no CSIT), and the time model (block fading, where one codeword sees a fixed number of independent fades) must be stated with $d$. In fast fading with codewords over very many independent fades, the error probability of a good code falls faster than every power of $\bar\gamma$ at rates below the [ergodic capacity](/ergodic-capacity/), and diversity order is not the useful measure.

## Examples and non-examples

**One Rayleigh branch: $d = 1$.** For coherent BPSK, $P_b = \frac12(1 - \sqrt{\bar\gamma/(1 + \bar\gamma)}) \approx 1/(4\bar\gamma)$, a closed form for Rayleigh fading with perfect CSIR. The values are 0.023269 at 10 dB and 0.0024814 at 20 dB, one decade per 10 dB. The outage at a fixed rate $R$, $1 - e^{-(2^R - 1)/\bar\gamma} \approx (2^R - 1)/\bar\gamma$, also has $d = 1$.

**$L$ independent Rayleigh branches: $d = L$.** For BPSK at 10 and 20 dB per branch, the slope between the two points, $\log_{10}(P_e(10\ \mathrm{dB})/P_e(20\ \mathrm{dB}))$, is:

| scheme | $P_b$ at 10 dB | $P_b$ at 20 dB | slope | $d$ |
|---|---|---|---|---|
| one branch | 0.023269 | $2.4814 \cdot 10^{-3}$ | 0.97 | 1 |
| maximal ratio combining, $L = 2$ | $1.5991 \cdot 10^{-3}$ | $1.8442 \cdot 10^{-5}$ | 1.94 | 2 |
| equal gain combining, $L = 2$ | $2.0704 \cdot 10^{-3}$ | $2.4508 \cdot 10^{-5}$ | 1.93 | 2 |
| selection combining, $L = 2$ | $2.9729 \cdot 10^{-3}$ | $3.6581 \cdot 10^{-5}$ | 1.91 | 2 |
| maximal ratio combining, $L = 4$ | $9.698 \cdot 10^{-6}$ | $1.319 \cdot 10^{-9}$ | 3.87 | 4 |
| selection combining, $L = 4$ | $1.4870 \cdot 10^{-4}$ | $3.003 \cdot 10^{-8}$ | 3.69 | 4 |

The slope between two finite SNR values is below $d$ and tends to it. For maximal ratio combining, the closed form $P_b \approx \binom{2L-1}{L}(4\bar\gamma)^{-L}$ shows $d = L$ directly. The three combiners have the same $d$ and different coding gains.

**Nakagami-$m$ fading: $d = m$.** A [Nakagami](/nakagami-m-fading-channel/) channel with parameter $m$ has $\Pr[|h|^2 < \epsilon] \approx c\,\epsilon^m$ near 0, so it acts like $m$ Rayleigh branches with maximal ratio combining; $m$ need not be an integer.

**Space-time codes.** The [Alamouti code](/alamouti-code/) with 2 transmit and $m$ receive antennas has $d = 2m$ without CSIT. In general, the [rank criterion](/rank-and-determinant-criteria/) of Tarokh, Seshadri and Calderbank (1998) gives the diversity order of a space-time code as $m$ times the minimum rank of its codeword difference matrices.

**Repetition over independent fades.** A [repetition code](/repetition-code/) that sends a symbol $L$ times, with [interleaving](/interleaving/) deep enough that each copy sees an independent fade, has $d = L$. The same repetition inside one coherence time has $d = 1$: the copies fade together.

**Non-example: correlated branches.** Two antennas with fully correlated fades give $d = 1$, whatever the combiner. For jointly Gaussian branch gains with covariance matrix $\Sigma$, maximal ratio combining has $d = \operatorname{rank}\Sigma$; partial correlation keeps $d$ and lowers the coding gain.

**Non-example: Rician fading.** With a fixed Rician factor $K$, the [Rician](/rician-fading-channel/) channel still has $d = 1$, since $|h|^2$ has a positive density at 0. A strong line of sight improves $G_c$, so the curve is steep over a range of $\bar\gamma$ before it reaches slope 1.

**Non-example: array gain.** Maximal ratio combining of $L$ branches raises the mean SNR by $L$, and selection combining by $1 + \frac12 + \cdots + \frac1L$. This array gain shifts the curve and is part of $G_c$; it is not the diversity order.

**Non-example: the AWGN channel.** Without fading, $P_b = Q(\sqrt{2\gamma})$ falls like $e^{-\gamma}$, faster than every power, so $d = +\infty$. Diversity order measures how well a scheme fights deep fades, and a channel without fades has none.

## Related definitions

- **[Diversity-multiplexing tradeoff](/diversity-multiplexing-tradeoff/).** Zheng and Tse (2003) let the rate grow as $r\log_2\bar\gamma$ and define the diversity gain $d(r)$ as the slope of the outage probability. The diversity order of a fixed-rate scheme corresponds to $r = 0$, and $d(0) = nm$ for i.i.d. Rayleigh MIMO channels.
- **Coding gain.** The constant $G_c$ in $P_e \approx (G_c\bar\gamma)^{-d}$, which sets the horizontal position of the curve at high SNR.
- **Array gain.** The increase of the mean output SNR from combining, $L$ for maximal ratio combining. It is part of the coding gain.
- **[Outage probability](/outage-probability/).** In block fading, good codes reach the slope of the outage probability at the same rate, so the outage is often used to compute $d$.
- **[Channel hardening](/channel-hardening/).** With many independent branches, the combined SNR is close to its mean; this is the limit $d \to \infty$.
- **[Multiuser diversity](/multiuser-diversity/).** Selection over $K$ users with independent fades, which gives a diversity order of $K$ for the scheduled link.

## References
