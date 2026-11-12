---
tag: A6YSHQ
kind: concept
slug: load-skew
name: Load skew
aliases:
- hot spot
area: systems/load-balancing-and-hashing
level: intro
summary: Uneven request load in an online service, where a few keys or servers receive much more traffic than the mean. Even a perfect hash spreads keys, not requests, so popular keys make hot servers.
prereqs: [hash-partitioning, load-balancing-problem]
see_also: [data-skew, bounded-load-consistent-hashing, power-of-two-choices, range-partitioning, frequent-items-problem, space-saving, cache-hit-ratio, load-shedding]
sources:
  - paper: doi:10.1145/258533.258660
    title: David Karger, Eric Lehman, Tom Leighton, Rina Panigrahy, Matthew Levine and Daniel Lewin, Consistent hashing and random trees, distributed caching protocols for relieving hot spots on the World Wide Web, STOC 1997
    locator: pages 654 to 663, the introduction (a popular page swamps the server that holds it, and caches must spread the load)
  - paper: doi:10.1109/INFCOM.1999.749260
    title: Lee Breslau, Pei Cao, Li Fan, Graham Phillips and Scott Shenker, Web caching and Zipf-like distributions, evidence and implications, IEEE INFOCOM 1999
    locator: pages 126 to 134, the Zipf-like popularity of requested pages in proxy traces
  - paper: doi:10.1145/2038916.2038939
    title: Bin Fan, Hyeontaek Lim, David G. Andersen and Michael Kaminsky, Small cache, big effect, provable load balancing for randomly partitioned cluster services, ACM Symposium on Cloud Computing (SoCC) 2011
    locator: "Section 4, Analysis: a front-end cache of the c most popular items, with c of order n log n for n back-end nodes, balances the back ends under any query distribution"
  - book: isbn:9781449373320
    title: Martin Kleppmann, Designing Data-Intensive Applications, O'Reilly, 2017
    locator: "Chapter 6, Partitioning: skewed workloads and relieving hot spots (the celebrity key, and a random two-digit suffix that splits one key over 100 keys)"
---

Load skew is the state of a running service where the request load is far from even over its servers: a few servers, or the few keys they hold, receive much more traffic than the mean. The usual measure is the peak-to-mean ratio $\max_i L_i / \bar{L}$, where $L_i$ is the request rate at server $i$ and $\bar{L}$ is the mean over the $n$ servers. A server whose rate exceeds its capacity builds a queue, and its latency, not the mean, sets the latency of the service. The page on [data skew](/data-skew/) covers the batch form of the same issue, where the input of a MapReduce job is fixed and an overloaded reducer delays the end of the job. Load skew is about online traffic: the demand changes all the time and must be served as it arrives.

## In plain words

A store spreads its products over several shelves so that each shelf holds the same number of products. Then one product goes on sale, and everybody crowds in front of the shelf that holds it, while the other shelves are quiet. The shelves are balanced by product count but not by people.

A service with many servers has the same problem. A good hash puts the same number of keys on every server, but some keys are asked for far more than others, so the server that holds them gets far more work. The fix is not a better hash. It is to treat the few hot keys differently: keep copies of them close to the users, spread them over more servers, or send their requests where there is room.

## The idea

**Keys versus requests.** Hash or range placement balances keys. With $m$ keys of equal popularity on $n$ servers, the busiest server has close to $m/n$ keys and close to the mean load; see [balls into bins](/balls-into-bins-max-load/). Popularity in real workloads is far from equal. Request traces of web proxies follow a Zipf-like law (Breslau et al. 1999): the $i$-th most popular item gets a share proportional to $1/i^{s}$, with $s$ a little below 1 in their traces. Then the most popular key alone can carry several times the mean load of a server, and no placement of whole keys can fix that. If one key has the share $p_1$ of all requests and keys are not split, then the peak-to-mean ratio is at least $n p_1$.

**Sources of skew.**

- **Popular keys.** A celebrity account, a front page, a viral video, a hot product. This is the main source in caches and key-value stores.
- **Coarse keys.** A key that stands for many users: one NAT address under [source IP hashing](/source-ip-hash/), one tenant ID, one /24 prefix.
- **Placement imbalance.** The hash itself can give unequal shares, as with [consistent hashing](/consistent-hashing/) and one point per server, where the largest arc is about $\ln n$ times the mean.
- **Order of writes.** Under [range partitioning](/range-partitioning/), keys that grow over time, such as timestamps, send every insert to the last partition.
- **Time.** Flash crowds, the daily cycle, and a key that is hot for one hour and cold the next. A skew that moves is harder to fix than a fixed one.
- **Unequal costs.** Requests of different cost, and servers of different speed, give unequal load even with equal counts.

