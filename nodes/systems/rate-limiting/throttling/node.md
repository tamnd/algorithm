---
tag: QHVA41
kind: concept
slug: throttling
name: Throttling
aliases:
- request throttling
- adaptive throttling
area: systems/rate-limiting
level: intro
summary: "Slowing a client or an operation on purpose, by delay or by a lower sending rate, to keep it within its share. Includes client-side adaptive throttling, CPU bandwidth limits and Retry-After."
prereqs: [rate-limiter]
see_also: [token-bucket, traffic-shaping, admission-control, backpressure, load-shedding, exponential-backoff, distributed-rate-limiting, completely-fair-scheduler]
sources:
  - book: isbn:9781491929124
    title: "Betsy Beyer, Chris Jones, Jennifer Petoff and Niall Richard Murphy (editors), Site Reliability Engineering, How Google Runs Production Systems, O'Reilly, 2016"
    locator: "Chapter 21, Handling Overload, by Alejandro Forero Cuervo: the section Client-Side Throttling (requests and accepts over the last two minutes, the client request rejection probability with the multiplier K, K = 2 preferred, K = 1.1 more aggressive) and the per-client retry budget"
  - url: https://sre.google/sre-book/handling-overload/
    title: "Site Reliability Engineering, Chapter 21, Handling Overload (online edition)"
    locator: Section Client-Side Throttling
  - url: https://docs.kernel.org/scheduler/sched-bwc.html
    title: "The Linux Kernel documentation, CFS Bandwidth Control"
    locator: "The quota and period of a task group (cpu.cfs_quota_us and cpu.cfs_period_us, default period 100 ms), throttled threads, and the Examples"
  - url: https://www.rfc-editor.org/rfc/rfc6585
    title: "Mark Nottingham and Roy Fielding, RFC 6585, Additional HTTP Status Codes, April 2012"
    locator: "Section 4 (429 Too Many Requests, which may include Retry-After)"
  - url: https://www.rfc-editor.org/rfc/rfc9110
    title: "Roy Fielding, Mark Nottingham and Julian Reschke (editors), RFC 9110, HTTP Semantics, June 2022"
    locator: "Section 10.2.3 (Retry-After) and Section 15.6.4 (503 Service Unavailable)"
---

Throttling is the deliberate slowing of a client, a task or an operation so that it stays within a share of a resource. Where a [rate limiter](/rate-limiter/) answers each request with yes or no, a throttle usually makes the work wait or makes the sender send less: it delays a request until a token is free, pauses a process until its next CPU period, or tells a client to come back later. The word also covers client-side adaptive throttling, in which a client that sees many rejections from its backend rejects some of its own requests before it sends them. Throttling does not lose the work that it delays, but the caller pays in latency.

## In plain words

A water tap with a flow limiter does not refuse water. It lets the water through more slowly. Throttling is the same idea for computer work: it slows a busy user or program down so that it does not take more than its share.

There are a few ways to do it. A server can hold a request for a moment before it handles it. An operating system can pause a program that has used up its CPU time for this tenth of a second. A server can answer "too many requests, try again in a minute".

A client can also throttle itself. If the server keeps saying "no", the client starts to drop some of its own requests at home, so it does not waste the server's time with requests that would fail.

## The idea

**Delay instead of reject.** A throttle keeps the work and changes its timing. A [token bucket](/token-bucket/) used as a [traffic shaper](/traffic-shaping/) holds each request until a token is free: with rate $r$ and depth $b$, the output fits $b + r\tau$ in every interval of length $\tau$, and no request is lost while the queue has room. A rate limiter with the same bucket rejects the requests that do not fit. The shaper adds delay, the limiter adds failures.

**The resource keeps the share.** In CPU bandwidth control, Linux gives a group of tasks a quota of CPU time per period (by default 100 ms). When the group has used its quota, its threads are throttled and do not run again until the next period. The tasks are not killed and lose no work; they finish later.

**The server asks the client to slow down.** HTTP status 429 Too Many Requests (RFC 6585, Section 4) and 503 Service Unavailable can carry a Retry-After header (RFC 9110, Section 10.2.3) with the number of seconds to wait. A client that waits as told, or uses [exponential backoff](/exponential-backoff/) when no time is given, throttles itself on the server's signal.

**Client-side adaptive throttling.** The SRE book (Chapter 21) describes a client that rejects some of its own requests when its backend is overloaded. Rejecting a request at the backend still costs the backend work, and a client that keeps sending requests that will be rejected wastes that work. Each client keeps two counts over the last two minutes:

- **requests**: the number of requests that the application tried to send, including those that the throttle rejected locally,
- **accepts**: the number of requests that the backend accepted.

Each new request is rejected locally with probability

$$p = \max\left(0,\ \frac{\text{requests} - K \cdot \text{accepts}}{\text{requests} + 1}\right),$$

with a multiplier $K$ that the book sets to 2 by default. The formula is an image in the online book; the form above is the one used by the implementations that follow the book.

- **No throttling while the backend accepts enough.** If requests $\le K \cdot$ accepts, then $p = 0$.
- **The bound on what is sent.** With $R$ requests and $a$ accepts, the expected number sent is $R(1 - p) = R \cdot \frac{K a + 1}{R + 1} < K a + 1$ whenever $p > 0$. So a client sends at most about $K$ times what the backend accepts, however many requests the application makes. With $K = 2$, the backend can spend work on about one rejection for each request that it accepts.
- **The choice of $K$.** A smaller $K$, such as 1.1, wastes less backend work: about one rejection for every 10 accepted requests. A larger $K$ lets more requests through, and the book prefers $K = 2$ because the clients then learn sooner that the backend has recovered.
- **Locally rejected requests still count.** They raise requests and not accepts, so the rejection probability grows with the demand of the application. The book says this is the intended behavior.

**A heuristic.** Adaptive throttling has no worst-case guarantee on the load of the backend. It reacts to a measured ratio over a window, so a backend with many clients can still get a burst before the counts catch up, and each client decides alone. The bound above holds per client, in expectation, for given counts.

**What throttling is not.**

- **[Rate limiting](/rate-limiter/)** rejects the requests above an agreed rate. Many systems use the two words for the same thing, but a throttle in the narrow sense delays or reduces, and a limiter refuses.
- **[Backpressure](/backpressure/)** is driven by the consumer's free buffer space. A throttle is driven by a share, a quota or the rejection rate, even when the consumer has room.
- **[Admission control](/admission-control/)** decides at the door whether new work can enter. Adaptive client-side throttling acts as an admission controller at the source.
- **[Load shedding](/load-shedding/)** drops work in an overloaded server. Throttling slows the work before the server is overloaded.

## Examples

**Adaptive throttling.** With $K = 2$ and 300 accepts in the last two minutes:

| requests | rejection probability $p$ | expected requests sent |
| --- | --- | --- |
| 400 | 0 | 400 |
| 600 | 0 | 600 |
| 1000 | $400/1001 \approx 0.3996$ | $\approx 600.4$ |
| 3000 | $2400/3001 \approx 0.7997$ | $\approx 600.8$ |

The number sent stays just above $K \cdot \text{accepts} = 600$, however large the demand. With $K = 1.1$ and the same 300 accepts, the client already rejects $70/401 \approx 17.5$ percent at 400 requests and sends about 330 at every level of demand in the table. The numbers come from the formula with exact fractions.

**CPU bandwidth.** A group has a quota of 50 ms per period of 100 ms, half a CPU. A job that needs 200 ms of CPU time runs for 50 ms in each of the periods that start at 0, 100 and 200 ms, and finishes 50 ms into the period that starts at 300 ms, at 350 ms of wall time. Without the throttle it would finish at 200 ms.

**A shaping throttle.** A token bucket with rate 5 per second and depth 1 delays 10 requests that come at time 0 to the times 0, 0.2, 0.4, and so on up to 1.8 s. A limiter with the same bucket admits the first request and rejects the other nine.

**Retry-After.** A server that allows 50 requests per hour per user answers the 51st with status 429 and `Retry-After: 3600`, the example of RFC 6585. A client that follows the header waits an hour instead of retrying at once.

## Where it is used

- **RPC clients at Google.** Client-side adaptive throttling as in the SRE book, together with per-request retry limits and a per-client retry budget.
- **Operating systems.** CPU bandwidth control of cgroups, I/O throttling of block devices, and limits on the bandwidth of a network interface by [traffic shaping](/traffic-shaping/).
- **Web APIs.** Status 429 with Retry-After, and client libraries that back off and retry later.
- **Distributed systems.** A shared quota for a fleet of clients, set by [distributed rate limiting](/distributed-rate-limiting/), with each client slowing down to its share.
- **Hardware.** Processors lower their clock frequency when they get too hot or use too much power. This is also called throttling: the work goes on at a lower speed.

## References
