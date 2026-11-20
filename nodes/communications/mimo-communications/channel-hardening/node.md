---
tag: 9Y4Y69
kind: concept
slug: channel-hardening
name: Channel hardening
aliases:
- MIMO channel hardening
area: communications/mimo-communications
level: advanced
summary: With many antennas the gain of the beamformed channel concentrates near its mean, so it behaves like a fixed channel.
prereqs: [massive-mimo, law-of-large-numbers]
see_also: [favorable-propagation, pilot-contamination, cell-free-massive-mimo, rayleigh-fading-channel, diversity-order, maximum-ratio-transmission, chebyshev-inequality, concentration-of-measure]
sources:
  - paper: doi:10.1109/TIT.2004.833345
    title: "Bertrand M. Hochwald, Thomas L. Marzetta and Vahid Tarokh, Multiple-antenna channel hardening and its implications for rate feedback and scheduling, IEEE Transactions on Information Theory 50(9), 1893-1909, 2004"
    locator: "the concentration of the mutual information of a multiple-antenna channel as the number of antennas grows, and its use for rate feedback and scheduling"
  - book: isbn:9781107175570
    title: "Thomas L. Marzetta, Erik G. Larsson, Hong Yang and Hien Quoc Ngo, Fundamentals of Massive MIMO, Cambridge University Press, 2016"
    locator: the discussion of channel hardening and the downlink capacity bound that uses only the mean of the effective gain
---

Channel hardening is the effect that, in a system with many antennas, the gain of a channel after beamforming or combining stays close to its mean, so that a fading channel behaves almost like a fixed one. With $M$ antennas and i.i.d. Rayleigh fading, the power gain $\|h\|^2$ has mean $M$ and standard deviation $\sqrt{M}$, so the ratio $\|h\|^2/M$ tends to 1 by the [law of large numbers](/law-of-large-numbers/). It is one of the two effects that make [massive MIMO](/massive-mimo/) work; the other, [favorable propagation](/favorable-propagation/), is about the inner products between the channels of different users, where hardening is about the norm of one channel. Hardening lets a user decode the downlink without its own pilots, and it holds also in [cell-free massive MIMO](/cell-free-massive-mimo/), though often less strongly.

## In plain words

A phone with one antenna sees its signal rise and fall as it moves, sometimes by a factor of a hundred, because the radio waves add up well at one place and cancel at another. This is fading.

A base station with a hundred antennas sees a hundred such signals from the phone. Some are weak, some are strong, and when the base station adds them up in the right way, the weak and strong ones balance. The total stays almost the same from moment to moment. The channel has become hard: it no longer fades. So the phone can use a fixed estimate of its channel strength, and the base station can choose the data rate without fresh reports.

## The idea

**The definition.** A sequence of channel vectors $h \in \mathbb{C}^M$ hardens if

$$\frac{\|h\|^2}{\mathbb{E}\|h\|^2} \to 1 \quad \text{in probability as } M \to \infty,$$

or, as a sufficient condition that is easy to check, if $\mathrm{Var}(\|h\|^2)/(\mathbb{E}\|h\|^2)^2 \to 0$. By [Chebyshev's inequality](/chebyshev-inequality/), $P(|\|h\|^2/\mathbb{E}\|h\|^2 - 1| > \delta) \le \mathrm{Var}(\|h\|^2)/(\delta^2 (\mathbb{E}\|h\|^2)^2)$.

**I.i.d. Rayleigh fading (a closed form).** With i.i.d. $\mathcal{CN}(0, 1)$ entries, $\|h\|^2$ is a sum of $M$ independent exponential variables of mean 1, a Gamma variable with shape $M$. So $\mathbb{E}\|h\|^2 = M$, $\mathrm{Var}(\|h\|^2) = M$, and $\mathrm{Var}(\|h\|^2/M) = 1/M$. The channel hardens, with fluctuations of relative size $1/\sqrt{M}$.

**Correlated fading (a closed form).** If $h \sim \mathcal{CN}(0, R)$, then $\mathbb{E}\|h\|^2 = \mathrm{tr}(R)$ and $\mathrm{Var}(\|h\|^2) = \mathrm{tr}(R^2)$. The channel hardens if $\mathrm{tr}(R^2)/\mathrm{tr}(R)^2 \to 0$, that is, if the energy of $R$ spreads over many eigenvalues. If $R$ has rank one, the ratio is 1 for every $M$, and the array fades like a single antenna.

**Link with diversity.** Hardening is the large-$M$ form of [diversity](/diversity-order/): the outage probability $P(\|h\|^2 < \epsilon M)$ is the Gamma distribution function at $\epsilon M$, which falls like $\epsilon^M$ for small $\epsilon$. Diversity describes the slope of the error curve at high SNR for fixed $M$; hardening describes the concentration at a fixed SNR as $M$ grows.

**Why it matters.** With [maximum ratio transmission](/maximum-ratio-transmission/) along $g_k$, user $k$ receives its symbol with the effective gain $\|g_k\|^2$, up to a fixed power factor, and this gain is random. If the channel hardens, the user can treat the mean of this gain as the true gain, and the error from doing so acts as a small extra noise. A standard capacity bound for massive MIMO uses exactly this: it gives a rate that needs only the mean gain at the user, so no downlink pilots are needed.

## Examples

**The distribution of $\|h\|^2/M$ in i.i.d. Rayleigh fading (closed form, from the Gamma distribution).**

| $M$ | $P(\|h\|^2/M < 0.8)$ | $P(\|h\|^2/M < 0.5)$ | standard deviation |
|---|---|---|---|
| 1 | 0.55067 | 0.39347 | 1 |
| 2 | 0.47507 | 0.26424 | 0.70711 |
| 4 | 0.39748 | 0.14288 | 0.5 |
| 10 | 0.28338 | 0.031828 | 0.31623 |
| 100 | 0.017108 | 3.2001e-10 | 0.1 |

With one antenna, the gain is below half its mean 39 percent of the time. With 100 antennas, this almost never happens, and the gain is above 80 percent of its mean more than 98 percent of the time.

**Line of sight.** If every antenna sees one plane wave with the same amplitude, $|h_m| = 1$ for all $m$, and $\|h\|^2 = M$ exactly. This channel is perfectly hard, though it may still have poor [favorable propagation](/favorable-propagation/) for users in nearby directions.

**A keyhole.** If all paths pass through one narrow point, $h = a\, z$ with a fixed vector $a$ and one Rayleigh scalar $z$. Then $\|h\|^2 = \|a\|^2 |z|^2$ fades as a single Rayleigh channel, with no hardening for any $M$.

## Where it is used

- **Downlink of massive MIMO.** Users decode with the mean gain, so the base station sends no downlink pilots in the simplest designs.
- **Rate adaptation and scheduling.** Hochwald, Marzetta and Tarokh showed that the mutual information of a multiple-antenna link concentrates as the number of antennas grows, so the transmitter can pick a rate with little feedback, and the gain from serving users at the peaks of their fading becomes small.
- **Analysis.** Deterministic approximations of the SINR, as in [massive MIMO](/massive-mimo/), rely on hardening to replace random gains by their means.
- **Cell-free systems.** In [cell-free massive MIMO](/cell-free-massive-mimo/), each user is served mostly by a few nearby access points, so the effective number of antennas is small and hardening is weaker (a heuristic). Designs there often keep downlink pilots.

## References
