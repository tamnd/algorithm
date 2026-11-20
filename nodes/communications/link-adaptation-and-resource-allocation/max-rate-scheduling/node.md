---
tag: ZZJV41
kind: algorithm
slug: max-rate-scheduling
name: Max-rate scheduling
aliases:
- "max C/I scheduling"
- maximum throughput scheduling
area: communications/link-adaptation-and-resource-allocation
level: core
summary: Gives each resource to the user with the highest instantaneous rate, which maximizes throughput but ignores fairness.
model: real-ram
complexity:
  vars: {T: the number of slots, K: the number of users, N: the number of resources per slot}
  time: {worst: O(T K N)}
  space: {extra: O(K)}
properties: {deterministic: true, greedy: true, maximizes_total_rate: true, fair: false, needs_channel_state: true}
history:
  year: 1995
  people: [Raymond Knopp, Pierre A. Humblet]
  note: "Knopp and Humblet showed that the sum capacity of the fading uplink with power control is reached when only the user with the best channel sends at each time, which is the max-rate rule."
prereqs: [multiuser-diversity, greedy-algorithm]
see_also: [multiuser-diversity, proportional-fair-scheduling, round-robin, wireless-link-scheduling, ofdma-resource-allocation, max-min-fairness, starvation, weighted-sum-rate-maximization]
sources:
  - paper: doi:10.1109/ICC.1995.525188
    title: "Raymond Knopp and Pierre A. Humblet, Information capacity and power control in single-cell multiuser communications, Proceedings of the IEEE International Conference on Communications (ICC), 1995, pages 331 to 335"
    locator: "the result that, for the fading uplink with power control, the sum capacity is reached by letting only the user with the best channel send at each time"
  - paper: doi:10.1109/TIT.2002.1003822
    title: "Pramod Viswanath, David N. C. Tse and Rajiv Laroia, Opportunistic beamforming using dumb antennas, IEEE Transactions on Information Theory 48(6), 2002, pages 1277 to 1294"
    locator: "the comparison of serving the best user with the proportional fair scheduler when the users have unequal mean channels"
  - book: isbn:9780521845274
    title: "David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005"
    locator: "Chapter 6, the sections on multiuser diversity and its system aspects (fairness and delay, channel prediction and feedback)"
---

Max-rate scheduling, also called max C/I scheduling, is the rule that gives each resource (a time slot, a subcarrier or a resource block) to the user who can get the highest rate on it at that moment. The rate comes from the channel quality that each user reports. Because the total rate of a slot is a sum over its resources, and each term is as large as it can be, the rule gets the largest total throughput of any scheduler that gives each resource to one user, in every slot and so over any horizon. The gain over a fixed turn grows with the number of users, because some user is usually near a peak of its fading; this is [multiuser diversity](/multiuser-diversity/). The cost is fairness: a user whose channel is weaker on average, for example because it is far from the base station, is almost never the best and may get nothing. [Proportional fair scheduling](/proportional-fair-scheduling/) keeps most of the gain and serves every user.

## In plain words

Several users share one radio channel, and each user's signal changes from moment to moment. Before each short time slot, every user tells the base station how fast it could receive right now. The base station gives the slot to the user with the highest speed. If two users are equally fast, it picks the one with the lower number. This sends the most data in total, because each slot is used at its best speed. But a user with a weak signal most of the time almost never wins, so it waits for a very long time or gets nothing. That is why real systems mix this rule with some form of fairness.

## The problem

There are $K$ users and, in each of $T$ slots, $N$ resources. In slot $t$, user $k$ can get the rate $r_{k,n}(t) \ge 0$ on resource $n$, in bits per slot. The rates are known at the start of the slot, from channel reports and the [adaptive modulation](/adaptive-modulation/) table. A schedule gives each resource of each slot to one user $a_t(n) \in \{1, \ldots, K\}$; user $k$ is then served

$$S_k = \sum_{t=1}^{T} \sum_{n : a_t(n) = k} r_{k,n}(t).$$

The problem asks for the schedule with the largest total $\sum_k S_k$, using in slot $t$ only the rates known at slot $t$.

## The algorithm

```pseudo id=main
MAX-RATE(r)
L1  for t ← 1 to T do
L2      for n ← 1 to N do
L3          k* ← the smallest k with r_{k,n}(t) = max_j r_{j,n}(t)
L4          give resource n of slot t to user k*
L5          S_{k*} ← S_{k*} + r_{k*,n}(t)
L6  return the assignment and S
```

Line L3 is one pass over the users. The tie rule makes the result deterministic; any user in the set of best users gives the same total.

## Example

Three users and six slots with one resource each. User 3 is far from the base station. The rates, in bit/s/Hz:

| slot | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| user 1 | 2.1 | **3.4** | 1.2 | **4.0** | 2.5 | 0.8 |
| user 2 | **3.0** | 1.1 | **2.6** | 2.2 | **3.3** | **2.9** |
| user 3 | 0.9 | 1.0 | 1.9 | 0.7 | 1.2 | 1.5 |

Max-rate scheduling serves the bold entries: users $2, 1, 2, 1, 2, 2$, for a total of $19.2$. User 1 gets $7.4$, user 2 gets $11.8$, and user 3 gets $0$. [Round robin](/round-robin/) in the order $1, 2, 3, 1, 2, 3$ gets $2.1 + 1.1 + 1.9 + 4.0 + 3.3 + 1.5 = 13.9$, which is $28\%$ less, but it serves user 3 with $3.4$.

**Who wins how often.** Let the users' channel gains be independent and Rayleigh faded, so each gain is exponential, with means $m_1, \ldots, m_K$. With $\lambda_k = 1/m_k$, user $i$ is the best with probability

