---
tag: PZPFQZ
kind: definition
slug: outage-capacity
name: Outage capacity
aliases:
- epsilon-outage capacity
area: communications/fading-channels
level: core
summary: "The largest rate R whose outage probability Pr[log2(1 + gamma) < R] is at most epsilon, in bits per channel use. It is the capacity measure for slow fading, where one codeword sees one fade."
prereqs: [outage-probability, rayleigh-fading-channel, channel-capacity]
see_also: [outage-probability, ergodic-capacity, diversity-order, maximal-ratio-combining, selection-combining, diversity-multiplexing-tradeoff, channel-capacity, rayleigh-fading-channel]
sources:
  - book: isbn:9780521845274
    title: "David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005"
    locator: "Section 5.4.1 (the slow fading channel and the epsilon-outage capacity) and Section 5.4.2 (receive diversity)"
  - book: isbn:9780521837163
    title: "Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005"
    locator: "Section 4.2.3 (channel side information at the receiver), on the capacity with outage"
  - paper: doi:10.1109/25.293655
    title: "L. H. Ozarow, S. Shamai and A. D. Wyner, Information theoretic considerations for cellular mobile radio, IEEE Transactions on Vehicular Technology 43(2), 1994, pages 359 to 378"
    locator: "the capacity versus outage of a fading channel against its average capacity"
---

The outage capacity $C_\epsilon$ of a slow fading channel is the largest rate $R$ for which the [outage probability](/outage-probability/) $\Pr[\log_2(1 + \gamma) < R]$ is at most $\epsilon$, in bits per channel use. The outage probability fixes the rate and asks how often it fails; the outage capacity fixes the failure probability and asks for the rate, so each is the inverse of the other. The [ergodic capacity](/ergodic-capacity/) is the measure for fast fading, where a codeword sees the average of many fades; in slow fading one codeword sees one fade, the ergodic capacity cannot be reached, and $C_\epsilon$ is usually much smaller.

## Definition

Take the slow fading channel $y_t = h x_t + w_t$, $t = 1, \ldots, T$, where the gain $h$ is random but fixed over the codeword, $w_t \sim CN(0, N_0)$ is i.i.d. noise, and $E|x_t|^2 \le P$. The receiver knows $h$ (CSIR) and the transmitter does not (no CSIT). Write $\bar\gamma = E|h|^2 P/N_0$ for the average SNR and $\gamma = |h|^2 P/N_0$ for the SNR of the fade that occurs. For a rate $R$, the outage probability is $p_{\mathrm{out}}(R) = \Pr[\log_2(1 + \gamma) < R]$, and for $0 < \epsilon < 1$ the **$\epsilon$-outage capacity** is

$$C_\epsilon = \sup\{R : p_{\mathrm{out}}(R) \le \epsilon\} = \log_2\big(1 + F^{-1}(\epsilon)\big) \quad \text{bits per channel use},$$

where $F$ is the distribution function of $\gamma$, assumed continuous and increasing, and $F^{-1}(\epsilon)$ is the SNR that the channel exceeds with probability $1 - \epsilon$.

The operational meaning is a theorem for long codewords: when $\log_2(1 + \gamma) > R$, a good code of rate $R$ has an error probability that tends to 0 as $T$ grows; when $\log_2(1 + \gamma) < R$, every code fails. So the error probability of the best codes tends to $p_{\mathrm{out}}(R)$, and $C_\epsilon$ is the largest rate with error probability at most $\epsilon$ (Tse and Viswanath, Section 5.4.1). In Rayleigh fading $F(x) > 0$ for every $x > 0$, so the capacity in the strict sense, with $\epsilon \to 0$, is 0, and a positive rate is possible only with a positive $\epsilon$.

## Examples and non-examples

**Rayleigh fading.** Here $F(x) = 1 - e^{-x/\bar\gamma}$, so the closed form (Rayleigh fading, CSIR, no CSIT) is

$$C_\epsilon = \log_2\big(1 - \bar\gamma \ln(1 - \epsilon)\big) \approx \log_2(1 + \epsilon\bar\gamma) \text{ for small } \epsilon .$$

