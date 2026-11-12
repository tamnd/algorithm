---
title: Nagle's rule keeps at most one small segment in flight and sends every byte
proves: [correctness]
status: full
---

**Model.** The application writes bytes at any times. The sender keeps $buf$, the bytes written but not sent, $sent$, the bytes sent, and $acked$, the bytes acknowledged, with $acked \le sent$. It runs TRY-SEND (lines L3 to L6) after each write (line L1) and after each ACK (line L2). A segment is *small* if it has fewer than MSS bytes. The receiver acknowledges the data that it has received, and every segment that is sent is acknowledged within a finite time. The receive window does not limit the sender.

**Claim 1 (no byte is lost or reordered).** The sender sends the bytes in the order in which they were written, each byte once. TRY-SEND takes bytes only from the front of $buf$ and moves them to $sent$; no other line changes $buf$ except line L1, which appends. $\square$

**Claim 2 (at most one small segment in flight).** At any time, at most one small segment is unacknowledged, and when one is, it is the last segment sent.

*Proof.* Line L5 sends a small segment only if $sent = acked$, that is, when no data is unacknowledged. After it, $sent > acked$ until an ACK covers this segment. While $sent > acked$, line L5 sends nothing, and line L4 sends only full segments. Since an ACK for a later byte also covers all earlier bytes, the next small segment can only be sent after an ACK that covers the previous small segment. $\square$

So if every round trip takes at least $\mathrm{RTT}_{\min}$, two small segments are sent at least $\mathrm{RTT}_{\min}$ apart, and in a time interval of length $T$ at most $\lfloor T/\mathrm{RTT}_{\min} \rfloor + 1$ small segments are sent. In the keystroke test, with a round-trip time of 120 ms and one key every 50 ms, the small segments are 120 ms apart, and 20 keys give 9 segments in place of 20.

**Claim 3 (no byte waits forever).** Every written byte is sent. A byte that is written at time $t$ is sent no later than the time when an ACK covers all the data that was in flight at time $t$, or at once if a full segment is ready.

*Proof.* If $buf \ge$ MSS, line L4 sends a full segment at once, so after TRY-SEND, $buf <$ MSS. If $0 < buf <$ MSS and the sender holds the bytes at line L6, then $sent > acked$. By the model, an ACK for all $sent$ bytes arrives in finite time. Line L2 then sets $acked = sent$, and TRY-SEND sends full segments and then the rest at line L5. So $buf = 0$ after that ACK. $\square$

**Claim 4 (the cost of a delayed ACK).** If the receiver acknowledges a single small segment only when a timer of $D$ expires, a byte can wait for $\mathrm{RTT} + D$.

*Proof.* Let the sender send a small segment at time 0 and get a write right after. By Claim 2, the new bytes are held. The receiver gets the segment at $d = \mathrm{RTT}/2$, waits $D$ for a second segment that will not come, and acknowledges at $d + D$. The ACK arrives at $\mathrm{RTT} + D$, and only then line L5 sends the new bytes. In the write-write-read test, with $d = 30$ ms and $D = 200$ ms, the second write arrives at $3d + D = 290$ ms, against 31 ms without Nagle and 90 ms without the delayed ACK. $\blacksquare$
