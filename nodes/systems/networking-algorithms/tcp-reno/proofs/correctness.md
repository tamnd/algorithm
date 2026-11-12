---
title: TCP Reno repairs one loss with one half of the window in flight, and its sawtooth gives the square-root law
proves: [correctness]
status: full
---

**The model.** Segments are numbered $0, \ldots, n-1$, and windows count segments. Each transmission either is lost or reaches the receiver $R/2$ after it is sent, in order. The receiver keeps every segment it gets and answers each arrival with the cumulative ACK $a$, the smallest segment number it does not have. Each ACK reaches the sender $R/2$ later. The sender runs lines L1 to L13 for each ACK. One retransmission timer runs while data is outstanding, restarts on each ACK of new data, and fires $\text{RTO} > 2R$ after its last start. A timeout runs lines L14 to L16 and then line L13. The caller says which transmissions are lost.

**Lemma 1 (invariants).** After each event: $0 \le \text{snd\_una} \le \text{snd\_nxt} \le n$, $\text{cwnd} \ge 1$, $\text{ssthresh} \ge 2$, and if $\text{snd\_una} < n$ then some segment is outstanding. The receiver hands the segments over in order, each one once.

*Proof.* The receiver acknowledges only segments that were sent, so line L9 keeps $\text{snd\_una} \le \text{snd\_nxt}$ (snd_nxt moves up to snd_una if a go-back left it below). Lines L5 and L14 give $\text{ssthresh} \ge 2$. Line L7 gives $\text{cwnd} \ge 5$, line L10 gives $\text{cwnd} = \text{ssthresh} \ge 2$, line L15 gives 1, and lines L2, L11 and L12 only add. Every event ends with line L13, which sends a segment when nothing is outstanding, $\text{snd\_una} < n$ and $\text{cwnd} \ge 1$. The receiver hands over segment $a$ only when it has $0, \ldots, a$, and then raises $a$. $\square$

**Theorem 1 (one loss).** Let the ACK $a = s$ arrive at time $T_0$ outside fast recovery, with $W = \text{snd\_nxt} - \text{snd\_una} = \text{cwnd} \ge 4$ just after line L13. Let segment $s$ be the only lost transmission, and let the sender have enough data. Then Reno repairs the loss with no timeout, the ACK of the retransmission arrives one round trip after line L6, and just after line L13 of that ACK, $\text{cwnd} = \text{ssthresh} = \lfloor W/2 \rfloor$ and $\lfloor W/2 \rfloor$ segments are in flight.

*Proof.* The $W - 1$ segments after $s$ were sent by $T_0$, arrive, and make $W - 1$ duplicate ACKs. The first two only count in line L3, and cwnd stays $W$, so line L13 sends nothing. The third arrives at $T_1 \le T_0 + R$. Line L5 sets $\text{ssthresh} = \max(\lfloor W/2 \rfloor, 2) = \lfloor W/2 \rfloor$, line L6 resends $s$, and line L7 sets $\text{cwnd} = \lfloor W/2 \rfloor + 3$. The other $W - 4$ duplicate ACKs each add 1 in line L2, so cwnd ends at $\lfloor W/2 \rfloor + W - 1$, and line L13 has sent $\lfloor W/2 \rfloor - 1$ new segments. The retransmission left before them, so it arrives first, and the receiver answers with $a = s + W$. This ACK reaches the sender at $T_1 + R \le T_0 + 2R < T_0 + \text{RTO}$, so no timeout fires before it. The new segments make new ACKs, not duplicates. Line L10 sets $\text{cwnd} = \lfloor W/2 \rfloor$, the flight is $\lfloor W/2 \rfloor - 1$, and line L13 sends one more. $\blacksquare$

**Theorem 2 (the sawtooth and the square-root law).** Consider the periodic model of Mathis, Semke, Mahdavi and Ott: the window grows by one segment per round trip from $w/2$ to $w$, with $w \ge 2$ even. In the round trip with window $w$ one segment is lost, and the next round trip starts with $w/2$. Then the loss rate is $p = 1/N$ with $N = \frac{3w}{4}\left(\frac{w}{2} + 1\right)$, the rate is $\frac{3w}{4}$ segments per round trip, and

$$\text{rate} \cdot \sqrt{p} = \sqrt{\frac{3}{2}} \sqrt{\frac{w}{w+2}} \quad\text{so}\quad \text{rate} \sim \sqrt{\frac{3}{2p}} \text{ segments per round trip as } p \to 0.$$

*Proof.* One cycle has the round trips with windows $w/2, w/2 + 1, \ldots, w$, which is $w/2 + 1$ round trips. It sends

$$N = \sum_{k = w/2}^{w} k = \left(\frac{w}{2} + 1\right) \cdot \frac{w/2 + w}{2} = \left(\frac{w}{2} + 1\right) \frac{3w}{4}$$

segments, by the sum of an arithmetic series, and loses one. So $p = 1/N$, and the rate is $N / (w/2 + 1) = 3w/4$. Then

$$\text{rate} \cdot \sqrt{p} = \frac{3w/4}{\sqrt{(3w/4)(w/2 + 1)}} = \sqrt{\frac{3w/4}{w/2 + 1}} = \sqrt{\frac{3w}{2w + 4}} = \sqrt{\frac{3}{2}} \sqrt{\frac{w}{w + 2}}.$$

As $p \to 0$, $N \to \infty$, so $w \to \infty$ and $\sqrt{w/(w+2)} \to 1$. $\blacksquare$

With segments of MSS bytes and a round trip of $T$ seconds, the rate is about $\frac{\text{MSS}}{T} \sqrt{3/(2p)}$ bytes per second. The sawtooth model has no timeouts and no slow start. With random losses, Mathis et al. get the same form with a different constant, and Padhye, Firoiu, Towsley and Kurose add the effect of timeouts.

**Theorem 3 (termination).** If only finitely many transmissions are lost, all $n$ segments get acknowledged.

*Proof.* Let $t^*$ be a time after the last lost transmission. By Lemma 1, while $\text{snd\_una} = u < n$ some segment is outstanding and the timer runs. If a copy of $u$ sent after $t^*$ is in flight, it arrives and the ACK rises above $u$. If not, either a new ACK comes, or the timer fires within $\text{RTO} \cdot 2^m$, where $m$ is the number of timeouts since the last new ACK, and lines L16 and L13 resend $u$. That copy arrives, and the ACK rises above $u$ one round trip later. So snd_una grows by at least 1 in each bounded interval and reaches $n$. $\blacksquare$
