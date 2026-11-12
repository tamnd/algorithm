---
tag: 5PJZGD
kind: algorithm
slug: sliding-window-protocol
name: Sliding window protocol
aliases:
- sliding window ARQ
area: systems/networking-algorithms
level: intro
summary: Keep up to a window of unacknowledged packets in flight so that the link stays busy. With FIFO channels, send window plus receive window at most M sequence numbers is safe.
solves: [reliable-data-transfer]
model: asynchronous-model
complexity:
  vars: {m: the number of messages, w: the send window in packets, T: "the time of one transmission plus one round trip"}
  time: {best: Θ(m T/w + T)}
  space: {extra: Θ(w)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1974
  people: [Vinton G. Cerf, Robert E. Kahn]
  note: The TCP design of Cerf and Kahn used a window of bytes that the receiver allows the sender to have outstanding, with retransmission after a timeout.
prereqs: [stop-and-wait]
see_also: [go-back-n, selective-repeat, alternating-bit-protocol, flow-control, congestion-control, reliable-data-transfer, fifo-delivery]
sources:
  - book: isbn:9780123850591
    title: Larry L. Peterson and Bruce S. Davie, Computer Networks, A Systems Approach, fifth edition
    locator: Section 2.5.2, Sliding Window (the algorithm, finite sequence numbers and the rule SWS < (MaxSeqNum + 1)/2)
  - book: isbn:9780132126953
    title: Andrew S. Tanenbaum and David J. Wetherall, Computer Networks, fifth edition
    locator: Section 3.4, Sliding Window Protocols
  - book: isbn:9780136681557
    title: James F. Kurose and Keith W. Ross, Computer Networking, A Top-Down Approach, eighth edition
    locator: Section 3.4.2, Pipelined Reliable Data Transfer Protocols
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 22, Data Link Protocols
  - paper: doi:10.1109/TCOM.1974.1092259
    title: Vinton G. Cerf and Robert E. Kahn, A Protocol for Packet Network Intercommunication, IEEE Transactions on Communications 22(5), 1974
    locator: the sections on retransmission and duplicate detection, and on flow control
---

A sliding window protocol is a protocol for [reliable data transfer](/reliable-data-transfer/) that lets the sender have up to $w_s$ packets in flight that are not yet acknowledged. The receiver accepts up to $w_r$ packets ahead of the next one it expects, and sends cumulative acknowledgements. With $w_s = 1$ it is [stop-and-wait](/stop-and-wait/), with $w_r = 1$ it is close to [Go-Back-N](/go-back-n/), and with $w_r = w_s$ and one ACK per packet it is [selective repeat](/selective-repeat/). Over FIFO channels with sequence numbers modulo $M$, it is correct when $w_s + w_r \le M$, and this bound is tight.

## In plain words

Stop-and-wait sends one letter and waits for the reply. On a long link, the sender waits almost all the time. A sliding window lets the sender post several letters before the first reply comes. The letters that are posted but not yet confirmed form the window. When the oldest letter is confirmed, the window slides forward, and one more letter can go out.

The receiver keeps a window too: the letters that it can accept now, even out of order. It keeps early letters until the gap before them is filled, then hands them all over in order.

The letters carry numbers that wrap around, like the hours on a clock. The windows must be small enough that an old copy cannot be taken for a new letter with the same number.

## The problem

The sender has messages $M[0], \ldots, M[m-1]$, and the receiver must deliver exactly this sequence, each message once. A packet carries its index modulo $M$, so a header of $k$ bits gives $M = 2^k$. Each direction is a FIFO channel that may lose or duplicate packets, as for the [alternating bit protocol](/alternating-bit-protocol/). The aim is to keep the link busy: on a link of rate $R$ and round-trip time RTT, the sender must keep about $R \cdot \mathrm{RTT}$ bits in flight.

## The algorithm

The sender keeps $base$, the oldest packet without an ACK, and $next$, the next new packet. The receiver keeps $r$, the next packet that it must deliver, and a buffer for the packets $r, \ldots, r + w_r - 1$. ACK$(a)$ means "I have delivered every packet before $a$". There is one timer, for the packet $base$.

```pseudo id=main
SENDER(M[0 .. m − 1])
L1  base ← 0; next ← 0
L2  while next < m and next < base + ws do
L3      send DATA(next mod M, M[next]); start the timer if it is off; next ← next + 1
L4  on ACK(a):
L5      k ← (a − base) mod M
L6      if 1 ≤ k ≤ next − base then base ← base + k; stop the timer
L7          if base < next then start the timer; go to L2
L8  on a timeout:
L9      resend DATA(base mod M, M[base]); restart the timer

RECEIVER (r ← 0)
L10 on DATA(s, d): off ← (s − r) mod M
L11     if off < wr then store d at index r + off
L12     while the slot r is full do deliver it; r ← r + 1
L13     send ACK(r mod M)
```

Line L5 turns the number on the wire back into a distance from $base$. This needs $w_s < M$. Line L10 does the same at the receiver: a packet with $\mathit{off} < w_r$ lies in the window, and any other packet is an old copy or is too far ahead. Line L13 answers every packet, also a duplicate, so that a lost ACK is repaired by the next one.

## Example

Eight messages with $w_s = w_r = 4$ and $M = 8$. A transmission takes 1 time unit, the delay is 1 in each direction, and the timeout is 10. The first copy of packet 2 is lost.

| time | event |
|---|---|
| 0 to 3 | the sender sends packets 0, 1, 2, 3 (packet 2 is lost) |
| 2, 3 | the receiver delivers 0 and 1 and sends ACK(1) and ACK(2) |
| 3, 4 | the sender takes the ACKs, $base = 2$, and sends packets 4 and 5 |
| 5 to 7 | the receiver stores 3, 4 and 5 and answers ACK(2) each time |
| 14 | timeout: the sender resends packet 2 |
| 16 | the receiver stores 2 and delivers 2, 3, 4, 5; it sends ACK(6) |
| 17, 18 | the sender sends packets 6 and 7 |
| 21 | ACK(8 mod 8) = ACK(0) arrives: $k = (0 - 6) \bmod 8 = 2$, and $base = 8$ |

The run makes 9 transmissions and ends at time 21. With $w_r = 1$ the receiver drops packets 3, 4 and 5, and the sender, which resends only $base$ on each timeout, needs 14 transmissions and ends at time 82.

The bound is tight. Take $w_s = 4$, $w_r = 1$ and $M = 4$. Packets 0 to 3 arrive, so $r = 4$, and their four ACKs are lost. The resent packet 0 carries the number 0 $= 4 \bmod 4$, so the receiver delivers the old $M[0]$ as message 4. The tests show this for eight pairs $(w_s, w_r)$ with $M = w_s + w_r - 1$, and show that $M = w_s + w_r$ is correct for each pair.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). Over FIFO channels, a DATA packet with index $j$ that reaches the receiver satisfies $r - w_s \le j \le r + w_s - 1$. The old part $r - w_s, \ldots, r - 1$ and the window $r, \ldots, r + w_r - 1$ are $w_s + w_r$ consecutive integers, so if $w_s + w_r \le M$ they have distinct residues modulo $M$, and line L11 stores each packet at its own index. At the sender, an ACK value lies between $base$ and $next$, at most $w_s < M$ apart, so line L5 reads it without error. Liveness needs fair channels and a timer that expires: the timer resends $base$ until an ACK moves it.