$$\Pr[i \text{ wins}] = \int_0^\infty \lambda_i e^{-\lambda_i x} \prod_{j \ne i} \big(1 - e^{-\lambda_j x}\big)\, dx = \sum_{S \subseteq \{j \ne i\}} (-1)^{|S|} \frac{\lambda_i}{\lambda_i + \sum_{j \in S} \lambda_j},$$

by [inclusion-exclusion](/inclusion-exclusion-principle/). For means $1, 2, 4$ (the users are 3 dB apart), the shares of slots are $11/105 = 10.5\%$, $30/105 = 28.6\%$ and $64/105 = 61.0\%$. With equal means each user wins $1/K$ of the slots, and max-rate scheduling is then fair in the long run.

**Throughput.** With $K$ users of equal mean SNR $\bar\gamma$ and i.i.d. Rayleigh fading, the mean rate is $\mathbb E[\log_2(1 + \bar\gamma X)]$ with $X$ the largest of $K$ unit exponentials. At $\bar\gamma = 10$ dB it is $2.907$, $3.659$, $4.243$, $4.687$, $5.034$ and $5.552$ bit/s/Hz for $K = 1, 2, 4, 8, 16, 64$, and $\mathbb E[X] = 1 + 1/2 + \cdots + 1/K$.

## Correctness

**Claim.** In each slot, the assignment of lines L2 to L4 has the largest total rate of all $K^N$ assignments, and of those with the largest total it is the first in lexicographic order. Over $T$ slots, the schedule has the largest total $\sum_k S_k$ among all schedules.

**Key steps.** The total of slot $t$ is $\sum_n r_{a(n), n}(t)$, a sum of $N$ terms, where the term of resource $n$ depends only on $a(n)$. So the sum is largest exactly when each term is largest, that is, when each $a(n)$ is a best user for resource $n$, and line L3 picks one. Among these assignments, the one with the smallest index in each place is the first in lexicographic order. The total over the horizon is the sum of the slot totals, and the choice in one slot does not change the rates of another, so the largest total is the sum of the per-slot largest totals. The share and mean-rate formulas follow from the tail $\Pr[X > x] = 1 - (1 - e^{-x})^K$. The full proof is in the proofs folder.

## Complexity

In the [real RAM](/real-ram/), line L3 costs $O(K)$ comparisons, so one slot costs $O(K N)$ and $T$ slots cost $O(T K N)$. The extra space is the $K$ totals $S_k$. The real cost is the feedback: each user must report a rate for each resource in each slot, $K N$ numbers per slot, which systems cut by reporting only the best few resources or a coarse summary.

## Properties

- **Throughput optimal.** It has the largest total rate in every slot, for any rates, among schedules that give each resource to one user.
- **Not fair.** A user whose rates are always below another user's is never served. Shares depend on the mean channel as well as on its changes.
- **Memoryless.** The choice uses only the current rates, not what users got before.
- **Greedy and exact.** The [greedy](/greedy-algorithm/) choice is exact here because the total is separable over resources and the rates are fixed. When rates depend on power shared across resources, or on interference between cells, the problem is no longer separable.
- **Gain from many users.** With i.i.d. fading, the mean rate grows like $\log_2 \log K$ with the number of users.

## Variants and improvements

- **Proportional fair.** Serve the user with the largest $r_{k,n}(t) / \bar R_k(t)$, where $\bar R_k$ is the user's average served rate; this maximizes $\sum_k \log \bar R_k$ in the long run.
- **Weighted max-rate.** Serve the user with the largest $w_k r_{k,n}(t)$. With $w_k$ equal to queue lengths, this is the max-weight rule of [wireless link scheduling](/wireless-link-scheduling/), which keeps all queues stable whenever any rule can.
- **Max-min.** Serve the user with the smallest served total; this is [max-min fairness](/max-min-fairness/) and gives up most of the gain.
- **Across frequency.** In [OFDMA](/ofdma-resource-allocation/), give each subcarrier to its best user, then spread the power over the subcarriers by water-filling; for the sum rate under a total power limit this is optimal.
- **With queues.** Serving a user with an empty buffer wastes the slot; practical forms use $\min(r_{k,n}(t), q_k)$ in place of the rate.

## When to use it

Use it when the total throughput is all that matters and the users have similar mean channels, for example in a benchmark for other schedulers or for best-effort traffic among users at similar distances. Its throughput is the upper bound that fair schedulers are compared with. Do not use it alone when users have different mean channels or delay needs.

## Pitfalls

- **Starvation.** A far user can wait forever, as user 3 in the example; this is [starvation](/starvation/), and it also hurts protocols such as TCP that time out.
- **Stale reports.** If the channel changes between the report and the slot, the "best" user may be in a fade. The gain falls when the delay approaches the coherence time.
- **Bad reports.** A user who reports a higher rate than it can receive wins slots and then fails to decode; schedulers depend on honest and calibrated reports.
- **Comparing rates, not SNRs.** With different modulation tables or code limits, the user with the best SNR is not always the user with the best rate. Compare the rates that each user can actually decode.

## Implementations

## History

Knopp and Humblet (1995) showed that the sum capacity of the fading uplink, with power control, is reached when at each time only the user with the strongest channel sends. The name "max C/I", for carrier to interference ratio, comes from the studies of the high data rate cellular systems of the late 1990s and 2000s, such as CDMA2000 EV-DO and HSDPA, where it was the throughput benchmark. Deployed systems mostly used proportional fair scheduling, because max C/I left users at the cell edge without service; Viswanath, Tse and Laroia (2002) analyzed proportional fair scheduling and showed how to keep the gain when the channel changes slowly.

## References
