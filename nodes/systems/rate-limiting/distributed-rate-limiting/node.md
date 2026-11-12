---
tag: 1S0PYE
kind: problem
slug: distributed-rate-limiting
name: Distributed rate limiting
aliases:
- global rate limiting
- DRL
area: systems/rate-limiting
level: advanced
summary: "Enforce one global limit, such as a token bucket of rate R and depth B, on traffic that enters through many servers, each of which sees only its own arrivals and late news of the others."
prereqs: [rate-limiting-problem, token-bucket]
see_also: [g-counter, pn-counter, gossip-protocol, max-min-fairness, sliding-window-counter, rate-limiter, admission-control, throttling]
sources:
  - paper: doi:10.1145/1282380.1282419
    title: "Barath Raghavan, Kashi Vishwanath, Sriram Ramabhadran, Kenneth Yocum and Alex C. Snoeren, Cloud Control with Distributed Rate Limiting, Proceedings of ACM SIGCOMM 2007, pages 337 to 348"
    locator: "Section 1 (accuracy against responsiveness), Section 3 (limiter design: estimation, communication and allocation), Section 3.2 (global token bucket), Section 3.2.1 and Figure 1 (global random drop), Section 3.2.2 and Figure 2 (flow proportional share), Appendix (stability of FPS)"
  - paper: doi:10.1109/SFCS.2003.1238221
    title: "David Kempe, Alin Dobra and Johannes Gehrke, Gossip-Based Computation of Aggregate Information, Proceedings of the 44th IEEE Symposium on Foundations of Computer Science (FOCS 2003), pages 482 to 491"
    locator: "The Push-Sum protocol for sums and averages, and its number of rounds"
  - url: https://www.rfc-editor.org/rfc/rfc2697
    title: "Juha Heinanen and Roch Guerin, RFC 2697, A Single Rate Three Color Marker, September 1999"
    locator: "Section 3 (the token bucket meter that a central limiter runs)"
---

Distributed rate limiting is the problem of enforcing one limit on the total traffic of a service when the traffic enters through many servers, and each server sees only its own arrivals and late reports from the others. The reference is a central limiter, usually a [token bucket](/token-bucket/) of rate $R$ and depth $B$ that sees the merged stream. A distributed solution must stay close to that limiter in two ways at once: it must not admit much more, and it must not reject traffic that the central limiter would admit. Raghavan, Vishwanath, Ramabhadran, Yocum and Snoeren stated the problem for cloud services in 2007 and gave three solutions: global token bucket, global random drop and flow proportional share.

## In plain words

A customer pays for 100 requests per second in total. The requests arrive at ten different data centers. Each data center can count its own requests, but it hears about the others only after a delay.

If each data center allows 10 requests per second, the total is safe, but a customer whose users are all in one city gets only 10. If each allows 100, a customer with users in all cities gets up to 1000. Neither is right.

So the data centers must talk. Each one tells the others how busy it is, and each one sets its own share from what it hears. The news is always a bit late, so a sudden rush at many places at once can get through before anyone hears of it. The more often the servers talk, the closer they get to one central limit, and the more messages they send.

## Definition

**Sites and arrivals.** There are $N$ sites (limiters). Request or packet $j$ arrives at one site $s_j$ at time $t_j$ with size $L_j$ (1 for requests, bytes for packets). The arrival model is adversarial: the traffic can move between sites at any time.

**The reference limit.** A central [token bucket](/token-bucket/) TB$(R, B)$ that sees all arrivals in time order. Its output satisfies, for every interval $I$ of length $\tau$, $\text{admitted}(I) \le B + R\tau$, and its long-term rate is at most $R$. Some systems use a window count instead, as in the [rate limiting problem](/rate-limiting-problem/).

**Information.** Site $i$ decides each of its arrivals at the arrival time. The decision can use the arrivals at site $i$ so far and the messages it has received. A message from site $k$ sent at time $t$ arrives no earlier than $t + d$, where $d > 0$ is the delay. Many designs send messages only at the end of each estimate interval of length $T$.

**The goals.**

