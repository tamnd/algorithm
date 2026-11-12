---
tag: FAZPQ4
kind: algorithm
slug: alternating-bit-protocol
name: Alternating bit protocol
aliases:
- alternating bit
- ABP
area: systems/networking-algorithms
level: intro
summary: Stop-and-wait with a one-bit sequence number. It is correct over a FIFO channel that loses or duplicates packets, and it fails if the channel reorders them.
solves: [reliable-data-transfer]
model: asynchronous-model
complexity:
  vars: {m: the number of messages, T: "the time of one transmission plus one round trip", t: the timeout, p: the probability that one attempt fails}
  time: {best: Θ(m T), average: Θ(m (T + t p/(1 - p)))}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1969
  people: [K. A. Bartlett, R. A. Scantlebury, P. T. Wilkinson]
  note: Bartlett, Scantlebury and Wilkinson of the National Physical Laboratory described the protocol in a two-page note in the Communications of the ACM.
prereqs: [stop-and-wait]
see_also: [reliable-data-transfer, sliding-window-protocol, go-back-n, selective-repeat, fifo-delivery, safety-property, liveness-property, invariant]
sources:
  - paper: doi:10.1145/362946.362970
    title: K. A. Bartlett, R. A. Scantlebury and P. T. Wilkinson, A note on reliable full-duplex transmission over half-duplex links, Communications of the ACM 12(5), 1969
    locator: pages 260 to 261
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 22, Data Link Protocols (the alternating bit protocol, its correctness over FIFO channels, and the impossibility results for bounded headers over channels that reorder)
  - book: isbn:9780132126953
    title: Andrew S. Tanenbaum and David J. Wetherall, Computer Networks, fifth edition
    locator: Section 3.3, Elementary Data Link Protocols, and Section 3.4.1, A One-Bit Sliding Window Protocol
  - book: isbn:9780136681557
    title: James F. Kurose and Keith W. Ross, Computer Networking, A Top-Down Approach, eighth edition
    locator: Section 3.4.1 (rdt3.0, which the authors also call the alternating-bit protocol)
---

The alternating bit protocol (ABP) is [stop-and-wait](/stop-and-wait/) with a sequence number of one bit. The sender tags message $i$ with the bit $i \bmod 2$ and resends it until an ACK with the same bit comes back; the receiver delivers a packet only if its bit is the one it expects. Bartlett, Scantlebury and Wilkinson published it in 1969. It solves [reliable data transfer](/reliable-data-transfer/) over a channel that loses and duplicates packets but keeps their order, and it fails over a channel that can reorder them.

## In plain words

Stop-and-wait numbers each letter so that the receiver can spot an old copy. But one packet at a time is in flight, so the receiver only has to tell two letters apart: the one it waits for and the one before it. One bit is enough for that. The letters take turns: the first carries a 0, the second a 1, the third a 0 again.

The receiver keeps the bit that it waits for. If a letter carries that bit, the receiver keeps the letter and flips its bit. If it carries the other bit, it is an old copy, and the receiver throws it away. In both cases it replies with the bit of the letter.

This works only if the post never overtakes: an old copy must never arrive after a newer letter.

## The problem

The sender has messages $M[0], \ldots, M[m-1]$, and the receiver must deliver exactly this sequence. Each direction is a FIFO channel that can lose a packet or duplicate it, but delivers the packets that it does deliver in the order in which they were sent. This is the channel model of Lynch, Chapter 22. A packet with a bit error is dropped by a [checksum](/checksum/), so it counts as a loss. There is no bound on the delay, and the timer can expire early.

## The algorithm

```pseudo id=main
SENDER(M[0 .. m − 1])
L1  b ← 0; i ← 0
L2  while i < m do
L3      send DATA(b, M[i]); start the timer
L4      on ACK(a) with a = b: stop the timer and go to L6
L5      on ACK(a) with a ≠ b: ignore it; on a timeout: go to L3
L6      i ← i + 1
L7      b ← 1 − b

RECEIVER
L8  e ← 0                                     ▷ the bit of the next new message
L9  on receipt of DATA(c, d): if c = e then
L10     deliver d; e ← 1 − e
L11 send ACK(c)
```

Both sides keep one bit: the sender keeps $b = i \bmod 2$, and the receiver keeps $e = r \bmod 2$, where $r$ is the number of messages it has delivered. Over a FIFO channel, the receiver is always at $r = i$ or $r = i + 1$, so the only packets that can arrive carry the label $i - 1$ or $i$, and one bit tells them apart.

## Example

A failure over a channel that reorders. The first copy of DATA(0, m0) takes 8 time units, every other packet takes 1, and the timeout is 4.

