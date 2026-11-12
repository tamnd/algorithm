---
tag: VM5NDN
kind: algorithm
slug: slow-start
name: Slow start
aliases:
- TCP slow start
area: systems/networking-algorithms
level: intro
summary: Start a TCP connection with a small congestion window and add one segment per ACK, so that the window doubles each round trip until a loss or the slow start threshold.
solves: [congestion-control]
model: asynchronous-model
complexity:
  vars: {w: the target window in segments, i: the initial window in segments, R: the round-trip time}
  time: {worst: Θ(R log(w/i))}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1988
  people: [Van Jacobson]
  note: Jacobson described slow start in Congestion avoidance and control in 1988. It came with the 4.3BSD Tahoe TCP.
prereqs: [congestion-control, aimd]
see_also: [tcp-tahoe, tcp-reno, fast-retransmit-fast-recovery, round-trip-time-estimation, jacobson-rto-estimation, exponential-backoff]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc5681"
    title: Mark Allman, Vern Paxson and Ethan Blanton, RFC 5681, TCP Congestion Control, 2009
    locator: Section 3.1 (the initial window, equations 2, 3 and 4, and the loss window) and Section 4.1 (restarting idle connections)
  - url: "https://www.rfc-editor.org/rfc/rfc3390"
    title: Mark Allman, Sally Floyd and Craig Partridge, RFC 3390, Increasing TCP's Initial Window, 2002
    locator: Section 1 (the upper bound min(4 MSS, max(2 MSS, 4380 bytes)))
  - url: "https://www.rfc-editor.org/rfc/rfc6928"
    title: Jerry Chu, Nandita Dukkipati, Yuchung Cheng and Matt Mathis, RFC 6928, Increasing TCP's Initial Window, 2013
    locator: Section 2 (the upper bound min(10 MSS, max(2 MSS, 14600 bytes)))
  - paper: doi:10.1145/52324.52356
    title: Van Jacobson, Congestion avoidance and control, ACM SIGCOMM 1988
    locator: pages 314 to 329 (the section on slow start and the appendix with the combined slow start and congestion avoidance)
  - book: isbn:9780136681557
    title: James F. Kurose and Keith W. Ross, Computer Networking, A Top-Down Approach, eighth edition
    locator: Section 3.7.1 (classic TCP congestion control, slow start)
---

Slow start is the phase of TCP [congestion control](/congestion-control/) in which the congestion window starts small and grows by one segment for each acknowledged segment. So the window doubles in each round trip, and the sender finds the capacity of the path in a number of round trips that is logarithmic in the window. Slow start ends at a loss or when the window reaches the threshold ssthresh, and then the [AIMD](/aimd/) increase of congestion avoidance takes over. RFC 5681 gives the standard rules, which this page follows.

## In plain words

A new connection does not know how fast the path is. If it sends all its data at once, it can flood a router. If it sends one packet at a time, a fast path stays empty for a long time.

Slow start sends a few packets first. Each time a packet is confirmed, the sender may send two new packets: one to replace it and one extra. So the number of packets in flight doubles in each round trip: a few, twice that, four times that, and so on. This finds even a very fast path after a small number of round trips. When a packet is lost, or the sender reaches a threshold from an earlier loss, it stops doubling and grows slowly.

## The problem

One TCP sender has a window cwnd: the bytes it may have sent and not yet seen acknowledged. It does not know the bandwidth-delay product of the path. It must raise cwnd from a safe small value to about the bandwidth-delay product, without a long phase of low rate and without a large burst at the start. After a timeout it must restart in the same safe way. The sender sees only the ACKs and the retransmission timer. The model is the TCP sender of RFC 5681, with the window in bytes and segments of SMSS bytes, the sender maximum segment size.

## The algorithm

The rules are RFC 5681, Section 3.1. Line L1 sets the initial window IW. Lines L2 to L5 run for each ACK that acknowledges $N > 0$ new bytes. Lines L6 and L7 run when the retransmission timer expires, with FlightSize the bytes in flight.

