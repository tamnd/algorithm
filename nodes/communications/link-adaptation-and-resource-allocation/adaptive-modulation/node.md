---
tag: RESKEP
kind: technique
slug: adaptive-modulation
name: Variable-rate variable-power modulation
aliases:
- Goldsmith-Chua adaptive modulation
area: communications/link-adaptation-and-resource-allocation
level: core
summary: "The adaptive MQAM of Goldsmith and Chua (1997): change the constellation size and the power with the fading SNR to keep a target bit error rate and maximize the average spectral efficiency."
prereqs: [quadrature-amplitude-modulation, rayleigh-fading-channel, snr-gap-approximation]
see_also: [link-adaptation, water-filling-power-allocation, truncated-channel-inversion, bit-error-rate, spectral-efficiency, outer-loop-link-adaptation, effective-snr-mapping, hybrid-arq]
sources:
  - paper: doi:10.1109/26.634685
    title: "Andrea J. Goldsmith and Soon-Ghee Chua, Variable-rate variable-power MQAM for fading channels, IEEE Transactions on Communications 45(10), 1997, pages 1218 to 1230"
    locator: "the BER fit for MQAM, the continuous-rate and discrete-rate policies with power adaptation, and their spectral efficiency on Rayleigh fading"
  - paper: doi:10.1109/18.641562
    title: "Andrea J. Goldsmith and Pravin P. Varaiya, Capacity of fading channels with channel side information, IEEE Transactions on Information Theory 43(6), 1997, pages 1986 to 1992"
    locator: "the capacity with side information at both ends, the bound that adaptive modulation is compared with"
  - book: isbn:9780521837163
    title: "Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005"
    locator: "Chapter 9 (adaptive modulation and coding: variable-rate variable-power MQAM, constant-power and discrete-rate forms)"
---

Variable-rate variable-power modulation is the adaptive modulation of Goldsmith and Chua (1997): on a flat fading channel whose SNR $\gamma$ the transmitter learns by feedback, it changes both the size $M(\gamma)$ of a QAM constellation and the transmit power $P(\gamma)$, so that the bit error rate stays at a target in every state while the average number of bits per symbol is as large as an average power limit allows. The key tool is a fit for the bit error rate of $M$-QAM, $\mathrm{BER} \approx 0.2\, e^{-1.5\gamma P(\gamma)/(\bar P (M - 1))}$, which turns the target into the rule $M(\gamma) = 1 + K\gamma P(\gamma)/\bar P$ with $K = -1.5/\ln(5\,\mathrm{BER})$. Maximizing the average of $\log_2 M$ then gives [water-filling](/water-filling-power-allocation/) over time with the [SNR gap](/snr-gap-approximation/) $1/K$. This page is about that policy and its constant-power and discrete-rate forms. [Link adaptation](/link-adaptation/) is the wider engineering problem of choosing a modulation and coding scheme from feedback, with coded block error targets, retransmissions and an outer loop; Goldsmith-Chua modulation is one answer to it, for uncoded QAM and a bit error target.

## In plain words

A radio link gets better and worse as the user moves. A fixed modulation must be chosen for the bad moments, so it wastes the good ones.

Adaptive modulation lets the receiver tell the sender how good the channel is now. When it is good, the sender packs more bits into each symbol; when it is poor, fewer; when it is very poor, none. The sender can also turn its power up or down. Both are chosen so that errors stay at the same low rate all the time, and so that the average number of bits sent is as high as the power budget allows.

## When it applies

- The channel changes slowly compared with the time it takes to measure the SNR and send it back, so the transmitter's knowledge is current. Goldsmith and Chua assume perfect and instantaneous knowledge; delay and estimation error reduce the gain.
- The service can take a variable rate, with buffering, as data traffic can.
- The error target is a bit error rate per symbol, which suits uncoded or lightly coded QAM. For strong codes and block error targets, use the methods of [link adaptation](/link-adaptation/).
- The SNR range is wide, as in Rayleigh fading, so a fixed scheme would waste much of it.

## The template

