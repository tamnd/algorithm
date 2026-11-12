---
tag: E5YMJD
kind: problem
slug: reliable-data-transfer
name: Reliable data transfer
aliases:
- ARQ problem
- reliable data transfer protocol
area: systems/networking-algorithms
level: intro
summary: Deliver a stream of messages exactly once and in order over a channel that may corrupt, lose, duplicate, delay or reorder packets.
prereqs: [checksum]
see_also: [two-generals-problem, fifo-delivery, binary-erasure-channel, tcp-acknowledgment-problem, congestion-control, error-detection]
sources:
  - book: isbn:9780136681557
    title: James F. Kurose and Keith W. Ross, Computer Networking, A Top-Down Approach, eighth edition
    locator: Section 3.4, Principles of Reliable Data Transfer (rdt1.0 to rdt3.0 in Section 3.4.1, pipelining in Section 3.4.2, Go-Back-N in 3.4.3 and Selective Repeat in 3.4.4)
  - book: isbn:9780123850591
    title: Larry L. Peterson and Bruce S. Davie, Computer Networks, A Systems Approach, fifth edition
    locator: Section 2.5, Reliable Transmission (2.5.1 Stop-and-Wait, 2.5.2 Sliding Window)
  - book: isbn:9780132126953
    title: Andrew S. Tanenbaum and David J. Wetherall, Computer Networks, fifth edition
    locator: Section 3.3, Elementary Data Link Protocols, and Section 3.4, Sliding Window Protocols
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 22, Data Link Protocols (the problem, Stenning's protocol, the alternating bit protocol, and the impossibility results for bounded headers)
  - paper: doi:10.1109/MCOM.1984.1091865
    title: Shu Lin, Daniel J. Costello Jr. and Michael J. Miller, Automatic-repeat-request error-control schemes, IEEE Communications Magazine 22(12), 1984
    locator: the definitions of the basic ARQ schemes and their throughput
---

Reliable data transfer is the problem of moving a sequence of messages from a sender to a receiver so that the receiver delivers each message exactly once and in the original order, although the channel between them may corrupt, lose, duplicate, delay or reorder packets. Its solutions are called ARQ protocols (automatic repeat request): the receiver acknowledges what it gets, and the sender retransmits what is not acknowledged. TCP, the link layers of HDLC and Wi-Fi, and many application protocols solve it.

## In plain words

You must send a long letter by a post that sometimes loses pages, sometimes delivers a page twice, and sometimes smudges a page. The reader must get every page once and in order.

So you number the pages. The reader checks each page for smudges, throws away bad pages and pages it already has, and writes back which pages it got. You send again any page that is not confirmed after a while. The rest of the problem is how many pages you may send before you wait for confirmations, how long you wait, and how few numbers you can use.

## Definition

A *sender* gets messages $m_1, m_2, \ldots$ from the layer above, and a *receiver* hands messages to the layer above (it *delivers* them). They are joined by two channels, one in each direction. The *channel model* says what a channel may do to a packet:

- **corrupt** it; a [checksum](/checksum/) or another [error-detecting code](/error-detection/) finds the error, and the receiver drops the packet, so a corruption becomes a loss;
- **lose** it;
- **duplicate** it;
- **delay** it by a finite time, which may be unknown and not bounded;
- **reorder** it with respect to other packets, in some models.

A channel never makes up a packet. It is *fair*: a packet that is sent infinitely often is received infinitely often.

A protocol solves the problem if, in every run:

- **safety**: the sequence of delivered messages is always a prefix of $m_1, m_2, \ldots$, so there is no loss inside the sequence, no duplicate and no reordering;
- **liveness**: every message that the sender gets is delivered in the end.

The quality measures are the throughput (delivered bits per second), the delay, the number of retransmissions, the size of the sequence number field, and the memory at both ends.

## Variants

- **Perfect channel.** Nothing goes wrong; the sender only sends. This is rdt1.0 in Kurose and Ross.
- **Bit errors only.** The receiver answers with ACK or NAK, and the sender resends on a NAK (rdt2.0). Because an ACK or NAK can itself be corrupted, the packets need a 1-bit sequence number (rdt2.1). A duplicate ACK for the previous packet can replace the NAK (rdt2.2).
- **Errors and loss.** The sender also needs a timer, and resends when it expires (rdt3.0). This is the [alternating bit protocol](/alternating-bit-protocol/).
- **FIFO or reordering channels.** Over a FIFO channel, a finite sequence number space suffices; over a channel that reorders without a bound on the delay, it does not (see Bounds).
- **Known delay bound.** If every packet is delivered or lost within a known time, numbers can be reused after that time, as TCP does with the maximum segment lifetime.
- **Byte streams.** TCP numbers bytes, not messages, and the window also does [flow control](/flow-control/).

## Examples

- A file transfer over a link that loses 1 packet in 100: the receiver must hand the file over complete and in order.
- A remote terminal: each keystroke must arrive once. A typed `rm` must not arrive twice.
- A link between two routers with a 3-bit sequence number field, as in HDLC: the window must respect the bounds below.

A stop-and-wait sender on a path with a rate of 1 Gbit/s, a round-trip time of 30 ms and packets of 1000 bytes uses the link for $L/R = 8\ \mu\mathrm{s}$ in each $30.008$ ms, a utilization of about $0.027$ percent. A window of $w$ packets multiplies this by $w$, up to 1.

## Known algorithms

| algorithm | idea | sequence numbers | when it fits |
|---|---|---|---|
| [stop-and-wait](/stop-and-wait/) | one packet in flight, resend on timeout | unbounded, or 1 bit over FIFO | short paths, simple devices |
| [alternating bit protocol](/alternating-bit-protocol/) | stop-and-wait with a 1-bit number | 2 values, FIFO only | the textbook rdt3.0 |
| [sliding window protocol](/sliding-window-protocol/) | up to $w$ packets in flight | $w_s + w_r \le 2^k$ over FIFO | the general frame |
| [Go-Back-N](/go-back-n/) | receiver keeps only in-order packets; resend the whole window | $N \le 2^k - 1$ | low loss, no receive buffer |
| [selective repeat](/selective-repeat/) | receiver buffers; resend only lost packets | $w \le 2^{k-1}$ | high loss or large windows |

The timeout comes from [round-trip time estimation](/round-trip-time-estimation/), usually with [Jacobson's RTO estimation](/jacobson-rto-estimation/) and [Karn's algorithm](/karn-algorithm/). TCP combines a cumulative ACK, selective ACKs and [fast retransmit](/fast-retransmit-fast-recovery/).

## Bounds

- **Sequence numbers over FIFO channels.** With $k$-bit numbers, a sender window $w_s$ and a receiver window $w_r$, a sliding window protocol is correct if and only if $w_s + w_r \le 2^k$. So Go-Back-N needs $N \le 2^k - 1$ and selective repeat needs $w \le 2^{k-1}$.
- **Reordering channels.** If the channel may reorder packets without a bound on the delay, no protocol with a finite set of packet headers solves the problem: an old copy can always come back when its number is in use again. Lynch's Chapter 22 proves this kind of result; Stenning's protocol, with unbounded numbers, solves it.
- **Retransmissions.** If each transmission is lost independently with probability $p$, each message needs at least $1/(1-p)$ transmissions on average, and selective repeat with an unlimited buffer reaches this bound.
- **Throughput.** With a window of $w$ packets, at most $w$ packets are delivered per round trip.
- **Termination.** A protocol cannot make both sides sure that the last acknowledgement arrived. This is the [two generals problem](/two-generals-problem/); TCP's connection close uses a timer instead.

## Reductions

- A corrupting channel reduces to a lossy one with an error-detecting code: a corrupted packet is dropped.
- A reordering channel with a maximum packet lifetime reduces to a FIFO-like channel for numbers that are not reused within that lifetime.
- Reliable data transfer gives the [FIFO delivery](/fifo-delivery/) assumption that many distributed algorithms make about their links.

## Applications

TCP and QUIC, link layers such as HDLC, LAPB and IEEE 802.11 (which uses stop-and-wait per frame), file transfer protocols over UDP such as TFTP (stop-and-wait), and message queues that redeliver messages until they are acknowledged.

## References
