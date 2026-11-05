---
tag: QGVXGV
kind: concept
slug: primary-clustering
name: Primary clustering
area: searching/hashing-search
level: core
summary: Runs of occupied slots that grow and merge under linear probing.
prereqs: [linear-probing, open-addressing, probe-sequence, load-factor]
see_also: [secondary-clustering, linear-probing-analysis, open-addressing-expected-probes, quadratic-probing, double-hashing, robin-hood-hashing, k-wise-independent-hashing, tabulation-hashing]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 11.4 (Open addressing), the discussion of linear probing and primary clustering
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.4 (Hashing), linear probing, its analysis, and the comparison with uniform probing
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.4 (Hash tables), linear probing and its clusters
---

Primary clustering is the tendency of [linear probing](/linear-probing/) to build long runs of occupied slots. A key whose home slot falls anywhere in a run is placed at the end of the run, so a long run catches more new keys than a short one and grows faster, and two runs merge when the gap between them fills. As a result, the expected cost of a failed search under linear probing grows like $1/(1-\alpha)^2$ in the [load factor](/load-factor/) $\alpha$, against $1/(1-\alpha)$ for a probing scheme without clusters. The name separates it from [secondary clustering](/secondary-clustering/), the weaker effect of keys that share a whole probe sequence.

## In plain words

Picture cars parking along a one-way street. Each driver goes to a chosen spot and, if it is taken, drives forward to the next free one. A row of parked cars is a trap: every driver whose spot is anywhere in the row ends up just after it, so the row gets longer. Longer rows trap more drivers, and two rows join into one when the gap between them closes.

Now a driver who looks for a free spot must walk past the whole row. When the street is half full the rows are short. When it is mostly full, a few long rows hold most of the cars, and a search walks much farther than the share of free spots would suggest. That growth of rows is primary clustering.

## The idea

**Runs.** In a table of $m$ slots, arranged in a circle, a *run* (or *cluster*) is a maximal block of consecutive occupied slots. Under linear probing, a key $k$ with home slot $h(k)$ is stored at the first free slot of $h(k), h(k) + 1, h(k) + 2, \ldots$ (modulo $m$). A search for $k$ probes the same slots. So a failed search that starts at slot $s$ makes $1 + r$ probes, where $r$ is the number of occupied slots from $s$ to the end of the run that contains $s$, or $r = 0$ if $s$ is free.

**Why runs grow.** Let a run occupy $i$ slots, with free slots $b$ just before it and $a$ just after it. A new key with a uniform home slot joins the run in two ways:

- its home slot is one of the $i$ slots of the run or the slot $a$, and it is stored at $a$, with probability $(i + 1)/m$;
- its home slot is $b$, and it is stored at $b$, with probability $1/m$.

So the run grows with probability $(i + 2)/m$, which increases with $i$. In particular the free slot $a$ that follows a run of $i$ slots is filled next with probability $(i+1)/m$, while a free slot that follows another free slot is filled next with probability $1/m$. This is the form of the argument in CLRS. When $a$ or $b$ is filled and the slot beyond it is the start or end of another run, the two runs merge into one, and the new run is longer than the sum of the two by one slot.

**The rich get richer.** The growth probability grows with the length, so the distribution of run lengths has a long tail. Under a scheme without this feedback, such as uniform probing, the free slots form a random subset and the run that a search meets is short; its expected cost is $1/(1-\alpha)$, as proved on the [expected probes](/open-addressing-expected-probes/) page. Under linear probing, Knuth's formulas give
$$\text{unsuccessful search} \approx \frac{1}{2}\left(1 + \frac{1}{(1-\alpha)^2}\right), \qquad \text{successful search} \approx \frac{1}{2}\left(1 + \frac{1}{1-\alpha}\right),$$
proved on the [linear probing analysis](/linear-probing-analysis/) page. The square in the first formula is the cost of clustering. At $\alpha = 1/2$ it is 2.5 probes against 2. At $\alpha = 0.9$ it is 50.5 against 10.