At $\bar\gamma = 10$ dB, $C_{0.01} = 0.138$ bits and $C_{0.1} = 1.038$ bits, against an ergodic capacity of 2.907 bits and an AWGN capacity of 3.459 bits. At 20 dB the values are 1.004 and 3.528 bits, against 5.884 and 6.658. At high SNR, $C_\epsilon$ is $\log_2\bar\gamma - \log_2(1/(-\ln(1 - \epsilon)))$ plus a vanishing term: the loss against the AWGN channel tends to 6.64 bits for $\epsilon = 0.01$ and to 3.25 bits for $\epsilon = 0.1$, the same as a loss of 20 dB and 9.8 dB of power.

**The inverse of the outage probability.** At 10 dB and $R = 1$ bit, the outage probability in Rayleigh fading is $1 - e^{-1/10} = 0.0952$. So $C_{0.0952} = 1$ bit: the two quantities are one curve read in two directions.

**Diversity.** With $L$ independent Rayleigh branches at $\bar\gamma$ each, the lower tail of $\gamma$ is thinner, and $C_\epsilon$ grows much faster with $L$ than the mean SNR does. With [selection combining](/selection-combining/), $F^{-1}(\epsilon) = -\bar\gamma\ln(1 - \epsilon^{1/L})$. With [maximal ratio combining](/maximal-ratio-combining/), $\gamma$ has the gamma distribution with shape $L$, and $F^{-1}$ is computed numerically. At 10 dB per branch and $\epsilon = 0.01$:

| scheme | $C_{0.01}$, bits per channel use |
|---|---|
| one branch | 0.138 |
| selection combining, $L = 2$ | 1.038 |
| maximal ratio combining, $L = 2$ | 1.314 |
| selection combining, $L = 4$ | 2.263 |
| maximal ratio combining, $L = 4$ | 3.207 |

The [diversity order](/diversity-order/) sets the slope: for small $\epsilon$, $F^{-1}(\epsilon)$ grows like $\epsilon^{1/d}$ with diversity order $d$, so $L$ branches turn the factor $\epsilon$ of one branch into about $\epsilon^{1/L}$.

**Non-example: fast fading.** If a codeword spans many independent fades, the code sees the average of $\log_2(1 + \gamma)$, and every rate below the [ergodic capacity](/ergodic-capacity/) has an error probability that tends to 0. The outage capacity with a single fade per codeword is not the right measure there, and it underestimates what the channel can carry.

**Non-example: a rate set by the mean SNR.** Sending at $\log_2(1 + \bar\gamma)$ in slow Rayleigh fading fails whenever $|h|^2 < 1$, which happens with probability $1 - e^{-1} = 0.632$. The rate that is safe with probability $1 - \epsilon$ is set by the lower tail of $\gamma$, not by its mean.

**Non-example: a channel with CSIT.** If the transmitter knows $h$, it can choose the rate $\log_2(1 + \gamma)$ in each block, and no outage occurs at all. The outage capacity is a measure for a transmitter that must fix its rate without knowing the fade.

## Related definitions

- **[Outage probability](/outage-probability/).** $p_{\mathrm{out}}(R) = \Pr[\log_2(1 + \gamma) < R]$; the outage capacity is its inverse at level $\epsilon$.
- **[Ergodic capacity](/ergodic-capacity/).** $E[\log_2(1 + \gamma)]$, the measure for fast fading. For every $\epsilon$ below the probability that $\log_2(1 + \gamma)$ is under its mean, $C_\epsilon$ is below the ergodic capacity.
- **[Diversity order](/diversity-order/).** The slope of the outage probability at high SNR, which sets how fast $C_\epsilon$ grows as $\epsilon$ falls.
- **[Diversity-multiplexing tradeoff](/diversity-multiplexing-tradeoff/).** Lets the rate grow as $r\log_2\bar\gamma$ and studies the slope of the outage probability, a high-SNR view of the same tradeoff between rate and outage.
- **[Channel capacity](/channel-capacity/).** The capacity with error probability tending to 0, which is 0 for slow Rayleigh fading.

## References
