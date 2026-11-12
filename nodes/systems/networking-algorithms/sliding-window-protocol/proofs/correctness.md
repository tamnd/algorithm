---
title: A sliding window protocol with ws + wr at most M is correct over FIFO channels
proves: [correctness]
status: full
---

**Model.** The sender holds $M[0], \ldots, M[m-1]$. Packet $j$ is DATA$(j \bmod M, M[j])$, where $M \ge 2$ is the size of the sequence number space. Each channel is a queue that may lose a packet or replace it by two adjacent copies, but never reorders packets and never makes one up. The timer may expire at any time. The sender has a window of $w_s$ packets, the receiver a window of $w_r$ packets, with $w_s, w_r \ge 1$. We prove:

**Theorem.** If $w_s + w_r \le M$, the receiver delivers $M[0], M[1], \ldots$ in this order, each message at most once, and the sender moves its base only over packets that the receiver has delivered. If both channels are fair and the timer always expires, the sender finishes, and then all $m$ messages were delivered. If $w_s + w_r = M + 1$, some run delivers a wrong message.

We write $b$ and $n$ for the sender's base and next index, and $r$ for the receiver's next expected index. The sender sends only packets $j$ with $b \le j < n$, and $n \le b + w_s$ (line L2). The receiver sends ACK$(r \bmod M)$ (line L13). For the proof, each packet carries a ghost label: the index $j$ for a DATA packet, and the value $r$ at the time of sending for an ACK. Since $w_r \ge 1$, the hypothesis gives $w_s < M$. Lemmas 1 and 2 below are proved together, by induction over the steps of a run: each one uses the other only for earlier steps.

**Lemma 1 (the receiver).** Assume that the receiver has stored only packets with the right index so far. When a DATA packet with label $j$ reaches the receiver, $r - w_s \le j \le r + w_s - 1$.

*Proof.* The receiver advances $r$ past an index only after it has received a packet with that index, so $r \le n$ at all times. Let $t_0$ be the time when this copy of packet $j$ was sent, and $b_0, n_0$ the sender's values just after it. Then $b_0 \le j$, and $n_0 \le b_0 + w_s$. By FIFO, each packet that the receiver got before this one was sent no later than $t_0$, so it has a label below $n_0$. So $r \le n_0 \le b_0 + w_s \le j + w_s$, which is the first inequality. For the second, $j < n \le b + w_s$ at the time of arrival, and $b \le r$, because the sender sets $b$ only to the label of an ACK (see Lemma 2), which is a past value of $r$. So $j \le r + w_s - 1$. $\square$

Now take the receiver step of lines L10 and L11, with $s = j \bmod M$ and $\mathit{off} = (s - r) \bmod M$.

- If $r \le j \le r + w_r - 1$, then $0 \le j - r < w_r \le M$, so $\mathit{off} = j - r < w_r$, and line L11 stores $M[j]$ at index $r + \mathit{off} = j$. This is right.
- If $r + w_r \le j \le r + w_s - 1$, then $\mathit{off} = j - r$, with $w_r \le \mathit{off} < w_s < M$, so the packet is not stored.
- If $r - w_s \le j \le r - 1$, then $\mathit{off} = M - (r - j)$, with $M - w_s \le \mathit{off} \le M - 1$. Since $M - w_s \ge w_r$, the packet is not stored.

So the receiver stores each packet at its own index, by induction over its steps. Line L12 delivers the stored packets $r, r+1, \ldots$ in order, so the deliveries are $M[0], M[1], \ldots$, each once.

**Lemma 2 (the sender).** When an ACK with label $a$ reaches the sender, $b \le a \le n$.

*Proof.* $a$ is a value of $r$, and $r \le n$ at all times, so $a \le n$. The ACK channel is FIFO and $r$ never decreases, so the ACK labels arrive in non-decreasing order. The base starts at 0 and line L6 sets it only to the label of an earlier ACK, so $b \le a$. $\square$

Line L5 computes $k = (a \bmod M - b) \bmod M$. By Lemma 2, $0 \le a - b \le n - b \le w_s < M$, so $k = a - b$, and line L6 sets $b$ to $a$. The receiver had delivered all packets below $a$ when it sent this ACK, so the base moves only over delivered packets.

**Liveness.** Assume that the sender stays at some base $b \lt m$ forever. Then its timer expires again and again, and line L9 sends packet $b$ infinitely often. By fairness, it reaches the receiver infinitely often. Each receipt makes an ACK with label $r \ge b$, and after the first receipt $r \ge b + 1$, because packet $b$ is then stored. By fairness, the sender gets an ACK with label at least $b + 1$, and moves its base. This is a contradiction. When the sender finishes, $b = m$, and by Lemma 2 it got an ACK with label $m$, so all $m$ messages were delivered.

**Tightness.** Let $M = w_s + w_r - 1 \ge 2$. The sender sends packets $0, \ldots, w_s - 1$; all arrive, so $r = w_s$, and the receiver window is $w_s, \ldots, w_s + w_r - 1 = M$. All $w_s$ ACKs are lost. The timer expires, and the sender sends packet 0 again, with the number 0. The receiver computes $\mathit{off} = (0 - w_s) \bmod M = w_r - 1 < w_r$, and stores the old $M[0]$ at index $M$. When the gap closes, it delivers $M[0]$ in place of $M[M]$. If $w_r = 1$, then $M = w_s$, and the receiver delivers it at once. $\blacksquare$
