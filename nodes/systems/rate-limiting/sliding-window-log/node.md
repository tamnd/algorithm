---
tag: JEWV9G
kind: algorithm
slug: sliding-window-log
name: Sliding window log
aliases:
- sliding log rate limiter
area: systems/rate-limiting
level: intro
summary: Keep the times of the passed requests of the last w seconds. A request passes if fewer than n are kept. Exact for every window, but it stores up to n times per key.
solves: [rate-limiting-problem]
model: word-ram
complexity:
  vars: {m: the number of requests on one key, n: the limit per window}
  time: {worst: Θ(m), amortized: Θ(1)}
  space: {extra: Θ(n)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [rate-limiting-problem, deque]
see_also: [sliding-window-counter, fixed-window-counter, token-bucket, gcra, circular-buffer, sliding-window-model, basic-counting, rate-limiter]
sources:
  - book: isbn:9798664653403
    title: Alex Xu, System Design Interview, An Insider's Guide, Volume 1, 2020
    locator: Chapter 4, Design a rate limiter (the sliding window log algorithm)
  - url: "https://www.figma.com/blog/an-alternative-approach-to-rate-limiting/"
    title: Nikrad Mahdi, An alternative approach to rate limiting, Figma engineering blog, 2017
    locator: the section on sliding window logs (a sorted set of timestamps per user, and its memory cost)
---

A sliding window log is a [rate limiter](/rate-limiter/) that keeps, for each key, the times of the requests that passed in the last $w$ seconds. A request at time $t$ first removes the times at or before $t - w$; then it passes if fewer than $n$ times remain, and its own time is added. It enforces "at most $n$ requests in any window of length $w$" exactly: it never passes $n + 1$ requests within less than $w$ seconds, and it never rejects a request that the rule allows. The cost is memory: up to $n$ times per key, against one or two numbers for a [token bucket](/token-bucket/) or a [fixed window counter](/fixed-window-counter/).

## In plain words

Keep a short list for each client: the times of its last few accepted requests. When a new request comes, cross out the times that are more than one window old. If fewer than $n$ times are left on the list, accept the request and write its time at the end. If the list is full, refuse it, and do not write anything.

The list is never longer than $n$. The oldest time on the list tells the client when it can try again: one window after that time.

## The problem

The input is a sequence of requests at times $t_1 \le t_2 \le \cdots$ on one key. The limiter decides each request at its arrival. The rule is: each window $(s - w, s]$ holds at most $n$ passed requests. In other words, any $n + 1$ passed requests span at least $w$ seconds. This is the sliding window form of the [rate limiting problem](/rate-limiting-problem/). The arrival model is adversarial: no assumption on the times.

## The algorithm

Each key has a [deque](/deque/) $Q$ of times, oldest first, empty at the start.

```pseudo id=main
SLIDING-LOG-ALLOW(Q, t)             ▷ a request at time t; times do not go back
L1  while Q is not empty and Q.front ≤ t − w do
L2      Q.pop_front()               ▷ this time has left the window
L3  if |Q| < n then
L4      Q.push_back(t)
L5      return ALLOW
L6  return REJECT
```

The log is sorted because the times do not go back, so all the old times are at the front. A rejected request does not go into the log. In a shared store, the same steps are often a sorted set per key with the times as scores: remove the scores at or below $t - w$, count, and add $t$ if the count is below $n$. All three steps must run as one atomic step.

## Example

Let $n = 3$ and $w = 10$. The column "log after" shows the times in the log after the request.

| time | removed at L1 and L2 | log size at L3 | decision | log after |
|---|---|---|---|---|
| 8 | none | 0 | pass | 8 |
| 9 | none | 1 | pass | 8, 9 |
| 9.5 | none | 2 | pass | 8, 9, 9.5 |
| 10 | none | 3 | reject | 8, 9, 9.5 |
| 10.5 | none | 3 | reject | 8, 9, 9.5 |
| 11 | none | 3 | reject | 8, 9, 9.5 |
| 12 | none | 3 | reject | 8, 9, 9.5 |
| 15 | none | 3 | reject | 8, 9, 9.5 |
| 18 | 8 | 2 | pass | 9, 9.5, 18 |
| 19 | 9 | 2 | pass | 9.5, 18, 19 |
| 21 | 9.5 | 2 | pass | 18, 19, 21 |
| 25 | none | 3 | reject | 18, 19, 21 |
| 28.5 | 18 | 2 | pass | 19, 21, 28.5 |

Seven requests pass. Each set of four passed requests spans at least 10 seconds: for example 8 and 18, and 18 and 28.5. On the same input a [fixed window counter](/fixed-window-counter/) passes 9 requests, six of them in $[8, 11]$. At time 25 the log rejects, because 18, 19 and 21 are all within the last 10 seconds; it accepts again at 28.5, after 18 has left the window.

## Correctness

The full proof is below. Lemma 1 is the invariant: after each request, the log holds exactly the passed times in $(t - w, t]$, in order. From it:

- **The rule.** A request passes if and only if fewer than $n$ passed requests lie in $(t - w, t]$.
- **Soundness.** Any $n + 1$ passed requests span at least $w$. When the last of them came, fewer than $n$ passed requests were in its window, so the first of them was already out of it.
- **Greedy and tight.** A request is rejected only when it would make $n + 1$ requests within less than $w$. So an input that already fits the rule passes whole.
- **Token bucket bound.** An interval of length $\tau$ holds at most $n(\lfloor \tau/w \rfloor + 1) \le (n/w)\tau + n$ passed requests, so the output fits a [token bucket](/token-bucket/) with rate $n/w$ and depth $n$. The log is stricter than that bucket: after a burst of $n$, the bucket passes one more request after $w/n$ seconds, but the log waits $w$ seconds.
- **Memory lower bound.** With integer times and $W$ ticks per window, any limiter that makes exactly these decisions needs at least $\log_2 \binom{W}{n}$ bits per key in the worst case. The proof sends $n$ requests at a set $S$ of ticks inside one window, then shows that bursts at later ticks reveal $S$. So any exact limiter must in effect store the times.

## Complexity

In the word RAM, with times in words:

- **Time.** Each time enters the log once and leaves it at most once, so $m$ requests cost $\Theta(m)$ in total, and the amortized time per request is $\Theta(1)$ (by the [aggregate method](/aggregate-method/)). One request can remove up to $n$ times, so a single call takes $\Theta(n)$ time in the worst case.
- **Space.** At most $n$ times per key. A key whose newest time is older than $w$ can be deleted.

With a [circular buffer](/circular-buffer/) of the last $n$ passed times (the variant below), every request takes $\Theta(1)$ time in the worst case, and the space is exactly $n$ slots per key.

## Properties

- **Exact.** It is the greedy limiter for the sliding window rule: sound and tight.
- **Online and deterministic.** Each decision uses only the past.
- **No edge effect.** The windows slide with each request, so there is no time at which all clients get new quota.
- **Strict after a burst.** After $n$ requests in a burst, the next request must wait a full window, while a token bucket with the same long-term rate passes one each $w/n$ seconds.
- **Exact retry time.** A rejected client can pass at $Q.front + w$, the time when the oldest time leaves the window.

## Variants and improvements

- **Ring of the last $n$ passed times.** A request passes if fewer than $n$ requests passed so far, or if the oldest of the last $n$ passed times is at or before $t - w$; then it replaces that oldest time. This makes the same decisions with $\Theta(1)$ worst-case time and no deletion loop.
- **Log of all requests.** Some versions add the time of a rejected request too. Then a client that keeps trying stays blocked for good, which punishes retries. This is a different rule; state it if you use it.
- **[Sliding window counter](/sliding-window-counter/).** Two counters instead of $n$ times. It estimates the count in the window under the assumption that the previous window was uniform, so it can pass up to $2n - 1$ in a window, and it is much cheaper.
- **Sub-window buckets.** Count per sub-window of length $w/s$ and sum the last $s$ counts. This uses $s$ counters per key, whatever $n$ is.
- **Approximate sliding counts.** The [exponential histogram](/exponential-histogram/) of the [sliding window model](/sliding-window-model/) counts the items in the last $w$ ticks within a factor $1 + \varepsilon$ in $O(\varepsilon^{-1} \log^2 W)$ bits. It answers "about how many", which is enough for a soft limit.

## When to use it

Use a sliding window log when the limit must hold exactly for every window, for example a contract that says "at most 5 password attempts in any 15 minutes", and $n$ is small. For large limits, such as 10,000 requests per hour per client, the memory of $n$ times per key is too much; use a [sliding window counter](/sliding-window-counter/), a [token bucket](/token-bucket/) or [GCRA](/gcra/) instead.

## Pitfalls

- **Logging rejected requests.** If the rejected times also go into the log, the log grows without bound under attack, and the client never recovers while it keeps trying.
- **Unbounded logs per key.** Without the limit $|Q| \le n$, a log of all requests in the window costs memory in proportion to the attack rate. The algorithm above never stores more than $n$.
- **Equal times in a sorted set.** A sorted set keyed by the time keeps one entry for two requests with the same time. Add a unique suffix to each member.
- **Closed or open window.** Removing times $< t - w$ instead of $\le t - w$ makes the window $[t - w, t]$, which is one tick longer. Choose one and test the edge.
- **Several steps in a shared store.** Remove, count and add must be one atomic step, or two servers can both see $n - 1$ and both pass. See [distributed rate limiting](/distributed-rate-limiting/).

## Implementations

The Python version keeps the log in a `collections.deque` and takes times as `int` or `Fraction`. A second class keeps the last $n$ passed times in a ring. The tests check the table above, check that the ring makes the same decisions as the deque on seeded random inputs, and check every multiset of up to six integer times in $0$ to $6$ against the brute-force rule for four pairs $(n, w)$: the output fits, the decision is greedy, and an input that fits passes whole. A last test runs the probe of the memory lower bound and checks that different sets give different answers.

## History

The sliding window log has no single known source. It is the direct way to check "at most $n$ in any window" and appears in many API gateways. Mahdi's 2017 write-up for Figma describes it with a sorted set per user in Redis and estimates its memory cost, and Xu's 2020 book on system design lists it among five rate limiting algorithms. The question of how much memory an exact sliding count needs was studied in the theory of data streams, in the [sliding window model](/sliding-window-model/) of Datar, Gionis, Indyk and Motwani.

## References
