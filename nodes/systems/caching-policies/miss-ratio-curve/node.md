---
tag: 38ZHAR
kind: concept
slug: miss-ratio-curve
name: Miss ratio curve
aliases:
- hit ratio curve
- miss rate curve
area: systems/caching-policies
level: intro
summary: "The miss ratio of one policy on one trace as a function of the cache size. For LRU and other stack algorithms it never rises; for FIFO it can."
prereqs: [cache-hit-ratio, reuse-distance]
see_also: [miss-ratio-curve-computation, mattson-stack-algorithm, shards, stack-algorithms, inclusion-property, belady-anomaly, working-set-model, multilevel-caching]
sources:
  - paper: doi:10.1147/sj.92.0078
    title: "R. L. Mattson, J. Gecsei, D. R. Slutz and I. L. Traiger, Evaluation techniques for storage hierarchies, IBM Systems Journal 9(2) (1970), 78-117"
    locator: the success function of a stack algorithm for all capacities in one pass, and the inclusion property that makes it non-increasing
  - paper: doi:10.1109/HPCA.2015.7056022
    title: "Nathan Beckmann and Daniel Sanchez, Talus: A simple way to remove cliffs in cache performance, HPCA 2015, 64-75"
    locator: "Section IV, Theorem 4 (sampling a fraction of the accesses scales the curve), the shadow partitions of Equation (2), and the convex hull of the miss curve"
  - paper: "Carl A. Waldspurger, Nohhyun Park, Alexander Garthwaite and Irfan Ahmad, Efficient MRC construction with SHARDS, 13th USENIX Conference on File and Storage Technologies (FAST 15), 2015, 95-110"
    title: "Waldspurger, Park, Garthwaite and Ahmad, Efficient MRC construction with SHARDS, FAST 2015"
    locator: Section 1, the uses of miss ratio curves for cache sizing and partitioning in storage systems
  - paper: doi:10.1145/363011.363155
    title: "L. A. Belady, R. A. Nelson and G. S. Shedler, An anomaly in space-time characteristics of certain programs running in a paging machine, Communications of the ACM 12(6) (1969), 349-353"
    locator: the FIFO trace on which a larger memory has more page faults
---

A miss ratio curve (MRC) gives, for one trace and one replacement policy, the miss ratio $m(c)$ of a cache of each size $c$. It shows at a glance how much a larger cache helps. For [LRU](/lru/) and the other [stack algorithms](/stack-algorithms/) the curve never rises, and one pass over the trace gives the whole curve. For [FIFO](/fifo-replacement/) the curve can rise, which is [Belady's anomaly](/belady-anomaly/). Systems use these curves to choose cache sizes and to divide one cache among many users.

## In plain words

Run the same list of requests through a cache of size 1, then of size 2, then 3, and so on, and write down the fraction of misses each time. Draw these numbers against the size. That drawing is the miss ratio curve.

The curve starts at 1 for a cache of size 0, because each request misses. When the cache can hold every item that the trace uses, only the first request for each item misses, and the curve stays flat from there on. Between these two ends, the curve can fall slowly, or stay flat for a long time and then drop all at once. A sudden drop means that a group of items that is used again and again now fits in the cache.

## The idea

**Definition.** Fix a trace $\sigma_1 \cdots \sigma_n$ and a policy $P$. Let $M_P(c)$ be the number of misses of $P$ with a cache of size $c$, starting empty. The miss ratio curve is $m(c) = M_P(c)/n$ for $c = 0, 1, 2, \ldots$, and the hit ratio curve is $1 - m(c)$. With objects of different sizes, $c$ is a number of bytes, and the byte miss ratio gives a second curve (see [cache hit ratio](/cache-hit-ratio/)).

Two points are fixed. $m(0) = 1$. For each $c$ at least the number $d$ of distinct items, $m(c) = d/n$: only the cold misses remain, the compulsory misses of the [three Cs](/three-cs-model/). The policy decides the shape in between.

**LRU and reuse distance.** An LRU cache of size $c$ hits a request exactly when its [reuse distance](/reuse-distance/), the number of distinct other items since the last use, is less than $c$. So, with $h(d)$ the number of requests with distance $d$,

$$m(c) = 1 - \frac{1}{n} \sum_{d < c} h(d).$$

The curve is one minus the cumulative histogram of reuse distances. This is why one pass over the trace, the [Mattson stack algorithm](/mattson-stack-algorithm/), gives the curve for all sizes at once. Faster methods and approximate ones are on the [MRC computation](/miss-ratio-curve-computation/) page.

**Monotone curves.** A policy has the [inclusion property](/inclusion-property/) when, on each trace and at each time, the content of the cache of size $c$ is a subset of the content of the cache of size $c + 1$. Then each hit at size $c$ is also a hit at size $c + 1$, so $m(c + 1) \le m(c)$. LRU, Belady's MIN and an LFU that counts all past requests have this property; an LFU that forgets the counts of evicted items does not (on $a\,a\,b\,c\,b\,c\,d\,a\,d\,a$ it has 6 misses with 2 slots and 7 with 3). FIFO and [CLOCK](/clock/) do not, and their curves can rise at some sizes.

**Cliffs and plateaus.** The curve need not be convex. A loop over $N$ items under LRU has $m(c) = 1$ for each $c < N$ and drops to the cold miss ratio at $c = N$. Real traces mix several working sets, and each set that starts to fit makes a drop. Between drops, extra space gives almost nothing.

**The convex hull.** Beckmann and Sanchez showed with Talus (2015) that a cache can reach each point of the lower [convex hull](/convex-hull/) of its curve. Their Theorem 4 says that a cache that sees only a fraction $\rho$ of the accesses, chosen by a hash of the address, and has size $s'$, has the miss curve $\rho\, m(s'/\rho)$; it behaves like a cache of size $s'/\rho$ on the full stream. Take two points $\alpha < s < \beta$ of the hull. Split the cache into two shadow partitions: the first gets the fraction $\rho = (\beta - s)/(\beta - \alpha)$ of the stream and the size $\rho \alpha$, the second gets the rest of the stream and the size $s - \rho\alpha$. The first behaves like a cache of size $\alpha$, the second like one of size $\beta$, and the total miss ratio is

