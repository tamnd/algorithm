---
title: TCP Tahoe delivers in order, ends under finite loss, and restarts slow start after each loss
proves: [correctness]
status: full
---

**The model.** Segments are numbered $0, \ldots, n-1$, and windows count segments. Each transmission either is lost or reaches the receiver $R/2$ after it is sent, in order. The receiver keeps every segment it gets and answers each arrival with the cumulative ACK $a$, the smallest segment number it does not have. Each ACK reaches the sender $R/2$ later. The sender runs lines L1 to L8 for each ACK. One retransmission timer runs while data is outstanding, restarts on each ACK of new data, and fires $\text{RTO} > 2R$ after its last start. A timeout runs LOSS (lines L9 to L11) and then line L8, and a repeated timeout of the same segment keeps ssthresh. The caller says which transmissions are lost.

**Lemma 1 (invariants).** After each event: $0 \le \text{snd\_una} \le \text{snd\_nxt} \le n$, $\text{cwnd} \ge 1$, $\text{ssthresh} \ge 2$, and if $\text{snd\_una} < n$ then some segment is outstanding.

*Proof.* The receiver acknowledges only segments that were sent, so line L5 keeps $\text{snd\_una} \le \text{snd\_nxt}$ (if a go-back left snd_nxt below the new snd_una, the sender moves snd_nxt up to it). Line L11 sets $\text{snd\_nxt} = \text{snd\_una}$, which keeps the order. Line L9 gives $\text{ssthresh} \ge 2$, line L10 gives $\text{cwnd} = 1$, and lines L6 and L7 only add. LOSS and each new ACK end with line L8, which sends at least one segment when $\text{cwnd} \ge 1$, nothing is outstanding and $\text{snd\_una} < n$. A duplicate ACK by definition comes while data is outstanding, and it removes nothing. $\square$

**Lemma 2 (in order).** The receiver hands segments $0, 1, 2, \ldots$ to the application in order, each one once, even when line L11 makes the sender resend segments that the receiver already has.

*Proof.* The receiver hands over segment $a$ only when it has all of $0, \ldots, a$, and then raises $a$. A copy of a segment below $a$, or of a segment it already keeps, changes nothing. $\square$

**Theorem 1 (one loss).** Let the ACK $a = s$ arrive at time $T_0$, and let $W = \text{snd\_nxt} - \text{snd\_una} = \text{cwnd} \ge 4$ just after line L8 of this ACK. Let segment $s$ be the only lost transmission, and let the sender have enough data. Then:

1. The third duplicate ACK arrives at a time $T_1 \le T_0 + R$. LOSS sets $\text{ssthresh} = \lfloor W/2 \rfloor$ and $\text{cwnd} = 1$, and line L8 resends $s$ only.
2. The ACK $s + W$ arrives at $T_1 + R$, and no timeout happens.
3. Let $h = \lfloor W/2 \rfloor$ and $j^* = \lceil \log_2 h \rceil$. Just after the ACKs that arrive at time $T_1 + jR$, the window is $2^j$ for $1 \le j < j^*$, and it is at least $h$ for $j = j^*$. So the window is back at ssthresh $j^*$ round trips after the fast retransmit.

*Proof.* (1) The $W$ segments in flight were all sent at or before $T_0$. The $W - 1$ segments after $s$ arrive and make duplicate ACKs. The first two only count in line L2. The third, made by segment $s + 3$, arrives at $T_1 \le T_0 + R$ and calls LOSS. The flight is $W$, so line L9 gives $\max(\lfloor W/2 \rfloor, 2) = \lfloor W/2 \rfloor$ since $W \ge 4$. Line L10 sets $\text{cwnd} = 1$, line L11 sets $\text{snd\_nxt} = s$, and line L8 sends segment $s$ and nothing else.

(2) The later duplicate ACKs only raise the counter in line L2. The retransmission of $s$ arrives, the receiver then has $s, \ldots, s + W - 1$, and its ACK $s + W$ reaches the sender at $T_1 + R \le T_0 + 2R < T_0 + \text{RTO}$, so the timer has not fired. Line L5 sets $\text{snd\_una} = s + W$, and snd_nxt moves up to it, so no segment of the old window is sent again.

(3) At $T_1 + R$, line L6 raises cwnd from 1 to 2, and line L8 sends two new segments. By induction on $j$: if the window is $c = 2^j$ after the ACKs at $T_1 + jR$ and $2^{j+1} \le h$, then the $c$ segments sent make $c$ ACKs at $T_1 + (j+1)R$. Before each of them the window is at most $2^{j+1} - 1 < h$, so each one is in slow start and adds 1, and the window becomes $2^{j+1}$. For $j < j^*$ we have $2^j < h$, so the induction reaches every $j < j^*$. The round that starts with $2^{j^* - 1} < h$ reaches ssthresh after $h - 2^{j^*-1} \le 2^{j^*-1}$ of its ACKs, and the other ACKs only add, so at $T_1 + j^* R$ the window is at least $h$. $\blacksquare$

In the same situation, [fast recovery](/fast-retransmit-fast-recovery/) keeps $h$ segments in flight at $T_1 + R$. Tahoe has 2 at that time and needs $\lceil \log_2 h \rceil - 1$ more round trips to get back to $h$. This is the cost that Reno removes.

**Theorem 2 (termination).** If only finitely many transmissions are lost, all $n$ segments get acknowledged.

*Proof.* Let $t^*$ be a time after the last lost transmission. By Lemma 1, while $\text{snd\_una} = u < n$ some segment is outstanding, so the timer runs. If a copy of $u$ sent after $t^*$ is in flight, it arrives and the ACK rises above $u$. If not, either a new ACK comes, or the timer fires within $\text{RTO} \cdot 2^m$, where $m$ is the number of timeouts since the last new ACK. The timeout resends $u$ (line L11 and line L8), that copy arrives, and the ACK rises above $u$ one round trip later. So snd_una grows by at least 1 in each bounded interval, and it is at most $n$. $\blacksquare$
