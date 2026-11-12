---
title: Selective repeat with a window of at most 2^(k-1) is correct over FIFO channels
proves: [correctness]
status: full
---

**Model.** Packet $j$ is DATA$(j \bmod M, M[j])$ with $M = 2^k$, and its acknowledgement is ACK$(j \bmod M)$. Each channel is a queue that may lose a packet or replace it by two adjacent copies, but never reorders packets and never makes one up. Timers may expire at any time. The sender keeps $base$, the smallest index without an ACK, and $next$, with $next \le base + w$ (line L1). The receiver keeps $r$, the smallest index that it has not received, and a buffer for the indices $r, \ldots, r + w - 1$. For the proof, each packet carries its index $j$ as a ghost label; an ACK carries the label of the DATA packet that it answers.

**Theorem.** If $2w \le M$, the receiver stores each packet at its own index and delivers $M[0], M[1], \ldots$ in this order, each message once, and the sender marks a packet as acknowledged only after the receiver has received it. With fair channels and timers that always expire, the sender finishes, and then all $m$ messages were delivered. If $2w > M$, some run delivers a wrong message.

*Proof.* We prove the claims below together, by induction over the steps of a run.

**Claim 1.** $base \le r \le base + w$. The sender marks index $j$ only on an ACK with label $j$ (Claim 3), which the receiver sends only after it received packet $j$. So all indices below $base$ were received, and $r \ge base$. The receiver can only receive packets that were sent, so $r \le next \le base + w$.

**Claim 2.** When a DATA packet with label $j$ reaches the receiver, $r - w \le j \le r + w - 1$. Let $base_0$ and $next_0$ be the sender's values just after this copy was sent. Then $base_0 \le j$ and $next_0 \le base_0 + w$. By FIFO, each packet that the receiver got earlier was sent no later than this copy, so its label is below $next_0$. The receiver moves $r$ past an index only after it received that index, so $r \le next_0 \le j + w$. Also $j < next \le base + w \le r + w$ by Claim 1.

The receiver computes $\mathit{off} = (j - r) \bmod M$ (line L9). The integers $r - w, \ldots, r + w - 1$ are $2w \le M$ consecutive integers, so their residues modulo $M$ are distinct. If $r \le j \le r + w - 1$, then $\mathit{off} = j - r < w$, and line L11 stores $M[j]$ at index $j$. If $r - w \le j \le r - 1$, then $\mathit{off} = M - (r - j) \ge M - w \ge w$, so line L10 rejects it, and line L13 sends ACK$(j \bmod M)$ for the old packet. So each stored packet has the right index, and line L12 delivers $M[r]$ and then increases $r$.

**Claim 3.** When an ACK with label $j$ reaches the sender, $base - w \le j < next$, and line L5 marks exactly packet $j$ if $j \ge base$, and nothing if $j < base$. The label $j$ is the index of a sent packet, so $j < next$. Let $t_a$ be the time when the receiver sent this ACK. By Claim 2 at that time, $j \ge r(t_a) - w$. By FIFO, the ACKs that reached the sender before this one were sent before $t_a$, and each of them answers a packet that the receiver had received by $t_a$. So all indices below the current $base$ were received before $t_a$, and $r(t_a) \ge base$. Hence $j \ge base - w$.

Line L4 computes $j' = base + ((j - base) \bmod M)$. If $base \le j < next$, then $0 \le j - base < w \le M$, so $j' = j$ and $j' < next$, and line L5 marks packet $j$. If $base - w \le j < base$, then $(j - base) \bmod M \ge M - w \ge w \ge next - base$, so $j' \ge next$ and line L5 does nothing. This proves the claim, and Claim 1 then holds after the step too.

**Liveness.** Assume that $base = b \lt m$ forever. The timer of packet $b$ expires again and again, and line L8 resends it each time, so by fairness the receiver gets it infinitely often. By Claim 1, $b \le r$. If $b \ge r$ at a receipt, then $b = r$ is in the window and is stored and acknowledged; if $b < r$, then $b \ge r - w$ by Claim 2, so line L13 acknowledges it. So ACK$(b \bmod M)$ is sent infinitely often, it reaches the sender by fairness, and by Claim 3 line L5 marks $b$. Then line L6 moves $base$, a contradiction. When $base = m$, every packet was received, so all $m$ messages were delivered.

**Tightness.** Let $w = M/2 + 1$. The sender sends packets $0, \ldots, w - 1$. All arrive, so $r = w$, and the receiver window is $w, \ldots, 2w - 1 = M + 1$, which contains the index $M$. All $w$ ACKs are lost. The timer of packet 0 expires, and the sender resends it with the number 0. The receiver computes $\mathit{off} = (0 - w) \bmod M = M - w = w - 2 < w$ and stores the old $M[0]$ at index $M$. When the gap before it closes, the receiver delivers $M[0]$ in place of $M[M]$. $\blacksquare$
