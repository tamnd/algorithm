---
tag: PSJD1J
kind: algorithm
slug: token-bucket
name: Token bucket
aliases:
- token bucket meter
- token bucket algorithm
- token bucket policer
area: systems/rate-limiting
level: intro
summary: Tokens arrive at rate r into a bucket of depth b. A packet of size L passes if L tokens are there, and takes them. Its output fits r t + b.
solves: [rate-limiting-problem]
model: word-ram
complexity:
  vars: {n: the number of requests on one key}
  time: {worst: Θ(n)}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [rate-limiting-problem]
see_also: [leaky-bucket-meter, gcra, leaky-bucket-queue, burst-tolerance, traffic-policing, traffic-shaping, rate-limiter, sliding-window-log]
sources:
  - book: isbn:9783540421849
    title: Jean-Yves Le Boudec and Patrick Thiran, Network Calculus, A Theory of Deterministic Queuing Systems for the Internet, Springer LNCS 2050, 2001
    locator: Chapter 1, Section 1.2.1 (arrival curves) and Section 1.2.2 (leaky bucket and GCRA; the book calls the token bucket a leaky bucket controller)
  - paper: doi:10.1109/18.61109
    title: Rene L. Cruz, A calculus for network delay, Part I, Network elements in isolation, IEEE Transactions on Information Theory 37(1), 1991, pages 114 to 131
    locator: the (sigma, rho) burstiness constraint on a traffic stream
  - url: "https://www.rfc-editor.org/rfc/rfc2215"
    title: Scott Shenker and John Wroclawski, RFC 2215, General Characterization Parameters for Integrated Service Network Elements, 1997
    locator: the TOKEN_BUCKET_TSPEC parameter (rate r, bucket depth b, and the conformance rule)
  - book: isbn:9780132126953
    title: Andrew S. Tanenbaum and David J. Wetherall, Computer Networks, fifth edition
    locator: Chapter 5, Section 5.4 (quality of service, traffic shaping with leaky and token buckets)
---

A token bucket is a [rate limiter](/rate-limiter/) with two numbers: a rate $r$ and a depth $b$. Tokens drip into the bucket at rate $r$ until it holds $b$; a packet of size $L$ passes if the bucket holds at least $L$ tokens, and then takes them. The packets that pass fit the arrival curve $r\tau + b$: no interval of length $\tau$ holds more than $r\tau + b$ units, and each input that already fits passes whole. With a lazy refill from a timestamp it needs $\Theta(1)$ time per request and two numbers per key, which is why it is the default answer to the [rate limiting problem](/rate-limiting-problem/).

## In plain words

Think of a jar of coins. A machine drops a coin into the jar at a steady pace, but the jar has a fixed size, and coins that do not fit fall on the floor. Each request must pay with coins from the jar. If the jar has enough coins, the request pays and goes through. If not, it is refused and pays nothing.

A client that was quiet for a while finds a full jar, so it can send a short burst at once. A client that sends all the time can only go as fast as the coins drop. The program does not drop coins one by one. When a request comes, it looks at the clock, works out how many coins fell since the last request, and adds them in one step.

## The problem

The input is a sequence of requests (packets) at times $t_1 \le t_2 \le \cdots$, with sizes $L_k > 0$ (for plain request counting, $L_k = 1$). The bucket must decide each request at its arrival, without delay, so that the passed requests satisfy the $(r, b)$ arrival curve of the [rate limiting problem](/rate-limiting-problem/):

$$\sum_{k \text{ passed},\ t_k \in I} L_k \;\le\; r\,|I| + b \qquad \text{for each interval } I \text{ of the time line.}$$

The arrival model is adversarial: no assumption on the times. We assume $b \ge \max_k L_k$; a larger packet can never pass.

## The algorithm

Each key has a bucket with the parameters $r$ and $b$, the tokens $x$ and the time $last$ of the last update. At the start, $x = b$ and $last$ is the start time.

```pseudo id=main
TOKEN-BUCKET-ALLOW(B, t, L)          ▷ a packet of size L arrives at time t ≥ B.last
L1  B.x ← min(b, B.x + r · (t − B.last))      ▷ lazy refill, capped at the depth
L2  B.last ← t
L3  if B.x ≥ L then
L4      B.x ← B.x − L
L5      return CONFORM
L6  return NONCONFORM
```

Line L1 does the work of a timer that adds one token each $1/r$ seconds, but only when a packet comes. The cap at $b$ is the only place where tokens are lost. A packet that fails at line L3 takes no tokens, so it does not hurt the packets after it. This is the policer form: it passes or rejects at once. The [traffic shaping](/traffic-shaping/) form keeps the packet in a queue until line L3 holds.

## Example

Let $r = 1/2$ token per second, $b = 3$, and unit requests at the times below. The column $x$ is the value after line L1, and the last column is the value after the decision.

| time | $x$ after refill | decision | tokens left |
|---|---|---|---|
| 0 | 3 | pass | 2 |
| 0 | 2 | pass | 1 |
| 0 | 1 | pass | 0 |
| 0 | 0 | reject | 0 |
| 1 | 1/2 | reject | 1/2 |
| 2 | 1 | pass | 0 |
| 3 | 1/2 | reject | 1/2 |
| 4 | 1 | pass | 0 |
| 5 | 1/2 | reject | 1/2 |
| 9 | 5/2 | pass | 3/2 |
| 9 | 3/2 | pass | 1/2 |
| 9 | 1/2 | reject | 1/2 |
| 9 | 1/2 | reject | 1/2 |

The first three requests use the burst $b = 3$. After that the client gets one request each 2 seconds, the rate $r$. In the quiet time from 5 to 9 the bucket refills by 2 tokens, so two more requests pass at time 9. In the interval $[0, 9]$ seven requests pass, and $r \cdot 9 + b = 7.5$.

