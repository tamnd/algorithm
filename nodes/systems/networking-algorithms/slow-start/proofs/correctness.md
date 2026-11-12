---
title: Slow start doubles the window per round trip, and congestion avoidance adds at most one segment
proves: [correctness]
status: full
---

**The model.** One sender has the window cwnd and the threshold ssthresh, both in bytes, and the segment size $\text{SMSS} > 0$. An ACK that acknowledges $N > 0$ new bytes runs lines L2 to L5 once. A timeout runs lines L6 and L7. In the *round model*, a round trip starts with the window $W$. The sender sends $k = \lfloor W / \text{SMSS} \rfloor$ full segments, and the receiver sends one ACK for each segment, so lines L2 to L5 run $k$ times with $N = \text{SMSS}$. There is no loss inside a round.

We assume $\text{IW} \ge \text{SMSS}$. Then $\text{cwnd} \ge \text{SMSS}$ at all times: line L1 starts at IW, lines L3 and L5 only add, and line L7 sets SMSS.

**Lemma 1 (one ACK).** An ACK raises cwnd by at least 1 byte and by at most SMSS bytes.

*Proof.* Line L3 adds $\min(N, \text{SMSS})$, which is at least 1 because $N \ge 1$ is an integer, and at most SMSS. Line L5 adds $\max(1, \lfloor \text{SMSS}^2 / \text{cwnd} \rfloor)$. This is at least 1, and since $\text{cwnd} \ge \text{SMSS}$ it is at most $\max(1, \text{SMSS}) = \text{SMSS}$. $\square$

**Lemma 2 (slow start doubles).** Let a round start with $W = k \cdot \text{SMSS}$ for an integer $k \ge 1$, and let $(2k - 1)\,\text{SMSS} < \text{ssthresh}$. Then the round ends with $\text{cwnd} = 2W$.

*Proof.* Before the $j$-th ACK of the round, for $j = 1, \ldots, k$, the window is $(k + j - 1)\,\text{SMSS}$. This is at most $(2k - 1)\,\text{SMSS} < \text{ssthresh}$, so line L2 chooses line L3, which adds $\min(\text{SMSS}, \text{SMSS}) = \text{SMSS}$. By induction on $j$, after the $k$ ACKs the window is $(k + k)\,\text{SMSS} = 2W$. $\square$

**Theorem 1 (rounds to reach a window).** Let $\text{IW} = i \cdot \text{SMSS}$ with an integer $i \ge 1$, let ssthresh be at least $2T$, and let $T \ge \text{IW}$ be a target. In the round model, the window first reaches at least $T$ at the start of round $r = \lceil \log_2 (T / \text{IW}) \rceil$, where the first round is round 0.

*Proof.* By Lemma 2 and induction, the window at the start of round $j$ is $\text{IW} \cdot 2^j$, as long as the last window $\text{IW} \cdot 2^{j-1}$ satisfies $(2 \cdot \text{IW}\, 2^{j-1} / \text{SMSS} - 1)\,\text{SMSS} < \text{ssthresh}$, that is $\text{IW}\, 2^j - \text{SMSS} < \text{ssthresh}$. For all $j \le r$ we have $\text{IW}\, 2^{j-1} < T$, so $\text{IW}\, 2^j < 2T \le \text{ssthresh}$, and the condition holds. The window at the start of round $j$ is at least $T$ exactly when $2^j \ge T/\text{IW}$, and the smallest such $j$ is $r$. $\blacksquare$

**Theorem 2 (congestion avoidance).** Let a round start with $W \ge \text{ssthresh}$ and $\text{SMSS} \le W \le \text{SMSS}^2$. Then the window grows in the round by at least 1 byte and by at most SMSS bytes.

*Proof.* The window does not decrease inside a round, so line L2 chooses line L5 for each of the $k = \lfloor W/\text{SMSS} \rfloor \ge 1$ ACKs. The lower bound follows from Lemma 1. Let $W_j \ge W$ be the window before the $j$-th ACK. If $\lfloor \text{SMSS}^2 / W_j \rfloor \ge 1$, the step is $\lfloor \text{SMSS}^2 / W_j \rfloor \le \text{SMSS}^2 / W$. If it is 0, then $W_j > \text{SMSS}^2 \ge W$ and the step is $1 \le \text{SMSS}^2 / W$. So each step is at most $\text{SMSS}^2 / W$, and the round adds at most $k\, \text{SMSS}^2 / W \le (W / \text{SMSS})\, \text{SMSS}^2 / W = \text{SMSS}$. $\blacksquare$

The condition $W \le \text{SMSS}^2$ is needed. Above it, each of the $k$ ACKs adds the rounded-up 1 byte, so a round adds $k > \text{SMSS}$ bytes. For $\text{SMSS} = 1460$ the condition is $W \le 2{,}131{,}600$ bytes.

**Theorem 3 (timeout).** After lines L6 and L7, $\text{cwnd} = \text{SMSS}$ and $\text{ssthresh} \ge 2\,\text{SMSS}$, so the sender is in slow start, and Lemma 2 applies until the window passes about one half of the data that was in flight.

*Proof.* Line L7 sets $\text{cwnd} = \text{SMSS}$, and line L6 sets $\text{ssthresh} = \max(\lfloor \text{FlightSize}/2 \rfloor, 2\,\text{SMSS}) \ge 2\,\text{SMSS} > \text{cwnd}$. So line L2 chooses line L3 on the next ACK. $\blacksquare$
