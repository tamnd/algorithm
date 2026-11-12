---
tag: 5CM6Z2
kind: algorithm
slug: sliding-window-counter
name: Sliding window counter
aliases:
- sliding window approximation
- weighted sliding window
area: systems/rate-limiting
level: intro
summary: Estimate the requests of the last w seconds as the current window count plus the previous one, weighted by its overlap. Three numbers per key; at most 2n - 1 per window.
solves: [rate-limiting-problem]
model: word-ram
complexity:
  vars: {m: the number of requests on one key, k: the number of active keys}
  time: {worst: Θ(m)}
  space: {extra: Θ(k)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [fixed-window-counter, sliding-window-log]
see_also: [fixed-window-counter, sliding-window-log, token-bucket, gcra, rate-limiter, distributed-rate-limiting, exponential-histogram, sliding-window-model]
sources:
  - url: "https://blog.cloudflare.com/counting-things-a-lot-of-different-things/"
    title: Cloudflare, How we built rate limiting capable of scaling to millions of domains, Cloudflare blog, 2017
    locator: the sliding window estimate rate = previous count times the overlap plus the current count, and the measurement on 400 million requests from 270,000 sources
  - url: "https://www.figma.com/blog/an-alternative-approach-to-rate-limiting/"
    title: Nikrad Mahdi, An alternative approach to rate limiting, Figma engineering blog, 2017
    locator: the sliding window counter with sub-windows of 1/60 of the window
  - book: isbn:9798664653403
    title: Alex Xu, System Design Interview, An Insider's Guide, Volume 1, 2020
    locator: Chapter 4, Design a rate limiter (the sliding window counter algorithm)
---

A sliding window counter is a [rate limiter](/rate-limiter/) that keeps two counts per key: the requests that passed in the previous aligned window and in the current one. At a time $t$ that is a fraction $f$ into the current window, it estimates the count of the last $w$ seconds as $prev \cdot (1 - f) + cur$, which is exact if the previous window's requests were spread evenly. A request passes if the estimate plus one is at most $n$. It costs three numbers per key and $\Theta(1)$ time, like a [fixed window counter](/fixed-window-counter/), but it removes most of the burst at the window edge. It is not exact: a window of length $w$ can hold up to $2n - 1$ passed requests, and the counter can reject a request when the window is empty.

## In plain words

A fixed window counter forgets everything at the edge of each window. This method keeps one more number: how many requests passed in the window before. When a request comes, say a quarter of the way into the current window, the last full window of time is three quarters of the old window and the quarter of the new one that has passed. The counter does not know when the old requests came, so it guesses that they came at an even pace, and counts three quarters of them. It adds the requests of the current window and compares the sum with the limit.

When traffic is steady, the guess is close. When the old requests all came at the very end of the old window, or all at the start, the guess is wrong, in one direction or the other.

## The problem

The input is a sequence of requests at times $t_1 \le t_2 \le \cdots$ on one key. The limiter decides each request at its arrival. The target rule is the one of the [sliding window log](/sliding-window-log/): at most $n$ passed requests in any window $(s - w, s]$. The counter approximates this rule with constant memory. The arrival model is adversarial for the worst-case bounds below; the measured error is for real or random traffic.

## The algorithm

Each key has the index $C.k$ of the current aligned window $[kw, (k+1)w)$ (none at the start), and the counts $C.prev$ and $C.cur$.

```pseudo id=main
SLIDING-COUNTER-ALLOW(C, t)         ▷ a request at time t; times do not go back
L1  k ← ⌊t / w⌋
L2  if k = C.k + 1 then C.prev ← C.cur; C.cur ← 0          ▷ the next window
L3  else if C.k is none or k > C.k + 1 then C.prev ← 0; C.cur ← 0    ▷ a gap
L4  C.k ← k; f ← (t − k·w) / w                              ▷ how far into the window
L5  if C.prev · (1 − f) + C.cur + 1 ≤ n then
L6      C.cur ← C.cur + 1
L7      return ALLOW
L8  return REJECT
```

Line L2 rolls the windows forward by one. Line L3 handles a gap of more than one window, after which both counts are 0. Only passed requests are counted at line L6.

## Example

Let $n = 3$ and $w = 10$, with the same requests as on the [sliding window log](/sliding-window-log/) page. The estimate is the value before the test at line L5.

| time | window | $f$ | prev | cur | estimate | decision |
|---|---|---|---|---|---|---|
| 8 | 0 | 0.8 | 0 | 0 | 0 | pass |
| 9 | 0 | 0.9 | 0 | 1 | 1 | pass |
| 9.5 | 0 | 0.95 | 0 | 2 | 2 | pass |
| 10 | 1 | 0 | 3 | 0 | 3 | reject |
| 10.5 | 1 | 0.05 | 3 | 0 | 2.85 | reject |
| 11 | 1 | 0.1 | 3 | 0 | 2.7 | reject |
| 12 | 1 | 0.2 | 3 | 0 | 2.4 | reject |
| 15 | 1 | 0.5 | 3 | 0 | 1.5 | pass |
| 18 | 1 | 0.8 | 3 | 1 | 1.6 | pass |
| 19 | 1 | 0.9 | 3 | 2 | 2.3 | reject |
| 21 | 2 | 0.1 | 2 | 0 | 1.8 | pass |
| 25 | 2 | 0.5 | 2 | 1 | 2 | pass |
| 28.5 | 2 | 0.85 | 2 | 2 | 2.3 | reject |

Seven requests pass, as with the log, but not the same ones. The request at 15 passes because the counter assumes that half of the three requests of window 0 are already out of the window, but all three came at 8 to 9.5 and are still in it. So the window $(8.5, 18.5]$ holds four passed requests: 9, 9.5, 15 and 18. In the other direction, the request at 28.5 is rejected, although only 21 and 25 passed in $(18.5, 28.5]$ and the exact rule allows a third.

## Correctness

The full proof is below. Lemma 1 shows that the fields hold the counts of the previous and current aligned windows. Then:

- **Aligned windows.** Each aligned window holds at most $n$ passed requests, because the estimate is at least $cur$. So over many windows the rate is at most $n/w$, and the output fits a [token bucket](/token-bucket/) with rate $n/w$ and depth $2n$.
- **Sliding windows.** Each window of length $w$ holds at most $2n - 1$ passed requests. A window $(s - w, s]$ lies in two aligned windows. If $p$ requests passed in the earlier one and $c$ in the later one up to $s$, the last of the $c$ passed at a fraction $f$ with $p(1-f) + c \le n$, so the total is at most $p + c \le n + pf < 2n$.
- **The bound is reached.** $n$ requests at $w - w/(2n)$ and then $n$ at $2w - w/n$: all of the first group and $n - 1$ of the second pass, and all $2n - 1$ lie within one window of length $w$. For $n = 10$ and $w = 60$, this is 10 requests at time 57 and 10 at time 114, of which 19 pass.
- **Rejects too much as well.** With $n = 10$ and $w = 60$, 10 requests at time 0 and one at time 61: the estimate is $10 \cdot 59/60 \approx 9.83$, so the request is rejected, although no passed request lies in $(1, 61]$.

So the worst case is between the [fixed window counter](/fixed-window-counter/) ($2n$) and the [sliding window log](/sliding-window-log/) ($n$), and the counter is neither sound nor tight for the sliding rule. Both errors come from the assumption that the previous window was uniform.

## Complexity

In the word RAM, with times and counts in words:

- **Time.** Each call runs lines L1 to L8 once: $\Theta(1)$ in the worst case per request, so $\Theta(m)$ for $m$ requests on one key.
- **Space.** Three numbers per key, so $\Theta(k)$ for $k$ active keys. A key with no request in the last two windows can be deleted.

## Properties

- **Online and deterministic.** Each decision uses only the past.
- **Approximate.** Worst case $2n - 1$ in a window of length $w$; it can also reject when the exact rule allows.
- **Close on steady traffic.** Cloudflare reported that on 400 million requests from 270,000 sources, 0.003% of requests were wrongly allowed or rate limited, with an average difference of 6% between the real rate and the estimate. In our seeded test with $n = 100$, $w = 60$ and about 90 requests per window, 60 of 10,000 decisions differ from the log (0.6%). Under overload of 110 and 150 requests per window, the totals passed differ from the log by less than 0.5%, but 13% and 32% of the single decisions differ, because the two methods pass different requests.
- **No edge reset.** The quota comes back smoothly over the window instead of all at once.

## Variants and improvements

- **Sub-windows.** Count in $s$ sub-windows of length $w/s$, at the cost of $s$ counters per key. If the sum covers the current sub-window and the $s$ before it, it covers all of the last $w$ seconds and some more. Then no window of length $w$ gets more than $n$ passed requests, and the only error is to reject too much. Figma uses sub-windows of 1/60 of the window and states that it prefers a limiter that is a little too strict.
- **Increment then compare.** In a shared store, increment $cur$ at once and compare after. The rejected requests then count too, which makes the limiter stricter for clients that keep retrying.
- **Integer weights.** Keep $f$ in thousandths and compare $prev \cdot (1000 - f') + 1000 \cdot (cur + 1) \le 1000 n$ in integers, to avoid floating point.
- **[Token bucket](/token-bucket/) or [GCRA](/gcra/).** If the goal is "rate $r$ with a burst of $b$" and not a window, these are exact in one or two numbers.

## When to use it

Use a sliding window counter when the rule is stated as "$n$ requests per $w$ seconds", the traffic is many clients with roughly steady rates, and a log per key would use too much memory. Cloudflare chose it for this reason. When the limit must hold exactly in every window, for example for login attempts, use a [sliding window log](/sliding-window-log/). When a stated burst is enough, use a [token bucket](/token-bucket/) or [GCRA](/gcra/).

## Pitfalls

- **Forgetting the gap case.** If line L3 is missing, a request after a gap of two windows uses the stale count of an old window as $prev$, and rejects without reason.
- **Assuming exactness.** The limit $n$ can be exceeded by up to $n - 1$ in a window of length $w$. If $n$ per $w$ is a hard capacity, set the limit lower or use an exact method.
- **Counting rejected requests in $prev$.** Then a client that was blocked in the last window starts the new one with a high estimate, and stays blocked longer.
- **Window edges in different servers.** As for the fixed window counter, each server computes $\lfloor t/w \rfloor$ from its own clock. Take the time from one place.
- **Floating point.** The test $prev(1 - f) + cur + 1 \le n$ at equality depends on rounding. Use integer or fraction arithmetic, as the implementation here does.

## Implementations

The Python version keeps $f$ as a `Fraction`, so the estimate at line L5 is exact. The tests check the table above, check on seeded random inputs that each aligned window holds at most $n$ and each window of length $w$ at most $2n - 1$, check the worst case of $2n - 1$ for $n$ from 1 to 11, check the request at time 61 that the counter rejects and the log passes, and compare the counter with the log on three seeded random loads.

## History

Cloudflare described the method in 2017 for its rate limiting service, with the formula that weights the previous count by the part of the previous window still inside the last minute, and with the measured error on real traffic. In the same year Figma described a variant that sums many small fixed windows. Xu's 2020 book on system design presents it as the compromise between the [fixed window counter](/fixed-window-counter/) and the [sliding window log](/sliding-window-log/).

## References