1. **Fix the target and the fit.** For $M$-QAM with $M \ge 4$ and a target bit error rate of at most $10^{-3}$, use the fit $\mathrm{BER}(\gamma, M) \approx 0.2\, e^{-1.5\gamma/(M-1)}$, where $\gamma$ is the received SNR. It is a curve fit, not a theorem. Solving for $M$ at the target gives $M = 1 + K\gamma$, with
   $$K = \frac{-1.5}{\ln(5\,\mathrm{BER})}, \qquad \frac{1}{K} = 5.48\text{ dB at } 10^{-3},\ 9.10\text{ dB at } 10^{-6}.$$
   So $1/K$ is an SNR gap.
2. **Write the rate and the power limit.** With power $P(\gamma)$ in state $\gamma$, the received SNR is $\gamma P(\gamma)/\bar P$, and the rate is $\log_2(1 + K\gamma P(\gamma)/\bar P)$ bits per symbol. The constraint is $\mathbb{E}[P(\gamma)] \le \bar P$.
3. **Continuous rate: water-fill.** Maximizing $\mathbb{E}[\log_2(1 + K\gamma P(\gamma)/\bar P)]$ gives
   $$\frac{P(\gamma)}{\bar P} = \begin{cases} \dfrac{1}{K}\left(\dfrac{1}{\gamma_K} - \dfrac{1}{\gamma}\right), & \gamma \ge \gamma_K, \\ 0, & \gamma < \gamma_K, \end{cases} \qquad \int_{\gamma_K}^{\infty}\left(\frac{1}{\gamma_K} - \frac{1}{\gamma}\right) p(\gamma)\, d\gamma = K,$$
   and the average rate $\int_{\gamma_K}^\infty \log_2(\gamma/\gamma_K)\, p(\gamma)\, d\gamma$. This is the capacity formula of Goldsmith and Varaiya with the power scaled by $K$.
4. **Discrete rate: choose regions.** Real systems use a few sizes $M_0 = 1$ (no transmission) $< M_1 < \cdots < M_J$. Split the SNR axis at thresholds $\gamma_1 < \cdots < \gamma_J$, and use $M_j$ for $\gamma_j \le \gamma < \gamma_{j+1}$. With constant power, the target holds at the edge of each region when $\gamma_j = (M_j - 1)/K$. With variable power, set $P(\gamma)/\bar P = (M_j - 1)/(K\gamma)$ inside region $j$, which meets the target exactly, and choose the thresholds to maximize $\sum_j \log_2 M_j \Pr(\text{region } j)$ under the power limit. Setting the derivative of the Lagrangian to zero gives $\gamma_j = \lambda (M_j - M_{j-1})/(K \log_2(M_j/M_{j-1}))$ for one constant $\lambda$ that the power limit fixes.
5. **Close the loop.** The receiver estimates $\gamma$, quantizes it to a region index, and sends the index back; the transmitter applies the size and power for that region.

**Why it works.** In each state the policy meets the error target by construction of $K$, so the average error rate is at the target too (more precisely, the ratio of the expected number of bit errors to the expected number of bits is at most the target). The rate problem is then a concave maximization over $P(\cdot)$ with one linear constraint, whose solution is water-filling.

## Classic examples

**How good the fit is.** For square $M$-QAM with Gray labels, the nearest-neighbor approximation $\frac{4}{\log_2 M}(1 - 1/\sqrt M)\, Q(\sqrt{3\gamma/(M-1)})$ reaches $10^{-3}$ at 9.80, 16.54, 22.55 and 28.41 dB for $M = 4, 16, 64, 256$. The fit says 10.25, 17.24, 23.47 and 29.55 dB. So the fit is cautious by 0.45 to 1.13 dB in this range.

**Rayleigh fading at 20 dB, target $10^{-3}$.** With $\bar\gamma = 100$ and $K = 0.2831$ (computed values):

| policy | average bits per symbol |
|---|---|
| capacity with side information at both ends | 5.90 |
| continuous rate, variable power (cutoff $\gamma_K$ = 4.92 dB) | 4.22 |
| continuous rate, constant power, $\mathbb{E}\log_2(1 + K\gamma)$ | 4.19 |
| discrete rate $M \in \{4, 16, 64, 256\}$, constant power | 3.19 |

