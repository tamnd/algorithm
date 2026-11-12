---
tag: 08G7GS
kind: problem
slug: rate-limiting-problem
name: Rate limiting problem
aliases:
- request throttling problem
area: systems/rate-limiting
level: intro
summary: Decide at the arrival of each request whether it passes, so that the passed requests obey a limit such as n per window of length w, or rate r with burst b.
prereqs: [online-algorithm]
see_also: [token-bucket, gcra, sliding-window-log, fixed-window-counter, sliding-window-counter, rate-limiter, traffic-policing, admission-control]
sources:
  - book: isbn:9783540421849
    title: Jean-Yves Le Boudec and Patrick Thiran, Network Calculus, A Theory of Deterministic Queuing Systems for the Internet, Springer LNCS 2050, 2001
    locator: Chapter 1, Section 1.2 (arrival curves, the leaky bucket controller and GCRA) and Section 1.5 (policers and shapers)
  - paper: doi:10.1109/18.61109
    title: Rene L. Cruz, A calculus for network delay, Part I, Network elements in isolation, IEEE Transactions on Information Theory 37(1), 1991, pages 114 to 131
    locator: the (sigma, rho) burstiness constraint on a traffic stream
  - url: "https://www.rfc-editor.org/rfc/rfc6585"
    title: Mark Nottingham and Roy T. Fielding, RFC 6585, Additional HTTP Status Codes, 2012
    locator: Section 4, 429 Too Many Requests
  - book: isbn:9798664653403
    title: Alex Xu, System Design Interview, An Insider's Guide, Volume 1, 2020
    locator: Chapter 4, Design a rate limiter (token bucket, leaking bucket, fixed window, sliding window log and sliding window counter)
---

The rate limiting problem asks a server to decide, at the arrival of each request, whether the request passes, so that the passed requests of each client obey a limit. The limit is a rule over intervals of time: "at most $n$ requests in any window of length $w$", "at most $n$ in each calendar minute", or "rate $r$ with bursts of at most $b$", which says that each interval of length $\tau$ gets at most $r\tau + b$. The decision must be online, cheap, and per key, often for millions of keys. This page is about the question and its answers. The interface that programs call is the [rate limiter](/rate-limiter/), and the standard solutions are the [token bucket](/token-bucket/), [GCRA](/gcra/) and the window counters.

## In plain words

A web service lets each customer make at most a certain number of calls. Calls come one at a time, and the service must answer at once: let this call through, or refuse it with "too many requests". It cannot wait to see the next calls, and it cannot keep much data for each customer, because there are many customers.

The rule can be stated in several ways. "At most 100 calls in any minute" counts over a window that moves with time. "At most 100 calls in each clock minute" counts over fixed minutes. "10 calls per second, with bursts of 20" lets a quiet customer save up some calls. Each rule gives a different method, a different amount of memory, and different mistakes at the edges.

## Definition

**Input.** A sequence of requests $(t_j, \kappa_j, L_j)$ for $j = 1, 2, \ldots$, with times $t_1 \le t_2 \le \cdots$, a key $\kappa_j$ (a client, an IP address, an API token) and a size $L_j > 0$. For plain request counting, $L_j = 1$. The times are not known in advance: the arrival model is adversarial, and no rate or distribution is assumed.

**Output.** For each request, at time $t_j$ and with the knowledge of requests $1$ to $j$ only, a decision: pass or reject. (A shaper may also delay a request; see Variants.)

**Constraint.** The limit is a family $\mathcal{I}$ of intervals of the time line with a cap $c(I)$ for each $I \in \mathcal{I}$. For each key, the passed requests must satisfy

$$\sum_{j \text{ passed},\ t_j \in I} L_j \;\le\; c(I) \qquad \text{for each } I \in \mathcal{I}.$$

The common limits are:

| limit | intervals $\mathcal{I}$ | cap $c(I)$ |
|---|---|---|
| sliding window $(n, w)$ | all $(s - w, s]$ | $n$ |
| fixed window $(n, w)$ | the aligned $[kw, (k+1)w)$ | $n$ |
| arrival curve $\alpha$ | all intervals | $\alpha(\lvert I \rvert)$ |
| token bucket $(r, b)$ | all intervals | $r\lvert I \rvert + b$ |
| dual bucket | all intervals | $\min(M + p\lvert I \rvert,\ r\lvert I \rvert + b)$ |

**Goals.** A solution is *sound* if the passed requests always obey the limit. It is *greedy* if it rejects a request only when passing it would break the limit, given the requests passed before. It should take $O(1)$ time per request and little memory per key.

