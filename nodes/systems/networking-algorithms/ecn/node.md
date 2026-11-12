---
tag: NJRD5Y
kind: concept
slug: ecn
name: Explicit congestion notification
aliases:
- ECN
area: systems/networking-algorithms
level: intro
summary: Routers signal congestion by setting a mark in the IP header of a packet instead of dropping it. The receiver echoes the mark, and the sender reduces its rate as if a packet were lost.
prereqs: [congestion-control]
see_also: [active-queue-management, red-random-early-detection, codel, pie-aqm, tcp-reno, tcp-cubic, bbr-congestion-control, aimd]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc3168"
    title: K. K. Ramakrishnan, Sally Floyd and David Black, RFC 3168, The Addition of Explicit Congestion Notification (ECN) to IP, 2001
    locator: Section 5 (the ECN field and its four codepoints), Section 6.1 (the ECE and CWR flags, the negotiation and the response of the TCP sender)
  - paper: doi:10.1145/1851182.1851192
    title: Mohammad Alizadeh, Albert Greenberg, David A. Maltz, Jitendra Padhye, Parveen Patel, Balaji Prabhakar, Sudipta Sengupta and Murari Sridharan, Data center TCP (DCTCP), ACM SIGCOMM 2010
    locator: pages 63 to 74 (marking at a queue threshold K and the estimate alpha of the fraction of marked packets)
  - url: "https://www.rfc-editor.org/rfc/rfc9331"
    title: Koen De Schepper and Bob Briscoe, RFC 9331, The Explicit Congestion Notification (ECN) Protocol for Low Latency, Low Loss, and Scalable Throughput (L4S), 2023
    locator: the use of ECT(1) as the L4S identifier
  - paper: doi:10.1016/0169-7552(89)90019-6
    title: Dah-Ming Chiu and Raj Jain, Analysis of the increase and decrease algorithms for congestion avoidance in computer networks, Computer Networks and ISDN Systems 17(1), 1989
    locator: pages 1 to 14 (controls driven by a binary feedback bit from the network)
---

Explicit congestion notification (ECN) lets a router signal congestion without dropping a packet. Two bits in the IP header say whether the endpoints understand ECN. A router with [active queue management](/active-queue-management/) that would drop such a packet early sets the bits to *Congestion Experienced* (CE) instead. The receiver echoes the mark back to the sender in the transport protocol, and the sender reduces its window as it would for a loss. RFC 3168 defines ECN for IP and TCP.

## In plain words

A router with a growing queue has only one way to tell senders to slow down: it throws a packet away. The sender sees the loss and slows down, but the packet must be sent again, and the sender may wait a long time before it notices.

With ECN, the router writes "I am getting full" in the packet header and lets the packet through. The receiver tells the sender about the note in its next confirmations. The sender slows down as if a packet were lost, but nothing is lost and nothing is sent twice. Both ends must say at the start of the connection that they understand these notes.

## The idea

**The IP field.** The two low bits of the IPv4 TOS byte or of the IPv6 Traffic Class byte form the ECN field (RFC 3168, Section 5):

| bits | name | meaning |
|---|---|---|
| 00 | Not-ECT | the transport does not support ECN |
| 10 | ECT(0) | ECN-capable transport |
| 01 | ECT(1) | ECN-capable transport (now the L4S identifier) |
| 11 | CE | Congestion Experienced |

A sender that has negotiated ECN marks its data packets ECT(0) or ECT(1). A router that decides to signal congestion to a packet with ECT sets CE. For a Not-ECT packet it drops, as before. When the queue is full, the router drops in any case. A router must not change CE back to another value.

**The TCP flags.** RFC 3168 uses two TCP header bits. ECN-Echo (ECE) goes from the receiver to the sender, and Congestion Window Reduced (CWR) from the sender to the receiver.

