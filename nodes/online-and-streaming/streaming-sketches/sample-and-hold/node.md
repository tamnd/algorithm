---
tag: HS0C9K
kind: algorithm
slug: sample-and-hold
name: Sample and hold
aliases:
- Estan-Varghese sample and hold
area: online-and-streaming/streaming-sketches
level: core
summary: Samples new flows with small probability and then counts every later packet exactly.
solves: [frequent-items-problem]
model: streaming-model
complexity:
  vars: {p: the sampling probability for each unit, m: the number of units in the stream}
  time: {expected: O(1)}
  space: {expected: O(p m)}
properties: {online: true, deterministic: false, comparison: false, recursive: false}
prereqs: [frequent-items-problem, frequency-vector, stream-sampling]
see_also: [sticky-sampling, lossy-counting, space-saving, count-min-sketch, frequency-estimation, epsilon-delta-guarantee]
sources:
  - paper: doi:10.1145/964725.633056
    title: Cristian Estan and George Varghese, New directions in traffic measurement and accounting, Proceedings of ACM SIGCOMM 2002
    locator: pages 323 to 336, the section on sample and hold, with the oversampling factor, the probability of missing a large flow, and the bounds on memory and error
  - url: https://www.vldb.org/conf/2002/S10P03.pdf
    title: Gurmeet Singh Manku and Rajeev Motwani, Approximate frequency counts over data streams, VLDB 2002, pages 346 to 357
    locator: Section 4.1, Sticky Sampling, the same sample-then-count idea with a falling rate
---

Sample and hold is a randomized method to find and measure the large flows on a network link, by Estan and Varghese (2002). Each byte or packet of a flow that is not yet in the table is sampled with a small probability $p$. Once a flow is sampled, it is held: every later byte of it is counted exactly. A flow with $f$ units is missed with probability $(1 - p)^f$, the held count misses about $1/p$ units at its start, and adding $(1-p)/p$ gives an unbiased estimate with standard deviation below $1/p$. The expected table size is at most $pm$ for a stream of $m$ units. With $p = O/T$ for a threshold $T$, a flow of size $T$ is missed with probability at most $e^{-O}$, and its relative error is at most $1/O$.

## In plain words

A router sees millions of packets and wants to know which flows send the most bytes. It cannot keep a counter for every flow. So it flips a coin with a small chance of success for each byte of a flow that it does not track yet. When the coin succeeds, the router starts a counter for that flow and from then on counts every byte of it.

A large flow gets many coin flips, so it is caught early and its counter misses only a few bytes at the start. A small flow is rarely caught, so it seldom takes up memory. The counter misses on average about one over the chance of success, so you add that to get a fair estimate.

## The problem

The input is a stream of $m$ units, each labeled with an item, the flow it belongs to. A unit is one byte or one packet; a packet of $b$ bytes is $b$ consecutive units of the same flow. Let $f_x$ be the number of units of flow $x$, the entry of the [frequency vector](/frequency-vector/). The goal is to report the flows with $f_x \ge T$, for a threshold $T$ that is a fraction of the link capacity, with good estimates of their sizes, and to use memory close to $m/T$. This is a form of the [frequent items problem](/frequent-items-problem/), with a randomized guarantee in the sense of the [epsilon-delta guarantee](/epsilon-delta-guarantee/).

## The algorithm

The table $H$ maps the held items to counts.

```pseudo id=main
SH-UPDATE(H, x)                          ▷ one unit of item x
L1  if x ∈ H then H[x] ← H[x] + 1
L2  else with probability p insert x with H[x] ← 1

SH-ESTIMATE(H, x)
L3  if x ∈ H then return H[x] + (1 − p)/p
L4  else return 0
```

**Oversampling.** For a threshold $T$, Estan and Varghese set $p = O/T$, where the *oversampling factor* $O$ is a small number such as 20. Then a flow of size $T$ gets about $O$ sampling chances. For a packet of $b$ bytes of a flow that is not held, line L2 is the same as sampling the packet with probability $1 - (1 - p)^b$; the paper then counts the whole packet, which makes the held count slightly too large, by less than one packet.

**Measurement intervals.** In the router, the table is read and cleared at the end of each interval. Estan and Varghese keep the entries of large flows into the next interval, so that a large flow is counted from the start of the next interval and its count there is exact.

## Example

Let $p = 1/2$ and let flow $a$ send 6 units. Suppose the coins for its first two units fail and the third succeeds. Then line L2 inserts $a$ at the third unit, and line L1 counts the last three, so $H[a] = 4$. The estimate is $4 + (1 - 1/2)/(1/2) = 5$, while $f_a = 6$.

Over all coin outcomes, the number $J$ of missed units has $\Pr[J = j] = (1/2)^{j+1}$ for $j < 6$, and the flow is missed entirely with probability $(1/2)^6 = 1/64$. The average of the estimate over these outcomes is exactly 6.

## Correctness

Let $q = 1 - p$. Fix an item $x$ with $f = f_x$ units. Let $J$ be the number of its units before the first sampled one, so $\Pr[J = j] = q^j p$ for $j < f$, and the item is never held with probability $q^f$.