| time | event |
|---|---|
| 0 | send DATA(0, m0); this copy is slow |
| 4 | timeout: send DATA(0, m0) again |
| 5 | the receiver delivers m0, $e = 1$, and sends ACK(0) |
| 6 | the sender takes ACK(0) and sends DATA(1, m1) |
| 7 | the receiver delivers m1, $e = 0$, and sends ACK(1) |
| 8 | the slow DATA(0, m0) arrives; its bit is $e$, so the receiver delivers m0 again and sends ACK(0) |
| 8 | the sender takes ACK(1) and sends DATA(0, m2) |
| 9 | the sender takes the ACK(0) of the old m0 as the ACK of m2 |
| 9 | DATA(0, m2) arrives; its bit is not $e$, so the receiver drops it |

The receiver delivered m0, m1, m0, and m2 is lost, after 4 transmissions. The slow packet overtook two newer packets. Over a FIFO channel this cannot happen. With lossy, duplicating FIFO channels (loss 0.3 and duplication 0.2 in each direction, 60 seeds), every run delivers the messages exactly once and in order. With random delays that reorder the packets, more than half of 40 seeds deliver a wrong sequence.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). It attaches a ghost label to each packet: the index $i$ of the message for a DATA packet, and the label of the answered packet for an ACK. Then an [invariant](/invariant/) holds: $r \in \{i, i+1\}$, the labels in each queue are non-decreasing and lie in $\{i - 1, i\}$, all DATA labels are $i$ once $r = i + 1$, and all ACK labels are $i - 1$ while $r = i$. From it, a DATA packet has the bit $e$ only when its label is $r$, so the receiver delivers $M[r]$ each time. An ACK has the bit $b$ only when its label is $i$, and then the receiver has $M[i]$. Liveness needs fair channels and a timer that expires. The invariant uses FIFO order at one point: the head of the data queue has the smallest label. The example breaks exactly this point.

## Complexity

The costs are the costs of [stop-and-wait](/stop-and-wait/): with link rate $R$, packet size $L$ and round-trip time RTT, the utilization is $(L/R)/(\mathrm{RTT} + L/R)$ without loss, and with independent failures of probability $p$ each message takes $1/(1-p)$ attempts on average. The header has 1 bit of sequence number, and each side keeps $O(1)$ state. Without loss, with delay 2 in each direction, each message takes 4 time units, so 4 messages finish at time 16.

## Properties

- **A bounded header.** One bit, against $\lceil \lg m \rceil$ bits for numbers $0, \ldots, m-1$.
- **Needs FIFO.** Over a channel that reorders, a bounded header is not enough for any protocol of this kind; Lynch, Chapter 22, proves impossibility results for this case.
- **Payload-independent.** The receiver never compares payloads, so equal messages, such as 25 copies of the same string, are delivered the right number of times.
- **Safety does not depend on the timer.** An early timeout costs only a transmission.

## Variants and improvements

- **Unbounded numbers.** [Stop-and-wait](/stop-and-wait/) with numbers $0, 1, 2, \ldots$ is correct even when the channel reorders.
- **Larger windows.** With $k$-bit numbers, a [sliding window protocol](/sliding-window-protocol/) keeps up to $2^k - 1$ packets in flight ([Go-Back-N](/go-back-n/)) or $2^{k-1}$ with a receive buffer ([selective repeat](/selective-repeat/)). ABP is the case $k = 1$ with a window of 1.
- **A bound on packet lifetime.** If the network guarantees that a packet dies after a fixed time, a sender that waits that long before it reuses a bit is safe even when packets are reordered. TCP relies on a maximum segment lifetime in this way.

## When to use it

Use ABP on a single physical link, a serial line or a bus, where the order of frames is kept and a small header matters. Do not use it over a network path that can reorder packets, such as an IP route; use large sequence numbers there.

## Pitfalls

- **Running it over a network that reorders.** A late duplicate with the same bit is taken for a new message, as in the example.
- **Comparing the payload instead of the bit.** Two different messages can be equal, so the payload cannot detect a duplicate.
- **Not acknowledging a duplicate.** After a lost ACK, the sender then waits forever.
- **Flipping the bit on a timeout.** Only an ACK with the right bit moves the sender to the next message.

## Implementations

## History

K. A. Bartlett, R. A. Scantlebury and P. T. Wilkinson of the National Physical Laboratory in the United Kingdom described the protocol in "A note on reliable full-duplex transmission over half-duplex links", Communications of the ACM, May 1969. It became a standard example for the verification of protocols. Lynch's textbook proves it correct over FIFO channels in Chapter 22, as an instance of a general data link protocol.

## References
