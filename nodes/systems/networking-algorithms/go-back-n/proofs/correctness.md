---
title: Go-Back-N with N at most 2^k - 1 is correct over FIFO channels
proves: [correctness]
status: full
---

**Model.** Packet $j$ is DATA$(j \bmod M, M[j])$ with $M = 2^k$. Each channel is a queue that may lose a packet or replace it by two adjacent copies, but never reorders packets and never makes one up. The timer may expire at any time. The sender keeps $base \le next \le base + N$ (line L2) and sends only packets $j$ with $base \le j < next$. The receiver keeps $r$, the number of messages that it has delivered, and sends ACK$(r \bmod M)$ (line L16). For the proof, each DATA packet carries its index $j$ as a ghost label, and each ACK carries the value of $r$ when it was sent.

**Theorem.** If $N \le M - 1$, the receiver delivers $M[0], M[1], \ldots$ in this order, each message at most once, and the sender moves $base$ only over delivered packets. With fair channels and a timer that always expires, the sender finishes, and then all $m$ messages were delivered. If $N = M$, some run delivers a wrong message.

*Proof.* We prove two claims together, by induction over the steps of a run.

**Claim 1.** When an ACK with label $a$ reaches the sender, $base \le a \le next$. The receiver delivers only packets that it has received, and the sender has sent only packets below $next$, so $r \le next$ and $a \le next$. The ACK channel keeps order and $r$ never decreases, so the labels arrive in non-decreasing order. By Claim 1 for the earlier ACKs, line L8 has set $base$ only to labels of earlier ACKs, so $base \le a$.

So $0 \le a - base \le next - base \le N < M$, and line L7 computes $c = (a \bmod M - base) \bmod M = a - base$. Line L8 sets $base$ to $a$ when $c \ge 1$. All packets below $a$ were delivered when the ACK was sent.

**Claim 2.** When a DATA packet with label $j$ reaches the receiver, $r - N \le j \le r + N - 1$. Let $base_0$ and $next_0$ be the sender's values just after this copy was sent. Then $base_0 \le j$ and $next_0 \le base_0 + N$. By FIFO, each packet that the receiver got before it was sent no later, so its label is below $next_0$, and $r \le next_0 \le j + N$. Also $j < next \le base + N \le r + N$, since $base$ is a past value of $r$ by Claim 1.

Line L14 accepts the packet if $j \bmod M = r \bmod M$. By Claim 2, $j - r$ lies in $[-N, N-1]$. The only multiple of $M$ in this range is 0, because $N \le M - 1$ gives $-M < -N$ and $N - 1 < M$. So line L14 accepts exactly the packet $j = r$, and line L15 delivers $M[r]$. This proves safety.

**Liveness.** Assume that $base = b \lt m$ forever. The timer expires again and again, and line L13 sends packet $b$ each time, so by fairness the receiver gets packet $b$. At that moment $r \ge b$ by Claim 1, and if $r = b$, it delivers it, so afterwards $r \ge b + 1$. Each later receipt of packet $b$, which happens infinitely often, sends an ACK with label at least $b + 1$. By fairness one of them arrives, and line L8 moves $base$, which is a contradiction. When $base = m$, an ACK with label $m$ arrived, so the receiver had delivered all $m$ messages.

**Tightness.** Let $N = M$. The sender sends packets $0, \ldots, M - 1$. They all arrive, so $r = M$, and all $M$ ACKs are lost. On the timeout, line L13 sends packet 0 again, with number 0. Since $r \bmod M = 0$, line L14 accepts it, and the receiver delivers the old $M[0]$ as message $M$. The sender also cannot read ACK$(0)$: it can mean $r = base$ (nothing new) or $r = base + M$ (all $M$ packets). $\blacksquare$
