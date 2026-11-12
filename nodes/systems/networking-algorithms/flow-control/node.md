---
tag: EXR5TR
kind: concept
slug: flow-control
name: Flow control
aliases:
- end-to-end flow control
- TCP flow control
area: systems/networking-algorithms
level: intro
summary: The receiver tells the sender how much buffer space it has left (the receive window), and the sender never has more unacknowledged data in flight than that.
prereqs: [sliding-window-protocol]
see_also: [congestion-control, backpressure, nagle-algorithm, selective-repeat, go-back-n, token-bucket, leaky-bucket-queue]
sources:
  - book: isbn:9780136681557
    title: James F. Kurose and Keith W. Ross, Computer Networking, A Top-Down Approach, eighth edition
    locator: Section 3.5.5, Flow Control (rwnd, LastByteRcvd, LastByteRead and the rule LastByteSent - LastByteAcked <= rwnd)
  - book: isbn:9780123850591
    title: Larry L. Peterson and Bruce S. Davie, Computer Networks, A Systems Approach, fifth edition
    locator: Section 5.2.4, Sliding Window Revisited (Flow Control), and Section 5.2.5, Triggering Transmission (Silly Window Syndrome)
  - url: https://www.rfc-editor.org/rfc/rfc813
    title: RFC 813, David D. Clark, Window and Acknowledgement Strategy in TCP, 1982
    locator: the description of the silly window syndrome and the receiver and sender rules that avoid it
  - url: https://www.rfc-editor.org/rfc/rfc1122
    title: RFC 1122, Requirements for Internet Hosts, Communication Layers, 1989
    locator: Section 4.2.2.17, Probing Zero Windows; Section 4.2.3.3, When to Send a Window Update; Section 4.2.3.4, When to Send Data
  - url: https://www.rfc-editor.org/rfc/rfc7323
    title: RFC 7323, TCP Extensions for High Performance, 2014
    locator: Section 2, TCP Window Scale Option
  - book: isbn:9780132126953
    title: Andrew S. Tanenbaum and David J. Wetherall, Computer Networks, fifth edition
    locator: Section 6.5.8, TCP Sliding Window (window management, Clark's solution to the silly window syndrome)
---

Flow control keeps a fast sender from overrunning a slow receiver. The receiver has a buffer of limited size, and the application drains it at its own speed. In TCP, each ACK carries the *receive window* rwnd, the free space in that buffer, and the sender keeps the amount of data that is sent but not acknowledged at most rwnd. It is a property of the two ends only, and it is different from [congestion control](/congestion-control/), which protects the network between them.

## In plain words

A writer sends pages to a reader who has a tray of fixed size. The reader takes pages from the tray when it has time. If the writer sends more pages than the tray holds, pages fall on the floor and must be sent again.

So with each reply the reader says how much room is still free in the tray. The writer never has more pages on the way than that room. If the tray is full, the writer stops, and from time to time asks whether there is room again.

## The idea

**The receive window.** The receiver has a buffer of RcvBuffer bytes. LastByteRcvd is the number of the last byte that arrived, and LastByteRead is the number of the last byte that the application read. In the notation of Kurose and Ross, the receiver advertises

$$\mathrm{rwnd} = \mathrm{RcvBuffer} - (\mathrm{LastByteRcvd} - \mathrm{LastByteRead}).$$

The sender keeps

$$\mathrm{LastByteSent} - \mathrm{LastByteAcked} \le \mathrm{rwnd}.$$

Then the data in flight plus the data in the buffer never exceeds the buffer, so no byte is dropped for lack of space. This is the window of a [sliding window protocol](/sliding-window-protocol/) whose size is set by the receiver at run time and not by a constant. TCP sends at most $\min(\mathrm{rwnd}, \mathrm{cwnd})$, where cwnd is the congestion window.

**The zero window.** When the application stops reading, rwnd falls to 0, and the sender stops. The receiver reports more space in an ACK when the application reads again, but that ACK carries no data and is not acknowledged, so it can be lost. Then the sender waits for a window update and the receiver waits for data. To avoid this deadlock, the sender keeps a persist timer and sends a *zero window probe*, a segment with one byte or no data, when the timer expires; each probe gets an ACK with the current window. RFC 1122, Section 4.2.2.17, requires probes and allows exponential backoff of their interval. The sender must keep the connection open as long as the receiver answers the probes.

**The silly window syndrome.** If the application at the receiver reads one byte at a time, each read opens one byte of window. A receiver that advertises each such opening invites the sender to send a one-byte segment, which costs 40 bytes of header. The flow then stays at tiny segments. David Clark described this in RFC 813 (1982) and gave rules for both sides:

- **receiver**: do not advertise a small increase. RFC 1122, Section 4.2.3.3, says to keep the advertised right edge fixed until the window can grow by at least $\min(\mathrm{MSS}, \mathrm{RcvBuffer}/2)$;
- **sender**: do not send a small segment into a small window. RFC 1122, Section 4.2.3.4, sends only a full segment, or at least a fixed fraction of the largest window that the receiver offered, or all remaining data when nothing is in flight. [Nagle's algorithm](/nagle-algorithm/) adds the rule for small writes.

**Window scaling.** The TCP header has 16 bits for the window, so at most 65535 bytes. On a path with a large bandwidth-delay product this caps the rate at $65535 / \mathrm{RTT}$: about 5.2 Mbit/s for a round trip of 100 ms. The window scale option of RFC 7323 multiplies the field by $2^s$ with $s \le 14$, which allows windows of up to 1 GiB.

**Flow control and congestion control.** Flow control asks: does the receiver have room? Congestion control asks: does the network have room? The first has an exact answer, which the receiver sends. The second must be guessed from losses, delays or marks: see [congestion control](/congestion-control/). A slow receiver on a fast network is a flow control case; a fast receiver behind a congested link is a congestion control case.

**Other forms.** Flow control can be end to end, as in TCP, or hop by hop, between two neighbours. Credit-based flow control gives the sender a number of credits, one per buffer, and the receiver returns credits as it frees buffers; HTTP/2 and QUIC use credits per stream and per connection. In data processing pipelines, a slow stage slows down the stage before it: see [backpressure](/backpressure/).

## Examples

**A slow reader.** The receive buffer has 4096 bytes, the MSS is 1024 bytes, and the application stops reading. The sender sends 4 segments; the ACKs announce rwnd = 3072, 2048, 1024 and 0. The sender stops and starts its persist timer. The application then reads 2048 bytes, and the receiver sends a window update with rwnd = 2048. If the update is lost, the next zero window probe gets an ACK with rwnd = 2048, and the sender sends 2 segments.

**Silly window syndrome.** The same buffer is full, and the application reads 1 byte at a time. Without Clark's rule, each read leads to an advertisement of 1 byte, and the sender sends 41-byte packets with 1 byte of data. With the rule, the receiver advertises nothing until $\min(1024, 4096/2) = 1024$ bytes are free, and the sender then sends a full segment.

**A window that is too small.** A path with a rate of 100 Mbit/s and a round trip of 80 ms holds 1 MB in flight. With a window of 64 KiB, TCP uses at most $65536 \cdot 8 / 0.08 \approx 6.6$ Mbit/s of it; with window scaling and a buffer of 1 MB it can fill the path.

## Where it is used

TCP (the receive window, persist timer and window scaling), QUIC and HTTP/2 (credit limits per stream and per connection), link layers (XON/XOFF on serial lines, the PAUSE frames of IEEE 802.3x, credit-based flow control in InfiniBand and PCI Express), and message systems that limit the number of unacknowledged messages for each consumer.

## References
