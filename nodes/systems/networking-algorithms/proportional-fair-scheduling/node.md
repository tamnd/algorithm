---
tag: PSY7PJ
kind: algorithm
slug: proportional-fair-scheduling
name: Proportional fair scheduling
aliases:
- proportional fair scheduler
- PF scheduler
area: systems/networking-algorithms
level: advanced
summary: "Each slot, serve the user whose current channel rate is highest relative to its average served rate; this greedy rule maximizes the sum of log throughputs."
solves: [packet-scheduling]
model: word-ram
complexity:
  vars: {N: the number of users, s: the number of slots}
  time: {worst: Θ(s·N)}
  space: {extra: Θ(N)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [packet-scheduling, exponential-moving-average]
see_also: [proportional-fairness, network-utility-maximization, round-robin, wireless-link-scheduling, backpressure-routing, stochastic-approximation, max-min-fairness, deficit-round-robin]
sources:
  - paper: doi:10.1109/VETECS.2000.851593
    title: A. Jalali, R. Padovani and R. Pankaj, Data throughput of CDMA-HDR a high efficiency-high data rate personal communication wireless system, IEEE VTC2000-Spring, vol. 3
    locator: pp. 1854 to 1858 (the scheduler that serves the largest ratio of requested rate to average throughput, with an exponential average over a time window t_c)
  - paper: doi:10.1109/TIT.2002.1003822
    title: Pramod Viswanath, David N. C. Tse and Rajiv Laroia, Opportunistic beamforming using dumb antennas, IEEE Transactions on Information Theory 48(6) (2002)
    locator: pp. 1277 to 1294 (Section III on the proportional fair scheduler, multiuser diversity, and the time scale t_c)
  - paper: doi:10.1109/TWC.2004.830826
    title: Harold J. Kushner and Philip A. Whiting, Convergence of proportional-fair sharing algorithms under general conditions, IEEE Transactions on Wireless Communications 3(4) (2004)
    locator: pp. 1250 to 1259 (the stochastic approximation analysis; as t_c grows, the averages converge to the maximizer of the sum of log throughputs)
  - paper: "Frank Kelly, Charging and rate control for elastic traffic, European Transactions on Telecommunications 8(1), 1997, pp. 33 to 37"
    locator: the definition of proportionally fair rates as the maximizer of the sum of logs
  - book: isbn:9780521845274
    title: David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005
    locator: Chapter 6 (multiuser diversity and the proportional fair scheduler)
  - book: isbn:9781107036055
    title: R. Srikant and Lei Ying, Communication Networks, An Optimization, Control and Stochastic Networks Perspective, Cambridge University Press, 2014
    locator: Section 5.2 (channel-aware scheduling in cellular networks)
---

Proportional fair (PF) scheduling is the downlink scheduler of cellular data systems, first used in the CDMA-HDR system by Jalali, Padovani and Pankaj (2000). In each time slot, every user $i$ reports the rate $r_i(t)$ that its channel supports now. The base station serves the user with the largest ratio $r_i(t) / R_i(t)$, where $R_i$ is an [exponential moving average](/exponential-moving-average/) of the rate that user $i$ has received, with time constant $t_c$ slots. A user is served when its channel is good compared with what it usually gets, so the scheduler rides the peaks of each user's fading and still gives every user a share. One step of the rule maximizes $\sum_i \log R_i(t+1)$, and for a large $t_c$ the long-run throughputs approach the [proportionally fair](/proportional-fairness/) point, which maximizes $\sum_i \log T_i$ over all throughputs that a scheduler can give. Each slot costs $\Theta(N)$ for $N$ users.

## In plain words

A cell tower sends data to many phones, one phone at a time. The radio signal to each phone rises and falls quickly. A phone near the tower always has a better signal than a phone at the edge.

If the tower always serves the phone with the best signal, the near phone gets almost everything and the far phone starves. If it takes turns, every phone gets the same time, but often at a bad moment for its signal.

Proportional fair scheduling compares each phone with its own past. It serves the phone whose signal now is best compared with the average service that phone has had. A far phone gets served at its own good moments, and the near phone at its own good moments. Each phone gets a fair share, and the tower moves more data than with plain turns.

## The problem

A base station serves $N$ users over one shared channel in time slots. In slot $t$ it can serve one user, and user $i$ then gets $r_i(t)$ bits. The rates change from slot to slot because of fading, and the base station learns them at the start of each slot. The aim is a choice rule that makes good use of the channel and is fair. Serving the largest $r_i(t)$ maximizes the total throughput but can starve users with weak channels. [Round robin](/round-robin/) gives each user the same time but ignores the channel. PF aims at the throughput vector $T$ that maximizes $\sum_i \log T_i$ over the set of long-run throughputs that some scheduler can give, the proportionally fair point of Kelly. The page [proportional fairness](/proportional-fairness/) treats that criterion for rates in a network; this page is the slot-by-slot scheduler that reaches it on one fading channel.

## The algorithm

Each user $i$ has an average $R_i > 0$. The time constant $t_c > 1$, in slots, sets how far back the average looks. The pseudocode gives the work of one slot.

```pseudo id=main
PF-SLOT(rates r_1, ..., r_N, averages R_1, ..., R_N, time constant t_c)
L1  i* ← the user i with the largest r_i / R_i, the lowest index on ties
L2  serve user i* at rate r_{i*}
L3  for i ← 1 to N:
L4      if i = i* then R_i ← (1 − 1/t_c) R_i + (1/t_c) r_i
L5      else R_i ← (1 − 1/t_c) R_i
```

Lines L4 and L5 average the rate that user $i$ received, which is $r_i$ in a slot where it is served and 0 otherwise. The averages start at a small positive value so that line L1 never divides by zero.

## Example

**A fixed channel.** Two users and $t_c = 2$, so each update moves the average halfway. User 1 always gets rate 1 and user 2 always gets rate 2. Both averages start at 1.

| slot | $R_1$ | $R_2$ | $r_1/R_1$ | $r_2/R_2$ | served |
|---|---|---|---|---|---|
| 1 | 1 | 1 | 1 | 2 | 2 |
| 2 | 0.5 | 1.5 | 2 | 1.33 | 1 |
| 3 | 0.75 | 0.75 | 1.33 | 2.67 | 2 |
| 4 | 0.375 | 1.375 | 2.67 | 1.45 | 1 |

PF alternates, so each user gets half of the slots and the throughputs are 0.5 and 1. This is the maximizer of $\log(x) + \log(2(1-x))$ over the time share $x$. If in slot 5 user 1 has a peak of rate 3 and user 2 has rate 1, the ratios are 4.36 and 1.45, and user 1 is served.

**Rayleigh fading.** Four users have mean signal-to-noise ratios 1, 3, 10 and 30, and the rate is $\log_2(1 + \text{snr}_i \cdot h)$ with $h$ drawn from an exponential distribution with mean 1 in each slot. In a seeded run of 20,000 slots with $t_c = 100$:

| scheduler | throughputs (bits per slot per hertz) | total | $\sum \log T_i$ |
|---|---|---|---|
| max-rate | 0.006, 0.105, 0.944, 3.559 | 4.615 | −6.09 |
| round robin | 0.220, 0.414, 0.734, 1.066 | 2.434 | −2.64 |
| PF | 0.371, 0.664, 1.081, 1.509 | 3.625 | −0.91 |

Max-rate gives 73% of the slots to the strongest user and almost nothing to the weakest. PF gives between 22% and 28% of the slots to each user, but serves each one near its peaks, so every user gets more than under round robin and the total is 49% higher. This gain is the multiuser diversity gain.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md).

