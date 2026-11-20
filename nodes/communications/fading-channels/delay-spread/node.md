---
tag: T38XE2
kind: definition
slug: delay-spread
name: Delay spread
aliases:
- rms delay spread
- multipath delay spread
area: communications/fading-channels
level: intro
summary: "The spread in arrival time of the paths of a channel: the RMS width of the power delay profile, sigma_tau = sqrt(sum P_l tau_l^2 - (sum P_l tau_l)^2) for tap powers P_l that sum to 1."
prereqs: [multipath-fading]
see_also: [coherence-bandwidth, tapped-delay-line-channel-model, wssus-channel-model, intersymbol-interference, cyclic-prefix, saleh-valenzuela-model, doppler-spread, rake-receiver]
sources:
  - book: isbn:9780130422323
    title: Theodore S. Rappaport, Wireless Communications, Principles and Practice, second edition, Prentice Hall, 2002
    locator: Section 5.4.1 (time dispersion parameters, the mean excess delay, the RMS delay spread and the maximum excess delay) and Section 5.5 (flat and frequency-selective fading)
  - book: isbn:9780521837163
    title: Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005
    locator: Section 3.3.1 (the power delay profile, its mean and RMS delay spread)
  - book: isbn:9780521845274
    title: David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005
    locator: Section 2.3 (the delay spread T_d as the largest difference of path delays, and its relation to the coherence bandwidth) and Table 2.1
  - url: https://www.etsi.org/deliver/etsi_ts/136100_136199/136104/09.11.00_60/ts_136104v091100p.pdf
    title: 3GPP TS 36.104, Base Station radio transmission and reception (E-UTRA), Release 9 (ETSI TS 136 104 V9.11.0)
    locator: Annex B.2 (multipath fading propagation conditions, the EPA, EVA and ETU delay profiles with RMS delay spreads of 43, 357 and 991 ns)
  - paper: "Bernard H. Fleury, An uncertainty relation for WSS processes and its application to WSSUS systems, IEEE Transactions on Communications 44(12), 1632 to 1634, 1996"
    locator: whole paper (the lower bound arccos(c)/(2 pi sigma_tau) on the coherence bandwidth at correlation level c)
---

The delay spread of a multipath channel measures how long the copies of one transmitted impulse keep arriving. The standard measure is the root mean square (RMS) delay spread $\sigma_\tau$, the standard deviation of the arrival time when each path is weighted by its power. It is the single number that decides whether a link sees [intersymbol interference](/intersymbol-interference/), how long a [cyclic prefix](/cyclic-prefix/) must be, and over what band the channel gain stays nearly constant: the [coherence bandwidth](/coherence-bandwidth/) is of the order of $1/\sigma_\tau$. The time-domain counterpart of this page in the Doppler domain is the [Doppler spread](/doppler-spread/).

## Definition

**The power delay profile.** Let the channel have $L$ paths, or taps of a [tapped delay line model](/tapped-delay-line-channel-model/), at the delays $\tau_0 \le \tau_1 \le \cdots \le \tau_{L-1}$ in seconds, with the mean powers $P_l = \mathbb{E}|h_l|^2 \ge 0$. The list of pairs $(\tau_l, P_l)$ is the **power delay profile** (PDP). It is a property of the statistics of the channel, not of one realization: in the [WSSUS model](/wssus-channel-model/) it is the mean power at each delay. Delays are measured from the first arrival, so $\tau_0 = 0$ unless the page says otherwise, and the powers are normalized so that $\sum_l P_l = 1$. For a profile that is not normalized, divide every sum below by $\sum_l P_l$.

**Mean delay and RMS delay spread.** With these weights,

$$\bar\tau = \sum_{l} P_l \tau_l, \qquad \sigma_\tau = \sqrt{\sum_l P_l (\tau_l - \bar\tau)^2} = \sqrt{\sum_l P_l \tau_l^2 - \bar\tau^2}.$$

$\bar\tau$ is the **mean excess delay** and $\sigma_\tau$ is the **RMS delay spread**. The two forms of $\sigma_\tau$ are equal because $\sum_l P_l(\tau_l - \bar\tau)^2 = \sum_l P_l \tau_l^2 - 2\bar\tau \sum_l P_l \tau_l + \bar\tau^2 \sum_l P_l$ and $\sum_l P_l = 1$. For a continuous profile $P(\tau) \ge 0$ with $\int P = 1$, replace the sums by integrals over $\tau$.