```pseudo id=main
INIT(SMSS)
L1  cwnd ← IW, ssthresh ← a very large value  ▷ IW from RFC 5681, 3390 or 6928

ON-ACK(N)                                      ▷ N new bytes acknowledged
L2  if cwnd < ssthresh then
L3      cwnd ← cwnd + min(N, SMSS)             ▷ slow start
L4  else
L5      cwnd ← cwnd + max(1, ⌊SMSS · SMSS / cwnd⌋)   ▷ congestion avoidance

ON-TIMEOUT(FlightSize)
L6  ssthresh ← max(⌊FlightSize / 2⌋, 2 · SMSS)
L7  cwnd ← SMSS                                ▷ the loss window: slow start again
```

The initial window in RFC 5681 is $2\,\text{SMSS}$ if $\text{SMSS} > 2190$, $3\,\text{SMSS}$ if $1095 < \text{SMSS} \le 2190$, and $4\,\text{SMSS}$ if $\text{SMSS} \le 1095$. RFC 3390 gives $\min(4\,\text{MSS}, \max(2\,\text{MSS}, 4380))$ bytes, and the experimental RFC 6928 gives $\min(10\,\text{MSS}, \max(2\,\text{MSS}, 14600))$ bytes. The first value of ssthresh should be very large, so the first slow start ends only at a loss.

Line L3 is the doubling. One round trip carries $\text{cwnd}/\text{SMSS}$ segments, each ACK adds one SMSS, so the window at the end of the round is twice the window at the start. Line L5 is the additive increase of congestion avoidance: about one SMSS per round trip. At $\text{cwnd} = \text{ssthresh}$, RFC 5681 lets the sender use either rule. This page uses line L5. A loss found by three duplicate ACKs is handled by [fast retransmit and fast recovery](/fast-retransmit-fast-recovery/), which set ssthresh with the same formula as line L6.

## Example

**Initial windows.** The three rules in bytes:

| SMSS (bytes) | RFC 5681 | RFC 3390 | RFC 6928 |
|---|---|---|---|
| 536 | 2144 | 2144 | 5360 |
| 1095 | 4380 | 4380 | 10950 |
| 1460 | 4380 | 4380 | 14600 |
| 2000 | 6000 | 4380 | 14600 |
| 4000 | 8000 | 8000 | 14600 |
| 9000 | 18000 | 18000 | 18000 |

RFC 5681 and RFC 3390 differ between 1095 and 2190 bytes: for SMSS 2000, RFC 5681 allows 3 segments, and RFC 3390 allows 4380 bytes, about 2.2 segments.

**A trace.** Take $\text{SMSS} = 1000$ bytes, $\text{IW} = 1000$ and $\text{ssthresh} = 8000$, one ACK per segment and no loss. The window at the start of each round trip is:

| round | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| cwnd | 1000 | 2000 | 4000 | 8000 | 8948 | 9803 | 10682 | 11580 | 12492 | 13416 |
| phase | SS | SS | SS | CA | CA | CA | CA | CA | CA | CA |

In round 3 the window equals ssthresh, so the 8 ACKs use line L5. They add 125, 123, 121, 119, 117, 116, 114 and 113 bytes, so the window becomes 8948. After that it grows by less than 1000 bytes per round trip, because the window in a round is not a multiple of SMSS and the sender sends only full segments.

**Delayed ACKs.** A receiver that sends one ACK for every two segments halves the number of ACKs. Then line L3 adds one SMSS per two segments, and the window grows by a factor of about 1.5 per round trip. From 10 segments of 1460 bytes, the window in segments is 10, 15, 23, 35, 53 and 80.

**Timeout.** With $\text{SMSS} = 1460$ and 40000 bytes in flight, lines L6 and L7 set $\text{ssthresh} = 20000$ and $\text{cwnd} = 1460$. With only 3000 bytes in flight, ssthresh is $\max(1500, 2920) = 2920$.

## Correctness

