---
tag: 5G9VHE
kind: abstract-type
slug: rate-limiter
name: Rate limiter
area: systems/rate-limiting
level: intro
summary: An object that grants units of work under a limit. try_acquire passes or rejects at once, reserve returns the time when the units may go, and acquire waits until then.
prereqs: [rate-limiting-problem]
see_also: [token-bucket, gcra, sliding-window-log, semaphore, throttling, distributed-rate-limiting, backpressure, count-min-sketch]
sources:
  - url: "https://pkg.go.dev/golang.org/x/time/rate"
    title: The Go Authors, package golang.org/x/time/rate
    locator: the type Limiter (a token bucket of size b, initially full, refilled at rate r), and the methods AllowN, ReserveN, WaitN, Reservation.Cancel and Reservation.Delay
  - url: "https://guava.dev/releases/snapshot-jre/api/docs/com/google/common/util/concurrent/RateLimiter.html"
    title: Google, Guava, class com.google.common.util.concurrent.RateLimiter
    locator: the class description (the permits of a request affect the throttling of the next request), and the methods create, acquire and tryAcquire
  - url: "https://www.rfc-editor.org/rfc/rfc6585"
    title: Mark Nottingham and Roy T. Fielding, RFC 6585, Additional HTTP Status Codes, 2012
    locator: Section 4, 429 Too Many Requests
  - url: "https://www.rfc-editor.org/rfc/rfc9110"
    title: Roy T. Fielding, Mark Nottingham and Julian Reschke, RFC 9110, HTTP Semantics, 2022
    locator: Section 10.2.3, Retry-After
---

A rate limiter is an object that grants units of work (requests, bytes, tokens) to callers so that the granted units obey a limit, such as "at most $n$ per window of length $w$" or "rate $r$ with bursts of $b$". It has three ways to ask: `try_acquire` grants at once or refuses, `reserve` books the units and returns the time when they may be used, and `acquire` waits until that time. A server uses `try_acquire` and answers a refused request with HTTP status 429; a client or a batch job uses `acquire` to slow itself down. The [rate limiting problem](/rate-limiting-problem/) is the question behind it, and the [token bucket](/token-bucket/), [GCRA](/gcra/) and the window counters are its common implementations.

## In plain words

Think of a ticket desk with a rule, for example "at most 10 tickets per second, and at most 20 at once". You can ask the desk in three ways. "Give me a ticket now, or say no." "Book me a ticket and tell me when to come back." "I will wait here until you can give me a ticket."

The desk keeps a record of the tickets it gave. It never gives out more than the rule allows, and a good desk never says no when the rule would allow a yes. A "no" costs nothing: it does not use up any of the allowance.

## Operations

**Model.** A limiter has a *limit*: a family of intervals of the time line with a cap on the units granted in each, as defined on the [rate limiting problem](/rate-limiting-problem/) page. It also has a *history* $H$, the set of grants $(s, n)$ made so far, each with the time $s$ when the $n$ units are used. The time $t$ of a call is read from a monotonic clock. A grant $(s, n)$ *fits* if $H \cup \{(s, n)\}$ obeys the limit. For a key-value limiter, each key has its own history.

| operation | result | effect |
|---|---|---|
| `try_acquire(n)` at time $t$ | true if $(t, n)$ fits, else false | on true, add $(t, n)$ to $H$ |
| `retry_after(n)` at time $t$ | the least $s \ge t$ such that $(s, n)$ fits, or never | none |
| `reserve(n)` at time $t$ | a reservation with that time $s$, or a failure if $s$ is never | add $(s, n)$ to $H$ |
| `cancel(v)` | none | remove the reservation $v$ from $H$ if its time has not come |
| `acquire(n)` | the time waited | `reserve(n)`, then sleep until $s$ |

In the Go package `golang.org/x/time/rate` these are `AllowN`, `ReserveN` (with `Reservation.Delay` and `Cancel`) and `WaitN`. Its `Limiter` "implements a "token bucket" of size b, initially full and refilled at rate r tokens per second". `ReserveN` returns a reservation whose `OK()` is false if $n$ exceeds the burst size, and `WaitN` returns an error in that case, or if the wait would pass the deadline of its context. In Guava, `tryAcquire` and `acquire` play the same roles; `acquire` returns the time spent sleeping, and `tryAcquire` with a timeout returns false at once if the permits would not come in time.

An HTTP server that refuses a request answers with status 429 Too Many Requests (RFC 6585, Section 4) and can put `retry_after(n) - t` in the Retry-After header (RFC 9110, Section 10.2.3).

## Laws

For an exact limiter, at each point in time and for each key:

