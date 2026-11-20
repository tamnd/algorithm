---
tag: KXZGGT
kind: concept
slug: multiuser-diversity
name: Multiuser diversity
aliases:
- opportunistic scheduling gain
area: communications/link-adaptation-and-resource-allocation
level: core
summary: "With independent fading and a scheduler that knows the channels, serving the strongest user in each slot raises total throughput as users are added, like log log K for i.i.d. Rayleigh."
prereqs: [rayleigh-fading-channel, ergodic-capacity]
see_also: [max-rate-scheduling, proportional-fair-scheduling, wireless-link-scheduling, ofdma-resource-allocation, selection-combining, rayleigh-fading-channel, coherence-time, diversity-order]
sources:
  - paper: doi:10.1109/ICC.1995.525188
    title: "Raymond Knopp and Pierre A. Humblet, Information capacity and power control in single-cell multiuser communications, Proceedings of the IEEE International Conference on Communications (ICC), 1995, pages 331 to 335"
    locator: "the result that the sum capacity of the fading uplink with power control is reached by letting only the user with the best channel send at each time"
  - paper: doi:10.1109/TIT.2002.1003822
    title: "Pramod Viswanath, David N. C. Tse and Rajiv Laroia, Opportunistic beamforming using dumb antennas, IEEE Transactions on Information Theory 48(6), 2002, pages 1277 to 1294"
    locator: "the proportional fair scheduler, and the use of random beam weights to create channel fluctuations when the physical channel is slow or line of sight"
  - book: isbn:9780521845274
    title: "David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005"
    locator: "Chapter 6, the sections on multiuser diversity and its system aspects"
---

Multiuser diversity is the gain in total throughput that a shared fading channel gets from many users, when a scheduler sends to (or receives from) the user whose channel is strongest at each moment. It needs two things. The users' channels must fade independently, so that at most times some user is near a peak. The scheduler must know the current channels, usually from short feedback reports. With $K$ users whose gains are independent [Rayleigh](/rayleigh-fading-channel/) with the same mean, the gain of the best user has mean $H_K = 1 + 1/2 + \cdots + 1/K \approx \ln K$, so the received SNR grows like $\ln K$ and the throughput like $\log_2 \log K$. The gain is slow but free: it costs no extra power or bandwidth. Knopp and Humblet (1995) showed that, for the fading uplink with power control, letting only the best user send at each time reaches the sum capacity. The scheduler that does this is [max-rate scheduling](/max-rate-scheduling/).

## In plain words

When many people share one radio channel, each person's signal gets stronger and weaker over time, and these changes are different for each person. At any moment, at least one of them probably has a very good signal. If the base station always serves the person with the best signal at that moment, it sends more data in total than if it served people in a fixed turn. The more people there are, the better the best one usually is, so the total grows with the number of people, but slowly. This only works if the signals change, if they change in different ways for different people, and if the station knows which one is best right now.

## The idea

**Model.** One base station and $K$ users share a channel in time slots. In slot $t$, user $k$ has the SNR $\bar\gamma\, |h_k(t)|^2$, where $\bar\gamma$ is the mean SNR and $|h_k(t)|^2$ the fading power gain. The station serves one user per slot, at the rate $\log_2(1 + \bar\gamma |h_k(t)|^2)$ that the current channel supports.

**The gain.** A scheduler that ignores the channels, such as [round robin](/round-robin/), gets the average rate of one user, $\mathbb E[\log_2(1 + \bar\gamma |h|^2)]$, whatever $K$ is. A scheduler that serves the best user gets

$$C_K = \mathbb E\Big[\log_2\big(1 + \bar\gamma \max_{k} |h_k|^2\big)\Big].$$

If the gains are i.i.d. with the exponential law of Rayleigh fading, $\Pr[\max_k |h_k|^2 \le x] = (1 - e^{-x})^K$, its mean is $H_K$, and $\max_k |h_k|^2 - \ln K$ tends in law to a fixed (Gumbel) law as $K \to \infty$. So $C_K \approx \log_2(1 + \bar\gamma \ln K)$ for large $K$, which grows like $\log_2 \log K$.

**What it needs.**