**Maximum excess delay.** For a threshold of $X$ dB, the maximum excess delay is $\tau_X - \tau_0$, where $\tau_X$ is the largest delay whose power is within $X$ dB of the strongest path (Rappaport, Section 5.4.1). It depends on $X$, and one weak late path can make it large while $\sigma_\tau$ hardly moves. Tse and Viswanath write $T_d$ for the largest difference of path delays, which is the maximum excess delay with no threshold.

**Properties.** For every normalized profile:

1. *Shift invariance.* Adding the same constant to every delay changes $\bar\tau$ by that constant and leaves $\sigma_\tau$ unchanged, because $\sigma_\tau$ uses only $\tau_l - \bar\tau$.
2. *Scaling.* Multiplying every delay by $a > 0$ multiplies $\bar\tau$ and $\sigma_\tau$ by $a$. The link-level models of 3GPP TR 38.901 use this: their delays are normalized to $\sigma_\tau = 1$ and scaled to the wanted spread.
3. *Range.* $0 \le \sigma_\tau \le (\tau_{L-1} - \tau_0)/2$. The lower bound holds with equality only when all the power sits at one delay. The upper bound holds because a variable in an interval of length $D$ has variance at most $D^2/4$, with equality for two equal taps at the ends.
4. *Link to frequency.* Let $R(\Delta f) = \sum_l P_l e^{-j 2\pi \Delta f \tau_l}$ be the normalized correlation of the channel gain at two frequencies $\Delta f$ apart. A Taylor expansion of $e^{-j 2\pi \Delta f (\tau_l - \bar\tau)}$ gives
   $$e^{j 2\pi \Delta f \bar\tau} R(\Delta f) = 1 - 2\pi^2 \sigma_\tau^2 \Delta f^2 + O(\Delta f^3),$$
   since the first-order term $\sum_l P_l (\tau_l - \bar\tau)$ is zero. So $\sigma_\tau$ sets how fast the gains at nearby frequencies decorrelate. Fleury (1996) proved the bound $|R(\Delta f)| \ge \cos(2\pi \sigma_\tau \Delta f)$ for $2\pi \sigma_\tau \Delta f \le \pi/2$; the proof and its use are on the [coherence bandwidth](/coherence-bandwidth/) page.

**Flat or selective.** A symbol of duration $T_s$ sees little intersymbol interference when $\sigma_\tau$ is small compared with $T_s$. Rappaport (Section 5.5) uses $T_s \ge 10\sigma_\tau$ as the condition for flat fading. That is a rule of thumb, not a theorem: the real effect depends on the shape of the profile, the pulse and the receiver.

### Computing the delay spread

The function below uses the centered form of $\sigma_\tau$. The form $\sum P_l \tau_l^2 - \bar\tau^2$ is equal in exact arithmetic but loses digits in floating point when all delays share a large offset, for example absolute delays of $3.3$ microseconds that differ by a few nanoseconds.

```pseudo id=main
RMS-DELAY-SPREAD(τ[0..L-1], P[0..L-1])      ▷ delays and mean powers, any positive scale
L1  S ← Σ_l P[l]
L2  μ ← (Σ_l P[l] · τ[l]) / S                ▷ mean excess delay
L3  v ← (Σ_l P[l] · (τ[l] - μ)²) / S         ▷ centered second moment
L4  return μ, √v

MAX-EXCESS-DELAY(τ[0..L-1], P[0..L-1], X)    ▷ X is the threshold in dB
L5  t ← max_l P[l] · 10^(-X/10)
L6  return max{τ[l] : P[l] ≥ t} - min_l τ[l]
```

The cost is $O(L)$ operations in the [real-RAM](/real-ram/) model. The implementation also gives the frequency correlation $|R(\Delta f)|$. Its tests check the examples on this page in exact rational arithmetic, the 3GPP values below, the shift and scale properties, and Fleury's bound on random profiles.

## Examples and non-examples

