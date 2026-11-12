---
tag: RQDMZ5
kind: concept
slug: cache-hit-ratio
name: Cache hit ratio
aliases:
- hit rate
- miss rate
- hit ratio
- miss ratio
- byte hit ratio
area: systems/caching-policies
level: intro
summary: "The fraction of requests that a cache serves without a miss, for a given trace, policy and size. The miss ratio is one minus it; the byte hit ratio weights each request by size."
prereqs: [cache]
see_also: [three-cs-model, miss-ratio-curve, locality-of-reference, reuse-distance, independent-reference-model, multilevel-caching, belady-anomaly]
sources:
  - book: isbn:9780128119051
    title: John L. Hennessy and David A. Patterson, Computer Architecture, A Quantitative Approach, sixth edition, Morgan Kaufmann, 2017
    locator: Appendix B, Review of Memory Hierarchy (miss rate, average memory access time, and local and global miss rates of two-level caches)
  - paper: doi:10.1145/356887.356892
    title: "Alan Jay Smith, Cache memories, ACM Computing Surveys 14(3) (1982), 473-530"
    locator: the miss ratio as the main figure of merit, and cold-start against warm-start miss ratios
  - paper: doi:10.1147/sj.92.0078
    title: "R. L. Mattson, J. Gecsei, D. R. Slutz and I. L. Traiger, Evaluation techniques for storage hierarchies, IBM Systems Journal 9(2) (1970), 78-117"
    locator: the hit ratio as a function of the capacity, computed for all capacities in one pass
---

The hit ratio of a cache on a request sequence is the number of hits divided by the number of requests, and the miss ratio is one minus the hit ratio. Both depend on three things together: the trace, the replacement policy and the cache size. Systems people quote the miss ratio more often, because the time spent on memory grows in proportion to it, as the formula for the average access time below shows. When items have different sizes, the byte hit ratio counts bytes instead of requests, and it can be very different from the hit ratio.

## In plain words

Count the requests that a cache answers by itself, and divide by all requests. That is the hit ratio. The rest of the requests go to the slow store, and their share is the miss ratio.

The number has no meaning alone. The same cache gives a high ratio on a program that reuses a few items, and a low ratio on a program that reads each item once. A bigger cache or a better policy usually raises it. A hit ratio that looks close to perfect can still hide a slow system. If a miss costs a hundred times a hit, then a change from 96 to 98 hits in each hundred requests halves the misses and makes the memory about 1.7 times as fast. So compare the misses, not the hits.

## The idea

**Definition.** Let $\sigma = \sigma_1 \cdots \sigma_n$ be a request sequence, $P$ a replacement policy and $k$ the cache size. Let $H_P(\sigma, k)$ be the number of hits and $M_P(\sigma, k) = n - H_P(\sigma, k)$ the number of misses. Then

$$h = \frac{H_P(\sigma, k)}{n}, \qquad m = \frac{M_P(\sigma, k)}{n} = 1 - h.$$

If request $t$ has size $s_t$ bytes, the *byte hit ratio* is $\sum_{t \text{ hit}} s_t / \sum_t s_t$. If a miss on request $t$ costs $c_t$, the cost of the misses is $\sum_{t \text{ miss}} c_t$. A policy that is best for one of these measures need not be best for another.

**Cold and warm.** A *cold-start* ratio counts from an empty cache, so it includes one compulsory miss for each distinct item. A *warm-start* ratio counts only after a warm-up part of the trace. On a short trace the two can differ a lot. Say which one you report.

**Average memory access time.** Let a hit take time $t_h$, and let a miss take an extra time $t_p$, the *miss penalty*. Each request pays $t_h$, and a miss also pays $t_p$. The mean time per request over the trace is then

$$\text{AMAT} = t_h + m \cdot t_p.$$

With $t_h = 1$ and $t_p = 100$ cycles, $m = 0.04$ gives 5 cycles and $m = 0.02$ gives 3 cycles. This is why a small change of $h$ near 1 matters.