- **Fading.** The gain comes from the peaks of the fading. If the channels are constant, or have a strong line-of-sight part as in a [Rician channel](/rician-fading-channel/) with a large factor, the best user is only a little better than the average one, and the gain is small.
- **Independence.** If all users fade together, the best user is no better than any one of them. Users in different places, with different scatterers, fade almost independently.
- **Channel knowledge.** The scheduler must know the current gains. Each user measures its channel and reports it; the report must arrive within the [coherence time](/coherence-time/), or the "best" user may already be in a fade.
- **Delay tolerance.** A user is served only when its channel is near a peak, so a user waits for some slots. Traffic that cannot wait gets less of the gain.

**Fairness.** With users at different distances, the best channel is almost always that of the nearest user, and max-rate scheduling starves the others. [Proportional fair scheduling](/proportional-fair-scheduling/) serves the user with the largest ratio of current rate to its own average rate, so each user is served near its own peaks. With i.i.d. channels the average rates become equal, and it then acts like max-rate scheduling; with unequal means, each user still gets a share of the gain.

**Compare with other diversity.** Classical diversity, such as [selection combining](/selection-combining/) over antennas, takes the best of several paths of one user to make that link more reliable and raise its [diversity order](/diversity-order/). Multiuser diversity takes the best of the users' channels to raise the total throughput; each single user sees an on-off service, not a more reliable link. The maximum of $K$ i.i.d. gains is the same in both cases, so the formulas match.

**Making fluctuations.** When the channels change slowly, Viswanath, Tse and Laroia (2002) proposed opportunistic beamforming: the station sends through several antennas with random, slowly changing weights, so that each user's effective channel fluctuates. With many users, some user is near the peak of the random beam at each time, and the scheduler gets the gain back.

## Examples

**Mean gain of the best user.** For i.i.d. Rayleigh fading, $\mathbb E[\max_k |h_k|^2] = H_K$:

| $K$ | 1 | 2 | 4 | 8 | 16 | 64 |
|---|---|---|---|---|---|---|
| $H_K$ | 1 | 1.5 | 2.083 | 2.718 | 3.381 | 4.744 |
| gain in dB | 0 | 1.76 | 3.19 | 4.34 | 5.29 | 6.76 |

**Throughput.** With mean SNR $\bar\gamma = 10$ dB, $C_K$ in bit/s/Hz, computed by numerical integration against the density $K e^{-x} (1 - e^{-x})^{K-1}$:

| $K$ | 1 | 2 | 4 | 8 | 16 | 64 |
|---|---|---|---|---|---|---|
| $C_K$ | 2.907 | 3.659 | 4.243 | 4.687 | 5.034 | 5.552 |
| $\log_2(1 + \bar\gamma \ln K)$ | | 2.988 | 3.894 | 4.446 | 4.844 | 5.412 |

One user gets $2.907$, less than the $3.459$ of a channel without fading at the same mean SNR, because of [Jensen's inequality](/jensens-inequality/). With two users, the scheduler already beats the channel without fading, and with 16 users it gets $5.034$, $73\%$ more than one user. The large-$K$ formula approaches $C_K$ from below. At $\bar\gamma = 0$ dB, the values are $0.860$, $1.199$, $1.528$, $1.822$, $2.077$ and $2.489$, a larger relative gain: $C_{16}/C_1 = 2.41$.

**Across frequency.** In [OFDMA](/ofdma-resource-allocation/), the same effect works across subcarriers: each subcarrier goes to the user with the best gain on it, and the sum rate grows with $K$ in the same way.

## Where it is used

- **Cellular data.** CDMA2000 EV-DO and HSDPA introduced fast channel reports and opportunistic schedulers in the downlink; LTE and 5G NR schedulers use the same idea in time and frequency.
- **Scheduler design.** Max-rate, proportional fair and other utility-based schedulers trade multiuser diversity against fairness and delay; see [wireless link scheduling](/wireless-link-scheduling/).
- **Feedback design.** Since only the best users matter, schemes where users report only when their channel is above a threshold keep most of the gain with much less feedback.
- **Multiuser MIMO.** With many antennas at the station, choosing users with nearly orthogonal channels to serve together is a form of multiuser diversity in space.

## References