**Remedies.** Each one acts on a different part of the problem.

- **Cache the hot keys in front.** A small cache in front of the servers takes the most popular keys out of the back-end load. Fan et al. (2011) prove that a cache of the $c$ most popular items, with $c$ of order $n \log n$, keeps the $n$ back ends balanced under any query distribution, because the requests that miss the cache are spread over many keys of small share. The cache size depends on $n$, not on the number of items.
- **Replicate hot keys.** Store a hot key on $r$ servers and spread its reads over them, which divides its load by $r$. Writes must then go to all copies.
- **Split a hot key.** Add a small random suffix to the key, so that its writes spread over several keys, and read all of them to answer a query. Kleppmann gives the example of a two-digit suffix that spreads one key over 100 keys.
- **Split a hot range.** Split a range partition by load, not by size, and move the hot part to its own server.
- **Route by load.** If a request may go to any of several servers, send it to the less loaded one: [the power of two choices](/power-of-two-choices/), or a hash with a load cap such as [bounded-load consistent hashing](/bounded-load-consistent-hashing/), which moves keys from a full server to the next one with room.
- **Find the hot keys.** All these remedies need to know which keys are hot now. Streaming summaries such as [Space-Saving](/space-saving/) and the [Count-Min sketch](/count-min-sketch/) find them in small memory; see the [frequent items problem](/frequent-items-problem/).
- **Shed load.** When nothing else helps in time, a server rejects or delays a part of its requests; see [load shedding](/load-shedding/).

**How it differs from data skew.** In a batch job, the whole input is known before the reduce phase starts, the cost is the time of the slowest reducer, and the fixes act once: sample the key counts, then split heavy keys or use a combiner. In an online service, the demand is a rate that changes; the cost is the queue, the latency and the errors at the hot server; and the fixes must act all the time, with caches, replicas and load-aware routing. The two pages share the root cause, few keys with much weight, and some tools, such as salting and finding the heavy keys.

## Examples

**Zipf traffic on 100 servers.** Take $m = 1{,}000{,}000$ keys, place them on $n = 100$ servers by a 64-bit BLAKE2b hash, and let key $i$ have the request share $p_i \propto 1/i^{s}$. The table gives the load of the busiest server divided by the mean, computed exactly from the shares:

| exponent $s$ | share of the top key | share of the top 100 keys | peak-to-mean |
|---|---|---|---|
| 0 (uniform) | 0.0001% | 0.01% | 1.02 |
| 0.8 | 1.34% | 10.9% | 2.30 |
| 1.0 | 6.95% | 36.0% | 7.83 |
| 1.2 | 18.95% | 68.3% | 19.61 |

The keys are balanced in all four rows; only the popularity changes. With $s = 1$, one server takes almost 8 times its share. A sample of 1,000,000 requests drawn with $s = 1$ (seed 3) shows the same picture: the busiest server gets 78,033 requests against a mean of 10,000, and the least busy one gets 5,201.

**A front-end cache.** With $s = 1$, put a cache of the $c$ most popular keys in front of the same 100 servers, and measure the peak-to-mean of the requests that miss it:

| cache size $c$ | requests served by the cache | back-end peak-to-mean |
|---|---|---|
| 10 | 20.4% | 2.10 |
| 100 | 36.0% | 1.46 |
| 1,000 | 52.0% | 1.10 |
| 10,000 | 68.0% | 1.05 |

A cache of 1,000 entries, out of a million keys, brings the back ends within 10% of each other. This is of the order $n \ln n \approx 460$ that the Fan et al. bound predicts.

**Replicating only the top key is not enough.** With $s = 1$, spread the reads of the top key over 4 servers. The peak-to-mean falls from 7.83 to 4.41, and stays at 4.41 with 16 copies, because the second key alone has 3.5% of the requests, 3.5 times the mean of a server. Skew under a Zipf law is a property of many keys, not one.

## Where it is used

- **Caches and key-value stores.** Memcached and Redis fleets, where a single hot key can saturate one node; client-side caches and replicated hot keys are the common fixes.
- **Sharded databases.** The choice of a shard key is mostly a choice about skew; see [sharding](/sharding/), [hash partitioning](/hash-partitioning/) and range partitioning.
- **Content delivery.** The consistent hashing paper of Karger et al. (1997) starts from hot spots on the web: a popular page swamps the server that holds it, and a set of caches must share the load.
- **Load balancers.** Affinity rules, such as [sticky sessions](/sticky-sessions/) and source IP hash, trade balance for locality and so create skew when some clients are heavier than others.
- **Stream processing.** A keyed operator in a streaming job sees the same issue as a reducer, but as a rate; operators that split hot keys, or route them with two choices, follow the remedies above.

## References
