---
tag: R0TNQW
kind: algorithm
slug: stop-and-wait
name: Stop-and-wait protocol
aliases:
- stop-and-wait ARQ
- stop-and-wait protocol
area: systems/networking-algorithms
level: intro
summary: Send one numbered packet, wait for its acknowledgement or a timeout, and resend it on a timeout. The receiver drops duplicates by the number.
solves: [reliable-data-transfer]
model: asynchronous-model
complexity:
  vars: {m: the number of messages, T: "the time of one transmission plus one round trip", t: the timeout, p: the probability that one attempt fails}
  time: {best: Θ(m T), average: Θ(m (T + t p/(1 - p)))}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1964
  people: [R. J. Benice, A. H. Frey Jr.]
  note: Benice and Frey analyzed the throughput of three basic retransmission logics. The first is send and wait for confirmation.
prereqs: [reliable-data-transfer]
see_also: [alternating-bit-protocol, sliding-window-protocol, go-back-n, selective-repeat, round-trip-time-estimation, geometric-distribution, two-generals-problem]
sources:
  - book: isbn:9780136681557
    title: James F. Kurose and Keith W. Ross, Computer Networking, A Top-Down Approach, eighth edition
    locator: Section 3.4.1, Building a Reliable Data Transfer Protocol (rdt3.0 and the utilization of a stop-and-wait sender)
  - book: isbn:9780123850591
    title: Larry L. Peterson and Bruce S. Davie, Computer Networks, A Systems Approach, fifth edition
    locator: Section 2.5.1, Stop-and-Wait
  - book: isbn:9780132126953
    title: Andrew S. Tanenbaum and David J. Wetherall, Computer Networks, fifth edition
    locator: Section 3.3, Elementary Data Link Protocols (the stop-and-wait protocol for an error-free channel, and for a noisy channel)
  - paper: doi:10.1109/MCOM.1984.1091865
    title: Shu Lin, Daniel J. Costello Jr. and Michael J. Miller, Automatic-repeat-request error-control schemes, IEEE Communications Magazine 22(12), 1984
    locator: the section on stop-and-wait ARQ
  - paper: "R. J. Benice and A. H. Frey Jr., An analysis of retransmission systems, IEEE Transactions on Communication Technology 12(4), 1964"
    title: R. J. Benice and A. H. Frey Jr., An analysis of retransmission systems, 1964
    locator: pages 135 to 145
---

Stop-and-wait is the simplest protocol for [reliable data transfer](/reliable-data-transfer/) over a channel that loses packets. The sender sends one numbered packet, then waits for an acknowledgement (ACK) with that number; if a timer expires first, it sends the packet again. The receiver uses the number to drop duplicates, so each message is delivered exactly once and in order. It is correct over a channel that loses, duplicates, delays and reorders packets, but only one packet is on the link at a time, so the link is idle for most of each round trip.

## In plain words

You post a letter and wait for a reply that says "got letter 7". If no reply comes after some time, you post a copy of letter 7. When the reply comes, you post letter 8.

Each letter carries its number. This is necessary because a reply can get lost. Then you post a copy, and the receiver gets letter 7 two times. The number tells the receiver that the second one is old, so it throws it away and replies again. Without the number, the receiver reads the same letter two times.

The method is simple and correct, but slow on a long or fast link. The sender spends almost all its time waiting for replies instead of sending.

## The problem

The sender has messages $M[0], \ldots, M[m-1]$, and the receiver must deliver exactly this sequence to its user: each message once, in order. The channel model is the one of [reliable data transfer](/reliable-data-transfer/): in each direction, a packet can be lost, copied, delayed for any finite time, or reordered. Bit errors are found by a [checksum](/checksum/), and the packet is then dropped. There is no bound on the delay, so this is the [asynchronous model](/asynchronous-model/), and the timer is only a hint: it can expire too early.

## The algorithm

Here the numbers are the integers $0, 1, 2, \ldots$ with no bound. The [alternating bit protocol](/alternating-bit-protocol/) is the same method with a 1-bit number, which needs a channel that keeps the order of packets.

```pseudo id=main
SENDER(M[0 .. m − 1])
L1  for i ← 0 to m − 1 do
L2      send DATA(i, M[i]); start the timer
L3      wait for ACK(i) or a timeout
L4      if the timeout came first then go to L2
L5      stop the timer                         ▷ an ACK(j) with j ≠ i is ignored

RECEIVER
L6  r ← 0                                      ▷ the number of the next new message
L7  on receipt of DATA(s, d) do
L8      if s = r then deliver d; r ← r + 1
L9      send ACK(s)                            ▷ also for a duplicate
```

Line L9 acknowledges a duplicate too. This is necessary: a duplicate arrives when the ACK of the first copy was lost or late, and the sender waits for an ACK. Line L5 drops an ACK with a wrong number. Such an ACK is a late copy of an earlier ACK, and if the sender took it as an ACK of the current packet, it could skip a message that was lost.

## Example

Three messages. The transmission of a packet takes 1 time unit, each direction has a delay of 2, and the timeout is 8, counted from the start of the transmission. The first copy of DATA(1) is lost, and the first ACK(2) is lost.