- **Accuracy (safety).** The admitted traffic of all sites together stays close to the reference: the overshoot $\max_I \big(\text{admitted}(I) - B - R\tau\big)$ is small, and the long-term rate is at most $R$.
- **Utility.** The sites admit about what the central limiter admits on the same trace, wherever the traffic arrives.
- **Fairness.** Optional. The share of each flow is about what it would get at one central limiter, for example the [max-min fair](/max-min-fairness/) share among TCP flows.
- **Cost.** The number of messages per second, and the work per arrival.

Raghavan et al. state the goal as "a receiver should not be able to tell whether the rate limit is enforced at one or many locations".

## Variants

- **Request limits and byte limits.** API gateways count requests per client key. Network limiters count bytes, as in the 2007 paper.
- **Hard and soft limits.** A hard limit allows no overshoot, so each admission waits for a central decision or for tokens leased in advance. A soft limit allows a bounded or measured overshoot in exchange for local decisions.
- **Central store and peer to peer.** One design keeps the count in one shared service that every site asks. The other has functionally identical peers that exchange estimates, as in the paper.
- **Per-key limits.** Each client key has its own global limit, so the sites keep one state per active key.
- **Window counts.** The limit is "at most $L$ requests per window", and each site keeps a replicated count per window, for example a [G-counter](/g-counter/), or a [PN-counter](/pn-counter/) when admissions can be returned.

## Examples

The examples use a global limit of $R = 100$ units per second. The numbers come from a short script with exact fractions.

**Static split.** Each of $N = 4$ sites runs a token bucket of rate 25. The total is safe (Theorem 1 below). If all the traffic, 100 units per second, arrives at site 1, the sites admit 25 units per second, while the central limiter admits 100. The utility is $1/4$.

**No coordination.** Each site runs a full token bucket of rate 100. When all four sites have 100 units per second of demand, they admit 400 units per second, four times the limit.

**Global random drop (GRD).** Every site knows the demand estimates $r = (60, 30, 30, 0)$, so the global demand is 120. Each site drops each arrival with probability $(120 - 100)/120 = 1/6$. The expected admitted rates are 50, 25, 25 and 0, a total of exactly 100. GRD matches the central limiter in the number of drops over a period, not in the burst behavior of a token bucket.

**Global token bucket (GTB) with a stale report.** Each GTB site refills its bucket at the global rate 100 and removes tokens for its own arrivals and at the reported rate of the others. Site 1 last heard that site 2 sends 60 units per second, but site 2 has stopped. Until the next report, site 1 drains 60 tokens per second for traffic that does not exist and admits only 40 units per second. This is why the paper finds GTB sensitive to stale and lost reports.

**Flow proportional share (FPS).** Two sites, three TCP flows at site A and one at site B, all limited only by the rate limiter, and local limits $50$ and $50$ at the start. At A each flow gets $50/3$, so A's weight is its local limit divided by its largest flow rate: $50/(50/3) = 3$. B's weight is $50/50 = 1$. The new local limits are $100 \cdot 3/4 = 75$ and $100 \cdot 1/4 = 25$, so each of the four flows gets 25, the max-min fair share. Now cap B's flow at 10 elsewhere in the network. B is below its limit 25, so its weight becomes $10 \cdot 3/(100 - 10) = 1/3$, and the limits become 90 and 10: the max-min fair split 30, 30, 30 and 10. In the next interval B's demand equals its limit 10, so FPS takes the first rule again, the weight returns to 1 and the limits to 75 and 25. The paper names this swing between the two rules and damps it with an [EWMA](/exponential-moving-average/).

**A shared counter with delay.** Three sites share a limit of $L = 100$ requests per window through a replicated count. At one instant each site gets 60 requests, and no site has heard of the others yet. Each site sees a count below 100 for each of its own requests, so it admits all 60, and the window gets 180 requests. Theorem 4 below gives the bound: the last request was admitted at a count of 59, and the 120 requests of the other sites were not yet visible, so $180 = 59 + 1 + 120$.

**Token leasing.** A central bucket of rate 100 gives tokens in chunks of $c = 10$ to $N = 4$ sites. A site asks for a new chunk only when its chunk is used up, so the sites send one request per 10 admissions instead of one per admission. At any time at most $N c = 40$ leased tokens wait unused at the sites.

