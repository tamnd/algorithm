---
tag: 1P82FV
kind: concept
slug: traffic-shaping
name: Traffic shaping
aliases:
- traffic smoothing
area: systems/rate-limiting
level: intro
summary: Hold packets in a queue and send each one as soon as it fits a traffic profile, so the output conforms. Bursts become delay instead of loss, at the cost of a buffer.
prereqs: [token-bucket, leaky-bucket-queue]
see_also: [traffic-policing, leaky-bucket-queue, token-bucket, burst-tolerance, min-plus-convolution, packet-scheduling, congestion-control, backpressure]
sources:
  - book: isbn:9783540421849
    title: Jean-Yves Le Boudec and Patrick Thiran, Network Calculus, A Theory of Deterministic Queuing Systems for the Internet, Springer LNCS 2050, 2001
    locator: Section 1.5 (definitions of policer, shaper and greedy shaper; Theorem 1.5.1, the output of a greedy shaper is R ⊗ σ; Corollaries 1.5.1 and 1.5.2; Theorem 1.5.2, re-shaping does not increase delay or buffer requirements; Theorem 1.5.3, shaping conserves arrival constraints) and Theorem 1.4.2 (the delay bound)
  - url: "https://www.rfc-editor.org/rfc/rfc2475"
    title: Steven Blake, David L. Black, Mark A. Carlson, Elwyn Davies, Zheng Wang and Walter Weiss, RFC 2475, An Architecture for Differentiated Services, 1998
    locator: Section 1.2 (the definition of shaping) and Section 2.3.3.3 (shapers)
  - url: "https://www.rfc-editor.org/rfc/rfc2212"
    title: Scott Shenker, Craig Partridge and Roch Guerin, RFC 2212, Specification of Guaranteed Quality of Service, 1997
    locator: the section on policing (reshaping with a buffer, a token bucket and a peak rate regulator)
  - paper: doi:10.1145/2934872.2934873
    title: Tobias Flach, Pavlos Papageorge, Andreas Terzis, Luis Pedrosa, Yuchung Cheng, Tayeb Karim, Ethan Katz-Bassett and Ramesh Govindan, An Internet-wide analysis of traffic policing, ACM SIGCOMM 2016, pages 468 to 482
    locator: pacing and shaping as alternatives to policing
---

Traffic shaping enforces a traffic profile, such as a [token bucket](/token-bucket/) with rate $r$ and depth $b$, by delay instead of loss. Packets that do not fit the profile wait in a queue, and each one leaves as soon as it fits. The output then conforms to the profile. A *greedy* shaper sends every packet as early as the profile allows, and network calculus gives its output exactly: the min-plus convolution of the input with the shaping curve. Shaping costs a buffer and adds delay, but it turns a burst into a smooth stream that the next hop can take without loss. The other way to enforce a profile is [traffic policing](/traffic-policing/), which drops or marks the packets that do not fit.

## In plain words

A shaper is a waiting room in front of a narrow door. People who come in a crowd do not get sent away; they wait in line, and the door lets them through at a steady pace. Nobody is lost as long as the waiting room is big enough, but the people at the back of the crowd wait longer.

A program does the same when it calls a rate limiter and sleeps until it may go on. A client that sleeps before each request, so that it never goes over its quota, is shaping its own traffic.

## The idea

**Definitions.** RFC 2475 defines shaping as "the process of delaying packets within a traffic stream to cause it to conform to some defined traffic profile". Le Boudec and Thiran call a *shaper* with shaping curve $\sigma$ a device "that forces its output to have $\sigma$ as an arrival curve", and a *greedy shaper* "a shaper that delays the input bits in a buffer, whenever sending a bit would violate the constraint σ, but outputs them as soon as possible".

**The token bucket shaper.** Put a FIFO queue in front of a [token bucket](/token-bucket/). The head of the queue leaves when the bucket holds enough tokens for it, and takes them. With depth $b$ equal to one packet, this is the [leaky bucket queue](/leaky-bucket-queue/), which sends at a constant rate. A larger $b$ lets a burst of up to $b$ go at once and then holds the rest to rate $r$. RFC 2212 describes the same device: "Reshaping is done by combining a buffer with a token bucket and peak rate regulator", and "Reshaping entails delaying datagrams until they are within conformance of the TSpec."

**The output of a greedy shaper.** Let $R(t)$ be the input (the data that arrived by time $t$), and let $\sigma$ be a "good" shaping curve, such as $\sigma(\tau) = r\tau + b$ for $\tau > 0$ and $\sigma(0) = 0$. If the buffer is large enough and empty at the start, the output is (Theorem 1.5.1)

$$R^*(t) = (R \otimes \sigma)(t) = \inf_{0 \le s \le t} \big(R(s) + \sigma(t - s)\big),$$

a [min-plus convolution](/min-plus-convolution/). From it:

- **Service curve.** The greedy shaper offers $\sigma$ as a service curve (Corollary 1.5.1). So if the input has the arrival curve $\alpha$, the delay is at most the horizontal deviation $h(\alpha, \sigma)$ and the backlog at most the vertical deviation $v(\alpha, \sigma)$ (Theorems 1.4.1 and 1.4.2).
- **Buffer.** The backlog at time $t$ is exactly $\sup_{0 \le s \le t} \big(R(t) - R(s) - \sigma(t - s)\big)$ (Corollary 1.5.2).
- **Shaping keeps old limits.** If the input already had the arrival curve $\alpha$, the output still has it, and so it has $\min(\alpha, \sigma)$ (Theorem 1.5.3).
- **Re-shaping is free in the worst case.** A greedy shaper with a curve $\sigma \ge \alpha$ placed between two parts of a network does not increase the worst-case delay or backlog bounds of the whole path (Theorem 1.5.2). The book says "greedy shapers come for free". It does lower the burst that the next node sees.

**A useful case.** If the input fits a token bucket with rate $r$ and depth $b'$, and the shaper has the same rate $r$ and a smaller depth $b$, then $h(\alpha, \sigma) = (b' - b)/r$ and $v(\alpha, \sigma) = b' - b$. Removing $b' - b$ units of burst costs at most $(b' - b)/r$ of delay and $b' - b$ of buffer.

**Shaping compared with policing.** A shaper adds delay and needs a buffer, but loses no packet while the buffer has room. A [policer](/traffic-policing/) adds no delay and needs no buffer, but drops every packet out of profile. A shaper whose buffer is full must drop too, so a real shaper is a shaper and a policer in series. For TCP, shaping replaces runs of losses with a higher round-trip time; Flach and others proposed pacing and shaping as alternatives to policing for this reason.

## Examples

**A burst through a shaper.** A sender at 100 Mbit/s sends 20 packets of 1500 bytes back to back, one each 0.12 ms, into a token bucket shaper of 10 Mbit/s (1250 bytes per ms) with depth 15,000 bytes, full at the start. The [policing](/traffic-policing/) page shows that a policer with the same bucket drops 9 of them. The shaper sends them all:

| packet | arrives (ms) | leaves (ms) | delay (ms) |
|---|---|---|---|
| 0 to 10 | $0.12k$ | $0.12k$ | 0 |
| 11 | 1.32 | 2.4 | 1.08 |
| 12 | 1.44 | 3.6 | 2.16 |
| 15 | 1.8 | 7.2 | 5.4 |
| 19 | 2.28 | 12.0 | 9.72 |

Packets 0 to 10 use the burst of 15,000 bytes. After that the shaper sends one packet each 1.2 ms, the time to earn 1500 bytes of tokens. The whole burst of 30,000 bytes spans 2.28 ms, so it fits a token bucket with rate 1250 bytes per ms and depth $b' = 30{,}000 - 1250 \times 2.28 = 27{,}150$ bytes. The bound $(b' - b)/r = 12{,}150 / 1250 = 9.72$ ms is reached by the last packet. The fluid backlog bound is 12,150 bytes; with whole packets the queue peaks at 9 packets (13,500 bytes) at 2.28 ms, because a packet leaves only when all its 1500 tokens are there.

**Pay bursts only once.** A flow with curve $r\tau + b$ crosses two nodes with latencies $T_1$ and $T_2$. Without a shaper the flow leaves node 1 with burst $b + rT_1$, and node 2 needs a buffer of $b + r(T_1 + T_2)$. With a greedy re-shaper to $r\tau + b$ after node 1, node 2 needs only $b + rT_2$, and by Theorem 1.5.2 the end-to-end delay bound does not grow.

**A client that waits.** A batch job calls `acquire(1)` on a rate limiter of 10 requests per second before each call to an API, as with `WaitN` in Go's `golang.org/x/time/rate` or `acquire` in Guava. The job never gets a 429 answer: its own calls are shaped to the limit.

**Constant rate output.** The [leaky bucket queue](/leaky-bucket-queue/) with rate $r$ and room for $K$ packets is the shaper with depth one packet. Its output is perfectly even, and a packet waits at most $K/r$.

## Where it is used

- **Network egress.** Routers and hosts shape traffic to the rate of a slower link or of a contract, so that the provider's policer does not drop it. Linux has a token bucket filter queueing discipline for this.
- **DiffServ boundary nodes.** RFC 2475 lists shapers among the parts of a traffic conditioner, next to meters, markers and droppers.
- **ATM and Integrated Services.** Sources shape cells to their GCRA contract; RFC 2212 reshapes flows inside the network to their TSpec.
- **Sender pacing.** A TCP sender that paces its packets at the estimated rate, as in some modern congestion controls, shapes its own output. See [congestion control](/congestion-control/).
- **Clients of rate-limited APIs.** Client libraries wait before each call so that they stay under the server's limit, which turns rejections into delay. See [backpressure](/backpressure/) for the same idea inside a system.

## References