1. **One step is greedy for the log utility.** Among all choices of the user to serve in a slot, line L1 picks one that maximizes $\sum_i \log R_i(t+1)$. Serving user $k$ adds $\log(1 + r_k / ((t_c - 1) R_k))$ to the sum, which grows with $r_k / R_k$.
2. **The fixed point is proportionally fair.** Let the channel states be independent and identically distributed over slots. If a vector $T^*$ is such that the fixed rule "serve the largest $r_i / T^*_i$" gives long-run throughputs $T^*$, then $T^*$ maximizes $\sum_i \log T_i$ over all throughputs that any scheduler can give, and it is the only maximizer.
4. **Equal time under scaling.** If the rate of user $i$ is a constant $c_i$ times a fading value with the same distribution for all users, the proportionally fair point gives each user $1/N$ of the slots.
3. **The averages converge.** Kushner and Whiting showed with [stochastic approximation](/stochastic-approximation/) that, as $t_c$ grows, the averages $R_i$ track a differential equation whose stable point is that maximizer. This result is cited, not proved here.

## Complexity

Each slot costs $\Theta(N)$ time: one pass over the users for line L1 and one for lines L3 to L5. The space is $\Theta(N)$ for the averages. The update of the users that are not served is a common scaling by $1 - 1/t_c$, so a form that keeps one global scale factor needs only $O(1)$ updates per slot, but line L1 still reads every rate.