1. **Safety.** The history $H$ obeys the limit. Each operation keeps it so.
2. **No needless refusal.** `try_acquire(n)` at time $t$ returns false only if $(t, n)$ does not fit.
3. **A refusal is free.** A false `try_acquire` leaves $H$ unchanged. So a caller that is refused and tries again later is treated as if the first try did not happen.
4. **Waiting helps.** For the limits of the [token bucket](/token-bucket/), [GCRA](/gcra/), the [fixed window counter](/fixed-window-counter/) and the [sliding window log](/sliding-window-log/): if $(t, n)$ fits and nothing is granted in between, then $(t', n)$ fits for each $t' \ge t$.
5. **Smaller asks.** If $(t, n)$ fits, then $(t, m)$ fits for each $m \le n$.
6. **Retry time.** If `retry_after(n)` at time $t$ returns $s$ and nothing is granted in between, then `try_acquire(n)` fails at each time in $[t, s)$ and succeeds at time $s$.
7. **Too large.** If no history at all lets $n$ units fit at once (for a token bucket, $n > b$), then `try_acquire(n)` is always false, and `reserve(n)` and `acquire(n)` must fail rather than wait forever.

Laws 1 and 2 together say that `try_acquire` is the greedy rule, which for unit requests passes as many requests as any sound policy (see Bounds on the [rate limiting problem](/rate-limiting-problem/) page). An approximate limiter, such as the [sliding window counter](/sliding-window-counter/), breaks law 1 or law 2 by a bounded amount. Some limiters break law 3 on purpose and count refused calls too, which punishes clients that retry too fast.

Guava breaks law 1 in a controlled way: "the number of permits requested never affects the throttling of the request itself", but "affects the throttling of the next request". A large request passes at once, and the next caller pays for it by waiting. This is a token bucket whose tokens may go below zero.

## Implementations

| implementation | limit | state per key | `try_acquire` | `retry_after(n)` |
|---|---|---|---|---|
| [token bucket](/token-bucket/) | $r\tau + b$ | tokens and time | $\Theta(1)$ | $t + (n - x)/r$ if $n > x$ |
| [GCRA](/gcra/) | $r\tau + b$ with $r = 1/T$ | one time $tat$ | $\Theta(1)$ | $tat + (n-1)T - \tau$ |
| [leaky bucket meter](/leaky-bucket-meter/) | $r\tau + b$ | level and time | $\Theta(1)$ | $t + (X + n - b)/r$ if $X + n > b$ |
| [fixed window counter](/fixed-window-counter/) | $n$ per aligned window | window and count | $\Theta(1)$ | the end of the window |
| [sliding window log](/sliding-window-log/) | $n$ per sliding window | up to $n$ times | $\Theta(1)$ amortized | the oldest logged time plus $w$, for $n = 1$ |
| [sliding window counter](/sliding-window-counter/) | about $n$ per sliding window | window and two counts | $\Theta(1)$ | solve the estimate for $f$ |
| [leaky bucket queue](/leaky-bucket-queue/) | output rate $r$ | a queue | $\Theta(1)$ | not used: it delays instead |

In the table, $x$ is the token count after the refill and $X$ the level after the leak. All the times are worst case per call except where marked. A limiter for many threads must make each operation atomic, for example with a lock or a [compare-and-swap](/compare-and-swap/) loop on the single time of GCRA. For many servers, see [distributed rate limiting](/distributed-rate-limiting/). A [semaphore](/semaphore/) is the related object that limits how many units are in use at once, not how many start per unit of time; the two are often combined.

## Lower bounds

- **Time.** The token bucket and GCRA limits allow $\Theta(1)$ worst-case time per operation, which is optimal. So does the exact sliding window, with a ring of the last $n$ grants.
- **Memory per key for exact sliding windows.** With $W$ ticks per window, each exact limiter for the sliding window rule needs at least $\log_2 \binom{W}{n}$ bits per key in the worst case (proof on the [sliding window log](/sliding-window-log/) page). The token bucket limit needs only one or two numbers.
- **Memory for many keys.** An exact limiter for $k$ keys needs at least $k$ bits, even for a limit of one request per window. For each subset $A$ of the keys, let each key in $A$ send one request at time 0; then a request on each key at time 0 passes if and only if the key is not in $A$. The $2^k$ subsets need $2^k$ different states.
- **Approximate counts.** A [count-min sketch](/count-min-sketch/) keeps counts for many keys in less memory than $k$ counters, but it only overestimates. A limiter built on it never passes more than the limit, but it can refuse a key that shares cells with heavy keys, which breaks law 2.

## References