## Correctness

The full proof is below. Its key step is a closed form for the tokens: if $A$ is the set of passed packets, then the tokens after line L1 at packet $j$ are

$$x_j = \min\Big(b,\ \min_{i \in A,\ i < j}\big(b + r(t_j - t_i) - \textstyle\sum_{k \in A,\ i \le k < j} L_k\big)\Big),$$

by induction on $j$. The rejected packets do not appear, because a rejected packet changes no tokens and two capped refills equal one capped refill. Three results follow.

- **Soundness.** The passed packets conform: for passed $i \le j$, the size of the passed packets from $i$ to $j$ is at most $r(t_j - t_i) + b$. Since the first and last packets in an interval of length $\tau$ are at most $\tau$ apart, every interval of length $\tau$ gets at most $r\tau + b$ units.
- **Greedy.** A packet passes if and only if the passed packets before it, with it, still conform. So the bucket rejects a packet only when passing it would break the curve.
- **Tightness.** If the whole input conforms to $(r, b)$, every packet passes. So the token bucket is the tightest filter for $r\tau + b$: it never passes too much, and it never drops a packet of a conforming input.

## Complexity

In the word RAM, with the times and token counts held in words:

- **Time.** Each call runs lines L1 to L6 once, so it is $\Theta(1)$ in the worst case, and $n$ requests on one key cost $\Theta(n)$.
- **Space.** Each key needs two numbers, $x$ and $last$, so $\Theta(1)$ per key and $\Theta(k)$ for $k$ active keys. A key whose bucket would be full again can be deleted, because a new bucket starts full.

## Properties

- **Online.** Each decision uses only the past.
- **No delay.** A policer decides at once; it never holds a packet.
- **Burst then rate.** After a quiet period of at least $b/r$, a client can send $b$ units at once, then $r$ units per second.
- **Work at arrivals only.** No timer runs between requests.

## Variants and improvements

- **[Leaky bucket meter](/leaky-bucket-meter/).** A counter that drains at rate $r$ and fills with each passed packet, with limit $b$. Its level is $b - x$, so it makes the same decisions.
- **[GCRA](/gcra/).** It stores one timestamp, the theoretical arrival time, instead of $x$ and $last$. GCRA$(T, \tau)$ is a token bucket with $r = 1/T$ and $b = 1 + \tau/T$ for unit cells.
- **Token bucket shaper.** Keep the packets that fail line L3 in a FIFO queue, and send the head when the bucket has enough tokens. See [traffic shaping](/traffic-shaping/).
- **Dual bucket.** Two buckets in series, a peak bucket $(R, M)$ and a sustained bucket $(r, b)$, bound both the peak rate and the long-term rate. See [burst tolerance](/burst-tolerance/) for the largest burst at the peak rate.
- **Three-color markers.** The [single-rate three-color marker](/single-rate-three-color-marker/) and the [two-rate three-color marker](/two-rate-three-color-marker/) use two token buckets to mark packets green, yellow or red instead of dropping them.
- **Debt.** Some limiters let $x$ go below zero, so that a large request passes and the client then waits longer. The output then no longer fits $r\tau + b$.

## When to use it

Use a token bucket when you want a long-term rate with a bounded burst, and you want to decide each request at once. It is cheap, exact and easy to explain to users ("10 requests per second, bursts of 20"). Use a [sliding window log](/sliding-window-log/) when the rule must be "at most $n$ in any window of length $w$" with no refill inside the window. Use a [fixed window counter](/fixed-window-counter/) only when a burst of twice the limit at a window edge is acceptable. Use a [leaky bucket queue](/leaky-bucket-queue/) or a shaper when you must smooth the traffic instead of dropping it.

## Pitfalls

- **Update the time only on a pass.** If line L1 runs at each call but line L2 runs only on a pass, the refill after a rejected packet counts the same seconds twice. Run line L2 at each call.
- **Integer tokens.** With an integer $x$ and a small $r$, the term $r(t - last)$ rounds to 0 at each call, and a client that calls often never gets a token. Keep $x$ in fractions or in small units (for example nanotokens), or store a timestamp as GCRA does.
- **Clock going back.** A wall clock can jump back. Then $t - last < 0$ and line L1 removes tokens. Use a monotonic clock, and treat a negative difference as 0.
- **A packet larger than $b$.** It can never pass. Check $L \le b$ when the limiter is set up.
- **Start empty or full.** A bucket that starts empty rejects the first requests of a new key. Most limiters start full.
- **Races.** With many threads or many servers, read, refill and take must be one atomic step, for example with a [compare-and-swap](/compare-and-swap/) loop or a server-side script. See [distributed rate limiting](/distributed-rate-limiting/).

## Implementations

The Python version keeps the time and the tokens as `int` or `Fraction`, so the tests check the arrival curve exactly. The tests run every sequence of up to four packets of size 1 or 2 at integer times 0 to 4 for six pairs $(r, b)$. They check soundness, tightness and the greedy rule against the brute-force definition that tests every interval.

## History

Cruz in 1991 put the $(\sigma, \rho)$ burstiness constraint, a bound of $\sigma + \rho\tau$ on the traffic in each interval of length $\tau$, at the base of a calculus of network delays. The token bucket is the meter for this constraint. The Integrated Services specifications of the IETF, for example RFC 2215 in 1997, describe traffic by a token bucket with rate $r$ and depth $b$, and the ATM standards use the equivalent [GCRA](/gcra/). Le Boudec and Thiran give the general theory of arrival curves and of the leaky bucket controller in their book on network calculus.

## References