**Clustering is the price of locality.** The same property that makes runs grow makes linear probing fast on real machines: the probes of a search read consecutive slots, often in one cache line. See [locality of reference](/locality-of-reference/). For loads up to about $1/2$ or $2/3$, the extra probes cost less than the cache misses that a scattered scheme would pay. This is why linear probing remains a common choice despite primary clustering.

**It depends on the hash function too.** The formulas above assume that the home slots are independent and uniform. With weak hash functions, the clustering can be much worse: linear probing with a hash function that is only pairwise independent can have expected cost $\Theta(\log n)$ per operation, while 5-wise independence is enough for constant expected cost at a load bounded below 1. [Tabulation hashing](/tabulation-hashing/) also gives constant expected cost. See [k-wise independent hashing](/k-wise-independent-hashing/).

## Examples

**A small trace.** Let $m = 10$ and $h(k) = k \bmod 10$. Insert 12, 13, 22, 33 and 14 in this order.

| key | home slot | probes | stored at | runs after the insert |
|---|---|---|---|---|
| 12 | 2 | 2 | 2 | [2] |
| 13 | 3 | 3 | 3 | [2..3] |
| 22 | 2 | 2, 3, 4 | 4 | [2..4] |
| 33 | 3 | 3, 4, 5 | 5 | [2..5] |
| 14 | 4 | 4, 5, 6 | 6 | [2..6] |

The keys have only three distinct home slots, 2, 3 and 4, but they form one run of 5 slots. The next key joins this run with probability $7/10$: it lands at slot 7 if its home is one of slots 2 to 7, and at slot 1 if its home is slot 1. A failed search with home slot 2 now makes 6 probes. With home slot 8 it makes 1 probe.

**Merging.** Continue the trace with 18 and 17. Key 18 goes to slot 8. Key 17 finds slot 7 free and takes it, which fills the gap between the runs [2..6] and [8], so the table now has one run [2..8] of 7 slots, and a failed search with home slot 2 makes 8 probes.

**A measurement.** In tables of $m = 1000$ slots with $n = 750$ keys whose home slots are uniform (20 tables, random seed 7), linear probing gave an average failed-search cost of 8.16 probes over all start slots, near the formula value 8.5, with on average 133 runs, a mean run length of 5.6 and a longest run of 59.5. When the same number of keys was put into uniformly random distinct slots, with no clustering, a linear scan from each start slot cost 3.94 probes on average, near $1/(1-\alpha) = 4$, with 186 runs, a mean run length of 4.0 and a longest run of 21.4. The load is the same in both cases; the difference is clustering alone.

**Non-example: quadratic probing.** [Quadratic probing](/quadratic-probing/) tries the slots $h(k) + c_1 i + c_2 i^2$. Two keys with different home slots follow different jumps, so a key that hits a run does not just go to its end, and runs do not trap keys in the same way. It still has secondary clustering: keys with the same home slot share all their probes.

## Where it is used

- **Choosing a probing scheme.** Primary clustering is the main reason to prefer [double hashing](/double-hashing/) or quadratic probing at high loads, and linear probing with a resize threshold at moderate loads.
- **Resize thresholds.** Linear-probing tables usually grow at a load of about $1/2$ to $3/4$, because the $1/(1-\alpha)^2$ term grows fast beyond it.
- **Variants that live with clusters.** [Robin Hood hashing](/robin-hood-hashing/) keeps the keys of a run sorted by home slot, which lowers the variance of the search cost and lets a failed search stop early, but leaves the runs themselves as they are. [Hopscotch hashing](/hopscotch-hashing/) keeps each key within a fixed distance of its home slot. The [Swiss table](/swiss-table/) probes groups of slots with vector instructions, so a run costs one probe per group.
- **Deletions.** In a clustered table, [lazy deletion](/lazy-deletion/) with [tombstones](/tombstone/) keeps runs long after their keys are gone. Linear probing allows a deletion that moves later keys of the run back instead, which shortens the run.
- **Analysis.** The run structure of linear probing is the subject of Knuth's analysis and of the study of linear probing with limited independence.

## References
