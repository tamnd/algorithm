---
tag: AT48F9
kind: algorithm
slug: go-back-n
name: Go-Back-N
aliases:
- GBN
- go-back-N ARQ
area: systems/networking-algorithms
level: intro
summary: A sliding window ARQ where the receiver keeps only in-order packets and a timeout resends every unacknowledged packet. With k-bit numbers the window must be at most 2^k - 1.
solves: [reliable-data-transfer]
model: asynchronous-model
complexity:
  vars: {m: the number of messages, N: the window in packets, T: "the time of one transmission plus one round trip", p: the probability that a packet is lost}
  time: {best: Θ(m T/N + T)}
  space: {extra: Θ(N)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1964
  people: [R. J. Benice, A. H. Frey Jr.]
  note: Benice and Frey analyzed three basic retransmission logics. Later surveys name them stop-and-wait, go-back-N and selective repeat.
prereqs: [sliding-window-protocol]
see_also: [selective-repeat, stop-and-wait, alternating-bit-protocol, reliable-data-transfer, fast-retransmit-fast-recovery, tcp-reno]
sources:
  - book: isbn:9780136681557
    title: James F. Kurose and Keith W. Ross, Computer Networking, A Top-Down Approach, eighth edition
    locator: Section 3.4.3, Go-Back-N (GBN)
  - book: isbn:9780132126953
    title: Andrew S. Tanenbaum and David J. Wetherall, Computer Networks, fifth edition
    locator: Section 3.4.2, A Protocol Using Go-Back-N (the window of at most MAX_SEQ frames)
  - book: isbn:9780123850591
    title: Larry L. Peterson and Bruce S. Davie, Computer Networks, A Systems Approach, fifth edition
    locator: Section 2.5.2, Sliding Window (the case RWS = 1)
  - paper: doi:10.1109/MCOM.1984.1091865
    title: Shu Lin, Daniel J. Costello Jr. and Michael J. Miller, Automatic-repeat-request error-control schemes, IEEE Communications Magazine 22(12), 1984
    locator: the section on go-back-N ARQ and its throughput
---

Go-Back-N (GBN) is a [sliding window protocol](/sliding-window-protocol/) for [reliable data transfer](/reliable-data-transfer/) in which the receiver accepts only the next packet in order and drops all others. The sender keeps up to $N$ packets in flight with one timer; when the timer expires, it goes back and resends every packet that is not yet acknowledged. With $k$-bit sequence numbers over FIFO channels it is correct if and only if $N \le 2^k - 1$. It needs no receive buffer, but one loss costs up to $N$ transmissions.

## In plain words

The sender posts several numbered letters without waiting. The receiver is strict: it takes only the letter with the next number. If letter 3 is lost, it throws away 4, 5 and 6 when they come, and each time it replies "I still wait for 3".

The sender has one clock, for its oldest letter. When the clock runs out, it goes back to letter 3 and posts 3, 4, 5 and 6 again.

The receiver needs no space to keep early letters, and its logic is very small. The cost is that one lost letter makes the sender post a whole window of letters again.

## The problem

The sender has messages $M[0], \ldots, M[m-1]$, and the receiver must deliver exactly this sequence. A packet carries its index modulo $M = 2^k$. Each direction is a FIFO channel that may lose or duplicate packets. The sender may have at most $N$ packets in flight.

## The algorithm

The receiver sends a cumulative ACK$(a)$ with $a$ = the next index that it expects. Kurose and Ross use the index of the last packet received in order instead, which is $a - 1$; the two forms carry the same information.

```pseudo id=main
SENDER(M[0 .. m − 1])
L1  base ← 0; next ← 0
L2  while next < m and next < base + N do
L3      send DATA(next mod M, M[next])
L4      if the timer is off then start the timer
L5      next ← next + 1
L6  on ACK(a):
L7      c ← (a − base) mod M
L8      if 1 ≤ c ≤ next − base then base ← base + c; stop the timer
L9          if base < next then start the timer; go to L2
L10 on a timeout:
L11     start the timer
L12     for j ← base to next − 1 do
L13         send DATA(j mod M, M[j])

RECEIVER (r ← 0)
L14 on DATA(s, d): if s = r mod M then
L15     deliver d; r ← r + 1
L16 send ACK(r mod M)                        ▷ for every packet, also a dropped one
```

## Example

Twelve messages with $N = 4$ and $k = 4$. A transmission takes 1 time unit, the delay is 2 in each direction, and the timeout is 15. The first copies of packets 3 and 7 are lost.

| time | event |
|---|---|
| 0 to 3 | send packets 0, 1, 2, 3 (3 is lost) |
| 5 to 7 | ACK(1), ACK(2), ACK(3) arrive; send packets 4, 5, 6 |
| 8 to 10 | the receiver drops 4, 5 and 6 and answers ACK(3) |
| 22 | timeout: resend 3, 4, 5, 6 |
| 27 to 30 | ACK(4) to ACK(7) arrive; send 7 (lost), 8, 9, 10 |
| 45 | timeout: resend 7, 8, 9, 10 |
| 50 | send 11 |
| 55 | ACK(12 mod 16) arrives: done |

The run makes 20 transmissions for 12 messages and ends at time 55: each loss costs the lost packet and the 3 packets after it. [Selective repeat](/selective-repeat/) needs 14 transmissions and ends at 45 on the same pattern. On 200 messages with 24 lost first copies (seed 42, loss 0.1, delay 4, timeout 30), GBN needs 271, 299 and 331 transmissions for $N = 4$, 8 and 16, and selective repeat needs 224 in each case.

The bound is tight. With $k = 2$ and $N = 4$, the sender sends packets 0 to 3, the receiver delivers them, and all four ACKs are lost. The timeout resends packet 0 with the number 0, which is also $4 \bmod 4$, so the receiver delivers m0, m1, m2, m3, m0, m1, and so on.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). Over FIFO channels, two facts hold at every step. An ACK that reaches the sender carries a value $a$ with $base \le a \le next$, so line L7 decodes it, because $next - base \le N < 2^k$. A DATA packet with index $j$ that reaches the receiver has $r - N \le j \le r + N - 1$, and the only multiple of $2^k$ in $[-N, N-1]$ is 0 when $N \le 2^k - 1$. So line L14 accepts exactly packet $r$. GBN is the [sliding window protocol](/sliding-window-protocol/) with $w_r = 1$, and the bound $w_s + w_r \le M$ becomes $N \le 2^k - 1$. Resending the whole window instead of the oldest packet does not change the argument.

