---
tag: R119Y0
kind: concept
slug: snr-gap-approximation
name: SNR gap approximation
aliases:
- SNR gap
- gap to capacity
area: communications/link-adaptation-and-resource-allocation
level: core
summary: "Writes the rate of a practical code and constellation as log2(1 + SNR/Gamma). The gap Gamma depends on the target error rate and the code; it is a design rule, not a theorem."
prereqs: [channel-capacity, quadrature-amplitude-modulation, gaussian-q-function]
see_also: [water-filling-power-allocation, bit-loading, chow-cioffi-bingham-algorithm, adaptive-modulation, shannon-hartley-theorem, symbol-error-rate, discrete-multitone, spectral-efficiency]
sources:
  - paper: doi:10.1109/18.720542
    title: "G. David Forney, Jr. and Gottfried Ungerboeck, Modulation and coding for linear Gaussian channels, IEEE Transactions on Information Theory 44(6), 1998, pages 2384 to 2415"
    locator: "the normalized SNR, the gap of uncoded QAM to capacity, and its split into coding gain and shaping gain"
  - paper: doi:10.1109/35.54342
    title: "John A. C. Bingham, Multicarrier modulation for data transmission: an idea whose time has come, IEEE Communications Magazine 28(5), 1990, pages 5 to 14"
    locator: "the gap and margin used to load the subchannels of a multicarrier modem"
  - book: isbn:9780521837163
    title: "Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005"
    locator: "Chapter 9 (the constellation size of M-QAM at a target bit error rate, written with the factor K = -1.5/ln(5 BER))"
---

The SNR gap approximation writes the number of bits that a real modulation and code carry per complex symbol, at a fixed target error rate, as $b = \log_2(1 + \mathrm{SNR}/\Gamma)$. Here SNR is $E_s/N_0$ per complex symbol and $\Gamma \ge 1$ is the gap: the factor by which the system needs more SNR than the [Shannon capacity](/channel-capacity/) $\log_2(1 + \mathrm{SNR})$ to carry the same rate. For uncoded square QAM the formula follows from the [symbol error rate](/symbol-error-rate/) at high SNR, with $\Gamma = (Q^{-1}(P_e/N_e))^2/3$, which is about 9 dB at the error rates of DSL modems. A code with coding gain $\gamma_c$ divides $\Gamma$ by $\gamma_c$, and a system margin multiplies it. The gap is a design rule with stated limits, not a theorem: it lets [water-filling](/water-filling-power-allocation/) and [bit loading](/bit-loading/) use the capacity formula for real constellations.

## In plain words

The capacity formula tells how many bits a channel can carry with an ideal code. A real modem uses a fixed set of points and a simple code, and it must keep its errors below a target. To carry the same number of bits, it needs a stronger signal than the ideal formula says.

The gap is that extra factor of signal strength. For a given error target and a given code, it stays nearly the same over a wide range of signal strengths. So an engineer can take the ideal formula, divide the signal strength by the gap, and read off a good estimate of what the real modem can carry. A better code makes the gap smaller. A safety margin makes it larger.

## The idea

**Derivation for uncoded QAM.** Take square $M$-QAM with Gray labels, unit average energy and SNR $= E_s/N_0$. Each real dimension is a $\sqrt{M}$-PAM, and its symbol error probability is

$$\bar P_e = 2\left(1 - \frac{1}{\sqrt{M}}\right) Q\!\left(\sqrt{\frac{3\,\mathrm{SNR}}{M - 1}}\right) \approx \bar N_e\, Q\!\left(\sqrt{\frac{3\,\mathrm{SNR}}{M - 1}}\right),$$

with $\bar N_e = 2$, the number of nearest neighbors per dimension of an inner point; [Q](/gaussian-q-function/) is the Gaussian tail function. Fix the target $\bar P_e$ and solve the approximation for $M$:

$$M - 1 = \frac{3\,\mathrm{SNR}}{\left(Q^{-1}(\bar P_e/\bar N_e)\right)^2} = \frac{\mathrm{SNR}}{\Gamma}, \qquad \Gamma = \frac{\left(Q^{-1}(\bar P_e/\bar N_e)\right)^2}{3}.$$

So $b = \log_2 M = \log_2(1 + \mathrm{SNR}/\Gamma)$. The only approximation is the factor $1 - 1/\sqrt{M} \approx 1$ and the neglect of the $-Q^2$ term of the QAM error rate, so the rule is close for large $M$ and a little pessimistic for small $M$.

**Normalized SNR.** Forney and Ungerboeck define $\mathrm{SNR}_{\mathrm{norm}} = \mathrm{SNR}/(2^b - 1)$ for a system that sends $b$ bits per complex symbol. Capacity says that reliable transmission needs $\mathrm{SNR}_{\mathrm{norm}} > 1$, or 0 dB. The gap of a scheme at a target error rate is the $\mathrm{SNR}_{\mathrm{norm}}$ it needs there. For uncoded QAM, the symbol error rate per dimension is about $2\,Q(\sqrt{3\,\mathrm{SNR}_{\mathrm{norm}}})$, the same curve for every large $M$, which is why one number describes all large constellations.

**Coding gain, shaping gain and margin.** In dB, the gap that a design uses is

$$\Gamma_{\mathrm{dB}} = \Gamma_{\mathrm{uncoded,dB}} - \gamma_{c,\mathrm{dB}} + \gamma_{m,\mathrm{dB}},$$