$$\rho\, m(\alpha) + (1 - \rho)\, m(\beta),$$

the straight line between the two hull points. The result needs three assumptions of the paper: the curve is stable over time, the miss ratio depends only on the size, and a sample of the accesses by address behaves like the full stream at a smaller scale.

## Examples

**LRU and FIFO on Belady's trace.** The trace is $1\,2\,3\,4\,1\,2\,5\,1\,2\,3\,4\,5$, with $n = 12$ and $5$ distinct items.

| size $c$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| LRU misses | 12 | 12 | 12 | 10 | 8 | 5 |
| LRU $m(c)$ | 1 | 1 | 1 | 0.833 | 0.667 | 0.417 |
| FIFO misses | 12 | 12 | 12 | 9 | 10 | 5 |
| FIFO $m(c)$ | 1 | 1 | 1 | 0.75 | 0.833 | 0.417 |

The reuse distances are $-, -, -, -, 3, 3, -, 2, 2, 4, 4, 4$, where $-$ marks a first use. Two requests have distance 2, so the LRU curve falls by $2/12$ from $c = 2$ to $c = 3$. Two more have distance 3, and three have distance 4. The FIFO curve rises from $9/12$ to $10/12$ between $c = 3$ and $c = 4$. At $c = 3$ FIFO is better than LRU on this trace, so neither curve lies below the other everywhere.

**A cliff.** A loop over 8 items, repeated 10 times, gives 80 requests. LRU has $m(c) = 1$ for $c \le 7$, and $m(8) = 8/80 = 0.1$. The lower convex hull is the straight line from $(0, 1)$ to $(8, 0.1)$, so Talus could give $m = 0.55$ at $c = 4$. In the same way, for a loop over 100 items and a cache of 50, one LRU cache misses each time. Talus with $\alpha = 0$ and $\beta = 100$ sends half of the items to a partition of size 0 and the other half to a partition of size 50. The second partition then holds its whole loop, and the miss ratio over 40 rounds falls from 1 to $(2000 + 50)/4000 \approx 0.51$.

## Where it is used

- **Cache sizing.** The curve shows the smallest size that meets a target miss ratio, and how much each extra unit of space buys. A flat part of the curve means that more space is wasted there.
- **Partitioning.** Several programs, tenants or virtual machines share one cache. Given a curve per user, a greedy rule or a dynamic program gives each user space where its curve falls fastest. Hardware does this for shared last-level caches, and storage systems for shared flash and memory caches; the SHARDS paper lists both uses.
- **Removing cliffs.** Talus uses the curve to choose $\alpha$, $\beta$ and $\rho$, and so turns a curve with cliffs into its convex hull. Convex curves also make the greedy partitioning rule optimal.
- **Comparing policies.** Two policies are compared across all sizes, not at one size that may hide a cliff. The curve of [Belady's MIN](/belady-optimal/) lies below the curve of each other policy that loads only on a miss, on the same trace.
- **Models of a hierarchy.** The miss ratio of each level of a [multilevel cache](/multilevel-caching/) at its size goes into the average access time.

## References