## Complexity

Without loss, the utilization is $\min(1, N (L/R)/(\mathrm{RTT} + L/R))$ for a link of rate $R$, packets of $L$ bits and round-trip time RTT, as for every [sliding window protocol](/sliding-window-protocol/). With a full window, a loss detected by the timer costs the lost packet and the up to $N - 1$ packets after it. With independent loss probability $p$ per packet and a full pipe of $N$ packets, the analysis in Lin, Costello and Miller gives a throughput efficiency of $(1-p)/(1 - p + Np)$ in packets per transmission slot, so a large window wastes much of the link when $p$ is not small. The sender buffers $N$ packets; the receiver buffers none and keeps one counter. Each event takes $O(1)$ time, and a timeout takes $O(N)$.

## Properties

- **No receive buffer.** The receiver keeps only $r$.
- **Cumulative ACKs.** A later ACK repairs a lost one.
- **Window bound.** $N \le 2^k - 1$, one less than the number of sequence numbers.
- **Wasteful on lossy links.** Each loss costs about a window of transmissions.
- **One timer.** The sender times only its oldest packet.

## Variants and improvements

- **Selective repeat.** Buffer packets out of order and resend only the lost ones; the window drops to $2^{k-1}$. See [selective repeat](/selective-repeat/).
- **NAK on a gap.** The receiver sends a negative acknowledgement when it sees a gap, so the sender goes back without waiting for the timeout. HDLC calls this REJ.
- **Fast retransmit.** TCP resends after three duplicate ACKs, without waiting for the timer: see [fast retransmit and fast recovery](/fast-retransmit-fast-recovery/).
- **A larger header.** With 32-bit byte numbers, as in TCP, the window bound is not the limit; the receive buffer and [congestion control](/congestion-control/) are.

## When to use it

Use GBN when the loss rate is low and the receiver must be simple or has no buffer, for example in a hardware link layer. When losses are common or the window is large, [selective repeat](/selective-repeat/) wastes fewer transmissions.

## Pitfalls

- **Using all $2^k$ numbers.** $N = 2^k$ lets an old packet pass as new, as in the tight example.
- **Not answering a dropped packet.** The receiver must send ACK$(r)$ for each out-of-order packet, or a lost ACK stalls the sender until the next timeout.
- **A timeout that is too short.** Each early timeout resends a whole window. Estimate it from the round-trip time: see [round-trip time estimation](/round-trip-time-estimation/).
- **Resending only the oldest packet.** That is a different protocol: the receiver drops the rest of the window, so recovery then takes one timeout per packet.

## Implementations

## History

Benice and Frey analyzed three basic retransmission logics in 1964. Later work, such as the survey of Lin, Costello and Miller (1984), names them stop-and-wait, go-back-N and selective repeat, and analyzes their throughput. Go-back-N is the recovery rule of the REJ frame of HDLC and its relatives.

## References
