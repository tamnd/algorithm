---
tag: WERYMV
kind: algorithm
slug: fixed-window-counter
name: Fixed window counter
aliases:
- fixed window rate limiter
area: systems/rate-limiting
level: intro
summary: Count the requests in each aligned window of length w and reject after n. Two numbers per key, but up to 2n requests can pass near a window edge.
solves: [rate-limiting-problem]
model: word-ram
complexity:
  vars: {m: the number of requests on one key, k: the number of active keys}
  time: {worst: Θ(m)}
  space: {extra: Θ(k)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [rate-limiting-problem]
see_also: [sliding-window-counter, sliding-window-log, token-bucket, gcra, rate-limiter, tumbling-window, distributed-rate-limiting, burst-tolerance]
sources:
  - book: isbn:9798664653403
    title: Alex Xu, System Design Interview, An Insider's Guide, Volume 1, 2020
    locator: Chapter 4, Design a rate limiter (the fixed window counter algorithm)
  - url: "https://www.figma.com/blog/an-alternative-approach-to-rate-limiting/"
    title: Nikrad Mahdi, An alternative approach to rate limiting, Figma engineering blog, 2017
    locator: the section on fixed window counters and the burst at the window edge
---

A fixed window counter is a [rate limiter](/rate-limiter/) that cuts the time line into aligned windows $[kw, (k+1)w)$ and counts the requests that pass in the current window. A request passes if the count is below the limit $n$. When a request comes in a new window, the count starts again at 0. It needs one window index and one counter per key and $\Theta(1)$ time per request. It is exact for the rule "at most $n$ per aligned window", but not for "at most $n$ in any window of length $w$": $n$ requests at the end of one window and $n$ at the start of the next all pass, so $2n$ requests can pass in a very short time.

## In plain words

A shop lets in at most 100 people each hour. A guard has a tally sheet. Each person who comes in gets a mark. When the sheet shows 100, the guard turns people away. On the hour, the guard throws the sheet away and starts a new one.

This is simple and cheap: one number per customer group, and one more number for the hour. The problem is the change of the hour. If 100 people come at 9:59 and 100 more at 10:00, all 200 get in within one minute, because each group fits in its own hour.

## The problem

The input is a sequence of requests at times $t_1 \le t_2 \le \cdots$ on one key. The counter decides each request at its arrival. The rule it enforces is: each aligned window $W_k = [kw, (k+1)w)$ holds at most $n$ passed requests. This is one form of the [rate limiting problem](/rate-limiting-problem/). The arrival model is adversarial: no assumption on the times.

## The algorithm

Each key has two fields: the index $C.k$ of the current window (none at the start) and the count $C.count$ of the requests that passed in it.

```pseudo id=main
FIXED-WINDOW-ALLOW(C, t)            ▷ a request at time t; times do not go back
L1  k ← ⌊t / w⌋                     ▷ the aligned window that holds t
L2  if k ≠ C.k then C.k ← k; C.count ← 0       ▷ a new window: start again
L3  if C.count < n then
L4      C.count ← C.count + 1
L5      return ALLOW
L6  return REJECT
```

A rejected request does not change the count. In a key-value store the same rule is often one atomic increment on the key "client id plus window index", with an expiry of one window: the request passes if the value after the increment is at most $n$. The rejected requests then also increase the value, but the decisions stay the same, because once the value is above $n$ every later request in the window is rejected.

## Example

Let $n = 3$ and $w = 10$. The windows are $[0, 10)$, $[10, 20)$ and $[20, 30)$.

| time | window | count before | decision | count after |
|---|---|---|---|---|
| 8 | 0 | 0 | pass | 1 |
| 9 | 0 | 1 | pass | 2 |
| 9.5 | 0 | 2 | pass | 3 |
| 10 | 1 | 0 (reset) | pass | 1 |
| 10.5 | 1 | 1 | pass | 2 |
| 11 | 1 | 2 | pass | 3 |
| 12 | 1 | 3 | reject | 3 |
| 15 | 1 | 3 | reject | 3 |
| 18 | 1 | 3 | reject | 3 |
| 19 | 1 | 3 | reject | 3 |
| 21 | 2 | 0 (reset) | pass | 1 |
| 25 | 2 | 1 | pass | 2 |
| 28.5 | 2 | 2 | pass | 3 |

Six requests pass in the interval $[8, 11]$, which has length 3. That is $2n$ in less than one window. Then the counter rejects all four requests from 12 to 19, because window 1 is full. A [sliding window log](/sliding-window-log/) with the same $n$ and $w$ passes 7 of these 13 requests and never more than 3 in any window of length 10.

## Correctness

The full proof is below. Lemma 1 is the invariant: after each request, $C.count$ is the number of passed requests in the window of that request. Three results follow from it.

- **Exact per aligned window.** A request passes if and only if fewer than $n$ requests passed before it in its aligned window. So no aligned window holds more than $n$.
- **Any interval.** An interval of length $\tau$ meets at most $\lceil \tau / w \rceil + 1$ aligned windows, so it holds at most $n(\lceil \tau/w \rceil + 1) \le (n/w)\tau + 2n$ passed requests. The output conforms to a [token bucket](/token-bucket/) with rate $n/w$ and depth $2n$.
- **The bound is reached.** $n$ requests at time $w - \varepsilon$ and $n$ at time $w$ all pass, for each small $\varepsilon > 0$. So the burst is $2n$, twice the limit, and it can come in an arbitrarily short time.

Over $K$ whole windows at most $Kn$ requests pass, so the long-run rate is $n / w$.

## Complexity

In the word RAM, with the times and counts in words:

- **Time.** Each call runs lines L1 to L6 once: $\Theta(1)$ in the worst case per request, and $\Theta(m)$ for $m$ requests on one key.
- **Space.** Two numbers per key, so $\Theta(k)$ for $k$ active keys. A key whose window has ended can be deleted, because a new key starts with a count of 0. A store with expiring keys does this on its own.

## Properties

- **Online and deterministic.** Each decision uses only the past.
- **No delay.** The counter passes or rejects at once.
- **Burst of $2n$ at the edge.** The worst case over any window of length $w$ is $2n$, by the theorem above.
- **Unfair inside a window.** A client that uses its $n$ requests at the start of a window waits until the next window, however long that is.
- **Synchronized resets.** With windows aligned to the clock, all clients get new quota at the same instant.

## Variants and improvements

- **Per-key offset.** Shift the windows of each key by a hash of the key, $W_k = [kw + h, (k+1)w + h)$. The bounds stay the same, but the resets of different clients no longer come at the same instant.
- **[Sliding window counter](/sliding-window-counter/).** Keep the count of the previous window too, and weight it by the part of the previous window that is still inside the last $w$ seconds. This removes most of the edge burst for two numbers more.
- **Sub-windows.** Count in $s$ sub-windows of length $w/s$ and sum the last $s$ of them. The memory is $s$ counters per key. The worst case is still $2n$ in a window of length $w$: $n$ requests at the end of one sub-window and $n$ at the start of the sub-window $s$ steps later, with nothing between them.
- **[Sliding window log](/sliding-window-log/).** Store the times of the passed requests. It is exact for any window, at the cost of up to $n$ times per key.
- **[Token bucket](/token-bucket/) or [GCRA](/gcra/).** Two numbers (or one) per key, a burst that the operator chooses, and no edge effect.

## When to use it

Use a fixed window counter when the quota is a billing or fairness quota per calendar period ("10,000 calls per day") and a burst at the period edge does not hurt, or when the only tool is an atomic increment with expiry in a shared store. Do not use it to protect a server from overload, because the edge burst is twice the limit. For that, use a [token bucket](/token-bucket/), [GCRA](/gcra/) or a [sliding window counter](/sliding-window-counter/).

## Pitfalls

- **Increment and expiry in two steps.** If the store sets the expiry in a separate command and the client stops between the two, the key never expires and the client is blocked for good. Do both in one atomic step, or put the window index in the key name.
- **The edge burst.** The limit $n$ per window does not mean $n$ per $w$ seconds. If the server can take only $n$ per $w$ seconds, set the limit to $n/2$ or use another method.
- **Clock skew.** With many servers, each one computes $\lfloor t / w \rfloor$ from its own clock. Near an edge, two servers can count the same request in different windows. Take the time from one place, for example the shared store.
- **Integer division of negative or float times.** Use a floor, not a truncation, and keep times in integers (for example milliseconds) to avoid rounding at the edge.
- **Retry-After.** A rejected client should wait until $(C.k + 1)w$, the end of the window, not for $w$ seconds.

## Implementations

The Python version takes times as `int` or `Fraction`, so the window index is exact. The tests check the table above and the edge burst of $2n$. On seeded random inputs they check that each request passes if and only if its aligned window has fewer than $n$, and that each interval of length $\tau$ holds at most $n(\lceil \tau/w \rceil + 1)$ passed requests.

## History

The fixed window counter has no single known source. It is the plain way to count calls per minute, hour or day, and API quotas are often stated in this form. Engineering write-ups such as the one by Mahdi at Figma in 2017 describe its burst at the window edge as the reason to move to a sliding window, and Xu's 2020 book on system design lists it with the [token bucket](/token-bucket/), the [leaky bucket](/leaky-bucket-queue/), the [sliding window log](/sliding-window-log/) and the [sliding window counter](/sliding-window-counter/).

## References