**Two levels.** With a first-level cache in front of a second-level cache, the *local* miss ratio of the second level is its misses divided by the requests that reach it, which are the misses of the first level. The *global* miss ratio is its misses divided by all requests, so it is the product of the two local ratios. If the first level misses on 10 percent of the requests and the second level misses on 40 percent of the requests that it gets, the global miss ratio is $0.1 \times 0.4 = 0.04$. Then $\text{AMAT} = t_{h1} + m_1 (t_{h2} + m_2 \, t_p)$ with the local ratios $m_1$ and $m_2$.

**As a function of the size.** For a fixed trace and policy, $k \mapsto m(k)$ is the [miss ratio curve](/miss-ratio-curve/). For LRU and for Belady's MIN it never rises as $k$ grows, because these policies have the [inclusion property](/inclusion-property/). For FIFO it can rise, which is [Belady's anomaly](/belady-anomaly/). One pass of the [Mattson stack algorithm](/mattson-stack-algorithm/) gives the whole LRU curve.

**As a probability.** Under the [independent reference model](/independent-reference-model/), the long-run hit ratio of a policy is a probability that one can compute from the popularity of the items.

### Pitfalls

- **The mean of ratios.** A cache with 900 hits in 1,000 requests in one hour and 5 hits in 10 requests in the next has an overall hit ratio of $905/1010 \approx 0.896$. The mean of the two hourly ratios is $0.7$, which is wrong. Add the counts, then divide.
- **Hits are not time.** Use the miss ratio, or better the AMAT, to compare designs. A hit ratio of 0.99 against 0.98 is a factor of 2 in misses.
- **Requests and bytes.** A content delivery network that keeps many small objects can show a high hit ratio and a low byte hit ratio. The first number tells the latency of users; the second tells the traffic to the origin.
- **Unknown warm-up.** A short simulation from an empty cache shows mostly compulsory misses and makes all policies look alike.

## Examples

Take the trace $A\,B\,C\,A\,B\,D\,A\,B\,C\,D$ with $n = 10$ and the LRU policy.

| $k$ | misses | hit ratio | miss ratio |
|---|---|---|---|
| 1 | 10 | 0 | 1 |
| 2 | 10 | 0 | 1 |
| 3 | 6 | 0.4 | 0.6 |
| 4 | 4 | 0.6 | 0.4 |

With $k = 4$, all 4 distinct items fit, so only the 4 compulsory misses remain. With $k = 2$, each item is evicted before its next use, because two other items always come between two uses of the same item. The jump between $k = 2$ and $k = 3$ comes from the same fact: the [reuse distance](/reuse-distance/) of each repeated request here is 2 or 3.

Now give the items sizes: $A$ and $B$ have 1 byte, $C$ has 8 bytes and $D$ has 2 bytes, and keep $k = 3$ items. The 4 hits are on $A$ and $B$, which make 4 bytes of the 26 bytes requested. So the byte hit ratio is $4/26 \approx 0.15$, while the hit ratio is $0.4$.

A non-example of a useful number is the hit ratio of a trace that reads each item once, such as a scan of a large file. Each request is a compulsory miss, so $h = 0$ for every policy and size, and the ratio says nothing about the policy.

## Where it is used

- **Processor caches.** Designers compare miss ratios, or misses per thousand instructions, and convert them to time with the AMAT formula.
- **Operating systems and databases.** The page cache and the buffer pool report hit ratios to size memory, and a sharp fall in the hit ratio is a sign of thrashing, see the [working set model](/working-set-model/).
- **Web and content caches.** Operators track both the object hit ratio and the byte hit ratio, because they measure different costs.
- **Cache sizing.** A [miss ratio curve](/miss-ratio-curve/), computed exactly or by sampling with [SHARDS](/shards/), shows how much a larger cache would help.

## References
