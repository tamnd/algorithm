---
tag: NTM3PJ
kind: algorithm
slug: selective-repeat
name: Selective repeat
aliases:
- selective repeat ARQ
- SR ARQ
area: systems/networking-algorithms
level: intro
summary: A sliding window ARQ with one ACK and one timer per packet. The receiver buffers packets out of order and only lost packets are resent. The window must be at most 2^(k-1).
solves: [reliable-data-transfer]
model: asynchronous-model
complexity:
  vars: {m: the number of messages, w: the window in packets, T: "the time of one transmission plus one round trip"}
  time: {best: Θ(m T/w + T)}
  space: {extra: Θ(w)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1964
  people: [R. J. Benice, A. H. Frey Jr.]
  note: Benice and Frey analyzed three basic retransmission logics. Later surveys name them stop-and-wait, go-back-N and selective repeat.
prereqs: [sliding-window-protocol, go-back-n]
see_also: [stop-and-wait, alternating-bit-protocol, reliable-data-transfer, fast-retransmit-fast-recovery, round-trip-time-estimation]
sources:
  - book: isbn:9780136681557
    title: James F. Kurose and Keith W. Ross, Computer Networking, A Top-Down Approach, eighth edition
    locator: Section 3.4.4, Selective Repeat (SR), with the dilemma of a window that is too large
  - book: isbn:9780132126953
    title: Andrew S. Tanenbaum and David J. Wetherall, Computer Networks, fifth edition
    locator: Section 3.4.3, A Protocol Using Selective Repeat (the window of at most (MAX_SEQ + 1)/2)
  - book: isbn:9780123850591
    title: Larry L. Peterson and Bruce S. Davie, Computer Networks, A Systems Approach, fifth edition
    locator: Section 2.5.2, Sliding Window (finite sequence numbers when RWS = SWS)
  - paper: doi:10.1109/MCOM.1984.1091865
    title: Shu Lin, Daniel J. Costello Jr. and Michael J. Miller, Automatic-repeat-request error-control schemes, IEEE Communications Magazine 22(12), 1984
    locator: the section on selective-repeat ARQ and its throughput
---

Selective repeat (SR) is a [sliding window protocol](/sliding-window-protocol/) for [reliable data transfer](/reliable-data-transfer/) in which the receiver buffers packets that arrive out of order and acknowledges each packet on its own. The sender keeps one timer per packet and resends only the packets whose timers expire. With $k$-bit sequence numbers over FIFO channels, it is correct if and only if the window $w$ is at most $2^{k-1}$, half of the [Go-Back-N](/go-back-n/) bound. Each loss costs one extra transmission, against up to a window for Go-Back-N.

## In plain words

The sender posts several numbered letters without waiting, and it keeps a separate clock for each letter. The receiver keeps every letter that is in its window, even when an earlier one is missing. It confirms each letter on its own, with the number of that letter.

If letter 3 is lost, letters 4, 5 and 6 still arrive and wait in the receiver's tray. Only the clock of letter 3 runs out, and the sender posts only letter 3 again. When it arrives, the receiver hands over 3, 4, 5 and 6 together.

The price is a tray at the receiver, a clock for each letter, and a smaller window for the same set of numbers.

## The problem

The sender has messages $M[0], \ldots, M[m-1]$, and the receiver must deliver exactly this sequence. A packet carries its index modulo $M = 2^k$. Each direction is a FIFO channel that may lose or duplicate packets. Both sides use a window of $w$ packets.

## The algorithm

The sender keeps $base$, the smallest index without an ACK, and $next$. The receiver keeps $r$, the smallest index that it has not received, and a buffer for $r, \ldots, r + w - 1$.

```pseudo id=main
SENDER(M[0 .. m − 1])
L1  while next < m and next < base + w do
L2      send DATA(next mod M, M[next]); start the timer of next; next ← next + 1
L3  on ACK(s):
L4      j ← base + ((s − base) mod M)
L5      if j < next then mark j as acknowledged; stop its timer
L6      while base is marked do base ← base + 1      ▷ then go to L1
L7  on the timeout of packet j:
L8      resend DATA(j mod M, M[j]); restart the timer of j

RECEIVER (r ← 0)
L9  on DATA(s, d): off ← (s − r) mod M
L10 if off < w then
L11     store d at index r + off if the slot is empty; send ACK(s)
L12     while the slot r is full do deliver it; r ← r + 1
L13 else if off ≥ M − w then send ACK(s)        ▷ an old packet whose ACK was lost
L14 else ignore the packet
```

Line L13 is necessary. An old packet arrives again only if its ACK was lost, and without a new ACK the sender would resend it forever.

## Example

On the loss pattern of the [Go-Back-N](/go-back-n/) example (12 messages, $w = 4$, $k = 4$, transmission time 1, delay 2, timeout 15, the first copies of packets 3 and 7 lost), selective repeat makes 14 transmissions and ends at time 45; Go-Back-N makes 20 and ends at 55. On 200 messages with 24 lost first copies (seed 42, delay 4, timeout 30), selective repeat makes $200 + 24 = 224$ transmissions for $w = 4$, 8 and 16, and Go-Back-N makes 271, 299 and 331.

The bound is tight. Take $k = 2$, so $M = 4$, and $w = 3$:

| step | event |
|---|---|
| 1 | send packets 0, 1, 2; all arrive; the receiver delivers m0, m1, m2; $r = 3$, window $\{3, 4, 5\}$ |
| 2 | all three ACKs are lost |
| 3 | the timer of packet 0 expires; it is resent with the number 0 |
| 4 | the receiver computes $\mathit{off} = (0 - 3) \bmod 4 = 1 < 3$ and stores the old m0 at index 4 |
| 5 | in the same way the old m1 is stored at index 5; packet 2 has $\mathit{off} = 3$ and is only acknowledged |
| 6 | the sender gets the ACKs, sends m3, and the receiver delivers m3, m0, m1 |

The receiver delivers m0, m1, m2, m3, m0, m1. With $w = 2$ the same run is correct.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). Over FIFO channels, a DATA packet with index $j$ that reaches the receiver has $r - w \le j \le r + w - 1$. These are $2w$ consecutive integers, so with $2w \le 2^k$ their numbers are distinct, and the receiver tells a packet in its window from an old copy. At the sender, an ACK for index $j$ arrives only with $base - w \le j < next$, so line L4 finds the right packet, or a value $j' \ge next$ for an old ACK, which line L5 ignores. Liveness needs fair channels and timers that expire.