## Known algorithms

- **Central limiter.** One token bucket on one server, or one shared counter store, decides every arrival. It is exact, but each decision costs a round trip, and the central server is a single point of failure and a bottleneck.
- **Static partition.** Site $i$ runs TB$(r_i, b_i)$ with $\sum r_i = R$ and $\sum b_i = B$. It needs no messages and is always safe, but it wastes the limit when the traffic is uneven.
- **Global token bucket (GTB).** Raghavan et al., Section 3.2. Each site refills at the global rate and removes tokens for its own arrivals and for the reported rates of the other sites. It tries to copy the packet-level behavior of the central bucket.
- **Global random drop (GRD).** Section 3.2.1, Figure 1. With global demand $D = \sum_i r_i$ from the exchanged estimates, each site drops each packet with probability $(D - R)/D$ when $D > R$. It copies the drop rate of the central limiter, not its bursts, and has no tuning parameters of its own other than the estimate interval and the EWMA weight. Its rule looks like [RED](/red-random-early-detection/) without a queue.
- **Flow proportional share (FPS).** Section 3.2.2, Figure 2. Each site runs a local token bucket and sets its local limit in proportion to a weight, the equivalent number of TCP flows for which the limiter is the bottleneck. If local demand is at least the local limit, the weight is the local limit divided by the largest sampled flow rate. Otherwise the weight is set so that the local limit equals the local demand. The local limit is weight times $R$ divided by the sum of all weights. The goal is max-min fairness among TCP flows across sites.
- **Estimation and dissemination.** Each site averages its arrival rate over an estimate interval, smooths it with an EWMA, and sends it to the others. A full mesh needs $\Theta(N^2)$ messages per interval. The paper uses a [gossip protocol](/gossip-protocol/) after Kempe, Dobra and Gehrke, in which each site sends to a fixed number of random sites per interval.
- **Replicated counters.** For window limits, each site counts its own admissions in its own entry of a [G-counter](/g-counter/) and merges the entries of the others by maximum. The sum of the entries is a lower estimate of the true count. See the [sliding window counter](/sliding-window-counter/) for the per-window counting.
- **Token leasing.** A central bucket hands out chunks of $c$ tokens, and a site admits only with tokens that it holds. It trades the message rate against the number of idle tokens (Theorem 5).

## Bounds

All bounds are worst case over adversarial arrivals. Theorems 1 to 5 are short proofs; the FPS results are from the paper, and the accuracy numbers in the paper are measured.

**Theorem 1 (static split is safe).** If site $i$ runs TB$(r_i, b_i)$ with $\sum_i r_i \le R$ and $\sum_i b_i \le B$, then for every interval of length $\tau$ the sites together admit at most $B + R\tau$.

*Proof.* A token bucket of rate $r$ and depth $b$ admits at most $b + r\tau$ in any interval of length $\tau$: its count is at most $b$ at the start, gains at most $r\tau$, and is never negative. Add over the sites: $\sum_i (b_i + r_i\tau) \le B + R\tau$. $\square$

**Theorem 2 (the cost of no communication).** Take a scheme without messages, and let $u_i$ be the long-term rate that site $i$ admits when it alone gets an unbounded demand. If the scheme never exceeds the long-term rate $R$ on any trace, then $\sum_i u_i \le R$. So some site has $u_i \le R/N$, and on a trace that sends all the traffic to that site the utility is at most $1/N$.

*Proof.* Without messages, the decisions of site $i$ depend only on its own arrivals. Take the trace in which every site $i$ gets the same arrivals as in its single-site trace. Each site makes the same decisions as before, so the long-term total rate is $\sum_i u_i$, and this must be at most $R$. $\square$

**Theorem 3 (accuracy against responsiveness).** Let the message delay be $d$. Suppose that a scheme admits a burst of size $B$ at a single site at once, as the central limiter does when it is full. Then at a time when all sites have been idle for at least $d$ with full state, a burst of size $B$ at each of the $N$ sites at the same instant is admitted in full, a total of $NB$ in an interval of length 0, against the reference bound $B$.

