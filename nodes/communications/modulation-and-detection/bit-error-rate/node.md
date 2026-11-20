---
tag: 45MRX1
kind: definition
slug: bit-error-rate
name: Bit error rate
aliases:
- BER
- bit error probability
area: communications/modulation-and-detection
level: intro
summary: The fraction of transmitted bits that the receiver gets wrong, the main figure of merit of a digital link.
prereqs: [symbol-error-rate, gray-labeling, energy-per-bit-to-noise-density-ratio]
see_also: [symbol-error-rate, gray-labeling, energy-per-bit-to-noise-density-ratio, gaussian-q-function, binary-symmetric-channel, shannon-hartley-theorem, rayleigh-fading-channel, hamming-distance]
sources:
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008
    locator: Sections 4.3-1 to 4.3-3 (the bit error probabilities of PAM, PSK and QAM with Gray coding) and Section 4.6 (the comparison of signaling methods by the SNR per bit)
  - paper: doi:10.1109/TCOMM.2002.800818
    title: Kyongkuk Cho and Dongweon Yoon, On the general BER expression of one- and two-dimensional amplitude modulations, IEEE Transactions on Communications 50(7), 1074-1080, 2002
    locator: the closed-form exact bit error probability of Gray-coded M-PAM and of square and rectangular QAM in AWGN
  - book: isbn:9780471649533
    title: Marvin K. Simon and Mohamed-Slim Alouini, Digital Communication over Fading Channels, second edition, Wiley, 2005
    locator: Chapter 4, Alternative Representations of Classical Functions (the integral forms used for bit error probabilities in AWGN and in fading)
---

The bit error rate (BER) is the probability that a transmitted information bit is received wrong, or, for a measurement, the fraction of bits that were wrong. It is the figure of merit that users of a link care about, because they receive bits, not symbols. The [symbol error rate](/symbol-error-rate/) counts wrong symbols; the BER also depends on how bits are attached to the points, the labeling, and with a [Gray labeling](/gray-labeling/) it is close to the symbol error rate divided by $\log_2 M$. The formulas on this page are written in terms of $E_b/N_0$, the [energy per bit to noise density ratio](/energy-per-bit-to-noise-density-ratio/), so that schemes with different numbers of bits per symbol can be compared.

## Definition

Let a constellation of $M = 2^k$ points have labels $\ell_0, \ldots, \ell_{M-1}$ of $k$ bits, priors $\pi_i$, and a decision rule with transition probabilities $P(j \mid i) = \Pr[\text{decide } j \mid a_i \text{ sent}]$. The **bit error rate** of an uncoded link is the mean number of wrong bits per bit sent:

$$P_b = \frac{1}{k}\sum_i \pi_i \sum_{j \ne i} P(j \mid i)\, d_H(\ell_i, \ell_j),$$

where $d_H$ is the [Hamming distance](/hamming-distance/). It is the average over the $k$ bit positions of the probability that the bit in that position is wrong. The **measured** BER is the number of wrong bits divided by the number of bits sent. For a coded link, the BER usually means the rate after decoding; the rate at the detector output is then called the raw or pre-decoding BER.

**Relation to the SER.** *Theorem.* For every labeling, $\mathrm{SER}/k \le P_b \le \mathrm{SER}$, since a wrong symbol changes between 1 and $k$ bits. With a Gray labeling at high SNR, $P_b \approx \mathrm{SER}/k$; this is an approximation, because errors beyond the nearest neighbors change more than one bit.

**Closed forms in AWGN.** These hold under these assumptions: complex AWGN $\mathcal{CN}(0, N_0)$, equal priors, minimum distance detection, Gray labeling, no channel code, and $\gamma_b = E_b/N_0$, so $E_s = k E_b$. Here $Q$ is the [Gaussian Q-function](/gaussian-q-function/).