## Complexity

Without loss, the utilization is $\min(1, w (L/R)/(\mathrm{RTT} + L/R))$, as for every [sliding window protocol](/sliding-window-protocol/). With independent loss probability $p$ per packet and an ideal buffer, each packet needs $1/(1-p)$ transmissions on average, so the throughput efficiency is $1 - p$ packets per slot (Lin, Costello and Miller). Both sides buffer up to $w$ packets, and the sender keeps $w$ timers. An event takes $O(1)$ time with a timer wheel or a heap of size $w$, plus the deliveries of line L12.

## Properties

- **Only lost packets are resent.** In the examples, the count is exactly the number of messages plus the number of losses.
- **Individual ACKs.** An ACK names one packet. A lost ACK causes one spurious retransmission, which line L13 answers.
- **Window bound.** $w \le 2^{k-1}$, half of the sequence space.
- **Receive buffer.** The receiver needs room for $w$ packets.

## Variants and improvements

- **Cumulative plus selective ACKs.** TCP sends a cumulative ACK and lists the blocks received out of order in the SACK option (RFC 2018). The sender then resends only the gaps.
- **NAK.** The receiver asks for a missing packet when it sees a gap. HDLC calls this frame SREJ.
- **Unequal windows.** The general bound is $w_s + w_r \le 2^k$: see [sliding window protocol](/sliding-window-protocol/).
- **Hybrid ARQ.** Wireless links combine selective repeat with forward error correction.

## When to use it

Use selective repeat when losses are not rare and the window is large, so that Go-Back-N would waste much of the link: satellite links, wireless links and fast long-distance paths. The receiver must have memory for a full window.

## Pitfalls

- **A window of more than half the sequence space.** An old packet is then stored as a new one, as in the tight example.
- **Ignoring old packets.** A packet below the window must be acknowledged again (line L13), or the sender never gets its ACK.
- **One timer for all packets.** Then a timeout cannot tell which packet to resend. TCP uses one timer, and recovers with SACK and [fast retransmit](/fast-retransmit-fast-recovery/).
- **Delivering on receipt.** The receiver must hold early packets and deliver only the in-order run (line L12).

## Implementations

## History

Benice and Frey analyzed three basic retransmission logics in 1964. Later surveys, such as Lin, Costello and Miller (1984), name them stop-and-wait, go-back-N and selective repeat, and show that selective repeat has the best throughput of the three when the receiver has an unlimited buffer. HDLC has a selective reject frame (SREJ), and TCP added selective acknowledgements in RFC 2018 (1996).

## References
