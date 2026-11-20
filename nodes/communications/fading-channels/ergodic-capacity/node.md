---
tag: 1ZFAY2
kind: definition
slug: ergodic-capacity
name: Ergodic capacity
aliases:
- average fading capacity
area: communications/fading-channels
level: core
summary: "The mean of log2(1 + gamma) over the fading, in bits per channel use. It is the capacity of a fading channel when each codeword spans many independent fades and the receiver knows the channel."
prereqs: [channel-capacity, rayleigh-fading-channel, expected-value]
see_also: [outage-capacity, outage-probability, channel-capacity, shannon-hartley-theorem, water-filling-power-allocation, truncated-channel-inversion, jensens-inequality, mimo-capacity]
sources:
  - book: isbn:9780521845274
    title: "David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005"
    locator: "Section 5.4.5 (the fast fading channel) and Section 5.4.6 (transmitter side information)"
  - book: isbn:9780521837163
    title: "Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005"
    locator: "Section 4.2.3 (channel side information at the receiver) and Section 4.2.4 (channel side information at the transmitter and receiver)"
  - paper: doi:10.1109/18.641562
    title: "A. J. Goldsmith and P. P. Varaiya, Capacity of fading channels with channel side information, IEEE Transactions on Information Theory 43(6), 1997, pages 1986 to 1992"
    locator: "the capacity with CSIT and CSIR, its water-filling power in time, and the comparison with channel inversion"
  - paper: doi:10.1109/25.293655
    title: "L. H. Ozarow, S. Shamai and A. D. Wyner, Information theoretic considerations for cellular mobile radio, IEEE Transactions on Vehicular Technology 43(2), 1994, pages 359 to 378"
    locator: "the average capacity of a fading channel against its capacity versus outage"
---

The ergodic capacity of a flat fading channel is the average of the instantaneous capacity $\log_2(1 + \gamma)$ over the distribution of the fading, $C_{\mathrm{erg}} = E[\log_2(1 + \gamma)]$ bits per channel use, for a receiver that knows the channel (CSIR). It is the right measure for fast fading, where a codeword spans so many independent fades that it sees their average. For slow fading, where one codeword sees one fade, the [outage probability](/outage-probability/) of a fixed rate and the [outage capacity](/outage-capacity/) $C_\epsilon$ replace it, because no positive rate is then safe in every fade.

## Definition

Take the flat fading channel $y_t = h_t x_t + w_t$, with $w_t \sim CN(0, N_0)$ i.i.d., an average power constraint $E|x_t|^2 \le P$, and a stationary and ergodic gain process $h_t$ with $E|h_t|^2 = 1$. Write $\rho = P/N_0$ for the average SNR, which is $\bar\gamma$ in the fading pages, and $\gamma = |h|^2\rho$ for the instantaneous SNR. With CSIR and no CSIT, the **ergodic capacity** is

$$C_{\mathrm{erg}} = E\big[\log_2(1 + |h|^2 \rho)\big] \quad \text{bits per channel use}.$$

This is a theorem in the following sense: when each codeword spans a number of independent fades that grows without bound (fast fading, or block fading with codewords over many blocks), every rate below $C_{\mathrm{erg}}$ can be reached with error probability tending to 0, and no rate above it can (Tse and Viswanath, Section 5.4.5; Goldsmith, Section 4.2.3). Gaussian inputs of power $P$ reach it, and the transmitter sends at a constant rate and power.

**With CSIT.** If the transmitter also knows $h_t$, it can vary its power $P(\gamma)$ with $E[P(\gamma)] \le P$. The capacity is then $\max E[\log_2(1 + \gamma P(\gamma)/P)]$, and the best power is the water-filling in time $P(\gamma)/P = (1/\gamma_0 - 1/\gamma)^+$, with the cutoff $\gamma_0$ set by the power constraint (Goldsmith and Varaiya 1997). See [water-filling power allocation](/water-filling-power-allocation/).

The capacity of a channel use is in bits with $\log_2$. With $\ln$ it is in nats, and $1$ nat $= \log_2 e = 1.4427$ bits.

## Examples and non-examples

**Rayleigh fading with CSIR.** Here $|h|^2$ is exponential with mean 1, and the closed form (Rayleigh fading, CSIR, Gaussian inputs) is $C_{\mathrm{erg}} = \log_2(e)\, e^{1/\rho} E_1(1/\rho)$, where $E_1(x) = \int_x^\infty e^{-t}/t\, dt$ is the exponential integral.