## Properties

- **Opportunistic.** A user is served when its channel is near its own peak, which gives the multiuser diversity gain. The gain grows with the number of users and with the fading spread.
- **Scale free.** If every rate of user $i$ is multiplied by a constant, the choices do not change. When the rates of the users have the same distribution up to scale, each user gets $1/N$ of the slots.
- **Fair in the log sense.** For a large $t_c$, the throughputs approach the maximizer of $\sum_i \log T_i$. In the fading example, every user gets more than under round robin.
- **No queues.** The rule uses rates and averages only. It assumes that every user always has data.
- **Short-term behavior set by $t_c$.** A small $t_c$ gives fairness over short windows and less diversity gain. A large $t_c$ gives more gain, but a user can wait longer between slots.

## Variants and improvements

- **Alpha-fair and gradient scheduling.** Serve the largest $r_i U'(R_i)$ for a concave utility $U$. With $U = \log$ this is PF. With $U'(x) = x^{-\alpha}$, $\alpha = 0$ is max-rate and a large $\alpha$ moves toward [max-min fairness](/max-min-fairness/).
- **Queue-aware rules.** Rules such as M-LWDF weigh the ratio with the queue length or the head-of-line delay, so that the scheduler also keeps queues stable, as in [backpressure routing](/backpressure-routing/).
- **Multi-carrier PF.** LTE and later systems apply the ratio per resource block in each slot, and update the averages with the total rate a user got.
- **Opportunistic beamforming.** Viswanath, Tse and Laroia add random phase and power to several antennas, so that a slow channel fluctuates and PF can exploit it.

## When to use it

Use PF for the downlink of a cellular or other shared wireless channel when the base station learns each user's rate before every slot, the users have independent fading and elastic data, and a fair share per user matters. For a wired link with fixed rates, PF gives each user equal time, and a byte-fair scheduler such as [DRR](/deficit-round-robin/) is a better fit. For traffic with delay targets, use a queue-aware rule.

## Pitfalls

- **A zero average.** If $R_i$ starts at 0, line L1 divides by zero. Start each average at a small positive value.
- **Idle users.** The average of a user with no data decays, so when that user comes back it can take many slots in a row. Freeze or cap the average of idle users.
- **Stale rate reports.** If the reported rate is older than the coherence time of the channel, the scheduler chases peaks that are gone, and the gain disappears.
- **No fading, no gain.** On a static channel, PF only shares the time equally. The gain needs the rates to change over a time scale shorter than $t_c$.
- **The wrong fairness.** PF gives users with good channels more bits. If each user must get the same bits, PF is not the right rule.

## Implementations

## History

Knopp and Humblet observed in 1995 that, with many users and independent fading, serving the user with the best channel raises the capacity of a cell, which became known as multiuser diversity. Kelly defined proportionally fair rates for elastic traffic in 1997. Jalali, Padovani and Pankaj of Qualcomm described the PF scheduler for the CDMA-HDR system in 2000, which became the downlink of cdma2000 1xEV-DO. Viswanath, Tse and Laroia analyzed PF in 2002 and added opportunistic beamforming. Kushner and Whiting proved convergence under general conditions in 2004. PF and its variants became the usual downlink schedulers of HSDPA and LTE.

## References
