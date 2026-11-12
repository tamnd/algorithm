---
tag: WMTKQ5
kind: concept
slug: cache-stampede
name: Cache stampede
aliases:
- dogpile effect
- cache miss storm
area: systems/caching-policies
level: advanced
summary: "When a hot key expires, every request in the recompute window misses and recomputes; locks and leases cut the herd to one, and probabilistic early expiration (XFetch) shrinks it."
prereqs: [ttl-expiration, cache-aside-pattern]
see_also: [cache-invalidation, mutex, load-shedding, rate-limiter, exponential-backoff, admission-control, inverse-transform-sampling]
sources:
  - paper: "Andrea Vattani, Flavio Chierichetti and Keegan Lowenstein, Optimal Probabilistic Cache Stampede Prevention, Proceedings of the VLDB Endowment 8(8), 886-897, 2015, doi:10.14778/2757807.2757813"
    title: "Vattani, Chierichetti and Lowenstein, Optimal Probabilistic Cache Stampede Prevention, PVLDB 8(8), 2015"
    locator: "Section 1 (external recomputation, locking, probabilistic early expiration), Section 2 (the model), Theorems 6 to 8, and Section 5 with Figure 3, p. 891 (the XFetch pseudocode)"
  - paper: "Rajesh Nishtala, Hans Fugal, Steven Grimm, Marc Kwiatkowski, Herman Lee, Harry C. Li, Ryan McElroy, Mike Paleczny, Daniel Peek, Paul Saab, David Stafford, Tony Tung and Venkateshwaran Venkataramani, Scaling Memcache at Facebook, 10th USENIX Symposium on Networked Systems Design and Implementation (NSDI 2013), 385-398"
    title: "Nishtala et al., Scaling Memcache at Facebook, NSDI 2013"
    locator: "Section 3.2.1, p. 388 (leases against thundering herds: one token per key every 10 seconds by default, other clients wait and retry)"
  - url: "https://www.rfc-editor.org/rfc/rfc5861"
    title: "RFC 5861, HTTP Cache-Control Extensions for Stale Content, 2010"
    locator: "Section 3 (the stale-while-revalidate extension)"
---

A cache stampede happens when a hot key leaves the [cache](/cache/), by [TTL expiration](/ttl-expiration/) or by eviction, and the value takes a while to recompute. Under the [cache-aside pattern](/cache-aside-pattern/) every request that arrives during the recompute misses and starts the same expensive recompute, so a key that gets $r$ requests per second and needs $\Delta$ seconds to rebuild sends about $r\Delta$ copies of the same query to the store at once. The extra load can slow the store, which makes $\Delta$ longer and the herd larger. The fixes make one request do the work: a lock or single flight, so that only one recompute runs; a lease from the cache, which gives the right to recompute to one client; and probabilistic early expiration, where each request recomputes a little before the expiry with a probability that grows as the expiry comes near. The last one, XFetch, needs no coordination at all and is optimal in a precise sense.

## In plain words

A popular page is built from a slow database query, and the result is kept in a cache for five minutes. When the five minutes end, the next request finds nothing and runs the query, which takes a second. During that second, a thousand more requests come in, and each one also finds nothing and runs the same query. The database now gets a thousand identical slow queries at the same moment.

There are three ways out. Let the first request take a lock, and make the others wait or use the old copy. Let the cache itself pick one client to do the work and tell the others to wait. Or let each request, shortly before the copy ends, flip a weighted coin and refresh it early; the coin is weighted so that usually exactly one request refreshes, before anyone sees a miss.

## The idea

### The model

One key holds a value that expires at time $E$ and takes $\Delta$ time units to recompute. A recompute that starts at time $s$ writes the new value at time $s + \Delta$. Until then the old entry is the only one in the cache. The stampede size is the number of recomputes that start before the first one finishes: all of them do the same work, and only one is needed.

With plain cache-aside, the stampede size is the number of requests in $[E, E + \Delta)$. For requests in a Poisson stream of rate $r$, that is the first request after $E$ plus a Poisson number with mean $r\Delta$ in the next $\Delta$ units, so the expected size is $1 + r\Delta$. Vattani, Chierichetti and Lowenstein use a model of the same kind: in their units a recompute takes 1 time unit, and requests arrive with independent gaps of mean $1/n$, so the plain stampede grows linearly in $n$.