| Scheme | $P_b$ | exact or approximate |
|---|---|---|
| BPSK, QPSK | $Q(\sqrt{2\gamma_b})$ | exact |
| $M$-PAM | $\frac{2(1 - 1/M)}{k}\, Q\big(\sqrt{6k\gamma_b/(M^2-1)}\big)$ | approximate, $\mathrm{SER}/k$ |
| square $M$-QAM | $\frac{4(1 - 1/\sqrt{M})}{k}\, Q\big(\sqrt{3k\gamma_b/(M-1)}\big)$ | approximate, nearest neighbors |
| $M$-PSK, $M \ge 4$ | $\frac{2}{k}\, Q\big(\sqrt{2k\gamma_b}\,\sin(\pi/M)\big)$ | approximate, nearest neighbors |
| 4-PAM | $\tfrac{1}{4}\big(3Q(a) + 2Q(3a) - Q(5a)\big)$, $a = \sqrt{4\gamma_b/5}$ | exact |
| 16-QAM | $\tfrac{1}{4}\big(3Q(a) + 2Q(3a) - Q(5a)\big)$, $a = \sqrt{4\gamma_b/5}$ | exact |

The exact forms for PAM and QAM of any size are finite sums of $Q$ terms (Cho and Yoon 2002). Gray 16-QAM has the same exact BER as Gray 4-PAM at the same $E_b/N_0$, because its labels are a 4-PAM label on each axis and the two axes have independent noise. QPSK has the BER of BPSK for the same reason.

**The floor.** By the [Shannon-Hartley theorem](/shannon-hartley-theorem/), no scheme, coded or not, can reach an arbitrarily small BER below $E_b/N_0 = \ln 2$, which is $-1.59$ dB. Uncoded schemes are far from this limit.

## Examples and non-examples

**BPSK.** $P_b = Q(\sqrt{2\gamma_b})$ is 0.078650 at $E_b/N_0 = 0$ dB, 0.012501 at 4 dB, $2.3883 \times 10^{-3}$ at 6 dB, $1.9091 \times 10^{-4}$ at 8 dB, $9.736 \times 10^{-6}$ at 9.6 dB and $3.8721 \times 10^{-6}$ at 10 dB. $P_b = 10^{-5}$ needs 9.588 dB.

**16-QAM at $E_b/N_0 = 10$ dB.** Here $E_s/N_0 = 16.02$ dB and $a = \sqrt{8}$. The exact BER is $1.7542 \times 10^{-3}$; $\mathrm{SER}/4 = 1.7511 \times 10^{-3}$ with $\mathrm{SER} = 7.0043 \times 10^{-3}$.

**The cost of more bits per symbol.** The $E_b/N_0$ needed for $P_b = 10^{-5}$ with Gray labels, computed as $\mathrm{SER}/k$ from the exact SER: 9.59 dB for BPSK and QPSK, 12.97 dB for 8-PSK, 13.44 dB for 16-QAM and 4-PAM, 17.44 dB for 16-PSK and 17.79 dB for 64-QAM. 4-PAM needs the same as 16-QAM because 16-QAM is two 4-PAM signals; it carries half the bits per symbol.

**The labeling matters.** 4-PAM at $E_s/N_0 = 15$ dB has the same SER, $2.818 \times 10^{-4}$, with any labeling. Its BER is $1.4090 \times 10^{-4}$ with the Gray labels and $1.8787 \times 10^{-4}$ with the natural binary labels.

**Non-example: BER on a fading channel.** On a [Rayleigh fading channel](/rayleigh-fading-channel/), the BER of BPSK with average $E_b/N_0 = \bar\gamma$ is $\tfrac{1}{2}\big(1 - \sqrt{\bar\gamma/(1 + \bar\gamma)}\big)$, which falls only like $1/(4\bar\gamma)$. At 10 dB it is 0.02327, against $3.87 \times 10^{-6}$ in AWGN. The AWGN formulas do not apply there.

**Non-example: the bit error probability of one bit position.** In 16-QAM with Gray labels, the bit that chooses the sign on an axis is more reliable than the bit that chooses inner or outer. The BER is the average over the positions; the individual positions have different error rates, which [bit-interleaved coded modulation](/bit-interleaved-coded-modulation/) has to take into account.

## Related definitions

- **Symbol error rate.** The probability of a wrong symbol; see [symbol error rate](/symbol-error-rate/).
- **Binary symmetric channel.** Hard decisions on BPSK turn the AWGN channel into a [binary symmetric channel](/binary-symmetric-channel/) with crossover probability $P_b$.
- **Labeling.** [Gray labeling](/gray-labeling/) makes $P_b$ close to its lower bound $\mathrm{SER}/k$.
- **Measuring the BER.** The measured BER is an estimate with a confidence interval, as for the SER. The bits of one symbol fail together, so an interval computed as if the bits were independent is too narrow; counting the errors per symbol or per block of symbols avoids this.

## References