**Two equal paths.** Taps of power $1/2$ at $0$ and $1$ microsecond give $\bar\tau = 0.5$ microseconds and $\sigma_\tau = \sqrt{0.5 - 0.25} = 0.5$ microseconds, the largest value that a span of 1 microsecond allows.

**Four paths.** Powers $(1/2, 1/4, 1/8, 1/8)$, that is $0$, $-3.01$, $-6.02$ and $-6.02$ dB, at delays $(0, 1, 2, 4)$ microseconds:

$$\bar\tau = \tfrac14 + \tfrac14 + \tfrac12 = 1, \qquad \sum_l P_l \tau_l^2 = \tfrac14 + \tfrac12 + 2 = 2.75, \qquad \sigma_\tau = \sqrt{2.75 - 1} = \sqrt{1.75} = 1.3229 \text{ microseconds}.$$

The maximum excess delay is $4$ microseconds for $X = 10$ dB, since every tap is within $6.02$ dB of the strongest, and $1$ microsecond for $X = 5$ dB.

**An exponential profile.** $P(\tau) = e^{-\tau/\tau_0}/\tau_0$ for $\tau \ge 0$ has $\bar\tau = \int_0^\infty \tau P(\tau)\, d\tau = \tau_0$ and the second moment $\int_0^\infty \tau^2 P(\tau)\, d\tau = 2\tau_0^2$, so $\sigma_\tau = \sqrt{2\tau_0^2 - \tau_0^2} = \tau_0$. This shape is common in indoor models, for example inside each cluster of the [Saleh-Valenzuela model](/saleh-valenzuela-model/).

**Standard profiles.** The LTE test profiles of 3GPP TS 36.104, Annex B.2, are tapped delay lines. EPA has taps at $0, 30, 70, 90, 110, 190, 410$ ns with powers $0, -1, -2, -3, -8, -17.2, -20.8$ dB. Converting the powers to linear values, normalizing them and applying the definition gives $\bar\tau = 44.2$ ns and $\sigma_\tau = 43.1$ ns. The same steps give $356.6$ ns for EVA and $990.9$ ns for ETU. The standard lists $43$, $357$ and $991$ ns.

**Symbol length.** With $\sigma_\tau = 991$ ns, a single-carrier link at $1$ Msymbol/s ($T_s = 1$ microsecond) has $T_s \approx \sigma_\tau$ and needs an [equalizer](/channel-equalization/). LTE instead uses [OFDM](/orthogonal-frequency-division-multiplexing/) with a symbol of about $66.7$ microseconds and a normal cyclic prefix of about $4.7$ microseconds. The prefix is almost five times $\sigma_\tau$ but a little shorter than the last ETU delay of $5$ microseconds; that tap is $7$ dB below the strongest and leaks a small amount of interference.

**Non-example: power from one realization.** The squared magnitudes $|h_l|^2$ of one draw of the taps are not the PDP. The RMS width of one draw is a random variable, and its mean is not $\sigma_\tau$ in general. The PDP needs an average over many realizations, or over a local area in measurements.

**Non-example: averaging in dB.** The weights must be linear powers. Weighting the EPA delays by the dB values, or by the amplitudes $\sqrt{P_l}$, gives a different number that has no meaning as a delay spread.

**Non-example: the largest delay.** For ETU the largest delay is $5$ microseconds and $\sigma_\tau$ is $0.991$ microseconds. The maximum excess delay and the RMS delay spread answer different questions: the first sizes a cyclic prefix that must catch every path, the second sets the coherence bandwidth.

## Related definitions

- [Coherence bandwidth](/coherence-bandwidth/): the frequency separation over which the gains stay correlated, bounded below in terms of $\sigma_\tau$.
- [Tapped delay line channel model](/tapped-delay-line-channel-model/): the model whose tap delays and powers form the PDP.
- [WSSUS channel model](/wssus-channel-model/): the statistical frame in which the PDP is the mean power per delay, and the transform of the frequency correlation.
- [Doppler spread](/doppler-spread/): the same kind of width, taken over the Doppler spectrum instead of the delays.
- [Intersymbol interference](/intersymbol-interference/) and [cyclic prefix](/cyclic-prefix/): the effects of a delay spread on a single-carrier and on a multicarrier link.
- [Rake receiver](/rake-receiver/): a receiver that resolves the paths and combines them, which turns the delay spread into diversity.

## References