## Variants

- **Policing or shaping.** A policer passes or rejects at once (see [traffic policing](/traffic-policing/)). A shaper keeps the requests that do not fit in a queue and sends them when they fit (see [traffic shaping](/traffic-shaping/) and the [leaky bucket queue](/leaky-bucket-queue/)). Shaping trades delay and buffer space for fewer drops.
- **Marking.** Instead of rejecting, mark the request as out of profile and let a later stage decide, as in the [single-rate three-color marker](/single-rate-three-color-marker/).
- **Weighted requests.** Requests have sizes (bytes, tokens of a language model, cost units), and the cap is on the sum.
- **Global or per key.** One limit for the whole service, one per client, or both at once.
- **Distributed.** Many servers decide for the same key and must share or split the state. See [distributed rate limiting](/distributed-rate-limiting/).
- **Waiting clients.** The server tells a rejected client when to retry (the HTTP status 429 Too Many Requests of RFC 6585, often with a Retry-After header), and a well-behaved client waits.
- **Adaptive limits.** The cap changes with the load of the server. This is closer to [admission control](/admission-control/) and [load shedding](/load-shedding/).

## Examples

The requests of one key come at the times 8, 9, 9.5, 10, 10.5, 11, 12, 15, 18, 19, 21, 25 and 28.5, with unit size. Four limiters with a limit of 3 per 10 seconds give these decisions (P for pass, R for reject):

| time | 8 | 9 | 9.5 | 10 | 10.5 | 11 | 12 | 15 | 18 | 19 | 21 | 25 | 28.5 | passed |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [fixed window counter](/fixed-window-counter/) | P | P | P | P | P | P | R | R | R | R | P | P | P | 9 |
| [sliding window log](/sliding-window-log/) | P | P | P | R | R | R | R | R | P | P | P | R | P | 7 |
| [sliding window counter](/sliding-window-counter/) | P | P | P | R | R | R | R | P | P | R | P | P | R | 7 |
| [token bucket](/token-bucket/) $r = 0.3$, $b = 3$ | P | P | P | R | R | R | P | P | P | R | R | P | P | 8 |

- The fixed window counter passes six requests in $[8, 11]$, twice the limit, because 10 starts a new window.
- The sliding window log is exact: no window of length 10 holds more than 3 passed requests, and no request is rejected unless the window holds 3.
- The sliding window counter passes four in $(8.5, 18.5]$, because it assumes the three requests of the first window were spread over it. It rejects 28.5, which the exact rule allows.
- The token bucket enforces a different rule: rate 0.3 per second with a burst of 3. After the burst it passes one request about every 3.3 seconds, while the log waits for a full window.

## Known algorithms

| algorithm | limit it enforces | state per key | time per request | most passed in a window of length $w$ |
|---|---|---|---|---|
| [token bucket](/token-bucket/) | $r\tau + b$, exactly | 2 numbers | $\Theta(1)$ worst case | $rw + b$ |
| [leaky bucket meter](/leaky-bucket-meter/) | $r\tau + b$, exactly | 2 numbers | $\Theta(1)$ worst case | $rw + b$ |
| [GCRA](/gcra/) | $r\tau + b$ with $r = 1/T$, $b = 1 + \tau/T$ | 1 time | $\Theta(1)$ worst case | $rw + b$ |
| [fixed window counter](/fixed-window-counter/) | $n$ per aligned window, exactly | 2 numbers | $\Theta(1)$ worst case | $2n$ |
| [sliding window log](/sliding-window-log/) | $n$ per sliding window, exactly | up to $n$ times | $\Theta(1)$ amortized, $\Theta(n)$ worst case; $\Theta(1)$ with a ring | $n$ |
| [sliding window counter](/sliding-window-counter/) | $n$ per sliding window, approximately | 3 numbers | $\Theta(1)$ worst case | $2n - 1$ |
| [leaky bucket queue](/leaky-bucket-queue/) | output rate $r$, queue of $K$ (a shaper) | up to $K$ packets | $\Theta(1)$ worst case per packet | $rw + 1$ unit packets out |

The bounds in the last column are worst-case bounds over adversarial inputs, proved on each page. The token bucket, the leaky bucket meter and GCRA make the same decisions for unit requests when the parameters match.

## Bounds

**Greedy is optimal for unit requests.** Let all sizes be 1, and let the limit be any family of intervals with caps, as in the definition. The greedy rule passes request $j$ if and only if the passed requests before $j$, with $j$, obey the limit. Then greedy passes as many requests as any sound policy, even one that knows the whole input in advance.

