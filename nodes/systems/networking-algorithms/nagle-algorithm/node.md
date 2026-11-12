---
tag: 0F8CT9
kind: algorithm
slug: nagle-algorithm
name: Nagle's algorithm
aliases:
- Nagle algorithm
- Nagling
area: systems/networking-algorithms
level: intro
summary: While sent data is not yet acknowledged, a TCP sender holds small writes and sends them together when an ACK arrives or a full segment is ready.
model: asynchronous-model
complexity:
  vars: {n: the number of writes and ACKs, s: the number of segments sent}
  time: {best: Θ(n + s), worst: Θ(n + s)}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1984
  people: [John Nagle]
  note: Nagle described the rule in RFC 896, Congestion Control in IP/TCP Internetworks, to stop small packets from flooding the Ford Aerospace network.
prereqs: [flow-control]
see_also: [tcp-acknowledgment-problem, congestion-control, sliding-window-protocol, stop-and-wait]
sources:
  - url: https://www.rfc-editor.org/rfc/rfc896
    title: RFC 896, John Nagle, Congestion Control in IP/TCP Internetworks, 1984
    locator: the section The small-packet problem, and its solution
  - url: https://www.rfc-editor.org/rfc/rfc1122
    title: RFC 1122, Requirements for Internet Hosts, Communication Layers, 1989
    locator: Section 4.2.3.4, When to Send Data (the Nagle algorithm, and a way to disable it), and Section 4.2.3.2, When to Send an ACK Segment
  - book: isbn:9780123850591
    title: Larry L. Peterson and Bruce S. Davie, Computer Networks, A Systems Approach, fifth edition
    locator: Section 5.2.5, Triggering Transmission (Silly Window Syndrome, Nagle's Algorithm)
  - book: isbn:9780132126953
    title: Andrew S. Tanenbaum and David J. Wetherall, Computer Networks, fifth edition
    locator: Section 6.5.8, TCP Sliding Window (Nagle's algorithm and delayed acknowledgements)
---

Nagle's algorithm is the TCP sender rule that stops a stream of small writes from becoming a stream of tiny packets. While any sent data is still unacknowledged, the sender holds data that does not fill a full segment (MSS), and sends it when an ACK arrives or when a full segment is ready. So at most one small segment is in flight. John Nagle described it in RFC 896 (1984); it is on by default in TCP stacks and is turned off with the socket option TCP_NODELAY.

## In plain words

A user types in a remote terminal, and each key is one byte. If each byte goes out in its own packet, each packet carries 40 bytes of headers for 1 byte of data.

Nagle's rule: if a packet is still on its way and not confirmed, do not send another small one. Collect the new keys. When the confirmation comes, send all collected keys in one packet. If enough data for a full packet collects, send it at once.

On a fast network, confirmations come back quickly, and almost nothing waits. On a slow network, more keys collect in each packet, so the network carries fewer packets when it has the least room.

## The problem

An application writes data in pieces that are often much smaller than the MSS. Each TCP/IP packet has at least 40 bytes of headers. RFC 896 notes that a 1-byte segment is a 41-byte packet, an overhead of 4000%, and that on a loaded network such packets can cause congestion collapse. The sender must send fewer, larger segments without a fixed timer, and without delay when the data is a full segment.

## The algorithm

The sender keeps $buf$, the bytes written but not sent, $sent$, the bytes sent, and $acked$, the bytes acknowledged.

```pseudo id=main
NAGLE
L1  on a write of n bytes: buf ← buf + n; TRY-SEND
L2  on an ACK for the first a bytes: acked ← max(acked, a); TRY-SEND

TRY-SEND
L3  while buf > 0 do
L4      if buf ≥ MSS then send a segment of MSS bytes
L5      else if sent = acked then send all buf bytes in one segment   ▷ nothing is in flight
L6      else return                         ▷ hold the small segment
```

With TCP_NODELAY, line L5 sends the bytes also when $sent > acked$. A real TCP also checks the receive window and the congestion window before it sends, and RFC 1122, Section 4.2.3.4, states the same rule: if there is unacknowledged data, buffer all user data until the outstanding data has been acknowledged or a full-sized segment can be sent.

## Example

Twenty keystrokes, one byte each at the times $5, 55, 105, \ldots, 955$ ms, with a one-way delay of 60 ms, so the round-trip time is 120 ms. The receiver acknowledges each segment at once.

| time (ms) | 5 | 125 | 245 | 365 | 485 | 605 | 725 | 845 | 965 |
|---|---|---|---|---|---|---|---|---|---|
| bytes | 1 | 2 | 2 | 3 | 2 | 3 | 2 | 2 | 3 |

The first key goes out at once. The keys at 55 and 105 wait for the ACK, which comes at 125, and go out together. So each segment carries the keys of one round trip. Nagle sends 9 segments and 380 bytes on the wire with 40-byte headers; with TCP_NODELAY the sender sends 20 segments and 820 bytes. The last key arrives at 1025 ms in place of 1015 ms, 10 ms later.

A bulk write of four full segments plus 100 bytes is sent at once: line L4 never holds a full segment, and the tail goes when the ACKs come back.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). The sender sends the bytes in order and each byte once, since it only moves bytes from the front of $buf$. Line L5 sends a small segment only when $sent = acked$, so at most one small segment is unacknowledged at a time, and two small segments are at least one round-trip time apart. No byte waits forever: if bytes are held, $sent > acked$, and the ACK for all sent bytes then lets line L5 send them. Without delayed ACKs, a byte waits at most about one round-trip time.

## Complexity

Each write and each ACK costs $O(1)$ work plus $O(1)$ per segment sent. The sender keeps three counters beyond the send buffer, which TCP keeps anyway.

## Properties

- **Self-clocking.** The ACKs, not a timer, decide when small data goes out, so the rule adapts to the round-trip time.
- **At most one small segment in flight.**
- **Full segments are never held.**
- **Fewer packets on slow paths.** The number of small segments per second is at most about $1/\mathrm{RTT}$.
- **Extra delay.** A small write can wait one round-trip time, or more with delayed ACKs.

## Variants and improvements

- **TCP_NODELAY.** The socket option turns the rule off, for interactive and request-response traffic that cannot wait. RFC 1122 requires that an application can disable it.
- **Minshall's variant.** Hold a small segment only if an earlier small segment is unacknowledged, not if any data is unacknowledged. This removes the delay after a bulk write with a short tail. Linux uses a check of this kind.
- **TCP_CORK and TCP_NOPUSH.** The opposite control: the application tells the stack to hold all partial segments until it uncorks.
- **Receiver side.** The receiver part of the [silly window syndrome](/flow-control/) fix, by Clark (RFC 813), stops a receiver from offering small windows. Nagle's rule is the sender part.

## When to use it

Keep it on for bulk transfers and for interactive sessions over slow or congested links, where it cuts the number of packets. Turn it off with TCP_NODELAY for latency-sensitive request-response protocols, for games and for remote desktop traffic, and in applications that write a request in several small pieces.

## Pitfalls

- **Nagle with delayed ACKs.** The receiver may wait up to 500 ms (RFC 1122, Section 4.2.3.2; 200 ms in many stacks) before it acknowledges a single segment. If the application writes a small header, then a small body, and then waits for the reply, the body waits for the delayed ACK of the header. In the tests, with a one-way delay of 30 ms and a 200 ms ACK timer, the second write arrives at 290 ms, against 31 ms with TCP_NODELAY and 90 ms without the delayed ACK. See also the [TCP acknowledgment problem](/tcp-acknowledgment-problem/).
- **An odd number of full segments.** With delayed ACKs that acknowledge every second segment, the last full segment of an odd count is acknowledged only by the timer, so the short tail waits for it: in the tests, a tail after 5 full segments goes out at 260 ms, and after 4 at 60 ms.
- **Fixing it with many small writes.** Write a whole request in one call (for example with writev), so that line L4 or line L5 sends it at once.

## Implementations

## History

John Nagle, at Ford Aerospace, saw that the company network was flooded by 41-byte packets from remote terminal sessions. RFC 896, Congestion Control in IP/TCP Internetworks (1984), describes the small-packet problem and the rule to inhibit new segments while sent data is unacknowledged; the same RFC also describes congestion collapse. RFC 1122 (1989) made the rule a SHOULD for TCP hosts, with a way for the application to turn it off. The same RFC recommends delayed ACKs, and the interaction of the two rules became a well-known source of latency.

## References