1. **Negotiation.** The client sends a SYN with ECE and CWR set. A server that agrees answers with a SYN-ACK with ECE set and CWR clear. Only then do the data packets carry ECT.
2. **Echo.** When the receiver gets a CE packet, it sets ECE on every ACK until it gets a packet with CWR set. So the mark survives the loss of single ACKs.
3. **Response.** On an ACK with ECE, the sender reduces cwnd and ssthresh as for a loss found by fast retransmit, but it does not resend anything. It reacts at most once per window of data, and sets CWR on the next new data packet.

The signal is still one bit per packet, so the endpoints keep the same [AIMD](/aimd/) logic as with losses. The gain is that the decrease comes without a lost packet, a retransmission or a possible timeout, and that the router can signal early, while the queue is short.

**More than one bit per round trip.** RFC 3168 tells the sender only that at least one packet in the window had a mark. DCTCP instead echoes each mark and has the switch mark every packet when the queue is above a threshold $K$. The sender keeps an estimate $\alpha$ of the fraction of marked packets and cuts by the factor $1 - \alpha/2$, so a few marks give a small cut and many marks give the full halving.

## Examples

**A single mark.** A Reno sender has 20 segments in flight, 100 to 119, and $\text{cwnd} = 20$. A RED router marks segment 107 with CE. The receiver sets ECE on the ACK for 107 and on all later ACKs. On the first of them, the sender sets $\text{ssthresh} = \text{cwnd} = 10$ and continues in congestion avoidance. Segments 108 to 119 are still in flight, 12 against a window of 10, so the sender waits for 3 more ACKs, and then sends segment 120 with CWR set. The other ACKs with ECE come from the same window, so the sender does not cut again. When segment 120 arrives with CWR, the receiver stops setting ECE. No segment was sent twice. With a drop instead of a mark, the sender would have needed three duplicate ACKs and a retransmission, and with a small window, a timeout.

**Codepoint changes along a path.**

| at the sender | at a router with a long queue | at the receiver |
|---|---|---|
| ECT(0) | set to CE | CE, echoed with ECE |
| Not-ECT | dropped | nothing arrives |
| CE | kept CE | CE, echoed with ECE |

**DCTCP.** With the gain $g = 1/16$ of the DCTCP paper and one quarter of the packets marked in each window, starting from $\alpha = 0$, the update $\alpha \leftarrow (1 - g)\alpha + g \cdot 0.25$ gives:

| windows | 1 | 2 | 5 | 10 | 20 | 40 | 60 |
|---|---|---|---|---|---|---|---|
| $\alpha$ | 0.0156 | 0.0303 | 0.0690 | 0.1189 | 0.1812 | 0.2311 | 0.2448 |
| cut factor $1 - \alpha/2$ | 0.992 | 0.985 | 0.966 | 0.941 | 0.909 | 0.885 | 0.878 |

So the cut moves towards $1 - 0.25/2 = 0.875$, much less than the halving of Reno.

## Where it is used

- **With active queue management.** [RED](/red-random-early-detection/), [CoDel](/codel/) and [PIE](/pie-aqm/) can mark ECT packets instead of dropping them, so the queue stays short with few losses.
- **TCP and QUIC.** Loss-based controls such as [Reno](/tcp-reno/) and [CUBIC](/tcp-cubic/) treat a CE echo as a loss without the retransmission. QUIC reports ECN counts in its ACK frames.
- **Data centers.** DCTCP uses marks at a shallow threshold to keep switch queues very short with high throughput.
- **Low latency (L4S).** RFC 9331 uses ECT(1) to identify traffic of scalable controls that expect frequent marks at a shallow queue, in the style of DCTCP.
- **Theory.** The binary feedback in the analysis of Chiu and Jain is such a one-bit congestion signal from the network, and in [network utility maximization](/network-utility-maximization/) a marking rate can carry the price of a link back to the sources.

ECN needs support at both endpoints and at the congested router, and a middlebox that clears or rewrites the bits breaks it. The sender must still react to losses, because a full queue drops in any case.

## References