*Proof.* Let $S$ be the greedy set and $O$ an optimal sound set that agrees with $S$ on the longest prefix. Suppose they differ, and let $j$ be the first request in only one of them. If $j \in O \setminus S$, greedy rejected $j$ because $(S \cap \{1..j-1\}) \cup \{j\}$ breaks some cap; this set equals $O \cap \{1..j\}$, a subset of $O$, so $O$ breaks the cap too, which is false. So $j \in S \setminus O$. If $O$ has no request after $j$, then $O \cup \{j\}$ restricted to any interval equals $S \cap \{1..j\}$ restricted to it, or a subset of $O$, so $O \cup \{j\}$ is sound and larger than $O$, which is false. Else let $k$ be the first request of $O$ after $j$, and $O' = O \cup \{j\} \setminus \{k\}$. An interval that holds $t_j$ but not $t_k$ ends before $t_k$, and $O'$ has no request between $j$ and $k$, so $O'$ in it equals $S \cap \{1..j\}$ in it, which obeys the cap. Every other interval holds at most as many requests of $O'$ as of $O$. So $O'$ is sound, $|O'| = |O|$, and it agrees with $S$ on a longer prefix, which is false. So $S = O$. $\square$

So for unit requests, the token bucket, GCRA and the sliding window log are optimal for their limits, since each is the greedy rule for its limit.

**No online policy is optimal for sizes.** With sizes, no deterministic online policy always passes the most requests, or the most units. Take a token bucket limit with $b = 2$ and a rate so small that nothing refills during the test, and send everything at time 0.

- *Count.* A request of size 2 comes first. If the policy passes it, two requests of size 1 follow; both must be rejected, and the best set (the two small ones) has 2 requests against 1. If the policy rejects it, nothing follows, and the best set has 1 request against 0.
- *Units.* A request of size 1 comes first. If the policy passes it, a request of size 2 follows and must be rejected: 1 unit against the best 2. If the policy rejects it, nothing follows: 0 against 1.

So a deterministic online policy can pass as little as half of the best count or units, in the sense of [online algorithms](/online-algorithm/).

**Memory for an exact sliding window.** With integer times and $W$ ticks per window, each limiter that makes exactly the decisions of the sliding window rule $(n, W)$ needs at least $\log_2 \binom{W}{n}$ bits per key in the worst case. After $n$ requests at a set of ticks inside one window, bursts at later ticks reveal the set, so different sets need different states. The proof is on the [sliding window log](/sliding-window-log/) page. In contrast, the token bucket limit needs two numbers, because its state after any past is the number of tokens and the time.

**Edge bursts of window counters.** A limit of $n$ per aligned window lets $2n$ requests pass within an arbitrarily short time around a window edge. The [sliding window counter](/sliding-window-counter/) lowers this to $2n - 1$ in a window of length $w$, and both bounds are reached.

## Reductions

- **Token bucket and arrival curves.** The token bucket $(r, b)$ is the greedy policer for the affine arrival curve $r\tau + b$ of Cruz. The [leaky bucket meter](/leaky-bucket-meter/) is the same limiter with the level $b$ minus the tokens, and [GCRA](/gcra/) is the same with one timestamp.
- **Sliding window to token bucket.** The output of a sliding window limiter $(n, w)$ fits a token bucket with rate $n/w$ and depth $n$. The reverse is false, so the sliding window rule is the stricter of the two.
- **Fixed window to token bucket.** The output of a fixed window counter $(n, w)$ fits a token bucket with rate $n/w$ and depth $2n$.
- **Sliding window counting.** An exact sliding window limiter answers "are fewer than $n$ items in the last $w$ ticks?" at each request. This is a threshold form of basic counting in the [sliding window model](/sliding-window-model/), which explains why exact limits need memory that grows with $n$.

## Applications

- **Web APIs.** Per-client limits protect servers and share capacity among customers. The server answers a rejected request with status 429 Too Many Requests.
- **Network edges.** Routers police or shape traffic to a contract with token buckets, as in Differentiated Services; see [traffic policing](/traffic-policing/).
- **ATM networks.** Usage parameter control checks each cell with [GCRA](/gcra/).
- **Login and abuse control.** Exact sliding windows for password attempts, sign-ups and messages.
- **Cost control.** Limits on paid calls to other services, on tokens sent to a language model, or on writes to a database.
- **Overload protection.** With [load shedding](/load-shedding/) and [backpressure](/backpressure/), rate limits keep a service inside the capacity it was sized for.

## References
