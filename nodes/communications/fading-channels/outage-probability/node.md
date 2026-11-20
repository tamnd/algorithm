---
tag: KSR0RH
kind: definition
slug: outage-probability
name: Outage probability
aliases:
- probability of outage
area: communications/fading-channels
level: core
summary: "The probability that the random SNR of a fading channel falls below a threshold, P(gamma < gamma_th); for a slow fading channel at rate R, the threshold is 2^R - 1."
prereqs: [rayleigh-fading-channel, channel-capacity]
see_also: [outage-capacity, ergodic-capacity, diversity-order, rayleigh-fading-channel, log-normal-shadowing, maximal-ratio-combining, level-crossing-rate, diversity-multiplexing-tradeoff]
sources:
  - paper: doi:10.1109/25.293655
    title: L. H. Ozarow, S. Shamai and A. D. Wyner, Information theoretic considerations for cellular mobile radio, IEEE Transactions on Vehicular Technology 43(2), 1994
    locator: pp. 359 to 378 (the capacity versus outage of a channel whose fading stays fixed over a codeword)
  - book: isbn:9780521845274
    title: David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005
    locator: Section 5.4.1 (the slow fading channel, the outage probability and the outage capacity) and Section 5.4.2 (receive diversity)
  - book: isbn:9780521837163
    title: Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005
    locator: Section 2.9 (outage probability under path loss and shadowing), Section 4.2.3 (channel side information at the receiver, outage capacity) and Section 6.3.1 (outage probability)
---

The outage probability of a fading link is the probability that the received SNR is too low for the link to work: $P_{\mathrm{out}} = \Pr[\gamma < \gamma_{\mathrm{th}}]$. For a slow fading channel used at a fixed rate $R$, the threshold comes from the capacity formula, and the outage is the event $\log_2(1 + \gamma) < R$. It is the right measure of performance when one codeword sees only one value of the fading, so that averaging over the fades is not possible. The same word is used for the probability that shadowing pushes the local mean power below the sensitivity of a receiver.

## Definition

Let $\gamma \ge 0$ be the random SNR of a link, with cumulative distribution function $F_\gamma$, and let $\gamma_{\mathrm{th}} > 0$ be the smallest SNR at which the receiver meets its target, for example a [bit error rate](/bit-error-rate/) of $10^{-3}$. The **outage probability** is

$$P_{\mathrm{out}} = \Pr[\gamma < \gamma_{\mathrm{th}}] = F_\gamma(\gamma_{\mathrm{th}}).$$

**The capacity form.** Take a slow (block) fading channel $y = h x + w$ with $w \sim \mathcal{CN}(0, N_0)$, in which $h$ stays fixed over a whole codeword, with CSIR and no CSIT, and $\gamma = |h|^2 E_s / N_0$. For a code of rate $R$ bit per channel use,

$$P_{\mathrm{out}}(R) = \Pr[\log_2(1 + \gamma) < R] = F_\gamma(2^R - 1).$$

So the capacity form is the general form with $\gamma_{\mathrm{th}} = 2^R - 1$. The reason for it: given $h$, the channel is an [AWGN channel](/additive-white-gaussian-noise-channel/) with capacity $\log_2(1 + \gamma)$, and no code of rate above that capacity works. For codewords long enough inside one fade, the error probability of good codes tends to $P_{\mathrm{out}}(R)$ (Ozarow, Shamai and Wyner 1994; Tse and Viswanath, Section 5.4.1).

**The outage capacity.** For a target $\epsilon$, the $\epsilon$-outage capacity is the largest rate with $P_{\mathrm{out}}(R) \le \epsilon$: $C_\epsilon = \log_2(1 + F_\gamma^{-1}(\epsilon))$. See [outage capacity](/outage-capacity/).

**The shadowing form.** With [log-normal shadowing](/log-normal-shadowing/) of $\sigma$ dB around a mean received power $\overline{P}_r$ in dBm, a receiver that needs $P_{\min}$ dBm is in outage with probability $Q((\overline{P}_r - P_{\min})/\sigma)$ (Goldsmith, Section 2.9). This is the general form applied to the local mean power instead of the instantaneous SNR.

## Examples and non-examples

**Rayleigh fading.** Here $\gamma$ is exponential with mean $\bar\gamma$, so

