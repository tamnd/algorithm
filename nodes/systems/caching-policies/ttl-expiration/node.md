---
tag: WFW1C7
kind: concept
slug: ttl-expiration
name: Time-to-live (TTL) expiration
aliases:
- time-based expiry
- time-to-live expiration
- sliding expiration
area: systems/caching-policies
level: intro
summary: "Each cache entry gets an expiry time and is dropped after it; an absolute TTL bounds staleness, a sliding TTL does not, and expiry runs lazily on access or by an active sweep."
prereqs: [cache]
see_also: [cache-invalidation, cache-stampede, cache-aside-pattern, lru, independent-reference-model, binary-heap, poisson-distribution]
sources:
  - paper: "Jaeyeon Jung, Arthur W. Berger and Hari Balakrishnan, Modeling TTL-based Internet Caches, IEEE INFOCOM 2003, vol. 1, 417-426, doi:10.1109/INFCOM.2003.1208693"
    title: "Jung, Berger and Balakrishnan, Modeling TTL-based Internet Caches, INFOCOM 2003"
    locator: "the hit-rate model of a single TTL cache in which a miss starts a new TTL, with request arrivals as a renewal process and DNS caches as the motivating case"
  - paper: "Hao Che, Ye Tung and Zhijun Wang, Hierarchical Web caching systems: modeling, design and experimental results, IEEE Journal on Selected Areas in Communications 20(7), 1305-1314, 2002"
    title: "Che, Tung and Wang, Hierarchical Web caching systems, IEEE JSAC 20(7), 2002"
    locator: "the analysis of an LRU cache through a characteristic time, after which an item not requested leaves the cache"
  - url: "https://redis.io/docs/latest/commands/expire/"
    title: "Redis documentation, EXPIRE command"
    locator: "Appendix: Redis expires, section How Redis expires keys (passive and active expiry), and the sections on refreshing expires and on which commands clear the timeout"
  - url: "https://www.rfc-editor.org/rfc/rfc9111"
    title: "RFC 9111, HTTP Caching, 2022"
    locator: "Section 4.2 (Freshness: freshness lifetime and age of a stored response)"
---

TTL expiration gives each [cache](/cache/) entry a lifetime $T$, the time to live. When the entry is stored at time $t$, it gets the expiry time $t + T$, and from then on the cache treats it as absent, even though nothing told the cache that the value changed. A TTL is the simplest way to bound how stale a cached value can be, and it needs no message from the owner of the data. Two choices define a TTL scheme: whether a hit moves the expiry time (absolute TTL does not, sliding TTL does), and when the cache actually frees an expired entry (lazily, when a request finds it, or actively, by a sweep). Under Poisson requests the hit probability of one key has a closed form, $\lambda T/(1+\lambda T)$ for an absolute TTL started at each miss, and $1 - e^{-\lambda T}$ for a sliding TTL.

## In plain words

When the cache stores a copy of something, it also writes down a time limit, like a best-before date on food. Before the limit, the copy is served. After the limit, the cache acts as if it never had the copy, and the next request goes to the real source and brings a fresh copy.

With a fixed limit, every copy is at most that old when it is served, no matter how busy the item is. With a sliding limit, each use pushes the date forward, so a popular copy can stay forever, and it can be very old.

The cache must also throw expired copies away to free memory. It can do this when someone asks for them, which costs nothing extra but keeps forgotten copies forever, or it can walk through its entries from time to time and remove the old ones. Real caches do both.

## The idea

### Absolute and sliding TTL

Let an entry be set at time $s$ with lifetime $T$. With an **absolute TTL** the entry is live on the interval $[s, s+T)$ and hits do not change it. With a **sliding TTL** each hit at time $t$ moves the expiry time to $t + T$, so the entry dies only after a gap of $T$ with no request.

The difference matters for staleness. Suppose the cache read the value from the store just before time $s$. With an absolute TTL, every hit is served before $s + T$, so every value that the cache returns is less than $T$ old. That is the guarantee that HTTP freshness lifetimes and DNS record TTLs give. With a sliding TTL there is no such bound: a key that is requested at least once every $T$ seconds never expires, and it serves its first value forever. A sliding TTL is a rule for freeing idle memory, such as idle sessions, not a rule for freshness. The Redis documentation describes a session pattern of this kind, where each access calls EXPIRE again to refresh the timeout.

### Hit probability under Poisson requests

Model one key whose requests form a Poisson process of rate $\lambda$, the usual [independent reference model](/independent-reference-model/) in continuous time. The cache has room for the key, so only the TTL removes it. On a miss the application loads the value and stores it with lifetime $T$.

**Absolute TTL, reset on a miss.** Call the time of a miss $\tau$. The entry is live on $[\tau, \tau + T)$. Because a Poisson process has independent increments, the requests after $\tau$ do not depend on anything before $\tau$. The requests in $(\tau, \tau+T)$ are all hits, and their number $N$ is [Poisson](/poisson-distribution/) with mean $\lambda T$. The first request at or after $\tau + T$ is a miss and starts the next cycle in the same way. So the request stream splits into independent, identically distributed cycles, each with exactly 1 miss and $N$ hits. Over $c$ cycles the fraction of hits is

$$\frac{N_1 + \cdots + N_c}{c + N_1 + \cdots + N_c} = \frac{\bar N_c}{1 + \bar N_c} \longrightarrow \frac{\lambda T}{1 + \lambda T},$$

where $\bar N_c$ is the mean of the $N_i$, which tends to $\lambda T$ by the strong law of large numbers. So the long-run hit probability is $\lambda T / (1 + \lambda T)$.