Line L3 adds at most one SMSS per ACK, and line L5 adds at least 1 byte and at most one SMSS per ACK. In the round model with one ACK per segment, a round that starts with $k$ full segments and stays below ssthresh ends with $2k$ segments. So from IW the window reaches a target $T$ after exactly $\lceil \log_2(T/\text{IW}) \rceil$ round trips. In congestion avoidance, a round adds at least 1 byte and at most one SMSS, as long as the window is at most $\text{SMSS}^2$ bytes. After a timeout, the window is one SMSS and ssthresh is at least two, so the sender is again in slow start. The proof has the details.

## Complexity

Each ACK and each timeout costs $\Theta(1)$ time and the state is two integers. The important cost is in round trips: to reach a window of $w$ segments from $i$ segments takes $\lceil \log_2(w/i) \rceil$ round trips. For a path of 100 Mbit/s and 40 ms, the bandwidth-delay product is about 342 segments of 1460 bytes. From 10 segments, slow start reaches it in $\lceil \log_2 34.2 \rceil = 6$ round trips. Congestion avoidance at one segment per round trip would take 332 round trips.

## Properties

- **Exponential growth.** The window doubles per round trip with one ACK per segment, and grows by about 1.5 with delayed ACKs.
- **Self-clocked.** New segments go out only when ACKs come back, so the sender cannot send faster than twice the rate at which the path delivered in the last round trip.
- **Bounded per ACK.** No ACK adds more than one SMSS, so a receiver that splits its ACKs cannot speed up the growth.
- **Not fair by itself.** Slow start only probes. Fairness comes from the decrease and from congestion avoidance.

## Variants and improvements

- **Appropriate byte counting (RFC 3465).** Increase by the bytes acknowledged, with a limit of $L \cdot \text{SMSS}$ per ACK. With $L = 2$ this makes up for delayed ACKs.
- **Larger initial windows.** RFC 3390 and RFC 6928 raise IW to save round trips for short transfers.
- **Restart after idle.** RFC 5681, Section 4.1: after an idle time longer than the retransmission timeout, set cwnd to $\min(\text{IW}, \text{cwnd})$ before sending.
- **Leaving slow start early.** Hybrid slow start, used with [CUBIC](/tcp-cubic/) in Linux, leaves slow start when the round-trip time starts to grow, before the first loss. Limited slow start (RFC 3742) grows more slowly when the window is very large.
- **Startup of BBR.** [BBR](/bbr-congestion-control/) also doubles its rate per round trip at the start, but it stops when the measured delivery rate stops growing, not at a loss.

## When to use it

Every standard TCP sender uses slow start at the start of a connection and after a timeout. It is the right tool when the sender has no estimate of the path capacity. When the sender has a good estimate, for example from an earlier connection on the same path, a larger initial window or pacing at the known rate saves round trips.

## Pitfalls

- **Counting ACKs instead of bytes in line L3.** If line L3 adds one SMSS for every ACK, whatever $N$ is, a receiver can split one ACK into many small ACKs and make the window grow much faster. The $\min(N, \text{SMSS})$ prevents this.
- **The overshoot at the end.** With a very large first ssthresh in line L1, the last round of slow start sends up to twice the capacity of the path. With a small buffer, about one half of that round can be lost. [TCP Reno](/tcp-reno/) then often needs a timeout to recover.
- **Using cwnd instead of FlightSize in line L6.** When the sender was limited by the application or by the receiver window, cwnd can be much larger than the data in flight. One half of cwnd is then too large a threshold.
- **A burst after idle.** A sender that keeps a large cwnd after a long idle time sends a full window at once. Restart from IW instead.

## Implementations

## History

Jacobson described slow start in his 1988 paper Congestion avoidance and control, together with congestion avoidance, and the algorithms went into the 4.3BSD Tahoe TCP. The name contrasts it with the older practice of sending a full receiver window at once. Stevens wrote the four algorithms (slow start, congestion avoidance, fast retransmit and fast recovery) into RFC 2001 in 1997. RFC 2581 replaced it in 1999, and RFC 5681 in 2009. RFC 3390 in 2002 and RFC 6928 in 2013 raised the initial window.

## References