### Fix 1: a lock or single flight

The first request that misses takes a lock for the key, recomputes, writes the value and releases the lock. A request that misses while the lock is held does not recompute; it waits for the value, or it returns the old value if the cache kept one. In one process, this is single flight: a map from key to the recompute in progress, guarded by a [mutex](/mutex/), and the waiters share its result. Across many servers, the lock is a key in the cache itself, created by an add that succeeds only if the key is absent.

The costs: waiting requests see a latency of up to $\Delta$; a lock holder that crashes blocks the key, so the lock key needs its own TTL; and a per-process single flight still lets each of $N$ servers recompute once, so the store sees up to $N$ recomputes. If the cache keeps the old value for a grace period, the waiters can be served the old value at once. In HTTP this is the stale-while-revalidate extension of RFC 5861: a cache may serve a stale response for a given time while it revalidates it in the background.

### Fix 2: leases

In the memcache system of Nishtala and others, a miss returns a lease token, and the cache gives out at most one token per key every 10 seconds by default. A client that misses while a token is out gets a reply that tells it to wait a short time and retry, and usually the token holder has set the value by then. This is a lock that lives in the cache, with a built-in timeout, and the same token also rejects stale sets. The [cache invalidation](/cache-invalidation/) page describes the mechanism.

### Fix 3: probabilistic early expiration (XFetch)

Locks and leases still let the key expire: the first request after the expiry pays the full $\Delta$. Probabilistic early expiration recomputes before the expiry, so in the usual case no request ever misses. The cache stores the recompute time $\Delta$ next to the value, and each request decides on its own whether to recompute now.

```pseudo id=main
XFETCH(key, ttl, β)
L1  value, Δ, expiry ← CACHE-READ(key)
L2  if value is missing or TIME() − Δ·β·ln(RAND()) ≥ expiry then
L3      start ← TIME()
L4      value ← RECOMPUTE(key)
L5      Δ ← TIME() − start
L6      CACHE-WRITE(key, (value, Δ), ttl)
L7  return value
```

Here RAND() is uniform on $(0, 1]$, so $-\ln(\text{RAND}())$ is exponential with mean 1, by [inverse transform sampling](/inverse-transform-sampling/), and line L2 adds a random head start with mean $\Delta\beta$ to the clock. The parameter $\beta > 0$ sets how early; $\beta = 1$ is the default in the paper, a larger $\beta$ recomputes earlier, and $\beta = 0$ never recomputes early. A request at time $t < E$ triggers if and only if the head start is at least $E - t$:

$$P(\text{trigger at } t) = P\left(\text{RAND}() \le e^{-(E-t)/(\Delta\beta)}\right) = e^{-(E-t)/(\Delta\beta)}.$$

So a request $\Delta\beta$ before the expiry triggers with probability $e^{-1} \approx 0.37$, and one $3\Delta\beta$ before with $e^{-3} \approx 0.05$. The rule scales with $\Delta$: a key that is expensive to rebuild starts its refresh earlier.

**Exact expected stampede size.** Let the requests come at fixed times $t_1 < t_2 < \cdots$ and let $p_j$ be the trigger probability of request $j$ as above, with $p_j = 1$ for $t_j \ge E$. Each request draws its own random number, so the decisions are independent until the first recompute finishes. Request $i$ starts the first recompute with probability $p_i \prod_{j<i}(1 - p_j)$. After that, the old entry stays until $t_i + \Delta$, so each later request $j$ with $t_j < t_i + \Delta$ still recomputes with probability $p_j$. By [linearity of expectation](/linearity-of-expectation/),

$$\mathbb{E}[S] = \sum_i p_i \prod_{j<i}(1 - p_j)\left(1 + \sum_{j > i,\ t_j < t_i + \Delta} p_j\right).$$

The implementation computes this sum and checks it against a seeded simulation of the policy, and against a brute-force sum over all outcomes of the coin flips on a small case.

**Why the exponential distribution.** Vattani and others compare distributions for the head start in terms of two quantities: the expected stampede size and how early the recompute happens. In their model, with request rate $n$:

- **Theorem 6.** A uniform head start on $[0, \xi]$, the rule of some earlier libraries, has an expected stampede that grows like $n/\xi$, so it does not stay bounded as $n$ grows unless the head start grows linearly with $n$.
- **Theorem 7.** An exponential head start with rate $\lambda$ gives an expected stampede size bounded by a constant that depends on $\lambda$ only, $(e^{\lambda} - 1)(1/\lambda + 1/e)$, while recomputing at most about $(1/\lambda)\log n$ time units early.
- **Theorem 8.** No distribution that does not depend on $n$ and recomputes at most about $(1/\lambda)\log n$ early can have an expected stampede below $e^{\Omega(\lambda)}$. So the exponential rule is optimal up to constants.

The intuition: the chance that a request triggers depends only on the time left, $E - t$, so the process needs no knowledge of the request rate. When requests are frequent, someone triggers far from the expiry, and the few other requests in that request's window of length $\Delta$ have small trigger probabilities. When requests are rare, the refresh simply happens nearer to the expiry.

### Pitfalls

- **Cold keys and evictions.** XFetch needs a cached value to start from. An empty cache, a new key or an eviction by [LRU](/lru/) before the expiry still produces a herd; combine XFetch with a lock or a lease for these cases.
- **Many keys with the same expiry.** Keys loaded together expire together. That is a different stampede, over many keys, and the fix is random jitter on each TTL.
- **ln(0).** RAND() must not return 0. Use $1 - u$ for a generator that returns $u$ in $[0, 1)$.
- **A lock without a timeout.** A crashed holder stops all refreshes of the key.
- **Retry storms.** Waiting clients that retry at fixed short intervals are a herd of their own; use [exponential backoff](/exponential-backoff/) with jitter, or [load shedding](/load-shedding/) at the store.

## Examples

**One fixed scenario.** Requests come every 0.25 time units from time 0 to 14.75, the cached value expires at $E = 10$, and a recompute takes $\Delta = 1$.

| policy | expected stampede size | probability of a refresh before $E$ |
|---|---|---|
| plain cache-aside | 4 (recomputes at 10, 10.25, 10.5 and 10.75) | 0 |
| lock or single flight | 1 | 0 |
| XFetch, $\beta = 0$ | 4 | 0 |
| XFetch, $\beta = 0.5$ | 3.0715 | 0.8651 |
| XFetch, $\beta = 1$ | 2.0657 | 0.9930 |
| XFetch, $\beta = 2$ | 1.4779 | 1.0000 |

The XFetch values are exact, from the formula above; a simulation with 20,000 seeded runs per row agrees within 4 standard errors. With $\beta = 1$, the requests at times 7, 8, 9, 9.5 and 9.75 trigger with probability 0.0498, 0.1353, 0.3679, 0.6065 and 0.7788. So the refresh almost always starts before the expiry, and no request sees a miss, but the three requests that follow the first trigger inside its window of length 1 have high trigger probabilities, which is why the expected size is still about 2. A larger $\beta$ moves the refresh earlier, where the trigger probabilities in the window are small, and the expected size falls toward 1. The price is a shorter useful life for each value: the expected time from the first recompute to the expiry, $\sum_i p_i \prod_{j<i}(1-p_j)(E - t_i)$, is 0.70, 2.02 and 5.02 time units for $\beta = 0.5$, 1 and 2.

**XFetch with a simulated clock.** A recompute costs 2 time units and the TTL is 10. The first call at time 0 recomputes, measures $\Delta = 2$, and writes the value with expiry 12. With $\beta = 1$, a call at time 10 recomputes with probability $e^{-2/2} = e^{-1}$, which the tests check over 4,000 seeded calls.

## Where it is used

- **Memcache at Facebook.** Leases limit each key to one token every 10 seconds; the paper reports that this cut the peak rate of database queries from 17,000 to 1,300 per second.
- **Single flight in libraries.** The Go package `golang.org/x/sync/singleflight` merges concurrent calls for the same key in one process; reverse proxies such as nginx have a cache lock that lets one request fill a cache entry while others wait.
- **HTTP caches.** The stale-while-revalidate directive of RFC 5861 lets a cache serve the old response while one background request revalidates it.
- **Application caches.** XFetch is a few lines on top of any key-value cache with TTLs, because it needs only the stored $\Delta$, the expiry time and a random number.

## References