$$P_{\mathrm{out}}(R) = 1 - e^{-(2^R - 1)/\bar\gamma} \approx \frac{2^R - 1}{\bar\gamma} \quad \text{for large } \bar\gamma .$$

At $\bar\gamma = 10$ dB: 0.0406 for $R = 0.5$, 0.0952 for $R = 1$, 0.259 for $R = 2$ and 0.503 for $R = 3$. At $R = 1$, raising $\bar\gamma$ to 20 dB gives 0.00995, and to 30 dB gives $1.00 \cdot 10^{-3}$: each 10 dB buys only a factor of 10.

**Other channels at $R = 1$ and $\bar\gamma = 10$ dB** (so $\gamma_{\mathrm{th}} = 1$, and every branch has mean SNR $\bar\gamma$):

| channel | $P_{\mathrm{out}}$ |
|---|---|
| [Rayleigh](/rayleigh-fading-channel/) | 0.0952 |
| [Nakagami](/nakagami-m-fading-channel/), $m = 2$ | 0.0175 |
| [selection combining](/selection-combining/) of 2 Rayleigh branches, $(1 - e^{-1/\bar\gamma})^2$ | $9.06 \cdot 10^{-3}$ |
| [maximal ratio combining](/maximal-ratio-combining/) of 2 Rayleigh branches, $1 - e^{-1/\bar\gamma}(1 + 1/\bar\gamma)$ | $4.68 \cdot 10^{-3}$ |
| [Rician](/rician-fading-channel/), $K = 10$ | $7.39 \cdot 10^{-4}$ |

**Outage capacity in Rayleigh fading.** $F_\gamma^{-1}(\epsilon) = -\bar\gamma \ln(1 - \epsilon)$, so $C_\epsilon = \log_2(1 - \bar\gamma \ln(1 - \epsilon))$. At 10 dB this is 0.138 bit for $\epsilon = 0.01$ and 1.04 bit for $\epsilon = 0.1$. The AWGN channel at the same SNR carries 3.46 bit, and the ergodic capacity of fast Rayleigh fading is 2.91 bit.

**Shadowing.** With $\sigma = 8$ dB and the mean 10 dB above the sensitivity, $P_{\mathrm{out}} = Q(1.25) = 0.106$.

**Non-example: fast fading with long codes.** If a codeword spans many independent fades, the code sees the average, and every rate below the [ergodic capacity](/ergodic-capacity/) $\mathbb{E}[\log_2(1 + \gamma)]$ works with error probability tending to 0. The outage probability of one symbol is then not the error probability of the code.

**Non-example: the average error rate.** The average bit error rate $\mathbb{E}[P_b(\gamma)]$ counts errors at all SNR values, weighted by the probability. The outage probability only counts how often $\gamma$ is below one threshold. The two have the same slope at high SNR but different values.

**Non-example: a channel known at the transmitter.** With CSIT, the transmitter can change its power or rate with $h$. Then "outage" means whatever event the scheme declares, for example the fades in which [truncated channel inversion](/truncated-channel-inversion/) stops sending, and the formula above does not apply.

## Related definitions

- **[Diversity order](/diversity-order/).** $d = -\lim_{\bar\gamma \to \infty} \log P_{\mathrm{out}} / \log \bar\gamma$. It is 1 for Rayleigh, $L$ for $L$ independent Rayleigh branches with selection or maximal ratio combining, and $m$ for Nakagami fading.
- **[Outage capacity](/outage-capacity/).** The rate $C_\epsilon$ at which the outage probability is $\epsilon$.
- **[Ergodic capacity](/ergodic-capacity/).** The average of $\log_2(1 + \gamma)$, the measure for fast fading.
- **[Level crossing rate](/level-crossing-rate/) and average fade duration.** How often $\gamma$ falls below $\gamma_{\mathrm{th}}$ per second, and how long it stays below. The product of the two is the outage probability.
- **[Diversity-multiplexing tradeoff](/diversity-multiplexing-tradeoff/).** How fast $P_{\mathrm{out}}$ falls when the rate grows with $\log \bar\gamma$.
- **Cell coverage.** The fraction of a cell area where the shadowing outage is below a target; see [log-normal shadowing](/log-normal-shadowing/).

## References