**Sliding TTL.** Every request, hit or miss, leaves the entry with expiry time equal to its own time plus $T$. So a request after the first is a hit if and only if the gap since the previous request is less than $T$. The gaps are exponential with rate $\lambda$, so the hit probability is exactly $1 - e^{-\lambda T}$ for every request after the first.

**Comparison.** With $x = \lambda T$, the sliding hit probability is never smaller: $1 - e^{-x} \ge x/(1+x)$ is the same as $e^{-x} \le 1/(1+x)$, which is $e^{x} \ge 1 + x$. A sliding TTL buys its higher hit ratio with the loss of the staleness bound.

The sliding formula also explains the Che approximation for [LRU](/lru/). In an LRU cache of $k$ items under the independent reference model, an item leaves after about the same time $T_C$ without a request, whatever the item is. If $T_C$ is the root of $\sum_i (1 - e^{-\lambda_i T_C}) = k$, item $i$ hits with probability about $1 - e^{-\lambda_i T_C}$: LRU acts like a sliding TTL cache with lifetime $T_C$. This is an approximation, not an exact result; Che, Tung and Wang introduced it for hierarchical web caches. Jung, Berger and Balakrishnan model TTL caches in which a miss starts the TTL, as in DNS, with request streams more general than Poisson.

### Lazy and active expiry

The expiry rule says when an entry is dead. A separate question is when the cache frees its memory.

- **Lazy expiry.** On each get, compare the expiry time with the clock; if it has passed, delete the entry and report a miss. This costs $O(1)$ per access and nothing else, but an expired key that nobody asks for again stays in memory forever.
- **Active expiry.** A background task removes expired entries. One exact method keeps a min-[heap](/binary-heap/) of (expiry time, key). A sweep at time $t$ pops items while the smallest expiry time is at most $t$. Each set pushes one item, in $O(\log m)$ time for $m$ items in the heap, and each removal pops one. When a key is overwritten, or a sliding TTL moves its expiry, the old heap item stays; a sequence number in each item tells the sweep to skip it, and the heap is rebuilt from the live entries when the old items grow too many.
- **Sampling.** As described in the Redis documentation, Redis uses both: a key that a client accesses after its timeout is removed then (the passive way), and Redis also periodically tests a few random keys among those with an expiry and deletes the expired ones (the active way). Random sampling needs no ordered structure, at the price of letting some expired keys stay for a while. The same documentation stores the expiry as an absolute Unix time, and commands that delete or overwrite the key, such as DEL and SET, clear it, while commands that change the value in place, such as INCR, keep it.

Both methods give the same answers to get; they differ only in memory use and in when the work is done.

### Pitfalls

- **Sliding TTL used for freshness.** It does not bound staleness, as shown above.
- **Many keys with the same TTL.** Keys loaded at the same moment expire at the same moment, and their misses arrive together at the store. Add random jitter to $T$, or see [cache stampede](/cache-stampede/) for the misses on one hot key.
- **Clock jumps.** Measure lifetimes with a monotonic clock. A wall clock that jumps forward expires everything; one that jumps back keeps entries too long.
- **The TTL as the only invalidation.** A TTL gives a staleness bound of $T$, no better. When a writer knows that a value changed, it should also delete the key, as in the [cache-aside pattern](/cache-aside-pattern/) and on the [cache invalidation](/cache-invalidation/) page.

## Examples

**Absolute against sliding.** A key is set at time 0 with $T = 10$ and then requested at times 9, 18, 27 and 37. With an absolute TTL the request at 9 hits and the entry dies at 10, so the request at 18 misses and reloads it with expiry 28; then 27 hits and 37 misses. With a sliding TTL the requests at 9, 18 and 27 hit (each gap is 9) and move the expiry to 19, 28 and 37, so the request at 37 misses. Note that the value served at time 27 was loaded before time 0.

**Lazy and active.** Keys 0 to 4 are set at time 0 with lifetimes 1 to 5. At time 3, a get of key 0 removes it lazily and reports a miss; keys 1 and 2 are also dead but still use memory. A sweep at time 3 removes keys 1 and 2 (expiry times 2 and 3, since an entry is dead when the clock reaches its expiry time), and keys 3 and 4 stay.

**Hit probabilities.** For Poisson requests:

| $\lambda T$ | absolute TTL, $\lambda T/(1+\lambda T)$ | sliding TTL, $1 - e^{-\lambda T}$ | seeded simulation, absolute | seeded simulation, sliding |
|---|---|---|---|---|
| 0.4 | 0.2857 | 0.3297 | 0.2856 | 0.3296 |
| 1 | 0.5000 | 0.6321 | 0.4993 | 0.6310 |
| 3 | 0.7500 | 0.9502 | 0.7496 | 0.9509 |

The simulation columns come from the implementation on this page with 120,000 requests per cell and the generator `random.Random(2003)`. So a key requested once per TTL on average hits half the time with an absolute TTL. To reach a hit probability $h$ with an absolute TTL, the TTL must be $T = h / (\lambda (1 - h))$: 9 mean gaps for 90 percent, 99 for 99 percent.

## Where it is used

- **DNS.** Each resource record carries a TTL in seconds, and resolvers cache the record for at most that time. Jung, Berger and Balakrishnan model this case.
- **HTTP caches.** A stored response is fresh while its age is less than its freshness lifetime, which comes from `max-age` or `Expires`, as in RFC 9111, Section 4.2.
- **Key-value caches.** Redis and memcached take a lifetime with each set; application caches use a TTL as a safety net under explicit invalidation.
- **Sessions and tokens.** Session stores use a sliding TTL to drop idle sessions; access tokens use an absolute one, so a stolen token works only for a bounded time.
- **Analysis of LRU.** The characteristic-time approximation treats an LRU cache as a TTL cache, as in the section on hit probability above.

## References