| time | sender | receiver |
|---|---|---|
| 0 | send DATA(0, m0) | |
| 3 | | deliver m0, $r = 1$, send ACK(0) |
| 5 | ACK(0): send DATA(1, m1), lost | |
| 13 | timeout: send DATA(1, m1) again | |
| 16 | | deliver m1, $r = 2$, send ACK(1) |
| 18 | ACK(1): send DATA(2, m2) | |
| 21 | | deliver m2, $r = 3$, send ACK(2), lost |
| 26 | timeout: send DATA(2, m2) again | |
| 29 | | $s = 2 \ne r$: duplicate, send ACK(2) |
| 31 | ACK(2): done | |

The sender made 5 transmissions, and the receiver delivered m0, m1, m2. Without numbers, a lost ACK(0) makes the receiver deliver m0, m0, m1, m2.

## Correctness

The proof is in [the correctness proof](proofs/correctness.md). An induction over the steps shows three facts: each DATA$(s, d)$ that was sent has $s \le i$ and $d = M[s]$; the counters satisfy $i \le r \le i + 1$; and each ACK$(s)$ that was sent has $s \lt r$. The receiver delivers only DATA$(r, d)$ and then adds 1 to $r$, so it delivers $M[0], M[1], \ldots$ in order and each one once. These are [safety properties](/safety-property/), and they hold for every loss pattern and every timeout, also an early one. Termination is a [liveness property](/liveness-property/). It needs a fair channel: a packet that is sent again and again eventually arrives. A channel that loses every packet stops every protocol.

## Complexity

The model has a link of rate $R$ bits per second, packets of $L$ bits, and a round-trip time RTT. The size of an ACK and the processing time are 0. Without loss, one message takes $T = L/R + \mathrm{RTT}$, and the sender transmits for $L/R$ of it. Its utilization is

$$U = \frac{L/R}{\mathrm{RTT} + L/R}.$$

- A 1500-byte packet ($L = 12000$ bits) on a 100 Mbit/s link with RTT 10 ms: $L/R = 0.12$ ms and $U = 0.12/10.12 = 3/253 \approx 0.0119$. The throughput is $U R \approx 1.19$ Mbit/s on a 100 Mbit/s link.
- The same packet at 1 Gbit/s with RTT 30 ms: $L/R = 0.012$ ms and $U = 1/2501 \approx 0.0004$.

If each attempt fails with probability $p$, independently, the number of attempts per message has the [geometric distribution](/geometric-distribution/) with mean $1/(1-p)$. With loss probability 0.25 on the data packets only, each message takes $4/3$ transmissions on average. A failed attempt costs the timeout $t$ and the good one costs $T$, so the expected time per message is $T + t\,p/(1-p)$, if $t \ge T$. There is no worst-case bound, because the channel can lose any number of packets in a row. Each side keeps $O(1)$ state: one message, one number and one timer.

## Properties

- **Correct under reordering.** With unbounded numbers, a late or reordered packet is recognized as old by its number.
- **Safety does not depend on the timer.** An early timeout only costs an extra transmission.
- **One packet in flight.** The window has size 1, so throughput is at most $L/(\mathrm{RTT} + L/R)$.
- **Flow control for free.** The receiver controls the rate, because the sender waits for each ACK.

## Variants and improvements

- **Alternating bit protocol.** A 1-bit number, correct over a channel that keeps the order of packets. See [alternating bit protocol](/alternating-bit-protocol/).
- **Negative acknowledgements.** The receiver sends a NAK for a damaged packet, so the sender resends at once and does not wait for the timeout. Kurose and Ross build up rdt2.0 and rdt2.1 in this way, before they add the timer of rdt3.0.
- **Sliding window.** Keep up to $N$ packets in flight to fill the link: [sliding window protocol](/sliding-window-protocol/), [Go-Back-N](/go-back-n/) and [selective repeat](/selective-repeat/).
- **An adaptive timeout.** Set the timer from measured round-trip times: [round-trip time estimation](/round-trip-time-estimation/).

## When to use it

Use stop-and-wait when the round-trip time is small compared to the transmission time of a packet, so that $U$ is near 1, or when the code must be very small. Examples are a serial line, a bus to a peripheral, and a bootloader. TFTP uses stop-and-wait. On a long or fast link, use a sliding window.

## Pitfalls

- **No sequence number.** A lost ACK then makes the receiver deliver a duplicate, as in the example.
- **No ACK for a duplicate.** If the receiver drops a duplicate in silence, the sender resends forever after a lost ACK.
- **Taking any ACK as the current one.** A late ACK of an earlier packet must be ignored (line L5).
- **A fixed timeout.** A timeout below the round-trip time doubles the traffic, and a timeout far above it makes each loss slow.
- **Expecting more from the protocol.** No protocol over a lossy channel can make both sides know that the last message arrived. This is the [two generals problem](/two-generals-problem/). Stop-and-wait gives the sender this knowledge, but the receiver does not know whether its last ACK arrived.

## Implementations

## History

Benice and Frey analyzed the throughput of three basic retransmission logics in 1964; the first is "send and wait for confirmation". Later surveys, such as Lin, Costello and Miller (1984), call the three schemes stop-and-wait, go-back-N and selective repeat. The textbooks of Tanenbaum and of Kurose and Ross build the protocol step by step: first a perfect channel, then a channel with bit errors, then a channel that also loses packets.

## References