The gap $1/K$ of 5.48 dB costs about 1.7 bits against capacity. Adapting the power adds only 0.03 bits over constant power: in this case almost all the gain comes from adapting the rate. The discrete set loses another bit, because each size is used from its threshold $(M_j - 1)/K$ up to the next one, which is 6 to 7 dB higher. The constant-power thresholds are 10.25, 17.24, 23.47 and 29.55 dB, and the rate is $2\sum_j e^{-\gamma_j/\bar\gamma}$, since each step adds 2 bits.

**Comparison with a fixed constellation.** Fixed 16-QAM at constant power on Rayleigh fading at 20 dB has an average bit error rate of about $1.7 \times 10^{-2}$ (computed with the nearest-neighbor formula above), because the deep fades dominate the average. To reach $10^{-3}$ on average, it needs a mean SNR of about 32.7 dB, almost 13 dB more, since the average error rate falls only as $1/\bar\gamma$. Adaptation removes this loss by not sending in the deep fades.

**Channel inversion.** [Truncated channel inversion](/truncated-channel-inversion/) is the opposite choice: a fixed rate, with the power varied to hold the received SNR constant. With a fixed QAM size it becomes a special case with one region.

## Variations

- **Rate only.** Constant power with a variable size is simpler for the amplifier and, as the example shows, loses little.
- **Coded modulation.** Replace the fit by the measured thresholds of each modulation and coding pair; the gap $1/K$ becomes a gap per scheme. This is the step from adaptive modulation to [link adaptation](/link-adaptation/).
- **Adaptive coset codes.** A trellis or lattice coset code on top of the adaptive constellation adds its coding gain to $K$, and the same policy applies with the larger $K$.
- **Imperfect feedback.** With delay or estimation error, the thresholds are raised by a margin, or chosen for the average error rate given the outdated estimate.
- **Multicarrier.** Applied per subcarrier, the policy becomes [bit loading](/bit-loading/), where the averaging is over frequency instead of time.
- **Average bit error rate target.** Instead of meeting the target in every state, meet it on average; this allows more bits in good states and gives a higher rate.

## Pitfalls

- **Using the fit out of range.** For BPSK, for $M = 2$, or for error rates above about $10^{-3}$, the fit is loose. Use the exact error rate there.
- **Instantaneous versus average error rate.** A target met in every state is met on average; the reverse is not true. Say which one a design uses.
- **Stale feedback.** Adaptation needs the SNR at the time of transmission. At high Doppler the estimate is old, and the error rate can be far above the target.
- **Thresholds in the wrong units.** $\gamma$ is the SNR at the average power. With power adaptation, the received SNR differs from it, and the thresholds refer to $\gamma$.
- **Confusing it with link adaptation.** Results for uncoded QAM with a bit error target do not carry over to coded systems with block error targets, where the curves are much steeper.

## Exercises

1. Show that for the continuous-rate policy the rate in state $\gamma \ge \gamma_K$ is $\log_2(\gamma/\gamma_K)$.
   *Answer.* $1 + K\gamma P(\gamma)/\bar P = 1 + \gamma(1/\gamma_K - 1/\gamma) = \gamma/\gamma_K$.
2. Compute $K$ and $1/K$ in dB for a target of $10^{-6}$.
   *Answer.* $K = -1.5/\ln(5 \times 10^{-6}) = 0.1229$, and $1/K = 9.10$ dB.
3. With constant power and target $10^{-3}$, at what SNR does the policy switch from 4-QAM to 16-QAM?
   *Answer.* $\gamma_2 = 15/K = 52.98$, or 17.24 dB.
4. Why is the rate of the constant-power discrete policy on Rayleigh fading $2\sum_j e^{-\gamma_j/\bar\gamma}$ for the sizes $4, 16, 64, 256$?
   *Answer.* The rate is $\sum_j \log_2 M_j \Pr(\gamma_j \le \gamma < \gamma_{j+1})$, and since $\log_2 M_j - \log_2 M_{j-1} = 2$, summing by parts gives $\sum_j 2\Pr(\gamma \ge \gamma_j)$, with $\Pr(\gamma \ge x) = e^{-x/\bar\gamma}$.
5. Explain why the continuous-rate policy sends nothing when $\gamma < \gamma_K$.
   *Answer.* The first small amount of power in state $\gamma$ buys bits at the rate $K\gamma/(\bar P \ln 2)$ per unit of power. The Lagrange condition gives power only to states where this rate is above the multiplier, which is the condition $\gamma > \gamma_K$.

## References