| $\rho$ | AWGN $\log_2(1 + \rho)$ | Rayleigh, CSIR | loss |
|---|---|---|---|
| -10 dB | 0.1375 | 0.1321 | 0.0054 |
| 0 dB | 1 | 0.8603 | 0.1397 |
| 10 dB | 3.4594 | 2.9065 | 0.5529 |
| 20 dB | 6.6582 | 5.8840 | 0.7742 |
| 30 dB | 9.9672 | 9.1436 | 0.8236 |

At high SNR, $C_{\mathrm{erg}} \approx \log_2\rho - \gamma_E \log_2 e$, with Euler's constant $\gamma_E = 0.5772$, so the loss tends to 0.8327 bit per channel use, the same as a power loss of 2.51 dB. At low SNR, $C_{\mathrm{erg}} \approx \rho \log_2 e$ for both channels, and fading costs almost nothing.

**Rayleigh fading with CSIT and CSIR.** With water-filling in time, the cutoff and the capacity are:

| $\rho$ | cutoff $\gamma_0$ | capacity with CSIT | CSIR only |
|---|---|---|---|
| 0 dB | 0.3938 | 1.0285 | 0.8603 |
| 10 dB | 0.7676 | 2.9794 | 2.9065 |
| 20 dB | 0.9516 | 5.8963 | 5.8840 |

Knowing the channel at the transmitter helps at low SNR, where the transmitter can save its power for good fades; at high SNR the gain is small. At 0 dB, the capacity with CSIT is above the AWGN value of 1 bit: fading helps when the transmitter can wait for strong fades.

**Receive diversity.** With [maximal ratio combining](/maximal-ratio-combining/) of two independent Rayleigh branches at 10 dB each, $\gamma$ has the gamma distribution with shape 2, and $C_{\mathrm{erg}} = 4.0586$ bits, against 4.3923 for an AWGN channel with the same mean SNR of 13 dB.

**Non-example: slow fading.** If $h$ stays fixed over the whole codeword (block fading with one block per codeword), the code sees one value of $\gamma$, not the average. In Rayleigh fading, $\Pr[\log_2(1 + \gamma) < R] > 0$ for every $R > 0$, so no positive rate has an error probability that tends to 0, and the capacity in the strict sense is 0. The useful measures are the outage probability and the [outage capacity](/outage-capacity/): at 10 dB, $C_{0.01} = 0.138$ bits and $C_{0.1} = 1.04$ bits, far below $C_{\mathrm{erg}} = 2.91$.

**Non-example: the capacity of the average SNR.** $\log_2(1 + E\gamma) = \log_2(1 + \rho)$ is the AWGN capacity at the same mean power. By [Jensen's inequality](/jensens-inequality/), $E\log_2(1 + \gamma) \le \log_2(1 + E\gamma)$, so with CSIR only, fading never increases the capacity.

**Non-example: channel inversion.** A transmitter that inverts the channel, $P(\gamma) \propto 1/\gamma$, gives the receiver a constant SNR. In Rayleigh fading $E[1/|h|^2] = \infty$, so this needs infinite power, and the capacity with full inversion is 0. [Truncated channel inversion](/truncated-channel-inversion/) stops sending in deep fades and has a positive capacity, below the ergodic capacity with water-filling.

## Related definitions

- **[Outage capacity](/outage-capacity/).** The largest rate with outage probability at most $\epsilon$, the measure for slow fading. It comes close to the ergodic capacity only when $\log_2(1 + \gamma)$ changes little from fade to fade, as with many independent branches.
- **[Outage probability](/outage-probability/).** $\Pr[\log_2(1 + \gamma) < R]$, the probability that a fixed rate fails in one fade.
- **[Channel capacity](/channel-capacity/).** The general definition; the ergodic capacity is the capacity of the fading channel with the receiver given $h$.
- **[Water-filling power allocation](/water-filling-power-allocation/).** The power allocation in time that reaches the capacity with CSIT.
- **[MIMO capacity](/mimo-capacity/).** The ergodic capacity $E[\log_2\det(I + (\rho/n) H H^*)]$ of a channel with $n$ transmit antennas.
- **[Channel hardening](/channel-hardening/).** With many antennas, $\log_2(1 + \gamma)$ is close to its mean in every fade, and the outage capacity approaches the ergodic capacity.

## References