where $\gamma_c$ is the coding gain at the target error rate and $\gamma_m$ is a margin against noise that the receiver did not measure. Forney and Ungerboeck split the gap of uncoded QAM into a part that coding recovers and a shaping part that only a constellation boundary closer to a sphere recovers. The shaping gain is at most $\pi e/6$, or 1.533 dB.

**What kind of claim it is.** The derivation is exact algebra on an approximation of the error rate, so for uncoded QAM the rule is a high-SNR approximation with a known error. For coded systems, $\Gamma$ is measured or fitted: the coding gain changes slowly with the rate and the SNR, and the rule treats it as constant. It is a design rule in both cases.

**One bit per 3 dB.** At high SNR, $\log_2(1 + \mathrm{SNR}/\Gamma) \approx \log_2 \mathrm{SNR} - \log_2 \Gamma$, so the gap costs $\log_2 \Gamma$ bits per complex symbol, one bit for each $10 \log_{10} 2 = 3.0103$ dB.

## Examples

**The gap of uncoded QAM.** The values of $\Gamma = (Q^{-1}(\bar P_e/\bar N_e))^2/3$:

| target $\bar P_e$ | $\bar N_e = 1$ | $\bar N_e = 2$ |
|---|---|---|
| $10^{-3}$ | | 5.574 dB |
| $10^{-5}$ | | 8.132 dB |
| $10^{-6}$ | 8.769 dB | 9.018 dB |
| $10^{-7}$ | 9.548 dB | 9.758 dB |

The value "9.8 dB" that DSL texts quote for uncoded QAM at $10^{-7}$ is the last entry, with the per-dimension error rate and $\bar N_e = 2$. Counting four neighbors per complex symbol at $10^{-6}$ per symbol gives 9.254 dB instead; a gap value is incomplete without its error target and its neighbor count.

**How close the rule is.** For square $M$-QAM at $\bar P_e = 10^{-6}$, compare the SNR that the exact per-dimension formula needs with the rule $\Gamma (M - 1)$, with $\Gamma = 9.018$ dB:

| $M$ | exact SNR | rule $\Gamma(M-1)$ | rule minus exact |
|---|---|---|---|
| 4 | 13.540 dB | 13.789 dB | 0.249 dB |
| 16 | 20.677 dB | 20.779 dB | 0.102 dB |
| 64 | 26.964 dB | 27.011 dB | 0.047 dB |
| 256 | 33.061 dB | 33.083 dB | 0.023 dB |
| 1024 | 39.106 dB | 39.117 dB | 0.011 dB |

The rule asks for slightly too much SNR, by less than 0.25 dB from 4-QAM up.

**The rate at 30 dB.** At SNR = 30 dB, capacity is $\log_2 1001 = 9.967$ bits per complex symbol. With the gap 9.758 dB, uncoded QAM carries $\log_2(1 + 1000/9.457) = 6.738$ bits, about 3.24 bits less, as the rule of one bit per 3 dB predicts. With a code of 5 dB coding gain and a margin of 6 dB, the gap is $9.758 - 5 + 6 = 10.758$ dB, and the rate is 6.409 bits.

**Adaptive QAM.** Goldsmith and Chua bound the bit error rate of $M$-QAM by $0.2\, e^{-1.5\,\mathrm{SNR}/(M-1)}$ for $M \ge 4$ and a bit error rate at most $10^{-3}$, a fit. Solving for $M$ gives $M = 1 + K\,\mathrm{SNR}$ with $K = -1.5/\ln(5\,\mathrm{BER})$, so $1/K$ is a gap. It is 5.480 dB at a bit error rate of $10^{-3}$ and 9.105 dB at $10^{-6}$; see [adaptive modulation](/adaptive-modulation/).

**A non-example.** The rule does not fit binary codes at low SNR or the region near capacity of a modern code. A turbo or LDPC code at rate 1/2 on BPSK works at an $E_b/N_0$ about 1 dB or less from its limit; there the error rate falls in a cliff, and a constant $\Gamma$ over a range of SNR has no meaning. Link adaptation then uses a table of measured thresholds per code instead.

## Where it is used

- **Bit loading.** The power to carry $b$ bits on a subcarrier with SNR per unit power $g$ is $\Gamma(2^b - 1)/g$. The [Hughes-Hartogs](/hughes-hartogs-algorithm/), [Levin-Campello](/levin-campello-algorithm/) and [Chow-Cioffi-Bingham](/chow-cioffi-bingham-algorithm/) algorithms all use this cost, and its doubling with each bit makes the incremental costs increase, which is the condition for the greedy methods to be optimal.
- **Water-filling with a gap.** Using $\log_2(1 + p_i/(\Gamma \nu_i))$ is [water-filling](/water-filling-power-allocation/) on the scaled levels $\Gamma \nu_i$.
- **DSL and multicarrier modems.** [Discrete multitone](/discrete-multitone/) modems compute the bits of each tone from its measured SNR, a gap and a margin; Bingham's 1990 paper describes this practice.
- **Rate tables in link adaptation.** A first estimate of the switching thresholds of [link adaptation](/link-adaptation/) is $\Gamma(2^{b_j} - 1)$ for the rates $b_j$, before calibration by simulation.
- **Comparing schemes.** Plotting the error rate against $\mathrm{SNR}_{\mathrm{norm}}$ puts schemes of different rates on one axis, and the gap at a target error rate is a fair figure of merit.

## References
