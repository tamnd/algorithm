---
title: Stop-and-wait delivers each message exactly once and in order
proves: [correctness]
status: full
---

**Model.** The sender holds the messages $M[0], \ldots, M[m-1]$. Two channels connect it to the receiver: the data channel carries DATA packets, and the ACK channel carries ACK packets. A channel may lose a packet, deliver it more than once, delay it by any finite time, and deliver packets in any order. A corrupted packet is detected by a [checksum](/checksum/) and dropped, so it counts as a loss. A channel never makes up a packet: each packet that it delivers is a copy of a packet that was sent on it. The timer may expire at any time after it is started, also too early. The sequence numbers are the integers $0, 1, 2, \ldots$, with no bound.

We use $i$ for the sender's index and $r$ for the receiver's counter. The receiver delivers by line L8 only.

**Lemma 1.** In each reachable state:

1. each DATA$(s, d)$ that was ever sent has $s \le i$ and $d = M[s]$;
2. $i \le r \le i + 1$;
3. each ACK$(s)$ that was ever sent has $s < r$.

*Proof.* By induction on the steps of the protocol. At the start, $i = r = 0$ and no packet was sent, so the three parts hold. A loss, a copy or a delay of a packet does not change $i$, $r$ or the set of packets that were sent, so it keeps the three parts. The other steps are these.

- *Line L2 sends* DATA$(i, M[i])$. This packet has $s = i$ and $d = M[s]$, so part 1 holds.
- *Lines L7 to L9 receive* DATA$(s, d)$. The channel delivers only copies, so by part 1, $s \le i \le r$. If $s = r$, line L8 sets $r$ to $s + 1 = i + 1$ (because $s \le i \le r = s$ gives $s = i$), so part 2 holds after the step. If $s < r$, nothing changes $r$. In both cases $s < r$ after line L8, so the ACK$(s)$ of line L9 keeps part 3.
- *Lines L3 and L5 accept* ACK$(i)$. By part 3, $i < r$, so $i + 1 \le r$. With part 2, $r = i + 1$. The step sets $i$ to $i + 1 = r$, so part 2 still holds. Part 1 holds because $i$ grew. Part 3 does not depend on $i$.
- *An ACK$(j)$ with $j \ne i$, and a timeout* do not change $i$ or $r$. A timeout leads to line L2, which is the first case. $\square$

**Theorem (safety).** At each moment, the receiver has delivered exactly $M[0], M[1], \ldots, M[r-1]$, in this order.

*Proof.* The counter $r$ starts at 0, and only line L8 changes it, by adding 1. Line L8 delivers $d$ of a packet DATA$(r, d)$, and by part 1 of Lemma 1, $d = M[r]$. So the deliveries are $M[0], M[1], \ldots$ in order, and no index is delivered twice, because $r$ only grows. $\square$

**Theorem (completion).** When the sender stops, with $i = m$, the receiver has delivered all $m$ messages, and it never delivers more.

*Proof.* By part 2 of Lemma 1, $r \ge i = m$, so by the safety theorem, $M[0], \ldots, M[m-1]$ were delivered. A delivery needs a packet DATA$(s, d)$ with $s = r$. Line L2 runs only while $i \lt m$, so each DATA packet has $s \le m - 1$. So after $r = m$, no delivery happens. $\square$

**Theorem (liveness).** Assume that each channel is fair: a packet that is sent infinitely often is received infinitely often. Assume that the timer expires a finite time after it starts, and that the receiver answers each DATA packet. Then the sender reaches $i = m$.

*Proof.* Assume that the sender stays at some $i \lt m$ forever. Then it never accepts ACK$(i)$, so its timer expires again and again, and it sends DATA$(i, M[i])$ infinitely often. By fairness, the receiver receives DATA$(i, M[i])$ infinitely often. After the first receipt, $r \ge i + 1$, and each receipt sends ACK$(i)$ by line L9. So ACK$(i)$ is sent infinitely often, and by fairness the sender receives it, which is a contradiction. $\blacksquare$

**Why the numbers are needed.** Without the number in the packet, the receiver cannot tell a new message from a retransmission. If the first ACK is lost, the sender sends $M[0]$ again, and a receiver that delivers each DATA packet delivers $M[0]$ twice. The proof uses the number in part 1 and in the test $s = r$ of line L8.