*Proof.* At the burst time, no site can have a message about the bursts at the other sites, since such a message arrives at least $d$ later. Each site's state is the same as in the trace where only it gets the burst, so it makes the same decisions and admits $B$. $\square$

This is the statement of Raghavan et al. that a distributed limiter cannot be both perfectly accurate and responsive: the delay of the communication bounds how fast one site can react to the others. Each scheme picks a point between the static split (accurate, not responsive) and independent full limiters (responsive, not accurate).

**Theorem 4 (overshoot of a delayed shared count).** Each site admits a request in a window only if its view of the count of the window is less than $L$. A site's view includes all its own admissions, and the admissions of other sites at least $d$ earlier. Then the window gets at most $L + U$ admissions, where $U$ is the number of admissions at the other sites in the $d$ before the last admission of the window.

*Proof.* Let the last admission be at site $i$ at time $t$. The view of site $i$ was at most $L - 1$. The view misses at most the admissions of the other sites in $(t - d, t]$, which are at most $U$. So the admissions before this one are at most $L - 1 + U$, and with it at most $L + U$. $\square$

In the example above, $L = 100$ and $U = 120$ give at most 220, and the real total is 180. If each site has at most $a$ arrivals per unit time, then $U \le (N-1) a d$.

**Theorem 5 (token leasing).** If a central TB$(R, B)$ hands out chunks of $c$ tokens, and each site holds at most one unused chunk, then in every interval of length $\tau$ the sites admit at most $B + R\tau + Nc$. The long-term rate is at most $R$, and at any time at most $Nc$ tokens are held unused.

*Proof.* The admissions in the interval use tokens held at its start, at most $Nc$, or tokens leased during it. The tokens leased during the interval are at most the central count at its start, at most $B$, plus the refill $R\tau$. Divide by $\tau$ and let $\tau$ grow for the rate. $\square$

**GRD rate.** If the estimates are exact and constant and $D > R$, the expected admitted rate is $\sum_i r_i (1 - (D-R)/D) = D \cdot R/D = R$.

**FPS stability.** Raghavan et al. prove in the Appendix that FPS is stable: with constant demands, once the weights are at the correct allocation they stay there. Whether FPS always converges, and how fast, is left open in the paper.

**Messages.** A full mesh sends $N(N-1)$ updates per estimate interval. Push-Sum gossip (Kempe, Dobra and Gehrke) computes sums and averages with each node sending one message per round, and reaches relative error $\varepsilon$ in $O(\log N + \log(1/\varepsilon))$ rounds with high probability.

**Measured numbers.** In the paper's experiments the baseline estimate interval is 50 ms with a 1-second EWMA parameter of 0.1, and FPS kept near-ideal rate enforcement and fairness to 490 limiters at a 50 Mbps limit with about 23 Kbps of control traffic per limiter. These numbers are measurements, not bounds.

## Reductions

- **One site.** With $N = 1$, or with zero delay and a message for every arrival, the problem is the central [rate limiting problem](/rate-limiting-problem/), solved exactly by a token bucket.
- **Distributed aggregation.** Every scheme needs an estimate of a global sum, the total demand or the total count. That is the aggregation problem of [gossip protocols](/gossip-protocol/) and of counter [CRDTs](/crdt/).
- **Fair allocation.** Once the demands are known, setting the local limits is an allocation problem; FPS solves it for [max-min fairness](/max-min-fairness/) among TCP flows.

## Applications

- **Cloud services.** A customer buys an aggregate bandwidth or request limit for a service that runs in many data centers. This is the motivation of the 2007 paper.
- **Content distribution networks.** A per-customer limit on the traffic served from many mirrors, as in Section 2.2 of the paper.
- **API gateways.** A per-key request quota enforced across a fleet of gateway servers, usually with a shared counter store or with leased tokens.
- **Testbeds.** Section 2.3 of the paper limits the bandwidth of one PlanetLab slice across many machines.
- **Overload protection.** A global limit on the work sent to one shared backend from many clients, together with [admission control](/admission-control/) and [throttling](/throttling/) at the clients.

## References