**Theorem.**

1. $\mathbb{E}[\hat f_x] = f_x$: the estimate is unbiased.
2. $\mathrm{Var}[\hat f_x] \le (1 - p)/p^2$, so the standard deviation is below $1/p$.
3. The held count is a lower bound, low by $\frac{q}{p}(1 - q^f) < 1/p$ on average.
4. The item is missed with probability $q^f \le e^{-pf}$.
5. The expected number of entries is at most $pm$.

The key step is to compare with an unlimited geometric variable $Y$, with $\Pr[Y = j] = q^j p$ for all $j \ge 0$. The variable $g = f - Y + q/p$ has mean $f$ and variance $\mathrm{Var}[Y] = q/p^2$. The estimate equals $g$ when $Y < f$ and $0$ when $Y \ge f$. Given $Y \ge f$, the excess $Y - f$ has the same geometric law as $Y$, because the geometric law has no memory. So $\mathbb{E}[g \mid Y \ge f] = 0$, and setting $g$ to 0 on this event does not change the mean. It also can only lower the second moment, so the variance of the estimate is at most that of $g$. The full proof is below.

**Large flows.** With $p = O/T$ and $f_x \ge T$, the flow is missed with probability at most $e^{-O}$, and the standard deviation of the estimate is below $1/p = T/O$, that is a relative error of at most $1/O$ for a flow of size $T$.

## Complexity

- **Time.** $O(1)$ expected time for each unit, with a hash table for $H$, and one random number for each unit of an unheld flow.
- **Space.** Item $x$ is held with probability $1 - q^{f_x} \le p f_x$, so the expected number of entries is at most $\sum_x p f_x = pm$. With $p = O/T$ and a link of capacity $C = m$ units in an interval, this is $O \cdot C/T$ entries. For $T = zC$, a fraction $z$ of the link, it is $O/z$.

## Properties

- **Randomized.** The estimates are random; the bounds hold in expectation and with the probabilities above.
- **Unbiased.** With the correction $(1 - p)/p$, the estimate has mean $f_x$ for every flow, including flows that are missed.
- **Error independent of the flow size.** The standard deviation is below $1/p$ for every flow. Sampling each packet independently and scaling by $1/p$, as in sampled NetFlow, gives standard deviation $\sqrt{f(1-p)/p}$, which grows with $f$. For a flow of size $T$ with $p = O/T$, that is a relative error of about $1/\sqrt{O}$, against $1/O$ here.
- **Insertion only.** There is no way to remove units.

## Variants and improvements

- **Multistage filters.** The same paper introduces multistage filters: several arrays of counters indexed by independent hash functions, and a flow enters the table only when all its counters pass the threshold. This is close to the [count-min sketch](/count-min-sketch/) with a conservative update, and it has no false negatives.
- **Preserving entries.** Keep the entries of large flows from one interval to the next, and remove early the entries that are added late in an interval and stay small.
- **A falling rate.** [Sticky sampling](/sticky-sampling/) uses the same "sample, then count exactly" rule with a rate that halves as the stream grows, so its memory does not depend on $m$.
- **Fixed memory.** When the table must have a fixed size, the deterministic [Space-Saving](/space-saving/) summary gives error at most $m/k$ with $k$ counters.

## When to use it

Use sample and hold to measure large flows, sources or keys in a high-speed stream when memory is very small compared with the number of distinct items, and when a fixed error of about $1/p$ units is good enough. It needs only one coin for each unit of an unheld item and one counter update for each unit of a held item. When you need a guarantee on every flow with probability 1, use [Space-Saving](/space-saving/). When you need deletions or a linear sketch, use the [count-min sketch](/count-min-sketch/).

## Pitfalls

- **Reading the held count as the size.** The held count misses about $1/p$ units at the start of the flow. Add $(1-p)/p$ for an unbiased estimate, or report the held count as a lower bound.
- **A threshold below $1/p$.** The standard deviation is about $1/p$ for every flow, so flows with fewer than a few times $1/p$ units are estimated with large relative error. Choose $p = O/T$ with $O$ large enough.
- **A memory bound for the worst case.** The bound $pm$ is on the expected number of entries. Each entry is an independent event for its flow, so the number is concentrated around its mean, but a fixed table needs headroom or a policy for when it is full.
- **Sampling packets with a fixed probability.** For packets of different sizes, a fixed probability for each packet favors flows of many small packets. Sample each byte, that is a packet of $b$ bytes with probability $1 - (1-p)^b$, to make the analysis hold for bytes.

## Implementations

## History

Cristian Estan and George Varghese introduced sample and hold and multistage filters at ACM SIGCOMM 2002, in *New directions in traffic measurement and accounting*, to identify and measure the large flows on high-speed links with a small amount of fast memory. They compared them with sampled NetFlow, the packet sampling then used in routers. The idea of sampling an item and then counting it exactly goes back to counting samples of Gibbons and Matias (1998), and it appears again in sticky sampling of Manku and Motwani the same year.

## References