## Complexity

Without loss, a window of $w_s$ packets covers a time of $w_s L/R$ per round, and a round takes $T = L/R + \mathrm{RTT}$. The utilization is

$$U = \min\left(1, \frac{w_s \, L/R}{\mathrm{RTT} + L/R}\right),$$

so the link is full when $w_s \ge 1 + \mathrm{RTT}/(L/R)$, which is about the bandwidth-delay product $R \cdot \mathrm{RTT}$ in packets. For the 1500-byte, 100 Mbit/s, 10 ms example of [stop-and-wait](/stop-and-wait/), this needs $w_s \ge 85$. In the simulation with transmission time 1 and delay $d$, $m$ messages end at time $\lfloor (m-1)/w_s \rfloor (1 + 2d) + ((m - 1) \bmod w_s) + 1 + 2d$ when $w_s \le 1 + 2d$, and at $m + 2d$ for a larger window; for $m = 23$ and $d = 3$, a window of 4 ends at 44 and a window of 7 or more at 29. The sender buffers $w_s$ packets and the receiver $w_r$, so the space is $\Theta(w_s + w_r)$. Each step takes $O(1)$ time, plus the deliveries of line L12.

## Properties

- **Bounded numbers.** The header needs $\lceil \lg(w_s + w_r) \rceil$ bits. A larger space only costs header bits.
- **Cumulative ACKs.** One ACK can confirm many packets, so a lost ACK is repaired by any later ACK.
- **Needs FIFO for bounded numbers.** Over a channel that reorders, an old packet can return at any later time. TCP uses 32-bit byte numbers and assumes a maximum segment lifetime.
- **Flow control.** The window limits how much the receiver must buffer. TCP lets the receiver set the window in each ACK: see [flow control](/flow-control/).

## Variants and improvements

- **Go-Back-N.** $w_r = 1$, and a timeout resends every packet in flight. It needs $w_s \le M - 1$. See [Go-Back-N](/go-back-n/).
- **Selective repeat.** $w_r = w_s = w$, one ACK per packet and one timer per packet. It needs $w \le M/2$. See [selective repeat](/selective-repeat/).
- **Negative and selective ACKs.** The receiver reports the gaps (NAK, or the SACK option of TCP), so the sender resends only the missing packets without waiting for the timer.
- **A variable window.** TCP takes the window as the minimum of the receiver's advertised window and the congestion window of [congestion control](/congestion-control/).

## When to use it

Use a sliding window on every link where RTT is not small compared to $L/R$: long-distance links, satellite links, and fast local networks. Choose $w_s$ near the bandwidth-delay product, and $M \ge w_s + w_r$. If the receiver has memory for a full window, a receive window larger than 1 saves retransmissions after a loss.

## Pitfalls

- **Too few sequence numbers.** $w_s + w_r > M$ lets an old copy be taken for a new packet, as in the tight example.
- **Comparing numbers without the modulus.** Use $(a - base) \bmod M$ and $(s - r) \bmod M$, not $a > base$.
- **Not acknowledging a packet outside the window.** An old duplicate means that an ACK was lost; the receiver must answer it with ACK$(r)$.
- **Taking a repeated ACK as progress.** An ACK with $k = 0$ confirms nothing new and must not restart the window logic.
- **A window larger than the receiver buffer.** The receiver then has to drop packets that the sender assumes are safe. This is what [flow control](/flow-control/) prevents.

## Implementations

## History

Cerf and Kahn's paper of 1974 on packet network intercommunication, the design that became TCP, used windows, retransmission after a timeout and sequence numbers to detect duplicates. Link protocols of the 1970s, such as HDLC, use windows with 3-bit or 7-bit sequence numbers. Lynch's textbook proves sliding window protocols correct over FIFO channels in Chapter 22, and gives impossibility results for bounded headers over channels that reorder.

## References
